from __future__ import annotations

import hashlib
import http.server
from html.parser import HTMLParser
from pathlib import Path
import threading
import urllib.request
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "assets" / "trotec-ttk-165-eco-betriebsanleitung-de.pdf"
EXPECTED_MANUAL_SHA256 = "e35f81105e080731d623b8b29bf4654251f41c3455819fd86d63cf6440cc915e"
BASE_PATH = "/wertobjekt-geraetepass/"
FORBIDDEN = (
    "192.168.",
    "/srv/wertobjekt",
    "iban",
    "steuerkennung",
)
LEGAL_PAGES = {"impressum/index.html", "datenschutz/index.html"}


class LinkCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        key = "href" if tag in {"a", "link"} else "src" if tag in {"img", "script"} else None
        if key and values.get(key):
            self.links.append(values[key] or "")


def resolve_local(html_file: Path, link: str) -> Path | None:
    parsed = urlsplit(link)
    if parsed.scheme or parsed.netloc or link.startswith(("#", "mailto:", "tel:")):
        return None
    if parsed.path.startswith(BASE_PATH):
        target = (ROOT / parsed.path.removeprefix(BASE_PATH)).resolve()
    elif parsed.path.startswith("/"):
        raise ValueError(f"Link außerhalb des GitHub-Pages-Basispfads: {link}")
    else:
        target = (html_file.parent / parsed.path).resolve()
    if not target.is_relative_to(ROOT):
        raise ValueError(f"Link außerhalb des Website-Verzeichnisses: {link}")
    if target.is_dir() or parsed.path.endswith("/"):
        target /= "index.html"
    return target


errors: list[str] = []
html_files = sorted(ROOT.rglob("*.html"))
if not html_files:
    errors.append("Keine HTML-Dateien gefunden.")

for html_file in html_files:
    text = html_file.read_text(encoding="utf-8")
    lower = text.lower()
    relative = html_file.relative_to(ROOT).as_posix()
    for forbidden in FORBIDDEN:
        if forbidden in lower:
            errors.append(f"Verbotener interner Inhalt in {html_file.relative_to(ROOT)}: {forbidden}")
    # Only the owner's explicitly approved public contact details belong in legal pages.
    if relative not in LEGAL_PAGES and ("mailto:" in lower or "<address" in lower):
        errors.append(f"Kontaktdaten außerhalb der Rechtstexte: {relative}")
    if any(token in lower for token in ("<script", "<iframe", "<form", "onload=", "onclick=")):
        errors.append(f"Nicht-statischer Inhalt: {relative}")
    if '<footer>' not in lower or f'href="{BASE_PATH}impressum/"' not in text or f'href="{BASE_PATH}datenschutz/"' not in text:
        errors.append(f"Rechtliche Navigation fehlt: {relative}")
    parser = LinkCollector()
    parser.feed(text)
    for link in parser.links:
        target = resolve_local(html_file, link)
        if target is not None and not target.exists():
            errors.append(f"Defekter Link in {html_file.relative_to(ROOT)}: {link}")

model_codes = ("m0001", "m0002", "m0003", "m0004", "m0006", "m0007", "m0008")
index_text = (ROOT / "index.html").read_text(encoding="utf-8").lower()
for model_code in model_codes:
    model_page = ROOT / "models" / model_code / "index.html"
    if not model_page.exists():
        errors.append(f"Stabile Modellseite models/{model_code}/ fehlt.")
        continue
    page_text = model_page.read_text(encoding="utf-8").lower()
    if "whatsapp" in page_text:
        errors.append(f"Unbestätigter WhatsApp-Kontakt ist auf {model_code} sichtbar.")
    if f'href="models/{model_code}/"' not in index_text:
        errors.append(f"Modellseite {model_code} fehlt auf der Ersatz-Geräteliste.")
    if f"modellkennung {model_code}" not in page_text:
        errors.append(f"Lesbare Modellkennung fehlt auf {model_code}.")

if not MANUAL.exists():
    errors.append("Hersteller-PDF fehlt.")
else:
    digest = hashlib.sha256(MANUAL.read_bytes()).hexdigest()
    if digest != EXPECTED_MANUAL_SHA256:
        errors.append(f"Hersteller-PDF hat unerwartete SHA-256: {digest}")

if errors:
    raise SystemExit("\n".join(errors))

print(f"OK: {len(html_files)} HTML-Dateien, alle lokalen Links gültig.")
print(f"OK: Hersteller-PDF SHA-256 {EXPECTED_MANUAL_SHA256}.")
print("OK: Keine internen Server-, Adress-, Steuer- oder Bankangaben gefunden.")


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        pass


handler = lambda *args, **kwargs: QuietHandler(*args, directory=str(ROOT), **kwargs)
server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()
try:
    requests = [
        ("/", "text/html"),
        ("/assets/styles.css", "text/css"),
        ("/assets/trotec-ttk-165-eco-betriebsanleitung-de.pdf", "application/pdf"),
    ] + [(f"/models/{model_code}/", "text/html") for model_code in model_codes]
    for request_path, expected_type in requests:
        with urllib.request.urlopen(f"http://127.0.0.1:{server.server_port}{request_path}") as response:
            payload = response.read()
            if response.status != 200:
                errors.append(f"HTTP {response.status} für {request_path}")
            if expected_type not in response.headers.get_content_type():
                errors.append(f"Unerwarteter Content-Type für {request_path}: {response.headers.get_content_type()}")
            if not payload:
                errors.append(f"Leere HTTP-Antwort für {request_path}")
finally:
    server.shutdown()
    server.server_close()
    thread.join(timeout=2)

if errors:
    raise SystemExit("\n".join(errors))

print("OK: Startseite, 7 freigegebene Modellseiten, CSS und M0001-Hersteller-PDF über lokalen HTTP-Server erreichbar.")
print("OK: Ohne bestätigte WhatsApp-Nummer ist kein WhatsApp-Kontakt sichtbar.")

electrical = "Unsere Mietgeräte werden entsprechend den geltenden Vorschriften und festgelegten Prüffristen auf ihre elektrische Sicherheit geprüft. Die Prüfungen werden für jedes Gerät einzeln dokumentiert."
if electrical not in (ROOT / "models" / "m0001" / "index.html").read_text(encoding="utf-8"):
    raise SystemExit("Allgemeiner Hinweis zur elektrischen Sicherheit fehlt.")
print("OK: Rechtliche Navigation und allgemeiner Hinweis zur elektrischen Sicherheit vorhanden.")

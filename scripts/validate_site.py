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
FORBIDDEN = (
    "192.168.",
    "/srv/wertobjekt",
    "erlenweg 17",
    "stefan.win@",
    "iban",
    "steuerkennung",
)


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
    target = (html_file.parent / parsed.path).resolve()
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
    for forbidden in FORBIDDEN:
        if forbidden in lower:
            errors.append(f"Verbotener interner Inhalt in {html_file.relative_to(ROOT)}: {forbidden}")
    parser = LinkCollector()
    parser.feed(text)
    for link in parser.links:
        target = resolve_local(html_file, link)
        if target is not None and not target.exists():
            errors.append(f"Defekter Link in {html_file.relative_to(ROOT)}: {link}")

model_page = ROOT / "models" / "m0001" / "index.html"
if not model_page.exists():
    errors.append("Stabile Modellseite models/m0001/ fehlt.")
elif "whatsapp" in model_page.read_text(encoding="utf-8").lower():
    errors.append("Unbestätigter WhatsApp-Kontakt ist auf der Modellseite sichtbar.")

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
    for request_path, expected_type in (
        ("/", "text/html"),
        ("/models/m0001/", "text/html"),
        ("/assets/styles.css", "text/css"),
        ("/assets/trotec-ttk-165-eco-betriebsanleitung-de.pdf", "application/pdf"),
    ):
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

print("OK: Startseite, Modellseite, CSS und Hersteller-PDF über lokalen HTTP-Server erreichbar.")
print("OK: Ohne bestätigte Geschäftsnummer ist kein WhatsApp-Kontakt sichtbar.")

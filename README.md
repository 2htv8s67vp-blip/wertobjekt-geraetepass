# WertObjekt GBS - Kunden-Gerätepass

Rein statische, von der internen GBS-Anwendung getrennte Gerätehilfe für GitHub Pages.

## Architektur

- keine Datenbank
- kein Backend
- keine Verbindung zur internen GBS-App
- ein stabiler Pfad je Modellkennung: `models/<kennung>/`
- ausschließlich freigegebene öffentliche Modellinformationen

## Veröffentlichte Gerätepass-Struktur

- Modellkennung: `M0001`
- Hersteller / Modell: Trotec TTK 165 ECO
- Pfad: `models/m0001/`
- Hersteller-PDF: `assets/trotec-ttk-165-eco-betriebsanleitung-de.pdf`

Für die Veröffentlichung zusätzlich vorbereitet und geprüft:

- `M0002` Güde GS 1103 PI
- `M0003` Trotec TCH 21 E / TCH 23 E
- `M0004` Zipper ZI-BAT60
- `M0006` Trotec TDS 20 R
- `M0007` Fuxtec FX-TP11100
- `M0008` Kärcher SP 2 Flat

Die Entwürfe `M0005` Kärcher NT 30/1 und `M0009` Pro Breeze PB-08 bleiben lokal zurückgehalten, bis ihre exakte Typenschildvariante bestätigt ist.

## Vor Veröffentlichung offen

- GitHub-Zielkonto und öffentliches Repository bestätigen
- GitHub Pages auf Branch `main`, Verzeichnis `/ (root)` aktivieren
- öffentliche HTTPS-Adresse prüfen
- erst danach die bestätigte Basis-URL in GBS eintragen und den Kunden-QR drucken

Ein WhatsApp-Kontakt wird erst nach ausdrücklicher Bestätigung einer öffentlichen Geschäftsnummer ergänzt. Bis dahin enthält die veröffentlichbare Modellseite keinen Kontaktbereich.

Die Website enthält bewusst keine interne IP-Adresse, keine Kundendaten, keine Preise, keine Projektinformationen und keine Verbindung zum internen Server.

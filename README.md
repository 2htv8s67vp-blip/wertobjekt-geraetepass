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
- `M0005` Kärcher NT 30/1 Ap L (Artikelnummer 1.148-221.0)
- `M0006` Trotec TDS 20 R
- `M0007` Fuxtec FX-TP11100
- `M0008` Kärcher SP 2 Flat
- `M0009` Pro Breeze PB-08 (20-Liter-Luftentfeuchter)

M0005 und M0009 sind anhand der bestätigten Typenschilder und modellbezogener Herstellerquellen zur Veröffentlichung vorbereitet. Die Seiten enthalten keine Serien-, Chargen- oder Inventarnummern. Herstellerunterlagen werden verlinkt und nicht in dieses Repository kopiert.

## Herstellerquellen M0005 und M0009

- Kärcher NT 30/1 Ap L, Artikelnummer 1.148-221.0: <https://www.kaercher.com/at/de/professional/produkte/nt-30-1-ap-l-p11482210>
- Kärcher Originalbetriebsanleitung: <https://dp6jru56judg7.cloudfront.net/BTA/000/BTA-5758316-000-01.pdf>
- Kärcher Sicherheitshinweise: <https://dp6jru56judg7.cloudfront.net/BTA/000/BTA-1000179-000-16.pdf>
- Pro Breeze PB-08 Modell-Support: <https://support.probreeze.com/de-DE/articles/pb-08---20l-luftentfeuchter-mit-waschetrocknungsmodus-140670>
- Pro Breeze PB-08 Kurzanleitung: <https://attachments.gorgias.help/0eMnwxKBgKK79bDN/hc/RdOkb7opQBxVXGNr/2024052913-61b3a2b2-bf7a-4ac1-9d4b-2e378fd3d02d-pb-08_quick_start_guide_%28uk%29_final_feb_24_v1-b0da7575-cd58-4a98-9aad-59d498719076.pdf>
- Pro Breeze Pflegehinweise: <https://support.probreeze.com/en-US/how-to-take-care-of-your-dehumidifier-2898799>

Die aktuelle PB-D-08-Produktseite beschreibt eine abweichende neuere SKU. Variantenabhängige Werte daraus wurden nicht auf M0009 übertragen.

## Vor Veröffentlichung offen

- GitHub-Zielkonto und öffentliches Repository bestätigen
- GitHub Pages auf Branch `main`, Verzeichnis `/ (root)` aktivieren
- öffentliche HTTPS-Adresse prüfen
- erst danach die bestätigte Basis-URL in GBS eintragen und den Kunden-QR drucken

Ein WhatsApp-Kontakt wird erst nach ausdrücklicher Bestätigung einer öffentlichen Geschäftsnummer ergänzt. Bis dahin enthält die veröffentlichbare Modellseite keinen Kontaktbereich.

Die Website enthält bewusst keine interne IP-Adresse, keine Kundendaten, keine Preise, keine Projektinformationen und keine Verbindung zum internen Server.

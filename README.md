# Zeit der Wunder – Webseite zum Adventskalender der Prinzenbaude

Webseite für den gedruckten „Lies mich!“-Adventskalender der
Prinz-Friedrich-August-Baude in Sohland an der Spree. Die QR-Codes hinter den
Kalendertürchen führen zu den 24 Kapiteln der Geschichte „Zeit der Wunder“
von Daniela Tetzlaff.

Statische Website, kein Build-Schritt, keine Cookies, keine externen Dienste.

## Seiten

| Datei | Inhalt |
|---|---|
| `/einleitung` | Begrüßung – Ziel des QR-Codes auf der Kalender-Rückseite (auch `/`) |
| `/tuer-01` … `/tuer-24` | Ein Kapitel – Ziel der QR-Codes in den Türchen |
| `impressum.html`, `datenschutz.html` | Pflichtangaben – **Platzhalter `[…]` noch ausfüllen** |

Die Adressen entsprechen den gedruckten QR-Codes (`https://adventsbaude.de/tuer-01` usw.).
Die Ordner `einleitung/` und `tuer-XX/` sind Kopien von `index.html` bzw. `kapitel.html`
und werden mit `python3 werkzeuge/seiten-erzeugen.py` neu erzeugt. Die Seite muss im
Wurzelverzeichnis der Domain liegen (alle Pfade sind absolut).

## Freischaltung

- November: alle Kapitel noch verschlossen
- Dezember: Kapitel *n* ab dem *n*-ten Dezember
- 25. Dezember bis Ende Oktober: die ganze Geschichte ist lesbar

Regel in `gemeinsam.js`. Testen: `?datum=2026-12-05` simuliert ein Datum,
`?alle` schaltet alles frei.

## Inhalte

- Geschichte: `geschichte.js` (übernommen aus `Zeit_der_Wunder_Daniela_Tetzlaff_final-1.docx`;
  kursive Zeilen im Dokument = Reime)
- Hörbuch: MP3 nach `audio/` legen und im Kapitel `audio: "audio/kapitel-01.mp3"` eintragen
- Kalenderbild: `bilder/kalender.jpg`

## Lokal ansehen

```bash
python3 -m http.server 8000   # → http://localhost:8000
```

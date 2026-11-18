# Zeit der Wunder – Webseite zum Adventskalender der Prinzenbaude

Webseite für den gedruckten „Lies mich!“-Adventskalender der
Prinz-Friedrich-August-Baude in Sohland an der Spree. Die QR-Codes hinter den
Kalendertürchen führen zu den 24 Kapiteln der Geschichte „Zeit der Wunder“
von Daniela Tetzlaff.

Statische Website, kein Build-Schritt, keine Cookies, keine externen Dienste.

## Seiten

| Datei | Inhalt |
|---|---|
| `index.html` | Begrüßung (QR-Code auf der Kalender-Rückseite), Kalenderbild, Übersicht der 24 Kapitel |
| `kapitel.html?nr=1` … `?nr=24` | Ein Kapitel – Ziel der QR-Codes in den Türchen |
| `impressum.html`, `datenschutz.html` | Pflichtangaben – **Platzhalter `[…]` noch ausfüllen** |

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

# Adventskalender der Prinz-Friedrich-August-Baude

Digitaler Adventskalender nach dem Vorbild des gedruckten Baudenkalenders:

- **Ein Gesamtbild mit 24 Türchen.** Hinter jedem Türchen liegt ein Stück eines
  zweiten, gezeichneten Bildes – mit jedem geöffneten Türchen verändert sich das
  Gesamtbild ein Stück weiter.
- **Hinter jedem Türchen ein Kapitel** der Geschichte vom kleinen Baudentroll im
  Brunnen, zum Lesen und (optional) als Hörbuch.
- Türchen und Kapitel lassen sich erst ab ihrem Tag im Dezember öffnen.
- Jedes Kapitel hat eine eigene Adresse (`kapitel.html?nr=5`) – dorthin können
  QR-Codes auf einem gedruckten Kalender zeigen.

Statische Website ohne Build-Schritt und ohne Abhängigkeiten.

## Starten

```bash
python3 -m http.server 8000
# → http://localhost:8000
```

Testen: `?datum=2026-12-14` simuliert ein Datum, `?alle` schaltet alles frei
(z. B. `index.html?datum=2026-12-24`).

## Eigene Inhalte einsetzen

| Was | Wo |
|---|---|
| Bild vor dem Öffnen | `bilder/vorher.*` (Pfad in `daten.js`) |
| Gezeichnetes Bild hinter den Türchen | `bilder/nachher.*` – **exakt gleich groß** wie das Vorher-Bild |
| Bildgröße, Titel | `daten.js` |
| Lage der 24 Türchen | `daten.js` → `tueren` (Prozent: `x`, `y` = linke obere Ecke, `b` = Breite, `h` = Höhe) |
| Kapiteltexte, Autorin | `geschichte.js` |
| Hörbuch | MP3s nach `audio/`, Pfad je Kapitel in `geschichte.js` (`audio: "audio/kapitel-01.mp3"`) |

Das Nachher-Bild wird nur innerhalb der Türchen sichtbar. Alles, was sich
verändern soll, muss also innerhalb der Türchenflächen liegen; außerhalb sollten
beide Bilder identisch sein.

Die Bilder in `bilder/` sind Platzhalter und werden von
`werkzeuge/platzhalter-bilder.py` erzeugt.

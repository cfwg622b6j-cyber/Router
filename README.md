# Digitaler Adventskalender

Ein statischer Adventskalender im Browser – 24 Türchen, kein Build-Schritt, keine Abhängigkeiten.

## Starten

`index.html` im Browser öffnen oder lokal einen Server starten:

```bash
python3 -m http.server 8000
# → http://localhost:8000
```

## Funktionen

- 24 Türchen in fester, gemischter Anordnung mit Aufklapp-Animation
- Türchen lassen sich erst ab ihrem Tag im Dezember öffnen; das heutige leuchtet
- Geöffnete Türchen werden im Browser gespeichert (`localStorage`)
- Countdown bis zum 1. Dezember, Schneefall, mobiltauglich

## Inhalte anpassen

In `inhalte.js` hat jedes Türchen einen Eintrag:

```js
{ titel: "Nikolaus", emoji: "🎅", text: "…", bild: "bilder/6.jpg", link: { url: "https://…", text: "Mehr" } }
```

Nur `titel` ist Pflicht.

## Testen

- `index.html?datum=2026-12-10` – simuliert ein Datum
- `index.html?alle` – alle Türchen freigeschaltet

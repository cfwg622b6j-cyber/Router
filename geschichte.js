// Die Geschichte in 24 Kapiteln.
// text:  Liste von Absätzen
// audio: Pfad zur Hörbuch-Datei (z. B. "audio/kapitel-01.mp3") oder null
window.GESCHICHTE = {
  titel: "Die Geschichte vom Baudentroll",
  autorin: "[Name der Autorin]",
  sprecher: null, // z. B. "gelesen von …"
  kapitel: Array.from({ length: 24 }, (_, i) => ({
    titel: `Kapitel ${i + 1}`,
    text: [
      `Platzhalter: Hier steht der Text von Kapitel ${i + 1} der Geschichte vom kleinen Baudentroll, der im Brunnen wohnt und Wünsche erfüllt.`,
      "Jeder Eintrag in dieser Liste wird ein eigener Absatz."
    ],
    audio: null
  }))
};

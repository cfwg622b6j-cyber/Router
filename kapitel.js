(function () {
  "use strict";
  const G = window.GESCHICHTE, A = window.ADVENT;
  const ausPfad = location.pathname.match(/tuer-(\d+)/);
  const nr = parseInt(ausPfad ? ausPfad[1] : new URLSearchParams(location.search).get("nr"), 10);
  const inhalt = document.getElementById("kapitel-inhalt");
  const titel = document.getElementById("kapitel-titel");
  const absatz = (t) => { const p = document.createElement("p"); p.textContent = t; inhalt.append(p); };
  document.getElementById("zur-start").href = A.link("/einleitung");

  if (!(nr >= 1 && nr <= 24)) {
    titel.textContent = "Dieses Kapitel gibt es nicht.";
    return;
  }
  document.getElementById("kapitel-kicker").textContent = `Kapitel ${nr} von 24`;

  if (!A.istFrei(nr)) {
    titel.textContent = "Noch ein wenig Geduld!";
    absatz(`Dieses Kapitel lässt sich ab dem ${A.freiAb(nr)} lesen. Bis dahin hütet der Troll es gut in seiner Höhle unter dem Brunnen.`);
    return;
  }

  const kap = G.kapitel[nr - 1];
  document.title = `${kap.titel} – Zeit der Wunder`;
  titel.textContent = kap.titel;

  if (kap.audio) {
    const fig = document.createElement("figure");
    fig.className = "hoerbuch";
    fig.innerHTML = "<figcaption>Hör mich! – Kapitel als Hörbuch</figcaption>";
    const audio = document.createElement("audio");
    audio.controls = true; audio.preload = "none"; audio.src = kap.audio;
    fig.append(audio); inhalt.append(fig);
  }
  for (const b of kap.bloecke) {
    if (typeof b === "string") { absatz(b); continue; }
    const vers = document.createElement("p");
    vers.className = "vers";
    b.vers.forEach((z) => { const zeile = document.createElement("span"); zeile.textContent = z; vers.append(zeile); });
    inhalt.append(vers);
  }

  const zurueck = document.getElementById("zurueck"), weiter = document.getElementById("weiter");
  if (nr > 1) { zurueck.href = A.link(A.tuer(nr - 1)); zurueck.textContent = `‹ ${G.kapitel[nr - 2].titel}`; }
  if (nr < 24 && A.istFrei(nr + 1)) { weiter.href = A.link(A.tuer(nr + 1)); weiter.textContent = `${G.kapitel[nr].titel} ›`; }
})();

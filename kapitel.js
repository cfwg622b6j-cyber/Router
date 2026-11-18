(function () {
  "use strict";
  const K = window.KALENDER, G = window.GESCHICHTE, A = window.ADVENT;
  const nr = parseInt(new URLSearchParams(location.search).get("nr"), 10);
  const inhalt = document.getElementById("kapitel-inhalt");
  document.getElementById("zum-kalender").href = A.link("index.html");
  document.getElementById("geschichte-titel").textContent =
    `${G.titel} · ${G.autorin}` + (G.sprecher ? ` · ${G.sprecher}` : "");

  if (!(nr >= 1 && nr <= 24)) {
    document.getElementById("kapitel-titel").textContent = "Dieses Kapitel gibt es nicht.";
    return;
  }
  const kap = G.kapitel[nr - 1] || { titel: `Kapitel ${nr}`, text: [] };
  document.getElementById("kapitel-tag").textContent = `${nr}. Dezember · Kapitel ${nr}`;

  if (!A.istFrei(nr)) {
    document.title = `Kapitel ${nr}`;
    document.getElementById("kapitel-titel").textContent = "Noch nicht so ungeduldig!";
    const p = document.createElement("p");
    p.textContent = `Dieses Kapitel lässt sich erst am ${nr}. Dezember lesen. Der kleine Troll im Brunnen hütet es bis dahin gut.`;
    inhalt.append(p);
    return;
  }

  A.markiereOffen(nr);
  document.title = `${kap.titel} – ${G.titel}`;
  document.getElementById("kapitel-titel").textContent = kap.titel;

  const t = K.tueren.find((x) => x.nr === nr);
  if (t) {
    const v = document.getElementById("vignette"), a = A.ausschnitt(t);
    Object.assign(v.style, {
      backgroundImage: `url("${K.bildNachher}")`, backgroundSize: a.size, backgroundPosition: a.position,
      aspectRatio: `${t.b * K.bildBreite} / ${t.h * K.bildHoehe}`
    });
    v.hidden = false;
  }

  if (kap.audio) {
    const fig = document.createElement("figure");
    fig.className = "hoerbuch";
    fig.innerHTML = `<figcaption>Als Hörbuch anhören</figcaption>`;
    const audio = document.createElement("audio");
    audio.controls = true; audio.preload = "none"; audio.src = kap.audio;
    fig.append(audio);
    inhalt.append(fig);
  }
  for (const absatz of kap.text || []) {
    const p = document.createElement("p"); p.textContent = absatz; inhalt.append(p);
  }

  const zurueck = document.getElementById("zurueck"), weiter = document.getElementById("weiter");
  if (nr > 1) { zurueck.href = A.link(`kapitel.html?nr=${nr - 1}`); zurueck.textContent = `‹ Kapitel ${nr - 1}`; }
  if (nr < 24 && A.istFrei(nr + 1)) { weiter.href = A.link(`kapitel.html?nr=${nr + 1}`); weiter.textContent = `Kapitel ${nr + 1} ›`; }
})();

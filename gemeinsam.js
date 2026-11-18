// Gemeinsame Logik: Wann ist welches Kapitel lesbar?
window.ADVENT = (function () {
  "use strict";
  const params = new URLSearchParams(location.search);
  // Zum Testen: ?datum=2026-12-10 simuliert ein Datum, ?alle schaltet alles frei.
  const heute = params.has("datum") ? new Date(params.get("datum") + "T12:00:00") : new Date();
  const alleFrei = params.has("alle");
  const monat = heute.getMonth(); // 0 = Januar, 10 = November, 11 = Dezember

  // November: alles noch verschlossen. Dezember: Kapitel n ab dem n-ten.
  // Ab 25. Dezember bis Ende Oktober: die ganze Geschichte ist lesbar.
  function istFrei(nr) {
    if (alleFrei) return true;
    if (monat === 10) return false;
    if (monat === 11) return heute.getDate() >= nr;
    return true;
  }
  function freiAb(nr) { return `${nr}. Dezember`; }

  // Testparameter an interne Links weitergeben
  function link(pfad) {
    const p = [];
    if (params.has("datum")) p.push("datum=" + encodeURIComponent(params.get("datum")));
    if (alleFrei) p.push("alle");
    if (!p.length) return pfad;
    return pfad + (pfad.includes("?") ? "&" : "?") + p.join("&");
  }
  // Adressen wie auf den gedruckten QR-Codes: /tuer-01 … /tuer-24
  function tuer(nr) { return "/tuer-" + String(nr).padStart(2, "0"); }

  return { heute, istFrei, freiAb, link, tuer };
})();

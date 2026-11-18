// Gemeinsame Logik für Kalender und Kapitelseite.
window.ADVENT = (function () {
  "use strict";
  const params = new URLSearchParams(location.search);
  // Zum Testen: ?datum=2026-12-10 simuliert ein Datum, ?alle schaltet alles frei.
  const heute = params.has("datum") ? new Date(params.get("datum") + "T12:00:00") : new Date();
  const alleFrei = params.has("alle");
  const jahr = heute.getMonth() === 0 ? heute.getFullYear() - 1 : heute.getFullYear();
  const SCHLUESSEL = "adventskalender-offen-" + jahr;

  function istFrei(tag) {
    if (alleFrei) return true;
    if (heute.getFullYear() > jahr) return true;
    return heute.getMonth() === 11 && heute.getDate() >= tag;
  }
  function istHeute(tag) {
    return heute.getMonth() === 11 && heute.getDate() === tag;
  }
  function ladeOffen() {
    try { return new Set(JSON.parse(localStorage.getItem(SCHLUESSEL)) || []); }
    catch { return new Set(); }
  }
  function speichereOffen(set) {
    try { localStorage.setItem(SCHLUESSEL, JSON.stringify([...set])); } catch {}
  }
  function markiereOffen(tag) {
    const s = ladeOffen(); s.add(tag); speichereOffen(s); return s;
  }
  // Testparameter an interne Links weitergeben
  function link(pfad) {
    const p = new URLSearchParams();
    if (params.has("datum")) p.set("datum", params.get("datum"));
    if (alleFrei) p.set("alle", "");
    const q = p.toString().replace(/=(&|$)/g, "$1");
    if (!q) return pfad;
    return pfad + (pfad.includes("?") ? "&" : "?") + q;
  }
  // CSS-Werte, um genau den Bildausschnitt eines Türchens zu zeigen
  function ausschnitt(t) {
    return {
      size: `${(100 / t.b) * 100}% ${(100 / t.h) * 100}%`,
      position: `${(t.x / (100 - t.b)) * 100}% ${(t.y / (100 - t.h)) * 100}%`
    };
  }
  return { heute, jahr, alleFrei, istFrei, istHeute, ladeOffen, speichereOffen, markiereOffen, link, ausschnitt };
})();

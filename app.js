(function () {
  "use strict";

  const SPEICHER = "adventskalender-offen";
  const inhalte = window.KALENDER_INHALTE || [];

  // Testdatum per URL: ?datum=2026-12-10  oder  ?alle  (alle Türen offen erlaubt)
  const params = new URLSearchParams(location.search);
  const heute = params.has("datum") ? new Date(params.get("datum") + "T12:00:00") : new Date();
  const alleFrei = params.has("alle");
  const jahr = heute.getMonth() === 11 ? heute.getFullYear()
             : heute.getMonth() === 0 ? heute.getFullYear() - 1 : heute.getFullYear();

  // Feste, "zufällige" Anordnung der Türchen (deterministisch pro Jahr)
  function mischen(arr, seed) {
    const a = arr.slice();
    let s = seed;
    const rnd = () => ((s = (s * 9301 + 49297) % 233280) / 233280);
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(rnd() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

  function ladeOffen() {
    try { return new Set(JSON.parse(localStorage.getItem(SPEICHER + "-" + jahr)) || []); }
    catch { return new Set(); }
  }
  function speichereOffen(set) {
    try { localStorage.setItem(SPEICHER + "-" + jahr, JSON.stringify([...set])); } catch {}
  }

  function istFrei(tag) {
    if (alleFrei) return true;
    if (heute.getFullYear() > jahr) return true;
    if (heute.getFullYear() === jahr + 1) return true; // Januar
    return heute.getMonth() === 11 && heute.getDate() >= tag;
  }
  function istHeute(tag) {
    return heute.getMonth() === 11 && heute.getDate() === tag;
  }

  const offen = ladeOffen();
  const kalender = document.getElementById("kalender");
  const dialog = document.getElementById("dialog");

  document.getElementById("jahr").textContent = jahr;

  function aktualisiereStatus() {
    const el = document.getElementById("status");
    if (heute.getMonth() !== 11 && !alleFrei && heute.getMonth() !== 0) {
      const start = new Date(jahr, 11, 1);
      const tage = Math.ceil((start - heute) / 86400000);
      el.textContent = `Noch ${tage} ${tage === 1 ? "Tag" : "Tage"} bis zum ersten Türchen.`;
    } else {
      el.textContent = `${offen.size} von 24 Türchen geöffnet.`;
    }
  }

  function zeigeInhalt(tag) {
    const i = inhalte[tag - 1] || { titel: "Überraschung!", emoji: "🎁" };
    document.getElementById("dialog-tag").textContent = `${tag}. Dezember`;
    document.getElementById("dialog-titel").textContent = i.titel;
    const box = document.getElementById("dialog-inhalt");
    box.replaceChildren();
    if (i.emoji) {
      const e = document.createElement("span");
      e.className = "emoji"; e.textContent = i.emoji; box.append(e);
    }
    if (i.bild) {
      const img = document.createElement("img");
      img.src = i.bild; img.alt = i.titel; box.append(img);
    }
    if (i.text) {
      const p = document.createElement("p"); p.textContent = i.text; box.append(p);
    }
    if (i.link && i.link.url) {
      const a = document.createElement("a");
      a.href = i.link.url; a.target = "_blank"; a.rel = "noopener";
      a.textContent = i.link.text || i.link.url; box.append(a);
    }
    dialog.showModal();
  }

  mischen([...Array(24)].map((_, i) => i + 1), jahr).forEach((tag) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "tuer";
    btn.setAttribute("aria-label", `Türchen ${tag}`);
    btn.innerHTML = `<div class="tuer-innen">${(inhalte[tag - 1] || {}).emoji || "🎁"}<div class="tuer-blatt">${tag}</div></div>`;
    if (offen.has(tag)) btn.classList.add("offen");
    if (!istFrei(tag)) btn.classList.add("gesperrt");
    if (istHeute(tag) && !offen.has(tag)) btn.classList.add("heute");

    btn.addEventListener("click", () => {
      if (!istFrei(tag)) {
        btn.classList.remove("wackeln"); void btn.offsetWidth; btn.classList.add("wackeln");
        document.getElementById("status").textContent = `Geduld! Türchen ${tag} öffnet am ${tag}. Dezember.`;
        return;
      }
      if (!offen.has(tag)) {
        offen.add(tag); speichereOffen(offen);
        btn.classList.add("offen"); btn.classList.remove("heute");
        aktualisiereStatus();
        setTimeout(() => zeigeInhalt(tag), 650);
      } else {
        zeigeInhalt(tag);
      }
    });
    kalender.append(btn);
  });

  document.getElementById("dialog-schliessen").addEventListener("click", () => dialog.close());
  dialog.addEventListener("click", (e) => { if (e.target === dialog) dialog.close(); });

  document.getElementById("zuruecksetzen").addEventListener("click", () => {
    if (!confirm("Alle geöffneten Türchen wieder schließen?")) return;
    offen.clear(); speichereOffen(offen);
    document.querySelectorAll(".tuer").forEach((b) => b.classList.remove("offen"));
    aktualisiereStatus();
  });

  aktualisiereStatus();

  // Schneefall
  const canvas = document.getElementById("schnee");
  const ctx = canvas.getContext("2d");
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  let flocken = [];
  function groesse() {
    canvas.width = innerWidth; canvas.height = innerHeight;
    flocken = [...Array(Math.round(innerWidth / 12))].map(() => ({
      x: Math.random() * canvas.width, y: Math.random() * canvas.height,
      r: Math.random() * 2.5 + .8, v: Math.random() * .8 + .3, w: Math.random() * Math.PI * 2
    }));
  }
  function schneien() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "rgba(255,255,255,.8)";
    for (const f of flocken) {
      f.y += f.v; f.w += .01; f.x += Math.sin(f.w) * .4;
      if (f.y > canvas.height) { f.y = -5; f.x = Math.random() * canvas.width; }
      ctx.beginPath(); ctx.arc(f.x, f.y, f.r, 0, Math.PI * 2); ctx.fill();
    }
    requestAnimationFrame(schneien);
  }
  addEventListener("resize", groesse);
  groesse(); schneien();
})();

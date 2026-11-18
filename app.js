(function () {
  "use strict";
  const K = window.KALENDER, A = window.ADVENT;
  const bild = document.getElementById("bild");
  const status = document.getElementById("status");
  let offen = A.ladeOffen();

  document.title = K.titel;
  document.getElementById("titel").textContent = K.titel;
  document.getElementById("untertitel").textContent = K.untertitel || "";
  bild.style.aspectRatio = `${K.bildBreite} / ${K.bildHoehe}`;
  bild.style.setProperty("--vorher", `url("${K.bildVorher}")`);
  bild.style.setProperty("--nachher", `url("${K.bildNachher}")`);
  document.getElementById("basis").src = K.bildVorher;
  new Image().src = K.bildNachher; // vorladen

  function aktualisiereStatus() {
    if (!A.alleFrei && A.heute.getMonth() !== 11 && A.heute.getMonth() !== 0) {
      const tage = Math.ceil((new Date(A.jahr, 11, 1) - A.heute) / 86400000);
      status.textContent = `Noch ${tage} ${tage === 1 ? "Tag" : "Tage"} bis zum ersten Türchen.`;
    } else if (offen.size === 24) {
      status.textContent = "Alle 24 Türchen sind offen – frohe Weihnachten!";
    } else {
      status.textContent = `${offen.size} von 24 Türchen geöffnet.`;
    }
  }

  K.tueren.forEach((t) => {
    const tag = t.nr;
    const a = A.ausschnitt(t);
    const slot = document.createElement("div");
    slot.className = "slot";
    Object.assign(slot.style, { left: t.x + "%", top: t.y + "%", width: t.b + "%", height: t.h + "%" });
    slot.style.setProperty("--bs", a.size);
    slot.style.setProperty("--bp", a.position);
    slot.innerHTML = `
      <div class="dahinter"></div>
      <a class="kapitel-link" href="${A.link("kapitel.html?nr=" + tag)}">Kapitel ${tag} ›</a>
      <button type="button" class="blatt" aria-label="Türchen ${tag}">
        <span class="vorne"><span class="zahl">${tag}</span></span>
        <span class="hinten"></span>
      </button>`;
    const btn = slot.querySelector(".blatt");
    const setze = () => {
      slot.classList.toggle("offen", offen.has(tag));
      slot.classList.toggle("gesperrt", !A.istFrei(tag));
      slot.classList.toggle("heute", A.istHeute(tag) && !offen.has(tag));
      btn.setAttribute("aria-label", offen.has(tag) ? `Türchen ${tag} schließen` : `Türchen ${tag} öffnen`);
    };
    setze();

    btn.addEventListener("click", () => {
      if (!A.istFrei(tag)) {
        slot.classList.remove("wackeln"); void slot.offsetWidth; slot.classList.add("wackeln");
        status.textContent = `Geduld! Türchen ${tag} öffnet sich am ${tag}. Dezember.`;
        return;
      }
      if (offen.has(tag)) {           // geöffnetes Türchen: zum Kapitel
        location.href = A.link("kapitel.html?nr=" + tag);
        return;
      }
      offen = A.markiereOffen(tag);
      setze(); aktualisiereStatus();
    });
    bild.append(slot);
  });

  const nurBild = document.getElementById("nur-bild");
  nurBild.addEventListener("click", () => {
    const an = bild.classList.toggle("nur-bild");
    nurBild.setAttribute("aria-pressed", an);
    nurBild.textContent = an ? "Türchen wieder zeigen" : "Nur das Bild ansehen";
  });

  document.getElementById("zuruecksetzen").addEventListener("click", () => {
    if (!confirm("Alle Türchen wieder schließen?")) return;
    offen = new Set(); A.speichereOffen(offen);
    document.querySelectorAll(".slot").forEach((s) => s.classList.remove("offen"));
    aktualisiereStatus();
  });

  aktualisiereStatus();
})();

(function () {
  "use strict";
  const G = window.GESCHICHTE, A = window.ADVENT;
  const liste = document.getElementById("kapitelliste");
  let frei = 0;
  G.kapitel.forEach((k, i) => {
    const nr = i + 1, li = document.createElement("li");
    if (A.istFrei(nr)) {
      frei++;
      const a = document.createElement("a");
      a.href = A.link("kapitel.html?nr=" + nr);
      a.innerHTML = `<span class="nr">${nr}</span><span class="name"></span>`;
      a.querySelector(".name").textContent = k.titel;
      li.append(a);
    } else {
      li.className = "zu";
      li.innerHTML = `<span class="nr">${nr}</span><span class="name">ab ${A.freiAb(nr)}</span>`;
    }
    liste.append(li);
  });
  const h = document.getElementById("hinweis");
  if (frei === 0) {
    const tage = Math.ceil((new Date(A.heute.getFullYear(), 11, 1) - A.heute) / 86400000);
    h.textContent = `Das erste Kapitel öffnet sich am 1. Dezember – noch ${tage} ${tage === 1 ? "Tag" : "Tage"}.`;
  } else if (frei < 24) {
    h.textContent = `Heute ist Kapitel ${frei} dazugekommen.`;
  } else {
    h.textContent = "Die ganze Geschichte ist zu lesen.";
  }
})();

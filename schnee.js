(function () {
  const canvas = document.getElementById("schnee");
  if (!canvas || matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  const ctx = canvas.getContext("2d");
  let flocken = [];
  function groesse() {
    canvas.width = innerWidth; canvas.height = innerHeight;
    flocken = Array.from({ length: Math.round(innerWidth / 14) }, () => ({
      x: Math.random() * canvas.width, y: Math.random() * canvas.height,
      r: Math.random() * 2.5 + .8, v: Math.random() * .8 + .3, w: Math.random() * Math.PI * 2
    }));
  }
  function schneien() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "rgba(255,255,255,.75)";
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

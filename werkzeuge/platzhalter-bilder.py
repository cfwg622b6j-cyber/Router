#!/usr/bin/env python3
"""Erzeugt Platzhalter-Bilder (vorher/nachher) und Türchen-Positionen.

Nur für die Entwicklung: Später werden bilder/vorher.* und bilder/nachher.*
durch die echten Zeichnungen ersetzt und die Türchen-Positionen in daten.js
an das echte Bild angepasst.
"""
import math, random, json, pathlib

W, H = 1200, 900
ROOT = pathlib.Path(__file__).resolve().parent.parent

def tree(x, y, s, deco=False, rnd=None):
    out = [f'<rect x="{x-6*s:.0f}" y="{y-10*s:.0f}" width="{12*s:.0f}" height="{22*s:.0f}" fill="#3b2a1e"/>']
    for i, (wd, top, bot) in enumerate([(70, 120, 40), (55, 165, 95), (40, 205, 145)]):
        out.append(f'<polygon points="{x-wd*s:.0f},{y-bot*s+20*s:.0f} {x:.0f},{y-top*s-20*s:.0f} {x+wd*s:.0f},{y-bot*s+20*s:.0f}" fill="#1f4d3a"/>')
        out.append(f'<polygon points="{x-wd*s*.55:.0f},{y-top*s+8*s:.0f} {x:.0f},{y-top*s-20*s:.0f} {x+wd*s*.55:.0f},{y-top*s+8*s:.0f}" fill="#eef3f8" opacity=".85"/>')
    if deco:
        cols = ["#e63946", "#f2c14e", "#4cc9f0", "#f72585", "#80ed99"]
        for _ in range(14):
            t = rnd.random(); yy = y - 20*s - t*190*s; half = (1-t)*60*s
            xx = x + rnd.uniform(-half, half)
            out.append(f'<circle cx="{xx:.0f}" cy="{yy:.0f}" r="{4*s:.1f}" fill="{rnd.choice(cols)}"/>')
        out.append(star(x, y-232*s, 14*s, "#f2c14e"))
    return "".join(out)

def star(cx, cy, r, fill, pts=5):
    p = []
    for i in range(pts*2):
        rr = r if i % 2 == 0 else r*0.45
        a = -math.pi/2 + i*math.pi/pts
        p.append(f"{cx+rr*math.cos(a):.1f},{cy+rr*math.sin(a):.1f}")
    return f'<polygon points="{" ".join(p)}" fill="{fill}"/>'

def funke(cx, cy, r):
    return (f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r*1.6:.0f}" fill="url(#glow)"/>'
            + star(cx, cy, r, "#ffe08a", 4))

def scene(nachher, tueren):
    rnd = random.Random(7)
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
         '<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
         f'<stop offset="0" stop-color="#0a1426"/>'
         f'<stop offset="1" stop-color="#1e2f48"/></linearGradient>'
         '<radialGradient id="glow"><stop offset="0" stop-color="#ffe08a" stop-opacity=".9"/>'
         '<stop offset="1" stop-color="#ffe08a" stop-opacity="0"/></radialGradient></defs>',
         f'<rect width="{W}" height="{H}" fill="url(#sky)"/>']
    # Sterne
    srnd = random.Random(1)
    for _ in range(90 if nachher else 30):
        s.append(f'<circle cx="{srnd.uniform(0,W):.0f}" cy="{srnd.uniform(0,420):.0f}" r="{srnd.uniform(.8,2.2):.1f}" fill="#fff" opacity="{srnd.uniform(.4,1):.2f}"/>')
    if nachher:
        s.append('<circle cx="1105" cy="95" r="62" fill="url(#glow)" opacity=".6"/><circle cx="1105" cy="95" r="38" fill="#fff3c4"/>')
        s.append('<path d="M250 110 L470 190" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".8"/>' + star(470, 190, 10, "#fff"))
    # Hügel und Boden
    s.append('<path d="M0 520 Q250 430 520 500 T1200 470 V900 H0Z" fill="#9fb0c8"/>')
    s.append('<path d="M0 640 Q300 600 600 640 T1200 620 V900 H0Z" fill="#e8eef6"/>')
    s.append('<path d="M575 640 Q560 780 520 900 H700 Q650 780 625 640Z" fill="#d3deeb"/>')
    # Bäume
    for (x, y, sc) in [(90, 660, 1.2), (200, 620, .9), (1060, 650, 1.3), (950, 670, 1.0), (1150, 600, .8), (340, 610, .6)]:
        s.append(tree(x, y, sc, nachher, rnd))
    # Baude
    s.append('<rect x="430" y="470" width="340" height="175" fill="#6b4a2e"/>')
    for yy in range(490, 640, 20):
        s.append(f'<line x1="430" y1="{yy}" x2="770" y2="{yy}" stroke="#4e3420" stroke-width="2"/>')
    s.append('<rect x="690" y="350" width="34" height="90" fill="#5a4a44"/>')
    s.append('<polygon points="395,485 600,320 805,485" fill="#3a2a20"/>')
    s.append('<path d="M395 485 L600 320 L805 485 L790 492 L600 340 L410 492Z" fill="#f4f7fb"/>')
    win = "#ffd66b" if nachher else "#1b2533"
    for (x, y, w, h) in [(455, 540, 42, 46), (510, 540, 42, 46), (648, 540, 42, 46), (703, 540, 42, 46), (575, 400, 50, 50)]:
        if nachher:
            s.append(f'<circle cx="{x+w/2}" cy="{y+h/2}" r="{w*1.3}" fill="url(#glow)" opacity=".7"/>')
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{win}" stroke="#3a2a20" stroke-width="4"/>')
        s.append(f'<line x1="{x+w/2}" y1="{y}" x2="{x+w/2}" y2="{y+h}" stroke="#3a2a20" stroke-width="3"/>')
    s.append('<rect x="575" y="565" width="50" height="78" fill="#3a2a20"/>')
    s.append('<rect x="540" y="497" width="120" height="30" rx="4" fill="#d9b382"/>'
             '<text x="600" y="519" font-family="Georgia,serif" font-size="18" text-anchor="middle" fill="#3a2a20">BAUDE</text>')
    if nachher:
        cols = ["#e63946", "#f2c14e", "#4cc9f0", "#80ed99"]
        for i in range(19):
            t = i/18
            s.append(f'<circle cx="{395+205*t:.0f}" cy="{487-165*t:.0f}" r="5" fill="{cols[i%4]}"/>')
            s.append(f'<circle cx="{600+205*t:.0f}" cy="{322+165*t:.0f}" r="5" fill="{cols[(i+2)%4]}"/>')
        s.append('<circle cx="600" cy="595" r="17" fill="none" stroke="#2d6a4f" stroke-width="8"/><circle cx="600" cy="612" r="5" fill="#e63946"/>')
        for i, (dx, r) in enumerate([(0, 14), (14, 18), (34, 22)]):
            s.append(f'<circle cx="{707+dx*.6:.0f}" cy="{330-i*34}" r="{r}" fill="#cfd6df" opacity="{.7-i*.15:.2f}"/>')
    # Brunnen
    s.append('<polygon points="185,575 260,525 335,575" fill="#3a2a20"/><rect x="205" y="572" width="10" height="90" fill="#4e3420"/><rect x="305" y="572" width="10" height="90" fill="#4e3420"/>')
    s.append('<rect x="200" y="655" width="120" height="65" fill="#7d7f86"/>')
    for yy in (672, 690, 708):
        s.append(f'<line x1="200" y1="{yy}" x2="320" y2="{yy}" stroke="#5d5f66" stroke-width="2"/>')
    s.append('<ellipse cx="260" cy="655" rx="60" ry="14" fill="#9a9ca3"/><ellipse cx="260" cy="655" rx="48" ry="9" fill="#0a0f18"/>')
    if nachher:
        s.append('<circle cx="260" cy="640" r="70" fill="url(#glow)" opacity=".5"/>')
        s.append('<ellipse cx="226" cy="636" rx="14" ry="7" fill="#6f8a5a"/><ellipse cx="294" cy="636" rx="14" ry="7" fill="#6f8a5a"/>')
        s.append('<path d="M232 652 Q232 618 260 618 Q288 618 288 652Z" fill="#7c9a63"/>')
        s.append('<polygon points="240,622 260,585 280,622" fill="#c1121f"/><circle cx="260" cy="585" r="5" fill="#fff"/>')
        s.append('<circle cx="250" cy="638" r="4" fill="#ffe08a"/><circle cx="270" cy="638" r="4" fill="#ffe08a"/>')
        for (x, y) in [(215, 605), (310, 615), (245, 560), (330, 590)]:
            s.append(star(x, y, 6, "#ffe08a", 4))
        # Schneemann, Laternen, Geschenke, Schlitten
        s.append('<circle cx="880" cy="760" r="42" fill="#fff"/><circle cx="880" cy="700" r="30" fill="#fff"/><polygon points="880,700 905,705 880,708" fill="#f77f00"/><circle cx="871" cy="692" r="3"/><circle cx="889" cy="692" r="3"/><rect x="860" y="660" width="40" height="10" fill="#222"/><rect x="867" y="635" width="26" height="28" fill="#222"/>')
        for (x, y) in [(535, 760), (665, 760), (515, 850), (690, 850)]:
            s.append(f'<rect x="{x-2}" y="{y-40}" width="4" height="40" fill="#333"/><circle cx="{x}" cy="{y-46}" r="22" fill="url(#glow)"/><rect x="{x-7}" y="{y-54}" width="14" height="16" fill="#ffd66b"/>')
        for (x, y, c) in [(380, 760, "#e63946"), (415, 772, "#2d6a4f"), (395, 790, "#4361ee")]:
            s.append(f'<rect x="{x}" y="{y}" width="34" height="28" fill="{c}"/><rect x="{x+15}" y="{y}" width="4" height="28" fill="#f2c14e"/>')
        s.append('<path d="M960 820 H1080 Q1100 820 1095 800" stroke="#7a3e1d" stroke-width="6" fill="none"/><rect x="970" y="800" width="100" height="12" fill="#c1121f"/>')
        # Wunschfunken – garantiert eine Veränderung hinter jedem Türchen
        frnd = random.Random(3)
        for t in tueren:
            cx = (t["x"] + t["b"]*frnd.uniform(.25, .75)) * W/100
            cy = (t["y"] + t["h"]*frnd.uniform(.2, .5)) * H/100
            s.append(funke(cx, cy, 11))
    s.append('</svg>')
    return "\n".join(s)

def tuer_positionen():
    rnd = random.Random(2026)
    nummern = list(range(1, 25)); rnd.shuffle(nummern)
    tueren = []
    for i in range(24):
        r, c = divmod(i, 6)
        b, h = rnd.uniform(125, 155), rnd.uniform(120, 150)
        x = c*200 + (200-b)/2 + rnd.uniform(-18, 18)
        y = r*225 + (225-h)/2 + rnd.uniform(-25, 25)
        tueren.append({"nr": nummern[i], "x": round(x/W*100, 2), "y": round(y/H*100, 2),
                       "b": round(b/W*100, 2), "h": round(h/H*100, 2)})
    return sorted(tueren, key=lambda t: t["nr"])

if __name__ == "__main__":
    t = tuer_positionen()
    (ROOT/"bilder/vorher.svg").write_text(scene(False, t))
    (ROOT/"bilder/nachher.svg").write_text(scene(True, t))
    for e in t:
        print("    " + json.dumps(e) + ",")

#!/usr/bin/env python3
"""Szene Kapitel 1: Der Wirt wünscht sich Schnee – der Troll hört es in seiner Höhle."""
import pathlib, re, random
ROOT = pathlib.Path(__file__).resolve().parent.parent
troll = (ROOT / "entwuerfe/baudentroll.svg").read_text()
defs = troll[troll.index("<defs>") + 6: troll.index("</defs>")]
koerper = troll[troll.index("  <!-- Laterne (Licht hinten) -->"): troll.index("  <text")]
rnd = random.Random(4)

W, H = 900, 1120
s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
     "<title>Kapitel 1 – Ich wünschte mir so sehr, es würde endlich schneien</title>",
     "<defs>" + defs + """
  <linearGradient id="himmel" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#5d6d8c"/><stop offset=".55" stop-color="#9aa3b5"/><stop offset="1" stop-color="#d8a88a"/></linearGradient>
  <linearGradient id="erde" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#8a7560"/><stop offset="1" stop-color="#5e4e3f"/></linearGradient>
  <radialGradient id="hoehle" cx="50%" cy="55%" r="55%">
    <stop offset="0" stop-color="#e9c48e"/><stop offset=".6" stop-color="#b98d62"/><stop offset="1" stop-color="#8a6a4c"/></radialGradient>
  <filter id="unscharf" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="6"/></filter>
</defs>""",
     f'<rect width="{W}" height="{H}" fill="#f6eedd"/>',
     # Himmel
     '<rect x="0" y="0" width="900" height="610" fill="url(#himmel)"/>']
# Sturmwolken
for i in range(7):
    x, y = rnd.uniform(-50, 850), rnd.uniform(30, 260)
    s.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rnd.uniform(110,190):.0f}" ry="{rnd.uniform(18,30):.0f}" fill="#4f5d79" opacity=".45" filter="url(#unscharf)"/>')
# Hügel
s.append('<path d="M0 470 Q200 410 420 450 T900 430 V610 H0Z" fill="#8f9a8c" opacity=".7"/>')
# Bäume im Wind (geneigt)
def baum(x, y, k, farbe="#3f5a4a"):
    return (f'<g transform="translate({x} {y}) scale({k}) skewX(-8)"><rect x="-6" y="-12" width="12" height="24" fill="#6b5442"/>'
            f'<path d="M-55 0 L0 -70 L55 0Z M-45 -45 L0 -115 L45 -45Z M-34 -90 L0 -155 L34 -90Z" fill="{farbe}"/></g>')
for x, y, k in [(40, 600, 1.2), (120, 590, .9), (870, 600, 1.1), (800, 585, .8)]:
    s.append(baum(x, y, k))
# Die Baude: weißes Erdgeschoss, grünes Obergeschoss, gelber Turm
s.append('''<g>
  <rect x="590" y="300" width="70" height="260" fill="#e8d27a" stroke="#a89a6c" stroke-width="2"/>
  <rect x="582" y="282" width="86" height="22" fill="#8c4a3c"/><rect x="590" y="266" width="70" height="18" fill="#efe6cf"/>
  <rect x="612" y="330" width="14" height="22" fill="#5d6d8c"/><rect x="612" y="390" width="14" height="22" fill="#5d6d8c"/>
  <rect x="640" y="330" width="14" height="22" fill="#5d6d8c"/>
  <rect x="520" y="480" width="300" height="100" fill="#efe9dc" stroke="#a89a8a" stroke-width="2"/>
  <path d="M510 482 L540 400 H810 L830 482Z" fill="#4f6b52" stroke="#3e5641" stroke-width="2"/>
  <path d="M540 400 L560 380 H795 L810 400Z" fill="#3e5641"/>''')
for x in range(545, 800, 42):
    lit = x in (587, 713)
    s.append(f'<rect x="{x}" y="505" width="20" height="28" fill="{"#ffd98a" if lit else "#59657a"}" stroke="#a89a8a" stroke-width="2"/>')
    s.append(f'<rect x="{x+2}" y="425" width="16" height="20" fill="#59657a" stroke="#3e5641" stroke-width="1.5"/>')
s.append('<circle cx="597" cy="519" r="22" fill="#ffd98a" opacity=".35" filter="url(#unscharf)"/></g>')
# Boden (matschig, noch kein Schnee) mit Pfützen
s.append('<path d="M0 600 Q300 590 600 602 T900 598 V640 H0Z" fill="#7b7262"/>')
s.append('<ellipse cx="395" cy="612" rx="46" ry="7" fill="#9aa3b5" opacity=".8"/><ellipse cx="520" cy="616" rx="30" ry="5" fill="#9aa3b5" opacity=".7"/>')
# Erde im Querschnitt
s.append('<rect x="0" y="625" width="900" height="400" fill="url(#erde)"/>')
for i in range(26):
    x, y = rnd.uniform(10, 890), rnd.uniform(650, 1010)
    s.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rnd.uniform(10,26):.0f}" ry="{rnd.uniform(6,14):.0f}" fill="#4e4136" opacity=".55"/>')
# Brunnenschacht
s.append('<path d="M228 600 V780 Q228 820 268 830 L330 840 V790 Q272 780 272 740 V600Z" fill="#2e2620" opacity=".85"/>')
# Höhle
s.append('<ellipse cx="520" cy="865" rx="300" ry="140" fill="#3e332a"/>')
s.append('<ellipse cx="520" cy="868" rx="285" ry="126" fill="url(#hoehle)"/>')
s.append('<clipPath id="hoehlenform"><ellipse cx="520" cy="868" rx="285" ry="126"/></clipPath>')
s.append('<path d="M200 945 Q520 990 840 945 V1010 H200Z" fill="#6f8a55" opacity=".85" clip-path="url(#hoehlenform)"/>')  # Moosboden
# Regal mit Gläsern und Bett aus Moos
s.append('''<rect x="660" y="820" width="90" height="8" rx="3" fill="#7a5a3e"/>
<rect x="668" y="796" width="16" height="24" rx="4" fill="#c7d8c0" opacity=".9"/><rect x="690" y="800" width="14" height="20" rx="4" fill="#e3b7a0"/>
<rect x="710" y="792" width="18" height="28" rx="4" fill="#d9cd8c"/><circle cx="740" cy="810" r="9" fill="#c48b80"/>
<ellipse cx="320" cy="950" rx="60" ry="20" fill="#86a36a"/><ellipse cx="320" cy="944" rx="50" ry="14" fill="#9cb882"/>''')
# Die Worte des Wirts wandern den Brunnen hinab
s.append('''<path id="wortweg" d="M250 610 C250 660 252 700 258 760 C266 820 330 836 470 832" fill="none"/>
<text font-family="Georgia, serif" font-size="16" font-style="italic" fill="#ffe7a8">
  <textPath href="#wortweg">… ich wünschte mir so sehr, es würde endlich schneien …</textPath></text>''')
for i in range(10):
    x, y = rnd.uniform(235, 450), rnd.uniform(620, 840)
    if x > 285 and y < 780: continue
    s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(1.5,3.5):.1f}" fill="#ffe7a8" opacity=".85"/>')
# Troll in der Höhle
s.append(f'<g transform="translate(395 728) scale(0.34)">{koerper}</g>')
# Brunnen (oben)
s.append('''<g>
  <rect x="200" y="540" width="100" height="64" fill="#9b968c" stroke="#6d675e" stroke-width="2"/>
  <path d="M200 560 H300 M200 582 H300 M232 540 V560 M268 560 V582 M226 582 V604 M276 582 V604" stroke="#6d675e" stroke-width="2"/>
  <ellipse cx="250" cy="540" rx="50" ry="12" fill="#b3ada2" stroke="#6d675e" stroke-width="2"/><ellipse cx="250" cy="540" rx="40" ry="7" fill="#2e2620"/>
  <rect x="206" y="440" width="8" height="100" fill="#6b5442"/><rect x="286" y="440" width="8" height="100" fill="#6b5442"/>
  <path d="M190 448 L250 405 L310 448Z" fill="#7a5a44"/>
  <path d="M250 452 L268 498" stroke="#555" stroke-width="2"/>
  <g transform="rotate(-24 268 498)"><path d="M256 498 H282 L278 526 H260Z" fill="#8f949a" stroke="#5b5f63" stroke-width="2"/></g>
</g>''')
# Der Wirt Martin, gegen den Wind gebeugt, ein Fuß in der Pfütze
s.append('''<g transform="translate(395 600) rotate(-6)">
  <rect x="-20" y="-58" width="14" height="58" fill="#4a4038"/><rect x="4" y="-58" width="14" height="52" fill="#4a4038"/>
  <ellipse cx="-13" cy="0" rx="14" ry="6" fill="#3a322c"/><ellipse cx="13" cy="-4" rx="14" ry="6" fill="#3a322c"/>
  <path d="M-34 -150 Q0 -162 34 -150 L42 -52 H-42Z" fill="#7b5c43" stroke="#5e4532" stroke-width="2"/>
  <path d="M0 -150 V-56" stroke="#5e4532" stroke-width="2"/><circle cx="-6" cy="-128" r="3" fill="#d8c8a0"/><circle cx="-6" cy="-104" r="3" fill="#d8c8a0"/>
  <path d="M-30 -146 Q-70 -120 -112 -110" stroke="#7b5c43" stroke-width="18" stroke-linecap="round" fill="none"/>
  <circle cx="-116" cy="-108" r="9" fill="#e6c4a4"/>
  <path d="M-24 -152 Q0 -142 26 -152 L26 -162 Q0 -152 -24 -162Z" fill="#a8463c"/>
  <path d="M18 -152 Q40 -150 54 -162" stroke="#a8463c" stroke-width="8" stroke-linecap="round" fill="none"/>
  <circle cx="0" cy="-182" r="22" fill="#e6c4a4" stroke="#b9967a" stroke-width="2"/>
  <circle cx="-8" cy="-186" r="2.5" fill="#3a2e24"/><circle cx="8" cy="-186" r="2.5" fill="#3a2e24"/>
  <path d="M-15 -196 L-3 -191 M3 -191 L15 -196" stroke="#4a3a2e" stroke-width="3" stroke-linecap="round"/>
  <path d="M-15 -174 Q0 -181 15 -174 Q8 -171 0 -173 Q-8 -171 -15 -174Z" fill="#6e5444"/>
  <path d="M-9 -164 Q0 -170 9 -164" stroke="#8a4a3e" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  <ellipse cx="0" cy="-200" rx="34" ry="7" fill="#3c3631"/><path d="M-20 -200 Q-18 -224 0 -224 Q18 -224 20 -200Z" fill="#3c3631"/>
</g>''')
# Windlinien und die ersten Schneeflocken
s.append('<g stroke="#eef1f6" stroke-width="2" stroke-linecap="round" opacity=".6" fill="none">'
         '<path d="M470 300 q40 -10 80 0"/><path d="M90 340 q50 -12 100 0"/><path d="M360 220 q40 -8 70 0"/><path d="M700 220 q40 -8 70 0"/></g>')
for i in range(22):
    s.append(f'<circle cx="{rnd.uniform(20,880):.0f}" cy="{rnd.uniform(20,560):.0f}" r="{rnd.uniform(2,4.5):.1f}" fill="#fff" opacity=".9"/>')
# Bildunterschrift
s.append('<rect x="0" y="1025" width="900" height="95" fill="#f6eedd"/>')
s.append('<text x="450" y="1066" text-anchor="middle" font-family="Georgia, serif" font-size="25" font-style="italic" fill="#5a3e2b">„Ich wünschte mir so sehr, es würde endlich schneien.“</text>')
s.append('<text x="450" y="1100" text-anchor="middle" font-family="Georgia, serif" font-size="17" fill="#8a6a52">Erster Dezember</text>')
s.append("</svg>")
ziel = ROOT / "entwuerfe/szenen/kapitel-01.svg"
ziel.write_text("\n".join(s))
print(ziel)

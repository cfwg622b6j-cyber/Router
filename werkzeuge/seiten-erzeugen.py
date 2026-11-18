#!/usr/bin/env python3
"""Erzeugt die Ordner für die Adressen auf den gedruckten QR-Codes.

  /einleitung      ← QR-Code auf der Rückseite  (Kopie von index.html)
  /tuer-01 … /tuer-24 ← QR-Codes in den Türchen (Kopie von kapitel.html)

Nach jeder Änderung an index.html oder kapitel.html erneut ausführen:
  python3 werkzeuge/seiten-erzeugen.py
"""
import pathlib, shutil
root = pathlib.Path(__file__).resolve().parent.parent
(root / "einleitung").mkdir(exist_ok=True)
shutil.copy(root / "index.html", root / "einleitung" / "index.html")
for nr in range(1, 25):
    d = root / f"tuer-{nr:02d}"
    d.mkdir(exist_ok=True)
    shutil.copy(root / "kapitel.html", d / "index.html")
print("einleitung/ und tuer-01/ … tuer-24/ erzeugt")

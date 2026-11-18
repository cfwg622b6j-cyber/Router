#!/usr/bin/env python3
"""Erzeugt das Hörbuch „Zeit der Wunder“ aus geschichte.js mit Piper-Sprachsynthese.

  python3 werkzeuge/hoerbuch.py STIMME.onnx [Kapitel ...] [--probe] [--ziel audio]

Ohne Kapitelangabe werden alle 24 Kapitel erzeugt (audio/kapitel-01.mp3 …).
"""
import argparse, io, json, pathlib, re, subprocess, tempfile, wave
from piper import PiperVoice, SynthesisConfig

ROOT = pathlib.Path(__file__).resolve().parent.parent

def lade_geschichte():
    js = (ROOT / "geschichte.js").read_text()
    roh = js[js.index("kapitel:") + len("kapitel:"):js.rindex("};")].strip()
    return json.loads(roh)

def stille(sek, rate):
    return b"\x00\x00" * int(sek * rate)

def sprich(stimme, text, cfg):
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        stimme.synthesize_wav(text, wf, syn_config=cfg)
    buf.seek(0)
    with wave.open(buf) as wf:
        return wf.readframes(wf.getnframes())

def kapitel_audio(stimme, kap, cfg_text, cfg_vers, nur_anfang=False):
    rate = stimme.config.sample_rate
    teile = [sprich(stimme, kap["titel"] + ".", cfg_text), stille(1.2, rate)]
    bloecke = kap["bloecke"]
    if nur_anfang:  # Hörprobe: erster Absatz (gekürzt) + der Reim
        erster = re.split(r"(?<=[.!?])\s", bloecke[0])
        bloecke = [" ".join(erster[:4])] + [b for b in bloecke if isinstance(b, dict)]
    for b in bloecke:
        if isinstance(b, str):
            teile += [sprich(stimme, b, cfg_text), stille(0.8, rate)]
        else:
            teile.append(stille(0.4, rate))
            for zeile in b["vers"]:
                teile += [sprich(stimme, zeile, cfg_vers), stille(0.35, rate)]
            teile.append(stille(0.8, rate))
    return b"".join(teile), rate

def als_mp3(pcm, rate, ziel):
    with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
        with wave.open(tmp.name, "wb") as wf:
            wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(rate); wf.writeframes(pcm)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", tmp.name,
                        "-af", "loudnorm=I=-18:TP=-1.5", "-ar", "44100",
                        "-codec:a", "libmp3lame", "-b:a", "64k", "-ac", "1", str(ziel)], check=True)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("stimme")
    ap.add_argument("kapitel", nargs="*", type=int)
    ap.add_argument("--probe", action="store_true")
    ap.add_argument("--ziel", default=str(ROOT / "audio"))
    ap.add_argument("--tempo", type=float, default=1.12, help="größer = langsamer")
    a = ap.parse_args()

    stimme = PiperVoice.load(a.stimme)
    cfg_text = SynthesisConfig(length_scale=a.tempo, noise_scale=0.6, noise_w_scale=0.8)
    cfg_vers = SynthesisConfig(length_scale=a.tempo * 1.08, noise_scale=0.6, noise_w_scale=0.8)
    alle = lade_geschichte()
    ziel = pathlib.Path(a.ziel); ziel.mkdir(parents=True, exist_ok=True)
    for nr in a.kapitel or range(1, 25):
        pcm, rate = kapitel_audio(stimme, alle[nr - 1], cfg_text, cfg_vers, a.probe)
        name = ziel / (f"probe-{pathlib.Path(a.stimme).stem}.mp3" if a.probe else f"kapitel-{nr:02d}.mp3")
        als_mp3(pcm, rate, name)
        print(name, f"{len(pcm) / 2 / rate / 60:.1f} min")

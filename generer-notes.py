#!/usr/bin/env python3
"""Genere les notes de violon (audio/<id>.mp3) pour le Quizz violon.

Source : VSCO 2 Community Edition (CC0-1.0), violon solo "Arco Vib".
URL    : https://github.com/sgossner/VSCO-2-CE (dossier Strings/Solo Violin/Arco Vib)

VSCO ne fournit que les notes Sol/Do/Mi (pas de demi-tons). On part donc de
8 echantillons de base et on decale la hauteur par re-echantillonnage (ffmpeg
asetrate), ce qui est la methode standard d'un sampler. Chaque note devient un
fichier mp3 autonome, court (~3 s), mono, normalise et versionnable.

Usage :
    python3 generer-notes.py            # telecharge si besoin puis genere
    python3 generer-notes.py --force    # regenere meme si le mp3 existe
"""

import argparse
import json
import os
import subprocess
import sys
import urllib.request
import urllib.parse

BASE_URL = ("https://raw.githubusercontent.com/sgossner/VSCO-2-CE/master/"
            "Strings/Solo%20Violin/Arco%20Vib/")

HERE = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(HERE, "audio-src")
OUT_DIR = os.path.join(HERE, "audio")

# note -> (echantillon de base VSCO, demi-tons a appliquer)
# Bases disponibles : G3 A3 C4 E4 G4 A4 C5 E5. Les autres notes sont decalees
# de +1 ou +2 demi-tons. (Ambitus vise : G3 -> E5.)
PLAN = {
    "G3":  ("LLVln_ArcoVib_G3_f.wav", 0),
    "A3":  ("LLVln_ArcoVib_A3_f.wav", 0),
    "B3":  ("LLVln_ArcoVib_A3_f.wav", 2),
    "C4":  ("LLVln_ArcoVib_C4_f.wav", 0),
    "C#4": ("LLVln_ArcoVib_C4_f.wav", 1),
    "D4":  ("LLVln_ArcoVib_C4_f.wav", 2),
    "E4":  ("LLVln_ArcoVib_E4_f.wav", 0),
    "F4":  ("LLVln_ArcoVib_E4_f.wav", 1),
    "F#4": ("LLVln_ArcoVib_E4_f.wav", 2),
    "G4":  ("LLVln_ArcoVib_G4_f.wav", 0),
    "A4":  ("LLVln_ArcoVib_A4_f.wav", 0),
    "B4":  ("LLVln_ArcoVib_A4_f.wav", 2),
    "C5":  ("LLVln_ArcoVib_C5_f.wav", 0),
    "C#5": ("LLVln_ArcoVib_C5_f.wav", 1),
    "D5":  ("LLVln_ArcoVib_C5_f.wav", 2),
    "E5":  ("LLVln_ArcoVib_E5_f.wav", 0),
}

# Nom de fichier mp3 (le diese devient 's' : C#4 -> Cs4).
def out_name(note_id):
    return note_id.replace("#", "s") + ".mp3"


def run(cmd):
    subprocess.run(cmd, check=True)


def have(tool):
    return subprocess.call(["which", tool], stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL) == 0


def sample_rate(path):
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-select_streams", "a:0",
        "-show_entries", "stream=sample_rate", "-of", "csv=p=0", path
    ])
    return int(out.decode().strip())


def download(base_file):
    os.makedirs(SRC_DIR, exist_ok=True)
    dest = os.path.join(SRC_DIR, base_file)
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return dest
    url = BASE_URL + urllib.parse.quote(base_file)
    print("telechargement :", base_file)
    urllib.request.urlretrieve(url, dest)
    return dest


def generate(src, note_id, semitones, force):
    os.makedirs(OUT_DIR, exist_ok=True)
    dest = os.path.join(OUT_DIR, out_name(note_id))
    if os.path.exists(dest) and not force:
        print("deja la   :", os.path.basename(dest))
        return
    sr = sample_rate(src)
    ratio = 2 ** (semitones / 12.0)
    af = (
        "asetrate={rate}*{ratio},aresample={rate},"
        "atrim=0:3,asetpts=N/SR/TB,"
        "afade=t=in:st=0:d=0.02,afade=t=out:st=2.5:d=0.5,"
        "loudnorm=I=-18:TP=-2:LRA=11"
    ).format(rate=sr, ratio=ratio)
    print("generation:", os.path.basename(dest), "(+%d demi-tons)" % semitones)
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-af", af,
         "-ac", "1", "-ar", "44100", "-b:a", "128k", dest])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="regenerer les mp3 existants")
    args = ap.parse_args()

    for tool in ("ffmpeg", "ffprobe"):
        if not have(tool):
            sys.exit("outil manquant : %s" % tool)

    # verifie que le plan correspond bien a notes.json
    with open(os.path.join(HERE, "notes.json"), encoding="utf-8") as f:
        ids = [n["id"] for n in json.load(f)["notes"]]
    missing = [i for i in ids if i not in PLAN]
    extra = [i for i in PLAN if i not in ids]
    if missing or extra:
        sys.exit("ecart entre notes.json et PLAN : manquants=%s en trop=%s" % (missing, extra))

    cache = {}
    for note_id in ids:
        base_file, semis = PLAN[note_id]
        if base_file not in cache:
            cache[base_file] = download(base_file)
        generate(cache[base_file], note_id, semis, args.force)

    print("\nOK : %d notes dans %s" % (len(ids), os.path.relpath(OUT_DIR, HERE)))


if __name__ == "__main__":
    main()

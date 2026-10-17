#!/usr/bin/env python3
"""Genere les notes (audio/<instrument>/<id>.mp3) pour le Quizz violon.

Sources : VSCO 2 Community Edition (Versilian Studios), libres d'usage.
  - violon : Strings/Solo Violin/Arco Vib (base _f, forte)
  - piano  : Keys/Upright Piano (Ivy Audio, base dyn3, forte)
URL      : https://github.com/sgossner/VSCO-2-CE

VSCO ne fournit pas toutes les notes : on part d'echantillons de base et on
decale la hauteur par re-echantillonnage (ffmpeg asetrate), la methode standard
d'un sampler. Chaque note devient un fichier mp3 autonome, court (~3 s), mono,
normalise et versionnable.

Le violon est echantillonne toutes les 1-2 notes (G3 A3 C4 E4 G4 A4 C5 E5),
le piano tous les 4 demi-tons (F3 A3 C#4 F4 A4 C#5 F5 dans notre ambitus).
Decalage maximal applique : 2 demi-tons montants, 1/2 descendant.

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

VSCO = "https://raw.githubusercontent.com/sgossner/VSCO-2-CE/master/"

# Pour chaque instrument : dossier source VSCO + plan note -> (echantillon, demi-tons)
INSTRUMENTS = {
    "violon": {
        "base_url": VSCO + "Strings/Solo%20Violin/Arco%20Vib/",
        "plan": {
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
        },
    },
    "piano": {
        "base_url": VSCO + "Keys/Upright%20Piano/",
        # Echantillons tous les 4 demi-tons : suffixe = (numero de touche - 21) / 2.
        # F3=016 A3=018 C#4=020 F4=022 A4=024 C#5=026 F5=028.
        "plan": {
            "G3":  ("Player_dyn3_rr1_016.wav", 2),
            "A3":  ("Player_dyn3_rr1_018.wav", 0),
            "B3":  ("Player_dyn3_rr1_018.wav", 2),
            "C4":  ("Player_dyn3_rr1_020.wav", -1),
            "C#4": ("Player_dyn3_rr1_020.wav", 0),
            "D4":  ("Player_dyn3_rr1_020.wav", 1),
            "E4":  ("Player_dyn3_rr1_022.wav", -1),
            "F4":  ("Player_dyn3_rr1_022.wav", 0),
            "F#4": ("Player_dyn3_rr1_022.wav", 1),
            "G4":  ("Player_dyn3_rr1_022.wav", 2),
            "A4":  ("Player_dyn3_rr1_024.wav", 0),
            "B4":  ("Player_dyn3_rr1_024.wav", 2),
            "C5":  ("Player_dyn3_rr1_026.wav", -1),
            "C#5": ("Player_dyn3_rr1_026.wav", 0),
            "D5":  ("Player_dyn3_rr1_026.wav", 1),
            "E5":  ("Player_dyn3_rr1_028.wav", -1),
        },
    },
}

HERE = os.path.dirname(os.path.abspath(__file__))


def out_name(note_id):
    """Nom de fichier mp3 (le diese devient 's' : C#4 -> Cs4)."""
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


def download(base_url, base_file, src_dir):
    os.makedirs(src_dir, exist_ok=True)
    dest = os.path.join(src_dir, base_file)
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return dest
    url = base_url + urllib.parse.quote(base_file)
    print("telechargement :", base_file)
    urllib.request.urlretrieve(url, dest)
    return dest


def generate(src, dest, semitones, force):
    if os.path.exists(dest) and not force:
        print("deja la   :", os.path.relpath(dest, HERE))
        return
    sr = sample_rate(src)
    ratio = 2 ** (semitones / 12.0)
    af = (
        "asetrate={rate}*{ratio},aresample={rate},"
        "atrim=0:3,asetpts=N/SR/TB,"
        "afade=t=in:st=0:d=0.02,afade=t=out:st=2.5:d=0.5,"
        "loudnorm=I=-18:TP=-2:LRA=11"
    ).format(rate=sr, ratio=ratio)
    print("generation:", os.path.relpath(dest, HERE), "(%+d demi-tons)" % semitones)
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-af", af,
         "-ac", "1", "-ar", "44100", "-b:a", "128k", dest])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="regenerer les mp3 existants")
    args = ap.parse_args()

    for tool in ("ffmpeg", "ffprobe"):
        if not have(tool):
            sys.exit("outil manquant : %s" % tool)

    # notes.json est la source de verite : liste des notes autorisees + instruments.
    with open(os.path.join(HERE, "notes.json"), encoding="utf-8") as f:
        data = json.load(f)
    ids = [n["id"] for n in data["notes"]]
    instruments = data.get("instruments") or list(INSTRUMENTS)

    # verifie que chaque plan correspond bien a notes.json
    for instr in instruments:
        if instr not in INSTRUMENTS:
            sys.exit("instrument inconnu du script : %s" % instr)
        plan = INSTRUMENTS[instr]["plan"]
        missing = [i for i in ids if i not in plan]
        extra = [i for i in plan if i not in ids]
        if missing or extra:
            sys.exit("ecart %s entre notes.json et le plan : manquants=%s en trop=%s"
                     % (instr, missing, extra))

    total = 0
    for instr in instruments:
        folder = INSTRUMENTS[instr]
        src_dir = os.path.join(HERE, "audio-src", instr)
        out_dir = os.path.join(HERE, "audio", instr)
        os.makedirs(out_dir, exist_ok=True)
        print("\n== %s ==" % instr)
        cache = {}
        for note_id in ids:
            base_file, semis = folder["plan"][note_id]
            if base_file not in cache:
                cache[base_file] = download(folder["base_url"], base_file, src_dir)
            generate(cache[base_file], os.path.join(out_dir, out_name(note_id)),
                     semis, args.force)
            total += 1

    print("\nOK : %d notes dans audio/" % total)


if __name__ == "__main__":
    main()

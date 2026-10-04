#!/usr/bin/env python3
"""Render lecture 1 and build its slide decks, in English and Bengali.

    python build.py                  draft render (480p, 15 fps) of every chapter, both languages
    python build.py -q p             for presenting: 1080p, 30 fps
    python build.py --lang bn        one language only (en or bn)
    python build.py --only Ch05      render only the matching chapters, then rebuild the decks
    python build.py --deck-only      rebuild the decks from what's already rendered
    python build.py --pptx           also export PowerPoint copies (without the live labs)
    python build.py --cdn            load reveal.js from the internet instead of bundling it

Quality: l 480p15 (draft), m 720p30, p 1080p30 (presenting), h 1080p60, k 4K60.

The decks land in build/deck-en/ and build/deck-bn/. Open index.html in a browser: → and ←
move between slides, ↓ opens a derivation where there is one, S opens the speaker view, F goes
full screen. Run it from anywhere; paths are relative to this file.
"""

import argparse
import os
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
FONTS = HERE.parents[1] / "kit" / "fonts"
BUILD = HERE / "build"

LANGS = {
    "en": {"title": "Lecture 1 · The Switch That Wouldn't Turn Off", "suffix": ""},
    "bn": {"title": "Lecture 1 · The Switch That Wouldn't Turn Off (বাংলা)", "suffix": "BN"},
}

# The deck, in order: ("scene", file, class) for a Manim chapter (its Bengali class is the same
# name + "BN"), ("lab", file, notes) for a live lab.
SEQUENCE = [
    ("scene", "chapters/ch00_cold_open.py", "Ch00ColdOpen"),
    ("scene", "chapters/ch01_before_the_switch.py", "Ch01BeforeTheSwitch"),
    ("scene", "chapters/ch02_accidental_transistor.py", "Ch02AccidentalTransistor"),
    ("scene", "chapters/ch03_glass.py", "Ch03Glass"),
    ("scene", "chapters/ch04_free_lunch.py", "Ch04FreeLunch"),
    ("scene", "chapters/ch05_boltzmann.py", "Ch05Boltzmann"),
    (
        "lab",
        "lab1_boltzmann.html",
        {
            "en": "Live lab. Drag the gate voltage slowly up from zero and watch electrons start "
            "to cross the hill; the dot on the right climbs one decade for every 60 mV. Then press "
            "77 K: the swing drops to about 15 mV per decade. Then raise the grip, m, to 1.4: the "
            "slope gets lazier. That's the whole chapter on one screen.",
            "bn": "এইটা live lab। Gate voltage শূন্য থেকে আস্তে আস্তে বাড়ান, দেখবেন electron-গুলা hill পার হওয়া "
            "শুরু করছে, আর ডানের dot-টা প্রতি 60 mV-তে এক decade করে উঠতেছে। এরপর 77 K চাপেন: swing নেমে "
            "আসে প্রায় 15 mV/decade-এ। তারপর grip, মানে m, বাড়ায়ে 1.4 করেন: slope-টা ঢিলা হয়ে যায়। পুরা "
            "chapter-টা এক screen-এ।",
        },
    ),
]

# Manim settings per quality. Use long options: manim-slides reads the "h" in "-qh" as its own
# -h (help) and exits without rendering.
QUALITY = {
    "l": (["--quality", "l"], "480p, 15 fps"),
    "m": (["--quality", "m"], "720p, 30 fps"),
    "p": (["--resolution", "1920,1080", "--frame_rate", "30"], "1080p, 30 fps"),
    "h": (["--quality", "h"], "1080p, 60 fps"),
    "k": (["--quality", "k"], "4K, 60 fps"),
}


def manim_slides(*args, **kw):
    return subprocess.run([sys.executable, "-m", "manim_slides", *args], cwd=HERE, **kw)


def scene_name(base, lang):
    return base + LANGS[lang]["suffix"]


def render(scene_file, scene, quality):
    log = BUILD / f"{scene}.log"
    start = time.time()
    with open(log, "w") as out:
        proc = manim_slides(
            # Each scene gets its own media folder: renders run in parallel, and a shared text
            # cache lets one process read a file another is still writing.
            "render", "--media_dir", str(BUILD / "media" / scene), *QUALITY[quality][0], scene_file, scene,
            stdout=out, stderr=subprocess.STDOUT,
        )
    took = time.time() - start
    out_json = HERE / "slides" / f"{scene}.json"
    fresh = out_json.exists() and out_json.stat().st_mtime >= start
    ok = proc.returncode == 0 and fresh
    status = "ok" if ok else f"FAILED (see {log.relative_to(HERE)})"
    print(f"  {scene:<28} {took:6.0f} s  {status}", flush=True)
    return ok


def lab_section(name, notes, lang):
    return (
        '<section class="lab" data-background-color="#0E1116">'
        f'<iframe data-src="labs/{name}?lang={lang}" title="Live lab" allow="fullscreen"></iframe>'
        f'<aside class="notes">{notes[lang]}</aside>'
        "</section>"
    )


def build_deck(lang, pptx=False, cdn=False):
    deck = BUILD / f"deck-{lang}"
    scenes = [scene_name(s[2], lang) for s in SEQUENCE if s[0] == "scene"]
    missing = [s for s in scenes if not (HERE / "slides" / f"{s}.json").exists()]
    if missing:
        sys.exit(f"Not rendered yet: {', '.join(missing)}. Run build.py without --deck-only first.")
    if deck.exists():
        shutil.rmtree(deck)
    deck.mkdir(parents=True)
    index = deck / "index.html"
    manim_slides(
        "convert", *scenes, str(index),
        "--to", "html",
        "--use-template", str(HERE / "template" / "deck.html"),
        f"-ctitle={LANGS[lang]['title']}",
        "-ccontrols=true",
        "-cprogress=true",
        "-cslide_number=c/t",
        "-chash=true",
        "-cview_distance=2",
        # Bundle reveal.js into the deck, so it presents without an internet connection.
        *([] if cdn else ["--offline"]),
        check=True,
    )
    # Put each lab after the chapter it follows. The template leaves a marker after every
    # scene: <!-- after-scene:N --> with N counting scenes from 0.
    html = index.read_text().replace("__DECK_LANG__", lang)
    labs_after = {}
    n_scene = -1
    for item in SEQUENCE:
        if item[0] == "scene":
            n_scene += 1
        else:
            labs_after.setdefault(n_scene, []).append(lab_section(item[1], item[2], lang))
    for n, sections in labs_after.items():
        marker = f"<!-- after-scene:{n} -->"
        if marker not in html:
            sys.exit(f"Template marker {marker} not found")
        html = html.replace(marker, marker + "\n" + "\n".join(sections))
    index.write_text(html)
    shutil.copytree(HERE / "labs", deck / "labs")
    shutil.copy(HERE / "template" / "speaker.html", deck / "speaker.html")
    # The fonts, so the labs and the speaker view look right offline (they look in labs/fonts/).
    (deck / "labs" / "fonts").mkdir()
    for f in [*FONTS.glob("Inter-*.ttf"), *FONTS.glob("NotoSansBengali-*.ttf"), *FONTS.glob("OFL*.txt")]:
        shutil.copy(f, deck / "labs" / "fonts" / f.name)
    print(f"Deck: {index.relative_to(HERE)}")
    if pptx:
        out = BUILD / f"lecture1-{lang}.pptx"
        manim_slides("convert", *scenes, str(out), "--to", "pptx", check=True)
        print(f"PowerPoint: {out.relative_to(HERE)}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-q", "--quality", choices=QUALITY, default="l")
    ap.add_argument("--lang", choices=["en", "bn", "both"], default="both")
    ap.add_argument("--only", nargs="*", default=None, help="render only scenes whose class name contains one of these")
    ap.add_argument("--deck-only", action="store_true")
    ap.add_argument("--pptx", action="store_true")
    ap.add_argument("--cdn", action="store_true", help="load reveal.js from the internet instead of bundling it")
    ap.add_argument("-j", "--jobs", type=int, default=os.cpu_count() or 2)
    args = ap.parse_args()
    langs = ["en", "bn"] if args.lang == "both" else [args.lang]

    BUILD.mkdir(exist_ok=True)
    if not args.deck_only:
        todo = [(s[1], scene_name(s[2], lang)) for lang in langs for s in SEQUENCE if s[0] == "scene"]
        if args.only:
            todo = [t for t in todo if any(k.lower() in t[1].lower() for k in args.only)]
        print(f"Rendering {len(todo)} scene(s) at {QUALITY[args.quality][1]}, {args.jobs} at a time:")
        with ThreadPoolExecutor(args.jobs) as pool:
            ok = list(pool.map(lambda t: render(t[0], t[1], args.quality), todo))
        if not all(ok):
            sys.exit(1)
    for lang in langs:
        build_deck(lang, pptx=args.pptx, cdn=args.cdn)


if __name__ == "__main__":
    main()

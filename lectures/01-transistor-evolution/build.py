#!/usr/bin/env python3
"""Render lecture 1 and build its slide deck.

    python build.py                  draft render (480p, 15 fps) of every chapter, then the deck
    python build.py -q m             720p 30 fps    (-q h: 1080p 60 fps, -q k: 4K)
    python build.py --only Ch05      render only the matching chapters, then rebuild the deck
    python build.py --deck-only      rebuild the deck from what's already rendered
    python build.py --pptx           also export a PowerPoint copy (without the live labs)
    python build.py --cdn            load reveal.js from the internet instead of bundling it

The deck lands in build/deck/index.html. Open it in a browser: → and ← move between slides,
↓ opens a derivation where there is one, S opens the speaker view with notes, F goes full
screen. Run it from anywhere; paths are relative to this file.
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
DECK = BUILD / "deck"
TITLE = "Lecture 1 · The Switch That Wouldn't Turn Off"

# The deck, in order: ("scene", file, class) for a Manim chapter, ("lab", file) for a live lab.
SEQUENCE = [
    ("scene", "chapters/ch00_cold_open.py", "Ch00ColdOpen"),
    ("scene", "chapters/ch05_boltzmann.py", "Ch05Boltzmann"),
    ("lab", "lab1_boltzmann.html"),
]

# Manim's quality presets. Use the long option: manim-slides reads the "h" in "-qh" as its own
# -h (help) and exits without rendering.
QUALITY = {"l": "480p, 15 fps", "m": "720p, 30 fps", "h": "1080p, 60 fps", "k": "4K, 60 fps"}


def manim_slides(*args, **kw):
    return subprocess.run([sys.executable, "-m", "manim_slides", *args], cwd=HERE, **kw)


def render(scene_file, scene, quality):
    log = BUILD / f"{scene}.log"
    start = time.time()
    with open(log, "w") as out:
        proc = manim_slides(
            "render", "--media_dir", str(BUILD / "media"), "--quality", quality, scene_file, scene,
            stdout=out, stderr=subprocess.STDOUT,
        )
    took = time.time() - start
    out_json = HERE / "slides" / f"{scene}.json"
    fresh = out_json.exists() and out_json.stat().st_mtime >= start
    ok = proc.returncode == 0 and fresh
    status = "ok" if ok else f"FAILED (see {log.relative_to(HERE)})"
    print(f"  {scene:<16} {took:6.0f} s  {status}", flush=True)
    return ok


def lab_section(name):
    return (
        '<section class="lab" data-background-color="#0E1116">'
        f'<iframe data-src="labs/{name}" title="Live lab" allow="fullscreen"></iframe>'
        "</section>"
    )


def build_deck(pptx=False, cdn=False):
    scenes = [s[2] for s in SEQUENCE if s[0] == "scene"]
    missing = [s for s in scenes if not (HERE / "slides" / f"{s}.json").exists()]
    if missing:
        sys.exit(f"Not rendered yet: {', '.join(missing)}. Run build.py without --deck-only first.")
    if DECK.exists():
        shutil.rmtree(DECK)
    DECK.mkdir(parents=True)
    index = DECK / "index.html"
    manim_slides(
        "convert", *scenes, str(index),
        "--to", "html",
        "--use-template", str(HERE / "template" / "deck.html"),
        f"-ctitle={TITLE}",
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
    html = index.read_text()
    labs_after = {}
    n_scene = -1
    for item in SEQUENCE:
        if item[0] == "scene":
            n_scene += 1
        else:
            labs_after.setdefault(n_scene, []).append(lab_section(item[1]))
    for n, sections in labs_after.items():
        marker = f"<!-- after-scene:{n} -->"
        if marker not in html:
            sys.exit(f"Template marker {marker} not found")
        html = html.replace(marker, marker + "\n" + "\n".join(sections))
    index.write_text(html)
    shutil.copytree(HERE / "labs", DECK / "labs")
    # The labs' font, so they look right offline too (lab.css looks for labs/fonts/).
    (DECK / "labs" / "fonts").mkdir()
    for f in FONTS.glob("Inter-*.ttf"):
        shutil.copy(f, DECK / "labs" / "fonts" / f.name)
    shutil.copy(FONTS / "OFL.txt", DECK / "labs" / "fonts" / "OFL.txt")
    print(f"Deck: {index.relative_to(HERE)}")
    if pptx:
        out = BUILD / "lecture1.pptx"
        manim_slides("convert", *scenes, str(out), "--to", "pptx", check=True)
        print(f"PowerPoint: {out.relative_to(HERE)}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-q", "--quality", choices=QUALITY, default="l")
    ap.add_argument("--only", nargs="*", default=None, help="render only scenes whose class name contains one of these")
    ap.add_argument("--deck-only", action="store_true")
    ap.add_argument("--pptx", action="store_true")
    ap.add_argument("--cdn", action="store_true", help="load reveal.js from the internet instead of bundling it")
    ap.add_argument("-j", "--jobs", type=int, default=max(1, (os.cpu_count() or 2) // 2))
    args = ap.parse_args()

    BUILD.mkdir(exist_ok=True)
    if not args.deck_only:
        todo = [s for s in SEQUENCE if s[0] == "scene"]
        if args.only:
            todo = [s for s in todo if any(k.lower() in s[2].lower() for k in args.only)]
        print(f"Rendering {len(todo)} chapter(s) at {QUALITY[args.quality]}, {args.jobs} at a time:")
        with ThreadPoolExecutor(args.jobs) as pool:
            ok = list(pool.map(lambda s: render(s[1], s[2], args.quality), todo))
        if not all(ok):
            sys.exit(1)
    build_deck(pptx=args.pptx, cdn=args.cdn)


if __name__ == "__main__":
    main()

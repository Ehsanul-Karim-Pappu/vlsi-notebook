#!/usr/bin/env python3
"""Render lecture 1 and build its slide deck: English slides, English and Bangla speaker notes.

    python build.py                  draft render (480p, 15 fps) of every chapter
    python build.py -q p             for presenting: 1080p, 30 fps
    python build.py --only Ch05      render only the matching chapters, then rebuild the deck
    python build.py --deck-only      rebuild the deck from what's already rendered
    python build.py --pptx           also export a PowerPoint copy (without the live labs)
    python build.py --cdn            load reveal.js from the internet instead of bundling it

Quality: l 480p15 (draft), m 720p30, p 1080p30 (presenting), h 1080p60, k 4K60.

The deck lands in build/deck/. Open index.html in a browser: → and ← move between slides, ↓
opens a derivation where there is one, S opens the speaker view, F goes full screen. Run it
from anywhere; paths are relative to this file.
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

TITLE = "Lecture 1 · The Switch That Wouldn't Turn Off"
AUTHOR = "Khandaker Ehsanul Karim"  # shown small on every slide: "Prepared by ..."
# Between a note's English and its Bangla, as kit.style.say() writes it.
BANGLA = "— বাংলা —"

# The deck, in order: ("scene", file, class) for a Manim chapter, ("lab", file, title, (English
# notes, Bangla notes)) for a live lab.
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
        "Live lab 1: Boltzmann's fence",
        (
            "Live lab. Drag the gate voltage slowly up from zero and watch electrons start "
            "to cross the hill; the dot on the right climbs one decade for every 60 mV. Then press "
            "77 K: the swing drops to about 15 mV per decade. Then raise the grip, m, to 1.4: the "
            "slope gets lazier. That's the whole chapter on one screen.",
            "এইটা live lab। Gate voltage শূন্য থেকে আস্তে আস্তে বাড়ান, দেখবেন electron-গুলা hill পার হওয়া "
            "শুরু করছে, আর ডানের dot-টা প্রতি 60 mV-তে এক decade করে উঠতেছে। এরপর 77 K চাপেন: swing নেমে "
            "আসে প্রায় 15 mV/decade-এ। তারপর grip, মানে m, বাড়ায়ে 1.4 করেন: slope-টা ঢিলা হয়ে যায়। পুরা "
            "chapter-টা এক screen-এ।",
        ),
    ),
    ("scene", "chapters/ch06_losing_grip.py", "Ch06LosingGrip"),
    (
        "lab",
        "lab2_barrier.html",
        "Live lab 2: Who controls the barrier?",
        (
            "Live lab. It opens on a planar transistor with a 30 nm gate: about four and a half "
            "lambda, in the red. Raise the drain voltage and watch the hill sink and the leakage "
            "climb. Now press FinFET: the same gate length, but lambda drops to 2.4 nm and the gate "
            "is back in control. Try the nanosheet and the 2D layer. Then press Shrink the gate and "
            "watch where each one gives up.",
            "এইটা live lab। শুরু হয় 30 nm gate-এর একটা planar transistor দিয়া: প্রায় সাড়ে চার lambda, লাল "
            "অংশে। Drain voltage বাড়ান, দেখেন hill নেমে যায় আর leakage বাড়ে। এবার FinFET চাপেন: gate length "
            "একই, কিন্তু lambda নেমে 2.4 nm, আর gate আবার control-এ। Nanosheet আর 2D layer try করেন। তারপর "
            "Shrink the gate চাপেন, দেখেন কোনটা কোথায় হাল ছাড়ে।",
        ),
    ),
    ("scene", "chapters/ch07_finfet.py", "Ch07FinFET"),
    ("scene", "chapters/ch08_nanosheet.py", "Ch08Nanosheet"),
    ("scene", "chapters/ch09_forksheet.py", "Ch09Forksheet"),
    ("scene", "chapters/ch10_cfet.py", "Ch10CFET"),
    ("scene", "chapters/ch11_beyond.py", "Ch11Beyond"),
    ("scene", "chapters/ch12_outro.py", "Ch12Outro"),
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


def lab_section(name, title, notes):
    en, bn = notes
    return (
        '<section class="lab" data-background-color="#0E1116">'
        f'<iframe data-src="labs/{name}" title="{title}" allow="fullscreen"></iframe>'
        f'<aside class="notes">{en}\n\n{BANGLA}\n\n{bn}</aside>'
        "</section>"
    )


def thumbnails(deck):
    """The last frame of every slide's video, small, for the speaker view's "Next" preview."""
    out = deck / "thumbs"
    out.mkdir()
    for video in sorted((deck / "index_assets").glob("*.mp4")):
        jpg = out / (video.stem + ".jpg")
        for seek in (["-sseof", "-0.1"], []):  # a very short clip has no 0.1 s to seek back
            subprocess.run(["ffmpeg", "-v", "error", "-y", *seek, "-i", str(video), "-frames:v", "1",
                            "-vf", "scale=640:-2", "-q:v", "4", str(jpg)], check=False)
            if jpg.exists():
                break


def build_deck(pptx=False, cdn=False):
    deck = BUILD / "deck"
    scenes = [s[2] for s in SEQUENCE if s[0] == "scene"]
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
    html = index.read_text().replace("__AUTHOR__", AUTHOR)
    labs_after = {}
    n_scene = -1
    for item in SEQUENCE:
        if item[0] == "scene":
            n_scene += 1
        else:
            labs_after.setdefault(n_scene, []).append(lab_section(*item[1:]))
    for n, sections in labs_after.items():
        marker = f"<!-- after-scene:{n} -->"
        if marker not in html:
            sys.exit(f"Template marker {marker} not found")
        html = html.replace(marker, marker + "\n" + "\n".join(sections))
    index.write_text(html)
    shutil.copytree(HERE / "labs", deck / "labs")
    shutil.copy(HERE / "template" / "speaker.html", deck / "speaker.html")
    thumbnails(deck)
    # The fonts, so the labs and the speaker view (whose notes are also in Bangla) look right
    # offline. Both look in labs/fonts/.
    (deck / "labs" / "fonts").mkdir()
    for f in [*FONTS.glob("Inter-*.ttf"), *FONTS.glob("NotoSansBengali-*.ttf"), *FONTS.glob("OFL*.txt")]:
        shutil.copy(f, deck / "labs" / "fonts" / f.name)
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
    ap.add_argument("-j", "--jobs", type=int, default=os.cpu_count() or 2)
    args = ap.parse_args()

    BUILD.mkdir(exist_ok=True)
    if not args.deck_only:
        todo = [(s[1], s[2]) for s in SEQUENCE if s[0] == "scene"]
        if args.only:
            todo = [t for t in todo if any(k.lower() in t[1].lower() for k in args.only)]
        print(f"Rendering {len(todo)} scene(s) at {QUALITY[args.quality][1]}, {args.jobs} at a time:")
        with ThreadPoolExecutor(args.jobs) as pool:
            ok = list(pool.map(lambda t: render(t[0], t[1], args.quality), todo))
        if not all(ok):
            sys.exit(1)
    build_deck(pptx=args.pptx, cdn=args.cdn)


if __name__ == "__main__":
    main()

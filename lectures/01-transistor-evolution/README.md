# Lecture 1 · The Switch That Wouldn't Turn Off

The transistor's evolution, told as one problem: turning it on is easy, but turning it *off* has
been the hard part for 100 years. From Lilienfeld's 1925 field-effect patent, through the
bipolar transistor and the MOSFET, to the FinFET, the nanosheet, the forksheet, the CFET and
what comes after. Each architecture shows up as the answer to a physics problem, with its
equations.

**Status: first sample built.** The cold open (Chapter 0), the Boltzmann chapter (Chapter 5)
and Live Lab 1 are done. The other chapters follow the storyboard in [PLAN.md](PLAN.md).

## Build the deck

Set up the tools first (see the [repository README](../../README.md#setup)), then from this
folder:

```bash
python build.py            # quick draft: 480p, 15 fps (a few minutes)
python build.py -q h       # for presenting: 1080p, 60 fps (much slower)
```

Other options: `-q m` (720p), `--only Ch05` (re-render one chapter), `--deck-only` (rebuild the
deck without rendering), `--pptx` (also export PowerPoint, without the live labs). Building the
deck downloads reveal.js once, to bundle it; `--cdn` skips that and loads it online instead.
Run `python build.py --help` for the rest.

The deck is written to `build/deck/`. Copy that whole folder to present from another machine.

## Present it

Open `build/deck/index.html` in Chrome, Edge or Firefox. Everything it needs (reveal.js, the
videos, the labs and their font) is inside `build/deck/`, so it works without an internet
connection. `--pptx` also writes `build/lecture1.pptx`, with the animations as embedded videos
but without the live labs.

| Key | Does |
|---|---|
| → / ← | next / previous slide |
| ↓ / ↑ | into / out of a derivation (where a slide says "↓ derivation") |
| Page Down / Page Up | a clicker's buttons: next / previous, skipping derivations |
| Space | pause or play the current animation |
| S | speaker view, with the script for each slide and a timer |
| F | full screen |
| Esc | overview of all slides |

Every slide's speaker notes hold the narration. In the live lab, a slider takes the arrow keys
while it has focus; click the background, or use the clicker, to move on.

## What's here

```
build.py               renders the chapters and assembles the deck
physics.py             every equation the lecture shows, as functions
chapters/              one Manim scene per chapter
labs/                  the live labs (plain HTML and JavaScript); lab-physics.js is the JS port of physics.py
template/deck.html     the reveal.js page the deck is built into
tests/test_physics.py  checks the equations, and that the labs' JS port agrees with them
references.md          a source for every date, name and number on the slides
data/, models/         FET Lab's device geometry and 3D models (see data/README.md)
```

Run the tests from the repository root:

```bash
python -m unittest discover lectures/01-transistor-evolution/tests
```

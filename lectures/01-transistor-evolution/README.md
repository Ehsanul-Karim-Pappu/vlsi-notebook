# Lecture 1 · The Switch That Wouldn't Turn Off

The transistor's evolution, told as one problem: turning it on is easy, but turning it *off* has
been the hard part for 100 years. From Lilienfeld's 1925 field-effect patent, through the
bipolar transistor and the MOSFET, to the FinFET, the nanosheet, the forksheet, the CFET and
what comes after. Each architecture shows up as the answer to a physics problem, with its
equations.

**Status: chapters 0 to 5 and Live Lab 1 are built**, in English and Bengali: the cold open,
the vacuum tube and Lilienfeld (1), the bipolar transistor (2), the oxide, the MOSFET and CMOS
(3), Moore and Dennard (4) and Boltzmann's tyranny (5). The rest follows the storyboard in
[PLAN.md](PLAN.md).

It's pitched at analog layout engineers: each chapter ties its physics to something they draw
(W and L, common-centroid pairs, taps and guard rings, threshold flavours, λ and DRC rules).

## Build the deck

Set up the tools first (see the [repository README](../../README.md#setup)), then from this
folder:

```bash
python build.py            # quick draft, both languages: 480p, 15 fps
python build.py -q p       # for presenting: 1080p, 30 fps (much slower)
```

Other options: `--lang en` or `--lang bn` (one language only), `-q m` (720p), `-q h` (1080p
at 60 fps), `--only Ch05` (re-render one chapter), `--deck-only` (rebuild the decks without
rendering), `--pptx` (also export PowerPoint, without the live labs). Building a deck downloads
reveal.js once, to bundle it; `--cdn` skips that and loads it online instead. Run
`python build.py --help` for the rest.

The decks are written to `build/deck-en/` and `build/deck-bn/`. Copy a whole folder to present
from another machine.

## Present it

Open `build/deck-en/index.html` (or `deck-bn`) in Chrome, Edge or Firefox. Everything it needs
(reveal.js, the videos, the labs and their fonts) is inside the folder, so it works without an
internet connection. `--pptx` also writes `build/lecture1-en.pptx` and `build/lecture1-bn.pptx`,
with the animations as embedded videos but without the live labs.

| Key | Does |
|---|---|
| → / ← | next / previous slide |
| ↓ / ↑ | into / out of a derivation (where a slide says "↓ derivation") |
| Page Down / Page Up | a clicker's buttons: next / previous, skipping derivations |
| Space | pause or play the current animation |
| S | speaker view (below) |
| F | full screen |
| Esc | overview of all slides |

### The speaker view

Press **S** to open it in a second window; put it on the laptop screen and the deck on the
projector. It shows the script for the current slide, what comes next, a clock and a timer,
and an **animation bar** along the bottom: it fills as the slide's animation plays, counts down
the seconds left, and turns green when the animation has finished, so you know it's safe to
move on. A looping slide (electrons jiggling while you talk) shows as a loop and can be left at
any time. The bar reads "live lab" on a lab slide.

The arrow keys, Space and Page Up/Down work in the speaker view too, and it has buttons for
back, next, into a derivation and pause. Its labels follow the deck's language.

Every slide's speaker notes hold the narration. In the live lab, a slider takes the arrow keys
while it has focus; click the background, or use the clicker, to move on.

## What's here

```
build.py               renders the chapters and assembles the deck
physics.py             every equation the lecture shows, as functions
chapters/              one Manim scene per chapter
labs/                  the live labs (plain HTML and JavaScript); lab-physics.js is the JS port of physics.py
template/deck.html     the reveal.js page the deck is built into
template/speaker.html  the speaker view (S)
tests/test_physics.py  checks the equations, and that the labs' JS port agrees with them
references.md          a source for every date, name and number on the slides
data/, models/         FET Lab's device geometry and 3D models (see data/README.md)
```

Run the tests from the repository root:

```bash
python -m unittest discover lectures/01-transistor-evolution/tests
```

# Lecture 2 · Matching and Symmetry, in Layout

For analog layout engineers: what each matching and symmetry technique does on the layout, and
what it cancels. No derivations. Every technique is shown on one of two real circuits, never on a
two-transistor example:

- a **fully differential folded-cascode OTA** with its common-mode feedback (CMFB), and
- a **bandgap reference**: a PMOS mirror, an amplifier, Q1 against an eight-unit Q2, R1 and R2.

About 45 minutes: nine chapters (some 4,600 words of notes, about 33 minutes of talk) and one live lab. The slides are in English; the speaker notes are
in English and Bangla (Bangla script, with the technical terms in English).

| # | Chapter | What it gives |
|---|---|---|
| 0 | Identical on paper | The two circuits; what a mismatch costs each, said as a bench outcome |
| 1 | What makes twins differ | Six causes (random, gradients, stress, temperature, the neighbourhood, the wiring), each on the die with what cancels it; the technique-against-cause matrix |
| 2 | Reading the OTA for matching | The matched groups, ranked by how directly their error reaches the input; the axis; the floorplan in rows |
| 3 | The input pair | Units; side by side, interdigitated, mirrored, cross-quad, and what each leaves; dummies; the tail on the axis; mirror-image wiring |
| — | Live lab: Place the units | Arrange A and B against a gradient of any angle and curvature, or click to make your own |
| 4 | Current sources and cascodes | Interleaved rows with dummies; cascodes in line; feeding the source rail (IR drop); current direction; ratios in whole units |
| 5 | The CMFB's R and C | Why R1 = R2 and C1 = C2; unit resistors interleaved; unit capacitors in a common centroid with a dummy ring |
| 6 | Routing as mirror images | The paired nets; mirror-image routes; symmetric crossings; shields; metal over devices; the extraction check |
| 7 | The bandgap | What must match, and why the amplifier's offset gets multiplied; Q1 inside Q2's eight with a dummy ring; R1 and R2 counted from one unit; the mirror; placement on the die; trimming |
| 8 | The matching review | A checklist for each circuit, the post-layout checks, and the question to ask of every technique |

The plan and storyboard are in [PLAN.md](PLAN.md); the sources in [references.md](references.md).

## Build the deck

Set up the tools first (see the [repository README](../../README.md#setup)), then from this
folder:

```bash
python build.py            # quick draft: 480p, 15 fps
python build.py -q p       # for presenting: 1080p, 30 fps
```

Other options: `-q m` (720p), `-q h` (1080p at 60 fps), `--only M03` (re-render one chapter),
`--deck-only` (rebuild the deck without rendering), `--pptx` (also export PowerPoint, to
`build/lecture2.pptx`, with the lab as a screenshot slide). Building the deck downloads reveal.js
once, to bundle it; `--cdn` skips that and loads it online instead.

The deck is written to `build/deck/index.html`. Copy that whole folder to present from another
machine; it works without an internet connection.

## Present it

Open `build/deck/index.html` in Chrome, Edge or Firefox. The keys and the speaker view (**S**)
work as in [lecture 1](../01-transistor-evolution/README.md#present-it): → / ← move on and
back, Page Down / Page Up for a clicker, Space pauses an animation, S opens the speaker view with
the script in English or Bangla (**L** flips between them) and the animation bar.

In the lab, a slider takes the arrow keys while it has focus; click the background, or use the
clicker, to move on. The arrangement buttons are named as the notes say them: Side by side,
Interdigitated, Mirrored, Cross-quad, Cross-quad + dummies, Bandgap 1 : 8.

## What's here

```
build.py               renders the chapters and assembles the deck
common.py              shared pieces: the schematic card (and rings around its devices), unit cells and
                       arrays, the illustrative gradient, centroids, unit resistors, the leftover meter
chapters/              one Manim scene per chapter (m00 to m08)
schematics/            the three circuits: cirfig_gen layouts written by build_layouts.py, their SVG
                       and PNG, and draw.py to redraw them
labs/                  the live lab (plain HTML and JavaScript)
template/              the reveal.js page and the speaker view
images/labs/           a screenshot of the lab, for PowerPoint
tests/test_lecture.py  checks the chapters, the notes, the schematics and the lab's arithmetic
PLAN.md                the plan and storyboard
references.md          the sources
```

The schematics are drawn with [cirfig_gen](https://github.com/KwantaeKim/cirfig_gen) by Kwantae
Kim (MIT licence, in `schematics/LICENSE-cirfig_gen.txt`). To redraw them, from this folder:

```bash
python schematics/build_layouts.py         # writes the JSON layouts
python schematics/draw.py ~/cirfig_gen     # renders each with your cirfig_gen clone, to SVG and PNG,
                                           # checking every wire end (needs cairosvg)
```

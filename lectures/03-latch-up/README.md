# Lecture 3 · Latch-up, in Layout

For analog and mixed-signal layout engineers: where latch-up comes from, how it fires, and why each
latch-up (LUP) rule in a DRC deck exists, so that every LUP error marker reads as a picture of the
silicon underneath, with an obvious fix.

About 45–50 minutes: nine chapters (some 4,500 words of notes, about 32 minutes of talk) and two
live labs. The slides are in English; the speaker notes are in English and Bangla (Bangla script,
with the technical terms in English).

| # | Chapter | What it gives |
|---|---|---|
| 0 | The chip that shorts itself | A bench story as a supply-current trace; the LUP section of a DRC report; the route |
| 1 | The thyristor in every inverter | The CMOS cross-section; the vertical PNP and the lateral NPN drawn over their silicon; R_well and R_sub; P-N-P-N; the SCR from VDD to VSS |
| 2 | How it fires, and why it stays on | Injectors; the loop step by step; β_npn·β_pnp > 1; the S-curve, the holding point, and the supply line |
| — | Live lab: Fire the thyristor | Tap distances, N+ to well spacing, an injection pulse and the supply: quiet, fires and lets go, or latched |
| 3 | Four knobs, four rule families | Resistance, gain, collection, distance (and many supplies), on the silicon and as rule families |
| 4 | Taps: the core rule | The rule as a voltage budget; how the deck checks it (size, subtract, flag); well-tap cells; rings and butted taps; taps that count for nothing; fixes that work |
| — | Live lab: Tap the floor | Place taps on a block from above; watch the coverage and the error markers |
| 5 | Guard rings at the I/O | Injected electrons reaching a core well; majority-carrier and minority-carrier rings; the double guard ring; the rules; mistakes that pass by eye |
| 6 | Keeping the core away from injectors | What counts as an injector; how the deck finds one; the band around the I/O; the analog pin; fixes |
| 7 | Many supplies, many wells | Well spacing across supplies; a well tied below what's inside it; floating wells; deep N-well; power-up order |
| 8 | The latch-up review | A checklist; reading a LUP report; JEDEC JESD78; the question to ask of every rule |

Rule names (LUP.TAP.1 and so on) and values are generic: real foundry decks are confidential and
differ, so every rule is tagged "typical · check your PDK". Numbers from the lecture's toy model
(`physics.py`) are tagged "toy model". The plan and storyboard are in [PLAN.md](PLAN.md); the
sources in [references.md](references.md).

## Build the deck

Set up the tools first (see the [repository README](../../README.md#setup)), then from this
folder:

```bash
python build.py            # quick draft: 480p, 15 fps
python build.py -q p       # for presenting: 1080p, 30 fps
```

Other options: `-q m` (720p), `-q h` (1080p at 60 fps), `--only X04` (re-render one chapter),
`--deck-only` (rebuild the deck without rendering), `--pptx` (also export PowerPoint, to
`build/lecture3.pptx`, with the labs as screenshot slides). Building the deck downloads
reveal.js once, to bundle it; `--cdn` skips that and loads it online instead.

The deck is written to `build/deck/index.html`. Copy that whole folder to present from another
machine; it works without an internet connection.

## Present it

Open `build/deck/index.html` in Chrome, Edge or Firefox. The keys and the speaker view (**S**)
work as in [lecture 1](../01-transistor-evolution/README.md#present-it): → / ← move on and
back, Page Down / Page Up for a clicker, Space pauses an animation, S opens the speaker view with
the script in English or Bangla (**L** flips between them) and the animation bar.

In a lab, a slider takes the arrow keys while it has focus; click the background, or use the
clicker, to move on. The buttons are named as the notes say them: in Fire the thyristor, the
supplies (0.8 V core, 1.8 V I/O, 3.3 V I/O), Inject and Power cycle; in Tap the floor, No taps,
Row ends, A fix and Wrong well.

## What's here

```
build.py               renders the chapters and assembles the deck
physics.py             the toy model of latch-up: resistances, gains, trigger and holding, the S-curve,
                       and the tap check (labs/lab-model.js is its JavaScript port)
common.py              shared pieces: the CMOS cross-section, bipolar and resistor symbols, the SCR
                       circuit, top-view taps and DRC markers, and the tags
chapters/              one Manim scene per chapter (x00 to x08)
labs/                  the two live labs (plain HTML and JavaScript)
template/              the reveal.js page and the speaker view
images/labs/           a screenshot of each lab, for PowerPoint
tests/test_lecture.py  checks the chapters and notes, the toy model, that the labs' port agrees with it,
                       and that the lab buttons match the notes
PLAN.md                the plan and storyboard
references.md          the sources
```

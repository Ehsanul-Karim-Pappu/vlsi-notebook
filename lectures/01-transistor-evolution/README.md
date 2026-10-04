# Lecture 1 · The Switch That Wouldn't Turn Off

The transistor's evolution, followed along one thread: every smaller transistor had to keep
its off state under control, while still giving enough current and fitting into a cell that can
be built. From Lilienfeld's 1925 field-effect patent, through the bipolar transistor and the
MOSFET, to the FinFET, the nanosheet, the forksheet, the CFET and what comes after. Each
architecture shows up as the answer to a physics problem, with its equations; the simple models
are labelled as models.

**Status: built.** Thirteen chapters (0 to 12): the cold open, the vacuum tube and Lilienfeld
(1), the bipolar transistor (2), the oxide, the MOSFET and CMOS (3), Moore and Dennard (4),
Boltzmann's tyranny (5), short channels and the natural length λ (6), the FinFET (7), nanosheets
and how they're made (8), the forksheet (9), the CFET with backside power (10), 2D channels and
steep-slope switches (11), and the outro (12). Five live labs: Dennard's dial after chapter 4,
Boltzmann's fence after chapter 5, who controls the barrier? after chapter 6, and build a cell
and hold it yourself (FET Lab's 3D models) after chapter 10. The full deck runs about an hour;
`core.html` is a 25-minute route through it with its own shorter script. It also exports to
PowerPoint and cuts to a continuous movie for a recorded version. An outside audit (October
2026) and what changed because of it are in [PLAN.md](PLAN.md#12-the-october-2026-audit-of-commit-c3cb12c).

It's pitched at analog layout engineers: each chapter ties its physics to something they draw
(W and L, common-centroid pairs, taps and guard rings, threshold flavours, λ and DRC rules). The
slides are in English; the speaker notes are in English and Bangla. Real photos and patent
drawings appear where the story reaches them: de Forest's triodes, ENIAC, Lilienfeld's patent, the
first transistor, Kahng's MOSFET, Wanlass's CMOS, the hand-drawn 4004 layout, the Berkeley FinFET
patent, and forksheet and CFET patents. The FinFET, nanosheet, forksheet and CFET are FET Lab's
3D models, built up layer by layer and cut open; their layouts are drawn from above, the way a
layout tool shows them.

## Build the deck

Set up the tools first (see the [repository README](../../README.md#setup)), then from this
folder:

```bash
python build.py            # quick draft: 480p, 15 fps
python build.py -q p --core   # for presenting: 1080p, 30 fps, and the 25-minute core (much slower)
```

Other options: `-q m` (720p), `-q h` (1080p at 60 fps), `--only Ch05` (re-render one
chapter), `--deck-only` (rebuild the deck without rendering), `--core` (also build the 25-minute
core deck), `--pptx` (also export PowerPoint), `--movie` (also cut a continuous movie; see below).
Building the deck downloads reveal.js once, to bundle it; `--cdn` skips that and loads it online
instead. Run `python build.py --help` for the rest.

The deck is written to `build/deck/`: `index.html` is the full lecture and `core.html` the
25-minute core, sharing the same videos. Copy that whole folder to present from another machine.

## Present it

Open `build/deck/index.html` (or `core.html`) in Chrome, Edge or Firefox. Everything it needs
(reveal.js, the videos, the labs, the 3D models and the fonts) is inside the folder, so it works
without an internet connection.

**The 25-minute core.** `core.html` keeps 69 of the full deck's slides and all five labs, with a
shorter script in both languages (about 2,800 words: some 19 minutes of talk, plus about 3 for the
labs and 2 for transitions). Which slides, and the script, are in `core.py`. Rehearse it once with
a clock; the derivations, latch-up, negative capacitance and Landauer are left for questions.

**PowerPoint.** `--pptx` writes `build/lecture1.pptx` (and `lecture1-core.pptx` with `--core`):
the animations as embedded videos, the notes in both languages, and each lab as a screenshot slide
that says where to find the live one. PowerPoint plays slides in a straight line, so the ↓
derivations sit inline. Check the videos play on the presenting machine before the talk.

**A recorded version.** `--movie` cuts the deck into one continuous movie, `build/lecture1-en.mp4`
(`--lang bn` for Bangla, `--core` for the core too), with a matching subtitle file and a narration
script, `build/narration-en.md`. The narration has to be yours: record one audio file per slide into
`narration/en/` (or `narration/en-core/`), named as the script says, and build again. Each slide then
plays its animation and holds until its recording ends. Until it has one, a slide is held for its
notes' length at 150 words a minute, silent, which is the timing to record against. For a lab, put a
screen recording of yourself working it at `narration/en/<lab name>.mp4`, with its sound, and it
replaces the screenshot.

**A synthetic English voice-over.** `voiceover.py` makes the core movie's narration with ElevenLabs
text-to-speech, from the script in `narration/en-core/manifest.csv`. The script is written to be
spoken ("k T", "four-oh-oh-four", the labs described as their screenshots), with a few of ElevenLabs'
audio tags to direct the delivery: `[curious]`, `[dry amusement]`, `[short pause]`. Eleven v4, the
default, follows them; for a model that can't, they're taken out before sending, and the subtitles
never show them. Run it on your own machine; it needs only Python 3, and the API key stays there:

```bash
export ELEVENLABS_API_KEY=...            # or leave it unset and type it when asked
python voiceover.py cost                 # what each model costs for the script, on your plan; spends nothing
python voiceover.py voices               # the voices you can use, and your credits
python voiceover.py sample <voice_id>    # one line, a few hundred characters; listen, try another
python voiceover.py make <voice_id>      # all 74 files; says the cost and asks first
```

`sample` takes `--segment <name>` for another line, `--stability` (lower is more expressive, higher
more even) and `--model`; `make` takes the same. If the script costs more than your credits,
`make --partial` makes what they cover, in order, and the same command finishes after they refill.
It writes `narration/en-core/*.mp3` and `voice.json` (the voice and settings, so a later run can't
mix in another voice), picks up where it stopped if interrupted, and never respends on a file
that's already there: delete one to remake it. Commit that folder, then
`python build.py -q p --core --movie` cuts the narrated movie, with every recording at the same
loudness and subtitles of what was said.

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
projector. It shows the script for the current slide in English or Bangla (the EN / বাংলা switch,
or **L**, flips between them), a live copy of the slide on screen ("Now") and the end of the
next one ("Next"), a clock and a timer,
and an **animation bar** along the bottom: it fills as the slide's animation plays, counts down
the seconds left, and turns green when the animation has finished, so you know it's safe to
move on. A looping slide (electrons jiggling while you talk) shows as a loop and can be left at
any time. The bar reads "live lab" on a lab slide.

The arrow keys, Space and Page Up/Down work in the speaker view too, and it has buttons for
back, next, into a derivation, pause and the notes language.

Every slide's speaker notes hold the narration. In the live lab, a slider takes the arrow keys
while it has focus; click the background, or use the clicker, to move on.

## What's here

```
build.py               renders the chapters and assembles the deck
core.py                the 25-minute core path: which slides, and their shorter script
voiceover.py           the core movie's English voice-over, with ElevenLabs (narration/en-core/)
physics.py             every equation the lecture shows, as functions
devicedata.py          loads FET Lab's device models from data/ for the chapters
chapters/              one Manim scene per chapter
labs/                  the five live labs (plain HTML and JavaScript); lab-physics.js is the JS port of
                       physics.py; lab5-models.js holds the 3D models for Lab 5 (written by build.py)
template/deck.html     the reveal.js page the deck is built into
template/speaker.html  the speaker view (S)
images/                historical photos and patent drawings, with their sources in images/CREDITS.md;
                       images/labs/ has a screenshot of each lab, for PowerPoint and the movie
tests/test_physics.py  checks the equations, that the labs' JS port agrees with them, and the core path
references.md          the sources for the slides' dates, names and numbers, with any gaps marked
narration/             narration for --movie: en-core/manifest.csv is the spoken script; the audio
                       is yours to add, recorded or from voiceover.py
data/, models/         FET Lab's device geometry and 3D models (see data/README.md)
```

Run the tests from the repository root:

```bash
python -m unittest discover lectures/01-transistor-evolution/tests
```

# kit

Code shared by every lecture, so the decks look and behave alike.

| File | What it holds |
|---|---|
| `style.py` | The palette (each colour means one thing in every lecture: electrons cyan, the gate gold, the drain red, heat orange), the fonts, text helpers, chapter cards, the timeline ribbon, and the `Chapter` mixin |
| `motifs.py` | Reusable pictures: device cross-sections (planar to CFET), the energy barrier with thermal electrons, the Boltzmann distribution |
| `devices3d.py` | Devices from box geometry in nanometres (FET Lab's format): in 3D, whole or cut open along any axis (`build_device(..., clip=...)`), and from above, as a layout tool draws them (`plan_view`) |
| `fonts/` | Inter (for the slides) and Noto Sans Bengali (for the Bangla speaker notes), both under the SIL Open Font License (`OFL.txt`, `OFL-NotoSansBengali.txt`); nothing needs installing |

A chapter imports these with `from kit.style import *`, after putting the repository root on
`sys.path` (each chapter file does this in its first lines).

## Chapters and speaker notes

Slides are in English. Speaker notes are in English and Bangla: the Bangla is the way it's
spoken in the office, in Bangla script, with the technical terms, names and units left in
English.

- `Chapter` is a mixin for a chapter's scene class: `class Ch01Foo(Chapter, Slide)`. It adds
  the helpers every chapter uses: `slide(notes)` to start a slide, `clear()`,
  `open_chapter(...)` for the chapter card and timeline, and `detour_in` / `detour_out` around
  a ↓ derivation.
- `say(en, bn)` writes a slide's notes: `self.slide(say("English…", "Bangla…"))`. It puts a
  `— বাংলা —` line between the two; the deck's speaker view splits on it and shows both.
- `figure(path, height, credit)` frames a real photo or document with its credit underneath;
  `Chapter.show_figure(notes, title, fig)` gives it a slide of its own, before the animation
  that explains it.
- `text()` and its relatives set text in Inter. `k_BT`-style subscripts in a string are
  typeset as subscripts.

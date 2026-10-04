# kit

Code shared by every lecture, so the decks look and behave alike.

| File | What it holds |
|---|---|
| `style.py` | The palette (each colour means one thing in every lecture: electrons cyan, the gate gold, the drain red, heat orange), the fonts, text helpers, chapter cards, the timeline ribbon, and the `Chapter` mixin |
| `motifs.py` | Reusable pictures: device cross-sections (planar to CFET), the energy barrier with thermal electrons, the Boltzmann distribution |
| `devices3d.py` | 3D devices from box geometry in nanometres (FET Lab's format), whole or cut away |
| `fonts/` | Inter and Noto Sans Bengali, both under the SIL Open Font License (`OFL.txt`, `OFL-NotoSansBengali.txt`); registered by `style.py`, so nothing needs installing |

A chapter imports these with `from kit.style import *`, after putting the repository root on
`sys.path` (each chapter file does this in its first lines).

## Two languages

Every lecture is built in English and in Bengali. The Bengali is the way it's spoken in the
office: Bengali script, with the technical terms, names and units left in English.

- `tr(en, bn)` returns the string for the current language. Write both side by side wherever
  text appears on screen or in the speaker notes.
- `Chapter` is a mixin for a chapter's scene class: `class Ch01Foo(Chapter, Slide)`. It sets
  the language from the class's `LANG` (`"en"` by default) and adds the helpers every chapter
  uses: `slide(notes)` to start a slide, `clear()`, `open_chapter(...)` for the chapter card
  and timeline, and `detour_in` / `detour_out` around a ↓ derivation.
- The Bengali scene is the English class with `LANG = "bn"` and the suffix `BN`:
  `class Ch01FooBN(Ch01Foo): LANG = "bn"`. A lecture's `build.py` renders both.
- `text()` and its relatives use Inter for Latin and fall back to Noto Sans Bengali for
  Bengali. `k_BT`-style subscripts in a string are typeset as subscripts.

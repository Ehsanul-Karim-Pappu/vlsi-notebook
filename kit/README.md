# kit

Code shared by every lecture, so the decks look and behave alike.

| File | What it holds |
|---|---|
| `style.py` | The palette (each colour means one thing in every lecture: electrons cyan, the gate gold, the drain red, heat orange), the Inter fonts, text helpers, chapter cards, the timeline ribbon |
| `motifs.py` | Reusable pictures: device cross-sections (planar to CFET), the energy barrier with thermal electrons, the Boltzmann distribution |
| `devices3d.py` | 3D devices from box geometry in nanometres (FET Lab's format), whole or cut away |
| `fonts/` | Inter, under the SIL Open Font License (`OFL.txt`); registered by `style.py`, so nothing needs installing |

A chapter imports these with `from kit.style import *`, after putting the repository root on
`sys.path` (each chapter file does this in its first lines).

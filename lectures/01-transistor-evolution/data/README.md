# Data and models from FET Lab

These files are copied unchanged from [FET Lab](https://github.com/Ehsanul-Karim-Pappu/fet-lab)
at commit `f1488dc`, under its MIT licence (Copyright (c) 2026 Khandaker Ehsanul Karim). The
deck uses them so its devices match the app's.

| File | What the deck uses it for |
|---|---|
| `data/geometry.json` | The nanosheet's boxes in nanometres, and the material colours |
| `data/devices.json` | The FinFET, nanosheet, forksheet and CFET models, built as 3D in Manim |
| `data/process.json` | Not read by the deck. Kept for reference: chapter 8's process animation is drawn by hand, after the same IBM route (its nFET branch, with bottom isolation) |
| `data/references.json` | Not read by the deck. Kept for reference; the deck's sources are in `references.md` |
| `models/show_*.glb`, `models/cfet_*.glb` | The 3D models you can rotate on the slides (Lab 5) |

If FET Lab's models change, copy the files again from its `data/` and `models/` folders.

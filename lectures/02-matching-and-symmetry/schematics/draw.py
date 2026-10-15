#!/usr/bin/env python3
"""Draw this lecture's schematics again, after changing a layout JSON here (or build_layouts.py).

    python schematics/draw.py ~/cirfig_gen       # the cirfig_gen clone to draw with

Each <name>.json is a cirfig_gen layout (github.com/KwantaeKim/cirfig_gen, MIT licence): its
tools/render.py turns it into <name>.svg and checks every wire end. This script then makes
<name>.png, the SVG at three times its size on a transparent background, which the slides show
on a paper-coloured card. Needs cairosvg (pip install cairosvg) and cirfig_gen's
tools/glyphs.json (its tools/make_glyphs.py builds it; these were drawn with Nimbus Sans
Narrow, metric-compatible with its reference font, Arial Narrow).
"""

import subprocess
import sys
from pathlib import Path

import cairosvg

HERE = Path(__file__).resolve().parent


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    cirfig = Path(sys.argv[1]).expanduser().resolve()
    for layout in sorted(HERE.glob("*.json")):
        subprocess.run([sys.executable, "tools/render.py", str(layout)], cwd=cirfig, check=True)
        svg = layout.with_suffix(".svg")
        cairosvg.svg2png(url=str(svg), write_to=str(layout.with_suffix(".png")), scale=3)
        print(f"  {svg.name} and {layout.with_suffix('.png').name}")


if __name__ == "__main__":
    main()

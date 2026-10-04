# VLSI Notebook

VLSI lectures and study notes, from transistor physics to analog layout and circuit design.
Animated slides built with Manim, with live simulations and the theory behind every step.

## Lectures

| # | Lecture | Status |
|---|---|---|
| 1 | [The Switch That Wouldn't Turn Off](lectures/01-transistor-evolution/): the transistor from Lilienfeld's 1925 patent to the MOSFET, FinFET, nanosheet, forksheet, CFET and beyond | Planning |
| 2 | Analog layout | Planned |
| 3 | Analog building blocks, with simulation | Planned |

Each lecture is an animated, presenter-paced slide deck built with
[Manim](https://www.manim.community/) and [manim-slides](https://github.com/jeertmans/manim-slides).
It exports to a browser deck (with speaker notes) and to PowerPoint.

## Notes

Study notes live in [notes/](notes/), one folder per topic.

## Layout

```
kit/          shared by every lecture: style, colours, animation helpers
lectures/     one folder per lecture, each with its own plan, data and slides
notes/        study notes
```

## Setup

You need Python 3.10 or newer, FFmpeg, Cairo and Pango (for Manim's text) and a LaTeX
distribution (for the equations).

On Ubuntu or Debian (this is the setup the toolchain was tested with):

```bash
sudo apt-get update
sudo apt-get install -y libpango1.0-dev pkg-config ffmpeg \
  texlive-latex-base texlive-latex-extra texlive-fonts-recommended texlive-science \
  dvisvgm cm-super
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

On macOS or Windows, follow Manim's
[installation guide](https://docs.manim.community/en/stable/installation.html) for the system
packages and LaTeX, then run `pip install -r requirements.txt`.

## Credits

Lecture 1's device geometry, process steps, references and 3D models come from
[FET Lab](https://github.com/Ehsanul-Karim-Pappu/fet-lab) (MIT licence). See
[its data notes](lectures/01-transistor-evolution/data/README.md).

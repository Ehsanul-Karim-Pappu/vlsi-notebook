# VLSI Notebook

VLSI lectures and study notes, from transistor physics to analog layout and circuit design.
Animated slides built with Manim, with live simulations and the theory behind every step.

## Lectures

| # | Lecture | Status |
|---|---|---|
| 1 | [The Switch That Wouldn't Turn Off](lectures/01-transistor-evolution/): the transistor from Lilienfeld's 1925 patent to the MOSFET, FinFET, nanosheet, forksheet, CFET and beyond | Chapters 0–5 and Live Lab 1 |
| 2 | Analog layout | Planned |
| 3 | Analog building blocks, with simulation | Planned |

Each lecture is an animated, presenter-paced slide deck built with
[Manim](https://www.manim.community/) and [manim-slides](https://github.com/jeertmans/manim-slides).
It exports to a browser deck, with a speaker view that shows the script and how long each
animation has left, and to PowerPoint. The slides are in English; the speaker notes are in
English and Bangla (Bangla script, with the technical terms in English).

## Notes

Study notes live in [notes/](notes/), one folder per topic.

## Layout

```
kit/          shared by every lecture: style, colours, fonts, animation helpers, speaker notes
lectures/     one folder per lecture, each with its own plan, data, slides and labs
notes/        study notes
```

To build a lecture, see its README, for example
[lecture 1](lectures/01-transistor-evolution/README.md#build-the-deck).

## Setup

You need Python 3.11 or newer, FFmpeg, Cairo and Pango (for Manim's text) and a LaTeX
distribution with dvisvgm (for the equations).

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

On AlmaLinux, Rocky or RHEL 9 (not tested here; FFmpeg comes from RPM Fusion):

```bash
sudo dnf install -y epel-release
sudo dnf config-manager --set-enabled crb
sudo dnf install -y https://mirrors.rpmfusion.org/free/el/rpmfusion-free-release-9.noarch.rpm
sudo dnf install -y python3.12 python3.12-devel gcc pkgconf-pkg-config cairo-devel pango-devel ffmpeg \
  texlive-collection-latexrecommended texlive-collection-fontsrecommended texlive-babel-english texlive-dvisvgm
python3.12 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

If an equation fails to render with a missing LaTeX package, install it as `texlive-<name>`.

On macOS or Windows, follow Manim's
[installation guide](https://docs.manim.community/en/stable/installation.html) for the system
packages and LaTeX, then run `pip install -r requirements.txt`.

## Credits

Lecture 1's device geometry, process steps, references and 3D models come from
[FET Lab](https://github.com/Ehsanul-Karim-Pappu/fet-lab) (MIT licence). See
[its data notes](lectures/01-transistor-evolution/data/README.md).

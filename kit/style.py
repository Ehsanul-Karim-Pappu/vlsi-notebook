"""The look shared by every lecture: colours, fonts and the recurring on-screen pieces.

Import it before building any mobject (``from kit.style import *``). It registers the bundled
Inter fonts and sets Manim's background, so every deck renders the same on any machine.
"""

from pathlib import Path

import manimpango
from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    Line,
    MarkupText,
    RoundedRectangle,
    Text,
    Triangle,
    VGroup,
    config,
)

FONTS = Path(__file__).parent / "fonts"
for _font in sorted(FONTS.glob("*.ttf")):
    manimpango.register_font(str(_font))

BODY = "Inter"
DISPLAY = "Inter Display"

# --- palette -------------------------------------------------------------------------------
# Neutrals
BG = "#0E1116"
INK = "#ECE8E1"
MUTED = "#8A8F98"
FAINT = "#3A3F47"
PANEL = "#171B22"

# Physics colours: fixed for the whole series, so a colour always means the same thing.
ELECTRON = "#4FC7D8"  # electrons, n-type, conduction band
HOLE = "#E05A9C"  # holes, p-type, valence band
GATE = "#F2B84B"  # the gate, its field, and the barrier it controls
DRAIN = "#E8553E"  # the drain and anything it does to the channel
THERMAL = "#FF8C42"  # k_B T, heat, power
GOOD = "#7BD389"
BAD = DRAIN

# Materials, as in FET Lab, plus lighter tints that stay readable as text on BG.
SILICON = "#F2C2CF"
SUBSTRATE = "#4E4148"  # bulk silicon, drawn darker so the channel stands out
OXIDE = "#8C1C13"
OXIDE_TEXT = "#E07A5F"
HIGHK = "#BE8250"
NITRIDE = "#E4AE1B"
METAL = "#B8BCC6"
WALL = "#9AA3AF"

config.background_color = BG


# --- text ----------------------------------------------------------------------------------
def text(s, size=32, color=INK, weight="NORMAL", font=BODY, **kw):
    """Body text in Inter."""
    return Text(s, font=font, font_size=size, color=color, weight=weight, **kw)


def rich(s, size=32, color=INK, weight="NORMAL", **kw):
    """Body text with Pango markup, for subscripts such as V<sub>DD</sub>."""
    return MarkupText(s, font=BODY, font_size=size, color=color, weight=weight, **kw)


def display(s, size=72, color=INK, weight="BOLD", **kw):
    """Large titles and numbers in Inter Display."""
    return Text(s, font=DISPLAY, font_size=size, color=color, weight=weight, **kw)


def kicker(s, size=20, color=MUTED, spacing=4000):
    """Small, letter-spaced capitals for labels such as CHAPTER 5."""
    return MarkupText(
        f'<span letter_spacing="{spacing}">{s.upper()}</span>',
        font=BODY,
        font_size=size,
        color=color,
        weight="MEDIUM",
    )


def pill(s, color=MUTED, size=18):
    """A rounded tag, used to mark a figure as a "model" or "illustrative"."""
    label = text(s, size=size, color=color, weight="MEDIUM")
    box = RoundedRectangle(
        width=label.width + 0.3,
        height=label.height + 0.2,
        corner_radius=0.12,
        stroke_color=color,
        stroke_width=1.5,
    )
    return VGroup(box, label.move_to(box))


def source(s, size=16):
    """A source line, shown bottom right like a documentary caption."""
    return text(s, size=size, color=MUTED).to_corner(DOWN + RIGHT, buff=0.3)


# --- recurring pieces ----------------------------------------------------------------------
class Timeline(VGroup):
    """A thin ribbon from START to END with a marker that slides from chapter to chapter."""

    START, END = 1920, 2050

    def __init__(self, year, width=11.0, ticks=(1925, 1950, 1975, 2000, 2025, 2045), **kw):
        super().__init__(**kw)
        self.width_ = width
        self.line = Line(LEFT * width / 2, RIGHT * width / 2, stroke_color=FAINT, stroke_width=2)
        self.add(self.line)
        for y in ticks:
            p = self.point(y)
            tick = Line(p + UP * 0.06, p + DOWN * 0.06, stroke_color=MUTED, stroke_width=2)
            label = text(str(y), size=16, color=MUTED).next_to(tick, DOWN, buff=0.1)
            self.add(tick, label)
        self.marker = Triangle(fill_color=GATE, fill_opacity=1, stroke_width=0)
        self.marker.scale(0.09).rotate(3.14159).move_to(self.point(year) + UP * 0.16)
        self.add(self.marker)

    def point(self, year):
        f = (year - self.START) / (self.END - self.START)
        return self.line.get_start() + (self.line.get_end() - self.line.get_start()) * f

    def marker_to(self, year):
        """Animation that slides the marker to YEAR."""
        return self.marker.animate.move_to(self.point(year) + UP * 0.16)


def chapter_card(number, year, title, hook):
    """The card that opens each chapter: chapter number, a giant year, the title and a hook."""
    num = kicker(f"Chapter {number}", color=GATE)
    big = display(str(year), size=150, color=FAINT)
    ttl = display(title, size=60)
    sub = text(hook, size=28, color=MUTED, slant="ITALIC")
    card = VGroup(num, big, ttl, sub).arrange(DOWN, buff=0.25)
    big.shift(UP * 0.1)
    return card.move_to(ORIGIN + UP * 0.3)

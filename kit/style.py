"""The look shared by every lecture: colours, fonts, speaker notes and the recurring pieces.

Import it before building any mobject (``from kit.style import *``). It registers the bundled
Inter fonts and sets Manim's background, so every deck renders the same on any machine.

Slides are in English. Speaker notes are in English and Bangla: write each slide's notes as
``say("English", "Bangla")``, and the speaker view shows both. The Bangla is spoken Bangla, as
it would be said in the office, in Bangla script, with every technical term, name, number and
unit kept in English: "gate voltage বাড়াইলে barrier নিচে নামে".
"""

import re
import textwrap
from pathlib import Path

import manimpango
from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    FadeIn,
    FadeOut,
    Group,
    ImageMobject,
    Line,
    MathTex,
    MarkupText,
    RoundedRectangle,
    SurroundingRectangle,
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
# Manim looks every font up in the installed-font list each time it makes text. The fonts are
# registered above, so skip the lookup: it slows down text that is redrawn every frame.
Text.set_default(warn_missing_font=False)
MarkupText.set_default(warn_missing_font=False)

# --- speaker notes -------------------------------------------------------------------------
# The line between a note's English and its Bangla. The deck's speaker view splits on it.
BANGLA = "— বাংলা —"


def say(en, bn):
    """A slide's speaker notes: the English, then the Bangla."""
    return f"{textwrap.dedent(en).strip()}\n\n{BANGLA}\n\n{textwrap.dedent(bn).strip()}"


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
NWELL = "#3E6A52"  # n-well, in the layout views
PSUB = "#4E4148"

config.background_color = BG


# --- text ----------------------------------------------------------------------------------
_SUB = re.compile(r"([A-Za-zφψβμΦΨΔ])_([A-Za-z0-9]+)")


def _subscripts(s):
    """'V_DD' -> 'V<sub>DD</sub>' (and 'k_BT' -> 'k<sub>B</sub>T'), for Pango markup."""
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = s.replace("k_BT", "k<sub>B</sub>T")
    return _SUB.sub(r"\1<sub>\2</sub>", s)


def text(s, size=32, color=INK, weight="NORMAL", font=BODY, **kw):
    """Body text. Symbols written like V_DD or k_BT get real subscripts."""
    if _SUB.search(s):
        return MarkupText(_subscripts(s), font=font, font_size=size, color=color, weight=weight, **kw)
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


def heading(s, size=40):
    """A slide's title, top centre."""
    return text(s, size=size, weight="SEMIBOLD").to_edge(UP, buff=0.4)


def rheading(s, size=40):
    """A heading with markup, for subscripts."""
    return rich(s, size=size, weight="SEMIBOLD").to_edge(UP, buff=0.4)


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


def model_tag():
    return pill("model")


def source(s, size=16):
    """A source line, shown bottom right like a documentary caption."""
    return text(s, size=size, color=MUTED).to_corner(DOWN + RIGHT, buff=0.3)


def wrap(s, width):
    """Break a string into lines of at most WIDTH characters."""
    return "\n".join(textwrap.wrap(s, width))


def figure(path, height, credit, max_width=None):
    """A real photo or document, in a thin frame, with its credit underneath."""
    img = ImageMobject(str(path)).scale_to_fit_height(height)
    if max_width and img.width > max_width:
        img.scale_to_fit_width(max_width)
    frame = SurroundingRectangle(img, buff=0, stroke_color=FAINT, stroke_width=2)
    cap = text(credit, size=14, color=MUTED).next_to(img, DOWN, buff=0.12)
    return Group(img, frame, cap)


def layout_note(s, size=24, width=60):
    """A gold-edged aside that ties the physics to layout work ("In your layout: ..."),
    wrapped to WIDTH characters."""
    label = text("In your layout", size=size - 4, color=GATE, weight="SEMIBOLD")
    body = text(wrap(s, width), size=size, color=INK)
    words = VGroup(label, body).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    bar = Line(words.get_corner(UP + LEFT) + LEFT * 0.2, words.get_corner(DOWN + LEFT) + LEFT * 0.2,
               stroke_color=GATE, stroke_width=4)
    return VGroup(bar, words)


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
    n = kicker(f"Chapter {number}", color=GATE)
    big = display(str(year), size=150, color=FAINT)
    ttl = display(title, size=60)
    sub = text(hook, size=28, color=MUTED, slant="ITALIC")
    card = VGroup(n, big, ttl, sub).arrange(DOWN, buff=0.25)
    big.shift(UP * 0.1)
    return card.move_to(ORIGIN + UP * 0.3)


# --- chapters ------------------------------------------------------------------------------
class Chapter:
    """Mix into a manim-slides Slide (or ThreeDSlide) to give every chapter the same slide
    helpers: ``class Ch05Boltzmann(Chapter, Slide): ...``"""

    def slide(self, notes="", **kw):
        """Start a slide, with its notes from say(). manim-slides gives a slide the options
        passed to the next_slide() call that opens it, so the notes sit above the animations
        they describe."""
        self.next_slide(notes=notes, **kw)

    def show_figure(self, notes, title, fig, clear=None):
        """A slide for a real photo or document (see figure()). Returns the title and the
        figure: the next slide keeps the title and fades the figure out."""
        self.slide(notes)
        if clear is not None:
            self.play(FadeOut(clear))
        t = heading(title)
        self.play(FadeIn(t), FadeIn(fig, shift=UP * 0.15))
        return t, fig

    def clear(self, run_time=1.0):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=run_time)

    def detour_in(self, screen):
        """Clear the slide for a ↓ derivation. FadeOut/FadeIn, not set_opacity: setting the
        opacity back to 1 would also fill every outline shape."""
        self.play(FadeOut(screen))

    def detour_out(self, screen, *shown):
        self.play(*[FadeOut(m) for m in shown], FadeIn(screen))

    def open_chapter(self, number, year, from_year, title, hook):
        """Play the chapter card: the timeline marker slides from the last chapter's year to
        this one's. Leaves the card on screen; the next slide clears it."""
        tl = Timeline(from_year).to_edge(DOWN, buff=0.45)
        card = chapter_card(number, year, title, hook)
        self.play(FadeIn(tl), FadeIn(card, shift=UP * 0.2), run_time=1.2)
        if from_year != year:
            self.play(tl.marker_to(year), run_time=1.2)
        return VGroup(tl, card)


def eq(*parts, size=44, color=INK, **kw):
    """A formula in LaTeX, split into parts so each can take its own colour."""
    return MathTex(*parts, font_size=size, color=color, **kw)

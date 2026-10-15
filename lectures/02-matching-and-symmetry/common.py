"""Pieces this lecture's chapters share: the two circuits on paper cards (and a way to point at a
device on them), the unit cells that matched devices are built from, gradients across a row, and
centroids.

The colours: device A cyan, device B gold, a third device magenta, dummies grey. A gradient runs
from blue (low) to orange (high).
"""

import json
import re
from pathlib import Path

import numpy as np
from manim import (DOWN, LEFT, RIGHT, UP, Circle, Group, ImageMobject, Line, Rectangle, RoundedRectangle,
                   Square, VGroup, interpolate_color, ManimColor)

from kit.style import ELECTRON, FAINT, GATE, GOOD, HOLE, INK, MUTED, PANEL, THERMAL, display, kicker, pill, text

LECTURE = Path(__file__).resolve().parent
SCHEMATICS = LECTURE / "schematics"
PAPER = "#E9E4DA"  # the schematic card, in the paper tone the series uses for drawings

A_COL, B_COL, C_COL, DUMMY = ELECTRON, GATE, HOLE, FAINT
COLD, HOT = "#3D6FB6", THERMAL
METAL_C = "#B8BCC6"  # contact heads, the kit's metal grey
COLOURS = {"A": A_COL, "B": B_COL, "C": C_COL, "D": DUMMY}


# --- the circuits ----------------------------------------------------------------------------
class Schematic(Group):
    """A cirfig_gen schematic (schematics/<name>.png) on a paper card. point(x, y) gives the
    scene position of a point in the schematic's own coordinates (its JSON, in pt), so a slide
    can ring a device or a net."""

    def __init__(self, name, height, credit=True):
        svg = (SCHEMATICS / f"{name}.svg").read_text()
        self.vx, self.vy, self.vw, self.vh = (float(v) for v in re.search(r'viewBox="([-\d.]+) ([-\d.]+) ([\d.]+) ([\d.]+)"', svg).groups())
        self.layout = json.loads((SCHEMATICS / f"{name}.json").read_text())
        img = ImageMobject(str(SCHEMATICS / f"{name}.png")).scale_to_fit_height(height)
        card = RoundedRectangle(width=img.width + 0.4, height=img.height + 0.4, corner_radius=0.12,
                                fill_color=PAPER, fill_opacity=1, stroke_width=0)
        super().__init__(card, img.move_to(card))
        self.img = img
        if credit:
            self.add(text("drawn with cirfig_gen", size=13, color=MUTED).next_to(card, DOWN, buff=0.08))

    def point(self, x, y):
        s = self.img.height / self.vh
        c = self.img.get_center()
        return c + np.array([(x - self.vx - self.vw / 2) * s, -(y - self.vy - self.vh / 2) * s, 0])

    def ring(self, ids, color, pad=4.0, width=4):
        """A rounded box around the symbols with these ids (from the schematic's JSON)."""
        boxes = [(s["left"], s["top"], s["left"] + SIZE[s["type"]][0], s["top"] + SIZE[s["type"]][1])
                 for s in self.layout["symbols"] if s["id"] in ids]
        x0, y0 = min(b[0] for b in boxes) - pad, min(b[1] for b in boxes) - pad
        x1, y1 = max(b[2] for b in boxes) + pad, max(b[3] for b in boxes) + pad
        a, b = self.point(x0, y0), self.point(x1, y1)
        r = RoundedRectangle(width=abs(b[0] - a[0]), height=abs(b[1] - a[1]), corner_radius=0.08,
                             stroke_color=color, stroke_width=width, fill_opacity=0)
        return r.move_to((a + b) / 2)


# cirfig_gen's symbol sizes, in pt
SIZE = {"NMOS": (39.40, 56.60), "PMOS": (39.38, 56.56), "PNP": (42.01, 53.36), "Amp": (72.52, 57.65),
        "Resistor": (34.90, 16.60), "Capacitor": (36.40, 20.50), "Voltage Node": (12.60, 12.60),
        "VDD": (22.90, 16.70), "GND": (14.80, 14.60)}


# --- unit cells and arrays ---------------------------------------------------------------------
def unit(label, size=0.62, fill=0.28):
    """One unit device: a square in its device's colour, its letter in the middle."""
    color = COLOURS.get(label, MUTED)
    sq = Square(side_length=size, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=fill)
    if label == "D":
        sq.set_stroke(opacity=0.8).set_fill(opacity=0.15)
        mark = text("d", size=int(size * 30), color=MUTED)
    else:
        mark = text(label, size=int(size * 40), color=color, weight="BOLD")
    return VGroup(sq, mark.move_to(sq))


def array(rows, size=0.62, gap=0.1):
    """Unit cells from strings, one per row ("DABBAD"); spaces leave a gap. Returns the group;
    each cell remembers its label and its grid position."""
    g = VGroup()
    step = size + gap
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch == " ":
                continue
            u = unit(ch, size)
            u.move_to([c * step, -r * step, 0])
            u.label, u.rc = ch, (r, c)
            g.add(u)
    return g


def stripe(label, height=2.2, width=0.34):
    """One unit resistor: a body in its device's colour and a contact head at each end."""
    color = COLOURS.get(label, MUTED)
    body = Rectangle(width=width, height=height, stroke_color=color, stroke_width=2.5, fill_color=color,
                     fill_opacity=0.15 if label == "D" else 0.3)
    heads = VGroup(*[Rectangle(width=width, height=0.22, stroke_width=0, fill_color=METAL_C, fill_opacity=0.9)
                     .move_to(body.get_edge_center(d) - d * 0.11) for d in (UP, DOWN)])
    g = VGroup(body, heads)
    g.label = label
    return g


def centroid(cells, label):
    pts = [c.get_center() for c in cells if getattr(c, "label", None) == label]
    return np.mean(pts, axis=0) if pts else None


def centroid_mark(point, color, size=0.18):
    """A ringed cross at a device's centroid."""
    ring = Circle(radius=size, stroke_color=color, stroke_width=4)
    cross = VGroup(Line(LEFT * size * 1.6, RIGHT * size * 1.6, stroke_color=color, stroke_width=3),
                   Line(DOWN * size * 1.6, UP * size * 1.6, stroke_color=color, stroke_width=3))
    return VGroup(ring, cross).move_to(point)


def gradient(width, height, angle=0.0, curvature=0.0, cells=26, opacity=0.55):
    """An illustrative process gradient behind an array, from COLD to HOT along ANGLE (radians,
    0 = left to right), bent into a bowl by CURVATURE. Its values match field_value()."""
    g = VGroup()
    nx = cells
    ny = max(1, round(cells * height / width))
    w, h = width / nx, height / ny
    for i in range(nx):
        for j in range(ny):
            x, y = -width / 2 + (i + 0.5) * w, -height / 2 + (j + 0.5) * h
            v = float(np.clip(field_value((x, y), (0, 0), width, angle, curvature, height), 0, 1))
            r = Rectangle(width=w * 1.02, height=h * 1.02, stroke_width=0,
                          fill_color=interpolate_color(ManimColor(COLD), ManimColor(HOT), v), fill_opacity=opacity)
            g.add(r.move_to([x, y, 0]))
    return g


def field_value(point, centre, width, angle=0.0, curvature=0.0, height=None):
    """The illustrative gradient's value (0 to 1) at a scene point, matching gradient()."""
    height = height or width
    d = np.array([np.cos(angle), np.sin(angle)])
    x, y = point[0] - centre[0], point[1] - centre[1]
    v = (x * d[0] + y * d[1]) / (0.5 * (width * abs(d[0]) + height * abs(d[1])) + 1e-9)
    return 0.5 + 0.5 * v + curvature * ((x / width) ** 2 + (y / height) ** 2)


def placed(rows, angle=0.0, curvature=0.0, size=0.62, gap=0.1, margin=0.5, marks=True):
    """An arrangement of units over an illustrative gradient, with A's and B's centroids marked.
    The group's .error is how far apart A's and B's average gradient values are (0 to 1 of the
    gradient's full swing); .cells, .field and .marks are its parts."""
    cells = array(rows, size, gap)
    centre = cells.get_center()
    w, h = cells.width + 2 * margin, cells.height + 2 * margin
    field = gradient(w, h, angle, curvature, cells=30).move_to(centre)
    vals = {}
    for c in cells:
        vals.setdefault(c.label, []).append(field_value(c.get_center(), centre, w, angle, curvature, h))
    g = VGroup(field, cells)
    g.error = abs(np.mean(vals.get("A", [0])) - np.mean(vals.get("B", [0])))
    g.field, g.cells, g.marks = field, cells, VGroup()
    if marks:
        for label, color in (("A", A_COL), ("B", B_COL)):
            pt = centroid(cells, label)
            if pt is not None:
                g.marks.add(centroid_mark(pt, color, 0.14))
        g.add(g.marks)
    return g


def meter(fraction, width=3.2, label="left over", color=None):
    """A horizontal bar showing what's left of a mismatch (1 = all of it)."""
    fraction = float(np.clip(fraction, 0, 1))
    color = color or (GOOD if fraction < 0.05 else GATE if fraction < 0.5 else THERMAL)
    track = RoundedRectangle(width=width, height=0.22, corner_radius=0.11, stroke_width=0, fill_color=FAINT, fill_opacity=1)
    bar = RoundedRectangle(width=max(width * fraction, 0.02), height=0.22, corner_radius=0.11, stroke_width=0,
                           fill_color=color, fill_opacity=1).align_to(track, LEFT)
    words = text(f"{label}: {round(100 * fraction)} %", size=20, color=color).next_to(track, UP, buff=0.12).align_to(track, LEFT)
    return VGroup(track, bar, words)


def chapter_title(n, title, sub):
    return VGroup(kicker(f"Chapter {n}", color=GATE), display(str(n), size=150, color=FAINT), display(title, size=56),
                  text(sub, size=28, color=MUTED, slant="ITALIC")).arrange(DOWN, buff=0.25).move_to(UP * 0.2)


# --- text pieces ---------------------------------------------------------------------------------
def pdk_tag():
    return pill("typical · check your PDK", color=MUTED, size=16)


def illustrative():
    return text("illustrative", size=16, color=MUTED)


def card_box(head, body, width=4.0, height=3.4, head_size=26, head_color=GATE):
    content = VGroup(text(head, size=head_size, weight="SEMIBOLD", color=head_color), *body).arrange(DOWN, buff=0.25)
    frame = RoundedRectangle(width=width, height=height, corner_radius=0.15, fill_color=PANEL, fill_opacity=1,
                             stroke_color=FAINT, stroke_width=2)
    return VGroup(frame, content.move_to(frame))


def table(rows, col_w, size=22, head_color=GATE, row_gap=0.3):
    """Rows of text in fixed columns; the first row is the header, the first column muted."""
    lines = VGroup()
    for i, row in enumerate(rows):
        cells = VGroup()
        for j, s in enumerate(row):
            color = head_color if i == 0 else (MUTED if j == 0 else INK)
            cells.add(text(s, size=size, color=color, weight="SEMIBOLD" if i == 0 else "NORMAL"))
        lines.add(cells)
    lines.arrange(DOWN, aligned_edge=LEFT, buff=row_gap)
    left = lines.get_left()[0]
    for row in lines:
        x = left
        for t, w in zip(row, col_w):
            t.move_to([x + t.width / 2, row.get_center()[1], 0])
            x += w
    y = lines[0].get_bottom()[1] - row_gap / 2
    rule = Line([left, y, 0], [left + sum(col_w) - 0.3, y, 0], stroke_color=FAINT, stroke_width=2)
    return VGroup(lines, rule)

"""Pieces the layout edition's chapters share: layer colours, the schematic card, a planar
MOSFET drawn the way a layout tool shows it, and the tags that mark what a PDK decides.

The layer colours are FET Lab's layout colours (data/devices.json), so the planar drawings here
match the FinFET, nanosheet, forksheet and CFET layouts that come from FET Lab's models.
"""

from pathlib import Path

from manim import DOWN, LEFT, Group, ImageMobject, Line, Rectangle, RoundedRectangle, VGroup

from kit.style import FAINT, INK, MUTED, PANEL, pill, text

SCHEMATICS = Path(__file__).resolve().parent / "schematics"
PAPER = "#E9E4DA"  # the schematic card: the same paper tone as the full lecture's patent drawings

# FET Lab's layout colours.
ACTIVE = "#C08A2E"  # active area: diffusion, fins, sheets ("nanowire" in FET Lab's layouts)
POLY = "#3B41CF"  # the gate
CONTACT = "#4FAE4F"  # contacts to the source and drain (MD)
VIA = "#8E1C1C"  # contact to metal
GATE_VIA = "#F5E93B"  # gate contact
METAL = "#F2C1A2"  # first metal
NWELL = "#EFE53A"
PWELL = "#7FC9EA"
NPLUS = "#4FC7D8"  # n+ source and drain, in the cross-sections (the kit's electron colour)


def schematic(name, height, credit=True):
    """A cirfig_gen schematic (layout/schematics/<name>.png) on a paper card."""
    img = ImageMobject(str(SCHEMATICS / f"{name}.png")).scale_to_fit_height(height)
    card = RoundedRectangle(width=img.width + 0.5, height=img.height + 0.5, corner_radius=0.12,
                            fill_color=PAPER, fill_opacity=1, stroke_width=0)
    group = Group(card, img.move_to(card))
    if credit:
        group.add(text("drawn with cirfig_gen", size=13, color=MUTED).next_to(card, DOWN, buff=0.08))
    return group


def pdk_tag():
    """Marks a statement as typical, not universal: the PDK decides."""
    return pill("typical · check your PDK", color=MUTED, size=16)


def box(x0, y0, x1, y1, color, opacity=0.55, stroke=1.6):
    """A layout shape between two corners, filled with its layer colour and outlined in it."""
    r = Rectangle(width=abs(x1 - x0), height=abs(y1 - y0))
    r.move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])
    return r.set_fill(color, opacity=opacity).set_stroke(color, width=stroke, opacity=1.0)


def planar_mos(w, l, nf=1, u=0.012, sd=60, contacts=True, metal=True, center=(0, 0)):
    """A planar MOSFET from above, in nm (scene units per nm: U): the active area, NF gate
    fingers of length L crossing it, a column of contacts on each source and drain, and a metal
    strap over each. W is the width of each finger. Returns (group, parts) with the parts in
    lists: "active", "poly", "contacts", "metal", and "sd", the x of each source/drain centre.
    """
    cx, cy = center
    span = nf * l + (nf + 1) * sd
    x0 = cx - span * u / 2
    parts = {"active": VGroup(), "poly": VGroup(), "contacts": VGroup(), "metal": VGroup(), "sd": []}
    parts["active"].add(box(x0, cy - w * u / 2, x0 + span * u, cy + w * u / 2, ACTIVE, 0.5))
    ext = 30  # the gate runs past the active on both sides
    for k in range(nf):
        gx = x0 + (sd + k * (l + sd)) * u
        parts["poly"].add(box(gx, cy - (w / 2 + ext) * u, gx + l * u, cy + (w / 2 + ext) * u, POLY, 0.7))
    for k in range(nf + 1):
        mx = x0 + (sd / 2 + k * (l + sd)) * u
        parts["sd"].append(mx)
        if contacts:
            c = 20
            n = max(1, int((w - 10) // (2 * c)))
            col = VGroup(*[box(mx - c / 2 * u, 0, mx + c / 2 * u, c * u, CONTACT, 0.95, 1.0) for _ in range(n)])
            col.arrange(DOWN, buff=c * u).move_to([mx, cy, 0])
            parts["contacts"].add(col)
        if metal:
            m = sd * 0.62
            parts["metal"].add(box(mx - m / 2 * u, cy - (w / 2 - 4) * u, mx + m / 2 * u, cy + (w / 2 - 4) * u, METAL, 0.3))
    group = VGroup(parts["active"], parts["poly"], parts["contacts"], parts["metal"])
    return group, parts


def knob_table(rows, col_w=(3.2, 3.6, 3.6), size=22, head_color=None):
    """A small table of text: ROWS is a list of lists of strings; the first row is the header."""
    from kit.style import GATE

    head_color = head_color or GATE
    lines = VGroup()
    for i, row in enumerate(rows):
        cells = VGroup()
        x = 0.0
        for j, (s, w) in enumerate(zip(row, col_w)):
            t = text(s, size=size, color=head_color if i == 0 else (INK if j else MUTED),
                     weight="SEMIBOLD" if i == 0 else "NORMAL")
            t.move_to([x + t.width / 2, 0, 0])
            cells.add(t)
            x += w
        lines.add(cells)
    lines.arrange(DOWN, aligned_edge=LEFT, buff=0.32)
    left = lines.get_left()[0]
    for row in lines:  # keep the columns aligned after arrange
        x = left
        for t, w in zip(row, col_w):
            t.move_to([x + t.width / 2, row.get_center()[1], 0])
            x += w
    y = lines[0].get_bottom()[1] - 0.14
    rule = Line([left, y, 0], [left + sum(col_w) - 0.3, y, 0], stroke_color=FAINT, stroke_width=2)
    return VGroup(lines, rule)


def card_box(head, body, width=4.0, height=3.4, head_size=26):
    """A dark card with a gold heading, for side-by-side comparisons."""
    from kit.style import GATE

    content = VGroup(text(head, size=head_size, weight="SEMIBOLD", color=GATE), *body).arrange(DOWN, buff=0.28)
    frame = RoundedRectangle(width=width, height=height, corner_radius=0.15, fill_color=PANEL, fill_opacity=1,
                             stroke_color=FAINT, stroke_width=2)
    return VGroup(frame, content.move_to(frame))

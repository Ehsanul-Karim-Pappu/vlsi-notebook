"""Pieces this lecture's chapters share: the CMOS cross-section with its parasitic bipolars and
resistors, bipolar and resistor symbols, top-view layout shapes with DRC markers, and the tags
that mark a toy-model number or a PDK-dependent rule.

Colours follow lecture 1's inverter: n⁺ cyan, p⁺ magenta, the n-well green, the p-substrate
mauve. In the top views the same colours mark N+ and P+ diffusion, so a shape reads the same in
both views.
"""

import numpy as np
from manim import (DOWN, LEFT, RIGHT, UP, Arrow, Circle, Line, Rectangle, RoundedRectangle,
                   Square, VGroup, VMobject)

from kit.style import (BG, DRAIN, ELECTRON, FAINT, GATE, GOOD, HOLE, INK, METAL, MUTED, NWELL, PANEL, PSUB, display,
                       kicker, pill, text)

NPLUS, PPLUS = ELECTRON, HOLE
WELL_EDGE = "#7FBF8F"  # the n-well's outline in the top views
TAP_MARK = INK


# --- small pieces ------------------------------------------------------------------------------
def box(x0, y0, x1, y1, color, opacity=1.0, stroke=0):
    r = Rectangle(width=abs(x1 - x0), height=abs(y1 - y0), stroke_width=stroke, stroke_color=color)
    return r.set_fill(color, opacity).move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])


def ring(center, width, height, thick, color, opacity=1.0, gap=0.0):
    """A ring drawn the way a layout tool draws one: four filled bars, so the corners are solid
    (a thick outline leaves a notch where its ends meet). WIDTH and HEIGHT are the outer size;
    GAP > 0 leaves an opening of that width in the middle of the top bar."""
    cx, cy = center[0], center[1]
    x0, x1, y0, y1 = cx - width / 2, cx + width / 2, cy - height / 2, cy + height / 2
    bars = [box(x0, y0, x1, y0 + thick, color, opacity), box(x0, y0 + thick, x0 + thick, y1 - thick, color, opacity),
            box(x1 - thick, y0 + thick, x1, y1 - thick, color, opacity)]
    if gap > 0:
        bars += [box(x0, y1 - thick, cx - gap / 2, y1, color, opacity), box(cx + gap / 2, y1 - thick, x1, y1, color, opacity)]
    else:
        bars.append(box(x0, y1 - thick, x1, y1, color, opacity))
    return VGroup(*bars)


def resistor(a, b, color=INK, width=3, zigs=6, amp=0.1, lead=0.15):
    """A zigzag resistor from point A to point B."""
    a, b = np.array(a, float), np.array(b, float)
    d = b - a
    length = np.linalg.norm(d)
    u = d / length
    n = np.array([-u[1], u[0], 0])
    pts = [a, a + u * lead]
    body = length - 2 * lead
    for k in range(zigs):
        t = lead + body * (k + 0.5) / zigs
        pts.append(a + u * t + n * amp * (1 if k % 2 == 0 else -1))
    pts += [b - u * lead, b]
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(pts)


def bjt(kind, scale=1.0, color=INK, width=3):
    """A bipolar symbol, base on the left, collector up, emitter down; kind is "npn" or "pnp".
    The group remembers its terminals as .b, .c and .e (scene points, kept up to date by
    calling .terminals())."""
    s = scale
    bar = Line([0, -0.35 * s, 0], [0, 0.35 * s, 0], stroke_color=color, stroke_width=width + 2)
    base = Line([-0.55 * s, 0, 0], [0, 0, 0], stroke_color=color, stroke_width=width)
    col = VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(
        [[0, 0.15 * s, 0], [0.4 * s, 0.4 * s, 0], [0.4 * s, 0.75 * s, 0]])
    emi = VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(
        [[0, -0.15 * s, 0], [0.4 * s, -0.4 * s, 0], [0.4 * s, -0.75 * s, 0]])
    if kind == "npn":  # the arrow points out of the emitter
        tip = Arrow([0.08 * s, -0.2 * s, 0], [0.38 * s, -0.39 * s, 0], buff=0, stroke_color=color, stroke_width=width,
                    max_tip_length_to_length_ratio=0.6)
    else:  # into the base, on the emitter, drawn on the top lead for a PNP (emitter up)
        tip = Arrow([0.38 * s, 0.39 * s, 0], [0.08 * s, 0.2 * s, 0], buff=0, stroke_color=color, stroke_width=width,
                    max_tip_length_to_length_ratio=0.6)
    g = VGroup(bar, base, col, emi, tip)
    g.kind = kind
    g.leads = (base, col, emi)
    return g


def terminals(sym):
    """A bjt's base, collector and emitter points, as drawn. For a PNP the emitter is the top
    lead and the collector the bottom one."""
    base, top, bottom = sym.leads
    b = base.get_start()
    t, d = top.get_end(), bottom.get_end()
    return (b, t, d) if sym.kind == "npn" else (b, d, t)


def flow(path_pts, color, dots=5, radius=0.05):
    """Dots spaced along a polyline, to animate current along it."""
    path = VMobject().set_points_as_corners([np.array(p, float) for p in path_pts])
    return path, VGroup(*[Circle(radius=radius, stroke_width=0, fill_color=color, fill_opacity=1) for _ in range(dots)])


# --- the cross-section -------------------------------------------------------------------------
class CrossSection(VGroup):
    """The CMOS inverter in silicon: a p-substrate with an n-well, the nMOS (N+ source and drain)
    with its P+ substrate tap, the pMOS (P+ source and drain) in the well with its N+ well tap.

    Positions are scene units. .at holds the places the chapters point at: the NPN's emitter
    (the nMOS source), the PNP's emitter (the pMOS source), the bases in the substrate and the
    well, and the two taps."""

    def __init__(self, top=0.6, left=-6.0, right=6.0, depth=3.0, well=(0.4, 5.6), well_depth=1.8,
                 sub_tap=-5.0, n_src=-3.3, n_drn=-1.5, p_drn=1.5, p_src=3.3, well_tap=4.8, labels=True):
        super().__init__()
        self.top = top
        sub = box(left, top - depth, right, top, PSUB)
        wl = box(well[0], top - well_depth, well[1], top, NWELL)
        self.sub, self.well = sub, wl
        self.diffs = {}
        d_w, d_h = 0.8, 0.38

        def dif(x, color, lab, key):
            r = box(x - d_w / 2, top - d_h, x + d_w / 2, top, color)
            t = text(lab, size=16, color=BG, weight="SEMIBOLD").move_to(r)
            self.diffs[key] = VGroup(r, t)
            return self.diffs[key]

        parts = VGroup(
            dif(sub_tap, PPLUS, "p⁺", "sub_tap"), dif(n_src, NPLUS, "n⁺", "n_src"), dif(n_drn, NPLUS, "n⁺", "n_drn"),
            dif(p_drn, PPLUS, "p⁺", "p_drn"), dif(p_src, PPLUS, "p⁺", "p_src"), dif(well_tap, NPLUS, "n⁺", "well_tap"))
        gates = VGroup(box((n_src + n_drn) / 2 - 0.4, top + 0.04, (n_src + n_drn) / 2 + 0.4, top + 0.3, GATE),
                       box((p_drn + p_src) / 2 - 0.4, top + 0.04, (p_drn + p_src) / 2 + 0.4, top + 0.3, GATE))
        self.add(sub, wl, parts, gates)
        self.gates = gates
        self.x = dict(sub_tap=sub_tap, n_src=n_src, n_drn=n_drn, p_drn=p_drn, p_src=p_src, well_tap=well_tap,
                      well_left=well[0], well_right=well[1])
        if labels:
            self.wires = VGroup()
            for key, name, color in (("sub_tap", "VSS", MUTED), ("n_src", "VSS", MUTED), ("p_src", "VDD", DRAIN),
                                     ("well_tap", "VDD", DRAIN)):
                x = self.x[key]
                self.wires.add(Line([x, top, 0], [x, top + 0.75, 0], stroke_color=METAL, stroke_width=4),
                               text(name, size=18, color=color, weight="SEMIBOLD").move_to([x, top + 0.98, 0]))
            gx = (self.x["n_drn"] + self.x["p_drn"]) / 2
            self.wires.add(VMobject(stroke_color=METAL, stroke_width=4).set_points_as_corners(
                [[n_drn, top, 0], [n_drn, top + 0.55, 0], [p_drn, top + 0.55, 0], [p_drn, top, 0]]),
                text("OUT", size=18, color=MUTED).move_to([gx, top + 0.78, 0]))
            self.tags = VGroup(text("p-substrate", size=20, color=INK).set_opacity(0.8).move_to([left + 1.6, top - depth + 0.35, 0]),
                               text("n-well", size=20, color=INK).set_opacity(0.8).move_to([well[0] + 0.7, top - well_depth + 0.3, 0]))
            self.add(self.wires, self.tags)
        y_sub = top - depth * 0.62
        self.at = {
            "npn_e": np.array([n_src, top - d_h, 0]),
            "npn_b": np.array([n_src + 0.3, y_sub, 0]),
            "npn_c": np.array([well[0] + 0.3, top - well_depth * 0.55, 0]),
            "pnp_e": np.array([p_src, top - d_h, 0]),
            "pnp_b": np.array([p_src, top - well_depth * 0.6, 0]),
            "pnp_c": np.array([p_src, top - depth * 0.8, 0]),
            "sub_tap": np.array([sub_tap, top - d_h, 0]),
            "well_tap": np.array([well_tap, top - d_h, 0]),
        }


# --- the equivalent circuit ------------------------------------------------------------------
def scr_circuit(center=(3.6, 0.0), scale=1.0, color=INK):
    """The parasitic thyristor as a circuit: the PNP (emitter to VDD, base to the well node W,
    collector to the substrate node S), the NPN (collector to W, base to S, emitter to VSS),
    R_well from W to VDD and R_sub from S to VSS. Returns a group with .parts (dict) and .nodes
    (dict of scene points: W, S, vdd, vss)."""
    cx, cy = center
    k = scale
    P = lambda x, y: np.array([cx + x * k, cy + y * k, 0])  # noqa: E731
    pnp = bjt("pnp", k, color).flip(UP).move_to(P(-0.9, 1.0))
    npn = bjt("npn", k, color).move_to(P(0.9, -0.9))
    pb, pc, pe = terminals(pnp)
    nb, nc, ne = terminals(npn)
    y_vdd, y_vss = cy + 2.3 * k, cy - 2.3 * k
    x_l, x_r = cx - 2.4 * k, cx + 2.4 * k
    w = lambda *pts: VMobject(stroke_color=color, stroke_width=3).set_points_as_corners([np.array(q) for q in pts])  # noqa: E731
    vdd = Line([x_l, y_vdd, 0], [x_r, y_vdd, 0], stroke_color=DRAIN, stroke_width=5)
    vss = Line([x_l, y_vss, 0], [x_r, y_vss, 0], stroke_color=MUTED, stroke_width=5)
    node_w = np.array([nc[0], pb[1], 0])
    node_s = np.array([pc[0], nb[1], 0])
    r_w_x = x_r - 0.3 * k
    r_s_x = x_l + 0.3 * k
    parts = {
        "pnp": pnp, "npn": npn, "vdd": vdd, "vss": vss,
        "pnp_e": w(pe, [pe[0], y_vdd, 0]),
        "w_wire": w(pb, node_w, nc),
        "s_wire": w(pc, node_s, nb),
        "npn_e": w(ne, [ne[0], y_vss, 0]),
        "r_well_wire": w(node_w, [r_w_x, node_w[1], 0]),
        "r_well": resistor([r_w_x, node_w[1], 0], [r_w_x, y_vdd, 0], color),
        "r_sub_wire": w(node_s, [r_s_x, node_s[1], 0]),
        "r_sub": resistor([r_s_x, node_s[1], 0], [r_s_x, y_vss, 0], color),
    }
    labels = VGroup(
        text("VDD", size=20, color=DRAIN, weight="SEMIBOLD").next_to(vdd, UP, buff=0.1),
        text("VSS", size=20, color=MUTED, weight="SEMIBOLD").next_to(vss, DOWN, buff=0.1),
        text("R_well", size=20, color=color).next_to(parts["r_well"], RIGHT, buff=0.12),
        text("R_sub", size=20, color=color).next_to(parts["r_sub"], LEFT, buff=0.12),
        text("PNP", size=20, color=PPLUS, weight="SEMIBOLD").next_to(pnp, LEFT, buff=0.15),
        text("NPN", size=20, color=NPLUS, weight="SEMIBOLD").next_to(npn, RIGHT, buff=0.15),
        text("W", size=18, color=MUTED).next_to(node_w, UP, buff=0.08),
        text("S", size=18, color=MUTED).next_to(node_s, DOWN, buff=0.08),
    )
    parts["labels"] = labels
    g = VGroup(*parts.values())
    g.parts = parts
    g.nodes = {"W": node_w, "S": node_s, "vdd_y": y_vdd, "vss_y": y_vss}
    return g


# --- top views ---------------------------------------------------------------------------------
def tap(x, y, kind, size=0.3):
    """A tap from above: its diffusion with a contact in the middle. kind "p" (substrate, VSS) or
    "n" (well, VDD)."""
    color = PPLUS if kind == "p" else NPLUS
    sq = Square(size, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.85).move_to([x, y, 0])
    c = Square(size * 0.35, stroke_width=0, fill_color=BG, fill_opacity=0.9).move_to(sq)
    return VGroup(sq, c)


def marker(mob, label, color=DRAIN, buff=0.06):
    """A DRC error marker: a dashed box around MOB and the rule's name."""
    r = RoundedRectangle(width=mob.width + 2 * buff, height=mob.height + 2 * buff, corner_radius=0.04,
                         stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.12).move_to(mob)
    t = pill(label, color=color, size=14).next_to(r, UP, buff=0.06)
    return VGroup(r, t)


# --- tags and text pieces ----------------------------------------------------------------------
def pdk_tag():
    return pill("typical · check your PDK", color=MUTED, size=16)


def illustrative():
    return text("illustrative", size=16, color=MUTED)


def toy_tag():
    return pill("toy model", color=MUTED, size=16)


def chapter_title(n, title, sub):
    return VGroup(kicker(f"Chapter {n}", color=GATE), display(str(n), size=150, color=FAINT), display(title, size=56),
                  text(sub, size=28, color=MUTED, slant="ITALIC")).arrange(DOWN, buff=0.25).move_to(UP * 0.2)


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


def checklist(items, size=22):
    rows = VGroup()
    for s in items:
        rows.add(VGroup(Square(0.22, stroke_color=GOOD, stroke_width=2.5), text(s, size=size, color=INK)).arrange(RIGHT, buff=0.25))
    return rows.arrange(DOWN, aligned_edge=LEFT, buff=0.26)


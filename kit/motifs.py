"""Reusable pictures: device cross-sections, the energy barrier with its thermal electrons,
and the Boltzmann distribution. Lectures build their scenes out of these.
"""

from math import exp

import numpy as np
from manim import (
    DOWN,
    LEFT,
    PI,
    RIGHT,
    UP,
    Axes,
    Dot,
    Line,
    ParametricFunction,
    Polygon,
    Rectangle,
    VGroup,
    VMobject,
    always_redraw,
)

from kit.style import (
    ELECTRON,
    FAINT,
    GATE,
    HOLE,
    INK,
    MUTED,
    OXIDE,
    OXIDE_TEXT,
    SILICON,
    SUBSTRATE,
    WALL,
    text,
    tr,
)


# --- device cross-sections (looking down the channel) --------------------------------------
def _box(w, h, x, y, color, opacity=1.0, stroke=0):
    r = Rectangle(width=w, height=h, fill_color=color, fill_opacity=opacity, stroke_width=stroke)
    return r.move_to([x, y, 0])


def _base():
    """Substrate with shallow-trench isolation either side."""
    return VGroup(
        _box(3.2, 0.6, 0, -0.9, SUBSTRATE),
        _box(1.2, 0.4, -1.0, -0.4, OXIDE, 0.9),
        _box(1.2, 0.4, 1.0, -0.4, OXIDE, 0.9),
    )


def _sheet(x, y, w=1.0, t=0.16, color=SILICON, faces=4):
    """One channel sheet with its gate oxide; faces=3 leaves the right-hand face bare."""
    ox_w = w + (0.08 if faces == 4 else 0.04)
    ox_x = x if faces == 4 else x - 0.02
    return VGroup(_box(ox_w, t + 0.08, ox_x, y, OXIDE_TEXT), _box(w, t, x, y, color))


def xsection(kind):
    """Cross-section of a transistor architecture, the gate in gold.

    kind: "planar", "finfet", "nanosheet", "forksheet" or "cfet". Every shape sits on the same
    base, so one can be transformed into the next.
    """
    if kind == "planar":
        sub = _box(3.2, 1.2, 0, -0.6, SUBSTRATE)
        sti = VGroup(_box(0.7, 0.5, -1.25, -0.25, OXIDE, 0.9), _box(0.7, 0.5, 1.25, -0.25, OXIDE, 0.9))
        channel = _box(1.8, 0.07, 0, -0.035, "#7FD8E4")
        ox = _box(1.8, 0.08, 0, 0.04, OXIDE_TEXT)
        gate = _box(1.8, 0.7, 0, 0.43, GATE)
        return VGroup(sub, sti, gate, ox, channel)
    if kind == "finfet":
        fin = _box(0.32, 1.45, 0, 0.125, SILICON)
        ox = _box(0.4, 1.08, 0, 0.34, OXIDE_TEXT)
        gate = _box(1.4, 1.45, 0, 0.525, GATE)
        return VGroup(_base(), gate, ox, fin)
    if kind == "nanosheet":
        gate = _box(1.6, 1.6, 0, 0.6, GATE)
        sheets = VGroup(*[_sheet(0, y) for y in (0.15, 0.6, 1.05)])
        return VGroup(_base(), gate, sheets)
    if kind == "forksheet":
        gate = _box(2.3, 1.6, 0, 0.6, GATE)
        wall = _box(0.16, 1.8, 0, 0.7, WALL)
        left = VGroup(*[_sheet(-0.5, y, w=0.76, faces=3) for y in (0.15, 0.6, 1.05)])
        right = VGroup(*[_sheet(0.5, y, w=0.76, faces=3).flip(UP) for y in (0.15, 0.6, 1.05)])
        for s in right:
            s[1].set_fill(HOLE, opacity=0.85)
        return VGroup(_base(), gate, left, right, wall)
    if kind == "cfet":
        gate = _box(1.6, 2.5, 0, 1.05, GATE)
        lower = VGroup(*[_sheet(0, y, color=HOLE) for y in (0.15, 0.55)])
        mid = _box(1.3, 0.22, 0, 0.98, WALL)
        upper = VGroup(*[_sheet(0, y) for y in (1.45, 1.85)])
        return VGroup(_base(), gate, lower, mid, upper)
    raise ValueError(kind)


# --- the energy barrier and its thermal electrons ------------------------------------------
def _smoothstep(t):
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3 - 2 * t)


class Barrier(VGroup):
    """The conduction-band edge along a transistor, source to drain, with electrons in it.

    Energies are in eV and drawn to scale (``scale`` scene units per eV), so the thermal spread
    of the electrons is k_B T as it really is. ``barrier`` and ``drain_drop`` are ValueTrackers;
    animate them and the band edge redraws and the electrons respond.
    """

    def __init__(
        self,
        barrier,
        drain_drop,
        n=160,
        kT=0.02585,
        scale=8.0,
        origin=(0.0, -1.2),
        source=(-5.0, -1.2),
        channel_half=1.2,
        drain_end=5.0,
        seed=7,
        **kw,
    ):
        super().__init__(**kw)
        self.barrier, self.drain_drop = barrier, drain_drop
        self.kT, self.e_scale = kT, scale
        self.x0, self.y0 = origin
        self.src_left, self.src_right = source
        self.half = channel_half
        self.drain_end = drain_end
        self.crossed = 0
        self.rng = np.random.default_rng(seed)

        self.edge = always_redraw(self._edge)
        self.add(self.edge)

        self.count = n
        self.px = self.rng.uniform(self.src_left + 0.1, self.src_right - 0.05, n)
        self.pe = self.rng.exponential(kT, n)
        self.mode = np.zeros(n, dtype=int)  # 0 source, 1 over the barrier, 2 in the drain
        self.vx = self.rng.normal(0, 1.0, n)
        self.dots = VGroup(*[Dot(radius=0.045, color=ELECTRON) for _ in range(n)])
        self._place()
        self.add(self.dots)

    # band edge E_c(x), in eV
    def ec(self, x):
        b, d = self.barrier.get_value(), self.drain_drop.get_value()
        x = np.asarray(x, dtype=float)
        left = b * _smoothstep((x - (self.x0 - self.half)) / self.half)
        right = b + (-d - b) * _smoothstep((x - self.x0) / self.half)
        out = np.where(x < self.x0, left, right)
        out = np.where(x < self.x0 - self.half, 0.0, out)
        return np.where(x > self.x0 + self.half, -d, out)

    def energy_y(self, e):
        return self.y0 + e * self.e_scale

    def _edge(self):
        xs = np.linspace(self.src_left, self.drain_end, 200)
        pts = [[x, self.energy_y(e), 0] for x, e in zip(xs, self.ec(xs))]
        return VMobject(stroke_color=INK, stroke_width=4).set_points_smoothly(pts)

    def _place(self):
        for i, d in enumerate(self.dots):
            d.move_to([self.px[i], self.energy_y(self.pe[i]) + 0.05, 0])

    def start(self):
        """Begin the thermal motion (call once the barrier is on screen)."""
        self.dots.add_updater(lambda m, dt: self.step(dt))

    def stop(self):
        self.dots.clear_updaters()

    def step(self, dt):
        if dt == 0:
            return
        rng, kT = self.rng, self.kT
        b = self.barrier.get_value()
        src = self.mode == 0
        # Energy: a reflected random walk with downward drift, whose steady state is the
        # Boltzmann distribution exp(-E / kT) with mean kT.
        tau = 0.35
        dif = kT * kT / tau
        self.pe[src] += -dif / kT * dt + np.sqrt(2 * dif * dt) * rng.standard_normal(src.sum())
        self.pe[src] = np.abs(self.pe[src])
        # Position: a random walk in the source, bouncing off the walls...
        self.vx[src] += rng.normal(0, 3.0 * np.sqrt(dt), src.sum()) - 0.6 * self.vx[src] * dt
        self.px[src] += self.vx[src] * dt
        lo = src & (self.px < self.src_left + 0.05)
        self.px[lo] = 2 * (self.src_left + 0.05) - self.px[lo]
        self.vx[lo] = np.abs(self.vx[lo])
        at_gate = src & (self.px > self.src_right)
        # ...unless an electron reaches the channel with more energy than the barrier.
        over = at_gate & (self.pe > b)
        back = at_gate & ~over
        self.px[back] = 2 * self.src_right - self.px[back]
        self.vx[back] = -np.abs(self.vx[back])
        self.mode[over] = 1
        self.vx[over] = 2.2
        # Crossing: carried over at its own energy.
        cross = self.mode == 1
        self.px[cross] += self.vx[cross] * dt
        done = cross & (self.px > self.x0 + self.half)
        self.crossed += int(done.sum())
        self.mode[done] = 2
        # In the drain: fall to the band edge, drift away, and come back as a new source
        # electron (the battery returns it).
        dr = self.mode == 2
        self.px[dr] += self.vx[dr] * dt
        floor = self.ec(self.px[dr])
        self.pe[dr] = np.maximum(floor, self.pe[dr] - 1.5 * dt)
        gone = dr & (self.px > self.drain_end - 0.1)
        k = int(gone.sum())
        if k:
            self.px[gone] = self.rng.uniform(self.src_left + 0.1, self.src_left + 1.0, k)
            self.pe[gone] = self.rng.exponential(kT, k)
            self.vx[gone] = self.rng.normal(0, 1.0, k)
            self.mode[gone] = 0
        self._place()


# --- the Boltzmann distribution ------------------------------------------------------------
class Boltzmann(VGroup):
    """n(E) against energy measured in k_B T, with the tail above the barrier shaded.

    Energy runs up the page, so it lines up with a band diagram. ``barrier_kT`` is a
    ValueTracker holding the barrier height in units of k_B T.
    """

    def __init__(self, barrier_kT, height=5.0, width=3.4, top=8.0, **kw):
        super().__init__(**kw)
        self.barrier_kT, self.top = barrier_kT, top
        self.axes = Axes(
            x_range=[0, 1.05, 1],
            y_range=[0, top, 1],
            x_length=width,
            y_length=height,
            tips=False,
            axis_config={"stroke_color": MUTED, "stroke_width": 2, "include_ticks": False},
        )
        self.curve = ParametricFunction(
            lambda e: self.axes.c2p(exp(-e), e), t_range=[0, top], stroke_color=ELECTRON, stroke_width=4
        )
        self.tail = always_redraw(self._tail)
        self.line = always_redraw(
            lambda: Line(
                self.axes.c2p(0, self.barrier_kT.get_value()),
                self.axes.c2p(1.05, self.barrier_kT.get_value()),
                stroke_color=GATE,
                stroke_width=3,
            )
        )
        e_label = text(tr("Energy", "energy"), size=22, color=MUTED).rotate(PI / 2)
        e_label.next_to(self.axes.y_axis, LEFT, buff=0.15)
        n_label = text(tr("number of electrons", "electron-এর সংখ্যা"), size=22, color=MUTED)
        n_label.next_to(self.axes.x_axis, DOWN, buff=0.15)
        self.add(self.axes, self.tail, self.curve, self.line, e_label, n_label)

    def _tail(self):
        b = self.barrier_kT.get_value()
        es = np.linspace(b, self.top, 60)
        pts = [self.axes.c2p(exp(-e), e) for e in es]
        pts += [self.axes.c2p(0, self.top), self.axes.c2p(0, b)]
        return Polygon(*pts, stroke_width=0, fill_color=ELECTRON, fill_opacity=0.45)


def panel_rule(width=12.0):
    """A faint horizontal rule, used to separate a figure from its equation."""
    return Line(LEFT * width / 2, RIGHT * width / 2, stroke_color=FAINT, stroke_width=1.5)


__all__ = ["xsection", "Barrier", "Boltzmann", "panel_rule"]

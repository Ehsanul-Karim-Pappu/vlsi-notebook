"""Chapter 0 · Cold open: the most-made thing in history.

A counter to 13 sextillion, a dive from a phone into a single transistor, the transistor in 3D,
the hook, and the five shapes this lecture moves through.

Each slide starts with ``self.slide(notes)``: manim-slides gives a slide the options passed to
the ``next_slide`` call that opens it.
"""

import json
import sys
from math import floor, log10
from pathlib import Path

LECTURE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(LECTURE.parents[1]), str(LECTURE)]

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403
from manim_slides import ThreeDSlide  # noqa: E402

from kit.devices3d import build_device  # noqa: E402
from kit.motifs import xsection  # noqa: E402
from kit.style import *  # noqa: E402,F403

GEOMETRY = json.loads((LECTURE / "data" / "geometry.json").read_text())
CHANNEL = "#7FD8E4"  # the channel sheets, picked out from the rest of the silicon
TOTAL = 13 * 10**21  # transistors made by 2018 (Jim Handy's estimate, via the Computer History Museum)


def big_count(e):
    """10**e as an integer with three significant figures and thousands separators."""
    if e >= log10(TOTAL) - 1e-9:
        return f"{TOTAL:,}"
    n = 10**e
    if n < 1000:
        return f"{int(round(n)):,}"
    k = floor(e)
    return f"{round(n / 10 ** (k - 2)) * 10 ** (k - 2):,}"


class Ch00ColdOpen(ThreeDSlide):
    def slide(self, notes="", **kw):
        self.next_slide(notes=notes, **kw)

    def clear(self, run_time=1.0):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=run_time)

    def construct(self):
        self.counter()
        self.dive_in()
        self.device()
        self.hook()
        self.shapes()
        self.title()

    # --- the counter -------------------------------------------------------------------------
    def counter(self):
        self.slide(
            """
            In December 1947 there was exactly one of these in the world. Since then, we have
            made about thirteen sextillion of them. That's a 13 followed by 21 zeros: more than
            a trillion and a half for every person alive.
            """
        )
        field = VGroup(
            *[
                Dot([x * 0.32, y * 0.32, 0], radius=0.035, color=ELECTRON)
                for x in range(-24, 25)
                for y in range(-13, 14)
            ]
        )
        field.set_opacity(0.0)
        one = Dot(ORIGIN, radius=0.07, color=ELECTRON)
        halo = Circle(radius=0.35, stroke_width=0, fill_color=ELECTRON, fill_opacity=0.15)
        year = text("1947", size=28, color=MUTED).next_to(one, DOWN, buff=0.5)
        self.play(FadeIn(halo, scale=0.5), GrowFromCenter(one), FadeIn(year))
        self.wait(0.5)

        e = ValueTracker(0.0)
        number = always_redraw(lambda: display(big_count(e.get_value()), size=58, color=INK).move_to(UP * 1.3))
        caption = text("transistors made", size=28, color=MUTED).move_to(UP * 0.45)
        field.scale(12, about_point=ORIGIN)
        self.add(field)
        self.play(
            FadeOut(one), FadeOut(halo), FadeOut(year),
            field.animate.scale(1 / 12, about_point=ORIGIN).set_opacity(0.18),
            run_time=1.5,
        )
        self.add(number)
        self.play(FadeIn(caption), e.animate.set_value(log10(TOTAL)), run_time=5, rate_func=rate_functions.ease_in_out_sine)
        self.wait(0.5)

        self.slide(
            """
            One historian at the Computer History Museum calls the MOS transistor the most
            frequently manufactured human artifact in history. Nothing else comes close.
            """
        )
        sci = MathTex(r"\approx 1.3\times10^{22}", font_size=48, color=ELECTRON).next_to(caption, DOWN, buff=0.4)
        per = text("about 1.6 trillion for every person alive", size=28, color=MUTED).next_to(sci, DOWN, buff=0.3)
        self.play(Write(sci))
        self.play(FadeIn(per))
        self.play(field.animate.set_opacity(0.07))
        quote = text("“The most frequently manufactured human artifact in history.”", size=30, color=GATE, slant="ITALIC")
        who = text("David C. Brock, historian, Computer History Museum", size=20, color=MUTED)
        VGroup(quote, who).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=1.0)
        src = source("Count: Jim Handy's estimate of transistors made through 2018, via the Computer History Museum")
        self.play(FadeIn(quote, shift=UP * 0.2), FadeIn(who), FadeIn(src))

    # --- from a phone to one transistor ------------------------------------------------------
    def dive(self, outer, inner, target, factor, run_time=2.4):
        """Zoom into TARGET by FACTOR: OUTER grows and fades, INNER (drawn at full size, centred
        on the origin) emerges from TARGET."""
        inner.scale(1 / factor).move_to(target)
        o0, i0 = outer.copy(), inner.copy()
        self.add(inner)
        t = np.array(target)

        def frame(alpha):
            s = factor**alpha
            return lambda m: m.scale(s, about_point=t).shift(-t * alpha)

        def upd_outer(m, a):
            m.become(frame(a)(o0.copy()))
            m.fade(np.clip((a - 0.45) / 0.45, 0, 1))

        def upd_inner(m, a):
            m.become(frame(a)(i0.copy()))
            m.fade(1 - np.clip((a - 0.35) / 0.45, 0, 1))

        self.play(
            UpdateFromAlphaFunc(outer, upd_outer),
            UpdateFromAlphaFunc(inner, upd_inner),
            run_time=run_time,
            rate_func=rate_functions.ease_in_out_cubic,
        )
        self.remove(outer)

    def dive_in(self):
        self.slide(
            """
            Where are they? Some of them are in your pocket. This is a phone. Inside it is a chip
            the size of a fingernail.
            """
        )
        self.clear()
        phone = VGroup(
            RoundedRectangle(width=2.4, height=4.8, corner_radius=0.35, stroke_color=INK, stroke_width=3),
            RoundedRectangle(width=2.1, height=4.3, corner_radius=0.2, stroke_color=FAINT, stroke_width=2),
        )
        chip_pt = np.array([0.0, 0.6, 0])
        chip = VGroup(
            Square(0.42, stroke_color=GATE, stroke_width=3, fill_color=PANEL, fill_opacity=1).move_to(chip_pt),
            *[
                Line(chip_pt + [x, 0.21, 0], chip_pt + [x, 0.28, 0], stroke_color=GATE, stroke_width=2)
                for x in np.linspace(-0.15, 0.15, 5)
            ],
            *[
                Line(chip_pt + [x, -0.21, 0], chip_pt + [x, -0.28, 0], stroke_color=GATE, stroke_width=2)
                for x in np.linspace(-0.15, 0.15, 5)
            ],
        )
        p_lbl = text("a phone", size=26, color=MUTED).next_to(phone, DOWN, buff=0.3)
        level1 = VGroup(phone, chip, p_lbl)
        self.play(Create(phone[0]), FadeIn(phone[1]), run_time=1.2)
        self.play(FadeIn(chip, scale=0.5), FadeIn(p_lbl))

        self.slide(
            """
            Zoom in, and the chip is a city: processor cores, graphics, memory, all wired
            together. Apple's A17 Pro, from 2023, has nineteen billion transistors on it.
            """
        )
        die = Square(5.6, stroke_color=GATE, stroke_width=3, fill_color=PANEL, fill_opacity=1)
        blocks = VGroup(
            Rectangle(width=1.9, height=1.6, fill_color="#2E4A5A", fill_opacity=1, stroke_width=0).move_to([-1.55, 1.55, 0]),
            Rectangle(width=1.9, height=1.6, fill_color="#2E4A5A", fill_opacity=1, stroke_width=0).move_to([0.55, 1.55, 0]),
            Rectangle(width=1.0, height=1.6, fill_color="#3B4F3A", fill_opacity=1, stroke_width=0).move_to([2.1, 1.55, 0]),
            Rectangle(width=3.0, height=1.9, fill_color="#4B3B5A", fill_opacity=1, stroke_width=0).move_to([-1.0, -0.6, 0]),
            Rectangle(width=1.8, height=1.9, fill_color="#5A4B2E", fill_opacity=1, stroke_width=0).move_to([1.7, -0.6, 0]),
            Rectangle(width=5.0, height=0.8, fill_color="#3A3F47", fill_opacity=1, stroke_width=0).move_to([0, -2.2, 0]),
        )
        cache = VGroup(
            *[
                Square(0.16, stroke_width=0, fill_color="#565E6A", fill_opacity=1).move_to([1.0 + 0.2 * i, -0.15 - 0.2 * j, 0])
                for i in range(7)
                for j in range(4)
            ]
        ).move_to(blocks[4])
        names = VGroup(
            text("CPU", size=22, color=INK).move_to(blocks[0]),
            text("CPU", size=22, color=INK).move_to(blocks[1]),
            text("GPU", size=22, color=INK).move_to(blocks[3]),
            text("memory", size=20, color=INK).move_to(blocks[5]),
        )
        d_lbl = text("Apple A17 Pro (2023): 19 billion transistors", size=24, color=MUTED).next_to(die, DOWN, buff=0.15)
        level2 = VGroup(die, blocks, cache, names, d_lbl)
        self.dive(level1, level2, chip_pt, die.width / 0.42)

        self.slide(
            """
            Zoom into a processor core and you find rows and rows of standard cells: the logic
            gates. The gold lines are the transistors' gates; the pink stripes are the silicon
            they control.
            """
        )
        rows = VGroup()
        for r in range(5):
            y = 2.0 - r * 1.0
            row = VGroup(
                Line([-5.5, y + 0.45, 0], [5.5, y + 0.45, 0], stroke_color=METAL, stroke_width=4),
                Rectangle(width=11, height=0.22, fill_color=SILICON, fill_opacity=0.55, stroke_width=0).move_to([0, y + 0.15, 0]),
                Rectangle(width=11, height=0.22, fill_color=HOLE, fill_opacity=0.4, stroke_width=0).move_to([0, y - 0.2, 0]),
                *[
                    Line([x, y - 0.38, 0], [x, y + 0.38, 0], stroke_color=GATE, stroke_width=5)
                    for x in np.arange(-5.2, 5.4, 0.4)
                ],
            )
            rows.add(row)
        rows.add(Line([-5.5, -2.55, 0], [5.5, -2.55, 0], stroke_color=METAL, stroke_width=4))
        c_lbl = text("standard cells", size=24, color=MUTED).to_edge(DOWN, buff=0.3)
        level3 = VGroup(rows, c_lbl)
        self.dive(level2, level3, blocks[0].get_center() + np.array([0.3, -0.2, 0]), 5.0)

        self.slide(
            """
            And where one gold line crosses one silicon stripe: that's a transistor. A switch,
            a few dozen nanometres across.
            """
        )
        act = Rectangle(width=7.0, height=1.6, fill_color=SILICON, fill_opacity=0.55, stroke_width=0)
        g = Rectangle(width=0.9, height=3.6, fill_color=GATE, fill_opacity=1, stroke_width=0)
        cs = Square(0.7, fill_color=METAL, fill_opacity=1, stroke_width=0).move_to([-2.4, 0, 0])
        cd = Square(0.7, fill_color=METAL, fill_opacity=1, stroke_width=0).move_to([2.4, 0, 0])
        labels = VGroup(
            text("source", size=26, color=INK).next_to(cs, DOWN, buff=0.6),
            text("gate", size=26, color=GATE).next_to(g, UP, buff=0.15),
            text("drain", size=26, color=INK).next_to(cd, DOWN, buff=0.6),
        )
        t_lbl = text("one transistor", size=24, color=MUTED).to_edge(DOWN, buff=0.3)
        level4 = VGroup(act, g, cs, cd, labels, t_lbl)
        target = np.array([-5.2 + 0.4 * 14, 2.0 + 0.15, 0])
        self.dive(level3, level4, target, 6.0)
        self.level4 = level4

    # --- the transistor in 3D ----------------------------------------------------------------
    def device(self):
        self.slide(
            """
            Here is one in three dimensions. This is a nanosheet transistor, the kind in the
            newest chips. At the bottom, the silicon wafer. Then the channel: three sheets of
            silicon, each five nanometres thick. Then the gate wraps all the way around every
            sheet: a thin oxide, then metal. Then insulating spacers, and the source and drain
            on either side.
            """
        )
        self.play(FadeOut(self.level4))
        self.set_camera_orientation(phi=65 * DEGREES, theta=-60 * DEGREES, zoom=1.0)
        order = ["Substrate & isolation", "Channel stack", "Gate-all-around stack", "Gate electrode", "Spacers", "Source / drain"]
        captions = [
            "the silicon wafer",
            "the channel: three silicon sheets, 5 nm thick (blue)",
            "the gate oxide and metal, all the way around",
            "the gate",
            "insulating spacers",
            "source and drain",
        ]
        contacts = {"gatew", "nisi_source", "ni_source", "w_source", "nisi_drain", "ni_drain", "w_drain"}
        channel = {f"sheet{i}": CHANNEL for i in (1, 2, 3)}
        kw = dict(scale=0.048, groups=order, skip=contacts, recolor=channel)
        back, back_g = build_device(GEOMETRY, keep="back", **kw)
        front, front_g = build_device(GEOMETRY, keep="front", **kw)
        shift = -VGroup(back, front).get_center() + np.array([0, 0, -0.3])
        back.shift(shift)
        front.shift(shift)
        lst = VGroup(*[text(c, size=20, color=MUTED) for c in captions]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        lst.to_corner(UL, buff=0.5)
        src = source("Model: FET Lab's nanosheet nFET (15 nm gate, 5 nm sheets), contacts left off")
        self.add_fixed_in_frame_mobjects(lst, src)
        self.remove(lst, src)
        self.play(FadeIn(src))
        for i, name in enumerate(order):
            item = lst[i]
            self.play(
                FadeIn(VGroup(back_g[name], front_g[name]), shift=IN * 0.8),
                FadeIn(item),
                *([lst[i - 1].animate.set_color(MUTED)] if i else []),
                run_time=1.0,
            )
            self.play(item.animate.set_color(INK), run_time=0.3)
        self.play(lst[-1].animate.set_color(MUTED), run_time=0.3)

        self.slide(
            """
            Now cut it open down the middle, along the channel. There are the three sheets,
            running from source to drain. And look between them: gate metal above and below
            every sheet. The gate has the channel completely surrounded. Hold on to that
            picture; by the end of the lecture you'll know why it had to look like this.
            """
        )
        cut = text("cut open along the channel", size=24, color=GATE).to_corner(UR, buff=0.5)
        self.add_fixed_in_frame_mobjects(cut)
        self.remove(cut)
        self.play(FadeOut(front, shift=np.array([0, -3.0, 0])), FadeIn(cut), run_time=1.8)
        self.move_camera(phi=78 * DEGREES, theta=-90 * DEGREES, run_time=2.0)
        self.device_mob = VGroup(back)
        self.device_labels = VGroup(lst, src, cut)

        self.slide(
            """
            Every one of the thirteen sextillion has a gate like this one, and the gate is how it
            switches.
            """,
            loop=True,
        )
        self.move_camera(theta=-62 * DEGREES, run_time=4, rate_func=rate_functions.ease_in_out_sine)
        self.move_camera(theta=-90 * DEGREES, run_time=4, rate_func=rate_functions.ease_in_out_sine)

    # --- the hook ----------------------------------------------------------------------------
    def hook(self):
        self.slide(
            """
            Every one of them has one job: let current through, or stop it. On, off. And here's
            the thing that surprised me. Turning a transistor on is easy. Turning it off, so that
            it really stops, has been the hard part for a hundred years. Almost every big change
            in how transistors are built was about turning them off.
            """
        )
        self.play(FadeOut(self.device_mob), FadeOut(self.device_labels))
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)
        job = text("Every one of them has one job.", size=44, weight="SEMIBOLD").to_edge(UP, buff=0.8)
        self.play(FadeIn(job))

        wire_y = 0.4
        left = Line([-5.5, wire_y, 0], [-0.6, wire_y, 0], stroke_color=FAINT, stroke_width=10)
        right = Line([0.6, wire_y, 0], [5.5, wire_y, 0], stroke_color=FAINT, stroke_width=10)
        chan = Line([-0.6, wire_y, 0], [0.6, wire_y, 0], stroke_color=ELECTRON, stroke_width=10)
        gate = Rectangle(width=1.2, height=0.4, fill_color=GATE, fill_opacity=1, stroke_width=0).move_to([0, wire_y + 0.55, 0])
        state = text("ON", size=40, color=GOOD, weight="BOLD").next_to(gate, UP, buff=0.3)
        flow = VGroup(*[Dot(radius=0.07, color=ELECTRON) for _ in range(14)])
        phase = ValueTracker(0.0)
        on = ValueTracker(1.0)

        def place(m):
            for i, d in enumerate(m):
                x = -5.5 + ((i * 0.8 + phase.get_value()) % 11.2)
                if on.get_value() < 0.5 and x > -0.7:
                    x = -0.7 - (i % 3) * 0.18
                d.move_to([x, wire_y, 0])

        flow.add_updater(place)
        tick = lambda m, dt: phase.increment_value(1.6 * dt)  # noqa: E731
        flow.add_updater(tick)
        self.play(Create(left), Create(right), Create(chan), FadeIn(gate), FadeIn(state), FadeIn(flow))
        self.wait(2)
        state_off = text("OFF", size=40, color=DRAIN, weight="BOLD").move_to(state)
        self.play(on.animate.set_value(0), chan.animate.set_stroke(FAINT), Transform(state, state_off), run_time=0.6)
        self.wait(1.5)
        flow.clear_updaters()

        self.slide(
            """
            Turning it on is easy. Turning it off has been the hard part for a hundred years.
            """
        )
        easy = text("Turning it on is easy.", size=36, weight="SEMIBOLD")
        hard = text("Turning it off has been the hard part for 100 years.", size=36, weight="SEMIBOLD", color=GATE)
        VGroup(easy, hard).arrange(DOWN, buff=0.4).move_to(DOWN * 1.9)
        self.play(FadeIn(easy, shift=UP * 0.2))
        self.wait(0.6)
        self.play(FadeIn(hard, shift=UP * 0.2))

    # --- five shapes -------------------------------------------------------------------------
    def shapes(self):
        self.slide(
            """
            To keep their switches off, engineers have rebuilt the transistor again and again.
            First flat: a gate on one side of the channel.
            """
        )
        self.clear()
        steps = [
            ("planar", "Planar MOSFET", "1960 →", "gate on 1 side"),
            ("finfet", "FinFET", "2011 →", "gate on 3 sides"),
            ("nanosheet", "Nanosheet", "2022 →", "gate on all 4 sides"),
            ("forksheet", "Forksheet", "~2030 (projected)", "n and p squeezed against a wall"),
            ("cfet", "CFET", "~2033 (projected)", "n stacked on top of p"),
        ]
        notes = [
            None,
            "Then the channel stood up as a fin, with the gate on three sides.",
            "Then the fin was sliced into sheets, with the gate all the way around.",
            "Next, probably: the two kinds of transistor pressed against a wall between them.",
            """
            And after that, stacked: one kind of transistor on top of the other. Every one of
            these changes was forced by physics. This lecture is the story of those forces.
            """,
        ]

        def card(kind, name, year, faces):
            pic = xsection(kind).scale(1.35)
            words = VGroup(
                display(name, size=48),
                text(year, size=26, color=GATE),
                text(faces, size=26, color=MUTED),
            ).arrange(DOWN, buff=0.15)
            return VGroup(pic, words.next_to(pic, DOWN, buff=0.5)).move_to(UP * 0.2)

        cur = card(*steps[0])
        self.play(FadeIn(cur[0], shift=UP * 0.2), FadeIn(cur[1]))
        for spec, note in zip(steps[1:], notes[1:]):
            self.slide(note)
            nxt = card(*spec)
            self.play(ReplacementTransform(cur[0], nxt[0]), FadeTransform(cur[1], nxt[1]), run_time=1.4)
            cur = nxt

        self.slide(
            """
            Five shapes in sixty years, and two more on the way. Let's see why.
            """
        )
        row = VGroup(*[xsection(s[0]) for s in steps]).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).scale(0.75)
        row.move_to(UP * 0.4)
        names = VGroup(
            *[
                VGroup(text(s[1], size=22, weight="MEDIUM"), text(s[2], size=18, color=GATE)).arrange(DOWN, buff=0.08).next_to(p, DOWN, buff=0.3)
                for s, p in zip(steps, row)
            ]
        )
        self.play(ReplacementTransform(cur[0], row[-1]), FadeOut(cur[1]))
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in row[:-1]], lag_ratio=0.15), FadeIn(names))

    # --- title -------------------------------------------------------------------------------
    def title(self):
        self.slide(
            """
            The story starts in 1925, with a patent for a transistor that nobody could build.
            """
        )
        self.clear()
        kick = kicker("Lecture 1", color=GATE)
        ttl = display("The Switch That Wouldn't Turn Off", size=54)
        sub = text("How the transistor evolved, told through its physics", size=30, color=MUTED)
        VGroup(kick, ttl, sub).arrange(DOWN, buff=0.3).move_to(UP * 0.6)
        tl = Timeline(2045).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(kick), Write(ttl), run_time=1.6)
        self.play(FadeIn(sub), FadeIn(tl))
        self.play(tl.marker_to(1925), run_time=2.0)

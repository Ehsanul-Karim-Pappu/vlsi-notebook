"""Chapter 2 · The accidental transistor (1947–1951).

The point-contact transistor, Shockley's junction transistor and its energy hill, the
exponential I_C(V_BE) with its 60 mV per decade (planted here, explained in chapter 5), the
bipolar transistor that survives in a bandgap reference, and its cost: base current.
"""

import sys
from math import log10
from pathlib import Path

LECTURE = Path(__file__).resolve().parents[1]
IMAGES = LECTURE / "images"
sys.path[:0] = [str(LECTURE.parents[1]), str(LECTURE)]

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403
from manim_slides import Slide  # noqa: E402

import physics as phys  # noqa: E402
from kit.motifs import Barrier  # noqa: E402
from kit.style import *  # noqa: E402,F403

PLASTIC = "#5B6B80"


class Ch02AccidentalTransistor(Chapter, Slide):
    def construct(self):
        self.card()
        self.point_contact()
        self.junction()
        self.exponential()
        self.bandgap()
        self.cost()

    # --- card --------------------------------------------------------------------------------
    def card(self):
        self.slide(say(
            """
            Bell Labs, December 1947. Bardeen and Brattain are pressing metal points into a crystal
            of germanium to understand its surface. They are not trying to build an amplifier.
            """,
            """
            Bell Labs, December 1947। Bardeen আর Brattain একটা germanium crystal-এ metal point চাপ দিয়া
            ধরতেছেন, শুধু surface-টা বোঝার জন্য। Amplifier বানানোর কোনো plan তাদের ছিল না।
            """,
        ))
        self.card_group = self.open_chapter(
            2, 1947, 1925, "The accidental transistor",
            "Gold foil, a plastic wedge and a paper clip",
        )

    # --- the point-contact transistor --------------------------------------------------------
    def point_contact(self):
        pics = Group(
            figure(IMAGES / "first_transistor_replica.jpg", 6.0, "A replica. Photo: Mister rf, CC BY-SA 4.0"),
            figure(IMAGES / "bardeen_brattain_US2524035.png", 5.0, "Bardeen & Brattain, US patent 2,524,035, filed 1948"),
        ).arrange(RIGHT, buff=0.6, aligned_edge=DOWN).move_to(DOWN * 0.4)
        title, pics = self.show_figure(say(
            """
            This is a replica of the first transistor. And this is the drawing from Bardeen and
            Brattain's patent, filed in June 1948: two metal points pressed into a block of
            germanium, almost touching.
            """,
            """
            এইটা প্রথম transistor-এর একটা replica। আর এইটা Bardeen আর Brattain-এর patent-এর drawing, file
            করা June 1948-এ: একটা germanium block-এ দুইটা metal point চাপ দিয়া বসানো, প্রায় গায়ে গায়ে।
            """,
        ), "16 December 1947: the point-contact transistor", pics, clear=self.card_group)

        self.slide(say(
            """
            Here's how it's put together. A block of germanium. On top, a plastic wedge with gold foil
            wrapped around its tip, and the foil slit with a razor, so there are two gold contacts a
            hair's width apart. A spring made from a paper clip presses it down. Put a small signal
            into one contact, and a bigger copy comes out of the other. On the 16th of December 1947
            it amplified; on the 23rd they showed it to Bell Labs management. The transistor was
            born, out of an experiment on surfaces.
            """,
            """
            জিনিসটা কীভাবে বানানো, দেখেন। একটা germanium block। উপরে একটা plastic wedge, তার মাথায় gold
            foil মোড়ানো, আর razor দিয়ে foil-টা চিরে দেওয়া, যাতে একটা চুলের সমান দূরে দুইটা gold contact
            হয়। Paper clip বাঁকায়ে বানানো একটা spring সেটারে নিচে চেপে রাখে। এক contact-এ ছোট একটা signal
            দিলে, আরেকটা দিয়া তার বড় একটা copy বের হয়। 16 December 1947-এ এইটা amplify করল; 23 তারিখে
            Bell Labs management-রে দেখানো হইল। Transistor-এর জন্ম হইলো, surface নিয়া একটা experiment থেকে।
            """,
        ))
        self.play(FadeOut(pics))
        cx = -2.6
        block = Rectangle(width=4.6, height=1.5, fill_color=METAL, fill_opacity=0.3, stroke_color=METAL, stroke_width=2).move_to([cx, -1.55, 0])
        base = Rectangle(width=5.0, height=0.22, fill_color=METAL, fill_opacity=1, stroke_width=0).move_to([cx, -2.42, 0])
        tip_y = -0.8
        wedge = Polygon([cx - 1.0, 1.25, 0], [cx + 1.0, 1.25, 0], [cx, tip_y, 0], fill_color=PLASTIC, fill_opacity=1, stroke_width=0)
        foil_l = Line([cx - 0.75, 0.75, 0], [cx - 0.06, tip_y + 0.02, 0], stroke_color=GATE, stroke_width=6)
        foil_r = Line([cx + 0.75, 0.75, 0], [cx + 0.06, tip_y + 0.02, 0], stroke_color=GATE, stroke_width=6)
        zig = [[cx, 1.25 + 0.16 * i, 0] if i % 2 == 0 else [cx + (0.32 if i % 4 == 1 else -0.32), 1.25 + 0.16 * i, 0] for i in range(9)]
        spring = VMobject(stroke_color=METAL, stroke_width=4).set_points_as_corners(zig)
        lbl = VGroup(
            text("germanium", size=22, color=MUTED).move_to(block),
            text("base", size=20, color=MUTED).next_to(base, DOWN, buff=0.1),
            text("emitter", size=22, color=GATE).next_to(foil_l, LEFT, buff=0.2).shift(DOWN * 0.4),
            text("collector", size=22, color=GATE).next_to(foil_r, RIGHT, buff=0.2).shift(DOWN * 0.4),
            text("paper-clip spring", size=20, color=MUTED).next_to(spring, RIGHT, buff=0.3),
            text("plastic wedge, gold foil", size=20, color=MUTED).next_to(wedge, LEFT, buff=0.25).shift(UP * 0.6),
        )
        gap = text("~50 µm apart", size=18, color=GATE).next_to([cx, tip_y, 0], DOWN, buff=0.15)
        src = source("J. Bardeen & W. H. Brattain, Phys. Rev. 74, 230 (1948)")
        self.play(FadeIn(src))
        self.play(FadeIn(block), FadeIn(base), FadeIn(lbl[0]), FadeIn(lbl[1]))
        self.play(FadeIn(wedge, shift=DOWN * 0.3), Create(foil_l), Create(foil_r), FadeIn(lbl[2:4]), FadeIn(lbl[5]))
        self.play(Create(spring), FadeIn(lbl[4]), FadeIn(gap))

        # Signals: a small wiggle in, a bigger copy out.
        def wave(x0, y0, amp, color):
            return FunctionGraph(lambda x: y0 + amp * np.sin(9 * (x - x0)), x_range=[x0, x0 + 2.2], color=color, stroke_width=4)

        sin_in = wave(1.6, 1.0, 0.12, ELECTRON)
        sin_out = wave(1.6, -0.9, 0.55, GOOD)
        in_l = text("small signal in", size=22, color=ELECTRON).next_to(sin_in, UP, buff=0.15)
        out_l = text("bigger copy out", size=22, color=GOOD).next_to(sin_out, DOWN, buff=0.15)
        self.play(Create(sin_in), FadeIn(in_l), run_time=1.2)
        self.play(Create(sin_out), FadeIn(out_l), run_time=1.2)
        dates = VGroup(
            text("16 Dec 1947: it amplifies", size=22),
            text("23 Dec 1947: shown to management", size=22, color=MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        dates.move_to([0.9 + dates.width / 2, -2.6, 0])
        self.play(FadeIn(dates, shift=UP * 0.2))
        self.pc_parts = VGroup(title, block, base, wedge, foil_l, foil_r, spring, lbl, gap, src, sin_in, sin_out, in_l, out_l, dates)

    # --- the junction transistor -------------------------------------------------------------
    def junction(self):
        pics = Group(
            figure(IMAGES / "bardeen_shockley_brattain_1948.jpg", 4.8, "Bardeen, Shockley and Brattain, 1948. AT&T photo (public domain)"),
            figure(IMAGES / "shockley_US2569347.png", 3.2, "W. Shockley, US patent 2,569,347, filed 1948"),
        ).arrange(RIGHT, buff=0.5).move_to(DOWN * 0.3)
        title, pics = self.show_figure(say(
            """
            The famous Bell Labs photo from 1948: John Bardeen, William Shockley at the bench, and
            Walter Brattain. Shockley was not in the room for the discovery, and it stung. Within
            weeks he had worked out something better, and filed this patent in June 1948.
            """,
            """
            1948-এর বিখ্যাত Bell Labs ছবি: John Bardeen, bench-এ বসা William Shockley, আর Walter Brattain।
            ওই discovery-র সময় Shockley room-এ ছিলেন না, আর এইটা তাঁরে খোঁচাইছিল। কয়েক সপ্তাহের মধ্যেই তিনি
            আরও ভালো একটা জিনিস বের করলেন, আর June 1948-এ এই patent file করলেন।
            """,
        ), "1948: Shockley's junction transistor", pics, clear=self.pc_parts)

        self.slide(say(
            """
            Here it is: a transistor made entirely inside the crystal, the junction transistor. A
            thin layer of p-type material, the base, between two n-type regions, the
            emitter and the collector. Now look at its energy picture. A hill between emitter and
            collector, and the base voltage sets its height. Raise V-B-E and the hill comes down;
            electrons pour over. Hold on to this picture. It is exactly the picture of the MOSFET,
            and we'll come back to it.
            """,
            """
            এই যে: পুরাটাই crystal-এর ভিতরে বানানো একটা transistor, junction transistor। দুইটা n-type region, মানে emitter আর collector, তাদের মাঝে p-type-এর একটা পাতলা
            layer, base। এবার এর energy-র ছবিটা দেখেন। Emitter আর collector-এর মাঝে একটা hill, আর base
            voltage ঠিক করে hill-টা কত উঁচু। V-B-E বাড়াইলে hill নিচে নামে, electron হুড়মুড় করে পার হয়। এই
            ছবিটা মনে রাখেন। MOSFET-এর ছবিও হুবহু এইটাই, পরে আবার আসবো।
            """,
        ))
        self.play(FadeOut(pics))
        e = Rectangle(width=3.0, height=0.8, fill_color=ELECTRON, fill_opacity=0.35, stroke_width=0)
        b = Rectangle(width=0.7, height=0.8, fill_color=HOLE, fill_opacity=0.45, stroke_width=0)
        c = Rectangle(width=3.0, height=0.8, fill_color=ELECTRON, fill_opacity=0.35, stroke_width=0)
        bar = VGroup(e, b, c).arrange(RIGHT, buff=0).move_to([0, 2.2, 0])
        bar_l = VGroup(
            text("emitter (n)", size=22).move_to(e),
            text("base (p)", size=18).next_to(b, DOWN, buff=0.1),
            text("collector (n)", size=22).move_to(c),
        )
        self.play(FadeIn(bar), FadeIn(bar_l))

        self.vbe = ValueTracker(0.30)
        self.drop = ValueTracker(0.30)
        hill = Barrier(self.vbe, self.drop, n=140, origin=(0.0, -1.3), scale=6.5, seed=4)
        names = VGroup(
            text("emitter", size=22, color=MUTED).move_to([-3.1, -1.65, 0]),
            text("base", size=22, color=HOLE).move_to([0, 0.95, 0]),
            text("collector", size=22, color=MUTED).move_to([3.3, -3.55, 0]),
        )
        self.play(Create(hill.edge), FadeIn(names))
        self.play(FadeIn(hill.dots, scale=0.5, lag_ratio=0.004), run_time=1.2)
        hill.start()
        self.wait(1)
        raise_ = text("raise V_BE: the hill comes down", size=26, color=GATE).move_to([3.6, 0.5, 0])
        self.play(FadeIn(raise_), self.vbe.animate.set_value(0.07), run_time=3)
        self.wait(2)
        same = text("Same picture as the MOSFET.\nKeep it in mind.", size=26, weight="SEMIBOLD").move_to([3.8, -0.9, 0])
        self.play(FadeIn(same, shift=UP * 0.2))
        self.wait(1)
        hill.stop()
        self.jt_parts = VGroup(title, bar, bar_l, hill, names, raise_, same)

    # --- the exponential ---------------------------------------------------------------------
    def exponential(self):
        self.slide(say(
            """
            Because the electrons have to get over that hill, the collector current is exponential
            in the base-emitter voltage. On a log scale it's a straight line. And here is a number
            to remember: every 60 millivolts more on the base, ten times more current. I won't
            explain the 60 yet. It will come back in chapter five, and when it does, it'll be the
            most important number in this lecture.
            """,
            """
            Electron-গুলারে যেহেতু ওই hill পার হইতে হয়, collector current base-emitter voltage-এর সাথে
            exponential-ভাবে বাড়ে। Log scale-এ একটা সোজা line। আর একটা সংখ্যা মনে রাখেন: base-এ প্রতি 60
            millivolt বেশি দিলে current দশ গুণ। 60 কেন, এখন বলব না। Chapter five-এ এইটা ফিরে আসবে, আর
            তখন এইটাই হবে পুরা lecture-এর সবচেয়ে important সংখ্যা।
            """,
        ))
        self.play(FadeOut(self.jt_parts))
        title = heading("An exponential switch")
        off = 8  # plot log10(I) + 8, so the x axis sits at the bottom
        axes = Axes(
            x_range=[0.5, 0.8, 0.05], y_range=[0, 6, 1], x_length=7.0, y_length=4.6, tips=False,
            axis_config={"stroke_color": MUTED, "stroke_width": 2, "tick_size": 0.05},
        ).move_to([-1.8, -0.3, 0])
        axes.x_axis.add_labels({v: MathTex(f"{v:.1f}", font_size=26, color=MUTED) for v in (0.5, 0.6, 0.7, 0.8)}, font_size=26)
        axes.y_axis.add_labels({k: MathTex(f"10^{{{k - off}}}", font_size=26, color=MUTED) for k in (0, 2, 4, 6)}, font_size=26)
        xl = MathTex(r"V_{BE}\ (\text{V})", font_size=30, color=MUTED).next_to(axes.x_axis, DOWN, buff=0.5)
        yl = MathTex(r"I_C\ (\text{A})", font_size=30, color=MUTED).next_to(axes.y_axis, UP, buff=0.15)
        curve = axes.plot(lambda v: log10(phys.collector_current(v)) + off, x_range=[0.5, 0.8], color=ELECTRON, stroke_width=5)
        law = eq(r"I_C", r"=", r"I_S\,e^{\,qV_{BE}/", r"k_BT", r"}", size=50)
        law[3].set_color(THERMAL)
        law.move_to([4.0, 1.5, 0])
        beta = eq(r"\beta = \frac{I_C}{I_B} \approx 100", size=40).next_to(law, DOWN, buff=0.5)
        self.play(FadeIn(title), Create(axes), FadeIn(xl), FadeIn(yl))
        self.play(Create(curve), Write(law), run_time=2)
        ss = phys.subthreshold_swing(300)
        v0 = 0.58
        p0 = axes.c2p(v0, log10(phys.collector_current(v0)) + off)
        p1 = axes.c2p(v0 + ss, log10(phys.collector_current(v0)) + off)
        p2 = axes.c2p(v0 + ss, log10(phys.collector_current(v0 + ss)) + off)
        tri = VGroup(Line(p0, p1), Line(p1, p2)).set_stroke(GATE, 3)
        tri_l = VGroup(
            text("60 mV", size=22, color=GATE).next_to(Line(p0, p1), DOWN, buff=0.08),
            text("×10", size=22, color=GATE).next_to(Line(p1, p2), RIGHT, buff=0.08),
        )
        self.play(Create(tri), FadeIn(tri_l))
        plant = VGroup(
            text("+60 mV on the base:", size=30),
            text("ten times the current", size=30, color=GATE, weight="SEMIBOLD"),
            text("Why 60? Chapter 5.", size=24, color=MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.0, -1.4, 0])
        self.play(FadeIn(beta))
        self.play(FadeIn(plant, shift=UP * 0.2))
        self.exp_parts = VGroup(title, axes, xl, yl, curve, law, beta, tri, tri_l, plant)

    # --- the bandgap: the BJT you still draw -------------------------------------------------
    def bandgap(self):
        self.slide(say(
            """
            This isn't only history. In a CMOS chip the bipolar transistor survives as a parasitic:
            the vertical PNP you place in a bandgap reference. You've probably drawn this array: one
            unit device in the middle, eight around it, in common centroid so gradients cancel. Run
            both sides at the same current and the difference in their base-emitter voltages is k-T
            over q times the log of eight: about 54 millivolts, proportional to absolute
            temperature. The same exponential, doing useful work.
            """,
            """
            এইটা শুধু ইতিহাস না। CMOS chip-এ bipolar transistor টিকে আছে parasitic হিসাবে: bandgap
            reference-এ যে vertical PNP বসান, সেইটা। এই array-টা আপনারা নিশ্চয়ই আঁকছেন: মাঝখানে একটা unit
            device, চারপাশে আটটা, common centroid-এ, যাতে gradient cancel হয়ে যায়। দুই দিকে same current
            চালাইলে দুইটার base-emitter voltage-এর পার্থক্য হয় k-T বাই q গুণ ln 8: প্রায় 54 millivolt, যেটা
            absolute temperature-এর সাথে proportional। সেই একই exponential, এবার কাজের কাজ করতেছে।
            """,
        ))
        self.play(FadeOut(self.exp_parts))
        title = heading("You still lay this transistor out")
        cell = 1.05
        grid = VGroup()
        for r in range(3):
            for c in range(3):
                center = r == 1 and c == 1
                sq = Square(cell * 0.9, stroke_color=GATE if center else ELECTRON, stroke_width=3,
                            fill_color=GATE if center else ELECTRON, fill_opacity=0.25)
                sq.move_to([(c - 1) * cell - 3.8, (1 - r) * cell + 0.3, 0])
                emitter = Square(cell * 0.38, stroke_width=0, fill_color=GATE if center else ELECTRON, fill_opacity=0.9).move_to(sq)
                grid.add(VGroup(sq, emitter, text("Q1" if center else "Q2", size=16, color=BG, weight="SEMIBOLD").move_to(emitter)))
        ring = SurroundingRectangle(grid, buff=0.18, color=MUTED, stroke_width=2)
        ring_l = text("1 : 8 vertical PNP array,\ncommon centroid", size=20, color=MUTED).next_to(ring, DOWN, buff=0.15)
        dvbe = phys.delta_vbe(8)
        e1 = eq(r"\Delta V_{BE}", r"=", r"\frac{k_BT}{q}", r"\ln 8", size=52)
        e1[0].set_color(GATE)
        e1[2].set_color(THERMAL)
        e2 = eq(rf"= {dvbe * 1e3:.1f}\ \text{{mV at 300 K}}", size=40)
        e3 = text("∝ T: the PTAT half of a bandgap", size=26, color=THERMAL)
        col = VGroup(e1, e2, e3).arrange(DOWN, buff=0.35).move_to([2.6, 1.2, 0])
        note = layout_note("Common centroid so process gradients hit Q1 and Q2 alike; dummies around the edge.", size=22, width=44)
        note.move_to([2.6, -1.9, 0])
        self.play(FadeIn(title))
        self.play(LaggedStart(*[FadeIn(g, scale=0.8) for g in grid], lag_ratio=0.08), run_time=1.5)
        self.play(Create(ring), FadeIn(ring_l))
        self.play(Write(e1))
        self.play(FadeIn(e2), FadeIn(e3))
        self.play(FadeIn(note, shift=UP * 0.2))
        self.bg_parts = VGroup(title, grid, ring, ring_l, col, note)

    # --- the cost ----------------------------------------------------------------------------
    def cost(self):
        self.slide(say(
            """
            But as a building block for logic, the bipolar transistor has a cost. To keep it on you
            must keep pushing current into the base, all the time, so a logic gate built from them
            burns power just sitting there. The field-effect idea, which needs almost no input
            current, was still blocked by those surface states, and germanium surfaces were
            especially bad. The answer came from silicon, and from something that grew on silicon
            by accident.
            """,
            """
            কিন্তু logic বানানোর block হিসাবে bipolar transistor-এর একটা দাম আছে। ওইটারে on রাখতে হলে base-এ
            সারাক্ষণ current ঢালতে হয়, তাই এগুলা দিয়া বানানো logic gate চুপচাপ বসে থেকেও power খায়।
            Field-effect-এর idea, যেটায় input current প্রায় লাগেই না, সেটা তখনো surface states-এর কাছে আটকা,
            আর germanium-এর surface ছিল বিশেষ করে খারাপ। Answer আসলো silicon থেকে, আর silicon-এর উপর
            accident-এ জন্মানো একটা জিনিস থেকে।
            """,
        ))
        self.play(FadeOut(self.bg_parts))
        title = heading("The catch: a bipolar switch is always eating")
        x0, y0 = -3.0, -0.2
        base_bar = Line([x0, y0 - 0.7, 0], [x0, y0 + 0.7, 0], stroke_color=INK, stroke_width=6)
        base_in = Line([x0 - 1.6, y0, 0], [x0, y0, 0], stroke_color=INK, stroke_width=4)
        col = Line([x0, y0 + 0.35, 0], [x0 + 1.0, y0 + 1.1, 0], stroke_color=INK, stroke_width=4)
        col_up = Line([x0 + 1.0, y0 + 1.1, 0], [x0 + 1.0, y0 + 2.2, 0], stroke_color=INK, stroke_width=4)
        emi = Arrow([x0, y0 - 0.35, 0], [x0 + 1.0, y0 - 1.1, 0], buff=0, stroke_color=INK, stroke_width=4, max_tip_length_to_length_ratio=0.25)
        emi_dn = Line([x0 + 1.0, y0 - 1.1, 0], [x0 + 1.0, y0 - 2.2, 0], stroke_color=INK, stroke_width=4)
        sym = VGroup(base_bar, base_in, col, col_up, emi, emi_dn)
        ib = Arrow([x0 - 1.6, y0 + 0.25, 0], [x0 - 0.3, y0 + 0.25, 0], buff=0, stroke_color=DRAIN, stroke_width=5)
        ib_l = MathTex("I_B", color=DRAIN, font_size=40).next_to(ib, UP, buff=0.1)
        ib_n = text("must flow all the time\nto stay ON", size=22, color=DRAIN).next_to(ib_l, UP, buff=0.15)
        self.play(FadeIn(title))
        self.play(Create(sym), run_time=1.2)
        self.play(GrowArrow(ib), FadeIn(ib_l), FadeIn(ib_n))
        pts = VGroup(
            text("a logic gate of these\nburns power standing still", size=26),
            text("the field effect needs\nalmost no input current…", size=26),
            text("…but surface states\nstill block it", size=26, color=MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([2.7, 0.5, 0])
        for p in pts:
            self.play(FadeIn(p, shift=RIGHT * 0.15), run_time=0.8)
        nxt = text("The answer would grow on silicon, by accident.", size=32, color=GATE, weight="SEMIBOLD")
        nxt.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(nxt, shift=UP * 0.2))

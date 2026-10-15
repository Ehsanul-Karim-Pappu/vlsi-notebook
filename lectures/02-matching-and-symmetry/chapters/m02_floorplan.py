"""Lecture 2 · M2 · Reading the OTA for matching.

The matched groups on the schematic, ranked by how directly their error reaches the input; the
symmetry axis; and the floorplan that keeps it, block by block.
"""

import sys
from pathlib import Path

LECTURE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(LECTURE.parents[1]), str(LECTURE)]

from manim import *  # noqa: E402,F403
from manim_slides import Slide  # noqa: E402

from common import A_COL, B_COL, C_COL, Schematic, chapter_title, illustrative  # noqa: E402
from kit.style import *  # noqa: E402,F403

GROUPS = [  # (ids, colour, name, how its error reaches the input, bar length)
    (["M1", "M2"], A_COL, "M1 · M2  input pair", "directly: its offset is the input offset", 1.0),
    (["M3", "M4"], B_COL, "M3 · M4  current sources", "scaled down by their g_m against the pair's", 0.55),
    (["M9", "M10"], B_COL, "M9 · M10  current sinks", "scaled down the same way", 0.5),
    (["M5", "M6", "M7", "M8"], C_COL, "M5 – M8  cascodes", "barely: they pass current, they don't set it", 0.12),
    (["M11"], MUTED, "M11  tail", "common to both halves: not a pair", 0.05),
]


def block(w, h, label, color, sub=None):
    r = RoundedRectangle(width=w, height=h, corner_radius=0.06, stroke_color=color, stroke_width=3,
                         fill_color=interpolate_color(ManimColor(BG), ManimColor(color), 0.18), fill_opacity=1)
    t = text(label, size=20, color=color, weight="SEMIBOLD")
    g = VGroup(t, text(sub, size=16, color=INK).set_opacity(0.75)).arrange(DOWN, buff=0.05) if sub else t
    return VGroup(r, g.move_to(r))


class M02Floorplan(Chapter, Slide):
    def construct(self):
        self.card()
        self.groups()
        self.ranking()
        self.axis()
        self.floorplan()
        self.why_rows()

    def card(self):
        self.slide(say(
            """
            Chapter two: reading the amplifier for matching. Before placing a single transistor,
            a layout engineer should be able to look at the schematic and answer three questions.
            Which devices are twins? Which twins matter most? And where's the line of symmetry
            the whole layout will be built around?
            """,
            """
            Chapter two: matching-এর চোখে amplifier পড়া। একটা transistor-ও বসানোর আগে, একজন layout engineer-এর schematic
            দেখে তিনটা প্রশ্নের উত্তর দিতে পারা উচিত। কোন device-গুলা যমজ? কোন যমজ সবচেয়ে গুরুত্বপূর্ণ? আর পুরা layout যে
            symmetry-র রেখা ঘিরে বানানো হবে, সেইটা কোথায়?
            """,
        ))
        self.card_group = chapter_title(2, "Reading the OTA for matching", "Which twins, how much they matter, and the axis")
        self.play(FadeIn(self.card_group, shift=UP * 0.2), run_time=1.2)

    def groups(self):
        self.slide(say(
            """
            The twins, group by group. The input pair, M1 and M2. The PMOS current sources, M3 and
            M4, on top. The NMOS current sinks, M9 and M10, at the bottom, which the common-mode
            feedback drives. The cascodes, M5 to M8, between them. And the tail, M11, which has no
            twin: it's shared by both halves. Every device except the tail is half of a pair.
            """,
            """
            যমজগুলা, group ধরে ধরে। Input pair, M1 আর M2। উপরে PMOS current source, M3 আর M4। নিচে NMOS current sink, M9
            আর M10, যেগুলা common-mode feedback চালায়। মাঝখানে cascode-গুলা, M5 থেকে M8। আর tail, M11, যার কোনো যমজ নাই:
            দুই অর্ধেকই এইটা ভাগ করে। Tail ছাড়া প্রত্যেকটা device একটা pair-এর অর্ধেক।
            """,
        ))
        self.play(FadeOut(self.card_group))
        sch = Schematic("ota", 4.6).move_to([-2.6, -0.2, 0])
        title = heading("The twins")
        self.play(FadeIn(title), FadeIn(sch))
        legend = VGroup()
        rings = VGroup()
        for ids, color, name, _, _ in GROUPS:
            if ids == ["M5", "M6", "M7", "M8"]:
                r = VGroup(sch.ring(["M5", "M7"], color), sch.ring(["M6", "M8"], color))
            elif len(ids) == 2 and ids != ["M1", "M2"]:
                r = VGroup(sch.ring([ids[0]], color), sch.ring([ids[1]], color))
            else:
                r = sch.ring(ids, color)
            rings.add(r)
            legend.add(VGroup(Square(0.22, stroke_width=0, fill_color=color, fill_opacity=0.9),
                              text(name, size=22, color=INK)).arrange(RIGHT, buff=0.2))
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(sch, RIGHT, buff=0.5)
        for r, l in zip(rings, legend):
            self.play(Create(r), FadeIn(l, shift=LEFT * 0.1), run_time=0.7)
        self.sch, self.rings, self.legend, self.title = sch, rings, legend, title

    def ranking(self):
        self.slide(say(
            """
            Now rank them, by how directly their error reaches the input. The input pair is first:
            any difference between M1 and M2 is the input offset, one for one. The current sources
            and sinks come next: their difference shows up at the input too, but scaled down by how
            strong they are compared with the input pair. That's why designers make them long and
            weak. The cascodes barely matter for offset: they pass the current along, they don't
            set it. The tail is common to both sides. So the input pair gets your best real estate
            and your most careful arrangement, then the sources and sinks.
            """,
            """
            এবার এদের ranking করেন, এদের error কতটা সরাসরি input-এ পৌঁছায় তা দিয়া। Input pair প্রথম: M1 আর M2-এর যেকোনো
            পার্থক্যই input offset, এক-এক করে। তারপর current source আর sink: এদের পার্থক্যও input-এ দেখা যায়, কিন্তু input
            pair-এর তুলনায় এরা কতটা শক্তিশালী সেই অনুপাতে ছোট হয়ে। এই জন্যই designer-রা এগুলারে লম্বা আর দুর্বল বানায়।
            Offset-এর জন্য cascode প্রায় কিছুই না: এরা current এগিয়ে দেয়, ঠিক করে না। Tail দুই দিকেরই common। তাই input
            pair পায় আপনার সবচেয়ে ভালো জায়গা আর সবচেয়ে যত্নের সাজানো, তারপর source আর sink।
            """,
        ))
        self.play(FadeOut(self.sch), FadeOut(self.rings), FadeOut(self.legend))
        self.play(Transform(self.title, heading("Ranked: how directly the error reaches the input")))
        rows = VGroup()
        for _, color, name, how, frac in GROUPS:
            bar = Rectangle(width=max(4.6 * frac, 0.06), height=0.3, stroke_width=0, fill_color=color, fill_opacity=0.85)
            rows.add(VGroup(text(name, size=24, color=INK, weight="SEMIBOLD"), bar, text(how, size=20, color=MUTED)))
        for k, r in enumerate(rows):
            r[0].move_to([-6.6, 2.0 - k * 0.95, 0], aligned_edge=LEFT)
            r[1].move_to([-1.9, 2.0 - k * 0.95, 0], aligned_edge=LEFT)
            r[2].next_to(r[1], DOWN, buff=0.1).align_to(r[1], LEFT)
        note = text("the order, not the numbers: the lengths are illustrative", size=18, color=MUTED).to_edge(DOWN, buff=0.4)
        for r in rows:
            self.play(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), FadeIn(r[2]), run_time=0.7)
        self.play(FadeIn(note))
        self.rank_rows, self.note = rows, note

    def axis(self):
        self.slide(say(
            """
            Next, the axis. Draw a vertical line through the middle of the schematic. Everything on
            the left has a mirror image on the right: M1 and M2, M3 and M4, every cascode, every
            sink, and the two outputs. Only the tail sits on the line. The layout keeps this exact
            axis. If the left half of the layout is a mirror image of the right half, then
            whatever the silicon does to one side, a gradient, a nearby heater, a neighbour, it does
            to the other side as well.
            """,
            """
            এরপর, axis। Schematic-এর মাঝখান দিয়া একটা খাড়া রেখা টানেন। বামে যা আছে তার প্রত্যেকটার ডানে একটা mirror image
            আছে: M1 আর M2, M3 আর M4, প্রত্যেকটা cascode, প্রত্যেকটা sink, আর দুইটা output। শুধু tail রেখার উপর বসে। Layout
            ঠিক এই axis-টাই রাখে। Layout-এর বাম অর্ধেক যদি ডান অর্ধেকের mirror image হয়, তাহলে silicon এক দিকে যা করে, একটা
            gradient, পাশের একটা heater, একটা প্রতিবেশী, অন্য দিকেও সেইটাই করে।
            """,
        ))
        self.play(FadeOut(self.rank_rows), FadeOut(self.note))
        self.play(Transform(self.title, heading("One axis, on paper and in layout")))
        sch = Schematic("ota", 4.9).move_to([0, -0.3, 0])
        top, bottom = sch.point(350, 16), sch.point(350, 388)
        line = DashedLine(top, bottom, stroke_color=GATE, stroke_width=4, dash_length=0.12)
        tag = text("axis", size=22, color=GATE, weight="SEMIBOLD").next_to(sch[0], UP, buff=0.1)
        pairs = VGroup(*[VGroup(sch.ring([a], GATE, width=2), sch.ring([b], GATE, width=2))
                         for a, b in (("M3", "M4"), ("M5", "M6"), ("M7", "M8"), ("M9", "M10"))],
                       sch.ring(["M1", "M2"], GATE, width=2))
        self.play(FadeIn(sch))
        self.play(Create(line), FadeIn(tag))
        self.play(LaggedStart(*[Create(p) for p in pairs], lag_ratio=0.15), run_time=1.5)
        self.axis_group = VGroup(line, pairs, tag)
        self.sch = sch

    def floorplan(self):
        self.slide(say(
            """
            And the floorplan that follows from it. Rows, top to bottom, the way current flows:
            the PMOS sources M3 and M4 under the supply rail, then their cascodes; the input pair
            in the middle, with the tail right under it on the axis; then the NMOS cascodes, and
            the sinks above the ground rail. Every row is centred on the axis, and every row is
            one matched group. The outputs leave on both sides at the same height. The CMFB's
            resistors and capacitors sit below, also on the axis. And the bias circuit goes off to
            one side, never between the halves.
            """,
            """
            আর এর থেকে যে floorplan আসে। Row-গুলা, উপর থেকে নিচে, current যেভাবে চলে: supply rail-এর নিচে PMOS source M3
            আর M4, তারপর তাদের cascode; মাঝখানে input pair, তার ঠিক নিচে axis-এর উপর tail; তারপর NMOS cascode, আর ground
            rail-এর উপরে sink-গুলা। প্রত্যেকটা row axis-এ centre করা, আর প্রত্যেকটা row একটা matched group। Output দুই দিক
            থেকে একই উচ্চতায় বের হয়। CMFB-এর resistor আর capacitor নিচে বসে, সেইটাও axis-এর উপর। আর bias circuit যায় এক
            পাশে, কখনো দুই অর্ধেকের মাঝখানে না।
            """,
        ))
        self.play(FadeOut(self.sch), FadeOut(self.axis_group))
        self.play(Transform(self.title, heading("The floorplan, block by block")))
        x0 = 0.4

        def rail(y, s):
            return VGroup(Rectangle(width=6.2, height=0.14, stroke_width=0, fill_color=METAL, fill_opacity=0.9)
                          .move_to([x0, y, 0]), text(s, size=16, color=MUTED).move_to([x0 - 3.55, y, 0]))


        vdd = rail(2.75, "VDD")
        well = Rectangle(width=6.0, height=1.5, stroke_width=0, fill_color=NWELL, fill_opacity=0.35).move_to([x0, 1.95, 0])
        rows = VGroup(
            block(5.4, 0.6, "M3 · M4", B_COL, "sources, interdigitated, dummies").move_to([x0, 2.25, 0]),
            block(5.4, 0.5, "M5 · M6", C_COL, "cascodes, in line with M3 · M4").move_to([x0, 1.55, 0]),
            block(4.2, 0.7, "M1 · M2", A_COL, "input pair, cross-quad, dummy ring").move_to([x0, 0.6, 0]),
            block(1.4, 0.4, "M11 tail", MUTED).move_to([x0, -0.15, 0]),
            block(5.4, 0.5, "M7 · M8", C_COL, "cascodes").move_to([x0, -0.85, 0]),
            block(5.4, 0.6, "M9 · M10", B_COL, "sinks, interdigitated, dummies").move_to([x0, -1.6, 0]),
        )
        gnd = rail(-2.15, "GND")
        cmfb = block(4.0, 0.6, "CMFB: R1 · R2,  C1 · C2", GATE, "unit arrays, on the axis").move_to([x0, -2.85, 0])
        bias = block(1.5, 2.2, "bias", MUTED, "off to\none side").move_to([x0 + 4.95, 0.9, 0])
        ax = DashedLine([x0, 3.05, 0], [x0, -3.3, 0], stroke_color=GATE, stroke_width=3, dash_length=0.1)
        outs = VGroup(Arrow([x0 - 2.7, -0.35, 0], [x0 - 3.9, -0.35, 0], buff=0, stroke_color=INK, stroke_width=4),
                      Arrow([x0 + 2.7, -0.35, 0], [x0 + 3.9, -0.35, 0], buff=0, stroke_color=INK, stroke_width=4))
        out_l = VGroup(text("V_OUT−", size=18).next_to(outs[0], DOWN, buff=0.05),
                       text("V_OUT+", size=18).next_to(outs[1], DOWN, buff=0.05))
        tag = illustrative().to_corner(DL, buff=0.3)
        self.add(ax)
        self.play(FadeIn(vdd), FadeIn(gnd), FadeIn(well), Create(ax), FadeIn(tag))
        self.play(LaggedStart(*[FadeIn(r, shift=DOWN * 0.1) for r in rows], lag_ratio=0.2), run_time=2.2)
        self.play(GrowArrow(outs[0]), GrowArrow(outs[1]), FadeIn(out_l))
        self.play(FadeIn(cmfb), FadeIn(bias))
        self.plan = VGroup(vdd, gnd, well, ax, rows, cmfb, bias, outs, out_l)

    def why_rows(self):
        self.slide(say(
            """
            Why rows, and why this order? Each row holds one matched group, so the two halves of a
            pair are as close as they can be, and the arrangement within a row can cancel
            gradients. The order follows the current, so the connections between rows are short
            and run straight up and down, the same on both sides. And because every row is centred
            on the same axis, the whole block is a mirror image. That one decision cancels more
            mismatch than any trick inside a single row.
            """,
            """
            Row কেন, আর এই ক্রম কেন? প্রত্যেকটা row একটা matched group রাখে, তাই একটা pair-এর দুই অর্ধেক যতটা সম্ভব কাছে থাকে,
            আর একটা row-এর ভিতরের সাজানো gradient কাটতে পারে। ক্রমটা current-এর পিছনে পিছনে যায়, তাই row-গুলার মধ্যের connection
            ছোট আর সোজা উপর-নিচে চলে, দুই দিকে একই রকম। আর যেহেতু প্রত্যেকটা row একই axis-এ centre করা, পুরা block একটা mirror
            image। এই একটা সিদ্ধান্ত একটা row-এর ভিতরের যেকোনো কৌশলের চেয়ে বেশি mismatch কাটে।
            """,
        ))
        notes = VGroup(
            text("one row, one matched group", size=22, color=INK),
            text("rows in the order current flows", size=22, color=INK),
            text("every row centred on the axis", size=22, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        ticks = VGroup(*[text("✓", size=24, color=GOOD).next_to(n, LEFT, buff=0.2) for n in notes])
        box = VGroup(ticks, notes).move_to([-4.9, 0.4, 0])
        self.play(self.plan.animate.scale(0.85).shift(RIGHT * 1.2))
        box.next_to(self.plan, LEFT, buff=0.5)
        self.play(LaggedStart(*[FadeIn(VGroup(t, n), shift=RIGHT * 0.1) for t, n in zip(ticks, notes)], lag_ratio=0.3))

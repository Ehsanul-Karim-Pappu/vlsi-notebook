"""Lecture 2 · M7 · The bandgap.

What must match and how much each error is amplified; Q1 at the centre of a 3 × 3 array with
Q2's eight around it and a dummy ring; R1 and R2 from one unit resistor; M1–M3 interleaved; the
amplifier's pair; placement on the die; trimming as the last resort.
"""

import sys
from pathlib import Path

LECTURE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(LECTURE.parents[1]), str(LECTURE)]

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403
from manim_slides import Slide  # noqa: E402

from common import (A_COL, B_COL, C_COL, Schematic, array, chapter_title, illustrative, meter, pdk_tag,  # noqa: E402
                    placed, stripe)
from kit.style import *  # noqa: E402,F403


def relabel(cells, names, size=18):
    for c in cells:
        if c.label in names:
            c[1].become(text(names[c.label], size=size, color=c[0].get_stroke_color(), weight="BOLD").move_to(c))
    return cells


class M07Bandgap(Chapter, Slide):
    def construct(self):
        self.card()
        self.what_matters()
        self.bjt_array()
        self.bjt_ring()
        self.resistors()
        self.mirror()
        self.amplifier()
        self.placement()
        self.trim()

    def card(self):
        self.slide(say(
            """
            Chapter seven: the bandgap. Its whole job is one accurate voltage that doesn't move
            with temperature, and it gets there by subtracting two things that are nearly equal.
            That makes it a magnifying glass for mismatch: small errors in the wrong places come
            out multiplied.
            """,
            """
            Chapter seven: bandgap। এর পুরা কাজ একটা নির্ভুল voltage, যেটা temperature-এর সাথে নড়ে না, আর সেখানে পৌঁছায় প্রায়
            সমান দুইটা জিনিস বিয়োগ করে। তাই এইটা mismatch-এর জন্য একটা magnifying glass: ভুল জায়গায় ছোট error বড় হয়ে বের হয়।
            """,
        ))
        self.card_group = chapter_title(7, "The bandgap", "Where small errors come out multiplied")
        self.play(FadeIn(self.card_group, shift=UP * 0.2), run_time=1.2)

    def what_matters(self):
        self.slide(say(
            """
            What must match, in order. First, the amplifier's input pair. Its offset sits in
            series with the small voltage difference between Q1 and Q2, and that difference gets
            multiplied by R2 over R1, typically about ten, on its way to V_REF. So a one-millivolt
            offset becomes about ten millivolts of error. Then Q1 against Q2's eight units, which
            create that voltage difference. Then the ratio of R2 to R1. Then the mirror, M1 to M3,
            which copies the current. Notice what's not on the list: the absolute value of any
            resistor. Only ratios matter, and ratios are what layout controls.
            """,
            """
            কী মিলতে হবে, ক্রমানুসারে। প্রথমে, amplifier-এর input pair। এর offset Q1 আর Q2-এর মধ্যের ছোট voltage পার্থক্যের সাথে
            series-এ বসে, আর ওই পার্থক্য V_REF-এ যাওয়ার পথে R2 ভাগ R1 দিয়া গুণ হয়, সাধারণত দশের মতো। তাই এক millivolt offset প্রায়
            দশ millivolt error হয়ে যায়। তারপর Q1 বনাম Q2-এর আটটা unit, যারা ওই voltage পার্থক্য তৈরি করে। তারপর R2 আর R1-এর ratio।
            তারপর mirror, M1 থেকে M3, যেটা current copy করে। খেয়াল করেন list-এ কী নাই: কোনো resistor-এর absolute মান। শুধু ratio
            গুরুত্বপূর্ণ, আর ratio-ই layout নিয়ন্ত্রণ করে।
            """,
        ))
        self.play(FadeOut(self.card_group))
        title = heading("What must match, in order")
        sch = Schematic("bandgap", 3.6).move_to([-3.6, -0.3, 0])
        items = [
            (["A1"], THERMAL, "1  the amplifier's pair", "its offset is multiplied by R2/R1, ×10 or so"),
            (["Q1", "Q2"], A_COL, "2  Q1 against Q2's eight", "they make the voltage that gets multiplied"),
            (["R1", "R2"], B_COL, "3  R2 against R1", "the multiplier itself: a ratio"),
            (["M1", "M2", "M3"], C_COL, "4  the mirror M1 – M3", "copies the current"),
        ]
        rows = VGroup()
        rings = VGroup()
        for ids, color, head, sub in items:
            if ids == ["R1", "R2"]:
                rings.add(VGroup(sch.ring(["R1"], color), sch.ring(["R2"], color)))
            elif ids == ["Q1", "Q2"]:
                rings.add(VGroup(sch.ring(["Q1"], color), sch.ring(["Q2"], color)))
            else:
                rings.add(sch.ring(ids, color))
            rows.add(VGroup(text(head, size=24, color=color, weight="SEMIBOLD"), text(sub, size=20, color=MUTED)
                            ).arrange(DOWN, aligned_edge=LEFT, buff=0.08))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to([3.4, -0.1, 0])
        foot = text("not on the list: any resistor's absolute value", size=22, color=GATE).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(title), FadeIn(sch))
        for r, row in zip(rings, rows):
            self.play(Create(r), FadeIn(row, shift=LEFT * 0.1), run_time=0.8)
        self.play(FadeIn(foot))

    def bjt_array(self):
        self.slide(say(
            """
            Q1 and Q2. Q2 is eight copies of Q1, so draw nine identical units in a three-by-three
            square: Q1 in the centre, Q2's eight all around it. The centroid of the eight is the
            centre, exactly where Q1 is. So a straight gradient in any direction cancels: whatever
            it adds to Q1, it adds on average to Q2 as well. Watch the gradient turn; the leftover
            stays at zero.
            """,
            """
            Q1 আর Q2। Q2 হইল Q1-এর আটটা copy, তাই নয়টা একই রকম unit একটা তিন-বাই-তিন square-এ আঁকেন: মাঝখানে Q1, চারপাশে
            Q2-এর আটটা। আটটার centroid হইল মাঝখান, ঠিক যেখানে Q1। তাই যেকোনো দিকের একটা সোজা gradient কেটে যায়: Q1-এ যা যোগ
            করে, গড়ে Q2-তেও তাই যোগ করে। Gradient ঘুরতে দেখেন; বাকিটা শূন্যেই থাকে।
            """,
        ))
        self.clear()
        title = heading("Q1 in the centre, Q2's eight around it")
        rows = ["BBB", "BAB", "BBB"]
        g = placed(rows, size=0.8, gap=0.12).move_to([-2.4, 0.0, 0])
        relabel(g.cells, {"A": "Q1", "B": "Q2"}, 22)
        m = meter(g.error).move_to([3.8, -1.6, 0])
        side = VGroup(text("1 : 8, common centroid", size=28, color=GATE, weight="SEMIBOLD"),
                      text("both centroids at the centre", size=22, color=INK),
                      text("cancels: a straight gradient,\nany direction", size=22, color=GOOD),
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.8, 0.9, 0])
        tag = illustrative().to_corner(DL, buff=0.3)
        self.play(FadeIn(title), FadeIn(g.field), FadeIn(g.cells), FadeIn(tag))
        self.play(FadeIn(g.marks, scale=1.4), FadeIn(side), FadeIn(m))
        for ang in (0.9, 1.9, 2.8):
            g2 = placed(rows, angle=ang, size=0.8, gap=0.12).move_to([-2.4, 0.0, 0])
            self.play(Transform(g.field, g2.field), run_time=1.0)

    def bjt_ring(self):
        self.slide(say(
            """
            Then the ring. The outer eight have empty space on one side; Q1 is surrounded. So
            add a ring of dummy transistors, the same drawing, sixteen of them, and now every one
            of the nine sees the same neighbours. Some designs use the ring's positions for Q3 or
            spare units. The whole five-by-five block is compact and square, which also keeps
            the curvature it sits on small.
            """,
            """
            তারপর ring। বাইরের আটটার এক পাশে খালি জায়গা; Q1 চারদিক থেকে ঘেরা। তাই dummy transistor-এর একটা ring যোগ করেন, একই
            drawing, ষোলটা, আর এখন নয়টার প্রত্যেকটা একই প্রতিবেশী দেখে। কিছু design ring-এর জায়গাগুলা Q3 বা বাড়তি unit-এর জন্য
            use করে। পুরা পাঁচ-বাই-পাঁচ block compact আর square, যেটা নিচের curvature-ও ছোট রাখে।
            """,
        ))
        self.clear()
        title = heading("A dummy ring around the nine")
        g = array(["DDDDD", "DBBBD", "DBABD", "DBBBD", "DDDDD"], 0.72, 0.1).move_to([-2.4, -0.2, 0])
        relabel(g, {"A": "Q1", "B": "Q2"}, 20)
        side = VGroup(text("5 × 5: 1 + 8 + 16 dummies", size=28, color=GATE, weight="SEMIBOLD"),
                      text("every real unit sees the same\nneighbours", size=22, color=INK),
                      text("compact and square: little\ncurvature across it", size=22, color=INK),
                      text("cancels: edge effects, and\nwhat's left of curvature", size=22, color=GOOD),
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.8, 0.0, 0])
        tag = pdk_tag().to_corner(DR, buff=0.3)
        self.play(FadeIn(title), FadeIn(g, lag_ratio=0.03), run_time=1.5)
        self.play(FadeIn(side), FadeIn(tag))

    def resistors(self):
        self.slide(say(
            """
            R1 and R2. Their absolute value can be off by fifteen or twenty percent from wafer to
            wafer, and the bandgap doesn't care, because only the ratio counts. Draw both from one
            unit resistor: here R1 is two units and R2 twenty. Put R1's two in the middle and R2's
            twenty split evenly on both sides, so both centroids sit on the axis. Same width, same
            orientation, same heads, dummies at both ends. Now the ratio is set by counting
            units, and counting doesn't drift.
            """,
            """
            R1 আর R2। এদের absolute মান wafer থেকে wafer-এ পনেরো-বিশ percent এদিক-ওদিক হইতে পারে, আর bandgap-এর কিছু যায় আসে না,
            কারণ শুধু ratio গোনা হয়। দুইটাই একটা unit resistor থেকে আঁকেন: এখানে R1 দুই unit আর R2 বিশ। R1-এর দুইটা মাঝখানে, আর R2-এর
            বিশটা দুই পাশে সমান ভাগ করে, তাই দুইটা centroid-ই axis-এর উপর। একই width, একই orientation, একই head, দুই মাথায় dummy।
            এখন ratio ঠিক হয় unit গুনে, আর গোনা কখনো drift করে না।
            """,
        ))
        self.clear()
        title = heading("R1 · R2: one unit, counted")
        pattern = "D" + "B" * 10 + "AA" + "B" * 10 + "D"
        stripes = VGroup(*[stripe(c, height=1.9, width=0.2) for c in pattern]).arrange(RIGHT, buff=0.1).move_to([0, 0.6, 0])
        ax = DashedLine([0, 1.9, 0], [0, -0.7, 0], stroke_color=GATE, stroke_width=3, dash_length=0.08)
        lab = VGroup(text("R1 = 2 units", size=24, color=A_COL), text("R2 = 20 units", size=24, color=B_COL),
                     text("R2 / R1 = 10, by counting", size=24, color=GATE, weight="SEMIBOLD")).arrange(RIGHT, buff=0.7).move_to([0, -1.3, 0])
        notes = text("absolute value: ±15–20 % · the ratio of matched units: a fraction of a percent", size=20,
                     color=MUTED).to_edge(DOWN, buff=1.0)
        tag = pdk_tag().to_corner(DR, buff=0.3)
        self.play(FadeIn(title), FadeIn(stripes, lag_ratio=0.03), run_time=1.4)
        self.play(Create(ax), FadeIn(lab))
        self.play(FadeIn(notes), FadeIn(tag))

    def mirror(self):
        self.slide(say(
            """
            The mirror, M1, M2 and M3. Three devices now, but the same idea: split each into
            units and interleave them so all three centroids coincide. A B C C B A, with dummies
            at the ends, in one row under the supply rail, the rail fed from the middle. If M3 is
            meant to carry a different current from the other two, give it a different number of
            the same units.
            """,
            """
            Mirror, M1, M2 আর M3। এখন তিনটা device, কিন্তু একই ধারণা: প্রত্যেকটারে unit-এ ভাগ করেন আর মিশিয়ে দেন যাতে তিনটা centroid-ই
            মিলে যায়। A B C C B A, মাথায় dummy সহ, supply rail-এর নিচে এক row-তে, rail মাঝখান থেকে feed করা। M3-এর যদি বাকি দুইটা থেকে
            আলাদা current বহন করার কথা থাকে, তারে একই unit-এর আলাদা সংখ্যা দেন।
            """,
        ))
        self.clear()
        title = heading("M1 · M2 · M3: three centroids, one point")
        row = array(["DABCCBAD"], 0.75).move_to([0, 0.5, 0])
        relabel(row, {"A": "M1", "B": "M2", "C": "M3"}, 18)
        rail = Rectangle(width=row.width + 0.4, height=0.16, stroke_width=0, fill_color=METAL, fill_opacity=0.9).next_to(row, UP, buff=0.35)
        feed = Arrow(rail.get_top() + UP * 0.55, rail.get_top(), buff=0, stroke_color=GATE, stroke_width=5)
        feed_l = text("VDD, fed from the middle", size=18, color=GATE).next_to(feed, RIGHT, buff=0.15)
        from common import centroid, centroid_mark

        marks = VGroup(*[centroid_mark(centroid(row, k), c, 0.13) for k, c in (("A", A_COL), ("B", B_COL), ("C", C_COL))])
        note = text("all three centroids at the centre", size=22, color=GOOD).next_to(row, DOWN, buff=0.45)
        self.play(FadeIn(title), FadeIn(row), FadeIn(rail))
        self.play(GrowArrow(feed), FadeIn(feed_l))
        self.play(FadeIn(marks, scale=1.4), FadeIn(note))

    def amplifier(self):
        self.slide(say(
            """
            And the amplifier, the most sensitive part of all, because its offset gets multiplied.
            Its input pair is a cross-quad with a dummy ring, exactly like the OTA's input pair in
            chapter three, and it's sized generously, because random offset only shrinks with
            area. Its inputs, X and Y, are routed as mirror images. Some designs go further and
            chop the amplifier, swapping its inputs back and forth so its offset averages out; but
            the layout still comes first.
            """,
            """
            আর amplifier, সবচেয়ে সংবেদনশীল অংশ, কারণ এর offset গুণ হয়। এর input pair একটা cross-quad, dummy ring সহ, ঠিক chapter
            three-এর OTA-র input pair-এর মতো, আর এইটারে উদারভাবে size করা হয়, কারণ random offset শুধু area দিয়াই কমে। এর input,
            X আর Y, mirror image হিসাবে route করা। কিছু design আরও এগিয়ে amplifier-রে chop করে, input-গুলা বারবার অদলবদল করে যাতে
            offset গড়ে কেটে যায়; কিন্তু layout তারপরও প্রথমে আসে।
            """,
        ))
        self.clear()
        title = heading("The amplifier: its offset gets multiplied")
        quad = array(["DDDDDD", "DABBAD", "DBAABD", "DDDDDD"], 0.62).move_to([-3.0, 0.0, 0])
        ql = text("cross-quad with a dummy ring", size=20, color=INK).next_to(quad, DOWN, buff=0.3)
        side = VGroup(text("as the OTA's input pair (chapter 3)", size=22, color=INK),
                      text("big: random offset shrinks only with area", size=22, color=INK),
                      text("X and Y routed as mirror images", size=22, color=INK),
                      text("chopping helps, but the layout comes first", size=22, color=MUTED),
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([3.4, 0.0, 0])
        mult = text("1 mV of offset  →  about 10 mV at V_REF", size=26, color=THERMAL, weight="SEMIBOLD").to_edge(DOWN, buff=0.7)
        self.play(FadeIn(title), FadeIn(quad), FadeIn(ql))
        self.play(LaggedStart(*[FadeIn(s, shift=LEFT * 0.1) for s in side], lag_ratio=0.2))
        self.play(FadeIn(mult))

    def placement(self):
        self.slide(say(
            """
            Where the bandgap goes on the die matters as much as how it's drawn. A bipolar's
            voltage moves about two millivolts per degree, so keep the block away from anything
            that gets hot: output drivers, regulators, big digital blocks. And keep it away from
            the die's edges and especially its corners, where the package stress is worst and
            shifts the bipolars' voltages too. The quiet middle of the die is the place, with the
            hot blocks as far away as the floorplan allows.
            """,
            """
            Bandgap die-এর কোথায় যায়, সেইটা এইটা কিভাবে আঁকা তার মতোই গুরুত্বপূর্ণ। একটা bipolar-এর voltage প্রতি degree-তে প্রায়
            দুই millivolt নড়ে, তাই block-টারে গরম হয় এমন যেকোনো কিছু থেকে দূরে রাখেন: output driver, regulator, বড় digital block।
            আর die-এর কিনারা থেকে দূরে রাখেন, বিশেষ করে কোণা থেকে, যেখানে package stress সবচেয়ে খারাপ আর bipolar-এর voltage-ও
            সরায়। Die-এর শান্ত মাঝখানটাই জায়গা, গরম block-গুলা floorplan যতটা দূরে দেয় ততটা দূরে।
            """,
        ))
        self.clear()
        title = heading("Placing the bandgap on the die")
        die = RoundedRectangle(width=6.4, height=4.6, corner_radius=0.05, stroke_color=MUTED, stroke_width=3,
                               fill_color=PANEL, fill_opacity=1).move_to([-3.0, -0.3, 0])
        zone = RoundedRectangle(width=3.4, height=2.0, corner_radius=0.2, stroke_color=GOOD, stroke_width=3,
                                fill_color=GOOD, fill_opacity=0.12).move_to(die.get_center() + LEFT * 0.4)
        zone_l = text("quiet middle", size=20, color=GOOD).move_to(zone.get_top() + DOWN * 0.3)
        bg = RoundedRectangle(width=1.0, height=0.6, corner_radius=0.05, fill_color=GATE, fill_opacity=0.9,
                              stroke_width=0).move_to(zone.get_center() + DOWN * 0.25)
        bg_l = text("bandgap", size=16, color=BG, weight="SEMIBOLD").move_to(bg)
        drv = RoundedRectangle(width=1.5, height=1.0, corner_radius=0.05, fill_color=THERMAL, fill_opacity=0.9,
                               stroke_width=0).move_to(die.get_corner(UR) + np.array([-0.95, -0.7, 0]))
        drv_l = text("driver", size=16, color=BG, weight="SEMIBOLD").move_to(drv)
        rings = VGroup(*[Circle(radius=r, stroke_color=THERMAL, stroke_width=2, stroke_opacity=0.8 - 0.2 * k).move_to(drv)
                         for k, r in enumerate((0.85, 1.15, 1.45))])
        corners = VGroup(*[Circle(radius=0.6, stroke_width=0, fill_color=DRAIN, fill_opacity=0.2).move_to(
            die.get_corner(c) + np.array([-0.4 * c[0], -0.4 * c[1], 0])) for c in (UL, UR, DL, DR)])
        side = VGroup(text("away from heat", size=24, color=THERMAL, weight="SEMIBOLD"),
                      text("≈ −2 mV per °C on each V_BE", size=20, color=INK),
                      text("away from edges and corners", size=24, color=DRAIN, weight="SEMIBOLD"),
                      text("package stress shifts V_BE too", size=20, color=INK),
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.5, 0.0, 0])
        side[2].shift(DOWN * 0.2)
        side[3].shift(DOWN * 0.2)
        tag = illustrative().to_corner(DL, buff=0.3)
        self.play(FadeIn(title), FadeIn(die), FadeIn(tag))
        self.play(FadeIn(drv), FadeIn(drv_l), LaggedStart(*[Create(r) for r in rings], lag_ratio=0.2), FadeIn(corners))
        self.play(FadeIn(zone), FadeIn(zone_l), FadeIn(bg), FadeIn(bg_l))
        self.play(FadeIn(side))

    def trim(self):
        self.slide(say(
            """
            And when everything's done, there's trimming: R2 drawn with a few extra segments
            that can be switched in or out at test, to pull V_REF onto target. It's useful, but
            it's the last resort, not the plan. A trim is set at one temperature and fixes the
            value there; it doesn't undo every drift. And every bit of trim range costs area and
            test time. Good matching keeps what's left small, so the trim range can be small too.
            """,
            """
            আর সব শেষ হইলে, trimming: R2 কয়েকটা বাড়তি segment সহ আঁকা, যেগুলা test-এর সময় ঢোকানো বা বাদ দেওয়া যায়, V_REF-রে
            target-এ টেনে আনতে। কাজের জিনিস, কিন্তু এইটা শেষ উপায়, plan না। একটা trim এক temperature-এ set করা হয় আর সেখানকার
            মান ঠিক করে; সব drift উল্টায় না। আর trim range-এর প্রত্যেকটা bit area আর test time খায়। ভালো matching বাকিটা ছোট রাখে,
            তাই trim range-ও ছোট রাখা যায়।
            """,
        ))
        self.clear()
        title = heading("Trimming: the last resort")
        segs = VGroup(*[stripe("B", height=1.4, width=0.22) for _ in range(8)],
                      *[stripe("C", height=1.4, width=0.22) for _ in range(4)]).arrange(RIGHT, buff=0.16).move_to([-2.8, 0.6, 0])
        sw = VGroup(*[VGroup(Line(s.get_bottom() + DOWN * 0.05, s.get_bottom() + DOWN * 0.4, stroke_color=C_COL, stroke_width=2),
                             Circle(radius=0.07, stroke_color=C_COL, stroke_width=2).move_to(s.get_bottom() + DOWN * 0.5))
                      for s in segs[8:]])
        l1 = text("R2's units", size=20, color=B_COL).next_to(segs[:8], DOWN, buff=0.3)
        l2 = text("trim segments, switched at test", size=20, color=C_COL).next_to(sw, DOWN, buff=0.2)
        side = VGroup(text("fixes the value at one temperature", size=22, color=GOOD),
                      text("doesn't undo every drift", size=22, color=THERMAL),
                      text("costs area and test time", size=22, color=THERMAL),
                      text("good matching keeps the range small", size=22, color=GATE),
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.9, 0.3, 0])
        self.play(FadeIn(title), FadeIn(segs[:8]), FadeIn(l1))
        self.play(FadeIn(segs[8:]), Create(sw), FadeIn(l2))
        self.play(LaggedStart(*[FadeIn(s, shift=LEFT * 0.1) for s in side], lag_ratio=0.2))

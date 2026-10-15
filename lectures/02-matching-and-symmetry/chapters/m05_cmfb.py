"""Lecture 2 · M5 · The CMFB's resistors and capacitors.

Why R1 = R2 and C1 = C2 matter (the CMFB sees part of the differential signal otherwise), then
R1/R2 as interleaved unit resistors and C1/C2 as a common-centroid unit-capacitor array with a
dummy ring.
"""

import sys
from pathlib import Path

LECTURE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(LECTURE.parents[1]), str(LECTURE)]

from manim import *  # noqa: E402,F403
from manim_slides import Slide  # noqa: E402

from common import A_COL, B_COL, Schematic, array, chapter_title, pdk_tag, stripe  # noqa: E402
from kit.style import *  # noqa: E402,F403

class M05CMFB(Chapter, Slide):
    def construct(self):
        self.card()
        self.why()
        self.resistors()
        self.capacitors()

    def card(self):
        self.slide(say(
            """
            Chapter five: the common-mode feedback's resistors and capacitors. Matching isn't
            only about transistors. The CMFB has its own twins, and if they don't match, the
            amplifier's two outputs stop being treated equally.
            """,
            """
            Chapter five: common-mode feedback-এর resistor আর capacitor। Matching শুধু transistor-এর ব্যাপার না। CMFB-এর
            নিজের যমজ আছে, আর এরা না মিললে amplifier-এর দুইটা output আর সমান আচরণ পায় না।
            """,
        ))
        self.card_group = chapter_title(5, "The CMFB's R and C", "Unit resistors, unit capacitors")
        self.play(FadeIn(self.card_group, shift=UP * 0.2), run_time=1.2)

    def why(self):
        self.slide(say(
            """
            Here's the CMFB. R1 and R2 sit between the two outputs, and the point between them
            should be exactly the average of the two: the common mode, with the signal cancelled.
            C1 and C2 do the same job at high frequency. If R1 is a little bigger than R2, that
            point isn't the average any more: a piece of the differential signal leaks into it.
            The CMFB then reacts to the signal, which it was never meant to see, and the output
            common mode wobbles with the signal and adds distortion.
            """,
            """
            এই যে CMFB। R1 আর R2 দুইটা output-এর মাঝখানে বসে, আর এদের মধ্যের point-টা ঠিক দুইটার গড় হওয়ার কথা: common mode,
            signal কেটে গিয়া। High frequency-তে C1 আর C2 একই কাজ করে। R1 যদি R2-এর চেয়ে একটু বড় হয়, ওই point আর গড় থাকে না:
            differential signal-এর একটা টুকরা এর ভিতরে ঢুকে পড়ে। তখন CMFB signal-এর প্রতি সাড়া দেয়, যেটা তার কখনো দেখার কথা
            না, আর output common mode signal-এর সাথে নড়ে আর distortion যোগ করে।
            """,
        ))
        self.play(FadeOut(self.card_group))
        title = heading("Why R1 = R2 and C1 = C2")
        sch = Schematic("cmfb", 3.4).move_to([-3.0, -0.2, 0])
        rings = VGroup(sch.ring(["R1"], A_COL), sch.ring(["R2"], B_COL), sch.ring(["C1"], A_COL), sch.ring(["C2"], B_COL))
        side = VGroup(
            text("matched", size=24, color=GOOD, weight="SEMIBOLD"),
            text("the midpoint is the true average:\nthe CMFB sees the common mode only", size=22, color=INK),
            text("mismatched", size=24, color=DRAIN, weight="SEMIBOLD"),
            text("part of the differential signal leaks\nin: the output common mode moves\nwith the signal, and distorts it", size=22, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.6, 0.0, 0])
        side[2].shift(DOWN * 0.25)
        side[3].shift(DOWN * 0.25)
        self.play(FadeIn(title), FadeIn(sch))
        self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.2))
        self.play(FadeIn(side[:2]))
        self.play(FadeIn(side[2:]))

    def resistors(self):
        self.slide(say(
            """
            The resistors. Build R1 and R2 from identical unit resistors, here four each. All one
            width, one length, one orientation, because a resistor's value depends on which way
            it runs in many processes. Every unit has the same contact head at each end: the
            heads add resistance, and different heads mean different values. Interleave them,
            A B B A A B B A, so a gradient along the row cancels. And put a dummy stripe at each
            end, because the etch treats the last stripe differently.
            """,
            """
            Resistor-গুলা। R1 আর R2 একই রকম unit resistor দিয়া বানান, এখানে চারটা করে। সব এক width, এক length, এক orientation,
            কারণ অনেক process-এ resistor-এর মান নির্ভর করে সে কোন দিকে চলে তার উপর। প্রত্যেকটা unit-এর দুই মাথায় একই contact
            head: head resistance যোগ করে, আর আলাদা head মানে আলাদা মান। এদের মিশিয়ে দেন, A B B A A B B A, যাতে row বরাবর gradient
            কেটে যায়। আর প্রত্যেক মাথায় একটা dummy stripe দেন, কারণ etch শেষ stripe-টারে আলাদা আচরণ করে।
            """,
        ))
        self.clear()
        title = heading("R1 · R2 from unit resistors")
        stripes = VGroup(*[stripe(c) for c in "DABBAABBAD"]).arrange(RIGHT, buff=0.22).move_to([-2.4, 0.3, 0])
        links = VGroup()
        for lab, color, dy in (("A", A_COL, 1), ("B", B_COL, -1)):
            members = [s for s in stripes if s.label == lab]
            for k in range(len(members) - 1):
                a, b = members[k], members[k + 1]
                end = UP if k % 2 == 0 else DOWN
                span = abs(list(stripes).index(b) - list(stripes).index(a))
                y = a.get_edge_center(end)[1] + end[1] * (0.14 + 0.1 * span)  # longer links outside shorter ones
                path = VMobject(stroke_color=color, stroke_width=3.5).set_points_as_corners(
                    [a.get_edge_center(end), [a.get_x(), y, 0], [b.get_x(), y, 0], b.get_edge_center(end)])
                links.add(path)
        rl = VGroup(text("R1 = 4 units", size=22, color=A_COL), text("R2 = 4 units", size=22, color=B_COL)
                    ).arrange(RIGHT, buff=0.6).next_to(stripes, DOWN, buff=0.8)
        rules = VGroup(text("one width, one length", size=22),
                       text("one orientation", size=22),
                       text("the same contact head on every unit", size=22),
                       text("interleaved: ABBA ABBA", size=22),
                       text("a dummy stripe at each end", size=22)).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([4.2, 0.3, 0])
        tag = pdk_tag().to_corner(DR, buff=0.3)
        self.play(FadeIn(title), FadeIn(stripes))
        self.play(Create(links), FadeIn(rl), run_time=1.5)
        self.play(LaggedStart(*[FadeIn(r, shift=LEFT * 0.1) for r in rules], lag_ratio=0.2), FadeIn(tag))

    def capacitors(self):
        self.slide(say(
            """
            The capacitors. Same idea, in two dimensions. C1 and C2 are each four unit capacitors
            in a common-centroid array, A B B A over B A A B, so a slope in the dielectric
            thickness cancels in any direction. Around it, a ring of dummy capacitors: the
            fringing field at a unit's edge depends on what's next to it, and the ring makes
            every real unit's neighbours the same. Route the top plates the same way for both,
            and keep other wires off the array: a wire over C1 but not over C2 adds capacitance
            to C1 alone.
            """,
            """
            Capacitor-গুলা। একই ধারণা, দুই মাত্রায়। C1 আর C2 প্রত্যেকটা চারটা unit capacitor, একটা common-centroid array-তে,
            B A A B-এর উপর A B B A, তাই dielectric-এর পুরুত্বের ঢাল যেকোনো দিকে কেটে যায়। চারপাশে dummy capacitor-এর একটা ring:
            একটা unit-এর কিনারায় fringing field নির্ভর করে পাশে কী আছে তার উপর, আর ring প্রত্যেকটা আসল unit-এর প্রতিবেশী একই
            করে দেয়। দুইটার top plate একইভাবে route করেন, আর অন্য wire array থেকে দূরে রাখেন: C1-এর উপর দিয়া যাওয়া কিন্তু
            C2-এর উপর দিয়া না যাওয়া একটা wire শুধু C1-এ capacitance যোগ করে।
            """,
        ))
        self.clear()
        title = heading("C1 · C2: a common centroid with a dummy ring")
        caps = array(["DDDDDD", "DABBAD", "DBAABD", "DDDDDD"], 0.72, 0.14).move_to([-2.6, 0.1, 0])
        for c in caps:
            if c.label in "AB":
                c[1].become(text("C1" if c.label == "A" else "C2", size=20, color=c[0].get_stroke_color(), weight="BOLD").move_to(c))
        rules = VGroup(text("4 + 4 unit capacitors", size=22),
                       text("common centroid: ABBA over BAAB", size=22),
                       text("a ring of dummies: equal fringing", size=22),
                       text("top plates routed the same way", size=22),
                       text("no other wires over the array", size=22)).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([3.9, 0.1, 0])
        cancels = text("cancels: dielectric gradients, edge fringing, stray coupling", size=22, color=GOOD).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(title), FadeIn(caps))
        self.play(LaggedStart(*[FadeIn(r, shift=LEFT * 0.1) for r in rules], lag_ratio=0.2))
        self.play(FadeIn(cancels))

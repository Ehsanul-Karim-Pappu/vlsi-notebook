"""Lecture 2 · M8 · The matching review.

A checklist for each circuit, the post-layout checks, the technique-against-cause matrix again,
and the one question to ask of every technique.
"""

import sys
from pathlib import Path

LECTURE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(LECTURE.parents[1]), str(LECTURE)]

from manim import *  # noqa: E402,F403
from manim_slides import Slide  # noqa: E402

from common import chapter_title  # noqa: E402
from kit.style import *  # noqa: E402,F403


def checklist(items, size=22):
    rows = VGroup()
    for s in items:
        rows.add(VGroup(Square(0.22, stroke_color=GOOD, stroke_width=2.5), text(s, size=size, color=INK)).arrange(RIGHT, buff=0.25))
    return rows.arrange(DOWN, aligned_edge=LEFT, buff=0.26)


class M08Review(Chapter, Slide):
    def construct(self):
        self.card()
        self.ota()
        self.bandgap()
        self.post_layout()
        self.question()
        self.thanks()

    def card(self):
        self.slide(say(
            """
            Chapter eight: the matching review. Everything from today, turned into lists you can
            take to a layout review, one per circuit, plus the checks that prove the layout did
            what you meant.
            """,
            """
            Chapter eight: matching review। আজকের সবকিছু, list বানিয়ে, যেগুলা আপনি একটা layout review-তে নিয়া যেতে পারেন, প্রত্যেকটা
            circuit-এর জন্য একটা, সাথে সেই check-গুলা যেগুলা প্রমাণ করে layout আপনি যা চাইছিলেন তাই করছে।
            """,
        ))
        self.card_group = chapter_title(8, "The matching review", "Checklists, and the checks that prove them")
        self.play(FadeIn(self.card_group, shift=UP * 0.2), run_time=1.2)

    def ota(self):
        self.slide(say(
            """
            For the amplifier. One axis, and every row centred on it. The input pair as a
            cross-quad with a dummy ring, sized for the offset you need. Sources and sinks as
            interleaved rows with dummies, cascodes in line. The tail on the axis. Rails fed from
            the middle or strapped from above. The same current direction in both halves. Ratios
            in whole units. The CMFB's resistors and capacitors in unit arrays. Every
            differential net routed as a mirror image, with nothing noisy beside just one of them.
            """,
            """
            Amplifier-এর জন্য। একটা axis, আর প্রত্যেকটা row তার উপর centre করা। Input pair একটা cross-quad, dummy ring সহ, যে
            offset লাগবে সেই মতো size করা। Source আর sink, dummy সহ interleaved row, cascode সারিতে। Tail axis-এর উপর। Rail
            মাঝখান থেকে feed করা বা উপর থেকে strap করা। দুই অর্ধেকে একই current direction। Ratio পুরা unit-এ। CMFB-এর resistor আর
            capacitor unit array-তে। প্রত্যেকটা differential net mirror image হিসাবে route করা, শুধু একটার পাশে কোনো হৈচৈ ছাড়া।
            """,
        ))
        self.play(FadeOut(self.card_group))
        title = heading("Review: the folded-cascode OTA")
        left = checklist(["one axis; every row centred on it",
                          "input pair: cross-quad, dummy ring",
                          "sources, sinks: interleaved rows, dummies",
                          "cascodes in line with their devices",
                          "tail on the axis"])
        right = checklist(["rails fed from the middle, or strapped",
                           "the same current direction in each half",
                           "ratios in whole units",
                           "CMFB: unit R and C arrays",
                           "differential nets as mirror images"])
        VGroup(left, right).arrange(RIGHT, buff=0.8, aligned_edge=UP).move_to(DOWN * 0.2)
        self.play(FadeIn(title))
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in [*left, *right]], lag_ratio=0.12), run_time=2.4)

    def bandgap(self):
        self.slide(say(
            """
            For the bandgap. Q1 in the centre of the three-by-three, Q2's eight around it, a dummy
            ring around all nine. R1 and R2 from one unit resistor, centred on the axis, with
            dummies. The mirror interleaved so all three centroids coincide. The amplifier's pair
            as a cross-quad, sized generously, its inputs routed as mirror images. The block in
            the quiet middle of the die, away from heat and corners. And a trim range kept small,
            because the matching kept the error small.
            """,
            """
            Bandgap-এর জন্য। তিন-বাই-তিনের মাঝখানে Q1, চারপাশে Q2-এর আটটা, নয়টার চারপাশে একটা dummy ring। R1 আর R2 একটা unit
            resistor থেকে, axis-এ centre করা, dummy সহ। Mirror interleaved, যাতে তিনটা centroid মিলে যায়। Amplifier-এর pair একটা
            cross-quad, উদারভাবে size করা, input mirror image হিসাবে route করা। Block die-এর শান্ত মাঝখানে, তাপ আর কোণা থেকে দূরে।
            আর trim range ছোট, কারণ matching error ছোট রাখছে।
            """,
        ))
        self.clear()
        title = heading("Review: the bandgap")
        left = checklist(["Q1 centred; Q2's eight around it",
                          "a dummy ring around the nine",
                          "R1 · R2 from one unit, centred, dummies",
                          "mirror interleaved: one centroid"])
        right = checklist(["amplifier pair: cross-quad, generous",
                           "X and Y routed as mirror images",
                           "away from heat, edges and corners",
                           "a small trim range"])
        VGroup(left, right).arrange(RIGHT, buff=0.8, aligned_edge=UP).move_to(DOWN * 0.2)
        self.play(FadeIn(title))
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in [*left, *right]], lag_ratio=0.12), run_time=2.0)

    def post_layout(self):
        self.slide(say(
            """
            And after layout, prove it. Check the dummies are connected and tied off, not
            floating. Check every unit's orientation. Extract parasitics and compare each pair of
            nets. Turn on the layout-dependent effects your PDK models, well proximity and
            diffusion length, so the simulator sees the neighbourhoods you drew. Then run Monte
            Carlo mismatch on the extracted netlist: offset and CMRR for the amplifier, V_REF's
            spread and drift for the bandgap. Those numbers are the review's verdict.
            """,
            """
            আর layout-এর পরে, প্রমাণ করেন। Check করেন dummy-গুলা connected আর বাঁধা, ভাসমান না। প্রত্যেকটা unit-এর orientation check
            করেন। Parasitic extract করেন আর net-এর প্রত্যেকটা pair তুলনা করেন। আপনার PDK যে layout-dependent effect model করে
            সেগুলা চালু করেন, well proximity আর diffusion length, যাতে simulator আপনার আঁকা আশেপাশগুলা দেখে। তারপর extracted netlist-এ
            Monte Carlo mismatch চালান: amplifier-এর জন্য offset আর CMRR, bandgap-এর জন্য V_REF-এর spread আর drift। ওই সংখ্যাগুলাই
            review-এর রায়।
            """,
        ))
        self.clear()
        title = heading("After layout: prove it")
        steps = VGroup(*[VGroup(text(n, size=30, color=GATE, weight="BOLD"), text(s, size=24, color=INK)).arrange(RIGHT, buff=0.35)
                         for n, s in (("1", "dummies connected and tied off"),
                                      ("2", "every unit's orientation"),
                                      ("3", "extract; compare each pair of nets"),
                                      ("4", "simulate with the PDK's layout-dependent effects on"),
                                      ("5", "Monte Carlo on the extracted netlist: offset, CMRR, V_REF spread"))]
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(DOWN * 0.1)
        self.play(FadeIn(title))
        self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.1) for s in steps], lag_ratio=0.2), run_time=2.0)

    def question(self):
        self.slide(say(
            """
            If you keep one thing from today, keep the question. For every technique in a layout,
            ask: what does this cancel? A common centroid cancels gradients. Dummies cancel the
            neighbourhood. Placement cancels stress and heat. Mirror-image routing cancels the
            wiring. Area is the only answer to random variation. If you can't say what a
            technique cancels in your circuit, it's either in the wrong place, or it isn't needed.
            """,
            """
            আজকের থেকে যদি একটা জিনিস রাখেন, প্রশ্নটা রাখেন। Layout-এর প্রত্যেকটা technique-এর জন্য জিজ্ঞেস করেন: এইটা কী কাটে?
            Common centroid gradient কাটে। Dummy আশেপাশ কাটে। Placement stress আর তাপ কাটে। Mirror-image routing wiring কাটে।
            Random variation-এর একমাত্র উত্তর area। আপনার circuit-এ একটা technique কী কাটে বলতে না পারলে, হয় সেইটা ভুল জায়গায়,
            নয় সেইটার দরকারই নাই।
            """,
        ))
        self.clear()
        q = display("What does this cancel?", size=64, color=GATE).move_to(UP * 1.6)
        pairs = VGroup(*[VGroup(text(a, size=26, color=INK), text("→", size=26, color=MUTED), text(b, size=26, color=GOOD)
                                ).arrange(RIGHT, buff=0.3)
                         for a, b in (("common centroid", "gradients"), ("dummies", "the neighbourhood"),
                                      ("placement", "stress and heat"), ("mirror-image routing", "the wiring"),
                                      ("area", "random variation"))]).arrange(DOWN, buff=0.3).move_to(DOWN * 1.1)
        for p in pairs:
            p.shift(RIGHT * (p[1].get_x() * -1))
        self.play(Write(q), run_time=1.4)
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.1) for p in pairs], lag_ratio=0.2), run_time=1.8)

    def thanks(self):
        self.slide(say(
            """
            That's lecture two. Next time you open an analog block, read it for twins first, find
            the axis, and build out from there. Thank you.
            """,
            """
            এই হইল lecture two। পরের বার একটা analog block খুললে, প্রথমে যমজগুলা খুঁজে পড়েন, axis বের করেন, আর সেখান থেকে বানান।
            ধন্যবাদ।
            """,
        ))
        self.clear()
        t = display("Thank you", size=72).move_to(UP * 0.5)
        s = text("Lecture 2 · Matching and Symmetry, in Layout", size=28, color=MUTED).next_to(t, DOWN, buff=0.4)
        self.play(FadeIn(t, shift=UP * 0.2), FadeIn(s))

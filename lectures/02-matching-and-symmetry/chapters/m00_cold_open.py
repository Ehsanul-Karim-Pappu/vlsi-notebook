"""Lecture 2 · M0 · Identical on paper.

The two circuits the whole lecture lays out, and what a mismatch costs each of them, said as an
outcome on the bench.
"""

import sys
from pathlib import Path

LECTURE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(LECTURE.parents[1]), str(LECTURE)]

from manim import *  # noqa: E402,F403
from manim_slides import Slide  # noqa: E402

from common import A_COL, B_COL, C_COL, Schematic, card_box  # noqa: E402
from kit.style import *  # noqa: E402,F403


class M00ColdOpen(Chapter, Slide):
    def construct(self):
        self.title()
        self.two_circuits()
        self.on_paper()
        self.costs()
        self.route()

    def title(self):
        self.slide(say(
            """
            Lecture two: matching and symmetry, in layout. No derivations today. Every technique
            you'll see comes with one question answered: what does it cancel on the silicon? And
            we won't use two-transistor toy circuits. We'll lay out two real blocks, a fully
            differential folded-cascode amplifier with its common-mode feedback, and a bandgap
            reference.
            """,
            """
            Lecture two: matching আর symmetry, layout-এ। আজকে কোনো derivation নাই। যত technique দেখবেন, প্রত্যেকটার সাথে
            একটা প্রশ্নের উত্তর: silicon-এ এইটা কী কাটে? আর আমরা দুই-transistor-এর খেলনা circuit use করব না। দুইটা আসল
            block-এর layout করব: common-mode feedback সহ একটা fully differential folded-cascode amplifier, আর একটা bandgap
            reference।
            """,
        ))
        kick = kicker("Lecture 2", color=GATE)
        ttl = display("Matching and Symmetry, in Layout", size=56)
        sub = text("What each technique cancels, on two real circuits", size=30, color=MUTED)
        VGroup(kick, ttl, sub).arrange(DOWN, buff=0.3).move_to(UP * 0.4)
        self.play(FadeIn(kick), Write(ttl), run_time=1.6)
        self.play(FadeIn(sub))

    def two_circuits(self):
        self.slide(say(
            """
            Here they are. On the left, the amplifier: an NMOS input pair, M1 and M2, folded into
            two branches of PMOS current sources and cascodes above, NMOS cascodes and current
            sinks below, with the common-mode feedback driving the bottom sinks. On the right,
            the bandgap: three PMOS mirror devices, an amplifier holding nodes X and Y equal, Q1
            against Q2, which is eight of the same transistor, a resistor R1, and the output
            branch through R2 and Q3. Between them they have every kind of matching problem
            you'll meet.
            """,
            """
            এই যে দুইটা। বামে amplifier: একটা NMOS input pair, M1 আর M2, উপরের PMOS current source আর cascode-এর দুইটা branch-এ
            fold করা, নিচে NMOS cascode আর current sink, আর common-mode feedback নিচের sink-গুলা চালায়। ডানে bandgap: তিনটা PMOS
            mirror device, একটা amplifier যেটা X আর Y node সমান রাখে, Q1 বনাম Q2, যেটা একই transistor-এর আটটা, একটা resistor R1,
            আর R2 আর Q3 দিয়া output branch। এই দুইটার মধ্যেই আপনি যত রকম matching সমস্যা পাবেন সব আছে।
            """,
        ))
        self.clear()
        ota = Schematic("ota", 3.9).move_to([-3.3, -0.2, 0])
        bg = Schematic("bandgap", 3.9).move_to([3.7, -0.2, 0])
        lo = text("folded-cascode OTA, with CMFB", size=24, weight="SEMIBOLD").next_to(ota, UP, buff=0.25)
        lb = text("bandgap reference", size=24, weight="SEMIBOLD").next_to(bg, UP, buff=0.25)
        self.play(FadeIn(ota), FadeIn(lo))
        self.play(FadeIn(bg), FadeIn(lb))
        self.ota, self.bg, self.lbls = ota, bg, VGroup(lo, lb)

    def on_paper(self):
        self.slide(say(
            """
            On paper, these circuits are full of twins. M1 equals M2. M3 equals M4, M9 equals M10.
            In the bandgap, M1, M2 and M3 are copies, and Q2 is exactly eight Q1s. The simulator
            believes it. The silicon never quite does: two transistors drawn identically come out
            slightly different, and how different depends a lot on how you laid them out.
            """,
            """
            কাগজে এই circuit-গুলা যমজে ভরা। M1 সমান M2। M3 সমান M4, M9 সমান M10। Bandgap-এ M1, M2 আর M3 একে অন্যের copy,
            আর Q2 হুবহু আটটা Q1। Simulator এইটা বিশ্বাস করে। Silicon কখনো পুরাপুরি করে না: একইভাবে আঁকা দুইটা transistor
            একটু আলাদা হয়ে বের হয়, আর কতটা আলাদা, সেইটা অনেকটাই নির্ভর করে আপনি layout কিভাবে করছেন তার উপর।
            """,
        ))
        rings = VGroup(
            self.ota.ring(["M1", "M2"], A_COL), self.ota.ring(["M3"], B_COL), self.ota.ring(["M4"], B_COL),
            self.ota.ring(["M9"], C_COL), self.ota.ring(["M10"], C_COL),
            self.bg.ring(["M1", "M2", "M3"], A_COL), self.bg.ring(["Q1", "Q2"], B_COL),
        )
        words = text("identical on paper", size=30, color=GATE, weight="SEMIBOLD").to_edge(DOWN, buff=0.35)
        self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.15), run_time=2.0)
        self.play(FadeIn(words))
        self.rings, self.words = rings, words

    def costs(self):
        self.slide(say(
            """
            And here's what the difference costs, said the way it shows up on the bench. In the
            amplifier: an offset, so the output isn't balanced when the inputs are; part of the
            common-mode signal leaking into the differential one; and distortion that symmetry
            would have cancelled. In the bandgap: a reference that's off by some millivolts, and
            moves with temperature more than it should. You trim it, or you lose yield. Every
            technique today is about shrinking those numbers with nothing but placement and
            wiring.
            """,
            """
            আর পার্থক্যটার দাম এই, bench-এ যেভাবে দেখা যায় সেভাবে বলি। Amplifier-এ: offset, মানে input সমান হইলেও output
            balanced না; common-mode signal-এর কিছুটা differential signal-এ ঢুকে পড়া; আর এমন distortion যেটা symmetry থাকলে কেটে
            যাইত। Bandgap-এ: reference কয়েক millivolt সরে থাকে, আর temperature-এর সাথে যতটা নড়ার কথা তার চেয়ে বেশি নড়ে। হয় trim
            করেন, নয় yield হারান। আজকের প্রত্যেকটা technique শুধু placement আর wiring দিয়া এই সংখ্যাগুলা ছোট করার জন্য।
            """,
        ))
        self.play(FadeOut(self.rings), FadeOut(self.words), FadeOut(self.ota), FadeOut(self.bg), FadeOut(self.lbls))
        title = heading("What a mismatch costs")
        cards = VGroup(
            card_box("The OTA", [text("an offset at the input", size=24, color=INK),
                                 text("common mode leaking into\nthe differential signal", size=24, color=INK),
                                 text("distortion that symmetry\nwould have cancelled", size=24, color=INK)], width=5.6, height=3.8),
            card_box("The bandgap", [text("V_REF off by millivolts", size=24, color=INK),
                                     text("more drift over temperature", size=24, color=INK),
                                     text("trimming, or lost yield", size=24, color=INK)], width=5.6, height=3.8),
        ).arrange(RIGHT, buff=0.6).move_to(DOWN * 0.2)
        foot = text("Today: shrink these with placement and wiring alone.", size=28, color=GATE).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(title))
        for c in cards:
            self.play(FadeIn(c, shift=UP * 0.15), run_time=0.8)
        self.play(FadeIn(foot))

    def route(self):
        self.slide(say(
            """
            The route. First, what makes twins differ: six causes, and which technique cancels
            which. Then the amplifier, part by part: how to read it for matching, the input pair,
            a live lab where you place the units yourself, the current sources and cascodes, the
            common-mode feedback's resistors and capacitors, and the routing. Then the bandgap,
            with its one-to-eight transistor array. And a review checklist to finish.
            """,
            """
            Route-টা এই। প্রথমে, যমজরা আলাদা হয় কেন: ছয়টা কারণ, আর কোন technique কোনটা কাটে। তারপর amplifier, অংশ ধরে ধরে:
            matching-এর চোখে এইটা কিভাবে পড়বেন, input pair, একটা live lab যেখানে unit-গুলা আপনি নিজে বসাবেন, current source আর
            cascode, common-mode feedback-এর resistor আর capacitor, আর routing। তারপর bandgap, তার এক-অনুপাত-আট transistor array
            সহ। আর শেষে একটা review checklist।
            """,
        ))
        self.clear()
        title = heading("The route")
        steps = [("1", "What makes twins differ"), ("2", "Reading the OTA for matching"), ("3", "The input pair"),
                 ("", "Live lab: place the units"), ("4", "Current sources and cascodes"), ("5", "The CMFB's R and C"),
                 ("6", "Routing as mirror images"), ("7", "The bandgap"), ("8", "The matching review")]
        rows = VGroup()
        for n, s in steps:
            num = text(n or "•", size=26, color=GATE, weight="BOLD")
            rows.add(VGroup(num, text(s, size=26, color=INK if n else ELECTRON)).arrange(RIGHT, buff=0.35))
        col1 = VGroup(*rows[:5]).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        col2 = VGroup(*rows[5:]).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        VGroup(col1, col2).arrange(RIGHT, buff=1.4, aligned_edge=UP).move_to(DOWN * 0.1)
        self.play(FadeIn(title))
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows], lag_ratio=0.12), run_time=2.0)

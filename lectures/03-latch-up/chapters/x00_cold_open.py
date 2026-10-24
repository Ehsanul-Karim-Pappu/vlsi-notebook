"""Lecture 3 · X0 · The chip that shorts itself.

A bench story told as a supply-current trace, the DRC report lines every layout engineer has seen,
and the route through the lecture.
"""

import sys
from pathlib import Path

LECTURE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(LECTURE.parents[1]), str(LECTURE)]

from manim import *  # noqa: E402,F403
from manim_slides import Slide  # noqa: E402

from common import illustrative, pdk_tag, table  # noqa: E402
from kit.style import *  # noqa: E402,F403

RULES = [  # generic rule names: real decks are confidential
    ["rule", "what it says", "errors"],
    ["LUP.TAP.1", "N+ active farther than 15 µm from a P+ substrate tap", "23"],
    ["LUP.TAP.2", "P+ active farther than 15 µm from an N+ well tap", "8"],
    ["LUP.GR.1", "I/O NMOS not enclosed by a continuous P+ guard ring", "2"],
    ["LUP.IO.1", "core N-well within 50 µm of an injector, no N-well ring", "1"],
    ["LUP.WELL.1", "N-wells on different supplies closer than 3 µm", "4"],
]


class X00ColdOpen(Chapter, Slide):
    def construct(self):
        self.title()
        self.bench()
        self.report()
        self.route()

    def title(self):
        self.slide(say(
            """
            Lecture three: latch-up, in layout. Every layout engineer has a set of latch-up rules
            in their DRC deck, and most of us have fixed those errors by adding taps until the
            markers went away. Today we'll look underneath: what's in the silicon that can
            short a chip's supply to ground, how it fires, and which part of that picture each
            rule is protecting.
            """,
            """
            Lecture three: latch-up, layout-এ। প্রত্যেক layout engineer-এর DRC deck-এ একগাদা latch-up rule থাকে, আর আমরা
            বেশিরভাগই marker না যাওয়া পর্যন্ত tap যোগ করে সেই error-গুলা ঠিক করছি। আজকে আমরা নিচে তাকাব: silicon-এর ভিতরে
            কী আছে যেটা একটা chip-এর supply-রে ground-এর সাথে short করতে পারে, সেইটা কিভাবে চালু হয়, আর প্রত্যেকটা rule
            ওই ছবির কোন অংশটা রক্ষা করে।
            """,
        ))
        kick = kicker("Lecture 3", color=GATE)
        ttl = display("Latch-up, in Layout", size=64)
        sub = text("Why every LUP rule exists, and what it protects", size=30, color=MUTED)
        VGroup(kick, ttl, sub).arrange(DOWN, buff=0.3).move_to(UP * 0.4)
        self.play(FadeIn(kick), Write(ttl), run_time=1.6)
        self.play(FadeIn(sub))
        self.title_group = VGroup(kick, ttl, sub)

    def bench(self):
        self.slide(say(
            """
            Here's how it looks on the bench. The supply current sits at a few milliamps. A
            spike arrives on an I/O pin: a cable plugged in, a ringing signal, a pin driven
            before the chip is powered. And the supply current jumps to hundreds of milliamps and
            stays there, even after the spike is long gone. The part gets hot. Nothing you do
            through its pins brings it back. Only cutting the power does, if the metal hasn't
            melted first. That's latch-up.
            """,
            """
            Bench-এ এইটা দেখতে এমন। Supply current কয়েক milliamp-এ বসে আছে। একটা I/O pin-এ একটা spike আসে: একটা cable
            লাগানো হইল, একটা ringing signal, chip power পাওয়ার আগেই একটা pin drive করা হইল। আর supply current লাফ দিয়া
            কয়েকশ milliamp-এ উঠে যায় আর সেখানেই থাকে, spike চলে যাওয়ার অনেক পরেও। Part গরম হয়। এর pin দিয়া যাই করেন,
            ফেরে না। শুধু power কাটলে ফেরে, যদি তার আগেই metal গলে না যায়। এইটাই latch-up।
            """,
        ))
        self.play(FadeOut(self.title_group))
        title = heading("On the bench")
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 320, 100], x_length=9.0, y_length=4.2,
                  axis_config={"color": MUTED, "include_ticks": False}).move_to([-0.6, -0.4, 0])
        xl = text("time", size=20, color=MUTED).next_to(ax, DOWN, buff=0.15)
        yl = text("supply current", size=20, color=MUTED).rotate(PI / 2).next_to(ax, LEFT, buff=0.15)

        def i_of_t(t):
            if t < 3.0:
                return 5
            if t < 3.25:
                return 5 + 60 * (t - 3.0) / 0.25
            if t < 3.6:
                return 65 + 215 * (t - 3.25) / 0.35
            if t < 8.0:
                return 280
            return 280 if t < 8.05 else 2

        trace = ax.plot(i_of_t, x_range=[0, 10, 0.01], color=DRAIN, stroke_width=5, use_smoothing=False)
        spike = Arrow(ax.c2p(1.6, 120), ax.c2p(2.9, 15), buff=0, stroke_color=GATE, stroke_width=5)
        spike_l = text("a spike on an I/O pin", size=20, color=GATE).next_to(spike.get_start(), UP, buff=0.1)
        stays = text("…and it stays", size=22, color=DRAIN).next_to(ax.c2p(5.8, 280), UP, buff=0.15)
        cut = DashedLine(ax.c2p(8.0, 0), ax.c2p(8.0, 310), stroke_color=MUTED, stroke_width=2)
        cut_l = text("power cycle", size=20, color=MUTED).next_to(cut, UP, buff=0.08)
        tag = illustrative().to_corner(DL, buff=0.3)
        self.play(FadeIn(title), Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(tag))
        self.play(Create(trace), run_time=3.0, rate_func=linear)
        self.play(GrowArrow(spike), FadeIn(spike_l))
        self.play(FadeIn(stays))
        self.play(Create(cut), FadeIn(cut_l))

    def report(self):
        self.slide(say(
            """
            And here's how it looks at your desk: a few lines in a DRC report. N+ active too far
            from a substrate tap. An I/O transistor without a continuous guard ring. A core well
            too close to something called an injector. Wells on different supplies too close
            together. The rule names and numbers here are made up, because every foundry's deck
            is different and confidential, but every deck has these four families. By the end of
            today, each of these lines should read as a picture of the silicon underneath, with an
            obvious fix.
            """,
            """
            আর আপনার desk-এ এইটা দেখতে এমন: একটা DRC report-এর কয়েকটা লাইন। N+ active একটা substrate tap থেকে বেশি দূরে।
            Continuous guard ring ছাড়া একটা I/O transistor। একটা core well এমন একটা জিনিসের খুব কাছে, যার নাম injector।
            আলাদা supply-র well-গুলা একে অন্যের খুব কাছে। এখানের rule-এর নাম আর সংখ্যা বানানো, কারণ প্রত্যেক foundry-র deck
            আলাদা আর গোপন, কিন্তু প্রত্যেক deck-এ এই চারটা family থাকে। আজকের শেষে, এই লাইনগুলার প্রত্যেকটা নিচের silicon-এর
            একটা ছবি হিসাবে পড়া যাওয়া উচিত, একটা পরিষ্কার সমাধান সহ।
            """,
        ))
        self.clear()
        title = heading("At your desk: the LUP section of a DRC report")
        t = table(RULES, col_w=(2.4, 8.4, 1.2), size=22, row_gap=0.34).move_to(DOWN * 0.1)
        for row in t[0][1:]:
            row[0].set_color(GATE)
            row[2].set_color(DRAIN)
        frame = SurroundingRectangle(t, buff=0.3, corner_radius=0.1, stroke_color=FAINT, stroke_width=2,
                                     fill_color=PANEL, fill_opacity=1)
        tag = pdk_tag().to_corner(DR, buff=0.3)
        note = text("generic names and values: every foundry's deck differs", size=18, color=MUTED).next_to(frame, DOWN, buff=0.25)
        self.play(FadeIn(title), FadeIn(frame), FadeIn(t[0][0]), FadeIn(t[1]), FadeIn(tag))
        for row in t[0][1:]:
            self.play(FadeIn(row, shift=UP * 0.08), run_time=0.5)
        self.play(FadeIn(note))

    def route(self):
        self.slide(say(
            """
            The route. First the physics, as pictures: the thyristor hiding in every CMOS
            inverter, how it fires and why it stays on, and a lab where you fire it yourself.
            Then the four knobs layout controls, and the four rule families they became: taps,
            with a lab where you tap a floorplan; guard rings at the I/O; distance from injectors;
            and the rules for many supplies and many wells. Then a review: how to read a latch-up
            report, and what the qualification test will do to your chip.
            """,
            """
            Route-টা এই। প্রথমে physics, ছবি হিসাবে: প্রত্যেকটা CMOS inverter-এ লুকানো thyristor, এইটা কিভাবে চালু হয় আর কেন
            চালু থাকে, আর একটা lab যেখানে আপনি নিজে এইটা চালু করবেন। তারপর layout যে চারটা knob নিয়ন্ত্রণ করে, আর সেগুলা থেকে
            যে চারটা rule family হইছে: tap, একটা lab সহ যেখানে আপনি একটা floorplan-এ tap বসাবেন; I/O-তে guard ring; injector
            থেকে দূরত্ব; আর অনেক supply আর অনেক well-এর rule। তারপর একটা review: একটা latch-up report কিভাবে পড়বেন, আর
            qualification test আপনার chip-এর সাথে কী করবে।
            """,
        ))
        self.clear()
        title = heading("The route")
        steps = [("1", "The thyristor in every inverter"), ("2", "How it fires, and why it stays on"),
                 ("", "Live lab: fire the thyristor"), ("3", "Four knobs, four rule families"), ("4", "Taps: the core rule"),
                 ("", "Live lab: tap the floor"), ("5", "Guard rings at the I/O"), ("6", "Keeping the core away from injectors"),
                 ("7", "Many supplies, many wells"), ("8", "The latch-up review")]
        rows = VGroup()
        for n, s in steps:
            num = text(n or "•", size=26, color=GATE, weight="BOLD")
            rows.add(VGroup(num, text(s, size=24, color=INK if n else ELECTRON)).arrange(RIGHT, buff=0.3))
        col1 = VGroup(*rows[:5]).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        col2 = VGroup(*rows[5:]).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        VGroup(col1, col2).arrange(RIGHT, buff=0.9, aligned_edge=UP).move_to(DOWN * 0.1)
        self.play(FadeIn(title))
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows], lag_ratio=0.12), run_time=2.0)

"""Lecture 2 · M4 · The current sources and the cascodes.

M3/M4 and M9/M10 as unit arrays with dummies; each cascode in line with its source; the source
rail fed from the axis (IR drop); the same current direction in both devices; ratios drawn as
whole units.
"""

import sys
from pathlib import Path

LECTURE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(LECTURE.parents[1]), str(LECTURE)]

from manim import *  # noqa: E402,F403
from manim_slides import Slide  # noqa: E402

from common import B_COL, C_COL, array, chapter_title, illustrative, pdk_tag, unit  # noqa: E402
from kit.style import *  # noqa: E402,F403


class M04Mirrors(Chapter, Slide):
    def construct(self):
        self.card()
        self.arrays()
        self.cascodes()
        self.rails()
        self.direction()
        self.ratios()

    def card(self):
        self.slide(say(
            """
            Chapter four: the current sources and the cascodes. After the input pair, these
            matter most. M3 and M4 set the current in each folded branch from the top, M9 and M10
            from the bottom. Any difference between them is a difference in current between the
            two halves, and the amplifier can only balance it with an offset at its input.
            """,
            """
            Chapter four: current source আর cascode। Input pair-এর পরে এগুলাই সবচেয়ে গুরুত্বপূর্ণ। M3 আর M4 উপর থেকে প্রত্যেকটা
            folded branch-এর current ঠিক করে, M9 আর M10 নিচ থেকে। এদের যেকোনো পার্থক্য দুই অর্ধেকের মধ্যে current-এর পার্থক্য,
            আর amplifier সেইটা শুধু তার input-এ একটা offset দিয়াই balance করতে পারে।
            """,
        ))
        self.card_group = chapter_title(4, "Current sources and cascodes", "Arrays, rails, direction, ratios")
        self.play(FadeIn(self.card_group, shift=UP * 0.2), run_time=1.2)

    def arrays(self):
        self.slide(say(
            """
            The sources are long, narrow devices on purpose: weak, so their mismatch reaches the
            input scaled down. That makes them long rows of units, not squares, so a one-row
            arrangement fits naturally. Interleave them, A B B A A B B A, with dummies at both
            ends, and the straight part of any gradient along the row cancels. M3 and M4 get one
            row, M9 and M10 another, both centred on the axis.
            """,
            """
            Source-গুলা ইচ্ছা করেই লম্বা আর সরু device: দুর্বল, যাতে এদের mismatch ছোট হয়ে input-এ পৌঁছায়। তাই এগুলা unit-এর
            লম্বা row হয়, square না, তাই এক row-এর সাজানো স্বাভাবিকভাবে মিলে যায়। এদের মিশিয়ে দেন, A B B A A B B A, দুই মাথায় dummy
            সহ, আর row বরাবর যেকোনো gradient-এর সোজা অংশ কেটে যায়। M3 আর M4 পায় একটা row, M9 আর M10 আরেকটা, দুইটাই axis-এ centre করা।
            """,
        ))
        self.play(FadeOut(self.card_group))
        title = heading("Sources and sinks: one row each")
        top = array(["DABBAABBAD"], 0.58).move_to([0, 1.3, 0])
        bot = array(["DABBAABBAD"], 0.58).move_to([0, -1.2, 0])
        for cells, names in ((top, ("M3", "M4")), (bot, ("M9", "M10"))):
            for c in cells:
                if c.label in "AB":
                    c[1].become(text(names[0] if c.label == "A" else names[1], size=15, color=c[0].get_stroke_color(),
                                     weight="BOLD").move_to(c))
        tl = text("PMOS sources M3 · M4, under VDD", size=22, color=INK).next_to(top, UP, buff=0.3)
        bl = text("NMOS sinks M9 · M10, driven by the CMFB", size=22, color=INK).next_to(bot, UP, buff=0.3)
        ax = VGroup(*[DashedLine([0, r.get_top()[1] + 0.15, 0], [0, r.get_bottom()[1] - 0.15, 0], stroke_color=GATE,
                                 stroke_width=3, dash_length=0.08) for r in (top, bot)])
        cancels = text("cancels: the straight part of a gradient along the row, and the end effects", size=22,
                       color=GOOD).to_edge(DOWN, buff=0.6)
        self.add(ax)
        self.play(FadeIn(title), Create(ax), FadeIn(top), FadeIn(tl))
        self.play(FadeIn(bot), FadeIn(bl))
        self.play(FadeIn(cancels))

    def cascodes(self):
        self.slide(say(
            """
            Where do the cascodes go? Directly in line with the devices they sit on. Each source
            unit gets its cascode unit right below it, in the same column, so the node between
            them is a short, identical stub everywhere. The cascodes repeat the source row's
            pattern, so they come out interleaved and common-centroid for free. Their own
            mismatch hardly matters; what matters is that they don't make the two halves'
            wiring different.
            """,
            """
            Cascode-গুলা কোথায় যায়? যে device-এর উপর বসে, ঠিক তার সারিতে। প্রত্যেকটা source unit-এর ঠিক নিচে তার cascode unit,
            একই column-এ, তাই এদের মধ্যের node সব জায়গায় একটা ছোট, একই রকম টুকরা। Cascode-গুলা source row-এর pattern-টাই
            repeat করে, তাই বিনা খরচে interleaved আর common-centroid হয়ে যায়। এদের নিজেদের mismatch প্রায় কিছুই না; যেটা
            গুরুত্বপূর্ণ, এরা যেন দুই অর্ধেকের wiring আলাদা না করে।
            """,
        ))
        self.clear()
        title = heading("Each cascode in line with its source")
        src = array(["DABBAABBAD"], 0.58).move_to([-1.0, 1.0, 0])
        cas = VGroup()
        for c in src:
            lab = {"A": "a", "B": "b"}.get(c.label, "D")
            u = unit("D" if lab == "D" else c.label, 0.58)
            if lab != "D":
                u[0].set_stroke(C_COL).set_fill(C_COL, 0.18)
                u[1].become(text("M5" if lab == "a" else "M6", size=15, color=C_COL, weight="BOLD").move_to(u))
            cas.add(u.move_to(c.get_center() + DOWN * 1.1))
        for c in src:
            if c.label in "AB":
                c[1].become(text("M3" if c.label == "A" else "M4", size=15, color=c[0].get_stroke_color(), weight="BOLD").move_to(c))
        stubs = VGroup(*[Line(s.get_bottom(), k.get_top(), stroke_color=METAL, stroke_width=4)
                         for s, k in zip(src, cas) if s.label in "AB"])
        sl = text("sources", size=20, color=B_COL).next_to(src, LEFT, buff=0.3)
        cl = text("cascodes", size=20, color=C_COL).next_to(cas, LEFT, buff=0.3)
        notes = VGroup(text("short, identical stubs", size=22, color=GOOD),
                       text("the same pattern, so the same centroid", size=22, color=GOOD),
                       text("no wire from one half crosses the other", size=22, color=GOOD)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([-1.0, -2.2, 0])
        self.play(FadeIn(title), FadeIn(src), FadeIn(sl))
        self.play(FadeIn(cas), FadeIn(cl), Create(stubs))
        self.play(LaggedStart(*[FadeIn(n, shift=UP * 0.1) for n in notes], lag_ratio=0.25))

    def rails(self):
        self.slide(say(
            """
            Now the rail that feeds them. Each unit draws current from the supply rail, and the
            rail has resistance, so the voltage sags along it. Feed it from one end, and the sag
            grows all the way to the far end, and it curves, because the current adds up as you go.
            The interleaving only cancels the straight part of that. Feed it from the axis, and
            the worst sag drops to a quarter, and it's the same on both sides. Best of all: a
            wide rail on a higher metal, dropping into every unit through its own vias, so every
            unit sits at nearly the same voltage.
            """,
            """
            এবার যে rail এদের খাওয়ায়। প্রত্যেকটা unit supply rail থেকে current টানে, আর rail-এর resistance আছে, তাই voltage এর
            দৈর্ঘ্য বরাবর ঝুলে পড়ে। এক মাথা থেকে feed করলে ঝুলটা দূরের মাথা পর্যন্ত বাড়তে থাকে, আর বাঁকে, কারণ যত যান current
            যোগ হয়। Interleaving এর শুধু সোজা অংশটা কাটে। Axis থেকে feed করলে সবচেয়ে খারাপ ঝুল চার ভাগের এক ভাগে নামে, আর
            দুই দিকে একই। সবচেয়ে ভালো: উপরের metal-এ একটা চওড়া rail, যেটা নিজের via দিয়া প্রত্যেকটা unit-এ নামে, তাই প্রত্যেকটা
            unit প্রায় একই voltage-এ বসে।
            """,
        ))
        self.clear()
        title = heading("Feeding the source rail")
        ax = Axes(x_range=[0, 1, 0.5], y_range=[0, 0.55, 0.25], x_length=5.0, y_length=3.6,
                  axis_config={"color": MUTED, "include_ticks": False}).move_to([-3.8, -0.4, 0])
        xl = text("position along the rail", size=20, color=MUTED).next_to(ax, DOWN, buff=0.2)
        yl = text("voltage sag", size=20, color=MUTED).rotate(PI / 2).next_to(ax, LEFT, buff=0.2)
        end = ax.plot(lambda x: x - x * x / 2, x_range=[0, 1], color=DRAIN, stroke_width=5)
        mid = ax.plot(lambda x: (lambda u: u - u * u / 2)(abs(x - 0.5) * 2) / 4, x_range=[0, 1], color=GATE, stroke_width=5)
        strap = ax.plot(lambda x: 0.015, x_range=[0, 1], color=GOOD, stroke_width=5)
        el = text("fed from one end", size=20, color=DRAIN).next_to(ax.c2p(1, 0.5), RIGHT, buff=0.2)
        ml = text("fed from the axis: ¼, symmetric", size=20, color=GATE).next_to(ax.c2p(1, 0.125), RIGHT, buff=0.2)
        sl = text("strapped: every unit fed", size=20, color=GOOD).next_to(ax.c2p(1, 0.015), RIGHT, buff=0.2).shift(DOWN * 0.1)
        side = VGroup(text("What it cancels", size=26, color=GATE, weight="SEMIBOLD"),
                      text("a current difference set by\nwhere each unit taps the rail", size=22, color=INK),
                      text("the interleaving cancels only\nthe straight part of the sag", size=22, color=MUTED),
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.7, 1.6, 0])
        tag = illustrative().to_corner(DL, buff=0.3)
        self.play(FadeIn(title), Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(tag))
        self.play(Create(end), FadeIn(el))
        self.play(Create(mid), FadeIn(ml))
        self.play(Create(strap), FadeIn(sl))
        self.play(FadeIn(side))

    def direction(self):
        self.slide(say(
            """
            A detail that's easy to miss: which way the current flows. In a multi-finger device,
            neighbouring fingers share a source or a drain, so half the fingers carry current left
            to right and half right to left. The source side and the drain side of a transistor
            aren't perfectly identical, angled implants and stress see to that. So make sure each
            device of a pair has the same number of fingers in each direction, or, with single
            units, that every unit points the same way.
            """,
            """
            একটা detail যেটা সহজে চোখ এড়ায়: current কোন দিকে চলে। Multi-finger device-এ পাশাপাশি finger-গুলা একটা source বা
            drain ভাগ করে, তাই অর্ধেক finger-এ current বাম থেকে ডানে, অর্ধেকে ডান থেকে বামে। একটা transistor-এর source দিক আর
            drain দিক পুরাপুরি একই না, কোনাকুনি implant আর stress সেইটা নিশ্চিত করে। তাই খেয়াল রাখেন একটা pair-এর প্রত্যেকটা
            device-এর প্রত্যেক দিকে সমান সংখ্যক finger আছে, বা single unit হইলে, প্রত্যেকটা unit একই দিকে মুখ করা।
            """,
        ))
        self.clear()
        title = heading("The same current direction")

        def fingers(labels, dirs, y, good):
            g = VGroup()
            for k, (lab, d) in enumerate(zip(labels, dirs)):
                u = unit(lab, 0.62).move_to([-4.2 + k * 0.85, y, 0])
                arr = Arrow(u.get_center() + LEFT * 0.28 * d, u.get_center() + RIGHT * 0.28 * d, buff=0,
                            stroke_color=INK, stroke_width=4, max_tip_length_to_length_ratio=0.35).shift(DOWN * 0.48)
                g.add(VGroup(u, arr))
            return g

        bad = fingers("AABB", (1, -1, 1, 1), 1.2, False)
        bad_l = text("A: one each way;  B: both the same way", size=22, color=DRAIN).next_to(bad, RIGHT, buff=0.6)
        good = fingers("ABBA", (1, 1, -1, -1), -1.0, True)
        good_l = text("A and B: one each way", size=22, color=GOOD).next_to(good, RIGHT, buff=0.6)
        cancels = text("cancels: source/drain asymmetry from angled implants and stress", size=22,
                       color=GOOD).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(title), FadeIn(bad), FadeIn(bad_l))
        self.play(FadeIn(good), FadeIn(good_l))
        self.play(FadeIn(cancels))

    def ratios(self):
        self.slide(say(
            """
            Last: ratios. The bias network sets the tail and every source from one reference
            device. When a device should carry four times the reference current, draw four
            reference units, never one device four times as wide. Four identical units match
            the reference the same way it matches itself: same edges, same length, same
            surroundings. One wide device has different edge effects, and the ratio comes out
            wrong by a few percent, every time.
            """,
            """
            শেষ: ratio। Bias network একটা reference device থেকে tail আর প্রত্যেকটা source ঠিক করে। যখন একটা device-এর reference-এর
            চার গুণ current বহন করার কথা, চারটা reference unit আঁকেন, কখনো চার গুণ চওড়া একটা device না। চারটা একই রকম unit
            reference-এর সাথে সেভাবেই মেলে যেভাবে সে নিজের সাথে মেলে: একই কিনারা, একই length, একই আশেপাশ। একটা চওড়া device-এর
            কিনারার effect আলাদা, আর ratio প্রতিবার কয়েক percent ভুল হয়।
            """,
        ))
        self.clear()
        title = heading("Ratios in whole units")
        ref = unit("C", 0.7).move_to([-4.6, 0.9, 0])
        ref_l = text("reference", size=20, color=C_COL).next_to(ref, DOWN, buff=0.15)
        bad = Rectangle(width=2.8, height=0.7, stroke_color=DRAIN, stroke_width=3, fill_color=DRAIN, fill_opacity=0.2).move_to([0.2, 0.9, 0])
        bad_l = text("one device, 4× as wide", size=20, color=DRAIN).next_to(bad, DOWN, buff=0.15)
        x1 = text("✗", size=40, color=DRAIN).next_to(bad, RIGHT, buff=0.3)
        good = VGroup(*[unit("C", 0.7) for _ in range(4)]).arrange(RIGHT, buff=0.1).move_to([0.2, -1.2, 0])
        good_l = text("four reference units", size=20, color=GOOD).next_to(good, DOWN, buff=0.15)
        x2 = text("✓", size=40, color=GOOD).next_to(good, RIGHT, buff=0.3)
        ratio = text("1 : 4", size=36, color=INK, weight="SEMIBOLD").move_to([-4.6, -1.2, 0])
        cancels = text("cancels: edge effects that don't scale with width", size=22, color=GOOD).to_edge(DOWN, buff=0.6)
        tag = pdk_tag().to_corner(DR, buff=0.3)
        self.play(FadeIn(title), FadeIn(ref), FadeIn(ref_l), FadeIn(ratio))
        self.play(FadeIn(bad), FadeIn(bad_l), FadeIn(x1))
        self.play(FadeIn(good), FadeIn(good_l), FadeIn(x2))
        self.play(FadeIn(cancels), FadeIn(tag))

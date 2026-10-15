"""Lecture 2 · M3 · The input pair.

M1 and M2 split into units; four arrangements against a gradient, each with what it cancels and
what it leaves; dummies; the tail on the axis; and the pair's wiring as mirror images.
"""

import sys
from pathlib import Path

LECTURE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(LECTURE.parents[1]), str(LECTURE)]

from manim import *  # noqa: E402,F403
from manim_slides import Slide  # noqa: E402

from common import A_COL, B_COL, Schematic, array, chapter_title, illustrative, meter, pdk_tag, placed  # noqa: E402
from kit.style import *  # noqa: E402,F403

ROW = [-3.0, 0.3, 0]
SIDE_X = 3.7
BASE = placed(["AAAABBBB"]).error  # side by side: the whole gradient, the reference


def verdict(name, cancels, leaves):
    return VGroup(text(name, size=32, color=GATE, weight="SEMIBOLD"),
                  VGroup(text("cancels", size=18, color=MUTED), text(cancels, size=22, color=GOOD)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
                  VGroup(text("leaves", size=18, color=MUTED), text(leaves, size=22, color=THERMAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
                  ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([SIDE_X, 0.6, 0])


class M03InputPair(Chapter, Slide):
    def construct(self):
        self.card()
        self.units()
        self.side_by_side()
        self.interdigitated()
        self.mirrored()
        self.cross_quad()
        self.what_is_left()
        self.dummies()
        self.tail()
        self.wiring()

    def card(self):
        self.slide(say(
            """
            Chapter three: the input pair. This is the pair whose mismatch becomes the
            amplifier's offset directly, so it gets the most careful treatment. We'll build it up
            in steps, and after each step, ask the same two questions: what did that cancel, and
            what's left?
            """,
            """
            Chapter three: input pair। এইটাই সেই pair যার mismatch সরাসরি amplifier-এর offset হয়, তাই এইটা সবচেয়ে যত্ন পায়।
            আমরা ধাপে ধাপে বানাব, আর প্রত্যেক ধাপের পরে একই দুইটা প্রশ্ন করব: এইটা কী কাটল, আর কী বাকি থাকল?
            """,
        ))
        self.card_group = chapter_title(3, "The input pair", "Units, arrangements, dummies, wiring")
        self.play(FadeIn(self.card_group, shift=UP * 0.2), run_time=1.2)

    def units(self):
        self.slide(say(
            """
            First, units. M1 and M2 are big: wide, for a strong pair and low noise, and large,
            because random variation shrinks only with area. Draw each as one wide transistor and
            you've got two blocks you can only place side by side. Split each into identical
            units, here four each, all the same width, length and orientation, and suddenly you
            can arrange them however you like. Units are what make every later trick possible.
            """,
            """
            প্রথমে, unit। M1 আর M2 বড়: চওড়া, যাতে pair শক্তিশালী হয় আর noise কম থাকে, আর বড়, কারণ random variation শুধু
            area দিয়াই কমে। প্রত্যেকটারে একটা চওড়া transistor হিসাবে আঁকলে আপনার হাতে দুইটা block, যেগুলা শুধু পাশাপাশিই
            বসানো যায়। প্রত্যেকটারে একই রকম unit-এ ভাগ করেন, এখানে চারটা করে, সব একই width, length আর orientation, তখন হঠাৎ
            এগুলা যেভাবে খুশি সাজাতে পারবেন। পরের সব কৌশল unit-এর কারণেই সম্ভব।
            """,
        ))
        self.play(FadeOut(self.card_group))
        title = heading("Step 1 · Split each device into units")
        sch = Schematic("ota", 2.6, credit=False).to_corner(UL, buff=0.5).shift(DOWN * 0.7)
        ring = sch.ring(["M1", "M2"], A_COL)
        big = VGroup(Rectangle(width=2.6, height=1.0, stroke_color=A_COL, stroke_width=3, fill_color=A_COL, fill_opacity=0.25),
                     Rectangle(width=2.6, height=1.0, stroke_color=B_COL, stroke_width=3, fill_color=B_COL, fill_opacity=0.25),
                     ).arrange(RIGHT, buff=0.2).move_to([2.6, 1.2, 0])
        big_l = VGroup(text("M1", size=28, color=A_COL, weight="BOLD").move_to(big[0]),
                       text("M2", size=28, color=B_COL, weight="BOLD").move_to(big[1]))
        u = array(["AAAABBBB"], 0.62).move_to([2.6, -1.0, 0])
        u_l = text("4 units each: same W, L and orientation", size=22, color=INK).next_to(u, DOWN, buff=0.3)
        arrows = VGroup(Arrow(big[0].get_bottom(), u[1].get_top() + UP * 0.05, stroke_color=MUTED, stroke_width=3),
                        Arrow(big[1].get_bottom(), u[6].get_top() + UP * 0.05, stroke_color=MUTED, stroke_width=3))
        self.play(FadeIn(title), FadeIn(sch), Create(ring))
        self.play(FadeIn(big), FadeIn(big_l))
        self.play(GrowArrow(arrows[0]), GrowArrow(arrows[1]), FadeIn(u))
        self.play(FadeIn(u_l))

    def show(self, rows, name, cancels, leaves, heading_text, angle=0.0, curvature=0.0):
        g = placed(rows, angle, curvature).move_to(ROW)
        m = meter(g.error / BASE).move_to([SIDE_X, -2.1, 0])
        v = verdict(name, cancels, leaves)
        title = heading(heading_text)
        return g, m, v, title

    def side_by_side(self):
        self.slide(say(
            """
            Now put a gradient under them: blue is low, orange is high, the threshold voltage
            creeping up from left to right, say. Side by side, all of M1 sits in the blue and all of
            M2 in the orange. The crosses mark each device's centroid, its centre of gravity, and
            they're four units apart. M2 gets the higher threshold, and that difference is
            offset. This is our reference: all of the gradient shows up.
            """,
            """
            এবার এদের নিচে একটা gradient দেন: নীল কম, কমলা বেশি, ধরেন threshold voltage বাম থেকে ডানে একটু একটু বাড়ছে।
            পাশাপাশি বসালে, পুরা M1 নীলে আর পুরা M2 কমলায়। Cross-গুলা প্রত্যেকটা device-এর centroid দেখায়, মানে তার ভারকেন্দ্র,
            আর এরা চার unit দূরে। M2 বেশি threshold পায়, আর সেই পার্থক্যটাই offset। এইটা আমাদের reference: gradient-এর পুরাটাই
            দেখা যায়।
            """,
        ))
        self.clear()
        g, m, v, title = self.show(["AAAABBBB"], "Side by side", "nothing", "the whole gradient", "Side by side")
        tag = illustrative().to_corner(DL, buff=0.3)
        self.play(FadeIn(title), FadeIn(g.field), FadeIn(g.cells), FadeIn(tag))
        self.play(FadeIn(g.marks, scale=1.4))
        self.play(FadeIn(v), FadeIn(m))
        self.cur = VGroup(g, m, v, title)

    def swap(self, new):
        g, m, v, title = new
        self.play(Transform(self.cur[3], title), FadeOut(self.cur[0].marks), Transform(self.cur[0].cells, g.cells),
                  FadeOut(self.cur[2]), run_time=1.2)
        self.play(FadeIn(g.marks, scale=1.4), Transform(self.cur[1], m), FadeIn(v))
        self.cur = VGroup(VGroup(self.cur[0].field, self.cur[0].cells, g.marks), self.cur[1], v, self.cur[3])
        self.cur[0].field, self.cur[0].cells, self.cur[0].marks = self.cur[0][0], self.cur[0][1], g.marks

    def interdigitated(self):
        self.slide(say(
            """
            Interleave them: A B A B. This is interdigitation. The centroids move to one unit
            apart, so a quarter of the gradient is left. Better, but notice the pattern still has
            a direction: every B sits one step to the right of an A, so a straight slope still
            favours one device.
            """,
            """
            এদের মিশিয়ে দেন: A B A B। এইটা interdigitation। Centroid-গুলা এক unit দূরে চলে আসে, তাই gradient-এর চার ভাগের এক
            ভাগ বাকি থাকে। ভালো, কিন্তু খেয়াল করেন pattern-টার এখনো একটা দিক আছে: প্রত্যেকটা B একটা A-র এক ধাপ ডানে বসে,
            তাই একটা সোজা ঢাল এখনো একটা device-এর পক্ষে যায়।
            """,
        ))
        self.swap(self.show(["ABABABAB"], "Interdigitated", "three quarters of a\nstraight gradient", "one unit's worth", "Interdigitated · ABAB"))

    def mirrored(self):
        self.slide(say(
            """
            Mirror it: A B B A, A B B A. Now the pattern is symmetric about its own centre, so
            both centroids land on the same spot, and a straight gradient along the row cancels
            completely. That's a common centroid. A gradient across the row is harmless too: it
            touches every unit of a single row equally. The weakness is length. A big pair makes
            a long row, and a long row spans a lot of the die, where real gradients bend.
            """,
            """
            Mirror করেন: A B B A, A B B A। এখন pattern-টা তার নিজের মাঝখানের সাপেক্ষে symmetric, তাই দুইটা centroid একই
            জায়গায় পড়ে, আর row বরাবর একটা সোজা gradient পুরাপুরি কেটে যায়। এইটাই common centroid। Row-এর আড়াআড়ি gradient-ও
            ক্ষতি করে না: এক row-এর প্রত্যেকটা unit-রে সমানভাবে ছোঁয়। দুর্বলতা হইল দৈর্ঘ্য। বড় pair মানে লম্বা row, আর লম্বা row
            die-এর অনেকটা জুড়ে থাকে, যেখানে আসল gradient বাঁকে।
            """,
        ))
        self.swap(self.show(["ABBAABBA"], "Mirrored · ABBA", "a straight gradient,\nany direction", "a long row: curvature",
                            "Mirrored · ABBA ABBA"))

    def cross_quad(self):
        self.slide(say(
            """
            So fold the row: the cross-quad. Two short rows, A B B A on top and B A A B below.
            Each device has units in both rows and on both diagonals, so the centroids still
            coincide whichever way the slope points. Watch: I'll turn the gradient, and the
            leftover stays at zero. And the array is half as long, with A and B spread evenly
            through it. Coincident, symmetric, evenly spread, compact: that's what a good common
            centroid looks like, and it's the standard arrangement for a critical input pair.
            """,
            """
            তাই row-টারে ভাঁজ করেন: cross-quad। দুইটা ছোট row, উপরে A B B A আর নিচে B A A B। প্রত্যেকটা device-এর unit দুইটা
            row-তেই আর দুইটা কর্ণেই আছে, তাই ঢাল যেদিকেই থাকুক centroid-গুলা এখনো মিলে থাকে। দেখেন: আমি gradient-টা ঘুরাব, আর বাকিটা
            শূন্যেই থাকবে। আর array-টা অর্ধেক লম্বা, A আর B তার ভিতরে সমানভাবে ছড়ানো। মিলে যাওয়া centroid, symmetric, সমানভাবে
            ছড়ানো, compact: ভালো common centroid দেখতে এমনই, আর critical input pair-এর জন্য এইটাই standard সাজানো।
            """,
        ))
        self.clear()
        tag = illustrative().to_corner(DL, buff=0.3)
        g = placed(["ABBA", "BAAB"]).move_to(ROW)
        m = meter(g.error / BASE).move_to([SIDE_X, -2.1, 0])
        v = verdict("Cross-quad", "a straight gradient,\nany direction", "less curvature (half\nthe length); random")
        title = heading("Cross-quad · ABBA over BAAB")
        self.play(FadeIn(title), FadeIn(g.field), FadeIn(g.cells), FadeIn(tag))
        self.play(FadeIn(g.marks, scale=1.4), FadeIn(v), FadeIn(m))
        for ang in (0.8, 1.57, 2.4):
            g2 = placed(["ABBA", "BAAB"], angle=ang).move_to(ROW)
            self.play(Transform(g.field, g2.field), run_time=1.0)
        self.cur = VGroup(g, m, v, title)

    def what_is_left(self):
        self.slide(say(
            """
            What's left after a common centroid? Two things. Curvature: real gradients bend, and a
            bend doesn't cancel the way a straight slope does. Here's the long mirrored row on a
            bowl, and some error comes back. The defence is to keep the array compact, so it sits
            on a small, nearly straight piece of the bowl: that's why the cross-quad beats one
            long row. And random variation, which no arrangement touches. Only area helps
            there.
            """,
            """
            Common centroid-এর পরে কী বাকি থাকে? দুইটা জিনিস। Curvature: আসল gradient বাঁকা হয়, আর বাঁক সোজা ঢালের মতো কাটে
            না। এই যে mirrored row একটা বাটির উপর, আর কিছু error ফিরে আসে। সমাধান array-টারে compact রাখা, যাতে সে বাটির ছোট,
            প্রায় সোজা একটা টুকরার উপর বসে, এইটা একটা কারণ কেন একটা লম্বা row-এর চেয়ে cross-quad ভালো। আর random variation,
            যেটা কোনো সাজানো ছোঁয় না। ওইখানে শুধু area সাহায্য করে।
            """,
        ))
        self.clear()
        tag = illustrative().to_corner(DL, buff=0.3)
        g = placed(["ABBAABBA"], curvature=0.9).move_to(ROW)
        m = meter(g.error / BASE).move_to([SIDE_X, -2.1, 0])
        v = verdict("On a bowl", "the straight part", "curvature: keep the\narray compact", )
        title = heading("What a common centroid leaves")
        rand = text("random: only area helps", size=22, color=THERMAL).next_to(g, DOWN, buff=0.45)
        self.play(FadeIn(title), FadeIn(g.field), FadeIn(g.cells), FadeIn(tag))
        self.play(FadeIn(g.marks, scale=1.4), FadeIn(v), FadeIn(m))
        self.play(FadeIn(rand))

    def dummies(self):
        self.slide(say(
            """
            Next, dummies. In the cross-quad, the outer units have empty space on one side and the
            inner units have neighbours on both. Etching, implants and stress all notice, so the
            outer units come out different. Surround the array with dummy units: real transistors,
            drawn the same, with their gates tied off so they do nothing. Now every real unit
            has the same neighbours. In FinFET processes, the dummies also keep the fins and
            gates continuous across the array. How many rows of dummies your process wants is in
            its rules.
            """,
            """
            এরপর, dummy। Cross-quad-এ বাইরের unit-গুলার এক পাশে খালি জায়গা, আর ভিতরের unit-গুলার দুই পাশেই প্রতিবেশী।
            Etching, implant আর stress সবাই এইটা টের পায়, তাই বাইরের unit-গুলা আলাদা হয়ে বের হয়। Array-টারে dummy unit দিয়া
            ঘিরে দেন: আসল transistor, একইভাবে আঁকা, gate বেঁধে দেওয়া যাতে এরা কিছু না করে। এখন প্রত্যেকটা আসল unit-এর একই
            প্রতিবেশী। FinFET process-এ dummy fin আর gate-গুলারেও array জুড়ে একটানা রাখে। কয় সারি dummy লাগবে, সেইটা আপনার
            process-এর rule-এ আছে।
            """,
        ))
        self.clear()
        title = heading("Step 2 · A ring of dummies")
        bare = array(["ABBA", "BAAB"], 0.62).move_to([-3.6, 0.2, 0])
        edge = VGroup(*[SurroundingRectangle(c, color=DRAIN, buff=0.03, stroke_width=3) for c in bare
                        if c.rc[1] in (0, 3)])
        bare_l = text("the end units see empty space", size=20, color=DRAIN).next_to(bare, DOWN, buff=0.45)
        ring = array(["DDDDDD", "DABBAD", "DBAABD", "DDDDDD"], 0.62).move_to([2.6, 0.2, 0])
        ring_l = text("every real unit sees the same neighbours", size=20, color=GOOD).next_to(ring, DOWN, buff=0.3)
        tied = text("dummies: same drawing, gates tied off", size=18, color=MUTED).next_to(ring_l, DOWN, buff=0.15)
        tag = pdk_tag().to_corner(DR, buff=0.3)
        self.play(FadeIn(title), FadeIn(bare))
        self.play(Create(edge), FadeIn(bare_l))
        self.play(FadeIn(ring), FadeIn(ring_l), FadeIn(tied), FadeIn(tag))

    def tail(self):
        self.slide(say(
            """
            The tail, M11, has no twin, but where it sits still matters. Its drain is the pair's
            common source node. Put the tail on the axis, right below the pair, and connect the
            node from the middle, so the wire from the tail to every A unit is the mirror image of
            the wire to every B unit. Put the tail off to one side, and one half of the pair gets
            a longer, more resistive source connection: a built-in offset you drew yourself.
            """,
            """
            Tail M11-এর কোনো যমজ নাই, কিন্তু সে কোথায় বসে তা এখনো গুরুত্বপূর্ণ। এর drain হইল pair-এর common source node। Tail-রে
            axis-এর উপর রাখেন, pair-এর ঠিক নিচে, আর node-টা মাঝখান থেকে connect করেন, যাতে tail থেকে প্রত্যেকটা A unit পর্যন্ত wire,
            প্রত্যেকটা B unit পর্যন্ত wire-এর mirror image হয়। Tail এক পাশে রাখলে pair-এর এক অর্ধেক একটা লম্বা, বেশি resistive
            source connection পায়: একটা built-in offset, যেটা আপনি নিজেই আঁকলেন।
            """,
        ))
        self.clear()
        title = heading("Step 3 · The tail on the axis")

        def pair_with_tail(x, tail_dx, good):
            arr = array(["ABBA", "BAAB"], 0.55).move_to([x, 0.9, 0])
            node = Line(arr.get_corner(DL) + DOWN * 0.3, arr.get_corner(DR) + DOWN * 0.3, stroke_color=METAL, stroke_width=6)
            drops = VGroup(*[Line([c.get_x(), arr.get_bottom()[1], 0], [c.get_x(), node.get_y(), 0], stroke_color=METAL,
                                  stroke_width=3) for c in arr if c.rc[0] == 1])
            t = VGroup(Rectangle(width=1.0, height=0.5, stroke_color=MUTED, stroke_width=3, fill_color=MUTED, fill_opacity=0.2),
                       text("M11", size=18, color=MUTED)).move_to([x + tail_dx, -1.0, 0])
            t[1].move_to(t[0])
            if good:
                feed = Line(t.get_top(), [t.get_x(), node.get_y(), 0], stroke_color=METAL, stroke_width=6)
            else:
                feed = VMobject(stroke_color=METAL, stroke_width=6).set_points_as_corners(
                    [t.get_top(), [t.get_x(), node.get_y(), 0], node.get_end()])
            lab = text("on the axis: equal paths" if good else "off to one side: unequal paths", size=20,
                       color=GOOD if good else DRAIN).move_to([x, -1.8, 0])
            ax = DashedLine([x, 1.9, 0], [x, -1.4, 0], stroke_color=GATE, stroke_width=2, dash_length=0.08)
            return VGroup(ax, arr, node, drops, t, feed, lab)

        bad = pair_with_tail(-3.4, 1.9, False)
        good = pair_with_tail(3.4, 0.0, True)
        self.play(FadeIn(title), FadeIn(bad))
        self.play(FadeIn(good))

    def wiring(self):
        self.slide(say(
            """
            Last step: the wiring. Each A unit needs its gate tied to V_IN+ and its drain to one
            folding node; each B unit to V_IN− and the other node. Run the A tracks and B tracks
            as mirror images: the same layer, the same length, the same number of vias, the same
            neighbours on each side. If A's drain wire is longer, it has more resistance and more
            capacitance, and the pair isn't matched any more, however perfect the units are.
            """,
            """
            শেষ ধাপ: wiring। প্রত্যেকটা A unit-এর gate V_IN+-এ আর drain একটা folding node-এ বাঁধা লাগবে; প্রত্যেকটা B unit-এর
            V_IN−-এ আর অন্য node-এ। A-র track আর B-র track mirror image হিসাবে চালান: একই layer, একই length, একই সংখ্যক via,
            প্রত্যেক পাশে একই প্রতিবেশী। A-র drain wire লম্বা হইলে তার resistance আর capacitance বেশি, আর unit-গুলা যত নিখুঁতই হোক,
            pair আর matched থাকে না।
            """,
        ))
        self.clear()
        title = heading("Step 4 · Wire the halves as mirror images")
        arr = array(["ABBA", "BAAB"], 0.7).move_to([-2.4, -0.2, 0])
        top_y = arr.get_top()[1]
        tracks = VGroup()
        names = (("A gate · V_IN+", A_COL, 0.35), ("B gate · V_IN−", B_COL, 0.7), ("A drain", A_COL, -0.35), ("B drain", B_COL, -0.7))
        for name, color, dy in names:
            y = top_y + dy if dy > 0 else arr.get_bottom()[1] + dy
            tr = Line([arr.get_left()[0] - 0.2, y, 0], [arr.get_right()[0] + 0.2, y, 0], stroke_color=color, stroke_width=5)
            lbl = text(name, size=18, color=color).next_to(tr, RIGHT, buff=0.2)
            label = name[0]
            vias = VGroup(*[Line([c.get_x() + (0.12 if "drain" in name else -0.12), y, 0],
                                 [c.get_x() + (0.12 if "drain" in name else -0.12), c.get_center()[1], 0],
                                 stroke_color=color, stroke_width=2.5, stroke_opacity=0.8) for c in arr if c.label == label])
            dots = VGroup(*[Dot([v.get_x(), y, 0], radius=0.06, color=color) for v in vias])
            tracks.add(VGroup(tr, vias, dots, lbl))
        rules = VGroup(text("same layer", size=22), text("same length", size=22), text("same via count: 4 and 4", size=22),
                       text("same neighbours either side", size=22)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.6, -0.2, 0])
        self.play(FadeIn(title), FadeIn(arr))
        for t in tracks:
            self.play(Create(t[0]), Create(t[1]), FadeIn(t[2]), FadeIn(t[3]), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(r, shift=LEFT * 0.1) for r in rules], lag_ratio=0.2))

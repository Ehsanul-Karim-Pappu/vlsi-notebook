"""Lecture 2 · M6 · Routing as mirror images.

The OTA's differential nets routed as mirror images; crossings done symmetrically; shields and
noisy neighbours; metal over the devices; and the extraction check that proves it.
"""

import sys
from pathlib import Path

LECTURE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(LECTURE.parents[1]), str(LECTURE)]

from manim import *  # noqa: E402,F403
from manim_slides import Slide  # noqa: E402

from common import A_COL, B_COL, array, chapter_title, illustrative, pdk_tag, table  # noqa: E402
from kit.style import *  # noqa: E402,F403


def path(points, color, width=6):
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners([[x, y, 0] for x, y in points])


def via(x, y, color=INK):
    return Square(0.16, stroke_color=color, stroke_width=2, fill_color=VIA, fill_opacity=1).move_to([x, y, 0])


VIA = "#8E1C1C"


class M06Routing(Chapter, Slide):
    def construct(self):
        self.card()
        self.nets()
        self.mirror()
        self.crossing()
        self.shields()
        self.metal_over()
        self.extraction()

    def card(self):
        self.slide(say(
            """
            Chapter six: routing as mirror images. You can place every unit perfectly and still
            undo it with the wires. In a differential circuit, the wires are part of the
            circuit: every pair of nets has to be a pair of twins too.
            """,
            """
            Chapter six: mirror image হিসাবে routing। আপনি প্রত্যেকটা unit নিখুঁতভাবে বসাতে পারেন আর তারপরও wire দিয়া সব নষ্ট
            করতে পারেন। Differential circuit-এ wire-ও circuit-এর অংশ: প্রত্যেকটা net-এর pair-কেও যমজ হতে হবে।
            """,
        ))
        self.card_group = chapter_title(6, "Routing as mirror images", "Every pair of nets is a pair of twins")
        self.play(FadeIn(self.card_group, shift=UP * 0.2), run_time=1.2)

    def nets(self):
        self.slide(say(
            """
            In the OTA, the paired nets are: the two inputs, V_IN+ and V_IN−; the two folding
            nodes, where M1 and M2's drains meet the cascodes; the two outputs; and the CMFB's
            connections to them. The inputs and the folding nodes are the sensitive ones: any
            extra resistance, capacitance or coupling on one of them goes straight into offset,
            or into a mismatch between the halves at high frequency.
            """,
            """
            OTA-তে জোড়া net-গুলা হইল: দুইটা input, V_IN+ আর V_IN−; দুইটা folding node, যেখানে M1 আর M2-এর drain cascode-এর সাথে
            মেলে; দুইটা output; আর ওগুলার সাথে CMFB-এর connection। Input আর folding node-গুলা সংবেদনশীল: এদের একটায় বাড়তি
            resistance, capacitance বা coupling সোজা offset-এ যায়, বা high frequency-তে দুই অর্ধেকের mismatch-এ।
            """,
        ))
        self.play(FadeOut(self.card_group))
        title = heading("The paired nets")
        rows = [["", "left", "right", "how sensitive"],
                ["inputs", "V_IN+", "V_IN−", "most: straight into offset"],
                ["folding nodes", "M1 drain", "M2 drain", "high: offset, and speed"],
                ["outputs", "V_OUT−", "V_OUT+", "medium: balance, CMFB"],
                ["CMFB taps", "to R1 · C1", "to R2 · C2", "medium: common-mode leak"]]
        t = table(rows, col_w=(3.0, 2.2, 2.2, 4.4), size=24, row_gap=0.4).move_to(DOWN * 0.1)
        for row in t[0][1:]:
            row[1].set_color(A_COL)
            row[2].set_color(B_COL)
        self.play(FadeIn(title), FadeIn(t[0][0]), FadeIn(t[1]))
        for row in t[0][1:]:
            self.play(FadeIn(row, shift=UP * 0.08), run_time=0.5)

    def mirror(self):
        self.slide(say(
            """
            The rule for each pair: mirror images about the axis. The same layers, the same
            length, the same number of vias, the same bends, and the same neighbours at the same
            distance. On the left, one route took a detour and an extra via, and runs next to a
            clock line: it's longer, more resistive, more capacitive, and it hears the clock.
            On the right, both routes are reflections of each other, and anything that happens to
            one happens to both.
            """,
            """
            প্রত্যেকটা pair-এর rule: axis-এর সাপেক্ষে mirror image। একই layer, একই length, একই সংখ্যক via, একই বাঁক, আর একই
            দূরত্বে একই প্রতিবেশী। বামে, একটা route ঘুরপথে গেছে আর একটা বাড়তি via নিছে, আর একটা clock line-এর পাশ দিয়া চলে:
            এইটা লম্বা, বেশি resistive, বেশি capacitive, আর clock শোনে। ডানে, দুইটা route একে অন্যের প্রতিফলন, আর একটার সাথে যা হয়
            দুইটার সাথেই হয়।
            """,
        ))
        self.clear()
        title = heading("Each pair as mirror images")

        def panel(cx, good):
            ax = DashedLine([cx, 2.4, 0], [cx, -2.6, 0], stroke_color=GATE, stroke_width=2, dash_length=0.08)
            pa = Square(0.5, stroke_color=A_COL, fill_color=A_COL, fill_opacity=0.3).move_to([cx - 0.6, -2.0, 0])
            pb = Square(0.5, stroke_color=B_COL, fill_color=B_COL, fill_opacity=0.3).move_to([cx + 0.6, -2.0, 0])
            ins = VGroup(text("V_IN+", size=18, color=A_COL).move_to([cx - 2.2, 2.1, 0]),
                         text("V_IN−", size=18, color=B_COL).move_to([cx + 2.2, 2.1, 0]))
            ra = path([(cx - 2.2, 1.85), (cx - 2.2, 0.4), (cx - 0.6, 0.4), (cx - 0.6, -1.75)], A_COL)
            if good:
                rb = path([(cx + 2.2, 1.85), (cx + 2.2, 0.4), (cx + 0.6, 0.4), (cx + 0.6, -1.75)], B_COL)
                extra = VGroup(via(cx - 0.6, 0.4), via(cx + 0.6, 0.4))
                lab = text("reflections: equal R, C and coupling", size=20, color=GOOD).move_to([cx, -3.0, 0])
            else:
                rb = path([(cx + 2.2, 1.85), (cx + 2.2, 1.2), (cx + 2.9, 1.2), (cx + 2.9, -0.6), (cx + 0.6, -0.6),
                           (cx + 0.6, -1.75)], B_COL)
                clk = DashedLine([cx + 3.15, 1.6, 0], [cx + 3.15, -1.2, 0], stroke_color=DRAIN, stroke_width=4, dash_length=0.1)
                clk_l = text("clock", size=16, color=DRAIN).next_to(clk, UP, buff=0.05)
                extra = VGroup(via(cx - 0.6, 0.4), via(cx + 2.9, 1.2), via(cx + 0.6, -0.6), clk, clk_l)
                lab = text("longer, one more via, beside a clock", size=20, color=DRAIN).move_to([cx, -3.0, 0])
            return VGroup(ax, pa, pb, ins, ra, rb, extra, lab)

        bad, good = panel(-3.6, False), panel(3.2, True)
        self.play(FadeIn(title), FadeIn(bad))
        self.play(FadeIn(good))

    def crossing(self):
        self.slide(say(
            """
            Sometimes two nets of a pair have to cross, to swap sides, or to get past each other.
            A crossing is a place where one net goes up a layer and the other doesn't, and that's
            an asymmetry: different layers, different resistance, a via on one net only. The fix
            is to cross twice, or to make both nets change layer at the crossing. Each net then
            has the same layers, the same vias, and the same overlap with the other.
            """,
            """
            কখনো কখনো একটা pair-এর দুইটা net-রে একে অন্যরে পার হইতে হয়, দিক বদলানোর জন্য, বা পাশ কাটানোর জন্য। Crossing মানে এমন
            একটা জায়গা যেখানে একটা net এক layer উপরে যায় আর অন্যটা যায় না, আর সেইটা একটা asymmetry: আলাদা layer, আলাদা
            resistance, শুধু একটা net-এ via। সমাধান দুইবার cross করা, বা crossing-এ দুইটা net-রেই layer বদলানো। তখন প্রত্যেকটা
            net-এর একই layer, একই via, আর অন্যটার সাথে একই overlap।
            """,
        ))
        self.clear()
        title = heading("Crossings, done symmetrically")

        def twist(cx, double):
            g = VGroup()
            xs = [cx - 2.6, cx - 0.9, cx + 0.9, cx + 2.6]
            ya, yb = 0.6, -0.6
            if not double:
                g.add(path([(xs[0], ya), (xs[1], ya), (xs[2], yb), (xs[3], yb)], A_COL),
                      path([(xs[0], yb), (xs[1], yb)], B_COL), path([(xs[2], ya), (xs[3], ya)], B_COL),
                      path([(xs[1], yb), (xs[2], ya)], B_COL, 3),
                      via(xs[1], yb), via(xs[2], ya))
                lab = text("B changes layer twice, A never", size=20, color=DRAIN)
            else:
                g.add(path([(xs[0], ya), (xs[1], ya)], A_COL), path([(xs[1], ya), (xs[2], yb), (xs[3], yb)], A_COL, 3),
                      path([(xs[0], yb), (xs[1], yb)], B_COL, 3), path([(xs[1], yb), (xs[2], ya), (xs[3], ya)], B_COL),
                      via(xs[1], ya), via(xs[1], yb))
                lab = text("each net: one layer change, one via", size=20, color=GOOD)
            names = VGroup(text("A", size=20, color=A_COL).next_to([xs[0], ya, 0], LEFT, buff=0.15),
                           text("B", size=20, color=B_COL).next_to([xs[0], yb, 0], LEFT, buff=0.15))
            return VGroup(g, names, lab.move_to([cx, -1.6, 0]))

        bad, good = twist(-3.4, False), twist(3.4, True)
        key = text("thick: lower metal · thin: upper metal", size=18, color=MUTED).to_edge(DOWN, buff=0.6)
        tag = illustrative().to_corner(DL, buff=0.3)
        self.play(FadeIn(title), FadeIn(bad), FadeIn(key), FadeIn(tag))
        self.play(FadeIn(good))

    def shields(self):
        self.slide(say(
            """
            Noisy neighbours. A clock, a digital bus, a switching supply: anything with fast
            edges couples into whatever runs beside it. If it runs beside one net of a pair, that
            noise is differential, and the amplifier amplifies it. Keep aggressors away, and if
            something has to pass, make it pass both nets equally, or run grounded shield lines
            on both sides of the pair. Shields come in pairs too: a shield on one net only is
            just more capacitance on that net.
            """,
            """
            হৈচৈ করা প্রতিবেশী। Clock, digital bus, switching supply: দ্রুত edge আছে এমন যেকোনো কিছু তার পাশ দিয়া যা চলে তাতে
            couple করে। এইটা যদি একটা pair-এর একটা net-এর পাশ দিয়া চলে, সেই noise differential, আর amplifier সেইটারে বড় করে।
            Aggressor-দের দূরে রাখেন, আর যদি কিছু পার হইতেই হয়, দুইটা net-রে সমানভাবে পার করান, বা pair-এর দুই পাশে grounded
            shield line চালান। Shield-ও জোড়ায় আসে: শুধু একটা net-এ shield মানে শুধু ওই net-এ বাড়তি capacitance।
            """,
        ))
        self.clear()
        title = heading("Shields and noisy neighbours")
        ys = [1.0, 0.5, 0.0, -0.5, -1.0]
        cols = [MUTED, A_COL, B_COL, MUTED, None]
        lines = VGroup()
        names = ["GND shield", "V_IN+", "V_IN−", "GND shield"]
        for y, c, n in zip(ys[:4], cols[:4], names):
            lines.add(VGroup(Line([-5.4, y + 0.25, 0], [-0.6, y + 0.25, 0], stroke_color=c, stroke_width=8),
                             text(n, size=18, color=c).next_to([-0.6, y + 0.25, 0], RIGHT, buff=0.2)))
        clk = VGroup(DashedLine([-5.4, -1.45, 0], [-0.6, -1.45, 0], stroke_color=DRAIN, stroke_width=6, dash_length=0.15),
                     text("clock, kept away", size=18, color=DRAIN).next_to([-0.6, -1.45, 0], RIGHT, buff=0.2))
        rules = VGroup(text("keep aggressors away", size=22),
                       text("if one must pass, it passes both", size=22),
                       text("shields on both sides, both nets", size=22),
                       text("a shield on one net only is\njust extra capacitance", size=22, color=MUTED)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.3, 0.0, 0])
        self.play(FadeIn(title), FadeIn(lines))
        self.play(FadeIn(clk))
        self.play(LaggedStart(*[FadeIn(r, shift=LEFT * 0.1) for r in rules], lag_ratio=0.2))

    def metal_over(self):
        self.slide(say(
            """
            Metal over the devices. A wire running over one unit of a pair but not the other
            changes it: it adds capacitance to whatever's below, and in many processes metal over
            the gate changes the transistor itself, through stress and through the hydrogen that
            reaches the gate oxide during processing. So keep the coverage the same over every
            unit: either nothing crosses the matched array, or the same wires cross every unit,
            with dummy metal where needed.
            """,
            """
            Device-এর উপর metal। একটা pair-এর একটা unit-এর উপর দিয়া চলা কিন্তু অন্যটার উপর দিয়া না চলা একটা wire সেইটারে বদলায়:
            নিচে যা আছে তাতে capacitance যোগ করে, আর অনেক process-এ gate-এর উপরের metal transistor-টারেই বদলায়, stress দিয়া,
            আর processing-এর সময় gate oxide-এ পৌঁছানো hydrogen দিয়া। তাই প্রত্যেকটা unit-এর উপর coverage একই রাখেন: হয় matched
            array-এর উপর দিয়া কিছুই যায় না, নয় প্রত্যেকটা unit-এর উপর দিয়া একই wire যায়, দরকার হলে dummy metal দিয়া।
            """,
        ))
        self.clear()
        title = heading("Metal over the devices")
        bad = array(["ABBA", "BAAB"], 0.62).move_to([-3.4, 0.3, 0])
        wire = Rectangle(width=0.3, height=1.9, stroke_width=0, fill_color=METAL, fill_opacity=0.7).move_to(bad[0].get_center() + DOWN * 0.36)
        bad_l = text("one wire over some units only", size=20, color=DRAIN).next_to(bad, DOWN, buff=0.55)
        good = array(["ABBA", "BAAB"], 0.62).move_to([3.4, 0.3, 0])
        wires = VGroup(*[Rectangle(width=0.3, height=1.9, stroke_width=0, fill_color=METAL, fill_opacity=0.7)
                         .move_to([c.get_x(), good.get_y(), 0]) for c in good if c.rc[0] == 0])
        good_l = text("the same coverage over every unit", size=20, color=GOOD).next_to(good, DOWN, buff=0.55)
        tag = pdk_tag().to_corner(DR, buff=0.3)
        self.play(FadeIn(title), FadeIn(bad), FadeIn(good))
        self.play(FadeIn(wire), FadeIn(bad_l))
        self.play(FadeIn(wires), FadeIn(good_l), FadeIn(tag))

    def extraction(self):
        self.slide(say(
            """
            Finally, prove it. After layout, run parasitic extraction and compare each pair of
            nets: total capacitance, resistance, and coupling to anything noisy. Matched routes
            give numbers within a percent or two of each other. When one pair is off, like the
            folding nodes here, the report tells you which net to look at before the silicon
            does. Then simulate offset and common-mode rejection with the extracted netlist, not
            the schematic.
            """,
            """
            শেষে, প্রমাণ করেন। Layout-এর পরে parasitic extraction চালান আর net-এর প্রত্যেকটা pair তুলনা করেন: মোট capacitance,
            resistance, আর হৈচৈ করা কিছুর সাথে coupling। Matched route-এর সংখ্যাগুলা একে অন্যের এক-দুই percent-এর মধ্যে থাকে। যখন
            একটা pair মেলে না, যেমন এখানে folding node-গুলা, report বলে দেয় কোন net দেখতে হবে, silicon বলার আগেই। তারপর
            offset আর common-mode rejection simulate করেন extracted netlist দিয়া, schematic দিয়া না।
            """,
        ))
        self.clear()
        title = heading("Prove it: compare the extracted pairs")
        rows = [["pair", "left", "right", "difference"],
                ["inputs", "41.2 fF", "41.5 fF", "0.7 %"],
                ["folding nodes", "63.0 fF", "71.8 fF", "14 %"],
                ["outputs", "118 fF", "117 fF", "0.9 %"],
                ["CMFB taps", "22.4 fF", "22.6 fF", "0.9 %"]]
        t = table(rows, col_w=(3.0, 2.2, 2.2, 2.4), size=26, row_gap=0.42).move_to(UP * 0.2)
        for k, row in enumerate(t[0][1:]):
            row[3].set_color(DRAIN if k == 1 else GOOD)
        flag = SurroundingRectangle(t[0][2], color=DRAIN, buff=0.12)
        note = text("then simulate offset and CMRR on the extracted netlist", size=24, color=GATE).to_edge(DOWN, buff=0.9)
        tag = illustrative().to_corner(DL, buff=0.3)
        self.play(FadeIn(title), FadeIn(t), FadeIn(tag))
        self.play(Create(flag))
        self.play(FadeIn(note))

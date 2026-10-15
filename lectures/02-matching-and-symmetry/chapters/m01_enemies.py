"""Lecture 2 · M1 · What makes twins differ.

Six causes, each as a picture on the die with what cancels it, and the matrix of technique
against cause that the rest of the lecture fills in.
"""

import sys
from pathlib import Path

LECTURE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(LECTURE.parents[1]), str(LECTURE)]

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403
from manim_slides import Slide  # noqa: E402

from common import A_COL, B_COL, COLD, HOT, centroid_mark, chapter_title, gradient, illustrative, table, unit  # noqa: E402
from kit.style import *  # noqa: E402,F403

DIE_W, DIE_H = 5.6, 3.8
DIE_C = np.array([-3.3, -0.3, 0])


def die():
    """A die from above: its edge, a ring of pads, and a quiet middle."""
    edge = RoundedRectangle(width=DIE_W, height=DIE_H, corner_radius=0.05, stroke_color=MUTED, stroke_width=3,
                            fill_color=PANEL, fill_opacity=1)
    pads = VGroup()
    for k in range(9):
        x = -DIE_W / 2 + 0.45 + k * (DIE_W - 0.9) / 8
        pads.add(Square(0.22, stroke_width=0, fill_color=FAINT, fill_opacity=1).move_to([x, DIE_H / 2 - 0.22, 0]))
        pads.add(Square(0.22, stroke_width=0, fill_color=FAINT, fill_opacity=1).move_to([x, -DIE_H / 2 + 0.22, 0]))
    for k in range(1, 6):
        y = -DIE_H / 2 + 0.45 + k * (DIE_H - 0.9) / 6
        pads.add(Square(0.22, stroke_width=0, fill_color=FAINT, fill_opacity=1).move_to([-DIE_W / 2 + 0.22, y, 0]))
        pads.add(Square(0.22, stroke_width=0, fill_color=FAINT, fill_opacity=1).move_to([DIE_W / 2 - 0.22, y, 0]))
    return VGroup(edge, pads).move_to(DIE_C)


def pair(a_pos, b_pos, size=0.42):
    return VGroup(unit("A", size).move_to(a_pos), unit("B", size).move_to(b_pos))


def side_text(head, what, fix, color=GATE):
    return VGroup(text(head, size=34, weight="SEMIBOLD", color=color),
                  text(what, size=24, color=INK),
                  VGroup(text("cancel it with", size=20, color=MUTED), text(fix, size=24, color=GOOD)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
                  ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([3.4, 0.0, 0])


class M01Enemies(Chapter, Slide):
    def construct(self):
        self.card()
        self.random()
        self.gradients()
        self.stress()
        self.temperature()
        self.neighbourhood()
        self.wiring()
        self.matrix()

    def card(self):
        self.slide(say(
            """
            Chapter one: what makes twins differ. There are six causes worth naming. Each one
            has a picture on the die, and each one is cancelled by a different habit. Once you
            know which is which, every rule in a matching checklist has a reason.
            """,
            """
            Chapter one: যমজরা আলাদা হয় কেন। নাম দেওয়ার মতো ছয়টা কারণ আছে। প্রত্যেকটার die-এর উপর একটা ছবি আছে, আর প্রত্যেকটা
            কাটে আলাদা একটা অভ্যাস। কোনটা কোনটারে কাটে জানলে, matching checklist-এর প্রত্যেকটা rule-এর একটা কারণ পাবেন।
            """,
        ))
        self.card_group = chapter_title(1, "What makes twins differ", "Six causes, and what cancels each")
        self.play(FadeIn(self.card_group, shift=UP * 0.2), run_time=1.2)

    def random(self):
        self.slide(say(
            """
            One: random variation. Every transistor is made of a countable number of dopant atoms
            and has edges that aren't perfectly straight. Two identical drawings get slightly
            different counts and edges, at random. No placement trick touches this: random means
            your neighbour's luck is independent of yours. Only size helps. Spread the device over
            more area, or more units, and the randomness averages out: four times the area halves
            the spread. That's why critical pairs are big.
            """,
            """
            এক: random variation। প্রত্যেকটা transistor গোনা যায় এমন কয়েকটা dopant atom দিয়া তৈরি, আর তার কিনারা পুরাপুরি সোজা
            না। একই রকম দুইটা drawing random-ভাবে একটু আলাদা সংখ্যা আর কিনারা পায়। কোনো placement কৌশল এইটা ছোঁয় না: random মানে
            পাশের জনের ভাগ্য আপনার থেকে স্বাধীন। শুধু size সাহায্য করে। Device-রে বেশি area-য়, বা বেশি unit-এ ছড়ান, randomness গড়ে
            কাটে: চার গুণ area-তে spread অর্ধেক। এই জন্যই critical pair-গুলা বড়।
            """,
        ))
        self.play(FadeOut(self.card_group))
        title = heading("1 · Random variation")
        rng = np.random.default_rng(7)

        def speckled(label, x, n):
            u = unit(label, 1.6)
            dots = VGroup(*[Dot([x + rng.uniform(-0.7, 0.7), rng.uniform(-0.7, 0.7) - 0.2, 0], radius=0.035,
                                color=INK).set_opacity(0.6) for _ in range(n)])
            return VGroup(u.move_to([x, -0.2, 0]), dots)

        a = speckled("A", -4.6, 23)
        b = speckled("B", -2.4, 31)
        la = text("23 dopants", size=20, color=MUTED).next_to(a, DOWN, buff=0.2)
        lb = text("31 dopants", size=20, color=MUTED).next_to(b, DOWN, buff=0.2)
        side = side_text("Random", "the atoms and edges of each\ndevice, at random; no\nplacement touches it",
                         "area: more units, bigger devices\n(4× the area, ½ the spread)")
        tag = illustrative().to_corner(DL, buff=0.3)
        self.play(FadeIn(title), FadeIn(a), FadeIn(b), FadeIn(tag))
        self.play(FadeIn(la), FadeIn(lb))
        self.play(FadeIn(side, shift=UP * 0.1))

    def gradients(self):
        self.slide(say(
            """
            Two: gradients. Across a die, the oxide is a little thicker on one side, the doping a
            little higher, the line widths a little wider: smooth slopes, from the way the wafer
            was processed. A pair placed side by side sits at two different points on the slope.
            The cure is geometry: split each device into units and arrange them so both devices
            have the same centre of gravity, the same centroid. Then a straight slope adds the same
            to both. Keeping the array compact limits what curvature is left.
            """,
            """
            দুই: gradient। Die জুড়ে oxide এক পাশে একটু মোটা, doping একটু বেশি, line width একটু চওড়া: wafer যেভাবে process হইছে
            তা থেকে মসৃণ ঢাল। পাশাপাশি বসানো একটা pair ঢালের দুইটা আলাদা জায়গায় থাকে। সমাধান জ্যামিতি: প্রত্যেকটা device-রে unit-এ
            ভাগ করেন আর এমনভাবে সাজান যাতে দুইটা device-এর ভারকেন্দ্র একই, মানে একই centroid। তখন একটা সোজা ঢাল দুইটাতেই সমান
            যোগ করে। Array compact রাখলে যতটুকু বাঁক বাকি থাকে সেইটা সীমিত থাকে।
            """,
        ))
        self.clear()
        title = heading("2 · Gradients across the die")
        d = die()
        ramp = gradient(DIE_W - 0.1, DIE_H - 0.1, angle=0.35, cells=30, opacity=0.5).move_to(DIE_C)
        p = pair(DIE_C + [-0.45, 0.2, 0], DIE_C + [0.45, 0.2, 0])
        ma, mb = centroid_mark(p[0].get_center(), A_COL), centroid_mark(p[1].get_center(), B_COL)
        lo = text("thinner oxide", size=18, color=COLD).next_to(d, DOWN, buff=0.15).align_to(d, LEFT)
        hi = text("thicker oxide", size=18, color=HOT).next_to(d, DOWN, buff=0.15).align_to(d, RIGHT)
        side = side_text("Gradients", "smooth slopes in oxide, doping\nand line width across the die",
                         "a common centroid, and a\ncompact array")
        tag = illustrative().to_corner(DL, buff=0.3)
        self.play(FadeIn(title), FadeIn(d), FadeIn(tag))
        self.play(FadeIn(ramp), FadeIn(lo), FadeIn(hi))
        self.play(FadeIn(p), FadeIn(ma), FadeIn(mb))
        self.play(FadeIn(side, shift=UP * 0.1))

    def stress(self):
        self.slide(say(
            """
            Three: mechanical stress. The package and its moulding compound squeeze the die, and
            the squeeze is strongest at the edges and worst at the corners. Stress changes how
            fast carriers move, so a transistor's current depends on where it sits, and also on
            which way it points, because the effect depends on direction. Put matched devices in
            the quiet middle of the die, away from corners and big pads, symmetric about the
            die's centre lines, and draw them pointing the same way.
            """,
            """
            তিন: mechanical stress। Package আর তার moulding compound die-রে চাপ দেয়, আর চাপটা কিনারায় সবচেয়ে বেশি, কোণায় সবচেয়ে
            খারাপ। Stress carrier কত দ্রুত চলে সেইটা বদলায়, তাই একটা transistor-এর current নির্ভর করে সে কোথায় বসে তার উপর, আর
            কোন দিকে মুখ করে তার উপরও, কারণ effect-টা দিকের উপর নির্ভর করে। Matched device-গুলারে die-এর শান্ত মাঝখানে রাখেন, কোণা
            আর বড় pad থেকে দূরে, die-এর মাঝের রেখাগুলার সাপেক্ষে symmetric, আর একই দিকে মুখ করে আঁকেন।
            """,
        ))
        self.clear()
        title = heading("3 · Stress from the package")
        d = die()
        arrows = VGroup()
        for sx, sy in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
            corner = DIE_C + np.array([sx * DIE_W / 2, sy * DIE_H / 2, 0])
            arrows.add(Arrow(corner + np.array([sx * 0.55, sy * 0.55, 0]), corner - np.array([sx * 0.25, sy * 0.25, 0]),
                             buff=0, stroke_color=DRAIN, stroke_width=6))
        for sx in (-1, 1):
            mid = DIE_C + np.array([sx * DIE_W / 2, 0, 0])
            arrows.add(Arrow(mid + np.array([sx * 0.55, 0, 0]), mid - np.array([sx * 0.1, 0, 0]), buff=0, stroke_color=DRAIN, stroke_width=4))
        glow = VGroup(*[Circle(radius=0.75, stroke_width=0, fill_color=DRAIN, fill_opacity=0.18).move_to(
            DIE_C + np.array([sx * (DIE_W / 2 - 0.45), sy * (DIE_H / 2 - 0.45), 0])) for sx in (-1, 1) for sy in (-1, 1)])
        bad = pair(DIE_C + [-DIE_W / 2 + 0.75, DIE_H / 2 - 0.85, 0], DIE_C + [-DIE_W / 2 + 1.25, DIE_H / 2 - 0.85, 0], 0.36)
        good = pair(DIE_C + [-0.22, 0, 0], DIE_C + [0.22, 0, 0], 0.36)
        bad_l = text("near a corner", size=18, color=DRAIN).next_to(bad, DOWN, buff=0.12)
        good_l = text("in the quiet middle", size=18, color=GOOD).next_to(good, DOWN, buff=0.12)
        side = side_text("Stress", "strongest at the edges, worst\nat the corners; it also\ndepends on direction",
                         "the die's middle, away from corners\nand pads; symmetric; one orientation")
        tag = illustrative().to_corner(DL, buff=0.3)
        self.play(FadeIn(title), FadeIn(d), FadeIn(tag))
        self.play(FadeIn(glow), *[GrowArrow(a) for a in arrows])
        self.play(FadeIn(bad), FadeIn(bad_l))
        self.play(FadeIn(good), FadeIn(good_l))
        self.play(FadeIn(side, shift=UP * 0.1))

    def temperature(self):
        self.slide(say(
            """
            Four: temperature. Anything that burns power, an output driver, a regulator, a busy
            digital block, makes a warm spot, and the heat spreads in rings. A transistor's
            current and a bipolar's voltage both move with temperature, so a pair straddling the
            rings sees two temperatures. Either put the pair far away, or put both halves on the
            same ring: symmetric about a line through the heat source. A common centroid also
            cancels the straight part of a thermal slope.
            """,
            """
            চার: temperature। যা কিছু power খায়, output driver, regulator, ব্যস্ত digital block, একটা গরম জায়গা বানায়, আর তাপ
            আংটির মতো ছড়ায়। Transistor-এর current আর bipolar-এর voltage দুইটাই temperature-এর সাথে নড়ে, তাই আংটিগুলার আড়াআড়ি
            বসা একটা pair দুইটা temperature দেখে। হয় pair-টারে অনেক দূরে রাখেন, নয় দুই অর্ধেকরে একই আংটিতে: heat source-এর ভিতর
            দিয়া যাওয়া একটা রেখার সাপেক্ষে symmetric। Common centroid thermal ঢালের সোজা অংশটাও কাটে।
            """,
        ))
        self.clear()
        title = heading("4 · Temperature")
        d = die()
        hot = DIE_C + np.array([-1.2, 0.0, 0])
        src = RoundedRectangle(width=0.9, height=0.6, corner_radius=0.06, fill_color=THERMAL, fill_opacity=0.9, stroke_width=0).move_to(hot)
        src_l = text("driver", size=16, color=BG, weight="SEMIBOLD").move_to(src)
        rings = VGroup(*[Circle(radius=r, stroke_color=THERMAL, stroke_width=2, stroke_opacity=0.9 - 0.15 * k).move_to(hot)
                         for k, r in enumerate((0.65, 0.95, 1.25, 1.55))])
        axis = DashedLine(hot + RIGHT * 0.5, hot + RIGHT * 3.6, stroke_color=MUTED, stroke_width=2)
        bad = pair(hot + np.array([0.95, 0.0, 0]), hot + np.array([1.5, 0.0, 0]), 0.34)
        ang = 0.42
        good = pair(hot + 1.25 * np.array([np.cos(ang), np.sin(ang), 0]), hot + 1.25 * np.array([np.cos(-ang), np.sin(-ang), 0]), 0.3)
        bad_l = text("across the rings", size=18, color=DRAIN).next_to(d, DOWN, buff=0.15)
        good_l = text("on one ring, mirrored about the axis", size=18, color=GOOD).next_to(d, DOWN, buff=0.15)
        axis_l = text("axis", size=16, color=MUTED).next_to(axis.get_end(), UP, buff=0.08).shift(LEFT * 0.3)
        side = side_text("Temperature", "warm spots from anything that\nburns power; heat spreads in rings",
                         "distance, or both halves on one\nring (symmetric about the source)")
        tag = illustrative().to_corner(DL, buff=0.3)
        self.play(FadeIn(title), FadeIn(d), FadeIn(tag))
        self.play(FadeIn(src), FadeIn(src_l), LaggedStart(*[Create(r) for r in rings], lag_ratio=0.2), run_time=1.4)
        self.play(FadeIn(bad), FadeIn(bad_l))
        self.play(FadeOut(bad), FadeOut(bad_l), Create(axis), FadeIn(axis_l), FadeIn(good), FadeIn(good_l))
        self.play(FadeIn(side, shift=UP * 0.1))

    def neighbourhood(self):
        self.slide(say(
            """
            Five: the neighbourhood. What sits right next to a device changes it: the edge of a
            well a micron away, the end of its active area, how close and how dense the
            neighbouring poly and diffusion are. Etching, implants and stress all read the
            surroundings. So give every unit of a matched set the same surroundings: dummy units
            at the ends so the last real one has a neighbour like everyone else, the same distance
            to every well edge and diffusion break, and the same density around the whole group.
            """,
            """
            পাঁচ: আশেপাশ। একটা device-এর ঠিক পাশে যা থাকে, তা তারে বদলায়: এক micron দূরে well-এর কিনারা, তার active area-র শেষ,
            পাশের poly আর diffusion কত কাছে আর কত ঘন। Etching, implant আর stress সবাই আশেপাশটা পড়ে। তাই একটা matched set-এর
            প্রত্যেকটা unit-রে একই আশেপাশ দেন: মাথায় dummy unit, যাতে শেষ আসল unit-টারও সবার মতো একটা প্রতিবেশী থাকে, প্রত্যেকটা
            well edge আর diffusion break পর্যন্ত একই দূরত্ব, আর পুরা group-এর চারপাশে একই ঘনত্ব।
            """,
        ))
        self.clear()
        title = heading("5 · The neighbourhood")
        bad_row = VGroup(*[unit(c, 0.6) for c in "ABAB"]).arrange(RIGHT, buff=0.1).move_to([-3.3, 1.0, 0])
        well = Rectangle(width=0.18, height=1.3, stroke_width=0, fill_color=NWELL, fill_opacity=0.7).next_to(bad_row, LEFT, buff=0.08)
        well_l = text("well edge", size=16, color=NWELL).next_to(well, UP, buff=0.08)
        open_r = text("nothing", size=16, color=MUTED).next_to(bad_row, RIGHT, buff=0.25)
        bad_l = text("the end units see different neighbours", size=20, color=DRAIN).next_to(bad_row, DOWN, buff=0.3)
        good_row = VGroup(*[unit(c, 0.6) for c in "DABABD"]).arrange(RIGHT, buff=0.1).move_to([-3.3, -1.4, 0])
        good_l = text("dummies at both ends; far from the well edge", size=20, color=GOOD).next_to(good_row, DOWN, buff=0.3)
        side = side_text("Neighbourhood", "well edges, the active's ends,\nnearby poly and density",
                         "dummies, the same surroundings,\ndistance from well edges")
        self.play(FadeIn(title), FadeIn(bad_row), FadeIn(well), FadeIn(well_l), FadeIn(open_r))
        self.play(FadeIn(bad_l))
        self.play(FadeIn(good_row), FadeIn(good_l))
        self.play(FadeIn(side, shift=UP * 0.1))

    def wiring(self):
        self.slide(say(
            """
            Six: the wiring. Two matched transistors are only as matched as what connects them.
            A source rail fed from one end drops voltage along its length, so the device at the
            far end gets a slightly smaller gate-to-source voltage, and a different current.
            Drain wires of different lengths and layers have different resistance and capacitance,
            and a signal running over one device but not the other couples into it. The fix is
            to make the wiring itself symmetric: feed rails from the axis, and route each
            differential pair as mirror images.
            """,
            """
            ছয়: wiring। দুইটা matched transistor ততটাই matched, যতটা তাদের জোড়া দেওয়ার জিনিসগুলা। এক মাথা থেকে feed করা একটা
            source rail তার দৈর্ঘ্য বরাবর voltage হারায়, তাই দূরের মাথার device একটু কম gate-to-source voltage পায়, আর আলাদা
            current। আলাদা দৈর্ঘ্য আর layer-এর drain wire-এর resistance আর capacitance আলাদা, আর একটা device-এর উপর দিয়া যাওয়া signal
            আরেকটার উপর দিয়া না গেলে সেইটায় couple করে। সমাধান wiring-রেই symmetric করা: rail axis থেকে feed করেন, আর প্রত্যেকটা
            differential pair mirror image হিসাবে route করেন।
            """,
        ))
        self.clear()
        title = heading("6 · The wiring")
        rail = Rectangle(width=4.8, height=0.22, stroke_width=0, fill_color=METAL, fill_opacity=0.85).move_to([-3.3, 0.9, 0])
        shade = VGroup(*[Rectangle(width=0.48, height=0.22, stroke_width=0, fill_color=DRAIN, fill_opacity=0.08 * k)
                         .move_to([-5.46 + 0.48 * k, 0.9, 0]) for k in range(10)])
        feed = Arrow([-6.2, 0.9, 0], [-5.75, 0.9, 0], buff=0, stroke_color=GATE, stroke_width=5)
        feed_l = text("fed here", size=16, color=GATE).next_to(feed, UP, buff=0.05)
        devs = VGroup(unit("A", 0.6).move_to([-5.0, 0.0, 0]), unit("B", 0.6).move_to([-1.6, 0.0, 0]))
        taps = VGroup(*[Line([d.get_x(), 0.79, 0], [d.get_x(), 0.3, 0], stroke_color=METAL, stroke_width=4) for d in devs])
        drop = text("the voltage drops along the rail:\nB's source sits higher than A's", size=20, color=DRAIN).move_to([-3.3, -0.75, 0])
        fix_rail = Rectangle(width=4.8, height=0.22, stroke_width=0, fill_color=METAL, fill_opacity=0.85).move_to([-3.3, -1.9, 0])
        fix_feed = Arrow([-3.3, -1.35, 0], [-3.3, -1.79, 0], buff=0, stroke_color=GATE, stroke_width=5)
        fix_devs = VGroup(unit("A", 0.5).move_to([-5.0, -2.7, 0]), unit("B", 0.5).move_to([-1.6, -2.7, 0]))
        fix_taps = VGroup(*[Line([d.get_x(), -2.01, 0], [d.get_x(), -2.45, 0], stroke_color=METAL, stroke_width=4) for d in fix_devs])
        fix_l = text("fed at the axis: both see the same drop", size=20, color=GOOD).move_to([-3.3, -3.3, 0])
        side = side_text("Wiring", "IR drop on rails; unequal drain\nand gate routes; coupling",
                         "rails fed from the axis;\nmirror-image routing")
        tag = illustrative().to_corner(DR, buff=0.3)
        self.play(FadeIn(title), FadeIn(rail), FadeIn(devs), Create(taps), FadeIn(tag))
        self.play(GrowArrow(feed), FadeIn(feed_l), FadeIn(shade), FadeIn(drop))
        self.play(FadeIn(fix_rail), GrowArrow(fix_feed), FadeIn(fix_devs), Create(fix_taps), FadeIn(fix_l))
        self.play(FadeIn(side, shift=UP * 0.1))

    def matrix(self):
        self.slide(say(
            """
            Here's the map for the rest of the lecture. Down the side, the techniques; across the
            top, the six causes; a tick where a technique cancels a cause. Notice two things.
            Random variation has exactly one cure, area. And no single technique covers
            everything: a common centroid does nothing about a well edge, and dummies do nothing
            about a gradient. A good layout stacks them. Every block we lay out today will use
            several of these rows at once.
            """,
            """
            বাকি lecture-এর map এইটা। পাশে নিচের দিকে technique-গুলা; উপরে আড়াআড়ি ছয়টা কারণ; যেখানে একটা technique একটা কারণ
            কাটে সেখানে tick। দুইটা জিনিস খেয়াল করেন। Random variation-এর ঠিক একটাই ওষুধ, area। আর কোনো একটা technique সব ঢাকে
            না: common centroid well edge নিয়া কিছু করে না, আর dummy gradient নিয়া কিছু করে না। ভালো layout এগুলা একসাথে জমায়।
            আজকে যে block-গুলার layout করব, প্রত্যেকটায় একসাথে এর কয়েকটা row লাগবে।
            """,
        ))
        self.clear()
        title = heading("Technique against cause")
        Y, P, N = "✓", "½", ""
        rows = [
            ["", "random", "gradient", "stress", "heat", "neighbours", "wiring"],
            ["more area, more units", Y, N, N, N, N, N],
            ["common centroid", N, Y, P, P, N, N],
            ["interdigitation", N, P, N, P, N, N],
            ["dummies, same surroundings", N, N, P, N, Y, N],
            ["one orientation", N, N, Y, N, P, N],
            ["placement on the die", N, N, Y, Y, N, N],
            ["mirror-image routing", N, N, N, N, N, Y],
            ["rails fed from the axis", N, N, N, N, N, Y],
        ]
        t = table(rows, col_w=(4.4, 1.5, 1.6, 1.4, 1.2, 1.9, 1.3), size=22, row_gap=0.24).move_to([0, -0.2, 0])
        for row in t[0][1:]:
            for cell in row[1:]:
                if cell.text == Y:
                    cell.set_color(GOOD)
                elif cell.text == P:
                    cell.set_color(GATE)
        key = text("✓ cancels it    ½ cancels part of it (the straight part, or along one direction)", size=18,
                   color=MUTED).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(title), FadeIn(t[0][0]), FadeIn(t[1]))
        for row in t[0][1:]:
            self.play(FadeIn(row, shift=UP * 0.08), run_time=0.45)
        self.play(FadeIn(key))

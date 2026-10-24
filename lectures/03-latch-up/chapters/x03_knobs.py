"""Lecture 3 · X3 · Four knobs, four rule families.

What layout controls in the parasitic thyristor, shown on the cross-section, and the rule family
each knob became.
"""

import sys
from pathlib import Path

LECTURE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(LECTURE.parents[1]), str(LECTURE)]

from manim import *  # noqa: E402,F403
from manim_slides import Slide  # noqa: E402

from common import NPLUS, PPLUS, CrossSection, box, chapter_title, resistor, table  # noqa: E402
from kit.style import *  # noqa: E402,F403


def callout(n, head, sub, color):
    badge = VGroup(Circle(radius=0.22, stroke_width=0, fill_color=color, fill_opacity=1),
                   text(str(n), size=22, color=BG, weight="BOLD"))
    badge[1].move_to(badge[0])
    words = VGroup(text(head, size=22, color=color, weight="SEMIBOLD"), text(sub, size=17, color=INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
    return VGroup(badge, words).arrange(RIGHT, buff=0.2)


class X03Knobs(Chapter, Slide):
    def construct(self):
        self.card()
        self.knobs()
        self.families()

    def card(self):
        self.slide(say(
            """
            Chapter three: four knobs, four rule families. Layout can't remove the thyristor. What
            it can do is make it very hard to fire and impossible to hold. There are exactly four
            things in the picture you control, and every latch-up rule turns one of them.
            """,
            """
            Chapter three: চারটা knob, চারটা rule family। Layout thyristor-টা সরাতে পারে না। যেটা পারে, সেইটা হইল এরে চালু করা
            খুব কঠিন আর ধরে রাখা অসম্ভব বানানো। ছবিতে ঠিক চারটা জিনিস আপনি নিয়ন্ত্রণ করেন, আর প্রত্যেকটা latch-up rule এর
            একটারে ঘুরায়।
            """,
        ))
        self.card_group = chapter_title(3, "Four knobs, four rule families", "What layout controls in the thyristor")
        self.play(FadeIn(self.card_group, shift=UP * 0.2), run_time=1.2)

    def knobs(self):
        self.slide(say(
            """
            Here they are on the silicon. One: the resistances. A tap close to every device keeps
            R_sub and R_well small, so it takes a much bigger current to reach 0.65 volts. Two:
            the gain. Spacing the N+ away from the well widens the NPN's base and cuts its gain;
            this is why I/O rules ask for extra N+ to well spacing. Three: collection. A guard ring
            catches the injected carriers before they reach the sensitive bases. Four: distance.
            Keep the core far from anything that injects, so most of the current is collected or
            dies out on the way. And a fifth, which really belongs to the first: with many
            supplies, every well must sit at the right potential, or it becomes an injector itself.
            """,
            """
            এই যে silicon-এর উপর এগুলা। এক: resistance। প্রত্যেকটা device-এর কাছে একটা tap R_sub আর R_well ছোট রাখে, তাই 0.65
            volt-এ পৌঁছাতে অনেক বড় current লাগে। দুই: gain। N+-রে well থেকে দূরে রাখলে NPN-এর base চওড়া হয় আর gain কমে; এই
            জন্যই I/O rule বাড়তি N+ থেকে well spacing চায়। তিন: সংগ্রহ। একটা guard ring injected carrier-গুলারে sensitive base
            পর্যন্ত পৌঁছানোর আগেই ধরে ফেলে। চার: দূরত্ব। Core-রে যেকোনো injector থেকে দূরে রাখেন, যাতে বেশিরভাগ current পথেই ধরা
            পড়ে বা মিলিয়ে যায়। আর পঞ্চম একটা, যেটা আসলে প্রথমটারই অংশ: অনেক supply থাকলে প্রত্যেকটা well-রে ঠিক potential-এ
            থাকতে হবে, নইলে সেইটা নিজেই একটা injector হয়ে যায়।
            """,
        ))
        self.play(FadeOut(self.card_group))
        title = heading("Four knobs on the silicon")
        xs = CrossSection(top=-0.1, depth=2.6, well=(0.3, 5.7), well_depth=1.6, p_drn=1.3, p_src=3.0, well_tap=5.0).scale(0.9)
        xs.move_to([0, -1.1, 0])
        top = xs.sub.get_top()[1]
        # 1: the resistances, drawn short, to close taps
        r1 = resistor([xs.diffs["n_src"].get_x(), top - 1.5, 0], [xs.diffs["sub_tap"].get_x(), top - 1.5, 0], GATE, 4, zigs=6)
        r1b = resistor([xs.diffs["p_src"].get_x() + 0.2, top - 0.75, 0], [xs.diffs["well_tap"].get_x(), top - 0.75, 0], GATE, 4, zigs=4)
        # 2: the NPN's base width
        x_n, x_w = xs.diffs["n_src"].get_x(), xs.well.get_left()[0]
        span = DoubleArrow([x_n, top - 0.65, 0], [x_w, top - 0.65, 0], buff=0, stroke_color=NPLUS, stroke_width=4, tip_length=0.18)
        # 3: a guard ring (drawn as an extra N+ well stripe between the nMOS and the well)
        ring = box(x_w - 0.65, top - 1.0, x_w - 0.25, top, NWELL, 1.0, 2)
        ring_tap = box(x_w - 0.6, top - 0.3, x_w - 0.3, top, NPLUS)
        # 4: distance from an injector, off to the left
        inj = Arrow([-6.9, top - 0.6, 0], [-5.9, top - 0.6, 0], buff=0, stroke_color=DRAIN, stroke_width=6)
        inj_l = text("injector", size=18, color=DRAIN).next_to(inj, UP, buff=0.05)
        c1 = callout(1, "Resistance", "taps close to every device", GATE).move_to([-4.2, 2.2, 0])
        c2 = callout(2, "Gain", "N+ to well spacing widens the NPN's base", NPLUS).move_to([2.6, 2.2, 0])
        c3 = callout(3, "Collection", "guard rings catch the carriers", WELL_EDGE_COL).move_to([-4.2, 1.2, 0])
        c4 = callout(4, "Distance", "the core far from injectors", DRAIN).move_to([2.6, 1.2, 0])
        self.play(FadeIn(title), FadeIn(xs))
        self.play(FadeIn(c1), Create(r1), Create(r1b))
        self.play(FadeIn(c2), GrowFromCenter(span))
        self.play(FadeIn(c3), FadeIn(ring), FadeIn(ring_tap))
        self.play(FadeIn(c4), GrowArrow(inj), FadeIn(inj_l))

    def families(self):
        self.slide(say(
            """
            And here's the map from knob to rule. Resistance became the tap rules: a maximum
            distance from any active to a tap of the right kind, and tap density in standard-cell
            rows. Gain became spacing rules, mostly in the I/O: N+ to well and P+ to well spacing.
            Collection became the guard ring rules: where rings are required, how wide, how
            continuous, how well contacted. Distance became the injector rules: a band around every
            pad and every injector where the core must stay out or be ringed. And multiple supplies
            gave us the well rules. The next four chapters take them one at a time.
            """,
            """
            আর এই যে knob থেকে rule-এর map। Resistance থেকে হইছে tap rule: যেকোনো active থেকে ঠিক ধরনের একটা tap পর্যন্ত সর্বোচ্চ
            দূরত্ব, আর standard-cell row-এ tap-এর ঘনত্ব। Gain থেকে হইছে spacing rule, বেশিরভাগ I/O-তে: N+ থেকে well আর P+ থেকে
            well spacing। Collection থেকে হইছে guard ring rule: কোথায় ring লাগবে, কত চওড়া, কতটা একটানা, কতটা ভালো contact করা।
            Distance থেকে হইছে injector rule: প্রত্যেকটা pad আর injector-এর চারপাশে একটা band, যেখানে core বাইরে থাকবে বা ring দিয়া
            ঘেরা থাকবে। আর অনেক supply থেকে আসছে well rule। পরের চারটা chapter এগুলা একটা একটা করে নেয়।
            """,
        ))
        self.clear()
        title = heading("Knob → rule family")
        rows = [["knob", "what it changes", "rule family", "chapter"],
                ["resistance", "R_sub, R_well", "tap distance, tap density", "4"],
                ["gain", "the NPN's base width", "N+ / P+ to well spacing (I/O)", "4, 5"],
                ["collection", "carriers reaching a base", "guard rings", "5"],
                ["distance", "how much current arrives", "injector-to-core spacing", "6"],
                ["many supplies", "junctions that forward-bias", "well spacing, well bias, ERC", "7"]]
        t = table(rows, col_w=(2.5, 4.3, 4.6, 1.3), size=21, row_gap=0.42).move_to(DOWN * 0.1)
        colors = [GATE, NPLUS, WELL_EDGE_COL, DRAIN, PPLUS]
        for row, c in zip(t[0][1:], colors):
            row[0].set_color(c)
            row[2].set_color(INK)
        self.play(FadeIn(title), FadeIn(t[0][0]), FadeIn(t[1]))
        for row in t[0][1:]:
            self.play(FadeIn(row, shift=UP * 0.08), run_time=0.5)


WELL_EDGE_COL = "#7FBF8F"

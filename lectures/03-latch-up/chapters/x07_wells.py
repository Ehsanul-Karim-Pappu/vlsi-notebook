"""Lecture 3 · X7 · Many supplies, many wells.

Wells on different supplies and their spacing; a well tied below the potential of what's inside
it; floating wells; deep N-well isolation and its own parasitics; power-up order.
"""

import sys
from pathlib import Path

LECTURE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(LECTURE.parents[1]), str(LECTURE)]

from manim import *  # noqa: E402,F403
from manim_slides import Slide  # noqa: E402

from common import NPLUS, PPLUS, box, ring, chapter_title, illustrative, marker, pdk_tag  # noqa: E402
from kit.style import *  # noqa: E402,F403

TOP = 0.3
PWELL = "#5C4A55"  # an isolated p-well, a shade lighter than the substrate


def diff(x, color, label, w=0.8, h=0.36, top=TOP):
    r = box(x - w / 2, top - h, x + w / 2, top, color)
    return VGroup(r, text(label, size=15, color=BG, weight="SEMIBOLD").move_to(r))


def lead(x, name, color, h=0.6, top=TOP):
    return VGroup(Line([x, top, 0], [x, top + h, 0], stroke_color=METAL, stroke_width=4),
                  text(name, size=17, color=color, weight="SEMIBOLD").move_to([x, top + h + 0.22, 0]))


class X07Wells(Chapter, Slide):
    def construct(self):
        self.card()
        self.spacing()
        self.bias()
        self.floating()
        self.deep_nwell()
        self.power_up()

    def card(self):
        self.slide(say(
            """
            Chapter seven: many supplies, many wells. A mixed-signal chip has a core supply, one or
            two I/O supplies, analog supplies, maybe a high-voltage domain. Each one gets its own
            wells, and every boundary between them is a place where a junction can end up forward-
            biased.
            """,
            """
            Chapter seven: অনেক supply, অনেক well। একটা mixed-signal chip-এ একটা core supply, এক-দুইটা I/O supply, analog supply,
            হয়তো একটা high-voltage domain থাকে। প্রত্যেকটা নিজের well পায়, আর এদের মাঝের প্রত্যেকটা সীমানা এমন একটা জায়গা যেখানে একটা
            junction forward-bias হয়ে যাইতে পারে।
            """,
        ))
        self.card_group = chapter_title(7, "Many supplies, many wells", "Every boundary is a junction")
        self.play(FadeIn(self.card_group, shift=UP * 0.2), run_time=1.2)

    def spacing(self):
        self.slide(say(
            """
            Two N-wells next to each other, on different supplies: the core at 0.8 volts and the
            I/O at 3.3. Between them, the p-substrate. N, P, N: another lateral bipolar, and a
            leakage path if the wells get close enough for their depletion regions to reach. So
            decks ask for more space between wells on different nets than between wells on the
            same net. The deck knows which is which from the taps' connectivity, so the same
            caveat applies: it's only as good as your labels.
            """,
            """
            পাশাপাশি দুইটা N-well, আলাদা supply-তে: core 0.8 volt-এ আর I/O 3.3-এ। মাঝে p-substrate। N, P, N: আরেকটা lateral bipolar,
            আর well-গুলা এত কাছে আসলে যে তাদের depletion region পৌঁছে যায়, তাহলে একটা leakage path। তাই deck একই net-এর well-এর
            চেয়ে আলাদা net-এর well-এর মাঝে বেশি জায়গা চায়। কোনটা কী, deck জানে tap-এর connectivity থেকে, তাই একই সতর্কতা খাটে: এইটা
            ততটাই ভালো যতটা আপনার label।
            """,
        ))
        self.play(FadeOut(self.card_group))
        title = heading("Wells on different supplies")
        sub = box(-6.4, TOP - 3.0, 6.4, TOP, PSUB)
        w1 = box(-5.6, TOP - 1.8, -1.0, TOP, NWELL)
        w2 = box(1.0, TOP - 1.8, 5.6, TOP, NWELL)
        taps = VGroup(diff(-1.8, NPLUS, "n⁺"), diff(1.8, NPLUS, "n⁺"))
        leads = VGroup(lead(-1.8, "0.8 V core", NPLUS), lead(1.8, "3.3 V I/O", PPLUS))
        gap = DoubleArrow([-1.0, TOP - 1.0, 0], [1.0, TOP - 1.0, 0], buff=0, stroke_color=GATE, stroke_width=4, tip_length=0.18)
        gap_l = text("larger spacing for different nets", size=20, color=GATE).next_to(gap, DOWN, buff=0.15)
        npn = text("N  P  N", size=26, color=INK, weight="SEMIBOLD").move_to([0, TOP - 2.5, 0])
        tag = pdk_tag().to_corner(DR, buff=0.3)
        self.play(FadeIn(title), FadeIn(sub), FadeIn(w1), FadeIn(w2), FadeIn(taps), FadeIn(leads))
        self.play(GrowFromCenter(gap), FadeIn(gap_l), FadeIn(tag))
        self.play(FadeIn(npn))

    def bias(self):
        self.slide(say(
            """
            The quiet killer: a well tied below the potential of what's inside it. Here a PMOS
            whose source sits on the 1.8 volt supply was placed in a well tied to the 0.8 volt
            core supply, perhaps to share a well with its neighbours. The P+ source is now a volt
            above its well: a forward-biased diode, injecting holes all the time, and a PNP that's
            already on. The rule: a well sits at the highest potential of anything P+ inside it.
            DRC alone can't see voltages; this is caught by ERC or by voltage-aware checks, from
            the supply names.
            """,
            """
            নিঃশব্দ ঘাতক: একটা well যেটা তার ভিতরের জিনিসের potential-এর নিচে বাঁধা। এখানে একটা PMOS, যার source 1.8 volt supply-তে,
            এমন একটা well-এ বসানো হইছে যেটা 0.8 volt core supply-তে বাঁধা, হয়তো পাশের device-গুলার সাথে well ভাগ করার জন্য। P+ source
            এখন তার well থেকে এক volt উপরে: একটা forward-biased diode, সারাক্ষণ hole inject করছে, আর একটা PNP যেটা আগে থেকেই on। Rule:
            একটা well তার ভিতরের যেকোনো P+-এর সবচেয়ে বেশি potential-এ বসে। শুধু DRC voltage দেখতে পারে না; এইটা ধরে ERC বা
            voltage-aware check, supply-র নাম থেকে।
            """,
        ))
        self.clear()
        title = heading("A well tied below what's inside it")
        sub = box(-6.4, TOP - 3.0, 6.4, TOP, PSUB)
        well = box(-3.2, TOP - 1.9, 3.2, TOP, NWELL)
        src = diff(-0.8, PPLUS, "p⁺")
        drn = diff(0.8, PPLUS, "p⁺")
        tp = diff(2.4, NPLUS, "n⁺")
        gate = box(-0.4, TOP + 0.04, 0.4, TOP + 0.28, GATE)
        leads = VGroup(lead(-0.8, "1.8 V", PPLUS), lead(2.4, "0.8 V", NPLUS))
        diode = Arrow([-0.8, TOP - 0.4, 0], [-0.8, TOP - 1.5, 0], buff=0, stroke_color=DRAIN, stroke_width=6)
        diode_l = text("forward-biased by 1 V:\nholes, all the time", size=20, color=DRAIN).next_to(diode, LEFT, buff=0.25)
        rule = text("a well sits at the highest potential of any P+ inside it", size=24, color=GOOD).move_to([0, TOP - 3.5, 0])
        how = text("checked by ERC or voltage-aware DRC, not by plain DRC", size=20, color=MUTED).next_to(rule, DOWN, buff=0.15)
        self.play(FadeIn(title), FadeIn(sub), FadeIn(well), FadeIn(src), FadeIn(drn), FadeIn(tp), FadeIn(gate), FadeIn(leads))
        self.play(GrowArrow(diode), FadeIn(diode_l))
        self.play(FadeIn(rule), FadeIn(how))

    def floating(self):
        self.slide(say(
            """
            A floating well, one with no tap at all, is worse than a badly tapped one: its voltage
            is whatever the leakage and coupling make it, and R_well is effectively infinite. A
            tiny current fires its PNP. The same goes for an isolated P-well with no P+ tap.
            Every well needs at least one tap, and then the tap-distance rule from chapter four
            still applies inside it. Decks check this as a well with no tap, or as an ERC on
            floating wells.
            """,
            """
            একটা ভাসমান well, মানে যার কোনো tap-ই নাই, খারাপভাবে tap করা well-এর চেয়েও খারাপ: এর voltage যা leakage আর coupling বানায়
            তাই, আর R_well কার্যত অসীম। খুব ছোট একটা current এর PNP চালু করে দেয়। P+ tap ছাড়া একটা isolated P-well-এর জন্যও একই কথা।
            প্রত্যেকটা well-এ অন্তত একটা tap লাগে, আর তারপর chapter four-এর tap-distance rule এর ভিতরেও খাটে। Deck এইটা check করে
            tap ছাড়া well হিসাবে, বা ভাসমান well-এর উপর একটা ERC হিসাবে।
            """,
        ))
        self.clear()
        title = heading("Floating wells")
        well = box(-4.0, -1.4, 0.0, 1.0, NWELL, 0.6, 2)
        devs = VGroup(*[box(-3.4 + k * 0.9, -0.8, -2.9 + k * 0.9, 0.4, PPLUS, 0.5, 2) for k in range(4)]).move_to(well)
        mk = marker(well, "LUP.WELL.2: no tap", buff=0.08)
        ok = box(1.4, -1.4, 5.4, 1.0, NWELL, 0.6, 2)
        devs2 = VGroup(*[box(2.0 + k * 0.9, -0.8, 2.5 + k * 0.9, 0.4, PPLUS, 0.5, 2) for k in range(3)]).move_to(ok)
        tapring = ring(ok.get_center(), 3.7, 2.1, 0.13, NPLUS)
        ok_l = text("tapped, and within the rule", size=20, color=GOOD).next_to(ok, DOWN, buff=0.2)
        bad_l = text("R_well → ∞: any current fires it", size=20, color=DRAIN).next_to(well, DOWN, buff=0.2)
        self.play(FadeIn(title), FadeIn(well), FadeIn(devs))
        self.play(FadeIn(mk), FadeIn(bad_l))
        self.play(FadeIn(ok), FadeIn(devs2), FadeIn(tapring), FadeIn(ok_l))

    def deep_nwell(self):
        self.slide(say(
            """
            Deep N-well is a popular fix for noise: the NMOS sits in a P-well, which sits in a deep
            N-well, isolated from the shared substrate. It also cuts the NMOS off from substrate
            injection. But it adds layers, and layers mean parasitics: N+ source, P-well, deep
            N-well, substrate is another stack of bipolars. So deep N-well comes with its own
            rules: the deep N-well tied to a supply, through an N-well ring around it; the P-well
            inside tapped like any substrate, with its own distance rule; and spacing to other
            wells.
            """,
            """
            Deep N-well noise-এর একটা জনপ্রিয় সমাধান: NMOS একটা P-well-এ বসে, যেটা একটা deep N-well-এ বসে, ভাগ করা substrate থেকে আলাদা।
            এইটা NMOS-রে substrate injection থেকেও বিচ্ছিন্ন করে। কিন্তু এইটা layer যোগ করে, আর layer মানে parasitic: N+ source, P-well,
            deep N-well, substrate হইল bipolar-এর আরেকটা স্তূপ। তাই deep N-well-এর নিজের rule আছে: deep N-well একটা supply-তে বাঁধা, এর
            চারপাশের একটা N-well ring দিয়া; ভিতরের P-well যেকোনো substrate-এর মতো tap করা, নিজের distance rule সহ; আর অন্য well থেকে spacing।
            """,
        ))
        self.clear()
        title = heading("Deep N-well: isolation, with its own rules")
        sub = box(-6.4, TOP - 3.2, 6.4, TOP, PSUB)
        dnw = box(-4.4, TOP - 2.2, 4.4, TOP - 1.4, NWELL)
        ring = VGroup(box(-4.4, TOP - 1.4, -3.6, TOP, NWELL), box(3.6, TOP - 1.4, 4.4, TOP, NWELL))
        pw = box(-3.6, TOP - 1.4, 3.6, TOP, PWELL)
        devs = VGroup(diff(-2.0, NPLUS, "n⁺"), diff(-0.6, NPLUS, "n⁺"), diff(2.6, PPLUS, "p⁺"),
                      diff(-4.0, NPLUS, "n⁺", 0.6), diff(4.0, NPLUS, "n⁺", 0.6))
        gate = box(-1.7, TOP + 0.04, -0.9, TOP + 0.28, GATE)
        leads = VGroup(lead(-4.0, "VDD", DRAIN), lead(4.0, "VDD", DRAIN), lead(2.6, "VSS (p-well)", MUTED))
        labels = VGroup(text("deep N-well", size=18, color=INK).move_to([0, TOP - 1.8, 0]),
                        text("isolated p-well", size=18, color=INK).move_to([0.9, TOP - 0.9, 0]),
                        text("p-substrate", size=18, color=INK).set_opacity(0.8).move_to([-5.2, TOP - 2.8, 0]))
        stack = text("N+ · P-well · deep N-well · substrate: another stack of bipolars", size=20, color=GATE).move_to([0, TOP - 3.7, 0]).to_edge(LEFT, buff=0.7)
        tag = VGroup(illustrative(), pdk_tag()).arrange(RIGHT, buff=0.3).to_corner(DR, buff=0.3)
        self.play(FadeIn(title), FadeIn(sub))
        self.play(FadeIn(dnw), FadeIn(ring), FadeIn(pw), FadeIn(labels))
        self.play(FadeIn(devs), FadeIn(gate), FadeIn(leads))
        self.play(FadeIn(stack), FadeIn(tag))

    def power_up(self):
        self.slide(say(
            """
            Finally, time. Supplies don't all come up together, and pins can see a voltage before
            the chip is powered: a peripheral powered first, a cable plugged into a live board.
            While a well's supply is still at zero, any P+ in it connected to a live pin is a
            forward-biased injector, and the latch-up can be waiting for the supply to arrive.
            This is mostly solved in the circuit, with tolerant I/O and sequencing, but layout's
            part is the same as before: separate wells for separate domains, the right spacing,
            and guard rings at domain boundaries.
            """,
            """
            শেষে, সময়। সব supply একসাথে ওঠে না, আর chip power পাওয়ার আগেই pin-গুলা একটা voltage দেখতে পারে: আগে power পাওয়া একটা
            peripheral, চালু board-এ লাগানো একটা cable। একটা well-এর supply যখন এখনো শূন্যে, তার ভিতরের যেকোনো P+ যেটা একটা চালু pin-এ
            যুক্ত, সেইটা একটা forward-biased injector, আর latch-up supply আসার অপেক্ষায় থাকতে পারে। এইটা বেশিরভাগ circuit-এ সমাধান হয়,
            tolerant I/O আর sequencing দিয়া, কিন্তু layout-এর অংশ আগের মতোই: আলাদা domain-এর জন্য আলাদা well, ঠিক spacing, আর domain-এর
            সীমানায় guard ring।
            """,
        ))
        self.clear()
        title = heading("Power-up order and hot-plug")
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 3.6, 1], x_length=7.2, y_length=3.8,
                  axis_config={"color": MUTED, "include_ticks": False}).move_to([-2.2, -0.4, 0])
        io = ax.plot(lambda t: 3.3 * min(max((t - 1.0) / 1.0, 0), 1), x_range=[0, 10, 0.02], color=PPLUS, stroke_width=5,
                     use_smoothing=False)
        core = ax.plot(lambda t: 0.8 * min(max((t - 5.0) / 1.0, 0), 1), x_range=[0, 10, 0.02], color=NPLUS, stroke_width=5,
                       use_smoothing=False)
        io_l = text("pin, from a powered peripheral", size=18, color=PPLUS).next_to(ax.c2p(2.0, 3.3), UP, buff=0.1).shift(RIGHT * 1.6)
        core_l = text("the chip's own supply", size=18, color=NPLUS).next_to(ax.c2p(6.0, 0.8), UP, buff=0.1).shift(RIGHT * 1.0)
        danger = box(ax.c2p(2.0, 0)[0], ax.c2p(0, 0)[1], ax.c2p(5.0, 0)[0], ax.c2p(0, 3.6)[1], DRAIN, 0.12, 0)
        danger_l = text("pin live, well at 0 V:\nan injector", size=18, color=DRAIN).move_to(danger).shift(DOWN * 0.6)
        xl = text("time", size=18, color=MUTED).next_to(ax, DOWN, buff=0.15)
        side = VGroup(text("circuit: tolerant I/O, sequencing", size=22, color=INK),
                      text("layout: separate wells per domain,", size=22, color=GOOD),
                      text("the right spacing, rings at the boundary", size=22, color=GOOD)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        side.move_to([4.0, 0.3, 0])
        tag = illustrative().to_corner(DL, buff=0.3)
        self.play(FadeIn(title), Create(ax), FadeIn(xl), FadeIn(tag))
        self.play(Create(io), FadeIn(io_l), Create(core), FadeIn(core_l), run_time=1.5)
        self.play(FadeIn(danger), FadeIn(danger_l))
        self.play(FadeIn(side))

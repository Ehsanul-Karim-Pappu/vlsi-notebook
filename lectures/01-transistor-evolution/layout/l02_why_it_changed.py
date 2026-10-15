"""Layout edition · L2 · Why planar had to go.

Three intuitions, no derivations: an off transistor still leaks; on a short channel the drain
acts like a second gate; and for analog that costs output resistance and gain. The fix: a
thinner channel, gripped from more sides.
"""

import sys
from pathlib import Path

LECTURE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(LECTURE.parents[1]), str(LECTURE), str(LECTURE / "layout")]

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403
from manim_slides import Slide  # noqa: E402

from kit.motifs import xsection  # noqa: E402
from kit.style import *  # noqa: E402,F403


def hill(x, length, drain):
    """An illustrative barrier along the channel, x from 0 (source) to LENGTH (drain): flat on
    top under the gate, falling into the source and drain. DRAIN pulls the drain end down, and
    on a short channel its pull reaches the top."""
    edge = 0.35
    top = 1.0 / (1 + np.exp(-(x - edge) / 0.08)) - 1.0 / (1 + np.exp(-(x - (length - edge)) / 0.08))
    pull = drain * np.exp(-(length - x) / 0.55)
    return top - pull


class L02WhyItChanged(Chapter, Slide):
    def construct(self):
        self.card()
        self.off_is_not_off()
        self.second_gate()
        self.analog_price()
        self.the_fix()

    def card(self):
        self.slide(say(
            """
            Chapter two: why the planar transistor had to go. Three ideas, each in a sentence,
            each behind a rule you already follow.
            """,
            """
            Chapter two: planar transistor-রে কেন বিদায় নিতে হইলো। তিনটা idea, প্রত্যেকটা এক বাক্যে, প্রত্যেকটার পিছনে
            এমন একটা rule যেটা আপনি অলরেডি মানেন।
            """,
        ))
        self.card_group = self.open_chapter(2, 2005, 1971, "Why planar had to go", "Three ideas, one sentence each")

    def off_is_not_off(self):
        self.slide(say(
            """
            One: off isn't off. Below the threshold, a transistor doesn't stop; its current
            falls by about ten times for every sixty to a hundred millivolts you take off the
            gate, at room temperature. Sixty is the best an ordinary transistor can ever do;
            real ones are a bit worse. So at zero volts on the gate there's still a small
            current: leakage. Multiply that by billions of transistors and it's a real part of
            the chip's power. And it set a floor: you can't keep lowering the threshold, and so
            the supply, without the leakage running away.
            """,
            """
            এক: off মানে off না। Threshold-এর নিচে transistor থামে না; gate থেকে প্রতি ষাট থেকে একশো millivolt কমাইলে
            current প্রায় দশ গুণ কমে, room temperature-এ। ষাট হইলো একটা সাধারণ transistor-এর সবচেয়ে ভালো যা সম্ভব; আসলগুলা
            একটু খারাপ। তাই gate-এ শূন্য volt থাকলেও একটা ছোট current থাকে: leakage। Billion transistor দিয়া গুণ করেন, chip-এর
            power-এর একটা আসল অংশ। আর এইটা একটা floor ঠিক করে দিল: threshold, আর তাই supply, কমাইতেই থাকা যায় না, leakage
            লাগামছাড়া না হয়ে।
            """,
        ))
        self.play(FadeOut(self.card_group))
        title = heading("1 · Off isn't off")
        ax = Axes(x_range=[0, 1.0, 0.2], y_range=[0, 6, 1], x_length=7.2, y_length=4.4, tips=False,
                  axis_config={"stroke_color": MUTED, "stroke_width": 2, "include_ticks": False}).move_to([-1.6, -0.5, 0])
        x_l = text("gate voltage", size=22, color=MUTED).next_to(ax.x_axis, DOWN, buff=0.3)
        y_l = text("drain current, log scale", size=22, color=MUTED).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.25)
        vt, ss = 0.45, 0.085  # illustrative: threshold, and the slope in V per decade

        def logi(v):
            return np.where(v < vt, 5.0 - (vt - v) / ss, 5.0 + 0.6 * (1 - np.exp(-(v - vt) / 0.12)))

        curve = ax.plot(lambda v: float(logi(v)), x_range=[0, 1.0], color=ELECTRON, stroke_width=5)
        vt_line = DashedLine(ax.c2p(vt, 0), ax.c2p(vt, 6), stroke_color=FAINT)
        vt_l = text("threshold", size=20, color=MUTED).next_to(ax.c2p(vt, 6), UP, buff=0.08)
        off = Dot(ax.c2p(0, float(logi(0.0))), color=DRAIN, radius=0.1)
        off_l = text("gate at 0 V: still a current\n(leakage)", size=22, color=DRAIN).move_to(ax.c2p(0.62, 0.9))
        steps = VGroup()
        for k in range(3):
            v0 = vt - (k + 1) * ss
            p0, p1, p2 = ax.c2p(v0, float(logi(v0))), ax.c2p(v0 + ss, float(logi(v0))), ax.c2p(v0 + ss, float(logi(v0 + ss)))
            steps.add(VGroup(Line(p0, p1, stroke_color=GATE, stroke_width=3), Line(p1, p2, stroke_color=GATE, stroke_width=3)))
        rule = VGroup(text("about ×10 per 60–100 mV", size=28, color=GATE, weight="SEMIBOLD"),
                      text("60 mV: the best an ordinary\ntransistor can do, at room\ntemperature", size=22, color=MUTED),
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.6, 0.6, 0])
        tag = text("illustrative", size=16, color=MUTED).next_to(ax, DOWN, buff=0.7).align_to(ax, RIGHT)
        self.play(FadeIn(title), Create(ax), FadeIn(x_l), FadeIn(y_l), FadeIn(tag))
        self.play(Create(curve), FadeIn(vt_line), FadeIn(vt_l), run_time=1.6)
        self.play(Create(steps), FadeIn(rule), run_time=1.4)
        self.play(FadeIn(off, scale=0.5), FadeIn(off_l))

    def second_gate(self):
        self.slide(say(
            """
            Two: on a short channel, the drain joins in. Think of the channel as a hill the
            electrons have to climb, from source to drain; the gate sets the height of its top.
            Raise the drain voltage and its end of the hill drops. On a long channel, that's all:
            the top, set by the gate, doesn't move. On a short channel, the drain's pull reaches
            the top and lowers it too. Now the drain is a second gate, one you don't control:
            more drain voltage, more current, more leakage. Its name is DIBL, drain-induced
            barrier lowering.
            """,
            """
            দুই: short channel-এ drain-ও খেলায় নামে। Channel-রে ভাবেন একটা পাহাড়, যেটা electron-গুলারে source থেকে drain
            পর্যন্ত চড়তে হয়; gate ঠিক করে তার চূড়ার উচ্চতা। Drain voltage বাড়ান, পাহাড়ের drain দিকের মাথা নামে। Long channel-এ
            শুধু এইটুকুই: চূড়া, যেটা gate ঠিক করে, নড়ে না। Short channel-এ drain-এর টান চূড়া পর্যন্ত পৌঁছায় আর সেইটাও নামায়।
            এখন drain একটা দ্বিতীয় gate, যেটা আপনি control করেন না: drain voltage বেশি, current বেশি, leakage বেশি। এর নাম
            DIBL, drain-induced barrier lowering।
            """,
        ))
        self.clear()
        title = heading("2 · On a short channel, the drain acts like a gate")
        vd = ValueTracker(0.0)

        def panel(x0, length, label):
            scale = 5.0 / 3.2

            def pts():
                xs = np.linspace(0, length, 160)
                return [[x0 + (x - length / 2) * scale, 0.2 + 1.5 * hill(x, length, vd.get_value()), 0] for x in xs]

            curve = always_redraw(lambda: VMobject(stroke_color=GATE, stroke_width=5).set_points_smoothly(pts()))
            gate_bar = Rectangle(width=(length - 0.7) * scale, height=0.22, fill_color=GATE, fill_opacity=0.35,
                                 stroke_width=0).move_to([x0, 2.25, 0])
            g_l = text("gate", size=20, color=GATE).next_to(gate_bar, UP, buff=0.06)
            s_l = text("source", size=20, color=MUTED).move_to([x0 - length / 2 * scale, -1.55, 0])
            d_l = text("drain", size=20, color=DRAIN).move_to([x0 + length / 2 * scale, -1.55, 0])
            name = text(label, size=26, weight="SEMIBOLD").move_to([x0, -2.1, 0])
            return curve, VGroup(gate_bar, g_l, s_l, d_l, name)

        long_c, long_f = panel(-3.4, 3.2, "long channel")
        short_c, short_f = panel(3.4, 1.4, "short channel")
        top_long = DashedLine([-5.0, 1.7, 0], [-1.8, 1.7, 0], stroke_color=FAINT)
        top_short = DashedLine([2.0, 1.7, 0], [4.8, 1.7, 0], stroke_color=FAINT)
        meter = always_redraw(lambda: text(f"drain voltage: {vd.get_value():.1f}", size=24, color=DRAIN).move_to([0, -2.65, 0]))
        verdict_l = text("the top stays put: the gate is in charge", size=22, color=GOOD).move_to([-3.4, -3.2, 0])
        verdict_s = text("the top drops: a second gate", size=22, color=DRAIN).move_to([3.4, -3.2, 0])
        tag = text("illustrative", size=16, color=MUTED).to_corner(DL, buff=0.3)
        self.play(FadeIn(title), FadeIn(long_f), FadeIn(short_f), FadeIn(tag))
        self.add(long_c, short_c)
        self.play(FadeIn(top_long), FadeIn(top_short), FadeIn(meter))
        self.play(vd.animate.set_value(1.0), run_time=2.5)
        self.play(FadeIn(verdict_l), FadeIn(verdict_s))
        dibl = text("DIBL: drain-induced barrier lowering", size=22, color=MUTED).move_to([3.4, -3.65, 0])
        self.play(FadeIn(dibl))

    def analog_price(self):
        self.slide(say(
            """
            Three: for analog, that has a price. In saturation, a good transistor's current
            hardly changes with its drain voltage: flat curves, a high output resistance, r-o.
            If the drain can move the barrier, the drain voltage moves the current, the curves
            tilt, r-o falls, and with it the gain you get from one transistor, g-m times r-o.
            That's the reason behind a rule you already know: current mirrors and amplifier
            devices are drawn at several times minimum length.
            """,
            """
            তিন: analog-এর জন্য এর একটা দাম আছে। Saturation-এ একটা ভালো transistor-এর current drain voltage-এ প্রায় বদলায়
            না: সমান curve, বড় output resistance, r-o। Drain যদি barrier সরাইতে পারে, drain voltage current-রে নাড়ায়, curve
            কাত হয়, r-o কমে, আর তার সাথে একটা transistor থেকে যে gain পান, g-m গুণ r-o, সেইটাও কমে। আপনার জানা একটা rule-এর
            কারণ এইটাই: current mirror আর amplifier device-গুলা minimum length-এর কয়েক গুণ লম্বা আঁকা হয়।
            """,
        ))
        self.clear()
        title = heading("3 · For analog: output resistance, and gain")

        def plot(x0, slope, name, color, verdict):
            ax = Axes(x_range=[0, 1.2, 0.4], y_range=[0, 1.4, 0.5], x_length=4.6, y_length=2.7, tips=False,
                      axis_config={"stroke_color": MUTED, "stroke_width": 2, "include_ticks": False}).move_to([x0, 0.55, 0])
            curves = VGroup(*[ax.plot(lambda v, k=k: k * (1 - np.exp(-v / 0.12)) * (1 + slope * v), x_range=[0, 1.2],
                                      color=color, stroke_width=4) for k in (0.35, 0.6, 0.85)])
            xl = text("drain voltage", size=18, color=MUTED).next_to(ax.x_axis, DOWN, buff=0.15)
            yl = text("current", size=18, color=MUTED).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.15)
            nm = text(name, size=26, weight="SEMIBOLD").next_to(ax, UP, buff=0.3)
            vd = text(verdict, size=22, color=color).next_to(ax, DOWN, buff=0.5)
            return VGroup(ax, xl, yl, nm), curves, vd

        a_f, a_c, a_v = plot(-3.4, 0.05, "long L", GOOD, "flat: high r_o, high gain")
        b_f, b_c, b_v = plot(3.4, 0.55, "short L", DRAIN, "tilted: low r_o, low gain")
        gain = text("gain of one transistor ≈ g_m · r_o", size=26, color=INK).to_edge(DOWN, buff=1.0)
        note = layout_note("Mirrors and amplifiers are drawn at several times minimum L: the drain then moves "
                           "the current less, the output resistance and the gain stay up, and matching improves.",
                           size=21, width=80).to_edge(DOWN, buff=0.25)
        tag = text("illustrative", size=16, color=MUTED).to_corner(UR, buff=0.3).shift(DOWN * 0.7)
        self.play(FadeIn(title), FadeIn(a_f), FadeIn(b_f), FadeIn(tag))
        self.play(Create(a_c), Create(b_c), run_time=1.6)
        self.play(FadeIn(a_v), FadeIn(b_v))
        self.play(FadeIn(gain))
        self.play(FadeOut(gain), FadeIn(note, shift=UP * 0.1))

    def the_fix(self):
        self.slide(say(
            """
            So how do you get the gate back in charge? Not by pushing the gate harder. Make the
            channel thinner, and put the gate on more sides of it, so the gate's reach is
            everywhere and the drain's isn't. One side, on planar. Three sides, on a fin. All
            the way around, on a sheet. Each of those steps changed what you draw. That's the
            rest of the talk.
            """,
            """
            তাহলে gate-রে আবার control-এ ফিরাবেন কিভাবে? Gate-রে আরও জোরে ঠেলে না। Channel-রে পাতলা করেন, আর তার আরও
            বেশি দিকে gate বসান, যাতে gate-এর হাত সব জায়গায় পৌঁছায় আর drain-এর না। Planar-এ এক দিক। Fin-এ তিন দিক।
            Sheet-এ চারপাশ ঘিরে। এই প্রত্যেকটা ধাপ আপনি কী আঁকেন সেইটা বদলাইছে। Talk-এর বাকিটা এইটা নিয়াই।
            """,
        ))
        self.clear()
        title = heading("The fix: a thinner channel, gripped from more sides")
        shapes = VGroup()
        for kind, name, sides in (("planar", "planar", "gate on one side"), ("finfet", "FinFET", "three sides"),
                                  ("nanosheet", "nanosheet", "all the way around")):
            x = xsection(kind).scale(1.15)
            col = VGroup(x, text(name, size=28, weight="SEMIBOLD"), text(sides, size=22, color=GATE)).arrange(DOWN, buff=0.3)
            shapes.add(col)
        shapes.arrange(RIGHT, buff=1.2, aligned_edge=DOWN).move_to(DOWN * 0.3)
        self.play(FadeIn(title))
        for c in shapes:
            self.play(FadeIn(c, shift=UP * 0.15), run_time=0.8)

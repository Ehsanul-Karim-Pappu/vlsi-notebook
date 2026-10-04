"""Chapter 6 · Losing grip (2005–2011).

Why a short transistor stops turning off: the drain's field reaches the barrier under the gate
(threshold roll-off, DIBL, a worse swing). The natural length λ measures how far it reaches,
and it gives the rule every later architecture follows: wrap more gate around a thinner channel.
"""

import sys
from pathlib import Path

LECTURE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(LECTURE.parents[1]), str(LECTURE)]

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403
from manim_slides import Slide  # noqa: E402

import physics as phys  # noqa: E402
from kit.motifs import xsection  # noqa: E402
from kit.style import *  # noqa: E402,F403

V_BI, PHI_GS = 1.0, 0.4  # the model's source barrier and the gate's long-channel potential (V)
SS0 = phys.subthreshold_swing(300)  # V/decade
CHANNEL = "#7FD8E4"


def energy(x, length, v_ds):
    """An electron's energy (eV) along the transistor, the source at 0: the flat source, the
    channel (quasi-2D model, lengths in λ), the flat drain."""
    if x <= 0:
        return 0.0
    if x >= length:
        return -v_ds
    return V_BI - phys.channel_potential(x, length, 1.0, V_BI, v_ds, PHI_GS)


def peak(length, v_ds):
    """Where the hill is highest, and its height."""
    xs = np.linspace(0, length, 241)
    es = [energy(x, length, v_ds) for x in xs]
    i = int(np.argmax(es))
    return xs[i], es[i]


def rounded(x):
    """A big ratio to two significant figures: 21,437 -> 21,000."""
    if x < 100:
        return f"{x:.0f}"
    k = 10 ** (len(str(int(x))) - 2)
    return f"{round(x / k) * k:,.0f}"


class Ch06LosingGrip(Chapter, Slide):
    def construct(self):
        self.card()
        self.long_channel()
        self.short_channel()
        self.dibl()
        self.equation()
        self.meter()
        self.analog()
        self.natural_length()
        self.gates()
        self.cliffhanger()

    # --- chapter card ------------------------------------------------------------------------
    def card(self):
        self.slide(say(
            """
            Short-channel effects had been fought since the 1970s, mostly with clever doping. By
            the late 2000s, with gates only a few tens of nanometres long, they had become the main
            problem. Even with the gate at zero volts, transistors wouldn't properly turn off. Not
            because of the oxide this time, and not because of Boltzmann. Because of the drain.
            """,
            """
            Short-channel effect-এর সাথে লড়াই চলতেছে 1970-এর দশক থেকে, বেশিরভাগ চালাক doping দিয়া। 2000-এর
            দশকের শেষে, gate-এর length যখন মাত্র কয়েক দশ nanometre, এইটাই হয়ে গেল প্রধান সমস্যা। Gate শূন্য volt-এ
            রাখলেও transistor ঠিকমতো off হয় না। এবার oxide-এর জন্য না, Boltzmann-এর জন্যও না। Drain-এর জন্য।
            """,
        ))
        self.card_group = self.open_chapter(6, 2007, 2005, "Losing grip", "When the drain starts to fight the gate")

    # --- the barrier along the channel -------------------------------------------------------
    def long_channel(self):
        self.slide(say(
            """
            Here's the hill again, now drawn along the transistor: the source on the left, the
            drain on the right, the gate on top. In a long channel, the gate holds the whole
            middle of the channel at its own potential. The source and the drain only bend the
            two ends. Lengths here are in units of lambda, a natural length we'll meet in a
            minute. This channel is ten lambda long.
            """,
            """
            আবার সেই hill, এবার transistor বরাবর আঁকা: বামে source, ডানে drain, উপরে gate। Channel লম্বা হলে gate
            channel-এর পুরা মাঝখানটা নিজের potential-এ ধরে রাখে। Source আর drain শুধু দুই মাথা একটু বাঁকায়। এখানে
            length-গুলা lambda-র unit-এ, একটা natural length, একটু পরেই এইটার পরিচয় হবে। এই channel দশ lambda লম্বা।
            """,
        ))
        self.play(FadeOut(self.card_group))
        L = ValueTracker(10.0)
        V = ValueTracker(0.05)
        self.L, self.V = L, V
        ax = Axes(x_range=[-2, 12, 1], y_range=[-0.9, 0.9, 0.3], x_length=8.4, y_length=4.4).move_to([-1.5, -0.45, 0])
        self.ax = ax

        curve = always_redraw(lambda: ax.plot(lambda x: energy(x, L.get_value(), V.get_value()), x_range=[-2, 12, 0.02],
                                              color=ELECTRON, stroke_width=5, use_smoothing=False))
        gate = always_redraw(lambda: Rectangle(width=L.get_value() * ax.x_length / 14, height=0.32, fill_color=GATE,
                                               fill_opacity=1, stroke_width=0).move_to(ax.c2p(L.get_value() / 2, 0.84)))
        gate_l = always_redraw(lambda: text("gate", size=22, color=BG, weight="SEMIBOLD").move_to(gate))
        src = text("source", size=24, color=MUTED).move_to(ax.c2p(-1.0, -0.13))
        drn = always_redraw(lambda: text("drain", size=24, color=MUTED).move_to(ax.c2p((L.get_value() + 12) / 2, -V.get_value() - 0.13)))
        arrow = Arrow(ax.c2p(-2.2, -0.75), ax.c2p(-2.2, 0.75), buff=0, stroke_color=MUTED, stroke_width=3)
        arrow_l = text("electron energy", size=20, color=MUTED).rotate(PI / 2).next_to(arrow, LEFT, buff=0.1)
        ref = always_redraw(lambda: DashedLine(ax.c2p(-2, 0), ax.c2p(peak(L.get_value(), V.get_value())[0], 0),
                                               stroke_color=FAINT, stroke_width=2))

        def eb_arrow():
            xp, ep = peak(L.get_value(), V.get_value())
            return DoubleArrow(ax.c2p(xp, 0), ax.c2p(xp, ep), buff=0, stroke_color=GATE, stroke_width=3,
                               tip_length=0.14, max_tip_length_to_length_ratio=0.3)

        eb = always_redraw(eb_arrow)
        eb_l = always_redraw(lambda: MathTex("E_b", color=GATE, font_size=34).next_to(eb, RIGHT, buff=0.08))
        brace = always_redraw(lambda: BraceBetweenPoints(ax.c2p(0, -0.92), ax.c2p(L.get_value(), -0.92), direction=DOWN, color=MUTED))
        brace_l = always_redraw(lambda: MathTex(rf"L = {L.get_value():.1f}\,\lambda", font_size=32, color=MUTED).next_to(brace, DOWN, buff=0.08))

        def readout(label, value, color):
            return VGroup(text(label, size=22, color=MUTED), display(value, size=46, color=color)).arrange(DOWN, buff=0.08)

        base = peak(10.0, 0.05)[1]
        self.base = base
        panel = always_redraw(lambda: VGroup(
            readout("barrier", f"{peak(L.get_value(), V.get_value())[1]:.2f} eV", GATE),
            readout("drain voltage", f"{V.get_value():.2f} V", DRAIN),
        ).arrange(DOWN, buff=0.45).move_to([4.95, 0.75, 0]))
        tag = model_tag().move_to([4.95, -3.3, 0])
        title = heading("The hill along the channel")
        self.play(FadeIn(title))
        self.play(FadeIn(arrow), FadeIn(arrow_l), FadeIn(src), FadeIn(drn), Create(curve), run_time=1.5)
        self.play(FadeIn(gate), FadeIn(gate_l), FadeIn(brace), FadeIn(brace_l))
        self.play(FadeIn(ref), FadeIn(eb), FadeIn(eb_l), FadeIn(panel), FadeIn(tag))
        self.title = title
        self.plot = VGroup(curve, gate, gate_l, src, drn, arrow, arrow_l, ref, eb, eb_l, brace, brace_l, panel, tag)

        self.slide(say(
            """
            Now put a real voltage on the drain: from 50 millivolts up to 0.75 volts. The drain
            end drops. But look at the top of the hill: it doesn't move. The drain has no say
            over the barrier; the gate is in charge. That's a good switch.
            """,
            """
            এবার drain-এ আসল voltage দেই: 50 millivolt থেকে 0.75 volt। Drain-এর দিকটা নিচে নামে। কিন্তু hill-এর
            চূড়াটা দেখেন: নড়ে না। Barrier-এর উপর drain-এর কোনো কথা চলে না; control gate-এর হাতে। এইটাই ভালো
            switch।
            """,
        ))
        self.play(Transform(self.title, heading("Long channel: the drain can't touch the hill")))
        self.play(V.animate.set_value(0.75), run_time=2.5)
        self.wait(0.5)
        ok = text("barrier unchanged: the gate is in charge", size=24, color=GOOD).move_to([-1.5, 2.55, 0])
        self.play(FadeIn(ok))
        self.ok = ok

    def short_channel(self):
        self.slide(say(
            """
            Now shrink the channel, with the drain back at 50 millivolts. Ten lambda, six, four,
            three. The source and the drain bend the ends, and in a short channel the two bends
            meet in the middle. The top of the hill sinks by itself, without the gate doing
            anything. The barrier has dropped by a quarter of a volt: with 60 millivolts per
            decade, that's about twenty thousand times more leakage. This is called threshold
            roll-off: the shorter the transistor, the lower its threshold voltage.
            """,
            """
            এবার channel ছোট করি, drain আবার 50 millivolt-এ। দশ lambda, ছয়, চার, তিন। Source আর drain দুই মাথা
            বাঁকায়, আর channel ছোট হলে দুইটা বাঁক মাঝখানে গিয়া মিলে যায়। Gate কিছু না করলেও hill-এর চূড়া নিজে
            নিজেই নেমে যায়। Barrier প্রায় এক volt-এর চার ভাগের এক ভাগ নামছে: প্রতি decade-এ 60 millivolt ধরলে, প্রায়
            বিশ হাজার গুণ বেশি leakage। এইটারে বলে threshold roll-off: transistor যত ছোট, threshold voltage তত কম।
            """,
        ))
        L, V = self.L, self.V
        self.play(FadeOut(self.ok), V.animate.set_value(0.05), run_time=1.2)
        leak = always_redraw(lambda: VGroup(
            text("leakage, vs. the long channel", size=22, color=MUTED),
            display("×" + rounded(10 ** ((self.base - peak(L.get_value(), V.get_value())[1]) / SS0)), size=46, color=DRAIN),
        ).arrange(DOWN, buff=0.08).move_to([4.95, -1.75, 0]))
        self.play(FadeIn(leak), Transform(self.title, heading("Shorten the channel")))
        self.play(L.animate.set_value(3.0), run_time=5, rate_func=rate_functions.ease_in_out_sine)
        roll = text("the hill sinks by itself: threshold roll-off", size=24, color=DRAIN).move_to([-1.5, 2.55, 0])
        self.play(FadeIn(roll))
        self.leak = leak
        self.roll = roll

    def dibl(self):
        self.slide(say(
            """
            And now the drain voltage, on this short channel. 50 millivolts to 0.75 volts again,
            and this time the top of the hill comes down with it. The drain is lowering the
            barrier: it's acting like a second gate, one we don't control. This is DIBL,
            drain-induced barrier lowering. In this model, about 160 millivolts of barrier per volt
            on the drain. The leakage is now over a million times the long channel's. The gate
            has lost its grip.
            """,
            """
            আর এবার এই ছোট channel-এ drain voltage। আবার 50 millivolt থেকে 0.75 volt, আর এইবার hill-এর চূড়াও সাথে
            নিচে নামে। Drain barrier নামায়ে দিতেছে: এইটা একটা দ্বিতীয় gate-এর মতো কাজ করতেছে, যেইটা আমাদের
            control-এ নাই। এইটার নাম DIBL, drain-induced barrier lowering। এই model-এ, drain-এর প্রতি volt-এ barrier
            প্রায় 160 millivolt নামে। Leakage এখন long channel-এর চেয়ে দশ লাখ গুণের বেশি। Gate তার grip হারায়ে
            ফেলছে।
            """,
        ))
        V = self.V
        self.play(FadeOut(self.roll), Transform(self.title, heading("Short channel: the drain pulls the hill down")))
        self.play(V.animate.set_value(0.75), run_time=3)
        d = phys.dibl_mV_per_V(3, 1)
        name = VGroup(text("DIBL: drain-induced barrier lowering", size=24, color=DRAIN, weight="SEMIBOLD"),
                      text(f"{d:.0f} mV of barrier per volt on the drain", size=20, color=MUTED)).arrange(DOWN, buff=0.08)
        name.move_to([-1.5, 2.5, 0])
        self.play(FadeIn(name))
        self.dibl_name = name

    # --- the model, with a ↓ derivation ------------------------------------------------------
    def equation(self):
        self.slide(say(
            """
            Why does this happen? Inside the channel, the potential obeys one simple equation.
            The gate tries to pull the potential to its own value, phi-g-s. The source and the
            drain pin the two ends. And the ends' influence dies away exponentially, over a
            distance lambda: the natural length. So the drain reaches about lambda into the
            channel. If the channel is many lambdas long, the gate owns the middle. If it's only a
            few, the source's and the drain's reach overlap, and the barrier sinks. Everything
            depends on one ratio: L over lambda. Press down for the derivation.
            """,
            """
            কেন এমন হয়? Channel-এর ভেতরে potential একটা সহজ equation মেনে চলে। Gate potential-রে নিজের value
            phi-g-s-এর দিকে টানে। Source আর drain দুই মাথা আটকে রাখে। আর মাথাগুলার প্রভাব exponential-ভাবে মিলায়ে
            যায়, lambda দূরত্বে: এইটাই natural length। মানে drain channel-এর ভেতরে মোটামুটি lambda পর্যন্ত হাত
            বাড়ায়। Channel যদি অনেক lambda লম্বা হয়, মাঝখানটা gate-এর দখলে। মাত্র কয়েক lambda হলে source আর
            drain-এর হাত মাঝখানে মিলে যায়, আর barrier নেমে যায়। সবকিছু নির্ভর করে একটা ratio-র উপর: L বাই lambda।
            Derivation দেখতে নিচে (↓) যান।
            """,
        ))
        self.play(FadeOut(self.plot), FadeOut(self.leak), FadeOut(self.dibl_name))
        self.play(Transform(self.title, heading("Why: the drain reaches in a distance λ")))
        e1 = eq(r"\frac{d^2\phi}{dx^2}", r"-", r"\frac{\phi-\phi_{gs}}{\lambda^2}", r"=0", size=50)
        e1_l = text("the gate pulls the potential to φ_gs; the ends pin it", size=22, color=MUTED)
        e2 = eq(r"\phi(x)-\phi_{gs}", r"\;\propto\;", r"e^{-x/\lambda}", r",\;", r"e^{-(L-x)/\lambda}", size=44)
        e2[2].set_color(MUTED)
        e2[4].set_color(DRAIN)
        e2_l = text("the source's and the drain's influence die away over λ", size=22, color=MUTED)
        e3 = eq(r"\Delta E_b", r"\approx", r"2\sqrt{ab}\;", r"e^{-L/2\lambda}", size=44)
        e3[0].set_color(GATE)
        e3[3].set_color(DRAIN)
        e4 = eq(r"SS", r"=", r"\frac{60\ \text{mV/dec}}{1-\operatorname{sech}(L/2\lambda)}", size=44)
        costs = VGroup(e3, e4).arrange(RIGHT, buff=1.2)
        costs_l = text("the barrier sinks (long-channel limit), and the swing gets worse (V_DS ≈ 0), as L/λ falls", size=20, color=MUTED)
        col = VGroup(VGroup(e1, e1_l).arrange(DOWN, buff=0.15), VGroup(e2, e2_l).arrange(DOWN, buff=0.15),
                     VGroup(costs, costs_l).arrange(DOWN, buff=0.15)).arrange(DOWN, buff=0.5).move_to([0, -0.2, 0])
        key = text("It all depends on L / λ.", size=30, color=GATE, weight="SEMIBOLD").to_edge(DOWN, buff=0.45)
        hint = text("↓ derivation", size=20, color=MUTED).to_corner(DR, buff=0.35)
        self.play(Write(e1), FadeIn(e1_l))
        self.play(Write(e2), FadeIn(e2_l))
        self.play(Write(costs), FadeIn(costs_l))
        self.play(FadeIn(key), FadeIn(hint))
        screen = VGroup(self.title, col, key, hint)

        steps = [
            (eq(r"\varepsilon_{Si}\,t_{Si}\,\frac{d^2\phi}{dx^2}\,dx", size=36),
             ("Gauss's law on a slice of channel, dx long and t_Si thick: the field along it, in minus out.",
              "Channel-এর dx লম্বা, t_Si পুরু একটা slice-এ Gauss's law: channel বরাবর field, ঢোকে বিয়োগ বের হয়।")),
            (eq(r"+\;N\,\frac{\varepsilon_{ox}}{t_{ox}}\,(V_G'-\phi)\,dx", r"\;=\;", r"q N_A t_{Si}\,dx", size=36),
             ("Plus the field from N gates, each a capacitor ε_ox/t_ox. It all ends on the slice's charge.",
              "সাথে N-টা gate থেকে oxide দিয়া আসা field, প্রত্যেকটা ε_ox/t_ox-এর একটা capacitor; সব গিয়া শেষ হয় slice-এর charge-এ।")),
            (eq(r"\frac{d^2\phi}{dx^2}-\frac{\phi-\phi_{gs}}{\lambda^2}=0,", r"\quad", r"\lambda^2=\frac{\varepsilon_{Si}\,t_{Si}\,t_{ox}}{N\,\varepsilon_{ox}}", size=36),
             ("Divide by ε_Si t_Si dx; the constants make φ_gs, the long-channel potential.",
              "ε_Si t_Si dx দিয়া ভাগ করেন, আর constant-গুলা φ_gs-এ জড়ো করেন: long channel-এর potential।")),
            (eq(r"\phi=\phi_{gs}+a\,\frac{\sinh\frac{L-x}{\lambda}}{\sinh\frac{L}{\lambda}}+b\,\frac{\sinh\frac{x}{\lambda}}{\sinh\frac{L}{\lambda}}", size=36),
             ("Solve with φ fixed at the source and the drain: a = V_bi − φ_gs, b = V_bi + V_DS − φ_gs.",
              "Source আর drain-এ φ fix রেখে solve করেন: a = V_bi − φ_gs, b = V_bi + V_DS − φ_gs।")),
            (eq(r"\phi_{min}-\phi_{gs}\approx 2\sqrt{ab}\,e^{-L/2\lambda}", r"\quad\Rightarrow\quad", r"\text{DIBL}\propto e^{-L/2\lambda}", size=36),
             ("For L much longer than λ, each sinh becomes an exponential. Raising V_DS raises b: that is DIBL.",
              "L যখন λ-র চেয়ে অনেক বড়, sinh-গুলা exponential হয়ে যায়। V_DS বাড়াইলে b বাড়ে: এইটাই DIBL।")),
        ]
        shown = VGroup()
        for i, (m, (why, why_bn)) in enumerate(steps):
            self.slide(say(f"Derivation, step {i + 1} of {len(steps)}: {why}", f"Derivation, step {i + 1} / {len(steps)}: {why_bn}"),
                       direction="vertical")
            if i == 0:
                self.detour_in(screen)
            why_t = text(why, size=18, color=MUTED)
            step = VGroup(m, why_t).arrange(DOWN, buff=0.08)
            if len(shown):
                step.next_to(shown, DOWN, buff=0.3)
            else:
                step.move_to([0, 3.55 - step.height / 2, 0])
            self.play(Write(m), FadeIn(why_t))
            shown.add(m, why_t)
        self.play(Circumscribe(steps[2][0][2], color=GATE, fade_out=True))

        self.slide(say("Back to the story.", "আবার গল্পে ফিরি।"), direction="vertical")
        self.detour_out(screen, shown)
        self.screen = screen

    # --- the control meter -------------------------------------------------------------------
    def meter(self):
        self.slide(say(
            """
            Here's the whole story in two curves, from the model. Left: DIBL against the channel
            length in lambdas. Right: the swing. Above about six lambda, both are fine: DIBL is
            small and the swing is close to 60. Below it, both blow up fast. The rule of thumb:
            keep the gate at least about six lambda long; different sources quote anything from
            five to ten. And note: this lambda is an electrostatic length, not the layout lambda of
            chapter 4. Same letter, different thing.
            """,
            """
            পুরা গল্পটা দুইটা curve-এ, model থেকে। বামে: channel length, lambda-র হিসাবে, তার সাথে DIBL। ডানে:
            swing। মোটামুটি ছয় lambda-র উপরে দুইটাই ঠিক আছে: DIBL কম, swing 60-এর কাছাকাছি। এর নিচে দুইটাই দ্রুত
            খারাপ হয়। Rule of thumb: gate-রে অন্তত মোটামুটি ছয় lambda লম্বা রাখেন; বিভিন্ন source পাঁচ থেকে দশ পর্যন্ত
            বলে। আর খেয়াল করেন: এই lambda একটা electrostatic length, chapter 4-এর layout lambda না। একই অক্ষর, আলাদা
            জিনিস।
            """,
        ))
        self.play(FadeOut(self.screen))
        title = heading("How short is too short?")
        kw = dict(x_length=5.0, y_length=3.6, tips=False,
                  axis_config={"stroke_color": MUTED, "stroke_width": 2, "include_ticks": True, "tick_size": 0.05})
        a1 = Axes(x_range=[2, 12, 2], y_range=[0, 250, 50], **kw).move_to([-3.3, -0.1, 0])
        a2 = Axes(x_range=[2, 12, 2], y_range=[50, 150, 25], **kw).move_to([3.4, -0.1, 0])
        for a, ys in ((a1, [0, 100, 200]), (a2, [50, 100, 150])):
            a.x_axis.add_labels({v: MathTex(str(v), font_size=26, color=MUTED) for v in (2, 4, 6, 8, 10, 12)})
            a.y_axis.add_labels({v: MathTex(str(v), font_size=26, color=MUTED) for v in ys})
        x1 = MathTex(r"L/\lambda", font_size=30, color=MUTED).next_to(a1.x_axis, DOWN, buff=0.45)
        x2 = MathTex(r"L/\lambda", font_size=30, color=MUTED).next_to(a2.x_axis, DOWN, buff=0.45)
        y1 = text("barrier DIBL (mV/V)", size=22, color=DRAIN).next_to(a1.y_axis, UP, buff=0.15)
        y1.shift(RIGHT * max(0, -6.75 - y1.get_left()[0]))  # keep it inside the frame
        y2 = text("swing at V_DS ≈ 0 (mV/decade)", size=22, color=GATE).next_to(a2.y_axis, UP, buff=0.15)
        c1 = a1.plot(lambda k: min(phys.dibl_mV_per_V(k, 1), 250), x_range=[2.75, 12, 0.1], color=DRAIN, stroke_width=5)
        c2 = a2.plot(lambda k: min(phys.short_channel_swing(k, 1) * 1e3, 150), x_range=[2.4, 12, 0.1], color=GATE, stroke_width=5)
        floor = DashedLine(a2.c2p(2, 59.5), a2.c2p(12, 59.5), stroke_color=MUTED, stroke_width=2)
        floor_l = text("60", size=18, color=MUTED).next_to(a2.c2p(12, 59.5), RIGHT, buff=0.08)

        def zone(a, top):
            lo, hi = a.c2p(2, top), a.c2p(6, a.y_range[0])
            return Rectangle(width=hi[0] - lo[0], height=lo[1] - hi[1], fill_color=DRAIN, fill_opacity=0.12,
                             stroke_width=0).move_to((lo + hi) / 2)

        z1, z2 = zone(a1, 250), zone(a2, 150)
        zl = text("L < 6λ", size=20, color=DRAIN).move_to(z1.get_top() + DOWN * 0.25)
        zl2 = text("L < 6λ", size=20, color=DRAIN).move_to(z2.get_top() + DOWN * 0.25)
        tag = model_tag().to_corner(DR, buff=0.35)
        rule = text("Rule of thumb: keep L ≳ 6λ  (sources say 5–10)", size=26, color=INK, weight="SEMIBOLD").to_edge(DOWN, buff=0.4)
        self.play(FadeIn(title), Create(a1), Create(a2), FadeIn(x1), FadeIn(x2), FadeIn(y1), FadeIn(y2), FadeIn(tag))
        self.play(Create(c1), Create(c2), FadeIn(floor), FadeIn(floor_l), run_time=2)
        self.play(FadeIn(z1), FadeIn(z2), FadeIn(zl), FadeIn(zl2))
        dots = VGroup()
        for k in (3, 6, 10):
            d1 = Dot(a1.c2p(k, phys.dibl_mV_per_V(k, 1)), color=DRAIN, radius=0.07)
            d2 = Dot(a2.c2p(k, phys.short_channel_swing(k, 1) * 1e3), color=GATE, radius=0.07)
            l1 = text(f"{phys.dibl_mV_per_V(k, 1):.0f}", size=18, color=DRAIN).next_to(d1, UR, buff=0.05)
            l2 = text(f"{phys.short_channel_swing(k, 1) * 1e3:.0f}", size=18, color=GATE).next_to(d2, UR, buff=0.05)
            dots.add(d1, d2, l1, l2)
        self.play(FadeIn(dots), FadeIn(rule))

    # --- analog: gain ------------------------------------------------------------------------
    def analog(self):
        g3, g6, g10 = (phys.intrinsic_gain(k, 1, 0.4) for k in (3, 6, 10))
        g10 = round(g10, -1)
        self.slide(say(
            f"""
            For analog, DIBL has a direct price. If the drain moves the barrier, the drain
            voltage moves the current, and that is output conductance. Below threshold the current
            follows the barrier, and both the gate and the drain pull on it: the gate by alpha-g,
            the drain by alpha-d. So the transistor's own gain, g-m times r-o, is alpha-g over
            alpha-d. With 0.4 volts on the drain, in this model: at three lambda, a gain of about
            {g3:.0f}. At six, about {g6:.0f}. At ten, nearly {g10:.0f}. Real devices have other effects
            too, so take these as an upper limit. But it's why your current mirrors and amplifier
            transistors are drawn longer than minimum, and why the matched devices in a pair always
            share the same L.
            """,
            f"""
            Analog-এর জন্য DIBL-এর একটা সরাসরি দাম আছে। Drain যদি barrier নাড়ায়, তাহলে drain voltage current
            নাড়ায়, আর সেইটাই output conductance। Threshold-এর নিচে current barrier-রে follow করে, আর gate আর drain
            দুইটাই barrier-রে টানে: gate টানে alpha-g দিয়া, drain alpha-d দিয়া। তাই transistor-এর নিজের gain, g-m গুণ
            r-o, হইলো alpha-g বাই alpha-d। Drain-এ 0.4 volt দিলে, এই model-এ: তিন lambda-তে gain প্রায় {g3:.0f}। ছয়-এ
            প্রায় {g6:.0f}। দশ-এ প্রায় {g10:.0f}। আসল device-এ আরও effect আছে, তাই এগুলারে upper limit ধরেন। কিন্তু এই কারণেই
            আপনার current mirror আর amplifier-এর transistor minimum-এর চেয়ে লম্বা করে আঁকা হয়, আর matched pair-এর দুইটা
            device-এর L সবসময় এক।
            """,
        ))
        self.clear()
        title = heading("DIBL is output conductance")
        e1 = eq(r"\frac{g_{ds}}{g_m}", r"=", r"\frac{\alpha_d}{\alpha_g}", r"\quad\Rightarrow\quad", r"g_m r_o", r"=", r"\frac{\alpha_g}{\alpha_d}", size=46)
        e1[2].set_color(DRAIN)
        e1[6].set_color(DRAIN)
        e1_l = text("α_g, α_d: how hard the gate and the drain each pull the barrier top", size=22, color=MUTED)
        VGroup(e1, e1_l).arrange(DOWN, buff=0.15).move_to([0, 2.15, 0])
        rows = VGroup()
        unit = 6.0 / 200
        for k in (3, 6, 10):
            g = phys.intrinsic_gain(k, 1, 0.4)
            bar = Rectangle(width=max(g * unit, 0.04), height=0.42, fill_color=GOOD, fill_opacity=0.8, stroke_width=0)
            lab = MathTex(rf"L = {k}\lambda", font_size=34, color=INK)
            val = text(f"gain ≈ {g:.0f}", size=24, color=GOOD)
            rows.add(VGroup(lab, bar, val))
        for r in rows:
            r[0].move_to([-4.6, 0, 0])
            r[1].move_to([-3.5 + r[1].width / 2, 0, 0])
            r[2].next_to(r[1], RIGHT, buff=0.2)
        for i, r in enumerate(rows):
            r.shift(UP * (0.75 - 0.75 * i))
        tag = VGroup(model_tag(), text("weak inversion, V_DS = 0.4 V, the barrier's pull only; real devices are lower", size=18, color=MUTED)).arrange(RIGHT, buff=0.2)
        tag.next_to(rows, DOWN, buff=0.3).align_to(rows, LEFT)
        note = layout_note("Analog transistors are drawn longer than minimum: for gain, and because a short "
                           "device's V_T depends on its exact L. Matched pairs share the same L, and the same "
                           "orientation.", size=22, width=78).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(title), Write(e1), FadeIn(e1_l))
        for r in rows:
            self.play(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), FadeIn(r[2]), run_time=0.9)
        self.play(FadeIn(tag))
        self.play(FadeIn(note, shift=UP * 0.15))

    # --- the natural length ------------------------------------------------------------------
    def natural_length(self):
        self.slide(say(
            """
            So how do you get the grip back? Not by pushing the gate harder: a higher gate voltage
            just moves the whole curve. You make lambda smaller. And here's lambda, in a simple
            model of a thin channel. Three things set it. The channel's thickness, t-Si: a thinner
            channel, a shorter reach. The oxide, t-ox: but we already took that as far as it goes,
            to about one nanometre, in the last chapter. And N: an equivalent number of gates
            around the channel. It's a toy, and real geometries need real calculations, but it
            captures the strategy behind every new architecture since 2011: a thinner channel, with
            more gate around it.
            """,
            """
            তাহলে grip ফিরায়ে পাবো কীভাবে? Gate-রে আরও জোরে চাপ দিয়া না: gate voltage বাড়াইলে শুধু পুরা curve-টা
            সরে। Lambda ছোট করতে হবে। আর এই হইলো lambda। তিনটা জিনিস এইটা ঠিক করে। Channel-এর thickness, t-Si:
            channel যত পাতলা, drain-এর হাত তত ছোট। Oxide, t-ox: কিন্তু সেইটা তো আগের chapter-এই যতদূর যায় নিয়া গেছি,
            প্রায় এক nanometre। আর N: channel-এর চারপাশে equivalent কয়টা gate। এইটা একটা toy, আসল geometry-র জন্য
            আসল হিসাব লাগে, কিন্তু 2011-এর পর থেকে প্রত্যেকটা নতুন architecture-এর কৌশল এইটাই: পাতলা channel, তার
            চারপাশে আরও gate।
            """,
        ))
        self.clear()
        title = heading("Don't push harder. Make λ smaller.")
        lam = MathTex(r"\lambda", r"=", r"\sqrt{\frac{\varepsilon_{Si}\,", r"t_{Si}", r"\,", r"t_{ox}", r"}{", r"N", r"\,\varepsilon_{ox}}}",
                      font_size=96, color=INK).move_to([0, 0.3, 0])
        lam[3].set_color(SILICON)
        lam[5].set_color(OXIDE_TEXT)
        lam[7].set_color(GATE)
        labels = VGroup(
            text("channel thickness:\nmake it thinner", size=22, color=SILICON).move_to([lam[3].get_x() - 1.7, 2.45, 0]),
            text("oxide (EOT): already\n~1 nm (chapter 5)", size=22, color=OXIDE_TEXT).move_to([lam[5].get_x() + 1.9, 2.45, 0]),
            text("N, an equivalent number of gates:\nwrap more around it", size=22, color=GATE).next_to(lam, DOWN, buff=0.5),
        )
        ar = VGroup(
            Arrow(labels[0].get_bottom(), lam[3].get_top(), buff=0.12, stroke_color=SILICON, stroke_width=3, tip_length=0.15),
            Arrow(labels[1].get_bottom(), lam[5].get_top(), buff=0.12, stroke_color=OXIDE_TEXT, stroke_width=3, tip_length=0.15),
            Arrow(labels[2].get_top(), lam[7].get_bottom(), buff=0.1, stroke_color=GATE, stroke_width=3, tip_length=0.15),
        )
        src = source("A toy model: Young 1989; Yan et al. 1992; Colinge 2004. Real geometries: Frank, Taur and Wong 1998")
        self.play(FadeIn(title))
        self.play(Write(lam), run_time=2)
        for lbl, a in zip(labels, ar):
            self.play(FadeIn(lbl), GrowArrow(a), run_time=0.8)
        self.play(FadeIn(src))

    def gates(self):
        self.slide(say(
            """
            Now count the gates, in this toy model. Planar, one gate on top, with an effective
            channel depth of about 15 nanometres: lambda is about 6.7 nanometres, so by the
            six-lambda rule the gate shouldn't be much shorter than 40. Two gates, one above and
            one below a 10 nanometre film: 3.9, so about 23. Three, a fin six nanometres thick: 2.4,
            so about 15. And four, all the way around a 5 nanometre square wire: 1.9, so about 12.
            Same oxide every time. Treat these as a trend, not hard limits: real fins and sheets
            aren't squares, and a wide, thin sheet behaves mostly like a double gate.
            """,
            """
            এবার gate গুনি, এই toy model-এ। Planar, উপরে একটা gate, channel-এর effective depth প্রায় 15 nanometre:
            lambda প্রায় 6.7 nanometre, তাই ছয়-lambda rule অনুযায়ী gate 40-এর চেয়ে খুব একটা ছোট হওয়া উচিত না। দুইটা gate,
            10 nanometre-এর একটা film-এর উপরে আর নিচে: 3.9, তাই প্রায় 23। তিনটা, মানে ছয় nanometre পুরু একটা fin: 2.4,
            তাই প্রায় 15। আর চারটা, 5 nanometre-এর একটা square wire-এর চারপাশ ঘিরে: 1.9, তাই প্রায় 12। প্রতিবার oxide
            একই। এগুলারে trend হিসাবে নেন, শক্ত limit না: আসল fin আর sheet square না, আর চওড়া পাতলা একটা sheet বেশিরভাগ
            double gate-এর মতো আচরণ করে।
            """,
        ))
        self.clear()
        title = heading("Count the gates (a toy model)")
        cases = [(1, 15, "planar", "planar"), (2, 10, "double", "double gate"), (3, 6, "finfet", "fin (three faces)"),
                 (4, 5, "nanosheet", "all around (square wire)")]
        cols = VGroup()
        bars = VGroup()
        unit = 1.9 / 40
        for n, t, kind, name in cases:
            pic = self.double_gate() if kind == "double" else xsection(kind)
            pic.scale_to_fit_height(1.45)
            lam = phys.natural_length_nm(t, 1, n)
            label = VGroup(MathTex(rf"N = {n}", font_size=36, color=GATE), text(name, size=20, color=MUTED),
                           text(f"t_Si = {t} nm", size=20, color=SILICON),
                           MathTex(rf"\lambda = {lam:.1f}\ \text{{nm}}", font_size=34, color=INK)).arrange(DOWN, buff=0.1)
            cols.add(VGroup(pic, label).arrange(DOWN, buff=0.25))
            bar = Rectangle(width=0.7, height=6 * lam * unit, fill_color=DRAIN, fill_opacity=0.75, stroke_width=0)
            bars.add(VGroup(bar, text(f"{6 * lam:.0f} nm", size=22, color=DRAIN)))
        cols.arrange(RIGHT, buff=0.9).move_to([0, 1.15, 0])
        base_y = -3.4
        for col, b in zip(cols, bars):
            b[0].move_to([col.get_x(), base_y + b[0].height / 2, 0])
            b[1].next_to(b[0], UP, buff=0.08)
        bar_l = text("≈ 6λ\n(rule of\nthumb)", size=20, color=DRAIN).move_to([-6.2, -2.6, 0])
        tag = VGroup(model_tag(), text("1 nm oxide (EOT);\nN: Colinge's\nequivalent gates", size=16, color=MUTED)).arrange(DOWN, buff=0.1).move_to([6.2, 2.4, 0])
        tag.shift(LEFT * max(0, tag.get_right()[0] - 6.8))
        self.play(FadeIn(title), FadeIn(tag))
        for col, b in zip(cols, bars):
            self.play(FadeIn(col, shift=UP * 0.15), GrowFromEdge(b[0], DOWN), FadeIn(b[1]), run_time=1.0)
            if col is cols[0]:
                self.play(FadeIn(bar_l), run_time=0.4)

    @staticmethod
    def double_gate():
        """A thin film between a top and a bottom gate."""
        def box(w, h, y, color):
            return Rectangle(width=w, height=h, fill_color=color, fill_opacity=1, stroke_width=0).move_to([0, y, 0])
        return VGroup(box(1.8, 0.55, 0.62, GATE), box(1.8, 0.08, 0.31, OXIDE_TEXT), box(1.8, 0.46, 0.0, SILICON),
                      box(1.8, 0.08, -0.31, OXIDE_TEXT), box(1.8, 0.55, -0.62, GATE), box(3.0, 0.5, -1.15, SUBSTRATE))

    # --- cliffhanger -------------------------------------------------------------------------
    def cliffhanger(self):
        self.slide(say(
            """
            So the way forward was clear: a thin channel with gate on more than one side. On a
            flat wafer, that's hard: how do you put a gate underneath a channel? The answer that
            won was to stop building the channel flat. Stand it up on its edge, like a fin, and
            wrap the gate over the top and down both sides.
            """,
            """
            তো সামনে যাওয়ার রাস্তা পরিষ্কার: পাতলা একটা channel, একাধিক দিকে gate। Flat wafer-এ এইটা কঠিন: channel-এর
            নিচে gate বসাবেন কীভাবে? যে উত্তরটা জিতলো: channel-রে আর flat বানানো যাবে না। এটারে কিনারার উপর খাড়া
            করে দাঁড় করান, একটা fin-এর মতো, আর gate-টা উপর দিয়া আর দুই পাশ দিয়া মুড়ে দেন।
            """,
        ))
        self.clear()
        a = text("Don't push harder. Hold tighter.", size=46, weight="SEMIBOLD").to_edge(UP, buff=0.7)
        b = text("Stand the channel up.", size=34, color=GATE).next_to(a, DOWN, buff=0.3)
        flat = xsection("planar").scale(1.3).move_to([0, -1.1, 0])
        fin = xsection("finfet").scale(1.3).move_to([0, -1.1, 0])
        self.play(FadeIn(a))
        self.play(FadeIn(flat))
        self.wait(0.5)
        self.play(FadeIn(b), ReplacementTransform(flat, fin), run_time=2.0)
        self.wait(1)

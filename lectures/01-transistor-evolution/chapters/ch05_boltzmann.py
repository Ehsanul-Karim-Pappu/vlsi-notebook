"""Chapter 5 · Boltzmann's tyranny (2003–2007).

Why a transistor needs about 60 mV of gate voltage to cut its current tenfold, why that stopped
the supply voltage from shrinking, and the gate oxide that got too thin.
"""

import sys
from math import exp, log, log10
from pathlib import Path

LECTURE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(LECTURE.parents[1]), str(LECTURE)]

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403
from manim_slides import Slide  # noqa: E402

import physics as phys  # noqa: E402
from kit.motifs import Barrier, Boltzmann  # noqa: E402
from kit.style import *  # noqa: E402,F403

LN10 = log(10)
I_SPEC = 2e-7  # puts I_D(V_T) near 100 nA, a common threshold definition
LOG0 = 13  # the I-V plot draws log10(I) + LOG0, so its x axis sits at the bottom


class Ch05Boltzmann(Chapter, Slide):
    def construct(self):
        self.card()
        self.hill()
        self.tail()
        self.divider()
        self.swing()
        self.iv()
        self.power_wall()
        self.oxide()
        self.cliffhanger()

    # --- chapter card ------------------------------------------------------------------------
    def card(self):
        self.slide(say(
            """
            For forty years, shrinking worked. Every new generation was smaller, faster and
            cheaper. Then, around 2005, something stopped: clock speeds stopped their steady
            climb. This chapter is about why. And a big part of the reason isn't engineering. It's
            thermodynamics.
            """,
            """
            চল্লিশ বছর ধরে ছোট করা কাজ করছে। প্রত্যেকটা নতুন generation আরও ছোট, আরও fast, আরও সস্তা।
            তারপর 2005-এর দিকে একটা জিনিস থেমে গেল: clock speed-এর একটানা বাড়া বন্ধ হইলো। এই chapter হইলো কেন,
            সেটা নিয়া। আর কারণের বড় একটা অংশ engineering না। সেইটা thermodynamics।
            """,
        ))
        self.card_group = self.open_chapter(
            5, 2005, 1965, "Boltzmann's tyranny",
            "The thermal limit every ordinary transistor lives with",
        )

    # --- a transistor is a hill --------------------------------------------------------------
    def hill(self):
        hill_notes = say(
            """
            Remember the hill from the junction transistor? Here it is again, for the MOSFET. The
            height of this line is the energy of an electron at each point along the transistor.
            On the left, the source, full of electrons. On the right, the drain, lower down. In
            between, under the gate, the hill. An electron only gets to the drain if it has enough
            energy to get over it. And the electrons are never still: they jiggle with thermal
            energy.
            """,
            """
            Junction transistor-এর hill-টা মনে আছে? এই যে আবার, এবার MOSFET-এর জন্য। এই line-টার উচ্চতা হইলো
            transistor বরাবর প্রত্যেক জায়গায় একটা electron-এর energy। বামে source, electron-এ ভরা। ডানে drain,
            আরও নিচে। মাঝখানে, gate-এর নিচে, hill। একটা electron drain-এ যাইতে পারে শুধু যদি hill পার হওয়ার মতো
            energy থাকে। আর electron-গুলা কখনো স্থির থাকে না: thermal energy-তে সারাক্ষণ কাঁপতেছে।
            """,
        )
        self.slide(hill_notes, auto_next=True)
        self.play(FadeOut(self.card_group))
        self.b = ValueTracker(0.30)
        self.d = ValueTracker(0.25)
        bar = Barrier(self.b, self.d, n=170)
        self.bar = bar
        gate = Rectangle(width=2.4, height=0.35, fill_color=GATE, fill_opacity=1, stroke_width=0).move_to([0, 2.45, 0])
        gate_lbl = text("gate", size=24, color=BG, weight="SEMIBOLD").move_to(gate)
        src_lbl = text("source", size=26, color=MUTED).move_to([-3.1, -1.65, 0])
        drn_lbl = text("drain", size=26, color=MUTED).move_to([3.4, -3.55, 0])
        axis = Arrow([-5.6, -1.5, 0], [-5.6, 2.2, 0], buff=0, stroke_color=MUTED, stroke_width=3)
        axis_lbl = text("electron energy", size=22, color=MUTED).rotate(PI / 2).next_to(axis, LEFT, buff=0.1)
        eb = always_redraw(lambda: DoubleArrow([1.55, bar.energy_y(0), 0], [1.55, bar.energy_y(self.b.get_value()), 0],
                                               buff=0, stroke_color=GATE, stroke_width=3, tip_length=0.15))
        eb_lbl = always_redraw(lambda: MathTex("E_b", color=GATE, font_size=36).next_to(eb, RIGHT, buff=0.1))
        title = heading("A transistor is a hill")
        self.play(FadeIn(title))
        self.play(Create(bar.edge), FadeIn(src_lbl), FadeIn(drn_lbl), FadeIn(axis), FadeIn(axis_lbl))
        self.play(FadeIn(gate), FadeIn(gate_lbl), FadeIn(eb), FadeIn(eb_lbl))
        # Fade in the group itself (not each dot): its updater only runs while it is in the scene.
        self.play(FadeIn(bar.dots, scale=0.5, lag_ratio=0.004), run_time=1.5)
        bar.start()
        self.wait(1)

        self.slide(hill_notes, loop=True)
        self.wait(4)

        self.slide(say(
            """
            The gate's job is to set the height of that hill. Raise the gate voltage and the hill
            comes down: more electrons have enough energy to get over, and current flows. Lower
            it and the hill goes back up. That's the whole switch.
            """,
            """
            Gate-এর কাজ হইলো ওই hill-এর উচ্চতা ঠিক করা। Gate voltage বাড়াইলে hill নিচে নামে: আরও বেশি
            electron-এর পার হওয়ার মতো energy থাকে, current চলে। কমাইলে hill আবার উঠে যায়। পুরা switch-টা এইটাই।
            """,
        ))
        counter = always_redraw(lambda: text(f"{bar.crossed} electrons over the hill",
                                             size=26, color=ELECTRON).move_to([4.3, 1.9, 0]))
        bar.crossed = 0
        vg = text("raise the gate voltage", size=24, color=GATE).next_to(gate, RIGHT, buff=0.3)
        self.play(Transform(title, heading("The gate sets the height of the hill")))
        self.add(counter)
        self.play(FadeIn(vg), self.b.animate.set_value(0.08), run_time=3)
        self.wait(3)
        self.play(FadeOut(vg), self.b.animate.set_value(0.30), run_time=2)
        self.wait(1)
        self.hill_parts = VGroup(title, gate, gate_lbl, src_lbl, drn_lbl, axis, axis_lbl, eb, eb_lbl, counter)

    # --- the Boltzmann tail ------------------------------------------------------------------
    def tail(self):
        self.slide(say(
            """
            Here's the question that matters: when the switch is off, how many electrons still
            make it over? Those electrons are leakage, and leakage is wasted power. Thermal energy
            isn't shared out evenly: most electrons have very little, a few have a lot. For the
            high-energy ones that matter here, the number falls off exponentially with energy: the
            Boltzmann tail, on a scale of k-B-T, the thermal energy, about 26
            milli-electron-volts at room temperature. It's a simplified picture, but it's the one
            that sets the numbers.
            """,
            """
            আসল প্রশ্নটা হইলো: switch off থাকলে কয়টা electron তবুও পার হয়ে যায়? ওই electron-গুলাই leakage, আর
            leakage মানে power নষ্ট। Thermal energy সবার মধ্যে সমান ভাগ হয় না: বেশিরভাগ electron-এর energy কম,
            অল্প কয়েকটার অনেক। এখানে যে বেশি-energy-র electron-গুলা দরকার, energy বাড়ার সাথে তাদের সংখ্যা
            exponential-ভাবে কমে: Boltzmann tail, k-B-T-এর scale-এ, মানে thermal energy, room temperature-এ প্রায় 26
            milli-electron-volt। এইটা একটা সরল ছবি, কিন্তু সংখ্যাগুলা এইটাই ঠিক করে।
            """,
        ))
        self.bar.stop()
        self.play(FadeOut(self.bar), FadeOut(self.hill_parts))
        b0 = 7.4  # starting barrier, in k_BT
        bk = ValueTracker(b0)
        dist = Boltzmann(bk, height=5.2, width=3.6).move_to([-3.6, -0.45, 0])
        b_lbl = always_redraw(lambda: MathTex("E_b", color=GATE, font_size=34).next_to(dist.axes.c2p(1.05, bk.get_value()), RIGHT, buff=0.1))
        title = heading("How many electrons make it over?")
        e1 = eq(r"n(E)", r"\;\propto\;", r"e^{-E/", r"k_BT", r"}")
        e1[3].set_color(THERMAL)
        e2 = eq(r"\frac{N(E > E_b)}{N}", r"\;=\;", r"e^{-", r"E_b", r"/", r"k_BT", r"}")
        e2[3].set_color(GATE)
        e2[5].set_color(THERMAL)
        kt = VGroup(eq(r"k_BT", r"= 25.9\ \text{meV}", size=36), text("at 300 K", size=24, color=MUTED)).arrange(RIGHT, buff=0.2)
        kt[0][0].set_color(THERMAL)
        col = VGroup(e1, e2, kt).arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to([2.6, 0.6, 0])
        self.play(FadeIn(title))
        self.play(Create(dist.axes), FadeIn(dist[-2:]))
        self.play(Create(dist.curve), run_time=1.5)
        self.play(Write(e1))

        self.slide(say(
            """
            The electrons that get over the hill are the ones in this tail, above the barrier. The
            fraction is e to the minus barrier height over k-T. So the current is exponential in
            the barrier height.
            """,
            """
            যে electron-গুলা hill পার হয়, ওরা এই tail-এর মধ্যে, barrier-এর উপরে। ভাগটা হইলো e to the minus barrier
            height বাই k-T। মানে current barrier height-এর সাথে exponential।
            """,
        ))
        self.play(FadeIn(dist.tail), Create(dist.line), FadeIn(b_lbl))
        self.play(Write(e2))
        self.play(FadeIn(kt))

        self.slide(say(
            """
            So how far do we have to lower the barrier to get ten times as many electrons over? Sixty
            milli-electron-volts. Notice what's not in this number. Not the material, not the size
            of the transistor, not how clever the design is. Only the temperature.
            """,
            """
            তাহলে দশ গুণ বেশি electron পার করাইতে barrier কতটা নামাইতে হবে? ষাট milli-electron-volt। খেয়াল করেন এই
            সংখ্যায় কী নাই। Material নাই, transistor-এর size নাই, design কত চালাক সেটাও নাই। আছে শুধু temperature।
            """,
        ))
        ratio = always_redraw(lambda: VGroup(
            text("electrons over the hill", size=24, color=MUTED),
            display(f"×{exp(b0 - bk.get_value()):,.0f}", size=60, color=ELECTRON),
        ).arrange(DOWN, buff=0.1).move_to([-3.2, 3.15, 0]))
        self.play(FadeOut(title), FadeIn(ratio))
        self.play(bk.animate.set_value(b0 - LN10), run_time=2.5)
        d1 = eq(r"\frac{n'}{n}", r"= e^{\Delta E/k_BT}", r"= 10")
        d2 = eq(r"\Delta E", r"= ", r"k_BT", r"\ln 10")
        d2[2].set_color(THERMAL)
        d3 = eq(r"= 25.9\ \text{meV} \times 2.30", r"\approx", r"60\ \text{meV}")
        d3[2].set_color(GATE)
        VGroup(d1, d2, d3).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to([2.6, -1.6, 0])
        self.play(col.animate.shift(UP * 1.2).set_opacity(0.45))
        self.play(Write(d1))
        self.play(Write(d2))
        self.play(Write(d3))
        self.play(Circumscribe(d3[2], color=GATE))

        self.slide(say(
            """
            Another 60: a hundred times. Another: a thousand. It's a ratchet. Every 60 meV is one
            decade of current, wherever you start.
            """,
            """
            আরও 60: একশ গুণ। আরও 60: হাজার গুণ। একটা ratchet-এর মতো। যেখান থেকেই শুরু করেন, প্রতি 60 meV মানে
            current-এর এক decade।
            """,
        ))
        self.play(bk.animate.set_value(b0 - 2 * LN10), run_time=2)
        self.wait(0.5)
        self.play(bk.animate.set_value(b0 - 3 * LN10), run_time=2)
        rule = text("Every 60 meV: ten times the current.", size=28, color=GATE, weight="SEMIBOLD")
        rule.move_to([2.6, -3.35, 0])
        self.play(FadeIn(rule, shift=UP * 0.2))

    # --- the capacitive divider (with a ↓ derivation) ----------------------------------------
    def divider(self):
        self.slide(say(
            """
            One more piece. The gate doesn't touch the electrons. It pushes on them through the
            oxide, which is a capacitor. And under the channel there's another capacitor, the
            depletion region, connected to the substrate. So the gate voltage is shared out by a
            capacitive divider, and only a fraction, one over m, reaches the channel. m is called
            the body factor, and it's always at least one. Press down for the derivation.
            """,
            """
            আরেকটা টুকরা বাকি। Gate electron-গুলারে সরাসরি ছোঁয় না। ধাক্কা দেয় oxide দিয়া, আর oxide হইলো একটা
            capacitor। আর channel-এর নিচে আরেকটা capacitor আছে, depletion region, substrate-এর সাথে জোড়া। তাই gate
            voltage একটা capacitive divider দিয়া ভাগ হয়, আর channel-এ পৌঁছায় শুধু একটা ভাগ, এক বাই m। m-রে বলে body
            factor, আর এইটা সবসময় অন্তত এক। Derivation দেখতে নিচে (↓) যান।
            """,
        ))
        self.clear()
        title = heading("But the gate doesn't push the hill directly")
        x = -3.6
        top = Dot([x, 2.2, 0], color=GATE, radius=0.08)
        vg = MathTex("V_G", color=GATE, font_size=40).next_to(top, LEFT, buff=0.2)

        def cap(y, color, label):
            p1 = Line([x - 0.6, y + 0.1, 0], [x + 0.6, y + 0.1, 0], stroke_color=color, stroke_width=6)
            p2 = Line([x - 0.6, y - 0.1, 0], [x + 0.6, y - 0.1, 0], stroke_color=color, stroke_width=6)
            lbl = MathTex(label, color=color, font_size=38).next_to(p1, RIGHT, buff=0.3).shift(DOWN * 0.1)
            return VGroup(p1, p2, lbl)

        cox = cap(1.2, OXIDE_TEXT, "C_{ox}")
        node = Dot([x, 0.2, 0], color=ELECTRON, radius=0.1)
        node_lbl = VGroup(MathTex(r"\psi_s", color=ELECTRON, font_size=40),
                          text("channel surface", size=22, color=ELECTRON)).arrange(DOWN, buff=0.05).next_to(node, LEFT, buff=0.3)
        cdep = cap(-0.8, HOLE, "C_{dep}")
        ground = VGroup(Line([x - 0.5, -1.9, 0], [x + 0.5, -1.9, 0]), Line([x - 0.32, -2.05, 0], [x + 0.32, -2.05, 0]),
                        Line([x - 0.14, -2.2, 0], [x + 0.14, -2.2, 0])).set_stroke(MUTED, 4)
        sub_lbl = text("substrate", size=22, color=MUTED).next_to(ground, DOWN, buff=0.1)
        wires = VGroup(Line(top.get_center(), [x, 1.3, 0]), Line([x, 1.1, 0], node.get_center()),
                       Line(node.get_center(), [x, -0.7, 0]), Line([x, -0.9, 0], [x, -1.9, 0])).set_stroke(INK, 3)
        circuit = VGroup(wires, top, vg, cox, node, node_lbl, cdep, ground, sub_lbl)
        e1 = eq(r"\Delta\psi_s", r"=", r"\Delta V_G", r"\,\frac{C_{ox}}{C_{ox}+C_{dep}}", r"=", r"\frac{\Delta V_G}{m}")
        e1[0].set_color(ELECTRON)
        e1[2].set_color(GATE)
        e2 = eq(r"m", r"= 1 + \frac{C_{dep}}{C_{ox}}", r"\;\geq 1")
        e2[0].set_color(OXIDE_TEXT)
        note = text("The gate gets only 1/m of its\nvoltage onto the channel.", size=26, color=MUTED)
        col = VGroup(e1, e2, note).arrange(DOWN, buff=0.55).move_to([2.4, 0.2, 0])
        hint = text("↓ derivation", size=20, color=MUTED).to_corner(DR, buff=0.35)
        self.play(FadeIn(title))
        self.play(Create(wires), FadeIn(top), FadeIn(vg), run_time=1.2)
        self.play(FadeIn(cox), FadeIn(node), FadeIn(node_lbl), FadeIn(cdep), FadeIn(ground), FadeIn(sub_lbl))
        self.play(Write(e1))
        self.play(Write(e2))
        self.play(FadeIn(note), FadeIn(hint))
        screen = VGroup(title, circuit, col, hint)

        steps = [
            (eq(r"I_D", r"\;\propto\;", r"e^{\,q\psi_s/k_BT}"),
             ("Current: the Boltzmann tail, set by the surface potential.", "Current: Boltzmann tail, surface potential দিয়া ঠিক হয়।")),
            (eq(r"\frac{d\psi_s}{dV_G}", r"=", r"\frac{1}{m}"),
             ("The divider: the channel follows the gate at 1/m.", "Divider: channel gate-রে 1/m হারে follow করে।")),
            (eq(r"\frac{d\,\log_{10} I_D}{dV_G}", r"=", r"\frac{1}{\ln 10}\cdot\frac{q}{k_BT}\cdot\frac{1}{m}"),
             ("Chain rule, and change from e to base 10.", "Chain rule, আর e থেকে base 10-এ নেওয়া।")),
            (eq(r"SS", r"\equiv", r"\frac{dV_G}{d\,\log_{10} I_D}", r"=", r"m\,\frac{k_BT}{q}\,\ln 10"),
             ("Invert it: the gate voltage needed per decade of current.", "উল্টায়ে দেন: current-এর প্রতি decade-এ কত gate voltage লাগে।")),
        ]
        shown = VGroup()
        y = 2.5
        for i, (m, (why, why_bn)) in enumerate(steps):
            self.slide(say(f"Derivation, step {i + 1} of 4: {why}", f"Derivation, step {i + 1} / 4: {why_bn}"), direction="vertical")
            if i == 0:
                self.detour_in(screen)
            why_t = text(why, size=22, color=MUTED)
            VGroup(m, why_t).arrange(DOWN, buff=0.12).move_to([0, y, 0])
            y -= 1.5
            self.play(Write(m), FadeIn(why_t))
            shown.add(m, why_t)
        self.play(Circumscribe(steps[-1][0][4], color=GATE))

        self.slide(say("Back to the story.", "আবার গল্পে ফিরি।"), direction="vertical")
        self.detour_out(screen, shown)
        self.screen = screen

    # --- the subthreshold swing --------------------------------------------------------------
    def swing(self):
        self.slide(say(
            """
            Put the two pieces together, the Boltzmann tail and the divider, and you get the
            subthreshold swing: how much gate voltage it takes to change the current ten times. A
            perfect gate, m equal to one, at room temperature, still needs 60 millivolts per
            decade. No transistor that works by lifting electrons over a hill, with an ordinary
            gate and no internal gain, can do better at room temperature. People call it the
            Boltzmann tyranny.
            """,
            """
            দুইটা টুকরা একসাথে করেন, Boltzmann tail আর divider, তাহলে পাবেন subthreshold swing: current দশ গুণ
            বদলাইতে কত gate voltage লাগে। একদম perfect gate, মানে m এক, room temperature-এ, তবুও লাগে প্রতি
            decade-এ 60 millivolt। যে transistor electron-রে hill পার করায়ে কাজ করে, সাধারণ gate দিয়া, ভিতরে কোনো
            gain ছাড়া, room temperature-এ সে এর চেয়ে ভালো পারবে না। এইটারে বলে Boltzmann tyranny।
            """,
        ))
        self.play(FadeOut(self.screen))
        title = heading("The subthreshold swing")
        big = MathTex(r"SS", r"=", r"m", r"\,\frac{k_BT}{q}", r"\,\ln 10", r"\;\geq\;", r"60\ \tfrac{\text{mV}}{\text{decade}}",
                      font_size=84, color=INK)
        big[2].set_color(OXIDE_TEXT)
        big[3].set_color(THERMAL)
        big[6].set_color(GATE)
        big.move_to(UP * 0.6)
        labels = VGroup(
            text("how well the gate\ngrips the channel", size=22, color=OXIDE_TEXT).next_to(big[2], DOWN, buff=0.5).shift(LEFT * 0.4),
            text("temperature", size=22, color=THERMAL).next_to(big[3], DOWN, buff=0.35).shift(RIGHT * 0.6),
            text("at 300 K, with a\nperfect gate (m = 1)", size=22, color=GATE).next_to(big[6], DOWN, buff=0.35),
        )
        self.play(FadeIn(title))
        self.play(Write(big[:5]), run_time=2)
        self.play(FadeIn(labels[0]), FadeIn(labels[1]))
        self.play(Write(big[5:]), FadeIn(labels[2]))
        box = SurroundingRectangle(big[6], color=GATE, buff=0.15, corner_radius=0.1)
        self.play(Create(box))

        self.slide(say(
            """
            The only knob is temperature: cool the chip to liquid nitrogen and, in this ideal
            formula, the swing drops to 15 millivolts per decade. Real cold transistors don't get
            all the way there, but they do get steeper. And remember the bipolar transistor from chapter two, whose
            current rises ten times for every 60 millivolts? Not a coincidence. It's the same
            Boltzmann tail.
            """,
            """
            হাতে knob একটাই: temperature। Chip-রে liquid nitrogen-এ ঠান্ডা করেন, এই ideal formula-য় swing নেমে আসবে
            প্রতি decade-এ 15 millivolt-এ। আসল ঠান্ডা transistor পুরাটা পৌঁছায় না, কিন্তু slope আরও খাড়া হয়। আর chapter two-এর bipolar transistor মনে আছে, যার current প্রতি 60 millivolt-এ দশ গুণ
            বাড়ে? এইটা কাকতালীয় না। সেই একই Boltzmann tail।
            """,
        ))
        cold = VGroup(text("Cool it to 77 K (liquid nitrogen):", size=28, color=MUTED),
                      MathTex(r"SS = 15\ \text{mV/decade}", font_size=44, color=ELECTRON),
                      text("(ideal)", size=24, color=MUTED)).arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=1.0)
        bjt = text("The same 60 mV sets a bipolar transistor's current: one Boltzmann tail, two devices.", size=22, color=MUTED).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(cold, shift=UP * 0.2))
        self.play(FadeIn(bjt))

    # --- I-V on a log scale, and Dennard's demand --------------------------------------------
    def iv(self):
        self.slide(say(
            """
            Here's what that means for a real transistor: current against gate voltage, on a log
            scale. Below the threshold voltage, V-T, the curve is a straight line, one decade for
            every 70 or so millivolts. This region is called weak inversion, and analog designers
            bias here on purpose: it gives the most transconductance per unit of current. A good
            digital switch needs a huge ratio between on and off, a million or more. With the
            threshold at 0.4 volts and a 1 volt supply, we get about that.
            """,
            """
            এবার একটা আসল transistor-এর জন্য এর মানে দেখেন: gate voltage-এর সাথে current, log scale-এ। Threshold
            voltage V-T-এর নিচে curve-টা সোজা line, প্রতি 70-এর মতো millivolt-এ এক decade। এই region-রে বলে weak
            inversion, আর analog designer-রা ইচ্ছা করেই এইখানে bias করেন: প্রতি unit current-এ সবচেয়ে বেশি
            transconductance এইখানেই। ভালো digital switch-এ on আর off-এর ratio লাগে বিশাল, এক million বা তার
            বেশি। Threshold 0.4 volt আর supply 1 volt হলে মোটামুটি সেটাই পাই।
            """,
        ))
        self.clear()
        axes = Axes(x_range=[0, 1.0, 0.2], y_range=[0, 10, 1], x_length=7.6, y_length=4.8, tips=False,
                    axis_config={"stroke_color": MUTED, "stroke_width": 2, "include_ticks": True, "tick_size": 0.05}).move_to([-1.6, 0.0, 0])
        axes.x_axis.add_labels({v: MathTex(f"{v:.1f}", font_size=26, color=MUTED) for v in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]})
        axes.y_axis.add_labels({k: MathTex(f"10^{{{k - LOG0}}}", font_size=26, color=MUTED) for k in range(1, 10, 2)})
        x_t = MathTex(r"V_{GS}\ (\text{V})", font_size=32, color=MUTED).next_to(axes.x_axis, DOWN, buff=0.5)
        y_t = MathTex(r"I_D\ (\text{A})", font_size=32, color=MUTED).next_to(axes.y_axis, UP, buff=0.15)
        m = 1.2
        ss = phys.subthreshold_swing(300, m)
        vt = ValueTracker(0.40)
        vdd = ValueTracker(1.0)

        def logi(v):
            return log10(phys.drain_current(v, vt.get_value(), 300, m, I_SPEC)) + LOG0

        curve = always_redraw(lambda: axes.plot(logi, x_range=[0, 1.0, 0.004], color=ELECTRON, stroke_width=5))
        vt_line = always_redraw(lambda: DashedLine(axes.c2p(vt.get_value(), 0), axes.c2p(vt.get_value(), 10), stroke_color=GATE, stroke_width=2))
        vt_lbl = always_redraw(lambda: MathTex("V_T", color=GATE, font_size=32).next_to(axes.c2p(vt.get_value(), 10), UP, buff=0.05))
        off = always_redraw(lambda: Dot(axes.c2p(0, logi(0)), color=DRAIN, radius=0.09))
        off_lbl = always_redraw(lambda: MathTex(r"I_{off}", color=DRAIN, font_size=34).next_to(off, RIGHT, buff=0.15))
        on = always_redraw(lambda: Dot(axes.c2p(vdd.get_value(), logi(vdd.get_value())), color=GOOD, radius=0.09))
        on_lbl = always_redraw(lambda: MathTex(r"I_{on}", color=GOOD, font_size=34).next_to(on, UP + LEFT, buff=0.08))
        title = heading("On and off, on a log scale")
        self.play(FadeIn(title), Create(axes), FadeIn(x_t), FadeIn(y_t))
        self.play(Create(curve), run_time=2)
        self.play(FadeIn(vt_line), FadeIn(vt_lbl), FadeIn(off), FadeIn(off_lbl), FadeIn(on), FadeIn(on_lbl))
        v0 = 0.08
        p0, p1 = axes.c2p(v0, logi(v0)), axes.c2p(v0 + ss, logi(v0))
        p2 = axes.c2p(v0 + ss, logi(v0 + ss))
        tri = VGroup(Line(p0, p1), Line(p1, p2)).set_stroke(GATE, 3)
        tri_l = VGroup(text(f"{ss * 1e3:.0f} mV", size=22, color=GATE).next_to(Line(p0, p1), DOWN, buff=0.08),
                       text("≈×10", size=22, color=GATE).next_to(Line(p1, p2), RIGHT, buff=0.08))
        a, b = axes.c2p(0.10, logi(0.10)), axes.c2p(0.24, logi(0.24))
        ang = np.arctan2(b[1] - a[1], b[0] - a[0])
        weak = text("weak inversion", size=20, color=MUTED).rotate(ang).move_to(axes.c2p(0.17, logi(0.17)) + rotate_vector(UP * 0.3, ang))
        side = VGroup(text("A real transistor\n(m = 1.2):", size=24, color=MUTED),
                      MathTex(rf"SS = {ss * 1e3:.0f}\ \text{{mV/decade}}", font_size=38, color=GATE)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.75, 1.7, 0])
        self.play(Create(tri), FadeIn(tri_l), FadeIn(side), FadeIn(weak))
        span = always_redraw(lambda: VGroup(
            text("decades between off and on", size=22, color=MUTED),
            display(f"{logi(vdd.get_value()) - logi(0):.1f}", size=54, color=INK),
        ).arrange(DOWN, buff=0.08).move_to([4.75, -0.4, 0]))
        self.play(FadeIn(span))

        self.slide(say(
            """
            Now do what Dennard scaling asks: shrink the supply voltage along with everything else,
            from 1 volt to 0.7. Look at the on current. It collapses, because we're barely above
            threshold any more. So we have to lower the threshold voltage too.
            """,
            """
            এবার Dennard scaling যা বলে তাই করেন: বাকি সবকিছুর সাথে supply voltage-ও কমান, 1 volt থেকে 0.7-এ। On
            current-টা দেখেন। ধসে পড়ে, কারণ আমরা এখন threshold-এর একটু উপরেই আছি। তাই threshold voltage-ও
            কমাইতে হবে।
            """,
        ))
        vdd_line = always_redraw(lambda: DashedLine(axes.c2p(vdd.get_value(), 0), axes.c2p(vdd.get_value(), 10), stroke_color=GOOD, stroke_width=2))
        vdd_lbl = always_redraw(lambda: MathTex("V_{DD}", color=GOOD, font_size=32).next_to(axes.c2p(vdd.get_value(), 10), UP, buff=0.05))
        self.play(FadeOut(tri), FadeOut(tri_l), FadeOut(weak),
                  Transform(title, heading("Dennard scaling: shrink the supply voltage too")),
                  FadeIn(vdd_line), FadeIn(vdd_lbl))
        self.play(vdd.animate.set_value(0.7), run_time=2)

        self.slide(say(
            """
            And here's the trap. Each time we lower the threshold by one swing, about 70 millivolts,
            the off current goes up about ten times. Lower it by three swings and the switch leaks
            about a thousand times more when it's supposed to be off. Billions of transistors, all leaking.
            So the threshold voltage stopped falling, and so did the supply voltage: it has sat near
            one volt, give or take, since the mid-2000s.
            """,
            """
            আর এইখানেই ফাঁদ। প্রতিবার threshold এক swing কমাইলে, মানে প্রায় 70 millivolt, off current প্রায় দশ গুণ
            বাড়ে। তিন swing কমাইলে switch-টা off থাকার কথা যখন, তখন প্রায় হাজার গুণ বেশি leak করে। Billion billion transistor,
            সবগুলা leak করতেছে। তাই threshold voltage কমা বন্ধ হইলো, supply voltage-ও: 2000-এর দশকের মাঝামাঝি থেকে
            এইটা মোটামুটি এক volt-এর আশেপাশেই আটকে আছে।
            """,
        ))
        def leak_ratio():
            """The off current against the starting one, read off the plotted model."""
            r = 10 ** (logi(0) - log10(phys.drain_current(0, 0.40, 300, m, I_SPEC)) - LOG0)
            return float(f"{r:.2g}")

        leak = always_redraw(lambda: VGroup(
            text("leakage", size=22, color=DRAIN),
            display(f"≈ ×{leak_ratio():,.0f}", size=54, color=DRAIN),
        ).arrange(DOWN, buff=0.08).move_to([4.75, -2.4, 0]))
        self.play(FadeIn(leak))
        for k in (1, 2, 3):
            self.play(vt.animate.set_value(0.40 - k * ss), run_time=1.6)
            self.wait(0.4)
        self.play(Transform(title, heading(f"Every {ss * 1e3:.0f} mV off V_T: about ten times the leakage")))

    # --- the power wall ----------------------------------------------------------------------
    def power_wall(self):
        self.slide(say(
            """
            You can see it in the clock speed. For thirty years it rose about a thousandfold. Then
            around 2004 base clocks reached three to four gigahertz and stopped climbing. Turbo modes
            reach higher today, about 6 gigahertz at the very top, but the steady climb was over. With the voltage stuck,
            Dennard's bargain broke: shrinking no longer kept power density constant, and faster
            clocks meant more heat than a chip could get rid of. So the industry went sideways, to
            more cores instead of faster ones.
            """,
            """
            Clock speed-এ এইটা পরিষ্কার দেখা যায়। তিরিশ বছর ধরে এইটা প্রায় হাজার গুণ বাড়ছে। তারপর 2004-এর দিকে
            base clock তিন থেকে চার gigahertz-এ পৌঁছায়ে আর উঠল না। আজ turbo mode আরও উপরে যায়, সবচেয়ে উপরে প্রায় 6
            gigahertz, কিন্তু একটানা বাড়াটা শেষ। Voltage আটকে যাওয়ায় Dennard-এর চুক্তি ভেঙে গেল: ছোট করলে আর
            power density একই থাকে না, আর clock বাড়াইলে এত heat হয় যে chip সেটা বের করতে পারে না। তাই industry পাশে
            সরে গেল: দ্রুত core-এর বদলে বেশি core।
            """,
        ))
        self.clear()
        # Base clocks of Intel desktop flagships (approximate), MHz.
        clocks = [(1971, 0.74), (1978, 5), (1982, 6), (1985, 16), (1989, 25), (1993, 60), (1997, 300),
                  (2000, 1500), (2004, 3800), (2006, 2930), (2011, 3400), (2017, 4200), (2020, 3700)]
        axes = Axes(x_range=[1970, 2022, 10], y_range=[0, 5, 1], x_length=7.4, y_length=4.8, tips=False,
                    axis_config={"stroke_color": MUTED, "stroke_width": 2, "tick_size": 0.05}).move_to([-0.9, -0.4, 0])
        # The y axis is log10(MHz) + 1, so 0.74 MHz (the 4004) sits above the x axis.
        axes.x_axis.add_labels({y: text(str(y), size=16, color=MUTED) for y in range(1970, 2021, 10)}, font_size=16)
        axes.y_axis.add_labels({1: text("1 MHz", size=16, color=MUTED), 2: text("10 MHz", size=16, color=MUTED),
                                3: text("100 MHz", size=16, color=MUTED), 4: text("1 GHz", size=16, color=MUTED),
                                5: text("10 GHz", size=16, color=MUTED)}, font_size=16)
        title = heading("Clock speed stopped climbing")
        dots = VGroup(*[Dot(axes.c2p(y, log10(f) + 1), color=THERMAL, radius=0.07) for y, f in clocks])
        trail = VMobject(stroke_color=THERMAL, stroke_width=3).set_points_as_corners([d.get_center() for d in dots])
        cap = text("Intel desktop processors, base clock (approximate)", size=18, color=MUTED).next_to(axes, DOWN, buff=0.35)
        self.play(FadeIn(title), Create(axes), FadeIn(cap))
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in dots[:9]], lag_ratio=0.25), Create(trail), run_time=3)
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in dots[9:]], lag_ratio=0.25), run_time=1.5)
        x0, x1 = axes.c2p(2004, 1)[0], axes.c2p(2022, 1)[0]
        y0, y1 = axes.c2p(1970, log10(2500) + 1)[1], axes.c2p(1970, log10(4500) + 1)[1]
        band = Rectangle(width=x1 - x0, height=y1 - y0, fill_color=DRAIN, fill_opacity=0.15, stroke_width=0).move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])
        flat = text("base clocks ~3–4 GHz since 2004", size=22, color=DRAIN, weight="SEMIBOLD").next_to(band, UP, buff=0.12)
        self.play(FadeIn(band), FadeIn(flat))
        side = VGroup(
            text("V_DD stuck near 1 V", size=22),
            text("→ power density rises", size=22),
            text("→ the clock can't", size=22),
            text("→ multicore instead", size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([5.0, 0.2, 0])
        self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.1) for s in side], lag_ratio=0.3))

        self.slide(say(
            """
            Intel saw this coming. In his keynote at the ISSCC conference in 2001, Pat Gelsinger
            showed a chart: if processors kept going the way they were, their power density would
            climb past a hot plate toward a nuclear reactor, then a rocket nozzle, then the surface
            of the Sun. None of that happened, because the industry changed course. But it shows
            how hard the wall was.
            """,
            """
            Intel এইটা আগেই দেখছিল। 2001-এ ISSCC conference-এর keynote-এ Pat Gelsinger একটা chart দেখান: processor যদি
            এভাবেই চলতে থাকে, তাহলে এদের power density hot plate পার হয়ে যাবে nuclear reactor-এর দিকে, তারপর rocket
            nozzle, তারপর সূর্যের surface। এগুলার কিছুই হয় নাই, কারণ industry রাস্তা বদলাইছে। কিন্তু দেয়ালটা কত শক্ত ছিল, এইটা তাই
            দেখায়।
            """,
        ))
        self.clear()
        title = heading("Where the heat was heading")
        rungs = ["hot plate", "nuclear reactor", "rocket nozzle", "surface of the Sun"]
        ladder = VGroup()
        for i, thing in enumerate(rungs):
            bar = Rectangle(width=1.6 + 1.5 * i, height=0.55, fill_color=THERMAL, fill_opacity=0.25 + 0.2 * i, stroke_width=0)
            ladder.add(VGroup(bar, text(thing, size=30, weight="MEDIUM")).arrange(RIGHT, buff=0.35))
        ladder.arrange(UP, aligned_edge=LEFT, buff=0.35).move_to([0, -0.1, 0])
        quote = text("Pat Gelsinger (Intel), ISSCC 2001 keynote talk: where power density was heading if trends held.", size=18, color=MUTED).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(title), FadeIn(quote))
        for row in ladder:
            self.play(FadeIn(row, shift=UP * 0.15), run_time=0.7)

    # --- the gate oxide ----------------------------------------------------------------------
    def oxide(self):
        self.slide(say(
            """
            There was a second wall at the same time. To keep its grip on the channel, the gate
            oxide had been thinned to about 1.2 nanometres: about five layers of atoms. At that
            thickness electrons stop respecting it. An electron is a wave, and a wave leaks through
            a thin enough barrier: quantum tunnelling. The leak is exponential in the thickness:
            every fifth of a nanometre thinner, ten times more gate current.
            """,
            """
            একই সময়ে আরেকটা দেয়াল ছিল। Channel-এর উপর grip ধরে রাখতে gate oxide পাতলা করতে করতে প্রায় 1.2
            nanometre-এ নামানো হইছিল: মোটে পাঁচ layer atom। এত পাতলায় electron আর এইটারে মানে না। Electron একটা
            wave, আর যথেষ্ট পাতলা barrier হলে wave সেটা ভেদ করে চলে যায়: quantum tunnelling। এই leak thickness-এর সাথে
            exponential: প্রতি এক nanometre-এর পাঁচ ভাগের এক ভাগ পাতলা করলে gate current দশ গুণ।
            """,
        ))
        self.clear()
        title = heading("Meanwhile, the oxide was five atoms thick")
        gate = Rectangle(width=3.7, height=1.2, fill_color=GATE, fill_opacity=1, stroke_width=0).move_to([-3.55, 1.7, 0])
        gate_l = text("gate", size=24, color=BG, weight="SEMIBOLD").move_to(gate)
        atoms = VGroup(*[Circle(radius=0.12, fill_color=OXIDE_TEXT, fill_opacity=0.85, stroke_width=0).move_to(
            [-5.25 + col * 0.3 + (0.15 if row % 2 else 0), 0.95 - row * 0.27, 0]) for row in range(5) for col in range(12)])
        ox_l = text("SiO₂, 1.2 nm", size=24, color=OXIDE_TEXT).next_to(atoms, RIGHT, buff=0.3)
        si = Rectangle(width=3.7, height=1.4, fill_color=SILICON, fill_opacity=0.35, stroke_width=0).move_to([-3.55, -0.85, 0])
        si_l = text("channel", size=24, color=SILICON).move_to(si)
        self.play(FadeIn(title))
        self.play(FadeIn(gate), FadeIn(gate_l), FadeIn(si), FadeIn(si_l))
        self.play(LaggedStart(*[GrowFromCenter(a) for a in atoms], lag_ratio=0.01), FadeIn(ox_l), run_time=1.5)
        y_top, y_bot = atoms.get_top()[1], atoms.get_bottom()[1]
        wave_x = -2.3

        def psi(y):
            if y < y_bot:
                return 0.45 * np.sin(14 * y)
            if y <= y_top:
                return 0.45 * np.exp(-(y - y_bot) * 2.2) * np.sin(14 * y_bot)
            return 0.45 * np.exp(-(y_top - y_bot) * 2.2) * np.sin(14 * y)

        wave = ParametricFunction(lambda y: [wave_x + psi(y), y, 0], t_range=[-1.5, 2.25], stroke_color=ELECTRON, stroke_width=4)
        wave_l = text("electron wave", size=22, color=ELECTRON).move_to([-0.6, -1.0, 0])
        self.play(Create(wave), FadeIn(wave_l), run_time=1.5)
        e1 = eq(r"J_G", r"\;\propto\;", r"\exp\!\left(-2\,", r"t_{ox}", r"\,\frac{\sqrt{2m^*\Phi_B}}{\hbar}\right)", size=40)
        e1[0].set_color(DRAIN)
        e1[3].set_color(OXIDE_TEXT)
        per = phys.thickness_per_decade_nm()
        e2 = text(f"≈ 10× more leakage\nfor every {per:.1f} nm thinner", size=28, color=DRAIN, weight="SEMIBOLD")
        e3 = text("with m* ≈ 0.4 m₀ and Φ_B ≈ 3.1 eV (Si/SiO₂)", size=20, color=MUTED)
        col = VGroup(e1, e2, e3, model_tag()).arrange(DOWN, buff=0.35).move_to([3.7, 0.5, 0])
        self.play(Write(e1))
        self.play(FadeIn(e2), FadeIn(e3), FadeIn(col[3]))

        self.slide(say(
            """
            The fix was a new material. A capacitor's strength is the permittivity, k, over the
            thickness. Hafnium oxide has a k around 20, five times silicon dioxide's. So about 6
            nanometres of hafnium oxide grips the channel like 1.2 nanometres of SiO2, in an ideal
            single layer, and it's far too thick to tunnel through easily. Real stacks keep a thin
            layer of SiO2 underneath, which adds to the EOT. Intel shipped hafnium-based high-k with
            metal gates at 45 nanometres in 2007. That wall, we got around: high-k cut the gate's
            leakage. It did nothing about the drain.
            """,
            """
            Fix-টা ছিল নতুন একটা material। Capacitor কতটা শক্তিশালী সেটা হইলো permittivity, k, বাই thickness।
            Hafnium oxide-এর k প্রায় 20, silicon dioxide-এর পাঁচ গুণ। তাই প্রায় 6 nanometre hafnium oxide channel-রে
            ততটাই ধরে যতটা 1.2 nanometre SiO2, একটা ideal single layer হিসাবে, আর এত পুরু যে tunnelling সহজে হয় না।
            আসল stack-এ নিচে SiO2-এর একটা পাতলা layer থাকে, যেটা EOT-এ যোগ হয়। Intel 2007-এ 45 nanometre-এ
            hafnium-based high-k আর metal gate ship করে। এই দেয়ালটা আমরা পার হইছি: high-k gate-এর leakage কমাইছে।
            Drain-এর ব্যাপারে কিছুই করে নাই।
            """,
        ))
        self.clear()
        title = heading("The fix: a thicker insulator that acts thinner")
        t_hk = phys.physical_thickness_nm(1.2, 20)
        u = 0.32  # scene units per nm, the same for both stacks

        def stack(x, t, color, name):
            ch = Rectangle(width=2.4, height=0.9, fill_color=SILICON, fill_opacity=0.35, stroke_width=0).move_to([x, -2.0, 0])
            ox = Rectangle(width=2.4, height=t * u, fill_color=color, fill_opacity=0.9, stroke_width=0).next_to(ch, UP, buff=0)
            g = Rectangle(width=2.4, height=0.9, fill_color=GATE, fill_opacity=1, stroke_width=0).next_to(ox, UP, buff=0)
            return VGroup(ch, ox, g, text(name, size=24, color=color).next_to(g, UP, buff=0.2))

        sio2 = stack(-4.4, 1.2, OXIDE_TEXT, "SiO₂  1.2 nm")
        hfo2 = stack(-1.4, t_hk, HIGHK, f"HfO₂  {t_hk:.1f} nm")
        same = text("same grip on the channel", size=22, color=MUTED).next_to(VGroup(sio2, hfo2), DOWN, buff=0.25)
        f1 = eq(r"C_{ox}", r"=", r"\frac{\varepsilon_0\,k}{t}", size=46)
        f1[0].set_color(OXIDE_TEXT)
        f2 = eq(r"\text{EOT}", r"\approx", r"t_{IL} + t_{hk}\,\frac{3.9}{k}", size=46)
        f3 = text(f"k ≈ 20: {t_hk:.1f} nm of HfO₂ acts\nlike 1.2 nm of SiO₂ (ideal, t_IL = 0)", size=24)
        f4 = text("Far less tunnelling.\nIntel 45 nm, 2007.", size=26, color=GOOD, weight="SEMIBOLD")
        VGroup(f1, f2, f3, f4).arrange(DOWN, buff=0.4).move_to([3.6, 0.0, 0])
        self.play(FadeIn(title), FadeIn(sio2))
        self.play(FadeIn(hfo2), FadeIn(same))
        self.play(Write(f1))
        self.play(Write(f2))
        self.play(FadeIn(f3))
        self.play(FadeIn(f4))

    # --- cliffhanger -------------------------------------------------------------------------
    def cliffhanger(self):
        self.slide(say(
            """
            So that's the state of things in the mid-2000s. We fixed the oxide. We could not fix
            Boltzmann: 60 millivolts per decade is a law of nature for this kind of switch. The only
            thing left to fight for is m, the gate's grip, getting it as close to one as we can. And
            as transistors kept getting shorter, an old problem became the main one: the drain
            started pulling the hill down by itself. That's the next chapter. But first, try it
            yourself.
            """,
            """
            তো 2000-এর দশকের মাঝামাঝি অবস্থা এই। Oxide আমরা ঠিক করছি। Boltzmann-রে ঠিক করতে পারি নাই: এই ধরনের switch-এর
            জন্য প্রতি decade-এ 60 millivolt প্রকৃতির law। লড়াই করার মতো বাকি থাকল শুধু m, gate-এর grip, যতটা সম্ভব এক-এর
            কাছে আনা। আর transistor যত ছোট হইতে থাকল, একটা পুরান সমস্যা হয়ে উঠল প্রধান সমস্যা: drain নিজেই hill-টারে টেনে
            নামাইতে শুরু করল। সেইটা পরের chapter। কিন্তু তার আগে, নিজে একবার try করে দেখেন।
            """,
        ))
        self.clear()
        a = text("We fixed the oxide.", size=46, weight="SEMIBOLD")
        b = text("We couldn't fix Boltzmann.", size=46, weight="SEMIBOLD", color=GATE)
        c = text("And the channel got so short that the drain started to fight the gate.", size=26, color=DRAIN)
        VGroup(a, b, c).arrange(DOWN, buff=0.3).to_edge(UP, buff=0.5)
        self.play(FadeIn(a))
        self.play(FadeIn(b))
        self.b.set_value(0.30)
        self.d.set_value(0.25)
        bar = Barrier(self.b, self.d, n=120, origin=(0.0, -1.4), scale=6.0, seed=11)
        self.play(FadeIn(bar))
        bar.start()
        self.wait(1)
        self.play(FadeIn(c), self.d.animate.set_value(0.38), self.b.animate.set_value(0.15), run_time=3)
        self.wait(1.5)
        bar.stop()

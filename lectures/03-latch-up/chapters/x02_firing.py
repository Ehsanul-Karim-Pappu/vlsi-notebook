"""Lecture 3 · X2 · How it fires, and why it stays on.

What injects the current; the feedback loop, step by step, on the equivalent circuit; the gain
condition; and the S-shaped I–V with its trigger and holding points against the supply.
"""

import sys
from pathlib import Path

LECTURE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(LECTURE.parents[1]), str(LECTURE)]

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403
from manim_slides import Slide  # noqa: E402

import physics as ph  # noqa: E402
from common import NPLUS, PPLUS, card_box, chapter_title, scr_circuit, toy_tag  # noqa: E402
from kit.style import *  # noqa: E402,F403


class X02Firing(Chapter, Slide):
    def construct(self):
        self.card()
        self.triggers()
        self.loop()
        self.self_sustaining()
        self.s_curve()
        self.summary()

    def card(self):
        self.slide(say(
            """
            Chapter two: how it fires, and why it stays on. The thyristor is always there, but
            it's normally off. Something has to kick it, and then a feedback loop does the rest.
            """,
            """
            Chapter two: এইটা কিভাবে চালু হয়, আর কেন চালু থাকে। Thyristor সবসময়ই আছে, কিন্তু সাধারণত off থাকে। কিছু একটা
            এরে ধাক্কা দিতে হয়, তারপর একটা feedback loop বাকিটা করে।
            """,
        ))
        self.card_group = chapter_title(2, "How it fires, and why it stays on", "A kick, a loop, a holding point")
        self.play(FadeIn(self.card_group, shift=UP * 0.2), run_time=1.2)

    def triggers(self):
        self.slide(say(
            """
            What kicks it? Anything that pushes current into the substrate or the well. The
            classic is an I/O pin. Drive a pin below ground, and the N+ drain of the output NMOS
            becomes a forward-biased diode that sprays electrons into the substrate. Drive it above
            VDD, and the P+ drain of the output PMOS sprays holes into the well. Then there are the
            supplies: a glitch, a fast power-up that charges the well capacitance, or one supply
            coming up before another. And, rarely in the field but always in the qualification
            test, deliberately forced current. All of these are injectors, and we'll keep coming
            back to that word.
            """,
            """
            ধাক্কাটা কে দেয়? যেকোনো কিছু যেটা substrate বা well-এ current ঠেলে দেয়। Classic উদাহরণ একটা I/O pin। একটা pin
            ground-এর নিচে টানেন, আর output NMOS-এর N+ drain একটা forward-biased diode হয়ে substrate-এ electron ছিটায়।
            VDD-এর উপরে তোলেন, আর output PMOS-এর P+ drain well-এ hole ছিটায়। তারপর supply-গুলা: একটা glitch, একটা দ্রুত
            power-up যেটা well-এর capacitance charge করে, বা একটা supply আরেকটার আগে উঠে আসা। আর, field-এ বিরল কিন্তু
            qualification test-এ সবসময়, ইচ্ছা করে ঠেলে দেওয়া current। এগুলা সবই injector, আর এই শব্দটায় আমরা বারবার ফিরব।
            """,
        ))
        self.play(FadeOut(self.card_group))
        title = heading("What kicks it: injectors")
        cards = VGroup(
            card_box("Pin below VSS", [text("the output NMOS's N+ drain\nforward-biases: electrons\ninto the substrate", size=20, color=INK)],
                     width=5.4, height=2.2, head_size=22, head_color=NPLUS),
            card_box("Pin above VDD", [text("the output PMOS's P+ drain\nforward-biases: holes\ninto the well", size=20, color=INK)],
                     width=5.4, height=2.2, head_size=22, head_color=PPLUS),
            card_box("Supply events", [text("a glitch, a fast ramp\ncharging the wells, one\nsupply up before another", size=20, color=INK)],
                     width=5.4, height=2.2, head_size=22),
            card_box("The test", [text("JESD78 forces current into\nevery pin and overdrives\nevery supply, on purpose", size=20, color=INK)],
                     width=5.4, height=2.2, head_size=22, head_color=MUTED),
        ).arrange_in_grid(rows=2, cols=2, buff=0.3).move_to(DOWN * 0.3)
        self.play(FadeIn(title))
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in cards], lag_ratio=0.25), run_time=2.0)

    def loop(self):
        self.slide(say(
            """
            Now watch the loop. One: an injector pushes current into the substrate node, and it
            has to flow out through R_sub to the tap. That raises the substrate under the nMOS
            source. Two: once that drop reaches about 0.65 volts, the NPN's base-emitter junction
            turns on. Three: the NPN's collector current comes out of the well, through R_well,
            pulling the well down from VDD. Four: once that drop reaches 0.65 volts, the PNP turns
            on, and its collector current goes straight into the substrate node. Back to step one,
            but now the current comes from inside the loop.
            """,
            """
            এবার loop-টা দেখেন। এক: একটা injector substrate node-এ current ঠেলে দেয়, আর সেইটারে R_sub দিয়া tap-এ বের হইতে
            হয়। এতে nMOS source-এর নিচের substrate উপরে উঠে। দুই: ওই drop প্রায় 0.65 volt-এ পৌঁছালে NPN-এর base-emitter
            junction on হয়। তিন: NPN-এর collector current well থেকে আসে, R_well দিয়া, well-রে VDD থেকে নিচে টানে। চার: ওই drop
            0.65 volt-এ পৌঁছালে PNP on হয়, আর এর collector current সোজা substrate node-এ যায়। আবার ধাপ এক-এ, কিন্তু এখন
            current আসে loop-এর ভিতর থেকেই।
            """,
        ))
        self.clear()
        title = heading("The loop, step by step")
        scr = scr_circuit(center=(-3.4, -0.3), scale=1.0)
        p, nodes = scr.parts, scr.nodes
        self.play(FadeIn(title), FadeIn(scr))
        S, W = nodes["S"], nodes["W"]
        inj = Arrow(S + LEFT * 0.0 + DOWN * 1.1 + RIGHT * 0.9, S + RIGHT * 0.05 + DOWN * 0.05, buff=0, stroke_color=GATE,
                    stroke_width=6)
        inj_l = text("injected", size=18, color=GATE).next_to(inj.get_start(), DOWN, buff=0.05)
        steps = VGroup(
            text("1  current into S flows out through R_sub", size=22),
            text("2  S rises to 0.65 V: the NPN turns on", size=22),
            text("3  its collector pulls W down through R_well", size=22),
            text("4  W is 0.65 V below VDD: the PNP turns on,", size=22),
            text("   and its collector feeds S", size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.2, 0.2, 0])
        self.play(GrowArrow(inj), FadeIn(inj_l), FadeIn(steps[0]))
        self.play(p["r_sub"].animate.set_color(GATE), FadeIn(steps[1]))
        self.play(p["npn"].animate.set_color(NPLUS).set_stroke(width=6), p["s_wire"].animate.set_color(GATE))
        self.play(p["w_wire"].animate.set_color(NPLUS), p["r_well"].animate.set_color(NPLUS), FadeIn(steps[2]))
        self.play(p["pnp"].animate.set_color(PPLUS).set_stroke(width=6), FadeIn(steps[3]), FadeIn(steps[4]))
        ring = Arc(radius=0.75, start_angle=PI * 0.75, angle=-1.8 * PI, color=DRAIN, stroke_width=6).move_to(
            (S + W) / 2 + np.array([0.0, 0.0, 0])).add_tip(tip_length=0.25)
        self.play(Create(ring), run_time=1.2)
        self.scr, self.inj, self.ring, self.steps, self.title = scr, VGroup(inj, inj_l), ring, steps, title

    def self_sustaining(self):
        self.slide(say(
            """
            Here's the trap. Once both transistors are on, each one supplies the other's base
            current. Take the injector away and nothing changes: the loop feeds itself, as long as
            the gains around the loop multiply to more than one. The NPN's gain times the PNP's
            gain, greater than one, is the simplified condition you'll see in textbooks; the
            resistors steal some base current, so the real threshold is a bit higher. And the
            current is limited only by the resistance of the silicon and the metal: hundreds of
            milliamps through one small spot.
            """,
            """
            ফাঁদটা এইখানে। দুইটা transistor একবার on হইলে, প্রত্যেকটা অন্যটার base current যোগায়। Injector সরিয়ে নেন, কিছুই
            বদলায় না: loop নিজেরে খাওয়ায়, যতক্ষণ loop ঘুরে gain-গুলা গুণ করলে একের বেশি হয়। NPN-এর gain গুণ PNP-এর gain,
            একের বেশি, এইটা textbook-এ দেখা সরল শর্ত; resistor-গুলা কিছু base current চুরি করে, তাই আসল সীমা একটু উপরে। আর
            current-এর সীমা শুধু silicon আর metal-এর resistance: একটা ছোট জায়গা দিয়া কয়েকশ milliamp।
            """,
        ))
        self.play(FadeOut(self.inj), Transform(self.title, heading("Take the kick away: it keeps itself on")))
        cond = VGroup(text("β_npn · β_pnp > 1", size=40, color=GATE, weight="SEMIBOLD"),
                      text("the simplified condition: the resistors\nsteal some base current, so the real\nthreshold is a little higher",
                           size=20, color=MUTED)).arrange(DOWN, buff=0.3)
        cond.move_to(self.steps)
        self.play(FadeOut(self.steps), FadeIn(cond))
        self.play(Rotate(self.ring, angle=-2 * PI, about_point=self.ring.get_center()), run_time=2.0)
        self.cond = cond

    def s_curve(self):
        self.slide(say(
            """
            Seen from the supply, the thyristor has an S-shaped curve. Below the trigger point it
            blocks: almost no current. Kick it past the trigger and it snaps back, the voltage
            falls while the current rises, until it reaches the holding point: the lowest voltage
            at which the loop can still keep itself on. Beyond that, it's a low resistance. Now
            draw the supply as a line. At 3.3 volts, the line crosses the on branch: there's a
            stable latched state, and the chip will sit in it. At 0.8 volts, the supply is below
            the holding voltage: the loop can fire, but it can't hold, and it lets go. That's one
            reason low-voltage core logic is less exposed than the I/O ring.
            """,
            """
            Supply থেকে দেখলে, thyristor-এর একটা S-আকারের curve আছে। Trigger point-এর নিচে এইটা আটকায়: প্রায় কোনো current
            নাই। Trigger পার করে ধাক্কা দেন, এইটা snap back করে, current বাড়ার সাথে voltage কমে, holding point পর্যন্ত: সবচেয়ে
            কম voltage যেখানে loop এখনো নিজেরে on রাখতে পারে। এর পরে, এইটা একটা কম resistance। এবার supply-রে একটা রেখা
            হিসাবে আঁকেন। 3.3 volt-এ রেখাটা on branch-রে কাটে: একটা stable latched অবস্থা আছে, আর chip সেখানে বসে থাকবে। 0.8
            volt-এ supply holding voltage-এর নিচে: loop চালু হইতে পারে, কিন্তু ধরে রাখতে পারে না, ছেড়ে দেয়। এইটা একটা কারণ
            কেন কম voltage-এর core logic I/O ring-এর চেয়ে কম ঝুঁকিতে।
            """,
        ))
        self.clear()
        title = heading("Seen from the supply: the S-curve")
        d_sub, d_well, sp = 10.0, 10.0, 2.0
        pts = ph.s_curve(d_sub, d_well, sp, v_trig=6.0, r_on=8.0, i_max=400.0)
        lg = lambda i: np.log10(max(i, 1e-3)) + 3  # log10(mA) + 3, so the axis sits at 1 µA  # noqa: E731
        ax = Axes(x_range=[0, 7, 1], y_range=[0, 6, 1], x_length=7.6, y_length=4.6,
                  axis_config={"color": MUTED, "include_ticks": False}).move_to([-1.8, -0.4, 0])
        xl = text("voltage across it (V)", size=20, color=MUTED).next_to(ax, DOWN, buff=0.15)
        yl = text("current (log scale)", size=20, color=MUTED).rotate(PI / 2).next_to(ax, LEFT, buff=0.55)
        ticks = VGroup(*[text(s_, size=16, color=MUTED).next_to(ax.c2p(0, y), LEFT, buff=0.1)
                         for s_, y in (("0.01 mA", 1), ("1 mA", 3), ("100 mA", 5))])
        curve = VMobject(stroke_color=INK, stroke_width=5).set_points_as_corners([ax.c2p(v, lg(i)) for v, i in pts])
        v_h, i_h = ph.holding_voltage(sp), ph.holding_current(d_sub, d_well)
        trig = Dot(ax.c2p(6.0, lg(pts[len(pts) // 3][1])), color=GATE, radius=0.09)
        trig_l = text("trigger", size=20, color=GATE).next_to(trig, UP, buff=0.12)
        hold = Dot(ax.c2p(v_h, lg(i_h)), color=DRAIN, radius=0.09)
        hold_l = text(f"holding: {v_h:.1f} V", size=20, color=DRAIN).next_to(hold, DR, buff=0.12)
        hi = DashedLine(ax.c2p(3.3, 0), ax.c2p(3.3, 6), stroke_color=PPLUS, stroke_width=3)
        lo = DashedLine(ax.c2p(0.8, 0), ax.c2p(0.8, 6), stroke_color=NPLUS, stroke_width=3)
        hi_l = text("3.3 V I/O", size=20, color=PPLUS).next_to(hi, UP, buff=0.08)
        lo_l = text("0.8 V core", size=20, color=NPLUS).next_to(lo, UP, buff=0.08)
        i_on = (3.3 - v_h) / 8.0 * 1e3
        op = Dot(ax.c2p(3.3, lg(i_on)), color=PPLUS, radius=0.1)
        op_l = text(f"latched: ≈ {i_on:.0f} mA", size=20, color=PPLUS).next_to(op, DR, buff=0.12)
        hi_l = VGroup(hi_l, op, op_l)
        side = VGroup(text("supply above holding:", size=22, color=PPLUS, weight="SEMIBOLD"),
                      text("a stable latched state", size=22, color=INK),
                      text("supply below holding:", size=22, color=NPLUS, weight="SEMIBOLD"),
                      text("it fires, then lets go", size=22, color=INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        side[2].shift(DOWN * 0.25)
        side[3].shift(DOWN * 0.25)
        side.move_to([4.6, 0.3, 0])
        tag = toy_tag().to_corner(DR, buff=0.3)
        self.play(FadeIn(title), Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(ticks), FadeIn(tag))
        self.play(Create(curve), run_time=2.5)
        self.play(FadeIn(trig), FadeIn(trig_l), FadeIn(hold), FadeIn(hold_l))
        self.play(Create(hi), FadeIn(hi_l), FadeIn(side[:2]))
        self.play(Create(lo), FadeIn(lo_l), FadeIn(side[2:]))

    def summary(self):
        self.slide(say(
            """
            So, two conditions for a latch-up you'll actually see. It fires when an injected
            current develops about 0.65 volts across R_sub or R_well. And it stays on while the
            supply is above the holding voltage and can deliver the holding current. Every layout
            rule we'll meet attacks one of those: it keeps the drops small, the gains low, the
            injected current away, or the holding point high. Before we go there, try it yourself.
            """,
            """
            তাহলে, সত্যিই দেখা যায় এমন latch-up-এর দুইটা শর্ত। এইটা চালু হয় যখন একটা injected current R_sub বা R_well-এর
            উপর প্রায় 0.65 volt তৈরি করে। আর on থাকে যতক্ষণ supply holding voltage-এর উপরে আর holding current দিতে পারে।
            আমরা যত layout rule দেখব, প্রত্যেকটা এর একটারে আক্রমণ করে: drop ছোট রাখে, gain কম রাখে, injected current দূরে
            রাখে, বা holding point উঁচু রাখে। সেখানে যাওয়ার আগে, নিজে একবার চেষ্টা করেন।
            """,
        ))
        self.clear()
        title = heading("Two conditions")
        a = card_box("It fires when…", [text("an injected current makes\n≈ 0.65 V across R_sub or R_well", size=24, color=INK),
                                        text("and β_npn · β_pnp > 1", size=24, color=INK)], width=5.6, height=3.2)
        b = card_box("It stays on while…", [text("VDD > the holding voltage", size=24, color=INK),
                                            text("and the supply can deliver\nthe holding current", size=24, color=INK)],
                     width=5.6, height=3.2, head_color=DRAIN)
        VGroup(a, b).arrange(RIGHT, buff=0.6).move_to(UP * 0.1)
        foot = text("every LUP rule attacks one of these", size=26, color=GATE).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(title), FadeIn(a, shift=UP * 0.15))
        self.play(FadeIn(b, shift=UP * 0.15))
        self.play(FadeIn(foot))

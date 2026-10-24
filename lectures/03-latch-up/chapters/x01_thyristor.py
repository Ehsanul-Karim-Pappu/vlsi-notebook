"""Lecture 3 · X1 · The thyristor in every inverter.

The CMOS inverter in silicon, built layer by layer; the vertical PNP and the lateral NPN drawn over
the silicon they come from; the well and substrate resistances; the four layers as a thyristor;
and the equivalent circuit, an SCR from VDD to VSS.
"""

import sys
from pathlib import Path

LECTURE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(LECTURE.parents[1]), str(LECTURE)]

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403
from manim_slides import Slide  # noqa: E402

from common import NPLUS, PPLUS, CrossSection, bjt, box, chapter_title, resistor, scr_circuit, terminals  # noqa: E402
from kit.style import *  # noqa: E402,F403


def wire(*pts, color=INK, width=3):
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners([np.array(p, float) for p in pts])


class X01Thyristor(Chapter, Slide):
    def construct(self):
        self.card()
        self.build()
        self.pnp()
        self.npn()
        self.resistances()
        self.four_layers()
        self.circuit()

    def card(self):
        self.slide(say(
            """
            Chapter one: the thyristor in every inverter. Latch-up isn't a defect, and it isn't
            rare bad luck. It's built into bulk CMOS: every time you put an nMOS and a pMOS near
            each other, you also draw two bipolar transistors you never asked for.
            """,
            """
            Chapter one: প্রত্যেকটা inverter-এ একটা thyristor। Latch-up কোনো defect না, আর বিরল দুর্ভাগ্যও না। এইটা bulk
            CMOS-এর ভিতরেই বানানো: যখনই একটা nMOS আর একটা pMOS একে অন্যের কাছে বসান, আপনি এমন দুইটা bipolar transistor-ও
            আঁকেন যেগুলা আপনি কখনো চান নাই।
            """,
        ))
        self.card_group = chapter_title(1, "The thyristor in every inverter", "Four layers, two bipolars, one loop")
        self.play(FadeIn(self.card_group, shift=UP * 0.2), run_time=1.2)

    def build(self):
        self.slide(say(
            """
            Here's the inverter, cut open. A p-type substrate, with the nMOS sitting directly in
            it: two N+ diffusions, the source tied to VSS and the drain to the output. Beside it,
            an n-well, with the pMOS inside: two P+ diffusions, the source tied to VDD. And two
            taps: a P+ tap that ties the substrate to VSS, and an N+ tap that ties the well to VDD.
            Those taps are what the rules are about, so keep an eye on them.
            """,
            """
            এই যে inverter-টা, কেটে খোলা। একটা p-type substrate, nMOS সরাসরি এর ভিতরে বসা: দুইটা N+ diffusion, source VSS-এ
            আর drain output-এ বাঁধা। পাশে একটা n-well, ভিতরে pMOS: দুইটা P+ diffusion, source VDD-তে বাঁধা। আর দুইটা tap:
            একটা P+ tap যেটা substrate-রে VSS-এ বাঁধে, আর একটা N+ tap যেটা well-রে VDD-তে বাঁধে। Rule-গুলা ওই tap-গুলা নিয়াই,
            তাই এদের উপর চোখ রাখেন।
            """,
        ))
        self.play(FadeOut(self.card_group))
        title = heading("The inverter, cut open")
        xs = CrossSection(top=0.3, depth=3.6, well=(0.3, 5.7), well_depth=2.2, p_drn=1.3, p_src=3.0, well_tap=5.0)
        self.play(FadeIn(title), FadeIn(xs.sub))
        self.play(FadeIn(xs.well), FadeIn(xs.tags))
        self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.1) for d in xs.diffs.values()], lag_ratio=0.15), FadeIn(xs.gates))
        self.play(FadeIn(xs.wires))
        taps = VGroup(SurroundingRectangle(xs.diffs["sub_tap"], color=GATE, buff=0.06),
                      SurroundingRectangle(xs.diffs["well_tap"], color=GATE, buff=0.06))
        tl = VGroup(text("substrate tap", size=18, color=GATE).next_to(taps[0], DOWN, buff=0.12),
                    text("well tap", size=18, color=GATE).next_to(taps[1], DOWN, buff=0.12))
        self.play(Create(taps), FadeIn(tl))
        self.xs, self.title, self.tap_marks = xs, title, VGroup(taps, tl)

    def pnp(self):
        self.slide(say(
            """
            Now read the layers under the pMOS source, top to bottom: P+, then the n-well, then
            the p-substrate. P, N, P. That's a bipolar transistor, a PNP, standing on its end.
            Its emitter is the pMOS source at VDD, its base is the well, and its collector is the
            whole substrate. A vertical PNP.
            """,
            """
            এবার pMOS source-এর নিচের layer-গুলা পড়েন, উপর থেকে নিচে: P+, তারপর n-well, তারপর p-substrate। P, N, P। এইটা
            একটা bipolar transistor, একটা PNP, খাড়া দাঁড়ানো। এর emitter হইল VDD-তে থাকা pMOS source, base হইল well, আর
            collector হইল পুরা substrate। একটা vertical PNP।
            """,
        ))
        self.play(FadeOut(self.tap_marks))
        xs = self.xs
        x = xs.x["p_src"]
        top = xs.top
        sym = bjt("pnp", 0.85, PPLUS, 4).flip(UP).move_to([x, top - 1.25, 0])
        b, c, e = terminals(sym)
        leads = VGroup(wire(e, [e[0], top - 0.38, 0], color=PPLUS), wire(c, [c[0], top - 2.7, 0], color=PPLUS))
        name = text("vertical PNP", size=26, color=PPLUS, weight="SEMIBOLD").move_to([3.2, 2.4, 0])
        lbl = text("emitter: P+ source · base: n-well · collector: substrate", size=17, color=INK).next_to(name, DOWN, buff=0.1)
        self.play(Transform(self.title, heading("A PNP, standing on its end")))
        self.play(Create(sym), Create(leads), FadeIn(name))
        self.play(FadeIn(lbl))
        self.pnp_sym, self.pnp_bits = sym, VGroup(leads, lbl, name)

    def npn(self):
        self.slide(say(
            """
            And sideways from the nMOS source: N+, then the p-substrate, then the n-well. N, P, N.
            A second bipolar, an NPN, lying on its side. Its emitter is the nMOS source at VSS,
            its base is the substrate between the source and the well, and its collector is the
            well. A lateral NPN. Notice what the two share: the PNP's collector is the NPN's
            base, and the NPN's collector is the PNP's base.
            """,
            """
            আর nMOS source থেকে পাশের দিকে: N+, তারপর p-substrate, তারপর n-well। N, P, N। দ্বিতীয় একটা bipolar, একটা NPN,
            কাত হয়ে শোয়া। এর emitter হইল VSS-এ থাকা nMOS source, base হইল source আর well-এর মাঝের substrate, আর collector
            হইল well। একটা lateral NPN। খেয়াল করেন এরা কী ভাগ করে: PNP-এর collector হইল NPN-এর base, আর NPN-এর collector
            হইল PNP-এর base।
            """,
        ))
        xs = self.xs
        top = xs.top
        sym = bjt("npn", 0.85, NPLUS, 4).rotate(-PI / 2).flip(RIGHT).move_to([-1.0, top - 1.55, 0])
        b, c, e = terminals(sym)
        src = xs.x["n_src"]
        leads = VGroup(wire(e, [src + 0.2, e[1], 0], [src + 0.2, top - 0.38, 0], color=NPLUS),
                       wire(c, [xs.x["well_left"] + 0.3, c[1], 0], color=NPLUS))
        name = text("lateral NPN", size=26, color=NPLUS, weight="SEMIBOLD").move_to([-3.2, 2.4, 0])
        lbl = text("emitter: N+ source · base: substrate · collector: n-well", size=17, color=INK).next_to(name, DOWN, buff=0.1)
        self.play(Transform(self.title, heading("An NPN, lying on its side")))
        self.play(Create(sym), Create(leads), FadeIn(name))
        self.play(FadeIn(lbl))
        self.npn_sym, self.npn_bits = sym, VGroup(leads, lbl, name)

    def resistances(self):
        self.slide(say(
            """
            Two more parts, and these are the ones layout controls. The PNP's base, the well,
            is connected to VDD only through the well tap, and the silicon in between has
            resistance: R_well. The NPN's base, the substrate, reaches VSS only through the
            substrate tap: R_sub. The farther the tap, the bigger the resistance. Hold on to these
            two resistors; most of the latch-up rules are about keeping them small.
            """,
            """
            আরও দুইটা অংশ, আর এগুলাই layout নিয়ন্ত্রণ করে। PNP-এর base, মানে well, VDD-তে যুক্ত শুধু well tap দিয়া, আর মাঝের
            silicon-এর resistance আছে: R_well। NPN-এর base, মানে substrate, VSS-এ পৌঁছায় শুধু substrate tap দিয়া: R_sub। Tap
            যত দূরে, resistance তত বড়। এই দুইটা resistor মনে রাখেন; বেশিরভাগ latch-up rule এদের ছোট রাখা নিয়া।
            """,
        ))
        xs = self.xs
        top = xs.top
        pb = terminals(self.pnp_sym)[0]
        nb = terminals(self.npn_sym)[0]
        wt, st = xs.x["well_tap"], xs.x["sub_tap"]
        rw = VGroup(resistor(pb + RIGHT * 0.05, [wt, pb[1], 0], GATE, 4, zigs=5, amp=0.09),
                    wire([wt, pb[1], 0], [wt, top - 0.38, 0], color=GATE, width=4))
        y_s = nb[1] - 0.25
        rs = VGroup(wire(nb, [nb[0], y_s, 0], color=GATE, width=4),
                    resistor([nb[0], y_s, 0], [st, y_s, 0], GATE, 4, zigs=9, amp=0.09),
                    wire([st, y_s, 0], [st, top - 0.38, 0], color=GATE, width=4))
        lw = text("R_well", size=22, color=GATE, weight="SEMIBOLD").move_to([(pb[0] + wt) / 2 + 0.1, pb[1] - 0.35, 0])
        ls = text("R_sub", size=22, color=GATE, weight="SEMIBOLD").move_to([(nb[0] + st) / 2, y_s - 0.32, 0])
        self.play(Transform(self.title, heading("…and the resistance to each tap")))
        self.play(Create(rw), FadeIn(lw))
        self.play(Create(rs), FadeIn(ls))
        self.res = VGroup(rw, rs, lw, ls)

    def four_layers(self):
        self.slide(say(
            """
            Put the two bipolars together and you have four layers in a row, from VDD to VSS:
            the P+ source, the n-well, the p-substrate, the N+ source. P, N, P, N. That's a
            thyristor, a silicon-controlled rectifier: the device power engineers use as a
            switch that, once it's on, stays on by itself. In our chip, nobody asked for it, and
            it sits right across the supply.
            """,
            """
            দুইটা bipolar একসাথে রাখেন, আর পাবেন একটানা চারটা layer, VDD থেকে VSS: P+ source, n-well, p-substrate, N+
            source। P, N, P, N। এইটা একটা thyristor, একটা silicon-controlled rectifier: power engineer-রা যেটা switch হিসাবে
            use করে, যেটা একবার on হইলে নিজে নিজেই on থাকে। আমাদের chip-এ কেউ এইটা চায় নাই, আর এইটা ঠিক supply-এর
            আড়াআড়ি বসা।
            """,
        ))
        self.play(FadeOut(self.res), FadeOut(self.pnp_sym), FadeOut(self.npn_sym), FadeOut(self.pnp_bits),
                  FadeOut(self.npn_bits), FadeOut(self.xs))
        self.play(Transform(self.title, heading("P, N, P, N: a thyristor across the supply")))
        layers = [("P+", "pMOS source", PPLUS), ("N", "n-well", NWELL), ("P", "p-substrate", PSUB), ("N+", "nMOS source", NPLUS)]
        blocks = VGroup()
        for k, (sym, name, color) in enumerate(layers):
            r = box(-4.6 + k * 2.3, -0.6, -4.6 + k * 2.3 + 2.2, 0.8, color)
            blocks.add(VGroup(r, text(sym, size=40, color=BG if k in (0, 3) else INK, weight="BOLD").move_to(r),
                              text(name, size=20, color=MUTED).next_to(r, DOWN, buff=0.18)))
        ends = VGroup(text("VDD", size=28, color=DRAIN, weight="SEMIBOLD").next_to(blocks[0][0], LEFT, buff=0.3),
                      text("VSS", size=28, color=MUTED, weight="SEMIBOLD").next_to(blocks[3][0], RIGHT, buff=0.3))
        brace_p = BraceBetweenPoints(blocks[0][0].get_corner(UL), blocks[2][0].get_corner(UR), direction=UP, color=PPLUS)
        brace_n = BraceBetweenPoints(blocks[1][0].get_corner(DL) + DOWN * 0.55, blocks[3][0].get_corner(DR) + DOWN * 0.55,
                                     direction=DOWN, color=NPLUS)
        bl = VGroup(text("PNP", size=22, color=PPLUS, weight="SEMIBOLD").next_to(brace_p, UP, buff=0.1),
                    text("NPN", size=22, color=NPLUS, weight="SEMIBOLD").next_to(brace_n, DOWN, buff=0.1))
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in blocks], lag_ratio=0.2), FadeIn(ends))
        self.play(GrowFromCenter(brace_p), GrowFromCenter(brace_n), FadeIn(bl))
        self.layers = VGroup(blocks, ends, brace_p, brace_n, bl)

    def circuit(self):
        self.slide(say(
            """
            Drawn as a circuit, it's this. The PNP's emitter on VDD, the NPN's emitter on VSS.
            Each one's collector drives the other one's base: the PNP feeds the substrate node S,
            the NPN pulls on the well node W. And across each base, a resistor to its supply:
            R_well and R_sub. Normally both bipolars are off, because those resistors hold each
            base at its emitter's voltage. The next chapter is about what happens when something
            pushes current through one of them.
            """,
            """
            Circuit হিসাবে আঁকলে এমন। PNP-এর emitter VDD-তে, NPN-এর emitter VSS-এ। প্রত্যেকটার collector অন্যটার base চালায়:
            PNP substrate node S-রে খাওয়ায়, NPN well node W-রে টানে। আর প্রত্যেকটা base-এর আড়াআড়ি তার supply পর্যন্ত একটা
            resistor: R_well আর R_sub। সাধারণত দুইটা bipolar-ই off, কারণ ওই resistor-গুলা প্রত্যেকটা base-রে তার emitter-এর
            voltage-এ ধরে রাখে। পরের chapter-টা হইল, কিছু একটা যখন এদের একটার ভিতর দিয়া current ঠেলে দেয়, তখন কী হয়।
            """,
        ))
        self.play(self.layers.animate.scale(0.55).to_edge(LEFT, buff=0.4).shift(DOWN * 0.3))
        scr = scr_circuit(center=(3.6, -0.4), scale=0.95)
        self.play(Transform(self.title, heading("The equivalent circuit: an SCR from VDD to VSS")))
        p = scr.parts
        self.play(Create(p["vdd"]), Create(p["vss"]), FadeIn(p["labels"][:2]))
        self.play(Create(p["pnp"]), Create(p["pnp_e"]), Create(p["npn"]), Create(p["npn_e"]), FadeIn(p["labels"][4:6]))
        self.play(Create(p["w_wire"]), Create(p["s_wire"]), FadeIn(p["labels"][6:]))
        self.play(Create(p["r_well_wire"]), Create(p["r_well"]), Create(p["r_sub_wire"]), Create(p["r_sub"]),
                  FadeIn(p["labels"][2:4]))

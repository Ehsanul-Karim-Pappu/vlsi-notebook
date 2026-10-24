"""Lecture 3 · X5 · Guard rings at the I/O.

An I/O NMOS driven below ground sprays electrons into the substrate; a nearby core well collects
them and fires. Majority-carrier rings (taps that lower R_sub and R_well) and minority-carrier rings
(collectors that catch the injected carriers); the double guard ring from above; the rules; the
mistakes.
"""

import sys
from pathlib import Path

LECTURE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(LECTURE.parents[1]), str(LECTURE)]

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403
from manim_slides import Slide  # noqa: E402

from common import NPLUS, PPLUS, box, chapter_title, ring, illustrative, marker, pdk_tag  # noqa: E402
from kit.style import *  # noqa: E402,F403

TOP = 0.2  # the silicon surface in the cross-sections


def substrate(x0=-6.6, x1=6.6, depth=3.2):
    return box(x0, TOP - depth, x1, TOP, PSUB)


def diff(x, color, label, w=0.8, h=0.36):
    r = box(x - w / 2, TOP - h, x + w / 2, TOP, color)
    return VGroup(r, text(label, size=15, color=BG, weight="SEMIBOLD").move_to(r))


def lead(x, name, color, h=0.65):
    return VGroup(Line([x, TOP, 0], [x, TOP + h, 0], stroke_color=METAL, stroke_width=4),
                  text(name, size=17, color=color, weight="SEMIBOLD").move_to([x, TOP + h + 0.22, 0]))


def electrons(start, end, n=16, spread=0.6, seed=3):
    """Dots along a sagging path from START to END, to be animated with a phase."""
    rng = np.random.default_rng(seed)
    offs = rng.uniform(-spread, spread, n)
    phases = np.linspace(0, 1, n, endpoint=False)
    start, end = np.array(start, float), np.array(end, float)

    def pos(t, k):
        p = start + (end - start) * t
        return p + np.array([0, -1.0 * np.sin(np.pi * t) + offs[k] * np.sin(np.pi * t) * 0.6, 0])

    dots = VGroup(*[Dot(radius=0.05, color=NPLUS) for _ in range(n)])
    tr = ValueTracker(0)

    def upd(group):
        for k, d in enumerate(group):
            d.move_to(pos((tr.get_value() + phases[k]) % 1, k))
    dots.add_updater(upd)
    upd(dots)
    return dots, tr


class X05GuardRings(Chapter, Slide):
    def construct(self):
        self.card()
        self.injection()
        self.rings()
        self.double()
        self.rules()
        self.mistakes()

    def card(self):
        self.slide(say(
            """
            Chapter five: guard rings at the I/O. The I/O ring is where the injectors live: the
            transistors whose drains connect straight to the pads, where the outside world can
            push a pin above the supply or below ground. Guard rings are how we keep what they
            inject from reaching anything else.
            """,
            """
            Chapter five: I/O-তে guard ring। Injector-রা থাকে I/O ring-এ: যে transistor-গুলার drain সরাসরি pad-এ যুক্ত, যেখানে
            বাইরের দুনিয়া একটা pin-রে supply-র উপরে বা ground-এর নিচে ঠেলে দিতে পারে। এরা যা inject করে সেইটা যাতে আর কিছুতে না
            পৌঁছায়, guard ring দিয়া আমরা সেইটাই করি।
            """,
        ))
        self.card_group = chapter_title(5, "Guard rings at the I/O", "Catch it before it reaches a base")
        self.play(FadeIn(self.card_group, shift=UP * 0.2), run_time=1.2)

    def injection(self):
        self.slide(say(
            """
            Here's an I/O NMOS, its drain wired to the pad, and a little way off, a core block's
            n-well. Pull the pad below ground, by ringing, by a cable, by the qualification test,
            and the drain's junction forward-biases. Electrons pour into the substrate. In the
            p-type substrate they're minority carriers: they wander a long way before they
            recombine, tens to hundreds of microns. Whatever n-well they reach collects them as
            current, and that current flows through R_well. That's a trigger, delivered to a block
            that never touched the pad.
            """,
            """
            এই যে একটা I/O NMOS, তার drain pad-এ যুক্ত, আর একটু দূরে একটা core block-এর n-well। Pad-রে ground-এর নিচে টানেন,
            ringing দিয়া, একটা cable দিয়া, qualification test দিয়া, আর drain-এর junction forward-bias হয়। Electron substrate-এ
            ঢুকে পড়ে। P-type substrate-এ এরা minority carrier: recombine করার আগে অনেক দূর ঘুরে বেড়ায়, দশ থেকে শত micron। যে
            n-well-এ পৌঁছায়, সেইটা এদের current হিসাবে সংগ্রহ করে, আর ওই current R_well দিয়া চলে। এইটা একটা trigger, এমন একটা
            block-এ পৌঁছে দেওয়া যেটা কখনো pad ছোঁয় নাই।
            """,
        ))
        self.play(FadeOut(self.card_group))
        title = heading("An injector, and a victim far away")
        sub = substrate()
        io_d = diff(-4.4, NPLUS, "n⁺")
        io_s = diff(-2.8, NPLUS, "n⁺")
        gate = box(-4.0, TOP + 0.04, -3.2, TOP + 0.28, GATE)
        well = box(2.4, TOP - 1.7, 6.2, TOP, NWELL)
        core = VGroup(diff(3.4, PPLUS, "p⁺"), diff(4.6, PPLUS, "p⁺"), diff(5.6, NPLUS, "n⁺"))
        leads = VGroup(lead(-4.4, "PAD < 0 V", GATE), lead(-2.8, "VSS", MUTED), lead(5.6, "VDD", DRAIN))
        tags = VGroup(text("I/O NMOS", size=20, color=NPLUS, weight="SEMIBOLD").move_to([-3.6, TOP + 1.55, 0]),
                      text("a core block's n-well", size=20, color=INK).move_to([4.3, TOP + 1.55, 0]),
                      text("p-substrate", size=18, color=INK).set_opacity(0.8).move_to([-5.4, TOP - 2.9, 0]))
        dots, tr = electrons([-4.4, TOP - 0.4, 0], [3.0, TOP - 1.2, 0])
        dist = DoubleArrow([-4.4, TOP - 2.6, 0], [2.4, TOP - 2.6, 0], buff=0, stroke_color=MUTED, stroke_width=2, tip_length=0.15)
        dist_l = text("tens to hundreds of µm", size=18, color=MUTED).next_to(dist, UP, buff=0.06)
        tag = illustrative().to_corner(DL, buff=0.3)
        self.play(FadeIn(title), FadeIn(sub), FadeIn(io_d), FadeIn(io_s), FadeIn(gate), FadeIn(well), FadeIn(core),
                  FadeIn(leads), FadeIn(tags), FadeIn(tag))
        self.add(dots)
        self.play(tr.animate.set_value(3), GrowFromCenter(dist), FadeIn(dist_l), run_time=4, rate_func=linear)
        dots.clear_updaters()
        self.scene_parts = VGroup(sub, io_d, io_s, gate, well, core, leads, tags, dist, dist_l, tag, dots)
        self.title = title

    def rings(self):
        self.slide(say(
            """
            There are two kinds of ring, and they do different jobs. A P+ ring in the substrate,
            tied to VSS, is a tap: it lowers R_sub around the NMOS and gives the substrate current a
            short way out. That's a majority-carrier ring. An N-well ring with N+ on top, tied to
            VDD and placed between the injector and everything else, is a collector: the electrons
            that reach it are swept into it and taken to the supply, harmlessly, before they reach
            a core well. That's a minority-carrier ring. The PMOS side is the mirror image: an N+
            ring in its well, and a P+ ring outside the well to catch holes.
            """,
            """
            Ring দুই রকম, আর এরা আলাদা কাজ করে। Substrate-এ একটা P+ ring, VSS-এ বাঁধা, একটা tap: NMOS-এর চারপাশে R_sub কমায় আর
            substrate current-রে বের হওয়ার একটা ছোট পথ দেয়। এইটা majority-carrier ring। উপরে N+ সহ একটা N-well ring, VDD-তে বাঁধা,
            injector আর বাকি সবকিছুর মাঝখানে বসানো, একটা collector: যে electron-গুলা এখানে পৌঁছায় সেগুলা এর ভিতরে টেনে নেওয়া হয় আর
            নিরাপদে supply-তে নিয়া যাওয়া হয়, core well-এ পৌঁছানোর আগেই। এইটা minority-carrier ring। PMOS-এর দিকটা mirror image:
            তার well-এ একটা N+ ring, আর well-এর বাইরে holes ধরার জন্য একটা P+ ring।
            """,
        ))
        self.play(Transform(self.title, heading("Two rings: a tap and a collector")))
        p_ring = VGroup(diff(-5.5, PPLUS, "p⁺", 0.6), diff(-1.7, PPLUS, "p⁺", 0.6))
        n_ring_well = box(-0.8, TOP - 1.4, 0.4, TOP, NWELL, 1.0, 2)
        n_ring = diff(-0.2, NPLUS, "n⁺", 0.7)
        p_l = text("P+ ring to VSS: a tap\n(majority carriers)", size=18, color=PPLUS).move_to([-3.6, TOP - 2.45, 0])
        n_l = text("N-well ring to VDD: a collector\n(minority carriers)", size=18, color=NPLUS).move_to([0.6, TOP + 1.1, 0])
        old_dots = self.scene_parts[-1]
        dots, tr = electrons([-4.4, TOP - 0.4, 0], [-0.2, TOP - 0.8, 0], seed=5)
        self.play(FadeOut(old_dots), FadeOut(self.scene_parts[8]), FadeOut(self.scene_parts[9]))
        self.play(FadeIn(p_ring), FadeIn(p_l))
        self.play(FadeIn(n_ring_well), FadeIn(n_ring), FadeIn(n_l))
        self.add(dots)
        caught = text("caught: the core well\nsees almost nothing", size=20, color=GOOD).move_to([4.3, TOP - 2.3, 0])
        self.play(tr.animate.set_value(3), FadeIn(caught), run_time=4, rate_func=linear)
        dots.clear_updaters()
        self.ring_parts = VGroup(p_ring, n_ring_well, n_ring, p_l, n_l, dots, caught)

    def double(self):
        self.slide(say(
            """
            From above, this becomes the double guard ring you see around every I/O driver. Around
            the I/O NMOS: first a P+ ring, the tap, then an N-well ring, the collector. Around the
            I/O PMOS, in its well: first an N+ ring, the well tap, then, outside the well, a P+
            ring that collects the holes. Inner ring, a tap for the device's own body. Outer ring, a
            collector that protects everyone else.
            """,
            """
            উপর থেকে, এইটাই সেই double guard ring যেটা আপনি প্রত্যেকটা I/O driver-এর চারপাশে দেখেন। I/O NMOS-এর চারপাশে: প্রথমে একটা
            P+ ring, মানে tap, তারপর একটা N-well ring, মানে collector। I/O PMOS-এর চারপাশে, তার well-এ: প্রথমে একটা N+ ring, well
            tap, তারপর, well-এর বাইরে, একটা P+ ring যেটা holes ধরে। ভিতরের ring, device-এর নিজের body-র জন্য একটা tap। বাইরের ring,
            একটা collector যেটা বাকি সবাইরে রক্ষা করে।
            """,
        ))
        self.clear()
        title = heading("From above: the double guard ring")

        cn, cp = np.array([-3.3, -0.4, 0]), np.array([3.3, -0.4, 0])
        nmos = VGroup(*[box(cn[0] - 1.05 + k * 0.6, cn[1] - 0.8, cn[0] - 0.65 + k * 0.6, cn[1] + 0.8, NPLUS, 0.5, 2) for k in range(4)]).move_to(cn)
        n_in = ring(cn, 3.4, 2.7, 0.16, PPLUS)
        n_out_well = ring(cn, 4.4, 3.7, 0.34, NWELL)  # the N-well collector ring, N+ along its middle
        n_out = ring(cn, 4.18, 3.48, 0.12, NPLUS)
        well = box(cp[0] - 1.9, cp[1] - 1.55, cp[0] + 1.9, cp[1] + 1.55, NWELL, 0.6, 0)
        pmos = VGroup(*[box(cp[0] - 1.05 + k * 0.6, cp[1] - 0.8, cp[0] - 0.65 + k * 0.6, cp[1] + 0.8, PPLUS, 0.5, 2) for k in range(4)]).move_to(cp)
        p_in = ring(cp, 3.2, 2.5, 0.16, NPLUS)
        p_out = ring(cp, 4.4, 3.7, 0.16, PPLUS)
        ln = VGroup(text("I/O NMOS", size=22, color=NPLUS, weight="SEMIBOLD").next_to(n_out_well, UP, buff=0.25),
                    text("inner: P+ tap ring, VSS\nouter: N-well collector ring, VDD", size=17, color=INK).next_to(n_out_well, DOWN, buff=0.25))
        lp = VGroup(text("I/O PMOS", size=22, color=PPLUS, weight="SEMIBOLD").next_to(p_out, UP, buff=0.25),
                    text("inner: N+ well-tap ring, VDD\nouter: P+ collector ring, VSS", size=17, color=INK).next_to(p_out, DOWN, buff=0.25))
        self.play(FadeIn(title))
        self.play(FadeIn(nmos), FadeIn(n_in))
        self.play(FadeIn(n_out_well), FadeIn(n_out), FadeIn(ln))
        self.play(FadeIn(well), FadeIn(pmos), FadeIn(p_in))
        self.play(FadeIn(p_out), FadeIn(lp))

    def rules(self):
        self.slide(say(
            """
            And the rules that come with them. Where: around every device connected to a pad, and
            around ESD devices, which are injectors by design. Continuity: the ring must close; a
            gap is a doorway. Width: a minimum, because a ring collects in proportion to its area
            and depth. Contacts: a maximum spacing along the whole ring, because a ring is only as
            good as its connection; it may have to carry tens of milliamps. Strapping: wide metal
            and many vias back to the supply. Which supply: a low-impedance, robust one, usually
            the I/O ground and supply, never a quiet analog reference. And at the I/O, larger
            spacing from N+ and P+ to the well edges, to cut the bipolar gain.
            """,
            """
            আর এদের সাথে যে rule-গুলা আসে। কোথায়: pad-এ যুক্ত প্রত্যেকটা device-এর চারপাশে, আর ESD device-এর চারপাশে, যেগুলা
            design অনুযায়ীই injector। Continuity: ring-টা বন্ধ হইতে হবে; একটা ফাঁক মানে একটা দরজা। Width: একটা minimum, কারণ ring তার
            area আর গভীরতার অনুপাতে সংগ্রহ করে। Contact: পুরা ring জুড়ে একটা maximum spacing, কারণ ring ততটাই ভালো যতটা তার connection;
            এইটারে কয়েক দশ milliamp বহন করতে হইতে পারে। Strapping: supply পর্যন্ত চওড়া metal আর অনেক via। কোন supply: একটা কম
            impedance-এর, মজবুত supply, সাধারণত I/O ground আর supply, কখনো একটা শান্ত analog reference না। আর I/O-তে, N+ আর P+ থেকে
            well-এর কিনারা পর্যন্ত বেশি spacing, bipolar gain কমানোর জন্য।
            """,
        ))
        self.clear()
        title = heading("The guard ring rules")
        rows = VGroup(*[VGroup(text(a, size=22, color=GATE, weight="SEMIBOLD"), text(b, size=21, color=INK)).arrange(RIGHT, buff=0.3)
                        for a, b in (("where", "every device on a pad; every ESD device"),
                                     ("continuity", "the ring closes: a gap is a doorway"),
                                     ("width", "a minimum: collection scales with area"),
                                     ("contacts", "a maximum spacing along the whole ring"),
                                     ("strapping", "wide metal, many vias: it may carry tens of mA"),
                                     ("supply", "the robust I/O supply, never a quiet reference"),
                                     ("spacing", "more N+ and P+ to well spacing: less gain"))])
        for r in rows:
            r[1].move_to([r[1].width / 2 - 2.6, 0, 0])
            r[0].move_to([-3.0 - r[0].width / 2, 0, 0])
        rows.arrange(DOWN, buff=0.3).move_to(DOWN * 0.2)
        for r in rows:
            r[0].align_to([-3.0, 0, 0], RIGHT)
            r[1].align_to([-2.7, 0, 0], LEFT)
        tag = pdk_tag().to_corner(DR, buff=0.3)
        self.play(FadeIn(title), FadeIn(tag))
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows], lag_ratio=0.15), run_time=2.2)

    def mistakes(self):
        self.slide(say(
            """
            The mistakes that pass by eye. A ring cut open so a wire can get through: route the
            wire over it in metal, never break the diffusion. A ring with diffusion all the way
            round but contacts on one side only: the far side floats. A ring tied to the core
            supply, or to a sensitive analog supply: now the injected current flows on the very
            rail you were trying to protect. And a beautifully closed ring drawn on the wrong
            layer: N+ in the substrate without the well under it is only a shallow collector, not a
            deep collector.
            """,
            """
            যে ভুলগুলা চোখে ধরা পড়ে না। একটা wire পার করার জন্য কাটা ring: wire-টারে metal দিয়া উপর দিয়া নেন, diffusion কখনো
            ভাঙবেন না। চারপাশে diffusion আছে কিন্তু শুধু এক দিকে contact আছে এমন ring: দূরের দিকটা ভাসে। Core supply-তে বা একটা
            sensitive analog supply-তে বাঁধা ring: এখন injected current ঠিক সেই rail দিয়া চলে যেটা আপনি রক্ষা করতে চাইছিলেন। আর ভুল
            layer-এ আঁকা একটা সুন্দর বন্ধ ring: নিচে well ছাড়া substrate-এ N+ শুধু একটা অগভীর collector, গভীর collector না।
            """,
        ))
        self.clear()
        title = heading("Mistakes that pass by eye")

        def mini(center, kind):
            c = np.array(center)
            dev = box(c[0] - 0.5, c[1] - 0.4, c[0] + 0.5, c[1] + 0.4, NPLUS, 0.5, 2)
            g = VGroup(dev)
            if kind == "gap":
                g.add(ring(c, 2.4, 1.8, 0.14, PPLUS, gap=0.45))
                g.add(Line(c + [0, 1.5, 0], c + [0, 0.4, 0], stroke_color=METAL, stroke_width=6))
            else:
                g.add(ring(c, 2.4, 1.8, 0.14, PPLUS))
            if kind == "contacts":
                g.add(*[Square(0.09, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(c + [-1.13, y, 0]) for y in (-0.6, -0.2, 0.2, 0.6)])
            if kind == "supply":
                g.add(text("to the core VSS", size=15, color=DRAIN).move_to(c + [0, -1.2, 0]))
            return g

        items = [("gap", "cut open for a wire", "cross it in metal instead"),
                 ("contacts", "contacts on one side only", "contact it all the way round"),
                 ("supply", "tied to the core supply", "the robust I/O supply")]
        cols = VGroup()
        for k, (kind, bad, fix) in enumerate(items):
            x = -4.4 + k * 4.4
            pic = mini([x, 0.5, 0], kind)
            mk = marker(pic, "LUP.GR", buff=0.15)
            words = VGroup(text(bad, size=20, color=DRAIN), text(fix, size=20, color=GOOD)).arrange(DOWN, buff=0.12)
            words.move_to([x, -1.9, 0])
            cols.add(VGroup(pic, mk, words))
        self.play(FadeIn(title))
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cols], lag_ratio=0.3), run_time=2.0)

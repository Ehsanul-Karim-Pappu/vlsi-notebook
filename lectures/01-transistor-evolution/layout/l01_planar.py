"""Layout edition · L1 · One rectangle over another: the planar MOSFET.

The schematic, the layout and the cross-section of one transistor, side by side; W and L as
drawn; fingers and multipliers; wells and taps; and an inverter.
"""

import sys
from pathlib import Path

LECTURE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(LECTURE.parents[1]), str(LECTURE), str(LECTURE / "layout")]

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403
from manim_slides import Slide  # noqa: E402

from common import (ACTIVE, CONTACT, METAL, NPLUS, NWELL, POLY, PWELL, box, planar_mos,  # noqa: E402
                    schematic)
from kit.style import *  # noqa: E402,F403

U = 0.009  # scene units per nm in this chapter's layouts (the sizes are illustrative)
POLY_TEXT = "#8F94F2"  # the poly colour, light enough for text


class L01Planar(Chapter, Slide):
    def construct(self):
        self.card()
        self.three_views()
        self.section()
        self.w_and_l()
        self.fingers()
        self.multiplier()
        self.wells()
        self.inverter()
        self.any_w()

    def card(self):
        self.slide(say(
            """
            Chapter one: the planar transistor, the one most of today's layout rules grew up
            around. Let's take one transistor apart three ways: the schematic you're given, the
            layout you draw, and the silicon it makes.
            """,
            """
            Chapter one: planar transistor, আজকের বেশিরভাগ layout rule যেটারে ঘিরে তৈরি। একটা transistor-রে তিনভাবে
            খুলে দেখি: যে schematic আপনারে দেওয়া হয়, যে layout আপনি আঁকেন, আর তাতে যে silicon তৈরি হয়।
            """,
        ))
        self.card_group = self.open_chapter(1, 1971, 1971, "One rectangle over another", "The planar MOSFET, as you draw it")

    # --- schematic, layout, cut line -----------------------------------------------------------
    def three_views(self):
        self.slide(say(
            """
            On the left, the schematic: gate, drain, source. In the middle, the same transistor
            in layout. A rectangle of active area, the diffusion. A strip of poly across it: that
            strip is the gate, and the transistor is exactly where poly crosses active. The
            active on either side becomes the source and the drain. Columns of contacts, and
            metal one over them. Now draw a cut line, A to A-prime, along the channel, from
            source to drain. That's the cross-section we'll look at next.
            """,
            """
            বামে schematic: gate, drain, source। মাঝখানে একই transistor, layout-এ। Active area-র একটা rectangle,
            মানে diffusion। তার উপর দিয়া poly-র একটা ফালি: ওই ফালিটাই gate, আর transistor ঠিক সেইখানে যেখানে poly
            active পার হয়। দুই পাশের active হয়ে যায় source আর drain। Contact-এর কয়েকটা column, আর তার উপর metal one।
            এবার channel বরাবর, source থেকে drain, একটা cut line টানেন, A থেকে A-prime। পরের slide-এ ওই cross-section-ই
            দেখব।
            """,
        ))
        self.play(FadeOut(self.card_group))
        title = heading("Three views of one transistor")
        sch = schematic("nmos", 2.4).move_to([-5.1, -0.1, 0])
        dev, parts = planar_mos(300, 60, nf=1, u=U, sd=100, center=(-0.6, -0.2))
        lay_l = text("layout", size=22, color=MUTED).next_to(dev, DOWN, buff=0.75)
        sch_l = text("schematic", size=22, color=MUTED).next_to(sch, DOWN, buff=0.35).set_y(lay_l.get_y())
        labels = VGroup(
            text("active (diffusion)", size=22, color=ACTIVE),
            text("poly: the gate", size=22, color=POLY_TEXT),
            text("contacts", size=22, color=CONTACT),
            text("metal 1", size=22, color=METAL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.6, 0.6, 0])
        s_l = text("S", size=28, weight="BOLD").next_to(parts["metal"][0], UP, buff=0.75)
        d_l = text("D", size=28, weight="BOLD").next_to(parts["metal"][1], UP, buff=0.75)
        g_l = text("G", size=28, weight="BOLD", color=POLY_TEXT).next_to(parts["poly"][0], UP, buff=0.08)
        y = parts["active"][0].get_center()[1]
        x0, x1 = parts["active"][0].get_left()[0] - 0.55, parts["active"][0].get_right()[0] + 0.55
        cut = DashedLine([x0, y, 0], [x1, y, 0], stroke_color=GATE, stroke_width=3, dash_length=0.12)
        a_l = text("A", size=24, color=GATE).next_to(cut, LEFT, buff=0.1)
        a2_l = text("A′", size=24, color=GATE).next_to(cut, RIGHT, buff=0.1)
        where = text("transistor = where\npoly crosses active", size=22, color=INK).move_to([4.6, -1.6, 0])
        self.play(FadeIn(title), FadeIn(sch), FadeIn(sch_l))
        self.play(FadeIn(parts["active"]), FadeIn(labels[0]), FadeIn(lay_l))
        self.play(FadeIn(parts["poly"]), FadeIn(labels[1]), FadeIn(g_l))
        self.play(FadeIn(parts["contacts"]), FadeIn(labels[2]))
        self.play(FadeIn(parts["metal"]), FadeIn(labels[3]), FadeIn(s_l), FadeIn(d_l))
        self.play(FadeIn(where))
        self.play(Create(cut), FadeIn(a_l), FadeIn(a2_l))

    # --- the cross-section ---------------------------------------------------------------------
    def section(self):
        self.slide(say(
            """
            Here's the cut along A to A-prime. The p-type silicon. Two heavily doped n-type
            regions: the source and the drain, under the contacts. Between them, under a very
            thin layer of oxide, the gate. With the gate at zero, the silicon between source and
            drain is p-type, and nothing flows. Raise the gate voltage, and it pulls electrons up
            to the surface, right under the oxide: a thin n-type layer forms, the channel, and
            it joins source to drain. That's the whole idea. The gate opens and closes a channel
            under itself.
            """,
            """
            এই যে A থেকে A-prime বরাবর cut। p-type silicon। দুইটা heavily doped n-type region: source আর drain,
            contact-গুলার নিচে। মাঝখানে, খুব পাতলা একটা oxide layer-এর নিচে, gate। Gate শূন্যতে থাকলে source আর drain-এর
            মাঝের silicon p-type, কিছুই যায় না। Gate voltage বাড়ান, gate electron-গুলারে টেনে surface-এ নিয়া আসে, oxide-এর
            ঠিক নিচে: একটা পাতলা n-type layer হয়, এইটাই channel, আর সেইটা source আর drain-রে জোড়া দেয়। পুরা idea এইটুকুই।
            Gate নিজের নিচে একটা channel খোলে আর বন্ধ করে।
            """,
        ))
        self.clear()
        title = heading("The cut A–A′: along the channel")
        sub = box(-5.0, -3.0, 5.0, -0.6, SUBSTRATE, 1.0, 0)
        sub_l = text("p-type silicon", size=22, color=MUTED).move_to([3.6, -2.5, 0])
        src = box(-4.2, -1.45, -1.3, -0.6, NPLUS, 0.85, 0)
        drn = box(1.3, -1.45, 4.2, -0.6, NPLUS, 0.85, 0)
        src_l = text("n+ source", size=22, color=BG, weight="SEMIBOLD").move_to(src)
        drn_l = text("n+ drain", size=22, color=BG, weight="SEMIBOLD").move_to(drn)
        ox = box(-1.3, -0.6, 1.3, -0.48, OXIDE_TEXT, 1.0, 0)
        gate = box(-1.3, -0.48, 1.3, 0.6, POLY, 0.9, 0)
        gate_l = text("gate (poly)", size=22, color=INK).move_to(gate)
        ox_l = text("thin oxide", size=16, color=OXIDE_TEXT).next_to(gate, LEFT, buff=0.08).align_to(ox, DOWN).shift(UP * 0.02)
        cs = box(-3.0, -0.6, -2.5, 1.2, CONTACT, 0.95, 0)
        cd = box(2.5, -0.6, 3.0, 1.2, CONTACT, 0.95, 0)
        m1 = VGroup(box(-3.5, 1.2, -2.0, 1.55, METAL, 0.9, 0), box(2.0, 1.2, 3.5, 1.55, METAL, 0.9, 0))
        s_t = text("S", size=26, weight="BOLD").next_to(m1[0], UP, buff=0.12)
        d_t = text("D", size=26, weight="BOLD").next_to(m1[1], UP, buff=0.12)
        g_t = text("G", size=26, weight="BOLD", color=POLY_TEXT).next_to(gate, UP, buff=0.12)
        not_scale = text("not to scale", size=16, color=MUTED).to_corner(DR, buff=0.3)
        self.play(FadeIn(title), FadeIn(sub), FadeIn(sub_l), FadeIn(not_scale))
        self.play(FadeIn(src), FadeIn(drn), FadeIn(src_l), FadeIn(drn_l))
        self.play(FadeIn(ox), FadeIn(ox_l), FadeIn(gate), FadeIn(gate_l), FadeIn(g_t))
        self.play(FadeIn(cs), FadeIn(cd), FadeIn(m1), FadeIn(s_t), FadeIn(d_t))

        vg = ValueTracker(0.0)
        meter = always_redraw(lambda: text(f"V_G = {vg.get_value():.1f} V", size=26, color=GATE).move_to([-5.2, 2.4, 0]))
        chan = always_redraw(lambda: box(-1.3, -0.6 - 0.12 * min(1, max(0, (vg.get_value() - 0.35) / 0.4)), 1.3, -0.6,
                                         ELECTRON, min(1, max(0, (vg.get_value() - 0.35) / 0.4)), 0))
        self.add(meter, chan)
        rng = np.random.default_rng(3)
        dots = VGroup(*[Dot([x, -0.66, 0], radius=0.035, color=ELECTRON) for x in rng.uniform(-1.25, 1.25, 14)])
        self.play(vg.animate.set_value(0.9), run_time=2.0)
        ch_l = text("the channel: electrons pulled up under the oxide", size=22, color=ELECTRON).move_to([0, -3.45, 0])
        self.play(FadeIn(ch_l), FadeIn(dots))
        self.play(*[d.animate.shift(RIGHT * (1.3 - d.get_x()) * 0.9) for d in dots], run_time=1.5)
        arrow = Arrow([-1.2, -1.0, 0], [1.2, -1.0, 0], buff=0, stroke_color=ELECTRON, stroke_width=5)
        cur = text("current", size=20, color=ELECTRON).next_to(arrow, DOWN, buff=0.05)
        self.play(GrowArrow(arrow), FadeIn(cur))

    # --- W and L ------------------------------------------------------------------------------
    def w_and_l(self):
        self.slide(say(
            """
            So the two things you draw are W and L. W is the width of the active under the gate:
            how wide the channel is. L is the width of the poly strip: how long the channel is,
            from source to drain. To first order, the current goes as W over L. Make it twice as
            wide and you get about twice the current, like two transistors side by side. Make it
            twice as long and you get about half. But longer isn't only weaker: a longer channel
            is steadier. It holds its current better as the drain voltage changes, so it gives
            more gain, and it matches its neighbour better. We'll see why in the next chapter.
            """,
            """
            তো আপনি যে দুইটা জিনিস আঁকেন সেইটা W আর L। W হইলো gate-এর নিচে active-এর width: channel কতটা চওড়া। L
            হইলো poly ফালিটার width: source থেকে drain পর্যন্ত channel কতটা লম্বা। মোটামুটি current যায় W ভাগ L হারে। দ্বিগুণ
            চওড়া করেন, current প্রায় দ্বিগুণ, যেন পাশাপাশি দুইটা transistor। দ্বিগুণ লম্বা করেন, প্রায় অর্ধেক। কিন্তু লম্বা মানে
            শুধু দুর্বল না: লম্বা channel বেশি স্থির। Drain voltage বদলাইলেও current ভালো ধরে রাখে, তাই gain বেশি, আর পাশের
            device-এর সাথে match-ও ভালো করে। কেন, সেইটা পরের chapter-এ দেখব।
            """,
        ))
        self.clear()
        title = heading("What you draw: W and L")
        dev, parts = planar_mos(300, 60, nf=1, u=U, sd=100, contacts=False, metal=False, center=(-3.6, -0.3))
        act, gate = parts["active"][0], parts["poly"][0]
        w_br = BraceBetweenPoints(act.get_corner(DR) + RIGHT * 0.1, act.get_corner(UR) + RIGHT * 0.1, direction=RIGHT, color=ACTIVE)
        w_l = text("W", size=32, color=ACTIVE, weight="BOLD").next_to(w_br, RIGHT, buff=0.1)
        l_br = BraceBetweenPoints(gate.get_corner(UL) + UP * 0.08, gate.get_corner(UR) + UP * 0.08, direction=UP, color=POLY_TEXT)
        l_l = text("L", size=32, color=POLY_TEXT, weight="BOLD").next_to(l_br, UP, buff=0.08)
        rule = VGroup(text("current ∝ W / L, roughly", size=34, weight="SEMIBOLD"),
                      text("twice as wide: about twice the current", size=24, color=MUTED),
                      text("twice as long: about half, but steadier:", size=24, color=MUTED),
                      text("more gain, better matching", size=24, color=GOOD)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        rule.move_to([3.2, 0.4, 0])
        self.play(FadeIn(title), FadeIn(dev))
        self.play(FadeIn(w_br), FadeIn(w_l), FadeIn(l_br), FadeIn(l_l))
        self.play(FadeIn(rule[0]))
        # wider
        cur = Arrow([-5.2, -2.9, 0], [-2.0, -2.9, 0], buff=0, stroke_color=ELECTRON, stroke_width=6)
        cur_l = text("current", size=20, color=ELECTRON).next_to(cur, DOWN, buff=0.06)
        self.play(GrowArrow(cur), FadeIn(cur_l))
        wide = VGroup(dev, w_br, w_l, l_br, l_l)
        self.play(act.animate.stretch(1.45, 1), gate.animate.stretch(1.35, 1),
                  w_br.animate.stretch(1.45, 1), w_l.animate.shift(RIGHT * 0.05),
                  l_br.animate.shift(UP * 0.6), l_l.animate.shift(UP * 0.6),
                  cur.animate.set_stroke(width=11), FadeIn(rule[1]), run_time=1.4)
        self.play(act.animate.stretch(1 / 1.45, 1), gate.animate.stretch(1 / 1.35, 1),
                  w_br.animate.stretch(1 / 1.45, 1), l_br.animate.shift(DOWN * 0.6), l_l.animate.shift(DOWN * 0.6),
                  cur.animate.set_stroke(width=6), run_time=1.0)
        # longer
        self.play(gate.animate.stretch(2.0, 0), l_br.animate.stretch(2.0, 0), l_l.animate.shift(UP * 0.02),
                  cur.animate.set_stroke(width=3), FadeIn(rule[2]), FadeIn(rule[3]), run_time=1.4)
        self.wl = VGroup(title, wide, rule, cur, cur_l)

    # --- fingers ------------------------------------------------------------------------------
    def fingers(self):
        self.slide(say(
            """
            A wide transistor is usually folded. Take one device with a big W, cut it into, say,
            four fingers, each a quarter of the width, and lay them side by side, sharing their
            sources and drains: source, drain, source, drain, source. The total W is the same.
            Why bother? Each gate finger is shorter, so less gate resistance. Two neighbouring
            fingers share one drain, so there's less drain area, and less drain capacitance,
            for the same W. And the device becomes a squarer block that fits a row. With an
            even number of fingers, both ends are sources, which is the usual choice.
            """,
            """
            চওড়া transistor সাধারণত ভাঁজ করা হয়। বড় W-এর একটা device নেন, কেটে ধরেন চারটা finger বানান, প্রত্যেকটা width-এর
            চার ভাগের এক ভাগ, আর পাশাপাশি বসান, source আর drain share করে: source, drain, source, drain, source। মোট W
            একই। কেন এত ঝামেলা? প্রত্যেকটা gate finger ছোট, তাই gate resistance কম। পাশাপাশি দুইটা finger একটা drain
            share করে, তাই একই W-এর জন্য drain area কম, drain capacitance-ও কম। আর device-টা একটা চৌকা block হয় যেটা row-তে
            বসে। Finger জোড় সংখ্যায় হইলে দুই মাথাতেই source থাকে, এইটাই সাধারণ পছন্দ।
            """,
        ))
        self.play(FadeOut(self.wl))
        title = heading("Fingers: one wide device, folded")
        one, op = planar_mos(400, 60, nf=1, u=0.0075, sd=90, center=(-4.4, -0.3))
        one_l = text("1 finger, W", size=22, color=MUTED).next_to(one, DOWN, buff=0.35)
        four, fp = planar_mos(100, 60, nf=4, u=0.0075, sd=90, center=(1.4, -0.3))
        four_l = text("4 fingers of W/4: the same total W", size=22, color=MUTED).next_to(four, DOWN, buff=0.35)
        names = VGroup(*[text(n, size=22, weight="BOLD", color=ELECTRON if n == "D" else INK).move_to([x, four.get_top()[1] + 0.35, 0])
                         for n, x in zip("SDSDS", fp["sd"])])
        arrow = Arrow([-3.0, -0.3, 0], [-1.3, -0.3, 0], buff=0, stroke_color=MUTED, stroke_width=3)
        why = VGroup(text("shorter gate fingers: less gate resistance", size=22),
                     text("shared drains: less drain area and capacitance", size=22),
                     text("a squarer block that fits the row", size=22)).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        why.next_to(four_l, DOWN, buff=0.45).set_x(0.8)
        self.play(FadeIn(title), FadeIn(one), FadeIn(one_l))
        self.play(GrowArrow(arrow), FadeIn(four), FadeIn(four_l), FadeIn(names))
        for w in why:
            self.play(FadeIn(w, shift=UP * 0.1), run_time=0.6)
        self.parts = VGroup(title, one, one_l, four, four_l, names, arrow, why)

    def multiplier(self):
        self.slide(say(
            """
            A multiplier is different. m equals two means two complete copies of the device,
            each with its own active, wired in parallel. Fingers share diffusion; multiplier
            copies don't. For matching, this is the habit worth keeping: design with one unit
            device, and build every size as a count of units. A one-to-two ratio is one unit
            against two units. Then the ratio is set by counting, not by how two different
            shapes happen to print.
            """,
            """
            Multiplier অন্য জিনিস। m সমান দুই মানে device-এর পুরা দুইটা copy, প্রত্যেকটার নিজের active, parallel-এ wire
            করা। Finger diffusion share করে; multiplier-এর copy করে না। Matching-এর জন্য যে অভ্যাসটা রাখার মতো: একটা unit
            device দিয়া design করেন, আর প্রত্যেকটা size বানান unit গুনে। এক-অনুপাত-দুই মানে এক unit বনাম দুই unit। তখন
            ratio ঠিক হয় গোনা দিয়া, দুইটা আলাদা shape কিভাবে print হয় তার উপর না।
            """,
        ))
        self.play(FadeOut(self.parts))
        title = heading("Multipliers: copies in parallel")
        def unit(c):
            return planar_mos(160, 60, nf=2, u=0.0085, sd=90, center=c)[0]

        a = unit((-4.6, 0.2))
        b1, b2 = unit((0.4, 0.2)), unit((3.6, 0.2))
        a_l = text("unit device, m = 1", size=22, color=MUTED).next_to(a, DOWN, buff=0.35)
        b_l = text("m = 2: two copies, each its own active", size=22, color=MUTED).next_to(VGroup(b1, b2), DOWN, buff=0.35)
        wire = Line(b1.get_top() + UP * 0.25, b2.get_top() + UP * 0.25, stroke_color=METAL, stroke_width=4)
        ticks = VGroup(Line(b1.get_top() + UP * 0.25, b1.get_top(), stroke_color=METAL, stroke_width=4),
                       Line(b2.get_top() + UP * 0.25, b2.get_top(), stroke_color=METAL, stroke_width=4))
        ratio = text("1 : 2 = one unit against two units: set by counting", size=28, color=GATE).to_edge(DOWN, buff=0.9)
        self.play(FadeIn(title), FadeIn(a), FadeIn(a_l))
        self.play(FadeIn(b1), FadeIn(b2), FadeIn(b_l))
        self.play(Create(wire), Create(ticks))
        self.play(FadeIn(ratio))

    # --- wells and taps -----------------------------------------------------------------------
    def wells(self):
        self.slide(say(
            """
            Now the other half of CMOS. The NMOS sits in p-type silicon. The PMOS needs n-type
            silicon under it, so it sits in an n-well. Each region has to be held at its supply:
            the p side at ground, the n-well at V-D-D, through taps, heavily doped contacts of the
            same type as the region. Why they matter: the n-well, the substrate and the source
            and drain diffusions form a parasitic p-n-p-n path between the supplies. If the
            silicon under it drifts away from its supply, that path can switch on and short the
            rails: latch-up. Taps close to the devices, and guard rings around sensitive ones,
            keep the wells where they belong. Your latch-up rules come from this.
            """,
            """
            এবার CMOS-এর আরেক অর্ধেক। NMOS বসে p-type silicon-এ। PMOS-এর নিচে n-type silicon লাগে, তাই সে বসে একটা
            n-well-এ। প্রত্যেকটা region-রে তার supply-তে ধরে রাখতে হয়: p দিক ground-এ, n-well V-D-D-তে, tap দিয়া, মানে
            region-এর একই type-এর heavily doped contact। কেন জরুরি: n-well, substrate আর source-drain diffusion মিলে
            supply-গুলার মাঝে একটা parasitic p-n-p-n path বানায়। নিচের silicon যদি তার supply থেকে সরে যায়, ওই path চালু
            হয়ে rail short করে দিতে পারে: latch-up। Device-এর কাছে tap, আর sensitive device-এর চারপাশে guard ring, well-গুলারে
            জায়গামতো রাখে। আপনার latch-up rule এইখান থেকেই আসে।
            """,
        ))
        self.clear()
        title = heading("Wells and taps")
        sub = box(-6.0, -3.0, 6.0, -0.6, PWELL, 0.35, 0)
        sub_l = text("p-type substrate (or p-well): tied to GND", size=20, color=PWELL).move_to([-3.2, -2.6, 0])
        well = box(0.4, -2.2, 5.6, -0.6, NWELL, 0.35, 0)
        well_l = text("n-well: tied to V_DD", size=20, color=INK).move_to([3.0, -1.9, 0])
        def mos(x, sd_color):
            return VGroup(box(x - 1.6, -1.2, x - 0.5, -0.6, sd_color, 0.9, 0), box(x + 0.5, -1.2, x + 1.6, -0.6, sd_color, 0.9, 0),
                          box(x - 0.5, -0.55, x + 0.5, 0.25, POLY, 0.9, 0))
        n = mos(-2.6, NPLUS)
        p = mos(2.4, HOLE)
        n_l = text("NMOS: n+ source and drain", size=20, color=NPLUS).next_to(n, UP, buff=0.25)
        p_l = text("PMOS: p+ source and drain", size=20, color=HOLE).next_to(p, UP, buff=0.25)
        ptap = box(-5.4, -1.2, -4.8, -0.6, HOLE, 0.9, 0)
        ntap = box(4.6, -1.2, 5.2, -0.6, NPLUS, 0.9, 0)
        ptap_l = text("p+ tap\nto GND", size=18, color=HOLE).next_to(ptap, UP, buff=0.15)
        ntap_l = text("n+ tap\nto V_DD", size=18, color=NPLUS).next_to(ntap, UP, buff=0.15)
        lu = text("Taps close by, guard rings around sensitive devices: they keep the parasitic\n"
                  "p-n-p-n path between the supplies off (latch-up).", size=22, color=MUTED).to_edge(DOWN, buff=0.35)
        not_scale = text("not to scale", size=16, color=MUTED).to_corner(UR, buff=0.3).shift(DOWN * 0.7)
        self.play(FadeIn(title), FadeIn(sub), FadeIn(sub_l), FadeIn(not_scale))
        self.play(FadeIn(n), FadeIn(n_l))
        self.play(FadeIn(well), FadeIn(well_l), FadeIn(p), FadeIn(p_l))
        self.play(FadeIn(ptap), FadeIn(ptap_l), FadeIn(ntap), FadeIn(ntap_l))
        self.play(FadeIn(lu))

    # --- an inverter --------------------------------------------------------------------------
    def inverter(self):
        self.slide(say(
            """
            Put it together: a CMOS inverter. The schematic on the left: the PMOS on top, from V-D-D,
            the NMOS below, to ground, gates tied together as the input, drains tied together as
            the output. On the right, a planar layout of it. The PMOS in its n-well at the top,
            the NMOS at the bottom, one poly line running down through both as the shared gate,
            the drains joined in metal to make OUT, and the sources on the power rails. Every
            standard cell you've seen is a variation on this.
            """,
            """
            সব একসাথে: একটা CMOS inverter। বামে schematic: উপরে PMOS, V-D-D থেকে, নিচে NMOS, ground-এ, দুই gate
            একসাথে input, দুই drain একসাথে output। ডানে এর একটা planar layout। উপরে n-well-এ PMOS, নিচে NMOS, একটা poly
            line দুইটার ভিতর দিয়া নামছে shared gate হিসাবে, drain-গুলা metal-এ জোড়া দিয়া OUT, আর source-গুলা power rail-এ।
            আপনি যত standard cell দেখছেন, সব এইটারই রকমফের।
            """,
        ))
        self.clear()
        title = heading("A CMOS inverter: schematic and layout")
        sch = schematic("inverter", 3.6).move_to([-4.0, -0.2, 0])
        u = 0.0075
        cx = 2.6
        nw = box(cx - 1.7, 0.15, cx + 1.7, 2.75, NWELL, 0.18)
        pdev, pp = planar_mos(220, 60, nf=1, u=u, sd=100, center=(cx, 1.35))
        ndev, npp = planar_mos(140, 60, nf=1, u=u, sd=100, center=(cx, -1.25))
        for d in (pdev, ndev):
            d.remove(d[1])  # one shared gate, drawn below
        gate = box(cx - 30 * u, -2.2, cx + 30 * u, 2.5, POLY, 0.75)
        vdd = box(cx - 1.9, 2.85, cx + 1.9, 3.15, METAL, 0.7)
        gnd = box(cx - 1.9, -2.95, cx + 1.9, -2.65, METAL, 0.7)
        xs, xd = pp["sd"][0], pp["sd"][1]
        s_up = box(xs - 0.12, 1.35, xs + 0.12, 2.85, METAL, 0.7)
        s_dn = box(xs - 0.12, -2.65, xs + 0.12, -1.25, METAL, 0.7)
        out = box(xd - 0.12, -1.25, xd + 0.12, 1.35, METAL, 0.7)
        out_l = text("OUT", size=22, weight="BOLD").next_to(out, RIGHT, buff=0.35)
        in_l = text("IN", size=22, weight="BOLD", color=POLY_TEXT).move_to([cx - 0.55, 0.05, 0])
        vdd_l = text("V_DD", size=20).next_to(vdd, RIGHT, buff=0.15)
        gnd_l = text("GND", size=20).next_to(gnd, RIGHT, buff=0.15)
        pm = text("PMOS\n(n-well)", size=18, color=MUTED).next_to(nw, RIGHT, buff=0.3).shift(DOWN * 0.3)
        nm = text("NMOS", size=18, color=MUTED).next_to(ndev, RIGHT, buff=0.55)
        lay = VGroup(nw, pdev, ndev, gate, vdd, gnd, s_up, s_dn, out, out_l, in_l, vdd_l, gnd_l, pm, nm)
        lay.scale(0.86).shift(DOWN * 0.3)
        self.play(FadeIn(title), FadeIn(sch))
        self.play(FadeIn(nw), FadeIn(pdev), FadeIn(ndev), FadeIn(pm), FadeIn(nm))
        self.play(FadeIn(gate), FadeIn(in_l))
        self.play(FadeIn(vdd), FadeIn(gnd), FadeIn(s_up), FadeIn(s_dn), FadeIn(vdd_l), FadeIn(gnd_l))
        self.play(FadeIn(out), FadeIn(out_l))

    def any_w(self):
        self.slide(say(
            """
            So in the planar world, you had real freedom. Any W, any L, on a fine grid, within the
            rules. That freedom is what changed. As L kept shrinking, the planar transistor
            stopped behaving, and the fix took away some of what you could draw. Let's see why,
            in three sentences of physics.
            """,
            """
            তো planar দুনিয়ায় আপনার আসল স্বাধীনতা ছিল। যেকোনো W, যেকোনো L, একটা fine grid-এ, rule-এর ভিতরে। এই
            স্বাধীনতাটাই বদলাইছে। L ছোট হইতে হইতে planar transistor বেয়াড়া হয়ে গেল, আর সমাধানটা আপনার আঁকার কিছু স্বাধীনতা
            কেড়ে নিল। কেন, physics-এর তিনটা বাক্যে দেখি।
            """,
        ))
        self.clear()
        a = text("Planar: any W, any L, on a fine grid.", size=44, weight="SEMIBOLD").move_to(UP * 0.5)
        b = text("Then L kept shrinking.", size=34, color=GATE).next_to(a, DOWN, buff=0.5)
        self.play(FadeIn(a))
        self.play(FadeIn(b, shift=UP * 0.1))

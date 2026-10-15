"""Layout edition · L5 · Squeezing n and p together: the forksheet and the CFET (roadmap).

A wall between n and p; n stacked on p; four inverter cells at one scale; what stacking would
mean for layout. Then the labs: Build a cell, Hold it yourself.
"""

import sys
from pathlib import Path

LECTURE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(LECTURE.parents[1]), str(LECTURE), str(LECTURE / "layout")]

from manim import *  # noqa: E402,F403
from manim_slides import Slide  # noqa: E402

from common import card_box  # noqa: E402
from devicedata import device, rail_span_nm  # noqa: E402
from kit.devices3d import LAYOUT_OPACITY, plan_view  # noqa: E402
from kit.motifs import xsection  # noqa: E402
from kit.style import *  # noqa: E402,F403

CELLS = [("show_fin", "FinFET"), ("show_ns", "nanosheet"), ("show_fs", "forksheet"), ("show_cfet", "CFET")]


def view_of(key, scale):
    """FET Lab's inverter layout, from above, without the field oxide and the deep well."""
    skip = {p["id"] for p in device(key)["parts"] if p["material"] == "fox" or p["id"] in ("pwell", "bild")}
    return plan_view(device(key), scale=scale, skip=skip, opacity=LAYOUT_OPACITY)


class L05ForkCFET(Chapter, Slide):
    def construct(self):
        self.card()
        self.forksheet()
        self.cfet()
        self.cells()
        self.what_it_means()

    def card(self):
        self.slide(say(
            """
            Chapter five: two devices that aren't in products yet. They're on imec's roadmap,
            and the dates are projections. Both go after the space between n and p.
            """,
            """
            Chapter five: দুইটা device যেগুলা এখনো product-এ আসে নাই। এগুলা imec-এর roadmap-এ আছে, আর date-গুলা অনুমান।
            দুইটাই n আর p-এর মাঝের জায়গাটার পিছে লাগছে।
            """,
        ))
        self.card_group = self.open_chapter(5, 2030, 2022, "Squeezing n and p together", "Forksheet and CFET: on the roadmap")

    def forksheet(self):
        span = rail_span_nm("show_fs")
        self.slide(say(
            f"""
            The forksheet. Put a thin insulating wall between the n sheets and the p sheets, and
            push both right up against it. The gate wraps three sides of each sheet, and the
            wall takes the fourth. The n-to-p space shrinks to little more than the wall, and in
            FET Lab's model the inverter cell drops to {span:.0f} nanometres, rail to rail. imec
            has also proposed putting the wall at the cell's edge instead, between neighbouring
            cells; that outer-wall version is the one on its roadmap, around 2030.
            """,
            f"""
            Forksheet। n sheet আর p sheet-এর মাঝে একটা পাতলা insulating wall দেন, আর দুইটারেই একদম তার গায়ে ঠেলে দেন। Gate
            প্রত্যেক sheet-এর তিন দিক ঘিরে, আর চার নম্বর দিকটা wall নেয়। n-to-p space নেমে আসে প্রায় wall-এর সমান, আর FET
            Lab-এর model-এ inverter cell নামে {span:.0f} nanometre-এ, rail থেকে rail। imec wall-টা cell-এর কিনারায়, পাশাপাশি
            cell-গুলার মাঝে বসানোর প্রস্তাবও দিছে; roadmap-এ প্রায় 2030-এ ওই outer-wall version-টাই আছে।
            """,
        ))
        self.play(FadeOut(self.card_group))
        title = heading("The forksheet: a wall between n and p")
        xs = xsection("forksheet").scale(1.4).move_to([-4.6, 0.2, 0])
        xs_l = text("cut across the gate", size=20, color=MUTED).next_to(xs, DOWN, buff=0.3)
        wall_l = text("the wall", size=22, color=WALL).next_to(xs, UP, buff=0.2)
        v, by = view_of("show_fs", 0.03)
        v.move_to([0.6, -0.4, 0])
        v_l = text(f"from above: {span:.0f} nm rail to rail (model)", size=20, color=MUTED).next_to(v, DOWN, buff=0.2)
        words = VGroup(text("n and p sheets pushed\nagainst one wall", size=24, weight="SEMIBOLD"),
                       text("the n-to-p space becomes\nlittle more than the wall", size=22, color=INK),
                       text("on imec's roadmap, around 2030,\nwith the wall at the cell edge\n(the outer-wall forksheet)",
                            size=20, color=MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.9, 0.2, 0])
        words.shift(RIGHT * (2.55 - words.get_left()[0]))
        self.play(FadeIn(title), FadeIn(xs), FadeIn(xs_l), FadeIn(wall_l))
        self.play(FadeIn(v), FadeIn(v_l), FadeIn(words[0]))
        self.play(FadeIn(words[1]))
        self.play(FadeIn(words[2]))

    def cfet(self):
        span = rail_span_nm("show_cfet")
        self.slide(say(
            f"""
            The CFET goes further: it stacks the n transistor right on top of the p. From above,
            the pair looks like one device. Their gates are one gate, and contacts run vertically
            between the tiers. In FET Lab's model the inverter is {span:.0f} nanometres rail to
            rail, under half the FinFET's, and its power rails are on the back. imec's roadmap puts
            it around 2033.
            """,
            f"""
            CFET আরও এক ধাপ যায়: n transistor-রে সোজা p-এর উপরে বসায়। উপর থেকে জোড়াটা একটা device-এর মতো দেখায়। দুইটার
            gate আসলে একটা gate, আর contact tier-গুলার মাঝে খাড়া চলে। FET Lab-এর model-এ inverter rail থেকে rail {span:.0f}
            nanometre, FinFET-এর অর্ধেকেরও কম, আর power rail পেছনে। imec-এর roadmap এইটারে রাখছে প্রায় 2033-এ।
            """,
        ))
        self.clear()
        title = heading("The CFET: n stacked on p")
        xs = xsection("cfet").scale(1.25).move_to([-4.6, 0.0, 0])
        n_l = text("n, on top", size=20, color=ELECTRON).next_to(xs, RIGHT, buff=0.15).shift(UP * 0.8)
        p_l = text("p, below", size=20, color=HOLE).next_to(xs, RIGHT, buff=0.15).shift(DOWN * 0.55)
        xs_l = text("cut across the gate", size=20, color=MUTED).next_to(xs, DOWN, buff=0.3)
        v, by = view_of("show_cfet", 0.034)
        v.move_to([0.9, -0.3, 0])
        v_l = text(f"from above: {span:.0f} nm rail to rail (model)", size=20, color=MUTED).next_to(v, DOWN, buff=0.25)
        words = VGroup(text("one footprint for\nthe n and the p", size=24, weight="SEMIBOLD"),
                       text("one shared gate; vertical\ncontacts between the tiers;\npower rails on the back", size=22, color=INK),
                       text("on imec's roadmap,\naround 2033", size=20, color=MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        words.move_to([5.0, 0.1, 0])
        self.play(FadeIn(title), FadeIn(xs), FadeIn(xs_l), FadeIn(n_l), FadeIn(p_l))
        self.play(FadeIn(v), FadeIn(v_l), FadeIn(words[0]))
        self.play(FadeIn(words[1]))
        self.play(FadeIn(words[2]))

    def cells(self):
        self.slide(say(
            """
            Now line up all four inverter cells from FET Lab, at one scale. FinFET, nanosheet,
            forksheet, CFET: 156, 136, 106 and 74 nanometres, rail to rail. These are schematic
            models, not any foundry's cells, but the trend is the point. Every step took away
            some of the space between n and p, and the cell got shorter.
            """,
            """
            এবার FET Lab-এর চারটা inverter cell একসাথে, একই scale-এ। FinFET, nanosheet, forksheet, CFET: 156, 136, 106 আর 74
            nanometre, rail থেকে rail। এগুলা schematic model, কোনো foundry-র cell না, কিন্তু আসল কথা trend-টা। প্রত্যেক ধাপে n আর
            p-এর মাঝের জায়গার কিছুটা গেছে, আর cell ছোট হইছে।
            """,
        ))
        self.clear()
        title = heading("Four inverters, one scale")
        views = VGroup()
        for key, name in CELLS:
            v, by = view_of(key, 0.022)
            r0 = by["m0_gnd"].get_center()[1] if "m0_gnd" in by else by["bm_gnd"].get_center()[1]
            r1 = by["m0_vdd"].get_center()[1] if "m0_vdd" in by else by["bm_vdd"].get_center()[1]
            x = v.get_left()[0] - 0.2
            arrow = DoubleArrow([x, r0, 0], [x, r1, 0], buff=0, stroke_color=GATE, stroke_width=4, tip_length=0.12)
            lbl = VGroup(text(name, size=24, color=MUTED), text(f"{rail_span_nm(key):.0f} nm", size=26, color=GATE, weight="SEMIBOLD"))
            lbl.arrange(DOWN, buff=0.08).next_to(v, DOWN, buff=0.2)
            views.add(VGroup(v, arrow, lbl))
        views.arrange(RIGHT, buff=0.7, aligned_edge=DOWN).move_to([0, -0.4, 0])
        tag = text("FET Lab's schematic inverter layouts (models), rail centre to rail centre. The CFET's rails are on the back.",
                   size=16, color=MUTED).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(title), FadeIn(tag))
        for v in views:
            self.play(FadeIn(v, shift=UP * 0.1), run_time=0.8)

    def what_it_means(self):
        self.slide(say(
            """
            What would this mean for layout, if it arrives? With a forksheet, n and p sit closer,
            and the wall becomes something you place, with its own rules. With a CFET, the
            pull-up and the pull-down share one footprint: a cell is drawn more like one device
            than two, connections that used to run sideways between n and p run up and down
            between tiers, and the wiring lives on both sides of the wafer. Both are roadmap, so
            treat this as direction, not rules. Next, the two live labs.
            """,
            """
            এইগুলা আসলে layout-এর জন্য কী মানে হবে? Forksheet-এ n আর p আরও কাছে বসে, আর wall হয়ে যায় এমন একটা জিনিস যেটা
            আপনি বসান, তার নিজের rule সহ। CFET-এ pull-up আর pull-down একটা footprint share করে: একটা cell আঁকা হয় দুইটা device-এর
            চেয়ে একটার মতো করে, যে connection আগে n আর p-এর মাঝে পাশাপাশি চলত সেগুলা tier-এর মাঝে উপর-নিচে চলে, আর wiring থাকে
            wafer-এর দুই দিকেই। দুইটাই roadmap, তাই এইটারে rule না, দিক হিসাবে নেন। এরপর দুইটা live lab।
            """,
        ))
        self.clear()
        title = heading("If they arrive: what changes for layout")
        cards = VGroup(
            card_box("Forksheet", [text("n and p closer;\nthe wall is something\nyou place, with rules", size=22, color=INK)],
                     width=5.2, height=3.0),
            card_box("CFET", [text("pull-up and pull-down in\none footprint; n-to-p links\nrun between tiers; wiring\non both sides of the wafer",
                                   size=22, color=INK)], width=5.2, height=3.0),
        ).arrange(RIGHT, buff=0.6).move_to([0, -0.1, 0])
        tag = text("roadmap: direction, not rules", size=22, color=MUTED, slant="ITALIC").to_edge(DOWN, buff=0.8)
        self.play(FadeIn(title))
        for c in cards:
            self.play(FadeIn(c, shift=UP * 0.15), run_time=0.7)
        self.play(FadeIn(tag))

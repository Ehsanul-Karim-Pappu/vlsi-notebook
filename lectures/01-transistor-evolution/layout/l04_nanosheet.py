"""Layout edition · L4 · Width is drawn again: the nanosheet.

Sheets in 3D, cut; from above, the active is a drawn rectangle again; the width you get for it;
what you size; the cell and its n-to-p space; power from the back of the wafer.
"""

import sys
from pathlib import Path

LECTURE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(LECTURE.parents[1]), str(LECTURE), str(LECTURE / "layout")]

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403
from manim_slides import ThreeDSlide  # noqa: E402

import physics as phys  # noqa: E402
from common import ACTIVE, METAL, knob_table, pdk_tag  # noqa: E402
from devicedata import NANOSHEET, device, rail_span_nm  # noqa: E402
from kit.devices3d import LAYOUT_OPACITY, beside, build_device, plan_view  # noqa: E402
from kit.style import *  # noqa: E402,F403

CHANNEL = "#7FD8E4"  # the channel sheets, picked out from the rest of the silicon
N_SH, W_SH, T_SH = 3, 30, 5  # FET Lab's nanosheet model, nm
LAYOUT_FIN, LAYOUT_NS = device("show_fin"), device("show_ns")


class L04Nanosheet(Chapter, ThreeDSlide):
    def construct(self):
        self.card()
        self.model()
        self.from_above()
        self.width()
        self.knobs()
        self.cell()
        self.backside()

    def flat(self):
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0, frame_center=ORIGIN)

    def card(self):
        self.slide(say(
            """
            Chapter four: the nanosheet, in production since 2022. Turn the fin on its side,
            slice it into thin sheets, stack them, and wrap the gate all the way around each
            one. For layout, the headline is simple: you draw the width again.
            """,
            """
            Chapter four: nanosheet, 2022 থেকে production-এ। Fin-রে কাত করে শোয়ান, পাতলা sheet-এ কাটেন, একটার উপর আরেকটা
            রাখেন, আর প্রত্যেকটার চারপাশ ঘিরে gate দেন। Layout-এর জন্য মূল খবর সোজা: width আবার আপনি আঁকেন।
            """,
        ))
        self.card_group = self.open_chapter(4, 2022, 2011, "Width is drawn again", "The nanosheet, from the layout side")

    def model(self):
        self.slide(say(
            """
            Here's FET Lab's nanosheet transistor, cut across through the gate. Three sheets of
            silicon, 5 nanometres thick and 30 wide, stacked with gaps between them. The gate
            fills every gap, so it wraps all four sides of every sheet. That's the most grip a
            gate can have on a silicon channel.
            """,
            """
            এই যে FET Lab-এর nanosheet transistor, gate-এর মাঝখান দিয়া আড়াআড়ি কাটা। তিনটা silicon sheet, 5 nanometre পুরু
            আর 30 চওড়া, মাঝে ফাঁক রেখে একটার উপর আরেকটা। Gate প্রত্যেকটা ফাঁক ভরে, তাই প্রত্যেকটা sheet-এর চার দিক ঘিরে
            থাকে। Silicon channel-এর উপর gate-এর এর চেয়ে বেশি grip হয় না।
            """,
        ))
        self.play(FadeOut(self.card_group))
        self.set_camera_orientation(phi=64 * DEGREES, theta=-58 * DEGREES, zoom=0.75, frame_center=beside(-58 * DEGREES, -1.6))
        order = ["Substrate & isolation", "Channel stack", "Gate-all-around stack", "Gate electrode", "Spacers", "Source / drain"]
        contacts = {"gatew", "nisi_source", "ni_source", "w_source", "nisi_drain", "ni_drain", "w_drain"}
        kw = dict(scale=0.05, groups=order, skip=contacts, recolor={f"sheet{i}": CHANNEL for i in (1, 2, 3)})
        back, _ = build_device(NANOSHEET, clip={"x": (None, 0.0)}, **kw)
        front, _ = build_device(NANOSHEET, clip={"x": (0.0, None)}, **kw)
        shift = -VGroup(back, front).get_center() + np.array([0, 0, -0.2])
        back.shift(shift)
        front.shift(shift)
        src = source("Model: FET Lab's nanosheet nFET (5 nm sheets, 30 nm wide)")
        info = VGroup(text("cut across the gate", size=26, color=GATE),
                      text("three sheets, stacked;\nthe gate on all four\nsides of every sheet", size=26, weight="SEMIBOLD"),
                      ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([4.6, 0.4, 0])
        self.add_fixed_in_frame_mobjects(src, info)
        self.remove(src, info)
        self.play(FadeIn(VGroup(back, front), shift=IN * 0.6), FadeIn(src), run_time=1.5)
        self.play(FadeOut(front, shift=RIGHT * 3), FadeIn(info[0]), run_time=1.6)
        self.move_camera(phi=82 * DEGREES, theta=-4 * DEGREES, zoom=0.95, frame_center=beside(-4 * DEGREES, -1.8), run_time=2.5)
        self.play(FadeIn(info[1]))
        self.parts3d = VGroup(back, src, info)

    def from_above(self):
        self.slide(say(
            """
            From above, the difference is plain. Left, the FinFET inverter: two narrow fins per
            transistor. Right, the nanosheet inverter: one sheet per transistor, and its width
            is the width of the shape you draw. The gates, the contacts and the rails look the
            same. The stack under it, how many sheets and how thick, is fixed by the process.
            """,
            """
            উপর থেকে পার্থক্যটা পরিষ্কার। বামে FinFET inverter: প্রত্যেক transistor-এ দুইটা সরু fin। ডানে nanosheet inverter:
            প্রত্যেক transistor-এ একটা sheet, আর তার width হইলো আপনার আঁকা shape-এর width। Gate, contact আর rail দেখতে একই।
            নিচের stack, কয়টা sheet আর কতটা পুরু, সেইটা process ঠিক করে।
            """,
        ))
        self.play(FadeOut(self.parts3d))
        self.flat()
        title = heading("From above: one drawn sheet")
        skip = ("pwell", "fox", "vd_gnd", "vd_vdd", "vd_out", "vg", "m0_in", "m0_out")
        fin, _ = plan_view(LAYOUT_FIN, scale=0.029, skip=skip, opacity=LAYOUT_OPACITY)
        ns, ns_by = plan_view(LAYOUT_NS, scale=0.029, skip=skip, opacity=LAYOUT_OPACITY)
        fin.move_to([-3.2, -0.4, 0])
        ns.move_to([3.2, -0.4, 0]).align_to(fin, DOWN)
        fl = text("FinFET: 2 fins each", size=24, color=MUTED).next_to(fin, DOWN, buff=0.2)
        nl = text("nanosheet: 1 drawn sheet each", size=24, color=ACTIVE).next_to(ns, DOWN, buff=0.2)
        w = ns_by["p_w1"]
        wb = BraceBetweenPoints(w.get_corner(DR) + RIGHT * 0.9, w.get_corner(UR) + RIGHT * 0.9, direction=RIGHT, color=ACTIVE)
        wl = text("drawn\nwidth", size=20, color=ACTIVE).next_to(wb, RIGHT, buff=0.08)
        self.play(FadeIn(title))
        self.play(FadeIn(fin), FadeIn(fl))
        self.play(FadeIn(ns), FadeIn(nl))
        self.play(FadeIn(wb), FadeIn(wl))

    def width(self):
        w0 = phys.weff_sheets_nm(N_SH, W_SH, T_SH)
        w1 = phys.weff_sheets_nm(N_SH, 45, T_SH)
        self.slide(say(
            f"""
            And the width you get: current flows on all four faces of every sheet, so each
            sheet is worth twice its width plus twice its thickness, times the number of sheets.
            Three sheets, 30 by 5, give {w0:.0f} nanometres. Draw the sheet wider, say 45, and
            it's {w1:.0f}, with no step in between. The number of sheets and their thickness are
            the process's; the width is yours again, within the range your PDK allows.
            """,
            f"""
            আর যে width পান: প্রত্যেকটা sheet-এর চার মুখ দিয়াই current যায়, তাই প্রত্যেক sheet-এর দাম দুইগুণ width যোগ
            দুইগুণ thickness, গুণ sheet-এর সংখ্যা। তিনটা sheet, 30 বাই 5, দেয় {w0:.0f} nanometre। Sheet চওড়া আঁকেন, ধরেন 45,
            তখন {w1:.0f}, মাঝে কোনো ধাপ নাই। Sheet-এর সংখ্যা আর thickness process-এর; width আবার আপনার, PDK যতটুকু range দেয়
            তার ভিতরে।
            """,
        ))
        self.clear()
        title = heading("The width you get")
        u, cx, y0 = 0.05, -3.0, -2.2
        wt = ValueTracker(W_SH)

        def stack():
            w = wt.get_value() * u
            g = VGroup(Rectangle(width=w + 16 * u, height=(3 * 21 + 6) * u, fill_color=GATE, fill_opacity=0.25,
                                 stroke_color=GATE, stroke_width=2).move_to([cx, y0 + (3 * 21 + 6) * u / 2, 0]))
            for i in range(N_SH):
                yc = y0 + (8 + i * 21 + T_SH / 2) * u
                g.add(Rectangle(width=w, height=T_SH * u, fill_color=CHANNEL, fill_opacity=1, stroke_width=0).move_to([cx, yc, 0]))
                g.add(Rectangle(width=w + 0.1, height=T_SH * u + 0.1, stroke_color=ELECTRON, stroke_width=4).move_to([cx, yc, 0]))
            return g

        pic = always_redraw(stack)
        wlab = always_redraw(lambda: text(f"sheet width {wt.get_value():.0f} nm", size=22, color=ACTIVE)
                             .move_to([cx, y0 - 0.4, 0]))
        rule = VGroup(text("each sheet ≈ 2 × (width + thickness)", size=26),
                      text(f"× {N_SH} sheets (the process's)", size=24, color=MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        rule.move_to([3.0, 1.3, 0])
        val = always_redraw(lambda: text(f"= {phys.weff_sheets_nm(N_SH, wt.get_value(), T_SH):.0f} nm", size=40,
                                         color=ELECTRON, weight="SEMIBOLD").next_to(rule, DOWN, buff=0.35).align_to(rule, LEFT))
        foot = text("no steps: any width within the PDK's range", size=24, color=GOOD).move_to([3.0, -1.2, 0])
        self.play(FadeIn(title), FadeIn(pic), FadeIn(wlab), FadeIn(rule), FadeIn(val))
        self.play(wt.animate.set_value(45), run_time=2.2)
        self.play(FadeIn(foot))
        self.play(wt.animate.set_value(W_SH), run_time=1.4)
        self.wait(0.4)

    def knobs(self):
        self.slide(say(
            """
            So the sizing table gets a third column. Width: a drawn sheet width again, but
            within limits: a minimum and a maximum, and in many processes a set of allowed
            values. Changing the width along a row usually comes with rules of its own.
            Length, fingers and multipliers work as they did on FinFET. As before,
            this is typical, and the PDK is the authority.
            """,
            """
            তো sizing table-এ তৃতীয় একটা column আসে। Width: আবার একটা আঁকা sheet width, কিন্তু সীমার ভিতরে: একটা minimum
            আর একটা maximum, আর অনেক process-এ নির্দিষ্ট কিছু মানের তালিকা। এক row-তে width বদলানোর জন্যও সাধারণত আলাদা rule থাকে। Length, finger আর multiplier FinFET-এর মতোই। আগের মতো, এইটা typical, আর শেষ কথা PDK-র।
            """,
        ))
        self.clear()
        title = heading("What you size, now")
        table = knob_table([
            ["", "planar", "FinFET", "nanosheet"],
            ["width", "W, any", "whole fins", "drawn sheet width,\nwithin a range"],
            ["length", "L, any", "a few lengths", "a few lengths"],
            ["fingers, copies", "nf, m", "nf, m", "nf, m"],
            ["fixed for you", "—", "fin height, pitch", "sheet count, thickness"],
        ], col_w=(2.9, 2.2, 3.0, 3.6), size=24).move_to([0, -0.1, 0])
        tag = pdk_tag().next_to(table, DOWN, buff=0.5)
        self.play(FadeIn(title), FadeIn(table[0][0]), FadeIn(table[1]))
        for row in table[0][1:]:
            self.play(FadeIn(row, shift=UP * 0.1), run_time=0.6)
        self.play(FadeIn(tag))

    def cell(self):
        span = rail_span_nm("show_ns")
        self.slide(say(
            f"""
            Now the cell. Its height is set by the routing above it: the number of metal tracks
            times the metal pitch. In FET Lab's nanosheet inverter, the rails sit {span:.0f}
            nanometres apart. And look inside: the space between the n sheet and the p sheet,
            46 nanometres here, a third of the cell. It's hard to shrink, because n and p need
            different gate metals, patterned apart with margin. That space is what the next two
            devices go after.
            """,
            f"""
            এবার cell। এর height ঠিক হয় উপরের routing দিয়া: metal track-এর সংখ্যা গুণ metal pitch। FET Lab-এর nanosheet
            inverter-এ rail দুইটা {span:.0f} nanometre দূরে। আর ভিতরে দেখেন: n sheet আর p sheet-এর মাঝের জায়গা, এইখানে 46
            nanometre, cell-এর তিন ভাগের এক ভাগ। এইটা কমানো কঠিন, কারণ n আর p-এর আলাদা gate metal লাগে, যেগুলারে margin
            রেখে আলাদা করে pattern করতে হয়। পরের দুইটা device ঠিক এই জায়গাটার পিছে লাগছে।
            """,
        ))
        self.clear()
        title = heading("The cell, and the space between n and p")
        view, by = plan_view(LAYOUT_NS, scale=0.031, skip=("pwell", "fox"), opacity=LAYOUT_OPACITY)
        view.move_to([-2.9, -0.45, 0])
        n_top, p_bot = by["n_w1"].get_top()[1], by["p_w1"].get_bottom()[1]
        x = by["m0_vdd"].get_right()[0] + 0.3
        gap = DoubleArrow([x, n_top, 0], [x, p_bot, 0], buff=0, stroke_color=DRAIN, stroke_width=4, tip_length=0.14)
        gap_l = text("n-to-p space\n46 nm (model)", size=20, color=DRAIN).next_to(gap, RIGHT, buff=0.12)
        r0, r1 = by["m0_gnd"].get_center()[1], by["m0_vdd"].get_center()[1]
        xl = by["m0_gnd"].get_left()[0] - 0.3
        h = DoubleArrow([xl, r0, 0], [xl, r1, 0], buff=0, stroke_color=GATE, stroke_width=4, tip_length=0.14)
        h_l = text(f"rail to rail {span:.0f} nm (model)", size=20, color=GATE).rotate(PI / 2).next_to(h, LEFT, buff=0.1)
        words = VGroup(text("cell height = tracks × metal pitch", size=24, weight="SEMIBOLD"),
                       text(f"e.g. 6 tracks × 24 nm = {phys.cell_height_nm(6, 24)} nm", size=22, color=MUTED),
                       text("n and p need different gate metals,\npatterned apart: the space between\nthem is hard to shrink",
                            size=22, color=INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.4, 0.2, 0])
        words.shift(RIGHT * (1.5 - words.get_left()[0]))
        tag = text("Schematic: FET Lab's nanosheet inverter layout (model)", size=16, color=MUTED).next_to(view, DOWN, buff=0.2)
        self.play(FadeIn(title), FadeIn(view), FadeIn(tag))
        self.play(GrowFromCenter(h), FadeIn(h_l), FadeIn(words[0]), FadeIn(words[1]))
        self.play(GrowFromCenter(gap), FadeIn(gap_l), FadeIn(words[2]))

    def backside(self):
        self.slide(say(
            """
            One more change arrives with nanosheets, and it touches your floorplan: power from
            the back. Normally the power rails share the front-side metal with every signal, and
            they're thin, so they drop voltage. Backside power moves the rails under the wafer,
            where they can be thick, and brings power up to the transistors from below. Intel
            ships it in its 18A process, as PowerVia; TSMC has announced it for A16. For you, the
            front-side metal is left mostly for signals, the cell's power connections move, and
            where taps and power vias go becomes a new set of rules.
            """,
            """
            Nanosheet-এর সাথে আরেকটা বদল আসে, আর সেইটা আপনার floorplan ছোঁয়: পেছন থেকে power। সাধারণত power rail
            সামনের metal-এ সব signal-এর সাথে জায়গা ভাগ করে, আর পাতলা হয়, তাই voltage কমায়। Backside power rail-গুলারে
            wafer-এর নিচে নিয়া যায়, যেখানে মোটা হইতে পারে, আর নিচ থেকে transistor পর্যন্ত power তুলে আনে। Intel এইটা ship
            করতেছে ওদের 18A process-এ, নাম PowerVia; TSMC A16-এর জন্য ঘোষণা দিছে। আপনার জন্য: সামনের metal মূলত signal-এর
            জন্য থাকে, cell-এর power connection সরে যায়, আর tap আর power via কোথায় যাবে সেইটা নতুন একগুচ্ছ rule।
            """,
        ))
        self.clear()
        title = heading("Power from the back of the wafer")
        dev = Rectangle(width=6.0, height=0.55, fill_color=SILICON, fill_opacity=0.45, stroke_width=0).move_to([-3.0, 0.0, 0])
        dev_l = text("transistors", size=22, color=INK).move_to(dev)
        front = VGroup(*[Line([-5.8, 0.55 + 0.32 * i, 0], [-0.2, 0.55 + 0.32 * i, 0], stroke_color=METAL, stroke_width=3 + i)
                         for i in range(6)])
        front_l = text("front: mostly signal wiring", size=22, color=METAL).next_to(front, UP, buff=0.15)
        back = VGroup(*[Rectangle(width=1.1, height=0.55, fill_color=THERMAL, fill_opacity=0.8, stroke_width=0)
                        .move_to([-5.2 + 1.55 * i, -0.75, 0]) for i in range(4)])
        back_l = text("back: thick power rails", size=22, color=THERMAL).next_to(back, DOWN, buff=0.2)
        vias = VGroup(*[Line([b.get_x(), -0.47, 0], [b.get_x(), -0.27, 0], stroke_color=THERMAL, stroke_width=5) for b in back])
        facts = VGroup(text("Intel 18A: PowerVia, in production", size=24, color=GOOD),
                       text("TSMC: announced for A16", size=24, color=MUTED),
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.4, 1.2, 0])
        note = layout_note("The front-side metal is left mostly for signals; the cell's power connections move "
                           "below; where taps and power vias go follows new rules from the process.", size=21, width=44)
        note.move_to([3.4, -1.0, 0])
        tag = text("illustrative side view", size=16, color=MUTED).to_corner(DL, buff=0.3)
        self.play(FadeIn(title), FadeIn(dev), FadeIn(dev_l), FadeIn(tag))
        self.play(Create(front), FadeIn(front_l))
        self.play(FadeIn(back, shift=UP * 0.2), Create(vias), FadeIn(back_l))
        self.play(FadeIn(facts))
        self.play(FadeIn(note, shift=UP * 0.15))

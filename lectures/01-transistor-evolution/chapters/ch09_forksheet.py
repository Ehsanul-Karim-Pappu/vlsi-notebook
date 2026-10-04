"""Chapter 9 · Forksheet: a wall between n and p (2017–, projected for about 2030).

The n and p sheet stacks pushed against a thin insulating wall (the original inner-wall
design), and the outer-wall variant on imec's roadmap. Each sheet gives one face to the wall; in
imec's 2021 devices that cost little measured control, and it buys a shorter cell. Optional on
the core path.
"""

import sys
from pathlib import Path

LECTURE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(LECTURE.parents[1]), str(LECTURE)]

from manim import *  # noqa: E402,F403
from manim_slides import ThreeDSlide  # noqa: E402

from devicedata import device, rail_span_nm  # noqa: E402
from kit.devices3d import LAYOUT_OPACITY, beside, build_device, plan_view  # noqa: E402
from kit.motifs import xsection  # noqa: E402
from kit.style import *  # noqa: E402,F403

IMAGES = LECTURE / "images"
CHANNEL = "#7FD8E4"
P_CHANNEL = "#E88BB8"  # the pFET's sheets, picked out in the hole colour
FORK = device("fs")
LAYOUT_NS, LAYOUT_FS = device("show_ns"), device("show_fs")


class Ch09Forksheet(Chapter, ThreeDSlide):
    def construct(self):
        self.card()
        self.history()
        self.model()
        self.tradeoff()
        self.area()
        self.cliffhanger()

    def flat(self):
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0, frame_center=ORIGIN)

    # --- chapter card ------------------------------------------------------------------------
    def card(self):
        self.slide(say(
            """
            This chapter and the next are about transistors that aren't in products yet: they're
            on the roadmap. The dates are projections, not facts. First, the forksheet. If you're
            short of time, this one can be skipped.
            """,
            """
            এই chapter আর পরেরটা এমন transistor নিয়া, যেগুলা এখনো product-এ আসে নাই: roadmap-এ আছে। Date-গুলা
            অনুমান, fact না। প্রথমে forksheet। সময় কম থাকলে এইটা বাদ দেওয়া যায়।
            """,
        ))
        self.card_group = self.open_chapter(9, 2030, 2022, "Forksheet", "A wall between n and p (projected)")

    # --- history -----------------------------------------------------------------------------
    def history(self):
        self.slide(say(
            """
            The forksheet comes from imec, the research centre in Belgium. They proposed it in
            2017, with the wall inside the cell, between the n and the p: the inner-wall
            forksheet. In 2021 they built working ones with the n and p transistors just 17
            nanometres apart, each with its own gate metal. imec's roadmap now has a different
            version, with the wall at the edge of the cell between two transistors of the same
            type, called the outer-wall forksheet, at around the A10 node: roughly 2030, if the
            roadmap holds.
            """,
            """
            Forksheet আসছে imec থেকে, Belgium-এর research centre। ওরা 2017-এ এইটা প্রস্তাব করে, wall-টা cell-এর ভিতরে,
            n আর p-এর মাঝখানে: inner-wall forksheet। 2021-এ ওরা চালু forksheet বানায়, n আর p transistor মাত্র 17
            nanometre দূরে, প্রত্যেকটার নিজের gate metal সহ। imec-এর roadmap-এ এখন একটা আলাদা version আছে, যেখানে wall-টা
            cell-এর কিনারায়, একই type-এর দুইটা transistor-এর মাঝে, নাম outer-wall forksheet, মোটামুটি A10 node-এ: roadmap
            ঠিক থাকলে প্রায় 2030।
            """,
        ))
        self.play(FadeOut(self.card_group))
        title = heading("An idea from imec")
        line = Line([-5.6, -0.2, 0], [5.6, -0.2, 0], stroke_color=FAINT, stroke_width=3)
        events = [
            (-4.4, "2017", "imec proposes it", "inner wall: n | p,\nfor denser cells", "P. Weckx et al., IEDM 2017", "forksheet"),
            (0.0, "2021", "Working forksheets", "n and p just 17 nm\napart, two gate metals", "H. Mertens et al., VLSI 2021", "forksheet"),
            (4.4, "~2030", "On the roadmap", "outer wall: n | n at the\ncell edge, imec's A10 node", "imec roadmap, 2025 (projection)", "forksheet_outer"),
        ]
        self.play(FadeIn(title), Create(line))
        for x, year, what, why, who, kind in events:
            dot = Dot([x, -0.2, 0], color=GATE, radius=0.1)
            y = display(year, size=48, color=GATE).move_to([x, 0.75, 0])
            body = VGroup(text(what, size=26, weight="SEMIBOLD"), text(why, size=22, color=MUTED),
                          text(who, size=16, color=MUTED)).arrange(DOWN, buff=0.15).next_to(dot, DOWN, buff=0.4)
            icon = xsection(kind).scale_to_fit_height(0.75).next_to(y, UP, buff=0.3)
            self.play(FadeIn(dot, scale=0.5), FadeIn(y), FadeIn(icon), FadeIn(body, shift=UP * 0.1), run_time=0.9)

        fig = figure(IMAGES / "forksheet_US11862700_fig12.png", 5.2,
                     "TSMC, US patent 11,862,700 (granted 2024), Fig. 12, a stage during manufacture:\n"
                     "sheet stacks, dielectric walls, and a sacrificial gate (142) that is replaced later")
        fig.move_to([0, -0.4, 0])
        self.show_figure(say(
            """
            And the foundries are patenting their own versions. This is from a TSMC patent granted
            in 2024, at a stage partway through manufacture: stacks of sheets, the striped layers,
            with thin dielectric walls standing between them. The block coming down over the top
            is a sacrificial gate, number 142, a placeholder. Like the dummy gate in the last
            chapter, it's pulled out and replaced by the real gate later.
            """,
            """
            আর foundry-গুলাও নিজেদের version patent করতেছে। এইটা 2024-এ grant হওয়া TSMC-র একটা patent থেকে, বানানোর
            মাঝপথের একটা ধাপ: sheet-এর stack, ডোরাকাটা layer-গুলা, মাঝে মাঝে পাতলা dielectric wall দাঁড়ানো। উপর দিয়া যে
            block-টা নেমে আসছে সেটা একটা sacrificial gate, নম্বর 142, জায়গা ধরে রাখার জন্য। আগের chapter-এর dummy gate-এর
            মতোই, পরে এইটা তুলে আসল gate বসানো হয়।
            """,
        ), "A forksheet patent", fig, clear=VGroup(*self.mobjects))
        self.fig = fig

    # --- the 3D model ------------------------------------------------------------------------
    def model(self):
        self.slide(say(
            """
            Here's the forksheet in 3D, the inner-wall kind: an n and a p transistor side by side.
            Down the middle, the wall: silicon nitride, 8 nanometres thick. The n sheets, in blue, are pressed
            against one side of it, the p sheets, in pink, against the other. One gate runs
            across both, with a different gate metal on each side.
            """,
            """
            এই যে 3D-তে forksheet, inner-wall ধরনের: একটা n আর একটা p transistor পাশাপাশি। মাঝখান বরাবর wall: silicon
            nitride, 8 nanometre পুরু। n sheet-গুলা, নীল রঙে, এর এক পাশে চাপা, p sheet-গুলা, গোলাপি, অন্য পাশে। একটা gate দুইটার
            উপর দিয়াই যায়, দুই পাশে দুই রকম gate metal।
            """,
        ))
        self.play(FadeOut(self.fig), FadeOut(VGroup(*[m for m in self.mobjects if m is not self.fig])))
        self.set_camera_orientation(phi=64 * DEGREES, theta=-58 * DEGREES, zoom=0.72, frame_center=beside(-58 * DEGREES, 1.5))
        order = ["Substrate & isolation", "Dielectric wall", "Channel stacks", "Forked gate films", "Gate electrode",
                 "Spacers", "Source / drain"]
        captions = ["the wafer and isolation", "the wall: SiN, 8 nm", "n sheets (blue) and p sheets (pink)",
                    "gate films: a different metal for n and p", "gate", "spacers", "sources and drains"]
        skip = {p["id"] for p in FORK["parts"] if p["id"].startswith(("nisi_", "ni_", "liner_", "cpw_"))} | {"gatew"}
        recolor = {f"sheet_n{i}": CHANNEL for i in (1, 2, 3)} | {f"sheet_p{i}": P_CHANNEL for i in (1, 2, 3)}
        kw = dict(scale=0.045, groups=order, skip=skip, recolor=recolor)
        back, back_g = build_device(FORK, clip={"x": (None, 0.0)}, **kw)
        front, front_g = build_device(FORK, clip={"x": (0.0, None)}, **kw)
        shift = -VGroup(back, front).get_center()
        back.shift(shift)
        front.shift(shift)
        lst = VGroup(*[text(c, size=20, color=MUTED) for c in captions]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        lst.to_corner(UL, buff=0.5)
        src = source("Model: FET Lab's forksheet pair (5 nm sheets, 8 nm wall), after imec EP 3 989 273 A1")
        self.add_fixed_in_frame_mobjects(lst, src)
        self.remove(lst, src)
        self.play(FadeIn(src))
        for i, name in enumerate(order):
            item = lst[i]
            self.play(FadeIn(VGroup(back_g[name], front_g[name]), shift=IN * 0.8), FadeIn(item),
                      *([lst[i - 1].animate.set_color(MUTED)] if i else []), run_time=0.9)
        self.play(lst[-1].animate.set_color(MUTED), run_time=0.3)

        self.slide(say(
            """
            Cut it across the gate. There's the wall, and there are the sheets touching it.
            Look at each sheet: the gate wraps the top, the bottom and the outer side, but not the
            side against the wall. Three faces, not four. The forksheet gives up a face to save
            space.
            """,
            """
            Gate-এর মাঝখান দিয়া আড়াআড়ি কাটেন। এই যে wall, আর এই যে sheet-গুলা ওইটা ছুঁয়ে আছে। প্রত্যেকটা sheet
            দেখেন: gate উপরে, নিচে আর বাইরের দিকে মুড়ে আছে, কিন্তু wall-এর দিকটায় না। চার দিক না, তিন দিক।
            Forksheet জায়গা বাঁচাইতে একটা দিক ছেড়ে দেয়।
            """,
        ))
        info = VGroup(text("cut across the gate", size=26, color=GATE),
                      text("p sheets  |  wall  |  n sheets", size=24, weight="SEMIBOLD"),
                      text("each sheet: gate on\nthree faces, not four", size=24),
                      ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([4.5, 0.5, 0])
        self.add_fixed_in_frame_mobjects(info)
        self.remove(info)
        self.play(FadeOut(front, shift=RIGHT * 3), FadeOut(lst), FadeIn(info[0]), run_time=1.6)
        self.move_camera(phi=82 * DEGREES, theta=-4 * DEGREES, zoom=0.95, frame_center=beside(-4 * DEGREES, -1.8), run_time=2.5)
        self.play(FadeIn(info[1:]))
        self.parts3d = VGroup(back, src, info)

    # --- the trade -----------------------------------------------------------------------
    def tradeoff(self):
        self.slide(say(
            """
            How much grip does that cost? Counting faces, as in our toy model, you'd guess a
            little. But the face count is a toy, and the real answer depends on the exact shape:
            how wide the sheets are, how thick, where the wall sits. So look at a measurement.
            imec's 2021 forksheets switched with 66 to 68 millivolts per decade, about as sharply
            as the nanosheets they built alongside them, with gates down to 22 nanometres. In
            those devices, at least, the price was small.
            """,
            """
            এতে grip কতটা যায়? আমাদের toy model-এর মতো দিক গুনলে মনে হবে, একটু। কিন্তু দিক গোনা একটা toy, আসল উত্তর
            নির্ভর করে ঠিক আকারের উপর: sheet কত চওড়া, কত পুরু, wall কোথায় বসা। তাই একটা measurement দেখি। imec-এর 2021-এর
            forksheet 66 থেকে 68 millivolt per decade-এ switch করছে, পাশাপাশি বানানো nanosheet-এর প্রায় সমান তীক্ষ্ণভাবে,
            22 nanometre পর্যন্ত gate-এ। অন্তত ওই device-গুলাতে দামটা কম ছিল।
            """,
        ))
        self.play(FadeOut(self.parts3d))
        self.flat()
        title = heading("Three faces instead of four")
        cols = VGroup()
        for kind, name in (("nanosheet", "nanosheet: four faces"), ("forksheet", "forksheet: three faces")):
            pic = xsection(kind).scale_to_fit_height(2.4)
            cols.add(VGroup(pic, text(name, size=26, weight="SEMIBOLD")).arrange(DOWN, buff=0.4))
        cols.arrange(RIGHT, buff=2.4).move_to([0, 0.35, 0])
        meas = VGroup(text("Measured, imec 2021: SS = 66–68 mV/dec,", size=24, color=GOOD),
                      text("comparable to nanosheets built alongside them", size=24, color=GOOD),
                      text("H. Mertens et al., VLSI 2021; those devices and dimensions, not every forksheet", size=16, color=MUTED),
                      ).arrange(DOWN, buff=0.12).next_to(cols, DOWN, buff=0.5)
        self.play(FadeIn(title), FadeIn(cols[0]))
        self.play(FadeIn(cols[1], shift=LEFT * 0.2))
        self.play(FadeIn(meas, shift=UP * 0.1))

    def area(self):
        self.slide(say(
            """
            And what does it buy? Here are FET Lab's two inverter layouts at the same scale. The
            nanosheet cell, rail to rail: 136 nanometres in this model. The forksheet: 106. About a
            fifth shorter, because the n-to-p space is now just the wall. These are schematic
            models, not a foundry's cells. And this is the inner-wall layout. imec's newer
            outer-wall variant moves the wall to the edge of the cell. There it stands between
            two transistors of the same type, from neighbouring cells, so it can be thicker and
            easier to build, and the gate can wrap part of the way round the wall side too. They
            are two different structures; the one on the roadmap for 2030 is the outer wall.
            """,
            """
            আর বিনিময়ে কী পাই? এই যে FET Lab-এর দুইটা inverter layout, একই scale-এ। Nanosheet cell, rail থেকে rail: এই
            model-এ 136 nanometre। Forksheet: 106। প্রায় পাঁচ ভাগের এক ভাগ ছোট, কারণ n-to-p space এখন শুধু wall-টা। এগুলা
            schematic model, কোনো foundry-র cell না। আর এইটা inner-wall layout। imec-এর নতুন outer-wall variant wall-টারে
            cell-এর কিনারায় নিয়া যায়। সেখানে এইটা পাশের cell-এর একই type-এর দুইটা transistor-এর মাঝে দাঁড়ায়, তাই এইটা
            আরও পুরু আর বানানো সহজ হইতে পারে, আর gate wall-এর দিকটাতেও খানিকটা মুড়ে যাইতে পারে। এই দুইটা আলাদা structure;
            2030-এর roadmap-এ যেটা আছে সেটা outer wall।
            """,
        ))
        self.clear()
        title = heading("What the wall buys: a shorter cell")
        skip = ("pwell", "fox", "vd_gnd", "vd_vdd", "vd_out", "vd_out2", "vg", "m0_in", "m0_out", "m0_out_jog")
        ns, ns_by = plan_view(LAYOUT_NS, scale=0.03, skip=skip, opacity=LAYOUT_OPACITY)
        fs, fs_by = plan_view(LAYOUT_FS, scale=0.03, skip=skip, opacity=LAYOUT_OPACITY)
        ns.move_to([-4.0, -0.1, 0])
        fs.move_to([-0.6, -0.1, 0]).align_to(ns, DOWN)

        def span(by, key, view):
            y0, y1 = by["m0_gnd"].get_center()[1], by["m0_vdd"].get_center()[1]
            x = view.get_left()[0] - 0.3
            return DoubleArrow([x, y0, 0], [x, y1, 0], buff=0, stroke_color=GATE, stroke_width=4, tip_length=0.14)

        s1, s2 = span(ns_by, "show_ns", ns), span(fs_by, "show_fs", fs)
        l1 = VGroup(text("nanosheet", size=24, color=MUTED), text(f"{rail_span_nm('show_ns'):.0f} nm", size=26, color=GATE, weight="SEMIBOLD"))
        l2 = VGroup(text("forksheet", size=24, color=MUTED), text(f"{rail_span_nm('show_fs'):.0f} nm", size=26, color=GATE, weight="SEMIBOLD"))
        l1.arrange(DOWN, buff=0.08).next_to(ns, DOWN, buff=0.2)
        l2.arrange(DOWN, buff=0.08).next_to(fs, DOWN, buff=0.2)
        wall = fs_by["wall"]
        wall_l = text("← wall", size=20, color=WALL).next_to(fs, RIGHT, buff=0.12).set_y(wall.get_y())
        cut = 1 - rail_span_nm("show_fs") / rail_span_nm("show_ns")
        res = VGroup(display(f"−{cut * 100:.0f}%", size=60, color=GOOD), text("cell height (model)", size=22, color=MUTED)).arrange(DOWN, buff=0.1)
        res.move_to([4.5, 1.6, 0])
        variants = VGroup()
        for kind, name, what in (("forksheet", "inner wall", "n | p,\ninside the cell\n(this layout)"),
                                 ("forksheet_outer", "outer wall", "n | n or p | p,\nat the cell edge\n(roadmap)")):
            icon = xsection(kind).scale_to_fit_height(1.05)
            variants.add(VGroup(icon, text(name, size=22, weight="SEMIBOLD"), text(what, size=17, color=MUTED))
                         .arrange(DOWN, buff=0.12))
        variants.arrange(RIGHT, buff=0.6, aligned_edge=UP).move_to([4.4, -0.45, 0])
        note = text("Schematic models, not foundry cells", size=18, color=MUTED).next_to(variants, DOWN, buff=0.35)
        self.play(FadeIn(title), FadeIn(ns), FadeIn(l1), FadeIn(s1))
        self.play(FadeIn(fs), FadeIn(l2), FadeIn(s2))
        self.play(Indicate(wall, color=INK), FadeIn(wall_l))
        self.play(FadeIn(res))
        self.play(FadeIn(variants[0]), FadeIn(note))
        self.play(FadeIn(variants[1], shift=LEFT * 0.15))

    # --- cliffhanger -------------------------------------------------------------------------
    def cliffhanger(self):
        self.slide(say(
            """
            But why put n and p side by side at all? We've shrunk the space between them down to
            a wall. The next step removes the space completely: put one on top of the other.
            """,
            """
            কিন্তু n আর p-রে পাশাপাশি রাখতেই হবে কেন? মাঝের জায়গা কমাইতে কমাইতে একটা wall-এ নামাইছি। পরের ধাপ জায়গাটাই
            পুরা সরায়ে দেয়: একটারে আরেকটার উপরে বসান।
            """,
        ))
        self.clear()
        a = text("Why side by side? Stack them.", size=46, weight="SEMIBOLD").to_edge(UP, buff=0.7)
        fs = xsection("forksheet").scale(1.2).move_to([0, -1.1, 0])
        cf = xsection("cfet").scale(1.2).move_to([0, -0.9, 0])
        self.play(FadeIn(a), FadeIn(fs))
        self.wait(0.4)
        self.play(ReplacementTransform(fs, cf), run_time=2.0)
        self.wait(1)

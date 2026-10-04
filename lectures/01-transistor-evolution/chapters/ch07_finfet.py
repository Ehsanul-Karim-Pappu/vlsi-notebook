"""Chapter 7 · Stand it up: the FinFET (1989–2011).

The channel turned on its edge, gated on three faces. Its width comes in whole fins, its
layout lives on fixed grids, and its fin can't get much thinner or taller.
"""

import sys
from pathlib import Path

LECTURE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(LECTURE.parents[1]), str(LECTURE)]

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403
from manim_slides import ThreeDSlide  # noqa: E402

import physics as phys  # noqa: E402
from devicedata import device  # noqa: E402
from kit.devices3d import LAYOUT_OPACITY, beside, build_device, plan_view  # noqa: E402
from kit.motifs import xsection  # noqa: E402
from kit.style import *  # noqa: E402,F403

IMAGES = LECTURE / "images"
FIN = device("fin")
LAYOUT = device("show_fin")
H_FIN, W_FIN, PITCH, L_G = 45, 6, 27, 18  # FET Lab's FinFET model, nm


class Ch07FinFET(Chapter, ThreeDSlide):
    def construct(self):
        self.card()
        self.history()
        self.model()
        self.cutaway()
        self.width()
        self.whole_fins()
        self.layout()
        self.three_nm()
        self.limits()
        self.cliffhanger()

    def flat(self):
        """Back to a flat, 2D view after a 3D slide."""
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0, frame_center=ORIGIN)



    # --- chapter card ------------------------------------------------------------------------
    def card(self):
        self.slide(say(
            """
            If you can't put a gate underneath a flat channel, stop making the channel flat. The
            idea is older than you might think: it took more than twenty years to go from a lab
            curiosity to the chip in your laptop.
            """,
            """
            Flat channel-এর নিচে gate বসানো না গেলে, channel-রে আর flat বানায়েন না। Idea-টা যতটা মনে হয় তার চেয়ে
            পুরান: lab-এর একটা কৌতূহল থেকে আপনার laptop-এর chip পর্যন্ত আসতে বিশ বছরের বেশি লাগছে।
            """,
        ))
        self.card_group = self.open_chapter(7, 2011, 2007, "Stand it up", "The FinFET: a gate on three sides")

    # --- history -----------------------------------------------------------------------------
    def history(self):
        self.slide(say(
            """
            1989: at Hitachi, Digh Hisamoto and colleagues build DELTA, a thin wall of silicon
            standing up on the wafer, gated from both sides. In the late 1990s, DARPA asks for a
            transistor that will still work at 25 nanometres, and a Berkeley team, Chenming Hu,
            Tsu-Jae King and Jeffrey Bokor among them, comes back with the FinFET, named for its
            shape. And in May 2011, Intel announces that its 22 nanometre chips will use it,
            calling it the tri-gate transistor, because the gate covers three sides. The first
            ones ship in 2012.
            """,
            """
            1989: Hitachi-তে Digh Hisamoto আর তার সহকর্মীরা বানান DELTA, wafer-এর উপর খাড়া দাঁড়ানো silicon-এর একটা পাতলা
            দেয়াল, দুই পাশ থেকে gate দেওয়া। 1990-এর দশকের শেষে DARPA এমন একটা transistor চায় যেটা 25 nanometre-এও
            কাজ করবে, আর Berkeley-র একটা team, তার মধ্যে Chenming Hu, Tsu-Jae King আর Jeffrey Bokor, নিয়া আসে FinFET,
            নামটা এর আকৃতি থেকে। আর 2011-এর May-তে Intel ঘোষণা দেয় যে ওদের 22 nanometre chip-এ এইটা থাকবে, নাম দেয়
            tri-gate transistor, কারণ gate তিন দিক ঢাকে। প্রথমগুলা ship হয় 2012-এ।
            """,
        ))
        self.play(FadeOut(self.card_group))
        title = heading("Twenty-two years from idea to product")
        line = Line([-5.6, -0.2, 0], [5.6, -0.2, 0], stroke_color=FAINT, stroke_width=3)
        events = [
            (-4.4, "1989", "Hitachi: DELTA", "a thin silicon wall,\ngated from both sides", "D. Hisamoto et al., IEDM 1989"),
            (0.0, "1998–99", "UC Berkeley: the FinFET", "for DARPA's push\nto 25 nm", "C. Hu, T.-J. King, J. Bokor et al."),
            (4.4, "2011", "Intel: 22 nm tri-gate", "the first FinFETs\nin production (2012)", "announced May 2011"),
        ]
        self.play(FadeIn(title), Create(line))
        for x, year, what, why, who in events:
            dot = Dot([x, -0.2, 0], color=GATE, radius=0.1)
            y = display(year, size=48, color=GATE).move_to([x, 0.75, 0])
            body = VGroup(text(what, size=26, weight="SEMIBOLD"), text(why, size=22, color=MUTED),
                          text(who, size=16, color=MUTED)).arrange(DOWN, buff=0.15).next_to(dot, DOWN, buff=0.4)
            fin = self.fin_icon(0.5).next_to(y, UP, buff=0.3)
            self.play(FadeIn(dot, scale=0.5), FadeIn(y), FadeIn(fin), FadeIn(body, shift=UP * 0.1), run_time=0.9)

        fig = figure(IMAGES / "hu_finfet_US6413802_fig1.png", 4.3,
                     "C. Hu, T.-J. King, J. Bokor et al. (University of California), US patent 6,413,802, filed 2000, Fig. 1: a double-gate FinFET")
        fig.move_to([0, -0.35, 0])
        self.show_figure(say(
            """
            Here's the Berkeley patent, filed in 2000. Look at figure 1: a source and a drain, and
            between them a thin silicon fin standing up on the wafer. The gate runs over the fin
            and down both sides, but a thick hard mask sits on the fin's top, so the gate controls
            the two sidewalls: a double-gate FinFET. Intel's tri-gate, a decade later, let the top
            conduct as well.
            """,
            """
            এই যে Berkeley-র patent, 2000-এ file করা। Figure 1 দেখেন: একটা source আর একটা drain, আর মাঝে wafer-এর উপর
            খাড়া একটা পাতলা silicon fin। Gate fin-এর উপর দিয়া গিয়া দুই পাশ বেয়ে নামছে, কিন্তু fin-এর মাথায় একটা মোটা hard
            mask বসানো, তাই gate control করে দুইটা sidewall: একটা double-gate FinFET। দশ বছর পরে Intel-এর tri-gate
            fin-এর মাথা দিয়াও current চালাইছে।
            """,
        ), "The FinFET patent, 2000", fig, clear=VGroup(*[m for m in self.mobjects]))
        self.fig = fig

    def fin_icon(self, h):
        """A small fin under its gate, for the timeline."""
        fin = Rectangle(width=0.16 * h, height=h, fill_color=SILICON, fill_opacity=1, stroke_width=0)
        gate = Rectangle(width=0.8 * h, height=0.7 * h, fill_color=GATE, fill_opacity=0.85, stroke_width=0)
        gate.move_to(fin.get_top() + DOWN * 0.25 * h)
        return VGroup(fin, gate)

    # --- the 3D model ------------------------------------------------------------------------
    def model(self):
        self.slide(say(
            """
            Here's a FinFET in 3D, built the way it's made. The silicon wafer, with oxide
            isolation. Two fins, each 6 nanometres wide and standing 45 above the oxide. The
            gate's films: a thin oxide, high-k, and the metal that sets the threshold voltage.
            The gate itself. Insulating spacers. And the source and drain, grown onto the ends of
            the fins.
            """,
            """
            এই যে 3D-তে একটা FinFET, যেভাবে বানানো হয় সেভাবে। Silicon wafer, oxide isolation সহ। দুইটা fin, প্রত্যেকটা
            6 nanometre চওড়া, oxide-এর উপরে 45 উঁচু। Gate-এর film-গুলা: পাতলা oxide, high-k, আর যে metal threshold
            voltage ঠিক করে। তারপর gate নিজে। Insulating spacer। আর source আর drain, fin-গুলার মাথায় grow করা।
            """,
        ))
        self.play(FadeOut(self.fig), FadeOut(VGroup(*[m for m in self.mobjects if m is not self.fig])))
        self.set_camera_orientation(phi=64 * DEGREES, theta=-58 * DEGREES, zoom=0.78, frame_center=beside(-58 * DEGREES, 2.3))
        order = ["Substrate & isolation", "Fins", "Tri-gate films", "Gate electrode", "Spacers", "Source / drain"]
        captions = [
            "the silicon wafer and oxide isolation",
            f"two fins: {W_FIN} nm wide, {H_FIN} nm tall",
            "gate films: oxide, high-k, work-function metal",
            "gate",
            "insulating spacers",
            "source and drain",
        ]
        kw = dict(scale=0.05, groups=order)
        back, back_g = build_device(FIN, clip={"x": (None, 0.0)}, **kw)
        front, front_g = build_device(FIN, clip={"x": (0.0, None)}, **kw)
        shift = -VGroup(back, front).get_center() + np.array([0, 0, -0.2])
        back.shift(shift)
        front.shift(shift)
        lst = VGroup(*[text(c, size=20, color=MUTED) for c in captions]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        lst.to_corner(UL, buff=0.5)
        src = source("Model: FET Lab's FinFET nFET (18 nm gate, 6 nm fins, 27 nm fin pitch), after TSMC US 9,812,358")
        self.add_fixed_in_frame_mobjects(lst, src)
        self.remove(lst, src)
        self.play(FadeIn(src))
        for i, name in enumerate(order):
            item = lst[i]
            self.play(FadeIn(VGroup(back_g[name], front_g[name]), shift=IN * 0.8), FadeIn(item),
                      *([lst[i - 1].animate.set_color(MUTED)] if i else []), run_time=1.0)
            self.play(item.animate.set_color(INK), run_time=0.3)
        self.play(lst[-1].animate.set_color(MUTED), run_time=0.3)
        self.back, self.front, self.labels3d = back, front, VGroup(lst, src)

    def cutaway(self):
        self.slide(say(
            """
            Now cut it across, right through the gate, and look at the cut face. There are the two
            fins, and the gate wraps over the top and down both sides of each one: three faces
            instead of one. In the toy model of the last chapter, N is roughly three. With a 6
            nanometre fin, lambda comes out at about 2.4 nanometres, and this model's 18 nanometre
            gate is about seven lambda long. The grip is back.
            """,
            """
            এবার এইটারে আড়াআড়ি কাটেন, ঠিক gate-এর মাঝখান দিয়া, আর কাটা মুখটা দেখেন। এই যে দুইটা fin, আর gate
            প্রত্যেকটার উপর দিয়া আর দুই পাশ দিয়া মুড়ে আছে: এক দিকের বদলে তিন দিক। আগের chapter-এর ভাষায়, N প্রায়
            তিন, মোটামুটি। 6 nanometre fin-এ lambda আসে প্রায় 2.4 nanometre, আর এই model-এর 18 nanometre gate প্রায় সাত
            lambda লম্বা। Grip ফিরে আসছে।
            """,
        ))
        lam = phys.natural_length_nm(W_FIN, 1, 3)
        cut = text("cut across the gate", size=26, color=GATE)
        info = VGroup(cut, text("the gate covers three\nfaces of each fin", size=26, weight="SEMIBOLD"),
                      MathTex(r"N \approx 3", font_size=36, color=GATE),
                      MathTex(rf"\lambda \approx {lam:.1f}\ \text{{nm}}", font_size=36, color=GATE),
                      MathTex(rf"L_G = {L_G}\ \text{{nm}} \approx {L_G / lam:.0f}\lambda", font_size=36, color=GATE),
                      ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([4.6, 0.3, 0])
        self.add_fixed_in_frame_mobjects(info)
        self.remove(info)
        self.play(FadeOut(self.front, shift=RIGHT * 3), FadeOut(self.labels3d[0]), FadeIn(cut), run_time=1.6)
        self.move_camera(phi=82 * DEGREES, theta=-4 * DEGREES, zoom=1.05, frame_center=beside(-4 * DEGREES, -1.6), run_time=2.5)
        self.play(FadeIn(info[1:]))
        self.wait(0.5)
        self.cut_parts = VGroup(self.back, self.labels3d[1], info)

        self.slide(say(
            """
            Take a moment with this view. Silicon fins, then the thin oxide and high-k, then the
            work-function metal, then the gate fill. Every face of the fin that touches the gate
            carries current.
            """,
            """
            এই view-টা একটু দেখেন। Silicon fin, তারপর পাতলা oxide আর high-k, তারপর work-function metal, তারপর gate
            fill। Fin-এর যে মুখগুলা gate ছোঁয়, সবগুলা দিয়াই current যায়।
            """,
        ), loop=True)
        self.move_camera(theta=-22 * DEGREES, frame_center=beside(-22 * DEGREES, -1.6), run_time=3, rate_func=rate_functions.ease_in_out_sine)
        self.move_camera(theta=-4 * DEGREES, frame_center=beside(-4 * DEGREES, -1.6), run_time=3, rate_func=rate_functions.ease_in_out_sine)

    # --- width -------------------------------------------------------------------------------
    def width(self):
        self.slide(say(
            """
            So what's the width of a FinFET? Current flows from source to drain along the fin, in
            a thin layer on every face the gate touches: both sidewalls and the top. To get the
            width, trace that perimeter: up one sidewall, across the top, down the other. So each
            fin is worth two heights plus its width: 96 nanometres here. Two fins, 192, on two fin
            pitches of floor. Notice what happened: the fin is tall and thin, so you get a lot of
            width from very little floor space. Most of it is standing up.
            """,
            """
            তাহলে FinFET-এর width কত? Current যায় source থেকে drain-এ, fin বরাবর, gate যে মুখগুলা ছোঁয় তার প্রত্যেকটার
            গায়ে একটা পাতলা layer-এ: দুইটা sidewall আর top। Width পাইতে ওই perimeter-টা ধরে যান: এক sidewall বেয়ে উপরে,
            top পার হয়ে, অন্য পাশ দিয়া নিচে। তাই প্রত্যেকটা fin-এর দাম দুইটা height যোগ তার width: এইখানে 96 nanometre।
            দুইটা fin, 192, দুইটা fin pitch-এর জায়গায়। কী হইলো খেয়াল করেন: fin লম্বা আর পাতলা, তাই অল্প জায়গায় অনেক width
            পাওয়া যায়। বেশিরভাগটা খাড়া দাঁড়ায়ে আছে।
            """,
        ))
        self.play(FadeOut(self.cut_parts))
        self.flat()
        title = heading("The width of a fin")
        u = 0.055  # scene units per nm
        base_y = -1.9
        sti = Rectangle(width=110 * u, height=12 * u, fill_color=OXIDE, fill_opacity=0.9, stroke_width=0).move_to([-2.6, base_y - 6 * u, 0])
        sub = Rectangle(width=110 * u, height=14 * u, fill_color=SUBSTRATE, fill_opacity=1, stroke_width=0).next_to(sti, DOWN, buff=0)
        fins, walls = VGroup(), VGroup()
        for k in (-0.5, 0.5):
            x = -2.6 + k * PITCH * u
            f = Rectangle(width=W_FIN * u, height=H_FIN * u, fill_color=SILICON, fill_opacity=1, stroke_width=0)
            f.move_to([x, base_y + H_FIN * u / 2, 0])
            fins.add(f)
            l, r, t = f.get_left()[0], f.get_right()[0], f.get_top()[1]
            path = VMobject(stroke_color=ELECTRON, stroke_width=7).set_points_as_corners(
                [[l - 0.04, base_y, 0], [l - 0.04, t + 0.04, 0], [r + 0.04, t + 0.04, 0], [r + 0.04, base_y, 0]])
            walls.add(path)
        gate = Rectangle(width=80 * u, height=(H_FIN + 14) * u, fill_color=GATE, fill_opacity=0.25, stroke_color=GATE,
                         stroke_width=2).move_to([-2.6, base_y + (H_FIN + 14) * u / 2, 0])
        gate_l = text("gate", size=22, color=GATE).next_to(gate, UP, buff=0.1)
        h_br = BraceBetweenPoints(fins[0].get_corner(DL) + LEFT * 0.08, fins[0].get_corner(UL) + LEFT * 0.08, direction=LEFT, color=MUTED)
        h_l = MathTex(rf"H_{{fin}} = {H_FIN}", font_size=30, color=MUTED).next_to(h_br, LEFT, buff=0.1)
        w_l = MathTex(rf"W_{{fin}} = {W_FIN}", font_size=30, color=MUTED).next_to(fins[1], UP, buff=0.12)
        p_l = text(f"fin pitch {PITCH} nm", size=20, color=MUTED).next_to(sub, DOWN, buff=0.15)
        weff = phys.weff_fin_nm(2, H_FIN, W_FIN)
        e1 = eq(r"W_{eff}", r"=", r"N_{fin}", r"\,(2H_{fin}+W_{fin})", size=48)
        e1[0].set_color(ELECTRON)
        e2 = eq(r"=", rf"2\times(2\cdot{H_FIN}+{W_FIN})", r"=", rf"{weff}\ \text{{nm}}", size=44)
        e2[3].set_color(ELECTRON)
        e3 = text(f"on two fin pitches ({2 * PITCH} nm) of floor", size=26, color=MUTED)
        VGroup(e1, e2, e3).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([3.3, 0.5, 0])
        self.play(FadeIn(title), FadeIn(sub), FadeIn(sti), FadeIn(fins), FadeIn(gate), FadeIn(gate_l))
        self.play(FadeIn(h_br), FadeIn(h_l), FadeIn(w_l), FadeIn(p_l))
        self.play(Create(walls), run_time=2.0)
        self.play(Write(e1))
        self.play(Write(e2))
        self.play(FadeIn(e3))

    def whole_fins(self):
        self.slide(say(
            """
            But there's a catch, and it changed how you draw. Every fin is the same height. So
            the width comes in steps of one fin: 96, 192, 288 nanometres. Nothing in between. On a
            planar transistor you drew any W you liked. On a FinFET, you choose a number of
            fins.
            """,
            """
            কিন্তু একটা প্যাঁচ আছে, আর এইটা আঁকার নিয়মই বদলায়ে দিছে। সব fin-এর height একই। তাই width আসে এক fin করে
            ধাপে ধাপে: 96, 192, 288 nanometre। মাঝখানে কিছু নাই। Planar transistor-এ যেকোনো W আঁকতে পারতেন। FinFET-এ
            আপনি বাছেন কয়টা fin।
            """,
        ))
        self.clear()
        title = heading("Width comes in whole fins")
        ax = Axes(x_range=[0, 420, 100], y_range=[0, 5, 1], x_length=10, y_length=4.2, tips=False,
                  axis_config={"stroke_color": MUTED, "stroke_width": 2, "include_ticks": False}).move_to([0, -0.5, 0])
        ax.x_axis.add_labels({v: text(str(v), size=18, color=MUTED) for v in (0, 100, 200, 300, 400)}, font_size=18)
        x_l = text("effective width (nm)", size=22, color=MUTED).next_to(ax.x_axis, DOWN, buff=0.45)
        planar = Line(ax.c2p(0, 1), ax.c2p(420, 1), stroke_color=MUTED, stroke_width=6)
        planar_l = text("planar: any width you draw", size=22, color=MUTED).next_to(planar, UP, buff=0.12).align_to(planar, LEFT)
        per = phys.weff_fin_nm(1, H_FIN, W_FIN)
        dots = VGroup(*[Dot(ax.c2p(n * per, 2.6), color=ELECTRON, radius=0.12) for n in (1, 2, 3, 4)])
        lbls = VGroup(*[text(f"{n} fin{'s' if n > 1 else ''}\n{n * per} nm", size=18, color=ELECTRON).next_to(d, UP, buff=0.15)
                        for n, d in zip((1, 2, 3, 4), dots)])
        fin_l = text("FinFET: whole fins only", size=22, color=ELECTRON).next_to(ax.c2p(0, 2.6), RIGHT, buff=0.1).shift(DOWN * 0.45)
        self.play(FadeIn(title), Create(ax), FadeIn(x_l))
        self.play(Create(planar), FadeIn(planar_l))
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.25), FadeIn(lbls), FadeIn(fin_l), run_time=1.6)

    # --- layout ------------------------------------------------------------------------------
    def layout(self):
        self.slide(say(
            """
            Here's what that does to a layout. A FinFET inverter seen from above, the way your
            layout tool shows it. The fins run left to right, on one fixed pitch, everywhere on
            the chip: you can't move a fin, you can only use it or cut it. The gates run up and
            down, also on one fixed pitch. Then the contacts, and metal zero with the power rails.
            This is why FinFET layout feels like painting by numbers: everything snaps to a grid.
            """,
            """
            Layout-এ এর ফল দেখেন। উপর থেকে দেখা একটা FinFET inverter, আপনার layout tool যেভাবে দেখায়। Fin-গুলা বাম
            থেকে ডানে চলে, একটা fixed pitch-এ, পুরা chip জুড়ে: fin সরানো যায় না, শুধু use করা যায় বা কাটা যায়। Gate-গুলা
            উপর-নিচে চলে, ওইগুলাও একটা fixed pitch-এ। তারপর contact, আর power rail সহ metal zero। এই কারণেই FinFET layout
            মনে হয় সংখ্যা মিলায়ে রং করার মতো: সবকিছু grid-এ বসে।
            """,
        ))
        self.clear()
        title = heading("A FinFET inverter, from above")
        view, by = plan_view(LAYOUT, scale=0.031, skip=("pwell", "fox"), opacity=LAYOUT_OPACITY)
        view.move_to([-3.6, -0.45, 0])
        layers = [
            ("wells", ["pwell_u", "nwell"]),
            ("fins, on a 27 nm pitch", [p["id"] for p in LAYOUT["parts"] if p["material"] == "nanowire"]),
            ("gate (poly)", ["po"]),
            ("contacts and vias", ["md_gnd", "md_vdd", "md_out", "vd_gnd", "vd_vdd", "vd_out", "vg"]),
            ("metal 0: rails, IN and OUT", ["m0_gnd", "m0_in", "m0_out", "m0_vdd"]),
        ]
        names = VGroup(*[text(n, size=20, color=MUTED) for n, _ in layers]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        names.move_to([2.7, 2.1, 0])
        vdd = text("V_DD", size=20, color=INK).next_to(by["m0_vdd"], LEFT, buff=0.15)
        gnd = text("GND", size=20, color=INK).next_to(by["m0_gnd"], LEFT, buff=0.15)
        pm = text("pMOS\n2 fins", size=18, color=MUTED).next_to(by["nwell"], LEFT, buff=0.55).shift(UP * 0.1)
        nm = text("nMOS\n2 fins", size=18, color=MUTED).next_to(by["pwell_u"], LEFT, buff=0.55).shift(DOWN * 0.1)
        tag = text("Schematic: FET Lab's FinFET inverter layout (model)", size=16, color=MUTED).next_to(view, DOWN, buff=0.2)
        self.play(FadeIn(title), FadeIn(tag))
        for (name, ids), lbl in zip(layers, names):
            self.play(*[FadeIn(by[i]) for i in ids if i in by], FadeIn(lbl), run_time=0.8)
        self.play(FadeIn(vdd), FadeIn(gnd), FadeIn(pm), FadeIn(nm))
        note = layout_note("You don't draw W any more: you pick a number of fins. A 1 : 2 current mirror is "
                           "2 fins and 4 fins, never 1.5. Fins and gates snap to fixed pitches, and dummy gates "
                           "at the ends keep every device's surroundings alike.", size=21, width=44)
        note.move_to([3.2, -1.15, 0])
        self.play(FadeIn(note, shift=UP * 0.15))

    # --- what does "3 nm" measure? -----------------------------------------------------------
    def three_nm(self):
        self.slide(say(
            """
            A quick myth while we're here. What does "3 nanometres" measure on a 3 nanometre chip?
            Not any one physical dimension. Here's the roadmap's 3 nanometre node, to scale: gates
            on a 48 nanometre pitch, the tightest metal on a 24 nanometre pitch. And here's 3
            nanometres: this dot. Node names stopped tracking the gate length in the late 1990s.
            Today they're labels for a generation, meaning "the next one".
            """,
            """
            এই ফাঁকে একটা ভুল ধারণা। 3 nanometre chip-এ "3 nanometre" কী মাপে? কোনো একটা নির্দিষ্ট physical মাপ না। এই যে
            roadmap-এর 3 nanometre node, scale মেনে আঁকা: gate 48 nanometre pitch-এ, সবচেয়ে চাপা metal 24 nanometre
            pitch-এ। আর এই হইলো 3 nanometre: এই ছোট্ট dot-টা। 1990-এর দশকের শেষ থেকেই node-এর নাম আর gate length-এর সাথে
            মিলে না। এখন এগুলা একটা generation-এর label, মানে "পরেরটা"।
            """,
        ))
        self.clear()
        title = heading("What does \"3 nm\" measure?")
        u = 0.045  # units per nm, the same for everything on the slide
        gates = VGroup(*[Rectangle(width=16 * u, height=4.6, fill_color=po_color(), fill_opacity=0.8, stroke_width=0)
                         .move_to([-6.0 + i * 48 * u, -0.7, 0]) for i in range(3)])
        g_br = BraceBetweenPoints(gates[0].get_center() + UP * 2.4, gates[1].get_center() + UP * 2.4, direction=UP, color=GATE)
        g_l = text("gate pitch 48 nm", size=22, color=GATE).next_to(g_br, UP, buff=0.08)
        metals = VGroup(*[Rectangle(width=12 * u, height=4.6, fill_color="#F2C1A2", fill_opacity=0.6, stroke_width=0)
                          .move_to([0.0 + i * 24 * u, -0.7, 0]) for i in range(5)])
        m_br = BraceBetweenPoints(metals[0].get_center() + UP * 2.4, metals[1].get_center() + UP * 2.4, direction=UP, color="#F2C1A2")
        m_l = text("metal pitch 24 nm", size=22, color="#F2C1A2").next_to(m_br, UP, buff=0.08)
        three = Square(side_length=3 * u, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([5.9, -0.7, 0])
        three_l = text("3 nm", size=26, color=INK, weight="SEMIBOLD").move_to([5.9, 1.0, 0])
        three_a = Arrow(three_l.get_bottom(), three.get_top(), buff=0.1, stroke_color=INK, stroke_width=3, tip_length=0.15)
        three_l = VGroup(three_l, three_a)
        cap = text("IRDS 2021 More Moore roadmap, \"3 nm\" ground rules (G48M24), to scale: a roadmap target, not a measured chip.\n"
                   "TSMC at IEDM 2022: N3, 45 nm contacted gate pitch; N3E, 23 nm minimum metal pitch.",
                   size=16, color=MUTED).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(title))
        self.play(FadeIn(gates), FadeIn(g_br), FadeIn(g_l))
        self.play(FadeIn(metals), FadeIn(m_br), FadeIn(m_l))
        self.play(FadeIn(three, scale=3), FadeIn(three_l))
        self.play(Indicate(three, color=GATE, scale_factor=3), FadeIn(cap))

    # --- limits ------------------------------------------------------------------------------
    def limits(self):
        self.slide(say(
            """
            The FinFET carried the industry for a decade, from 22 nanometres down to 3. But the
            fin ran out of room. It's hard to make much thinner: in very thin silicon, atom-scale
            fluctuations in the thickness scatter the electrons, and theory puts that part of the
            mobility at about the sixth power of the thickness, so going from 5 to 4 nanometres
            would cost it about three quarters. Other effects push the other way, and real mobility
            depends on the details, but thinner keeps getting harder: confinement also shifts the
            threshold, and variation grows. It can't easily get taller: tall, thin fins are hard to
            etch straight, and they add capacitance. And the width still comes in whole fins.
            """,
            """
            FinFET দশ বছর industry-রে টানছে, 22 nanometre থেকে 3 পর্যন্ত। কিন্তু fin-এর জায়গা ফুরায়ে গেল। এইটা আরও
            পাতলা করা কঠিন: খুব পাতলা silicon-এ thickness-এর atom-মাপের ওঠানামা electron-গুলারে ছিটকায়ে দেয়, আর theory বলে
            mobility-র ওই অংশ thickness-এর প্রায় sixth power হারে চলে, তাই 5 থেকে 4 nanometre-এ গেলে ওই অংশের প্রায় চার ভাগের
            তিন ভাগ যাবে। অন্য কিছু effect উল্টা দিকে টানে, আর আসল mobility খুঁটিনাটির উপর নির্ভর করে, কিন্তু যত পাতলা তত
            কঠিন: confinement threshold-ও সরায়, আর variation বাড়ে। সহজে আরও উঁচুও হইতে পারে না: লম্বা পাতলা fin সোজা করে
            etch করা কঠিন, আর capacitance বাড়ায়। আর width এখনো whole fin-এ আসে।
            """,
        ))
        self.clear()
        title = heading("Where the fin runs out of room")
        r = phys.roughness_mobility_ratio(4, 5)
        cards = VGroup(
            self.card_box("Hard to get thinner", [
                MathTex(r"\mu_{rough}\ \propto\ t^6", font_size=40, color=ELECTRON),
                text(f"5 → 4 nm: ×{r:.2f}", size=24, color=DRAIN),
                text("one part of the mobility (theory);\nillustrative", size=16, color=MUTED)]),
            self.card_box("Can't easily get taller", [
                text("tall, thin fins are hard\nto etch straight, and\nadd capacitance", size=22, color=INK)]),
            self.card_box("Width in whole fins", [
                text("96, 192, 288 nm …", size=24, color=ELECTRON),
                text("nothing in between", size=22, color=MUTED)]),
        ).arrange(RIGHT, buff=0.45).move_to([0, -0.3, 0])
        self.play(FadeIn(title))
        for c in cards:
            self.play(FadeIn(c, shift=UP * 0.15), run_time=0.8)

    @staticmethod
    def card_box(head, body):
        content = VGroup(text(head, size=26, weight="SEMIBOLD", color=GATE), *body).arrange(DOWN, buff=0.3)
        box = RoundedRectangle(width=4.0, height=3.6, corner_radius=0.15, fill_color=PANEL, fill_opacity=1,
                               stroke_color=FAINT, stroke_width=2)
        return VGroup(box, content.move_to(box))

    # --- cliffhanger -------------------------------------------------------------------------
    def cliffhanger(self):
        self.slide(say(
            """
            So here's the next idea. Take the fin, and turn it on its side. Then slice it into
            thin sheets and stack them, with gaps in between. Now fill every gap with gate. Four
            faces on every sheet, and the sheets can be as wide as you like.
            """,
            """
            তো পরের idea-টা এই। Fin-টা নেন, আর কাত করে শোয়ায়ে দেন। তারপর পাতলা পাতলা sheet-এ কেটে একটার উপর
            আরেকটা রাখেন, মাঝখানে ফাঁক রেখে। এবার প্রত্যেকটা ফাঁক gate দিয়া ভরেন। প্রত্যেক sheet-এ চার দিক, আর sheet যত
            চওড়া চান তত।
            """,
        ))
        self.clear()
        a = text("Turn the fin on its side. Slice it.", size=44, weight="SEMIBOLD").to_edge(UP, buff=0.7)
        fin_x = xsection("finfet").scale(1.4).move_to([0, -1.2, 0])
        ns = xsection("nanosheet").scale(1.4).move_to([0, -1.2, 0])
        fin = fin_x[-1]
        self.play(FadeIn(a), FadeIn(fin_x))
        self.wait(0.4)
        self.play(FadeOut(fin_x[1]), FadeOut(fin_x[2]))
        self.play(Rotate(fin, -PI / 2), run_time=1.2)
        sheets = ns[2]
        slices = VGroup(*[s[1].copy() for s in sheets])
        self.play(ReplacementTransform(fin, slices), run_time=1.5)
        self.play(FadeIn(ns[1]), FadeIn(VGroup(*[s[0] for s in sheets])), FadeOut(fin_x[0]), FadeIn(ns[0]),
                  slices.animate.set_z_index(2), run_time=1.5)
        self.wait(1)


def po_color():
    """The layout tool's poly colour, as in FET Lab."""
    return "#3B41CF"

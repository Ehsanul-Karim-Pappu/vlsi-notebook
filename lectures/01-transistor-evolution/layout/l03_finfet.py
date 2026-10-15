"""Layout edition · L3 · Width comes in fins: the FinFET.

The fin in 3D and cut; the fin and gate grids; width in whole fins; what you size; fin cuts,
dummy gates and diffusion breaks; a 1 : 2 mirror built from units; the local interconnect.
"""

import sys
from pathlib import Path

LECTURE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(LECTURE.parents[1]), str(LECTURE), str(LECTURE / "layout")]

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403
from manim_slides import ThreeDSlide  # noqa: E402

import physics as phys  # noqa: E402
from common import (ACTIVE, CONTACT, GATE_VIA, METAL, POLY, box, card_box, knob_table, pdk_tag,  # noqa: E402
                    schematic)
from devicedata import device  # noqa: E402
from kit.devices3d import LAYOUT_OPACITY, beside, build_device, plan_view  # noqa: E402
from kit.style import *  # noqa: E402,F403

FIN = device("fin")
LAYOUT = device("show_fin")
H_FIN, W_FIN, PITCH = 45, 6, 27  # FET Lab's FinFET model, nm
POLY_TEXT = "#8F94F2"


class L03FinFET(Chapter, ThreeDSlide):
    def construct(self):
        self.card()
        self.model()
        self.cutaway()
        self.from_above()
        self.grids()
        self.whole_fins()
        self.knobs()
        self.stacks()
        self.breaks()
        self.flavours()
        self.mirror()
        self.local_wires()
        self.limits()

    def flat(self):
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0, frame_center=ORIGIN)

    def card(self):
        self.slide(say(
            """
            Chapter three: the FinFET. If you can't put a gate under a flat channel, stand the
            channel up and wrap the gate over it. It came into production in 2011, and it
            changed layout more than any device before it.
            """,
            """
            Chapter three: FinFET। Flat channel-এর নিচে gate বসানো না গেলে, channel-রে খাড়া করেন আর gate দিয়া তার উপর মুড়ে দেন।
            Production-এ আসছে 2011-এ, আর এর আগের যেকোনো device-এর চেয়ে বেশি layout বদলাইছে।
            """,
        ))
        self.card_group = self.open_chapter(3, 2011, 2005, "Width comes in fins", "The FinFET, from the layout side")

    # --- 3D ---------------------------------------------------------------------------------
    def model(self):
        self.slide(say(
            """
            Here it is in 3D, built the way it's made, from FET Lab's model. The wafer, with oxide
            isolation. Two fins of silicon, each 6 nanometres wide and 45 tall above the oxide.
            The gate's thin films. The gate, running across both fins. Spacers. And the source
            and drain, grown onto the fins on either side of the gate.
            """,
            """
            এই যে 3D-তে, যেভাবে বানানো হয় সেভাবে, FET Lab-এর model থেকে। Wafer, oxide isolation সহ। Silicon-এর দুইটা fin,
            প্রত্যেকটা 6 nanometre চওড়া আর oxide-এর উপরে 45 উঁচু। Gate-এর পাতলা film-গুলা। Gate, দুইটা fin-এর উপর দিয়া
            আড়াআড়ি। Spacer। আর source আর drain, gate-এর দুই পাশে fin-এর উপর grow করা।
            """,
        ))
        self.play(FadeOut(self.card_group))
        self.set_camera_orientation(phi=64 * DEGREES, theta=-58 * DEGREES, zoom=0.78, frame_center=beside(-58 * DEGREES, 2.3))
        order = ["Substrate & isolation", "Fins", "Tri-gate films", "Gate electrode", "Spacers", "Source / drain"]
        captions = ["wafer and oxide isolation", f"two fins: {W_FIN} nm wide, {H_FIN} nm tall", "gate films",
                    "gate", "spacers", "source and drain"]
        kw = dict(scale=0.05, groups=order)
        back, back_g = build_device(FIN, clip={"x": (None, 0.0)}, **kw)
        front, front_g = build_device(FIN, clip={"x": (0.0, None)}, **kw)
        shift = -VGroup(back, front).get_center() + np.array([0, 0, -0.2])
        back.shift(shift)
        front.shift(shift)
        lst = VGroup(*[text(c, size=22, color=MUTED) for c in captions]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        lst.to_corner(UL, buff=0.5)
        src = source("Model: FET Lab's FinFET nFET (18 nm gate, 6 nm fins, 27 nm fin pitch)")
        self.add_fixed_in_frame_mobjects(lst, src)
        self.remove(lst, src)
        self.play(FadeIn(src))
        for i, name in enumerate(order):
            self.play(FadeIn(VGroup(back_g[name], front_g[name]), shift=IN * 0.8), FadeIn(lst[i]),
                      *([lst[i - 1].animate.set_color(MUTED)] if i else []), run_time=0.9)
            self.play(lst[i].animate.set_color(INK), run_time=0.25)
        self.back, self.front, self.labels3d = back, front, VGroup(lst, src)

    def cutaway(self):
        self.slide(say(
            """
            Cut it across, through the gate. The gate wraps over the top and down both sides of
            each fin: three faces instead of one, on a channel only 6 nanometres thick. That's
            the grip the last chapter asked for. Current flows along every face the gate
            touches.
            """,
            """
            Gate-এর মাঝখান দিয়া আড়াআড়ি কাটেন। Gate প্রত্যেকটা fin-এর মাথার উপর দিয়া আর দুই পাশ বেয়ে মুড়ে আছে: এক দিকের
            বদলে তিন দিক, মাত্র 6 nanometre পুরু একটা channel-এ। আগের chapter যে grip চাইছিল, এইটাই। Gate যে মুখগুলা ছোঁয়,
            তার প্রত্যেকটা দিয়া current যায়।
            """,
        ))
        info = VGroup(text("cut through the gate", size=26, color=GATE),
                      text("the gate covers three\nfaces of each fin", size=26, weight="SEMIBOLD")).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        info.move_to([4.5, 0.6, 0])
        self.add_fixed_in_frame_mobjects(info)
        self.remove(info)
        self.play(FadeOut(self.front, shift=RIGHT * 3), FadeOut(self.labels3d[0]), FadeIn(info[0]), run_time=1.5)
        self.move_camera(phi=82 * DEGREES, theta=-4 * DEGREES, zoom=1.05, frame_center=beside(-4 * DEGREES, -1.6), run_time=2.5)
        self.play(FadeIn(info[1]))
        self.wait(0.5)
        self.cut_parts = VGroup(self.back, self.labels3d[1], info)

    # --- from above ---------------------------------------------------------------------------
    def from_above(self):
        self.slide(say(
            """
            Now from above, the way your tool shows it: FET Lab's FinFET inverter. The fins run
            left to right on one fixed pitch, here 27 nanometres, and that pitch is the same
            everywhere on the chip. You can't move a fin, or make one wider; you can only use it,
            or cut it away. The gates run up and down, also on one fixed pitch. So you don't
            draw the width of the active any more. You choose how many fins it covers.
            """,
            """
            এবার উপর থেকে, আপনার tool যেভাবে দেখায়: FET Lab-এর FinFET inverter। Fin-গুলা বাম থেকে ডানে চলে একটা fixed
            pitch-এ, এইখানে 27 nanometre, আর ওই pitch পুরা chip-এ একই। Fin সরাইতে পারবেন না, চওড়াও করতে পারবেন না; শুধু
            use করতে পারেন, বা কেটে ফেলতে পারেন। Gate-গুলা উপর-নিচে চলে, ওইগুলাও একটা fixed pitch-এ। তাই active-এর width আপনি
            আর আঁকেন না। আপনি বাছেন active কয়টা fin ঢাকবে।
            """,
        ))
        self.play(FadeOut(self.cut_parts))
        self.flat()
        title = heading("From above: two fixed grids")
        mat = {p["id"]: p["material"] for p in LAYOUT["parts"]}
        view, by = plan_view(LAYOUT, scale=0.033, skip=("pwell", "fox"), opacity=LAYOUT_OPACITY)
        view.move_to([-3.4, -0.45, 0])
        wells = VGroup(*[s for pid, s in by.items() if mat[pid] in ("nwell", "pwell")])
        fins = VGroup(*[s for pid, s in by.items() if mat[pid] == "nanowire"])
        rest = VGroup(*[s for pid, s in by.items() if mat[pid] in ("md", "vd", "vg", "m0")])
        ys = sorted({round(f.get_center()[1], 3) for f in fins})
        top_two = [y for y in ys][-2:]
        x_r = view.get_right()[0] + 0.25
        pb = BraceBetweenPoints([x_r, top_two[0], 0], [x_r, top_two[1], 0], direction=RIGHT, color=ACTIVE)
        pb_l = text("fin pitch 27 nm", size=20, color=ACTIVE).next_to(pb, RIGHT, buff=0.1)
        notes = VGroup(text("fins: one fixed pitch, the same\neverywhere; use them or cut them", size=22, color=ACTIVE),
                       text("gates: one fixed pitch too", size=22, color=POLY_TEXT),
                       text("you don't draw the active's width:\nyou choose how many fins\nit covers", size=24, weight="SEMIBOLD")
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        notes.move_to([0, 0, 0]).shift(RIGHT * (1.5 - notes.get_left()[0]))
        tag = text("Schematic: FET Lab's FinFET inverter layout (model)", size=16, color=MUTED).next_to(view, DOWN, buff=0.2)
        self.play(FadeIn(title), FadeIn(wells), FadeIn(tag))
        self.play(FadeIn(fins), FadeIn(pb), FadeIn(pb_l), FadeIn(notes[0]))
        self.play(FadeIn(by["po"]), FadeIn(notes[1]))
        self.play(FadeIn(rest), FadeIn(notes[2]))

    def grids(self):
        self.slide(say(
            """
            Why is everything on a grid now? Because of how the tightest layers are made. Lines
            this close together can't be printed one by one. So the fab makes a uniform pattern
            of lines, all the same width and pitch, by building spacers around a coarser pattern
            and using the spacers as the mask. That's self-aligned double or quadruple
            patterning. Then a separate cut mask removes the pieces that aren't wanted. The fins
            are made this way, and in many processes so are the tightest metals. That's where your rules come
            from: one direction, one pitch, and cut rules instead of free shapes. It's also why
            some metal layers ask for a colour or follow fixed tracks.
            """,
            """
            এখন সবকিছু grid-এ কেন? কারণ সবচেয়ে চাপা layer-গুলা যেভাবে বানানো হয়। এত কাছাকাছি লাইন একটা একটা করে print করা
            যায় না। তাই fab একটা uniform লাইনের pattern বানায়, সব একই width আর pitch-এ, একটা মোটা pattern-এর চারপাশে spacer বানায়ে
            আর সেই spacer-গুলারে mask হিসাবে use করে। এইটারে বলে self-aligned double বা quadruple patterning। তারপর আলাদা একটা cut
            mask অদরকারি টুকরাগুলা সরায়ে দেয়। Fin এইভাবে বানানো, আর অনেক process-এ সবচেয়ে চাপা metal-ও। আপনার rule-গুলা এখান থেকেই আসে: এক দিক,
            এক pitch, আর ইচ্ছামতো shape-এর বদলে cut rule। এই কারণেই কিছু metal layer একটা colour চায় বা fixed track মানে।
            """,
        ))
        self.clear()
        title = heading("Why everything is on a grid: lines, then cuts")
        ys = [-1.6 + 0.4 * k for k in range(9)]
        lines = VGroup(*[box(-6.0, y - 0.06, 0.4, y + 0.06, ACTIVE, 0.95, 1.0) for y in ys])
        step1 = text("1 · one uniform pattern: the same width,\n    the same pitch, everywhere", size=22, color=ACTIVE)
        cuts = VGroup(box(-3.4, ys[0] - 0.2, -2.6, ys[3] + 0.2, DRAIN, 0.35), box(-6.1, ys[5] - 0.2, -4.6, ys[6] + 0.2, DRAIN, 0.35),
                      box(-1.2, ys[4] - 0.2, 0.5, ys[8] + 0.2, DRAIN, 0.35))
        step2 = text("2 · a cut mask removes what isn't wanted", size=22, color=DRAIN)
        rules = text("so: one direction, one pitch,\nand cut rules instead of free shapes", size=26, weight="SEMIBOLD")
        VGroup(step1, step2, rules).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([3.9, 0.0, 0])
        how = text("fins, and in many processes the tightest metals: self-aligned double or quadruple patterning, then cuts", size=18,
                   color=MUTED).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(title), FadeIn(how))
        self.play(LaggedStart(*[FadeIn(l) for l in lines], lag_ratio=0.08), FadeIn(step1), run_time=1.4)
        self.play(FadeIn(cuts), FadeIn(step2))
        kept = VGroup()
        for l in lines:
            y = l.get_center()[1]
            pieces = [(-6.0, 0.4)]
            for c in cuts:
                if c.get_bottom()[1] < y < c.get_top()[1]:
                    a, b = c.get_left()[0], c.get_right()[0]
                    pieces = [q for p in pieces for q in ((p[0], min(p[1], a)), (max(p[0], b), p[1])) if q[1] - q[0] > 0.05]
            kept.add(*[box(a, y - 0.06, b, y + 0.06, ACTIVE, 0.95, 1.0) for a, b in pieces])
        self.play(FadeOut(lines), FadeOut(cuts), FadeIn(kept), run_time=1.2)
        self.play(FadeIn(rules))

    def whole_fins(self):
        per = phys.weff_fin_nm(1, H_FIN, W_FIN)
        self.slide(say(
            f"""
            So what's the width of a FinFET? Current flows along every face the gate covers: up
            one sidewall, across the top, down the other. Each fin is worth two heights plus its
            width, {per} nanometres in this model. And every fin is the same. So the width comes
            in steps: {per}, {2 * per}, {3 * per} nanometres, and nothing in between. On planar
            you drew any W. Here you count fins.
            """,
            f"""
            তাহলে FinFET-এর width কত? Gate যে মুখগুলা ঢাকে, তার প্রত্যেকটা দিয়া current যায়: এক sidewall বেয়ে উপরে, top পার
            হয়ে, অন্যটা দিয়া নিচে। প্রত্যেকটা fin-এর দাম দুইটা height যোগ তার width, এই model-এ {per} nanometre। আর সব fin একই।
            তাই width আসে ধাপে ধাপে: {per}, {2 * per}, {3 * per} nanometre, মাঝে কিছু নাই। Planar-এ যেকোনো W আঁকতেন। এইখানে
            fin গোনেন।
            """,
        ))
        self.clear()
        title = heading("Width comes in whole fins")
        u, base_y = 0.05, -0.6
        fin = Rectangle(width=W_FIN * u * 3, height=H_FIN * u, fill_color=SILICON, fill_opacity=1, stroke_width=0)
        fin.move_to([-4.6, base_y + H_FIN * u / 2, 0])
        l, r, t = fin.get_left()[0], fin.get_right()[0], fin.get_top()[1]
        path = VMobject(stroke_color=ELECTRON, stroke_width=7).set_points_as_corners(
            [[l - 0.05, base_y, 0], [l - 0.05, t + 0.05, 0], [r + 0.05, t + 0.05, 0], [r + 0.05, base_y, 0]])
        floor = Line([-5.8, base_y, 0], [-3.4, base_y, 0], stroke_color=MUTED, stroke_width=3)
        one = text(f"one fin ≈ 2 × height + width\n= {per} nm (model)", size=22, color=ELECTRON).next_to(floor, DOWN, buff=0.3)
        ax = Axes(x_range=[0, 420, 100], y_range=[0, 3, 1], x_length=7.0, y_length=2.6, tips=False,
                  axis_config={"stroke_color": MUTED, "stroke_width": 2, "include_ticks": False}).move_to([2.6, -0.4, 0])
        ax.x_axis.add_labels({v: text(str(v), size=18, color=MUTED) for v in (0, 100, 200, 300, 400)}, font_size=18)
        x_l = text("effective width (nm)", size=20, color=MUTED).next_to(ax.x_axis, DOWN, buff=0.45)
        planar = Line(ax.c2p(0, 0.8), ax.c2p(420, 0.8), stroke_color=MUTED, stroke_width=6)
        planar_l = text("planar: any width", size=20, color=MUTED).next_to(planar, UP, buff=0.1).align_to(planar, LEFT)
        dots = VGroup(*[Dot(ax.c2p(n * per, 2.0), color=ELECTRON, radius=0.12) for n in (1, 2, 3, 4)])
        lbls = VGroup(*[text(f"{n} fin{'s' if n > 1 else ''}", size=18, color=ELECTRON).next_to(d, UP, buff=0.12)
                        for n, d in zip((1, 2, 3, 4), dots)])
        self.play(FadeIn(title), FadeIn(floor), FadeIn(fin))
        self.play(Create(path), FadeIn(one), run_time=1.4)
        self.play(Create(ax), FadeIn(x_l), Create(planar), FadeIn(planar_l))
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.25), FadeIn(lbls), run_time=1.4)

    def knobs(self):
        self.slide(say(
            """
            Here's what you size now, side by side with planar. Width: not W, but the number of
            fins per finger. Fingers and multipliers work as before. Length is the big change:
            the gates sit on one fixed pitch, so most processes offer only a few gate lengths,
            and a long device for a mirror or a current source is often built as a stack of
            short devices in series. That's typical, not universal: your PDK says exactly which
            lengths and which stacks you get.
            """,
            """
            এই যে এখন কী size করেন, planar-এর পাশাপাশি। Width: W না, বরং প্রতি finger-এ কয়টা fin। Finger আর multiplier আগের
            মতোই। বড় বদল length-এ: gate-গুলা একটা fixed pitch-এ বসে, তাই বেশিরভাগ process মাত্র কয়েকটা gate length দেয়, আর
            mirror বা current source-এর জন্য লম্বা device প্রায়ই বানানো হয় কয়েকটা ছোট device series-এ stack করে। এইটা typical,
            সব জায়গায় না: ঠিক কোন length আর কোন stack পাবেন, সেইটা আপনার PDK বলে।
            """,
        ))
        self.clear()
        title = heading("What you size")
        table = knob_table([
            ["", "planar", "FinFET"],
            ["width", "W, any value", "fins per finger (nfin)"],
            ["length", "L, any value", "a few lengths; long ones\noften as series stacks"],
            ["fingers", "nf", "nf"],
            ["copies", "m", "m"],
        ], col_w=(2.4, 3.6, 4.6), size=26).move_to([0, -0.1, 0])
        tag = pdk_tag().next_to(table, DOWN, buff=0.5)
        self.play(FadeIn(title), FadeIn(table[0][0]), FadeIn(table[1]))
        for row in table[0][1:]:
            self.play(FadeIn(row, shift=UP * 0.1), run_time=0.6)
        self.play(FadeIn(tag))

    def stacks(self):
        self.slide(say(
            """
            How do you get a long device, then, for a mirror or a current source, when the gate
            length comes from a short list? You chain short ones. Put several gates in series on
            the same fins, sharing their diffusion, with no contacts in between and the gates
            tied together. Electrically it behaves much like one longer device. Close to, not
            identical to, a single long gate: the PDK models the stack, and its output resistance
            and matching aren't exactly a long device's. It's the standard answer; just
            simulate it the way you'll draw it.
            """,
            """
            তাহলে mirror বা current source-এর জন্য লম্বা device পাবেন কিভাবে, যখন gate length একটা ছোট তালিকা থেকে আসে? ছোটগুলারে
            শিকলের মতো জোড়েন। একই fin-এ কয়েকটা gate series-এ বসান, diffusion share করে, মাঝে কোনো contact ছাড়া, আর gate-গুলা
            একসাথে জোড়া। Electrically এইটা অনেকটা একটা লম্বা device-এর মতো আচরণ করে। কাছাকাছি, হুবহু না: PDK stack-টারে model
            করে, আর এর output resistance আর matching একটা লম্বা device-এর মতো ঠিক এক না। এইটাই standard উত্তর; শুধু যেভাবে আঁকবেন
            সেভাবেই simulate করেন।
            """,
        ))
        self.clear()
        title = heading("A long device, from short ones")
        act = box(-5.6, 0.6, -2.2, 1.6, ACTIVE, 0.5)
        long_g = box(-4.6, 0.3, -3.2, 1.9, POLY, 0.75)
        lp = text("planar: one long gate", size=22, color=MUTED).next_to(act, DOWN, buff=0.55)
        fins = VGroup(*[box(0.0, y - 0.04, 5.6, y + 0.04, ACTIVE, 0.95, 1.0) for y in (0.75, 1.1, 1.45)])
        gx = [1.3 + 0.75 * k for k in range(4)]
        gates = VGroup(*[box(x - 0.09, 0.3, x + 0.09, 1.9, POLY, 0.8) for x in gx])
        tie = Line([gx[0], 2.1, 0], [gx[-1], 2.1, 0], stroke_color=POLY_TEXT, stroke_width=4)
        ticks = VGroup(*[Line([x, 1.9, 0], [x, 2.1, 0], stroke_color=POLY_TEXT, stroke_width=4) for x in gx])
        sd = VGroup(box(0.25, 0.55, 0.65, 1.65, CONTACT, 0.6), box(4.95, 0.55, 5.35, 1.65, CONTACT, 0.6))
        s_l = text("S", size=22, weight="BOLD").next_to(sd[0], DOWN, buff=0.12)
        d_l = text("D", size=22, weight="BOLD").next_to(sd[1], DOWN, buff=0.12)
        fl = text("FinFET: four short gates in series, tied together,\nno contacts in between", size=22, color=INK)
        fl.next_to(fins, DOWN, buff=0.65)
        cave = text("close to one long device, not identical: the PDK models the stack; simulate what you draw",
                    size=22, color=GATE).to_edge(DOWN, buff=0.9)
        tag = pdk_tag().to_corner(UR, buff=0.3).shift(DOWN * 0.75)
        self.play(FadeIn(title), FadeIn(act), FadeIn(long_g), FadeIn(lp), FadeIn(tag))
        self.play(FadeIn(fins), FadeIn(gates), FadeIn(sd), FadeIn(s_l), FadeIn(d_l))
        self.play(Create(tie), Create(ticks), FadeIn(fl))
        self.play(FadeIn(cave))

    def flavours(self):
        self.slide(say(
            """
            One more layer you now draw on purpose: the threshold flavour. Low, standard and
            high threshold devices are made with different gate metals or implants, so in layout
            they're marker layers over the devices. Where two flavours meet, there's a boundary
            the process has to pattern, with spacing and alignment rules, often tied to the gate
            grid. It's the same reason n and p can't touch: different gate metals need room to
            be patterned apart. Group devices of one flavour together, and keep matched devices
            in the same flavour.
            """,
            """
            আরেকটা layer যেটা এখন ইচ্ছা করে আঁকেন: threshold flavour। Low, standard আর high threshold device বানানো হয় আলাদা gate
            metal বা implant দিয়া, তাই layout-এ এগুলা device-এর উপর marker layer। যেখানে দুইটা flavour মিলে, সেখানে একটা সীমানা থাকে
            যেটা process-রে pattern করতে হয়, spacing আর alignment rule সহ, প্রায়ই gate grid-এর সাথে বাঁধা। n আর p যে ছুঁইতে পারে না,
            একই কারণ: আলাদা gate metal-রে আলাদা করে pattern করতে জায়গা লাগে। এক flavour-এর device একসাথে রাখেন, আর matched device-গুলা
            একই flavour-এ।
            """,
        ))
        self.clear()
        title = heading("Threshold flavours are layers you draw")
        fins = VGroup(*[box(-6.0, y - 0.04, 6.0, y + 0.04, ACTIVE, 0.95, 1.0) for y in (-0.6, -0.25, 0.1, 0.45)])
        gates = VGroup(*[box(x - 0.08, -1.0, x + 0.08, 0.85, POLY, 0.75) for x in np.arange(-5.4, 5.5, 0.6)])
        regions = [("LVT", -6.0, -2.1, GOOD), ("SVT", -2.1, 2.1, GATE), ("HVT", 2.1, 6.0, DRAIN)]
        marks, labels = VGroup(), VGroup()
        for name, a, b, c in regions:
            marks.add(box(a + 0.05, -1.25, b - 0.05, 1.1, c, 0.12, 2.0))
            labels.add(text(name, size=26, weight="BOLD", color=c).move_to([(a + b) / 2, 1.5, 0]))
        edges = VGroup(*[DashedLine([x, -1.5, 0], [x, 1.25, 0], stroke_color=INK, stroke_width=2) for x in (-2.1, 2.1)])
        edge_l = text("flavour boundaries: spacing and alignment rules, often on the gate grid", size=22, color=INK)
        edge_l.next_to(fins, DOWN, buff=1.0)
        why = text("the same reason n and p can't touch: different gate metals, patterned apart", size=22, color=MUTED)
        why.next_to(edge_l, DOWN, buff=0.3)
        note = text("group one flavour together; keep matched devices in one flavour", size=24, color=GATE).to_edge(DOWN, buff=0.4)
        tag = pdk_tag().to_corner(UR, buff=0.3).shift(DOWN * 0.75)
        self.play(FadeIn(title), FadeIn(fins), FadeIn(gates), FadeIn(tag))
        self.play(FadeIn(marks), FadeIn(labels))
        self.play(Create(edges), FadeIn(edge_l))
        self.play(FadeIn(why))
        self.play(FadeIn(note))

    def breaks(self):
        self.slide(say(
            """
            Because the fins are continuous, you also draw where they stop. Here's a row: fins
            running across, gates on their grid. A device uses some of the gates. At its ends sit
            dummy gates, so every real gate has the same neighbours on both sides; PDKs give them
            names like PODE. Between two devices, the fins have to be cut: a diffusion break,
            under one gate pitch or two, a single or a double break. The break you choose sets
            how close two devices can sit, and, as we'll see in chapter six, it changes the
            devices next to it.
            """,
            """
            Fin-গুলা একটানা বলে, কোথায় থামবে সেইটাও আঁকেন। এই যে একটা row: fin আড়াআড়ি চলতেছে, gate তার grid-এ। একটা device
            কয়েকটা gate use করে। তার দুই মাথায় থাকে dummy gate, যাতে প্রত্যেকটা আসল gate-এর দুই পাশে একই রকম প্রতিবেশী থাকে;
            PDK এগুলার নাম দেয় PODE-র মতো কিছু। দুইটা device-এর মাঝে fin কাটতে হয়: একটা diffusion break, এক gate pitch বা দুই
            gate pitch-এর নিচে, single বা double break। কোন break নিবেন তাতে ঠিক হয় দুইটা device কত কাছে বসতে পারে, আর chapter
            six-এ দেখব, এইটা পাশের device-গুলারেও বদলায়।
            """,
        ))
        self.clear()
        title = heading("Where the fins stop: dummy gates and breaks")
        pitch, n_g = 0.72, 15
        x0 = -pitch * (n_g - 1) / 2
        gx = [x0 + k * pitch for k in range(n_g)]
        fin_y = [-1.0 + 0.36 * k for k in range(5)]
        # Two devices on gates 2-5 and 8-11; the fins end under dummy gates, cut between gates 6 and 7.
        a_gates, b_gates = [2, 3, 4, 5], [8, 9, 10, 11]
        dummies = [1, 6, 7, 12]
        fins = VGroup()
        segs = [(gx[0] - 0.3, gx[6] + 0.08), (gx[7] - 0.08, gx[12] + 0.08)]
        for y in fin_y:
            for a, b in segs:
                fins.add(box(a, y - 0.04, b, y + 0.04, ACTIVE, 0.95, 1.0))
        gates = VGroup()
        for k, x in enumerate(gx[:14]):
            real = k in a_gates or k in b_gates
            g = box(x - 0.1, -1.55, x + 0.1, 0.95, POLY, 0.75 if real else 0.25)
            if not real:
                g.set_stroke(POLY, width=1.5, opacity=0.8)
            gates.add(g)
        brace_a = BraceBetweenPoints([gx[2] - 0.15, 1.05, 0], [gx[5] + 0.15, 1.05, 0], direction=UP, color=INK)
        brace_b = BraceBetweenPoints([gx[8] - 0.15, 1.05, 0], [gx[11] + 0.15, 1.05, 0], direction=UP, color=INK)
        la = text("device A", size=22, weight="SEMIBOLD").next_to(brace_a, UP, buff=0.08)
        lb = text("device B", size=22, weight="SEMIBOLD").next_to(brace_b, UP, buff=0.08)
        dummy_l = text("dummy gates at\nevery end", size=20, color=POLY_TEXT).move_to([gx[1], -2.25, 0])
        brk = DashedLine([(gx[6] + gx[7]) / 2, -1.7, 0], [(gx[6] + gx[7]) / 2, 1.0, 0], stroke_color=DRAIN, stroke_width=3)
        brk_l = text("diffusion break:\nthe fins are cut", size=20, color=DRAIN).move_to([(gx[6] + gx[7]) / 2 + 0.2, -2.25, 0])
        end_l = text("fins end under\na dummy gate", size=20, color=ACTIVE).move_to([gx[12] + 0.15, -2.25, 0])
        line = text("single or double break (one gate pitch or two): it sets how close devices sit,\n"
                    "and it changes the devices next to it (chapter 6)", size=22, color=MUTED).to_edge(DOWN, buff=0.35)
        tag = pdk_tag().to_corner(UR, buff=0.3).shift(DOWN * 0.75)
        self.play(FadeIn(title), FadeIn(fins), FadeIn(gates), FadeIn(tag))
        self.play(FadeIn(brace_a), FadeIn(la), FadeIn(brace_b), FadeIn(lb))
        self.play(*[Indicate(gates[k], color=POLY_TEXT, scale_factor=1.0) for k in dummies], FadeIn(dummy_l))
        self.play(Create(brk), FadeIn(brk_l), FadeIn(end_l))
        self.play(FadeIn(line))

    def mirror(self):
        self.slide(say(
            """
            Now a one-to-two current mirror. You could draw M1 with 2 fins and M2 with 4. Better:
            pick one unit device, say 2 fins and 2 fingers, use it twice for M1 and four times
            for M2, and place the units so both devices have the same centre: B, A, B, B, A, B,
            with dummies at both ends. A gradient across the row, in oxide thickness or stress,
            then pulls both devices the same way, and the ratio stays one to two. Fins make this
            natural: every unit is identical by construction.
            """,
            """
            এবার এক-অনুপাত-দুই একটা current mirror। M1 2 fin আর M2 4 fin দিয়া আঁকতে পারেন। আরও ভালো: একটা unit device
            বাছেন, ধরেন 2 fin আর 2 finger, M1-এর জন্য দুইবার আর M2-এর জন্য চারবার use করেন, আর unit-গুলা এমনভাবে বসান যাতে
            দুইটা device-এর center একই থাকে: B, A, B, B, A, B, দুই মাথায় dummy। Row জুড়ে কোনো gradient থাকলে, oxide thickness
            বা stress-এ, সেইটা দুইটা device-রে একই দিকে টানে, আর ratio এক-অনুপাত-দুই-ই থাকে। Fin এইটারে সহজ করে: প্রত্যেকটা unit
            বানানোর নিয়মেই একরকম।
            """,
        ))
        self.clear()
        title = heading("A 1 : 2 mirror, built from units")
        sch = schematic("mirror", 2.6).move_to([-5.0, 0.35, 0])
        order = "DBABBABD"
        colors = {"A": ELECTRON, "B": GATE, "D": FAINT}
        cells = VGroup()
        for ch in order:
            fins = VGroup(*[box(-0.5, y - 0.035, 0.5, y + 0.035, ACTIVE, 0.95, 1.0) for y in (-0.3, -0.1, 0.1, 0.3)])
            gates = VGroup(*[box(x - 0.07, -0.5, x + 0.07, 0.5, POLY, 0.8 if ch != "D" else 0.25) for x in (-0.2, 0.2)])
            lab = text("dummy" if ch == "D" else ch, size=22 if ch != "D" else 15, weight="BOLD", color=colors[ch])
            cells.add(VGroup(fins, gates, lab.move_to([0, 0.78, 0])))
        cells.arrange(RIGHT, buff=0.1).move_to([2.0, 0.35, 0])
        unit = text("unit: 2 fins × 2 fingers", size=20, color=MUTED).next_to(cells, DOWN, buff=0.35)
        key = VGroup(text("A = M1: 2 units", size=22, color=ELECTRON), text("B = M2: 4 units", size=22, color=GATE)
                     ).arrange(RIGHT, buff=0.8).next_to(unit, DOWN, buff=0.3)
        centre = DashedLine(cells.get_top() + UP * 0.1, cells.get_bottom() + DOWN * 0.1, stroke_color=INK, stroke_width=2).move_to(cells)
        centre_l = text("both centred here", size=18, color=INK).next_to(centre, UP, buff=0.05)
        note = layout_note("Build every size from one unit device, place the units around a common centre, "
                           "and put dummies at the ends: a gradient then moves both devices together.",
                           size=21, width=70).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(title), FadeIn(sch))
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cells], lag_ratio=0.12), FadeIn(unit), run_time=1.8)
        self.play(FadeIn(key))
        self.play(Create(centre), FadeIn(centre_l))
        self.play(FadeIn(note))

    def local_wires(self):
        self.slide(say(
            """
            One more thing that's new: the local wiring. Each source and drain gets a contact bar
            that runs across all its fins, often called MD, and the gate gets its own contact.
            Above them, metal zero, the first level of routing, with the rails. The distance from
            one gate to the next, with a contact between them, is the contacted gate pitch, one
            of a process's two key numbers. For analog, the contact bar runs right beside the
            gate, so it adds gate-to-drain capacitance, and the contacts and vias add series
            resistance. We'll come back to that in chapter six.
            """,
            """
            আরেকটা নতুন জিনিস: local wiring। প্রত্যেকটা source আর drain পায় একটা contact bar যেটা তার সব fin-এর উপর দিয়া
            আড়াআড়ি চলে, প্রায়ই নাম MD, আর gate পায় নিজের contact। তার উপরে metal zero, routing-এর প্রথম স্তর, rail সহ। একটা
            gate থেকে পরেরটা পর্যন্ত দূরত্ব, মাঝে একটা contact সহ, হইলো contacted gate pitch, একটা process-এর দুইটা মূল সংখ্যার
            একটা। Analog-এর জন্য: contact bar gate-এর ঠিক পাশে চলে, তাই gate-to-drain capacitance যোগ করে, আর contact আর via
            series resistance যোগ করে। Chapter six-এ আবার ফিরব।
            """,
        ))
        self.clear()
        title = heading("The local wiring")
        mat = {p["id"]: p["material"] for p in LAYOUT["parts"]}
        view, by = plan_view(LAYOUT, scale=0.03, skip=("pwell", "fox", "nwell", "pwell_u"), opacity=LAYOUT_OPACITY)
        view.move_to([-3.4, -0.7, 0])
        groups = [("fins and gate", ["nanowire", "po"], MUTED),
                  ("MD: a contact bar across all the fins", ["md"], CONTACT),
                  ("vias, and the gate contact", ["vd", "vg"], GATE_VIA),
                  ("metal 0: the first routing, and the rails", ["m0"], METAL)]
        labels = VGroup(*[text(n, size=22, color=c) for n, _, c in groups]).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        labels.move_to([3.3, 1.2, 0])
        md = [s for pid, s in by.items() if mat[pid] == "md"]
        xs = sorted({round(m.get_center()[0], 3) for m in md})
        cpp = BraceBetweenPoints([xs[0], view.get_top()[1] + 0.1, 0], [xs[-1], view.get_top()[1] + 0.1, 0],
                                 direction=UP, color=POLY_TEXT)
        cpp_l = text("contacted gate pitch: 54 nm (model)", size=18, color=POLY_TEXT).next_to(cpp, UP, buff=0.05)
        note = layout_note("The contact bar runs beside the gate: it adds gate-to-drain capacitance. Contacts and "
                           "vias add series resistance. Both matter for analog; check them after extraction.",
                           size=21, width=48).move_to([3.2, -1.7, 0])
        tag = text("Schematic: FET Lab's FinFET inverter layout (model)", size=16, color=MUTED).next_to(view, DOWN, buff=0.2)
        self.play(FadeIn(title), FadeIn(tag))
        for (name, mats, c), lbl in zip(groups, labels):
            self.play(*[FadeIn(s) for pid, s in by.items() if mat[pid] in mats], FadeIn(lbl), run_time=0.8)
        self.play(FadeIn(cpp), FadeIn(cpp_l))
        self.play(FadeIn(note))

    def limits(self):
        self.slide(say(
            """
            The FinFET carried the industry for a decade. But it ran out of room. Every fin is
            the same height, so the width still comes in steps. It's hard to make the fins much
            thinner, and hard to make them taller and keep them straight. And each fin, with
            its spacing, costs floor. The next idea: turn the fin on its side, slice it into
            sheets, and let you draw the width again.
            """,
            """
            FinFET দশ বছর industry-রে টানছে। কিন্তু তার জায়গা ফুরাইলো। সব fin-এর height একই, তাই width এখনো ধাপে ধাপে।
            Fin-রে আরও পাতলা করা কঠিন, আর উঁচু করে সোজা রাখাও কঠিন। আর প্রত্যেকটা fin, তার spacing সহ, জায়গা খায়। পরের idea:
            fin-রে কাত করে শোয়ায়ে দেন, sheet-এ কাটেন, আর আপনারে আবার width আঁকতে দেন।
            """,
        ))
        self.clear()
        title = heading("Where the fin runs out of room")
        cards = VGroup(
            card_box("Width in steps", [text("every fin the same height", size=22, color=INK)]),
            card_box("Hard to change", [text("thinner: harder to make\nand to keep uniform;\ntaller: hard to etch\nstraight", size=21, color=INK)]),
            card_box("Floor per fin", [text("each fin and its\nspacing costs area", size=22, color=INK)]),
        ).arrange(RIGHT, buff=0.45).move_to([0, -0.2, 0])
        nxt = text("Next: turn it on its side, and slice it into sheets.", size=28, color=GATE).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(title))
        for c in cards:
            self.play(FadeIn(c, shift=UP * 0.15), run_time=0.7)
        self.play(FadeIn(nxt))

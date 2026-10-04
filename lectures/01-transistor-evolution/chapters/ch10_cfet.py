"""Chapter 10 · CFET: build upward (2018–, projected for about 2033).

The nFET stacked on the pFET, one gate through both: the n-to-p space disappears. The cell's
height drops, the power moves to the back of the wafer, and the heat has to go somewhere. Then
the cliffhanger: silicon itself is the next limit.
"""

import sys
from pathlib import Path

LECTURE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(LECTURE.parents[1]), str(LECTURE)]

from manim import *  # noqa: E402,F403
from manim_slides import ThreeDSlide  # noqa: E402

import physics as phys  # noqa: E402
from devicedata import device, rail_span_nm  # noqa: E402
from kit.devices3d import LAYOUT_OPACITY, beside, build_device, plan_view  # noqa: E402
from kit.motifs import xsection  # noqa: E402
from kit.style import *  # noqa: E402,F403

IMAGES = LECTURE / "images"
CHANNEL = "#7FD8E4"
P_CHANNEL = "#E88BB8"
CFET = device("cfet_mono")
CELLS = [("show_fin", "FinFET"), ("show_ns", "nanosheet"), ("show_fs", "forksheet"), ("show_cfet", "CFET")]


class Ch10CFET(Chapter, ThreeDSlide):
    def construct(self):
        self.card()
        self.history()
        self.model()
        self.two_ways()
        self.cells()
        self.backside()
        self.heat()
        self.cliffhanger()

    def flat(self):
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0, frame_center=ORIGIN)

    # --- chapter card ------------------------------------------------------------------------
    def card(self):
        self.slide(say(
            """
            Every transistor so far has been built in one layer: n and p side by side, across the
            wafer. The CFET, the complementary FET, stacks them: the n transistor right on top of
            the p. Like the forksheet, it's on the roadmap, not yet in products.
            """,
            """
            এখন পর্যন্ত প্রত্যেকটা transistor এক layer-এ বানানো: n আর p পাশাপাশি, wafer জুড়ে। CFET, মানে complementary
            FET, এগুলারে স্তূপ করে: n transistor সোজা p-এর উপরে। Forksheet-এর মতো এইটাও roadmap-এ আছে, product-এ এখনো
            আসে নাই।
            """,
        ))
        self.card_group = self.open_chapter(10, 2033, 2030, "CFET", "Build upward (projected)")

    # --- history -----------------------------------------------------------------------------
    def history(self):
        self.slide(say(
            """
            imec proposed the CFET in 2018, to keep scaling beyond 3 nanometres. At IEDM in December 2023, Intel, TSMC and
            Samsung each showed stacked transistors: Intel a working inverter at a 60 nanometre
            gate pitch, TSMC stacked devices at 48. A year later TSMC showed a working inverter
            at 48. imec's roadmap puts the monolithic CFET at its A7 node, around 2033, if all
            goes to plan.
            """,
            """
            imec 2018-এ CFET প্রস্তাব করে, 3 nanometre-এর পরেও scaling চালু রাখতে। 2023-এর December-এ IEDM-এ Intel, TSMC আর Samsung প্রত্যেকে stacked
            transistor দেখায়: Intel 60 nanometre gate pitch-এ একটা চালু inverter, TSMC 48-এ stacked device। এক বছর পর TSMC
            48-এ চালু inverter দেখায়। imec-এর roadmap monolithic CFET-রে রাখছে ওদের A7 node-এ, প্রায় 2033, সব ঠিকঠাক
            চললে।
            """,
        ))
        self.play(FadeOut(self.card_group))
        title = heading("Stacking n on p")
        line = Line([-5.6, -0.2, 0], [5.6, -0.2, 0], stroke_color=FAINT, stroke_width=3)
        events = [
            (-4.4, "2018", "imec proposes it", "CMOS scaling\nbeyond 3 nm", "J. Ryckaert et al., VLSI 2018"),
            (0.0, "2023–24", "Stacked demos", "Intel, TSMC, Samsung;\nworking inverters", "IEDM 2023 and 2024"),
            (4.4, "~2033", "On the roadmap", "monolithic CFET,\nimec's A7 node", "imec (projection)"),
        ]
        self.play(FadeIn(title), Create(line))
        for x, year, what, why, who in events:
            dot = Dot([x, -0.2, 0], color=GATE, radius=0.1)
            y = display(year, size=48, color=GATE).move_to([x, 0.75, 0])
            body = VGroup(text(what, size=26, weight="SEMIBOLD"), text(why, size=22, color=MUTED),
                          text(who, size=16, color=MUTED)).arrange(DOWN, buff=0.15).next_to(dot, DOWN, buff=0.4)
            icon = xsection("cfet").scale_to_fit_height(0.85).next_to(y, UP, buff=0.3)
            self.play(FadeIn(dot, scale=0.5), FadeIn(y), FadeIn(icon), FadeIn(body, shift=UP * 0.1), run_time=0.9)

        fig = figure(IMAGES / "cfet_US11869812_fig17.png", 5.2,
                     "IBM, US patent 11,869,812 (granted 2024), Fig. 17: a stacked pair, the upper source/drain above the lower")
        fig.move_to([0, -0.4, 0])
        self.show_figure(say(
            """
            Here's one from IBM's patents, granted in 2024. On the left, the stack of sheets cut
            along the channel: the lower transistor's sheets and the upper one's, in one column.
            On the right, across the source and drain: the lower transistor's source/drain,
            the dark shape, and the upper one's right above it, with insulation between them.
            The CFET model you're about to see is drawn after this patent.
            """,
            """
            এই যে IBM-এর একটা patent থেকে, 2024-এ grant হওয়া। বামে, channel বরাবর কাটা sheet-এর stack: নিচের
            transistor-এর sheet আর উপরেরটার, এক column-এ। ডানে, source আর drain বরাবর: নিচের transistor-এর source/drain,
            কালো shape-টা, আর উপরেরটা ঠিক তার উপরে, মাঝে insulation। এখন যে CFET model দেখবেন সেটা এই patent ধরে আঁকা।
            """,
        ), "A CFET patent", fig, clear=VGroup(*self.mobjects))
        self.fig = fig

    # --- the 3D model ------------------------------------------------------------------------
    def model(self):
        self.slide(say(
            """
            Here it is in 3D. The wafer and an insulating layer. The lower tier: the p
            transistor, two pink sheets with its source and drain. An insulating layer between
            the tiers. The upper tier: the n transistor, two blue sheets. One gate, running
            down through both tiers. Spacers, and the contacts, one of them reaching down past
            the upper tier to the lower one.
            """,
            """
            এই যে 3D-তে। Wafer আর একটা insulating layer। নিচের tier: p transistor, দুইটা গোলাপি sheet, তার source আর
            drain সহ। দুই tier-এর মাঝে একটা insulating layer। উপরের tier: n transistor, দুইটা নীল sheet। একটা gate, দুই
            tier-এর ভিতর দিয়াই নেমে গেছে। Spacer, আর contact-গুলা, তার একটা উপরের tier পার হয়ে নিচেরটায় পৌঁছায়।
            """,
        ))
        self.play(FadeOut(self.fig), FadeOut(VGroup(*[m for m in self.mobjects if m is not self.fig])))
        self.set_camera_orientation(phi=64 * DEGREES, theta=-58 * DEGREES, zoom=0.72, frame_center=beside(-58 * DEGREES, 2.0))
        order = ["Substrate & isolation", "Lower tier (p)", "Tier isolation", "Upper tier (n)", "Gate electrode", "Spacers", "Contacts"]
        captions = ["the wafer and an insulating layer", "lower tier: the pFET (pink sheets)", "isolation between the tiers",
                    "upper tier: the nFET (blue sheets)", "one gate through both tiers", "spacers", "contacts"]
        recolor = {"sheet_p1": P_CHANNEL, "sheet_p2": P_CHANNEL, "sheet_n1": CHANNEL, "sheet_n2": CHANNEL}
        kw = dict(scale=0.042, groups=order, recolor=recolor)
        back, back_g = build_device(CFET, clip={"x": (None, 0.0)}, **kw)
        front, front_g = build_device(CFET, clip={"x": (0.0, None)}, **kw)
        shift = -VGroup(back, front).get_center()
        back.shift(shift)
        front.shift(shift)
        lst = VGroup(*[text(c, size=20, color=MUTED) for c in captions]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        lst.to_corner(UL, buff=0.5)
        src = source("Model: FET Lab's monolithic CFET (5 nm sheets, 12 nm between the tiers), after IBM US 11,869,812")
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
            Cut across the gate. Two pink sheets below, two blue sheets above, and one gate
            wrapped around all four. The n and the p transistor now take the floor space of one.
            The n-to-p space, the thing we've been squeezing for two chapters, is now vertical:
            it costs height, not area.
            """,
            """
            Gate-এর মাঝখান দিয়া আড়াআড়ি কাটেন। নিচে দুইটা গোলাপি sheet, উপরে দুইটা নীল, আর একটা gate চারটারেই ঘিরে আছে।
            n আর p transistor এখন একটার জায়গা নেয়। n-to-p space, যেটা দুই chapter ধরে চাপতেছি, এখন খাড়া: এর দাম height-এ,
            area-তে না।
            """,
        ))
        info = VGroup(text("cut across the gate", size=26, color=GATE),
                      text("n above (blue)\np below (pink)", size=24, weight="SEMIBOLD"),
                      text("one gate around all four sheets", size=22),
                      text("two transistors,\none footprint", size=24, color=GOOD),
                      ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([4.6, 0.4, 0])
        self.add_fixed_in_frame_mobjects(info)
        self.remove(info)
        self.play(FadeOut(front, shift=RIGHT * 3), FadeOut(lst), FadeIn(info[0]), run_time=1.6)
        self.move_camera(phi=82 * DEGREES, theta=-4 * DEGREES, zoom=0.9, frame_center=beside(-4 * DEGREES, -1.9), run_time=2.5)
        self.play(FadeIn(info[1:]))
        self.parts3d = VGroup(back, src, info)

    def two_ways(self):
        self.slide(say(
            """
            There are two ways to build one. Monolithic: grow one tall stack of sheets and make
            both transistors from it, together, sharing one gate. That's the model you just saw.
            Sequential: make the bottom transistor, bond a second thin layer of silicon on top,
            and build the top transistor in that. Sequential lets each tier be made its own way,
            but the top tier has to be made cool enough that the bottom one survives.
            """,
            """
            বানানোর দুইটা উপায়। Monolithic: একটা লম্বা sheet-এর stack grow করেন, আর দুইটা transistor একসাথে ওইটা থেকেই
            বানান, একটা gate share করে। এইমাত্র যে model দেখলেন সেইটা। Sequential: নিচের transistor বানান, উপরে silicon-এর
            আরেকটা পাতলা layer bond করেন, আর উপরের transistor ওইটাতে বানান। Sequential-এ প্রত্যেক tier নিজের মতো করে বানানো
            যায়, কিন্তু উপরের tier এমন ঠান্ডায় বানাইতে হয় যাতে নিচেরটা টিকে থাকে।
            """,
        ))
        self.play(FadeOut(self.parts3d))
        self.flat()
        title = heading("Two ways to stack")
        mono = xsection("cfet").scale_to_fit_height(2.6)
        seq = xsection("cfet").scale_to_fit_height(2.6)
        bond = DashedLine(seq.get_left() + RIGHT * 0.0, seq.get_right(), stroke_color=GATE, stroke_width=3)
        bond.move_to(seq[3])
        seq_gate_gap = Line(seq[1].get_left(), seq[1].get_right(), stroke_color=BG, stroke_width=8).move_to(seq[3])
        seq_pic = VGroup(seq, seq_gate_gap, bond)
        c1 = VGroup(mono, text("Monolithic", size=30, weight="SEMIBOLD"),
                    text("one stack, both tiers made together;\none shared gate", size=22, color=MUTED)).arrange(DOWN, buff=0.3)
        c2 = VGroup(seq_pic, text("Sequential", size=30, weight="SEMIBOLD"),
                    text("bottom tier first, a new layer bonded\non top (dashed), the top tier made cool", size=22, color=MUTED)).arrange(DOWN, buff=0.3)
        VGroup(c1, c2).arrange(RIGHT, buff=2.2).move_to([0, -0.4, 0])
        src = source("imec, \"Imec puts complementary FET (CFET) on the logic technology roadmap\"; FET Lab's CFET models")
        self.play(FadeIn(title), FadeIn(c1))
        self.play(FadeIn(c2), FadeIn(src))

    # --- the four cells ----------------------------------------------------------------------
    def cells(self):
        self.slide(say(
            """
            Now line up the four inverter cells from FET Lab, from above, at one scale. FinFET,
            nanosheet, forksheet, CFET. The height of each, rail to rail: 156, 136, 106 and 74
            nanometres, in these schematic models. The CFET cell is under half the FinFET's.
            These aren't any foundry's real cells, but the trend is the point: each step took
            the n-to-p space away, and the cell got shorter.
            """,
            """
            এবার FET Lab-এর চারটা inverter cell পাশাপাশি রাখেন, উপর থেকে, একই scale-এ। FinFET, nanosheet, forksheet, CFET।
            প্রত্যেকটার height, rail থেকে rail: এই schematic model-গুলায় 156, 136, 106 আর 74 nanometre। CFET cell FinFET-এর
            অর্ধেকেরও কম। এগুলা কোনো foundry-র আসল cell না, কিন্তু আসল কথা trend-টা: প্রত্যেক ধাপে n-to-p space সরানো
            হইছে, আর cell ছোট হইছে।
            """,
        ))
        self.clear()
        title = heading("Four inverters, one scale")
        views = VGroup()
        for key, name in CELLS:
            skip = {p["id"] for p in device(key)["parts"] if p["material"] in ("fox",) or p["id"] in ("pwell", "bild")}
            v, by = plan_view(device(key), scale=0.022, skip=skip, opacity=LAYOUT_OPACITY)
            span = rail_span_nm(key)
            r0 = by["m0_gnd"].get_center()[1] if "m0_gnd" in by else by["bm_gnd"].get_center()[1]
            r1 = by["m0_vdd"].get_center()[1] if "m0_vdd" in by else by["bm_vdd"].get_center()[1]
            x = v.get_left()[0] - 0.2
            arrow = DoubleArrow([x, r0, 0], [x, r1, 0], buff=0, stroke_color=GATE, stroke_width=4, tip_length=0.12)
            lbl = VGroup(text(name, size=24, color=MUTED), text(f"{span:.0f} nm", size=26, color=GATE, weight="SEMIBOLD"))
            lbl.arrange(DOWN, buff=0.08).next_to(v, DOWN, buff=0.2)
            views.add(VGroup(v, arrow, lbl))
        views.arrange(RIGHT, buff=0.7, aligned_edge=DOWN).move_to([0, -0.4, 0])
        tag = text("FET Lab's schematic inverter layouts (models), rail centre to rail centre. The CFET's rails are on the back.",
                   size=16, color=MUTED).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(title), FadeIn(tag))
        for v in views:
            self.play(FadeIn(v, shift=UP * 0.1), run_time=0.8)

    # --- backside power ----------------------------------------------------------------------
    def backside(self):
        self.slide(say(
            """
            Look at the CFET cell's rails: they're not on the front any more. Power has a problem.
            Every wire has resistance, R equals rho L over width times thickness, and the supply
            current through it drops voltage: I times R. Front-side wires have to be thin to fit
            the signals. So move the power to the back of the wafer, where the rails can be
            thick: four times wider and twice as thick is eight times less resistance. Intel
            ships this today, in 18A, as PowerVia. In its 2023 test chip, the voltage droop fell
            by over 30 percent.
            """,
            """
            CFET cell-এর rail-গুলা দেখেন: এগুলা আর সামনে নাই। Power-এর একটা সমস্যা আছে। প্রত্যেকটা wire-এর resistance আছে, R
            সমান rho L বাই width গুণ thickness, আর এর ভিতর দিয়া supply current গেলে voltage কমে: I গুণ R। সামনের দিকের wire
            পাতলা রাখতে হয়, signal-এর জায়গা দিতে। তাই power-রে wafer-এর পেছনে নিয়া যান, যেখানে rail মোটা হইতে পারে: চার গুণ
            চওড়া আর দুই গুণ পুরু মানে আট গুণ কম resistance। Intel আজকেই এইটা ship করতেছে, 18A-তে, নাম PowerVia। ওদের 2023-এর
            test chip-এ voltage droop 30 percent-এর বেশি কমছে।
            """,
        ))
        self.clear()
        title = heading("Power from the back of the wafer")
        # A side view: back-side power rails, the transistors, the front-side signal wires.
        dev = Rectangle(width=6.0, height=0.55, fill_color=SILICON, fill_opacity=0.45, stroke_width=0).move_to([-3.0, 0.0, 0])
        dev_l = text("transistors", size=22, color=INK).move_to(dev)
        front = VGroup(*[Line([-5.8, 0.55 + 0.32 * i, 0], [-0.2, 0.55 + 0.32 * i, 0], stroke_color="#F2C1A2", stroke_width=3 + i)
                         for i in range(6)])
        front_l = text("front: signal wiring only", size=22, color="#F2C1A2").next_to(front, UP, buff=0.15)
        back = VGroup(*[Rectangle(width=1.1, height=0.55, fill_color=THERMAL, fill_opacity=0.8, stroke_width=0)
                        .move_to([-5.2 + 1.55 * i, -0.75, 0]) for i in range(4)])
        back_l = text("back: thick power rails", size=22, color=THERMAL).next_to(back, DOWN, buff=0.2)
        vias = VGroup(*[Line([b.get_x(), -0.47, 0], [b.get_x(), -0.27, 0], stroke_color=THERMAL, stroke_width=5) for b in back])
        thin = 4 * 2  # four times wider, twice as thick
        r_front = phys.wire_resistance_ohm(1000, 20, 40)
        e1 = eq(r"\Delta V", r"=", r"I", r"\,R", r",\qquad", r"R = \frac{\rho\,L}{w\,t}", size=42)
        e1[0].set_color(DRAIN)
        e2 = text(f"thin front rail, 20 × 40 nm:  {r_front:.0f} Ω per µm\n4× wider, 2× thicker, on the back:  {r_front / thin:.1f} Ω per µm",
                  size=21, color=INK)
        e2_tag = VGroup(text("illustrative, ρ = 2 × 10⁻⁸ Ω m", size=16, color=MUTED))
        e3 = text("Intel PowerVia (in 18A), 2023 test chip:\n>30% less voltage droop, 6% higher clock", size=22, color=GOOD)
        VGroup(e1, e2, e2_tag, e3).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([3.4, 0.0, 0])
        self.play(FadeIn(title), FadeIn(dev), FadeIn(dev_l))
        self.play(Create(front), FadeIn(front_l))
        self.play(FadeIn(back, shift=UP * 0.2), Create(vias), FadeIn(back_l))
        self.play(Write(e1))
        self.play(FadeIn(e2), FadeIn(e2_tag))
        self.play(FadeIn(e3))
        note = layout_note("With power on the back, the front metal is all signal: no V_DD and GND rails "
                           "in the cell's M0, and taps and power straps move with them.", size=20, width=46)
        note.to_corner(DL, buff=0.35)
        self.play(FadeIn(note, shift=UP * 0.15))

    def heat(self):
        self.slide(say(
            """
            And there's heat. Two transistors in the footprint of one is twice the power in the
            same area. The temperature rise is power times thermal resistance, and the top tier
            sits further from where the heat leaves the chip, through more layers of material
            that don't conduct heat well. Stacking packs in more switches, and it also stacks the
            heat.
            """,
            """
            আর আছে heat। একটার জায়গায় দুইটা transistor মানে একই area-তে দুইগুণ power। Temperature কতটা বাড়বে সেটা হইলো
            power গুণ thermal resistance, আর উপরের tier chip থেকে heat যেখান দিয়া বের হয় সেখান থেকে আরও দূরে, এমন আরও কয়েক
            layer material-এর ভিতর দিয়া যেগুলা heat ভালো conduct করে না। Stack করলে বেশি switch ঢুকে, আর heat-ও stack হয়।
            """,
        ))
        self.clear()
        title = heading("Stacking stacks the heat too")
        e = eq(r"\Delta T", r"=", r"P", r"\;R_{th}", size=80)
        e[0].set_color(THERMAL)
        e.move_to([0, 1.0, 0])
        lines = VGroup(
            text("twice the transistors per area: up to twice the power density", size=26),
            text("the upper tier is further from the heat path, through poor heat conductors", size=26),
        ).arrange(DOWN, buff=0.3).move_to([0, -1.2, 0])
        tag = text("Qualitative", size=18, color=MUTED).to_corner(DR, buff=0.35)
        self.play(FadeIn(title), Write(e))
        for ln in lines:
            self.play(FadeIn(ln, shift=UP * 0.1))
        self.play(FadeIn(tag))

    # --- cliffhanger -------------------------------------------------------------------------
    def cliffhanger(self):
        self.slide(say(
            """
            Step back and look at chapters 6 to 10 together. Every step did the same two things:
            a thinner channel, and more gate around it. We're now at sheets 5 nanometres thick,
            about 37 layers of silicon atoms. Thinner than that, and silicon's electrons stop moving
            well. So the next question is radical: what if the channel weren't silicon at all, but
            a material just one molecule thick? And what if the switch didn't have to climb
            Boltzmann's hill? That's chapter 11.
            """,
            """
            একটু পিছায়ে chapter 6 থেকে 10 একসাথে দেখেন। প্রত্যেক ধাপে একই দুইটা কাজ: channel আরও পাতলা, আর তার চারপাশে আরও
            gate। আমরা এখন 5 nanometre পুরু sheet-এ, মোটামুটি silicon atom-এর 37টা layer। এর চেয়ে পাতলা হলে silicon-এর electron
            আর ভালো চলে না। তাই পরের প্রশ্নটা অনেক বড়: channel যদি silicon না হয়ে একটা মাত্র molecule পুরু কোনো material হয়?
            আর switch-রে যদি Boltzmann-এর hill বাইতেই না হয়? সেইটা chapter 11।
            """,
        ))
        self.clear()
        a = text("Thinner channel. More gate. Every time.", size=42, weight="SEMIBOLD").to_edge(UP, buff=0.7)
        shapes = VGroup(*[xsection(k).scale_to_fit_height(1.3) for k in ("planar", "finfet", "nanosheet", "forksheet", "cfet")])
        shapes.arrange(RIGHT, buff=0.6, aligned_edge=DOWN).move_to([0, 0.4, 0])
        years = VGroup(*[text(y, size=20, color=MUTED).next_to(s, DOWN, buff=0.2)
                         for y, s in zip(("planar", "2011", "2022", "~2030", "~2033"), shapes)])
        b = text("Next: beyond silicon, and beyond Boltzmann.", size=34, color=GATE).to_edge(DOWN, buff=0.9)
        self.play(FadeIn(a))
        self.play(LaggedStart(*[FadeIn(VGroup(s, y), shift=UP * 0.15) for s, y in zip(shapes, years)], lag_ratio=0.3), run_time=2.5)
        self.play(FadeIn(b))
        self.wait(1)

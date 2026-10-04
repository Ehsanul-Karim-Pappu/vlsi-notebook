"""Chapter 8 · Nanosheets: the gate goes all the way around (2017–2025).

The fin turned on its side and sliced into sheets, gated on four faces. Its width is continuous
again; the trick that makes it is a sacrificial SiGe layer etched away from between the sheets.
What stops it shrinking further: the space between n and p, and the cell's height.
"""

import sys
from pathlib import Path

LECTURE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(LECTURE.parents[1]), str(LECTURE)]

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403
from manim_slides import ThreeDSlide  # noqa: E402

import physics as phys  # noqa: E402
from devicedata import NANOSHEET, device  # noqa: E402
from kit.devices3d import LAYOUT_OPACITY, beside, build_device, plan_view  # noqa: E402
from kit.motifs import xsection  # noqa: E402
from kit.style import *  # noqa: E402,F403

CHANNEL = "#7FD8E4"  # the channel sheets, picked out from the rest of the silicon
SIGE = "#B37FA0"  # FET Lab's SiGe
INNER = "#D8C06A"  # inner spacer (SiBCN)
FILL = "#5A6270"  # oxide fill over the source and drain
GE_RICH = "#7A4A6E"  # the Ge-rich SiGe layer that becomes the bottom isolation
BOTTOM_ISO = "#C9D4DE"  # bottom dielectric isolation
N_SH, W_SH, T_SH = 3, 30, 5  # FET Lab's nanosheet model, nm
LAYOUT_FIN, LAYOUT_NS = device("show_fin"), device("show_ns")


def box(x0, x1, y0, y1, color, opacity=1.0):
    """A rectangle between two corners, for the process cross-section."""
    return Rectangle(width=x1 - x0, height=y1 - y0, fill_color=color, fill_opacity=opacity,
                     stroke_width=0).move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])


class Ch08Nanosheet(Chapter, ThreeDSlide):
    def construct(self):
        self.card()
        self.history()
        self.model()
        self.width()
        self.process()
        self.layout()
        self.limits()
        self.cliffhanger()

    def flat(self):
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0, frame_center=ORIGIN)

    # --- chapter card ------------------------------------------------------------------------
    def card(self):
        self.slide(say(
            """
            Turn the fin on its side, slice it into sheets, and wrap the gate around every one.
            It sounds simple. Building it took one of the cleverest tricks in the whole story.
            """,
            """
            Fin-টারে কাত করে শোয়ান, sheet-এ কাটেন, আর প্রত্যেকটার চারপাশে gate মুড়ে দেন। শুনতে সহজ। বানাইতে লাগছে
            পুরা গল্পের সবচেয়ে চালাক একটা কৌশল।
            """,
        ))
        self.card_group = self.open_chapter(8, 2022, 2011, "Nanosheets", "The gate goes all the way around")

    # --- history -----------------------------------------------------------------------------
    def history(self):
        self.slide(say(
            """
            In 2017, IBM, GlobalFoundries and Samsung showed stacked silicon nanosheets with the
            gate all the way around, as the way to scale beyond the FinFET. On the 30th of June
            2022, Samsung started making chips with them at 3 nanometres, the first in
            production. TSMC's N2 followed at the end of 2025, and Intel's 18A, which Intel calls
            RibbonFET, the same year, with power delivered from the back of the wafer.
            """,
            """
            2017-এ IBM, GlobalFoundries আর Samsung stacked silicon nanosheet দেখায়, চারদিক ঘেরা gate সহ, FinFET-এর পরের
            ধাপ হিসাবে। 2022-এর 30 June Samsung 3 nanometre-এ এগুলা দিয়া chip বানানো শুরু করে, production-এ প্রথম।
            TSMC-র N2 আসে 2025-এর শেষে, আর Intel-এর 18A, Intel যেটারে বলে RibbonFET, একই বছরে, wafer-এর পেছন দিয়া power
            দেওয়ার ব্যবস্থা সহ।
            """,
        ))
        self.play(FadeOut(self.card_group))
        title = heading("From the lab to production in five years")
        line = Line([-5.6, -0.2, 0], [5.6, -0.2, 0], stroke_color=FAINT, stroke_width=3)
        events = [
            (-4.4, "2017", "Stacked nanosheets", "IBM, GlobalFoundries\nand Samsung", "N. Loubet et al., VLSI 2017"),
            (0.0, "2022", "Samsung 3 nm", "the first in production\n(30 June 2022)", "Samsung press release"),
            (4.4, "2025", "TSMC N2, Intel 18A", "Intel's RibbonFET adds\npower from the back", "TSMC; Intel"),
        ]
        self.play(FadeIn(title), Create(line))
        for x, year, what, why, who in events:
            dot = Dot([x, -0.2, 0], color=GATE, radius=0.1)
            y = display(year, size=48, color=GATE).move_to([x, 0.75, 0])
            body = VGroup(text(what, size=26, weight="SEMIBOLD"), text(why, size=22, color=MUTED),
                          text(who, size=16, color=MUTED)).arrange(DOWN, buff=0.15).next_to(dot, DOWN, buff=0.4)
            icon = xsection("nanosheet").scale_to_fit_height(0.75).next_to(y, UP, buff=0.3)
            self.play(FadeIn(dot, scale=0.5), FadeIn(y), FadeIn(icon), FadeIn(body, shift=UP * 0.1), run_time=0.9)

    # --- the 3D model, cut across ------------------------------------------------------------
    def model(self):
        self.slide(say(
            """
            Remember the nanosheet transistor from the start of the lecture? Here it is again, and
            this time we cut it across, through the gate. Three sheets of silicon, five nanometres
            thick and thirty wide. And around every one of them, all four sides: the oxide, the
            high-k, the work-function metal, then the gate fill. In our toy model, N sits
            somewhere between two and four: a wide, thin sheet is gated mostly from above and
            below, and the narrow edges help less. So lambda is roughly two to two and a half
            nanometres. It's a toy number; real designs use a model for the real shape.
            """,
            """
            Lecture-এর শুরুর nanosheet transistor-টা মনে আছে? এই যে আবার, আর এইবার gate-এর মাঝখান দিয়া আড়াআড়ি কাটি। তিনটা
            silicon sheet, পাঁচ nanometre পুরু, ত্রিশ চওড়া। আর প্রত্যেকটার চারপাশে, চার দিকেই: oxide, high-k,
            work-function metal, তারপর gate fill। আমাদের toy model-এ N দুই থেকে চারের মাঝামাঝি কোথাও: চওড়া, পাতলা
            sheet-রে gate মূলত উপর আর নিচ থেকে ধরে, সরু কিনারাগুলা কম সাহায্য করে। তাই lambda মোটামুটি দুই থেকে আড়াই
            nanometre। এইটা toy সংখ্যা; আসল design-এ আসল আকারের জন্য model লাগে।
            """,
        ))
        self.clear()
        self.set_camera_orientation(phi=64 * DEGREES, theta=-58 * DEGREES, zoom=0.75, frame_center=beside(-58 * DEGREES, -1.6))
        order = ["Substrate & isolation", "Channel stack", "Gate-all-around stack", "Gate electrode", "Spacers", "Source / drain"]
        contacts = {"gatew", "nisi_source", "ni_source", "w_source", "nisi_drain", "ni_drain", "w_drain"}
        kw = dict(scale=0.05, groups=order, skip=contacts, recolor={f"sheet{i}": CHANNEL for i in (1, 2, 3)})
        back, _ = build_device(NANOSHEET, clip={"x": (None, 0.0)}, **kw)
        front, _ = build_device(NANOSHEET, clip={"x": (0.0, None)}, **kw)
        shift = -VGroup(back, front).get_center() + np.array([0, 0, -0.2])
        back.shift(shift)
        front.shift(shift)
        src = source("Model: FET Lab's nanosheet nFET (5 nm sheets, 30 nm wide), after IBM US 2023/0420457 A1")
        lam_hi, lam_lo = phys.natural_length_nm(T_SH, 1, 2), phys.natural_length_nm(T_SH, 1, 4)
        cut = text("cut across the gate", size=26, color=GATE)
        info = VGroup(cut, text("the gate covers all four\nfaces of every sheet", size=26, weight="SEMIBOLD"),
                      MathTex(r"N \approx 2\text{ to }4", font_size=36, color=GATE),
                      MathTex(rf"\lambda \approx {lam_lo:.1f}\text{{ to }}{lam_hi:.1f}\ \text{{nm}}", font_size=36, color=GATE),
                      MathTex(rf"6\lambda \approx {6 * lam_lo:.0f}\text{{ to }}{6 * lam_hi:.0f}\ \text{{nm}}", font_size=36, color=GATE),
                      text("toy model, not a design value", size=18, color=MUTED),
                      ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([4.6, 0.3, 0])
        self.add_fixed_in_frame_mobjects(src, info)
        self.remove(src, info)
        self.play(FadeIn(VGroup(back, front), shift=IN * 0.6), FadeIn(src), run_time=1.5)
        self.play(FadeOut(front, shift=RIGHT * 3), FadeIn(cut), run_time=1.6)
        self.move_camera(phi=82 * DEGREES, theta=-4 * DEGREES, zoom=0.95, frame_center=beside(-4 * DEGREES, -1.8), run_time=2.5)
        self.play(FadeIn(info[1:]))
        self.parts3d = VGroup(back, src, info)

    # --- width -------------------------------------------------------------------------------
    def width(self):
        self.slide(say(
            """
            Its width: current flows on all four faces of each sheet, so each sheet is worth twice
            its width plus twice its thickness. Three sheets, 30 by 5: 210 nanometres. That's
            more than the two-fin FinFET's 192, on about the same floor: two fins at a 27
            nanometre pitch are given 54 nanometres, and one 30 nanometre sheet needs a little
            room on each side.
            """,
            """
            এর width: প্রত্যেকটা sheet-এর চার মুখ দিয়াই current যায়, তাই প্রত্যেকটা sheet-এর দাম দুইগুণ width যোগ দুইগুণ
            thickness। তিনটা sheet, 30 বাই 5: 210 nanometre। দুই fin-এর FinFET-এর 192-এর চেয়ে বেশি, মোটামুটি একই
            জায়গায়: 27 nanometre pitch-এ দুইটা fin-রে 54 nanometre ধরা হয়, আর 30 nanometre-এর একটা sheet-এর দুই পাশে
            একটু ফাঁক লাগে।
            """,
        ))
        self.play(FadeOut(self.parts3d))
        self.flat()
        title = heading("The width of a stack of sheets")
        u = 0.055
        cx, y0 = -3.0, -2.5
        wt = ValueTracker(W_SH)

        def stack():
            w = wt.get_value() * u
            g = VGroup()
            gate = Rectangle(width=w + 16 * u, height=(3 * 21 + 6) * u, fill_color=GATE, fill_opacity=0.25,
                             stroke_color=GATE, stroke_width=2).move_to([cx, y0 + (3 * 21 + 6) * u / 2, 0])
            g.add(gate)
            for i in range(N_SH):
                yc = y0 + (8 + i * 21 + T_SH / 2) * u
                sheet = Rectangle(width=w, height=T_SH * u, fill_color=CHANNEL, fill_opacity=1, stroke_width=0).move_to([cx, yc, 0])
                ring = Rectangle(width=w + 0.1, height=T_SH * u + 0.1, stroke_color=ELECTRON, stroke_width=5).move_to([cx, yc, 0])
                g.add(sheet, ring)
            return g

        pic = always_redraw(stack)
        sub = Rectangle(width=6.0, height=0.5, fill_color=SUBSTRATE, fill_opacity=1, stroke_width=0).move_to([cx, y0 - 0.25, 0])
        w_l = always_redraw(lambda: MathTex(rf"W_{{sh}} = {wt.get_value():.0f}", font_size=30, color=MUTED)
                            .next_to(pic, UP, buff=0.15))
        t_l = MathTex(rf"T_{{sh}} = {T_SH}", font_size=30, color=MUTED).next_to(pic, RIGHT, buff=0.3).shift(UP * 0.9)
        e1 = eq(r"W_{eff}", r"=", r"N_{sh}", r"\cdot 2\,(W_{sh}+T_{sh})", size=48)
        e1[0].set_color(ELECTRON)
        weff = always_redraw(lambda: MathTex(rf"= 3\cdot 2\,({wt.get_value():.0f}+{T_SH}) = {phys.weff_sheets_nm(3, wt.get_value(), T_SH):.0f}\ \text{{nm}}",
                                             font_size=42, color=INK).next_to(e1, DOWN, buff=0.35).align_to(e1, LEFT))
        cmp = text(f"two-fin FinFET: {phys.weff_fin_nm(2, 45, 6)} nm", size=24, color=MUTED)
        col = VGroup(e1, Rectangle(width=0.1, height=0.75, stroke_width=0, fill_opacity=0), cmp).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        col.move_to([3.3, 0.6, 0])
        self.play(FadeIn(title), FadeIn(sub), FadeIn(pic), FadeIn(w_l), FadeIn(t_l))
        self.play(Write(e1))
        self.play(FadeIn(weff))
        self.play(FadeIn(cmp))

        self.slide(say(
            """
            And here's the part layout people care about. The sheet width isn't fixed by a fin
            height. It's set by the mask, so it can be drawn. Make the sheets narrower, 15
            nanometres, or wider, 45: the width changes smoothly. After a decade of counting fins,
            width is something you draw again, within what the rules allow.
            """,
            """
            আর এইখানে layout-এর লোকদের আসল আগ্রহ। Sheet-এর width কোনো fin height দিয়া fix না। এইটা mask দিয়া ঠিক হয়,
            তাই আঁকা যায়। Sheet সরু করেন, 15 nanometre, বা চওড়া, 45: width মসৃণভাবে বদলায়। দশ বছর fin গোনার পর width আবার
            এমন জিনিস যেটা আপনি আঁকেন, rule যতটা allow করে তার মধ্যে।
            """,
        ))
        drawn = text("width is drawn again", size=28, color=GOOD, weight="SEMIBOLD").move_to([3.3, -1.6, 0])
        self.play(wt.animate.set_value(15), run_time=2)
        self.play(wt.animate.set_value(45), run_time=2.5)
        self.play(wt.animate.set_value(W_SH), FadeIn(drawn), run_time=1.5)

    # --- the process: the magic trick --------------------------------------------------------
    def process(self):
        self.slide(say(
            """
            How do you put a gate under a sheet of silicon? You don't. You grow the space for it
            first, and fill it later. Here's one common route, for an n-type device. Start with
            the wafer. First a thin layer of silicon-germanium with extra germanium in it:
            remember it, it has a job later. Then grow a stack: silicon-germanium, silicon,
            silicon-germanium, silicon, a few nanometres each. The silicon layers will be the
            channels. The silicon-germanium is just a placeholder. We're looking from the side
            now, along the channel.
            """,
            """
            Silicon-এর একটা sheet-এর নিচে gate বসাবেন কীভাবে? বসান না। আগে ওই জায়গাটা grow করেন, পরে ভরেন। এইটা একটা
            প্রচলিত পথ, n-type device-এর জন্য। Wafer দিয়া শুরু করেন। প্রথমে silicon-germanium-এর একটা পাতলা layer, যেটাতে
            germanium একটু বেশি: এইটা মনে রাখেন, পরে এর একটা কাজ আছে। তারপর একটা stack grow করেন: silicon-germanium,
            silicon, silicon-germanium, silicon, প্রত্যেকটা কয়েক nanometre। Silicon layer-গুলা হবে channel।
            Silicon-germanium শুধু জায়গা ধরে রাখে। এখন আমরা পাশ থেকে দেখতেছি, channel বরাবর।
            """,
        ))
        self.clear()
        title = heading("How to build a gate under a sheet")
        self.play(FadeIn(title))
        X = 4.4
        sige_y = [(-2.0, -1.68), (-1.46, -1.14), (-0.92, -0.60)]
        si_y = [(-1.68, -1.46), (-1.14, -0.92), (-0.60, -0.38)]
        sub = box(-X, X, -3.0, -2.3, SUBSTRATE)
        rich = box(-X, X, -2.3, -2.0, GE_RICH)
        sige = VGroup(*[box(-X, X, a, b, SIGE) for a, b in sige_y])
        si = VGroup(*[box(-X, X, a, b, CHANNEL) for a, b in si_y])

        def swatch(color, label):
            return VGroup(Square(0.22, fill_color=color, fill_opacity=1, stroke_width=0),
                          text(label, size=18, color=MUTED)).arrange(RIGHT, buff=0.12)

        key = VGroup(swatch(CHANNEL, "silicon: the channels"), swatch(SIGE, "SiGe: a placeholder"),
                     swatch(BOTTOM_ISO, "bottom insulator"), swatch(INNER, "inner spacer")).arrange(RIGHT, buff=0.45)
        key.move_to([0, 2.65, 0])
        late = (key[3].width + 0.45) / 2  # the inner spacer joins the key later; centre the rest until then
        key[:3].shift(RIGHT * late)
        rich_key = swatch(GE_RICH, "Ge-rich SiGe").move_to(key[2], aligned_edge=LEFT)
        cap = text("1 · Grow a stack: SiGe and Si, a few nanometres each", size=24, color=INK).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(sub), FadeIn(cap))
        self.play(GrowFromEdge(rich, DOWN), run_time=0.45)
        for a, b in zip(sige, si):
            self.play(GrowFromEdge(a, DOWN), run_time=0.45)
            self.play(GrowFromEdge(b, DOWN), run_time=0.45)
        self.play(FadeIn(key[:2]), FadeIn(rich_key))

        self.slide(say(
            """
            Next, a dummy gate: a block of polysilicon that marks where the real gate will go,
            with insulating spacers on its sides. Now that germanium-rich layer at the bottom: an
            etch that attacks only it takes it away, and insulator fills the gap. That's the
            bottom isolation. It will cut the transistor off from the wafer. Then etch the stack
            away outside the spacers, down to that insulator. Now the trick's first half: a
            selective etch eats a little way into the silicon-germanium layers only, from the
            sides, leaving notches under the spacers. Fill the notches with insulator: these are
            the inner spacers. They'll keep the gate away from the source and drain.
            """,
            """
            এরপর একটা dummy gate: polysilicon-এর একটা block, আসল gate কোথায় বসবে সেটা চিহ্ন দিয়া রাখে, দুই পাশে
            insulating spacer। এবার নিচের ওই germanium-বেশি layer-টা: একটা etch শুধু ওইটারেই খায়, সরায়ে ফেলে, আর ফাঁকটা
            insulator দিয়া ভরে যায়। এইটা bottom isolation। এইটা transistor-রে wafer থেকে আলাদা করে দিবে। তারপর spacer-এর
            বাইরে stack-টা etch করে ফেলেন, ওই insulator পর্যন্ত। এবার কৌশলের প্রথম অর্ধেক: একটা selective etch শুধু
            silicon-germanium layer-গুলারে পাশ থেকে একটু খেয়ে ফেলে, spacer-এর নিচে খাঁজ রেখে। খাঁজগুলা insulator দিয়া
            ভরেন: এইগুলা inner spacer। এগুলা gate-রে source আর drain থেকে দূরে রাখবে।
            """,
        ))
        dummy = box(-0.7, 0.7, -0.38, 1.4, "#8FA67A")
        hm = box(-0.7, 0.7, 1.4, 1.7, "#9AA7B8")
        sp = VGroup(box(-1.0, -0.7, -0.38, 1.7, NITRIDE), box(0.7, 1.0, -0.38, 1.7, NITRIDE))
        self.play(FadeIn(dummy, shift=DOWN * 0.2), FadeIn(hm, shift=DOWN * 0.2),
                  Transform(cap, text("2 · A dummy gate, with spacers", size=24).to_edge(DOWN, buff=0.4)))
        self.play(FadeIn(sp))
        self.wait(0.3)
        bdi = box(-X, X, -2.3, -2.0, BOTTOM_ISO)
        self.play(FadeOut(rich), Transform(cap, text("3 · Swap the Ge-rich layer for insulator: bottom isolation", size=24).to_edge(DOWN, buff=0.4)))
        self.play(FadeIn(bdi), ReplacementTransform(rich_key, key[2]))
        si_c = VGroup(*[box(-1.0, 1.0, a, b, CHANNEL) for a, b in si_y])
        sige_c = VGroup(*[box(-1.0, 1.0, a, b, SIGE) for a, b in sige_y])
        self.play(ReplacementTransform(si, si_c), ReplacementTransform(sige, sige_c),
                  Transform(cap, text("4 · Etch the stack away outside the spacers, down to the insulator", size=24).to_edge(DOWN, buff=0.4)), run_time=1.5)
        sige_i = VGroup(*[box(-0.75, 0.75, a, b, SIGE) for a, b in sige_y])
        self.play(ReplacementTransform(sige_c, sige_i),
                  Transform(cap, text("5 · Etch a notch into the SiGe only, from the sides", size=24).to_edge(DOWN, buff=0.4)), run_time=1.5)
        inner = VGroup(*[VGroup(box(-1.0, -0.75, a, b, INNER), box(0.75, 1.0, a, b, INNER)) for a, b in sige_y])
        self.play(FadeIn(inner), Transform(cap, text("6 · Fill the notches: inner spacers", size=24).to_edge(DOWN, buff=0.4)))
        self.play(key[:3].animate.shift(LEFT * late), FadeIn(key[3]))

        self.slide(say(
            """
            Grow the source and drain, silicon full of donor atoms, from the exposed ends of the
            sheets. They sit on the bottom insulator, so they're connected to the sheets, and
            only to the sheets, not to the wafer. Then cover everything with oxide. Real flows
            also polish the top flat here, and do much else; we're leaving those steps out.
            """,
            """
            Sheet-গুলার খোলা মাথা থেকে source আর drain grow করেন: donor atom-এ ভরা silicon। এগুলা নিচের insulator-এর
            উপর বসা, তাই এগুলা sheet-গুলার সাথে জোড়া, শুধু sheet-গুলার সাথেই, wafer-এর সাথে না। তারপর সবকিছু oxide
            দিয়া ঢেকে দেন। আসল process-এ এইখানে উপরটা polish করে সমানও করা হয়, আরও অনেক কিছু হয়; ওই ধাপগুলা আমরা বাদ
            দিতেছি।
            """,
        ))
        epi = VGroup(box(-3.9, -1.0, -2.0, 0.0, ELECTRON, 0.55), box(1.0, 3.9, -2.0, 0.0, ELECTRON, 0.55))
        epi_l = VGroup(text("source", size=22, color=INK).move_to(epi[0]), text("drain", size=22, color=INK).move_to(epi[1]))
        fill = VGroup(box(-X, -1.0, 0.0, 1.7, FILL), box(1.0, X, 0.0, 1.7, FILL))
        self.play(GrowFromEdge(epi[0], DOWN), GrowFromEdge(epi[1], DOWN), FadeIn(epi_l),
                  Transform(cap, text("7 · Grow the source and drain from the sheets' ends", size=24).to_edge(DOWN, buff=0.4)), run_time=1.5)
        self.play(FadeIn(fill), Transform(cap, text("8 · Cover with oxide", size=24).to_edge(DOWN, buff=0.4)))

        self.slide(say(
            """
            Now the magic. Pull out the dummy gate: there's a trench where it was. And then a
            second selective etch reaches down the trench and dissolves the silicon-germanium
            between the sheets, and leaves the silicon. The sheets are left hanging in mid-air,
            held at their ends by the source and the drain. Every gap is now a place for gate.
            """,
            """
            এবার আসল জাদু। Dummy gate-টা তুলে ফেলেন: যেখানে ছিল সেখানে একটা trench। তারপর দ্বিতীয় একটা selective etch
            trench দিয়া নেমে sheet-গুলার মাঝের silicon-germanium গলায়ে ফেলে, আর silicon রেখে দেয়। Sheet-গুলা শূন্যে ঝুলে
            থাকে, দুই মাথায় source আর drain ধরে রাখছে। প্রত্যেকটা ফাঁক এখন gate-এর জায়গা।
            """,
        ))
        self.play(FadeOut(dummy, shift=UP * 0.4), FadeOut(hm, shift=UP * 0.4),
                  Transform(cap, text("9 · Pull out the dummy gate", size=24).to_edge(DOWN, buff=0.4)))
        self.play(FadeOut(sige_i, scale=0.6), Transform(cap, text("10 · Dissolve the SiGe: the sheets are released", size=24, color=GATE).to_edge(DOWN, buff=0.4)),
                  run_time=2.0)
        float_l = text("hanging between source and drain", size=20, color=GATE).move_to([0, 2.15, 0])
        self.play(FadeIn(float_l), FadeOut(key[1]))

        self.slide(say(
            """
            Finally, coat every exposed surface with oxide and high-k, then fill the trench and
            every gap with metal. The gate now wraps all the way around each sheet. That's one
            common way to make stacked nanosheets. A p-type device often takes a slightly
            different path, and real flows have many more steps. But the idea at the heart of it
            is the same: build the space for the gate out of a material you'll later dissolve.
            """,
            """
            শেষে খোলা সব surface-এ oxide আর high-k-এর আস্তর দেন, তারপর trench আর প্রত্যেকটা ফাঁক metal দিয়া ভরেন। Gate
            এখন প্রত্যেকটা sheet-এর চারপাশ ঘিরে আছে। Stacked nanosheet বানানোর এইটা একটা প্রচলিত পথ। p-type device অনেক
            সময় একটু অন্য পথে যায়, আর আসল process-এ আরও অনেক ধাপ থাকে। কিন্তু মূল idea-টা একই: gate-এর জায়গাটা এমন একটা
            material দিয়া বানান, যেটা পরে গলায়ে ফেলবেন।
            """,
        ))
        liners = VGroup(*[Rectangle(width=1.5, height=b - a + 0.08, stroke_color=HIGHK, stroke_width=5).move_to([0, (a + b) / 2, 0])
                          for a, b in si_y])
        metal = VGroup(box(-0.7, 0.7, -0.38, 1.7, GATE), *[box(-0.75, 0.75, a, b, GATE) for a, b in sige_y])
        self.play(Create(liners), Transform(cap, text("11 · Line every surface: oxide and high-k", size=24).to_edge(DOWN, buff=0.4)))
        self.play(FadeIn(metal), liners.animate.set_z_index(3), si_c.animate.set_z_index(4), FadeOut(float_l),
                  Transform(cap, text("12 · Fill with metal: the gate, all the way around", size=24, color=GATE).to_edge(DOWN, buff=0.4)), run_time=1.5)
        src = text("One common nFET route, after IBM US 2023/0420457 A1 (which also describes a SiGe pFET branch).\n"
                   "Simplified: polishing and other steps left out; not to scale.",
                   size=16, color=MUTED, line_spacing=0.9).move_to([0, 2.12, 0])
        self.play(FadeIn(src))

    # --- layout ------------------------------------------------------------------------------
    def layout(self):
        self.slide(say(
            """
            From above, the change is easy to see. Left, the FinFET inverter: two narrow fins per
            transistor. Right, the nanosheet inverter: one wide sheet per transistor, its width
            set by the drawn shape. The gates, contacts and rails look just the same.
            """,
            """
            উপর থেকে দেখলে পরিবর্তনটা সহজে বোঝা যায়। বামে FinFET inverter: প্রত্যেক transistor-এ দুইটা সরু fin। ডানে
            nanosheet inverter: প্রত্যেক transistor-এ একটা চওড়া sheet, তার width আঁকা shape দিয়া ঠিক হয়। Gate, contact
            আর rail দেখতে একই রকম।
            """,
        ))
        self.clear()
        title = heading("Fins and sheets, from above")
        skip = ("pwell", "fox", "vd_gnd", "vd_vdd", "vd_out", "vg", "m0_in", "m0_out")
        fin, fin_by = plan_view(LAYOUT_FIN, scale=0.029, skip=skip, opacity=LAYOUT_OPACITY)
        ns, ns_by = plan_view(LAYOUT_NS, scale=0.029, skip=skip, opacity=LAYOUT_OPACITY)
        fin.move_to([-3.2, -0.4, 0])
        ns.move_to([3.2, -0.4, 0]).align_to(fin, DOWN)
        fl = text("FinFET: 2 fins each", size=24, color=MUTED).next_to(fin, DOWN, buff=0.2)
        nl = text("nanosheet: 1 drawn sheet each", size=24, color=MUTED).next_to(ns, DOWN, buff=0.2)
        self.play(FadeIn(title))
        self.play(FadeIn(fin), FadeIn(fl))
        self.play(FadeIn(ns), FadeIn(nl))
        self.fin_view, self.ns_view, self.ns_by = VGroup(fin, fl), VGroup(ns, nl), ns_by
        self.layout_title = title

    def limits(self):
        self.slide(say(
            """
            So what stops the nanosheet? Look at the cell's height. It's set by the routing: the
            number of metal tracks times the metal pitch. For example, six tracks at 24
            nanometres is 144, and five is 120. This model's rails sit 136 nanometres apart,
            centre to centre: a different example, and people draw the cell's edge in slightly
            different places. To make the cell shorter you take tracks away, and then everything
            inside has to squeeze. And look at the gap between the n sheets and the p sheets.
            Here it's 46 nanometres, a third of the cell. It can't shrink much, because the n
            and the p transistors need different gate metals, and those have to be patterned
            apart with room to spare.
            """,
            """
            তাহলে nanosheet-রে আটকায় কে? Cell-এর height দেখেন। এইটা routing দিয়া ঠিক হয়: metal track-এর সংখ্যা গুণ
            metal pitch। যেমন, 24 nanometre-এ ছয়টা track মানে 144, আর পাঁচটা মানে 120। এই model-এর rail দুইটা
            center থেকে center 136 nanometre দূরে: এইটা আরেকটা উদাহরণ, আর cell-এর কিনারা সবাই ঠিক একই জায়গায় ধরে না।
            Cell ছোট করতে track কমাইতে হয়, আর তখন ভিতরের সবকিছু চাপতে হয়। আর n sheet আর p sheet-এর মাঝের ফাঁকটা দেখেন। এইখানে 46 nanometre, cell-এর তিন ভাগের এক
            ভাগ। এইটা খুব একটা কমানো যায় না, কারণ n আর p transistor-এর আলাদা gate metal লাগে, আর সেগুলারে যথেষ্ট জায়গা
            রেখে আলাদা করে pattern করতে হয়।
            """,
        ))
        self.play(FadeOut(self.fin_view), self.ns_view.animate.move_to([-2.9, -0.4, 0]),
                  Transform(self.layout_title, heading("What stops the nanosheet")))
        by = self.ns_by
        n_top = by["n_w1"].get_top()[1]
        p_bot = by["p_w1"].get_bottom()[1]
        x = by["m0_vdd"].get_right()[0] + 0.3
        gap = DoubleArrow([x, n_top, 0], [x, p_bot, 0], buff=0, stroke_color=DRAIN, stroke_width=4, tip_length=0.14)
        gap_l = text("n-to-p space\n46 nm (model)", size=20, color=DRAIN).next_to(gap, RIGHT, buff=0.12)
        r0, r1 = by["m0_gnd"].get_center()[1], by["m0_vdd"].get_center()[1]
        xl = by["m0_gnd"].get_left()[0] - 0.3
        h = DoubleArrow([xl, r0, 0], [xl, r1, 0], buff=0, stroke_color=GATE, stroke_width=4, tip_length=0.14)
        span = round((r1 - r0) / 0.029)  # rail centre to rail centre, in nm (plan_view scale)
        h_l = text(f"rail to rail\n{span} nm (model)", size=20, color=GATE).rotate(PI / 2).next_to(h, LEFT, buff=0.1)
        e1 = eq(r"H_{cell}", r"=", r"\text{tracks}", r"\times", r"\text{metal pitch}", size=42)
        e1[0].set_color(GATE)
        e2 = VGroup(text("For example:", size=20, color=MUTED),
                    text(f"6 tracks × 24 nm = {phys.cell_height_nm(6, 24)} nm\n5 tracks × 24 nm = {phys.cell_height_nm(5, 24)} nm",
                         size=24, color=INK)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        e3 = text("Take a track away and everything\ninside must squeeze, including\nthe space between n and p.", size=22, color=MUTED)
        VGroup(e1, e2, e3).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to([3.7, 0.0, 0])
        self.play(GrowFromCenter(h), FadeIn(h_l))
        self.play(Write(e1))
        self.play(FadeIn(e2))
        self.play(GrowFromCenter(gap), FadeIn(gap_l))
        self.play(FadeIn(e3))

    # --- cliffhanger -------------------------------------------------------------------------
    def cliffhanger(self):
        self.slide(say(
            """
            So what if the n and the p sheets didn't need space between them? What if you put a
            thin insulating wall right down the middle, and pushed both stacks up against it?
            """,
            """
            তাহলে n আর p sheet-এর মাঝে যদি জায়গা লাগতো না? যদি মাঝখান বরাবর একটা পাতলা insulating দেয়াল বসায়ে দুই
            stack-রেই ওইটার গায়ে ঠেলে দিতেন?
            """,
        ))
        self.clear()
        a = text("Close the gap: put a wall between n and p.", size=42, weight="SEMIBOLD").to_edge(UP, buff=0.7)
        n = xsection("nanosheet").scale(1.1).move_to([-2.0, -1.0, 0])
        p = xsection("nanosheet").scale(1.1).move_to([2.0, -1.0, 0])
        for s in p[2]:
            s[1].set_fill(HOLE, opacity=0.85)
        fs = xsection("forksheet").scale(1.1).move_to([0, -1.0, 0])
        nl = text("n", size=30, color=ELECTRON).next_to(n, DOWN, buff=0.2)
        pl = text("p", size=30, color=HOLE).next_to(p, DOWN, buff=0.2)
        self.play(FadeIn(a), FadeIn(n), FadeIn(p), FadeIn(nl), FadeIn(pl))
        self.wait(0.4)
        self.play(ReplacementTransform(VGroup(n, p), fs), nl.animate.next_to(fs, DOWN, buff=0.2).shift(LEFT * 0.6),
                  pl.animate.next_to(fs, DOWN, buff=0.2).shift(RIGHT * 0.6), run_time=2.0)
        self.wait(1)

"""Chapter 1 · The switch nobody could build (1904–1947).

The vacuum tube and its heat, ENIAC, Lilienfeld's 1925 field-effect patent, and why it failed:
Bardeen's surface states swallow the gate's charge.
"""

import sys
from pathlib import Path

LECTURE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(LECTURE.parents[1]), str(LECTURE)]

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403
from manim_slides import Slide  # noqa: E402

import physics as phys  # noqa: E402
from kit.style import *  # noqa: E402,F403


class Ch01BeforeTheSwitch(Chapter, Slide):
    def construct(self):
        self.card()
        self.tube()
        self.eniac()
        self.lilienfeld()
        self.surface_states()
        self.cliffhanger()

    # --- card --------------------------------------------------------------------------------
    def card(self):
        self.slide(tr(
            """
            Before we get to that 1925 patent, we need to know what it was trying to replace. In
            the 1920s, if you wanted an electrical switch with no moving parts, you had exactly one
            option: the vacuum tube.
            """,
            """
            ওই 1925-এর patent-এ যাওয়ার আগে দেখা দরকার, ওইটা আসলে কী replace করতে চাইছিল। 1920-এর
            দশকে যদি এমন একটা electrical switch চাইতেন যেটায় কোনো moving part নাই, তাহলে option ছিল
            একটাই: vacuum tube।
            """,
        ))
        self.card_group = self.open_chapter(
            1, 1925, 1925, "The switch nobody could build",
            tr("An idea twenty years too early", "সময়ের বিশ বছর আগে আসা একটা idea"),
        )

    # --- the vacuum tube ---------------------------------------------------------------------
    def tube(self):
        self.slide(tr(
            """
            Here's how a tube switches. A filament heats the cathode until electrons boil off it.
            That's thermionic emission, and look at its law: an exponential of a barrier, the
            work function W, divided by k-T. Remember that shape; it's going to haunt this whole
            lecture. The grid in the middle is the gate of this switch. Make it negative, and it
            pushes the electrons back. The current stops.
            """,
            """
            Tube কীভাবে switch করে দেখেন। একটা filament cathode-টাকে এত গরম করে যে electron ফুটে
            বের হয়ে আসে। এইটাকে বলে thermionic emission, আর এর law-টা খেয়াল করেন: একটা barrier, মানে
            work function W, সেটাকে k-T দিয়ে ভাগ করে তার exponential। এই shape-টা মনে রাখেন, পুরা
            lecture জুড়ে এইটা বারবার ফিরে আসবে। মাঝখানের grid-টাই এই switch-এর gate। ওইটাকে negative
            করলে electron-গুলারে পিছনে ঠেলে দেয়, current বন্ধ হয়ে যায়।
            """,
        ))
        self.play(FadeOut(self.card_group))
        title = heading(tr("Before the transistor: the vacuum tube", "Transistor-এর আগের switch: vacuum tube"))
        cx = -3.4
        glass = RoundedRectangle(width=3.0, height=4.6, corner_radius=1.1, stroke_color=MUTED, stroke_width=3)
        glass.move_to([cx, -0.4, 0])
        cathode = Rectangle(width=2.0, height=0.16, fill_color=THERMAL, fill_opacity=1, stroke_width=0).move_to([cx, -2.1, 0])
        glow = Rectangle(width=2.4, height=0.5, fill_color=THERMAL, fill_opacity=0.18, stroke_width=0).move_to(cathode)
        grid = DashedLine([cx - 1.15, -0.5, 0], [cx + 1.15, -0.5, 0], dash_length=0.14, stroke_color=GATE, stroke_width=6)
        plate = Rectangle(width=2.0, height=0.22, fill_color=METAL, fill_opacity=1, stroke_width=0).move_to([cx, 1.2, 0])
        pins = VGroup(*[Line([cx + dx, -2.7, 0], [cx + dx, -3.2, 0], stroke_color=MUTED, stroke_width=3) for dx in (-0.6, 0, 0.6)])
        lbl = VGroup(
            text(tr("plate", "plate"), size=22, color=METAL).next_to(plate, RIGHT, buff=0.5),
            text(tr("grid (the gate)", "grid (এইটাই gate)"), size=22, color=GATE).next_to(grid, RIGHT, buff=0.4),
            text(tr("hot cathode", "গরম cathode"), size=22, color=THERMAL).next_to(cathode, RIGHT, buff=0.5),
        )
        tube = VGroup(glass, glow, cathode, grid, plate, pins)

        rng = np.random.default_rng(3)
        xs = rng.uniform(cx - 0.85, cx + 0.85, 26)
        ph = rng.uniform(0, 3.1, 26)
        clock = ValueTracker(0.0)
        open_ = ValueTracker(1.0)
        flow = VGroup(*[Dot(radius=0.05, color=ELECTRON) for _ in xs])

        def place(m):
            t = clock.get_value()
            for i, d in enumerate(m):
                if open_.get_value() > 0.5:
                    y = -1.95 + ((ph[i] + 1.4 * t) % 3.05)
                else:
                    y = -1.95 + 0.6 * abs(np.sin(ph[i] + 2.2 * t))
                d.move_to([xs[i], y, 0])

        flow.add_updater(place)
        tick = lambda m, dt: clock.increment_value(dt)  # noqa: E731
        state = text("ON", size=34, color=GOOD, weight="BOLD").move_to([cx, 2.55, 0])
        grid_v = text(tr("grid 0 V", "grid 0 V"), size=22, color=GATE).next_to(grid, LEFT, buff=0.3)

        law = eq(r"J", r"=", r"A_G\,", r"T^2", r"\,e^{-", r"W", r"/", r"k_BT", r"}", size=54)
        law[3].set_color(THERMAL)
        law[5].set_color(GATE)
        law[7].set_color(THERMAL)
        law.move_to([3.2, 0.9, 0])
        law_lbl = text(tr("thermionic emission (Richardson)", "thermionic emission (Richardson)"), size=22, color=MUTED).next_to(law, UP, buff=0.3)
        w_lbl = text(tr("W: the barrier\n(the cathode's work function)", "W: barrier, মানে\ncathode-এর work function"), size=22, color=GATE)
        kt_lbl = text(tr("k_BT: the thermal energy", "k_BT: thermal energy"), size=22, color=THERMAL)
        keys = VGroup(w_lbl, kt_lbl).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(law, DOWN, buff=0.4).align_to(law, LEFT)
        remember = text(tr("Remember this shape.", "এই shape-টা মনে রাখেন।"), size=30, color=GATE, weight="SEMIBOLD").next_to(keys, DOWN, buff=0.55)

        self.play(FadeIn(title))
        self.play(Create(glass), FadeIn(pins), run_time=1)
        self.play(FadeIn(cathode), FadeIn(glow), FadeIn(grid), FadeIn(plate), FadeIn(lbl))
        self.add(flow)
        flow.add_updater(tick)
        self.play(FadeIn(flow), FadeIn(state), FadeIn(grid_v))
        self.wait(1.5)
        self.play(Write(law), FadeIn(law_lbl))
        self.play(FadeIn(keys))
        self.wait(0.5)
        off = text("OFF", size=34, color=DRAIN, weight="BOLD").move_to(state)
        grid_neg = text(tr("grid −5 V", "grid −5 V"), size=22, color=GATE).move_to(grid_v)
        self.play(open_.animate.set_value(0), Transform(state, off), Transform(grid_v, grid_neg), run_time=0.6)
        self.wait(1.5)
        self.play(FadeIn(remember, shift=UP * 0.2))
        self.wait(0.5)
        flow.clear_updaters()
        self.tube_parts = VGroup(title, tube, lbl, flow, state, grid_v, law, law_lbl, keys, remember)

    # --- ENIAC -------------------------------------------------------------------------------
    def eniac(self):
        self.slide(tr(
            """
            Now build a computer out of them. ENIAC, unveiled in 1946: 17,468 tubes, every one of
            them a little heater, drawing 150 kilowatts. Tubes burned out, and finding the dead
            one among eighteen thousand took time. Everyone knew what they wanted instead: a switch
            made from a cold, solid piece of material, with no vacuum and no filament.
            """,
            """
            এখন এই tube দিয়ে একটা computer বানান। ENIAC, 1946-এ সবার সামনে আসে: 17,468টা tube, প্রত্যেকটা
            একটা ছোট heater, সব মিলায়ে 150 kilowatt টানে। Tube পুড়ে যাইত, আর আঠারো হাজারের মধ্যে নষ্টটা
            খুঁজে বের করতে সময় লাগত। সবাই জানত তারা আসলে কী চায়: ঠান্ডা, solid কোনো material-এর একটা
            switch, যেটায় vacuum নাই, filament নাই।
            """,
        ))
        self.play(FadeOut(self.tube_parts))
        title = heading(tr("ENIAC, 1946: 17,468 tubes, all glowing", "ENIAC, 1946: 17,468টা tube, সবগুলা জ্বলতেছে"))
        cols, rows, s = 50, 35, 0.15
        rng = np.random.default_rng(5)
        dots = VGroup(*[
            Square(0.1, stroke_width=0, fill_color=THERMAL, fill_opacity=rng.uniform(0.45, 0.95)).move_to(
                [(c - cols / 2) * s - 2.0, (rows / 2 - r) * s - 0.3, 0])
            for r in range(rows) for c in range(cols)
        ])
        key = text(tr("each square: 10 tubes", "প্রতি square = 10টা tube"), size=20, color=MUTED).next_to(dots, DOWN, buff=0.2)
        stats = VGroup(
            display("17,468", size=64, color=THERMAL),
            text(tr("vacuum tubes", "vacuum tube"), size=26, color=MUTED),
            display("150 kW", size=64, color=THERMAL),
            text(tr("of heat, all the time", "শুধু heat, সারাক্ষণ"), size=26, color=MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.4, 0.7, 0])
        stats[2].shift(DOWN * 0.3)
        stats[3].shift(DOWN * 0.3)
        src = source(tr("ENIAC figures: University of Pennsylvania / U.S. Army, 1946", "ENIAC-এর সংখ্যা: University of Pennsylvania / U.S. Army, 1946"))
        self.play(FadeIn(title), FadeIn(src))
        self.play(FadeIn(dots, lag_ratio=0.0006), run_time=2.5)
        self.play(FadeIn(key), FadeIn(stats[:2], shift=LEFT * 0.2))
        self.play(FadeIn(stats[2:], shift=LEFT * 0.2))
        dead = [dots[i] for i in rng.choice(len(dots), 9, replace=False)]
        self.play(*[d.animate.set_fill(FAINT, opacity=1) for d in dead], run_time=1.2)
        want = text(tr("Wanted:\na cold, solid switch", "দরকার:\nঠান্ডা, solid\nএকটা switch"), size=28, color=INK, weight="SEMIBOLD")
        want.next_to(stats, DOWN, buff=0.5).align_to(stats, LEFT)
        self.play(FadeIn(want, shift=UP * 0.2))
        self.eniac_parts = VGroup(title, dots, key, stats, src, want)

    # --- Lilienfeld --------------------------------------------------------------------------
    def lilienfeld(self):
        self.slide(tr(
            """
            In 1925 a physicist named Julius Edgar Lilienfeld filed a patent for exactly that. Look
            at the drawing: a thin film of semiconductor, two contacts, and a metal plate on top,
            separated by an insulator. Put a voltage on the plate and it pulls charge into the film,
            the way one plate of a capacitor pulls charge onto the other. Source, drain, and a gate
            on an insulator. That is the transistor you lay out every day, thirty-five years early.
            """,
            """
            1925-এ Julius Edgar Lilienfeld নামে একজন physicist ঠিক এই জিনিসের patent file করেন। Drawing-টা
            দেখেন: semiconductor-এর একটা পাতলা film, দুই পাশে দুইটা contact, আর উপরে insulator দিয়ে আলাদা
            করা একটা metal plate। Plate-এ voltage দিলে ওইটা film-এর ভিতরে charge টেনে আনে, ঠিক যেভাবে
            capacitor-এর এক plate আরেক plate-এ charge জমায়। Source, drain, আর insulator-এর উপর একটা gate।
            আপনারা প্রতিদিন যে transistor-এর layout করেন, এইটা সেটাই, পঁয়ত্রিশ বছর আগে।
            """,
        ))
        self.play(FadeOut(self.eniac_parts))
        title = heading(tr("1925: Lilienfeld's idea", "1925: Lilienfeld-এর idea"))
        y0 = 0.6
        glass = Rectangle(width=7.4, height=0.5, fill_color="#26323F", fill_opacity=1, stroke_width=0).move_to([0, y0 - 0.55, 0])
        film = Rectangle(width=6.4, height=0.22, fill_color=SILICON, fill_opacity=0.8, stroke_width=0).move_to([0, y0 - 0.19, 0])
        c_l = Rectangle(width=1.1, height=0.5, fill_color=METAL, fill_opacity=1, stroke_width=0).move_to([-2.9, y0 + 0.17, 0])
        c_r = c_l.copy().move_to([2.9, y0 + 0.17, 0])
        ins = Rectangle(width=2.8, height=0.3, fill_color=OXIDE_TEXT, fill_opacity=0.9, stroke_width=0).move_to([0, y0 + 0.07, 0])
        plate = Rectangle(width=2.8, height=0.3, fill_color=GATE, fill_opacity=1, stroke_width=0).move_to([0, y0 + 0.37, 0])
        names = VGroup(
            text("source", size=22, color=MUTED).next_to(c_l, UP, buff=0.15),
            text("drain", size=22, color=MUTED).next_to(c_r, UP, buff=0.15),
            text(tr("gate (metal plate)", "gate (metal plate)"), size=22, color=GATE).next_to(plate, UP, buff=0.15),
            text(tr("insulator", "insulator"), size=16, color=BG, weight="SEMIBOLD").move_to(ins),
        )
        device = VGroup(glass, film, c_l, c_r, ins, plate)
        src = source(tr("Lilienfeld: Canadian application 1925; US 1,745,175, filed 1926, granted 1930",
                        "Lilienfeld: Canadian application 1925; US 1,745,175, filed 1926, granted 1930"))
        self.play(FadeIn(title), FadeIn(src))
        self.play(LaggedStart(*[FadeIn(m, shift=DOWN * 0.15) for m in device], lag_ratio=0.2), FadeIn(names), run_time=2)

        plus = VGroup(*[MathTex("+", font_size=30, color=BG).move_to([x, y0 + 0.37, 0]) for x in np.linspace(-1.1, 1.1, 6)])
        induced = VGroup(*[Dot([x, y0 - 0.19, 0], radius=0.05, color=ELECTRON) for x in np.linspace(-1.25, 1.25, 12)])
        vg = text(tr("+ V on the gate", "gate-এ + V"), size=24, color=GATE).move_to([0, y0 + 1.25, 0])
        arrow = Arrow([-2.3, y0 - 0.19, 0], [2.3, y0 - 0.19, 0], buff=0, stroke_color=ELECTRON, stroke_width=5)
        cur = text(tr("current flows in the film", "film-এর ভিতর দিয়া current চলে"), size=20, color=ELECTRON).next_to(glass, DOWN, buff=0.12)
        self.play(FadeIn(vg), FadeIn(plus, lag_ratio=0.1), FadeIn(induced, lag_ratio=0.05), run_time=1.5)
        self.play(GrowArrow(arrow), FadeIn(cur))
        tie = layout_note(tr("Source, drain, a gate on an insulator: the MOSFET you draw, 35 years early.",
                             "Source, drain, insulator-এর উপর gate: আপনারা যে MOSFET আঁকেন, 35 বছর আগে।"), size=22)
        tie.to_edge(DOWN, buff=0.9)
        self.play(FadeIn(tie, shift=UP * 0.2))

        self.slide(tr(
            """
            And the numbers say it should have worked. The plate and the film are a capacitor: the
            charge is C times V. With an insulator a tenth of a micron thick and ten volts on the
            gate, that's about two times ten to the twelve electrons per square centimetre, plenty
            to carry a current. It should have worked. It didn't.
            """,
            """
            আর হিসাবও বলে এইটা কাজ করার কথা। Plate আর film মিলে একটা capacitor: charge হলো C গুণ V।
            Insulator যদি এক micron-এর দশ ভাগের এক ভাগ পুরু হয়, আর gate-এ দেন দশ volt, তাহলে প্রতি square
            centimetre-এ প্রায় দুই গুণ দশের বারো ঘাত electron, current চালানোর জন্য যথেষ্ট। কাজ করার কথা ছিল।
            করে নাই।
            """,
        ))
        n_s = phys.induced_sheet_density_cm2(10, 100)
        e1 = eq(r"Q", r"=", r"C_{ox}", r"V_G", size=48)
        e1[2].set_color(OXIDE_TEXT)
        e1[3].set_color(GATE)
        e2 = eq(r"n_s", r"=", r"\frac{\varepsilon_{ox}\,V_G}{q\,t_{ox}}", size=48)
        e2[0].set_color(ELECTRON)
        e3 = eq(r"=", rf"{n_s / 1e12:.1f}\times10^{{12}}\ \text{{cm}}^{{-2}}", size=44)
        e3[1].set_color(ELECTRON)
        cond = text(tr("t_ox = 100 nm, V_G = 10 V", "t_ox = 100 nm, V_G = 10 V"), size=20, color=MUTED)
        VGroup(e1, e2, e3, cond).arrange(DOWN, buff=0.3).move_to([4.4, -1.55, 0])
        self.play(FadeOut(tie), VGroup(device, names, plus, induced, vg, arrow, cur).animate.shift(LEFT * 2.2 + UP * 0.2))
        self.play(Write(e1))
        self.play(Write(e2))
        self.play(Write(e3), FadeIn(cond))
        verdict = VGroup(
            text(tr("It should have worked.", "কাজ করার কথা ছিল।"), size=34, weight="SEMIBOLD"),
            text(tr("It didn't.", "করে নাই।"), size=34, weight="SEMIBOLD", color=DRAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([-3.2, -2.3, 0])
        self.play(FadeIn(verdict[0]))
        self.wait(0.6)
        self.play(FadeIn(verdict[1]))
        self.lil_parts = VGroup(title, device, names, plus, induced, vg, arrow, cur, src, e1, e2, e3, cond, verdict)

    # --- surface states ----------------------------------------------------------------------
    def surface_states(self):
        self.slide(tr(
            """
            At Bell Labs in 1945, William Shockley built devices like Lilienfeld's and worked out how
            big the effect should be. He measured almost nothing. The explanation came from John
            Bardeen in 1947. The surface of a semiconductor is a broken crystal: bonds that end in
            nothing. They trap electrons. So when the gate pulls charge in, almost all of it gets
            stuck in these surface states and never reaches the channel. With a typical density of
            surface states, only about two percent of the charge is free to carry current. Press
            down for where the two percent comes from.
            """,
            """
            1945-এ Bell Labs-এ William Shockley Lilienfeld-এর মতো device বানায়ে হিসাব করলেন effect কতটা
            বড় হওয়ার কথা। মাপতে গিয়ে প্রায় কিছুই পাইলেন না। Explanation দিলেন John Bardeen, 1947-এ।
            Semiconductor-এর surface হইলো একটা ভাঙা crystal: এমন bond যেগুলা কোথাও গিয়া শেষ হয় না। এগুলা
            electron আটকায়ে ফেলে। তাই gate যখন charge টানে, তার প্রায় পুরাটাই এই surface states-এ আটকায়ে
            যায়, channel পর্যন্ত আর পৌঁছায় না। Surface states-এর typical density-তে, যত charge আনলেন তার
            মাত্র দুই percent-এর মতো current carry করতে পারে। দুই percent কোথা থেকে আসলো, দেখতে চাইলে
            নিচে (↓) যান।
            """,
        ))
        self.play(FadeOut(self.lil_parts))
        title = heading(tr("Why it failed: the surface eats the field", "কেন fail করল: surface-টাই field খেয়ে ফেলে"))
        x0 = -3.2
        gate = Rectangle(width=5.2, height=0.45, fill_color=GATE, fill_opacity=1, stroke_width=0).move_to([x0, 2.35, 0])
        ins = Rectangle(width=5.2, height=1.1, fill_color=OXIDE_TEXT, fill_opacity=0.25, stroke_width=0).move_to([x0, 1.57, 0])
        semi = Rectangle(width=5.2, height=2.7, fill_color=SILICON, fill_opacity=0.14, stroke_width=0).move_to([x0, -0.33, 0])
        surface_y = 1.0
        xs = np.linspace(x0 - 2.3, x0 + 2.3, 16)
        traps = VGroup(*[Circle(radius=0.09, stroke_color=MUTED, stroke_width=2).move_to([x, surface_y - 0.12, 0]) for x in xs])
        labels = VGroup(
            text("gate", size=22, color=BG, weight="SEMIBOLD").move_to(gate),
            text(tr("insulator", "insulator"), size=20, color=OXIDE_TEXT).move_to(ins).add_background_rectangle(color=BG, opacity=0.85, buff=0.08),
            text(tr("surface states\n(broken bonds)", "surface states\n(ভাঙা bond)"), size=20, color=MUTED).next_to(traps, DOWN, buff=0.12).align_to(semi, LEFT).shift(RIGHT * 0.15),
            text(tr("channel", "channel"), size=20, color=ELECTRON).move_to([x0, -1.25, 0]),
        )
        self.play(FadeIn(title))
        self.play(FadeIn(gate), FadeIn(ins), FadeIn(semi), FadeIn(labels[0]), FadeIn(labels[1]))
        self.play(LaggedStart(*[Create(c) for c in traps], lag_ratio=0.05), FadeIn(labels[2]))
        # Field lines from the gate: almost all end on a surface state.
        lines = VGroup()
        for i, x in enumerate(xs):
            end = [x, -1.0, 0] if i == 8 else [x, surface_y - 0.03, 0]
            lines.add(Arrow([x, 2.1, 0], end, buff=0, stroke_color=GATE, stroke_width=3, max_tip_length_to_length_ratio=0.08))
        fills = VGroup(*[Dot(c.get_center(), radius=0.075, color=ELECTRON) for i, c in enumerate(traps) if i != 8])
        free = Dot([xs[8], -1.0, 0], radius=0.075, color=ELECTRON)
        self.play(LaggedStart(*[GrowArrow(a) for a in lines], lag_ratio=0.06), run_time=2)
        self.play(FadeIn(fills, lag_ratio=0.05), FadeIn(free), FadeIn(labels[3]))
        self.play(Indicate(free, color=ELECTRON, scale_factor=2))

        share = phys.share_reaching_channel(1e13)
        e1 = eq(r"\frac{\Delta Q_{ch}}{\Delta Q_G}", r"\approx", r"\frac{C_{dep}}{C_{dep}+C_{it}}", size=46)
        e2 = eq(r"C_{it}", r"=", r"q\,D_{it}", size=42)
        e2[0].set_color(MUTED)
        dit = text(tr("D_it ≈ 10¹³ states per cm² per eV", "D_it ≈ 10¹³ state / cm² / eV"), size=22, color=MUTED)
        big = VGroup(
            display(f"≈ {share * 100:.0f}%", size=72, color=ELECTRON),
            text(tr("of the gate's charge\nreaches the channel", "gate-এর charge-এর এতটুকুই\nchannel-এ পৌঁছায়"), size=24, color=INK),
        ).arrange(DOWN, buff=0.12)
        col = VGroup(e1, e2, dit, big, model_tag()).arrange(DOWN, buff=0.32).move_to([3.6, -0.1, 0])
        src = source(tr("J. Bardeen, Phys. Rev. 71, 717 (1947)", "J. Bardeen, Phys. Rev. 71, 717 (1947)"))
        self.play(Write(e1), FadeIn(src))
        self.play(Write(e2), FadeIn(dit))
        self.play(FadeIn(big, shift=UP * 0.2), FadeIn(col[4]))
        self.screen = VGroup(title, gate, ins, semi, traps, labels, lines, fills, free, col, src)

        # ↓ where the 2% comes from
        self.slide(tr(
            """
            Here's the charge balance. Whatever charge the gate adds has to be matched underneath,
            either by charge stuck in surface states or by charge in the semiconductor. Both respond
            to the same change in surface potential, so the charge splits in proportion to two
            capacitances.
            """,
            """
            এইটা charge-এর হিসাব। Gate যত charge যোগ করে, নিচে ঠিক ততটুকু charge লাগে, হয় surface
            states-এ আটকানো, নয়তো semiconductor-এর ভিতরে। দুইটাই একই surface potential-এর পরিবর্তনে
            সাড়া দেয়, তাই charge দুই ভাগ হয় দুইটা capacitance-এর অনুপাতে।
            """,
        ), direction="vertical")
        self.detour_in(self.screen)
        rows = [
            (eq(r"\Delta Q_G", r"=", r"-(\Delta Q_{it} + \Delta Q_{s})"),
             tr("Charge balance: the gate's charge is matched underneath.", "Charge balance: gate-এর charge নিচে match হয়।")),
            (eq(r"\Delta Q_{it} = -C_{it}\,\Delta\psi_s", r"\qquad", r"\Delta Q_{s} = -C_{dep}\,\Delta\psi_s"),
             tr("Both follow the same surface potential ψ_s.", "দুইটাই একই surface potential ψ_s মেনে চলে।")),
            (eq(r"\frac{\Delta Q_{s}}{\Delta Q_G}", r"=", r"-\frac{C_{dep}}{C_{dep}+C_{it}}"),
             tr("So the semiconductor gets only its share.", "তাই semiconductor পায় শুধু নিজের ভাগটুকু।")),
        ]
        shown = VGroup()
        y = 2.4
        for m, why in rows:
            w = text(why, size=22, color=MUTED)
            VGroup(m, w).arrange(DOWN, buff=0.12).move_to([0, y, 0])
            y -= 1.55
            self.play(Write(m), FadeIn(w))
            shown.add(m, w)

        self.slide(tr(
            """
            Now the numbers. A lightly doped substrate gives a depletion capacitance of about 34
            nanofarads per square centimetre. Ten to the thirteen surface states per square
            centimetre per electron-volt give a surface-state capacitance of 1.6 microfarads, about
            fifty times bigger. So about two percent goes to the channel.
            """,
            """
            এবার সংখ্যা। হালকা doping-এর substrate-এ depletion capacitance প্রতি square centimetre-এ প্রায় 34
            nanofarad। আর প্রতি square centimetre প্রতি eV-তে দশের তেরো ঘাত surface state মানে
            surface-state capacitance 1.6 microfarad, প্রায় পঞ্চাশ গুণ বড়। তাই channel-এ যায় মাত্র দুই
            percent-এর মতো।
            """,
        ), direction="vertical")
        c_dep = phys.depletion_capacitance_cm2(1e16, 2 * phys.fermi_potential(1e16))
        c_it = phys.surface_state_capacitance_cm2(1e13)
        nums = VGroup(
            eq(rf"C_{{dep}} \approx {c_dep * 1e9:.0f}\ \text{{nF/cm}}^2", r"\quad(N_A = 10^{16}\ \text{cm}^{-3})", size=38),
            eq(rf"C_{{it}} \approx {c_it * 1e6:.1f}\ \mu\text{{F/cm}}^2", r"\quad(D_{it} = 10^{13}\ \text{cm}^{-2}\text{eV}^{-1})", size=38),
            eq(r"\frac{C_{dep}}{C_{dep}+C_{it}}", rf"\approx {share * 100:.1f}\%", size=44),
        ).arrange(DOWN, buff=0.35).move_to([0, -2.1, 0])
        nums[2][1].set_color(ELECTRON)
        self.play(FadeOut(shown[:4]), shown[4:].animate.shift(UP * 3.1))
        self.play(Write(nums[0]))
        self.play(Write(nums[1]))
        self.play(Write(nums[2]))

        self.slide(tr("Back to the story.", "আবার গল্পে ফিরি।"), direction="vertical")
        self.detour_out(self.screen, shown[4:], nums)

    # --- cliffhanger -------------------------------------------------------------------------
    def cliffhanger(self):
        self.slide(tr(
            """
            That was the dead end of the 1940s: a perfect idea, defeated by a few atoms' worth of
            broken bonds. So Bardeen and his colleague Walter Brattain stopped trying to beat the
            surface. Instead they started poking it with fine metal points, to study it. And in
            December 1947, one of those experiments did something nobody expected.
            """,
            """
            1940-এর দশকে এইটাই ছিল dead end: একটা perfect idea, হেরে গেল কয়েকটা atom-এর সমান ভাঙা
            bond-এর কাছে। তাই Bardeen আর তাঁর colleague Walter Brattain surface-রে হারানোর চেষ্টা বাদ
            দিলেন। বরং ওইটাকে বোঝার জন্য সরু metal point দিয়ে খোঁচানো শুরু করলেন। আর 1947-এর ডিসেম্বরে,
            এমনই এক experiment এমন একটা কাজ করল যেটা কেউ আশা করে নাই।
            """,
        ))
        self.play(FadeOut(self.screen))
        crystal = Rectangle(width=4.0, height=1.4, fill_color=METAL, fill_opacity=0.35, stroke_color=METAL, stroke_width=2)
        crystal.move_to([3.2, -1.4, 0])
        needle = Polygon([3.15, 2.6, 0], [3.25, 2.6, 0], [3.2, -0.68, 0], fill_color=GATE, fill_opacity=1, stroke_width=0)
        needle.shift(UP * 1.6)
        lbl = text("germanium", size=24, color=MUTED).next_to(crystal, DOWN, buff=0.2)
        a = text(tr("They stopped fighting\nthe surface.", "তাঁরা surface-এর সাথে\nযুদ্ধ বাদ দিলেন।"), size=40, weight="SEMIBOLD")
        b = text(tr("They started poking it.", "খোঁচানো শুরু করলেন।"), size=40, weight="SEMIBOLD", color=GATE)
        VGroup(a, b).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-2.8, 0.6, 0])
        self.play(FadeIn(a))
        self.play(FadeIn(crystal), FadeIn(lbl))
        self.play(needle.animate.shift(DOWN * 1.6), FadeIn(b), run_time=1.5)
        spark = Circle(radius=0.12, stroke_color=ELECTRON, stroke_width=4).move_to([3.2, -0.7, 0])
        self.play(GrowFromCenter(spark), run_time=0.3)
        self.play(spark.animate.scale(4).set_stroke(opacity=0), run_time=0.9)


class Ch01BeforeTheSwitchBN(Ch01BeforeTheSwitch):
    LANG = "bn"

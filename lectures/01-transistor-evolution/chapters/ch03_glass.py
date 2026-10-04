"""Chapter 3 · The glass that saved electronics (1955–1963).

Oxide masking, Atalla's passivation (chapter 1's surface-state model, with good oxide), the MOSFET,
how a gate makes a channel (band bending to 2 phi_F), the threshold voltage, the square law
with its drawn W/L (and the gradual-channel derivation one level down), CMOS, and its price in
layout: latch-up.
"""

import sys
from pathlib import Path

LECTURE = Path(__file__).resolve().parents[1]
IMAGES = LECTURE / "images"
sys.path[:0] = [str(LECTURE.parents[1]), str(LECTURE)]

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403
from manim_slides import Slide  # noqa: E402

import physics as phys  # noqa: E402
from kit.style import *  # noqa: E402,F403

N_A = 1e17
T_OX = 10
V_FB = -0.98


def box(w, h, x, y, color, opacity=1.0):
    return Rectangle(width=w, height=h, fill_color=color, fill_opacity=opacity, stroke_width=0).move_to([x, y, 0])


class Ch03Glass(Chapter, Slide):
    def construct(self):
        self.card()
        self.oxide_mask()
        self.passivation()
        self.mosfet()
        self.kahng_patent()
        self.band_bending()
        self.threshold()
        self.layout_view()
        self.pinch_off()
        self.cmos()
        self.latchup()
        self.cliffhanger()

    # --- card --------------------------------------------------------------------------------
    def card(self):
        self.slide(say(
            """
            So the field effect was stuck behind the surface, and bipolar transistors burned power.
            The way out started as an accident in a furnace.
            """,
            """
            তো field effect আটকা পড়ে আছে surface-এর পিছনে, আর bipolar transistor power খায়। বের হওয়ার রাস্তা
            শুরু হইলো একটা furnace-এর ভিতরে, একটা accident থেকে।
            """,
        ))
        self.card_group = self.open_chapter(
            3, 1959, 1947, "The glass that saved electronics",
            "A furnace accident, and a switch Bell Labs set aside",
        )

    # --- oxide masking -----------------------------------------------------------------------
    def oxide_mask(self):
        self.slide(say(
            """
            In the mid-1950s at Bell Labs, Carl Frosch and Lincoln Derick were diffusing dopants into
            silicon in a hot furnace when steam got in by accident. The wafers came out coated in a
            thin layer of glass: silicon dioxide, grown from the silicon itself. And that glass
            blocks dopants. Open a window in it and the dopants go in only there. Every layer you
            draw in a layout becomes a mask like this one; this is where that idea starts.
            """,
            """
            1950-এর দশকের মাঝামাঝি, Bell Labs-এ Carl Frosch আর Lincoln Derick একটা গরম furnace-এ silicon-এ
            dopant ঢুকাইতেছিলেন, এমন সময় accident-এ ভিতরে steam ঢুকে গেল। Wafer বের হইলো পাতলা একটা কাচের
            আস্তরণ নিয়া: silicon dioxide, silicon থেকেই জন্মানো। আর এই কাচ dopant আটকায়। এতে একটা window
            কাটলে dopant শুধু ওইখান দিয়াই ঢোকে। Layout-এ আপনারা যত layer আঁকেন, প্রত্যেকটা শেষে এরকম একটা
            mask হয়; idea-টার শুরু এইখান থেকে।
            """,
        ))
        self.play(FadeOut(self.card_group))
        title = heading("Mid-1950s: silicon grows its own glass")
        si = box(9.0, 2.2, 0, -1.6, SUBSTRATE)
        si_l = text("silicon", size=24, color=MUTED).move_to([3.6, -2.3, 0])
        ox_h = ValueTracker(0.02)
        left = always_redraw(lambda: box(3.7, ox_h.get_value(), -2.65, -0.5 + ox_h.get_value() / 2, OXIDE_TEXT, 0.9))
        right = always_redraw(lambda: box(3.7, ox_h.get_value(), 2.65, -0.5 + ox_h.get_value() / 2, OXIDE_TEXT, 0.9))
        ox_l = text("SiO₂, grown in steam", size=22, color=OXIDE_TEXT).move_to([-2.95, 0.25, 0])
        self.play(FadeIn(title), FadeIn(si), FadeIn(si_l))
        self.add(left, right)
        self.play(ox_h.animate.set_value(0.42), FadeIn(ox_l), run_time=2)
        win = text("a window", size=22, color=GATE).move_to([0, 0.25, 0])
        self.play(FadeIn(win))
        rng = np.random.default_rng(9)
        xs = rng.uniform(-4.2, 4.2, 30)
        drops = VGroup(*[Arrow([x, 2.6, 0], [x, 1.9, 0], buff=0, stroke_color=ELECTRON, stroke_width=3, max_tip_length_to_length_ratio=0.3) for x in xs])
        dop = text("dopants", size=22, color=ELECTRON).move_to([-4.6, 2.6, 0])
        self.play(FadeIn(drops), FadeIn(dop))
        anims = []
        for a, x in zip(drops, xs):
            if abs(x) < 0.75:
                anims.append(a.animate.shift(DOWN * 2.6).set_opacity(0))
            else:
                anims.append(a.animate.shift(DOWN * 1.3).set_opacity(0.15))
        doped = box(1.7, 0.7, 0, -0.85, ELECTRON, 0.55)
        self.play(*anims, FadeIn(doped), run_time=1.6)
        dl = text("doped only under the window", size=22, color=ELECTRON).next_to(doped, DOWN, buff=0.15)
        self.play(FadeIn(dl))
        note = layout_note("Every layer you draw becomes a mask like this: open where you drew, blocked elsewhere.", size=22, width=90)
        note.to_edge(DOWN, buff=0.25)
        self.play(FadeOut(si_l), FadeIn(note, shift=UP * 0.2))
        self.parts = VGroup(title, si, left, right, ox_l, win, drops, dop, doped, dl, note)

    # --- passivation -------------------------------------------------------------------------
    def passivation(self):
        self.slide(say(
            """
            Then Mohamed Atalla at Bell Labs found something even more important. A carefully grown
            oxide doesn't just protect the silicon: it ties up most of those broken bonds at the
            surface. A good thermal oxide has orders of magnitude fewer surface states: typically
            around ten to the ten per square centimetre per electron-volt, against around ten to
            the thirteen for a bare surface. Put typical values like these into chapter one's
            simple model: the semiconductor's share of the induced charge goes from about two
            percent to about ninety-six. Now the gate can bend the bands far enough to make a
            channel. That's Atalla on the right, in 1963.
            """,
            """
            এরপর Bell Labs-এর Mohamed Atalla আরও important একটা জিনিস পাইলেন। যত্ন করে জন্মানো oxide শুধু
            silicon-রে protect করে না: surface-এর ভাঙা bond-গুলার বেশিরভাগই বাঁধে ফেলে। ভালো একটা thermal oxide-এ
            surface state কয়েক order কম: সাধারণত প্রতি square centimetre প্রতি electron-volt-এ দশের দশ ঘাতের আশেপাশে,
            খালি surface-এর দশের তেরো ঘাতের বিপরীতে। এই রকম typical মান chapter one-এর সহজ model-এ বসান:
            induce করা charge-এ semiconductor-এর ভাগ প্রায় দুই percent থেকে প্রায় ছিয়ানব্বই percent হয়। এখন gate band
            যথেষ্ট বাঁকায়ে একটা channel বানাইতে পারে। ডানের ছবিতে Atalla, 1963-এ।
            """,
        ))
        self.play(FadeOut(self.parts))
        title = heading("Atalla: the glass also heals the surface")
        x0 = -3.2
        gate = box(5.2, 0.45, x0, 2.35, GATE)
        ox = box(5.2, 1.1, x0, 1.57, OXIDE_TEXT, 0.3)
        semi = box(5.2, 2.7, x0, -0.33, SILICON, 0.14)
        xs = np.linspace(x0 - 2.3, x0 + 2.3, 16)
        traps = VGroup(*[Circle(radius=0.09, stroke_color=MUTED, stroke_width=2).move_to([x, 0.88, 0]) for x in xs])
        lines = VGroup(*[Arrow([x, 2.1, 0], [x, 0.97 if i != 8 else -1.0, 0], buff=0, stroke_color=GATE, stroke_width=3,
                               max_tip_length_to_length_ratio=0.08) for i, x in enumerate(xs)])
        self.play(FadeIn(title), FadeIn(gate), FadeIn(ox), FadeIn(semi), FadeIn(traps), FadeIn(lines))
        before = phys.share_in_semiconductor(1e13)
        after = phys.share_in_semiconductor(1e10)
        e1 = eq(r"\frac{C_{dep}}{C_{dep}+C_{it}}", r"\approx", rf"{before * 100:.0f}\%", size=50)
        e1[2].set_color(DRAIN)
        d1 = text("D_it ≈ 10¹³ (bare surface, typical)", size=24, color=MUTED)
        col = VGroup(e1, d1).arrange(DOWN, buff=0.3).move_to([3.4, 0.6, 0])
        self.play(Write(e1), FadeIn(d1))
        heal = text("thermal oxide: D_it ≈ 10¹⁰ (typical)", size=24, color=GOOD).move_to(d1)
        e2 = eq(r"\frac{C_{dep}}{C_{dep}+C_{it}}", r"\approx", rf"{after * 100:.0f}\%", size=50).move_to(e1)
        e2[2].set_color(GOOD)
        deep = VGroup(*[Arrow([x, 2.1, 0], [x, -1.0, 0], buff=0, stroke_color=GATE, stroke_width=3, max_tip_length_to_length_ratio=0.03) for x in xs])
        chan = box(5.0, 0.12, x0, -1.05, ELECTRON)
        chan_l = text("a channel, at last", size=22, color=ELECTRON).next_to(chan, DOWN, buff=0.15)
        self.play(FadeOut(traps, lag_ratio=0.05), Transform(lines, deep), Transform(d1, heal), Transform(e1, e2), run_time=2)
        self.play(FadeIn(chan), FadeIn(chan_l))
        src = source("M. M. Atalla, E. Tannenbaum & E. J. Scheibner, Bell Syst. Tech. J. 38, 749 (1959)")
        portrait = figure(IMAGES / "atalla_1963.jpg", 2.3, "M. M. Atalla, 1963 (public domain)").move_to([5.4, -1.95, 0])
        self.play(FadeIn(src), FadeIn(portrait, shift=UP * 0.15))
        self.parts = Group(title, gate, ox, semi, lines, col, chan, chan_l, src, portrait)

    # --- the MOSFET and the planar process ---------------------------------------------------
    def mosfet(self):
        self.slide(say(
            """
            With the surface tamed, everything arrives at once. Jack Kilby builds the first
            integrated circuit at Texas Instruments in 1958. In 1959 Jean Hoerni at Fairchild
            invents the planar process, everything flat and protected under oxide, and Robert Noyce
            uses it for the planar IC. And at Bell Labs, Atalla and Dawon Kahng make the first
            working MOSFET: metal, oxide, semiconductor. Bell Labs didn't push it; early MOSFETs were
            slower than bipolar transistors, and they drifted. Others saw the future in it.
            """,
            """
            Surface বশে আসার পর সব একসাথে আসা শুরু করল। 1958-এ Texas Instruments-এ Jack Kilby প্রথম
            integrated circuit বানান। 1959-এ Fairchild-এ Jean Hoerni planar process বের করেন, সবকিছু flat,
            oxide-এর নিচে protected, আর Robert Noyce সেটা দিয়া planar IC বানান। আর Bell Labs-এ Atalla আর
            Dawon Kahng বানান প্রথম কাজ করা MOSFET: metal, oxide, semiconductor। Bell Labs এইটা নিয়া বেশি আগায়
            নাই; প্রথম দিকের MOSFET bipolar-এর চেয়ে slow ছিল, আর drift করত। অন্যরা এর মধ্যে future দেখল।
            """,
        ))
        self.play(FadeOut(self.parts))
        title = heading("1959: the MOSFET, at last")
        sub = box(8.0, 2.0, 0, -1.2, PSUB)
        s = box(1.6, 0.6, -2.3, -0.5, ELECTRON, 0.6)
        d = box(1.6, 0.6, 2.3, -0.5, ELECTRON, 0.6)
        ox = box(3.4, 0.14, 0, -0.13, OXIDE_TEXT)
        g = box(3.4, 0.55, 0, 0.215, METAL)
        cs = box(0.9, 0.7, -2.3, 0.15, METAL)
        cd = box(0.9, 0.7, 2.3, 0.15, METAL)
        lbl = VGroup(
            text("metal (Al) gate", size=22, color=METAL).next_to(g, UP, buff=0.2),
            text("↑ thin oxide", size=18, color=OXIDE_TEXT).move_to([0, -0.48, 0]),
            text("n⁺ source", size=22).next_to(s, DOWN, buff=0.15),
            text("n⁺ drain", size=22).next_to(d, DOWN, buff=0.15),
            text("p-type silicon", size=22, color=MUTED).move_to([0, -1.8, 0]),
        )
        dev = VGroup(sub, s, d, ox, g, cs, cd, lbl).shift(UP * 0.7)
        self.play(FadeIn(title))
        self.play(LaggedStart(*[FadeIn(m, shift=DOWN * 0.1) for m in (sub, s, d, ox, g, cs, cd)], lag_ratio=0.15), FadeIn(lbl), run_time=2)
        events = [
            ("1958", "Kilby: first IC (TI)"),
            ("1959", "Hoerni: planar process"),
            ("1959", "Noyce: planar IC"),
            ("1959–60", "Atalla & Kahng: MOSFET"),
        ]
        strip = VGroup()
        for i, (yr, what) in enumerate(events):
            item = VGroup(text(yr, size=24, color=GATE, weight="SEMIBOLD"), text(what, size=20)).arrange(DOWN, buff=0.08)
            strip.add(item)
        strip.arrange(RIGHT, buff=0.6).to_edge(DOWN, buff=0.45)
        self.play(LaggedStart(*[FadeIn(it, shift=UP * 0.15) for it in strip], lag_ratio=0.3), run_time=2)
        self.mos = dev
        self.parts = VGroup(title, strip)

    # --- how a gate makes a channel ----------------------------------------------------------
    def kahng_patent(self):
        title, pic = self.show_figure(say(
            """
            Here it is as Dawon Kahng drew it in his patent, filed in May 1960. A silicon wafer, a
            thermally grown oxide, a metal electrode on top, and two p-type regions diffused on
            either side: a p-channel transistor, on n-type silicon. The patent gives the oxide as
            about a thousand angstroms, a hundred nanometres: the same thickness we gave
            Lilienfeld's insulator in chapter one.
            """,
            """
            এই যে, Dawon Kahng-এর patent-এ যেভাবে আঁকা, file করা May 1960-এ। একটা silicon wafer, তার উপর
            thermally grown oxide, তার উপর metal electrode, আর দুই পাশে diffuse করা দুইটা p-type region: n-type
            silicon-এর উপর একটা p-channel transistor। Patent-এ oxide প্রায় এক হাজার angstrom, মানে একশ
            nanometre: chapter one-এ Lilienfeld-এর insulator-এর জন্য আমরা ঠিক এই thickness-ই ধরছিলাম।
            """,
        ), "The MOSFET, as Kahng drew it",
            figure(IMAGES / "kahng_US3102230_fig1a.png", 5.6,
                   "D. Kahng, US patent 3,102,230, filed 1960 (public domain)").move_to(DOWN * 0.4),
            clear=VGroup(self.parts, self.mos))
        self.parts = Group(title, pic)

    def band_bending(self):
        self.slide(say(
            """
            So how does a gate make a channel? Kahng's device was p-channel, on n-type silicon.
            We'll draw the mirror image, an n-channel device on p-type silicon, which works the
            same way with the signs flipped. Here is the gate, the oxide, and p-type silicon, with
            the silicon's energy bands drawn to the right: the conduction band, the intrinsic level,
            the valence band, and the Fermi level, flat. Put a positive voltage on the gate and the
            bands bend down near the surface. First the holes are pushed away, leaving a depletion
            layer of fixed negative charge. Bend further, until the intrinsic level at the surface
            drops below the Fermi level by as much as it sits above it in the bulk: that's surface
            potential two phi-F. There the surface has as many electrons as the bulk has holes, and
            beyond it, more. It has inverted. That thin layer of electrons is the channel.
            """,
            """
            তাহলে gate কীভাবে channel বানায়? Kahng-এর device ছিল p-channel, n-type silicon-এর উপর। আমরা আঁকবো
            তার আয়নার ছবি, p-type silicon-এর উপর একটা n-channel device, যেটা sign উল্টায়ে একইভাবে কাজ করে। এই যে
            gate, oxide, আর p-type silicon, ডানে silicon-এর energy
            band আঁকা: conduction band, intrinsic level, valence band, আর Fermi level, সমান। Gate-এ positive
            voltage দিলে surface-এর কাছে band নিচের দিকে বাঁকে। প্রথমে hole-গুলা সরে যায়, পিছনে থাকে fixed
            negative charge-এর একটা depletion layer। আরও বাঁকান, যতক্ষণ না surface-এ intrinsic level Fermi
            level-এর নিচে ততটাই নামে যতটা bulk-এ উপরে ছিল: এইটাই surface potential two phi-F। ওইখানে surface-এ
            electron-এর সংখ্যা bulk-এর hole-এর সমান, আর তার পরে বেশি। Surface invert হয়ে গেছে। Electron-এর ওই
            পাতলা layer-টাই channel।
            """,
        ))
        self.play(FadeOut(self.parts))
        title = heading("How a gate makes a channel")
        s = 2.4  # screen units per eV
        phi_f = phys.fermi_potential(N_A)
        x_s, x_end = -3.4, 1.8
        y_f = -0.9
        y_i = y_f + phi_f * s
        half = 0.56 * s
        w_max = 2.3
        psi = ValueTracker(0.0)

        gate = box(1.2, 4.2, -5.4, 0.1, GATE)
        ox = box(0.8, 4.2, -4.4, 0.1, OXIDE_TEXT, 0.35)
        gate_l = text("gate", size=22, color=BG, weight="SEMIBOLD").rotate(PI / 2).move_to(gate)
        ox_l = text("oxide", size=18, color=OXIDE_TEXT).rotate(PI / 2).move_to(ox)
        si_l = text("p-type silicon →", size=20, color=MUTED).move_to([1.0, -3.15, 0])

        def bend(x):
            w = w_max * np.sqrt(max(psi.get_value(), 1e-6) / (2 * phi_f))
            u = np.clip((x - x_s) / w, 0, 1)
            return psi.get_value() * (1 - u) ** 2 * s

        def band(offset, color, dashed=False):
            def make():
                xs = np.linspace(x_s, x_end, 80)
                pts = [[x, offset - bend(x), 0] for x in xs]
                m = VMobject(stroke_color=color, stroke_width=4).set_points_smoothly(pts)
                return DashedVMobject(m, num_dashes=40) if dashed else m
            return always_redraw(make)

        ec = band(y_i + half, ELECTRON)
        ei = band(y_i, MUTED, dashed=True)
        ev = band(y_i - half, HOLE)
        ef = DashedLine([x_s, y_f, 0], [x_end, y_f, 0], stroke_color=GATE, stroke_width=3)
        names = VGroup(
            MathTex("E_c", font_size=34, color=ELECTRON).move_to([x_end + 0.45, y_i + half, 0]),
            MathTex("E_i", font_size=34, color=MUTED).move_to([x_end + 0.45, y_i, 0]),
            MathTex("E_F", font_size=34, color=GATE).move_to([x_end + 0.45, y_f + 0.1, 0]),
            MathTex("E_v", font_size=34, color=HOLE).move_to([x_end + 0.45, y_i - half - 0.12, 0]),
        )
        holes = VGroup(*[Dot([x, y_i - half - 0.15 - 0.12 * (i % 3), 0], radius=0.05, color=HOLE)
                         for i, x in enumerate(np.linspace(x_s + 0.2, x_end - 0.2, 24))])

        def hole_update(m):
            w = w_max * np.sqrt(max(psi.get_value(), 1e-6) / (2 * phi_f)) if psi.get_value() > 0.01 else 0
            for d, x in zip(m, np.linspace(x_s + 0.2, x_end - 0.2, 24)):
                d.set_opacity(0.0 if x < x_s + w else 1.0)
                d.set_y(y_i - half - 0.15 - bend(x))

        holes.add_updater(hole_update)

        def electrons():
            p = psi.get_value()
            n = int(np.clip(16 / (1 + np.exp(-(p - 2 * phi_f + 0.06) / 0.025)), 0, 16))
            surf = y_i + half - bend(x_s)
            return VGroup(*[Dot([x_s + 0.1 + 0.11 * (i % 4), surf + 0.12 + 0.11 * (i // 4), 0], radius=0.045, color=ELECTRON) for i in range(n)])

        elec = always_redraw(electrons)

        def ions():
            w = w_max * np.sqrt(max(psi.get_value(), 1e-6) / (2 * phi_f)) if psi.get_value() > 0.01 else 0
            k = int(w / 0.35)
            return VGroup(*[MathTex("-", font_size=28, color=HOLE).move_to([x_s + 0.2 + 0.35 * i, -2.75, 0]) for i in range(k)])

        ion = always_redraw(ions)
        readout = always_redraw(lambda: VGroup(
            MathTex(r"\psi_s =", font_size=36), DecimalNumber(psi.get_value(), num_decimal_places=2, font_size=36, color=GATE),
            MathTex(r"\text{V}", font_size=36),
        ).arrange(RIGHT, buff=0.12).move_to([4.9, 2.4, 0]))
        phase = VGroup(
            text("flat bands", size=26, color=MUTED),
        ).move_to([4.9, 1.7, 0])

        self.play(FadeIn(title), FadeIn(gate), FadeIn(ox), FadeIn(gate_l), FadeIn(ox_l), FadeIn(si_l))
        self.play(Create(ec), Create(ei), Create(ev), Create(ef), FadeIn(names), run_time=1.5)
        self.add(holes, elec, ion)
        self.play(FadeIn(holes), FadeIn(readout), FadeIn(phase))
        dep = text("depletion:\nholes pushed away", size=26, color=HOLE).move_to(phase)
        self.play(psi.animate.set_value(phi_f), Transform(phase, dep), run_time=3)
        inv = text("inversion:\na layer of electrons", size=26, color=ELECTRON).move_to(phase)
        self.play(psi.animate.set_value(2 * phi_f), Transform(phase, inv), run_time=3)
        f1 = eq(r"\phi_F", r"=", r"\frac{k_BT}{q}", r"\ln\frac{N_A}{n_i}", size=40)
        f1[2].set_color(THERMAL)
        f2 = eq(r"\text{threshold:}\ ", r"\psi_s = 2\phi_F", size=40)
        cols = VGroup(f1, f2).arrange(DOWN, buff=0.3).move_to([4.9, -0.3, 0])
        f3 = text(f"N_A = 10¹⁷: 2φ_F = {2 * phi_f:.2f} V", size=22, color=MUTED).next_to(cols, DOWN, buff=0.25)
        self.play(Write(f1))
        self.play(Write(f2), FadeIn(f3))
        holes.clear_updaters()
        self.parts = VGroup(title, gate, ox, gate_l, ox_l, si_l, ec, ei, ev, ef, names, holes, elec, ion, readout, phase, cols, f3)

    # --- the threshold voltage ---------------------------------------------------------------
    def threshold(self):
        self.slide(say(
            """
            The threshold voltage is just the gate voltage that gets you there, and every term has a
            job. V-F-B lines the bands up flat: it comes from the difference in work functions and
            any charge in the oxide. Two phi-F bends them to inversion. And the last term holds up
            the depletion charge, through the oxide's capacitance. With ten to the seventeen doping
            and ten nanometres of oxide, it comes to about a third of a volt. And this is where your
            PDK's LVT, SVT and HVT come from: the same transistor with different doping and gate
            work function, so a different threshold.
            """,
            """
            Threshold voltage মানে শুধু ওই gate voltage যেটা দিয়া ওইখানে পৌঁছানো যায়, আর প্রত্যেকটা term-এর
            একটা কাজ আছে। V-F-B band-গুলারে সমান করে: এইটা আসে work function-এর পার্থক্য আর oxide-এর ভিতরের
            charge থেকে। Two phi-F band বাঁকায়ে inversion-এ নেয়। আর শেষ term-টা depletion charge-রে ধরে রাখে,
            oxide-এর capacitance দিয়া। দশের সতেরো ঘাত doping আর দশ nanometre oxide-এ এইটা আসে প্রায় এক volt-এর
            তিন ভাগের এক ভাগ। আর আপনার PDK-এর LVT, SVT, HVT আসে এইখান থেকেই: একই transistor, কিন্তু আলাদা
            doping আর gate work function, তাই আলাদা threshold।
            """,
        ))
        self.play(FadeOut(self.parts))
        title = heading("The threshold voltage, term by term")
        big = eq(r"V_T", r"=", r"V_{FB}", r"+", r"2\phi_F", r"+", r"\frac{\sqrt{2q\,\varepsilon_{Si}N_A\,(2\phi_F)}}{C_{ox}}", size=64)
        big[2].set_color(MUTED)
        big[4].set_color(GATE)
        big[6].set_color(HOLE)
        big.move_to(UP * 1.0)
        labels = VGroup(
            text("make the bands flat", size=22, color=MUTED).next_to(big[2], DOWN, buff=0.45),
            text("bend them to inversion", size=22, color=GATE).next_to(big[4], DOWN, buff=1.05),
            text("hold the depletion charge,\nthrough the oxide", size=22, color=HOLE).next_to(big[6], DOWN, buff=0.35),
        )
        vt = phys.threshold_voltage(N_A, T_OX, V_FB)
        ex = text(f"N_A = 10¹⁷ cm⁻³, t_ox = 10 nm, V_FB = {V_FB} V:  V_T ≈ {vt:.2f} V", size=26)
        ex_row = VGroup(ex, model_tag()).arrange(RIGHT, buff=0.3).move_to([0, -1.55, 0])
        note = layout_note("LVT / SVT / HVT in your PDK: the same device, different doping and gate work function.", size=22, width=90)
        note.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(title))
        self.play(Write(big[:2]))
        for i, lab in zip((2, 4, 6), labels):
            self.play(Write(big[i - 1:i + 1] if i > 2 else big[i]), FadeIn(lab, shift=UP * 0.1), run_time=1.2)
        self.play(FadeIn(ex_row))
        self.play(FadeIn(note, shift=UP * 0.2))
        self.parts = VGroup(title, big, labels, ex_row, note)

    # --- the layout view: W and L ------------------------------------------------------------
    def layout_view(self):
        self.slide(say(
            """
            Now the current. Look at a transistor the way you see it in layout: diffusion, with the
            poly gate crossing it. L is the distance across the gate, source to drain. W is the
            width of the channel, along the gate. Above threshold, in saturation, the current goes
            as W over L, times the overdrive squared. That's the square law. The ratio you draw sets
            the current, which is why matched devices copy W, L, fingers and orientation exactly.
            """,
            """
            এবার current। Transistor-টারে layout-এ যেভাবে দেখেন সেভাবে দেখেন: diffusion, আর তার উপর দিয়া poly
            gate। L হইলো gate-এর এপার-ওপার, source থেকে drain। W হইলো gate বরাবর channel-এর চওড়া। Threshold-এর
            উপরে, saturation-এ, current যায় W বাই L গুণ overdrive-এর square হিসাবে। এইটাই square law। আপনি যে
            ratio আঁকেন সেটাই current ঠিক করে, তাই matched device-এ W, L, finger আর orientation হুবহু copy করা
            হয়।
            """,
        ))
        self.play(FadeOut(self.parts))
        title = heading("The W and L you draw")
        od = box(4.6, 2.4, -3.2, -0.2, SILICON, 0.45)
        poly = box(0.7, 3.6, -3.2, -0.2, GATE, 0.95)
        cts = VGroup(*[box(0.32, 0.32, -3.2 + dx, y, METAL) for dx in (-1.5, 1.5) for y in (-0.9, -0.2, 0.5)])
        l_arr = DoubleArrow([-3.55, 1.85, 0], [-2.85, 1.85, 0], buff=0, stroke_color=INK, stroke_width=3, tip_length=0.14)
        l_lbl = MathTex("L", font_size=40).next_to(l_arr, UP, buff=0.08)
        w_arr = DoubleArrow([-0.65, -1.4, 0], [-0.65, 1.0, 0], buff=0, stroke_color=INK, stroke_width=3, tip_length=0.14)
        w_lbl = MathTex("W", font_size=40).next_to(w_arr, RIGHT, buff=0.1)
        tags = VGroup(
            text("diffusion", size=20, color=INK).next_to(od, DOWN, buff=0.12).align_to(od, LEFT),
            text("poly gate", size=20, color=GATE).next_to(poly, DOWN, buff=0.12),
            text("source", size=20, color=MUTED).move_to([-4.7, 1.25, 0]),
            text("drain", size=20, color=MUTED).move_to([-1.7, 1.25, 0]),
        )
        self.play(FadeIn(title))
        self.play(FadeIn(od), FadeIn(poly), FadeIn(cts), FadeIn(tags))
        self.play(GrowFromCenter(l_arr), FadeIn(l_lbl), GrowFromCenter(w_arr), FadeIn(w_lbl))
        sq = eq(r"I_D", r"=", r"\tfrac{1}{2}\,", r"\mu C_{ox}", r"\,\frac{W}{L}", r"\,(V_{GS}-V_T)^2", size=48)
        sq[4].set_color(GATE)
        sq.move_to([3.7, 1.2, 0])
        sq.shift(LEFT * max(0, sq.get_right()[0] - 6.6))  # keep a margin from the frame's edge
        sat = text("saturation (the square law)", size=22, color=MUTED).next_to(sq, UP, buff=0.25)
        k = 400 * phys.oxide_capacitance_cm2(T_OX)
        i_ex = phys.square_law_current(0.84, 1.0, 0.34, k, 10)
        ex = text(f"W/L = 10, overdrive 0.5 V:  I_D ≈ {i_ex * 1e6:.0f} µA", size=22)
        ex_row = VGroup(ex, model_tag()).arrange(RIGHT, buff=0.3).next_to(sq, DOWN, buff=0.45)
        note = layout_note("The ratio you draw sets the current: matched devices copy W, L, fingers and orientation.", size=22, width=44)
        note.move_to([3.4, -2.0, 0])
        self.play(FadeIn(sat), Write(sq))
        self.play(Indicate(sq[4], color=GATE), Indicate(VGroup(l_lbl, w_lbl), color=GATE))
        self.play(FadeIn(ex_row))
        self.play(FadeIn(note, shift=UP * 0.2))
        self.parts = VGroup(title, od, poly, cts, l_arr, l_lbl, w_arr, w_lbl, tags, sat, sq, ex_row, note)

    # --- pinch-off and the output curves (with a ↓ derivation) -------------------------------
    def pinch_off(self):
        self.slide(say(
            """
            Here's the channel from the side. Raise the drain voltage and the channel gets thinner
            at the drain end, because the gate has less voltage over the channel there. When V-D-S
            reaches the overdrive, the channel pinches off at the drain, and the current stops
            rising: saturation. That's the flat part of every output curve you've seen. Press down
            for the derivation.
            """,
            """
            এইটা পাশ থেকে দেখা channel। Drain voltage বাড়াইলে drain-এর দিকে channel পাতলা হয়ে যায়, কারণ
            ওইখানে channel-এর উপর gate-এর voltage কম। V-D-S যখন overdrive-এর সমান হয়, drain-এর কাছে channel
            pinch off হয়ে যায়, আর current বাড়া বন্ধ হয়: saturation। আপনারা যত output curve দেখছেন, তার flat
            অংশটা এইটাই। Derivation দেখতে চাইলে নিচে (↓) যান।
            """,
        ))
        self.play(FadeOut(self.parts))
        title = heading("Pinch-off: why the current saturates")
        vov = 0.5
        vds = ValueTracker(0.0)
        x0, x1, y0 = -6.0, -1.2, 0.2
        gate = box(x1 - x0 - 0.6, 0.35, (x0 + x1) / 2, y0 + 0.95, GATE)
        ox = box(x1 - x0 - 0.6, 0.12, (x0 + x1) / 2, y0 + 0.72, OXIDE_TEXT)
        src = box(0.8, 0.7, x0 + 0.1, y0 + 0.25, ELECTRON, 0.55)
        drn = box(0.8, 0.7, x1 - 0.1, y0 + 0.25, ELECTRON, 0.55)
        body = box(x1 - x0 + 0.4, 1.6, (x0 + x1) / 2, y0 - 0.55, PSUB)

        def channel():
            xs = np.linspace(x0 + 0.5, x1 - 0.5, 60)
            v = vds.get_value()
            # local channel charge ~ (V_ov - V(x)), with V(x) from the gradual-channel solution
            th = []
            for u in np.linspace(0, 1, 60):
                vs = min(v, vov)
                vx = vov - np.sqrt(max(vov**2 - u * (2 * vov * vs - vs * vs), 0))
                th.append(max(vov - vx, 0) / vov * 0.42)
            top = [[x, y0 + 0.62, 0] for x in xs]
            bot = [[x, y0 + 0.62 - t, 0] for x, t in zip(xs[::-1], th[::-1])]
            return Polygon(*top, *bot, fill_color=ELECTRON, fill_opacity=0.85, stroke_width=0)

        chan = always_redraw(channel)
        labels = VGroup(
            text("source", size=20, color=MUTED).next_to(src, DOWN, buff=0.2),
            text("drain", size=20, color=MUTED).next_to(drn, DOWN, buff=0.2),
            text("channel", size=20, color=ELECTRON).move_to([(x0 + x1) / 2, y0 - 0.35, 0]),
        )
        axes = Axes(x_range=[0, 1.2, 0.2], y_range=[0, 1.1, 0.25], x_length=5.2, y_length=3.6, tips=False,
                    axis_config={"stroke_color": MUTED, "stroke_width": 2, "include_ticks": False}).move_to([3.4, -0.2, 0])
        xl = MathTex(r"V_{DS}", font_size=32, color=MUTED).next_to(axes.x_axis, DOWN, buff=0.2)
        yl = MathTex(r"I_D", font_size=32, color=MUTED).next_to(axes.y_axis, UP, buff=0.15)
        k, wl = 1.0, 1.0
        norm = 0.5 * k * wl * 0.7**2

        def curve(v_ov, color):
            return axes.plot(lambda x: phys.square_law_current(v_ov + 0.34, x, 0.34, k, wl) / norm, x_range=[0, 1.2], color=color, stroke_width=4)

        fam = VGroup(curve(0.3, FAINT), curve(0.5, ELECTRON), curve(0.7, FAINT))
        dot = always_redraw(lambda: Dot(axes.c2p(vds.get_value(), phys.square_law_current(vov + 0.34, vds.get_value(), 0.34, k, wl) / norm), color=GATE, radius=0.08))
        sat_line = DashedLine(axes.c2p(vov, 0), axes.c2p(vov, 1.05), stroke_color=GATE, stroke_width=2)
        sat_l = MathTex(r"V_{DS} = V_{GS}-V_T", font_size=28, color=GATE).next_to(sat_line, UP, buff=0.05)
        self.play(FadeIn(title), FadeIn(body), FadeIn(src), FadeIn(drn), FadeIn(ox), FadeIn(gate), FadeIn(labels))
        self.add(chan)
        self.play(Create(axes), FadeIn(xl), FadeIn(yl), Create(fam), FadeIn(dot))
        self.play(vds.animate.set_value(vov), run_time=3)
        po = text("pinched off at the drain", size=22, color=GATE).move_to([x1 - 1.0, y0 + 1.55, 0])
        self.play(FadeIn(sat_line), FadeIn(sat_l), FadeIn(po))
        self.play(vds.animate.set_value(1.1), run_time=2)
        lin = eq(r"I_D = \mu C_{ox}\frac{W}{L}\Big[(V_{GS}-V_T)V_{DS} - \tfrac{1}{2}V_{DS}^2\Big]", size=34)
        lin_l = text("linear region", size=20, color=MUTED)
        VGroup(lin_l, lin).arrange(DOWN, buff=0.1).to_edge(DOWN, buff=0.4)
        hint = text("↓ derivation", size=20, color=MUTED).to_corner(DR, buff=0.35)
        self.play(FadeIn(lin_l), Write(lin), FadeIn(hint))
        screen = VGroup(title, body, src, drn, ox, gate, labels, chan, axes, xl, yl, fam, dot, sat_line, sat_l, po, lin_l, lin, hint)

        steps = [
            (eq(r"Q_i(y) = -C_{ox}\big(V_{GS}-V_T-V(y)\big)"), ("Charge in the channel at a point y along it.", "Channel-এর y জায়গায় charge।")),
            (eq(r"I_D = -W\,\mu\,Q_i(y)\,\frac{dV}{dy}"), ("Current = charge × velocity, and velocity = μ × field.", "Current = charge × velocity, আর velocity = μ × field।")),
            (eq(r"\int_0^L I_D\,dy = W\mu C_{ox}\int_0^{V_{DS}}\big(V_{GS}-V_T-V\big)\,dV"), ("I_D is the same everywhere: integrate source to drain.", "I_D সব জায়গায় সমান: source থেকে drain integrate করেন।")),
            (eq(r"I_D = \mu C_{ox}\frac{W}{L}\Big[(V_{GS}-V_T)V_{DS}-\tfrac{1}{2}V_{DS}^2\Big]\ \xrightarrow{V_{DS}=V_{GS}-V_T}\ \tfrac{1}{2}\mu C_{ox}\frac{W}{L}(V_{GS}-V_T)^2", size=34),
             ("At pinch-off the bracket peaks: that's the square law.", "Pinch-off-এ bracket-টা maximum: এইটাই square law।")),
        ]
        shown = VGroup()
        y = 2.5
        for i, (m, (why, why_bn)) in enumerate(steps):
            self.slide(say(f"Derivation, step {i + 1} of 4: {why}", f"Derivation, step {i + 1} / 4: {why_bn}"), direction="vertical")
            if i == 0:
                self.detour_in(screen)
            w = text(why, size=22, color=MUTED)
            VGroup(m, w).arrange(DOWN, buff=0.12).move_to([0, y, 0])
            y -= 1.5
            self.play(Write(m), FadeIn(w))
            shown.add(m, w)
        self.slide(say("Back to the story.", "আবার গল্পে ফিরি।"), direction="vertical")
        self.detour_out(screen, shown)
        self.parts = screen

    # --- CMOS --------------------------------------------------------------------------------
    def cmos(self):
        title, pic = self.show_figure(say(
            """
            In June 1963 Frank Wanlass, at Fairchild, filed this patent. Figure 5: an n-channel and
            a p-channel transistor in series between the supplies, their gates tied together. Under
            it, the input and the output: when one goes up, the other comes down.
            """,
            """
            June 1963-এ Fairchild-এর Frank Wanlass এই patent file করেন। Figure 5: supply-গুলার মাঝে series-এ
            একটা n-channel আর একটা p-channel transistor, gate দুইটা একসাথে জোড়া। নিচে input আর output: একটা
            উঠলে আরেকটা নামে।
            """,
        ), "1963: CMOS, a switch that sips power",
            figure(IMAGES / "wanlass_US3356858_fig5.png", 5.9,
                   "F. M. Wanlass, US patent 3,356,858, filed 1963 (public domain)").move_to(DOWN * 0.4),
            clear=self.parts)

        self.slide(say(
            """
            Here's how it switches. Input low: the p-device is on and the n-device is off, so the
            output is high. Input high: the reverse. With the input at either rail, one of them is
            off, so ideally no current flows from supply to ground, apart from leakage. Only while
            the input passes through the middle are both partly on, and a little current flows
            straight through: that hump, plotted against the input voltage. Most of the power goes
            into charging the load: alpha C V squared f, with alpha the share of clock cycles in
            which the node rises from 0 to 1. Real chips add that short-circuit current and
            leakage. Wanlass and C. T. Sah called their 1963 paper nanowatt logic.
            """,
            """
            এইটা কীভাবে switch করে দেখেন। Input low হলে p-device on, n-device off, তাই output high। Input high হলে
            উল্টা। Input যেকোনো rail-এ থাকলে একটা না একটা off থাকে, তাই ideally supply থেকে ground-এ কোনো current যায়
            না, leakage বাদে। শুধু input যখন মাঝখান দিয়া যায়, দুইটাই আংশিক on থাকে, আর সোজা একটু current চলে যায়: ওই
            কুঁজটা, input voltage-এর সাথে আঁকা। Power-এর বেশিরভাগ যায় load charge করতে: alpha C V square f, যেখানে alpha হইলো
            কত ভাগ clock cycle-এ node 0 থেকে 1-এ ওঠে। আসল chip-এ এর সাথে যোগ হয় ওই short-circuit current আর leakage।
            Wanlass আর C. T. Sah-এর 1963-এর paper-এর নামই ছিল nanowatt logic।
            """,
        ))
        self.play(FadeOut(pic))
        x = -3.6
        vdd = Line([x - 1.4, 2.4, 0], [x + 1.4, 2.4, 0], stroke_color=INK, stroke_width=4)
        gnd = Line([x - 1.4, -2.6, 0], [x + 1.4, -2.6, 0], stroke_color=INK, stroke_width=4)
        vdd_l = MathTex("V_{DD}", font_size=32).next_to(vdd, UP, buff=0.1)
        gnd_l = MathTex("0", font_size=32).next_to(gnd, DOWN, buff=0.1)

        def fet(yc, kind):
            ch = Line([x, yc - 0.5, 0], [x, yc + 0.5, 0], stroke_color=INK, stroke_width=6)
            g = Line([x - 0.25, yc - 0.45, 0], [x - 0.25, yc + 0.45, 0], stroke_color=GATE, stroke_width=5)
            bub = Circle(radius=0.09, stroke_color=GATE, stroke_width=3).move_to([x - 0.37, yc, 0]) if kind == "p" else VMobject()
            lead = Line([x - 1.3, yc, 0], [x - (0.46 if kind == "p" else 0.25), yc, 0], stroke_color=GATE, stroke_width=3)
            lbl = text("pMOS" if kind == "p" else "nMOS", size=20, color=HOLE if kind == "p" else ELECTRON).next_to(ch, RIGHT, buff=0.15)
            return VGroup(ch, g, bub, lead, lbl)

        p = fet(1.0, "p")
        n = fet(-1.2, "n")
        wires = VGroup(
            Line([x, 2.4, 0], [x, 1.5, 0]), Line([x, 0.5, 0], [x, -0.7, 0]), Line([x, -1.7, 0], [x, -2.6, 0]),
            Line([x - 1.3, 1.0, 0], [x - 1.3, -1.2, 0]), Line([x - 1.3, -0.1, 0], [x - 2.1, -0.1, 0]),
            Line([x, -0.1, 0], [x + 1.4, -0.1, 0]),
        ).set_stroke(INK, 3)
        in_l = MathTex(r"V_{in}", font_size=34, color=GATE).next_to([x - 2.1, -0.1, 0], LEFT, buff=0.1)
        out_l = MathTex(r"V_{out}", font_size=34).next_to([x + 1.4, -0.1, 0], RIGHT, buff=0.1)
        self.play(Create(vdd), Create(gnd), FadeIn(vdd_l), FadeIn(gnd_l), FadeIn(p), FadeIn(n), Create(wires), FadeIn(in_l), FadeIn(out_l), run_time=1.5)
        path_hi = VGroup(Line([x, 2.4, 0], [x, 0.5, 0]), Line([x, 0.5, 0], [x, -0.1, 0]), Line([x, -0.1, 0], [x + 1.4, -0.1, 0])).set_stroke(GOOD, 7)
        path_lo = VGroup(Line([x, -2.6, 0], [x, -0.1, 0]), Line([x, -0.1, 0], [x + 1.4, -0.1, 0])).set_stroke(GOOD, 7)
        st = VGroup(text("in 0 → out 1", size=26, color=GOOD)).move_to([x, -3.3, 0])
        self.play(Create(path_hi), FadeIn(st), p[0].animate.set_stroke(GOOD), run_time=1)
        self.wait(0.8)
        st2 = text("in 1 → out 0", size=26, color=GOOD).move_to(st)
        self.play(FadeOut(path_hi), Create(path_lo), Transform(st, st2), p[0].animate.set_stroke(INK), n[0].animate.set_stroke(GOOD), run_time=1)
        self.wait(0.8)

        axes = Axes(x_range=[0, 1, 0.5], y_range=[0, 1, 0.5], x_length=3.6, y_length=3.0, tips=False,
                    axis_config={"stroke_color": MUTED, "stroke_width": 2, "include_ticks": False}).move_to([1.2, 0.7, 0])
        vtc = axes.plot(lambda v: 1 / (1 + np.exp((v - 0.5) / 0.045)), x_range=[0, 1], color=GATE, stroke_width=4)
        cur = axes.plot(lambda v: 0.9 * np.exp(-((v - 0.5) / 0.07) ** 2), x_range=[0, 1], color=THERMAL, stroke_width=3)
        ax_l = VGroup(MathTex(r"V_{in}", font_size=28, color=MUTED).next_to(axes.x_axis, DOWN, buff=0.15),
                      MathTex(r"V_{out}", font_size=28, color=GATE).next_to(axes.y_axis, UP, buff=0.1))
        cur_l = text("through-current vs. V_in (qualitative):\nboth devices on in the middle", size=18, color=THERMAL).next_to(axes, DOWN, buff=0.5)
        self.play(Create(axes), FadeIn(ax_l), Create(vtc))
        self.play(Create(cur), FadeIn(cur_l))
        pw = eq(r"P", r"\approx", r"\alpha\,C\,", r"V_{DD}^2", r"\,f", size=50).move_to([4.9, 1.2, 0])
        pw[3].set_color(THERMAL)
        pw2 = eq(r"+\,P_{sc}", r"+\,V_{DD}I_{leak}", size=36, color=MUTED).next_to(pw, DOWN, buff=0.2)
        pw_l = text("α: share of cycles with\na 0→1 transition", size=18, color=MUTED).next_to(pw2, DOWN, buff=0.25)
        pw_l = VGroup(pw2, pw_l)
        VGroup(pw, pw_l).shift(LEFT * max(0, VGroup(pw, pw_l).get_right()[0] - 6.6))
        src = source("F. Wanlass & C. T. Sah, “Nanowatt logic…”, ISSCC 1963")
        self.play(Write(pw), FadeIn(pw_l), FadeIn(src))
        self.inv = VGroup(vdd, gnd, vdd_l, gnd_l, p, n, wires, in_l, out_l, path_lo, st)
        self.parts = VGroup(title, axes, vtc, cur, ax_l, cur_l, pw, pw_l, src)

    # --- latch-up ----------------------------------------------------------------------------
    def latchup(self):
        self.slide(say(
            """
            But CMOS has a price, and you pay it in layout. Build the inverter in silicon: the
            nMOS sits in the p-substrate, the pMOS in an n-well. Look at the layers from the pMOS
            source down: p-plus, n-well, p-substrate, and across to the nMOS source, n-plus. That's
            p-n-p-n: two parasitic bipolar transistors wired in a loop, a thyristor. Kick it with a
            current spike and each transistor turns the other on harder: the loop latches, and the
            supply is shorted to ground until you cut the power. That's latch-up. What breaks the
            loop is low resistance in the well and substrate: taps close to the devices, and guard
            rings. That's what those layout rules are for.
            """,
            """
            কিন্তু CMOS-এর একটা দাম আছে, আর সেটা দিতে হয় layout-এ। Inverter-টা silicon-এ বানান: nMOS বসে
            p-substrate-এ, pMOS বসে n-well-এ। pMOS-এর source থেকে নিচের দিকে layer-গুলা দেখেন: p-plus, n-well,
            p-substrate, তারপর পাশে nMOS-এর source, n-plus। মানে p-n-p-n: দুইটা parasitic bipolar transistor
            একটা loop-এ জোড়া, একটা thyristor। একটা current spike দিয়া ধাক্কা দেন, প্রত্যেকটা আরেকটারে আরও
            জোরে on করে: loop latch হয়ে যায়, আর power না কাটা পর্যন্ত supply ground-এর সাথে short। এইটাই
            latch-up। Loop ভাঙে well আর substrate-এর কম resistance দিয়া: device-এর কাছে tap, আর guard ring।
            আপনাদের ওই layout rule-গুলা এইজন্যই।
            """,
        ))
        self.inv_copy = self.inv.copy()
        self.play(FadeOut(self.parts), FadeOut(self.inv))
        title = heading("The price of CMOS: latch-up")
        y_top = 0.6
        sub = box(11.0, 3.2, 0.4, y_top - 1.6, PSUB)
        well = box(4.8, 1.9, 3.1, y_top - 0.95, NWELL, 0.95)
        def dif(x, color, lab):
            r = box(0.9, 0.42, x, y_top - 0.21, color, 0.9)
            return VGroup(r, text(lab, size=16, color=BG, weight="SEMIBOLD").move_to(r))
        n_src = dif(-2.6, ELECTRON, "n⁺")
        n_drn = dif(-0.8, ELECTRON, "n⁺")
        p_tap = dif(-4.4, HOLE, "p⁺")
        p_src = dif(3.7, HOLE, "p⁺")
        p_drn = dif(1.9, HOLE, "p⁺")
        n_tap = dif(5.0, ELECTRON, "n⁺")
        g1 = box(0.8, 0.28, -1.7, y_top + 0.16, GATE)
        g2 = box(0.8, 0.28, 2.8, y_top + 0.16, GATE)
        tags = VGroup(
            text("p-substrate", size=20, color=MUTED).move_to([-2.0, y_top - 2.7, 0]),
            text("n-well", size=20, color=INK).move_to([3.1, y_top - 1.6, 0]),
            text("substrate tap → 0", size=16, color=MUTED).next_to(p_tap, UP, buff=0.75),
            text("well tap → V_DD", size=16, color=MUTED).next_to(n_tap, UP, buff=0.75),
            text("nMOS", size=20, color=ELECTRON).next_to(g1, UP, buff=0.45),
            text("pMOS", size=20, color=HOLE).next_to(g2, UP, buff=0.45),
        )
        self.play(FadeIn(title), FadeIn(sub), FadeIn(well))
        self.play(*[FadeIn(m) for m in (n_src, n_drn, p_tap, p_src, p_drn, n_tap, g1, g2)], FadeIn(tags), run_time=1.5)
        # The parasitic thyristor: vertical PNP (p+ source / n-well / p-sub), lateral NPN (n-well / p-sub / n+ source).
        pnp = Arrow([3.7, y_top - 0.45, 0], [3.7, y_top - 2.2, 0], buff=0, stroke_color=DRAIN, stroke_width=5)
        npn = Arrow([1.0, y_top - 1.2, 0], [-2.6, y_top - 0.5, 0], buff=0, stroke_color=DRAIN, stroke_width=5)
        pnp_l = text("PNP", size=20, color=DRAIN, weight="SEMIBOLD").next_to(pnp, RIGHT, buff=0.1)
        npn_l = text("NPN", size=20, color=DRAIN, weight="SEMIBOLD").next_to(npn, DOWN, buff=0.1)
        loop = text("a parasitic thyristor: p-n-p-n", size=24, color=DRAIN).to_edge(DOWN, buff=1.05)
        self.play(GrowArrow(pnp), GrowArrow(npn), FadeIn(pnp_l), FadeIn(npn_l), FadeIn(loop))
        surge = VGroup(*[Dot(radius=0.07, color=DRAIN) for _ in range(10)])
        path = VMobject().set_points_smoothly([[3.7, y_top - 0.5, 0], [3.7, y_top - 2.1, 0], [1.0, y_top - 2.3, 0],
                                               [-2.6, y_top - 0.6, 0], [0.5, y_top - 0.8, 0], [3.7, y_top - 0.5, 0]])
        clock = ValueTracker(0.0)

        def ride(m):
            for i, d in enumerate(m):
                d.move_to(path.point_from_proportion((clock.get_value() + i / len(m)) % 1))

        surge.add_updater(ride)
        cond = eq(r"\beta_{npn}\,\beta_{pnp} > 1", r"\ \Rightarrow\ ", r"\text{latch}", size=38)
        cond[0].set_color(DRAIN)
        cond.to_corner(UR, buff=0.4).shift(DOWN * 0.7 + LEFT * 0.3)
        short = text("V_DD shorted to ground", size=26, color=DRAIN, weight="SEMIBOLD").next_to(cond, DOWN, buff=0.2).align_to(cond, RIGHT)
        self.add(surge)
        self.play(clock.animate.set_value(2), FadeIn(cond), FadeIn(short), run_time=4, rate_func=linear)
        surge.clear_updaters()

        self.slide(say(
            """
            The fix is resistance, or rather the lack of it. The loop only latches if enough current
            flows through the well and substrate to turn the parasitic transistors on. Put taps
            close to the devices and surround them with guard rings, and that current has a short,
            low-resistance path to the supply instead. The loop can't build up. That is exactly
            what the tap-spacing and guard-ring rules in your DRC deck are protecting.
            """,
            """
            Fix-টা হইলো resistance, মানে resistance কমানো। Loop latch হয় শুধু যদি well আর substrate দিয়া
            যথেষ্ট current যায় parasitic transistor-গুলারে on করার মতো। Device-এর কাছে tap বসান, guard ring
            দিয়া ঘিরে দেন, তাহলে ওই current একটা ছোট, কম-resistance রাস্তা পায় supply-তে চলে যাওয়ার। Loop আর
            গড়ে উঠতে পারে না। আপনার DRC deck-এর tap-spacing আর guard-ring rule-গুলা ঠিক এইটাই protect করে।
            """,
        ))
        ring_n = SurroundingRectangle(VGroup(n_src, n_drn, g1), color=HOLE, buff=0.35, stroke_width=6)
        ring_p = SurroundingRectangle(VGroup(p_src, p_drn, g2), color=ELECTRON, buff=0.35, stroke_width=6)
        rings_l = text("guard rings + close taps", size=24, color=GOOD, weight="SEMIBOLD").next_to(cond, DOWN, buff=0.2).align_to(cond, RIGHT)
        self.play(FadeOut(surge), Create(ring_n), Create(ring_p), pnp.animate.set_opacity(0.25), npn.animate.set_opacity(0.25), Transform(short, rings_l))
        note = layout_note("Taps close to the devices and guard rings keep the well and substrate resistance low: no latch.", size=22, width=52)
        note.to_edge(DOWN, buff=0.3)
        self.play(FadeOut(loop), FadeIn(note, shift=UP * 0.2))
        self.parts = VGroup(title, sub, well, n_src, n_drn, p_tap, p_src, p_drn, n_tap, g1, g2, tags, pnp, npn, pnp_l, npn_l, cond, short, ring_n, ring_p, note)

    # --- cliffhanger -------------------------------------------------------------------------
    def cliffhanger(self):
        self.slide(say(
            """
            So by the mid-1960s we have it: a switch that barely leaks, burns power only when it
            switches, and is made by drawing shapes on masks. Now ask the obvious question. What
            happens if you draw everything smaller?
            """,
            """
            তো 1960-এর দশকের মাঝামাঝি আমাদের হাতে চলে আসলো: এমন একটা switch যেটা প্রায় leak করে না, power
            খায় শুধু switch করার সময়, আর mask-এ shape এঁকে বানানো যায়। এবার obvious প্রশ্নটা করেন। সবকিছু যদি
            আরও ছোট করে আঁকেন, তাহলে কী হয়?
            """,
        ))
        inv = self.inv_copy.move_to(ORIGIN + UP * 0.4)
        self.play(FadeOut(self.parts), FadeIn(inv))
        q = text("What happens if you draw everything smaller?", size=40, weight="SEMIBOLD", color=GATE)
        q.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(q))
        for _ in range(3):
            self.play(inv.animate.scale(0.6), run_time=0.8)

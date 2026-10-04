"""Chapter 11 · Beyond silicon, beyond Boltzmann (the 2030s and after: research).

Channels one molecule thick, and the old problem they bring back (the contacts); two ways to
try to beat 60 mV per decade; and the two floors no design gets under: tunnelling straight
through a very short channel, and Landauer's k_BT ln 2.
"""

import sys
from math import log10
from pathlib import Path

LECTURE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(LECTURE.parents[1]), str(LECTURE)]

from manim import *  # noqa: E402,F403
from manim_slides import Slide  # noqa: E402

import physics as phys  # noqa: E402
from kit.motifs import xsection  # noqa: E402
from kit.style import *  # noqa: E402,F403

CHANNEL = "#7FD8E4"
MO, S = "#7FA7E8", "#E9D66B"  # molybdenum and sulfur atoms
METAL_C = "#9AA3AF"
E_B = 0.4  # the channel's barrier in the tunnelling model, eV


class Ch11Beyond(Chapter, Slide):
    def construct(self):
        self.card()
        self.thin_silicon()
        self.two_d()
        self.contacts()
        self.beat_sixty()
        self.tfet()
        self.ncfet()
        self.tunnelling_floor()
        self.landauer()
        self.other_roads()
        self.cliffhanger()

    # --- chapter card ------------------------------------------------------------------------
    def card(self):
        self.slide(say(
            """
            Everything from here on is research. Some of it will reach products, most of it
            won't, and nobody knows which. But the questions are the same ones we've been asking
            all along: how thin can the channel get, and can anything beat Boltzmann?
            """,
            """
            এখান থেকে সবকিছু research। এর কিছু product-এ যাবে, বেশিরভাগই যাবে না, আর কোনটা যাবে কেউ জানে না। কিন্তু
            প্রশ্নগুলা সেই একই, যা আমরা শুরু থেকে করতেছি: channel কত পাতলা হইতে পারে, আর কেউ কি Boltzmann-রে হারাইতে
            পারবে?
            """,
        ))
        self.card_group = self.open_chapter(11, 2040, 2033, "Beyond silicon", "…and beyond Boltzmann (research)")

    # --- silicon's last nanometres -----------------------------------------------------------
    def thin_silicon(self):
        r = phys.roughness_mobility_ratio(3, 5)
        self.slide(say(
            f"""
            Every chapter since the sixth has made the channel thinner, because lambda goes as
            the square root of its thickness. Today's sheets are 5 nanometres. Why not 3, or 1?
            Because silicon stops working. Remember the sixth power from the FinFET chapter:
            thinning a sheet from 5 to 3 nanometres would cut the roughness-limited mobility to
            about {r * 100:.0f} percent. At a few atoms thick, every bump on the surface is a big
            fraction of the whole channel.
            """,
            f"""
            Chapter ছয় থেকে প্রত্যেক chapter channel পাতলা করছে, কারণ lambda বাড়ে thickness-এর square root হারে। আজকের
            sheet 5 nanometre। 3 বা 1 না কেন? কারণ silicon আর কাজ করে না। FinFET chapter-এর sixth power মনে আছে: sheet 5 থেকে
            3 nanometre-এ পাতলা করলে roughness-limited mobility নেমে যাবে মোটে {r * 100:.0f} percent-এ। কয়েকটা atom পুরু হলে
            surface-এর প্রত্যেকটা খাঁজ পুরা channel-এর একটা বড় অংশ।
            """,
        ))
        self.play(FadeOut(self.card_group))
        title = heading("Silicon's last nanometres")
        u = 0.55  # units per nm
        bars = VGroup()
        for t, label in ((5, "5 nm: today's sheet"), (3, "3 nm"), (1, "1 nm")):
            bar = Rectangle(width=1.6, height=t * u, fill_color=CHANNEL, fill_opacity=0.85, stroke_width=0)
            layers = VGroup(*[Line(bar.get_left() + UP * (bar.height / 2 - k * 0.136 * u), bar.get_right() + UP * (bar.height / 2 - k * 0.136 * u),
                                   stroke_color=BG, stroke_width=0.6, stroke_opacity=0.5) for k in range(1, int(t / 0.136))])
            bars.add(VGroup(bar, layers, text(label, size=22, color=MUTED).next_to(bar, DOWN, buff=0.2)))
        bars.arrange(RIGHT, buff=0.8, aligned_edge=DOWN).move_to([-3.0, -0.6, 0])
        lam = MathTex(r"\lambda", r"\propto", r"\sqrt{t_{ch}}", font_size=60).move_to([3.3, 1.6, 0])
        lam[2].set_color(CHANNEL)
        mu = VGroup(MathTex(r"\mu_{rough}\propto t^6", font_size=44, color=ELECTRON),
                    text(f"5 → 3 nm: ×{r:.2f}", size=28, color=DRAIN),
                    text("(illustrative; chapter 7)", size=18, color=MUTED)).arrange(DOWN, buff=0.25).move_to([3.3, -0.6, 0])
        lines = text("one line = one layer of silicon atoms (0.14 nm)", size=18, color=MUTED).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(title), Write(lam))
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in bars], lag_ratio=0.3), FadeIn(lines), run_time=1.5)
        self.play(FadeIn(mu))

    def two_d(self):
        lam_si = phys.natural_length_nm(5, 1, 4)
        lam_2d = phys.natural_length_nm(0.65, 1, 2)
        self.slide(say(
            f"""
            So use a material that is thin by nature. Molybdenum disulfide, MoS2, comes in sheets
            one molecule thick: a layer of molybdenum between two layers of sulfur, 0.65
            nanometres in all. Its surfaces have no loose bonds, and its thickness can't vary,
            because it's set by the crystal. Put it in the lambda formula with a gate above and
            below: lambda is about {lam_2d:.1f} nanometre, against {lam_si:.1f} for a silicon
            nanosheet. The shortest workable gate halves, to about 6 nanometres. imec's roadmap
            brings 2D channels in after the CFET, around its A2 node.
            """,
            f"""
            তাহলে এমন material নেন যেটা স্বভাবতই পাতলা। Molybdenum disulfide, MoS2, আসে এক molecule পুরু sheet-এ:
            দুই layer sulfur-এর মাঝে এক layer molybdenum, সব মিলায়ে 0.65 nanometre। এর surface-এ কোনো খোলা bond নাই, আর
            thickness বদলাইতে পারে না, কারণ crystal-ই সেটা ঠিক করে। উপরে আর নিচে gate দিয়া lambda formula-য় বসান: lambda
            প্রায় {lam_2d:.1f} nanometre, silicon nanosheet-এর {lam_si:.1f}-এর বিপরীতে। সবচেয়ে ছোট কাজের gate অর্ধেক হয়ে প্রায় 6
            nanometre। imec-এর roadmap 2D channel আনে CFET-এর পরে, ওদের A2 node-এর আশেপাশে।
            """,
        ))
        self.clear()
        title = heading("A channel one molecule thick")
        # MoS2 seen from the side: S, Mo, S.
        atoms = VGroup()
        for row, (y, color, r) in enumerate(((0.55, S, 0.17), (0.0, MO, 0.22), (-0.55, S, 0.17))):
            for k in range(9):
                x = -4.6 + k * 0.62 + (0.31 if row == 1 else 0)
                atoms.add(Circle(radius=r, fill_color=color, fill_opacity=1, stroke_width=0).move_to([x, y + 0.9, 0]))
        bonds = VGroup()
        for k in range(9):
            mo = atoms[9 + k].get_center()
            for s_ in (atoms[k], atoms[min(k + 1, 8)], atoms[18 + k], atoms[18 + min(k + 1, 8)]):
                bonds.add(Line(mo, s_.get_center(), stroke_color=MUTED, stroke_width=2))
        mol = VGroup(bonds, atoms)
        br = BraceBetweenPoints(atoms[0].get_top() + LEFT * 0.35, atoms[18].get_bottom() + LEFT * 0.35, direction=LEFT, color=INK)
        br_l = text("0.65 nm", size=24, color=INK).next_to(br, LEFT, buff=0.1)
        key = VGroup(VGroup(Dot(color=S, radius=0.1), text("sulfur", size=20, color=MUTED)).arrange(RIGHT, buff=0.1),
                     VGroup(Dot(color=MO, radius=0.12), text("molybdenum", size=20, color=MUTED)).arrange(RIGHT, buff=0.1)
                     ).arrange(RIGHT, buff=0.5).next_to(mol, DOWN, buff=0.35)
        why = VGroup(text("no loose bonds on its surfaces", size=24),
                     text("thickness fixed by the crystal", size=24)).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        why.next_to(key, DOWN, buff=0.4).align_to(mol, LEFT)
        rows = VGroup(
            VGroup(text("silicon nanosheet, 5 nm, N = 4", size=24, color=MUTED), MathTex(rf"\lambda = {lam_si:.1f}\ \text{{nm}}", font_size=38),
                   text(f"shortest gate ≈ {6 * lam_si:.0f} nm", size=24, color=DRAIN)).arrange(DOWN, buff=0.12),
            VGroup(text("MoS₂ layer, 0.65 nm, N = 2", size=24, color=CHANNEL), MathTex(rf"\lambda = {lam_2d:.1f}\ \text{{nm}}", font_size=38, color=CHANNEL),
                   text(f"shortest gate ≈ {6 * lam_2d:.0f} nm", size=24, color=GOOD)).arrange(DOWN, buff=0.12),
        ).arrange(DOWN, buff=0.55).move_to([3.7, 0.2, 0])
        tag = VGroup(model_tag(), text("1 nm oxide; silicon's permittivity for both", size=18, color=MUTED)).arrange(RIGHT, buff=0.2)
        tag.to_corner(DR, buff=0.35)
        self.play(FadeIn(title))
        self.play(LaggedStart(*[GrowFromCenter(a) for a in atoms], lag_ratio=0.02), Create(bonds), run_time=1.6)
        self.play(FadeIn(br), FadeIn(br_l), FadeIn(key))
        self.play(FadeIn(why, shift=UP * 0.1))
        self.play(FadeIn(rows[0]))
        self.play(FadeIn(rows[1]), FadeIn(tag))

    def contacts(self):
        self.slide(say(
            """
            The catch is where the metal touches it: the contacts. Put a metal on a 2D
            semiconductor and states at the interface pin the Fermi level, leaving a barrier
            the electrons must cross to get in, whatever metal you pick. That is the surface-state
            problem Bardeen explained in 1947, the one that killed the first field-effect
            transistors, back again a hundred years on. There's progress: in 2021, contacts made
            of bismuth, a semimetal, cut the contact resistance on MoS2 to near the quantum limit.
            But making that work by the billion is still open.
            """,
            """
            ঝামেলাটা যেখানে metal এইটারে ছোঁয়: contact-এ। একটা 2D semiconductor-এর উপর metal বসান, interface-এর
            state-গুলা Fermi level-রে pin করে দেয়, একটা barrier রেখে যেটা electron-রে পার হয়ে ঢুকতে হয়, যে metal-ই নেন। এইটা
            সেই surface-state সমস্যা যেটা Bardeen 1947-এ ব্যাখ্যা করছিলেন, যেটা প্রথম field-effect transistor-গুলারে মেরে
            ফেলছিল, একশ বছর পরে আবার ফিরে আসছে। অগ্রগতি আছে: 2021-এ bismuth, একটা semimetal, দিয়া বানানো contact MoS2-এ
            contact resistance প্রায় quantum limit-এ নামায়ে আনছে। কিন্তু billion-এর হিসাবে এইটা চালু করা এখনো খোলা প্রশ্ন।
            """,
        ))
        self.clear()
        title = heading("The catch: the contacts")
        metal = Rectangle(width=2.6, height=3.0, fill_color=METAL_C, fill_opacity=0.35, stroke_width=0).move_to([-4.2, 0.5, 0])
        metal_l = text("metal", size=24, color=METAL_C).next_to(metal, UP, buff=0.15)
        ef = DashedLine([-5.5, -0.2, 0], [1.6, -0.2, 0], stroke_color=MUTED, stroke_width=2)
        ef_l = MathTex("E_F", font_size=32, color=MUTED).next_to(ef, RIGHT, buff=0.1)
        x0 = metal.get_right()[0]
        ec = VMobject(stroke_color=ELECTRON, stroke_width=5).set_points_smoothly(
            [[x0, 1.05, 0], [x0 + 0.5, 0.75, 0], [x0 + 1.2, 0.42, 0], [x0 + 2.2, 0.3, 0], [x0 + 4.3, 0.28, 0]])
        ec_l = MathTex("E_C", font_size=32, color=ELECTRON).next_to(ec.get_end(), UP, buff=0.12)
        phi = DoubleArrow([x0 + 0.12, -0.2, 0], [x0 + 0.12, 1.02, 0], buff=0, stroke_color=GATE, stroke_width=4, tip_length=0.14)
        phi_l = MathTex(r"\Phi_B", font_size=36, color=GATE).next_to(phi, RIGHT, buff=0.1).shift(UP * 0.1)
        traps = VGroup(*[Line([x0 - 0.05, y, 0], [x0 + 0.25, y, 0], stroke_color=DRAIN, stroke_width=4) for y in (-0.1, -0.35, -0.6, 0.15)])
        traps_l = text("interface states pin E_F", size=22, color=DRAIN).next_to(traps, RIGHT, buff=0.3).shift(DOWN * 0.15)
        sc_l = text("MoS₂", size=24, color=CHANNEL).move_to([x0 + 2.6, 1.5, 0])
        notes = VGroup(text("The same physics as Bardeen's 1947 surface states (chapter 1),", size=24),
                       text("now at the contacts.", size=24),
                       text("2021: semimetal (bismuth) contacts on MoS₂ cut the contact", size=22, color=GOOD),
                       text("resistance close to the quantum limit (Shen et al., Nature).", size=22, color=GOOD)
                       ).arrange(DOWN, buff=0.12, aligned_edge=LEFT).to_edge(DOWN, buff=0.4).set_x(0)
        self.play(FadeIn(title), FadeIn(metal), FadeIn(metal_l), Create(ef), FadeIn(ef_l))
        self.play(Create(ec), FadeIn(ec_l), FadeIn(sc_l))
        self.play(FadeIn(traps), FadeIn(traps_l))
        self.play(GrowFromCenter(phi), FadeIn(phi_l))
        self.play(FadeIn(notes[:2]))
        self.play(FadeIn(notes[2:]))

    # --- beating 60 mV/decade ----------------------------------------------------------------
    def beat_sixty(self):
        self.slide(say(
            """
            Now the other wall: 60 millivolts per decade. Look at the formula again. There are
            only two ways under it. Make m less than one, which chapter 5 said can't happen with
            ordinary capacitors. Or stop using the Boltzmann tail at all: don't lift electrons
            over a hill. Both have been tried for twenty years.
            """,
            """
            এবার অন্য দেয়ালটা: প্রতি decade-এ 60 millivolt। Formula-টা আবার দেখেন। এর নিচে যাওয়ার মাত্র দুইটা রাস্তা।
            m-রে এক-এর কম করা, যেটা chapter 5 বলছিল সাধারণ capacitor দিয়া হয় না। নয়তো Boltzmann tail ব্যবহারই না করা:
            electron-রে hill-এর উপর দিয়া তোলা বন্ধ। দুইটাই বিশ বছর ধরে চেষ্টা করা হইতেছে।
            """,
        ))
        self.clear()
        title = heading("Can anything beat 60 mV per decade?")
        big = MathTex(r"SS", r"=", r"m", r"\cdot", r"\frac{k_BT}{q}\ln 10", font_size=96).move_to([0, 0.9, 0])
        big[2].set_color(OXIDE_TEXT)
        big[4].set_color(THERMAL)
        a = text("make m < 1:\nnegative capacitance", size=26, color=OXIDE_TEXT).move_to([-3.4, -1.7, 0])
        b = text("don't climb the hill:\ntunnel through it", size=26, color=THERMAL).move_to([3.4, -1.7, 0])
        aa = Arrow(a.get_top(), big[2].get_bottom(), buff=0.15, stroke_color=OXIDE_TEXT, stroke_width=3, tip_length=0.18)
        bb = Arrow(b.get_top(), big[4].get_bottom(), buff=0.15, stroke_color=THERMAL, stroke_width=3, tip_length=0.18)
        self.play(FadeIn(title), Write(big))
        self.play(FadeIn(a), GrowArrow(aa))
        self.play(FadeIn(b), GrowArrow(bb))

    def tfet(self):
        self.slide(say(
            """
            The tunnel FET. In a normal transistor, current is the hot tail of the Boltzmann
            distribution climbing over the hill, and that tail is what sets 60 millivolts. In a
            tunnel FET the source is p-type. Its electrons sit in the valence band, below its top
            edge, and they don't climb; they tunnel sideways into the channel's conduction band
            once the gate pulls it down far enough. The band edge cuts the tail off, so the
            current can switch on faster than 60 millivolts per decade, and it has, in the lab.
            The problem: tunnelling currents are small, far too small so far for real circuits.
            """,
            """
            Tunnel FET। সাধারণ transistor-এ current হইলো Boltzmann distribution-এর গরম tail, যা hill বেয়ে ওঠে, আর
            ওই tail-ই 60 millivolt ঠিক করে। Tunnel FET-এ source p-type। এর electron-গুলা valence band-এ, তার উপরের কিনারার
            নিচে, আর এরা বাইয়া ওঠে না; gate channel-এর conduction band যথেষ্ট নামাইলে এরা পাশাপাশি tunnel করে চলে যায়।
            Band-এর কিনারা tail-টারে কেটে দেয়, তাই current 60 millivolt প্রতি decade-এর চেয়ে দ্রুত on হইতে পারে, আর lab-এ
            হইছেও। সমস্যা: tunnelling current ছোট, এখন পর্যন্ত আসল circuit-এর জন্য অনেক বেশি ছোট।
            """,
        ))
        self.clear()
        title = heading("The tunnel FET: through, not over")
        # Left: a MOSFET's hill and the Boltzmann tail that climbs it.
        hill = VMobject(stroke_color=ELECTRON, stroke_width=5).set_points_smoothly(
            [[-6.2, -0.6, 0], [-5.0, -0.6, 0], [-4.2, 0.5, 0], [-3.4, 0.6, 0], [-2.6, -0.4, 0], [-1.4, -1.4, 0], [-0.9, -1.4, 0]])
        tail = VGroup(*[Dot([-6.0 + 0.16 * (k % 7), -0.52 + 0.12 * (k // 7), 0], radius=0.05, color=ELECTRON,
                            fill_opacity=max(0.15, 1 - 0.13 * (k // 7))) for k in range(56)])
        hot = Dot([-3.7, 0.72, 0], radius=0.07, color=THERMAL)
        hot_a = CurvedArrow([-5.2, 0.2, 0], [-3.9, 0.8, 0], radius=-1.5, stroke_color=THERMAL, tip_length=0.15)
        l1 = VGroup(text("MOSFET: over the hill", size=26, weight="SEMIBOLD"),
                    text("the Boltzmann tail climbs it: ≥ 60 mV/dec", size=20, color=MUTED)).arrange(DOWN, buff=0.1).move_to([-3.6, -2.5, 0])
        # Right: p+ source, gated channel, n+ drain; the band edges.
        def band(points, color):
            return VMobject(stroke_color=color, stroke_width=5).set_points_as_corners([[x, y, 0] for x, y in points])
        ev = band([(0.6, 0.35), (2.3, 0.35), (2.6, -0.4), (4.4, -0.4), (4.7, -1.2), (6.4, -1.2)], HOLE)
        ec = band([(0.6, 1.45), (2.3, 1.45), (2.6, 0.15), (4.4, 0.15), (4.7, -0.1), (6.4, -0.1)], ELECTRON)
        filled = Polygon([0.6, 0.35, 0], [2.3, 0.35, 0], [2.3, -0.9, 0], [0.6, -0.9, 0], fill_color=HOLE, fill_opacity=0.25, stroke_width=0)
        window = Rectangle(width=0.32, height=0.2, fill_color=GATE, fill_opacity=0.6, stroke_width=0).move_to([2.45, 0.25, 0])
        tun = Arrow([1.7, 0.25, 0], [3.4, 0.25, 0], buff=0, stroke_color=GATE, stroke_width=4, tip_length=0.15)
        labels = VGroup(text("p⁺ source", size=20, color=HOLE).move_to([1.45, -1.2, 0]),
                        text("channel", size=20, color=MUTED).move_to([3.5, -0.95, 0]),
                        text("n⁺ drain", size=20, color=ELECTRON).move_to([5.55, 0.25, 0]),
                        MathTex("E_V", font_size=28, color=HOLE).next_to([0.6, 0.35, 0], LEFT, buff=0.1),
                        MathTex("E_C", font_size=28, color=ELECTRON).next_to([0.6, 1.45, 0], LEFT, buff=0.1))
        l2 = VGroup(text("Tunnel FET: through the gap", size=26, weight="SEMIBOLD"),
                    text("the band edge cuts the tail off: < 60 mV/dec possible", size=20, color=MUTED)).arrange(DOWN, buff=0.1).move_to([3.5, -2.5, 0])
        src = source("A. M. Ionescu and H. Riel, Nature 479, 329 (2011); on-currents still far too low")
        self.play(FadeIn(title), Create(hill), FadeIn(tail))
        self.play(Create(hot_a), FadeIn(hot), FadeIn(l1))
        self.play(Create(ev), Create(ec), FadeIn(filled), FadeIn(labels))
        self.play(GrowArrow(tun), FadeIn(window), FadeIn(l2))
        self.play(FadeIn(src))

    def ncfet(self):
        m = phys.body_factor(1.0, -5.0)
        self.slide(say(
            f"""
            The other road: negative capacitance. Remember the divider from chapter 5: the gate's
            voltage is shared between the insulator and the depletion layer, and only one over m
            reaches the channel. With ordinary capacitors m is at least one. But a ferroelectric
            layer in the gate can, over part of its range, behave like a negative capacitor. Then
            m drops below one: the channel moves more than the gate. With m of {m:.1f}, the swing
            is {phys.subthreshold_swing(300, m) * 1e3:.0f} millivolts per decade. It's real physics
            and still argued over: the effect can come with hysteresis, and it isn't in any
            product.
            """,
            f"""
            অন্য রাস্তা: negative capacitance। Chapter 5-এর divider মনে আছে: gate-এর voltage insulator আর depletion layer-এর
            মধ্যে ভাগ হয়, আর channel-এ পৌঁছায় মাত্র এক বাই m। সাধারণ capacitor দিয়া m অন্তত এক। কিন্তু gate-এ একটা
            ferroelectric layer তার range-এর একটা অংশে negative capacitor-এর মতো আচরণ করতে পারে। তখন m এক-এর নিচে নামে:
            channel gate-এর চেয়ে বেশি নড়ে। m {m:.1f} হলে swing প্রতি decade-এ {phys.subthreshold_swing(300, m) * 1e3:.0f} millivolt।
            এইটা আসল physics, আর এখনো তর্ক চলতেছে: effect-টার সাথে hysteresis আসতে পারে, আর কোনো product-এ নাই।
            """,
        ))
        self.clear()
        title = heading("Negative capacitance: m < 1")
        e1 = eq(r"m", r"=", r"1+\frac{C_{dep}}{C_{ins}}", size=60)
        e1[0].set_color(OXIDE_TEXT)
        e2 = text("ordinary insulator, C_ins > 0:   m ≥ 1", size=28, color=MUTED)
        e3 = text("ferroelectric, C_ins < 0 (over part of its range):   m < 1", size=28, color=OXIDE_TEXT)
        e4 = eq(r"C_{ins} = -5\,C_{dep}", r"\;\Rightarrow\;", rf"m = {m:.1f},", r"\quad", rf"SS = {phys.subthreshold_swing(300, m) * 1e3:.0f}\ \text{{mV/dec}}", size=46)
        e4[4].set_color(GOOD)
        col = VGroup(e1, e2, e3, e4).arrange(DOWN, buff=0.5).move_to([0, -0.2, 0])
        src = source("S. Salahuddin and S. Datta, Nano Lett. 8, 405 (2008); debated, not in products")
        self.play(FadeIn(title), Write(col[0]))
        self.play(FadeIn(col[1]))
        self.play(FadeIn(col[2]))
        self.play(Write(col[3]), FadeIn(src))

    # --- the floors --------------------------------------------------------------------------
    def tunnelling_floor(self):
        xover = phys.tunnelling_crossover_nm(E_B)
        self.slide(say(
            f"""
            And there are floors no design gets under. The first: make the channel short enough,
            and electrons stop climbing the barrier and go straight through it, quantum
            tunnelling again, this time from source to drain. Here's the share of electrons that
            gets past a 0.4 electron-volt barrier, over it by heat, and through it by tunnelling,
            against the channel length. They cross at about {xover:.0f} nanometres. Below that the
            barrier isn't a wall any more, and no gate, however tight its grip, can turn the
            transistor off.
            """,
            f"""
            আর এমন floor আছে যার নিচে কোনো design যাইতে পারে না। প্রথমটা: channel যথেষ্ট ছোট করেন, electron barrier বেয়ে
            ওঠা বন্ধ করে সোজা ভেদ করে চলে যায়, আবার সেই quantum tunnelling, এবার source থেকে drain-এ। এই যে 0.4
            electron-volt barrier পার হওয়া electron-এর ভাগ, heat দিয়া উপর দিয়া, আর tunnelling দিয়া ভেতর দিয়া, channel
            length-এর সাথে। দুইটা মিলে প্রায় {xover:.0f} nanometre-এ। এর নিচে barrier আর দেয়াল না, আর gate-এর grip যত শক্তই
            হোক, transistor-রে off করা যায় না।
            """,
        ))
        self.clear()
        title = heading("Floor one: tunnelling straight through")
        # The plot draws log10(share) + 14, so its x axis sits at the bottom.
        ax = Axes(x_range=[2, 10, 1], y_range=[0, 12, 2], x_length=7.6, y_length=4.6, tips=False,
                  axis_config={"stroke_color": MUTED, "stroke_width": 2, "tick_size": 0.05}).move_to([-1.2, -0.4, 0])
        ax.x_axis.add_labels({v: text(str(v), size=18, color=MUTED) for v in range(2, 11, 2)}, font_size=18)
        ax.y_axis.add_labels({v + 14: MathTex(f"10^{{{v}}}", font_size=26, color=MUTED) for v in range(-14, -1, 4)})
        x_l = text("channel length (nm)", size=22, color=MUTED).next_to(ax.x_axis, DOWN, buff=0.45)
        y_l = text("share of electrons that get past", size=22, color=MUTED).next_to(ax, UP, buff=0.2).align_to(ax, LEFT)
        thermal = ax.plot(lambda L: log10(phys.fraction_over_barrier(E_B)) + 14, x_range=[2, 10], color=THERMAL, stroke_width=5)
        tunnel = ax.plot(lambda L: max(0, log10(phys.source_drain_tunnelling(L, E_B)) + 14), x_range=[2.3, 10, 0.05], color=ELECTRON, stroke_width=5)
        t_l = text("over the barrier (heat)", size=22, color=THERMAL).next_to(ax.c2p(10, log10(phys.fraction_over_barrier(E_B)) + 14), UP, buff=0.12).shift(LEFT * 2.2)
        n_l = text("through it (tunnelling)", size=22, color=ELECTRON).next_to(ax.c2p(3.0, log10(phys.source_drain_tunnelling(3.0, E_B)) + 14), RIGHT, buff=0.3)
        xover = phys.tunnelling_crossover_nm(E_B)
        dot = Dot(ax.c2p(xover, log10(phys.fraction_over_barrier(E_B)) + 14), color=GATE, radius=0.1)
        zone = Rectangle(width=ax.c2p(xover, 0)[0] - ax.c2p(2, 0)[0], height=ax.y_length, fill_color=DRAIN, fill_opacity=0.12,
                         stroke_width=0).move_to([(ax.c2p(2, 0)[0] + ax.c2p(xover, 0)[0]) / 2, ax.get_center()[1], 0])
        side = VGroup(display(f"≈ {xover:.0f} nm", size=56, color=GATE),
                      text("below this, the barrier\nisn't a wall any more", size=24, color=INK)).arrange(DOWN, buff=0.2).move_to([4.8, 0.6, 0])
        tag = VGroup(model_tag(), text("WKB; E_b = 0.4 eV, m* = 0.2 m₀", size=18, color=MUTED)).arrange(RIGHT, buff=0.2).to_corner(DR, buff=0.35)
        self.play(FadeIn(title), Create(ax), FadeIn(x_l), FadeIn(y_l), FadeIn(tag))
        self.play(Create(thermal), FadeIn(t_l))
        self.play(Create(tunnel), FadeIn(n_l), run_time=1.6)
        self.play(FadeIn(zone), FadeIn(dot, scale=0.5), FadeIn(side))

    def landauer(self):
        e_min = phys.landauer_limit_J()
        e_now = phys.switching_energy_J(0.1, 0.7)
        self.slide(say(
            f"""
            The second floor is thermodynamics itself. In 1961 Rolf Landauer showed that erasing
            one bit of information must release at least k-B-T times the log of 2 of heat: about
            3 zeptojoules at room temperature. It was measured in 2012. Where are we? Charging a
            tenth of a femtofarad to 0.7 volts, a rough figure for one logic node, takes about
            {e_now * 1e18:.0f} attojoules: some ten thousand times the limit. So there's room left,
            a lot of it. But it's set by the same k-B-T that set the 60 millivolts.
            """,
            f"""
            দ্বিতীয় floor-টা স্বয়ং thermodynamics। 1961-এ Rolf Landauer দেখান যে এক bit information মুছতে অন্তত k-B-T গুণ
            log 2 পরিমাণ heat ছাড়তেই হবে: room temperature-এ প্রায় 3 zeptojoule। 2012-এ এইটা মাপা হইছে। আমরা কোথায়? এক
            femtofarad-এর দশ ভাগের এক ভাগ 0.7 volt-এ charge করতে, মানে একটা logic node-এর মোটামুটি হিসাব, লাগে প্রায়
            {e_now * 1e18:.0f} attojoule: limit-এর প্রায় দশ হাজার গুণ। তাই জায়গা বাকি আছে, অনেক। কিন্তু এইটাও সেই k-B-T দিয়া ঠিক
            হয়, যেটা 60 millivolt ঠিক করছিল।
            """,
        ))
        self.clear()
        title = heading("Floor two: k_BT ln 2")
        ax = NumberLine(x_range=[-21, -15, 1], length=10, color=MUTED, include_numbers=False).move_to([0, -1.6, 0])
        labels = VGroup(*[MathTex(f"10^{{{k}}}", font_size=28, color=MUTED).next_to(ax.n2p(k), DOWN, buff=0.2) for k in range(-21, -14)])
        unit = text("joules per switching event (log scale)", size=20, color=MUTED).next_to(labels, DOWN, buff=0.2)

        def mark(e, color, top, sub, up):
            p = ax.n2p(log10(e))
            line = Line(p, p + UP * up, stroke_color=color, stroke_width=6)
            words = VGroup(text(top, size=26, color=color, weight="SEMIBOLD"), text(sub, size=20, color=MUTED)).arrange(DOWN, buff=0.08)
            return VGroup(line, words.next_to(line, UP, buff=0.12))

        lim = mark(e_min, GOOD, f"k_BT ln 2 = {e_min * 1e21:.1f} zJ", "Landauer 1961; measured 2012", 1.2)
        now = mark(e_now, THERMAL, f"½CV² ≈ {e_now * 1e18:.0f} aJ", "0.1 fF at 0.7 V (illustrative)", 2.4)
        gap = DoubleArrow(ax.n2p(log10(e_min)) + UP * 0.6, ax.n2p(log10(e_now)) + UP * 0.6, buff=0, stroke_color=INK, stroke_width=3, tip_length=0.15)
        gap_l = text(f"≈ {round(e_now / e_min, -2):,.0f}×", size=28, color=INK, weight="SEMIBOLD").next_to(gap, DOWN, buff=0.1)
        self.play(FadeIn(title), Create(ax), FadeIn(labels), FadeIn(unit))
        self.play(FadeIn(lim, shift=UP * 0.1))
        self.play(FadeIn(now, shift=UP * 0.1))
        self.play(GrowFromCenter(gap), FadeIn(gap_l))

    # --- other roads -------------------------------------------------------------------------
    def other_roads(self):
        self.slide(say(
            """
            A few other roads, briefly. Vertical transistors, where the current flows up through
            the wafer instead of across it: IBM and Samsung showed one in 2021. Carbon nanotubes:
            in 2019 a team at MIT built a 16-bit RISC-V processor out of more than fourteen
            thousand nanotube transistors. And monolithic 3D: whole layers of transistors built
            one above another on the same chip. And one for the layout room: in a tunnel FET the
            source and drain are doped opposite ways, so they're no longer interchangeable. You
            couldn't just flip a device any more.
            """,
            """
            আরও কয়েকটা রাস্তা, সংক্ষেপে। Vertical transistor, যেখানে current wafer-এর আড়াআড়ি না গিয়া উপরের দিকে যায়:
            IBM আর Samsung 2021-এ একটা দেখায়। Carbon nanotube: 2019-এ MIT-এর একটা team চৌদ্দ হাজারের বেশি nanotube
            transistor দিয়া একটা 16-bit RISC-V processor বানায়। আর monolithic 3D: একই chip-এ transistor-এর পুরা পুরা layer
            একটার উপর আরেকটা বানানো। আর layout room-এর জন্য একটা কথা: tunnel FET-এ source আর drain উল্টা রকম dope করা, তাই
            এগুলা আর অদলবদল করা যায় না। একটা device আর ইচ্ছামতো উল্টায়ে বসাইতে পারতেন না।
            """,
        ))
        self.clear()
        title = heading("Other roads")
        cards = VGroup(
            self.card_box("Vertical transistors", "current flows up through\nthe wafer, not across it", "IBM and Samsung, VTFET, 2021"),
            self.card_box("Carbon nanotubes", "RV16X-NANO: a 16-bit RISC-V\nprocessor, 14,000+ nanotube\ntransistors", "G. Hills et al., Nature, 2019"),
            self.card_box("Monolithic 3D", "layers of transistors built\none above another, on one chip", "research"),
        ).arrange(RIGHT, buff=0.3).move_to([0, 0.5, 0])
        note = layout_note("In a tunnel FET the source is p⁺ and the drain n⁺, so they aren't interchangeable: "
                           "no more flipping a device or sharing a source/drain both ways.", size=22, width=70)
        note.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(title))
        for c in cards:
            self.play(FadeIn(c, shift=UP * 0.15), run_time=0.7)
        self.play(FadeIn(note, shift=UP * 0.15))

    @staticmethod
    def card_box(head, body, who):
        content = VGroup(text(head, size=26, weight="SEMIBOLD", color=GATE), text(body, size=19),
                         text(who, size=16, color=MUTED)).arrange(DOWN, buff=0.3)
        box = RoundedRectangle(width=max(4.1, content.width + 0.5), height=3.2, corner_radius=0.15, fill_color=PANEL,
                               fill_opacity=1, stroke_color=FAINT, stroke_width=2)
        return VGroup(box, content.move_to(box))

    # --- cliffhanger -------------------------------------------------------------------------
    def cliffhanger(self):
        self.slide(say(
            """
            So the frontier looks like this: a channel one molecule thick, contacts that have to
            beat Bardeen's surface states all over again, switches that try to dodge Boltzmann,
            and below it all, tunnelling and k-B-T. Let's step back and look at the whole
            hundred years at once.
            """,
            """
            তাহলে সীমান্তটা এমন: এক molecule পুরু channel, contact যেগুলারে আবার Bardeen-এর surface state হারাইতে হবে,
            switch যেগুলা Boltzmann-রে এড়াইতে চায়, আর সবকিছুর নিচে tunnelling আর k-B-T। এবার একটু পিছায়ে পুরা একশ বছর
            একসাথে দেখি।
            """,
        ))
        self.clear()
        a = text("Thinner than silicon. Steeper than Boltzmann?", size=42, weight="SEMIBOLD").to_edge(UP, buff=0.8)
        floors = VGroup(text("floor: tunnelling, ~5 nm", size=30, color=ELECTRON),
                        text("floor: k_BT ln 2", size=30, color=THERMAL)).arrange(DOWN, buff=0.35).move_to([0, -0.4, 0])
        shapes = VGroup(*[xsection(k).scale_to_fit_height(0.9) for k in ("planar", "finfet", "nanosheet", "forksheet", "cfet")])
        shapes.arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(DOWN, buff=0.8)
        self.play(FadeIn(a))
        self.play(FadeIn(floors, shift=UP * 0.1))
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.1) for s in shapes], lag_ratio=0.2), run_time=1.5)
        self.wait(1)

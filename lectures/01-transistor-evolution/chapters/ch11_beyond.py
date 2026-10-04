"""Chapter 11 · Beyond silicon, beyond Boltzmann (the 2030s and after: research).

Channels one molecule thick, and the old problem they bring back (the contacts); two examples
of trying to beat 60 mV per decade, one of them now with real current in the lab; an
illustrative tunnelling crossover for very short channels; and how far today's switching energy
is from Landauer's k_BT ln 2. Research now; on imec's roadmap, 2D channels arrive in the 2040s.
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
        self.tunnelling()
        self.landauer()
        self.other_roads()
        self.cliffhanger()

    # --- chapter card ------------------------------------------------------------------------
    def card(self):
        self.slide(say(
            """
            Everything from here on is research, happening now. On imec's roadmap the earliest
            of it, 2D channels, only arrives around the 2040s, and that's a projection. Some of it
            will reach products, most of it won't, and nobody knows which. But the questions are
            the same ones we've been asking all along: how thin can the channel get, and can
            anything beat Boltzmann?
            """,
            """
            এখান থেকে সবকিছু research, যেটা এখনই চলতেছে। imec-এর roadmap-এ এর প্রথমটা, 2D channel, আসে মোটামুটি 2040-এর
            দশকে, আর সেটাও অনুমান। এর কিছু product-এ যাবে, বেশিরভাগই যাবে না, আর কোনটা যাবে কেউ জানে না। কিন্তু প্রশ্নগুলা
            সেই একই, যা আমরা শুরু থেকে করতেছি: channel কত পাতলা হইতে পারে, আর কেউ কি Boltzmann-রে হারাইতে পারবে?
            """,
        ))
        self.card_group = self.open_chapter(11, 2040, 2033, "Beyond silicon", "…and beyond Boltzmann (research now; roadmap 2040s)")

    # --- silicon's last nanometres -----------------------------------------------------------
    def thin_silicon(self):
        r = phys.roughness_mobility_ratio(3, 5)
        self.slide(say(
            f"""
            Thinner channels have helped since chapter 6: in our toy model, lambda goes as the
            square root of the thickness. Today's sheets are 5 nanometres. Why not 3, or 1?
            Because very thin silicon gets hard to use. One reason, from the FinFET chapter: tiny
            changes in thickness scatter the electrons, and theory puts that part of the mobility
            at about the sixth power of the thickness. From 5 to 3 nanometres, that part would
            fall to about {r * 100:.0f} percent. It's one mechanism, not the whole story; in
            measurements several effects compete. But at a few atoms thick, every bump on the
            surface is a big fraction of the whole channel.
            """,
            f"""
            Chapter ছয় থেকে পাতলা channel কাজে লাগছে: আমাদের toy model-এ lambda বাড়ে thickness-এর square root হারে।
            আজকের sheet 5 nanometre। 3 বা 1 না কেন? কারণ খুব পাতলা silicon কাজে লাগানো কঠিন। একটা কারণ, FinFET chapter
            থেকে: thickness-এর ছোট ছোট তারতম্য electron-রে ছিটকায়ে দেয়, আর theory বলে mobility-র ওই অংশটা thickness-এর
            মোটামুটি sixth power হারে চলে। 5 থেকে 3 nanometre-এ ওই অংশটা নেমে যাবে প্রায় {r * 100:.0f} percent-এ। এইটা একটা
            mechanism, পুরা গল্প না; measurement-এ কয়েকটা effect একসাথে কাজ করে। কিন্তু কয়েকটা atom পুরু হলে surface-এর
            প্রত্যেকটা খাঁজ পুরা channel-এর একটা বড় অংশ।
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
        lam = VGroup(MathTex(r"\lambda", r"\propto", r"\sqrt{t_{ch}}", font_size=60),
                     text("(toy model)", size=18, color=MUTED)).arrange(DOWN, buff=0.1).move_to([3.3, 1.6, 0])
        lam[0][2].set_color(CHANNEL)
        mu = VGroup(MathTex(r"\mu_{rough}\propto t^6", font_size=44, color=ELECTRON),
                    text(f"5 → 3 nm: ×{r:.2f}", size=28, color=DRAIN),
                    text("one mechanism, illustrative (chapter 7)", size=18, color=MUTED)).arrange(DOWN, buff=0.25).move_to([3.3, -0.6, 0])
        lines = text("one line = one layer of silicon atoms (0.14 nm)", size=18, color=MUTED).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(title), Write(lam))
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in bars], lag_ratio=0.3), FadeIn(lines), run_time=1.5)
        self.play(FadeIn(mu))

    def two_d(self):
        ratio = (5 / 0.65) ** 0.5
        self.slide(say(
            f"""
            So use a material that is thin by nature. Molybdenum disulfide, MoS2, comes in sheets
            one molecule thick: a layer of molybdenum between two layers of sulfur, 0.65
            nanometres in all. Its surfaces have no loose bonds, and its thickness can't vary,
            because it's set by the crystal. In our toy formula lambda goes as the square root of
            the thickness, so with the same gates and the same oxide, going from 5 nanometres of
            silicon to 0.65 of MoS2 makes lambda about {ratio:.1f} times shorter. That's a toy
            estimate: MoS2's own permittivity and the real shape change it, and real 2D
            transistors still have to show it. imec's roadmap brings 2D channels in after the
            CFET, around its A2 node, in the early 2040s if it holds.
            """,
            f"""
            তাহলে এমন material নেন যেটা স্বভাবতই পাতলা। Molybdenum disulfide, MoS2, আসে এক molecule পুরু sheet-এ:
            দুই layer sulfur-এর মাঝে এক layer molybdenum, সব মিলায়ে 0.65 nanometre। এর surface-এ কোনো খোলা bond নাই, আর
            thickness বদলাইতে পারে না, কারণ crystal-ই সেটা ঠিক করে। আমাদের toy formula-য় lambda চলে thickness-এর square
            root হারে, তাই একই gate আর একই oxide রেখে 5 nanometre silicon থেকে 0.65 nanometre MoS2-এ গেলে lambda প্রায়
            {ratio:.1f} গুণ ছোট হয়। এইটা toy হিসাব: MoS2-এর নিজের permittivity আর আসল আকার এইটা বদলায়, আর আসল 2D transistor-এ
            এইটা এখনো দেখাইতে হবে। imec-এর roadmap 2D channel আনে CFET-এর পরে, ওদের A2 node-এর আশেপাশে, roadmap ঠিক থাকলে
            2040-এর দশকের শুরুতে।
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
            VGroup(text("silicon sheet", size=24, color=MUTED), MathTex(r"t = 5\ \text{nm}", font_size=38)).arrange(DOWN, buff=0.12),
            VGroup(text("MoS₂ layer", size=24, color=CHANNEL), MathTex(r"t = 0.65\ \text{nm}", font_size=38, color=CHANNEL)).arrange(DOWN, buff=0.12),
            VGroup(MathTex(r"\lambda \propto \sqrt{t}", font_size=40),
                   MathTex(rf"\frac{{\lambda_{{Si}}}}{{\lambda_{{MoS_2}}}} \approx \sqrt{{\frac{{5}}{{0.65}}}} \approx {ratio:.1f}", font_size=40, color=GOOD)
                   ).arrange(DOWN, buff=0.25),
        ).arrange(DOWN, buff=0.45).move_to([3.7, 0.3, 0])
        tag = VGroup(model_tag(), text("same gates and oxide; real 2D devices differ", size=18, color=MUTED)).arrange(RIGHT, buff=0.2)
        tag.to_corner(DR, buff=0.35)
        self.play(FadeIn(title))
        self.play(LaggedStart(*[GrowFromCenter(a) for a in atoms], lag_ratio=0.02), Create(bonds), run_time=1.6)
        self.play(FadeIn(br), FadeIn(br_l), FadeIn(key))
        self.play(FadeIn(why, shift=UP * 0.1))
        self.play(FadeIn(rows[:2]))
        self.play(FadeIn(rows[2]), FadeIn(tag))

    def contacts(self):
        self.slide(say(
            """
            The catch is where the metal touches it: the contacts. Put a metal on a 2D
            semiconductor and states at the interface pin the Fermi level, leaving a barrier
            the electrons must cross to get in, almost whatever metal you pick. That is the
            surface-state problem Bardeen explained in 1947, the one that stopped Shockley's
            field-effect experiments, back again eighty years on. There's progress: in 2021, contacts made
            of bismuth, a semimetal, cut the contact resistance on MoS2 to near the quantum limit.
            But making that work by the billion is still open.
            """,
            """
            ঝামেলাটা যেখানে metal এইটারে ছোঁয়: contact-এ। একটা 2D semiconductor-এর উপর metal বসান, interface-এর
            state-গুলা Fermi level-রে pin করে দেয়, একটা barrier রেখে যেটা electron-রে পার হয়ে ঢুকতে হয়, প্রায় যে metal-ই নেন।
            এইটা সেই surface-state সমস্যা যেটা Bardeen 1947-এ ব্যাখ্যা করছিলেন, যেটা Shockley-র field-effect experiment আটকায়ে
            দিছিল, আশি বছর পরে আবার ফিরে আসছে। অগ্রগতি আছে: 2021-এ bismuth, একটা semimetal, দিয়া বানানো contact MoS2-এ
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
            Now the other wall: 60 millivolts per decade, at room temperature. Look at the formula
            again. Here are two ways people try to get under it. Make m less than one, which
            chapter 5 said can't happen with ordinary capacitors alone. Or stop relying on the
            Boltzmann tail: don't lift electrons over a hill at all. They're two examples, not the
            only ideas, and both have been worked on for about twenty years.
            """,
            """
            এবার অন্য দেয়ালটা: room temperature-এ প্রতি decade-এ 60 millivolt। Formula-টা আবার দেখেন। এর নিচে যাওয়ার
            জন্য মানুষ যে দুইটা রাস্তা চেষ্টা করে। m-রে এক-এর কম করা, যেটা chapter 5 বলছিল শুধু সাধারণ capacitor দিয়া হয় না।
            নয়তো Boltzmann tail-এর উপর নির্ভর করাই বন্ধ করা: electron-রে hill-এর উপর দিয়া তোলাই না। এগুলা দুইটা উদাহরণ,
            একমাত্র idea না, আর দুইটা নিয়াই প্রায় বিশ বছর ধরে কাজ চলতেছে।
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
        two = text("two examples; there are other ideas too", size=20, color=MUTED).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(title), Write(big))
        self.play(FadeIn(a), GrowArrow(aa))
        self.play(FadeIn(b), GrowArrow(bb), FadeIn(two))

    def tfet(self):
        self.slide(say(
            """
            The tunnel FET. In a normal transistor, current is the hot tail of the Boltzmann
            distribution climbing over the hill, and that tail is what sets 60 millivolts. In a
            tunnel FET the source is p-type. Its electrons sit in the valence band, below its top
            edge, and they don't climb; they tunnel sideways into the channel's conduction band
            once the gate pulls it down far enough. The band edge cuts the tail off, so the
            current can switch on faster than 60 millivolts per decade, and it has, in the lab.
            The problem has been current: tunnelling currents are usually small. That's moving.
            In 2024 a team at MIT made tiny vertical tunnel transistors from gallium antimonide
            and indium arsenide that switched more steeply than 60 millivolts per decade and still
            carried about 300 microamps per micrometre at 0.3 volts. It's a lab result, not a
            product, but small current isn't a law of nature.
            """,
            """
            Tunnel FET। সাধারণ transistor-এ current হইলো Boltzmann distribution-এর গরম tail, যা hill বেয়ে ওঠে, আর
            ওই tail-ই 60 millivolt ঠিক করে। Tunnel FET-এ source p-type। এর electron-গুলা valence band-এ, তার উপরের কিনারার
            নিচে, আর এরা বাইয়া ওঠে না; gate channel-এর conduction band যথেষ্ট নামাইলে এরা পাশাপাশি tunnel করে চলে যায়।
            Band-এর কিনারা tail-টারে কেটে দেয়, তাই current 60 millivolt প্রতি decade-এর চেয়ে দ্রুত on হইতে পারে, আর lab-এ
            হইছেও। সমস্যা ছিল current: tunnelling current সাধারণত ছোট। এইটা বদলাইতেছে। 2024-এ MIT-এর একটা team gallium
            antimonide আর indium arsenide দিয়া ছোট্ট vertical tunnel transistor বানায়, যেগুলা 60 millivolt প্রতি decade-এর
            চেয়ে খাড়াভাবে switch করছে, আর তবুও 0.3 volt-এ প্রতি micrometre-এ প্রায় 300 microamp current দিছে। এইটা lab-এর
            result, product না, কিন্তু current কম হওয়া প্রকৃতির নিয়ম না।
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
        lab = text("lab, 2024 (MIT): < 60 mV/dec with ~300 µA/µm at 0.3 V", size=18, color=GOOD).next_to(l2, DOWN, buff=0.18)
        src = source("A. M. Ionescu and H. Riel, Nature 479, 329 (2011); Y. Shao et al., Nature Electronics 8, 157 (2025; online 2024)")
        self.play(FadeIn(title), Create(hill), FadeIn(tail))
        self.play(Create(hot_a), FadeIn(hot), FadeIn(l1))
        self.play(Create(ev), Create(ec), FadeIn(filled), FadeIn(labels))
        self.play(GrowArrow(tun), FadeIn(window), FadeIn(l2))
        self.play(FadeIn(lab), FadeIn(src))

    def ncfet(self):
        c_s, c_ox, c_fe = 1.0, 4.0, -3.0  # in units of the semiconductor's capacitance
        m = phys.nc_body_factor(c_s, c_ox, c_fe)
        ss = phys.subthreshold_swing(300, m) * 1e3
        assert phys.nc_stable(c_s, c_ox, c_fe)
        self.slide(say(
            f"""
            The other road: negative capacitance. Remember the divider from chapter 5: the gate's
            voltage is shared between the insulator and the semiconductor, and only one over m
            reaches the channel. With ordinary capacitors m is at least one. But a ferroelectric
            layer can, over part of its range, behave like a negative capacitance. Put it in
            series with the ordinary oxide, and m becomes one plus C-s times one over C-ox plus
            one over C-F-E. If the ferroelectric's capacitance, in size, is smaller than the
            oxide's, m drops below one: the channel moves more than the gate. In this example m
            is {m:.2f}, and the swing is {ss:.0f} millivolts per decade. But it mustn't be too
            small: the whole stack's capacitance has to stay positive, or the device becomes
            unstable, snaps between states and shows hysteresis. That balance holds only over a
            range of bias. It's real physics, still argued over, and not in any product.
            """,
            f"""
            অন্য রাস্তা: negative capacitance। Chapter 5-এর divider মনে আছে: gate-এর voltage insulator আর semiconductor-এর
            মধ্যে ভাগ হয়, আর channel-এ পৌঁছায় মাত্র এক বাই m। সাধারণ capacitor দিয়া m অন্তত এক। কিন্তু একটা ferroelectric
            layer তার range-এর একটা অংশে negative capacitance-এর মতো আচরণ করতে পারে। এইটারে সাধারণ oxide-এর সাথে series-এ
            বসান, তখন m হয় এক যোগ C-s গুণ, এক বাই C-ox যোগ এক বাই C-F-E। Ferroelectric-এর capacitance-এর মান যদি oxide-এর
            চেয়ে ছোট হয়, m এক-এর নিচে নামে: channel gate-এর চেয়ে বেশি নড়ে। এই উদাহরণে m {m:.2f}, আর swing প্রতি decade-এ
            {ss:.0f} millivolt। কিন্তু মানটা বেশি ছোটও হওয়া যাবে না: পুরা stack-এর capacitance positive থাকতে হবে, নইলে device
            অস্থির হয়ে যায়, এক অবস্থা থেকে আরেক অবস্থায় লাফ দেয়, hysteresis দেখায়। এই balance শুধু bias-এর একটা range-এ টিকে।
            এইটা আসল physics, এখনো তর্ক চলতেছে, আর কোনো product-এ নাই।
            """,
        ))
        self.clear()
        title = heading("Negative capacitance: m < 1")
        e1 = MathTex(r"m", r"=", r"1 + C_s\left(\frac{1}{C_{ox}} + \frac{1}{C_{FE}}\right)", font_size=56)
        e1[0].set_color(OXIDE_TEXT)
        e2 = text("ordinary stack, every C > 0:   m > 1", size=26, color=MUTED)
        e3 = VGroup(text("ferroelectric, C_FE < 0 over part of its range, and |C_FE| < C_ox:   m < 1", size=26, color=OXIDE_TEXT))
        e5 = VGroup(text("stable, no hysteresis, only if the whole stack stays positive:", size=22, color=INK),
                    MathTex(r"\frac{1}{C_{FE}} + \frac{1}{C_{ox}} + \frac{1}{C_s} > 0", font_size=36)).arrange(RIGHT, buff=0.3)
        e4 = MathTex(rf"C_{{ox}} = {c_ox:.0f}\,C_s,\ C_{{FE}} = {c_fe:.0f}\,C_s", r"\;\Rightarrow\;", rf"m = {m:.2f},",
                     r"\quad", rf"SS \approx {ss:.0f}\ \text{{mV/dec}}", font_size=42)
        e4[4].set_color(GOOD)
        col = VGroup(e1, e2, e3, e5, e4).arrange(DOWN, buff=0.42).move_to([0, -0.25, 0])
        src = source("S. Salahuddin and S. Datta, Nano Lett. 8, 405 (2008); one bias point, illustrative; not in products")
        self.play(FadeIn(title), Write(col[0]))
        self.play(FadeIn(col[1]))
        self.play(FadeIn(col[2]))
        self.play(FadeIn(col[3]))
        self.play(Write(col[4]), FadeIn(src))

    # --- two scales: tunnelling and Landauer ---------------------------------------------------
    def tunnelling(self):
        xover = phys.tunnelling_crossover_nm(E_B)
        self.slide(say(
            f"""
            Shrinking has other limits too. Make the channel short enough, and electrons can go
            straight through the barrier instead of over it: quantum tunnelling again, this time
            from source to drain. Here's a simple comparison for one assumed barrier, 0.4
            electron-volts high and rectangular, with silicon's electron mass: the factor for
            getting over it by heat, and the factor for getting through it, against the channel
            length. In this toy they cross at about {xover:.0f} nanometres; shorter than that,
            tunnelling would take over the leakage. It's not a universal floor. Another barrier,
            another material, or the real shape of the bands moves the crossing, and a real
            leakage current needs much more than these two factors. But it shows why the gate
            can't shrink forever on grip alone.
            """,
            f"""
            ছোট করার আরও সীমা আছে। Channel যথেষ্ট ছোট করেন, electron barrier-এর উপর দিয়া না গিয়া সোজা ভেদ করে চলে যাইতে পারে:
            আবার সেই quantum tunnelling, এবার source থেকে drain-এ। এই যে একটা সহজ তুলনা, একটা ধরে নেওয়া barrier-এর জন্য, 0.4
            electron-volt উঁচু আর চারকোনা, silicon-এর electron mass সহ: heat দিয়া উপর দিয়া যাওয়ার factor, আর ভেদ করে যাওয়ার
            factor, channel length-এর সাথে। এই toy-তে দুইটা মিলে প্রায় {xover:.0f} nanometre-এ; এর চেয়ে ছোট হলে leakage-এ
            tunnelling-ই বড় হয়ে উঠবে। এইটা সব জায়গার floor না। অন্য barrier, অন্য material, বা band-এর আসল আকার মিলনবিন্দুটা
            সরায়ে দেয়, আর আসল leakage current-এর জন্য এই দুইটা factor-এর চেয়ে অনেক বেশি কিছু লাগে। কিন্তু এইটা দেখায়, কেন
            শুধু grip দিয়া gate চিরকাল ছোট করা যায় না।
            """,
        ))
        self.clear()
        title = heading("Tunnelling straight through: an illustration")
        # The plot draws log10(factor) + 14, so its x axis sits at the bottom.
        ax = Axes(x_range=[2, 10, 1], y_range=[0, 12, 2], x_length=7.6, y_length=4.6, tips=False,
                  axis_config={"stroke_color": MUTED, "stroke_width": 2, "tick_size": 0.05}).move_to([-1.2, -0.4, 0])
        ax.x_axis.add_labels({v: text(str(v), size=18, color=MUTED) for v in range(2, 11, 2)}, font_size=18)
        ax.y_axis.add_labels({v + 14: MathTex(f"10^{{{v}}}", font_size=26, color=MUTED) for v in range(-14, -1, 4)})
        x_l = text("channel length (nm)", size=22, color=MUTED).next_to(ax.x_axis, DOWN, buff=0.45)
        y_l = text("factor for getting past the barrier", size=22, color=MUTED).next_to(ax, UP, buff=0.2).align_to(ax, LEFT)
        thermal = ax.plot(lambda L: log10(phys.fraction_over_barrier(E_B)) + 14, x_range=[2, 10], color=THERMAL, stroke_width=5)
        tunnel = ax.plot(lambda L: max(0, log10(phys.source_drain_tunnelling(L, E_B)) + 14), x_range=[2.3, 10, 0.05], color=ELECTRON, stroke_width=5)
        t_l = text("over the barrier (heat)", size=22, color=THERMAL).next_to(ax.c2p(10, log10(phys.fraction_over_barrier(E_B)) + 14), UP, buff=0.12).shift(LEFT * 2.2)
        n_l = text("through it (tunnelling)", size=22, color=ELECTRON).next_to(ax.c2p(3.0, log10(phys.source_drain_tunnelling(3.0, E_B)) + 14), RIGHT, buff=0.3)
        dot = Dot(ax.c2p(xover, log10(phys.fraction_over_barrier(E_B)) + 14), color=GATE, radius=0.1)
        zone = Rectangle(width=ax.c2p(xover, 0)[0] - ax.c2p(2, 0)[0], height=ax.y_length, fill_color=DRAIN, fill_opacity=0.12,
                         stroke_width=0).move_to([(ax.c2p(2, 0)[0] + ax.c2p(xover, 0)[0]) / 2, ax.get_center()[1], 0])
        side = VGroup(display(f"≈ {xover:.0f} nm", size=56, color=GATE),
                      text("for these assumptions:\nshorter, and tunnelling\nwould dominate the leakage", size=22, color=INK),
                      text("not a universal floor", size=20, color=MUTED)).arrange(DOWN, buff=0.2).move_to([4.8, 0.6, 0])
        tag = VGroup(model_tag(), text("illustrative: WKB, rectangular barrier,\nE_b = 0.4 eV, m* = 0.2 m₀", size=18, color=MUTED)
                     ).arrange(DOWN, buff=0.12).next_to(side, DOWN, buff=0.45)
        self.play(FadeIn(title), Create(ax), FadeIn(x_l), FadeIn(y_l), FadeIn(tag))
        self.play(Create(thermal), FadeIn(t_l))
        self.play(Create(tunnel), FadeIn(n_l), run_time=1.6)
        self.play(FadeIn(zone), FadeIn(dot, scale=0.5), FadeIn(side))

    def landauer(self):
        e_min = phys.landauer_limit_J()
        e_now = phys.cycle_energy_J(0.1, 0.7)
        ratio = round(e_now / e_min, -3)
        self.slide(say(
            f"""
            One more scale to compare with. In 1961 Rolf Landauer showed that erasing one bit of
            information, a step that can't be undone, must release at least k-B-T times the log
            of 2 of heat: about 3 zeptojoules at room temperature. Experiments confirmed it in
            2012. It's a bound on erasing information, not on every switching of a transistor;
            but logic does erase information, and today it spends far more. Charging a tenth of
            a femtofarad to 0.7 volts, a rough figure for one logic node, draws C V squared from
            the supply: about {e_now * 1e18:.0f} attojoules. Half of that is stored on the node,
            half lost in the charging, and the stored half is lost when it discharges. That's
            some {ratio:,.0f} times Landauer's figure. So there's room left, a lot of it. And it's
            the same k-B-T that set the 60 millivolts.
            """,
            f"""
            তুলনার জন্য আরেকটা scale। 1961-এ Rolf Landauer দেখান যে এক bit information মুছতে, মানে এমন একটা ধাপ যেটা আর
            ফেরানো যায় না, অন্তত k-B-T গুণ log 2 পরিমাণ heat ছাড়তেই হবে: room temperature-এ প্রায় 3 zeptojoule। 2012-এ
            experiment এইটা নিশ্চিত করছে। এইটা information মোছার সীমা, transistor-এর প্রত্যেকটা switching-এর না; কিন্তু logic
            information মোছে, আর আজকে তার জন্য অনেক বেশি খরচ করে। এক femtofarad-এর দশ ভাগের এক ভাগ 0.7 volt-এ charge করতে,
            মানে একটা logic node-এর মোটামুটি হিসাব, supply থেকে লাগে C V square: প্রায় {e_now * 1e18:.0f} attojoule। এর অর্ধেক
            node-এ জমা থাকে, অর্ধেক charge করার সময় হারায়, আর জমা অর্ধেকটা discharge-এর সময় হারায়। এইটা Landauer-এর হিসাবের
            প্রায় {ratio:,.0f} গুণ। তাই জায়গা বাকি আছে, অনেক। আর এইটাও সেই k-B-T, যেটা 60 millivolt ঠিক করছিল।
            """,
        ))
        self.clear()
        title = heading("How far from k_BT ln 2?")
        ax = NumberLine(x_range=[-21, -15, 1], length=10, color=MUTED, include_numbers=False).move_to([0, -1.6, 0])
        labels = VGroup(*[MathTex(f"10^{{{k}}}", font_size=28, color=MUTED).next_to(ax.n2p(k), DOWN, buff=0.2) for k in range(-21, -14)])
        unit = text("energy in joules (log scale)", size=20, color=MUTED).next_to(labels, DOWN, buff=0.2)

        def mark(e, color, top, sub, up):
            p = ax.n2p(log10(e))
            line = Line(p, p + UP * up, stroke_color=color, stroke_width=6)
            words = VGroup(text(top, size=26, color=color, weight="SEMIBOLD"), text(sub, size=20, color=MUTED)).arrange(DOWN, buff=0.08)
            return VGroup(line, words.next_to(line, UP, buff=0.12))

        lim = mark(e_min, GOOD, f"k_BT ln 2 = {e_min * 1e21:.1f} zJ", "erasing one bit (Landauer 1961;\nmeasured 2012)", 1.2)
        now = mark(e_now, THERMAL, f"CV² ≈ {e_now * 1e18:.0f} aJ", "drawn from the supply per charge,\n0.1 fF at 0.7 V (illustrative; ½CV² stored)", 2.4)
        gap = DoubleArrow(ax.n2p(log10(e_min)) + UP * 0.6, ax.n2p(log10(e_now)) + UP * 0.6, buff=0, stroke_color=INK, stroke_width=3, tip_length=0.15)
        gap_l = text(f"≈ {ratio:,.0f}×", size=28, color=INK, weight="SEMIBOLD").next_to(gap, DOWN, buff=0.1)
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
            can still mirror or rotate a device, but you can't swap its source and drain.
            """,
            """
            আরও কয়েকটা রাস্তা, সংক্ষেপে। Vertical transistor, যেখানে current wafer-এর আড়াআড়ি না গিয়া উপরের দিকে যায়:
            IBM আর Samsung 2021-এ একটা দেখায়। Carbon nanotube: 2019-এ MIT-এর একটা team চৌদ্দ হাজারের বেশি nanotube
            transistor দিয়া একটা 16-bit RISC-V processor বানায়। আর monolithic 3D: একই chip-এ transistor-এর পুরা পুরা layer
            একটার উপর আরেকটা বানানো। আর layout room-এর জন্য একটা কথা: tunnel FET-এ source আর drain উল্টা রকম dope করা, তাই
            এগুলা আর অদলবদল করা যায় না। Device-রে mirror বা rotate করতে পারবেন, কিন্তু source আর drain অদলবদল করতে
            পারবেন না।
            """,
        ))
        self.clear()
        title = heading("Other roads")
        cards = VGroup(
            self.card_box("Vertical transistors", "current flows up through\nthe wafer, not across it", "IBM and Samsung, VTFET, 2021"),
            self.card_box("Carbon nanotubes", "RV16X-NANO: a 16-bit RISC-V\nprocessor, 14,000+ nanotube\ntransistors", "G. Hills et al., Nature, 2019"),
            self.card_box("Monolithic 3D", "layers of transistors built\none above another, on one chip", "research"),
        ).arrange(RIGHT, buff=0.3).move_to([0, 0.5, 0])
        note = layout_note("In a tunnel FET the source is p⁺ and the drain n⁺, so they can't be swapped. Mirroring or "
                           "rotating a device is still fine, as long as the source stays the source.", size=22, width=70)
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
            So the frontier looks like this: channels a few atoms thick, contacts that have to
            beat Bardeen's surface states all over again, and switches that try to get under 60
            millivolts per decade, some of which already have, in the lab. It's research now; on
            imec's roadmap the first of it arrives in the 2040s. And underneath it all, the same
            k-B-T. Let's step back and look at the whole hundred years at once.
            """,
            """
            তাহলে সীমান্তটা এমন: কয়েকটা atom পুরু channel, contact যেগুলারে আবার Bardeen-এর surface state হারাইতে হবে, আর
            switch যেগুলা 60 millivolt প্রতি decade-এর নিচে যাইতে চায়, যার কয়েকটা lab-এ পারছেও। এইটা এখনকার research;
            imec-এর roadmap-এ এর প্রথমটা আসে 2040-এর দশকে। আর সবকিছুর নিচে সেই একই k-B-T। এবার একটু পিছায়ে পুরা একশ বছর
            একসাথে দেখি।
            """,
        ))
        self.clear()
        a = text("Thinner than silicon. Steeper than Boltzmann?", size=42, weight="SEMIBOLD").to_edge(UP, buff=0.8)
        floors = VGroup(text("research now: channels a few atoms thick, steeper switches", size=28, color=ELECTRON),
                        text("on imec's roadmap: 2D channels, around the 2040s (projection)", size=24, color=MUTED),
                        text("and underneath it all: k_BT", size=28, color=THERMAL)).arrange(DOWN, buff=0.35).move_to([0, -0.2, 0])
        shapes = VGroup(*[xsection(k).scale_to_fit_height(0.9) for k in ("planar", "finfet", "nanosheet", "forksheet", "cfet")])
        shapes.arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(DOWN, buff=0.8)
        self.play(FadeIn(a))
        self.play(FadeIn(floors, shift=UP * 0.1))
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.1) for s in shapes], lag_ratio=0.2), run_time=1.5)
        self.wait(1)

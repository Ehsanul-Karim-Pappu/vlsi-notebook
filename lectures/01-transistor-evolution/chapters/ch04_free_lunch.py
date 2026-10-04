"""Chapter 4 · The free lunch (1965–2003).

Moore's 1965 line, fifty years of chips on it, Dennard's 1974 scaling recipe and why it kept
power density constant, the lambda design rules that let layouts ride the same wave, and the one
row of Dennard's table that couldn't keep shrinking: the voltage.
"""

import sys
from math import log10, sqrt
from pathlib import Path

LECTURE = Path(__file__).resolve().parents[1]
IMAGES = LECTURE / "images"
sys.path[:0] = [str(LECTURE.parents[1]), str(LECTURE)]

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403
from manim_slides import Slide  # noqa: E402

import physics as phys  # noqa: E402
from kit.style import *  # noqa: E402,F403

# Transistor counts (manufacturers' figures).
CHIPS = [
    (1971, 2.3e3, "4004"),
    (1978, 2.9e4, "8086"),
    (1985, 2.75e5, "386"),
    (1993, 3.1e6, "Pentium"),
    (2000, 4.2e7, "Pentium 4"),
    (2006, 2.91e8, "Core 2 Duo"),
    (2020, 1.6e10, "Apple M1"),
    (2023, 9.2e10, "Apple M3 Max"),
    (2024, 2.08e11, "NVIDIA B200"),
]

# Approximate points from Moore's 1965 figure: log2(components per chip).
MOORE_1965 = [(1959, 0), (1962, 3), (1963, 4), (1964, 5), (1965, 6)]


def box(w, h, x, y, color, opacity=1.0):
    return Rectangle(width=w, height=h, fill_color=color, fill_opacity=opacity, stroke_width=0).move_to([x, y, 0])


class Ch04FreeLunch(Chapter, Slide):
    def construct(self):
        self.card()
        self.moore()
        self.fifty_years()
        self.dennard()
        self.free_lunch()
        self.lambda_rules()
        self.cliffhanger()

    # --- card --------------------------------------------------------------------------------
    def card(self):
        self.slide(say(
            """
            For the next forty years, the answer to that question was: everything gets better. This
            is the free lunch.
            """,
            """
            পরের চল্লিশ বছর ওই প্রশ্নের উত্তর ছিল: সবকিছু ভালো হয়। এইটাই free lunch।
            """,
        ))
        self.card_group = self.open_chapter(
            4, 1965, 1959, "The free lunch",
            "Shrink everything, and everything gets better",
        )

    # --- Moore, 1965 -------------------------------------------------------------------------
    def moore(self):
        self.slide(say(
            """
            In 1965 Gordon Moore, then at Fairchild, was asked to predict the future of
            electronics. He had five data points: the number of components on the most
            cost-effective chip, doubling every year. He drew a straight line through them on a log
            scale and carried it ten years forward: sixty-five thousand components by 1975. Notice
            what it's about. Not physics: economics. The number of components at the lowest cost
            per component. In 1975 he slowed it to doubling every two years.
            """,
            """
            1965-এ Gordon Moore, তখন Fairchild-এ, তাঁরে বলা হইল electronics-এর future predict করতে। তাঁর হাতে
            ছিল পাঁচটা data point: সবচেয়ে cost-effective chip-এ component-এর সংখ্যা, প্রতি বছর দ্বিগুণ। Log
            scale-এ এগুলার মধ্য দিয়া একটা সোজা line টেনে দশ বছর সামনে নিলেন: 1975-এর মধ্যে পঁয়ষট্টি হাজার
            component। খেয়াল করেন এইটা কী নিয়া। Physics না: economics। সবচেয়ে কম cost per component-এ কয়টা
            component। 1975-এ তিনি এইটা কমায়ে করলেন প্রতি দুই বছরে দ্বিগুণ।
            """,
        ))
        self.play(FadeOut(self.card_group))
        title = heading("1965: Gordon Moore draws a straight line")
        axes = Axes(x_range=[1959, 1975, 2], y_range=[0, 16, 4], x_length=7.4, y_length=4.6, tips=False,
                    axis_config={"stroke_color": MUTED, "stroke_width": 2, "tick_size": 0.05}).move_to([-1.6, -0.4, 0])
        axes.x_axis.add_labels({y: text(str(y), size=16, color=MUTED) for y in range(1959, 1976, 4)}, font_size=16)
        axes.y_axis.add_labels({k: text(f"{2 ** k:,}", size=16, color=MUTED) for k in (0, 4, 8, 12, 16)}, font_size=16)
        yl = text("components per chip", size=20, color=MUTED).next_to(axes.y_axis, UP, buff=0.15).align_to(axes.y_axis, LEFT)
        pts = VGroup(*[Dot(axes.c2p(y, k), color=GATE, radius=0.08) for y, k in MOORE_1965])
        line = DashedLine(axes.c2p(1959, 0), axes.c2p(1975, 16), stroke_color=GATE, stroke_width=3)
        end = text("~65,000 by 1975", size=24, color=GATE, weight="SEMIBOLD").next_to(axes.c2p(1975, 16), LEFT, buff=0.2).shift(UP * 0.3)
        src = source("After G. E. Moore, Electronics, 19 April 1965 (points approximate)")
        self.play(FadeIn(title), Create(axes), FadeIn(yl), FadeIn(src))
        self.play(LaggedStart(*[FadeIn(p, scale=0.4) for p in pts], lag_ratio=0.25), run_time=1.5)
        self.play(Create(line), run_time=2)
        self.play(FadeIn(end))
        myth = VGroup(
            text("Not a law of physics.", size=28, weight="SEMIBOLD"),
            text("Economics: the component\ncount at the lowest cost\nper component.", size=22, color=MUTED),
            text("1975: revised to ×2\nevery two years.", size=22, color=GATE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.7, 0.2, 0]).to_edge(RIGHT, buff=0.55)
        self.play(FadeIn(myth, shift=LEFT * 0.2))
        self.parts = VGroup(title, axes, yl, pts, line, end, src, myth)

    # --- fifty years -------------------------------------------------------------------------
    def fifty_years(self):
        self.slide(say(
            """
            Now take Moore's 1975 version, doubling every two years, start it from Intel's first
            microprocessor in 1971, two thousand three hundred transistors, and draw it for fifty
            years. Then put real chips on it. The 8086, the 386, the Pentium, the Pentium 4, Core
            2, Apple's M1 and M3 Max. In 2024, NVIDIA's B200 has 208 billion transistors. The line
            drawn in 1975 says 218 billion. A straight line on a log plot, held for fifty years.
            """,
            """
            এবার Moore-এর 1975-এর version নেন, প্রতি দুই বছরে দ্বিগুণ, 1971-এ Intel-এর প্রথম microprocessor থেকে
            শুরু করেন, দুই হাজার তিনশ transistor, আর পঞ্চাশ বছর ধরে টানেন। তারপর আসল chip-গুলা বসান। 8086,
            386, Pentium, Pentium 4, Core 2, Apple-এর M1 আর M3 Max। 2024-এ NVIDIA-র B200-তে 208 billion
            transistor। 1975-এ টানা line বলে 218 billion। Log plot-এ একটা সোজা line, পঞ্চাশ বছর টিকে আছে।
            """,
        ))
        self.play(FadeOut(self.parts))
        title = heading("The line held for fifty years")
        axes = Axes(x_range=[1970, 2026, 10], y_range=[3, 12, 1], x_length=8.6, y_length=5.0, tips=False,
                    axis_config={"stroke_color": MUTED, "stroke_width": 2, "tick_size": 0.05}).move_to([-1.0, -0.45, 0])
        axes.x_axis.add_labels({y: text(str(y), size=16, color=MUTED) for y in range(1970, 2021, 10)}, font_size=16)
        names = {3: "1,000", 6: "1 million", 9: "1 billion", 12: "1 trillion"}
        axes.y_axis.add_labels({k: text(v, size=16, color=MUTED) for k, v in names.items()}, font_size=16)
        line = axes.plot(lambda y: log10(phys.moore_count(y)), x_range=[1971, 2025], color=GATE, stroke_width=3)
        # The label runs along the line, just above it.
        a, b = (axes.c2p(y, log10(phys.moore_count(y))) for y in (1980, 1992))
        ang = np.arctan2(b[1] - a[1], b[0] - a[0])
        line_l = text("Moore 1975: ×2 every 2 years", size=20, color=GATE).rotate(ang)
        line_l.move_to(axes.c2p(1986, log10(phys.moore_count(1986))) + rotate_vector(UP * 0.42, ang))
        self.play(FadeIn(title), Create(axes))
        self.play(Create(line), FadeIn(line_l), run_time=2)
        dots = VGroup()
        for y, n, name in CHIPS:
            d = Dot(axes.c2p(y, log10(n)), color=ELECTRON, radius=0.08)
            where = RIGHT if y >= 2023 else DOWN + RIGHT
            lab = text(name, size=16, color=INK).next_to(d, where, buff=0.08)
            lab.shift({"NVIDIA B200": UP * 0.1, "Apple M3 Max": DOWN * 0.1}.get(name, ORIGIN))
            dots.add(VGroup(d, lab))
        self.play(LaggedStart(*[FadeIn(g, scale=0.5) for g in dots], lag_ratio=0.3), run_time=4)
        pred = phys.moore_count(2024)
        callout = VGroup(
            text("NVIDIA B200, 2024", size=22, color=ELECTRON, weight="SEMIBOLD"),
            text("actual: 208 billion", size=22),
            text(f"1975 line: {pred / 1e9:.0f} billion", size=22, color=GATE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([5.1, -1.2, 0]).to_edge(RIGHT, buff=0.5)
        self.play(Indicate(dots[-1][0], color=ELECTRON, scale_factor=2), FadeIn(callout))
        src = source("Transistor counts: manufacturers' figures")
        self.play(FadeIn(src))
        self.parts = VGroup(title, axes, line, line_l, dots, callout, src)

    # --- Dennard, 1974 -----------------------------------------------------------------------
    def dennard(self):
        title, pic = self.show_figure(say(
            """
            Moore said how many. In 1974 Robert Dennard and his colleagues at IBM said how. That's
            Dennard, much later. The sketch behind him is his other famous invention, patented in
            1968: the one-transistor DRAM cell, a transistor and a capacitor.
            """,
            """
            Moore বলছিলেন কয়টা। 1974-এ IBM-এ Robert Dennard আর তাঁর colleague-রা বললেন কীভাবে। ছবিতে
            Dennard, অনেক পরের। পিছনের sketch-টা তাঁর আরেকটা বিখ্যাত invention, 1968-এর patent: one-transistor
            DRAM cell, একটা transistor আর একটা capacitor।
            """,
        ), "1974: Dennard's recipe",
            figure(IMAGES / "dennard.jpg", 5.6, "Robert Dennard. Photo: Fred Holland, CC BY-SA 3.0").move_to(DOWN * 0.4),
            clear=self.parts)

        self.slide(say(
            """
            His recipe: shrink every dimension by a factor kappa: length, width, oxide thickness. Shrink the voltage by
            the same kappa, and raise the doping by kappa. Then the electric fields inside stay the
            same, so the transistor behaves the same, just smaller. And everything else follows:
            current down by kappa, capacitance down by kappa, so the delay, C V over I, goes down
            by kappa. Power per circuit drops by kappa squared, circuits per area rise by kappa
            squared, and power density stays exactly the same.
            """,
            """
            তাঁর recipe: প্রত্যেকটা dimension একটা factor kappa দিয়া ছোট করেন: length, width, oxide thickness। Voltage-ও একই kappa দিয়া
            কমান, আর doping kappa গুণ বাড়ান। তাহলে ভিতরের electric field একই থাকে, তাই transistor একই রকম আচরণ
            করে, শুধু ছোট। বাকি সব এর থেকেই আসে: current kappa গুণ কমে, capacitance kappa গুণ কমে, তাই delay, মানে C
            V বাই I, kappa গুণ কমে। Circuit প্রতি power kappa square গুণ কমে, area প্রতি circuit kappa square গুণ
            বাড়ে, আর power density একদম same থাকে।
            """,
        ))
        self.play(FadeOut(pic))
        dev = VGroup(
            box(3.6, 1.2, 0, -0.6, PSUB),
            box(0.9, 0.4, -1.2, -0.2, ELECTRON, 0.6),
            box(0.9, 0.4, 1.2, -0.2, ELECTRON, 0.6),
            box(1.6, 0.1, 0, 0.05, OXIDE_TEXT),
            box(1.6, 0.4, 0, 0.3, GATE),
        ).move_to([-4.0, 0.6, 0])
        k_lbl = MathTex(r"\times\frac{1}{\kappa}", font_size=44, color=GATE).next_to(dev, DOWN, buff=0.4)
        rows = [
            ("dimensions L, W, t_ox", r"1/\kappa"),
            ("doping N_A", r"\kappa"),
            ("voltage V", r"1/\kappa"),
            ("current I", r"1/\kappa"),
            ("capacitance C", r"1/\kappa"),
            ("delay CV/I", r"1/\kappa"),
            ("power per circuit VI", r"1/\kappa^2"),
            ("circuits per area", r"\kappa^2"),
            ("power density", r"1"),
        ]
        table = VGroup()
        for name, f in rows:
            r = VGroup(text(name, size=24), MathTex(f, font_size=34, color=GATE))
            table.add(r)
        for r in table:
            r[1].next_to(r[0], RIGHT, buff=0.4)
        table.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([2.6, -0.2, 0])
        for r in table:
            r[1].set_x(5.4)
        table[-1][1].set_color(GOOD)
        src = source("R. H. Dennard et al., IEEE J. Solid-State Circuits SC-9(5), 256 (1974)")
        self.play(FadeIn(dev), FadeIn(src))
        self.play(dev.animate.scale(1 / 1.6), FadeIn(k_lbl), run_time=1.5)
        for r in table[:3]:
            self.play(FadeIn(r, shift=LEFT * 0.15), run_time=0.5)
        fields = text("so the electric fields\nstay the same", size=22, color=MUTED).next_to(k_lbl, DOWN, buff=0.4)
        self.play(FadeIn(fields))
        for r in table[3:]:
            self.play(FadeIn(r, shift=LEFT * 0.15), run_time=0.5)
        self.play(Indicate(table[-1], color=GOOD))
        self.table = table
        self.parts = VGroup(title, dev, k_lbl, src, fields)

    # --- the free lunch ----------------------------------------------------------------------
    def free_lunch(self):
        self.slide(say(
            """
            Here's what that meant, generation after generation. Take kappa as the square root of
            two. Every new node, the same area holds twice the transistors, each switching about
            forty percent faster, and the chip runs exactly as hot as before. Check it with the
            switching power: C down by kappa, V squared down by kappa squared, f up by kappa. Per
            circuit that's one over kappa squared; times kappa squared more circuits: constant. For
            thirty years, everything got better and nothing got worse. A free lunch.
            """,
            """
            Generation-এর পর generation এর মানে কী দাঁড়াইল দেখেন। Kappa ধরেন root two। প্রতিটা নতুন node-এ, একই
            area-তে দ্বিগুণ transistor, প্রত্যেকটা প্রায় চল্লিশ percent দ্রুত switch করে, আর chip ঠিক আগের মতোই
            গরম হয়। Switching power দিয়া check করেন: C কমে kappa গুণ, V square কমে kappa square গুণ, f বাড়ে kappa
            গুণ। Circuit প্রতি এইটা এক বাই kappa square; kappa square গুণ বেশি circuit দিয়া গুণ করলে: constant।
            তিরিশ বছর ধরে সবকিছু ভালো হইছে, কিছুই খারাপ হয় নাই। একটা free lunch।
            """,
        ))
        self.table_copy = self.table.copy()
        self.play(FadeOut(self.parts), FadeOut(self.table))
        title = heading("Twice the transistors, faster, same heat")
        tile = Square(3.2, stroke_color=MUTED, stroke_width=2).move_to([-4.4, 0.5, 0])

        def fill(n):
            cols = int(np.ceil(np.sqrt(n)))
            rows = int(np.ceil(n / cols))
            s = 3.0 / max(cols, rows)
            g = VGroup()
            for i in range(n):
                r, c = divmod(i, cols)
                g.add(Square(s * 0.7, stroke_width=0, fill_color=ELECTRON, fill_opacity=0.8).move_to(
                    tile.get_center() + np.array([(c - (cols - 1) / 2) * s, ((rows - 1) / 2 - r) * s, 0])))
            return g

        cells = fill(1)
        gen = text("node 1", size=24, color=MUTED).next_to(tile, DOWN, buff=0.2)
        heat = VGroup(Rectangle(width=0.35, height=2.6, stroke_color=MUTED, stroke_width=2),
                      box(0.35, 1.0, 0, -0.8, THERMAL)).move_to([-1.6, 0.9, 0])
        heat[1].align_to(heat[0], DOWN)
        heat_l = text("heat per mm²", size=20, color=THERMAL).next_to(heat, DOWN, buff=0.2)
        speed = DecimalNumber(1.0, num_decimal_places=2, font_size=44, color=GOOD)
        speed_g = VGroup(text("speed", size=22, color=MUTED), VGroup(MathTex(r"\times", font_size=40, color=GOOD), speed).arrange(RIGHT, buff=0.08)).arrange(DOWN, buff=0.1).move_to([-1.6, -1.6, 0])
        self.play(FadeIn(title), Create(tile), FadeIn(cells), FadeIn(gen), FadeIn(heat), FadeIn(heat_l), FadeIn(speed_g))
        for i, n in enumerate((2, 4, 8)):
            new = fill(n)
            self.play(Transform(cells, new), Transform(gen, text(f"node {i + 2}", size=24, color=MUTED).move_to(gen)),
                      speed.animate.set_value(sqrt(2) ** (i + 1)), run_time=1.2)
        p = eq(r"P_{circuit}", r"\propto", r"C", r"V^2", r"f", r"\to", r"\frac{1}{\kappa}\cdot\frac{1}{\kappa^2}\cdot\kappa", r"=", r"\frac{1}{\kappa^2}", size=40)
        p[3].set_color(THERMAL)
        d = eq(r"\frac{P}{\text{area}}", r"\propto", r"\frac{1}{\kappa^2}\cdot\kappa^2", r"=", r"1", size=40)
        d[4].set_color(GOOD)
        col = VGroup(p, d).arrange(DOWN, buff=0.5).move_to([3.3, 0.2, 0])
        self.play(Write(p))
        self.play(Write(d))
        self.parts = VGroup(title, tile, cells, gen, heat, heat_l, speed_g, col)

    # --- lambda rules ------------------------------------------------------------------------
    def lambda_rules(self):
        title, pic = self.show_figure(say(
            """
            And layout? This is a layout drawing of Intel's 4004 from 1971, the first
            microprocessor: about 2,300 transistors, drawn by hand at many times the chip's real
            size. Every rectangle on it is the kind of thing you draw in your layout tool today.
            """,
            """
            আর layout? এইটা 1971-এর Intel 4004-এর একটা layout drawing, প্রথম microprocessor: প্রায় 2,300
            transistor, chip-এর আসল size-এর অনেক গুণ বড় করে হাতে আঁকা। এর প্রত্যেকটা rectangle আজকে আপনারা
            layout tool-এ যা আঁকেন, সেই জিনিসই।
            """,
        ), "1971: layout, drawn by hand",
            figure(IMAGES / "intel4004_layout_1971.jpg", 5.6,
                   "Intel 4004 layout drawing, 1971. Photo: Flickr user stiefkind, CC0").move_to(DOWN * 0.4),
            clear=self.parts)
        self.parts = Group(title, pic)

        self.slide(say(
            """
            Layout rode the same wave. In 1980 Carver Mead and Lynn Conway wrote design rules in
            units of a single length, lambda: poly two lambda wide, spaced two lambda, and so on.
            Draw your inverter on the lambda grid once, and when the next node arrives, shrink
            lambda and the whole layout scales with it. That only works because Dennard scaling
            shrank everything together. When scaling stopped being uniform, the rules stopped being
            simple multiples of lambda, and the DRC decks you work with today grew into what they
            are.
            """,
            """
            Layout-ও একই ঢেউয়ে চড়ছিল। 1980-এ Carver Mead আর Lynn Conway design rule লিখলেন একটা মাত্র length-এর
            হিসাবে, lambda: poly দুই lambda চওড়া, দুই lambda ফাঁক, এরকম। আপনার inverter একবার lambda grid-এ
            আঁকেন, পরের node আসলে lambda ছোট করেন, পুরা layout সেটার সাথে scale হয়ে যায়। এইটা কাজ করে শুধু কারণ
            Dennard scaling সবকিছু একসাথে ছোট করত। Scaling যখন আর uniform থাকল না, rule-গুলাও আর lambda-র সরল
            গুণিতক থাকল না, আর আজকে যে DRC deck নিয়া আপনারা কাজ করেন সেটা আজকের চেহারায় পৌঁছাইল।
            """,
        ))
        self.play(FadeOut(self.parts))
        title = heading("Layout rode the same wave: λ rules")
        lam = ValueTracker(0.22)
        origin = np.array([-5.6, -2.6, 0])

        def grid_and_layout():
            l = lam.get_value()
            g = VGroup()
            for i in range(0, 25):
                g.add(Line(origin + [i * l, 0, 0], origin + [i * l, 24 * l, 0], stroke_color=FAINT, stroke_width=1))
                g.add(Line(origin + [0, i * l, 0], origin + [24 * l, i * l, 0], stroke_color=FAINT, stroke_width=1))

            def r(x, y, w, h, color, op=0.85):
                return Rectangle(width=w * l, height=h * l, fill_color=color, fill_opacity=op, stroke_width=0).move_to(origin + [(x + w / 2) * l, (y + h / 2) * l, 0])

            lay = VGroup(
                r(2, 14, 20, 8, NWELL, 0.5),
                r(6, 16, 12, 4, HOLE, 0.7), r(6, 3, 12, 4, ELECTRON, 0.7),
                r(11, 1, 2, 22, GATE, 0.9),
                r(3, 21, 18, 2, METAL, 0.6), r(3, 0, 18, 2, METAL, 0.6),
                r(16, 5, 2, 13, METAL, 0.8),
            )
            return VGroup(g, lay)

        art = always_redraw(grid_and_layout)
        legend = VGroup(
            text("poly width ≥ 2λ", size=22, color=GATE),
            text("poly spacing ≥ 2λ", size=22, color=GATE),
            text("diffusion width ≥ 3λ", size=22, color=ELECTRON),
            text("metal width ≥ 3λ", size=22, color=METAL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.4, 1.4, 0])
        self.play(FadeIn(title), FadeIn(art), FadeIn(legend))
        shrink = text("next node: shrink λ,\nthe whole layout follows", size=24, color=INK).move_to([3.0, -0.3, 0])
        self.play(FadeIn(shrink))
        self.play(lam.animate.set_value(0.155), run_time=2)
        self.play(lam.animate.set_value(0.11), run_time=2)
        note = layout_note("When scaling stopped being uniform, rules stopped being multiples of λ: hence today's DRC decks.", size=22, width=44)
        note.move_to([3.0, -2.1, 0])
        src = source("C. Mead & L. Conway, Introduction to VLSI Systems (1980); widths as in the MOSIS SCMOS rules")
        self.play(FadeIn(note, shift=UP * 0.2), FadeIn(src))
        self.parts = VGroup(title, art, legend, shrink, note, src)

    # --- cliffhanger -------------------------------------------------------------------------
    def cliffhanger(self):
        self.slide(say(
            """
            But look at Dennard's table again. Every row could keep shrinking for as long as we
            could draw smaller, except one. The voltage. To shrink the voltage, you have to shrink
            the threshold voltage too, and the threshold voltage is tied to something no amount of
            lithography can change. That's the next chapter.
            """,
            """
            কিন্তু Dennard-এর table-টা আবার দেখেন। যতদিন আরও ছোট আঁকা যায়, প্রত্যেকটা row ছোট হইতে পারত, একটা
            বাদে। Voltage। Voltage কমাইতে হলে threshold voltage-ও কমাইতে হয়, আর threshold voltage বাঁধা আছে এমন
            একটা জিনিসের সাথে যেটা কোনো lithography দিয়াই বদলানো যায় না। সেইটাই পরের chapter।
            """,
        ))
        self.table = self.table_copy.move_to([0, -0.2, 0])
        self.play(FadeOut(self.parts), FadeIn(self.table))
        v_row = self.table[2]
        hl = SurroundingRectangle(v_row, color=DRAIN, buff=0.12, corner_radius=0.08)
        q = text("One row couldn't keep shrinking forever.", size=36, weight="SEMIBOLD", color=DRAIN)
        q.to_edge(UP, buff=0.5)
        self.play(FadeIn(q))
        self.play(Create(hl), *[r.animate.set_opacity(0.3) for i, r in enumerate(self.table) if i != 2])

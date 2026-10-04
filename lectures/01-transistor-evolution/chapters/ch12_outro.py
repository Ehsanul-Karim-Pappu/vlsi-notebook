"""Chapter 12 · Outro: turning it off.

The hundred years in one table, the grip chapter by chapter, and the one number that hasn't
moved since the first transistor.
"""

import sys
from pathlib import Path

LECTURE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(LECTURE.parents[1]), str(LECTURE)]

from manim import *  # noqa: E402,F403
from manim_slides import Slide  # noqa: E402

import physics as phys  # noqa: E402
from kit.motifs import Barrier, xsection  # noqa: E402
from kit.style import *  # noqa: E402,F403

# (era, who took control away from the gate, the fix)
FIGHT = [
    ("1925–47", "surface states swallow the gate's field", "none: the idea fails"),
    ("1947–59", "go around it", "the bipolar transistor"),
    ("1959–", "surface states, tamed by glass", "thermal oxide: the MOSFET, then CMOS"),
    ("2000s", "tunnelling through a five-atom oxide", "high-k and a metal gate"),
    ("2005–", "Boltzmann: 60 mV per decade", "none: the supply voltage stops falling"),
    ("2011–", "the drain reaches the barrier", "wrap the gate: fin, sheet, fork, CFET"),
    ("2030s–", "silicon too thin to work", "2D channels? steep switches?"),
]
# (cross-section, name, channel thickness nm, gates N)
GRIP = [("planar", "planar", 15, 1), ("finfet", "FinFET", 6, 3), ("nanosheet", "nanosheet", 5, 4),
        ("forksheet", "forksheet", 5, 3), ("cfet", "CFET", 5, 4), (None, "2D layer", 0.65, 2)]


class Ch12Outro(Chapter, Slide):
    def construct(self):
        self.card()
        self.table()
        self.grip()
        self.closing()
        self.thanks()

    def card(self):
        self.slide(say(
            """
            Let's step back and look at the whole hundred years at once.
            """,
            """
            চলেন, একটু পিছায়ে পুরা একশ বছর একসাথে দেখি।
            """,
        ))
        self.card_group = self.open_chapter(12, 2026, 2040, "Turning it off", "A hundred years, one fight")

    def table(self):
        self.slide(say(
            """
            Here's every chapter in one table. Each row is the same fight. Something takes control
            of the barrier away from the gate: surface states, then the oxide letting electrons
            tunnel, then Boltzmann, then the drain, and next, silicon itself. And each fix was a
            new way to hold the barrier: glass, a better insulator, more gate wrapped around a
            thinner channel. Twice there was no fix at all, and the industry went around the
            problem instead.
            """,
            """
            এই যে প্রত্যেকটা chapter এক table-এ। প্রত্যেকটা row একই লড়াই। কিছু একটা gate-এর হাত থেকে barrier-এর control
            কেড়ে নেয়: surface state, তারপর oxide দিয়া electron-এর tunnel করা, তারপর Boltzmann, তারপর drain, আর এরপর silicon
            নিজেই। আর প্রত্যেকটা fix ছিল barrier ধরে রাখার নতুন একটা উপায়: glass, আরও ভালো insulator, পাতলা channel-এর
            চারপাশে আরও gate। দুইবার কোনো fix-ই ছিল না, আর industry সমস্যাটার পাশ কাটায়ে গেছে।
            """,
        ))
        self.play(FadeOut(self.card_group))
        title = heading("The same fight, every time")
        head = VGroup(text("when", size=20, color=MUTED), text("who took control from the gate", size=20, color=MUTED),
                      text("the fix", size=20, color=MUTED))
        rows = VGroup(*[VGroup(text(era, size=22, color=GATE, weight="SEMIBOLD"), text(thief, size=22, color=DRAIN),
                               text(fix, size=22, color=GOOD if not fix.startswith("none") else MUTED))
                        for era, thief, fix in FIGHT])
        widths = [max(r[k].width for r in rows) for k in range(3)]
        total = sum(widths) + 2 * 0.5
        xs = [-total / 2, -total / 2 + widths[0] + 0.5, -total / 2 + widths[0] + widths[1] + 1.0]
        for i, r in enumerate(rows):
            for m, x in zip(r, xs):
                m.move_to([x, 2.05 - 0.68 * (i + 1), 0], aligned_edge=LEFT)
        for m, x in zip(head, xs):
            m.move_to([x, 2.05, 0], aligned_edge=LEFT)
        rule = Line([xs[0], 1.75, 0], [xs[0] + total, 1.75, 0], stroke_color=FAINT, stroke_width=2)
        self.play(FadeIn(title), FadeIn(head), Create(rule))
        for r in rows:
            self.play(FadeIn(r, shift=RIGHT * 0.15), run_time=0.6)

    def grip(self):
        self.slide(say(
            """
            And here's the grip, architecture by architecture: the natural length lambda, and the
            shortest gate it allows, about six lambda. Planar, about 40 nanometres. The FinFET,
            15. The nanosheet, 12. The forksheet gives a little back, on purpose, for area. The
            CFET holds at 12, and stacks. And a 2D layer would take it to about 6, close to the
            point where electrons tunnel straight through. Every bar is the same equation.
            """,
            """
            আর এই যে grip, architecture ধরে ধরে: natural length lambda, আর এইটা যতটা ছোট gate allow করে, প্রায় ছয় lambda।
            Planar, প্রায় 40 nanometre। FinFET, 15। Nanosheet, 12। Forksheet ইচ্ছা করে একটু ফেরত দেয়, area-র জন্য। CFET 12-তে
            থাকে, আর stack করে। আর একটা 2D layer এইটারে নিয়া যাবে প্রায় 6-এ, সেই জায়গার কাছে যেখানে electron সোজা tunnel করে
            চলে যায়। প্রত্যেকটা bar একই equation।
            """,
        ))
        self.clear()
        title = heading("The grip, chapter by chapter")
        unit = 3.0 / 40
        cols = VGroup()
        for kind, name, t, n in GRIP:
            lam = phys.natural_length_nm(t, 1, n)
            if kind:
                pic = xsection(kind).scale_to_fit_height(1.0)
            else:
                pic = VGroup(Rectangle(width=1.4, height=0.3, fill_color=GATE, fill_opacity=1, stroke_width=0),
                             Rectangle(width=1.4, height=0.06, fill_color="#7FD8E4", fill_opacity=1, stroke_width=0),
                             Rectangle(width=1.4, height=0.3, fill_color=GATE, fill_opacity=1, stroke_width=0)).arrange(DOWN, buff=0.04)
                pic.add(Rectangle(width=1.8, height=0.3, fill_color=SUBSTRATE, fill_opacity=1, stroke_width=0).next_to(pic, DOWN, buff=0))
                pic.scale_to_fit_height(1.0)
            bar = Rectangle(width=0.7, height=6 * lam * unit, fill_color=DRAIN, fill_opacity=0.75, stroke_width=0)
            num = text(f"{6 * lam:.0f} nm", size=22, color=DRAIN)
            lbl = VGroup(text(name, size=22, color=INK), MathTex(rf"\lambda = {lam:.1f}", font_size=30, color=GATE)).arrange(DOWN, buff=0.08)
            cols.add(VGroup(pic, lbl, bar, num))
        x0 = -5.6
        for i, c in enumerate(cols):
            x = x0 + 1.95 * i
            c[0].move_to([x, 2.0, 0])
            c[1].next_to(c[0], DOWN, buff=0.2)
            c[2].move_to([x, -3.3 + c[2].height / 2, 0])
            c[3].next_to(c[2], UP, buff=0.08)
        floor = DashedLine([-6.4, -3.3 + 5.3 * unit, 0], [6.6, -3.3 + 5.3 * unit, 0], stroke_color=ELECTRON, stroke_width=2)
        floor_l = text("tunnelling\nfloor, ~5 nm", size=18, color=ELECTRON).next_to(floor, UP, buff=0.08).align_to(floor, RIGHT)
        bar_l = text("shortest gate ≈ 6λ", size=20, color=DRAIN).move_to([5.7, -0.6, 0])
        tag = text("model: 1 nm oxide (EOT)", size=16, color=MUTED).move_to([5.7, -0.95, 0])
        self.play(FadeIn(title), FadeIn(bar_l), FadeIn(tag))
        for c in cols:
            self.play(FadeIn(c[0]), FadeIn(c[1]), GrowFromEdge(c[2], DOWN), FadeIn(c[3]), run_time=0.7)
        self.play(Create(floor), FadeIn(floor_l))

    def closing(self):
        self.slide(say(
            """
            So here's what I'd like you to take away. Every reinvention of the transistor in this
            story, the oxide, CMOS, high-k, the fin, the sheet, the fork, the stack, was never
            about turning it on better. It was always about turning it off: holding that hill up
            when the gate says off.
            """,
            """
            তো যেটা আপনাদের সাথে নিয়া যাইতে বলবো: এই গল্পে transistor-এর প্রত্যেকবার নতুন করে বানানো, oxide, CMOS,
            high-k, fin, sheet, fork, stack, কখনোই আরও ভালো on করার জন্য ছিল না। সবসময় ছিল off করার জন্য: gate যখন off বলে,
            তখন ওই hill-টারে ধরে রাখা।
            """,
        ))
        self.clear()
        a = text("It was never about turning it on.", size=44, weight="SEMIBOLD").to_edge(UP, buff=0.6)
        b = text("It was always about turning it off.", size=44, weight="SEMIBOLD", color=GATE).next_to(a, DOWN, buff=0.25)
        bt, dt = ValueTracker(0.08), ValueTracker(0.25)
        bar = Barrier(bt, dt, n=120, origin=(0.0, -1.7), scale=6.0, seed=5)
        self.play(FadeIn(a))
        self.play(FadeIn(bar))
        bar.start()
        self.wait(1.5)
        self.play(FadeIn(b), bt.animate.set_value(0.32), run_time=3)
        self.wait(1.5)
        self.bar, self.closing_text = bar, VGroup(a, b)

        self.slide(say(
            """
            And through all of it, one number never moved. Raise the gate 60 millivolts and the
            current goes up ten times: k-B-T over q, times the log of ten. It was in the bipolar
            transistor in 1948, and it's in the nanosheets of today's newest chips. Every architecture since
            has been a way of living with it. Whoever finally beats it writes the next chapter.
            """,
            """
            আর এর পুরাটা জুড়ে একটা সংখ্যা কখনো নড়ে নাই। Gate 60 millivolt বাড়ান, current দশ গুণ: k-B-T বাই q, গুণ log
            দশ। এইটা 1948-এর bipolar transistor-এ ছিল, আর আজকের সবচেয়ে নতুন chip-এর nanosheet-এও আছে। এর পরের প্রত্যেকটা architecture
            এইটার সাথে বাঁচার একটা উপায়। যে শেষ পর্যন্ত এইটারে হারাবে, পরের chapter সে-ই লিখবে।
            """,
        ), loop=False)
        self.bar.stop()
        self.play(FadeOut(self.bar), FadeOut(self.closing_text))
        f = MathTex(r"\frac{k_BT}{q}\,\ln 10", r"\;=\;", rf"{phys.subthreshold_swing(300) * 1e3:.1f}\ \text{{mV per decade}}", font_size=84)
        f[0].set_color(THERMAL)
        f[2].set_color(GATE)
        f.move_to([0, 0.7, 0])
        sub = text("at 300 K: in the bipolar transistor of 1948, and in today's nanosheets", size=26, color=MUTED)
        sub.next_to(f, DOWN, buff=0.5)
        last = text("Whoever beats it writes the next chapter.", size=36, weight="SEMIBOLD").to_edge(DOWN, buff=1.0)
        self.play(Write(f), run_time=2)
        self.play(FadeIn(sub))
        self.play(FadeIn(last, shift=UP * 0.15))

    def thanks(self):
        self.slide(say(
            """
            Thank you. I'm happy to take questions. Every date and number in the talk has a
            source in the references file that comes with the slides.
            """,
            """
            ধন্যবাদ। প্রশ্ন থাকলে করেন। Talk-এর প্রত্যেকটা date আর সংখ্যার source slide-এর সাথের references file-এ আছে।
            """,
        ))
        self.clear()
        t = display("Thank you", size=96)
        q = text("Questions?", size=40, color=GATE)
        name = text("Lecture 1 · The Switch That Wouldn't Turn Off", size=26, color=MUTED)
        VGroup(name, t, q).arrange(DOWN, buff=0.45).move_to([0, 0.3, 0])
        self.play(FadeIn(name), FadeIn(t, shift=UP * 0.2))
        self.play(FadeIn(q))

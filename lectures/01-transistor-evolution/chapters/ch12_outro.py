"""Chapter 12 · Outro: turning it off.

The hundred years in one table, the grip in the toy model, and the ideal thermal factor that a
conventional transistor still can't beat at room temperature: the off state as the thread, with
on-current and buildable cells alongside it.
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

# (era, the problem, what answered it)
ROWS = [
    ("1925–47", "surface states block the gate's field", "not yet: no usable field-effect switch"),
    ("1947–59", "a working solid-state amplifier", "the bipolar transistor"),
    ("1959–", "surface states, again", "thermal oxide: the MOSFET, then CMOS"),
    ("2000s", "tunnelling through a five-atom oxide", "high-k and a metal gate"),
    ("2005–", "power, and 60 mV per decade at 300 K", "none: the supply voltage stops falling"),
    ("2011–", "the drain reaches the barrier", "more gate around the channel: fin, sheet"),
    ("~2030s", "the space between n and p", "forksheet, CFET (projected)"),
    ("research", "silicon too thin to use well", "2D channels? steep switches?"),
]
# (cross-section, name, channel thickness nm, gates N: one value, or the toy model's range)
GRIP = [("planar", "planar", 15, (1,)), ("finfet", "FinFET", 6, (3,)), ("nanosheet", "nanosheet", 5, (4, 2))]


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
        self.card_group = self.open_chapter(12, 2026, 2040, "Turning it off", "A hundred years, one thread")

    def table(self):
        self.slide(say(
            """
            Here's every chapter in one table. A thread runs through it: keep the gate in control
            of the barrier, so the switch turns off, while it still gives enough current and fits
            in a cell you can build. First, surface states blocked the field, and there was no
            usable field-effect switch; the bipolar transistor amplified another way. Glass tamed
            the surface and gave us the MOSFET and CMOS. Then the oxide let electrons tunnel, and
            high-k fixed it. Power, and Boltzmann's 60 millivolts, stopped the supply voltage
            falling. The drain reached the barrier, and the gate wrapped around: fin, sheet. The
            forksheet and the CFET are about packing n and p closer. And next, silicon getting
            too thin to use well. Not every row is the same problem, but the off state runs
            through most of them.
            """,
            """
            এই যে প্রত্যেকটা chapter এক table-এ। এর ভিতর দিয়া একটা সুতা গেছে: barrier-এর control gate-এর হাতে রাখা, যাতে
            switch off হয়, আর একই সাথে যথেষ্ট current দেয় আর এমন cell-এ আঁটে যেটা বানানো যায়। প্রথমে surface state field-রে
            আটকায়ে দিছিল, আর কাজের কোনো field-effect switch ছিল না; bipolar transistor অন্য উপায়ে amplify করছে। Glass surface-রে
            বশ করছে, আর আমাদের MOSFET আর CMOS দিছে। তারপর oxide দিয়া electron tunnel করতে লাগলো, আর high-k সেটা ঠিক করছে।
            Power আর Boltzmann-এর 60 millivolt supply voltage কমা থামায়ে দিছে। Drain barrier পর্যন্ত পৌঁছাইছে, আর gate চারপাশে
            মুড়ছে: fin, sheet। Forksheet আর CFET হইলো n আর p-রে আরও কাছে ঠাসার জন্য। আর এরপর, silicon এত পাতলা যে ঠিকমতো
            কাজে লাগানো কঠিন। প্রত্যেকটা row একই সমস্যা না, কিন্তু off অবস্থাটা এর বেশিরভাগের ভিতর দিয়া গেছে।
            """,
        ))
        self.play(FadeOut(self.card_group))
        title = heading("A hundred years in one table")
        head = VGroup(text("when", size=20, color=MUTED), text("the problem", size=20, color=MUTED),
                      text("what answered it", size=20, color=MUTED))
        rows = VGroup(*[VGroup(text(era, size=21, color=GATE, weight="SEMIBOLD"), text(problem, size=21, color=DRAIN),
                               text(fix, size=21, color=MUTED if fix.startswith(("not yet", "none")) else GOOD))
                        for era, problem, fix in ROWS])
        widths = [max(r[k].width for r in rows) for k in range(3)]
        total = sum(widths) + 2 * 0.5
        xs = [-total / 2, -total / 2 + widths[0] + 0.5, -total / 2 + widths[0] + widths[1] + 1.0]
        for i, r in enumerate(rows):
            for m, x in zip(r, xs):
                m.move_to([x, 2.2 - 0.6 * (i + 1), 0], aligned_edge=LEFT)
        for m, x in zip(head, xs):
            m.move_to([x, 2.2, 0], aligned_edge=LEFT)
        rule = Line([xs[0], 1.92, 0], [xs[0] + total, 1.92, 0], stroke_color=FAINT, stroke_width=2)
        self.play(FadeIn(title), FadeIn(head), Create(rule))
        for r in rows:
            self.play(FadeIn(r, shift=RIGHT * 0.15), run_time=0.55)

    def grip(self):
        self.slide(say(
            """
            And here's the grip, in our toy model: the natural length lambda, and the shortest
            gate it suggests, about six lambda. Planar, about 40 nanometres. The FinFET, about 15.
            The nanosheet, somewhere around 12 to 16, depending on how you count its faces. That's
            the grip story. The forksheet and the CFET aren't about grip: they pack the n and the
            p closer, and imec's measured forksheets switched about like nanosheets. These bars
            are a toy, the same simple equation each time; real devices need real models.
            """,
            """
            আর এই যে grip, আমাদের toy model-এ: natural length lambda, আর এইটা যতটা ছোট gate-এর ইঙ্গিত দেয়, প্রায় ছয় lambda।
            Planar, প্রায় 40 nanometre। FinFET, প্রায় 15। Nanosheet, মোটামুটি 12 থেকে 16-এর মধ্যে, এর দিকগুলা কীভাবে গোনেন তার
            উপর নির্ভর করে। এইটা grip-এর গল্প। Forksheet আর CFET grip-এর ব্যাপার না: এগুলা n আর p-রে আরও কাছে ঠাসে, আর
            imec-এর মাপা forksheet প্রায় nanosheet-এর মতোই switch করছে। এই bar-গুলা toy, প্রত্যেকবার একই সহজ equation; আসল
            device-এর জন্য আসল model লাগে।
            """,
        ))
        self.clear()
        title = heading("The grip, in the toy model")
        unit = 3.0 / 40
        cols = VGroup()
        for kind, name, t, ns in GRIP:
            lams = [phys.natural_length_nm(t, 1, n) for n in ns]
            pic = xsection(kind).scale_to_fit_height(1.0)
            bar = Rectangle(width=0.8, height=6 * lams[0] * unit, fill_color=DRAIN, fill_opacity=0.75, stroke_width=0)
            if len(lams) > 1:
                more = Rectangle(width=0.8, height=6 * (lams[1] - lams[0]) * unit, fill_color=DRAIN, fill_opacity=0.3, stroke_width=0)
                bar = VGroup(bar, more.next_to(bar, UP, buff=0))
                num = text(f"{6 * lams[0]:.0f}–{6 * lams[1]:.0f} nm", size=22, color=DRAIN)
                lam_t = MathTex(rf"\lambda \approx {lams[0]:.1f}\text{{–}}{lams[1]:.1f}", font_size=30, color=GATE)
            else:
                num = text(f"{6 * lams[0]:.0f} nm", size=22, color=DRAIN)
                lam_t = MathTex(rf"\lambda \approx {lams[0]:.1f}", font_size=30, color=GATE)
            lbl = VGroup(text(name, size=22, color=INK), lam_t).arrange(DOWN, buff=0.08)
            cols.add(VGroup(pic, lbl, bar, num))
        x0 = -5.4
        for i, c in enumerate(cols):
            x = x0 + 2.3 * i
            c[0].move_to([x, 2.0, 0])
            c[1].next_to(c[0], DOWN, buff=0.2)
            c[2].move_to([x, -3.3 + c[2].height / 2, 0])
            c[3].next_to(c[2], UP, buff=0.08)
        bar_l = VGroup(text("shortest gate ≈ 6λ", size=20, color=DRAIN),
                       text("toy model: 1 nm oxide (EOT), N gates", size=16, color=MUTED)).arrange(DOWN, buff=0.1)
        bar_l.move_to([cols[-1].get_x(), -0.75, 0]).shift(RIGHT * 0.0)
        pack = VGroup(xsection("forksheet").scale_to_fit_height(0.9), xsection("cfet").scale_to_fit_height(0.9)).arrange(RIGHT, buff=0.4)
        pack_t = VGroup(text("forksheet, CFET:", size=24, weight="SEMIBOLD"),
                        text("about packing n and p,\nnot about grip", size=22, color=MUTED),
                        text("measured forksheets switch\nabout like nanosheets\n(imec, 2021)", size=20, color=GOOD)
                        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        right = VGroup(pack, pack_t).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([4.6, 0.2, 0])
        sep = DashedLine([2.7, 2.6, 0], [2.7, -3.2, 0], stroke_color=FAINT, stroke_width=2)
        self.play(FadeIn(title))
        for c in cols:
            self.play(FadeIn(c[0]), FadeIn(c[1]), GrowFromEdge(c[2], DOWN), FadeIn(c[3]), run_time=0.7)
        self.play(FadeIn(bar_l))
        self.play(Create(sep), FadeIn(right))

    def closing(self):
        self.slide(say(
            """
            So here's what I'd like you to take away. Every smaller transistor in this story had
            to do three things at once: keep the off state under control, still give enough
            current when it's on, and fit into a cell that can be built by the billion. The off
            state is the thread we followed, because it's the one that kept coming back: holding
            that hill up when the gate says off.
            """,
            """
            তো যেটা আপনাদের সাথে নিয়া যাইতে বলবো: এই গল্পের প্রত্যেকটা ছোট transistor-রে একসাথে তিনটা কাজ করতে হইছে: off
            অবস্থা control-এ রাখা, on অবস্থায় তবুও যথেষ্ট current দেওয়া, আর এমন একটা cell-এ আঁটা যেটা billion-এ বানানো যায়।
            Off অবস্থাটাই আমরা সুতা হিসাবে ধরছি, কারণ এইটাই বারবার ফিরে আসছে: gate যখন off বলে, তখন ওই hill-টারে ধরে রাখা।
            """,
        ))
        self.clear()
        a = text("Every smaller transistor had to:", size=40, weight="SEMIBOLD").to_edge(UP, buff=0.55)
        jobs = VGroup(text("turn off: hold the hill up", size=30, color=GATE, weight="SEMIBOLD"),
                      text("still turn on: give enough current", size=30),
                      text("fit: a cell you can build by the billion", size=30)).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        jobs.next_to(a, DOWN, buff=0.35)
        bt, dt = ValueTracker(0.08), ValueTracker(0.25)
        bar = Barrier(bt, dt, n=120, origin=(0.0, -1.9), scale=5.5, seed=5)
        self.play(FadeIn(a))
        self.play(FadeIn(bar))
        bar.start()
        self.wait(1.0)
        self.play(FadeIn(jobs[0]), bt.animate.set_value(0.3), run_time=2.5)
        self.play(FadeIn(jobs[1:], shift=UP * 0.1))
        self.wait(1.0)
        self.bar, self.closing_text = bar, VGroup(a, jobs)

        self.slide(say(
            f"""
            And through all of it, one number stayed put: k-B-T over q, times the log of ten,
            {phys.subthreshold_swing(300) * 1e3:.1f} millivolts per decade at room temperature.
            It's the ideal thermal factor: the best swing a conventional transistor can reach at
            room temperature without some internal gain, and real ones are a little worse. The
            bipolar transistor's base voltage follows the same factor, from 1948 to today. Some
            lab devices have already switched faster, as we saw in the last chapter. Turning
            that into useful, reliable circuits, by the billion, is the next chapter.
            """,
            f"""
            আর এর পুরাটা জুড়ে একটা সংখ্যা একই জায়গায় থাকছে: k-B-T বাই q, গুণ log দশ, room temperature-এ প্রতি decade-এ
            {phys.subthreshold_swing(300) * 1e3:.1f} millivolt। এইটা ideal thermal factor: ভিতরে কোনো gain ছাড়া একটা সাধারণ
            transistor room temperature-এ সবচেয়ে ভালো যে swing পাইতে পারে, আর আসলগুলা একটু খারাপ। Bipolar transistor-এর base
            voltage-ও একই factor মেনে চলে, 1948 থেকে আজ পর্যন্ত। Lab-এর কিছু device এর চেয়ে দ্রুত switch করছে, আগের chapter-এ
            দেখলাম। সেটারে কাজের, ভরসাযোগ্য circuit-এ পরিণত করা, billion-এর হিসাবে, সেইটাই পরের chapter।
            """,
        ), loop=False)
        self.bar.stop()
        self.play(FadeOut(self.bar), FadeOut(self.closing_text))
        f = MathTex(r"\frac{k_BT}{q}\,\ln 10", r"\;=\;", rf"{phys.subthreshold_swing(300) * 1e3:.1f}\ \text{{mV per decade}}", font_size=84)
        f[0].set_color(THERMAL)
        f[2].set_color(GATE)
        f.move_to([0, 0.9, 0])
        sub = text("at 300 K: the ideal thermal factor for a conventional transistor without internal gain.\n"
                   "Real devices are a little worse; a bipolar transistor's V_BE follows the same factor.",
                   size=24, color=MUTED, line_spacing=1.0)
        sub.next_to(f, DOWN, buff=0.5)
        last = VGroup(text("Lab devices have crossed it.", size=34, weight="SEMIBOLD"),
                      text("Making them useful, by the billion, is the next chapter.", size=34, weight="SEMIBOLD", color=GATE)
                      ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.85)
        self.play(Write(f), run_time=2)
        self.play(FadeIn(sub))
        self.play(FadeIn(last, shift=UP * 0.15))

    def thanks(self):
        self.slide(say(
            """
            Thank you. I'm happy to take questions. The references file that comes with the
            slides lists the sources for the dates and numbers, and says which figures are models.
            """,
            """
            ধন্যবাদ। প্রশ্ন থাকলে করেন। Slide-এর সাথের references file-এ date আর সংখ্যাগুলার source আছে, আর কোন figure-গুলা
            model সেটাও বলা আছে।
            """,
        ))
        self.clear()
        t = display("Thank you", size=96)
        q = text("Questions?", size=40, color=GATE)
        name = text("Lecture 1 · The Switch That Wouldn't Turn Off", size=26, color=MUTED)
        VGroup(name, t, q).arrange(DOWN, buff=0.45).move_to([0, 0.3, 0])
        self.play(FadeIn(name), FadeIn(t, shift=UP * 0.2))
        self.play(FadeIn(q))

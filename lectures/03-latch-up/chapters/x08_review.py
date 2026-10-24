"""Lecture 3 · X8 · The latch-up review.

A checklist before the deck runs, how to read a LUP report (rule family → knob → fix), what the
JEDEC JESD78 latch-up test does to a finished part, and the question to ask of every rule.
"""

import sys
from pathlib import Path

LECTURE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(LECTURE.parents[1]), str(LECTURE)]

from manim import *  # noqa: E402,F403
from manim_slides import Slide  # noqa: E402

from common import NPLUS, PPLUS, card_box, chapter_title, checklist, table  # noqa: E402
from kit.style import *  # noqa: E402,F403


class X08Review(Chapter, Slide):
    def construct(self):
        self.card()
        self.checks()
        self.reading()
        self.jesd78()
        self.question()
        self.thanks()

    def card(self):
        self.slide(say(
            """
            Chapter eight: the latch-up review. Three things to take back to your desk: a
            checklist for before you run the deck, a way to read the report when it comes back,
            and a picture of what the qualification test will do to the chip.
            """,
            """
            Chapter eight: latch-up review। আপনার desk-এ নিয়া যাওয়ার মতো তিনটা জিনিস: deck চালানোর আগে একটা checklist, report ফিরে আসলে
            সেইটা পড়ার একটা উপায়, আর qualification test chip-এর সাথে কী করবে তার একটা ছবি।
            """,
        ))
        self.card_group = chapter_title(8, "The latch-up review", "Before the deck, after the deck, and the test")
        self.play(FadeIn(self.card_group, shift=UP * 0.2), run_time=1.2)

    def checks(self):
        self.slide(say(
            """
            Before you run the deck. Every N+ and P+ active has a tap of its kind nearby, and every
            well has at least one tap. Every tap is connected, with contacts and metal, to the
            right supply. Every device on a pad, every ESD device and every analog pin has its
            double guard ring, closed, contacted all the way round, strapped wide to the robust
            supply. Sensitive blocks sit outside the injector bands. Every well is tied to the
            highest potential inside it, wells on different supplies are spaced apart, and the
            pad labels and markers the deck needs are all there.
            """,
            """
            Deck চালানোর আগে। প্রত্যেকটা N+ আর P+ active-এর কাছে তার ধরনের একটা tap আছে, আর প্রত্যেকটা well-এ অন্তত একটা tap। প্রত্যেকটা
            tap contact আর metal দিয়া ঠিক supply-তে connected। Pad-এর প্রত্যেকটা device, প্রত্যেকটা ESD device আর প্রত্যেকটা analog pin-এর
            double guard ring আছে, বন্ধ, চারপাশে contact করা, মজবুত supply-তে চওড়া strap করা। Sensitive block-গুলা injector band-এর বাইরে।
            প্রত্যেকটা well তার ভিতরের সবচেয়ে বেশি potential-এ বাঁধা, আলাদা supply-র well-গুলা দূরে দূরে, আর deck-এর দরকারি pad label আর
            marker সব আছে।
            """,
        ))
        self.play(FadeOut(self.card_group))
        title = heading("Before you run the deck")
        left = checklist(["a tap of its kind near every active",
                          "at least one tap in every well",
                          "every tap contacted, on the right net",
                          "double rings on pad, ESD and analog-pin devices",
                          "rings closed, contacted, strapped wide"], size=21)
        right = checklist(["sensitive blocks outside the injector bands",
                           "each well at the highest potential inside it",
                           "wells on different supplies spaced apart",
                           "deep N-wells tied, their p-wells tapped",
                           "pad labels and LUP markers in place"], size=21)
        VGroup(left, right).arrange(RIGHT, buff=0.6, aligned_edge=UP).move_to(DOWN * 0.2)
        self.play(FadeIn(title))
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in [*left, *right]], lag_ratio=0.12), run_time=2.4)

    def reading(self):
        self.slide(say(
            """
            When the report comes back, read each error in three steps. Which family is it: tap,
            ring, injector or well? Which knob does that family protect: the resistance, the
            collection, the distance, or a junction's bias? And so, what's the real fix in the
            picture? A tap error means the base resistance is too high there: add a tap nearby. A
            ring error means carriers have a way through: close or contact the ring. An injector
            error means a victim is too close: move it or put a collector between. A well error
            means a junction can forward-bias: fix the tie or the spacing.
            """,
            """
            Report ফিরে আসলে, প্রত্যেকটা error তিন ধাপে পড়েন। এইটা কোন family: tap, ring, injector না well? ওই family কোন knob রক্ষা
            করে: resistance, collection, distance, না একটা junction-এর bias? তাহলে, ছবিতে আসল সমাধান কী? Tap error মানে ওইখানে base
            resistance খুব বেশি: কাছে একটা tap দেন। Ring error মানে carrier-দের পার হওয়ার একটা পথ আছে: ring বন্ধ করেন বা contact করেন।
            Injector error মানে একটা victim খুব কাছে: সরান বা মাঝে একটা collector দেন। Well error মানে একটা junction forward-bias হইতে পারে:
            tie বা spacing ঠিক করেন।
            """,
        ))
        self.clear()
        title = heading("Reading a LUP report")
        rows = [["family", "the knob", "what the error means", "the real fix"],
                ["tap", "resistance", "base resistance too high here", "a tap nearby"],
                ["ring", "collection", "carriers have a way through", "close, contact, strap the ring"],
                ["injector", "distance", "a victim is too close", "move it, or a collector between"],
                ["well", "junction bias", "a junction can forward-bias", "fix the tie or the spacing"]]
        t = table(rows, col_w=(1.9, 2.4, 4.7, 4.3), size=20, row_gap=0.45).move_to(DOWN * 0.1)
        for row in t[0][1:]:
            row[0].set_color(GATE)
            row[3].set_color(GOOD)
        self.play(FadeIn(title), FadeIn(t[0][0]), FadeIn(t[1]))
        for row in t[0][1:]:
            self.play(FadeIn(row, shift=UP * 0.08), run_time=0.5)

    def jesd78(self):
        self.slide(say(
            """
            And what the chip faces at qualification: the JEDEC latch-up test, JESD78. With the
            supplies at their maximum, it forces current into and out of each I/O pin, the I-test,
            typically up to a hundred milliamps. It overdrives each supply, the V-test, typically
            to one and a half times its maximum. After each stress, the supply current must come
            back to normal. It's run at room temperature, and for the harder class, at the maximum
            operating temperature, where the bipolars have more gain and the resistances are
            higher. Your layout passes or fails right there.
            """,
            """
            আর qualification-এ chip-এর সামনে যা আসে: JEDEC-এর latch-up test, JESD78। Supply-গুলা maximum-এ রেখে, এইটা প্রত্যেকটা I/O pin-এ
            current ঢোকায় আর বের করে, মানে I-test, সাধারণত একশ milliamp পর্যন্ত। প্রত্যেকটা supply-রে বাড়িয়ে চালায়, মানে V-test, সাধারণত
            তার maximum-এর দেড় গুণ পর্যন্ত। প্রত্যেকটা stress-এর পরে supply current স্বাভাবিকে ফিরতে হবে। এইটা room temperature-এ চালানো
            হয়, আর কঠিন class-এর জন্য, সর্বোচ্চ operating temperature-এ, যেখানে bipolar-এর gain বেশি আর resistance বেশি। আপনার layout
            ঠিক সেখানেই pass বা fail করে।
            """,
        ))
        self.clear()
        title = heading("At qualification: JEDEC JESD78")
        cards = VGroup(
            card_box("I-test", [text("force current into and out\nof each I/O pin", size=21, color=INK),
                                text("typically up to ±100 mA", size=21, color=GATE)], width=4.0, height=2.8, head_color=NPLUS),
            card_box("V-test", [text("overdrive each supply", size=21, color=INK),
                                text("typically to 1.5 × its max", size=21, color=GATE)], width=4.0, height=2.8, head_color=PPLUS),
            card_box("Pass", [text("after each stress, the\nsupply current returns\nto normal", size=21, color=INK)],
                     width=4.0, height=2.8, head_color=GOOD),
        ).arrange(RIGHT, buff=0.3).move_to(UP * 0.1)
        hot = text("Class II: at the maximum operating temperature: more gain, more resistance", size=21, color=THERMAL)
        hot.next_to(cards, DOWN, buff=0.45)
        note = text("check the current revision of JESD78 and your product's class", size=17, color=MUTED).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(title))
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.12) for c in cards], lag_ratio=0.25), run_time=1.6)
        self.play(FadeIn(hot), FadeIn(note))

    def question(self):
        self.slide(say(
            """
            If you keep one thing from today, keep the question. For every latch-up rule, and every
            marker it draws, ask: which part of the thyristor does this protect? The tap rules keep
            the base resistances low. The rings collect what the injectors spray. The bands keep
            the victims far away. The well rules keep the junctions reverse-biased. If a fix
            doesn't change the silicon in one of those ways, it only changed the report.
            """,
            """
            আজকের থেকে যদি একটা জিনিস রাখেন, প্রশ্নটা রাখেন। প্রত্যেকটা latch-up rule, আর এর আঁকা প্রত্যেকটা marker-এর জন্য জিজ্ঞেস
            করেন: এইটা thyristor-এর কোন অংশ রক্ষা করে? Tap rule base resistance কম রাখে। Ring injector-এর ছিটানো জিনিস সংগ্রহ করে। Band
            victim-দের দূরে রাখে। Well rule junction-গুলা reverse-bias রাখে। একটা সমাধান যদি silicon-রে এর কোনো একভাবে না বদলায়, তাহলে
            সেইটা শুধু report বদলাইছে।
            """,
        ))
        self.clear()
        q = display("Which part of the thyristor\ndoes this protect?", size=54, color=GATE).move_to(UP * 1.5)
        pairs = VGroup(*[VGroup(text(a, size=26, color=INK), text("→", size=26, color=MUTED), text(b, size=26, color=GOOD)
                                ).arrange(RIGHT, buff=0.3)
                         for a, b in (("tap rules", "low base resistance"), ("guard rings", "collect what's injected"),
                                      ("injector bands", "victims far away"), ("well rules", "junctions reverse-biased"))]
                       ).arrange(DOWN, buff=0.3).move_to(DOWN * 1.3)
        for p in pairs:
            p.shift(RIGHT * (p[1].get_x() * -1))
        self.play(Write(q), run_time=1.6)
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.1) for p in pairs], lag_ratio=0.2), run_time=1.6)

    def thanks(self):
        self.slide(say(
            """
            That's lecture three. Next time a LUP marker shows up in your report, picture the two
            bipolars under it, find the knob, and fix the silicon. Thank you.
            """,
            """
            এই হইল lecture three। পরের বার আপনার report-এ একটা LUP marker আসলে, এর নিচের দুইটা bipolar কল্পনা করেন, knob-টা খুঁজে
            বের করেন, আর silicon ঠিক করেন। ধন্যবাদ।
            """,
        ))
        self.clear()
        t = display("Thank you", size=72).move_to(UP * 0.5)
        s = text("Lecture 3 · Latch-up, in Layout", size=28, color=MUTED).next_to(t, DOWN, buff=0.4)
        self.play(FadeIn(t, shift=UP * 0.2), FadeIn(s))

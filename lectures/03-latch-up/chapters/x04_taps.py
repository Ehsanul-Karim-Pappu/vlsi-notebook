"""Lecture 3 · X4 · Taps: the core rule.

Why the rule is a distance (a voltage budget), how a DRC deck checks it (size the taps, subtract
from the active), well-tap cells in standard-cell rows, taps in analog blocks, the traps, and the
fixes that work.
"""

import sys
from pathlib import Path

LECTURE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(LECTURE.parents[1]), str(LECTURE)]

from manim import *  # noqa: E402,F403
from manim_slides import Slide  # noqa: E402

import physics as ph  # noqa: E402
from common import NPLUS, PPLUS, box, ring, card_box, chapter_title, marker, pdk_tag, tap, toy_tag  # noqa: E402
from kit.style import *  # noqa: E402,F403

RULE = 15.0  # µm, the generic tap distance used on the slides


def active(x0, y0, x1, y1, color):
    return box(x0, y0, x1, y1, color, 0.35, 2.5)


class X04Taps(Chapter, Slide):
    def construct(self):
        self.card()
        self.budget()
        self.check()
        self.std_cells()
        self.analog()
        self.traps()
        self.fixes()

    def card(self):
        self.slide(say(
            """
            Chapter four: taps, the core rule. It's the latch-up rule you meet most: every N+
            active in the substrate within some distance of a P+ substrate tap, and every P+
            active in a well within some distance of an N+ well tap.
            """,
            """
            Chapter four: tap, মূল rule। এইটা সেই latch-up rule যেটা আপনি সবচেয়ে বেশি দেখেন: substrate-এর প্রত্যেকটা N+ active
            একটা P+ substrate tap থেকে নির্দিষ্ট দূরত্বের মধ্যে, আর well-এর প্রত্যেকটা P+ active একটা N+ well tap থেকে নির্দিষ্ট
            দূরত্বের মধ্যে।
            """,
        ))
        self.card_group = chapter_title(4, "Taps: the core rule", "A distance that is really a voltage budget")
        self.play(FadeIn(self.card_group, shift=UP * 0.2), run_time=1.2)

    def budget(self):
        self.slide(say(
            """
            Why a distance? Because the resistance from a device's base to its tap grows with the
            distance, and the rule is really a voltage budget. Pick the current your process
            assumes might be injected nearby, multiply by the resistance, and keep the result well
            below 0.65 volts. Here's the toy model: at one milliamp, the drop crosses 0.65 volts at
            about 24 microns; at two milliamps, at about 11. A rule of 15 microns says: we budget
            for about one milliamp here, with margin. The real number comes from the foundry's
            silicon, not from this plot.
            """,
            """
            দূরত্ব কেন? কারণ একটা device-এর base থেকে তার tap পর্যন্ত resistance দূরত্বের সাথে বাড়ে, আর rule-টা আসলে একটা
            voltage budget। আপনার process কাছাকাছি যতটা current inject হইতে পারে বলে ধরে, সেইটা নেন, resistance দিয়া গুণ করেন,
            আর ফলটা 0.65 volt-এর অনেক নিচে রাখেন। এই যে toy model: এক milliamp-এ drop প্রায় 24 micron-এ 0.65 volt পার হয়; দুই
            milliamp-এ, প্রায় 11-এ। 15 micron-এর একটা rule বলে: এখানে আমরা margin সহ প্রায় এক milliamp-এর budget ধরছি। আসল সংখ্যা
            আসে foundry-র silicon থেকে, এই plot থেকে না।
            """,
        ))
        self.play(FadeOut(self.card_group))
        title = heading("The rule is a voltage budget")
        ax = Axes(x_range=[0, 40, 10], y_range=[0, 1.6, 0.4], x_length=7.4, y_length=4.4,
                  axis_config={"color": MUTED, "include_ticks": False}).move_to([-2.0, -0.4, 0])
        xl = text("distance to the substrate tap (µm)", size=20, color=MUTED).next_to(ax, DOWN, buff=0.15)
        yl = text("drop at the NPN's base (V)", size=20, color=MUTED).rotate(PI / 2).next_to(ax, LEFT, buff=0.2)
        ticks = VGroup(*[text(f"{v:g}", size=16, color=MUTED).next_to(ax.c2p(v, 0), DOWN, buff=0.08) for v in (10, 20, 30, 40)],
                       *[text(f"{v:g}", size=16, color=MUTED).next_to(ax.c2p(0, v), LEFT, buff=0.08) for v in (0.4, 0.8, 1.2)])
        on = DashedLine(ax.c2p(0, ph.V_ON), ax.c2p(40, ph.V_ON), stroke_color=DRAIN, stroke_width=3)
        on_l = text("0.65 V: the NPN turns on", size=18, color=DRAIN).next_to(ax.c2p(40, ph.V_ON), DL, buff=0.08)
        c1 = ax.plot(lambda d: ph.base_drop(1.0, d), x_range=[0, 40], color=GATE, stroke_width=5)
        c2 = ax.plot(lambda d: min(ph.base_drop(2.0, d), 1.6), x_range=[0, 32], color=THERMAL, stroke_width=5)
        l1 = text("1 mA", size=20, color=GATE).next_to(ax.c2p(40, ph.base_drop(1.0, 40)), RIGHT, buff=0.1)
        l2 = text("2 mA", size=20, color=THERMAL).next_to(ax.c2p(31, 1.6), RIGHT, buff=0.1)
        rule = DashedLine(ax.c2p(RULE, 0), ax.c2p(RULE, 1.6), stroke_color=GOOD, stroke_width=3)
        rule_l = text(f"rule: {RULE:g} µm", size=20, color=GOOD).next_to(rule, UP, buff=0.08)
        side = VGroup(text("current it might see", size=22, color=INK),
                      text("× resistance to the tap", size=22, color=INK),
                      text("< 0.65 V, with margin", size=22, color=GOOD, weight="SEMIBOLD")).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        side.move_to([4.7, 0.6, 0])
        tags = VGroup(toy_tag(), pdk_tag()).arrange(RIGHT, buff=0.2).to_corner(DR, buff=0.3)
        self.play(FadeIn(title), Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(ticks), FadeIn(tags))
        self.play(Create(on), FadeIn(on_l))
        self.play(Create(c1), FadeIn(l1), Create(c2), FadeIn(l2))
        self.play(Create(rule), FadeIn(rule_l), FadeIn(side))

    def check(self):
        self.slide(say(
            """
            Now, how does the deck check it? Not with circles. It takes every substrate tap and
            sizes it, grows it, by the rule distance in x and y. Then it subtracts that grown
            shape from the N+ active. Whatever active is left over is farther than the rule from
            every tap, and that's the error marker. So when you see a LUP marker, it's drawn
            exactly on the piece of active that the nearest tap doesn't reach. Note also: only a
            tap of the right kind counts, P+ in the substrate for N+ active, N+ in the well for P+
            active.
            """,
            """
            এবার, deck এইটা check করে কিভাবে? Circle দিয়া না। এইটা প্রত্যেকটা substrate tap নেয় আর rule-এর দূরত্ব দিয়া x আর y-তে
            size করে, মানে বড় করে। তারপর ওই বড় করা আকারটা N+ active থেকে বিয়োগ করে। যতটুকু active বাকি থাকে, সেইটা সব tap থেকে
            rule-এর চেয়ে দূরে, আর সেইটাই error marker। তাই একটা LUP marker দেখলে, সেইটা ঠিক active-এর সেই টুকরার উপর আঁকা যেখানে
            কাছের tap পৌঁছায় না। আরও খেয়াল করেন: শুধু ঠিক ধরনের tap গোনা হয়, N+ active-এর জন্য substrate-এ P+, P+ active-এর
            জন্য well-এ N+।
            """,
        ))
        self.clear()
        title = heading("How the deck checks it: size, subtract, flag")
        ys = (1.0, 0.0, -1.0)
        rows = VGroup(*[active(-6.0, y - 0.25, 3.0, y + 0.25, NPLUS) for y in ys])
        rows_l = text("N+ active", size=18, color=NPLUS).next_to(rows, UP, buff=0.2).align_to(rows, LEFT)
        taps = VGroup(tap(-5.6, 0.0, "p"), tap(-1.6, 0.0, "p"))
        reach = 1.6  # scene units for the rule distance
        grown = VGroup(*[Square(2 * reach, stroke_color=PPLUS, stroke_width=2, fill_color=PPLUS, fill_opacity=0.12).move_to(t)
                         for t in taps])
        left = VGroup(*[box(x0, y - 0.25, x1, y + 0.25, DRAIN, 0.45, 2.5) for y in ys for x0, x1 in ((-4.0, -3.2), (0.0, 3.0))])
        mk = VGroup(marker(VGroup(*left[1::2]), "LUP.TAP.1", buff=0.12), marker(VGroup(*left[0::2]), "LUP.TAP.1", buff=0.12))
        steps = VGroup(text("1  P+ taps", size=22, color=PPLUS),
                       text("2  SIZE taps BY the rule", size=22, color=PPLUS),
                       text("3  N+ active NOT sized taps", size=22, color=DRAIN),
                       text("4  what's left is the error", size=22, color=DRAIN)).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        steps.move_to([4.6, -0.3, 0])
        tag = pdk_tag().to_corner(DR, buff=0.3)
        pic = VGroup(rows, rows_l, taps, grown, left, mk)
        pic.scale(0.82).move_to([-2.4, -0.3, 0])
        self.play(FadeIn(title), FadeIn(rows), FadeIn(rows_l))
        self.play(FadeIn(taps), FadeIn(steps[0]))
        self.play(*[GrowFromCenter(g) for g in grown], FadeIn(steps[1]))
        self.play(FadeIn(left), FadeIn(steps[2]))
        self.play(FadeIn(mk), FadeIn(steps[3]), FadeIn(tag))

    def std_cells(self):
        self.slide(say(
            """
            In digital and mixed-signal blocks, the standard cells usually have no taps of their
            own. Instead, the library has a well-tap cell, holding an N+ tap for the well and a P+
            tap for the substrate, and the place-and-route tool drops one into every row at a fixed
            pitch. Each tap covers the rule distance on both sides, so the pitch can be up to
            twice the rule. The rows are staggered so the taps in neighbouring rows cover the
            gaps. If you hand-place cells, or cut a row short, you inherit that job.
            """,
            """
            Digital আর mixed-signal block-এ standard cell-গুলার সাধারণত নিজেদের কোনো tap থাকে না। তার বদলে library-তে একটা
            well-tap cell থাকে, যেটায় well-এর জন্য একটা N+ tap আর substrate-এর জন্য একটা P+ tap, আর place-and-route tool প্রত্যেকটা
            row-তে একটা নির্দিষ্ট pitch-এ একটা করে বসায়। প্রত্যেকটা tap দুই পাশে rule-এর দূরত্ব ঢাকে, তাই pitch rule-এর দুই গুণ পর্যন্ত
            হইতে পারে। Row-গুলা stagger করা, যাতে পাশের row-এর tap ফাঁকগুলা ঢাকে। আপনি নিজে cell বসালে, বা একটা row ছোট করে
            কাটলে, ওই দায়িত্বটা আপনার।
            """,
        ))
        self.clear()
        title = heading("Standard cells: well-tap cells in every row")
        rows = VGroup()
        cell_h, x0, x1 = 0.7, -6.0, 6.0
        for r in range(4):
            y = 1.5 - r * cell_h
            is_n = r % 2 == 0
            band = box(x0, y - cell_h / 2, x1, y + cell_h / 2, NWELL if is_n else PSUB, 0.55, 1)
            cells = VGroup(*[Rectangle(width=0.55, height=cell_h * 0.9, stroke_color=FAINT, stroke_width=1.5)
                             .move_to([x0 + 0.35 + k * 0.6, y, 0]) for k in range(20)])
            rows.add(VGroup(band, cells))
        tcells = VGroup()
        for r in range(4):
            y = 1.5 - r * cell_h
            offset = 0.0 if r % 2 == 0 else 2.4
            for k in range(3):
                x = x0 + 0.9 + offset + k * 4.8
                if x < x1 - 0.3:
                    t = VGroup(box(x - 0.25, y - cell_h * 0.42, x + 0.25, y + cell_h * 0.42, GATE, 0.9, 1.5),
                               text("TAP", size=12, color=BG, weight="BOLD").move_to([x, y, 0]))
                    tcells.add(t)
        pitch = DoubleArrow([x0 + 0.9, 2.15, 0], [x0 + 5.7, 2.15, 0], buff=0, stroke_color=GATE, stroke_width=3, tip_length=0.15)
        pitch_l = text("pitch ≤ 2 × the rule", size=20, color=GATE).next_to(pitch, UP, buff=0.06)
        note = text("rows alternate: N-well (PMOS) and substrate (NMOS); each tap cell holds an N+ and a P+ tap", size=19,
                    color=MUTED).move_to([0, -1.85, 0])
        tag = pdk_tag().to_corner(DR, buff=0.3)
        self.play(FadeIn(title), FadeIn(rows))
        self.play(LaggedStart(*[FadeIn(t, scale=1.3) for t in tcells], lag_ratio=0.08), run_time=1.6)
        self.play(GrowFromCenter(pitch), FadeIn(pitch_l), FadeIn(note), FadeIn(tag))

    def analog(self):
        self.slide(say(
            """
            In analog blocks you place the taps yourself, and the cleanest way is to make them part
            of the structure. A P+ substrate ring around every NMOS group, an N+ ring inside every
            well around the PMOS, tied with plenty of contacts and wide metal to quiet supplies.
            Rings close to the devices satisfy the tap rule almost for free, give every device the
            same neighbourhood, which you'll remember from the matching lecture, and keep the noise
            from one block out of the next. Butted taps, a tap drawn against an NMOS source tied to
            VSS, are another way to put a tap right where it's needed.
            """,
            """
            Analog block-এ tap আপনি নিজে বসান, আর সবচেয়ে পরিষ্কার উপায় এগুলারে structure-এর অংশ বানানো। প্রত্যেকটা NMOS group-এর
            চারপাশে একটা P+ substrate ring, প্রত্যেকটা well-এর ভিতরে PMOS-এর চারপাশে একটা N+ ring, অনেক contact আর চওড়া metal
            দিয়া শান্ত supply-তে বাঁধা। Device-এর কাছের ring প্রায় বিনা খরচে tap rule মেটায়, প্রত্যেকটা device-রে একই আশেপাশ দেয়,
            যেটা matching lecture থেকে আপনার মনে আছে, আর এক block-এর noise পরেরটায় যাইতে দেয় না। Butted tap, মানে VSS-এ বাঁধা
            একটা NMOS source-এর গায়ে লাগিয়ে আঁকা একটা tap, দরকারের জায়গায় ঠিক tap বসানোর আরেকটা উপায়।
            """,
        ))
        self.clear()
        title = heading("Analog blocks: rings and butted taps")
        # an NMOS group with a P+ ring
        ring_n = ring([-3.4, -0.2], 4.2, 2.6, 0.22, PPLUS)
        devs_n = VGroup(*[active(-5.0 + k * 1.1, -0.9, -4.3 + k * 1.1, 0.5, NPLUS) for k in range(3)])
        devs_n.move_to([-3.4, -0.2, 0])  # centred in its ring
        well = box(0.9, -1.8, 6.1, 1.4, NWELL, 0.55, 2)
        ring_p = ring([3.5, -0.2], 4.2, 2.6, 0.22, NPLUS)
        devs_p = VGroup(*[active(1.9 + k * 1.1, -0.9, 2.6 + k * 1.1, 0.5, PPLUS) for k in range(3)]).move_to([3.5, -0.2, 0])
        l1 = text("P+ substrate ring, to VSS", size=20, color=PPLUS).next_to(ring_n, UP, buff=0.2)
        l2 = text("N+ well ring, to VDD", size=20, color=NPLUS).next_to(well, UP, buff=0.2)
        butt = VGroup(active(-1.4, -2.9, -0.4, -2.3, NPLUS), box(-0.4, -2.9, 0.0, -2.3, PPLUS, 0.9, 2))
        butt_l = text("butted tap: P+ against an N+ source at VSS", size=18, color=MUTED).next_to(butt, RIGHT, buff=0.25)
        self.play(FadeIn(title), FadeIn(well))
        self.play(FadeIn(devs_n), FadeIn(ring_n), FadeIn(l1))
        self.play(FadeIn(devs_p), FadeIn(ring_p), FadeIn(l2))
        self.play(FadeIn(butt), FadeIn(butt_l))

    def traps(self):
        self.slide(say(
            """
            Four traps, all of which look like a tap and count for nothing. A P+ square drawn
            inside a well isn't a substrate tap: it's just P+ in the well. A tap whose metal goes
            to the wrong net, a signal or a different supply, holds the substrate at the wrong
            voltage, and the DRC alone may not see it; that's for LVS and ERC. A tap with no
            contact, or contacts but no metal to VSS, is floating. And a butted tap against a
            source that isn't at VSS isn't a substrate tap either. Each of these can pass a sloppy
            check and fail on silicon.
            """,
            """
            চারটা ফাঁদ, যেগুলা সবই দেখতে tap-এর মতো আর কোনো কাজে আসে না। একটা well-এর ভিতরে আঁকা একটা P+ square substrate tap
            না: এইটা শুধু well-এর ভিতরের P+। যে tap-এর metal ভুল net-এ যায়, একটা signal বা আরেকটা supply, সেইটা substrate-রে ভুল
            voltage-এ ধরে, আর শুধু DRC এইটা নাও দেখতে পারে; এইটা LVS আর ERC-র কাজ। Contact ছাড়া একটা tap, বা contact আছে কিন্তু
            VSS পর্যন্ত metal নাই, এইটা ভাসমান। আর VSS-এ না থাকা একটা source-এর গায়ে লাগানো butted tap-ও substrate tap না। এর
            প্রত্যেকটা একটা ঢিলা check পার হইতে পারে আর silicon-এ fail করতে পারে।
            """,
        ))
        self.clear()
        title = heading("Four taps that count for nothing")
        cards = VGroup(
            card_box("In the wrong well", [text("P+ inside an N-well is\njust P+, not a substrate tap", size=20, color=INK)],
                     width=5.4, height=1.9, head_size=22, head_color=DRAIN),
            card_box("On the wrong net", [text("metal to a signal or another\nsupply: a job for LVS and ERC", size=20, color=INK)],
                     width=5.4, height=1.9, head_size=22, head_color=DRAIN),
            card_box("Floating", [text("no contact, or no metal\nback to VSS", size=20, color=INK)],
                     width=5.4, height=1.9, head_size=22, head_color=DRAIN),
            card_box("Butted to the wrong source", [text("butted against a source\nthat isn't at VSS", size=20, color=INK)],
                     width=5.4, height=1.9, head_size=22, head_color=DRAIN),
        ).arrange_in_grid(rows=2, cols=2, buff=0.3).move_to(DOWN * 0.3)
        self.play(FadeIn(title))
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.12) for c in cards], lag_ratio=0.25), run_time=1.8)

    def fixes(self):
        self.slide(say(
            """
            So, fixing a tap error. Real fixes: add a tap, or a tap row, close to the flagged
            active; use butted taps on sources that really are at VSS; break a long finger array
            with a tap strip in the middle; put rings around analog groups. And the fixes that only
            silence the checker: a marker layer that excludes the area, a tap that isn't connected,
            a waiver nobody signed for a reason. The checker goes quiet. The thyristor doesn't
            care.
            """,
            """
            তাহলে, একটা tap error ঠিক করা। আসল সমাধান: flagged active-এর কাছে একটা tap বা একটা tap row যোগ করেন; যে source সত্যিই
            VSS-এ আছে সেখানে butted tap use করেন; একটা লম্বা finger array-রে মাঝখানে একটা tap strip দিয়া ভাঙেন; analog group-এর
            চারপাশে ring দেন। আর যে সমাধান শুধু checker-রে চুপ করায়: area বাদ দেওয়ার একটা marker layer, একটা tap যেটা connected
            না, কোনো কারণ ছাড়া কেউ sign করা একটা waiver। Checker চুপ হয়ে যায়। Thyristor-এর তাতে কিছু যায় আসে না।
            """,
        ))
        self.clear()
        title = heading("Fixing a tap error")
        good = VGroup(text("Fixes that work", size=28, color=GOOD, weight="SEMIBOLD"),
                      *[text(s, size=22, color=INK) for s in ("a tap or a tap row near the flagged active",
                                                              "butted taps on sources really at VSS",
                                                              "a tap strip through a long finger array",
                                                              "rings around analog groups")]).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        bad = VGroup(text("Fixes that only silence it", size=28, color=DRAIN, weight="SEMIBOLD"),
                     *[text(s, size=22, color=INK) for s in ("a marker layer that excludes the area",
                                                             "a tap that isn't connected",
                                                             "a waiver with no reason behind it")]).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        VGroup(good, bad).arrange(RIGHT, buff=1.0, aligned_edge=UP).move_to(DOWN * 0.2)
        self.play(FadeIn(title), FadeIn(good, shift=UP * 0.1))
        self.play(FadeIn(bad, shift=UP * 0.1))


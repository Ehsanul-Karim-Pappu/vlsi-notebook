"""Layout edition · L6 · Where you put it changes what it does.

Layout-dependent effects in plain words: the well's edge, stress from the isolation, the
neighbours and the density rules, self-heating, the contacts' parasitics. Then the matching
habits that tame them, and a checklist.
"""

import sys
from pathlib import Path

LECTURE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(LECTURE.parents[1]), str(LECTURE), str(LECTURE / "layout")]

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403
from manim_slides import Slide  # noqa: E402

from common import ACTIVE, CONTACT, METAL, NWELL, POLY, box, planar_mos, schematic  # noqa: E402
from kit.style import *  # noqa: E402,F403

RESIST = "#C9A0DC"
OXIDE_FILL = "#5A6270"


class L06Neighbourhood(Chapter, Slide):
    def construct(self):
        self.card()
        self.same_device()
        self.well_edge()
        self.stress()
        self.neighbours()
        self.centroid()
        self.habits()
        self.orientation()
        self.substrate()
        self.heat()
        self.parasitics()
        self.antenna()
        self.checklist()

    def card(self):
        self.slide(say(
            """
            Chapter six. Everything so far was about the device itself. This chapter is about
            its surroundings, because on every one of these processes, planar to nanosheet,
            where you put a transistor changes what it does.
            """,
            """
            Chapter six। এতক্ষণ সব ছিল device নিজেরে নিয়া। এই chapter তার আশেপাশে নিয়া, কারণ এই প্রত্যেকটা process-এ,
            planar থেকে nanosheet, transistor কোথায় বসাইলেন তাতেই বদলায় সে কী করে।
            """,
        ))
        n = kicker("Chapter 6", color=GATE)
        big = display("LDE", size=150, color=FAINT)
        ttl = display("Where you put it changes what it does", size=52)
        sub = text("Layout-dependent effects, and the habits that tame them", size=28, color=MUTED, slant="ITALIC")
        self.card_group = VGroup(n, big, ttl, sub).arrange(DOWN, buff=0.25).move_to(UP * 0.2)
        self.play(FadeIn(self.card_group, shift=UP * 0.2), run_time=1.2)

    def same_device(self):
        self.slide(say(
            """
            Here's the problem in one picture. Two transistors, the same schematic symbol, the
            same W, the same L, the same fingers. One sits in the middle of open space. The other
            sits close to the edge of its well, at the end of its active, next to a crowd of
            other shapes. On silicon, they don't carry the same current. The models in your PDK
            account for this from the layout, which is why the same schematic can simulate
            differently after extraction. These are called layout-dependent effects. Let's take
            the main ones one at a time.
            """,
            """
            এক ছবিতে সমস্যাটা এই। দুইটা transistor, একই schematic symbol, একই W, একই L, একই finger। একটা খোলা জায়গার
            মাঝখানে। আরেকটা তার well-এর কিনারার কাছে, active-এর মাথায়, আরও অনেক shape-এর ভিড়ে। Silicon-এ দুইটা একই current
            বয় না। আপনার PDK-র model layout দেখে এইটা হিসাব করে, এই কারণেই একই schematic extraction-এর পরে আলাদা simulate
            হইতে পারে। এগুলারে বলে layout-dependent effect। প্রধানগুলা একটা একটা করে দেখি।
            """,
        ))
        self.play(FadeOut(self.card_group))
        title = heading("Same schematic, same size, different place")
        a, _ = planar_mos(160, 60, nf=2, u=0.009, sd=90, center=(-3.6, 0.3))
        b, _ = planar_mos(160, 60, nf=2, u=0.009, sd=90, center=(3.0, 0.3))
        well = box(1.4, -1.7, 6.6, 2.2, NWELL, 0.12)
        well_edge = Line([1.4, -1.7, 0], [1.4, 2.2, 0], stroke_color=NWELL, stroke_width=4)
        crowd = VGroup(*[box(x, y, x + 0.25, y + 1.0, POLY, 0.35) for x, y in ((4.9, -0.3), (5.4, -0.3), (5.9, -0.3))])
        crowd.add(box(4.75, -1.3, 6.3, -0.75, ACTIVE, 0.3))
        la = text("open space", size=24, color=GOOD).move_to([-3.6, -2.15, 0])
        lb = text("near a well edge, in a crowd", size=24, color=DRAIN).move_to([3.4, -2.15, 0])
        bars = VGroup(Rectangle(width=2.0, height=0.28, fill_color=GOOD, fill_opacity=0.9, stroke_width=0),
                      Rectangle(width=1.55, height=0.28, fill_color=DRAIN, fill_opacity=0.9, stroke_width=0))
        bars[0].next_to(la, DOWN, buff=0.35)
        bars[1].next_to(lb, DOWN, buff=0.35).align_to(lb, LEFT)
        bars[0].align_to(la, LEFT)
        cur = VGroup(text("current", size=18, color=MUTED).next_to(bars[0], LEFT, buff=0.15),
                     text("current", size=18, color=MUTED).next_to(bars[1], LEFT, buff=0.15))
        tag = text("illustrative", size=16, color=MUTED).to_corner(DR, buff=0.3)
        self.play(FadeIn(title), FadeIn(a), FadeIn(la))
        self.play(FadeIn(well), Create(well_edge), FadeIn(b), FadeIn(crowd), FadeIn(lb))
        self.play(GrowFromEdge(bars[0], LEFT), GrowFromEdge(bars[1], LEFT), FadeIn(cur), FadeIn(tag))

    def well_edge(self):
        self.slide(say(
            """
            One: the edge of the well. The well is made by implanting ions at high energy, with
            photoresist blocking everywhere the well shouldn't be. Some of those ions hit the
            side of the resist and scatter sideways, into the silicon just inside the edge. So
            the silicon near a well edge gets a little extra doping, and a transistor there has
            a higher threshold voltage than the same transistor further in. It's strongest within
            about a micron of the edge. The habit: keep matched devices away from well edges, and
            if you can't, put them the same distance from the same edge.
            """,
            """
            এক: well-এর কিনারা। Well বানানো হয় high energy-তে ion implant করে, আর যেখানে well হওয়ার কথা না সেখানে photoresist
            আটকায়। ওই ion-গুলার কিছু resist-এর গায়ে লেগে পাশে ছিটকায়, কিনারার ঠিক ভিতরের silicon-এ। তাই well-এর কিনারার কাছের
            silicon একটু বেশি doping পায়, আর সেখানে একটা transistor-এর threshold voltage ভিতরের একই transistor-এর চেয়ে বেশি। কিনারা
            থেকে মোটামুটি এক micron-এর মধ্যে এইটা সবচেয়ে বেশি। অভ্যাস: matched device-গুলারে well-এর কিনারা থেকে দূরে রাখেন, আর
            না পারলে, একই কিনারা থেকে একই দূরত্বে বসান।
            """,
        ))
        self.clear()
        title = heading("1 · The well's edge")
        si = box(-6.4, -2.6, 1.0, -0.8, SUBSTRATE, 1.0, 0)
        well = box(-6.4, -2.0, -1.5, -0.8, NWELL, 0.3, 0)
        resist = box(-1.5, -0.8, 1.0, 0.7, RESIST, 0.75, 0)
        resist_l = text("photoresist", size=20, color=BG, weight="SEMIBOLD").move_to(resist)
        well_l = text("n-well", size=20, color=INK).move_to([-4.6, -1.7, 0])
        ions = VGroup(*[Arrow([x, 2.2, 0], [x, -0.75 if x < -1.5 else 0.75, 0], buff=0, stroke_color=GATE,
                              stroke_width=3, max_tip_length_to_length_ratio=0.08) for x in np.linspace(-6.0, 0.6, 12)])
        ion_l = text("well implant: high-energy ions", size=20, color=GATE).move_to([-2.6, 2.5, 0])
        scatter = VGroup(*[CurvedArrow([-1.45, y, 0], [-1.45 - dx, y - 0.45, 0], angle=-0.6, stroke_color=DRAIN, stroke_width=3)
                           for y, dx in ((0.5, 0.7), (0.15, 1.0), (-0.2, 0.6))])
        extra = box(-2.5, -1.35, -1.5, -0.8, DRAIN, 0.45, 0)
        extra_l = text("extra doping\nnear the edge", size=20, color=DRAIN).move_to([-2.2, -3.1, 0])
        ax = Axes(x_range=[0, 3, 1], y_range=[0, 1.1, 0.5], x_length=4.4, y_length=2.4, tips=False,
                  axis_config={"stroke_color": MUTED, "stroke_width": 2, "include_ticks": False}).move_to([4.3, 0.1, 0])
        curve = ax.plot(lambda d: np.exp(-d / 0.6), x_range=[0, 3], color=DRAIN, stroke_width=5)
        xl = text("distance from the well edge (µm)", size=18, color=MUTED).next_to(ax.x_axis, DOWN, buff=0.45)
        yl = text("threshold shift", size=18, color=MUTED).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.15)
        ticks = VGroup(*[text(str(v), size=16, color=MUTED).next_to(ax.c2p(v, 0), DOWN, buff=0.08) for v in (0, 1, 2, 3)])
        tag = text("illustrative; after T. B. Hook et al., IEEE TED 2003, and P. G. Drennan et al., CICC 2006",
                   size=15, color=MUTED).to_corner(DR, buff=0.3)
        note = layout_note("Keep matched devices away from well edges; if you can't, put them the same distance "
                           "from the same edge.", size=20, width=40).move_to([4.2, -2.4, 0])
        self.play(FadeIn(title), FadeIn(si), FadeIn(well), FadeIn(well_l), FadeIn(resist), FadeIn(resist_l), FadeIn(tag))
        self.play(LaggedStart(*[GrowArrow(a) for a in ions], lag_ratio=0.06), FadeIn(ion_l), run_time=1.6)
        self.play(Create(scatter), FadeIn(extra), FadeIn(extra_l), run_time=1.4)
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(ticks), Create(curve))
        self.play(FadeIn(note, shift=UP * 0.1))

    def stress(self):
        self.slide(say(
            """
            Two: stress from the isolation. The trench oxide around the active squeezes the
            silicon, and how hard depends on how far the gate is from the end of the active: the
            distances the models call SA and SB. A gate near the end of a short active feels more
            squeeze than one in the middle of a long active, and the current changes with it, in
            opposite directions for n and p. The habit: give matched devices the same SA and SB,
            add dummy fingers at the ends so the real gates sit inside, and don't pack a matched
            pair against the active's edge. On FinFET and nanosheet processes, the same idea
            shows up as the distance to the nearest diffusion break, and the kind of break.
            """,
            """
            দুই: isolation থেকে stress। Active-এর চারপাশের trench oxide silicon-রে চাপ দেয়, আর কতটা জোরে, সেইটা নির্ভর করে gate
            active-এর মাথা থেকে কত দূরে তার উপর: model যেগুলারে বলে SA আর SB। ছোট active-এর মাথার কাছের gate লম্বা active-এর
            মাঝখানের gate-এর চেয়ে বেশি চাপ পায়, আর তার সাথে current বদলায়, n আর p-তে উল্টা দিকে। অভ্যাস: matched device-গুলারে
            একই SA আর SB দেন, মাথায় dummy finger দেন যাতে আসল gate-গুলা ভিতরে বসে, আর matched pair-রে active-এর কিনারায় ঠেলে
            দিয়েন না। FinFET আর nanosheet process-এ একই কথা আসে সবচেয়ে কাছের diffusion break-এর দূরত্ব, আর break-এর ধরন হিসাবে।
            """,
        ))
        self.clear()
        title = heading("2 · Stress from the isolation")
        sti = box(-6.2, -2.2, 0.6, 2.0, OXIDE_FILL, 0.5, 0)
        sti_l = text("trench oxide", size=18, color=MUTED).move_to([-5.4, 1.7, 0])
        act = box(-5.0, -1.0, -0.6, 1.0, ACTIVE, 0.6)
        gates = VGroup(*[box(x - 0.15, -1.4, x + 0.15, 1.4, POLY, 0.75) for x in (-3.9, -2.8, -1.7)])
        gates[0].set_fill(opacity=0.25)
        gates[2].set_fill(opacity=0.25)
        dummy_l = text("dummy", size=16, color=MUTED).next_to(gates[0], DOWN, buff=0.1)
        dummy2 = text("dummy", size=16, color=MUTED).next_to(gates[2], DOWN, buff=0.1)
        sa = DoubleArrow([-5.0, 0.0, 0], [-2.95, 0.0, 0], buff=0, stroke_color=GATE, stroke_width=3, tip_length=0.12)
        sb = DoubleArrow([-2.65, -0.45, 0], [-0.6, -0.45, 0], buff=0, stroke_color=GATE, stroke_width=3, tip_length=0.12)
        sa_l = text("SA", size=22, color=GATE, weight="BOLD").next_to(sa, UP, buff=0.06).shift(LEFT * 0.4)
        sb_l = text("SB", size=22, color=GATE, weight="BOLD").next_to(sb, DOWN, buff=0.06).shift(RIGHT * 0.4)
        push = VGroup(Arrow([-6.0, 0.6, 0], [-5.1, 0.6, 0], buff=0, stroke_color=DRAIN, stroke_width=4),
                      Arrow([0.5, 0.6, 0], [-0.5, 0.6, 0], buff=0, stroke_color=DRAIN, stroke_width=4))
        push_l = text("the oxide squeezes the active", size=20, color=DRAIN).move_to([-2.8, 2.45, 0])
        words = VGroup(text("current depends on SA and SB:\nthe gate's distance to the\nactive's ends", size=24, weight="SEMIBOLD"),
                       text("n and p shift in opposite\ndirections", size=22, color=INK),
                       text("FinFET, nanosheet: the distance\nto the nearest diffusion break,\nand its type", size=22, color=MUTED),
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.0, 0.7, 0])
        note = layout_note("Same SA and SB for matched devices; dummy fingers at the ends; don't pack a "
                           "matched pair against the active's edge.", size=20, width=40).move_to([4.0, -2.3, 0])
        tag = text("after R. A. Bianchi et al., IEDM 2002; the SA/SB stress model in BSIM4", size=15, color=MUTED).to_corner(DL, buff=0.3)
        self.play(FadeIn(title), FadeIn(sti), FadeIn(sti_l), FadeIn(act), FadeIn(gates), FadeIn(dummy_l), FadeIn(dummy2), FadeIn(tag))
        self.play(GrowArrow(push[0]), GrowArrow(push[1]), FadeIn(push_l))
        self.play(GrowFromCenter(sa), GrowFromCenter(sb), FadeIn(sa_l), FadeIn(sb_l), FadeIn(words[0]))
        self.play(FadeIn(words[1]))
        self.play(FadeIn(words[2]))
        self.play(FadeIn(note, shift=UP * 0.1))

    def neighbours(self):
        self.slide(say(
            """
            Three: the neighbours. The shapes around a device, within a few microns, change how
            it prints and how it's processed: the spacing to the next poly, the spacing to the
            next active, how dense the area is. The density rules exist for the same reason;
            that's why the fill tool drops dummy shapes everywhere. You can't stop the
            neighbourhood from mattering, but you can make it the same. Surround every matched
            device with the same dummies, the same spacings, the same fill, so whatever the
            neighbours do, they do it to all of them equally.
            """,
            """
            তিন: প্রতিবেশী। একটা device-এর আশেপাশের shape-গুলা, কয়েক micron-এর মধ্যে, বদলায় সে কিভাবে print হয় আর কিভাবে
            process হয়: পরের poly পর্যন্ত spacing, পরের active পর্যন্ত spacing, জায়গাটা কতটা ঘন। Density rule-ও একই কারণে আছে;
            এই জন্যই fill tool সব জায়গায় dummy shape ফেলে। প্রতিবেশীর প্রভাব থামাইতে পারবেন না, কিন্তু সবার জন্য একই করতে পারবেন।
            প্রত্যেকটা matched device-এর চারপাশে একই dummy, একই spacing, একই fill দেন, যাতে প্রতিবেশী যা-ই করুক, সবার সাথে সমানভাবে
            করে।
            """,
        ))
        self.clear()
        title = heading("3 · The neighbours, and the density rules")

        def scene(cx, uniform):
            g = VGroup()
            for k, ch in enumerate("AB"):
                dev, _ = planar_mos(120, 60, nf=2, u=0.006, sd=80, contacts=False, metal=False, center=(cx - 1.25 + 2.5 * k, 0.2))
                lab = text(ch, size=22, weight="BOLD", color=ELECTRON if ch == "A" else GATE).next_to(dev, UP, buff=0.35)
                g.add(dev, lab)
            if uniform:
                for x in (cx - 2.75, cx - 0.0, cx + 2.75):
                    g.add(box(x - 0.1, -0.75, x + 0.1, 1.15, POLY, 0.25))
            else:
                g.add(box(cx + 2.55, -0.75, cx + 2.75, 1.15, POLY, 0.25), box(cx + 2.95, -0.75, cx + 3.15, 1.15, POLY, 0.25),
                      box(cx - 3.1, -1.4, cx - 2.3, -1.0, ACTIVE, 0.3))
            return g

        bad = scene(-3.5, False)
        good = scene(3.5, True)
        bl = text("different neighbours: A ≠ B", size=24, color=DRAIN).next_to(bad, DOWN, buff=0.5)
        gl = text("the same neighbours: A ≈ B", size=24, color=GOOD).next_to(good, DOWN, buff=0.5).align_to(bl, UP)
        note = layout_note("Give every matched device the same dummies, spacings and fill. Density rules and "
                           "dummy fill are part of the same story.", size=21, width=70).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(title), FadeIn(bad), FadeIn(bl))
        self.play(FadeIn(good), FadeIn(gl))
        self.play(FadeIn(note, shift=UP * 0.1))

    def centroid(self):
        self.slide(say(
            """
            Why does a common centre work? Because most of what varies across a die varies
            smoothly: oxide thickness, stress, temperature, a little more on one side than the
            other. Model it as a slope. Put four units in a row, at positions one, two, three,
            four, and let each pick up its position's value. Placed A A B B, device A gets one
            plus two, three, and B gets three plus four, seven: a mismatch. Placed A B B A, A
            gets one plus four, B gets two plus three: five and five. A linear gradient cancels
            exactly. That's all common centroid is.
            """,
            """
            Common center কেন কাজ করে? কারণ die জুড়ে যা বদলায় তার বেশিরভাগ মসৃণভাবে বদলায়: oxide thickness, stress, temperature,
            এক পাশে একটু বেশি, আরেক পাশে কম। এইটারে একটা ঢাল ধরেন। এক row-তে চারটা unit রাখেন, এক, দুই, তিন, চার নম্বর জায়গায়, আর
            প্রত্যেকটা তার জায়গার মানটা পায়। A A B B বসাইলে A পায় এক যোগ দুই, তিন, আর B পায় তিন যোগ চার, সাত: mismatch। A B B A
            বসাইলে A পায় এক যোগ চার, B পায় দুই যোগ তিন: পাঁচ আর পাঁচ। একটা linear gradient পুরাপুরি কেটে যায়। Common centroid
            মানে শুধু এইটুকুই।
            """,
        ))
        self.clear()
        title = heading("Why a common centre works")
        ramp = VGroup(*[Rectangle(width=1.6, height=0.35, stroke_width=0, fill_color=interpolate_color(ManimColor(ELECTRON), ManimColor(DRAIN), k / 3),
                                  fill_opacity=0.8).move_to([-3.6 + 1.6 * k, 2.15, 0]) for k in range(4)])
        ramp_l = text("a smooth gradient across the row (oxide, stress, temperature)", size=20, color=MUTED).next_to(ramp, UP, buff=0.15)

        def row(order, y, verdict, color):
            cells = VGroup()
            for k, ch in enumerate(order):
                c = ELECTRON if ch == "A" else GATE
                sq = RoundedRectangle(width=1.4, height=0.9, corner_radius=0.08, stroke_color=c, stroke_width=3,
                                      fill_color=c, fill_opacity=0.15).move_to([-3.6 + 1.6 * k, y, 0])
                cells.add(VGroup(sq, text(f"{ch}: {k + 1}", size=26, weight="BOLD", color=c).move_to(sq)))
            a = sum(k + 1 for k, ch in enumerate(order) if ch == "A")
            b = sum(k + 1 for k, ch in enumerate(order) if ch == "B")
            res = text(f"A = {a}, B = {b}: {verdict}", size=26, color=color).next_to(cells, RIGHT, buff=0.6)
            return cells, res

        r1, v1 = row("AABB", 0.6, "a mismatch", DRAIN)
        r2, v2 = row("ABBA", -1.0, "equal", GOOD)
        n1 = text("A A B B", size=22, color=MUTED).next_to(r1, LEFT, buff=0.5)
        n2 = text("A B B A", size=22, color=MUTED).next_to(r2, LEFT, buff=0.5)
        foot = text("a linear gradient cancels exactly around a common centre", size=26, color=GATE).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(title), FadeIn(ramp), FadeIn(ramp_l))
        self.play(FadeIn(r1), FadeIn(n1))
        self.play(FadeIn(v1))
        self.play(FadeIn(r2), FadeIn(n2))
        self.play(FadeIn(v2))
        self.play(FadeIn(foot))

    def habits(self):
        self.slide(say(
            """
            So the matching habits you learned on planar still hold, on every process. Take this
            five-transistor amplifier. The input pair, M1 and M2, and the mirror, M3 and M4, must
            match. Build each from identical units. Interleave them around a common centre:
            A, B, B, A. Keep them in one orientation, with dummies at both ends, and the same
            metal running over each. And when matching matters, spend area: mismatch falls with
            the square root of the gate area, so four times the area halves it.
            """,
            """
            তো planar-এ শেখা matching-এর অভ্যাসগুলা এখনো খাটে, সব process-এ। এই five-transistor amplifier-টা নেন। Input pair,
            M1 আর M2, আর mirror, M3 আর M4, match করতে হবে। প্রত্যেকটা একই unit দিয়া বানান। একটা common center ঘিরে মিশায়ে বসান:
            A, B, B, A। এক orientation-এ রাখেন, দুই মাথায় dummy, আর প্রত্যেকটার উপর দিয়া একই metal। আর matching জরুরি হইলে area
            খরচ করেন: mismatch gate area-র square root হারে কমে, তাই চার গুণ area-তে অর্ধেক।
            """,
        ))
        self.clear()
        title = heading("Habits that still work, on every process")
        sch = schematic("ota5t", 3.4).move_to([-4.4, -0.1, 0])
        row = VGroup()
        for ch in "DABBAD":
            col = ELECTRON if ch == "A" else GATE if ch == "B" else FAINT
            dev, _ = planar_mos(100, 50, nf=1, u=0.0065, sd=70, contacts=False, metal=False)
            lab = text("dummy" if ch == "D" else ch, size=20 if ch != "D" else 14, weight="BOLD", color=col)
            if ch == "D":
                dev.set_opacity(0.35)
            row.add(VGroup(dev, lab.next_to(dev, UP, buff=0.12)))
        row.arrange(RIGHT, buff=0.1).move_to([2.6, 1.6, 0])
        key = text("A = M1, B = M2: interleaved around one centre", size=20, color=MUTED).next_to(row, DOWN, buff=0.2)
        habits = VGroup(*[text(h, size=22, color=INK) for h in (
            "identical units for every matched device",
            "a common centre: A B B A",
            "one orientation; dummies at both ends",
            "the same metal over each device",
            "area for matching: 4× the area, ½ the mismatch",
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([2.6, -1.3, 0])
        cite = text("mismatch ∝ 1/√(gate area): M. J. M. Pelgrom et al., IEEE JSSC 1989", size=15, color=MUTED).to_corner(DR, buff=0.3)
        self.play(FadeIn(title), FadeIn(sch))
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in row], lag_ratio=0.15), FadeIn(key), run_time=1.4)
        for h in habits:
            self.play(FadeIn(h, shift=UP * 0.08), run_time=0.5)
        self.play(FadeIn(cite))

    def orientation(self):
        self.slide(say(
            """
            Why does orientation matter? Some implants come in at a tilt, so the gate casts a
            small shadow on one side: the source side and the drain side of a device don't get
            quite the same dose. Turn a device around and its shadow moves with it. Two matched
            devices drawn in opposite orientations are no longer identical, even with the same
            size and the same neighbours. On FinFET and nanosheet processes the gates usually
            have to run in one direction anyway; inside a matched group, also keep the source
            and the drain on the same sides.
            """,
            """
            Orientation কেন জরুরি? কিছু implant কাত হয়ে আসে, তাই gate এক পাশে একটা ছোট ছায়া ফেলে: একটা device-এর source
            দিক আর drain দিক ঠিক একই dose পায় না। Device-টা ঘুরায়ে দিলে ছায়াও তার সাথে সরে। দুইটা matched device উল্টা
            orientation-এ আঁকলে আর হুবহু এক থাকে না, size আর প্রতিবেশী এক হইলেও। FinFET আর nanosheet process-এ gate সাধারণত
            এমনিতেই এক দিকে চলতে হয়; একটা matched group-এর ভিতরে source আর drain-ও একই পাশে রাখেন।
            """,
        ))
        self.clear()
        title = heading("Orientation: the same way round")
        si = box(-6.0, -2.2, 0.0, -1.0, SUBSTRATE, 1.0, 0)
        gate = box(-3.4, -1.0, -2.6, 0.6, POLY, 0.85, 0)
        slope = 1.4 / 3.4  # the implant's tilt: x moves this much left per unit down

        def ray(x0):
            """A ray from (x0, 2.4), stopped by the gate's top or right side, or the surface."""
            end_top = (x0 - slope * (2.4 - 0.6), 0.6)
            if -3.4 <= end_top[0] <= -2.6:
                return end_top
            y_side = 2.4 - (x0 + 2.6) / slope  # where it crosses x = -2.6
            if -1.0 <= y_side <= 0.6:
                return (-2.6, y_side)
            return (x0 - slope * 3.4, -1.0)

        rays = VGroup(*[Line([x, 2.4, 0], [*ray(x), 0], stroke_color=GATE, stroke_width=3) for x in np.linspace(-4.6, 0.8, 13)])
        shadow = box(-4.06, -1.25, -3.4, -1.0, FAINT, 1.0, 0)
        sh_l = text("shadow: a little less dose\non this side", size=20, color=MUTED).move_to([-4.4, -2.75, 0])
        tilt = text("a tilted implant", size=20, color=GATE).move_to([-1.6, 2.6, 0])
        a = VGroup(text("S", size=24, weight="BOLD"), Arrow(LEFT * 0.5, RIGHT * 0.5, buff=0, stroke_color=ELECTRON), text("D", size=24, weight="BOLD")
                   ).arrange(RIGHT, buff=0.15)
        b = a.copy()
        c = VGroup(text("D", size=24, weight="BOLD"), Arrow(RIGHT * 0.5, LEFT * 0.5, buff=0, stroke_color=DRAIN), text("S", size=24, weight="BOLD")
                   ).arrange(RIGHT, buff=0.15)
        good = VGroup(a, b).arrange(RIGHT, buff=0.8)
        good_l = text("matched: the same way round", size=22, color=GOOD)
        bad = VGroup(a.copy(), c).arrange(RIGHT, buff=0.8)
        bad_l = text("mirrored: not identical", size=22, color=DRAIN)
        col = VGroup(VGroup(good, good_l).arrange(DOWN, buff=0.2), VGroup(bad, bad_l).arrange(DOWN, buff=0.2)).arrange(DOWN, buff=0.7)
        col.move_to([3.8, 0.5, 0])
        note = layout_note("Gates in one direction, and inside a matched group the sources and drains on the "
                           "same sides.", size=20, width=40).move_to([3.8, -2.2, 0])
        tag = text("illustrative", size=16, color=MUTED).to_corner(DL, buff=0.3)
        self.play(FadeIn(title), FadeIn(si), FadeIn(gate), FadeIn(tag))
        self.play(Create(rays), FadeIn(tilt), run_time=1.4)
        self.play(FadeIn(shadow), FadeIn(sh_l))
        self.play(FadeIn(col[0]))
        self.play(FadeIn(col[1]))
        self.play(FadeIn(note, shift=UP * 0.1))

    def substrate(self):
        self.slide(say(
            """
            And the neighbour you can't see: the substrate. Every digital edge pushes a little
            current into the silicon underneath, and the substrate carries it to every device
            sitting on it, including your quiet analog ones. Guard rings intercept it: a ring of
            p-plus taps around a sensitive block, tied to a quiet ground, and an n-well ring
            tied to a quiet supply. Distance helps, and in many processes a deep n-well can put
            a whole block in its own isolated tub. Keep the noisy and the quiet apart, and give
            each its own supplies.
            """,
            """
            আর যে প্রতিবেশীরে দেখা যায় না: substrate। প্রত্যেকটা digital edge নিচের silicon-এ একটু current ঢুকায়, আর substrate
            সেইটা তার উপরে বসা সব device-এর কাছে নিয়া যায়, আপনার শান্ত analog device-গুলা সহ। Guard ring এইটারে মাঝপথে ধরে: একটা
            sensitive block-এর চারপাশে p-plus tap-এর একটা ring, একটা শান্ত ground-এ বাঁধা, আর একটা n-well ring, একটা শান্ত supply-তে।
            দূরত্বও সাহায্য করে, আর অনেক process-এ deep n-well একটা পুরা block-রে নিজের আলাদা গর্তে রাখতে পারে। গোলমেলে আর শান্ত
            জিনিস আলাদা রাখেন, আর প্রত্যেকটারে তার নিজের supply দেন।
            """,
        ))
        self.clear()
        title = heading("The neighbour you can't see: the substrate")
        sub = box(-6.2, -2.4, 6.2, -0.4, SUBSTRATE, 1.0, 0)
        dig = box(-5.6, -0.4, -3.0, 0.4, DRAIN, 0.35)
        dig_l = text("digital: noisy", size=22, color=DRAIN).next_to(dig, UP, buff=0.12)
        ana = box(2.4, -0.4, 5.0, 0.4, ELECTRON, 0.35)
        ana_l = text("analog: sensitive", size=22, color=ELECTRON).next_to(ana, UP, buff=0.12)
        ring = VGroup(box(1.6, -0.6, 2.0, -0.4, HOLE, 0.9, 0), box(5.4, -0.6, 5.8, -0.4, HOLE, 0.9, 0))
        ring_l = text("guard ring: p+ taps to a quiet ground", size=20, color=HOLE).move_to([3.9, -2.1, 0])
        path = VMobject(stroke_color=DRAIN, stroke_width=4).set_points_smoothly(
            [[-4.3, -0.5, 0], [-2.0, -1.6, 0], [0.4, -1.5, 0], [1.8, -0.75, 0]])
        tip = Arrow([1.4, -1.0, 0], [1.8, -0.7, 0], buff=0, stroke_color=DRAIN, stroke_width=4, max_tip_length_to_length_ratio=0.5)
        path_l = text("noise current through the substrate", size=20, color=DRAIN).move_to([-1.6, -2.0, 0])
        stop = text("collected here", size=18, color=HOLE).next_to(ring[0], DOWN, buff=0.12)
        note = layout_note("Guard rings around sensitive blocks, distance from noisy ones, separate quiet supplies, "
                           "and deep n-well isolation where the process offers it.", size=20, width=70).to_edge(DOWN, buff=0.2)
        tag = text("illustrative", size=16, color=MUTED).to_corner(UR, buff=0.3).shift(DOWN * 0.7)
        self.play(FadeIn(title), FadeIn(sub), FadeIn(dig), FadeIn(dig_l), FadeIn(ana), FadeIn(ana_l), FadeIn(tag))
        self.play(Create(path), FadeIn(tip), FadeIn(path_l), run_time=1.4)
        self.play(FadeIn(ring), FadeIn(stop), FadeIn(ring_l))
        self.play(FadeIn(note, shift=UP * 0.1))

    def heat(self):
        self.slide(say(
            """
            Four: heat. A fin or a sheet is a sliver of silicon wrapped in oxide and metal, and
            oxide is a poor conductor of heat. When it carries current, the device runs hotter
            than the chip around it. That's self-heating. It lowers the current, it ages the
            device faster, and it heats the wires above, which then wear out sooner by
            electromigration. For layout: don't pack high-current devices into one tight block;
            spread their fingers, give the heat somewhere to go, and follow the
            electromigration width and via rules for every high-current wire.
            """,
            """
            চার: তাপ। একটা fin বা sheet হইলো oxide আর metal-এ মোড়ানো silicon-এর একটা সরু টুকরা, আর oxide তাপ খুব একটা
            পরিবহন করে না। Current বইলে device তার চারপাশের chip-এর চেয়ে বেশি গরম হয়। এইটারে বলে self-heating। এইটা current
            কমায়, device-রে দ্রুত বুড়া করে, আর উপরের wire-গুলারে গরম করে, যেগুলা তখন electromigration-এ তাড়াতাড়ি নষ্ট হয়।
            Layout-এর জন্য: বেশি current-এর device-গুলারে এক চাপা block-এ ঠেসে দিয়েন না; finger ছড়ায়ে দেন, তাপের যাওয়ার জায়গা
            দেন, আর বেশি current-এর প্রত্যেকটা wire-এ electromigration-এর width আর via rule মানেন।
            """,
        ))
        self.clear()
        title = heading("4 · Heat stays in the fin")
        sub = box(-5.6, -2.6, -1.0, -1.6, SUBSTRATE, 1.0, 0)
        ox = box(-5.6, -1.6, -1.0, -1.1, OXIDE_FILL, 0.8, 0)
        fins = VGroup(*[box(x - 0.12, -1.6, x + 0.12, 0.4, SILICON, 1.0, 0) for x in (-4.3, -3.3, -2.3)])
        gate = box(-5.0, -1.1, -1.6, 0.8, GATE, 0.25)
        glow = VGroup(*[Circle(radius=0.45, stroke_width=0, fill_color=THERMAL, fill_opacity=0.35).move_to(f.get_center() + UP * 0.4)
                        for f in fins])
        heat_l = text("hotter than the chip around it", size=22, color=THERMAL).next_to(gate, UP, buff=0.4)
        path = Arrow([-3.3, -0.6, 0], [-3.3, -2.4, 0], buff=0, stroke_color=THERMAL, stroke_width=4)
        path_l = text("a narrow way out,\nthrough the fin's base", size=18, color=THERMAL).next_to(sub, DOWN, buff=0.15)
        words = VGroup(text("self-heating: less current,\nfaster ageing, hotter wires", size=24, weight="SEMIBOLD"),
                       text("electromigration: hot wires\nwear out sooner", size=22, color=INK),
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([3.3, 1.0, 0])
        note = layout_note("Spread high-current devices and their fingers; give the heat a path; follow the "
                           "electromigration width and via rules on every high-current wire.", size=20, width=42)
        note.move_to([3.3, -1.5, 0])
        tag = text("qualitative; not to scale", size=16, color=MUTED).to_corner(DR, buff=0.3)
        self.play(FadeIn(title), FadeIn(sub), FadeIn(ox), FadeIn(fins), FadeIn(gate), FadeIn(tag))
        self.play(FadeIn(glow), FadeIn(heat_l))
        self.play(GrowArrow(path), FadeIn(path_l))
        self.play(FadeIn(words))
        self.play(FadeIn(note, shift=UP * 0.1))

    def parasitics(self):
        self.slide(say(
            """
            Five: the parasitics close to the device. On advanced processes the contacts and vias
            are tiny, so their resistance is large, and the contact bar runs right beside the
            gate, so the gate-to-contact capacitance is large too. For analog, that's extra
            gate-to-drain capacitance and extra series resistance, on every device. The habits:
            redundant vias wherever there's room, short connections, symmetric routing for
            matched devices, and always check the extracted netlist, not just the schematic.
            """,
            """
            পাঁচ: device-এর একদম কাছের parasitic। Advanced process-এ contact আর via খুব ছোট, তাই তাদের resistance বড়, আর
            contact bar gate-এর ঠিক পাশে চলে, তাই gate-to-contact capacitance-ও বড়। Analog-এর জন্য এর মানে প্রত্যেকটা device-এ
            বাড়তি gate-to-drain capacitance আর বাড়তি series resistance। অভ্যাস: জায়গা থাকলে redundant via, ছোট connection,
            matched device-এর জন্য symmetric routing, আর সবসময় extracted netlist check করেন, শুধু schematic না।
            """,
        ))
        self.clear()
        title = heading("5 · Parasitics right at the device")
        gate = box(-3.4, -1.8, -2.9, 1.8, POLY, 0.75)
        md = VGroup(box(-4.6, -1.5, -4.0, 1.5, CONTACT, 0.5), box(-2.3, -1.5, -1.7, 1.5, CONTACT, 0.5))
        fins = VGroup(*[box(-5.2, y - 0.04, -1.1, y + 0.04, ACTIVE, 0.95, 1.0) for y in (-1.0, -0.4, 0.2, 0.8)])
        cap = VGroup(Line([-2.9, 0.45, 0], [-2.55, 0.45, 0], stroke_color=DRAIN, stroke_width=4),
                     Line([-2.55, 0.15, 0], [-2.55, 0.75, 0], stroke_color=DRAIN, stroke_width=4),
                     Line([-2.42, 0.15, 0], [-2.42, 0.75, 0], stroke_color=DRAIN, stroke_width=4),
                     Line([-2.42, 0.45, 0], [-2.3, 0.45, 0], stroke_color=DRAIN, stroke_width=4))
        cap_l = text("gate to contact:\nextra C_gd", size=20, color=DRAIN).move_to([-2.0, 2.45, 0])
        vias = VGroup(*[box(-2.12, y - 0.1, -1.88, y + 0.1, METAL, 0.95) for y in (-0.9, 0.0, 0.9)])
        via_l = text("redundant vias:\nless series R", size=20, color=METAL).move_to([-1.0, -2.35, 0])
        words = VGroup(text("tiny contacts and vias:\nlarge resistance", size=24, weight="SEMIBOLD"),
                       text("contact beside the gate:\nlarge capacitance", size=24, weight="SEMIBOLD"),
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([3.4, 1.1, 0])
        note = layout_note("Redundant vias where there's room, short connections, symmetric routing for matched "
                           "devices, and check the extracted netlist, not just the schematic.", size=20, width=42)
        note.move_to([3.9, -1.4, 0])
        self.play(FadeIn(title), FadeIn(fins), FadeIn(gate), FadeIn(md))
        self.play(Create(cap), FadeIn(cap_l))
        self.play(FadeIn(vias), FadeIn(via_l))
        self.play(FadeIn(words))
        self.play(FadeIn(note, shift=UP * 0.1))

    def antenna(self):
        self.slide(say(
            """
            Six: antennas. While the chip is being made, the metal layers are etched in a plasma,
            one level at a time. A long piece of metal connected to a gate, before the upper
            levels exist to tie it to a diffusion, collects charge from that plasma, and the only
            way out is through the gate's thin oxide. Enough charge damages it. The antenna rules
            limit how much metal area may hang on a gate, relative to the gate's area, at each
            level. The fixes: break the long run and jump up to a higher metal near the gate, or
            add a small diode to a diffusion that gives the charge a safe way out.
            """,
            """
            ছয়: antenna। Chip বানানোর সময় metal layer-গুলা plasma-তে etch করা হয়, এক স্তর এক স্তর করে। একটা gate-এর সাথে জোড়া
            লম্বা একটা metal-এর টুকরা, উপরের স্তরগুলা তৈরি হওয়ার আগে যেটা কোনো diffusion-এর সাথে বাঁধা না, ওই plasma থেকে charge জমায়,
            আর বের হওয়ার একমাত্র পথ gate-এর পাতলা oxide। যথেষ্ট charge জমলে oxide নষ্ট হয়। Antenna rule সীমা দেয়, প্রত্যেক স্তরে একটা
            gate-এ gate-এর area-র তুলনায় কতটা metal area ঝুলতে পারবে। সমাধান: লম্বা run-টা ভেঙে gate-এর কাছে উপরের metal-এ লাফ দেন,
            অথবা একটা ছোট diode দেন কোনো diffusion-এ, যেটা charge-রে নিরাপদে বের হওয়ার পথ দেয়।
            """,
        ))
        self.clear()
        title = heading("6 · Antennas")
        act = box(-4.8, -1.4, -3.4, -0.2, ACTIVE, 0.5)
        gate = box(-4.25, -1.7, -3.95, 0.4, POLY, 0.8)
        g_l = text("gate", size=20, color="#8F94F2").next_to(gate, DOWN, buff=0.12)
        wire = box(-4.2, 0.25, 3.0, 0.55, METAL, 0.8)
        w_l = text("a long metal run on the gate, before the upper levels connect it", size=20, color=METAL)
        w_l.move_to([0, 1.55, 0]).align_to(wire, LEFT)
        charges = VGroup(*[text("+", size=26, color=DRAIN, weight="BOLD").move_to([x, 0.9, 0]) for x in np.linspace(-3.4, 2.6, 10)])
        plasma = text("plasma etch", size=20, color=DRAIN).move_to([4.4, 0.9, 0])
        zap = Arrow([-4.1, 0.2, 0], [-4.1, -0.9, 0], buff=0, stroke_color=DRAIN, stroke_width=5)
        zap_l = text("out through the thin\ngate oxide: damage", size=20, color=DRAIN).next_to(act, RIGHT, buff=0.3)
        rule = text("antenna rule: metal area on a gate ÷ the gate's area, at each level", size=22, color=INK).to_edge(DOWN, buff=1.5)
        fixes = VGroup(text("fix 1: break the run, jump up to a higher metal near the gate", size=22, color=GOOD),
                       text("fix 2: a small diode to a diffusion, a safe way out for the charge", size=22, color=GOOD)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(title), FadeIn(act), FadeIn(gate), FadeIn(g_l), FadeIn(wire), FadeIn(w_l))
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.2) for c in charges], lag_ratio=0.08), FadeIn(plasma), run_time=1.2)
        self.play(GrowArrow(zap), FadeIn(zap_l))
        self.play(FadeIn(rule))
        self.play(FadeIn(fixes))

    def checklist(self):
        self.slide(say(
            """
            Here's the whole chapter as a checklist for every matched or sensitive device. Away
            from well edges, or the same distance from the same edge. The same SA and SB, the
            same distance to the diffusion breaks, dummies at the ends. The same neighbours and
            fill, and one orientation. Guard rings, and distance from anything noisy. Identical
            units around a common centre, with enough area.
            High-current devices spread out, with the electromigration rules met. The extracted
            netlist checked, with redundant vias and symmetric routing. And the antenna rules
            met.
            """,
            """
            পুরা chapter-টা প্রত্যেকটা matched বা sensitive device-এর জন্য একটা checklist হিসাবে। Well-এর কিনারা থেকে দূরে, বা একই
            কিনারা থেকে একই দূরত্বে। একই SA আর SB, diffusion break পর্যন্ত একই দূরত্ব, মাথায় dummy। একই প্রতিবেশী আর fill, আর এক
            orientation। Guard ring, আর গোলমেলে যেকোনো কিছু থেকে দূরত্ব। একই unit, একটা common center ঘিরে, যথেষ্ট area সহ। বেশি current-এর device ছড়ানো, electromigration rule
            মেনে। Extracted netlist check করা, redundant via আর symmetric routing সহ। আর antenna rule মানা।
            """,
        ))
        self.clear()
        title = heading("A checklist for every matched device")
        items = [
            "away from well edges, or the same distance from the same edge",
            "the same SA and SB, and distance to the diffusion breaks; dummies at the ends",
            "the same neighbours, spacings and fill; one orientation",
            "guard rings and distance between noisy and quiet blocks",
            "identical units, a common centre, enough area",
            "high-current devices spread out; electromigration rules met",
            "redundant vias, symmetric routing; the extracted netlist checked",
            "antenna rules met: a jump up near the gate, or a diode",
        ]
        rows = VGroup()
        for s in items:
            tick = Square(side_length=0.28, stroke_color=GATE, stroke_width=2.5)
            rows.add(VGroup(tick, text(s, size=24, color=INK)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24).move_to([0, -0.35, 0])
        self.play(FadeIn(title))
        for r in rows:
            c = r[0].get_center()
            mark = VMobject(stroke_color=GOOD, stroke_width=5).set_points_as_corners(
                [c + [-0.1, 0.0, 0], c + [-0.02, -0.1, 0], c + [0.13, 0.12, 0]])
            self.play(FadeIn(r, shift=RIGHT * 0.1), FadeIn(mark), run_time=0.5)

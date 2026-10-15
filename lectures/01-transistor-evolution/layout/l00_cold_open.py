"""Layout edition · L0 · The picture on your screen.

Poly crossing diffusion: the picture a layout engineer has looked at since 1971. What it means
has changed three times, and the talk follows those changes.
"""

import sys
from pathlib import Path

LECTURE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(LECTURE.parents[1]), str(LECTURE), str(LECTURE / "layout")]

from manim import *  # noqa: E402,F403
from manim_slides import Slide  # noqa: E402

from common import ACTIVE, POLY, box  # noqa: E402
from devicedata import device  # noqa: E402
from kit.devices3d import LAYOUT_OPACITY, plan_view  # noqa: E402
from kit.style import *  # noqa: E402,F403

IMAGES = LECTURE / "images"
WALL_C = "#7A8AA0"  # FET Lab's dielectric wall


class L00ColdOpen(Chapter, Slide):
    def construct(self):
        self.title()
        self.then()
        self.now()
        self.map()

    def title(self):
        self.slide(say(
            """
            This is lecture one, in its layout edition. It's the same story as the full
            lecture: how the transistor went from a flat channel to fins, sheets, and stacks.
            But we'll tell it from your side of the screen: what each device looks like in a
            layout tool, what you draw and size, what's fixed for you, and what the
            surroundings do to it. The physics comes one sentence at a time, only where it
            explains a rule you follow.
            """,
            """
            এইটা lecture one, layout edition। Full lecture-এর একই গল্প: transistor কিভাবে flat channel থেকে fin,
            sheet আর stack-এ গেল। কিন্তু বলব আপনার screen-এর দিক থেকে: layout tool-এ প্রত্যেকটা device দেখতে
            কেমন, আপনি কী আঁকেন আর size করেন, কী আপনার জন্য fixed, আর আশেপাশের জিনিস এর উপর কী করে। Physics
            আসবে এক লাইন করে, শুধু যেখানে সেইটা আপনার মানা কোনো rule-এর কারণ বুঝায়।
            """,
        ))
        kick = kicker("Lecture 1 · layout edition", color=GATE)
        ttl = display("What You Draw, and Why It Changed", size=54)
        sub = text("The transistor from planar to CFET, seen from the layout side", size=30, color=MUTED)
        VGroup(kick, ttl, sub).arrange(DOWN, buff=0.3).move_to(UP * 0.4)
        self.play(FadeIn(kick), Write(ttl), run_time=1.6)
        self.play(FadeIn(sub))

    def then(self):
        fig = figure(IMAGES / "intel4004_layout_1971.jpg", 5.6,
                     "Intel 4004 layout drawing, 1971. Photo: Flickr user stiefkind, CC0").move_to(DOWN * 0.4)
        self.show_figure(say(
            """
            1971. This is part of the layout of the Intel 4004, the first microprocessor, drawn
            by hand, at a time when a layout was a drawing on a light table. Look closely and
            every transistor is the same picture: a strip of polysilicon crossing a strip of
            diffusion. Where they cross, there's a transistor. Fifty-five years later, that's
            still the picture on your screen.
            """,
            """
            1971। এইটা Intel 4004-এর layout-এর একটা অংশ, প্রথম microprocessor, হাতে আঁকা, এমন সময়ের যখন layout
            মানে light table-এর উপর একটা drawing। ভালো করে দেখলে প্রত্যেকটা transistor একই ছবি: diffusion-এর একটা
            ফালির উপর দিয়া polysilicon-এর একটা ফালি পার হইছে। যেখানে পার হয়, সেখানে transistor। পঞ্চান্ন বছর পরেও
            আপনার screen-এ ছবিটা এইটাই।
            """,
        ), "1971: poly crossing diffusion", fig, clear=VGroup(*self.mobjects))
        self.fig = fig

    def now(self):
        self.slide(say(
            """
            And here's a FinFET inverter today, from above, the way your tool draws it. Still
            lines crossing lines: the gate runs up the page, and where it crosses the active,
            there's a transistor. But the active isn't one rectangle any more. It's a set of
            thin fins, all the same, on one fixed pitch. The picture looks familiar; what it
            means has changed. That change, three times over, is this talk.
            """,
            """
            আর এই যে আজকের একটা FinFET inverter, উপর থেকে, আপনার tool যেভাবে আঁকে। এখনো লাইনের উপর লাইন: gate
            page-এর উপর-নিচে চলে, আর active-এর উপর দিয়া যেখানে পার হয়, সেখানে transistor। কিন্তু active আর একটা
            rectangle না। এইটা কয়েকটা পাতলা fin, সব একরকম, একটা fixed pitch-এ। ছবিটা চেনা লাগে; মানেটা বদলায়ে গেছে।
            ওই বদল, তিনবার, এইটাই আজকের talk।
            """,
        ))
        self.clear()
        title = heading("Today: a FinFET inverter, from above")
        layout = device("show_fin")
        view, by = plan_view(layout, scale=0.03, skip=("pwell", "fox"), opacity=LAYOUT_OPACITY)
        view.move_to([-2.4, -0.4, 0])
        mat = {p["id"]: p["material"] for p in layout["parts"]}
        fins = VGroup(*[s for pid, s in by.items() if mat[pid] == "nanowire"])
        wells = VGroup(*[s for pid, s in by.items() if mat[pid] in ("nwell", "pwell")])
        gate = by["po"]
        top = VGroup(*[s for pid, s in by.items() if mat[pid] in ("md", "vd", "vg", "m0")])
        tag = text("Schematic: FET Lab's FinFET inverter layout (model)", size=16, color=MUTED).next_to(view, DOWN, buff=0.2)
        l_fins = text("fins: the active,\nnow on a fixed pitch", size=24, color=ACTIVE).move_to([3.4, 1.5, 0])
        l_gate = text("the gate (poly)", size=24, color="#8F94F2").move_to([3.4, 0.0, 0])
        l_top = text("then contacts and metal on top", size=24, color=MUTED).move_to([3.4, -1.4, 0])
        fin = max(fins, key=lambda f: f.get_center()[1])
        a1 = Arrow(l_fins.get_left(), fin.get_right(), buff=0.15, stroke_color=ACTIVE, stroke_width=3)
        a2 = Arrow(l_gate.get_left(), gate.get_right() + LEFT * 0.05, buff=0.15, stroke_color="#8F94F2", stroke_width=3)
        self.play(FadeIn(title), FadeIn(wells), FadeIn(tag))
        self.play(FadeIn(fins), FadeIn(l_fins), GrowArrow(a1))
        self.play(FadeIn(gate), FadeIn(l_gate), GrowArrow(a2))
        self.play(FadeIn(top), FadeIn(l_top))

    def map(self):
        self.slide(say(
            """
            Here's the route. The planar transistor, where you drew W and L. The FinFET, where
            the width comes in whole fins. The nanosheet, where you draw the width again. Then
            two on the roadmap that squeeze n and p together: the forksheet, with a wall
            between them, and the CFET, with one stacked on the other. And then the part that
            never goes away: where you put a device changes what it does.
            """,
            """
            Route-টা এই। Planar transistor, যেখানে আপনি W আর L আঁকতেন। FinFET, যেখানে width আসে whole fin-এ।
            Nanosheet, যেখানে width আবার আঁকেন। তারপর roadmap-এর দুইটা, যেগুলা n আর p-রে কাছাকাছি চাপে: forksheet,
            মাঝখানে একটা wall, আর CFET, একটার উপর আরেকটা। আর শেষে সেই অংশ যেটা কখনো যায় না: device কোথায় বসাইলেন,
            তাতেই বদলায় সে কী করে।
            """,
        ))
        self.clear()
        title = heading("The route")
        icons = [
            (self.icon_planar(), "planar", "you draw W and L"),
            (self.icon_fin(), "FinFET", "you pick fins"),
            (self.icon_sheet(), "nanosheet", "you draw width again"),
            (self.icon_fork(), "forksheet", "a wall between n and p"),
            (self.icon_cfet(), "CFET", "n stacked on p"),
        ]
        cols = VGroup()
        for i, (ic, name, what) in enumerate(icons):
            col = VGroup(ic, text(name, size=26, weight="SEMIBOLD"), text(what, size=19, color=MUTED)).arrange(DOWN, buff=0.22)
            if i >= 3:
                col.add(text("roadmap", size=16, color=MUTED, slant="ITALIC").next_to(col, DOWN, buff=0.1))
            cols.add(col)
        cols.arrange(RIGHT, buff=0.55, aligned_edge=UP).move_to(UP * 0.35)
        nb = text("…and through all of them: where you put a device changes what it does", size=26, color=GATE)
        nb.to_edge(DOWN, buff=0.9)
        self.play(FadeIn(title))
        for c in cols:
            self.play(FadeIn(c, shift=UP * 0.15), run_time=0.7)
        self.play(FadeIn(nb))

    # --- top-view icons, 1.6 units across ----------------------------------------------------
    @staticmethod
    def _gate():
        return box(-0.14, -0.85, 0.14, 0.85, POLY, 0.8)

    def icon_planar(self):
        return VGroup(box(-0.8, -0.5, 0.8, 0.5, ACTIVE, 0.5), self._gate())

    def icon_fin(self):
        fins = VGroup(*[box(-0.8, y - 0.035, 0.8, y + 0.035, ACTIVE, 0.95) for y in (-0.45, -0.15, 0.15, 0.45)])
        return VGroup(fins, self._gate())

    def icon_sheet(self):
        return VGroup(box(-0.8, -0.3, 0.8, 0.3, ACTIVE, 0.9), self._gate())

    def icon_fork(self):
        n = box(-0.8, -0.55, 0.8, -0.08, ACTIVE, 0.9)
        p = box(-0.8, 0.08, 0.8, 0.55, ACTIVE, 0.9)
        wall = box(-0.8, -0.04, 0.8, 0.04, WALL_C, 1.0)
        return VGroup(n, p, wall, self._gate())

    def icon_cfet(self):
        lower = box(-0.74, -0.36, 0.86, 0.24, ACTIVE, 0.45)
        upper = box(-0.86, -0.24, 0.74, 0.36, ACTIVE, 0.95)
        return VGroup(lower, upper, self._gate())

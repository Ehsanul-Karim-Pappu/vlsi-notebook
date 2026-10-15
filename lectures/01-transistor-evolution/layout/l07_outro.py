"""Layout edition · L7 · What changed in what you draw.

One table, planar to CFET, and a closing word.
"""

import sys
from pathlib import Path

LECTURE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(LECTURE.parents[1]), str(LECTURE), str(LECTURE / "layout")]

from manim import *  # noqa: E402,F403
from manim_slides import Slide  # noqa: E402

from common import knob_table  # noqa: E402
from kit.style import *  # noqa: E402,F403


class L07Outro(Chapter, Slide):
    def construct(self):
        self.summary()
        self.thanks()

    def summary(self):
        self.slide(say(
            """
            So here's the whole talk on one slide. Planar: you drew W and L, with fingers and
            multipliers, inside wells and taps. FinFET: the width became whole fins, the length a
            short list, and you started placing dummy gates and diffusion breaks on fixed grids.
            Nanosheet: the width is drawn again, the stack is the process's, and power is moving
            to the back. Forksheet and CFET, if they arrive: a wall to place, then n and p in one
            footprint, wired on both sides. And on every one of them, the neighbourhood matters.
            """,
            """
            তো পুরা talk এক slide-এ। Planar: আপনি W আর L আঁকতেন, finger আর multiplier সহ, well আর tap-এর ভিতরে। FinFET: width
            হইলো whole fin, length একটা ছোট তালিকা, আর fixed grid-এ dummy gate আর diffusion break বসানো শুরু করলেন। Nanosheet:
            width আবার আঁকা, stack process-এর, আর power পেছনে চলে যাইতেছে। Forksheet আর CFET, যদি আসে: বসানোর মতো একটা wall,
            তারপর n আর p এক footprint-এ, দুই দিকে wiring। আর এই প্রত্যেকটায়, আশেপাশেটা গুরুত্বপূর্ণ।
            """,
        ))
        title = heading("What changed in what you draw")
        table = knob_table([
            ["", "you size", "fixed for you", "new around it"],
            ["planar", "W, L, nf, m", "—", "wells, taps"],
            ["FinFET", "fins, nf, m;\na few lengths", "fin height and pitch;\ngate pitch", "dummy gates, diffusion\nbreaks, MD and M0"],
            ["nanosheet", "sheet width (a range),\nnf, m", "sheet count\nand thickness", "power from the back"],
            ["forksheet*", "sheet width", "the wall", "a wall to place"],
            ["CFET*", "sheet width, per tier", "the stack", "vertical links;\nwiring on both sides"],
        ], col_w=(2.3, 3.4, 3.5, 3.7), size=22).move_to([0, -0.15, 0])
        foot = VGroup(text("* on the roadmap", size=18, color=MUTED),
                      text("and on every one: the neighbourhood matters (chapter 6)", size=22, color=GATE)
                      ).arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(title), FadeIn(table[0][0]), FadeIn(table[1]))
        for row in table[0][1:]:
            self.play(FadeIn(row, shift=UP * 0.1), run_time=0.6)
        self.play(FadeIn(foot))

    def thanks(self):
        self.slide(say(
            """
            The picture on your screen is still lines crossing lines. What changed is what each
            line means, and what's left for you to decide. Thank you. Questions?
            """,
            """
            আপনার screen-এর ছবিটা এখনো লাইনের উপর লাইন। বদলাইছে প্রত্যেকটা লাইনের মানে, আর আপনার হাতে কী সিদ্ধান্ত বাকি থাকে
            সেইটা। ধন্যবাদ। প্রশ্ন?
            """,
        ))
        self.clear()
        a = text("Still lines crossing lines.", size=46, weight="SEMIBOLD")
        b = text("What changed is what each one means, and what's left for you to decide.", size=28, color=MUTED)
        c = display("Thank you", size=64, color=GATE)
        VGroup(a, b, c).arrange(DOWN, buff=0.5).move_to(UP * 0.2)
        self.play(FadeIn(a))
        self.play(FadeIn(b))
        self.play(FadeIn(c, shift=UP * 0.15))

"""Lecture 3 · X6 · Keeping the core away from injectors.

What counts as an injector, how a deck finds one (marker layers and connectivity from the pad),
the distance band around the I/O, the analog pin that brings an injector into your block, and the
fixes.
"""

import sys
from pathlib import Path

LECTURE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(LECTURE.parents[1]), str(LECTURE)]

from manim import *  # noqa: E402,F403
from manim_slides import Slide  # noqa: E402

from common import NPLUS, PPLUS, box, ring, card_box, chapter_title, marker, pdk_tag  # noqa: E402
from kit.style import *  # noqa: E402,F403


class X06Injectors(Chapter, Slide):
    def construct(self):
        self.card()
        self.what()
        self.finding()
        self.band()
        self.analog_pin()
        self.fixes()

    def card(self):
        self.slide(say(
            """
            Chapter six: keeping the core away from injectors. Guard rings catch most of what an
            injector sprays, but not all of it, and minority carriers travel far. So the second
            line of defence is plain distance.
            """,
            """
            Chapter six: core-রে injector থেকে দূরে রাখা। Guard ring একটা injector যা ছিটায় তার বেশিরভাগই ধরে, কিন্তু সবটা না, আর
            minority carrier অনেক দূর যায়। তাই প্রতিরক্ষার দ্বিতীয় লাইন হইল সোজাসাপ্টা দূরত্ব।
            """,
        ))
        self.card_group = chapter_title(6, "Keeping the core away from injectors", "Distance, and how the deck measures it")
        self.play(FadeIn(self.card_group, shift=UP * 0.2), run_time=1.2)

    def what(self):
        self.slide(say(
            """
            What counts as an injector? Any diffusion that the outside world can forward-bias. The
            N+ and P+ drains of output drivers. The diodes and clamps of ESD protection, which are
            designed to conduct. Any diffusion connected straight to a pad, including the input of
            an analog block. And, less obviously, any junction that a badly sequenced or wrongly
            tied supply can forward-bias, which is chapter seven.
            """,
            """
            Injector কোনগুলা? যেকোনো diffusion যেটা বাইরের দুনিয়া forward-bias করতে পারে। Output driver-এর N+ আর P+ drain। ESD
            protection-এর diode আর clamp, যেগুলা conduct করার জন্যই বানানো। Pad-এ সরাসরি যুক্ত যেকোনো diffusion, একটা analog block-এর
            input সহ। আর, একটু কম চোখে পড়ে এমন, ভুল ক্রমে চালু হওয়া বা ভুল জায়গায় বাঁধা supply যে junction forward-bias করতে পারে, যেইটা
            chapter seven।
            """,
        ))
        self.play(FadeOut(self.card_group))
        title = heading("What counts as an injector")
        cards = VGroup(
            card_box("Output drivers", [text("the N+ and P+ drains\non the pad", size=20, color=INK)], width=5.4, height=1.6, head_size=22),
            card_box("ESD devices", [text("diodes and clamps,\nbuilt to conduct", size=20, color=INK)], width=5.4, height=1.6, head_size=22),
            card_box("Analog pins", [text("a switch or a device\nwired straight to a pad", size=20, color=INK)], width=5.4, height=1.6, head_size=22),
            card_box("Wrong supplies", [text("a well or a junction\nforward-biased by a supply", size=20, color=INK)], width=5.4, height=1.6,
                     head_size=22, head_color=MUTED),
        ).arrange_in_grid(rows=2, cols=2, buff=0.3).move_to(DOWN * 0.1)
        rule = text("any diffusion the outside world can forward-bias", size=26, color=GATE).to_edge(DOWN, buff=0.8)
        self.play(FadeIn(title))
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in cards], lag_ratio=0.25), run_time=1.8)
        self.play(FadeIn(rule))

    def finding(self):
        self.slide(say(
            """
            How does a DRC deck know which diffusion is an injector? It can't tell from the shape.
            It follows connectivity. The pads carry a marker or a text label; the deck traces the
            net from each pad down through the metal and vias to every diffusion it touches, and
            calls those injectors. Some decks also ask you to draw a marker layer over I/O and ESD
            cells, or over any analog pin. Then it grows each injector by the rule distance, and
            anything sensitive inside that band, without the required ring, is flagged. Which
            means a missing pad label or a missing marker can hide an injector from the deck
            entirely.
            """,
            """
            একটা DRC deck কিভাবে জানে কোন diffusion injector? আকার দেখে বলতে পারে না। এইটা connectivity অনুসরণ করে। Pad-গুলাতে একটা
            marker বা text label থাকে; deck প্রত্যেকটা pad থেকে net-টা metal আর via দিয়া নিচে প্রত্যেকটা diffusion পর্যন্ত trace করে যেটা
            ছোঁয়, আর সেগুলারে injector বলে। কিছু deck আপনারে I/O আর ESD cell-এর উপর, বা যেকোনো analog pin-এর উপর একটা marker layer-ও
            আঁকতে বলে। তারপর প্রত্যেকটা injector-রে rule-এর দূরত্ব দিয়া বড় করে, আর ওই band-এর ভিতরে প্রয়োজনীয় ring ছাড়া sensitive যা
            আছে, সেইটা flag করে। মানে একটা হারানো pad label বা marker একটা injector-রে deck-এর চোখ থেকে পুরাপুরি লুকাতে পারে।
            """,
        ))
        self.clear()
        title = heading("How the deck finds an injector")
        steps = ["pad label\nor marker", "trace the net\nthrough metal", "diffusions on it:\nINJECTOR", "SIZE by the rule:\nthe band",
                 "sensitive shapes\ninside: error"]
        colors = [GATE, METAL, DRAIN, DRAIN, DRAIN]
        boxes = VGroup()
        for s, c in zip(steps, colors):
            r = RoundedRectangle(width=2.3, height=1.3, corner_radius=0.12, stroke_color=c, stroke_width=3, fill_color=PANEL, fill_opacity=1)
            boxes.add(VGroup(r, text(s, size=19, color=INK).move_to(r)))
        boxes.arrange(RIGHT, buff=0.35).move_to(UP * 0.4)
        arrows = VGroup(*[Arrow(boxes[k].get_right(), boxes[k + 1].get_left(), buff=0.05, stroke_color=MUTED, stroke_width=3)
                          for k in range(len(boxes) - 1)])
        warn = text("no label, no marker: the deck never sees the injector", size=24, color=DRAIN).move_to(DOWN * 1.6)
        tag = pdk_tag().to_corner(DR, buff=0.3)
        self.play(FadeIn(title), FadeIn(tag))
        for k, b in enumerate(boxes):
            self.play(FadeIn(b, shift=RIGHT * 0.1), *([GrowArrow(arrows[k - 1])] if k else []), run_time=0.6)
        self.play(FadeIn(warn))

    def band(self):
        self.slide(say(
            """
            On the floorplan, it looks like this. The pads and I/O cells around the edge, each one
            surrounded by its band. A core block that stays outside the bands is fine. One that
            reaches inside needs a ring between it and the injector, or it gets a marker, like the
            corner of this block here. The bands are wide, often tens of microns, which is why
            pad-limited designs leave a moat between the I/O ring and the core, and why you should
            check the band before you commit an analog block's position near the edge.
            """,
            """
            Floorplan-এ এইটা দেখতে এমন। কিনারা ঘিরে pad আর I/O cell, প্রত্যেকটা তার band দিয়া ঘেরা। যে core block band-এর বাইরে থাকে,
            সেইটা ঠিক আছে। যেইটা ভিতরে ঢুকে, তার আর injector-এর মাঝে একটা ring লাগবে, নইলে একটা marker পায়, এই block-এর কোণাটার মতো।
            Band-গুলা চওড়া, প্রায়ই কয়েক দশ micron, এই জন্যই pad-limited design-এ I/O ring আর core-এর মাঝে একটা পরিখা রাখা হয়, আর এই
            জন্যই কিনারার কাছে একটা analog block-এর জায়গা ঠিক করার আগে band check করা উচিত।
            """,
        ))
        self.clear()
        title = heading("The band around the I/O")
        die = Rectangle(width=11.0, height=5.6, stroke_color=MUTED, stroke_width=3, fill_color=PANEL, fill_opacity=1).move_to(DOWN * 0.4)
        pads = VGroup()
        for k in range(9):
            x = -4.8 + k * 1.2
            for y in (die.get_top()[1] - 0.35, die.get_bottom()[1] + 0.35):
                pads.add(Square(0.5, stroke_width=0, fill_color=FAINT, fill_opacity=1).move_to([x, y, 0]))
        io = VGroup(*[box(-5.2, y - 0.25, 5.2, y + 0.25, GATE, 0.35, 0) for y in (die.get_top()[1] - 0.95, die.get_bottom()[1] + 0.95)])
        band = VGroup(*[box(-5.4, y0, 5.4, y1, DRAIN, 0.12, 0) for y0, y1 in (
            (die.get_top()[1] - 1.85, die.get_top()[1] - 0.65), (die.get_bottom()[1] + 0.65, die.get_bottom()[1] + 1.85))])
        band_l = text("injector band", size=18, color=DRAIN).next_to(band[0], DOWN, buff=0.08).align_to(band[0], RIGHT)
        io_l = text("I/O cells", size=18, color=GATE).move_to([-4.3, die.get_top()[1] - 0.95, 0])
        ok = box(-4.6, -1.6, -1.2, 0.6, NWELL, 0.6, 2)
        ok_l = text("core block: outside", size=18, color=GOOD).move_to(ok)
        bad = box(0.6, -1.6, 4.4, 1.25, NWELL, 0.6, 2)
        bad_l = text("analog block", size=18, color=INK).move_to(bad).shift(DOWN * 0.3)
        poke = box(0.6, 0.85, 4.4, 1.25, DRAIN, 0.5, 0)
        mk = marker(poke, "LUP.IO.1", buff=0.05)
        tag = pdk_tag().to_corner(DR, buff=0.3)
        self.play(FadeIn(title), FadeIn(die), FadeIn(pads), FadeIn(io), FadeIn(io_l), FadeIn(tag))
        self.play(FadeIn(band), FadeIn(band_l))
        self.play(FadeIn(ok), FadeIn(ok_l))
        self.play(FadeIn(bad), FadeIn(bad_l))
        self.play(FadeIn(poke), FadeIn(mk))

    def analog_pin(self):
        self.slide(say(
            """
            For analog layout engineers, this one matters most. An analog input often goes from
            the pad, through the ESD, straight into your block: to a sampling switch, a resistor,
            the gate and drain of an input device. The diffusion at the end of that wire is an
            injector, and it's sitting inside your block, next to your matched pairs and your
            bandgap. Treat it like an I/O device: put its own double guard ring around it, keep
            sensitive devices away from it, and check that the deck actually recognised it, with
            a marker if your PDK asks for one.
            """,
            """
            Analog layout engineer-দের জন্য, এইটাই সবচেয়ে গুরুত্বপূর্ণ। একটা analog input প্রায়ই pad থেকে ESD হয়ে সরাসরি আপনার
            block-এ যায়: একটা sampling switch, একটা resistor, একটা input device-এর gate আর drain। ওই wire-এর শেষের diffusion-টা একটা
            injector, আর সেইটা আপনার block-এর ভিতরে বসা, আপনার matched pair আর bandgap-এর পাশে। এরে একটা I/O device-এর মতো ধরেন:
            এর চারপাশে আলাদা double guard ring দেন, sensitive device-গুলা দূরে রাখেন, আর check করেন deck এইটারে আসলেই চিনছে কিনা,
            আপনার PDK চাইলে একটা marker দিয়া।
            """,
        ))
        self.clear()
        title = heading("The analog pin: an injector inside your block")
        pad = Square(1.0, stroke_width=0, fill_color=FAINT, fill_opacity=1).move_to([-5.6, 0.4, 0])
        pad_l = text("pad", size=20, color=MUTED).next_to(pad, DOWN, buff=0.1)
        esd = RoundedRectangle(width=1.4, height=1.0, corner_radius=0.08, stroke_color=GATE, stroke_width=3).move_to([-3.6, 0.4, 0])
        esd_l = text("ESD", size=20, color=GATE).move_to(esd)
        blk = RoundedRectangle(width=7.4, height=4.2, corner_radius=0.12, stroke_color=MUTED, stroke_width=2).move_to([2.6, 0.0, 0])
        blk_l = text("your analog block", size=20, color=MUTED).next_to(blk, UP, buff=0.1).align_to(blk, LEFT)
        sw = box(-0.2, 0.0, 0.6, 0.8, NPLUS, 0.6, 2)
        sw_l = text("switch", size=16, color=INK).next_to(sw, DOWN, buff=0.75)
        ring_in = ring(sw.get_center(), 1.7, 1.7, 0.13, PPLUS)
        ring_out = ring(sw.get_center(), 2.3, 2.3, 0.13, NPLUS)
        wire = VMobject(stroke_color=METAL, stroke_width=5).set_points_as_corners([pad.get_right(), esd.get_left()])
        wire2 = VMobject(stroke_color=METAL, stroke_width=5).set_points_as_corners([esd.get_right(), [sw.get_left()[0] - 1.3, 0.4, 0], sw.get_left()])
        pair = VGroup(*[box(3.4 + k * 0.6, -1.6, 3.8 + k * 0.6, -0.6, ELECTRON, 0.35, 2) for k in range(4)])
        pair_l = text("matched pair", size=16, color=INK).next_to(pair, DOWN, buff=0.1)
        bg = box(3.3, 0.6, 5.6, 1.6, GATE, 0.25, 2)
        bg_l = text("bandgap", size=16, color=INK).move_to(bg)
        note = VGroup(text("its own double guard ring", size=20, color=GOOD),
                      text("distance to anything sensitive", size=20, color=GOOD),
                      text("a marker, if the PDK asks", size=20, color=GOOD)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        note.next_to(blk, DOWN, buff=0.2).align_to(blk, LEFT)
        self.play(FadeIn(title), FadeIn(pad), FadeIn(pad_l), FadeIn(esd), FadeIn(esd_l), FadeIn(blk), FadeIn(blk_l))
        self.play(Create(wire), Create(wire2), FadeIn(sw), FadeIn(sw_l), FadeIn(pair), FadeIn(pair_l), FadeIn(bg), FadeIn(bg_l))
        self.play(Indicate(sw, color=DRAIN, scale_factor=1.3))
        self.play(FadeIn(ring_in), FadeIn(ring_out), FadeIn(note))

    def fixes(self):
        self.slide(say(
            """
            The fixes, again in two columns. Ones that work: move the sensitive block out of the
            band; add a collector ring between the injector and the victim; give the injector its
            own double ring; add series resistance between the pad and the diffusion, where the
            circuit allows, to limit the current. And ones that only silence the checker: deleting
            or shrinking the marker layer, relabelling the pad so the trace stops, or a waiver
            that says it's fine because it was fine last time.
            """,
            """
            সমাধানগুলা, আবার দুই column-এ। যেগুলা কাজ করে: sensitive block-রে band-এর বাইরে সরান; injector আর victim-এর মাঝে একটা
            collector ring দেন; injector-রে তার নিজের double ring দেন; circuit অনুমতি দিলে pad আর diffusion-এর মাঝে series resistance
            দেন, current সীমিত করতে। আর যেগুলা শুধু checker-রে চুপ করায়: marker layer মুছে ফেলা বা ছোট করা, pad-এর label বদলানো যাতে
            trace থেমে যায়, বা একটা waiver যেটা বলে এইটা ঠিক আছে কারণ গতবার ঠিক ছিল।
            """,
        ))
        self.clear()
        title = heading("Fixing an injector error")
        good = VGroup(text("Fixes that work", size=28, color=GOOD, weight="SEMIBOLD"),
                      *[text(s, size=22, color=INK) for s in ("move the sensitive block out of the band",
                                                              "a collector ring between injector and victim",
                                                              "the injector's own double guard ring",
                                                              "series resistance from the pad, if the circuit allows")]
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        bad = VGroup(text("Fixes that only silence it", size=28, color=DRAIN, weight="SEMIBOLD"),
                     *[text(s, size=22, color=INK) for s in ("shrinking or deleting the marker",
                                                             "relabelling the pad",
                                                             "\"it was fine last time\"")]).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        VGroup(good, bad).arrange(RIGHT, buff=0.9, aligned_edge=UP).move_to(DOWN * 0.2)
        self.play(FadeIn(title), FadeIn(good, shift=UP * 0.1))
        self.play(FadeIn(bad, shift=UP * 0.1))

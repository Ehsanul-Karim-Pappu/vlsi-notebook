"""Checks the lecture: every chapter defines its scene and has notes in both languages, every
schematic it shows exists, and the arithmetic behind the arrangements says what the slides and the
lab say it does.

Run from the repository root:  python -m unittest discover lectures/02-matching-and-symmetry/tests
"""

import ast
import re
import sys
import unittest
from pathlib import Path

import numpy as np

LECTURE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(LECTURE.parents[1]), str(LECTURE)]

BANGLA = ("ঀ", "৿")


def has_bangla(s):
    return any(BANGLA[0] <= c <= BANGLA[1] for c in s)


# The lab's model (labs/lab1_placement.html), ported: a straight gradient of STRENGTH mV across
# 8 unit pitches at ANGLE degrees, plus a bowl centred 3 pitches left and 1 down, CUR / 10 mV per
# pitch squared. Positions are in unit pitches from the array's centre.
def lab_field(x, y, angle=0.0, strength=2.0, cur=0.0):
    a = np.radians(angle)
    lin = strength / 8 * (x * np.cos(a) + y * np.sin(a))
    return lin + cur / 10 * ((x + 3) ** 2 + (y + 1) ** 2)


def lab_mismatch(rows, **field):
    cols, n = max(len(r) for r in rows), len(rows)
    vals = {"A": [], "B": []}
    for i, r in enumerate(rows):
        for j, ch in enumerate(r):
            if ch in vals:
                vals[ch].append(lab_field(j - (cols - 1) / 2, (n - 1) / 2 - i, **field))
    return np.mean(vals["A"]) - np.mean(vals["B"])


class Chapters(unittest.TestCase):
    def test_every_chapter_and_its_notes(self):
        from build import SEQUENCE

        for step in SEQUENCE:
            if step[0] == "lab":
                self.assertTrue((LECTURE / "labs" / step[1]).exists(), step[1])
                self.assertTrue(has_bangla(step[3][1]), f"{step[1]}: Bangla notes")
                continue
            source = (LECTURE / step[1]).read_text()
            tree = ast.parse(source)
            with self.subTest(scene=step[2]):
                self.assertIn(step[2], [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)])
                says = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and getattr(n.func, "id", "") == "say"]
                self.assertTrue(says)
                for call in says:
                    en, bn = (ast.literal_eval(a) for a in call.args)
                    self.assertTrue(en.strip() and not has_bangla(en), f"{step[2]} line {call.lineno}: English")
                    self.assertTrue(has_bangla(bn), f"{step[2]} line {call.lineno}: Bangla")
                for name in re.findall(r'Schematic\("(\w+)"', source):
                    for ext in (".json", ".svg", ".png"):
                        self.assertTrue((LECTURE / "schematics" / (name + ext)).exists(), name + ext)

    def test_rings_name_real_devices(self):
        """Every device a slide rings is a symbol in that schematic."""
        import json

        for f in sorted((LECTURE / "chapters").glob("m*.py")):
            source = f.read_text()
            for var, name in re.findall(r'(\w+) = Schematic\("(\w+)"', source):
                ids = {s["id"] for s in json.loads((LECTURE / "schematics" / f"{name}.json").read_text())["symbols"]}
                for group in re.findall(rf"{var}\.ring\(\[([^\]]*)\]", source):
                    for dev in re.findall(r'"(\w+)"', group):
                        self.assertIn(dev, ids, f"{f.name}: {dev} on {name}")

    def test_lab_buttons_match_the_notes(self):
        from build import PLACEMENT_LAB

        html = (LECTURE / "labs" / PLACEMENT_LAB[1]).read_text()
        buttons = re.findall(r'<button class="ghost" data-p="\w+">([^<]+)</button>', html)
        for name in ("Side by side", "Interdigitated", "Mirrored", "Cross-quad"):
            self.assertIn(name, buttons)
            self.assertIn(name, PLACEMENT_LAB[3][0])
        self.assertTrue((LECTURE / "images" / "labs" / "lab1_placement.jpg").exists())


class Arrangements(unittest.TestCase):
    """What chapter 3 and the lab say each arrangement leaves, in the lab's model."""

    def test_the_lab_uses_this_model(self):
        html = (LECTURE / "labs" / "lab1_placement.html").read_text()
        self.assertIn("(+ui.str.value / 8)", html)
        self.assertIn("const bx = x + 3, by = y + 1;", html)
        self.assertIn("(+ui.cur.value / 10)", html)

    def test_straight_gradient(self):
        side = lab_mismatch(["AAAABBBB"])
        self.assertAlmostEqual(abs(side), 1.0)  # 2 mV across 8 pitches, centroids 4 apart
        self.assertAlmostEqual(lab_mismatch(["ABABABAB"]) / side, 0.25)  # a quarter left
        for angle in range(0, 181, 15):
            for rows in (["ABBAABBA"], ["ABBA", "BAAB"], ["DDDDDD", "DABBAD", "DBAABD", "DDDDDD"]):
                self.assertAlmostEqual(lab_mismatch(rows, angle=angle), 0.0, msg=f"{rows} at {angle}°")

    def test_curvature(self):
        # the long mirrored row keeps some; the cross-quad, folded, keeps none (for this bowl)
        self.assertGreater(abs(lab_mismatch(["ABBAABBA"], cur=2)), 0.1)
        self.assertAlmostEqual(lab_mismatch(["ABBA", "BAAB"], cur=2), 0.0)
        # the bandgap's 1 : 8 cancels a straight gradient but not a bowl
        bg = ["BBB", "BAB", "BBB"]
        self.assertAlmostEqual(lab_mismatch(bg, angle=40), 0.0)
        self.assertGreater(abs(lab_mismatch(bg, cur=2)), 0.1)

    def test_slide_arrangements(self):
        """common.placed, which draws chapter 3's and chapter 7's leftover meters, agrees."""
        try:
            from common import placed
        except ImportError as e:  # Manim isn't installed
            self.skipTest(str(e))
        base = placed(["AAAABBBB"]).error
        self.assertAlmostEqual(placed(["ABABABAB"]).error / base, 0.25, places=6)
        for angle in (0.0, 0.8, 1.57, 2.4):
            self.assertAlmostEqual(placed(["ABBA", "BAAB"], angle=angle).error, 0.0, places=9)
            self.assertAlmostEqual(placed(["BBB", "BAB", "BBB"], angle=angle).error, 0.0, places=9)
        self.assertGreater(placed(["ABBAABBA"], curvature=0.9).error, 0.01)


class Numbers(unittest.TestCase):
    def test_bandgap_ratio(self):
        """Chapter 7: ΔV_BE = (kT/q) ln 8 ≈ 54 mV, so V_REF ≈ 1.2 V needs R2/R1 ≈ 10."""
        vt = 1.380649e-23 * 300 / 1.602176634e-19
        dvbe = vt * np.log(8)
        self.assertAlmostEqual(dvbe * 1e3, 53.8, delta=0.3)
        self.assertAlmostEqual((1.2 - 0.65) / dvbe, 10.0, delta=0.5)

    def test_rail_fed_from_the_middle(self):
        """Chapter 4: a uniformly loaded rail's worst sag, fed from the middle, is a quarter."""
        x = np.linspace(0, 1, 1001)
        end = x - x * x / 2
        u = np.abs(x - 0.5) * 2
        mid = (u - u * u / 2) / 4
        self.assertAlmostEqual(mid.max() / end.max(), 0.25, places=6)


if __name__ == "__main__":
    unittest.main()

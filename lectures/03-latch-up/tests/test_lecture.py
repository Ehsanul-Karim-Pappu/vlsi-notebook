"""Checks the lecture: every chapter defines its scene and has notes in both languages; the toy
model behaves the way the slides and the labs say; the labs' JavaScript port agrees with it; and the
lab buttons the notes name exist.

Run from the repository root:  python -m unittest discover lectures/03-latch-up/tests
"""

import ast
import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

LECTURE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(LECTURE.parents[1]), str(LECTURE)]

import physics as ph  # noqa: E402


def has_bangla(s):
    return any("ঀ" <= c <= "৿" for c in s)


class Chapters(unittest.TestCase):
    def test_every_chapter_and_its_notes(self):
        from build import SEQUENCE

        for step in SEQUENCE:
            if step[0] == "lab":
                self.assertTrue((LECTURE / "labs" / step[1]).exists(), step[1])
                self.assertTrue(has_bangla(step[3][1]), f"{step[1]}: Bangla notes")
                continue
            tree = ast.parse((LECTURE / step[1]).read_text())
            with self.subTest(scene=step[2]):
                self.assertIn(step[2], [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)])
                says = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and getattr(n.func, "id", "") == "say"]
                self.assertTrue(says)
                for call in says:
                    en, bn = (ast.literal_eval(a) for a in call.args)
                    self.assertTrue(en.strip() and not has_bangla(en), f"{step[2]} line {call.lineno}: English")
                    self.assertTrue(has_bangla(bn), f"{step[2]} line {call.lineno}: Bangla")

    def test_lab_buttons_match_the_notes(self):
        from build import FIRE_LAB, TAP_LAB

        fire = (LECTURE / "labs" / FIRE_LAB[1]).read_text()
        for name in ("Inject", "Power cycle", "0.8 V core", "1.8 V I/O", "3.3 V I/O"):
            self.assertIn(f">{name}</button>", fire)
        for name in ("Inject", "Power cycle"):
            self.assertIn(name, FIRE_LAB[3][0])
        taps = (LECTURE / "labs" / TAP_LAB[1]).read_text()
        for name in ("No taps", "Row ends", "Wrong well"):
            self.assertIn(f">{name}</button>", taps)
            self.assertIn(name, TAP_LAB[3][0])
        for lab in (FIRE_LAB, TAP_LAB):
            self.assertTrue((LECTURE / "images" / "labs" / (Path(lab[1]).stem + ".jpg")).exists(), lab[1])


class ToyModel(unittest.TestCase):
    """What the slides and the lab notes claim, in the model."""

    def test_taps_close_keep_it_quiet(self):
        self.assertEqual(ph.state(2.0, 5, 5, 2.0, 3.3), "quiet")  # the lab's starting point
        self.assertEqual(ph.state(2.0, 20, 5, 2.0, 3.3), "latched")  # drag the tap out

    def test_core_supply_lets_go(self):
        self.assertEqual(ph.state(2.0, 20, 5, 2.0, 0.8), "lets go")
        self.assertGreater(ph.holding_voltage(0.0), 0.8)

    def test_spacing_at_1v8(self):
        self.assertEqual(ph.state(2.0, 20, 5, 9.5, 1.8), "latched")
        self.assertEqual(ph.state(2.0, 20, 5, 10.5, 1.8), "lets go")  # holding climbs past 1.8 V near 10 µm
        self.assertGreater(ph.loop_gain(24.0), 1.0)
        self.assertLess(ph.loop_gain(26.0), 1.0)  # and the gain falls below one near 25 µm

    def test_budget_slide(self):
        # "at one milliamp the drop crosses 0.65 V at about 24 µm; at two, at about 11"
        d1 = (ph.V_ON / 1e-3 - ph.R_SUB0) / ph.K_SUB
        d2 = (ph.V_ON / 2e-3 - ph.R_SUB0) / ph.K_SUB
        self.assertAlmostEqual(d1, 24, delta=0.5)
        self.assertAlmostEqual(d2, 11, delta=0.5)
        self.assertLess(ph.base_drop(1.0, 15), ph.V_ON)

    def test_s_curve_slide(self):
        pts = ph.s_curve(10, 10, 2.0, i_max=400.0)
        self.assertAlmostEqual(max(v for v, _ in pts[: len(pts) // 3 + 1]), 6.0, delta=0.1)
        self.assertAlmostEqual(min(v for v, _ in pts), 0.0)
        i_on = (3.3 - ph.holding_voltage(2.0)) / 8.0 * 1e3
        self.assertAlmostEqual(i_on, 267, delta=1)  # "latched: ≈ 267 mA"

    def test_tap_lab_presets(self):
        free = {0, 5, 11, 17, 23}
        region = ["A", "A", "s", "s", "B", "B", "s", "s"]
        actives = [(c, r) for r in range(8) for c in range(24) if c not in free]

        def errors(taps, reach=5):
            return [a for a in actives
                    if not ph.covered(a, [t for t in taps if region[t[1]] == region[a[1]]], reach)]

        rows = [0, 2, 4, 6]
        self.assertEqual(len(errors([])), 152)
        self.assertEqual(len(errors([t for r in rows for t in ((0, r), (23, r + 1))])), 80)
        self.assertEqual(len(errors([t for r in rows for t in ((5, r), (17, r + 1))])), 0)


@unittest.skipUnless(shutil.which("node"), "node is not installed")
class JavaScriptPort(unittest.TestCase):
    def test_lab_model_agrees(self):
        cases = [(2.0, 5, 5, 2.0, 3.3), (2.0, 20, 5, 2.0, 3.3), (2.0, 20, 5, 2.0, 0.8), (5.0, 40, 60, 12.0, 1.8), (1.0, 2, 2, 30, 3.3)]
        js = (LECTURE / "labs" / "lab-model.js").read_text()
        script = "const window = {};\n" + js + f"""
const M = window.LUP, out = [];
for (const [i, ds, dw, s, v] of {json.dumps(cases)}) {{
  out.push([M.rSub(ds), M.rWell(dw), M.betaNpn(s), M.triggerCurrent(ds), M.holdingCurrent(ds, dw),
            M.holdingVoltage(s), M.state(i, ds, dw, s, v)]);
}}
out.push(M.sCurve(10, 10, 2.0, 6.0, 8.0, 400.0).slice(0, 200).flat());
console.log(JSON.stringify(out));
"""
        res = json.loads(subprocess.run(["node", "-e", script], capture_output=True, text=True, check=True).stdout)
        for (i, ds, dw, s, v), got in zip(cases, res):
            want = [ph.r_sub(ds), ph.r_well(dw), ph.beta_npn(s), ph.trigger_current(ds), ph.holding_current(ds, dw),
                    ph.holding_voltage(s), ph.state(i, ds, dw, s, v)]
            for g, w in zip(got[:6], want[:6]):
                self.assertAlmostEqual(g, w, places=9)
            self.assertEqual(got[6], want[6])
        flat = [x for p in ph.s_curve(10, 10, 2.0, 6.0, 8.0, 400.0) for x in p]
        for g, w in zip(res[-1], flat):
            self.assertAlmostEqual(g, w, places=9)


if __name__ == "__main__":
    unittest.main()

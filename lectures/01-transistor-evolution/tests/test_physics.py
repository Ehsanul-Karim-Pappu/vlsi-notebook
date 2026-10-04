"""Checks the lecture's equations against textbook values, and the labs' JS port against them.

Run from the repository root:  python -m unittest discover lectures/01-transistor-evolution/tests
"""

import json
import shutil
import subprocess
import sys
import unittest
from math import log10
from pathlib import Path

LECTURE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LECTURE))

import physics as p  # noqa: E402


class TextbookValues(unittest.TestCase):
    def test_thermal_voltage(self):
        self.assertAlmostEqual(p.thermal_voltage(300) * 1e3, 25.85, places=1)

    def test_swing_limit_is_60_mV_per_decade(self):
        self.assertAlmostEqual(p.subthreshold_swing(300) * 1e3, 59.5, delta=0.2)
        self.assertAlmostEqual(p.subthreshold_swing(77) * 1e3, 15.3, delta=0.1)
        self.assertAlmostEqual(p.subthreshold_swing(300, m=1.3) * 1e3, 77.4, delta=0.2)

    def test_barrier_drop_for_ten_times_the_electrons(self):
        e = p.barrier_drop_per_decade_eV(300)
        ratio = p.fraction_over_barrier(0.3 - e) / p.fraction_over_barrier(0.3)
        self.assertAlmostEqual(ratio, 10.0, places=6)

    def test_drain_current_slope_below_threshold_is_the_swing(self):
        ss = p.subthreshold_swing(300, m=1.2)
        i1 = p.drain_current(0.0, 0.6, m=1.2)
        i2 = p.drain_current(0.0 + ss, 0.6, m=1.2)
        self.assertAlmostEqual(log10(i2 / i1), 1.0, places=3)

    def test_drain_current_is_square_law_far_above_threshold(self):
        i1 = p.drain_current(1.4, 0.4)
        i2 = p.drain_current(2.4, 0.4)
        self.assertAlmostEqual(i2 / i1, 4.0, delta=0.1)

    def test_drain_current_does_not_overflow(self):
        self.assertGreater(p.drain_current(50.0, 0.0), 0)

    def test_lower_vt_by_one_swing_costs_ten_times_the_leakage(self):
        ss = p.subthreshold_swing(300)
        self.assertAlmostEqual(p.off_current_ratio(ss, ss), 10.0)
        self.assertAlmostEqual(p.off_current_ratio(3 * ss, ss), 1000.0, places=6)

    def test_oxide_tunnelling_rises_tenfold_per_fifth_of_a_nanometre(self):
        self.assertAlmostEqual(p.thickness_per_decade_nm(), 0.2, delta=0.02)
        r = p.tunnel_transmission(1.0) / p.tunnel_transmission(1.2)
        self.assertGreater(r, 9)

    def test_high_k_buys_physical_thickness(self):
        self.assertAlmostEqual(p.eot_nm(6.15, 20), 1.2, delta=0.01)
        self.assertAlmostEqual(p.physical_thickness_nm(1.2, 20), 6.15, delta=0.01)


@unittest.skipUnless(shutil.which("node"), "node is not installed")
class LabPortAgrees(unittest.TestCase):
    def js(self, expr):
        script = (
            f"const P = require({json.dumps(str(LECTURE / 'labs' / 'lab-physics.js'))});"
            f"console.log(JSON.stringify({expr}));"
        )
        return json.loads(subprocess.check_output(["node", "-e", script]))

    def test_same_numbers(self):
        cases = [
            ("P.thermalVoltage(300)", p.thermal_voltage(300)),
            ("P.subthresholdSwing(77, 1.4)", p.subthreshold_swing(77, 1.4)),
            ("P.fractionOverBarrier(0.2, 400)", p.fraction_over_barrier(0.2, 400)),
            ("P.drainCurrent(0.25, 0.4, 300, 1.3)", p.drain_current(0.25, 0.4, 300, 1.3)),
            ("P.drainCurrent(40, 0.4)", p.drain_current(40, 0.4)),
            ("P.offCurrentRatio(0.12, 0.06)", p.off_current_ratio(0.12, 0.06)),
        ]
        for expr, want in cases:
            with self.subTest(expr=expr):
                self.assertAlmostEqual(self.js(expr) / want, 1.0, places=9)


if __name__ == "__main__":
    unittest.main()

"""Checks the lecture's equations against textbook values, and the labs' JS port against them.

Run from the repository root:  python -m unittest discover lectures/01-transistor-evolution/tests
"""

import json
import shutil
import subprocess
import sys
import unittest
from math import exp, log10
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


class HistoryChapters(unittest.TestCase):
    def test_thermionic_emission_is_boltzmann_in_the_work_function(self):
        j1 = p.thermionic_current_density(2000, 4.5)
        j2 = p.thermionic_current_density(2000, 4.5 - p.thermal_voltage(2000) * p.LN10)
        self.assertAlmostEqual(j2 / j1, 10.0, places=6)

    def test_lilienfeld_gate_induces_about_2e12_per_cm2(self):
        self.assertAlmostEqual(p.induced_sheet_density_cm2(10, 100) / 1e12, 2.16, delta=0.02)

    def test_surface_states_swallow_the_field(self):
        self.assertAlmostEqual(p.share_reaching_channel(1e13), 0.021, delta=0.002)
        self.assertGreater(p.share_reaching_channel(1e10), 0.95)

    def test_bjt_rises_tenfold_per_60_mV(self):
        r = p.collector_current(0.6 + p.subthreshold_swing(300)) / p.collector_current(0.6)
        self.assertAlmostEqual(r, 10.0, places=6)

    def test_bandgap_delta_vbe_for_one_to_eight(self):
        self.assertAlmostEqual(p.delta_vbe(8) * 1e3, 53.8, delta=0.1)

    def test_threshold_voltage_example(self):
        self.assertAlmostEqual(p.fermi_potential(1e17), 0.417, delta=0.002)
        self.assertAlmostEqual(p.oxide_capacitance_cm2(10) * 1e7, 3.45, delta=0.01)
        self.assertAlmostEqual(p.threshold_voltage(1e17, 10, -0.98), 0.34, delta=0.01)

    def test_square_law(self):
        k = 400 * p.oxide_capacitance_cm2(10)  # mu = 400 cm^2/Vs
        self.assertAlmostEqual(p.square_law_current(0.84, 1.0, 0.34, k, 10) * 1e6, 172, delta=1)
        self.assertEqual(p.square_law_current(0.2, 1.0, 0.34, k, 10), 0.0)
        # continuous at the edge of saturation
        lin = p.square_law_current(0.84, 0.4999999, 0.34, k, 10)
        sat = p.square_law_current(0.84, 0.5, 0.34, k, 10)
        self.assertAlmostEqual(lin, sat, places=9)

    def test_moore_line_reaches_the_biggest_chips(self):
        self.assertAlmostEqual(p.moore_count(2024) / 2.08e11, 1.05, delta=0.05)

    def test_dennard_keeps_power_density_constant(self):
        k = 1.4
        f = {name: p.dennard_factor(pw, k) for name, pw in p.DENNARD}
        density = f["power per circuit VI"] * f["circuits per area"]
        self.assertAlmostEqual(density, 1.0)
        self.assertAlmostEqual(f["power density"], 1.0)
        self.assertAlmostEqual(p.dynamic_power(1, 1 / k, 1 / k, k) * k * k, p.dynamic_power(1, 1, 1, 1))


@unittest.skipUnless(shutil.which("node"), "node is not installed")
class ArchitectureChapters(unittest.TestCase):
    def test_natural_length_shrinks_as_the_gate_wraps(self):
        planar = p.natural_length_nm(15, 1, 1)
        fin = p.natural_length_nm(6, 1, 3)
        gaa = p.natural_length_nm(5, 1, 4)
        self.assertAlmostEqual(planar, 6.71, places=2)
        self.assertAlmostEqual(fin, 2.45, places=2)
        self.assertAlmostEqual(gaa, 1.94, places=2)

    def test_long_channel_barrier_is_set_by_the_gate(self):
        self.assertAlmostEqual(p.barrier_height(30, 1), 0.6, places=4)
        self.assertLess(p.dibl_mV_per_V(30, 1), 0.1)

    def test_dibl_grows_as_the_channel_shortens(self):
        d10, d6, d3 = (p.dibl_mV_per_V(k, 1) for k in (10, 6, 3))
        self.assertLess(d10, d6)
        self.assertLess(d6, d3)
        self.assertTrue(20 < d6 < 60, d6)

    def test_short_channel_swing(self):
        self.assertAlmostEqual(p.short_channel_swing(100, 1) * 1e3, 59.5, places=1)
        self.assertAlmostEqual(p.short_channel_swing(6, 1) / p.subthreshold_swing(), 1 / (1 - 2 * exp(-3)), places=6)

    def test_effective_widths(self):
        self.assertEqual(p.weff_fin_nm(2, 45, 6), 192)
        self.assertEqual(p.weff_sheets_nm(3, 30, 5), 210)

    def test_cells_and_wires(self):
        self.assertEqual(p.cell_height_nm(6, 24), 144)
        self.assertAlmostEqual(p.wire_resistance_ohm(1000, 20, 40), 25.0)
        self.assertAlmostEqual(p.roughness_mobility_ratio(4, 5), 0.262, places=3)

    def test_self_gain_from_dibl(self):
        self.assertAlmostEqual(p.self_gain_from_dibl(100), 10.0)
        short, long_ = (p.self_gain_from_dibl(p.dibl_mV_per_V(k, 1)) for k in (3, 10))
        self.assertTrue(5 < short < 8 and long_ > 100, (short, long_))


class BeyondChapters(unittest.TestCase):
    def test_a_2d_layer_halves_lambda(self):
        self.assertAlmostEqual(p.natural_length_nm(0.65, 1, 2), 0.99, places=2)

    def test_negative_capacitance_gives_m_below_one(self):
        self.assertAlmostEqual(p.body_factor(1.0, 4.0), 1.25)
        m = p.body_factor(1.0, -5.0)
        self.assertAlmostEqual(m, 0.8)
        self.assertLess(p.subthreshold_swing(300, m), 0.05)

    def test_tunnelling_matches_the_thermal_leak_near_5_nm(self):
        L = p.tunnelling_crossover_nm()
        self.assertTrue(4.5 < L < 6.0, L)
        self.assertAlmostEqual(p.source_drain_tunnelling(L), p.fraction_over_barrier(0.4), places=12)
        self.assertGreater(p.source_drain_tunnelling(3), p.fraction_over_barrier(0.4))

    def test_landauer_and_today(self):
        self.assertAlmostEqual(p.landauer_limit_J() * 1e21, 2.87, places=2)
        ratio = p.switching_energy_J(0.1, 0.7) / p.landauer_limit_J()
        self.assertTrue(5e3 < ratio < 2e4, ratio)


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
            ("P.naturalLength(6, 1, 3)", p.natural_length_nm(6, 1, 3)),
            ("P.channelPotential(1.3, 4, 1.2, 1.0, 0.6)", p.channel_potential(1.3, 4, 1.2, 1.0, 0.6)),
            ("P.barrierHeight(5, 1, 1.0, 0.75)", p.barrier_height(5, 1, 1.0, 0.75)),
            ("P.diblMVperV(6, 1)", p.dibl_mV_per_V(6, 1)),
            ("P.shortChannelSwing(7, 1.1)", p.short_channel_swing(7, 1.1)),
        ]
        for expr, want in cases:
            with self.subTest(expr=expr):
                self.assertAlmostEqual(self.js(expr) / want, 1.0, places=9)


if __name__ == "__main__":
    unittest.main()

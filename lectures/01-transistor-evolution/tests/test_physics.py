"""Checks the lecture's equations against textbook values, and the labs' JS port against them.

Run from the repository root:  python -m unittest discover lectures/01-transistor-evolution/tests
"""

import json
import shutil
import subprocess
import sys
import unittest
from math import cosh, exp, log10
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
        self.assertAlmostEqual(p.share_in_semiconductor(1e13), 0.021, delta=0.002)
        self.assertGreater(p.share_in_semiconductor(1e10), 0.95)
        self.assertAlmostEqual(p.surface_state_capacitance_cm2(1e13) * 1e6, 1.602, places=3)  # q D_it, uF/cm^2

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

    def test_generalized_scaling(self):
        k = 2.0
        cf = p.generalized_scaling(k, k)  # Dennard: the DENNARD table again
        for name, pw in (("size", -1), ("voltage", -1), ("current", -1), ("capacitance", -1),
                         ("delay", -1), ("power", -2), ("density", 2), ("power_density", 0)):
            self.assertAlmostEqual(cf[name], k**pw, msg=name)
        cv = p.generalized_scaling(k, 1)  # the voltage stuck: the textbook constant-voltage case
        self.assertAlmostEqual(cv["current"], k)
        self.assertAlmostEqual(cv["delay"], k**-2)
        self.assertAlmostEqual(cv["power_density"], k**3)
        held = p.generalized_scaling(k, 1, fixed_clock=True)  # ...with the clock held as well
        self.assertAlmostEqual(held["power_density"], k)


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
        # At V_DS = 0 the barrier top follows the gate by 1 - sech(L / 2 lambda): no pole.
        self.assertAlmostEqual(p.short_channel_swing(6, 1) / p.subthreshold_swing(), 1 / (1 - 1 / cosh(3)), places=9)
        self.assertAlmostEqual(p.short_channel_swing(1.5, 1) * 1e3, 261.528, places=2)
        self.assertAlmostEqual(p.short_channel_swing(20, 1) / p.subthreshold_swing(), 1 / (1 - 2 * exp(-10)), places=6)

    def test_closed_form_barrier_matches_a_grid_search(self):
        for L, v in ((1.5, 0.05), (3, 0.75), (6, 0.4)):
            grid = 1.0 - min(p.channel_potential(L * i / 4000, L, 1, 1.0, v, 0.4) for i in range(4001))
            self.assertAlmostEqual(p.barrier_height(L, 1, v_ds=v), grid, places=6)

    def test_gate_and_drain_coupling(self):
        self.assertAlmostEqual(p.gate_coupling(3, 1, 0.4), 0.5577, places=4)
        self.assertAlmostEqual(p.drain_coupling(3, 1, 0.4), 0.15367, places=5)
        h = 1e-6  # the closed forms agree with finite differences of the barrier
        dg = (p.barrier_height(3, 1, v_ds=0.4, phi_gs=0.4 - h) - p.barrier_height(3, 1, v_ds=0.4, phi_gs=0.4 + h)) / (2 * h)
        dd = (p.barrier_height(3, 1, v_ds=0.4 - h) - p.barrier_height(3, 1, v_ds=0.4 + h)) / (2 * h)
        self.assertAlmostEqual(dg, p.gate_coupling(3, 1, 0.4), places=5)
        self.assertAlmostEqual(dd, p.drain_coupling(3, 1, 0.4), places=5)

    def test_effective_widths(self):
        self.assertEqual(p.weff_fin_nm(2, 45, 6), 192)
        self.assertEqual(p.weff_sheets_nm(3, 30, 5), 210)

    def test_cells_and_wires(self):
        self.assertEqual(p.cell_height_nm(6, 24), 144)
        # Live Lab 4's model gives back FET Lab's four inverter cells, rail to rail.
        self.assertEqual(p.cell_height_needed_nm("fin", p.fin_footprint_nm(2)), 156)
        self.assertEqual(p.cell_height_needed_nm("sheet", 22), 136)
        self.assertEqual(p.cell_height_needed_nm("fork", 22), 106)
        self.assertEqual(p.cell_height_needed_nm("cfet", 20), 74)
        from devicedata import rail_span_nm
        for key, arch, w in (("show_fin", "fin", p.fin_footprint_nm(2)), ("show_ns", "sheet", 22),
                             ("show_fs", "fork", 22), ("show_cfet", "cfet", 20)):
            self.assertAlmostEqual(rail_span_nm(key), p.cell_height_needed_nm(arch, w), msg=key)
        self.assertAlmostEqual(p.wire_resistance_ohm(1000, 20, 40), 25.0)
        self.assertAlmostEqual(p.roughness_mobility_ratio(4, 5), 0.262, places=3)

    def test_intrinsic_gain(self):
        self.assertAlmostEqual(p.intrinsic_gain(3, 1, 0.4), 3.63, places=2)
        self.assertGreater(p.intrinsic_gain(10, 1, 0.4), 100)

    def test_specific_current_keeps_strong_inversion_fixed(self):
        hot = p.drain_current(0.8, 0.4, 300, 1.0, p.specific_current(2e-7, 300, 1.0))
        cold = p.drain_current(0.8, 0.4, 77, 1.0, p.specific_current(2e-7, 77, 1.0))
        self.assertAlmostEqual(cold / hot, 1.0, delta=0.02)


class BeyondChapters(unittest.TestCase):
    def test_a_2d_layer_halves_lambda(self):
        self.assertAlmostEqual(p.natural_length_nm(0.65, 1, 2), 0.99, places=2)

    def test_negative_capacitance_gives_m_below_one(self):
        self.assertAlmostEqual(p.body_factor(1.0, 4.0), 1.25)
        m = p.nc_body_factor(1.0, 4.0, -3.0)
        self.assertAlmostEqual(m, 1 - 1 / 12)
        self.assertTrue(p.nc_stable(1.0, 4.0, -3.0))
        self.assertFalse(p.nc_stable(1.0, 4.0, -0.5))
        self.assertGreater(p.nc_body_factor(1.0, 4.0, -5.0), 1)  # |C_FE| > C_ox: no gain
        self.assertAlmostEqual(p.subthreshold_swing(300, m) * 1e3, 54.6, places=1)

    def test_tunnelling_matches_the_thermal_leak_near_5_nm(self):
        L = p.tunnelling_crossover_nm()
        self.assertTrue(4.5 < L < 6.0, L)
        self.assertAlmostEqual(p.source_drain_tunnelling(L), p.fraction_over_barrier(0.4), places=12)
        self.assertGreater(p.source_drain_tunnelling(3), p.fraction_over_barrier(0.4))

    def test_landauer_and_today(self):
        self.assertAlmostEqual(p.landauer_limit_J() * 1e21, 2.87, places=2)
        self.assertAlmostEqual(p.stored_energy_J(0.1, 0.7) * 1e18, 24.5)
        self.assertAlmostEqual(p.cycle_energy_J(0.1, 0.7) * 1e18, 49.0)
        ratio = p.cycle_energy_J(0.1, 0.7) / p.landauer_limit_J()
        self.assertTrue(1.6e4 < ratio < 1.8e4, ratio)


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
            ("P.shortChannelSwing(2.5, 1.0, 300, 0.6)", p.short_channel_swing(2.5, 1.0, 300, 0.6)),
            ("P.gateCoupling(3, 1, 0.4)", p.gate_coupling(3, 1, 0.4)),
            ("P.drainCoupling(4, 1.2, 0.7)", p.drain_coupling(4, 1.2, 0.7)),
            ("P.intrinsicGain(5, 1, 0.4)", p.intrinsic_gain(5, 1, 0.4)),
            ("P.specificCurrent(2e-7, 77, 1.3)", p.specific_current(2e-7, 77, 1.3)),
            ("P.generalizedScaling(2.7, 1.6).power_density", p.generalized_scaling(2.7, 1.6)["power_density"]),
            ("P.generalizedScaling(2.7, 1.6, true).power", p.generalized_scaling(2.7, 1.6, True)["power"]),
            ("P.generalizedScaling(3.1, 3.1).frequency", p.generalized_scaling(3.1, 3.1)["frequency"]),
            ("P.cellHeightNeeded('fin', P.finFootprint(3))", p.cell_height_needed_nm("fin", p.fin_footprint_nm(3))),
            ("P.cellHeightNeeded('cfet', 31)", p.cell_height_needed_nm("cfet", 31)),
            ("P.weffSheets(3, 30, 5)", p.weff_sheets_nm(3, 30, 5)),
            ("P.weffFin(2, 45, 6)", p.weff_fin_nm(2, 45, 6)),
        ]
        for expr, want in cases:
            with self.subTest(expr=expr):
                self.assertAlmostEqual(self.js(expr) / want, 1.0, places=9)


class DeckFiles(unittest.TestCase):
    def test_lab5_models_match_the_glb_files(self):
        import base64

        text = (LECTURE / "labs" / "lab5-models.js").read_text()
        glbs = sorted((LECTURE / "models").glob("*.glb"))
        self.assertTrue(glbs)
        for glb in glbs:
            with self.subTest(model=glb.stem):
                self.assertIn(f'{glb.stem}: "{base64.b64encode(glb.read_bytes()).decode()}"', text)

    def test_core_path(self):
        """Every core slide still exists and is the slide core.py means (checked against the
        rendered slides when there are any), every scene keeps one, and every lab has notes."""
        import core

        sys.path.insert(0, str(LECTURE.parents[1]))
        from build import BANGLA, SEQUENCE

        scenes = [s[2] for s in SEQUENCE if s[0] == "scene"]
        self.assertEqual(set(core.CORE), set(scenes))
        self.assertEqual(set(core.LABS), {s[1] for s in SEQUENCE if s[0] == "lab"})
        words = 0
        for scene in scenes:
            rows = core.CORE[scene]
            self.assertTrue(rows, scene)
            self.assertEqual([r[0] for r in rows], sorted({r[0] for r in rows}), scene)
            for i, anchor, en, bn in rows:
                words += len(en.split())
                self.assertTrue(any("\u0980" <= c <= "\u09ff" for c in bn), f"{scene} {i}: Bangla notes")
            rendered = LECTURE / "slides" / f"{scene}.json"
            if rendered.exists():
                slides = json.loads(rendered.read_text())["slides"]
                for i, anchor, en, bn in rows:
                    full = " ".join(slides[i]["notes"].split(BANGLA)[0].split())
                    self.assertTrue(full.startswith(anchor), f"{scene} {i}: {full[:40]!r}")
        words += sum(len(en.split()) for en, bn in core.LABS.values())
        self.assertTrue(2500 <= words <= 3400, f"core script: {words} words")

    def test_voice_over_script(self):
        """The voice-over has one line per slide of the core movie, in the movie's order; its audio
        tags are well formed; and the subtitles and voiceover.py take them out the same way."""
        import csv
        import re

        import core
        import voiceover

        sys.path.insert(0, str(LECTURE.parents[1]))
        from build import SEQUENCE, untagged

        order = []
        for step in SEQUENCE:
            if step[0] == "scene":
                order += [f"{step[2]}-{row[0]:02d}" for row in core.CORE[step[2]]]
            else:
                order.append(Path(step[1]).stem)
        with open(LECTURE / "narration" / "en-core" / "manifest.csv", newline="", encoding="utf-8") as f:
            table = list(csv.DictReader(f))
        self.assertEqual([Path(r["file"]).stem for r in table], order)
        for r in table:
            text = r["text"]
            with self.subTest(file=r["file"]):
                self.assertRegex(text, r"^[^\[\]]*(\[[^\[\]]{1,30}\][^\[\]]*)*$")
                self.assertEqual(untagged(text), voiceover.untagged(text))
                self.assertNotIn("[", untagged(text))
                self.assertEqual(untagged(text), " ".join(untagged(text).split()))
                self.assertLess(len(text), 5000)  # the shortest per-request limit, Eleven v3's
                self.assertNotIn("[", voiceover.spoken(text, "eleven_flash_v2_5"))
                self.assertEqual(voiceover.spoken(text, "eleven_v4").count("["), text.count("["))


if __name__ == "__main__":
    unittest.main()

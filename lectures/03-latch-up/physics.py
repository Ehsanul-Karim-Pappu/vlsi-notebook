"""The lecture's toy model of latch-up, used by the slides, both labs (labs/lab-model.js is its
JavaScript port) and the tests.

It is a teaching model, labelled "toy model" wherever one of its numbers appears: the shapes are
right (what grows, what shrinks, what decides latched or not), the values are illustrative, not a
process's. Units: µm, mA, V, Ω.

The picture: an injected current flows to the nearest substrate tap through R_sub. When the drop
reaches V_ON, the lateral NPN turns on; its collector current pulls the well down through R_well,
which turns the vertical PNP on, whose collector current feeds R_sub again. The loop fires if both
bipolars turn on and their gains multiply to more than one. Once fired it stays on only while the
supply is above the holding voltage.
"""

from math import exp

V_ON = 0.65  # a bipolar's base-emitter turn-on voltage, V

# Resistance from a parasitic bipolar's base to its tap: a little spreading resistance near the
# device, then more for every µm of distance. Illustrative values.
R_SUB0, K_SUB = 50.0, 25.0  # Ω, Ω per µm: p-substrate
R_WELL0, K_WELL = 100.0, 40.0  # Ω, Ω per µm: n-well (shallower, more resistive)

BETA_NPN0, BASE_SCALE = 40.0, 4.0  # the lateral NPN's gain with no spacing, and how fast it falls (µm)
BETA_PNP = 15.0  # the vertical PNP's gain: set by the well depth, which layout doesn't change

V_HOLD0, K_HOLD = 1.0, 0.08  # V, V per µm of N+ to N-well spacing


def r_sub(d_um):
    """Substrate resistance seen by the NPN's base, d µm from the nearest P+ tap (Ω)."""
    return R_SUB0 + K_SUB * d_um


def r_well(d_um):
    """Well resistance seen by the PNP's base, d µm from the nearest N+ well tap (Ω)."""
    return R_WELL0 + K_WELL * d_um


def beta_npn(spacing_um):
    """The lateral NPN's gain: its base is the p-substrate between the N+ diffusion and the
    N-well, so more spacing means a wider base and less gain."""
    return BETA_NPN0 * exp(-spacing_um / BASE_SCALE)


def loop_gain(spacing_um):
    return beta_npn(spacing_um) * BETA_PNP


def base_drop(i_inj_ma, d_um):
    """The voltage an injected current develops across the substrate resistance (V)."""
    return i_inj_ma * 1e-3 * r_sub(d_um)


def trigger_current(d_um):
    """The injected current that brings the NPN's base to V_ON (mA)."""
    return V_ON / r_sub(d_um) * 1e3


def holding_current(d_sub_um, d_well_um):
    """The current the loop must carry to keep both base resistors at V_ON (mA)."""
    return (V_ON / r_sub(d_sub_um) + V_ON / r_well(d_well_um)) * 1e3


def holding_voltage(spacing_um):
    """The lowest supply that keeps a fired loop on (V). Grows with the N+ to well spacing."""
    return V_HOLD0 + K_HOLD * spacing_um


def state(i_inj_ma, d_sub_um, d_well_um, spacing_um, vdd):
    """'quiet', 'lets go' (fires but the supply is below the holding voltage) or 'latched'."""
    fires = base_drop(i_inj_ma, d_sub_um) >= V_ON and loop_gain(spacing_um) > 1.0
    if not fires:
        return "quiet"
    return "latched" if vdd > holding_voltage(spacing_um) else "lets go"


def s_curve(d_sub_um, d_well_um, spacing_um, v_trig=6.0, r_on=8.0, i_max=None, n=200):
    """An illustrative S-shaped I–V of the parasitic thyristor, as (V, mA) points: the blocking
    branch up to the trigger point, the snapback to the holding point, then the on branch."""
    i_t = trigger_current(d_sub_um) * 0.05  # the device's own leakage at its trigger point
    i_h = holding_current(d_sub_um, d_well_um)
    v_h = holding_voltage(spacing_um)
    i_max = i_max or max(3 * i_h, 100.0)
    pts = []
    for k in range(n // 3):  # blocking: a small, slowly rising current
        v = v_trig * k / (n // 3)
        pts.append((v, i_t * (v / v_trig) ** 4))
    for k in range(n // 3):  # snapback: voltage falls as the current rises
        t = k / (n // 3)
        pts.append((v_trig + (v_h - v_trig) * t, i_t + (i_h - i_t) * t))
    for k in range(n - 2 * (n // 3)):  # on: the holding voltage plus an on-resistance
        i = i_h + (i_max - i_h) * k / (n - 2 * (n // 3) - 1)
        pts.append((v_h + (i - i_h) * 1e-3 * r_on, i))
    return pts


# --- the tap rule, on a grid (lab 2) ---------------------------------------------------------
def covered(cell, taps, reach):
    """A diffusion cell (x, y) is covered if a tap of its kind lies within REACH grid steps in
    both x and y: what a DRC does when it sizes every tap by the rule distance."""
    x, y = cell
    return any(abs(x - tx) <= reach and abs(y - ty) <= reach for tx, ty in taps)


def violations(cells, taps, reach):
    return [c for c in cells if not covered(c, taps, reach)]

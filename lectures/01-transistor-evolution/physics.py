"""Every equation lecture 1 shows, as plain functions.

The slides plot these and the labs port them to JavaScript (labs/lab-physics.js); the tests
check both against each other and against textbook numbers, so the numbers on screen are the
numbers the equations give.

Units are SI unless a name says otherwise (_eV, _nm, _mV).
"""

from math import exp, log, log1p, sqrt

K_B = 1.380649e-23  # J/K
Q = 1.602176634e-19  # C
HBAR = 1.054571817e-34  # J s
M0 = 9.1093837015e-31  # kg
LN10 = log(10)

EPS_SIO2 = 3.9  # relative permittivity of SiO2


def thermal_voltage(T=300.0):
    """k_B T / q, in volts. About 25.9 mV at 300 K."""
    return K_B * T / Q


def body_factor(c_dep, c_ox):
    """m = 1 + C_dep / C_ox: how much of the gate voltage reaches the channel surface (1/m)."""
    return 1.0 + c_dep / c_ox


def subthreshold_swing(T=300.0, m=1.0):
    """SS = m (k_B T / q) ln 10, in volts per decade. At least ~59.6 mV/dec at 300 K."""
    return m * thermal_voltage(T) * LN10


def fraction_over_barrier(barrier_eV, T=300.0):
    """Share of a Boltzmann population with energy above the barrier: exp(-E_b / k_B T)."""
    return exp(-barrier_eV / thermal_voltage(T))


def barrier_drop_per_decade_eV(T=300.0):
    """How far the barrier must drop for ten times as many electrons to cross: k_B T ln 10."""
    return thermal_voltage(T) * LN10


def drain_current(vgs, vt, T=300.0, m=1.2, i_spec=1e-6):
    """A smooth MOSFET I_D(V_GS) through weak and strong inversion (EKV interpolation).

    I_D = I_spec [ln(1 + exp((V_GS - V_T) / (2 m U_T)))]^2. Below V_T it falls as
    exp((V_GS - V_T) / (m U_T)), so its slope is exactly subthreshold_swing(T, m); above V_T
    it grows as (V_GS - V_T)^2, the square law.
    """
    ut = thermal_voltage(T)
    x = (vgs - vt) / (2 * m * ut)
    soft = x + log1p(exp(-x)) if x > 30 else log1p(exp(x))
    return i_spec * soft**2


def off_current_ratio(delta_vt, ss):
    """Factor by which I_off rises when V_T is lowered by delta_vt (both in volts)."""
    return 10 ** (delta_vt / ss)


def tunnel_decay_per_m(barrier_eV=3.1, m_eff=0.4):
    """WKB decay constant 2 kappa = 2 sqrt(2 m* Phi_B) / hbar, in 1/m.

    Defaults: the Si/SiO2 conduction-band offset (~3.1 eV) and an oxide effective mass of
    ~0.4 m0, both typical textbook values.
    """
    return 2 * sqrt(2 * m_eff * M0 * barrier_eV * Q) / HBAR


def tunnel_transmission(t_ox_nm, barrier_eV=3.1, m_eff=0.4):
    """WKB transmission through a rectangular barrier: exp(-2 kappa t)."""
    return exp(-tunnel_decay_per_m(barrier_eV, m_eff) * t_ox_nm * 1e-9)


def thickness_per_decade_nm(barrier_eV=3.1, m_eff=0.4):
    """How much thinner the oxide gets for each 10x rise in tunnelling."""
    return LN10 / tunnel_decay_per_m(barrier_eV, m_eff) * 1e9


def eot_nm(t_phys_nm, k):
    """Equivalent oxide thickness: EOT = t (3.9 / k)."""
    return t_phys_nm * EPS_SIO2 / k


def physical_thickness_nm(eot, k):
    """The physical thickness of a k dielectric with the given EOT."""
    return eot * k / EPS_SIO2

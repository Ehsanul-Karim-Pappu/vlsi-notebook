"""Every equation lecture 1 shows, as plain functions.

The slides plot these and the labs port them to JavaScript (labs/lab-physics.js); the tests
check both against each other and against textbook numbers, so the numbers on screen are the
numbers the equations give.

Units are SI unless a name says otherwise (_eV, _nm, _mV).
"""

from math import exp, log, log1p, sinh, sqrt

K_B = 1.380649e-23  # J/K
Q = 1.602176634e-19  # C
HBAR = 1.054571817e-34  # J s
M0 = 9.1093837015e-31  # kg
LN10 = log(10)

EPS_0 = 8.8541878128e-12  # F/m
EPS_SIO2 = 3.9  # relative permittivity of SiO2
EPS_SI = 11.7  # relative permittivity of Si
N_I = 1.0e10  # intrinsic carrier density of Si at 300 K, cm^-3 (modern value ~9.7e9)


def thermal_voltage(T=300.0):
    """k_B T / q, in volts. About 25.9 mV at 300 K."""
    return K_B * T / Q


def body_factor(c_dep, c_ox):
    """m = 1 + C_dep / C_ox: how much of the gate voltage reaches the channel surface (1/m).
    A negative-capacitance insulator (C_ox < 0, chapter 11) gives m < 1, and a swing below
    60 mV/decade (S. Salahuddin and S. Datta, Nano Lett. 8, 405 (2008))."""
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


# --- Chapter 1: tubes, the field effect and surface states -----------------------------------
def thermionic_current_density(T, work_function_eV, a_g=1.2e6):
    """Richardson-Dushman: J = A_G T^2 exp(-W / k_B T), in A/m^2. A_G ~ 1.2e6 A m^-2 K^-2."""
    return a_g * T * T * exp(-work_function_eV / thermal_voltage(T))


def induced_sheet_density_cm2(v_g, t_ox_nm, k=EPS_SIO2):
    """Electrons per cm^2 a gate induces through an insulator: n_s = C_ox V_G / q."""
    c_ox = k * EPS_0 / (t_ox_nm * 1e-9)  # F/m^2
    return c_ox * v_g / Q * 1e-4


def depletion_capacitance_cm2(n_a_cm3, psi_s):
    """C_dep = eps_Si / W_dep, with W_dep = sqrt(2 eps_Si psi_s / (q N_A)); in F/cm^2."""
    eps = EPS_SI * EPS_0 * 1e-2  # F/cm
    w = sqrt(2 * eps * psi_s / (Q * n_a_cm3))  # cm
    return eps / w


def surface_state_capacitance_cm2(d_it_cm2_eV):
    """C_it = q^2 D_it, with D_it per cm^2 per eV; in F/cm^2 (q x states per volt)."""
    return Q * d_it_cm2_eV


def share_reaching_channel(d_it_cm2_eV, n_a_cm3=1e16):
    """Of the charge a gate induces, the share that reaches the channel instead of filling
    surface states: C_dep / (C_dep + C_it), with the depletion region at threshold (psi_s =
    2 phi_F). Bardeen's surface states (D_it ~ 1e13) leave almost nothing for the channel."""
    c_dep = depletion_capacitance_cm2(n_a_cm3, 2 * fermi_potential(n_a_cm3))
    c_it = surface_state_capacitance_cm2(d_it_cm2_eV)
    return c_dep / (c_dep + c_it)


# --- Chapter 2: the bipolar transistor -------------------------------------------------------
def collector_current(v_be, i_s=1e-16, T=300.0):
    """I_C = I_S exp(q V_BE / k_B T), in amps."""
    return i_s * exp(v_be / thermal_voltage(T))


def delta_vbe(ratio, T=300.0):
    """The bandgap's PTAT voltage: two BJTs at a current-density ratio N differ in V_BE by
    (k_B T / q) ln N."""
    return thermal_voltage(T) * log(ratio)


# --- Chapter 3: the MOS capacitor and the MOSFET ---------------------------------------------
def fermi_potential(n_a_cm3, T=300.0):
    """phi_F = (k_B T / q) ln(N_A / n_i), in volts."""
    return thermal_voltage(T) * log(n_a_cm3 / N_I)


def oxide_capacitance_cm2(t_ox_nm, k=EPS_SIO2):
    """C_ox = k eps_0 / t_ox, in F/cm^2."""
    return k * EPS_0 / (t_ox_nm * 1e-9) * 1e-4


def threshold_voltage(n_a_cm3, t_ox_nm, v_fb):
    """V_T = V_FB + 2 phi_F + sqrt(2 q eps_Si N_A 2 phi_F) / C_ox, in volts."""
    phi2 = 2 * fermi_potential(n_a_cm3)
    eps = EPS_SI * EPS_0 * 1e-2  # F/cm
    q_dep = sqrt(2 * Q * eps * n_a_cm3 * phi2)  # C/cm^2
    return v_fb + phi2 + q_dep / oxide_capacitance_cm2(t_ox_nm)


def square_law_current(v_gs, v_ds, v_t, k_prime, w_over_l):
    """Long-channel MOSFET (gradual-channel approximation), in amps. k' = mu C_ox.
    Off below threshold; linear when V_DS < V_GS - V_T; saturated (square law) beyond."""
    v_ov = v_gs - v_t
    if v_ov <= 0:
        return 0.0
    if v_ds < v_ov:
        return k_prime * w_over_l * (v_ov * v_ds - v_ds * v_ds / 2)
    return 0.5 * k_prime * w_over_l * v_ov * v_ov


def dynamic_power(alpha, c, v, f):
    """Switching power P = alpha C V^2 f, in watts."""
    return alpha * c * v * v * f


# --- Chapter 4: Moore and Dennard ------------------------------------------------------------
def moore_count(year, start_year=1971, start_count=2300, doubling_years=2.0):
    """Moore's 1975 rule from the 4004: the transistor count doubles every two years."""
    return start_count * 2 ** ((year - start_year) / doubling_years)


DENNARD = [
    # quantity, how it scales with kappa (as a power of kappa)
    ("dimensions: L, W, t_ox", -1),
    ("doping N_A", 1),
    ("voltage V", -1),
    ("current I", -1),
    ("capacitance C", -1),
    ("delay CV/I", -1),
    ("power per circuit VI", -2),
    ("circuits per area", 2),
    ("power density", 0),
]


def dennard_factor(power, kappa):
    """kappa ** power: how a quantity in DENNARD changes when everything scales by kappa."""
    return kappa**power


# --- Chapter 6: losing grip (the quasi-2D model) ---------------------------------------------
# The channel's potential along x (source at 0, drain at L) under a gate that holds it at
# phi_gs far from the ends: d2phi/dx2 - (phi - phi_gs)/lambda^2 = 0, with phi = V_bi at the
# source and V_bi + V_DS at the drain (K. K. Young, IEEE TED 36, 399 (1989); R.-H. Yan,
# A. Ourmazd and K. F. Lee, IEEE TED 39, 1704 (1992)).
def natural_length_nm(t_si_nm, t_ox_nm, n_gates=1, eps_si=EPS_SI, eps_ox=EPS_SIO2):
    """lambda = sqrt(eps_si t_si t_ox / (N eps_ox)): how far the drain's field reaches into the
    channel. N counts the gates around it: 1 planar, 2 double gate, 3 tri-gate, 4 all around."""
    return sqrt(eps_si * t_si_nm * t_ox_nm / (n_gates * eps_ox))


def channel_potential(x, length, lam, v_bi=1.0, v_ds=0.05, phi_gs=0.4):
    """phi(x) in volts, x and length in the same units as lam."""
    s = sinh(length / lam)
    return (phi_gs + (v_bi - phi_gs) * sinh((length - x) / lam) / s
            + (v_bi + v_ds - phi_gs) * sinh(x / lam) / s)


def barrier_height(length, lam, v_bi=1.0, v_ds=0.05, phi_gs=0.4, n=2001):
    """The electron's barrier from the source, V_bi - min(phi), in eV. Long channel: V_bi - phi_gs."""
    lo = min(channel_potential(length * i / (n - 1), length, lam, v_bi, v_ds, phi_gs) for i in range(n))
    return v_bi - lo


def dibl_mV_per_V(length, lam, v_lo=0.05, v_hi=0.75, **kw):
    """Drain-induced barrier lowering: how much the barrier drops per volt on the drain."""
    return 1000 * (barrier_height(length, lam, v_ds=v_lo, **kw) - barrier_height(length, lam, v_ds=v_hi, **kw)) / (v_hi - v_lo)


def short_channel_swing(length, lam, T=300.0):
    """SS ~ (60 mV/dec at 300 K) / (1 - 2 exp(-L/(2 lambda))), in V/decade (K. Suzuki et al.,
    IEEE TED 40, 2326 (1993)). A model: it fails as L approaches lambda."""
    return subthreshold_swing(T) / (1 - 2 * exp(-length / (2 * lam)))


# --- Chapters 7-10: width, cells, wires ------------------------------------------------------
def weff_fin_nm(n_fin, h_fin_nm, w_fin_nm):
    """A FinFET's effective width: each fin conducts on both sidewalls and the top."""
    return n_fin * (2 * h_fin_nm + w_fin_nm)


def weff_sheets_nm(n_sheets, w_sh_nm, t_sh_nm):
    """A nanosheet's effective width: each sheet conducts all the way round."""
    return n_sheets * 2 * (w_sh_nm + t_sh_nm)


def roughness_mobility_ratio(t_nm, t_ref_nm):
    """Below about 5 nm, thickness fluctuations make mobility fall roughly as t^6 (K. Uchida et
    al., IEDM 2002). Illustrative: the ratio of mobilities at two thicknesses."""
    return (t_nm / t_ref_nm) ** 6


def cell_height_nm(tracks, m2_pitch_nm):
    """A standard cell's height: its number of routing tracks times the metal pitch."""
    return tracks * m2_pitch_nm


def wire_resistance_ohm(length_nm, width_nm, thickness_nm, rho_ohm_m=2.0e-8):
    """R = rho L / (w t). The default rho is a thin-wire copper value, not the bulk 1.7e-8."""
    return rho_ohm_m * length_nm * 1e-9 / (width_nm * 1e-9 * thickness_nm * 1e-9)


def self_gain_from_dibl(dibl_mV_per_V):
    """An analog transistor's intrinsic gain g_m r_o when DIBL is all that sets its output
    resistance: the drain moves the current like eta = DIBL (V/V) times the gate, so
    g_ds = eta g_m and g_m r_o = 1/eta. A model: channel-length modulation lowers it further."""
    return 1000.0 / dibl_mV_per_V


# --- Chapter 11: beyond silicon, beyond Boltzmann ---------------------------------------------
def source_drain_tunnelling(length_nm, barrier_eV=0.4, m_eff=0.2):
    """WKB share of electrons that tunnel straight through the channel's barrier, source to
    drain, rather than climbing over it. m_eff ~0.2 m0 for electrons in silicon."""
    return tunnel_transmission(length_nm, barrier_eV, m_eff)


def tunnelling_crossover_nm(barrier_eV=0.4, m_eff=0.2, T=300.0):
    """The channel length at which tunnelling through the barrier equals the thermal leak over
    it: exp(-2 kappa L) = exp(-E_b / k_B T)."""
    return barrier_eV / thermal_voltage(T) / tunnel_decay_per_m(barrier_eV, m_eff) * 1e9


def landauer_limit_J(T=300.0):
    """The least energy to erase one bit: k_B T ln 2 (R. Landauer, IBM J. Res. Dev. 5, 183 (1961))."""
    return K_B * T * log(2)


def switching_energy_J(c_fF, v):
    """The energy one switching event draws from the supply into a node: C V^2 / 2."""
    return 0.5 * c_fF * 1e-15 * v**2

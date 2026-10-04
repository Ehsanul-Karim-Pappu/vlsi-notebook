# Sources

Every date, name and number on the slides, with where it comes from. Results of the lecture's
own simple models are labelled "model" on screen and computed in `physics.py`. The historical
photos and patent drawings, with their sources and licences, are listed in
[images/CREDITS.md](images/CREDITS.md).

## Chapter 0 · Cold open

| Claim | Source |
|---|---|
| About 13 sextillion (1.3 × 10²²) transistors made through 2018 | Jim Handy (Objective Analysis), reported in D. Laws, "13 Sextillion & Counting: The Long & Winding Road to the Most Frequently Manufactured Human Artifact in History", Computer History Museum, 2018. https://computerhistory.org/blog/13-sextillion-counting-the-long-winding-road-to-the-most-frequently-manufactured-human-artifact-in-history/ |
| "The most frequently manufactured human artifact in history" | David C. Brock, historian, quoted in the same Computer History Museum article |
| About 1.6 trillion per person | 1.3 × 10²² divided by a world population of about 8.1 billion |
| Apple A17 Pro (2023): 19 billion transistors | Apple Newsroom, iPhone 15 Pro announcement, 12 September 2023 |
| The 3D nanosheet: 15 nm gate, 5 nm sheets | FET Lab's nanosheet nFET model (`data/geometry.json`), after IBM US 2023/0420457 A1 |
| FinFET 2011, nanosheet 2022 | Intel's 22 nm tri-gate announcement (May 2011); Samsung's first 3 nm gate-all-around production (June 2022) |
| Forksheet ~2030 and CFET ~2033 | imec logic roadmap projections (outer-wall forksheet at A10, monolithic CFET at A7). Projections, not facts. https://www.imec-int.com/en/articles/performance-boosters-scale-monolithic-cfet-across-multiple-logic-technology-nodes |

## Chapter 1 · Before the switch

| Claim | Source |
|---|---|
| A triode's grid switches the plate current; thermionic emission J = A T² exp(−W/k_BT) | O. W. Richardson (Nobel Prize in Physics 1928) and S. Dushman; Sze and Ng, ch. 3. Computed in `physics.thermionic_current_density` |
| ENIAC (1946): 17,468 vacuum tubes, about 150 kW | University of Pennsylvania and the U.S. Army, the ENIAC's public unveiling, February 1946; Penn Engineering, "ENIAC" history page |
| Lilienfeld's field-effect device | J. E. Lilienfeld, Canadian patent application 272,437 (22 October 1925); US patent 1,745,175, "Method and apparatus for controlling electric currents", filed 8 October 1926, granted 28 January 1930 |
| Induced sheet charge n_s ≈ 2.2 × 10¹² cm⁻² (t_ox = 100 nm, V_G = 10 V) | Model: n_s = C_ox V_G / q in `physics.induced_sheet_density_cm2` |
| Shockley's 1945 field-effect experiments failed | M. Riordan and L. Hoddeson, *Crystal Fire: The Birth of the Information Age* (Norton, 1997), ch. 6 |
| Surface states screen the gate's field | J. Bardeen, "Surface states and rectification at a metal semi-conductor contact", *Phys. Rev.* 71, 717 (1947) |
| About 2% of the gate's charge reaches the channel (D_it ≈ 10¹³ cm⁻² eV⁻¹) | Model: C_dep / (C_dep + q²D_it) at N_A = 10¹⁶ cm⁻³, in `physics.share_reaching_channel` |

## Chapter 2 · The accidental transistor

| Claim | Source |
|---|---|
| The point-contact transistor: amplified on 16 December 1947, shown to Bell Labs management on 23 December | Riordan and Hoddeson, *Crystal Fire*, ch. 7; Computer History Museum, "1947: Invention of the point-contact transistor", *The Silicon Engine* |
| Gold foil on a plastic wedge, a paper-clip spring, contacts about 50 µm apart | The same CHM page; J. Bardeen and W. H. Brattain, "The transistor, a semi-conductor triode", *Phys. Rev.* 74, 230 (1948) |
| Bardeen and Brattain's patent, filed 17 June 1948 | US patent 2,524,035 |
| Shockley's patent, filed 26 June 1948 | US patent 2,569,347 |
| Shockley's junction transistor, conceived in January 1948 | W. Shockley, "The theory of p-n junctions in semiconductors and p-n junction transistors", *Bell Syst. Tech. J.* 28, 435 (1949); US patent 2,569,347 |
| I_C = I_S exp(qV_BE/k_BT): 10× per about 60 mV | Sze and Ng, ch. 5. Computed in `physics.collector_current` |
| ΔV_BE = (k_BT/q) ln N = 53.8 mV for a 1 : 8 pair, proportional to T | P. Brokaw, "A simple three-terminal IC bandgap reference", *IEEE J. Solid-State Circuits* SC-9(6), 388 (1974); B. Razavi, *Design of Analog CMOS Integrated Circuits*, 2nd ed. (McGraw-Hill, 2017), ch. 12. Computed in `physics.delta_vbe` |
| Common-centroid arrays and dummy devices for matching | A. Hastings, *The Art of Analog Layout*, 2nd ed. (Prentice Hall, 2006), ch. 7 and 9 |

## Chapter 3 · Glass

| Claim | Source |
|---|---|
| Silicon's own oxide masks diffusion (found in 1955) | C. J. Frosch and L. Derick, "Surface protection and selective masking during diffusion in silicon", *J. Electrochem. Soc.* 104, 547 (1957) |
| Thermal oxide passivates the surface | M. M. Atalla, E. Tannenbaum and E. J. Scheibner, "Stabilization of silicon surfaces by thermally grown oxides", *Bell Syst. Tech. J.* 38, 749 (1959) |
| D_it ≈ 10¹³ (bare) and ≈ 10¹⁰ cm⁻² eV⁻¹ (thermal oxide); the share rises from about 2% to 96% | Typical values: Sze and Ng, ch. 4; E. H. Nicollian and J. R. Brews, *MOS Physics and Technology* (Wiley, 1982). Model: `physics.share_reaching_channel` |
| 1958 Kilby's IC (Texas Instruments); 1959 Hoerni's planar process and Noyce's planar IC | Computer History Museum, *The Silicon Engine*: "1958: All semiconductor 'solid circuit' is demonstrated", "1959: Practical monolithic integrated circuit concept patented"; J. A. Hoerni, US patent 3,025,589; R. N. Noyce, US patent 2,981,877 |
| Atalla and Kahng's MOSFET, 1959–60 | D. Kahng and M. M. Atalla, "Silicon-silicon dioxide field induced surface devices", IRE-AIEE Solid-State Device Research Conference, Pittsburgh, 1960; CHM, "1960: Metal oxide semiconductor (MOS) transistor demonstrated" |
| Kahng's patent, filed 31 May 1960: thermally grown oxide of about 1000 Å, p-type regions in n-type silicon | D. Kahng, US patent 3,102,230 (granted 27 August 1963) |
| Wanlass's CMOS patent, filed 18 June 1963 | F. M. Wanlass, US patent 3,356,858 (granted 5 December 1967) |
| Band bending, inversion at ψ_s = 2φ_F; V_T = V_FB + 2φ_F + Q_dep/C_ox | Sze and Ng, ch. 4 and 6; Taur and Ning, ch. 2 and 3 |
| V_T ≈ 0.34 V (N_A = 10¹⁷ cm⁻³, t_ox = 10 nm, V_FB = −0.98 V) | Model: `physics.threshold_voltage` |
| Square law I_D = ½ µC_ox (W/L)(V_GS − V_T)²; 173 µA for W/L = 10 at 0.5 V overdrive | Razavi, ch. 2. Model: `physics.square_law_current`, with µ = 400 cm²/V·s and a 10 nm oxide |
| Pinch-off and the gradual-channel derivation | Taur and Ning, ch. 3 |
| CMOS, 1963 | F. M. Wanlass and C. T. Sah, "Nanowatt logic using field-effect metal-oxide semiconductor triodes", *ISSCC Digest of Technical Papers*, 32–33 (1963) |
| P = α C V² f | N. Weste and D. Harris, *CMOS VLSI Design*, 4th ed. (Addison-Wesley, 2010), ch. 5. Computed in `physics.dynamic_power` |
| Latch-up: the parasitic p-n-p-n, β_npn β_pnp > 1; guard rings and close taps | Weste and Harris, ch. 7; Hastings, ch. 4 |

## Chapter 4 · The free lunch

| Claim | Source |
|---|---|
| Moore's 1965 line, about 65,000 components by 1975 | G. E. Moore, "Cramming more components onto integrated circuits", *Electronics* 38(8), 19 April 1965. Points read approximately from his figure |
| Revised to doubling every two years | G. E. Moore, "Progress in digital integrated electronics", IEDM 1975 |
| Transistor counts: 4004 (2,300), 8086 (29,000), 386 (275,000), Pentium (3.1 M), Pentium 4 (42 M), Core 2 Duo (291 M), Apple M1 (16 B), M3 Max (92 B), NVIDIA B200 (208 B) | Intel, Apple and NVIDIA product announcements. The 1975 line's value for 2024 is `physics.moore_count` |
| Dennard's one-transistor DRAM cell, patented 1968 | R. H. Dennard, "Field-effect transistor memory", US patent 3,387,286 (4 June 1968) |
| The 4004's layout, drawn by hand | F. Faggin, "The making of the first microprocessor", *IEEE Solid-State Circuits Magazine* 1(1), 8–21 (2009) |
| Dennard's scaling table | R. H. Dennard et al., *IEEE J. Solid-State Circuits* SC-9(5), 256 (1974). Factors in `physics.DENNARD` |
| λ rules | C. Mead and L. Conway, *Introduction to VLSI Systems* (Addison-Wesley, 1980); the widths shown (poly 2λ, diffusion and metal 3λ) are those of the MOSIS scalable CMOS (SCMOS) rules |

## Chapter 5 · Boltzmann's tyranny

| Claim | Source |
|---|---|
| Boltzmann distribution; k_BT = 25.9 meV at 300 K | Any statistical-physics text; computed in `physics.thermal_voltage` |
| Subthreshold swing SS = m (k_BT/q) ln 10 ≥ 60 mV/decade; m = 1 + C_dep/C_ox | S. M. Sze and K. K. Ng, *Physics of Semiconductor Devices*, 3rd ed. (Wiley, 2007), ch. 6; Y. Taur and T. H. Ning, *Fundamentals of Modern VLSI Devices*, 2nd ed. (Cambridge, 2009), ch. 3 |
| 15 mV/decade at 77 K | The same formula at 77 K (`physics.subthreshold_swing`) |
| A bipolar transistor's collector current rises 10× per ~60 mV of V_BE | I_C = I_S exp(qV_BE/k_BT); Sze and Ng, ch. 5 |
| The I–V curve (V_T = 0.4 V, m = 1.2) | Model: EKV interpolation in `physics.drain_current` |
| Weak inversion gives the most transconductance per unit current (g_m/I_D) | C. C. Enz, F. Krummenacher and E. A. Vittoz, "An analytical MOS transistor model valid in all regions of operation…", *Analog Integr. Circuits Signal Process.* 8, 83 (1995); P. G. A. Jespers and B. Murmann, *Systematic Design of Analog CMOS Circuits* (Cambridge, 2017) |
| Dennard scaling | R. H. Dennard et al., "Design of ion-implanted MOSFET's with very small physical dimensions", *IEEE J. Solid-State Circuits* SC-9(5), 256–268 (1974) |
| Clock speeds, 1971–2020 (approximate) | Intel product specifications for the 4004, 8086, 80286, 386, 486, Pentium, Pentium II, Pentium 4, Core 2 Extreme X6800, Core i7-2600K, Core i7-7700K and Core i9-10900K (base clocks) |
| Power density: nuclear reactor by 2005, rocket nozzle by 2010, Sun's surface by 2015 | P. P. Gelsinger, "Microprocessors for the new millennium: challenges, opportunities, and new frontiers", ISSCC 2001 keynote, *ISSCC Digest of Technical Papers*, 22–25 (2001) |
| A 1.2 nm gate oxide (about five atomic layers) | S. Thompson et al., "A 90 nm logic technology featuring 50 nm strained silicon channel transistors…", IEDM 2002 |
| Direct tunnelling ~10× per 0.2 nm; Φ_B ≈ 3.1 eV, m* ≈ 0.4 m₀ | Model: WKB in `physics.tunnel_transmission`, with textbook Si/SiO₂ values (Taur and Ning, ch. 2) |
| HfO₂ k ≈ 20; EOT = t (3.9/k) | G. D. Wilk, R. M. Wallace and J. M. Anthony, "High-κ gate dielectrics: current status and materials properties considerations", *J. Appl. Phys.* 89, 5243 (2001) |
| High-k + metal gate at Intel 45 nm, 2007 | K. Mistry et al., "A 45nm logic technology with high-k+metal gate transistors, strained silicon, 9 Cu interconnect layers…", IEDM 2007 |

## Chapter 6 · Losing grip

| Claim | Source |
|---|---|
| The quasi-2D (Gauss's-law) channel model, d²φ/dx² − (φ − φ_gs)/λ² = 0, and its sinh solution | K. K. Young, "Short-channel effect in fully depleted SOI MOSFETs", *IEEE Trans. Electron Devices* 36(2), 399 (1989); R.-H. Yan, A. Ourmazd and K. F. Lee, "Scaling the Si MOSFET: from bulk to SOI to bulk", *IEEE Trans. Electron Devices* 39(7), 1704 (1992). Computed in `physics.channel_potential` |
| λ = √(ε_Si t_Si t_ox / (N ε_ox)), N the equivalent number of gates (1 planar, 2 double gate, about 3 tri-gate, 4 all around) | J.-P. Colinge, "Multiple-gate SOI MOSFETs", *Solid-State Electronics* 48(6), 897 (2004). Computed in `physics.natural_length_nm` |
| Barrier heights, threshold roll-off and DIBL against L/λ (e.g. 157 mV/V at 3λ, 39 at 6λ, 5 at 10λ); leakage ratios at 60 mV per decade | Model: `physics.barrier_height` and `physics.dibl_mV_per_V`, with V_bi = 1 V and a 0.6 eV long-channel barrier |
| SS ≈ 60 mV/dec / (1 − 2e^(−L/2λ)) | K. Suzuki et al., "Scaling theory for double-gate SOI MOSFETs", *IEEE Trans. Electron Devices* 40(12), 2326 (1993). Computed in `physics.short_channel_swing` |
| Keep L ≳ 6λ (sources quote 5 to 10) | Rule of thumb; see Yan et al. (1992) and Colinge (2004) |
| g_ds = η g_m, so g_m r_o = 1/η when DIBL alone sets the output conductance | Model: `physics.self_gain_from_dibl`. Background: Y. Tsividis and C. McAndrew, *Operation and Modeling of the MOS Transistor*, 3rd ed. (Oxford, 2011), ch. 6 |
| λ = 6.7, 3.9, 2.4 and 1.9 nm for N = 1 to 4 (15, 10, 6 and 5 nm channels; 1 nm oxide) | Model: `physics.natural_length_nm` |

## Chapter 7 · FinFET

| Claim | Source |
|---|---|
| DELTA, a vertical thin-silicon transistor gated from both sides (Hitachi, 1989) | D. Hisamoto, T. Kaga, Y. Kawamoto and E. Takeda, "A fully depleted lean-channel transistor (DELTA): a novel vertical ultra thin SOI MOSFET", IEDM 1989 |
| The Berkeley FinFET, 1998–99, under DARPA funding | D. Hisamoto et al., "A folded-channel MOSFET for deep-sub-tenth micron era", IEDM 1998; X. Huang et al., "Sub 50-nm FinFET: PMOS", IEDM 1999 |
| The FinFET patent, filed 23 October 2000 (Fig. 1 shown) | C. Hu, T.-J. King, V. Subramanian, L. Chang, X. Huang, Y.-K. Choi, J. Kedzierski, N. Lindert, J. Bokor and W.-C. Lee (University of California), US patent 6,413,802 B1, granted 2 July 2002 |
| Intel's 22 nm tri-gate transistors: announced May 2011, in products in 2012 | Intel press announcement, 4 May 2011; C. Auth et al., "A 22nm high performance and low-power CMOS technology featuring fully-depleted tri-gate transistors…", VLSI 2012 |
| The FinFET model: 6 nm fins, 45 nm tall, 27 nm pitch, 18 nm gate | FET Lab's FinFET (`data/devices.json`, key `fin`), after TSMC US 9,812,358 B1 |
| W_eff = N_fin (2H_fin + W_fin) = 192 nm for two fins | Model: `physics.weff_fin_nm` |
| "3 nm" node: 48 nm contacted gate pitch, 24 nm tightest metal pitch | IEEE IRDS 2021, More Moore (G48M24). TSMC N3: 45 nm gate pitch, 23 nm metal pitch (IEDM 2022) |
| Mobility falls about as t⁶ below ~5 nm (thickness fluctuation scattering) | K. Uchida et al., "Experimental study on carrier transport mechanism in ultrathin-body SOI n- and p-MOSFETs with SOI thickness less than 5 nm", IEDM 2002. Illustrative ratio in `physics.roughness_mobility_ratio` |
| The FinFET inverter layout | FET Lab's schematic layout model (`show_fin`) |

## Chapter 8 · Nanosheets

| Claim | Source |
|---|---|
| Stacked nanosheets (IBM, GlobalFoundries, Samsung), 2017 | N. Loubet et al., "Stacked nanosheet gate-all-around transistor to enable scaling beyond FinFET", VLSI 2017 |
| Samsung's 3 nm GAA production began 30 June 2022 | Samsung Electronics, "Samsung begins chip production using 3nm process technology with GAA architecture", 30 June 2022 |
| TSMC N2 in volume production in the fourth quarter of 2025 | TSMC announcement (reported December 2025) |
| Intel 18A: RibbonFET and PowerVia, 2025 | Intel |
| The nanosheet model: three sheets, 5 nm thick, 30 nm wide | FET Lab's nanosheet nFET (`data/geometry.json`), after IBM US 2023/0420457 A1 |
| W_eff = N_sh · 2(W_sh + T_sh) = 210 nm | Model: `physics.weff_sheets_nm` |
| The process: Si/SiGe stack, dummy gate, recess, SiGe indent, inner spacers, epitaxy, dummy-gate removal, SiGe release, high-k and metal gate | FET Lab's nanosheet process (`data/process.json`), after IBM US 2023/0420457 A1; N. Loubet et al., "A novel dry selective etch of SiGe for the enablement of high performance logic stacked gate-all-around nanosheet devices", IEDM 2019 |
| Cell height = tracks × metal pitch (6 × 24 nm = 144 nm) | imec, "A view on the logic technology roadmap". Computed in `physics.cell_height_nm` |
| The n-to-p space in the nanosheet inverter layout (46 nm) | FET Lab's schematic layout model (`show_ns`) |

## Chapter 9 · Forksheet

| Claim | Source |
|---|---|
| imec's forksheet, proposed in 2017 | P. Weckx et al., "Stacked nanosheet fork architecture for SRAM design and device co-optimization toward 3nm", IEDM 2017 |
| Forksheets with dual work-function metal gates at 17 nm n-to-p space; short-channel control on par with nanosheets down to 22 nm gates | H. Mertens et al., "Forksheet FETs for advanced CMOS scaling: forksheet-nanosheet co-integration and dual work function metal gates at 17nm N-P space", VLSI 2021 |
| The outer-wall forksheet at the A10 node (projection) | imec, "Outer wall forksheet to bridge nanosheet and CFET device architectures in the logic technology roadmap" |
| A foundry forksheet patent (Fig. 12 shown) | TSMC, US patent 11,862,700 B2, granted 2 January 2024 |
| The forksheet model: 5 nm sheets, 8 nm SiN wall | FET Lab's forksheet pair (`fs`), after imec EP 3 989 273 A1 |
| λ = 2.2 nm with three faces (N = 3) against 1.9 nm with four | Model: `physics.natural_length_nm` |
| Cell height 136 → 106 nm, rail to rail | FET Lab's schematic layout models (`show_ns`, `show_fs`); `devicedata.rail_span_nm` |

## Chapter 10 · CFET

| Claim | Source |
|---|---|
| imec's CFET proposal, 2018 | J. Ryckaert et al., "The Complementary FET (CFET) for CMOS scaling beyond N3", VLSI 2018 |
| IEDM 2023: Intel a stacked CMOS inverter at 60 nm gate pitch; TSMC CFETs at 48 nm gate pitch; Samsung also. IEDM 2024: TSMC a working CFET inverter at 48 nm | IEEE Spectrum, "Intel, Samsung, and TSMC demo 3D-stacked transistors", December 2023; Intel IEDM 2023 paper 29.2; TSMC IEDM 2023 and 2024 |
| Monolithic CFET at imec's A7 node (projection) | imec, "Performance boosters to scale monolithic CFET across multiple logic technology nodes" |
| Monolithic against sequential integration; the temperature limit after layer transfer | imec, "Imec puts complementary FET (CFET) on the logic technology roadmap" |
| A CFET patent (Fig. 17 shown) | IBM, US patent 11,869,812 B2, granted 9 January 2024 |
| The CFET model: 5 nm sheets, a 12 nm gap between the tiers, one common gate | FET Lab's monolithic CFET (`cfet_mono`), after IBM US 11,869,812 B2; sequential: `cfet_seq`, after TSMC US 2024/0413156 A1 |
| Inverter cell heights 156, 136, 106 and 74 nm, rail to rail | FET Lab's schematic layout models (`show_fin`, `show_ns`, `show_fs`, `show_cfet`). Not foundry cells |
| R = ρL/(wt): 25 Ω per µm for a 20 × 40 nm rail (ρ = 2 × 10⁻⁸ Ω m) | Model: `physics.wire_resistance_ohm`; illustrative dimensions |
| PowerVia: >30% less platform voltage droop, 6% frequency benefit, >90% cell utilization (test chip) | Intel, VLSI Symposium 2023 (June 2023) |
| ΔT = P R_th; the upper tier is further from the heat path | Qualitative |
| 5 nm of silicon is about 37 atomic layers | Si (100) layer spacing a/4 = 0.136 nm |

## Live Lab 2 · Who controls the barrier?

| Claim | Source |
|---|---|
| The barrier, λ, DIBL and swing it shows | Chapter 6's quasi-2D model, ported line for line to `labs/lab-physics.js`; `tests/test_physics.py` checks the port against `physics.py` |
| Channel thickness per architecture (planar 15 nm effective depth, double gate 10, fin 6, sheets 5, 2D 0.65) | Illustrative values, as in chapter 6; every channel uses silicon's permittivity |

## Chapter 11 · Beyond silicon, beyond Boltzmann

| Claim | Source |
|---|---|
| Mobility falls about as t⁶ in very thin silicon (5 → 3 nm: ×0.05) | K. Uchida et al., IEDM 2002 (see chapter 7). Illustrative ratio in `physics.roughness_mobility_ratio` |
| A MoS₂ monolayer is about 0.65 nm thick; 2D surfaces have no dangling bonds | B. Radisavljevic et al., "Single-layer MoS₂ transistors", *Nature Nanotechnology* 6, 147 (2011) |
| λ ≈ 1.0 nm for a 0.65 nm layer gated on both sides (1 nm oxide), against 1.9 nm for a 5 nm silicon sheet | Model: `physics.natural_length_nm`, with silicon's permittivity for both |
| 2D channels on imec's roadmap after the CFET, around the A2 node, early 2040s (projection) | imec, "Introducing 2D-material based devices in the logic scaling roadmap" (https://www.imec-int.com/en/articles/introducing-2d-material-based-devices-logic-scaling-roadmap) |
| Fermi-level pinning at metal contacts to 2D semiconductors | Y. Liu et al., "Approaching the Schottky–Mott limit in van der Waals metal–semiconductor junctions", *Nature* 557, 696 (2018), and references there |
| Semimetal (bismuth) contacts on MoS₂ with contact resistance near the quantum limit, 2021 | P.-C. Shen et al., "Ultralow contact resistance between semimetal and monolayer semiconductors", *Nature* 593, 211 (2021) |
| Tunnel FETs: band-to-band tunnelling cuts off the Boltzmann tail; swings below 60 mV/dec shown, on-currents low | A. M. Ionescu and H. Riel, "Tunnel field-effect transistors as energy-efficient electronic switches", *Nature* 479, 329 (2011) |
| Negative capacitance: a ferroelectric gate layer can give m < 1 | S. Salahuddin and S. Datta, "Use of negative capacitance to provide voltage amplification for low power nanoscale devices", *Nano Letters* 8, 405 (2008). m = 1 + C_dep/C_ins, `physics.body_factor` |
| Source-to-drain tunnelling equals the thermal leak at about 5 nm (0.4 eV barrier, m* = 0.2 m₀) | Model: WKB in `physics.source_drain_tunnelling` and `physics.tunnelling_crossover_nm` |
| Landauer's limit k_BT ln 2 ≈ 2.9 zJ at 300 K | R. Landauer, "Irreversibility and heat generation in the computing process", *IBM J. Res. Dev.* 5, 183 (1961); measured: A. Bérut et al., *Nature* 483, 187 (2012) |
| A logic node's switching energy, ½CV² ≈ 25 aJ (0.1 fF at 0.7 V) | Illustrative estimate, `physics.switching_energy_J` |
| Vertical-transport FET (VTFET), 2021 | IBM and Samsung, announced at IEDM, December 2021 |
| RV16X-NANO: a 16-bit RISC-V processor of more than 14,000 carbon-nanotube transistors | G. Hills et al., "Modern microprocessor built from complementary carbon nanotube transistors", *Nature* 572, 595 (2019) |
| A tunnel FET's source and drain are doped p⁺ and n⁺, so it is asymmetric | Ionescu and Riel (2011) |

## Chapter 12 · Outro

| Claim | Source |
|---|---|
| The table of eras | Chapters 1 to 11 of this lecture, and their sources above |
| Shortest gates ≈ 6λ: 40, 15, 12, 13, 12 and 6 nm | Model: `physics.natural_length_nm`, 1 nm oxide (EOT) |
| (k_BT/q) ln 10 = 59.5 mV per decade at 300 K | `physics.subthreshold_swing` |

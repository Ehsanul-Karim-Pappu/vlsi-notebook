# Sources

Every date, name and number on the slides, with where it comes from. Results of the lecture's
own simple models are labelled "model" on screen and computed in `physics.py`.

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

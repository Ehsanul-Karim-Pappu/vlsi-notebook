# Sources

The sources behind the dates, names and numbers on the slides. A source listed here supports the
claim as the slide words it; where it supports less than that, the row says so. Results of the
lecture's own simple models are labelled "model" or "toy model" on screen and computed in
`physics.py`; they are teaching estimates, not predictions for real devices. Roadmap dates are
projections and are labelled that way. The historical photos and patent drawings, with their
sources and licences, are listed in [images/CREDITS.md](images/CREDITS.md).

Having a source is not the same as the source being enough. The rows marked *gap* below say
where a citation is weaker than the claim and what the slide does about it.

## Chapter 0 · Cold open

| Claim | Source |
|---|---|
| About 13 sextillion (1.3 × 10²²) transistors made, cumulatively | Jim Handy (Objective Analysis), reported in D. Laws, "13 Sextillion & Counting: The Long & Winding Road to the Most Frequently Manufactured Human Artifact in History", Computer History Museum, published 2 April 2018. An estimate, not a census, and not a 2026 total. https://computerhistory.org/blog/13-sextillion-counting-the-long-winding-road-to-the-most-frequently-manufactured-human-artifact-in-history/ |
| "The most frequently manufactured human artifact in history" | David C. Brock, historian, quoted in the same Computer History Museum article |
| About 1.6 trillion per person | Illustrative only: the 2018 estimate divided by today's world population of about 8.1 billion, which mixes dates (said on the slide) |
| Apple A20 Pro (September 2026), made on TSMC's 2 nm (N2) process with nanosheet (gate-all-around) transistors | Apple Newsroom, "Apple debuts iPhone 18 Pro and iPhone 18 Pro Max", September 2026 (A20 Pro, 2 nm); TechInsights, "Apple A20 Pro: TSMC 2nm processor analysis" (preliminary teardown: TSMC N2, nanosheet GAA); TSMC, "2nm technology" (N2 uses nanosheets; volume production from Q4 2025), https://www.tsmc.com/english/dedicatedFoundry/technology/logic/l_2nm. No transistor count or dimension is given for the A20 Pro on the slides |
| The 3D nanosheet: 15 nm gate, 5 nm sheets | FET Lab's illustrative nanosheet nFET model (`data/geometry.json`), after IBM US 2023/0420457 A1. Not the measured N2 geometry |
| FinFET 2011, nanosheet 2022 | Intel's 22 nm tri-gate announcement, 4 May 2011 (first products 2012); Samsung's 3 nm gate-all-around production announcement, 30 June 2022 (a production milestone, not the invention of the nanosheet) |
| Forksheet ~2030 and CFET ~2033 | imec logic roadmap projections (outer-wall forksheet at A10, monolithic CFET at A7). Projections for imec's variants, not industry commitments. The small forksheet icon in the timeline is the earlier inner-wall concept and is labelled so. https://www.imec-int.com/en/articles/outer-wall-forksheet-bridge-nanosheet-and-cfet-device-architectures-logic-technology ; https://www.imec-int.com/en/articles/performance-boosters-scale-monolithic-cfet-across-multiple-logic-technology-nodes |

## Chapter 1 · Before the switch

| Claim | Source |
|---|---|
| A triode's grid switches the plate current; thermionic emission J = A T² exp(−W/k_BT) | O. W. Richardson (Nobel Prize in Physics 1928) and S. Dushman; Sze and Ng, ch. 3. Computed in `physics.thermionic_current_density`. An emission law, not the full plate-current law |
| ENIAC (1946): about 18,000 vacuum tubes, about 150 kW | University of Pennsylvania, "ENIAC" history page, https://www.engineering.upenn.edu/about/history-heritage/eniac/. The often-quoted exact count, 17,468, is not used because we have no primary inventory for it. The photo (Glen Beck and Betty Snyder) is from about 1947 |
| Lilienfeld's field-effect device | J. E. Lilienfeld, Canadian patent application 272,437 (22 October 1925); US patent 1,745,175, "Method and apparatus for controlling electric currents", filed 8 October 1926, granted 28 January 1930. The modern-style drawing on the slide is an analogy, labelled as such; the patent's own figure is shown beside it |
| Induced sheet charge n_s ≈ 2.2 × 10¹² cm⁻² (t_ox = 100 nm, V_G = 10 V) | Model: an ideal capacitor, n_s = C_ox V_G / q, in `physics.induced_sheet_density_cm2` ("on paper") |
| Shockley's 1945 field-effect experiments failed | M. Riordan and L. Hoddeson, *Crystal Fire: The Birth of the Information Age* (Norton, 1997), ch. 6. Why Lilienfeld's own devices did or didn't work is not known with certainty |
| Surface states screen the gate's field | J. Bardeen, "Surface states and rectification at a metal semi-conductor contact", *Phys. Rev.* 71, 717 (1947) |
| About 2% of the induced charge ends up in the semiconductor (D_it ≈ 10¹³ cm⁻² eV⁻¹), the rest in surface states | Model: C_dep / (C_dep + C_it), with C_it = q·D_it (D_it per eV) at N_A = 10¹⁶ cm⁻³, in `physics.share_in_semiconductor`. A small-signal capacitance share at one bias, not the mobile channel charge |

## Chapter 2 · The unexpected transistor

| Claim | Source |
|---|---|
| Bardeen and Brattain were deliberately looking for amplification; the point-contact mechanism was the unexpected part | W. H. Brattain's laboratory notebook, December 1947 (facsimile, PBS/AIP, "Transistorized!"), https://www.pbs.org/transistor/science/labpages/labpg1.html |
| The point-contact transistor: amplified on 16 December 1947, shown to Bell Labs management on 23 December | Riordan and Hoddeson, *Crystal Fire*, ch. 7; Computer History Museum, "1947: Invention of the point-contact transistor", *The Silicon Engine* |
| Gold foil on a plastic wedge, a paper-clip spring, contacts about 50 µm apart | The same CHM page; J. Bardeen and W. H. Brattain, "The transistor, a semi-conductor triode", *Phys. Rev.* 74, 230 (1948) |
| Bardeen and Brattain's patent, filed 17 June 1948, granted 3 October 1950 | US patent 2,524,035 |
| Shockley's patent, filed 26 June 1948, granted 25 September 1951 | US patent 2,569,347 |
| Shockley's junction transistor, conceived in January 1948 | W. Shockley, "The theory of p-n junctions in semiconductors and p-n junction transistors", *Bell Syst. Tech. J.* 28, 435 (1949); US patent 2,569,347 |
| I_C = I_S exp(qV_BE/k_BT): 10× per about 60 mV | Sze and Ng, ch. 5 (ideal forward-active transistor, ideality factor 1). Computed in `physics.collector_current` |
| ΔV_BE = (k_BT/q) ln N = 53.8 mV for a 1 : 8 pair at equal currents, proportional to T | P. Brokaw, "A simple three-terminal IC bandgap reference", *IEEE J. Solid-State Circuits* SC-9(6), 388 (1974); B. Razavi, *Design of Analog CMOS Integrated Circuits*, 2nd ed. (McGraw-Hill, 2017), ch. 12. Computed in `physics.delta_vbe` |
| Common-centroid arrays and dummy devices for matching | A. Hastings, *The Art of Analog Layout*, 2nd ed. (Prentice Hall, 2006), ch. 7 and 9 |

## Chapter 3 · Glass

| Claim | Source |
|---|---|
| Silicon's own oxide masks diffusion (found in 1955, published 1957) | C. J. Frosch and L. Derick, "Surface protection and selective masking during diffusion in silicon", *J. Electrochem. Soc.* 104, 547 (1957) |
| Thermal oxide passivates the surface | M. M. Atalla, E. Tannenbaum and E. J. Scheibner, "Stabilization of silicon surfaces by thermally grown oxides", *Bell Syst. Tech. J.* 38, 749 (1959) |
| D_it ≈ 10¹³ (bare) and ≈ 10¹⁰ cm⁻² eV⁻¹ (thermal oxide); the semiconductor's share rises from about 2% to 96% | Typical values: Sze and Ng, ch. 4; E. H. Nicollian and J. R. Brews, *MOS Physics and Technology* (Wiley, 1982). Model: `physics.share_in_semiconductor`, C_it = q·D_it. *Gap:* the 1959 paper shows the passivation; the percentages are the model's, not measurements from it |
| 1958 Kilby's IC (Texas Instruments); 1959 Hoerni's planar process and Noyce's planar IC | Computer History Museum, *The Silicon Engine*: "1958: All semiconductor 'solid circuit' is demonstrated", "1959: Practical monolithic integrated circuit concept patented"; J. A. Hoerni, US patent 3,025,589; R. N. Noyce, US patent 2,981,877 |
| Atalla and Kahng's MOSFET, 1959–60 | D. Kahng and M. M. Atalla, "Silicon-silicon dioxide field induced surface devices", IRE-AIEE Solid-State Device Research Conference, Pittsburgh, 1960; CHM, "1960: Metal oxide semiconductor (MOS) transistor demonstrated" |
| Kahng's patent, filed 31 May 1960: thermally grown oxide of about 1000 Å, p-type regions in n-type silicon (a p-channel device; the lecture's band pictures use an n-channel one, as the slide says) | D. Kahng, US patent 3,102,230 (granted 27 August 1963) |
| Wanlass's CMOS patent, filed 18 June 1963 | F. M. Wanlass, US patent 3,356,858 (granted 5 December 1967) |
| Band bending; at ψ_s = 2φ_F the surface electron density equals the bulk hole density; V_T = V_FB + 2φ_F + Q_dep/C_ox | Sze and Ng, ch. 4 and 6; Taur and Ning, ch. 2 and 3 |
| V_T ≈ 0.34 V (N_A = 10¹⁷ cm⁻³, t_ox = 10 nm, V_FB = −0.98 V) | Model: `physics.threshold_voltage` (long channel, no body bias) |
| Square law I_D = ½ µC_ox (W/L)(V_GS − V_T)²; 173 µA for W/L = 10 at 0.5 V overdrive | Razavi, ch. 2. Model: `physics.square_law_current`, with µ = 400 cm²/V·s and a 10 nm oxide; no channel-length modulation |
| Pinch-off and the gradual-channel derivation | Taur and Ning, ch. 3 |
| CMOS, 1963 | F. M. Wanlass and C. T. Sah, "Nanowatt logic using field-effect metal-oxide semiconductor triodes", *ISSCC Digest of Technical Papers*, 32–33 (1963) |
| With the input at a rail, ideally no path from supply to ground; while the input passes mid-rail both conduct briefly (short-circuit current); leakage always | MIT 6.012, lecture 15 (CMOS inverter), https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-fall-2009/ ; Weste and Harris, ch. 5 |
| P = α C V² f (+ P_sc + V_DD I_leak); α counts 0 → 1 transitions per cycle | N. Weste and D. Harris, *CMOS VLSI Design*, 4th ed. (Addison-Wesley, 2010), ch. 5. Computed in `physics.dynamic_power` |
| Latch-up: the parasitic p-n-p-n, β_npn β_pnp > 1 (a simplified criterion); guard rings and close taps reduce the risk | Weste and Harris, ch. 7; Hastings, ch. 4 |

## Chapter 4 · The free lunch

| Claim | Source |
|---|---|
| Moore's 1965 line, about 65,000 components by 1975 | G. E. Moore, "Cramming more components onto integrated circuits", *Electronics* 38(8), 19 April 1965. Points read approximately from his figure |
| Revised to doubling every two years | G. E. Moore, "Progress in digital integrated electronics", IEDM 1975 |
| Transistor counts: 4004 (2,300), 8086 (29,000), 386 (275,000), Pentium (3.1 M), Pentium 4 (42 M), Core 2 Duo (291 M), Apple M1 (16 B), M3 Max (92 B), NVIDIA B200 (208 B) | Manufacturers' figures: Intel product pages and museum material for the Intel parts; Apple, "Apple unleashes M1" (10 November 2020) and "Apple unveils M3, M3 Pro, and M3 Max" (30 October 2023); NVIDIA, Blackwell architecture page (208 B across two reticle-limited dies, labelled "2 dies" on the slide). *Gap:* the early Intel counts are widely quoted figures; we have not tied each to one dated Intel page |
| The extrapolated line (218 billion in 2024) | The lecture's own extrapolation from the 4004 (1971, 2,300) doubling every two years, `physics.moore_count`. Labelled "our extrapolation" on the slide; not a point Moore plotted |
| Dennard's one-transistor DRAM cell, patented 1968 | R. H. Dennard, "Field-effect transistor memory", US patent 3,387,286 (4 June 1968) |
| The 4004's layout, drawn by hand | F. Faggin, "The making of the first microprocessor", *IEEE Solid-State Circuits Magazine* 1(1), 8–21 (2009) |
| Dennard's scaling table (ideal constant-field scaling) | R. H. Dennard et al., "Design of ion-implanted MOSFET's with very small physical dimensions", *IEEE J. Solid-State Circuits* SC-9(5), 256 (1974). Factors in `physics.DENNARD` |
| λ rules | C. Mead and L. Conway, *Introduction to VLSI Systems* (Addison-Wesley, 1980); the widths shown (poly 2λ, diffusion and metal 3λ) are those of the MOSIS scalable CMOS (SCMOS) rules. The drawing is schematic, not DRC-checked. This λ is a layout grid unit, not chapter 6's electrostatic λ |

## Chapter 5 · Boltzmann's tyranny

| Claim | Source |
|---|---|
| Boltzmann factor; k_BT = 25.9 meV at 300 K | Any statistical-physics text; computed in `physics.thermal_voltage` |
| Subthreshold swing SS = m (k_BT/q) ln 10 ≥ 60 mV/decade for a conventional MOSFET; m = 1 + C_dep/C_ox | S. M. Sze and K. K. Ng, *Physics of Semiconductor Devices*, 3rd ed. (Wiley, 2007), ch. 6; Y. Taur and T. H. Ning, *Fundamentals of Modern VLSI Devices*, 2nd ed. (Cambridge, 2009), ch. 3 |
| 15 mV/decade at 77 K | The ideal formula at 77 K (`physics.subthreshold_swing`). Real cryogenic MOSFETs saturate well above it: A. Beckers, F. Jazaeri and C. Enz, "Characterization and modeling of 28-nm bulk CMOS technology down to 4.2 K", arXiv:1806.02142 (2018) |
| A bipolar transistor's collector current rises 10× per ~60 mV of V_BE | I_C = I_S exp(qV_BE/k_BT); Sze and Ng, ch. 5 |
| The I–V curve (V_T = 0.4 V, m = 1.2); ≈10× per swing, ≈1000× for three | Model: EKV interpolation in `physics.drain_current`, with the specific current I_spec ∝ m U_T² (`physics.specific_current`). The ratios are approximate because the marked points are not deep in weak inversion |
| Weak inversion gives the most transconductance per unit current (g_m/I_D) | C. C. Enz, F. Krummenacher and E. A. Vittoz, "An analytical MOS transistor model valid in all regions of operation…", *Analog Integr. Circuits Signal Process.* 8, 83 (1995); P. G. A. Jespers and B. Murmann, *Systematic Design of Analog CMOS Integrated Circuits* (Cambridge, 2017) |
| Dennard scaling | R. H. Dennard et al., *IEEE J. Solid-State Circuits* SC-9(5), 256–268 (1974) |
| Base clock speeds, 1971–2020 (approximate); base clocks levelled at about 3–4 GHz from about 2004 | Intel product specifications for the 4004, 8086, 80286, 386, 486, Pentium, Pentium II, Pentium 4, Core 2 Extreme X6800, Core i7-2600K, Core i7-7700K and Core i9-10900K (base clocks). Turbo clocks go higher: the Core i9-14900KS reaches 6.2 GHz maximum turbo (Intel specifications; announced 14 March 2024) |
| Power density heading past a hot plate toward a nuclear reactor, a rocket nozzle and the Sun's surface | P. P. Gelsinger, ISSCC 2001 keynote talk. *Gap:* the published digest ("Microprocessors for the new millennium: challenges, opportunities, and new frontiers", *ISSCC Digest of Technical Papers*, 22–25, 2001) supports the power concern but does not carry the chart; the comparison comes from the talk's slides as widely reproduced. The slide therefore gives no years |
| A 1.2 nm gate oxide (about five atomic layers) | S. Thompson et al., "A 90 nm logic technology featuring 50 nm strained silicon channel transistors…", IEDM 2002 |
| Direct tunnelling ~10× per 0.2 nm; Φ_B ≈ 3.1 eV, m* ≈ 0.4 m₀ | Model: WKB in `physics.tunnel_transmission`, with textbook Si/SiO₂ values (Taur and Ning, ch. 2) |
| HfO₂ k ≈ 20; EOT = t_IL + t_HK (3.9/k_HK) | G. D. Wilk, R. M. Wallace and J. M. Anthony, "High-κ gate dielectrics: current status and materials properties considerations", *J. Appl. Phys.* 89, 5243 (2001). The 6.2 nm on the slide is one ideal layer, not Intel's measured stack |
| High-k + metal gate at Intel 45 nm, 2007 | K. Mistry et al., "A 45nm logic technology with high-k+metal gate transistors, strained silicon, 9 Cu interconnect layers…", IEDM 2007; Intel press release, 27 January 2007 |

## Chapter 6 · Losing grip

| Claim | Source |
|---|---|
| The quasi-2D (Gauss's-law) channel model, d²φ/dx² − (φ − φ_gs)/λ² = 0, and its sinh solution | K. K. Young, "Short-channel effect in fully depleted SOI MOSFETs", *IEEE Trans. Electron Devices* 36(2), 399 (1989); R.-H. Yan, A. Ourmazd and K. F. Lee, "Scaling the Si MOSFET: from bulk to SOI to bulk", *IEEE Trans. Electron Devices* 39(7), 1704 (1992). Computed in `physics.channel_potential` and, for the barrier top, in closed form in `physics.barrier_top` |
| λ = √(ε_Si t_Si t_ox / (N ε_ox)), N an "equivalent number of gates" (1 planar, 2 double gate, about 3 tri-gate, 4 all around) | A toy model: J.-P. Colinge, "Multiple-gate SOI MOSFETs", *Solid-State Electronics* 48(6), 897 (2004), for square-ish cross-sections. Real shapes need a scale length for the actual geometry: D. J. Frank, Y. Taur and H.-S. P. Wong, "Generalized scale length for two-dimensional effects in MOSFETs", *IEEE Electron Device Lett.* 19(10), 385 (1998). Computed in `physics.natural_length_nm`. Not the layout λ of chapter 4 |
| Barrier heights and barrier DIBL (the barrier top's drop per volt of drain) against L/λ: about 157 mV/V at 3λ, 39 at 6λ, 5 at 10λ; leakage ratios at 60 mV per decade | Toy model: `physics.barrier_height`, `physics.drain_coupling` and `physics.dibl_mV_per_V`, with V_bi = 1 V. Barrier DIBL, not threshold-voltage DIBL |
| SS = 60 mV/dec / (1 − sech(L/2λ)) at V_DS = 0 | Exact for the toy model (`physics.short_channel_swing`); its long-channel limit is the familiar 60 / (1 − 2e^(−L/2λ)) (K. Suzuki et al., "Scaling theory for double-gate SOI MOSFETs", *IEEE Trans. Electron Devices* 40(12), 2326 (1993)) |
| Keep L ≳ 6λ (sources quote 5 to 10) | Rule of thumb; see Yan et al. (1992) and Colinge (2004) |
| Intrinsic gain g_m r_o ≈ α_g/α_d, the gate's and the drain's coupling to the barrier top (about 4, 23 and 190 at 3λ, 6λ and 10λ, V_DS = 0.4 V) | Toy model: `physics.gate_coupling`, `physics.drain_coupling`, `physics.intrinsic_gain`. Background: Y. Tsividis and C. McAndrew, *Operation and Modeling of the MOS Transistor*, 3rd ed. (Oxford, 2011), ch. 6 |
| λ = 6.7, 3.9, 2.4 and 1.9 nm for N = 1 to 4 (15, 10, 6 and 5 nm channels; 1 nm oxide) | Toy model: `physics.natural_length_nm` |

## Live Lab 1 · Boltzmann's fence

| Claim | Source |
|---|---|
| The current against gate voltage at different temperatures and body factors | Illustrative EKV model (`labs/lab-physics.js`, the port of `physics.drain_current`), with I_spec ∝ m U_T² so the curves move with temperature as the model says they should. Not a calibrated device: a real transistor's threshold and mobility also change with temperature |

## Chapter 7 · FinFET

| Claim | Source |
|---|---|
| DELTA, a vertical thin-silicon transistor gated from both sides (Hitachi, 1989) | D. Hisamoto, T. Kaga, Y. Kawamoto and E. Takeda, "A fully depleted lean-channel transistor (DELTA): a novel vertical ultra thin SOI MOSFET", IEDM 1989 |
| The Berkeley FinFET, 1998–99, under DARPA funding | D. Hisamoto et al., "A folded-channel MOSFET for deep-sub-tenth micron era", IEDM 1998; X. Huang et al., "Sub 50-nm FinFET: PMOS", IEDM 1999 |
| The FinFET patent, filed 23 October 2000 (Fig. 1 shown: a double-gate device, with a thick hard mask on top of the fin) | C. Hu, T.-J. King, V. Subramanian, L. Chang, X. Huang, Y.-K. Choi, J. Kedzierski, N. Lindert, J. Bokor and W.-C. Lee (University of California), US patent 6,413,802 B1, granted 2 July 2002 |
| Intel's 22 nm tri-gate transistors: announced 4 May 2011, in products in 2012 | Intel, "22nm transistor backgrounder" (May 2011), https://download.intel.com/newsroom/kits/22nm/pdfs/Intel_Transistor_Backgrounder.pdf ; C. Auth et al., "A 22nm high performance and low-power CMOS technology featuring fully-depleted tri-gate transistors…", VLSI 2012 |
| The FinFET model: 6 nm fins, 45 nm tall, 27 nm pitch, 18 nm gate | FET Lab's FinFET (`data/devices.json`, key `fin`), after TSMC US 9,812,358 B1 |
| W_eff = N_fin (2H_fin + W_fin) = 192 nm for two fins; current flows from source to drain along the fin, on its sidewalls and top | Model: `physics.weff_fin_nm` |
| Two fins "on 54 nm of floor" | The allocation convention: two fins on a 27 nm pitch are given 2 × 27 nm. The two fins' own silicon spans 33 nm |
| The "3 nm" node: 48 nm contacted gate pitch, 24 nm tightest metal pitch (a roadmap target) | IEEE IRDS 2021, More Moore, ground rules for the "3 nm" node (G48M24), https://irds.ieee.org/images/files/pdf/2021/2021IRDS_MM.pdf . *Gap:* we cite the roadmap's G48M24 label; a roadmap target is not a measurement of any chip |
| TSMC N3: 45 nm contacted gate pitch; N3E: 23 nm minimum metal pitch | TSMC, IEDM 2022: "Critical process features enabling aggressive contacted gate pitch scaling for 3nm CMOS technology and beyond" (N3) and "A 3nm CMOS FinFlex platform technology with enhanced power efficiency and performance for mobile SoC and high performance computing applications" (N3E); as reported by SemiWiki, "IEDM 2022 – TSMC 3nm" |
| One component of the mobility (thickness-fluctuation scattering) goes roughly as t⁶ in very thin silicon | Illustrative ratio, `physics.roughness_mobility_ratio`. K. Uchida et al., "Experimental study on carrier transport mechanism in ultrathin-body SOI n- and p-MOSFETs with SOI thickness less than 5 nm", IEDM 2002, measured several competing mechanisms (including a mobility rise over 3.5–4.5 nm in some conditions); the slide does not claim a universal cutoff |
| The FinFET inverter layout | FET Lab's schematic layout model (`show_fin`) |

## Chapter 8 · Nanosheets

| Claim | Source |
|---|---|
| Stacked nanosheets (IBM, GlobalFoundries, Samsung), 2017: a research demonstration | N. Loubet et al., "Stacked nanosheet gate-all-around transistor to enable scaling beyond FinFET", VLSI 2017 |
| Samsung's 3 nm GAA production began 30 June 2022 | Samsung Electronics, "Samsung begins chip production using 3nm process technology with GAA architecture", 30 June 2022 |
| TSMC N2 in volume production in the fourth quarter of 2025 | TSMC, "2nm technology" page |
| Intel 18A: RibbonFET and PowerVia, 2025 | Intel Foundry, process milestones (VLSI Symposium 2025); Intel, Panther Lake architecture announcement (first products on 18A) |
| The nanosheet model: three sheets, 5 nm thick, 30 nm wide | FET Lab's nanosheet nFET (`data/geometry.json`), after IBM US 2023/0420457 A1 |
| N ≈ 2 to 4, λ ≈ 1.9 to 2.7 nm for a 5 nm sheet | Toy model (`physics.natural_length_nm`): a wide, thin sheet is gated mostly from above and below |
| W_eff = N_sh · 2(W_sh + T_sh) = 210 nm | Model: `physics.weff_sheets_nm` (a geometric perimeter) |
| The process: a Ge-rich SiGe layer, Si/SiGe stack, dummy gate, bottom dielectric isolation in place of the Ge-rich layer, recess, SiGe indent, inner spacers, epitaxy on the insulator, oxide, dummy-gate removal, SiGe release, high-k and metal gate | One common nFET route, after IBM US 2023/0420457 A1 (its nFET branch uses bottom dielectric isolation; its pFET branch keeps a SiGe channel and differs). Drawn by hand for the slide, simplified, not to scale; planarisation and other steps left out. Selective release: N. Loubet et al., "A novel dry selective etch of SiGe for the enablement of high performance logic stacked gate-all-around nanosheet devices", IEDM 2019 |
| Cell height = tracks × metal pitch: 6 × 24 = 144 nm and 5 × 24 = 120 nm, as examples | Computed in `physics.cell_height_nm`. The model's own rails are 136 nm apart, centre to centre (`show_ns`), a different example; where the cell edge is drawn varies |
| The n-to-p space in the nanosheet inverter layout (46 nm) | FET Lab's schematic layout model (`show_ns`) |

## Chapter 9 · Forksheet

| Claim | Source |
|---|---|
| imec's forksheet (the inner-wall kind, n and p either side of a wall), proposed in 2017 | P. Weckx et al., "Stacked nanosheet fork architecture for SRAM design and device co-optimization toward 3nm", IEDM 2017 |
| Integrated forksheets with dual work-function metal gates at 17 nm n-to-p space; SS of 66–68 mV/dec, comparable to co-integrated nanosheets, with gates down to 22 nm | H. Mertens et al., "Forksheet FETs for advanced CMOS scaling: forksheet-nanosheet co-integration and dual work function metal gates at 17nm N-P space", VLSI 2021; imec press release, 15 June 2021, https://www.imec-int.com/en/press/imec-reports-first-electrical-demonstration-integrated-forksheet-devices-extend-nanosheets . Those devices and dimensions, not every forksheet |
| The outer-wall forksheet (wall at the cell edge, between devices of the same type; a thicker wall; the gate can wrap partly round the wall side) at the A10 node (projection) | imec, "Outer wall forksheet to bridge nanosheet and CFET device architectures in the logic technology roadmap" (2025), https://www.imec-int.com/en/articles/outer-wall-forksheet-bridge-nanosheet-and-cfet-device-architectures-logic-technology |
| A foundry forksheet patent (Fig. 12 shown: a stage during manufacture, with sacrificial gate 142) | TSMC, US patent 11,862,700 B2, granted 2 January 2024 |
| The forksheet model: 5 nm sheets, 8 nm SiN wall (inner wall) | FET Lab's forksheet pair (`fs`), after imec EP 3 989 273 A1 |
| Cell height 136 → 106 nm, rail to rail (about 22% shorter) | FET Lab's schematic layout models (`show_ns`, `show_fs`); `devicedata.rail_span_nm`. Model cells, not a foundry's measured area |

## Chapter 10 · CFET

| Claim | Source |
|---|---|
| imec's CFET proposal, 2018 | J. Ryckaert et al., "The Complementary FET (CFET) for CMOS scaling beyond N3", VLSI 2018 |
| IEDM 2023: Intel, functional stacked CMOS inverters at 60 nm gate pitch; TSMC, CFETs at 48 nm gate pitch; Samsung, stacked devices. IEDM 2024: TSMC, the first monolithic CFET inverter at 48 nm | Intel, "Intel demonstrates breakthroughs in next-generation transistor scaling for future nodes", December 2023, https://www.intel.com/content/www/us/en/newsroom/news/research-advancements-extend-moore-law.html ; S. Liao et al. (TSMC), "Complementary field-effect transistor (CFET) demonstration at 48nm gate pitch for future logic technology scaling", IEDM 2023; S. Liao et al. (TSMC), "First demonstration of monolithic CFET inverter at 48nm gate pitch toward future logic technology scaling", IEDM 2024; IEEE Spectrum, "Intel, Samsung, and TSMC demo 3D-stacked transistors", December 2023. *Gap:* Samsung's paper details are not on the slide and not cited here |
| Monolithic CFET at imec's A7 node (projection) | imec, "Performance boosters to scale monolithic CFET across multiple logic technology nodes" |
| Monolithic against sequential integration; the temperature limit after layer transfer | imec, "Imec puts complementary FET (CFET) on the logic technology roadmap", https://www.imec-int.com/en/articles/imec-puts-complementary-fet-cfet-logic-technology-roadmap |
| A CFET patent (Fig. 17 shown) | IBM, US patent 11,869,812 B2, granted 9 January 2024 |
| The CFET model: 5 nm sheets, a 12 nm gap between the tiers, one common gate (one configuration; split-gate designs exist) | FET Lab's monolithic CFET (`cfet_mono`), after IBM US 11,869,812 B2; sequential: `cfet_seq`, after TSMC US 2024/0413156 A1 |
| Inverter cell heights 156, 136, 106 and 74 nm, rail to rail | FET Lab's schematic layout models (`show_fin`, `show_ns`, `show_fs`, `show_cfet`). Not foundry cells |
| R = ρL/(wt): 25 Ω per µm for a 20 × 40 nm rail; 3.1 Ω per µm at 4× the width and 2× the thickness | Model: `physics.wire_resistance_ohm`, illustrative dimensions, the same length and ρ = 2 × 10⁻⁸ Ω m. Real thin-wire resistivity, contacts and vias change the numbers |
| PowerVia: >30% less platform voltage droop, 6% frequency benefit (test chip); in production in 18A with nanosheets, without CFET | Intel, "PowerVia test shows industry-leading performance", June 2023, https://www.intel.com/content/www/us/en/newsroom/news/powervia-test-shows-industry-leading-performance.html ; Intel 18A process and Panther Lake announcements (2025) |
| ΔT = P R_th; up to twice the power per area if both tiers switch as much; with the heat sink below the wafer, the upper tier's path is longer | Qualitative, for the heat-sink arrangement drawn on the slide; the order changes with the sink's side. Background on 3D thermal issues: IEEE IRDS 2021, More Moore |
| 5 nm of silicon is about 37 atomic layers | Si (100) layer spacing a/4 = 0.136 nm |

## Live Lab 2 · Who controls the barrier?

| Claim | Source |
|---|---|
| The barrier, λ, barrier DIBL and swing it shows | Chapter 6's toy quasi-2D model, ported line for line to `labs/lab-physics.js`; `tests/test_physics.py` checks the port against `physics.py`. The couplings are evaluated at the V_DS chosen on the slider |
| Channel thickness per architecture (planar 15 nm effective depth, double gate 10, fin 6, sheets 5, 2D 0.65) | Illustrative values, as in chapter 6; every channel uses silicon's permittivity |

## Chapter 11 · Beyond silicon, beyond Boltzmann

| Claim | Source |
|---|---|
| One part of the mobility goes roughly as t⁶ in very thin silicon (5 → 3 nm: ×0.05) | Illustrative, one mechanism: `physics.roughness_mobility_ratio`; see Uchida et al. (chapter 7) for the measured, more complicated picture |
| A MoS₂ monolayer is about 0.65 nm thick; 2D surfaces have no dangling bonds | B. Radisavljevic et al., "Single-layer MoS₂ transistors", *Nature Nanotechnology* 6, 147 (2011) |
| With the same gates and oxide, λ ∝ √t makes λ about √(5/0.65) ≈ 2.8× shorter for a 0.65 nm layer than for a 5 nm silicon sheet | Toy model (`physics.natural_length_nm`), silicon's permittivity for both. No minimum gate length is claimed for real 2D devices |
| 2D channels on imec's roadmap after the CFET, around the A2 node, early 2040s (projection); research now | imec, "Introducing 2D-material based devices in the logic scaling roadmap", https://www.imec-int.com/en/articles/introducing-2d-material-based-devices-logic-scaling-roadmap ; for current research on 300 mm wafers: imec, ASML and TSMC press release (2026) |
| Fermi-level pinning at metal contacts to 2D semiconductors | Y. Liu et al., "Approaching the Schottky–Mott limit in van der Waals metal–semiconductor junctions", *Nature* 557, 696 (2018), and references there |
| Semimetal (bismuth) contacts on MoS₂ with contact resistance near the quantum limit, 2021 | P.-C. Shen et al., "Ultralow contact resistance between semimetal and monolayer semiconductors", *Nature* 593, 211 (2021). It doesn't settle contacts for manufacturing |
| Two examples of ways under 60 mV/dec (not the only ideas) | Ionescu and Riel (2011); Salahuddin and Datta (2008) |
| Tunnel FETs: band-to-band tunnelling cuts off the Boltzmann tail; swings below 60 mV/dec shown | A. M. Ionescu and H. Riel, "Tunnel field-effect transistors as energy-efficient electronic switches", *Nature* 479, 329 (2011) |
| 2024: vertical GaSb/InAs nanowire tunnel FETs with sub-60 mV/dec switching and about 300 µA/µm at 0.3 V, in the lab | Y. Shao et al. (MIT), *Nature Electronics* 8, 157–167 (2025; published online 4 November 2024), doi:10.1038/s41928-024-01279-w ; MIT News, "Nanoscale transistors could enable more efficient electronics", 4 November 2024. A lab result, not a product |
| Negative capacitance: m = 1 + C_s (1/C_ox + 1/C_FE) for a ferroelectric in series with the oxide; m < 1 needs \|C_FE\| < C_ox; stable (no hysteresis) only if 1/C_FE + 1/C_ox + 1/C_s > 0. Example: C_ox = 4 C_s, C_FE = −3 C_s gives m ≈ 0.92, SS ≈ 55 mV/dec | S. Salahuddin and S. Datta, "Use of negative capacitance to provide voltage amplification for low power nanoscale devices", *Nano Letters* 8, 405 (2008) (arXiv:0707.2073). Model: `physics.nc_body_factor`, `physics.nc_stable`; one illustrative bias point |
| Source-to-drain tunnelling factor equals the thermal factor at about 5.3 nm (rectangular 0.4 eV barrier, m* = 0.2 m₀) | Toy model: WKB in `physics.source_drain_tunnelling` and `physics.tunnelling_crossover_nm`. An illustrative crossover for these assumptions, not a universal limit on gate length |
| Landauer: erasing one bit (a logically irreversible step) releases at least k_BT ln 2 ≈ 2.9 zJ at 300 K | R. Landauer, "Irreversibility and heat generation in the computing process", *IBM J. Res. Dev.* 5, 183 (1961); measured: A. Bérut et al., *Nature* 483, 187 (2012). A bound on erasure, not on every transistor transition |
| Charging 0.1 fF to 0.7 V draws CV² ≈ 49 aJ from the supply (½CV² ≈ 24.5 aJ stored, the rest lost in charging; the stored half is lost on discharge), about 17,000 × k_BT ln 2 | Illustrative estimate: `physics.cycle_energy_J`, `physics.stored_energy_J`; MIT 6.012 lecture 15 for CMOS switching energy |
| Vertical-transport FET (VTFET), 2021 | IBM and Samsung, announced at IEDM, December 2021 |
| RV16X-NANO: a 16-bit RISC-V processor of more than 14,000 carbon-nanotube transistors | G. Hills et al., "Modern microprocessor built from complementary carbon nanotube transistors", *Nature* 572, 595 (2019) |
| A tunnel FET's source and drain are doped p⁺ and n⁺, so they can't be swapped (mirroring or rotating a device is still fine) | Ionescu and Riel (2011) |

## Chapter 12 · Outro

| Claim | Source |
|---|---|
| The table of eras | Chapters 1 to 11 of this lecture, and their sources above |
| Shortest gates ≈ 6λ: about 40 (planar), 15 (FinFET) and 12–16 nm (nanosheet) | Toy model: `physics.natural_length_nm`, 1 nm oxide (EOT) |
| Forksheets switch about like nanosheets | imec, 15 June 2021 (chapter 9) |
| (k_BT/q) ln 10 = 59.5 mV per decade at 300 K: the ideal thermal factor for a conventional transistor without internal gain; real devices are a little worse; a bipolar transistor's V_BE follows the same factor | `physics.subthreshold_swing`; Sze and Ng, ch. 5 and 6 |

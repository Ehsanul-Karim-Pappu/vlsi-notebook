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

## Chapter 5 · Boltzmann's tyranny

| Claim | Source |
|---|---|
| Boltzmann distribution; k_BT = 25.9 meV at 300 K | Any statistical-physics text; computed in `physics.thermal_voltage` |
| Subthreshold swing SS = m (k_BT/q) ln 10 ≥ 60 mV/decade; m = 1 + C_dep/C_ox | S. M. Sze and K. K. Ng, *Physics of Semiconductor Devices*, 3rd ed. (Wiley, 2007), ch. 6; Y. Taur and T. H. Ning, *Fundamentals of Modern VLSI Devices*, 2nd ed. (Cambridge, 2009), ch. 3 |
| 15 mV/decade at 77 K | The same formula at 77 K (`physics.subthreshold_swing`) |
| A bipolar transistor's collector current rises 10× per ~60 mV of V_BE | I_C = I_S exp(qV_BE/k_BT); Sze and Ng, ch. 5 |
| The I–V curve (V_T = 0.4 V, m = 1.2) | Model: EKV interpolation in `physics.drain_current` |
| Dennard scaling | R. H. Dennard et al., "Design of ion-implanted MOSFET's with very small physical dimensions", *IEEE J. Solid-State Circuits* SC-9(5), 256–268 (1974) |
| Clock speeds, 1971–2020 (approximate) | Intel product specifications for the 4004, 8086, 80286, 386, 486, Pentium, Pentium II, Pentium 4, Core 2 Extreme X6800, Core i7-2600K, Core i7-7700K and Core i9-10900K (base clocks) |
| Power density: nuclear reactor by 2005, rocket nozzle by 2010, Sun's surface by 2015 | P. P. Gelsinger, "Microprocessors for the new millennium: challenges, opportunities, and new frontiers", ISSCC 2001 keynote, *ISSCC Digest of Technical Papers*, 22–25 (2001) |
| A 1.2 nm gate oxide (about five atomic layers) | S. Thompson et al., "A 90 nm logic technology featuring 50 nm strained silicon channel transistors…", IEDM 2002 |
| Direct tunnelling ~10× per 0.2 nm; Φ_B ≈ 3.1 eV, m* ≈ 0.4 m₀ | Model: WKB in `physics.tunnel_transmission`, with textbook Si/SiO₂ values (Taur and Ning, ch. 2) |
| HfO₂ k ≈ 20; EOT = t (3.9/k) | G. D. Wilk, R. M. Wallace and J. M. Anthony, "High-κ gate dielectrics: current status and materials properties considerations", *J. Appl. Phys.* 89, 5243 (2001) |
| High-k + metal gate at Intel 45 nm, 2007 | K. Mistry et al., "A 45nm logic technology with high-k+metal gate transistors, strained silicon, 9 Cu interconnect layers…", IEDM 2007 |

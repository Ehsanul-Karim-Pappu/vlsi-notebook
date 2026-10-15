# Sources

The sources behind the lecture's rules and numbers. The slides show no equations; where a slide
gives a number, this page says where it comes from. Pictures of gradients, heat, stress and IR
drop are labelled "illustrative" on screen: they show the shape of an effect, not a measurement.
Rules that depend on the process (dummy counts, resistor orientation, spacing, how much a
resistor's value varies) are tagged "typical · check your PDK".

## The general references

| Topic | Source |
|---|---|
| Matching in layout: unit devices, interdigitation, common centroids, dummies, orientation, metal over matched devices, resistors and capacitors | A. Hastings, *The Art of Analog Layout*, 2nd ed. (Prentice Hall, 2006), the chapters on matching resistors, capacitors and MOS transistors |
| The four rules of a common centroid: coincidence, symmetry, dispersion, compactness (chapter 3's "coincident, symmetric, evenly spread, compact") | Hastings, as above |
| Random mismatch shrinks with area: the spread goes as one over the square root of the gate area, so four times the area halves it | M. J. M. Pelgrom, A. C. J. Duinmaijer, A. P. G. Welbers, "Matching properties of MOS transistors", *IEEE J. Solid-State Circuits* 24(5), 1433–1440 (1989) |
| Random and systematic mismatch, and why gradients and the neighbourhood need layout, not just area | P. G. Drennan, C. C. McAndrew, "Understanding MOSFET mismatch for analog design", *IEEE J. Solid-State Circuits* 38(3), 450–456 (2003) |
| The folded-cascode OTA, its common-mode feedback, and the bandgap reference | B. Razavi, *Design of Analog CMOS Integrated Circuits*, 2nd ed. (McGraw-Hill, 2017), the chapters on operational amplifiers, common-mode feedback and bandgap references; D. Johns, K. Martin, *Analog Integrated Circuit Design* (Wiley, 1997) |

## Chapter 1 · What makes twins differ

| Claim | Source |
|---|---|
| Random variation from dopant counts and edge roughness; only area reduces it | Pelgrom et al. (1989); Drennan and McAndrew (2003) |
| Smooth gradients across the die; a common centroid cancels the straight part | Hastings; the slide's gradient is illustrative |
| Package stress is strongest at the die's edges and corners, and changes carrier mobility, depending on direction (piezoresistance) | F. Fruett, G. C. M. Meijer, *The Piezojunction Effect in Silicon Integrated Circuits and Sensors* (Kluwer, 2002); Hastings |
| The neighbourhood: well edges (well proximity effect) and the active area's ends (stress from trench isolation) shift a transistor's threshold and current | T. B. Hook, J. Brown, P. Cottrell et al., "Lateral ion implant straggle and mask proximity effect", *IEEE Trans. Electron Devices* 50(9), 1946–1951 (2003); R. A. Bianchi, G. Bouche, O. Roux-dit-Buisson, "Accurate modeling of trench isolation induced mechanical stress effects on MOSFET electrical performance", IEDM 2002 |
| The matrix of technique against cause | A summary of Hastings' rules in this lecture's words; "½" marks a technique that cancels only part (the straight part of a gradient, or one direction) |

## Chapters 2 to 6 · The OTA

| Claim | Source |
|---|---|
| The input pair's mismatch is the input offset; the current sources' and sinks' mismatch reaches the input scaled down by their transconductance against the input pair's; the cascodes' barely matters | Razavi, the offset of a differential pair with a current-mirror or folded load. The bar lengths on the ranking slide are illustrative; only the order is claimed |
| Interdigitated (ABAB) leaves a quarter of a side-by-side pair's straight-gradient mismatch, for four units each | Arithmetic: the centroids are one unit apart instead of four. Computed by `common.placed` and the lab |
| A single mirrored row (ABBA ABBA) cancels a straight gradient in any direction; a long row is more exposed to curvature; the cross-quad folds it into two short rows | Hastings (compactness); the arithmetic is in `common.placed` and the lab, and checked in `tests/test_lecture.py` |
| Dummies give the end units the same neighbours; in FinFET processes they also keep fins and gates continuous | Hastings; foundry FinFET layout guidance (check your PDK for how many) |
| An end-fed rail's voltage sag curves and grows to the far end; fed from the middle, the worst sag is a quarter as large and symmetric | Model: a uniform current drawn along a resistive rail, sag(x) ∝ x − x²/2 from the feed; illustrative |
| Matched devices should carry current in the same direction (source/drain asymmetry from angled implants and stress) | Hastings |
| Ratios drawn as whole units, not one wider device (edge effects don't scale with width) | Hastings |
| Unequal CMFB resistors or capacitors let part of the differential signal into the common-mode loop | Razavi and Johns and Martin, common-mode feedback |
| Unit resistors: one width, one orientation, the same contact heads, interleaved, dummies at the ends; unit capacitors in a common centroid with a dummy ring | Hastings |
| Metal over a matched device can shift it (stress, and hydrogen reaching the gate oxide during processing) | Hastings |
| The extracted capacitances on the "Prove it" slide | Illustrative numbers, not from a real extraction |

## Chapter 7 · The bandgap

| Claim | Source |
|---|---|
| The amplifier's offset sits in series with ΔV_BE and is multiplied by R2/R1 on its way to V_REF | Razavi, bandgap references (the effect of op-amp offset) |
| R2/R1 of about ten, with Q2 eight times Q1 | Arithmetic: ΔV_BE = (kT/q)·ln 8 ≈ 54 mV at 300 K, and V_REF ≈ V_BE + (R2/R1)·ΔV_BE ≈ 1.2 V needs R2/R1 ≈ 10. Typical, not a design |
| V_BE falls by about 2 mV per °C | Razavi, bandgap references |
| A poly resistor's absolute value varies by about ±15–20 % between wafers, while the ratio of matched units holds to a fraction of a percent | Typical; Hastings. Check your PDK's corners and matching data |
| Q1 at the centre of a 3 × 3 array with Q2's eight around it, and a dummy ring | Hastings, matching bipolar transistors |
| Package stress shifts V_BE (the piezojunction effect); keep the bandgap away from the die's edges and corners | Fruett and Meijer (2002) |
| Chopping an amplifier to average out its offset | C. C. Enz, G. C. Temes, "Circuit techniques for reducing the effects of op-amp imperfections: autozeroing, correlated double sampling, and chopper stabilization", *Proc. IEEE* 84(11), 1584–1614 (1996) |
| A trim set at one temperature fixes the value there, not every drift | Razavi, bandgap references |

## Chapter 8 · The review

| Claim | Source |
|---|---|
| Simulate with the PDK's layout-dependent effects (well proximity, diffusion length) and run Monte Carlo mismatch on the extracted netlist | Drennan and McAndrew (2003); Hook et al. (2003); your PDK's documentation |

## The circuits

The three schematics are drawn with [cirfig_gen](https://github.com/KwantaeKim/cirfig_gen) by
Kwantae Kim (MIT licence; `schematics/LICENSE-cirfig_gen.txt`), from layouts written by
`schematics/build_layouts.py`. They are textbook topologies, not a particular product's design.

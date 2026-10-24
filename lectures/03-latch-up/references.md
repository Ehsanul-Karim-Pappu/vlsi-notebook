# Sources

The sources behind the lecture's physics and rules. The slides show pictures, not derivations;
where a slide gives a number, this page says where it comes from. Pictures of carriers, heat and
supplies are labelled "illustrative". Numbers from the lecture's own model (`physics.py`) are
labelled "toy model": they get the shapes right, not a process's values. Rule names and values
are generic and tagged "typical · check your PDK", because real foundry rule decks are
confidential and differ.

## The general references

| Topic | Source |
|---|---|
| Latch-up in CMOS: the parasitic thyristor, triggering, holding, and the layout cures | R. R. Troutman, *Latchup in CMOS Technology: The Problem and Its Cure* (Kluwer, 1986) |
| Latch-up across technologies, guard rings, injection, multiple supplies, test | S. H. Voldman, *Latchup* (Wiley, 2007) |
| Layout practice: taps, guard rings, wells, deep N-well | A. Hastings, *The Art of Analog Layout*, 2nd ed. (Prentice Hall, 2006) |
| The CMOS process and latch-up in a design text | N. H. E. Weste, D. M. Harris, *CMOS VLSI Design*, 4th ed. (Addison-Wesley, 2010), the chapter on robustness |
| The latch-up qualification test | JEDEC Standard JESD78, *IC Latch-Up Test* (check the current revision) |

## Chapter by chapter

| Claim | Source |
|---|---|
| The CMOS inverter holds a vertical PNP (P+ source, n-well, p-substrate) and a lateral NPN (N+ source, p-substrate, n-well) forming a P-N-P-N thyristor between VDD and VSS, with the well and substrate resistances across their bases | Troutman, ch. 1–2; Weste and Harris |
| Triggers: I/O overshoot and undershoot, supply transients, power-up order, forced current in test | Troutman; Voldman; JESD78 |
| A bipolar turns on at a base-emitter voltage of about 0.6–0.7 V; the lecture uses 0.65 V | Any device text (e.g. Sze and Ng) |
| β_npn·β_pnp > 1 as the regenerative condition (simplified: the shunt resistors raise the real threshold) | Troutman; Weste and Harris |
| The S-shaped I–V with trigger and holding points; a supply below the holding voltage cannot sustain latch-up | Troutman; Voldman. The curve on the slides is from the toy model |
| Low-voltage core supplies are less exposed than I/O supplies, because the supply may sit below the holding voltage | Voldman. Not a guarantee: holding voltages depend on the process and the structure |
| Taps close to devices lower R_sub and R_well; the tap-distance rule is a budget on the base voltage | Troutman; Hastings. The voltages on the "budget" slide are from the toy model |
| DRC tap checks size the taps and subtract them from the active | The usual construction in DRC rule decks (Calibre SVRF, IC Validator, Pegasus all provide SIZE and NOT); the slide's rule name and distance are generic |
| Well-tap cells in tapless standard-cell libraries, inserted at a fixed pitch | Standard practice in tapless libraries; the pitch is set by the library's tap rule |
| Majority-carrier rings (P+ in the substrate, N+ in the well) and minority-carrier collector rings (an N-well ring in the substrate, a P+ ring outside a well); the double guard ring at the I/O | Troutman; Voldman; Hastings |
| Minority carriers injected into the substrate can travel tens to hundreds of µm | Voldman; Troutman (diffusion lengths in lightly doped substrates). Order of magnitude only |
| Injectors found by connectivity from the pads and by marker layers; a distance band around them | The usual construction in foundry LUP decks; generic here |
| A well must be tied to the highest potential of the P+ inside it; floating wells; spacing between wells on different supplies | Voldman; Hastings |
| Deep N-well isolates an NMOS in a P-well and adds its own parasitic stack | Voldman; Hastings |
| JESD78: the I-test (current forced into and out of I/O pins, typically up to ±100 mA) and the V-test (supply overvoltage, typically 1.5 × the maximum), at room temperature (Class I) and at the maximum operating temperature (Class II); pass if the supply current returns to normal | JEDEC JESD78. Values and classes as the slides say "typically": check the current revision and the product's specification |

## The toy model

`physics.py` (and its port, `labs/lab-model.js`): R_sub = 50 Ω + 25 Ω/µm, R_well = 100 Ω + 40 Ω/µm
to the nearest tap; turn-on at 0.65 V; β_npn = 40·exp(−spacing / 4 µm), β_pnp = 15; holding
voltage 1.0 V + 0.08 V per µm of N+ to well spacing; 8 Ω once latched. These are chosen to show
the right behaviour (what grows, what shrinks, which supply holds), not to predict a process.

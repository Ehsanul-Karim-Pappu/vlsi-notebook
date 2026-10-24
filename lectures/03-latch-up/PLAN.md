# Lecture 3 · Latch-up, in Layout — plan

A technical, visual lecture for analog and mixed-signal layout engineers: where latch-up comes
from, how it fires, and why each latch-up (LUP) rule in a DRC deck exists. The goal is that every
LUP error marker a layout engineer meets reads as a picture of the silicon underneath, with an
obvious fix.

## 1. The promise

By the end, the audience can look at a LUP violation and say: which parasitic path it protects,
which knob it turns (substrate or well resistance, bipolar gain, carrier collection, distance from
an injector), what the right fix is, and what a "fix" that only silences the checker looks like.

Rule for every slide: the physics is shown as a picture on a cross-section or a top view, and
every rule is tied to the part of that picture it controls. Numbers come from a labelled toy model
or are tagged "typical · check your PDK". Real foundry rule decks are confidential, so the rule
names (LUP.TAP.1 and so on) and values are generic.

## 2. Length and structure

About 55 minutes: about 5,500 words of notes (English and Bangla), plus two live labs.

| # | Chapter | Min | What it gives |
|---|---|---|---|
| X0 | **The chip that shorts itself** | 3 | A bench story (supply current jumps, the part heats, only a power cycle recovers); the DRC report line every layout engineer has seen; the promise |
| X1 | **The thyristor in every inverter** | 6 | The CMOS cross-section built layer by layer; the vertical PNP and the lateral NPN; the well and substrate resistances; the equivalent circuit: an SCR from VDD to VSS |
| X2 | **How it fires, and why it stays on** | 6 | Triggers (I/O overshoot and undershoot, supply glitches, power-up order); the 0.6–0.7 V base threshold; the feedback loop animated; the S-shaped I–V with its trigger and holding points; VDD against the holding voltage |
| — | Live lab: **Fire the thyristor** | 5 | Tap distance, N+ to well spacing, an injection pulse and the supply: quiet, fires and lets go, or latched |
| X3 | **Four knobs, four rule families** | 4 | What layout controls: the resistances (taps), the bipolar gain (spacing), carrier collection (guard rings), distance (from injectors); the rule family each knob became |
| X4 | **Taps: the core rule** | 7 | The maximum distance from any diffusion to its tap, and why (a voltage budget); well-tap cells in standard-cell rows; tap rows in analog blocks; how the deck checks it (size the taps, subtract); traps: a tap in the wrong well, a tap on the wrong net, a floating tap, a butted tap that isn't |
| — | Live lab: **Tap the floor** | 5 | A top view with a tap rule: place taps, watch the coverage and the error markers |
| X5 | **Guard rings at the I/O** | 7 | Injectors and the minority carriers they spray into the substrate; majority-carrier rings (P+ in the substrate, N+ in the well) and minority-carrier collector rings (an N-well ring in the substrate); the double guard ring; the rules: width, continuity, contacts, strapping, the supply it ties to |
| X6 | **Keeping the core away from injectors** | 5 | What counts as an injector (diffusion connected to a pad); how the deck finds it (marker layers, connectivity); the distance band around the I/O; fixes that work and "fixes" that only silence the checker |
| X7 | **Many supplies, many wells** | 6 | Wells at different potentials and their spacing; a well tied to the highest potential of what's inside it; floating wells (ERC); deep N-well isolation and what it adds; power-up order and hot-plug |
| X8 | **The latch-up review** | 4 | The checklist; reading a LUP report; what the JEDEC JESD78 latch-up test does to a finished part; the question to ask of every rule |

## 3. Storyboard notes

- **X1** builds the cross-section from the inverter of lecture 1 (same colours: n⁺ cyan, p⁺
  magenta, n-well and p-substrate as in the layout views). The PNP and NPN symbols are drawn over
  the silicon they come from, then lifted out into the SCR circuit.
- **X2** animates the loop: injected current → drop across R_sub → the NPN wakes → its collector
  current pulls the well down through R_well → the PNP wakes → its collector current feeds R_sub.
  The S-curve shows the trigger point, the negative-resistance branch and the holding point; a
  horizontal VDD line shows why a supply below the holding voltage lets go.
- **X4**'s check is drawn as a DRC would do it: size every tap by the rule distance, subtract from
  the diffusion, flag what's left.
- **X5** shows electrons injected by an N+ diffusion pulled below ground, spreading through the
  substrate, collected by an N-well ring at VDD before they reach the core's wells.

## 4. The toy model

`physics.py` holds one small model, used by the slides, both labs and the tests, and labelled
"toy model" wherever a number from it is shown:

- the substrate and well resistance seen by a parasitic bipolar grows with the distance to its tap
  (illustrative Ω per µm);
- a bipolar turns on when the drop across its base resistance reaches about 0.65 V;
- the lateral NPN's gain falls as the N+ to N-well spacing (its base width) grows;
- the loop latches if both bipolars turn on and the loop gain β_n·β_p exceeds one, and it stays
  latched only while the supply is above the holding voltage and can source the holding current.

## 5. Accuracy rules

- Rule names and values are generic and tagged "typical · check your PDK".
- Physics pictures are labelled illustrative; numbers from the model are labelled toy model.
- The sources are in `references.md` (Troutman; Voldman; Hastings; Weste and Harris; JEDEC JESD78).

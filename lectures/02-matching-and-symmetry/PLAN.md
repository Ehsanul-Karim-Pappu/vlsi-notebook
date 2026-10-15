# Lecture 2 · Matching and Symmetry, in Layout — plan

A practical lecture for analog layout engineers: what each matching and symmetry technique
does on the layout, and what it cancels. No derivations. Every technique is shown on one of two
real circuits, never on a two-transistor example:

- a **fully differential folded-cascode OTA** with its common-mode feedback (CMFB), and
- a **bandgap reference** (a PMOS mirror, an amplifier, Q1 against an eight-unit Q2, R1 and R2).

## 1. The promise

By the end, the audience can take either circuit and say: which devices must match, how badly
each pair's mismatch hurts, which arrangement to use for each group, what it cancels and what it
leaves, how to route and feed the pairs, where to put the block on the die, and what to check
before tape-out.

Rule for every slide: a technique is always shown with **what it mitigates**. If a slide can't
say that, it goes.

## 2. Length and structure

About 45 minutes: about 4,600 words of notes (English and Bangla), plus one live lab.

| # | Chapter | Min | What it gives |
|---|---|---|---|
| M0 | **Identical on paper** | 3 | The two circuits; what a mismatch costs each one, said as an outcome (offset, a common-mode leak, a reference that's off and needs trimming) |
| M1 | **What makes twins differ** | 6 | The six causes, each as a picture on the die: random variation, process gradients, stress, temperature, the neighbourhood, the wiring. The matrix: technique against cause |
| M2 | **Reading the OTA for matching** | 6 | The matched groups, ranked by how directly their error reaches the input; the symmetry axis; the floorplan, block by block |
| M3 | **The input pair** | 7 | Units; side by side, interdigitated, mirrored, cross-quad, and what each cancels; dummies; the tail on the axis; the pair's drains and gates routed as mirror images |
| — | Live lab: **Place the units** | 5 | Arrange A and B units against a gradient of any angle and curvature; side by side, ABAB, ABBA, cross-quad, the bandgap's 1 : 8 |
| M4 | **The current sources and the cascodes** | 6 | Large current-source pairs as interdigitated arrays with dummies; the cascodes beside their devices; feeding the source rails from the axis (IR drop); the same current direction; the tail and the bias as unit ratios |
| M5 | **The CMFB's resistors and capacitors** | 5 | R1 and R2 from unit resistors, interleaved, same orientation, same heads, dummies; C1 and C2 from unit capacitors in a common-centroid array with a dummy ring; why: otherwise the CMFB sees part of the signal |
| M6 | **Routing as mirror images** | 5 | The same layers, lengths, vias and neighbours for each differential net; crossings done symmetrically; shields; metal over the devices; the extraction check |
| M7 | **The bandgap** | 8 | Q1 in the centre of a 3 × 3 array with Q2's eight around it and a dummy ring; R1 and R2 from one unit resistor; M1 to M3 as interleaved units; the amplifier's pair as a cross-quad; placing the block away from hot spots and the die's edges and corners; trimming as the last resort |
| M8 | **The matching review** | 4 | A checklist for both circuits, post-layout checks, and the matrix again |

## 3. Storyboard notes

- **M1's six causes**, each with its picture and what cancels it:
  random (size: more area, more units); gradients (common centroid, compact arrays);
  stress (orientation, die-centre placement, away from corners and pads); temperature
  (symmetric to the heat source, on an isotherm); neighbourhood (dummies, the same surroundings,
  distance from well edges); wiring (mirror-image routing, centre-fed rails, Kelvin sense where it
  matters).
- **The ranking in M2**: the input pair first (its error appears directly as input offset),
  then the current sources and sinks (their error arrives at the input divided by the input
  pair's gain), then the cascodes (their error barely reaches the output current), the tail
  last (it's common to both halves). Said in those words, no equations.
- **M3's arrangements**: a gradient across the row; A and B centroids drawn; side by side
  leaves the full gradient; ABAB leaves one unit's worth; ABBA cancels a straight gradient along
  the row; the cross-quad cancels it in any direction. What none of them cancel: random
  variation (only area does) and curvature (compact arrays help).
- **M7's array**: Q1 at the centre, Q2's eight around it; the centroid of both is the centre;
  a dummy ring around the nine. Resistors: R2 = k units, R1 = m units, all one width and
  orientation, interleaved.

## 4. The circuits

Drawn with [cirfig_gen](https://github.com/KwantaeKim/cirfig_gen) (Kwantae Kim, MIT licence),
from layouts written by `schematics/build_layouts.py`:

| File | Circuit |
|---|---|
| `ota.svg` | Fully differential folded-cascode OTA: M1/M2 input pair, M3/M4 PMOS current sources, M5/M6 PMOS cascodes, M7/M8 NMOS cascodes, M9/M10 NMOS sinks driven by the CMFB, M11 tail |
| `cmfb.svg` | The CMFB: R1/R2 sense the output common mode (C1/C2 across them), an amplifier compares it with V_CM and drives V_CMFB |
| `bandgap.svg` | The bandgap: M1–M3 PMOS mirror driven by an amplifier holding X = Y; Q1 against Q2 (eight units) through R1; M3, R2 and Q3 give V_REF |

## 5. Accuracy rules

- No equations on the slides. Effects are described by what they do to the layout and the
  circuit, and every picture of a gradient or an effect is labelled illustrative.
- Rules that depend on the process (resistor orientation, dummy counts, spacing) are marked
  "typical · check your PDK".
- The sources are in `references.md`.

# Lecture 1, layout edition · What You Draw, and Why It Changed — plan

The same story as lecture 1 (planar → FinFET → nanosheet → forksheet → CFET), told from the
layout side: what each transistor looks like in a layout tool, what you draw and size, and
what the neighbourhood does to it. Physics comes in one sentence at a time, as the intuition
behind a rule, never as a derivation.

The full lecture stays exactly as it is. This edition lives next to it and shares its data
(FET Lab's devices and layouts), its 3D models, its labs and the `kit/`.

## 1. Audience and promise

Analog layout engineers, junior and senior. By the end they can say, for each device:

- what the layers mean (where the transistor is, where current flows, which way it's cut);
- what they size (W and L, fingers, multipliers; then fins; then sheet width), and what's fixed;
- what changes around the device (grids, dummy gates, diffusion breaks, cell height, rails);
- which layout-dependent effects to watch, and the habits that tame them.

Rule for every slide: if it doesn't change what someone draws, checks or asks the PDK about, it
goes, or it becomes a one-line intuition.

## 2. Length and structure

About 45 to 50 minutes: about 4,800 words of notes (37 minutes at 130 words a minute, in English
and Bangla, as in the full lecture), plus three live labs and the animations.

| # | Chapter | Minutes | What it gives the audience |
|---|---|---|---|
| L0 | **The picture on your screen** | 3 | Poly over diffusion: the same picture since 1971, but what it means has changed. The map of the talk |
| L1 | **One rectangle over another**: the planar MOSFET | 8 | Schematic ↔ layout ↔ cross-section. W and L as drawn, fingers, multipliers, wells and taps, an inverter |
| L2 | **Why planar had to go** | 5 | Three intuitions: an off transistor still leaks; a short channel lets the drain act like a gate; for analog that costs output resistance, which is why mirrors use long L. The fix: grip the channel from more sides |
| — | Live lab 2: **Who controls the barrier?** | 3 | The drain acting as a second gate, and the fin taking control back |
| L3 | **Width comes in fins**: the FinFET | 13 | The fin in 3D and cut; the fin and gate grids, and why (lines, then cuts); width in whole fins; nfin × nf × m; long devices as series stacks; dummy gates and diffusion breaks; threshold flavours as layers; a 1 : 2 mirror from units; MD, gate contact and M0 |
| L4 | **Width is drawn again**: the nanosheet | 8 | Sheets in 3D; the sheet width is a mask dimension again, the sheet count is the process's; the inverter cell and its n-to-p space; backside power and what it frees on the front |
| L5 | **Squeezing n and p together**: forksheet and CFET | 6 | The wall; n on top of p; four cells at one scale (156 / 136 / 106 / 74 nm, model); roadmap, labelled as such |
| — | Live lab 4: **Build a cell**, live lab 5: **Hold it yourself** | 4 | The cell from above at any fin count or sheet width; the 3D models cut open |
| L6 | **Where you put it changes what it does** | 13 | Layout-dependent effects in plain words: well proximity, STI stress and diffusion length, neighbours and density; why a common centre cancels a gradient; the matching habits; orientation and tilted implants; substrate noise and guard rings; self-heating; contact parasitics; antennas; a checklist |
| L7 | **What changed in what you draw** | 2 | One table, planar to CFET, and the checklist |

## 3. Storyboard, slide by slide

### L0 · The picture on your screen (≈3 min)
1. Card: "What you draw, and why it changed".
2. The Intel 4004's layout drawing, 1971 (photo): every transistor is poly crossing diffusion.
3. Today, from above: FET Lab's FinFET inverter. Still lines crossing lines, but the diffusion
   became fins on a grid.
4. The map: five devices as top-view icons, each with the one thing you now draw (W·L, fins,
   sheet width, a wall, a stack), then "the neighbourhood".

### L1 · One rectangle over another (≈8 min)
1. A schematic NMOS (cirfig_gen), its layout (active, poly, contacts, metal 1) and the cut A–A'.
2. The cross-section along A–A': source, drain, the thin oxide, the gate, the channel that forms
   under it. One line: the gate's voltage pulls electrons up under the oxide and joins source to
   drain.
3. W and L as drawn. Current goes roughly as W / L: wider gives more, longer gives less but
   steadier (gain, matching).
4. Fingers: one wide device folded into four, sharing source and drain. Why: shorter gates (less
   gate resistance), less drain area (less capacitance), a squarer shape.
5. Multipliers: m copies in parallel; the unit device as the building block for matching.
6. Wells and taps: NMOS in p, PMOS in an n-well; body taps and guard rings keep the wells at
   their supplies (one line on latch-up).
7. An inverter: schematic beside its planar layout.
8. "Any W, any L, on a fine grid." Then the trouble started.

### L2 · Why planar had to go (≈5 min)
1. Off isn't off: below threshold the current falls about tenfold for every 60 to 100 mV of gate
   at room temperature, never to zero. A rule of thumb, shown on one log plot (illustrative).
2. A short channel lets the drain reach under the gate and pull the barrier down too: a second
   gate you don't control.
3. For analog: the drain voltage now moves the current, the output curves tilt, r_o and gain
   fall. That's why mirrors and amplifiers are drawn at several times minimum L.
4. The fix: a thinner channel, gripped from more sides. Planar → fin → sheets (the kit's
   cross-sections).

### Live lab 2 (≈3 min), after L2
Who controls the barrier? A short planar gate, the drain voltage raised, then the FinFET.

### L3 · Width comes in fins (≈13 min)
1. The FinFET in 3D, built layer by layer (FET Lab's model), then cut through the gate: three
   gated faces.
2. From above (FET Lab's FinFET inverter layout): fins on one fixed pitch, gates on another.
   You don't draw the active's width; you choose fins.
3. Why everything is on a grid: a uniform pattern of lines (self-aligned double or quadruple
   patterning), then a cut mask. One direction, one pitch, cut rules.
4. Width in whole fins: each fin is worth about two heights plus its width (96 nm in this
   model), so widths come in steps.
5. The knobs: planar (W, L, nf, m) against FinFET (nfin, nf, m, and L from a short list).
   Marked "typical · check your PDK".
6. A long device from short ones: gates in series on shared fins, tied together; close to, not
   identical to, one long gate.
7. Cuts and breaks: two devices on a row; dummy gates on the ends; the fins cut between them.
8. Threshold flavours are layers you draw: LVT, SVT, HVT regions and the rules at their
   boundaries.
9. A 1 : 2 mirror: the schematic (cirfig_gen); one unit device used twice and four times,
   placed B A B B A B with dummies.
10. Local interconnect: the contact bar across all fins (MD), the gate contact, metal 0; the
    contacted gate pitch.
11. Where the fin runs out: fixed height, hard to make thinner, width still in steps.

### L4 · Width is drawn again (≈8 min)
1. The nanosheet in 3D and cut: sheets stacked, gate all around.
2. From above: the active is a rectangle again. The sheet width is set by the mask; the number
   of sheets by the process. W_eff ≈ sheets × 2 × (width + thickness).
3. What you size: the sheet width, within the range and steps the PDK allows; nf and m as before.
4. The cell (FET Lab's nanosheet inverter): tracks, the n-to-p space, 136 nm rail to rail (model).
5. Backside power: the rails go under the wafer. Intel ships it in 18A (PowerVia); TSMC
   announced it for A16. On the front: more room for signals, less IR drop; power reaches the
   devices from below.

### L5 · Squeezing n and p together (≈6 min)
1. The forksheet: a thin wall between the n and p sheets, so they sit closer (FET Lab's layout).
   On imec's roadmap; the inner and outer wall variants.
2. The CFET: n stacked on p. From above it's one device; between the tiers, vertical contacts.
   imec's roadmap puts it in the early 2030s.
3. Four inverter cells at one scale: 156, 136, 106, 74 nm rail to rail (schematic models).
4. Then the labs: Build a cell; Hold it yourself.

### L6 · Where you put it changes what it does (≈13 min)
1. Same schematic, same size, different place: different current. Layout-dependent effects.
2. Well proximity: in the well implant, ions scatter off the resist edge into the silicon near
   it, so transistors near a well edge get a higher threshold. Keep matched devices the same
   distance from the edge, and not close to it. (Hook et al., IEEE TED 2003; Drennan et al.,
   CICC 2006.)
3. Stress from the isolation: the trench oxide squeezes the active, and the current depends on
   the distance from the gate to the active's edge (SA, SB in the models). nMOS and pMOS react
   differently. Give matched devices the same SA and SB; add dummy fingers. In FinFET and
   nanosheet processes the same idea shows up as the distance to the nearest diffusion break
   and its type. (Bianchi et al., IEDM 2002; BSIM4.)
4. Neighbours and density: nearby poly and active, and the density rules that bring dummy fill.
   Put dummies on purpose, the same around every matched device.
5. Why a common centre works: A A B B against A B B A on a linear gradient.
6. Matching habits that still work (the five-transistor OTA, cirfig_gen): unit devices, common
   centroid, interdigitation, one orientation, dummies, the same metal over every device.
   Mismatch falls with area: four times the gate area halves it (Pelgrom et al., JSSC 1989).
7. Orientation: a tilted implant shadows one side of the gate; matched devices the same way
   round.
8. The substrate: digital noise through the silicon; guard rings, distance, deep n-well.
9. Self-heating: a fin or sheet sits in oxide and gets hot when it carries current. It changes
   the current and ages the device and its wires. Spread high-current devices, mind the
   electromigration width rules. Qualitative.
10. Parasitics in the contacts: contact and via resistance, the gate-to-contact capacitance.
    For analog: extra C_gd and series R. Redundant vias, short connections, check post-layout.
11. Antennas: charge from plasma etching, through the gate oxide; jump up near the gate, or a
    diode.
12. The checklist, on one slide.

### L7 · What changed in what you draw (≈2 min)
One table: device → what you size → what's fixed → what's new around it. Then thanks.

## 4. Schematics

Drawn with [cirfig_gen](https://github.com/KwantaeKim/cirfig_gen) (Kwantae Kim, MIT licence):
one SVG per circuit, from its symbol palette, checked against its drawing rules. They're black
on white, so the slides show them on a light card. The JSON layouts are in
`layout/schematics/`, so a figure can be changed and drawn again.

| File | Circuit | Used in |
|---|---|---|
| `nmos.svg` | One NMOS with gate, drain, source | L1 |
| `inverter.svg` | CMOS inverter | L1 |
| `mirror.svg` | NMOS current mirror with a reference current | L3, L6 |
| `diffpair.svg` | Differential pair with a tail current source | L6 |

## 5. Accuracy rules for this edition

- PDK-dependent statements ("L from a short list", "diffusion break types", "allowed sheet
  widths") are said as typical and marked "check your PDK" on screen.
- Numbers from FET Lab's schematic models are labelled "model", as in the full lecture.
- Roadmap devices (forksheet, CFET) are labelled as roadmap.
- Layout-dependent effects are described qualitatively; any curve is labelled illustrative.

## 6. Build

`python build.py --edition layout` renders these chapters (`layout/l*.py`) and builds
`build/deck-layout/index.html`, with the labs. The full lecture's `python build.py` is unchanged.

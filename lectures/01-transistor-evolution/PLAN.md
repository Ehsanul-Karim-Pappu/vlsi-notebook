# Lecture 1 · The Switch That Wouldn't Turn Off — production plan

An animated, presenter-paced slide deck about the transistor's evolution, from Lilienfeld's
1925 field-effect patent to the bipolar transistor, the MOSFET, the FinFET, the nanosheet, the
forksheet, the CFET and beyond. It's built with **Manim** and **manim-slides**, styled after
Veritasium, and heavy on theory: each architecture shows up as the answer to a physics problem
that we state with its equations.

Status: **built**: the style kit, all thirteen chapters (0 to 12) and Live Labs 1 to 5, with
English slides, speaker notes in English and Bangla, a speaker view that shows each animation's
progress, a 25-minute core path (`core.py`, `build/deck/core.html`), a PowerPoint export with the
labs as screenshots, and a tool that cuts a continuous movie to your recorded narration. See
`README.md` to build and present it. What's left is yours: rehearse the core with a clock,
check the PowerPoint on the presenting machine, and record the narration for the movie.

The device data in `data/` and the 3D models in `models/` are copied from
[FET Lab](https://github.com/Ehsanul-Karim-Pappu/fet-lab), so the deck's devices match that
app. See `data/README.md`.

---

## 1. The big idea (the throughline)

Veritasium videos hang on one question that sounds simple and turns out to be deep. Ours:

> **"Every smaller transistor had to keep its off state under control, while still giving
> enough current and fitting into a cell that can be built. The off state is the thread that
> keeps coming back."**

The off state is the organising thread, not a claim that it explains every invention. The gate
tries to keep **control** of a potential barrier, and physics (surface states, Boltzmann
statistics, tunnelling, the drain's electric field) keeps taking that control away. Other
problems sit alongside it: making a usable amplifier at all, drive current, and packing n and p
into the cell.

| Era | The problem | What answered it | The gate's grip |
|---|---|---|---|
| 1925–47 | Surface states block the field; no usable field-effect switch | (not yet) | 0 |
| 1947–59 | A working solid-state amplifier | Point contact, BJT | n/a |
| 1959–2003 | Surface states again | Thermal SiO₂ → MOSFET, CMOS | 1 face |
| 2003–07 | Tunnelling through 5-atom oxide | Strain, high-κ/metal gate | 1 face |
| 2005– | Power, and 60 mV/decade at 300 K | (no fix: V_DD stops scaling) | 1 face |
| 2011 | The drain reaches the barrier | FinFET | 3 faces |
| 2022 | Fins come in whole numbers and can't get much thinner | Nanosheet (GAA) | 4 faces |
| ~2030 (projected) | n-to-p spacing eats the cell | Forksheet | 3 faces + wall (packing, not grip) |
| ~2033 (projected) | Out of floor space | CFET (stack n on p) | as the nanosheet, 2 storeys |
| research now; roadmap 2040s | Silicon very hard to thin further | 2D channels; steep-slope switches | thinner channel (toy model) |

The recurring visual **motifs** carry this table:

- **The hill and the marbles.** Electrons are marbles jiggling in a valley (the source). The
  gate sets the height of a hill (the barrier). Current is marbles that hop over. This one
  picture explains the Boltzmann limit, DIBL, short-channel effects and tunnelling.
- **The grip.** A hand squeezing a hose: one finger (planar), three fingers (FinFET), a fist
  (GAA), two fists stacked (CFET).
- **The control meter.** A heads-up gauge that shows the natural length λ and the swing SS for
  the current architecture. It improves with each chapter.
- **The timeline ribbon.** A thin 1925 → 2045 ribbon along the bottom, with a marker that
  slides forward from chapter to chapter.

## 2. How we'll borrow from Veritasium

1. **Cold open before the title**: a counterintuitive claim, never a title card first.
2. **One question drives everything** (above). Every chapter ends on a cliffhanger, the next
   problem, so the deck pulls forward.
3. **People and stakes**: Lilienfeld, ignored; Shockley's failed FET and his rivalry with
   Bardeen and Brattain; Atalla and Kahng's MOSFET, shelved by Bell Labs; Dennard; Chenming
   Hu's DARPA-funded FinFET; imec's roadmap bets.
4. **Misconception beats**: "Moore's law is a law of physics" (no, it's an economic
   observation); "a 3 nm chip has 3 nm features" (no feature measures 3 nm); "more gates is
   always better" (the forksheet gives a face up on purpose).
5. **The picture first, then the equation, term by term.** Each symbol appears attached to
   the object it describes, in that object's colour (C_ox in the oxide colour, kT in the
   thermal-jiggle colour, and so on). No equation shows up without a picture.
6. **Plant and payoff.** The number **60 mV per decade** first appears with no explanation in
   the bipolar transistor (ch. 2), is explained in ch. 5, and is attacked in ch. 11.
7. **Scales that land.** A 1.2 nm gate oxide is 5 atoms thick. 13 sextillion transistors had
   been made by 2018. A modern gate pitch is a few hundred silicon atoms.
8. **One idea per slide, almost no text on screen.** The narration lives in the **speaker
   notes** as a written script, so the presenter can read it or riff on it.

## 3. Format and interactivity (decisions made)

**Engine: Manim Community + manim-slides.** Each chapter is one `Slide` (or `ThreeDSlide`)
class. `self.next_slide()` marks a pause, so the presenter advances with → or a clicker.

The deck is interactive in three layers:

| Layer | What it does | How |
|---|---|---|
| **1. Presenter-paced animation** | Animations stop at every beat. Idle states loop (marbles keep jiggling while you talk). ← plays a slide backwards. | `next_slide()`, `next_slide(loop=True)`, reversed playback |
| **2. Deep-dive detours** | The main story runs horizontally. Press **↓** on a theory slide to drop into the full derivation, then ↑ to return. One deck serves a 25-minute talk and a 60-minute lecture. | manim-slides `direction="vertical"` (reveal.js vertical slides) |
| **3. Live labs** | Five browser simulations sit between the Manim slides. The audience can watch sliders change the physics in real time. | Custom reveal.js template (`--use-template`); plain HTML/JS/SVG with no framework, matching the repo's no-build style |
| **3b. Real 3D** | Spin and zoom FET Lab's own FinFET, nanosheet, forksheet and CFET models on the slide. | `<model-viewer>` loading FET Lab's `models/*.glb` (copied into this repo) |

**Outputs**

1. **HTML deck** (main): a folder you open in any browser. **S** opens the speaker view with
   notes and a timer; **F** goes full screen.
2. **PPTX** fallback (`manim-slides convert --to pptx`): videos embedded, without the live labs.
3. **Documentary cut**: each chapter rendered as one continuous MP4 and joined into a single
   video in the YouTube format.

**Specs**: 16:9, 1920×1080. 30 fps for the deck to keep files small; 60 fps or 1440p for the
documentary cut. Draft renders use `-ql` (480p15).

**Defaults I picked** (change any of them):

- **Audience** (confirmed): junior and senior engineers in an analog layout department.
  Equations are derived, not just quoted, and each chapter ties its physics to something they
  draw, in an "In your layout" note: W and L, common-centroid pairs, threshold flavours, taps
  and guard rings, λ and DRC rules, weak-inversion biasing.
- **Languages** (confirmed): one deck, with the slides in English and the speaker notes in
  English and Bangla. The Bangla is spoken office Bangla in Bangla script, with technical
  terms, names, units and numbers left in English. Slides flow into each other: objects carry
  over between slides and the notes bridge each change of scene.
- **Length**: about 45 minutes in full, with a marked **25-minute core path** that skips the
  ↓ detours and the optional chapters.
- **Delivery**: presented live from the speaker notes, on a laptop. There's no recorded
  voice-over. The speaker view (S) has an animation bar so the presenter knows when a slide's
  animation has finished.

## 4. Chapter storyboard

Each chapter follows the same pattern: **story → problem → equation → fix → new problem**.
The ↓ marks the deep-dive derivations.

### Ch 0 · Cold open: "The most-made thing in history" (≈2 min)

- **Visual**: a dark screen. A counter races to **1.3 × 10²²**, the CHM/Jim Handy estimate of
  transistors made by 2018. Then a zoom from a phone, to the die, to a standard cell, to a
  single nanosheet stack (3D, from `geometry.json`).
- **Hook**: "Every one of these switches has one job. And the hard part was never turning it
  on."
- **Beat**: a flash-forward of the five shapes (planar, fin, sheet, fork, CFET) morphing into
  one another, then a hard cut to 1925.

### Ch 1 · Before the switch: tubes, and an idea 20 years too early (1904–1947, ≈3.5 min)

- **Story**: the vacuum-tube triode; ENIAC's 17,468 tubes and ~150 kW. Lilienfeld's patents
  (Canada 1925; US 1,745,175, filed 1926, granted 1930) describe a field-effect device.
  Shockley's 1945 FET experiment finds almost no effect.
- **Problem**: why didn't the field effect work?
- **Equations**:
  - Thermionic emission, the tube's heat problem: $J = A_G T^2 e^{-W/k_BT}$
  - The field effect, how it was supposed to work: $Q_{ind} = C_{ox}V_G$, so
    $n_s = \varepsilon_{ox}V_G/(q\,t_{ox})$
  - Bardeen's surface states (1947): the induced charge is shared between interface traps and
    the channel, $\Delta Q_{ch}/\Delta Q_G \approx C_{dep}/(C_{dep}+C_{it})$ with
    $C_{it}=q^2D_{it}$. With $D_{it}\sim10^{13}$ cm⁻²eV⁻¹, almost nothing reaches the channel.
    The Fermi level is **pinned**.
- **Animation**: field lines from the gate plate land on trap states (little sinks) at the
  surface before they reach the electrons, like a "bucket brigade" of charge that leaks away.
- **↓ Detour**: the surface-state band diagram and Fermi-level pinning.
- **Cliffhanger**: "So Bardeen and Brattain stopped trying to beat the surface, and started
  poking it."
- **Layout tie-in**: Lilienfeld's drawing already has the source, drain and gate-on-insulator
  you draw today.

### Ch 2 · The accidental transistor (1947–1951, ≈3 min)

- **Story**: Bell Labs, 16 December 1947, the point-contact transistor (gold foil, a plastic
  wedge, a paper clip); shown to management 23 December. Shockley, left out, conceives the
  junction transistor in January 1948.
- **Equations**:
  - The BJT, an exponential switch: $I_C = I_S\,e^{qV_{BE}/k_BT}$, $\beta = I_C/I_B$
  - **Plant**: "Raise V_BE by **60 mV** and the current goes up **10×**." We leave it
    unexplained on purpose.
- **Animation**: carriers diffusing across a thin base, with an exponential plot that grows a
  decade for every 60 mV.
- **Problem**: the BJT works, but it always draws base current (static power), and the
  surface still ruins everything that touches it.
- **Cliffhanger**: "The solution would come from rust. Well, glass."
- **Layout tie-in** (built): the bipolar transistor is still on their chips: a 1 : 8 vertical
  PNP array in common centroid for a bandgap, with $\Delta V_{BE} = (k_BT/q)\ln 8 = 53.8$ mV.

### Ch 3 · The glass that saved electronics: oxide, planar, MOSFET, CMOS (1955–1963, ≈4.5 min)

- **Story**: Frosch and Derick's accidental SiO₂ masking (1955–57); Atalla's thermal-oxide
  passivation (1957–59) tames the surface states; Hoerni's planar process; the Kilby and Noyce
  ICs. Atalla and Kahng's MOSFET (1959–60), which Bell Labs shelved. Wanlass and Sah's CMOS
  (ISSCC 1963).
- **Equations**:
  - MOS capacitor band bending (animated: accumulation → depletion → inversion)
  - Threshold voltage: $V_T = V_{FB} + 2\phi_F + \dfrac{\sqrt{2q\varepsilon_{Si}N_A(2\phi_F)}}{C_{ox}}$, with $\phi_F=\frac{k_BT}{q}\ln\frac{N_A}{n_i}$
  - Square law: $I_D = \tfrac12\mu_n C_{ox}\tfrac{W}{L}(V_{GS}-V_T)^2$, built term by term on
    the device
  - CMOS: static current ≈ 0; dynamic power $P = \alpha C V_{DD}^2 f$
- **Animation**: the inversion layer "condenses" under the gate as V_G rises. Then a CMOS
  inverter in which only one transistor conducts at a time, and its transfer curve drawn live.
- **↓ Detour**: deriving the square law from the gradual channel approximation.
- **Cliffhanger**: "Now we had a switch that sips power. What happens if you shrink it?"
- **Layout tie-ins** (built): every drawn layer is a mask like Frosch and Derick's oxide
  window; LVT/SVT/HVT are the V_T equation's terms; W and L on the top view set the current;
  latch-up as a p-n-p-n with β_npn·β_pnp > 1, and the taps and guard rings that stop it.

### Ch 4 · The free lunch: Moore and Dennard (1965–2003, ≈3.5 min)

- **Story**: Moore's 1965 *Electronics* article (doubling every year, revised to every two
  years in 1975). Dennard *et al.* 1974: the recipe for shrinking. The Intel 4004 (2,300
  transistors, 10 µm) to today's 10¹¹-transistor chips.
- **Misconception beat**: Moore's law is economics, not physics.
- **Equations**: the Dennard scaling table, animated row by row with the scale factor κ.
  Dimensions, $V$ ÷ κ and $N_A$ × κ lead to delay ÷ κ, power per circuit ÷ κ², density × κ²,
  **power density × 1**.
- **Animation**: a die tile splits into 4, then 16, then 64 transistors while a power-density
  thermometer stays flat. A log-scale transistor-count plot sweeps from 1971 to today.
- **Cliffhanger**: "There was one line in Dennard's table that couldn't keep shrinking forever:
  the voltage."
- **Layout tie-in** (built): Mead and Conway's λ rules shrank with Dennard; when scaling stopped
  being uniform, the rules stopped being multiples of λ and grew into today's DRC decks.

### Ch 5 · Boltzmann's tyranny and the power wall (2003–2007, ≈5 min) — *the theory heart*

- **Payoff**: the 60 mV/decade from ch. 2, explained.
- **Equations**:
  - Electrons over a barrier: $n(E)\propto e^{-E/k_BT}$, the Maxwell-Boltzmann tail
  - Subthreshold current: $I_D = I_0\,e^{q(V_{GS}-V_T)/mk_BT}$, $m = 1+C_{dep}/C_{ox}$
  - **The limit**: $SS = m\,\frac{k_BT}{q}\ln 10 \ \geq\ 60\ \text{mV/dec}$ at 300 K
  - Why V_T can't shrink: $I_{off} \approx I_{D}(V_T)\cdot10^{-V_T/SS}$, so every 60 mV of
    V_T you give up costs **10×** more leakage. V_DD stalls near 1 V and power density takes
    off.
  - Gate oxide tunnelling (WKB): $J_G\propto e^{-2t_{ox}\sqrt{2m^*\Phi_B}/\hbar}$. That's about
    **10× more leakage for every 0.2 nm** thinner. A 1.2 nm oxide is ~5 atoms.
  - The high-κ fix: $\text{EOT} = t_{hk}\,\varepsilon_{SiO_2}/\varepsilon_{hk}$ (HfO₂,
    κ≈20–25). Intel 45 nm, 2007. Also strained Si (90 nm, 2003).
- **Animation**: marbles with a Boltzmann energy spread. Lower the hill 60 mV and ten times as
  many hop over. Then the clock-frequency plateau (~2005) and Gelsinger's 2001 ISSCC "hot
  plate → nuclear reactor → rocket nozzle → Sun's surface" power-density chart.
- **Live Lab 1** follows this chapter.
- **Analog tie-in** (built): the straight line below V_T is weak inversion, where analog
  designers bias for the most g_m per unit current.
- **↓ Detour**: deriving SS from the capacitor divider ($C_{ox}$ in series with $C_{dep}$).
- **Cliffhanger**: "We'd hit the thermodynamic floor. Then the transistor got short enough
  that the drain started to fight the gate."

### Ch 6 · Losing grip: short-channel effects and the natural length (≈4.5 min) — *theory spine for every later architecture*

- **Problem**: in a short channel, the drain's field reaches the barrier. The drain lowers the
  hill, not the gate (DIBL); V_T rolls off; SS degrades.
- **Equations** (a quasi-2D Poisson model in the Young / Yan–Ourmazd–Lee form):
  - $\dfrac{d^2\phi}{dx^2} - \dfrac{\phi-\phi_{gs}}{\lambda^2} = 0$, so
    $\phi(x)=\phi_{gs}+(V_{bi}-\phi_{gs})\dfrac{\sinh\frac{L-x}{\lambda}}{\sinh\frac{L}{\lambda}}+(V_{bi}+V_{DS}-\phi_{gs})\dfrac{\sinh\frac{x}{\lambda}}{\sinh\frac{L}{\lambda}}$
  - Barrier lowering: $\Delta\phi_{min}\approx 2\sqrt{ab}\;e^{-L/2\lambda}$ (with $a, b$ the
    source and drain barrier heights), and
    $SS \approx \dfrac{60\ \text{mV/dec}}{1-2e^{-L/2\lambda}}$
  - **The unifying formula**: $\lambda_N \approx \sqrt{\dfrac{\varepsilon_{Si}}{N\,\varepsilon_{ox}}\,t_{Si}\,t_{ox}}$,
    where **N is the number of gates touching the channel**. Rule of thumb: $L_g \gtrsim 6\lambda$
    (sources quote 5–10).
- **The insight** (the "aha"): you don't win back control by pushing the gate harder. You
  shrink λ, by making the channel thin and wrapping more gate around it. **Everything after
  2011 is this equation.**
- **Animation**: a 3D potential surface φ(x, y) under the channel. Shorten L and watch the
  drain side pull the saddle down. Then the λ formula with N stepping 1 → 2 → 3 → 4 as the
  gate wraps around.
- **↓ Detour**: the derivation of λ (Gauss's law on a channel slice) and the cylindrical-GAA
  form.

### Ch 7 · FinFET: stand the channel up (1989–2011, ≈3.5 min)

- **Story**: Hitachi's DELTA (Hisamoto, IEDM 1989). DARPA's 25 nm challenge and the Berkeley
  FinFET (Hu, Bokor, King; IEDM 1998/99). Intel's 22 nm Tri-Gate (announced 2011).
- **Equations**: $W_{eff} = N_{fin}(2H_{fin}+W_{fin})$, so width comes **in whole fins only**.
  λ with N≈3.
- **Misconception beat**: "What does '3 nm' measure?" Nothing. We show the real contacted gate
  pitch and metal pitch, to scale.
- **3D**: FET Lab's FinFET model (`show_fin.glb`) builds up layer by layer, then the gate peels
  back to show the tri-gate wrap.
- **Problem**: fins can't get thinner (surface-roughness mobility goes as $\mu\propto t^6$ below
  ~5 nm), taller fins are hard to etch and add capacitance, and width is quantized.
- **Cliffhanger**: "So turn the fin on its side, and slice it."

### Ch 8 · Nanosheets: the gate wraps all the way around (2017–2025, ≈4 min)

- **Story**: IBM/GF/Samsung's stacked nanosheet (VLSI 2017). Samsung 3 nm GAA (June 2022).
  TSMC N2 and Intel 18A RibbonFET + PowerVia (2025).
- **Equations**: $W_{eff} = N_{sh}\cdot2(W_{sh}+T_{sh})$, with **continuous** width; λ with N=4;
  the cylindrical limit.
- **Process animation**: driven by FET Lab's `data/process.json`. Si/SiGe superlattice → fin →
  dummy gate → S/D recess → SiGe indent → **inner spacers** → epi → **channel release**
  (selective SiGe etch, the "magic trick") → high-κ/metal gate fill.
- **Problem**: the n-to-p spacing (gate-metal patterning, work-function boundaries) and the
  cell height (tracks × metal pitch) stop shrinking.

### Ch 9 · Forksheet: a wall to squeeze n and p together (2017–, ≈2 min, *optional on the core path*)

- **Story**: imec's forksheet (IEDM 2017; 17 nm n-to-p space shown in 2021). The outer-wall
  forksheet is aimed at A10.
- **Trade-off**: one face goes to the wall, so N≈3 again. Area goes down, grip goes down a
  little. The control meter dips for the first time, on purpose.
- **3D**: FET Lab's forksheet "fork" view.

### Ch 10 · CFET: build upward (2018–~2033, ≈4 min)

- **Story**: imec's CFET proposal (VLSI 2018). Intel, TSMC and Samsung stacked-CFET demos at
  IEDM 2023 (TSMC at 48 nm gate pitch; Intel an inverter at 60 nm gate pitch). imec's roadmap
  puts monolithic CFET at the A7 node.
- **Equations**:
  - Cell area: height = tracks × M2 pitch; going from 5T to ~4T
  - Heat: $\Delta T = P\,R_{th}$; the upper tier is farther from the heat sink
  - Backside power: $\Delta V_{IR} = I\,R$, so moving power to thick backside rails cuts
    droop. PowerVia reports 5–10% better cell utilization.
- **3D**: monolithic vs sequential CFET (`cfet_mono.glb`, `cfet_seq.glb`). The pFET tier
  slides under the nFET tier; the wafer flips to show backside contacts.
- **Problem**: silicon itself is the next limit. Below ~3 nm thick, its mobility collapses.

### Ch 11 · Beyond silicon, beyond Boltzmann (research now; roadmap 2040s, ≈4 min)

- **2D channels** (MoS₂, a 0.65 nm monolayer): in the toy model λ ∝ √t, so with the same gates
  and oxide λ is about √(5/0.65) ≈ 2.8× shorter than for a 5 nm silicon sheet. No minimum gate
  length is claimed. imec's roadmap places 2D FETs around A2, in the early 2040s (projection).
  **Callback**: the open problem is the contacts, where Fermi-level pinning (Bardeen's 1947
  surface states) is back.
- **Two examples of beating 60 mV/dec** (not the only ideas), with the ch. 5 payoff challenged:
  - Tunnel FET: band-to-band tunnelling cuts off the Boltzmann tail, so SS < 60. Current was
    the problem; MIT's 2024 GaSb/InAs vertical nanowire TFETs reached sub-60 mV/dec with about
    300 µA/µm at 0.3 V, in the lab.
  - Negative capacitance: a ferroelectric in series with the oxide gives
    $m = 1 + C_s(1/C_{ox} + 1/C_{FE})$; m < 1 needs |C_FE| < C_ox, and stability needs
    $1/C_{FE} + 1/C_{ox} + 1/C_s > 0$. Example: m ≈ 0.92, SS ≈ 55 mV/dec at one bias point.
- **Two scales, not floors**:
  - Source-to-drain tunnelling: for a rectangular 0.4 eV barrier and m* = 0.2 m₀ the WKB factor
    meets the thermal factor at about 5.3 nm. Illustrative for those assumptions only.
  - Landauer: erasing a bit costs at least $k_BT\ln2\approx 2.9\times10^{-21}$ J. Charging
    0.1 fF to 0.7 V draws CV² ≈ 49 aJ from the supply (½CV² stored), about 17,000 times that.
- Also briefly: VTFET, carbon nanotubes (the RV16X-NANO, 2019), monolithic 3D; a tunnel FET's
  source and drain can't be swapped.

### Ch 12 · Outro (≈1.5 min)

- The table of eras; the grip in the toy model (planar, FinFET, nanosheet), with the forksheet
  and the CFET shown as packing rather than grip.
- **Closing thought**: every smaller transistor had to turn off, still turn on, and fit in a
  buildable cell. For a conventional room-temperature MOSFET without internal gain,
  $\frac{k_BT}{q}\ln10$ is still the best possible swing; lab devices have crossed it, and
  making them useful and reliable by the billion is the next chapter.

## 5. The live labs (HTML/JS, inside the deck)

| # | Lab | Controls | What the audience sees |
|---|---|---|---|
| 1 | **Boltzmann's fence** | V_G, temperature (77 / 300 / 400 K), body factor m | Particle marbles over the hill; a live log(I_D)–V_G plot that draws 60 mV/dec at 300 K and gets steeper when cold |
| 2 | **Who controls the barrier?** | L_g, t_ox, t_ch, V_DS, gate count N (planar / fin / GAA / forksheet / 2D) | The φ(x) barrier from the ch. 6 model; readouts of λ, DIBL and SS; a warning when L_g < 6λ |
| 3 | **Dennard's dial** | κ; how far the voltage follows (V ∝ 1/κ^a); hold the clock | A patch of chip with its transistors and its heat; every quantity relative to before the shrink, against Dennard's constant field (ideal long-channel scaling, after Baccarani, Wordeman and Dennard, 1984) |
| 4 | **Build a cell** | FinFET / nanosheet / forksheet / CFET; fins or sheet width; tracks | The inverter cell from above and one transistor across its channel, to scale; whether it fits, and the fewest tracks (schematic model with FET Lab's spacings) |
| 5 | **Hold it yourself** | Rotate, zoom, cut through the gate or along the channel, switch layers off | FET Lab's 3D models (`models/*.glb`) in a small offline WebGL viewer, cut faces capped, each part named on hover |

The same equations live in one Python module (`physics.py`, unit-tested). Manim plots use
it, and the labs port it to JS. A small test checks that both give the same numbers, so what
the slides show matches what the labs compute.

## 6. Visual language

- **Background**: deep ink (#0E1116); text off-white.
- **Material colours** are FET Lab's own (`data/geometry.json`), so the 3D devices match the
  app: silicon #F2C2CF, SiO₂ #8C1C13, HfO₂ #BE8250, SiN #E4AE1B, and so on.
- **Physics colours**, fixed for the whole deck: electrons cyan (#4FC7D8), holes magenta, gate
  and field gold, drain influence red, thermal energy (kT) orange, barrier amber.
- **Equation terms** are coloured like the object they describe.
- **Type**: a clean sans for titles; LaTeX Latin Modern for math.
- **Chapter cards**: a giant year plus a one-line hook. The timeline marker slides.
- **No bullet-point slides.** Any text on screen is a label or a single sentence.
- **The real thing first.** Where the story reaches a real device or document, show it (a photo
  or the patent drawing, credited on the slide and in `images/CREDITS.md`), then animate it.

## 7. Repository layout

This lecture is the first in the `vlsi-notebook` repository. Code that later lectures will
reuse goes in the shared `kit/`; everything specific to this lecture stays in its folder.

```
vlsi-notebook/
  requirements.txt        manim, manim-slides (pinned), shared by every lecture
  kit/                    shared by every lecture
    style.py              palette, fonts, title cards, timeline ribbon, control meter
    fonts/                Inter (slides) and Noto Sans Bengali (Bangla notes), SIL OFL
    motifs.py             band diagrams, field lines, the hill and marbles, the grip
    devices3d.py          devices from a lecture's geometry data: 3D, cut open, and from above
  lectures/01-transistor-evolution/
    PLAN.md               this file
    README.md             build and present instructions
    physics.py            every equation in this lecture, as functions (unit-tested)
    devicedata.py         loads FET Lab's device models from data/
    data/                 device geometry, process steps and references, from FET Lab
    models/               FET Lab's 3D models (.glb) for the 3D slides and Lab 5
    chapters/             ch00_cold_open.py … ch12_outro.py, one Slide class per chapter
    labs/                 lab1_boltzmann.html … lab5_models.html (+ shared lab.css, lab.js, lab-physics.js)
    template/deck.html    reveal.js template that adds the labs and the 3D viewer
    template/speaker.html the speaker view: notes, timer, and each animation's progress
    references.md         the sources for the slides' dates and numbers, with any gaps marked
    build.py              render (draft/final) → manim-slides convert → html/pptx/mp4
    tests/test_physics.py
```

Renders (`media/`, `slides/`, `build/`) are git-ignored. Videos aren't committed; the HTML
deck is a build output.

**Setup**: see the repository's top-level `README.md`.

## 8. Build phases (each ends with something you can click through)

1. ✅ **Vertical slice**: the style kit + **Ch 0** (cold open) + **Ch 5** (Boltzmann) + **Lab 1**,
   exported as an HTML deck. This is the checkpoint: you judge the look, the tone and the
   depth of the theory before I scale it up.
2. ✅ **The history arc**: Ch 1–4, with notes in both languages and the speaker view.
3. ✅ **The architecture arc**: Ch 6–10, with the 3D devices, the layouts from above and the
   nanosheet process animation.
4. ✅ **The frontier**: Ch 11–12 and Labs 2 to 5.
5. ✅ **Polish**: the outside audit and its fixes, the 25-minute core path, final 1080p renders,
   HTML + PPTX, the movie-cutting tool, and the README. Still yours: a timed rehearsal, and the
   narration recordings for the movie.

## 9. Accuracy policy (same standard as FET Lab)

- Dates, names and numbers get sources in `references.md`. Where a source supports less than
  the slide says, the slide is reworded or the gap is marked there.
- Results from simplified models (quasi-2D λ, the SS formula, Landauer comparisons) are
  labelled **"model" / "illustrative"** on screen.
- Roadmap claims (A10, A7, A2 timing) are presented as imec's projections, not facts, and
  re-checked at final build.

## 10. Risks and how I'll handle them

| Risk | Mitigation |
|---|---|
| 3D scenes render slowly with Cairo | Low polygon counts; drafts at 480p; chapters render in parallel (4 cores); switch to the OpenGL renderer if needed |
| The HTML deck gets large (1080p video) | 30 fps, tuned CRF; renders aren't committed |
| Arrow keys clash with lab sliders | The template captures keys only while a lab has focus |
| Simplified physics reads as exact | "model" labels; limits stated in the ↓ detours |
| 2025–26 industry claims go stale | Re-checked against sources at the final build |

## 11. Decisions

1. **Live talk**: a live, clicker-paced deck presented from a laptop, with a script in the
   speaker notes. The documentary cut comes as a by-product.
2. **Length**: about an hour in full (about 11,000 words of notes), with a 25-minute core path
   (`core.py`).
3. **Audience**: analog layout engineers, junior and senior (confirmed).
4. **Languages**: English slides; speaker notes in English and Bangla (confirmed).
5. **Hosting**: a local HTML folder per language, plus PPTX.

## 12. The October 2026 audit (of commit c3cb12c)

An outside audit listed 22 findings (F01–F22). Each was checked against its sources and the
code before changing anything; all were accepted. What changed:

| # | Finding | What we did |
|---|---|---|
| F01 | Opening chip didn't match the transistor shown | Ch 0 now opens on the A20 Pro (TSMC N2, nanosheets), and the 3D model is labelled illustrative, not measured N2 geometry |
| F02 | "Reaches the channel" share was mislabelled; q²D_it units | `share_in_semiconductor`, C_it = q·D_it; Ch 1, Ch 3 and the references reworded |
| F03 | Lilienfeld drawing wasn't his patent's geometry | Labelled a modern analogy; the patent figure shown beside it |
| F04 | CMOS "current only while switching" | Short-circuit current and leakage added: P = αCV²f + P_sc + V_DD I_leak |
| F05 | Lab 1's fixed I_spec | I_spec ∝ m U_T² (`specific_current`), in Python and JS |
| F06 | Boltzmann factor called the whole distribution | Reworded as the Boltzmann factor; labels say illustrative |
| F07 | Face-counting λ treated as universal | Labelled a toy model everywhere; Frank, Taur and Wong cited; electrostatic λ ≠ layout λ |
| F08 | SS formula used past its range | Exact toy-model closed form, 60/(1 − sech(L/2λ)) at V_DS = 0 |
| F09 | Barrier DIBL used as threshold DIBL for gain | Gain = α_g/α_d; "barrier DIBL" labels |
| F10 | t⁶ roughness as a hard cutoff | One mechanism, illustrative; Uchida's competing effects noted |
| F11 | Nanosheet cartoon contradicted its isolation claim | Bottom dielectric isolation drawn; one nFET route; omitted steps stated; `process.json` not claimed as used |
| F12 | Patent captions | FinFET patent: double gate with hard mask; TSMC forksheet: a stage with sacrificial gate 142 |
| F13 | Inner- and outer-wall forksheets mixed up | Separate icons and words; motif and Lab 2 icon fixed; no λ penalty; imec's measured 66–68 mV/dec |
| F14 | Layout labels | SCMOS widths, current direction along the fin, 54 nm convention, 136 nm rail span vs 144/120 nm track examples, model cells |
| F15 | Steep-slope chapter too categorical; NC needed the full stack | "Two examples"; MIT 2024 TFET; NC with C_s, C_ox, C_FE and the stability condition |
| F16 | ~5 nm called a universal floor | An illustrative crossover for stated assumptions; floor removed from Ch 11 and Ch 12 |
| F17 | ½CV² called supply energy | CV² = 49 aJ drawn from the supply, ½CV² stored; Landauer's erasure scope; ≈17,000× |
| F18 | Backside power and heat stated universally | PowerVia in 18A without CFET; "mostly signal"; 8× illustrative; heat-sink path drawn; "up to" 2× |
| F19 | The thesis overstated the off-state story | Off state as a thread, alongside current and buildable cells; new closing |
| F20 | Date labels | CHM 2 April 2018; deliberate amplification research; 2011/2012; 2022 production; node names; research now vs roadmap |
| F21 | Numbers needing a definition | B200 two dies; our extrapolation; ≈10×/≈1000×; interfacial layer in EOT; base vs turbo clocks |
| F22 | Gelsinger chart years unsourced | Years removed; attributed to his keynote talk, with the gap noted |

The audit's remaining-work list is done too: Labs 3–5, the core path, the PowerPoint export (now
with lab screenshot slides) and a movie-cutting tool. Two of its acceptance checks can only be done by
you: a rehearsal of the core with a clock, and PowerPoint playback on the presenting machine.

### The 25-minute core path, beat by beat

The budget the core script was written to (about 2,800 words; the labs are timed for working them):

| Beat | Slides kept | Budget |
|---|---|---:|
| Opening: the A20 Pro and the question | Ch 0: 5 | 1:30 |
| Tubes, Lilienfeld, the surface | Ch 1: 6 | 1:30 |
| The bipolar transistor | Ch 2: 4 | 1:00 |
| Oxide, MOSFET, CMOS | Ch 3: 8 | 2:30 |
| Moore and Dennard, then Lab 3 | Ch 4: 6 | 1:45 + 0:30 |
| The thermal swing and high-k, then Lab 1 | Ch 5: 9 | 2:30 + 0:45 |
| Short channels, then Lab 2 | Ch 6: 7 | 2:00 + 0:45 |
| The fin and its width | Ch 7: 6 | 1:30 |
| The nanosheet and how it's made | Ch 8: 6 | 2:00 |
| The forksheet, as a bridge | Ch 9: 1 | 0:45 |
| The CFET, backside power, heat, then Labs 4 and 5 | Ch 10: 5 | 1:30 + 1:00 |
| Beyond silicon, a teaser | Ch 11: 3 | 0:45 |
| The ending | Ch 12: 3 | 0:45 |
| Transitions and slack | | 2:00 |
| **Total** | **69 + 5 labs** | **25:00** |


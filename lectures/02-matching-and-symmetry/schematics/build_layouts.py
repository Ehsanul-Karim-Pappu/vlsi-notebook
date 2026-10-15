#!/usr/bin/env python3
"""Write this lecture's cirfig_gen layouts (the JSON beside this file) from pin positions.

    python schematics/build_layouts.py         then: python schematics/draw.py <cirfig_gen clone>

Every symbol is placed by where its pins must land, so every wire ends exactly on a pin. Pins
are cirfig_gen's (its AGENTS.md lists them; the resistor, capacitor, amplifier and PNP ones are
worked out from their SVGs the same way).
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
W = 4.053          # a terminal's wire ends this far from the node's centre
R = 5.551 + 3      # node ring edge + gap, for signal labels
SIZE = {"NMOS": (39.40, 56.60), "PMOS": (39.38, 56.56), "PNP": (42.01, 53.36), "Amp": (72.52, 57.65)}


class Fig:
    def __init__(self, name):
        self.d = {"name": name, "symbols": [], "wires": [], "dots": [], "labels": []}

    def sym(self, sid, kind, left, top, flip=False):
        self.d["symbols"].append({"id": sid, "type": kind, "left": round(left, 4), "top": round(top, 4), "flip": flip})

    def wire(self, x1, y1, x2, y2):
        self.d["wires"].append([round(x1, 4), round(y1, 4), round(x2, 4), round(y2, 4)])

    def dot(self, x, y):
        self.d["dots"].append([round(x, 4), round(y, 4)])

    def label(self, runs, x, y, align):
        self.d["labels"].append({"runs": runs, "x": round(x, 4), "y": round(y, 4), "align": align})

    # --- devices, placed by their drain/source (or emitter) lead's x and the top of the symbol --
    def mos(self, sid, kind, lead_x, top, gate_right=False):
        """A MOSFET whose drain/source lead runs at LEAD_X. Returns its pins."""
        w, _ = SIZE[kind]
        lead = 37.130 if kind == "PMOS" else 37.149
        gate = 2.250 if kind == "PMOS" else 2.251
        left = lead_x - (w - lead) if gate_right else lead_x - lead
        self.sym(sid, kind, left, top, flip=gate_right)
        gx = left + (w - gate) if gate_right else left + gate
        if kind == "PMOS":
            return {"g": (gx, top + 28.209), "s": (lead_x, top + 2.250), "d": (lead_x, top + 54.310)}
        return {"g": (gx, top + 28.296), "d": (lead_x, top + 2.252), "s": (lead_x, top + 54.348)}

    def pnp(self, sid, emitter_x, top):
        left = emitter_x - 38.01
        self.sym(sid, "PNP", left, top)
        return {"b": (left + 4.0, top + 26.68), "e": (emitter_x, top + 4.0), "c": (emitter_x, top + 49.36)}

    def resistor(self, sid, left_pin_x, y):
        """A resistor lying down, its left pin at (LEFT_PIN_X, Y). Its right pin sits 0.067 lower."""
        left, top = left_pin_x - 2.252, y - 8.233
        self.sym(sid, "Resistor", left, top)
        return {"l": (left_pin_x, y), "r": (left + 32.648, top + 8.300)}

    def capacitor(self, sid, left_pin_x, y):
        left, top = left_pin_x - 2.251, y - 10.250
        self.sym(sid, "Capacitor", left, top)
        return {"l": (left_pin_x, y), "r": (left + 34.149, y)}

    def amp(self, sid, left, top, flip=False):
        self.sym(sid, "Amp", left, top, flip=flip)
        ix, ox = (left + 72.52 - 2.25, left + 72.52 - 70.275) if flip else (left + 2.25, left + 70.275)
        return {"+": (ix, top + 14.2125), "-": (ix, top + 43.1175), "o": (ox, top + 28.8225)}

    # --- supplies and terminals ----------------------------------------------------------------
    def vdd(self, sid, pin):
        self.sym(sid, "VDD", pin[0] - 11.447, pin[1] - 14.905)

    def gnd(self, sid, pin):
        """GND on a 13.5 pt wire below PIN."""
        self.wire(pin[0], pin[1], pin[0], pin[1] + 13.5)
        self.sym(sid, "GND", pin[0] - 7.4, pin[1] + 13.5 - 1.799)

    def terminal(self, sid, pin, length, side, runs):
        """A wire from PIN out to a terminal on SIDE ("left", "right", "up", "down"), labelled."""
        x, y = pin
        if side == "left":
            ex, ey, cx, cy = x - length, y, x - length - W, y
            self.label(runs, cx - R, cy, "right")
        elif side == "right":
            ex, ey, cx, cy = x + length, y, x + length + W, y
            self.label(runs, cx + R, cy, "left")
        elif side == "up":
            ex, ey, cx, cy = x, y - length, x, y - length - W
            self.label(runs, cx + R, cy, "left")
        else:
            ex, ey, cx, cy = x, y + length, x, y + length + W
            self.label(runs, cx + R, cy, "left")
        self.wire(x, y, ex, ey)
        self.sym(sid, "Voltage Node", cx - 6.3, cy - 6.3)

    def save(self, name):
        (HERE / f"{name}.json").write_text(json.dumps(self.d, indent=1) + "\n")


def V(sub):
    return [["V", "main"], [sub, "sub"]]


def M(n):
    return [["M", "main"], [str(n), "sub"]]


def ota():
    """A fully differential folded-cascode OTA: NMOS input pair, PMOS current sources and
    cascodes, NMOS cascodes and the current sinks the CMFB drives, the tail."""
    f = Fig("Fully differential folded-cascode OTA")
    xL, x1, xc = 130.0, 290.0, 350.0
    x2, xR = 2 * xc - x1, 2 * xc - xL
    gap = 24.0
    tA = 30.0
    # Row A: PMOS current sources; row B: PMOS cascodes; row C: NMOS cascodes; row D: NMOS sinks.
    a = [f.mos("M3", "PMOS", xL, tA), f.mos("M4", "PMOS", xR, tA, gate_right=True)]
    yF = a[0]["d"][1] + gap
    tB = yF + gap - 2.250
    b = [f.mos("M5", "PMOS", xL, tB), f.mos("M6", "PMOS", xR, tB, gate_right=True)]
    yO = b[0]["d"][1] + gap
    tC = yO + gap - 2.252
    c = [f.mos("M7", "NMOS", xL, tC), f.mos("M8", "NMOS", xR, tC, gate_right=True)]
    tD = c[0]["s"][1] + gap - 2.252
    d = [f.mos("M9", "NMOS", xL, tD), f.mos("M10", "NMOS", xR, tD, gate_right=True)]
    # The input pair, its drains folding into the branches at yF; the tail below it.
    t1 = yF + gap - 2.252
    p = [f.mos("M1", "NMOS", x1, t1), f.mos("M2", "NMOS", x2, t1, gate_right=True)]
    ytail = p[0]["s"][1]
    t0 = ytail + gap - 2.252
    m0 = f.mos("M11", "NMOS", xc, t0)
    for side, (pa, pb, pc, pd, pp, xb) in enumerate(((a[0], b[0], c[0], d[0], p[0], xL), (a[1], b[1], c[1], d[1], p[1], xR))):
        f.vdd(f"VDD{side}", pa["s"])
        f.wire(*pa["d"], *pb["s"])                       # current source to cascode, through the fold node
        f.wire(*pb["d"], *pc["d"])                       # PMOS cascode to NMOS cascode, through the output
        f.wire(*pc["s"], *pd["d"])
        f.gnd(f"GND{side}", pd["s"])
        f.wire(pp["d"][0], pp["d"][1], pp["d"][0], yF)   # the input device's drain up to the fold
        f.wire(pp["d"][0], yF, xb, yF)
        f.dot(xb, yF)
        f.dot(xb, yO)
        out = "left" if side == 0 else "right"
        f.terminal(f"VOUT{side}", (xb, yO), 52, out, V("OUT−" if side == 0 else "OUT+"))
        for dev, net in ((pa, "BP1"), (pb, "BP2"), (pc, "BN2"), (pd, "CMFB")):
            f.terminal(f"{net}{side}", dev["g"], 18, out, V(net))
        f.terminal(f"IN{side}", pp["g"], 16, out, V("IN+" if side == 0 else "IN−"))
    f.wire(p[0]["s"][0], ytail, p[1]["s"][0], ytail)     # the tail: one wire on both sources
    f.wire(xc, ytail, *m0["d"])
    f.dot(xc, ytail)
    f.gnd("GND2", m0["s"])
    f.terminal("BN1", m0["g"], 16, "left", V("BN1"))
    for n, dev, side in ((3, a[0], 0), (4, a[1], 1), (5, b[0], 0), (6, b[1], 1), (7, c[0], 0), (8, c[1], 1),
                         (9, d[0], 0), (10, d[1], 1), (1, p[0], 0), (2, p[1], 1)):
        x = dev["d"][0] + 4.5 if side == 0 else dev["d"][0] - 4.5
        f.label(M(n), x, dev["g"][1], "left" if side == 0 else "right")
    f.label(M(11), xc + 4.5, m0["g"][1], "left")
    f.save("ota")


def cmfb():
    """The CMFB: a matched resistor pair (with matched capacitors across them) senses the output
    common mode, and an amplifier compares it with V_CM and drives the sinks' gates."""
    f = Fig("Common-mode feedback")
    yC = 12.0
    r1 = f.resistor("R1", 40.0, 40.0)
    s = 110.0
    r2 = f.resistor("R2", 2 * s - r1["r"][0], r1["r"][1])
    c1 = f.capacitor("C1", 30.0, yC)
    c2 = f.capacitor("C2", 2 * s - c1["r"][0], yC)
    f.terminal("VOP", r1["l"], 20.95, "left", V("OUT+"))
    f.wire(*r1["r"], s, r1["r"][1])
    f.wire(s, r1["r"][1], *r2["l"])
    f.terminal("VON", r2["r"], 20.95, "right", V("OUT−"))
    # The capacitors across the resistors.
    f.wire(c1["l"][0], yC, c1["l"][0], r1["l"][1])
    f.dot(c1["l"][0], r1["l"][1])
    f.wire(*c1["r"], 85.0, yC)
    f.wire(85.0, yC, 85.0, r1["r"][1])
    f.dot(85.0, r1["r"][1])
    f.wire(*c2["l"], 2 * s - 85.0, yC)
    f.wire(2 * s - 85.0, yC, 2 * s - 85.0, r2["l"][1])
    f.dot(2 * s - 85.0, r2["l"][1])
    f.wire(c2["r"][0], yC, c2["r"][0], r2["r"][1])
    f.dot(c2["r"][0], r2["r"][1])
    # The sensed common mode into the amplifier, against V_CM; out to the sinks' gates.
    amp = f.amp("A1", 0, 0)
    ax = 125.0 - 2.25
    f.d["symbols"].pop()
    amp = f.amp("A1", ax, 95.0 - 14.2125)
    f.wire(s, r1["r"][1], s, amp["+"][1])
    f.wire(s, amp["+"][1], *amp["+"])
    f.dot(s, r1["r"][1])
    f.terminal("VCM", amp["-"], 16, "left", V("CM"))
    f.terminal("VCMFB", amp["o"], 20, "right", V("CMFB"))
    f.label([["R", "main"], ["1", "sub"]], 46.0, 58.0, "left")
    f.label([["R", "main"], ["2", "sub"]], 2 * s - 46.0, 58.0, "right")
    f.label([["C", "main"], ["1", "sub"]], 40.0, -8.0, "left")
    f.label([["C", "main"], ["2", "sub"]], 2 * s - 40.0, -8.0, "right")
    f.save("cmfb")


def bandgap():
    """A bandgap reference: a PMOS mirror (M1, M2, M3) driven by an amplifier that holds X and Y
    equal; Q1 against eight-times-larger Q2 through R1 makes a current proportional to absolute
    temperature, and R2 with Q3 turns it into V_REF."""
    f = Fig("Bandgap reference")
    top = 40.0
    xX = 60.0                                 # M1's lead: node X
    m1 = f.mos("M1", "PMOS", xX, top, gate_right=True)
    m2_left_gate = m1["g"][0] + 95.0          # room for the amplifier between the gates
    m2_lead = m2_left_gate - 2.250 + 37.130
    m2 = f.mos("M2", "PMOS", m2_lead, top)
    xY = m2["d"][0]
    x3 = xY + 120.0
    m3 = f.mos("M3", "PMOS", x3, top, gate_right=True)
    for i, m in enumerate((m1, m2, m3)):
        f.vdd(f"VDD{i}", m["s"])
    yg = m1["g"][1]
    f.wire(*m1["g"], *m2["g"])                # the M1–M2 gate tie
    # M3's gate over the top, back down into the M1–M2 gap.
    xg = m1["g"][0] + 22.0
    ybus = top - 30.0
    f.wire(*m3["g"], m3["g"][0] + 14.0, yg)
    f.wire(m3["g"][0] + 14.0, yg, m3["g"][0] + 14.0, ybus)
    f.wire(m3["g"][0] + 14.0, ybus, xg, ybus)
    f.wire(xg, ybus, xg, yg)
    f.dot(xg, yg)
    # The amplifier below the tie, its output up into the tie.
    amp = f.amp("A1", xX + 24.0, yg + 40.0)
    xo = amp["o"][0] + 8.0
    f.wire(*amp["o"], xo, amp["o"][1])
    f.wire(xo, amp["o"][1], xo, yg)
    f.dot(xo, yg)
    # X: M1's drain down to Q1, tapped into the + input.
    q_top = amp["-"][1] + 70.0
    q1 = f.pnp("Q1", xX, q_top)
    f.wire(*m1["d"], *q1["e"])
    f.wire(xX, amp["+"][1], *amp["+"])
    f.dot(xX, amp["+"][1])
    # Y: M2's drain down to R1 and Q2; wrapped under the amplifier into the − input.
    yw = amp["-"][1] + 22.0
    xw = amp["-"][0] - 9.0
    f.wire(*m2["d"], xY, yw)
    f.wire(xY, yw, xw, yw)
    f.wire(xw, yw, xw, amp["-"][1])
    f.wire(xw, amp["-"][1], *amp["-"])
    yr = yw + 24.0
    f.wire(xY, yw, xY, yr)
    f.dot(xY, yw)
    r1 = f.resistor("R1", xY + 14.0, yr)
    f.wire(xY, yr, *r1["l"])
    xq2 = r1["r"][0] + 18.0
    q2 = f.pnp("Q2", xq2, q_top)
    f.wire(*r1["r"], xq2, r1["r"][1])
    f.wire(xq2, r1["r"][1], *q2["e"])
    # M3: V_REF, then R2 and Q3.
    yref = m3["d"][1] + 20.0
    f.wire(*m3["d"], x3, yref)
    f.dot(x3, yref)
    f.terminal("VREF", (x3, yref), 40.0, "right", V("REF"))
    r2 = f.resistor("R2", x3 + 14.0, yref + 46.0)
    f.wire(x3, yref, x3, r2["l"][1])
    f.wire(x3, r2["l"][1], *r2["l"])
    xq3 = r2["r"][0] + 18.0
    q3 = f.pnp("Q3", xq3, q_top)
    f.wire(*r2["r"], xq3, r2["r"][1])
    f.wire(xq3, r2["r"][1], *q3["e"])
    # Each PNP diode-connected: base and collector to ground.
    for i, q in enumerate((q1, q2, q3)):
        f.gnd(f"GC{i}", q["c"])
        bx = q["b"][0] - 10.0
        f.wire(*q["b"], bx, q["b"][1])
        f.gnd(f"GB{i}", (bx, q["b"][1]))
    for n, m, side in ((1, m1, 0), (2, m2, 1), (3, m3, 0)):
        x = m["d"][0] - 4.5 if side == 0 else m["d"][0] + 4.5
        f.label(M(n), x, m["g"][1], "right" if side == 0 else "left")
    for n, q, extra in ((1, q1, ""), (2, q2, " (8)"), (3, q3, "")):
        f.label([["Q", "main"], [str(n) + extra, "sub"]], q["e"][0] + 4.5, q["b"][1], "left")
    f.label([["R", "main"], ["1", "sub"]], r1["l"][0] + 4.0, yr + 18.0, "left")
    f.label([["R", "main"], ["2", "sub"]], r2["l"][0] + 4.0, r2["l"][1] + 18.0, "left")
    f.label([["X", "main"]], xX - 6.0, amp["+"][1] - 12.0, "right")
    f.label([["Y", "main"]], xY + 6.0, yw - 12.0, "left")
    f.save("bandgap")


if __name__ == "__main__":
    ota()
    cmfb()
    bandgap()

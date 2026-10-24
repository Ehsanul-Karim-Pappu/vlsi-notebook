// The lecture's toy model of latch-up: a port of physics.py, so the labs show the same numbers
// as the slides. tests/test_lecture.py checks the two agree. Units: µm, mA, V, Ω.
(function () {
  const V_ON = 0.65;
  const R_SUB0 = 50.0, K_SUB = 25.0;
  const R_WELL0 = 100.0, K_WELL = 40.0;
  const BETA_NPN0 = 40.0, BASE_SCALE = 4.0;
  const BETA_PNP = 15.0;
  const V_HOLD0 = 1.0, K_HOLD = 0.08;

  const rSub = (d) => R_SUB0 + K_SUB * d;
  const rWell = (d) => R_WELL0 + K_WELL * d;
  const betaNpn = (s) => BETA_NPN0 * Math.exp(-s / BASE_SCALE);
  const loopGain = (s) => betaNpn(s) * BETA_PNP;
  const baseDrop = (iInj, d) => iInj * 1e-3 * rSub(d);
  const triggerCurrent = (d) => (V_ON / rSub(d)) * 1e3;
  const holdingCurrent = (dSub, dWell) => (V_ON / rSub(dSub) + V_ON / rWell(dWell)) * 1e3;
  const holdingVoltage = (s) => V_HOLD0 + K_HOLD * s;

  function state(iInj, dSub, dWell, s, vdd) {
    const fires = baseDrop(iInj, dSub) >= V_ON && loopGain(s) > 1.0;
    if (!fires) return "quiet";
    return vdd > holdingVoltage(s) ? "latched" : "lets go";
  }

  function sCurve(dSub, dWell, s, vTrig = 6.0, rOn = 8.0, iMax = null, n = 200) {
    const iT = triggerCurrent(dSub) * 0.05;
    const iH = holdingCurrent(dSub, dWell);
    const vH = holdingVoltage(s);
    iMax = iMax || Math.max(3 * iH, 100.0);
    const third = Math.floor(n / 3);
    const pts = [];
    for (let k = 0; k < third; k++) {
      const v = (vTrig * k) / third;
      pts.push([v, iT * Math.pow(v / vTrig, 4)]);
    }
    for (let k = 0; k < third; k++) {
      const t = k / third;
      pts.push([vTrig + (vH - vTrig) * t, iT + (iH - iT) * t]);
    }
    const rest = n - 2 * third;
    for (let k = 0; k < rest; k++) {
      const i = iH + ((iMax - iH) * k) / (rest - 1);
      pts.push([vH + (i - iH) * 1e-3 * rOn, i]);
    }
    return pts;
  }

  const covered = (cell, taps, reach) =>
    taps.some(([tx, ty]) => Math.abs(cell[0] - tx) <= reach && Math.abs(cell[1] - ty) <= reach);
  const violations = (cells, taps, reach) => cells.filter((c) => !covered(c, taps, reach));

  window.LUP = {
    V_ON, BETA_PNP, rSub, rWell, betaNpn, loopGain, baseDrop, triggerCurrent, holdingCurrent, holdingVoltage,
    state, sCurve, covered, violations,
  };
})();

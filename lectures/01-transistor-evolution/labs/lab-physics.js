// The lecture's equations for the labs: a line-for-line port of ../physics.py.
// tests/test_physics.py runs both and checks that they agree.
(function (root) {
  const K_B = 1.380649e-23;
  const Q = 1.602176634e-19;
  const LN10 = Math.log(10);

  function thermalVoltage(T = 300) {
    return (K_B * T) / Q;
  }

  function subthresholdSwing(T = 300, m = 1) {
    return m * thermalVoltage(T) * LN10;
  }

  function fractionOverBarrier(barrierEV, T = 300) {
    return Math.exp(-barrierEV / thermalVoltage(T));
  }

  function drainCurrent(vgs, vt, T = 300, m = 1.2, iSpec = 1e-6) {
    const ut = thermalVoltage(T);
    const x = (vgs - vt) / (2 * m * ut);
    const soft = x > 30 ? x + Math.log1p(Math.exp(-x)) : Math.log1p(Math.exp(x));
    return iSpec * soft * soft;
  }

  function offCurrentRatio(deltaVt, ss) {
    return Math.pow(10, deltaVt / ss);
  }

  // Chapter 6: the quasi-2D channel (lengths in nm, potentials in volts).
  const EPS_SI = 11.7;
  const EPS_SIO2 = 3.9;

  function naturalLength(tSi, tOx, nGates = 1, epsSi = EPS_SI, epsOx = EPS_SIO2) {
    return Math.sqrt((epsSi * tSi * tOx) / (nGates * epsOx));
  }

  function channelPotential(x, length, lam, vBi = 1.0, vDs = 0.05, phiGs = 0.4) {
    const s = Math.sinh(length / lam);
    return (phiGs + ((vBi - phiGs) * Math.sinh((length - x) / lam)) / s
      + ((vBi + vDs - phiGs) * Math.sinh(x / lam)) / s);
  }

  // The barrier top: phi is convex, so its minimum solves phi'(x) = 0. Returns u = x / lambda.
  function barrierTop(length, lam, vBi = 1.0, vDs = 0.05, phiGs = 0.4) {
    const l = length / lam, a = vBi - phiGs, b = vBi + vDs - phiGs, e = Math.exp(-l);
    if (a - b * e <= 0) return 0;
    return Math.min(Math.max(0.5 * (l + Math.log(a - b * e) - Math.log(b - a * e)), 0), l);
  }

  function barrierHeight(length, lam, vBi = 1.0, vDs = 0.05, phiGs = 0.4) {
    const u = barrierTop(length, lam, vBi, vDs, phiGs);
    return vBi - channelPotential(u * lam, length, lam, vBi, vDs, phiGs);
  }

  function gateCoupling(length, lam, vDs = 0.05, vBi = 1.0, phiGs = 0.4) {
    const l = length / lam, u = barrierTop(length, lam, vBi, vDs, phiGs);
    return 1 - (Math.sinh(l - u) + Math.sinh(u)) / Math.sinh(l);
  }

  function drainCoupling(length, lam, vDs = 0.05, vBi = 1.0, phiGs = 0.4) {
    const l = length / lam, u = barrierTop(length, lam, vBi, vDs, phiGs);
    return Math.sinh(u) / Math.sinh(l);
  }

  function diblMVperV(length, lam, vLo = 0.05, vHi = 0.75) {
    return (1000 * (barrierHeight(length, lam, 1.0, vLo) - barrierHeight(length, lam, 1.0, vHi))) / (vHi - vLo);
  }

  function shortChannelSwing(length, lam, T = 300, vDs = 0) {
    return subthresholdSwing(T) / gateCoupling(length, lam, vDs);
  }

  function intrinsicGain(length, lam, vDs = 0.4) {
    return gateCoupling(length, lam, vDs) / drainCoupling(length, lam, vDs);
  }

  function specificCurrent(iSpecRef, T = 300, m = 1, tRef = 300, mRef = 1) {
    return iSpecRef * (m / mRef) * (T / tRef) ** 2;
  }

  // Chapter 4 and Live Lab 3: ideal scaling, dimensions by kappa and the voltage by u.
  function generalizedScaling(kappa, u, fixedClock = false) {
    const delay = u / kappa ** 2;
    const frequency = fixedClock ? 1 : 1 / delay;
    const power = (1 / kappa) * (1 / u) ** 2 * frequency;
    return {
      size: 1 / kappa, voltage: 1 / u, density: kappa ** 2, current: kappa / u ** 2,
      capacitance: 1 / kappa, delay, frequency, power, power_density: power * kappa ** 2,
    };
  }

  // Chapters 7-10 and Live Lab 4: widths and the cell's height.
  function weffFin(nFin, hFin, wFin) {
    return nFin * (2 * hFin + wFin);
  }

  function weffSheets(nSheets, wSh, tSh) {
    return nSheets * 2 * (wSh + tSh);
  }

  const CELL_SPACING = { fin: [22.5, 45], sheet: [23, 46], fork: [27, 8], cfet: [27, null] };

  function finFootprint(nFin, wFin = 6, pitch = 27) {
    return (nFin - 1) * pitch + wFin;
  }

  function cellHeightNeeded(arch, deviceNm) {
    const [edge, gap] = CELL_SPACING[arch];
    return gap === null ? 2 * edge + deviceNm : 2 * edge + 2 * deviceNm + gap;
  }

  const api = {
    thermalVoltage, subthresholdSwing, fractionOverBarrier, drainCurrent, offCurrentRatio,
    naturalLength, channelPotential, barrierTop, barrierHeight, gateCoupling, drainCoupling,
    diblMVperV, shortChannelSwing, intrinsicGain, specificCurrent, generalizedScaling,
    weffFin, weffSheets, CELL_SPACING, finFootprint, cellHeightNeeded,
  };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.LabPhysics = api;
})(typeof window !== "undefined" ? window : globalThis);

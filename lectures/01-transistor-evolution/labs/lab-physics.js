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

  function barrierHeight(length, lam, vBi = 1.0, vDs = 0.05, phiGs = 0.4, n = 2001) {
    let lo = Infinity;
    for (let i = 0; i < n; i++) lo = Math.min(lo, channelPotential((length * i) / (n - 1), length, lam, vBi, vDs, phiGs));
    return vBi - lo;
  }

  function diblMVperV(length, lam, vLo = 0.05, vHi = 0.75, n = 2001) {
    return (1000 * (barrierHeight(length, lam, 1.0, vLo, 0.4, n) - barrierHeight(length, lam, 1.0, vHi, 0.4, n))) / (vHi - vLo);
  }

  function shortChannelSwing(length, lam, T = 300) {
    return subthresholdSwing(T) / (1 - 2 * Math.exp(-length / (2 * lam)));
  }

  const api = {
    thermalVoltage, subthresholdSwing, fractionOverBarrier, drainCurrent, offCurrentRatio,
    naturalLength, channelPotential, barrierHeight, diblMVperV, shortChannelSwing,
  };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.LabPhysics = api;
})(typeof window !== "undefined" ? window : globalThis);

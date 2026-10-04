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

  const api = { thermalVoltage, subthresholdSwing, fractionOverBarrier, drainCurrent, offCurrentRatio };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.LabPhysics = api;
})(typeof window !== "undefined" ? window : globalThis);

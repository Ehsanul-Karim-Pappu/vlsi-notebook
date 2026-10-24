// Shared helpers for the live labs.
(function () {
  const inDeck = window.parent !== window;

  // Inside the deck, a lab keeps the keyboard; Page Down / Page Up (a clicker) and ← / → (when
  // a slider doesn't have focus) move the deck on.
  document.addEventListener("keydown", (e) => {
    if (!inDeck) return;
    const onSlider = e.target && e.target.tagName === "INPUT";
    let go = null;
    if (e.key === "PageDown" || (!onSlider && e.key === "ArrowRight")) go = "next";
    if (e.key === "PageUp" || (!onSlider && e.key === "ArrowLeft")) go = "prev";
    if (go) {
      e.preventDefault();
      window.parent.postMessage({ type: "deck", go }, "*");
    }
  });

  // Size a canvas to its box at the screen's pixel density; calls draw(ctx, w, h) on resize.
  function fitCanvas(canvas, onResize) {
    const ctx = canvas.getContext("2d");
    const state = { ctx, w: 0, h: 0 };
    const resize = () => {
      const r = canvas.getBoundingClientRect();
      const dpr = window.devicePixelRatio || 1;
      canvas.width = Math.max(1, Math.round(r.width * dpr));
      canvas.height = Math.max(1, Math.round(r.height * dpr));
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      state.w = r.width;
      state.h = r.height;
      if (onResize) onResize(state);
    };
    new ResizeObserver(resize).observe(canvas);
    resize();
    return state;
  }

  const css = (name) => getComputedStyle(document.documentElement).getPropertyValue(name).trim();

  window.Lab = { fitCanvas, css, inDeck };
})();

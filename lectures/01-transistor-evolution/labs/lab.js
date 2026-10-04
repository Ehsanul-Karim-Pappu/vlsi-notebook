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

  // Language: the deck opens a lab with ?lang=en or ?lang=bn. The page's HTML is English;
  // translate(bn) swaps in Bengali for every element marked data-i18n="key".
  const lang = new URLSearchParams(location.search).get("lang") === "bn" ? "bn" : "en";
  document.documentElement.lang = lang;
  const t = (en, bn) => (lang === "bn" ? bn : en);
  function translate(bn) {
    if (lang !== "bn") return;
    document.querySelectorAll("[data-i18n]").forEach((el) => {
      const s = bn[el.dataset.i18n];
      if (s !== undefined) el.innerHTML = s;
    });
    if (bn._title) document.title = bn._title;
  }

  window.Lab = { fitCanvas, css, inDeck, lang, t, translate };
})();

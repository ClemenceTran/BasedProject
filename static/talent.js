document.addEventListener("DOMContentLoaded", () => {
  const cards = document.querySelectorAll(".talent-card");

  cards.forEach((card, idx) => {
    const target = parseInt(card.dataset.pct || "0", 10);
    const label = card.dataset.label || "";

    const donut = card.querySelector(".donut");
    const numberEl = card.querySelector(".donut-number");
    const labelEl = card.querySelector(".talent-label");

    if (labelEl) labelEl.textContent = label;

    // small stagger so it feels nice
    const delay = 80 * idx;

    setTimeout(() => {
      const duration = 900; // ms
      const start = performance.now();

      function tick(now) {
        const t = Math.min(1, (now - start) / duration);
        // easeOutCubic
        const eased = 1 - Math.pow(1 - t, 3);
        const val = Math.round(eased * target);

        donut.style.setProperty("--p", val);
        numberEl.textContent = `${val}%`;

        if (t < 1) requestAnimationFrame(tick);
      }

      requestAnimationFrame(tick);
    }, delay);
  });
});
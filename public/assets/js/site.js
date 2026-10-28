(() => {
  const menuBtn = document.querySelector("[data-menu-btn]");
  const menu = document.getElementById("menu");
  if (menuBtn && menu) {
    const setOpen = (open) => {
      menuBtn.setAttribute("aria-expanded", String(open));
      menuBtn.querySelector(".sr-only").textContent = open ? "Fechar menu" : "Abrir menu";
      menu.hidden = !open;
    };
    menuBtn.addEventListener("click", () => setOpen(menuBtn.getAttribute("aria-expanded") !== "true"));
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && !menu.hidden) { setOpen(false); menuBtn.focus(); }
    });
    menu.addEventListener("click", (e) => { if (e.target.closest("a")) setOpen(false); });
  }

  const chips = [...document.querySelectorAll("[data-filter]")];
  if (chips.length) {
    const items = [...document.querySelectorAll("[data-tags]")];
    const count = document.querySelector("[data-count]");
    const valid = new Set(chips.map((c) => c.dataset.filter));
    const apply = (raw) => {
      const f = valid.has(raw) ? raw : "todos";
      chips.forEach((c) => c.setAttribute("aria-pressed", String(c.dataset.filter === f)));
      let n = 0;
      items.forEach((el) => {
        const show = f === "todos" || el.dataset.tags.split(" ").includes(f);
        el.hidden = !show;
        if (show) n++;
      });
      if (count) count.textContent = n === 1 ? "1 peça" : `${n} peças`;
    };
    chips.forEach((c) => c.addEventListener("click", () => {
      const f = c.dataset.filter;
      history.replaceState(null, "", f === "todos" ? location.pathname : `#${f}`);
      apply(f);
    }));
    const fromHash = () => apply(decodeURIComponent(location.hash.slice(1)) || "todos");
    window.addEventListener("hashchange", fromHash);
    fromHash();
  }

  const slots = [...document.querySelectorAll("[data-rotate]")];
  if (slots.length && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
    let turn = 0;
    setInterval(() => {
      if (document.hidden) return;
      const imgs = [...slots[turn % slots.length].querySelectorAll("img")];
      const i = imgs.findIndex((el) => el.classList.contains("is-on"));
      const next = imgs[(i + 1) % imgs.length];
      if (next.complete) { imgs[i].classList.remove("is-on"); next.classList.add("is-on"); }
      turn++;
    }, 2200);
  }

  const bar = document.querySelector("[data-buybar]");
  const anchor = document.querySelector("[data-buy-anchor]");
  if (bar && anchor && "IntersectionObserver" in window) {
    new IntersectionObserver(([entry]) => {
      bar.classList.toggle("is-visible", !entry.isIntersecting && entry.boundingClientRect.top < 0);
    }).observe(anchor);
  }
})();

/* ATH cinema layer (2026-11-13): hero loops from the v3 commercial footage, story beats, reveal on scroll.
   Loops are silent, ≤1 MB, load only when the hero is on screen, pause off screen / in a hidden tab, and never run
   for prefers-reduced-motion (the poster frame stays). Phones in portrait get the vertical cut. */
(() => {
  window.ATH_CINE = 1;
  const calm = matchMedia('(prefers-reduced-motion:reduce)');
  const tall = matchMedia('(max-aspect-ratio:4/5)');
  document.querySelectorAll('video[data-cine]').forEach((v) => {
    const d = v.dataset, poster = v.parentElement.querySelector('img.cine-poster');
    const want = () => (tall.matches && d.src9 ? d.src9 : d.src16);
    const still = () => (tall.matches && d.poster9 ? d.poster9 : d.poster16);
    const setStill = () => { const p = still(); if (p && poster && poster.getAttribute('src') !== p) poster.src = p; };
    setStill();
    if (calm.matches) return;
    let cur = '', seen = false;
    const go = () => {
      const s = want(); if (s !== cur) { cur = s; v.src = s; }
      const p = v.play(); if (p && p.then) p.then(() => v.classList.add('is-rolling')).catch(() => {});
    };
    v.addEventListener('playing', () => v.classList.add('is-rolling'));
    new IntersectionObserver((es) => es.forEach((e) => { seen = e.isIntersecting; if (seen && !document.hidden) go(); else if (!v.paused) v.pause(); }), { threshold: 0.04 }).observe(v.parentElement);
    tall.addEventListener?.('change', () => { setStill(); if (cur) { v.classList.remove('is-rolling'); cur = ''; if (seen) go(); } });
    document.addEventListener('visibilitychange', () => { if (document.hidden) v.pause(); else if (seen && cur) go(); });
  });
  document.querySelectorAll('[data-beats]').forEach((b) => {
    const lines = [...b.children];
    if (calm.matches) { lines.forEach((x) => x.classList.add('on')); return; }
    lines.forEach((x, i) => setTimeout(() => { x.classList.add('on'); if (i) lines[i - 1].classList.add('dim'); }, 350 + i * 1500));
  });
  if (calm.matches || !('IntersectionObserver' in window)) return;
  const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('rv-in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -6% 0px' });
  document.querySelectorAll('main > .block > .wrap > .block-head').forEach((el) => {
    if (el.hidden || el.getBoundingClientRect().top < innerHeight) return;
    el.classList.add('rv'); io.observe(el);
  });
})();

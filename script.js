// Small progressive enhancement: mark the visible navigation section.
// All content and links remain available without JavaScript.
(() => {
  const sections = [...document.querySelectorAll('main section[id]:not(#top)')];
  const links = [...document.querySelectorAll('.nav-links a[href^="#"]')];
  if (!('IntersectionObserver' in window)) return;
  const observer = new IntersectionObserver((entries) => {
    const visible = entries.filter((entry) => entry.isIntersecting)
      .sort((a, b) => b.intersectionRatio - a.intersectionRatio);
    if (!visible.length) return;
    const id = visible[0].target.id;
    links.forEach((link) => {
      const active = link.getAttribute('href') === `#${id}`;
      link.classList.toggle('is-active', active);
      if (active) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  }, { rootMargin: '-18% 0px -58% 0px', threshold: [0, 0.1, 0.5] });
  sections.forEach((section) => observer.observe(section));
})();

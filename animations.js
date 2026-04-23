// animations.js — TechFlair micro-animations
// GPU-only (opacity + transform), aucune librairie, ~1 Ko minifié
(function () {
  'use strict';

  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ── 1. Scroll-reveal via IntersectionObserver ──────────────────
  const observer = reduced ? null : new IntersectionObserver(
    function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add('is-visible');
          observer.unobserve(e.target);
        }
      });
    },
    { threshold: 0.07, rootMargin: '0px 0px -40px 0px' }
  );

  window.revealAll = function () {
    document.querySelectorAll('.reveal:not(.is-visible)').forEach(function (el) {
      if (reduced) {
        el.classList.add('is-visible');
      } else {
        observer.observe(el);
      }
    });
  };

  // Premier passage au chargement
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', window.revealAll);
  } else {
    window.revealAll();
  }

  // ── 2. Header scroll-shadow ────────────────────────────────────
  document.addEventListener('DOMContentLoaded', function () {
    var header = document.querySelector('header');
    if (!header) return;
    window.addEventListener('scroll', function () {
      header.classList.toggle('header-scrolled', window.scrollY > 10);
    }, { passive: true });
  });

})();

(function () {
  const KEY = 'tf_cookie_consent';
  if (localStorage.getItem(KEY)) return;

  const banner = document.createElement('div');
  banner.id = 'tf-cookie-banner';
  banner.setAttribute('role', 'dialog');
  banner.setAttribute('aria-label', 'Gestion des cookies');
  banner.style.cssText = [
    'position:fixed;bottom:0;left:0;right:0;z-index:99998',
    'background:#111827;color:#f9fafb',
    'padding:1rem 1.5rem',
    'display:flex;align-items:center;justify-content:space-between;gap:1rem;flex-wrap:wrap',
    'font-family:Inter,system-ui,sans-serif;font-size:.875rem;line-height:1.5',
    'box-shadow:0 -4px 24px rgba(0,0,0,.18)',
  ].join(';');

  banner.innerHTML =
    '<p style="margin:0;color:#d1d5db;flex:1;min-width:200px">' +
      'TechFlair utilise <strong style="color:#f9fafb">Google Analytics</strong> pour mesurer son audience. ' +
      '<a href="/confidentialite.html" style="color:#38bdf8;text-decoration:underline">En savoir plus</a>' +
    '</p>' +
    '<div style="display:flex;gap:.5rem;flex-shrink:0">' +
      '<button id="tf-cookie-refuse" style="padding:.5rem 1rem;border-radius:.5rem;background:transparent;border:1px solid #374151;color:#9ca3af;font-size:.8rem;cursor:pointer;white-space:nowrap">Refuser</button>' +
      '<button id="tf-cookie-accept" style="padding:.5rem 1rem;border-radius:.5rem;background:#0ea5e9;border:none;color:#fff;font-size:.8rem;font-weight:600;cursor:pointer;white-space:nowrap">Accepter</button>' +
    '</div>';

  function hideBanner() { banner.remove(); }

  function onAccept() {
    localStorage.setItem(KEY, 'accepted');
    if (typeof gtag === 'function') {
      gtag('consent', 'update', { analytics_storage: 'granted' });
    }
    hideBanner();
  }

  function onRefuse() {
    localStorage.setItem(KEY, 'refused');
    hideBanner();
  }

  if (document.body) {
    document.body.appendChild(banner);
    document.getElementById('tf-cookie-accept').addEventListener('click', onAccept);
    document.getElementById('tf-cookie-refuse').addEventListener('click', onRefuse);
  } else {
    document.addEventListener('DOMContentLoaded', function () {
      document.body.appendChild(banner);
      document.getElementById('tf-cookie-accept').addEventListener('click', onAccept);
      document.getElementById('tf-cookie-refuse').addEventListener('click', onRefuse);
    });
  }
})();

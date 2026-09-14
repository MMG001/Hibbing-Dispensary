// Hibbing Dispensary — site scripts
(function () {
  // ---- Age gate (remembered for 30 days) ----
  var gate = document.getElementById('age-gate');
  var yes = document.getElementById('age-yes');
  var KEY = 'hd_age_verified';
  function verified() {
    try {
      var v = localStorage.getItem(KEY);
      return v && Date.now() - parseInt(v, 10) < 30 * 24 * 60 * 60 * 1000;
    } catch (e) { return false; }
  }
  if (gate && !verified()) {
    gate.classList.remove('hidden');
    gate.classList.add('flex');
    document.body.style.overflow = 'hidden';
  }
  if (yes) {
    yes.addEventListener('click', function () {
      try { localStorage.setItem(KEY, String(Date.now())); } catch (e) {}
      gate.classList.add('hidden');
      gate.classList.remove('flex');
      document.body.style.overflow = '';
    });
  }

  // ---- Mobile menu ----
  var btn = document.getElementById('menu-btn');
  var menu = document.getElementById('mobile-menu');
  if (btn && menu) {
    btn.addEventListener('click', function () {
      var open = !menu.classList.contains('hidden');
      menu.classList.toggle('hidden');
      btn.setAttribute('aria-expanded', String(!open));
      btn.querySelector('span').textContent = open ? 'menu' : 'close';
    });
  }
})();

document.addEventListener('DOMContentLoaded', function () {
  var buttons = document.querySelectorAll('.lang-toggle button');
  var titles = { en: document.body.getAttribute('data-title-en'), es: document.body.getAttribute('data-title-es') };

  function applyLang(lang) {
    document.documentElement.setAttribute('data-lang', lang);
    document.documentElement.lang = lang;
    if (titles[lang]) document.title = titles[lang];
    buttons.forEach(function (b) { b.classList.toggle('active', b.dataset.setLang === lang); });
  }

  buttons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var lang = btn.dataset.setLang;
      try {
        localStorage.setItem('site-lang', lang);
      } catch (e) {
        /* localStorage unavailable — language still switches, just won't persist across pages */
      }
      applyLang(lang);
    });
  });

  applyLang(document.documentElement.getAttribute('data-lang') || 'en');
});

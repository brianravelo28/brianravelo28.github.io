(function () {
  var lang = 'en';
  try {
    lang = localStorage.getItem('site-lang') || 'en';
  } catch (e) {
    /* localStorage unavailable (e.g. file:// with storage restrictions) — fall back to English */
  }
  document.documentElement.setAttribute('data-lang', lang);
  document.documentElement.lang = lang;
})();

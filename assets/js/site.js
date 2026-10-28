/* Painting With Purpose, demo 1: menu, photo fade-in, before/after sliders, demo forms. No libraries. */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  document.documentElement.classList.add('js');

  /* menu: drops down under the header; Menu / Close */
  var hdr = $('.hdr'), btn = $('.menu-btn');
  function setMenu(open) {
    hdr.classList.toggle('open', open);
    document.body.classList.toggle('menu-open', open);
    btn.setAttribute('aria-expanded', String(open));
    btn.textContent = open ? 'Close' : 'Menu';
  }
  btn.addEventListener('click', function () { setMenu(!hdr.classList.contains('open')); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && hdr.classList.contains('open')) { setMenu(false); btn.focus(); }
  });
  document.addEventListener('click', function (e) {
    if (hdr.classList.contains('open') && !hdr.contains(e.target)) setMenu(false);
  });
  $$('.menu a').forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });

  /* photographs fade in once loaded */
  $$('main img:not(.wc)').forEach(function (im) {
    var show = function () { im.classList.add('in'); };
    if (im.complete && im.naturalWidth) show();
    else { im.addEventListener('load', show); im.addEventListener('error', show); }
  });

  /* before/after: the range input drives --p */
  $$('.ba-frame:not(.ba-dip)').forEach(function (f) {
    var r = $('.ba-range', f);
    r.addEventListener('input', function () { f.style.setProperty('--p', r.value + '%'); });
  });

  /* demo forms: check required fields, then thank (nothing is sent) */
  $$('[data-form]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var bad = $$('[required]', form).filter(function (i) {
        var ok = i.value.trim() !== '' && i.checkValidity();
        i.closest('.field').classList.toggle('bad', !ok);
        return !ok;
      });
      if (bad.length) { bad[0].focus(); return; }
      var ok = $('.form-ok', form);
      ok.hidden = false;
      $('.submit', form).hidden = true;
    });
  });
})();

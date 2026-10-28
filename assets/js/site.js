/* Painting With Purpose, demo 1: menu, solid header, hero clips, work peek, before/after sliders, demo forms. No libraries. */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var body = document.body;
  var still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.documentElement.classList.add('js');

  /* menu: full screen sheet under the header; Menu / Close */
  var menu = $('#menu'), btn = $('.menu-btn'), shut;
  function setMenu(open) {
    clearTimeout(shut);
    btn.setAttribute('aria-expanded', String(open));
    btn.textContent = open ? 'Close' : 'Menu';
    if (open) {
      menu.hidden = false;
      requestAnimationFrame(function () { body.classList.add('menu-open'); });
    } else {
      body.classList.remove('menu-open');
      shut = setTimeout(function () { menu.hidden = true; }, 350);
    }
  }
  btn.addEventListener('click', function () { setMenu(menu.hidden || !body.classList.contains('menu-open')); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !menu.hidden) { setMenu(false); btn.focus(); }
  });
  $$('a', menu).forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });

  /* scroll: the header turns solid once past the top; nothing else is tied to scroll */
  var ticking = false;
  /* the header goes clear (white logo and links) while a full-width photo is under it */
  var darks = $$('[data-dark]');
  function onScroll() {
    ticking = false;
    body.classList.toggle('scrolled', window.scrollY > 40);
    var h = 40, w = window.innerWidth;
    body.classList.toggle('ondark', darks.some(function (el) {
      var r = el.getBoundingClientRect();
      return r.top <= 1 && r.bottom > h && r.left <= 1 && r.right >= w - 1;
    }));
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  window.addEventListener('resize', onScroll);
  onScroll();

  /* hero clips: only present once the mp4s are dropped in; the still shows until a clip can play */
  var clips = $$('video.clip');
  if (clips.length && !still) {
    var tall = window.matchMedia('(max-aspect-ratio: 4/5)').matches;
    var start = function (v) {
      var src = (tall && v.dataset.srcTall) || v.dataset.src || v.dataset.srcTall;
      if (!src) return;
      if (!v.src) {
        v.src = src;
        v.addEventListener('playing', function () { v.classList.add('ready'); });
        /* loop by dissolving back to the still (the clip's first frame), then playing again */
        v.addEventListener('ended', function () {
          v.classList.remove('ready');
          setTimeout(function () { v.currentTime = 0; v.play().catch(function () {}); }, 900);
        });
      }
      var p = v.play();
      if (p && p.catch) p.catch(function () {});
    };
    if ('IntersectionObserver' in window) {
      var vo = new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          if (e.isIntersecting) start(e.target);
          else if (e.target.src) e.target.pause();
        });
      }, { rootMargin: '200px 0px' });
      clips.forEach(function (v) { vo.observe(v); });
    } else clips.forEach(start);
  }

  /* work index: a small photo follows the pointer over each row (pointer devices only) */
  var peek = $('.peek');
  if (peek && window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
    var pimg = $('img', peek);
    $$('.prow[data-peek]').forEach(function (row) {
      new Image().src = row.dataset.peek;
      row.addEventListener('mouseenter', function () { pimg.src = row.dataset.peek; peek.classList.add('on'); });
      row.addEventListener('mouseleave', function () { peek.classList.remove('on'); });
    });
    document.addEventListener('mousemove', function (e) {
      peek.style.left = (e.clientX + 24) + 'px';
      peek.style.top = e.clientY + 'px';
    }, { passive: true });
  }

  /* before/after: the range input drives --p */
  $$('.ba-frame:not(.ba-dip)').forEach(function (f) {
    var r = $('.ba-range', f);
    if (r) r.addEventListener('input', function () { f.style.setProperty('--p', r.value + '%'); });
  });

  /* before & after: nine pairs first, the rest on request */
  var more = $('[data-show-more]');
  if (more) more.addEventListener('click', function () {
    $$('.ba[data-more]').forEach(function (f) { f.hidden = false; });
    more.parentNode.hidden = true;
  });

  /* demo forms: check required fields, then thank (nothing is sent) */
  $$('[data-form]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var bad = $$('[required]', form).filter(function (i) {
        var ok = i.value.trim() !== '' && i.checkValidity();
        var f = i.closest('.field');
        if (f) {
          f.classList.toggle('bad', !ok);
          var m = $('.err', f);
          if (!m) {
            m = document.createElement('small');
            m.className = 'err';
            m.id = 'err-' + (form.dataset.form || 'f') + '-' + i.name;
            m.setAttribute('aria-live', 'polite');
            f.appendChild(m);
            i.setAttribute('aria-describedby', m.id);
          }
          m.textContent = i.value.trim() === '' ? 'Required' : (i.type === 'email' ? 'Check this email address' : 'Check this field');
          m.hidden = ok;
        }
        i.setAttribute('aria-invalid', String(!ok));
        return !ok;
      });
      if (bad.length) { bad[0].focus(); return; }
      $('.form-ok', form).hidden = false;
      var s = $('.submit', form);
      if (s) s.hidden = true;
    });
  });
})();

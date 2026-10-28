/* Painting With Purpose, demo 1: menu, scroll motion, hero clips, work peek, before/after sliders, demo forms. No libraries. */
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

  /* scroll: solid header once past the top, reveal progress */
  var reveals = $$('[data-reveal]');
  var ticking = false;
  function onScroll() {
    ticking = false;
    var vh = window.innerHeight;
    body.classList.toggle('scrolled', window.scrollY > 40);
    reveals.forEach(function (el) {
      var r = el.getBoundingClientRect();
      var span = Math.max(1, r.height - vh);
      var p = still ? 1 : Math.min(1, Math.max(0, -r.top / (span * 0.75)));
      el.style.setProperty('--r', p.toFixed(4));
    });
  }
  function req() { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }
  window.addEventListener('scroll', req, { passive: true });
  window.addEventListener('resize', req);
  onScroll();

  /* quiet fade-up for blocks marked .rv */
  var rvs = $$('.rv');
  if ('IntersectionObserver' in window && !still) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -10% 0px' });
    rvs.forEach(function (el) { io.observe(el); });
  } else {
    rvs.forEach(function (el) { el.classList.add('in'); });
  }

  /* hero clips: only present once the mp4s are dropped in; the still shows until a clip can play */
  var clips = $$('video.clip');
  var LOOP = 6;
  if (clips.length && !still) {
    var tall = window.matchMedia('(max-aspect-ratio: 4/5)').matches;
    var start = function (v) {
      var src = (tall && v.dataset.srcTall) || v.dataset.src || v.dataset.srcTall;
      if (!src) return;
      if (!v.src) {
        v.src = src;
        /* keep each loop short: only the first few seconds of a clip are used */
        v.addEventListener('timeupdate', function () { if (v.currentTime > LOOP) v.currentTime = 0; });
        v.addEventListener('playing', function () { v.classList.add('ready'); }, { once: true });
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

  /* sound: muted until the visitor turns it on; then only the clip most in view is heard, faded in and out */
  var snd = $('.snd');
  if (snd && clips.length && !still) {
    var on = false, seen = new Map();
    var fade = function (v, to) {
      cancelAnimationFrame(v._f);
      if (to > 0) { v.muted = false; }
      var step = function () {
        var d = to - v.volume;
        if (Math.abs(d) < 0.03) { v.volume = to; if (to === 0) v.muted = true; return; }
        v.volume = Math.min(1, Math.max(0, v.volume + d * 0.12));
        v._f = requestAnimationFrame(step);
      };
      step();
    };
    var mix = function () {
      var best = null, top = 0.35;
      seen.forEach(function (r, v) { if (r > top) { top = r; best = v; } });
      clips.forEach(function (v) { fade(v, on && v === best ? 1 : 0); });
    };
    if ('IntersectionObserver' in window) {
      var so = new IntersectionObserver(function (es) {
        es.forEach(function (e) { seen.set(e.target, e.isIntersecting ? e.intersectionRatio : 0); });
        if (on) mix();
      }, { threshold: [0, 0.2, 0.35, 0.5, 0.65, 0.8, 1] });
      clips.forEach(function (v) { so.observe(v); });
    }
    clips.forEach(function (v) { v.volume = 0; });
    snd.addEventListener('click', function () {
      on = !on;
      snd.classList.toggle('on', on);
      snd.setAttribute('aria-pressed', String(on));
      $('.snd-t', snd).textContent = on ? 'Sound on' : 'Sound off';
      if (on) clips.forEach(function (v) { if (v.src && v.paused && (seen.get(v) || 0) > 0) v.play().catch(function () {}); });
      mix();
    });
  } else if (snd) snd.hidden = true;

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

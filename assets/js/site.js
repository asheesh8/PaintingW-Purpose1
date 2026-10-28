(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* header: transparent over heroes, solid after scrolling */
  var hdr = $('.hdr');
  if (hdr && hdr.dataset.over === '1') {
    var onScroll = function () {
      var solid = window.scrollY > 40;
      hdr.classList.toggle('solid', solid);
      hdr.classList.toggle('over', !solid);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* mobile menu */
  var menu = $('#menu'), mBtn = $('.menu-btn'), mClose = $('.menu-close');
  function setMenu(open) {
    if (!menu) return;
    menu.classList.toggle('open', open);
    menu.setAttribute('aria-hidden', String(!open));
    if (mBtn) mBtn.setAttribute('aria-expanded', String(open));
    document.body.style.overflow = open ? 'hidden' : '';
    if (open && mClose) mClose.focus();
  }
  if (mBtn) mBtn.addEventListener('click', function () { setMenu(true); });
  if (mClose) mClose.addEventListener('click', function () { setMenu(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });

  /* home hero slideshow */
  var hero = $('[data-hero]');
  var slides = hero ? $$('.hero-slide', hero) : [];
  if (slides.length > 1) {
    var ticks = $$('.ticks button', hero), cur = 0, timer;
    var nameEl = $('[data-hero-name]'), locEl = $('[data-hero-loc]'), linkEl = $('[data-hero-link]');
    var show = function (i) {
      slides[cur].classList.remove('on'); if (ticks[cur]) ticks[cur].classList.remove('on');
      cur = (i + slides.length) % slides.length;
      var s = slides[cur];
      s.classList.add('on'); if (ticks[cur]) ticks[cur].classList.add('on');
      if (nameEl) nameEl.textContent = s.dataset.name;
      if (locEl) locEl.textContent = s.dataset.loc;
      if (linkEl) linkEl.setAttribute('href', s.dataset.href);
    };
    var play = function () { clearInterval(timer); if (!reduce) timer = setInterval(function () { show(cur + 1); }, 6500); };
    ticks.forEach(function (t, i) { t.addEventListener('click', function () { show(i); play(); }); });
    play();
  }

  /* project index: photo follows the cursor */
  var peek = $('.peek'), peekImg = peek ? $('img', peek) : null;
  if (peek && window.matchMedia('(hover: hover)').matches) {
    var px = 0, py = 0, tx = 0, ty = 0, raf = null;
    var loop = function () {
      px += (tx - px) * 0.18; py += (ty - py) * 0.18;
      peek.style.left = px + 'px'; peek.style.top = py + 'px';
      raf = Math.abs(tx - px) + Math.abs(ty - py) > 0.5 ? requestAnimationFrame(loop) : null;
    };
    $$('.prow').forEach(function (row) {
      row.addEventListener('mouseenter', function (e) {
        peekImg.src = row.dataset.img; peek.classList.add('on');
        px = tx = e.clientX + 160; py = ty = e.clientY;
      });
      row.addEventListener('mousemove', function (e) {
        tx = e.clientX + 160; ty = e.clientY;
        if (!raf) raf = requestAnimationFrame(loop);
      });
      row.addEventListener('mouseleave', function () { peek.classList.remove('on'); });
    });
  }

  /* before / after sliders: drag anywhere, keyboard via the range input */
  $$('[data-ba]').forEach(function (ba) {
    var input = $('input', ba);
    var set = function (v) { v = Math.max(0, Math.min(100, v)); ba.style.setProperty('--pos', v + '%'); input.value = v; };
    input.addEventListener('input', function () { set(+input.value); });
    var dragging = false;
    var fromEvent = function (e) { var r = ba.getBoundingClientRect(); set(((e.clientX - r.left) / r.width) * 100); };
    ba.addEventListener('pointerdown', function (e) { dragging = true; ba.classList.add('drag'); fromEvent(e); try { ba.setPointerCapture(e.pointerId); } catch (_) {} });
    ba.addEventListener('pointermove', function (e) { if (dragging) fromEvent(e); });
    var end = function () { dragging = false; ba.classList.remove('drag'); };
    ba.addEventListener('pointerup', end); ba.addEventListener('pointercancel', end);
    // one gentle sweep when it first scrolls into view, so people see it moves
    if (!reduce && 'IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (en) {
          if (!en.isIntersecting) return; io.disconnect();
          var t0 = performance.now(), d = 1600;
          (function step(t) {
            if (dragging) return;
            var k = Math.min(1, (t - t0) / d);
            set(50 + Math.sin(k * Math.PI * 2) * 18 * (1 - k));
            if (k < 1) requestAnimationFrame(step);
          })(t0);
        });
      }, { threshold: 0.6 });
      io.observe(ba);
    }
  });

  /* transformations page: stage + filterable thumbnails */
  var tfData = $('#tf-data');
  if (tfData) {
    var list = JSON.parse(tfData.textContent), ti = 0;
    var stage = $('[data-tf-stage]'), sba = $('.ba', stage), sinput = $('input', sba);
    var thumbs = $$('.tf-th'), peekBtn = $('[data-tf-peek]');
    var pad = function (n) { return (n < 10 ? '0' : '') + n; };
    var load = function (i, scroll) {
      ti = (i + list.length) % list.length; var d = list[ti];
      ['before', 'after'].forEach(function (side) {
        var im = $('.' + side + ' img', sba); im.src = 'assets/ba/' + d.id + '-' + side + '.jpg'; im.alt = d.title + ', ' + side;
      });
      sba.classList.toggle('dip', !!d.dip);
      sba.style.setProperty('--pos', '50%'); if (sinput) sinput.value = 50;
      if (peekBtn) { peekBtn.setAttribute('aria-pressed', 'false'); peekBtn.textContent = 'Show before'; peekBtn.hidden = !!d.dip; }
      $('[data-tf-n]').textContent = pad(ti + 1);
      $('[data-tf-cat]').textContent = d.cat;
      $('[data-tf-title]').textContent = d.title;
      $('[data-tf-note]').textContent = d.note;
      thumbs.forEach(function (t) { t.classList.toggle('cur', +t.dataset.i === ti); });
      sba.classList.remove('tf-swap'); void sba.offsetWidth; sba.classList.add('tf-swap');
      if (scroll) stage.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'center' });
    };
    thumbs.forEach(function (t) { t.addEventListener('click', function () { load(+t.dataset.i, true); }); });
    $$('[data-tf-step]').forEach(function (b) { b.addEventListener('click', function () { load(ti + (+b.dataset.tfStep)); }); });
    document.addEventListener('keydown', function (e) {
      if (/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName) && document.activeElement !== sinput) return;
      if (e.key === 'ArrowRight' && document.activeElement !== sinput) load(ti + 1);
      if (e.key === 'ArrowLeft' && document.activeElement !== sinput) load(ti - 1);
    });
    if (peekBtn) peekBtn.addEventListener('click', function () {
      var on = peekBtn.getAttribute('aria-pressed') !== 'true';
      peekBtn.setAttribute('aria-pressed', String(on)); peekBtn.textContent = on ? 'Show after' : 'Show before';
      sba.style.transition = 'none';
      var from = on ? 50 : 100, to = on ? 100 : 50, t0 = performance.now();
      (function step(t) { var k = Math.min(1, (t - t0) / 600), e2 = 1 - Math.pow(1 - k, 3), v = from + (to - from) * e2;
        sba.style.setProperty('--pos', v + '%'); if (sinput) sinput.value = v; if (k < 1) requestAnimationFrame(step); })(t0);
    });
    var tchips = $$('[data-tf-filter]');
    tchips.forEach(function (c) {
      c.addEventListener('click', function () {
        tchips.forEach(function (x) { x.setAttribute('aria-pressed', String(x === c)); });
        var f = c.dataset.tfFilter;
        thumbs.forEach(function (t) { t.hidden = !(f === 'all' || t.dataset.cat === f); });
      });
    });
    thumbs[0] && thumbs[0].classList.add('cur');
  }

  /* reviews carousel */
  var data = $('#reviews-data');
  if (data) {
    var reviews = JSON.parse(data.textContent), ri = 0, stage = $('.rev-stage');
    var q = $('[data-rev-q]'), n = $('[data-rev-n]'), r = $('[data-rev-r]'), c = $('[data-rev-count]');
    var showR = function (i) {
      ri = (i + reviews.length) % reviews.length;
      var v = reviews[ri];
      q.textContent = '“' + v.q + '”'; n.textContent = v.n; r.textContent = '· ' + v.r;
      c.textContent = (ri + 1) + ' / ' + reviews.length;
      stage.classList.remove('rev-fade'); void stage.offsetWidth; stage.classList.add('rev-fade');
    };
    $$('[data-rev]').forEach(function (b) { b.addEventListener('click', function () { showR(ri + (+b.dataset.rev)); }); });
  }

  /* work filters + grid/index toggle */
  var chips = $$('[data-filter]');
  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      chips.forEach(function (c) { c.setAttribute('aria-pressed', String(c === chip)); });
      var f = chip.dataset.filter;
      $$('.work-grid .card').forEach(function (card) {
        card.hidden = !(f === 'all' || (' ' + card.dataset.tags + ' ').indexOf(' ' + f + ' ') > -1);
      });
    });
  });
  var views = $$('[data-view]');
  views.forEach(function (v) {
    v.addEventListener('click', function () {
      views.forEach(function (x) { x.setAttribute('aria-pressed', String(x === v)); });
      var grid = $('[data-view-grid]'), idx = $('[data-view-index]');
      grid.hidden = v.dataset.view !== 'grid'; idx.hidden = v.dataset.view !== 'index';
      $$('[data-filter]').forEach(function (c) { c.disabled = v.dataset.view !== 'grid'; });
    });
  });

  /* demo forms */
  $$('[data-form]').forEach(function (f) {
    f.addEventListener('submit', function (e) { e.preventDefault(); var ok = $('.form-ok', f); if (ok) ok.hidden = false; });
  });

  /* watercolor art slots: show the painted placeholder until the real file exists */
  $$('.art').forEach(function (fig) {
    var im = $('img', fig);
    var fail = function () { fig.classList.add('empty'); if (im) im.remove(); };
    if (!im) return fail();
    if (im.complete && im.naturalWidth === 0) fail();
    im.addEventListener('error', fail);
  });

  /* number count-up (numbers are already correct in the HTML) */
  if (!reduce && 'IntersectionObserver' in window) {
    var cio = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (!en.isIntersecting) return; cio.unobserve(en.target);
        var el = en.target, end = +el.dataset.count, pre = el.dataset.prefix || '', t0 = performance.now();
        (function f(t) {
          var k = Math.min(1, (t - t0) / 1500), v = Math.round(end * (1 - Math.pow(1 - k, 3)));
          el.textContent = pre + v.toLocaleString('en-US');
          if (k < 1) requestAnimationFrame(f);
        })(t0);
      });
    }, { threshold: 0.6 });
    $$('[data-count]').forEach(function (el) { cio.observe(el); });
  }

  /* gentle lift for blocks below the fold (visible at rest; only offset until they enter) */
  if (!reduce && 'IntersectionObserver' in window) {
    var vh = window.innerHeight;
    var rio = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.remove('pre'); rio.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    $$('.rv').forEach(function (el) {
      if (el.getBoundingClientRect().top > vh) { el.classList.add('pre'); rio.observe(el); }
    });
  }

  /* drag-to-scroll for the photo rail on desktop */
  $$('.rail').forEach(function (rail) {
    var down = false, sx = 0, sl = 0;
    rail.addEventListener('pointerdown', function (e) { if (e.pointerType !== 'mouse') return; down = true; sx = e.clientX; sl = rail.scrollLeft; rail.style.scrollSnapType = 'none'; });
    window.addEventListener('pointermove', function (e) { if (down) rail.scrollLeft = sl - (e.clientX - sx); });
    window.addEventListener('pointerup', function () { if (down) { down = false; rail.style.scrollSnapType = ''; } });
  });
})();

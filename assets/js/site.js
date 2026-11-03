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
    var h = 40, w = document.documentElement.clientWidth; /* not innerWidth, which counts a classic (Windows) scrollbar */
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
      var small = window.innerWidth < 1100;
      var src = (tall && v.dataset.srcTall) || (small && v.dataset.srcSm) || v.dataset.src || v.dataset.srcSm || v.dataset.srcTall;
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

  /* home hero: the walkthrough loop behind the logo; phones get the tall cut, smaller screens the 720p one */
  var loop = $('.hero-loop');
  if (loop && !still) {
    var tallScreen = window.matchMedia('(max-aspect-ratio: 4/5)').matches;
    loop.src = tallScreen ? loop.dataset.srcTall : window.innerWidth < 1100 ? loop.dataset.srcSm : loop.dataset.src;
    loop.addEventListener('playing', function () { loop.classList.add('ready'); });
    var go = loop.play();
    if (go && go.catch) go.catch(function () {});
  }

  /* work index: a small photo follows the pointer over each row (pointer devices only) */
  var peek = $('.peek');
  if (peek && window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
    var pimg = $('img', peek), pal = $('.peek-pal', peek);
    $$('.prow[data-peek]').forEach(function (row) {
      new Image().src = row.dataset.peek;
      /* the job's paint colors sit under the photo */
      var chips = (row.dataset.palette || '').split('|').filter(Boolean).map(function (s) {
        var p = s.split(':');
        return '<span class="chip"><i style="background:' + p[1] + '"></i><b>' + p[0] + '</b><small>' + p[1] + '</small></span>';
      }).join('');
      row.addEventListener('mouseenter', function () { pimg.src = row.dataset.peek; pal.innerHTML = chips; peek.classList.add('on'); });
      row.addEventListener('mouseleave', function () { peek.classList.remove('on'); });
    });
    document.addEventListener('mousemove', function (e) {
      peek.style.left = (e.clientX + 24) + 'px';
      peek.style.top = e.clientY + 'px';
    }, { passive: true });
  }

  /* contact: a "Request a proposal" link from a service preselects it */
  var want = new URLSearchParams(location.search).get('service');
  if (want) $$('select[name="service"] option').forEach(function (o) { if (o.dataset.k === want) o.selected = true; });

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

  /* where this visit came from, saved on the first page they land on (later pages only show this site as the referrer) */
  var leadSource = (function () {
    var q = new URLSearchParams(location.search), src = '';
    if (q.get('utm_source')) src = [q.get('utm_source'), q.get('utm_medium'), q.get('utm_campaign')].filter(Boolean).join(' / ');
    else if (document.referrer) { try { var r = new URL(document.referrer); if (r.origin !== location.origin) src = r.hostname; } catch (e) {} }
    try {
      var saved = sessionStorage.getItem('lead_src');
      if (saved && !src) return saved;
      if (src || !saved) sessionStorage.setItem('lead_src', src || 'direct');
    } catch (e) {}
    return src || 'direct';
  })();

  /* forms: check required fields, then send (forms with data-endpoint) or just thank (the careers demo form) */
  var phoneOk = function (v) { var d = v.replace(/\D/g, '').replace(/^1(?=\d{10}$)/, ''); return d.length === 10; };
  $$('[data-form]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (form.dataset.sending) return;
      var bad = $$('[required]', form).filter(function (i) {
        var ok = i.value.trim() !== '' && i.checkValidity() && (i.name !== 'phone' || !form.dataset.endpoint || phoneOk(i.value));
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
          m.textContent = i.value.trim() === '' ? 'Required' : (i.type === 'email' ? 'Check this email address' : i.name === 'phone' ? 'Enter a 10-digit phone number' : 'Check this field');
          m.hidden = ok;
        }
        i.setAttribute('aria-invalid', String(!ok));
        return !ok;
      });
      if (bad.length) { bad[0].focus(); return; }
      var s = $('.submit', form), err = $('.form-err', form);
      var done = function () { $('.form-ok', form).hidden = false; if (s) s.hidden = true; };
      if (!form.dataset.endpoint) { done(); return; }

      var v = function (n) { var f = form.elements[n]; return f ? f.value.trim() : ''; };
      /* the portal takes one free-text message, so address, timing and referral ride along at its top */
      var extra = [['Address', v('address')], ['Timing', v('timing')], ['Heard about us', v('heard')]]
        .filter(function (p) { return p[1]; }).map(function (p) { return p[0] + ': ' + p[1]; });
      var body = {
        org: form.dataset.org, name: v('name'), email: v('email'), phone: v('phone'), service: v('service'),
        message: extra.concat(v('msg') ? [(extra.length ? '\n' : '') + v('msg')] : []).join('\n'), town: v('town'),
        page: location.pathname,
        source: leadSource,
        consent_text: ($('.consent', form) || {}).textContent || '',
        hp_fax2: v('hp_fax2'),
      };
      form.dataset.sending = '1';
      if (err) err.hidden = true;
      if (s) { s.disabled = true; s.dataset.label = s.textContent; s.textContent = 'Sending…'; }
      var fail = function (msg) {
        delete form.dataset.sending;
        if (s) { s.disabled = false; s.textContent = s.dataset.label; }
        if (err) { err.textContent = (msg || 'That didn’t go through.') + ' You can also call or text 802-PAINTER.'; err.hidden = false; }
      };
      fetch(form.dataset.endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
        .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, j: j }; }); })
        .then(function (res) { if (res.ok && res.j.ok) done(); else fail(res.j.error); })
        .catch(function () { fail('We couldn’t reach our server.'); });
    });
  });
})();

document.querySelectorAll('[data-detail-lens]').forEach(function (photo) {
  if (!window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;

  var image = photo.querySelector('img');
  var lens = document.createElement('span');
  lens.className = 'painting-lens';
  lens.setAttribute('aria-hidden', 'true');
  photo.appendChild(lens);
  var palette = document.createElement('span');
  palette.className = 'painting-palette';
  palette.setAttribute('aria-hidden', 'true');
  var swatches = Array.from({ length: 3 }, function () {
    var swatch = document.createElement('span');
    palette.appendChild(swatch);
    return swatch;
  });
  photo.appendChild(palette);
  var sample = document.createElement('canvas');
  sample.width = 7;
  sample.height = 7;
  var context = sample.getContext('2d', { willReadFrequently: true });
  var unavailable = false;

  function updatePalette(x, y, width, height, spread) {
    if (unavailable || !context) return;
    var radius = Math.max(3, Math.round(spread));
    context.imageSmoothingEnabled = false;
    context.clearRect(0, 0, 7, 7);
    // Draw the full source at the lens scale so responsive image density
    // cannot shift the sampled crop relative to the CSS background.
    var scale = 7 / (radius * 2);
    context.drawImage(image, 3.5 - x * scale, 3.5 - y * scale, width * scale, height * scale);
    try {
      var colors = context.getImageData(0, 0, 7, 7).data;
      var center = 24 * 4;
      function distance(offset) {
        return Math.hypot(colors[offset] - colors[center],
          colors[offset + 1] - colors[center + 1], colors[offset + 2] - colors[center + 2]);
      }
      // Keep swatches near the pointed-at color when the patch crosses an edge.
      var offsets = [center];
      [[22, 23, 17, 16], [26, 25, 31, 32]].forEach(function (neighbors) {
        var match = neighbors.map(function (pixel) { return pixel * 4; }).find(function (offset) {
          return colors[offset + 3] && distance(offset) <= 36;
        });
        offsets.push(match === undefined ? center : match);
      });
      swatches.forEach(function (swatch, i) {
        var offset = offsets[i];
        var hex = '#' + Array.from(colors.slice(offset, offset + 3), function (value) {
          return value.toString(16).padStart(2, '0');
        }).join('').toUpperCase();
        swatch.style.setProperty('--sample-color', hex);
        swatch.textContent = hex;
      });
      palette.classList.add('has-colors');
    } catch (error) {
      if (error.name !== 'SecurityError') throw error;
      unavailable = true;
    }
  }

  var pointer;
  var frame = 0;

  function hide() {
    pointer = null;
    photo.classList.remove('lens-active');
  }

  function render() {
    frame = 0;
    if (!pointer || !image.naturalWidth) return;
    var bounds = image.getBoundingClientRect();
    var container = photo.getBoundingClientRect();
    var x = pointer.clientX - bounds.left;
    var y = pointer.clientY - bounds.top;
    if (x < 0 || y < 0 || x >= bounds.width || y >= bounds.height) {
      hide();
      return;
    }

    var radius = lens.offsetWidth / 2;
    var centerX = Math.max(radius, Math.min(x, bounds.width - radius));
    var centerY = Math.max(radius, Math.min(y, bounds.height - radius));
    var cover = Math.max(bounds.width / image.naturalWidth, bounds.height / image.naturalHeight);
    var width = image.naturalWidth * cover;
    var height = image.naturalHeight * cover;
    var position = getComputedStyle(image).objectPosition.split(' ').map(parseFloat);
    var sourceX = centerX + (width - bounds.width) * position[0] / 100;
    var sourceY = centerY + (height - bounds.height) * position[1] / 100;
    var zoom = 1.65;

    lens.style.transform = 'translate3d(' + (bounds.left - container.left + centerX - radius) +
      'px, ' + (bounds.top - container.top + centerY - radius) + 'px, 0)';
    lens.style.backgroundImage = 'url("' + image.currentSrc + '")';
    lens.style.backgroundSize = width * zoom + 'px ' + height * zoom + 'px';
    lens.style.backgroundPosition = (radius - sourceX * zoom) + 'px ' + (radius - sourceY * zoom) + 'px';
    updatePalette(sourceX, sourceY, width, height, radius / zoom * .3);
    var paletteWidth = palette.offsetWidth;
    var paletteHeight = palette.offsetHeight;
    var paletteX = Math.max(0, Math.min(centerX - paletteWidth / 2, bounds.width - paletteWidth));
    var paletteY = centerY + radius + 8;
    if (paletteY + paletteHeight > bounds.height) paletteY = centerY - radius - paletteHeight - 8;
    palette.style.transform = 'translate3d(' + (bounds.left - container.left + paletteX) +
      'px, ' + (bounds.top - container.top + Math.max(0, paletteY)) + 'px, 0)';
    photo.classList.add('lens-active');
  }

  function scheduleRender() {
    if (pointer && !frame) frame = requestAnimationFrame(render);
  }

  photo.addEventListener('pointermove', function (event) {
    if (event.pointerType !== 'mouse' || event.target.closest('a')) {
      hide();
      return;
    }
    pointer = event;
    scheduleRender();
  });
  photo.addEventListener('pointerleave', hide);
  window.addEventListener('scroll', hide, { passive: true });
  image.addEventListener('load', scheduleRender);
  new ResizeObserver(scheduleRender).observe(image);
});

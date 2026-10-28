"""Builds the static pages for Demo 1.

Minimal and photo-led: four hero photographs carry the whole site (Sigma Phi,
the Queen Anne Victorian, the library, the porch), with type and white space
doing the rest. Run from the repo root:  python3 tools/build.py

Page copy lives in this file; project facts live in tools/projects.json and
before/after pairs in tools/transformations.json.

Hero video: drop a clip into assets/hero/ as <name>.mp4 (16:9) and/or
<name>-tall.mp4 (9:16), where <name> is sigma, victorian, library or porch,
then rerun this script. Until a clip exists the still is shown.
"""
import html
import json
import os

P = json.load(open('tools/projects.json'))
TF = json.load(open('tools/transformations.json'))

PHONE, TEL, EMAIL = '802-724-6837', '+18027246837', 'marketing@pwpvt.com'
IG, FB = 'https://www.instagram.com/paintingwithpurposevt/', 'https://www.facebook.com/PaintingWithPurposeVT'

MENU = [('index.html', 'Home'), ('work.html', 'Work'), ('transformations.html', 'Before & After'), ('services.html', 'Services'),
        ('purpose.html', 'Purpose'), ('careers.html', 'Careers'), ('contact.html', 'Contact')]
ORDER = ['project-sigma-phi-house.html', 'project-queen-anne-victorian.html', 'project-library.html',
         'project-built-ins-and-porch.html', 'project-lake-cottage.html', 'project-red-shingle-colonial.html',
         'project-dealership.html']
# the one frame that leads each project page
LEAD = {'project-sigma-phi-house.html': 'assets/hero/sigma-wide.jpg', 'project-queen-anne-victorian.html': 'assets/hero/victorian-wide.jpg',
        'project-library.html': 'assets/hero/library-wide.jpg', 'project-built-ins-and-porch.html': 'assets/img/pwp-1094.jpg',
        'project-lake-cottage.html': 'assets/img/pwp-0701.jpg', 'project-red-shingle-colonial.html': 'assets/img/pwp-0631.jpg',
        'project-dealership.html': 'assets/img/pwp-1337.jpg'}
POS = {'assets/img/pwp-0701.jpg': '40% 60%', 'assets/img/pwp-1337.jpg': '50% 40%', 'assets/img/pwp-1094.jpg': '50% 40%'}


def plain(s):
    return html.unescape(s)


def cur(h, current):
    return ' aria-current="page"' if h == current else ''


def img(src, alt, sizes='100vw', eager=False, cls=''):
    md = src.replace('.jpg', '-md.jpg')
    srcset = f' srcset="{md} 1100w, {src} 2400w" sizes="{sizes}"' if os.path.exists(md) else ''
    pos = f' style="object-position:{POS[src]}"' if src in POS else ''
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ''
    return f'<img{c} src="{src}"{srcset} alt="{alt}" {load} decoding="async"{pos}>'


def hero_media(name, alt, eager=False, tall_only=False):
    """One of the four hero photographs: a wide still with a tall crop for phones, plus the clip when it exists."""
    wide, tall = f'assets/hero/{name}-wide.jpg', f'assets/hero/{name}-tall.jpg'
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    if tall_only or not os.path.exists(wide):
        pic = f'<img src="{tall}" alt="{alt}" {load} decoding="async">'
    else:
        pic = (f'<picture><source media="(max-aspect-ratio: 4/5)" srcset="{tall}">'
               f'<img src="{wide}" alt="{alt}" {load} decoding="async"></picture>')
    vids = [v for v in (f'assets/hero/{name}.mp4', f'assets/hero/{name}-tall.mp4') if os.path.exists(v)]
    if vids:
        attrs = ' '.join(f'data-src{"-tall" if v.endswith("-tall.mp4") else ""}="{v}"' for v in vids)
        pic += f'<video class="clip" muted playsinline loop preload="none" aria-hidden="true" {attrs}></video>'
    return pic


def page(fn, title, desc, body, current=None, og='assets/hero/sigma-wide.jpg', over=False):
    menu = ''.join(f'<li><a href="{h}"{cur(h, current)}>{html.escape(t)}</a></li>' for h, t in MENU)
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#FAF8F4">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{og}">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500&family=Instrument+Serif&display=swap">
<link rel="stylesheet" href="assets/css/site.css">
</head>
<body{' class="over"' if over else ''}>
<a class="skip" href="#main">Skip to content</a>
<header class="hdr">
  <a class="logo" href="index.html" aria-label="Painting With Purpose, home"><img src="assets/logo.png" alt="Painting With Purpose" width="600" height="402"></a>
  <nav class="hdr-r" aria-label="Primary"><a class="hide-s" href="work.html"{cur("work.html", current)}>Work</a><a href="contact.html"{cur("contact.html", current)}>Free estimate</a><button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu">Menu</button></nav>
</header>
<div class="menu" id="menu" hidden>
  <ul class="menu-l">{menu}</ul>
  <div class="menu-r"><p>Greater Burlington, Vermont</p><p><a href="tel:{TEL}">802-PAINTER · {PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p><p><a href="{IG}" target="_blank" rel="noopener">Instagram</a> · <a href="{FB}" target="_blank" rel="noopener">Facebook</a></p></div>
</div>
<main id="main">
{body}
</main>
<footer class="ftr">
  <a class="ftr-logo" href="index.html"><img src="assets/logo.png" alt="Painting With Purpose" width="600" height="402" loading="lazy"></a>
  <p class="ftr-line">Good painting that does some good.</p>
  <ul class="ftr-links"><li><a href="work.html">Work</a></li><li><a href="transformations.html">Before &amp; After</a></li><li><a href="services.html">Services</a></li><li><a href="purpose.html">Purpose</a></li><li><a href="careers.html">Careers</a></li><li><a href="contact.html">Contact</a></li></ul>
  <ul class="ftr-links"><li><a href="tel:{TEL}">802-PAINTER</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="{IG}" target="_blank" rel="noopener">Instagram</a></li><li><a href="{FB}" target="_blank" rel="noopener">Facebook</a></li></ul>
  <p class="ftr-bot"><span>© 2026 Painting With Purpose · Greater Burlington, Vermont</span><span>A share of every job goes to CVOEO</span><span>Site by ArkiTech Solutions</span></p>
</footer>
<script src="assets/js/site.js"></script>
</body>
</html>
'''
    open(fn, 'w').write(doc)


def ending(line='Planning a project?'):
    return f'''<section class="ending rv">
  <h2>{line}</h2>
  <p><a class="tlink" href="contact.html">Request a free estimate</a> <span class="mute">or call</span> <a class="tlink" href="tel:{TEL}">802-PAINTER</a></p>
</section>'''


# ---------------------------------------------------------------- home: four screens
page('index.html', 'Painting With Purpose | House painters in Greater Burlington, Vermont',
     'Careful residential and commercial painting in Greater Burlington, Vermont. Part of every job helps end homelessness.',
     f'''<section class="h1-screen">
  <div class="h1-media">{hero_media('sigma', 'Sigma Phi House in Burlington: white Corinthian columns on a brick facade', eager=True)}</div>
  <div class="h1-in"><h1>Careful painting for Vermont homes and buildings.</h1></div>
  <span class="h1-cap">Sigma Phi House, Burlington</span>
</section>

<section class="statement">
  <p class="eyebrow rv">Painting With Purpose</p>
  <p class="big rv">A small painting company in Greater Burlington. We prepare every surface properly, leave a clean site each evening, and give part of every job to helping Vermonters find a home.</p>
</section>

<section class="reveal" data-reveal>
  <div class="reveal-pin">
    <p class="reveal-h eyebrow">Selected work</p>
    <figure class="reveal-fig">{hero_media('victorian', 'A restored Queen Anne Victorian with layered white porches')}</figure>
  </div>
</section>
<p class="reveal-cap"><span>Queen Anne restoration, Burlington</span><span class="links"><a class="tlink" href="work.html">View the work</a><a class="tlink" href="transformations.html">Before &amp; after</a></span></p>

<section class="inside">
  <div class="inside-media">{hero_media('library', 'A library atrium with timber ceilings, a stone wall and glass doors onto autumn trees')}</div>
  <div class="inside-items">
    <article><p class="eyebrow">01</p><h2>Interiors</h2><p>Walls, ceilings, trim and cabinets, finished to gallery standard.</p></article>
    <article><p class="eyebrow">02</p><h2>Commercial</h2><p>Libraries, storefronts and offices, scheduled so the doors stay open.</p></article>
    <article><p class="eyebrow">03</p><h2>Historic</h2><p>Victorians and pre-1978 homes, with certified lead-safe practice.</p><p><a class="tlink" href="services.html">All services</a></p></article>
  </div>
</section>

<section class="purpose-line">
  <p class="big rv">Part of every job goes to CVOEO, to help end homelessness in Vermont.</p>
  <p class="rv"><span class="mute">$15,000+ given so far.</span> <a class="tlink" href="purpose.html">Our purpose</a></p>
</section>

<section class="invite">
  <figure class="invite-media">{hero_media('porch', 'A freshly painted covered porch with a diamond inlay in the floor', tall_only=True)}</figure>
  <div class="invite-txt rv">
    <h2>Start a project.</h2>
    <p>We’ll walk it with you and send a written estimate, free.</p>
    <p class="invite-links"><a class="tlink" href="contact.html">Request an estimate</a><a href="tel:{TEL}">802-PAINTER · {PHONE}</a><a href="mailto:{EMAIL}">{EMAIL}</a></p>
  </div>
</section>''', over=True)


# ---------------------------------------------------------------- work: a quiet index, photos appear on hover
def peek_src(fn):
    md = LEAD[fn].replace('.jpg', '-md.jpg')
    return md if os.path.exists(md) else LEAD[fn]


rows = ''.join(
    f'<li><a class="prow" href="{fn}" data-peek="{peek_src(fn)}">'
    f'<span class="n">{i:02d}</span><span class="t">{P[fn]["title"]}</span><span class="k">{P[fn]["kind"].split(" · ")[-1]}</span><span class="l">{P[fn]["loc"]}</span></a></li>'
    for i, fn in enumerate(ORDER, 1))
page('work.html', 'Work | Painting With Purpose', 'Homes, storefronts and public buildings painted by Painting With Purpose.',
     f'''<section class="phead">
  <p class="eyebrow">Work</p>
  <h1>Homes, storefronts and public buildings.</h1>
</section>
<section class="pindex"><ul>{rows}</ul></section>
<div class="peek" aria-hidden="true"><img alt=""></div>
{ending()}''', 'work.html')

# ---------------------------------------------------------------- project pages: one photograph, then words
for i, fn in enumerate(ORDER):
    d = P[fn]
    facts = d['facts'].replace('<dt>', '<div><dt>').replace('</dd>', '</dd></div>') + '<div><dt>Photography</dt><dd>Gabe Dunn</dd></div>'
    nxt = ORDER[(i + 1) % len(ORDER)]
    body = f'''<section class="pj-hero">{img(LEAD[fn], plain(d['title']), eager=True)}</section>
<section class="pj-head">
  <p class="eyebrow">{d['kind']}</p>
  <h1>{d['title']}</h1>
  <p class="big">{d['lede']}</p>
</section>
<section class="pj-body">
  <div class="pj-text">{''.join(f'<p>{t}</p>' for t in d['text'])}</div>
  <div class="pj-side"><dl class="credits">{facts}</dl><p class="eyebrow">Palette</p><div class="palette">{d['palette']}</div></div>
</section>
<section class="pj-next"><p class="eyebrow">Next project</p><a href="{nxt}">{P[nxt]['title']} <span>→</span></a></section>'''
    page(fn, f'{plain(d["title"])} | Painting With Purpose', plain(d['lede']), body, 'work.html', og=LEAD[fn])

# ---------------------------------------------------------------- services: words only
SV = [('residential', 'Residential painting', 'Interiors and exteriors, from a single room to a full Victorian restoration: cabinets, trim, siding, porches and the repairs underneath them.'),
      ('commercial', 'Commercial painting', 'Storefronts, offices, multi-unit and public buildings, worked in phases and off-hours so your doors stay open.'),
      ('decks', 'Decks & porches', 'Cleaning, brightening, stripping where needed, and staining with products made for Vermont winters.'),
      ('lead', 'Lead-safe work', 'Certified Essential Maintenance Practices inspections for pre-1978 homes and rentals, with lead-safe repair when it’s needed.'),
      ('gutters', 'Gutter cleaning', 'Fall and spring cleanouts that keep water off your siding, away from your foundation, and off fresh paint.')]
svc_rows = ''.join(f'<li id="{k}" class="rv"><span class="n">{i:02d}</span><h2>{html.escape(n)}</h2><p>{t}</p></li>' for i, (k, n, t) in enumerate(SV, 1))
page('services.html', 'Services | Painting With Purpose',
     'Residential and commercial painting, deck staining, EMP lead inspections and gutter cleaning in Greater Burlington, Vermont.',
     f'''<section class="phead">
  <p class="eyebrow">Services</p>
  <h1>Five services, one standard.</h1>
</section>
<section class="svc"><ul>{svc_rows}</ul></section>
<section class="steps">
  <p class="eyebrow">How a job runs</p>
  <ol>
    <li class="rv"><h3>Walkthrough</h3><p>We visit, measure, talk through colors and surfaces, and note any repairs.</p></li>
    <li class="rv"><h3>Written estimate</h3><p>An itemized proposal with scope, products, schedule and price.</p></li>
    <li class="rv"><h3>Prep and paint</h3><p>Protection first, then careful prep, then paint. The site is cleaned every evening.</p></li>
    <li class="rv"><h3>Final walkthrough</h3><p>We review every surface together and touch up anything before we call it done.</p></li>
  </ol>
</section>
{ending()}''', 'services.html')

# ---------------------------------------------------------------- purpose: words only
page('purpose.html', 'Purpose | Painting With Purpose',
     'Part of every Painting With Purpose job funds CVOEO’s work to end homelessness in Vermont.',
     f'''<section class="phead">
  <p class="eyebrow">Purpose</p>
  <h1>We paint to help end homelessness in Vermont.</h1>
</section>
<section class="prose">
  <p class="big rv">Homelessness affects our whole community, and the solutions are few and far between.</p>
  <p class="rv">Part of what every client pays goes to CVOEO, the Champlain Valley Office of Economic Opportunity, and straight to helping people find a long-term, stable home. So far that is more than $15,000 and twelve people helped into secure housing, with the Joy &amp; Jerry Meyers Cup along the way. It adds nothing to your price.</p>
  <p class="rv">Brothers Gabe and Zach Dunn started Painting With Purpose to prove a painting company could be really good at the work and really good for the community. One of them is on nearly every job, and Gabe takes most of the photographs on this site.</p>
  <p class="rv"><a class="tlink" href="https://www.cvoeo.org/" target="_blank" rel="noopener">About CVOEO ↗</a></p>
</section>
<section class="quote rv">
  <blockquote>“Their mission for giving back to the homeless community is truly amazing.”</blockquote>
  <p class="eyebrow">Pam Mathe · Google review</p>
</section>
{ending()}''', 'purpose.html')

# ---------------------------------------------------------------- careers
FORMOK = '<p class="form-ok" hidden>Thanks. This demo form isn’t connected yet; on the live site it goes straight to the PWP inbox.</p>'
page('careers.html', 'Careers | Painting With Purpose', 'Painting jobs in Greater Burlington, Vermont, with paid training.',
     f'''<section class="phead">
  <p class="eyebrow">Careers</p>
  <h1>Paint with us.</h1>
  <p class="lede">We hire careful people and train them well: prep, cutting in, spraying, lead-safe practice, and how to treat a client’s home. Training is paid, crews are local, and interiors keep us working through the winter.</p>
</section>
<section class="roles">
  <ul><li><a href="#apply"><span class="t">Painter</span><span class="k">Full-time · year-round</span><span class="go">Apply →</span></a></li><li><a href="#apply"><span class="t">Crew lead</span><span class="k">Full-time · year-round</span><span class="go">Apply →</span></a></li><li><a href="#apply"><span class="t">Seasonal painter</span><span class="k">May to October</span><span class="go">Apply →</span></a></li></ul>
</section>
<section class="form-sec" id="apply">
  <h2>Apply</h2>
  <form class="form" data-form novalidate>
    <label class="field"><span>Name</span><input name="name" autocomplete="name" required></label>
    <label class="field"><span>Phone</span><input name="phone" type="tel" autocomplete="tel"></label>
    <label class="field"><span>Email</span><input name="email" type="email" autocomplete="email" required></label>
    <label class="field"><span>Role</span><select name="role"><option>Painter</option><option>Crew lead</option><option>Seasonal painter</option></select></label>
    <label class="field"><span>Experience</span><textarea name="exp" rows="3" placeholder="Years painting, certifications, anything else"></textarea></label>
    <button class="btn submit" type="submit">Send application</button>
    {FORMOK}
  </form>
</section>''', 'careers.html')

# ---------------------------------------------------------------- contact: the porch again, as the invitation
towns = ['Burlington', 'South Burlington', 'Winooski', 'Colchester', 'Essex', 'Williston', 'Shelburne', 'Richmond', 'Hinesburg', 'Charlotte']
page('contact.html', 'Contact | Painting With Purpose', 'Request a free painting estimate in Greater Burlington, Vermont.',
     f'''<section class="contact">
  <figure class="contact-media">{hero_media('porch', 'A freshly painted covered porch', eager=True, tall_only=True)}</figure>
  <div class="contact-txt">
    <p class="eyebrow">Free estimate</p>
    <h1>Tell us about your project.</h1>
    <p class="lede">Call or text <a class="tlink" href="tel:{TEL}">802-PAINTER</a>, email <a class="tlink" href="mailto:{EMAIL}">{EMAIL}</a>, or use the form. We work across {", ".join(towns[:-1])} and {towns[-1]}.</p>
    <form class="form" data-form novalidate>
      <label class="field"><span>Name</span><input name="name" autocomplete="name" required></label>
      <label class="field"><span>Email</span><input name="email" type="email" autocomplete="email" required></label>
      <label class="field"><span>Phone</span><input name="phone" type="tel" autocomplete="tel"></label>
      <label class="field"><span>Service</span><select name="service">{"".join(f"<option>{html.escape(n)}</option>" for _, n, _ in SV)}</select></label>
      <label class="field"><span>Town</span><select name="town">{"".join(f"<option>{t}</option>" for t in towns)}<option>Other</option></select></label>
      <label class="field"><span>Project</span><textarea name="msg" rows="3" placeholder="Rooms, surfaces, timing, anything we should know"></textarea></label>
      <button class="btn submit" type="submit">Request my estimate</button>
      {FORMOK}
    </form>
  </div>
</section>''', 'contact.html', og='assets/hero/porch-tall.jpg')


# ---------------------------------------------------------------- before & after: the one place with many photos
def ba_frame(t):
    if t['dip']:  # different angles: show the two frames side by side instead of a slider
        return (f'<div class="ba-frame ba-dip"><img src="assets/ba/{t["id"]}-before.jpg" alt="{t["title"]}, before" loading="lazy" decoding="async">'
                f'<img src="assets/ba/{t["id"]}-after.jpg" alt="{t["title"]}, after" loading="lazy" decoding="async"></div>')
    return f'''<div class="ba-frame" style="--p:50%">
    <img src="assets/ba/{t["id"]}-before.jpg" alt="{t["title"]}, before" loading="lazy" decoding="async">
    <img class="ba-after" src="assets/ba/{t["id"]}-after.jpg" alt="{t["title"]}, after" loading="lazy" decoding="async">
    <span class="ba-tag b">Before</span><span class="ba-tag a">After</span>
    <span class="ba-line" aria-hidden="true"></span>
    <input class="ba-range" type="range" min="0" max="100" value="50" aria-label="Compare before and after: {t["title"]}">
  </div>'''


tiles = ''.join(f'<figure class="ba rv">{ba_frame(t)}<figcaption><span>{t["title"]}</span><span>{t["note"]}</span></figcaption></figure>' for t in TF)
page('transformations.html', 'Before & After | Painting With Purpose', 'Before and after photos from real Painting With Purpose jobs.',
     f'''<section class="phead">
  <p class="eyebrow">Before &amp; after</p>
  <h1>Same house, same angle.</h1>
  <p class="lede">Drag across any photograph to compare the first day of the job with the last.</p>
</section>
<section class="ba-grid">{tiles}</section>
{ending()}''', 'transformations.html')
print('built')

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

PHONE, TEL, EMAIL = '802-724-6837', '+18027246837', 'office@pwpvt.com'
ADDRESS = '133 Elm Street, Office B, Winooski, Vermont'
IG, FB = 'https://www.instagram.com/paintingwithpurposevt/', 'https://www.facebook.com/PaintingWithPurposeVT'

MENU = [('index.html', 'Home'), ('work.html', 'Work'), ('transformations.html', 'Before & after'), ('services.html', 'Services'),
        ('purpose.html', 'Purpose'), ('careers.html', 'Careers'), ('contact.html', 'Contact')]
ORDER = ['project-sigma-phi-house.html', 'project-queen-anne-victorian.html', 'project-library.html',
         'project-built-ins-and-porch.html', 'project-lake-cottage.html', 'project-red-shingle-colonial.html',
         'project-dealership.html']
# the one frame that leads each project page
LEAD = {'project-sigma-phi-house.html': 'assets/hero/sigma-wide.jpg', 'project-queen-anne-victorian.html': 'assets/hero/victorian-wide.jpg',
        'project-library.html': 'assets/hero/library-wide.jpg', 'project-built-ins-and-porch.html': 'assets/img/pwp-1094.jpg',
        'project-lake-cottage.html': 'assets/img/pwp-0701.jpg', 'project-red-shingle-colonial.html': 'assets/img/pwp-0631.jpg',
        'project-dealership.html': 'assets/img/pwp-1337.jpg'}
MORE = {'project-sigma-phi-house.html': 'assets/img/pwp-0179-door.jpg', 'project-queen-anne-victorian.html': 'assets/img/pwp-0058-gable.jpg',
        'project-library.html': 'assets/img/pwp-0856.jpg', 'project-built-ins-and-porch.html': 'assets/img/pwp-1094-shelves.jpg',
        'project-lake-cottage.html': 'assets/img/pwp-0686.jpg', 'project-red-shingle-colonial.html': 'assets/img/pwp-0631-windows.jpg'}
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


WC = {'mountains': (364, 286), 'church': (429, 222), 'leaves': (231, 220), 'brush': (133, 207), 'can': (183, 208), 'ladder': (158, 222)}


def wc(name):
    """A small Vermont watercolour, used sparingly as an accent on cream (never over photos)."""
    w, h = WC[name]
    return f'<img class="wc wc-{name}" src="assets/wc/{name}.webp" alt="" aria-hidden="true" width="{w}" height="{h}" loading="lazy" decoding="async">'


def hero_media(name, alt, eager=False, tall_only=False, clip=True):
    """One of the four hero photographs: a wide still with a tall crop for phones, plus its silent clip when it exists
    (each clip is used once on the site: Sigma on home, Victorian and Library on their project pages, Porch on contact)."""
    wide, tall = f'assets/hero/{name}-wide.jpg', f'assets/hero/{name}-tall.jpg'
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    if tall_only or not os.path.exists(wide):
        pic = f'<img src="{tall}" alt="{alt}" {load} decoding="async">'
    else:
        pic = (f'<picture><source media="(max-aspect-ratio: 4/5)" srcset="{tall}">'
               f'<img src="{wide}" alt="{alt}" {load} decoding="async"></picture>')
    kinds = (('', f'assets/hero/{name}.mp4'), ('-sm', f'assets/hero/{name}-720.mp4'), ('-tall', f'assets/hero/{name}-tall.mp4'))
    vids = [(k, v) for k, v in kinds if clip and os.path.exists(v)]
    if vids:
        attrs = ' '.join(f'data-src{k}="{v}"' for k, v in vids)
        pic += f'<video class="clip" muted playsinline preload="{"auto" if eager else "none"}" aria-hidden="true" {attrs}></video>'
    return pic


SITE = 'https://paintingwithpurpose01.vercel.app'


def page(fn, title, desc, body, current=None, og='assets/og.jpg', over=False):
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
<meta property="og:image" content="{SITE}/{og}">
<meta property="og:url" content="{SITE}/{fn}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Painting With Purpose">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{SITE}/{fn}">
<link rel="icon" href="assets/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500&family=Instrument+Serif&display=swap">
<link rel="stylesheet" href="assets/css/site.css">
</head>
<body{' class="over"' if over else ''}>
<a class="skip" href="#main">Skip to content</a>
<header class="hdr">
  <a class="logo" href="index.html" aria-label="Painting With Purpose, home"><img class="logo-n" src="assets/logo-navy-180.png" srcset="assets/logo-navy-360.png 2x" alt="Painting With Purpose" width="180" height="116"><img class="logo-w" src="assets/logo-white-180.png" srcset="assets/logo-white-360.png 2x" alt="" width="180" height="116"></a>
  <nav class="hdr-r" aria-label="Primary"><a class="hide-s" href="work.html"{cur("work.html", current)}>Work</a><a href="contact.html"{cur("contact.html", current)}>Contact</a><button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu">Menu</button></nav>
</header>
<div class="menu" id="menu" hidden>
  <ul class="menu-l">{menu}</ul>
  <div class="menu-r"><p>Greater Burlington, Vermont</p><p><a href="tel:{TEL}">802-PAINTER · {PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p><p><a href="{IG}" target="_blank" rel="noopener">Instagram</a> · <a href="{FB}" target="_blank" rel="noopener">Facebook</a></p></div>
</div>
<main id="main">
{body}
</main>
<footer class="ftr">
  <div class="ftr-brand"><a class="ftr-logo" href="index.html"><img src="assets/logo-navy-360.png" alt="Painting With Purpose" width="360" height="232" loading="lazy"></a><p>Greater Burlington, Vermont</p><p class="mute">Good painting that does some good.</p>{wc("mountains")}</div>
  <ul class="ftr-links"><li><a href="tel:{TEL}">802-PAINTER</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="{IG}" target="_blank" rel="noopener">@paintingwithpurposevt</a></li><li class="mute">{ADDRESS}</li></ul>
  <ul class="ftr-links"><li><a href="work.html">Work</a></li><li><a href="transformations.html">Before &amp; after</a></li><li><a href="services.html">Services</a></li><li><a href="purpose.html">Purpose</a></li><li><a href="careers.html">Careers</a></li><li><a href="contact.html">Contact</a></li></ul>
  <p class="ftr-bot"><span>© 2026 Painting With Purpose LLC</span><span>Part of every job goes to CVOEO.</span><span>Site by ArkiTech Solutions</span></p>
</footer>
<script src="assets/js/site.js"></script>
</body>
</html>
'''
    open(fn, 'w').write(doc)


# ---------------------------------------------------------------- home: four screens
page('index.html', 'Painting With Purpose · House painters in Greater Burlington, Vermont',
     'Residential and commercial painting in Greater Burlington, Vermont. Part of every job helps end homelessness in Vermont.',
     f'''<section class="h1-screen" data-dark>
  <div class="h1-media">{hero_media('sigma', 'Sigma Phi House in Burlington, white Corinthian columns against red brick', eager=True)}</div>
  <div class="h1-in"><h1 class="sr">Painting With Purpose: house and commercial painters in Greater Burlington, Vermont</h1><p class="beat" aria-hidden="true">Whether it’s a frat house on the hill,</p></div>
  <a class="cap" href="project-sigma-phi-house.html">Sigma Phi House · Burlington →</a>
  <span class="h1-cue" aria-hidden="true"></span>
</section>

<section class="reveal" data-dark>
  <div class="reveal-pin">
    <figure class="reveal-fig">{hero_media('victorian', 'A restored Queen Anne Victorian with layered white porches', clip=False)}</figure>
    <p class="beat reveal-beat" aria-hidden="true">a Victorian on a quiet street,</p>
    <a class="cap" href="project-queen-anne-victorian.html">Queen Anne Victorian · Burlington →</a>
  </div>
</section>

<section class="inside">
  <div class="inside-media" data-dark>{hero_media('library', 'A library atrium with timber ceilings, a stone wall and glass doors onto fall trees', clip=False)}<p class="beat inside-beat" aria-hidden="true">a library in the middle of town,</p></div>
  <div class="inside-items">
    <p class="eyebrow">What we paint</p>
    <ul class="inside-list">
      <li><h2>Homes</h2><p>Interiors, exteriors, cabinets and trim.</p></li>
      <li><h2>Commercial</h2><p>Phased around your hours.</p></li>
      <li><h2>Older houses</h2><p>EPA lead certified.</p></li>
    </ul>
    <p><a class="tlink" href="services.html">All services</a></p>
    {wc('leaves')}
  </div>
</section>

<section class="invite">
  <figure class="invite-media" data-dark>{hero_media('porch', 'A freshly painted covered porch with a diamond pattern in the floor', tall_only=True, clip=False)}</figure>
  <div class="invite-txt">
    <p class="invite-beat">or the porch you come home to,</p>
    <h2>we paint with purpose.</h2>
    <p>A Greater Burlington painting company. Careful prep, a clean site at the end of every day, and a free written estimate.</p>
    <p class="invite-links"><a class="tlink" href="contact.html">Request an estimate</a><a href="tel:{TEL}">802-PAINTER</a></p>
    <p class="invite-give">Part of every job goes to CVOEO to help Vermonters move from shelter into a home. More than $15,000 so far. <a class="tlink" href="purpose.html">Our purpose</a></p>
  </div>
</section>''', over=True)


# ---------------------------------------------------------------- work: a quiet index, photos appear on hover
def POSATTR(fn):
    return f' style="object-position:{POS[LEAD[fn]]}"' if LEAD[fn] in POS else ''


def peek_src(fn):
    md = LEAD[fn].replace('.jpg', '-md.jpg')
    return md if os.path.exists(md) else LEAD[fn]


rows = ''.join(
    f'<li><a class="prow" href="{fn}" data-peek="{peek_src(fn)}">'
    f'<img class="prow-img" src="{peek_src(fn)}" alt="" loading="lazy" decoding="async"{POSATTR(fn)}>'
    f'<span class="n">{i:02d}</span><span class="t">{P[fn]["title"]}</span><span class="k">{P[fn]["kind"].split(" · ")[-1]}</span><span class="l">{P[fn]["loc"]}</span></a></li>'
    for i, fn in enumerate(ORDER, 1))
page('work.html', 'Work · Painting With Purpose', 'Homes, halls and storefronts painted by Painting With Purpose across Greater Burlington.',
     f'''<section class="phead">
  <p class="eyebrow">Work</p>
  <h1>Homes, halls and storefronts.</h1>
  {wc('brush')}
</section>
<section class="pindex"><ul>{rows}</ul></section>
<div class="peek" aria-hidden="true"><img alt=""></div>''', 'work.html')

# ---------------------------------------------------------------- project pages: one photograph, then words
for i, fn in enumerate(ORDER):
    d = P[fn]
    facts = d['facts'].replace('<dt>', '<div><dt>').replace('</dd>', '</dd></div>') + '<div><dt>Photography</dt><dd>Gabe Dunn</dd></div>'
    nxt = ORDER[(i + 1) % len(ORDER)]
    slot = LEAD[fn].split('/')[-1].replace('-wide.jpg', '') if LEAD[fn].startswith('assets/hero/') else None
    hero = hero_media(slot, plain(d['title']), eager=True, clip=slot != 'sigma') if slot else img(LEAD[fn], plain(d['title']), eager=True)
    more = f'<figure class="pj-more">{img(MORE[fn], plain(d["title"]) + ", detail", sizes="(max-width: 760px) 100vw, 70vw")}</figure>\n' if fn in MORE else ''
    body = f'''<section class="pj-hero">{hero}</section>
<section class="pj-head">
  <p class="eyebrow">{d['kind']}</p>
  <h1>{d['title']}</h1>
  <p class="big">{d['lede']}</p>
</section>
<section class="pj-body">
  <div class="pj-text">{''.join(f'<p>{t}</p>' for t in d['text'])}</div>
  <div class="pj-side"><dl class="credits">{facts}</dl><p class="eyebrow">Palette</p><div class="palette">{d['palette']}</div></div>
</section>
{more}<section class="pj-next"><p class="eyebrow">Next project</p><a href="{nxt}">{P[nxt]['title']} <span>→</span></a></section>'''
    page(fn, f'{plain(d["title"])} · Painting With Purpose', plain(d['lede']), body, 'work.html', og=LEAD[fn])

# ---------------------------------------------------------------- services: words only
SV = [('residential', 'Residential painting', 'Interiors and exteriors, from one room to a whole house. Siding, trim, doors, cabinets and porches, with rot repair when the wood needs it first.'),
      ('commercial', 'Commercial painting', 'Offices, storefronts, multi-unit and public buildings, inside and out. Phased around your hours, with crews experienced on lifts.'),
      ('decks', 'Decks & porches', 'Washing, sanding, repair and stain or paint for wood, composite and metal decks.'),
      ('lead', 'EMP lead inspections', 'Essential Maintenance Practices inspections for owners and property managers. We are EPA lead certified, so older homes are handled safely from the first scrape.'),
      ('gutters', 'Gutter cleaning', 'Spring and fall cleanouts, so water keeps moving through a Vermont winter.')]
svc_rows = ''.join(f'<li id="{k}"><span class="n">{i:02d}</span><h2>{html.escape(n)}</h2><p>{t}</p></li>' for i, (k, n, t) in enumerate(SV, 1))
page('services.html', 'Services · Painting With Purpose',
     'Residential and commercial painting, deck staining, EMP lead inspections and gutter cleaning in northern Vermont.',
     f'''<section class="phead">
  <p class="eyebrow">Services</p>
  <h1>Five services, one standard.</h1>
</section>
<figure class="page-photo">{img('assets/img/pwp-0631-painter.jpg', 'A painter on a ladder at a red shingle colonial', eager=True)}</figure>
<section class="svc"><ul>{svc_rows}</ul></section>
<section class="steps">
  <p class="eyebrow">How a job runs</p>
  {wc('can')}
  <ol>
    <li><h3>Walkthrough</h3><p>We visit, measure and talk through colors, surfaces and repairs.</p></li>
    <li><h3>Written estimate</h3><p>Scope, schedule and price, in writing and free.</p></li>
    <li><h3>Prep and paint</h3><p>Protection first, then prep, then paint. The site is cleaned at the end of every day.</p></li>
    <li><h3>Final walkthrough</h3><p>We go over the finished job with you before we call it done.</p></li>
  </ol>
  <p class="area">Addison, Chittenden, Franklin, Grand Isle, Lamoille, Orange and Washington counties.</p>
</section>''', 'services.html')

# ---------------------------------------------------------------- purpose: words only
page('purpose.html', 'Purpose · Painting With Purpose',
     'Part of every job goes to CVOEO to help Vermonters move from shelter into a home. $15,000 and counting.',
     f'''<section class="phead">
  <p class="eyebrow">Purpose</p>
  <h1>We paint to help end homelessness in Vermont.</h1>
</section>
<figure class="page-photo">{img('assets/img/pwp-1247.jpg', 'The Painting With Purpose booth at a street fair in a Vermont town', eager=True)}</figure>
<section class="prose">
  <p class="big">Homelessness touches the whole community, and the answers are few. We wanted our work to be one of them.</p>
  <p>Part of the profit from every job goes to CVOEO, the Champlain Valley Office of Economic Opportunity. It helps people in shelters move into permanent housing by covering security deposits, a first month’s rent and utilities. So far that is more than $15,000, and more than a dozen people in secure homes. It adds nothing to your price.</p>
  <p>Zach and Gabe Dunn started Painting With Purpose in 2022 to show that a painting company could be very good at the work and good for the place it works. The business plan took first place at the Joy and Jerry Meyers Cup at UVM. More than a hundred jobs later, the idea is the same.</p>
  <p><a class="tlink" href="https://www.cvoeo.org/" target="_blank" rel="noopener">About CVOEO ↗</a></p>
</section>
<figure class="wc-band">{wc('church')}</figure>
<section class="quote">
  <blockquote>“Their mission for giving back to the homeless community is truly amazing.”</blockquote>
  <p class="eyebrow">Pam Mathe · Google review</p>
</section>''', 'purpose.html')

# ---------------------------------------------------------------- careers
FORMOK = '<p class="form-ok" role="status" hidden>Thanks. This demo form isn’t connected yet. On the live site it goes straight to the PWP inbox.</p>'
page('careers.html', 'Careers · Painting With Purpose', 'Painter jobs in Greater Burlington. $18 to $30 an hour, paid lunch and room to grow.',
     f'''<section class="phead">
  <p class="eyebrow">Careers</p>
  <h1>Paint with us.</h1>
  {wc('ladder')}
  <p class="lede">We hire people who show up, care about the details and treat every home like their own. Experience helps. We teach the rest.</p>
  <ul class="perks">
    <li>$18 to $30 an hour, based on experience</li>
    <li>Paid lunch, paid uniforms, paid drives over 30 minutes</li>
    <li>Short and long term disability, and life insurance</li>
    <li>Flexible scheduling and vacation</li>
    <li>Room to grow into a lead role</li>
  </ul>
</section>
<figure class="page-photo">{img('assets/img/crew-three.jpg', 'Three Painting With Purpose painters on a job, with ladders and drop cloths', eager=True)}</figure>
<section class="roles">
  <ul><li><a href="#apply"><span class="t">Painter</span><span class="k">Full-time · Greater Burlington</span><span class="go">Apply →</span></a></li></ul>
</section>
<section class="form-sec" id="apply">
  <h2>Apply</h2>
  <form class="form" data-form novalidate>
    <label class="field"><span>Name</span><input name="name" autocomplete="name" required></label>
    <label class="field"><span>Phone</span><input name="phone" type="tel" autocomplete="tel"></label>
    <label class="field"><span>Email</span><input name="email" type="email" autocomplete="email" required></label>
    <label class="field"><span>Town you live in</span><input name="town" autocomplete="address-level2"></label>
    <label class="field"><span>Role</span><select name="role"><option>Painter</option></select></label>
    <label class="field"><span>Experience</span><textarea name="exp" rows="3" placeholder="Where you’ve painted, for how long, and anything else we should know"></textarea></label>
    <button class="btn submit" type="submit">Send application</button>
    {FORMOK}
  </form>
</section>''', 'careers.html')

# ---------------------------------------------------------------- contact: the porch again, as the invitation
CONTACT_SERVICES = ['Residential painting', 'Commercial painting', 'Decks & porches', 'EMP lead inspection', 'Gutter cleaning', 'Not sure yet']
towns = ['Burlington', 'South Burlington', 'Winooski', 'Colchester', 'Essex', 'Williston', 'Shelburne', 'Richmond', 'Hinesburg', 'Charlotte']
page('contact.html', 'Free estimate · Painting With Purpose', 'Tell us about your project. Call 802-PAINTER or send a note for a free written estimate.',
     f'''<section class="contact">
  <figure class="contact-media">{hero_media('porch', 'A freshly painted covered porch', eager=True, tall_only=True)}</figure>
  <div class="contact-txt">
    <p class="eyebrow">Free estimate</p>
    <h1>Tell us about your project.</h1>
    <p class="lede">Call or text <a class="tlink" href="tel:{TEL}">802-PAINTER</a>, email <a class="tlink" href="mailto:{EMAIL}">{EMAIL}</a>, or use the form. We work across Chittenden County and the counties around it.</p>
    <p class="addr">133 Elm Street, Office B, Winooski · 8:00 to 5:00 daily · <a href="{IG}" target="_blank" rel="noopener">@paintingwithpurposevt</a></p>
    <form class="form" data-form novalidate>
      <label class="field"><span>Name</span><input name="name" autocomplete="name" required></label>
      <label class="field"><span>Email</span><input name="email" type="email" autocomplete="email" required></label>
      <label class="field"><span>Phone</span><input name="phone" type="tel" autocomplete="tel"></label>
      <label class="field"><span>Service</span><select name="service">{"".join(f"<option>{html.escape(n)}</option>" for n in CONTACT_SERVICES)}</select></label>
      <label class="field"><span>Town</span><select name="town">{"".join(f"<option>{t}</option>" for t in towns)}<option>Other</option></select></label>
      <label class="field"><span>Project</span><textarea name="msg" rows="3" placeholder="Rooms or surfaces, timing, budget if you have one"></textarea></label>
      <button class="btn submit" type="submit">Request my estimate</button>
      {FORMOK}
    </form>
  </div>
</section>''', 'contact.html', og='assets/hero/porch-tall.jpg')


# ---------------------------------------------------------------- before & after: the one place with many photos
BASZ = '(max-width: 760px) 46vw, (max-width: 1024px) 46vw, 30vw'


def ba_frame(t):
    if t['dip']:  # different angles: show the two frames side by side instead of a slider
        return (f'<div class="ba-frame ba-dip"><img src="assets/ba/{t["id"]}-before.jpg" srcset="assets/ba/{t["id"]}-before-th.jpg 480w, assets/ba/{t["id"]}-before.jpg 1024w" sizes="{BASZ}" alt="{t["title"]}, before" loading="lazy" decoding="async">'
                f'<img src="assets/ba/{t["id"]}-after.jpg" srcset="assets/ba/{t["id"]}-after-th.jpg 480w, assets/ba/{t["id"]}-after.jpg 1024w" sizes="{BASZ}" alt="{t["title"]}, after" loading="lazy" decoding="async"></div>')
    return f'''<div class="ba-frame" style="--p:50%">
    <img src="assets/ba/{t["id"]}-before.jpg" srcset="assets/ba/{t["id"]}-before-th.jpg 480w, assets/ba/{t["id"]}-before.jpg 1024w" sizes="{BASZ}" alt="{t["title"]}, before" loading="lazy" decoding="async">
    <img class="ba-after" src="assets/ba/{t["id"]}-after.jpg" srcset="assets/ba/{t["id"]}-after-th.jpg 480w, assets/ba/{t["id"]}-after.jpg 1024w" sizes="{BASZ}" alt="{t["title"]}, after" loading="lazy" decoding="async">
    <span class="ba-tag b">Before</span><span class="ba-tag a">After</span>
    <span class="ba-line" aria-hidden="true"></span>
    <input class="ba-range" type="range" min="0" max="100" value="50" aria-label="Compare before and after: {t["title"]}">
  </div>'''


FIRST = ['ext-07', 'ext-04', 'deck-04', 'int-02', 'com-02', 'ext-06', 'deck-02', 'ext-01', 'int-04']
TFO = [t for i in FIRST for t in TF if t['id'] == i] + [t for t in TF if t['id'] not in FIRST]
tiles = ''.join(f'<figure class="ba"{" data-more hidden" if k >= len(FIRST) else ""}>{ba_frame(t)}<figcaption><span>{t["title"]}</span><span>{t["note"]}</span></figcaption></figure>' for k, t in enumerate(TFO))
page('transformations.html', 'Before & after · Painting With Purpose', 'The first day and the last day of twenty Vermont painting projects.',
     f'''<section class="phead">
  <p class="eyebrow">Before &amp; after</p>
  <h1>Same house, same angle.</h1>
  <p class="lede">Drag across any photo to compare the first day with the last.</p>
</section>
<section class="ba-grid">{tiles}</section>
<p class="ba-all"><button class="tlink" type="button" data-show-more>Show all {len(TF)}</button></p>''', 'transformations.html')
# ---------------------------------------------------------------- 404 (Vercel serves 404.html for missing paths)
page('404.html', 'Page not found · Painting With Purpose', 'This page could not be found.',
     '''<section class="phead nf">
  <p class="eyebrow">404</p>
  <h1>This page isn’t here.</h1>
  <p class="lede">The link may be old, or the page may have moved.</p>
  <p class="nf-links"><a class="tlink" href="index.html">Home</a><a class="tlink" href="work.html">Work</a><a class="tlink" href="contact.html">Contact</a></p>
</section>''')
# the 404 can be served at any depth, so its links start from the site root
nf = open('404.html').read()
for attr in ('href="', 'src="', 'srcset="'):
    nf = nf.replace(attr + 'assets/', attr + '/assets/')
import re
nf = re.sub(r'href="([a-z0-9-]+\.html)', r'href="/\1', nf)
open('404.html', 'w').write(nf)
print('built')

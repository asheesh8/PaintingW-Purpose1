"""Builds the static pages for Demo 1.

Photo-led, with the Vermont watercolors painted in behind the content.
Run from the repo root:  python3 tools/build.py
Page copy lives in this file; project facts live in tools/projects.json and
before/after pairs in tools/transformations.json.
"""
import html
import json
import os

P = json.load(open('tools/projects.json'))
TF = json.load(open('tools/transformations.json'))

PHONE, TEL, EMAIL = '802-724-6837', '+18027246837', 'marketing@pwpvt.com'
IG, FB = 'https://www.instagram.com/paintingwithpurposevt/', 'https://www.facebook.com/PaintingWithPurposeVT'

NAV = [('work.html', 'Work'), ('transformations.html', 'Before & After'), ('services.html', 'Services'),
       ('purpose.html', 'Purpose'), ('careers.html', 'Careers')]
SERVICES = [('residential', 'Residential'), ('commercial', 'Commercial'), ('decks', 'Decks & Porches'),
            ('lead', 'Lead-Safe Work'), ('gutters', 'Gutter Cleaning')]

ORDER = ['project-sigma-phi-house.html', 'project-queen-anne-victorian.html', 'project-lake-cottage.html',
         'project-library.html', 'project-red-shingle-colonial.html', 'project-built-ins-and-porch.html',
         'project-dealership.html']
LEAD = {'project-lake-cottage.html': 'assets/img/pwp-0695.jpg', 'project-built-ins-and-porch.html': 'assets/img/pwp-1371.jpg',
        'project-library.html': 'assets/img/pwp-0995.jpg'}
POS = {'assets/img/pwp-0179.jpg': '50% 62%', 'assets/img/pwp-0058.jpg': '72% 40%', 'assets/img/pwp-0701.jpg': '40% 60%',
       'assets/img/pwp-0686.jpg': '50% 30%', 'assets/img/pwp-1247.jpg': '78% 50%', 'assets/img/pwp-1337.jpg': '50% 40%',
       'assets/img/pwp-1371.jpg': '50% 62%', 'assets/img/pwp-0995.jpg': '50% 55%'}
# the watercolor that sits behind each project
ART = {'project-sigma-phi-house.html': 'vermont-church-village', 'project-queen-anne-victorian.html': 'white-vermont-farmhouse',
       'project-lake-cottage.html': 'lake-champlain-sailboats', 'project-library.html': 'sunny-living-room',
       'project-red-shingle-colonial.html': 'red-barn-fall', 'project-built-ins-and-porch.html': 'white-clapboard-porch',
       'project-dealership.html': 'wooden-clapboard-lantern'}
# project photo sequence: each group opens with a numbered note; 'full' is one wide frame, 'pair' two tall frames
GROUPS = {
    'project-sigma-phi-house.html': [[('full', 'pwp-0179-pediment')], [('full', 'pwp-0179-door')]],
    'project-queen-anne-victorian.html': [[('full', 'pwp-0058-gable')], [('full', 'pwp-0058-porch')]],
    'project-lake-cottage.html': [[('full', 'pwp-0686'), ('full', 'pwp-0701')], [('full', 'pwp-0686-porch')]],
    'project-library.html': [[('full', 'pwp-0856')], [('pair', 'pwp-0951', 'pwp-0735')]],
    'project-red-shingle-colonial.html': [[('full', 'pwp-0631-windows')], [('pair', 'pwp-0631-painter', 'pwp-0631-windows')]],
    'project-built-ins-and-porch.html': [[('pair', 'pwp-1094', 'pwp-1371')], [('full', 'pwp-1094-shelves')]],
    'project-dealership.html': [[('full', 'pwp-1337')], [('full', 'pwp-1343')]],
}


def img(src, alt, sizes='100vw', eager=False, cls=''):
    md = src.replace('.jpg', '-md.jpg')
    srcset = f' srcset="{md} 1100w, {src} 2400w" sizes="{sizes}"' if os.path.exists(md) else ''
    pos = f' style="object-position:{POS[src]}"' if src in POS else ''
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ''
    return f'<img{c} src="{src}"{srcset} alt="{alt}" {load} decoding="async"{pos}>'


def art(name, cls):
    """A watercolor painted in behind the content (decorative)."""
    src = 'assets/art/w01-hero-panorama.jpg' if name == 'panorama' else f'assets/art/wc/{name}.jpg'
    return f'<img class="wc {cls}" src="{src}" alt="" aria-hidden="true" decoding="async">'


def plain(s):
    return html.unescape(s)


def lead(fn):
    return LEAD.get(fn, P[fn]['hero'])


def cur(h, current):
    return ' aria-current="page"' if h == current else ''


def page(fn, title, desc, body, current=None, og='assets/img/pwp-0179.jpg'):
    nav = ''.join(f'<a href="{h}"{cur(h, current)}>{html.escape(t)}</a>' for h, t in NAV)
    big = ''.join(f'<li><a href="services.html#{k}">{html.escape(t)}</a></li>' for k, t in SERVICES)
    small = ''.join(f'<li><a href="{h}"{cur(h, current)}>{html.escape(t)}</a></li>' for h, t in [('index.html', 'Home')] + NAV + [('contact.html', 'Contact')])
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#FBF8F3">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{og}">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500&family=Instrument+Serif:ital@0;1&display=swap">
<link rel="stylesheet" href="assets/css/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="hdr">
  <a class="logo" href="index.html" aria-label="Painting With Purpose, home"><img src="assets/logo.png" alt="Painting With Purpose" width="600" height="402"></a>
  <nav class="nav" aria-label="Primary">{nav}</nav>
  <div class="hdr-r"><a class="est" href="contact.html"{cur("contact.html", current)}>Free estimate</a><button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu">Menu</button></div>
  <nav class="menu" id="menu" aria-label="Menu">
    <ul class="menu-big">{big}</ul>
    <ul class="menu-small">{small}</ul>
    <div class="menu-est"><a href="contact.html">Free estimate →</a><a href="tel:{TEL}">802-PAINTER · {PHONE}</a>{art('lake-champlain-sailboats', 'wc-menu')}</div>
  </nav>
</header>
<main id="main">
{body}
</main>
<footer class="ftr">
  {art('misty-green-mountains', 'wc-ftr')}
  <div class="ftr-top">
    <div class="ftr-l">
      <a class="ftr-logo" href="index.html"><img src="assets/logo.png" alt="Painting With Purpose" width="600" height="402" loading="lazy"></a>
      <p class="ftr-line">Good painting that does some good.</p>
      <p>Greater Burlington, Vermont<br><a href="tel:{TEL}">802-PAINTER · {PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    </div>
    <ul class="ftr-r"><li><a href="work.html">Work</a></li><li><a href="transformations.html">Before &amp; After</a></li><li><a href="services.html">Services</a></li><li><a href="purpose.html">Purpose</a></li><li><a href="careers.html">Careers</a></li><li><a href="contact.html">Contact</a></li></ul>
    <ul class="ftr-r"><li><a href="{IG}" target="_blank" rel="noopener">Instagram</a></li><li><a href="{FB}" target="_blank" rel="noopener">Facebook</a></li><li><a href="https://www.cvoeo.org/" target="_blank" rel="noopener">CVOEO</a></li></ul>
  </div>
  <div class="ftr-bot"><span>© 2026 Painting With Purpose</span><span>A share of every job goes to CVOEO</span><span>Site by ArkiTech Solutions</span></div>
</footer>
<script src="assets/js/site.js"></script>
</body>
</html>
'''
    open(fn, 'w').write(doc)


def cap(title, where):
    return f'<span class="cap"><span>{title}</span><span>{where}</span></span>'


def ba_frame(t, cls=''):
    if t['dip']:  # different angles: show the two frames side by side instead of a slider
        return (f'<div class="ba-frame ba-dip {cls}"><img src="assets/ba/{t["id"]}-before.jpg" alt="{t["title"]}, before" loading="lazy" decoding="async">'
                f'<img src="assets/ba/{t["id"]}-after.jpg" alt="{t["title"]}, after" loading="lazy" decoding="async"></div>')
    return f'''<div class="ba-frame {cls}" style="--p:50%">
    <img src="assets/ba/{t["id"]}-before.jpg" alt="{t["title"]}, before" loading="lazy" decoding="async">
    <img class="ba-after" src="assets/ba/{t["id"]}-after.jpg" alt="{t["title"]}, after" loading="lazy" decoding="async">
    <span class="ba-tag b">Before</span><span class="ba-tag a">After</span>
    <span class="ba-line" aria-hidden="true"></span>
    <input class="ba-range" type="range" min="0" max="100" value="50" aria-label="Compare before and after: {t["title"]}">
  </div>'''


def ending(line='Planning a project? We’ll walk it with you and send a written estimate.'):
    return f'''<section class="ending">
  {art('panorama', 'wc-end')}
  <div class="ending-in"><h2>{line}</h2><div class="ctas"><a class="btn" href="contact.html">Request a free estimate</a><a class="tlink" href="tel:{TEL}">or call 802-PAINTER</a></div></div>
</section>'''


# ---------------------------------------------------------------- home
def ptile(fn, cls, sizes, wc=None):
    d = P[fn]
    a = art(wc[0], f'wc-tile {wc[1]}') if wc else ''
    return (f'<a class="ptile {cls}" href="{fn}">{a}<span class="ptile-img">{img(lead(fn), plain(d["title"]), sizes)}</span>'
            f'<span class="ptile-t">{d["title"]}</span><span class="ptile-l">{d["loc"]} · {d["kind"].split(" · ")[-1]}</span></a>')


def hero(i, fn):
    d = P[fn]
    head = ('<div class="hero-head"><p class="eyebrow">House painters · Greater Burlington, Vermont</p>'
            '<p class="hero-h">Careful painting for Vermont homes, <em>with purpose.</em></p>'
            '<div class="ctas"><a class="btn btn-light" href="contact.html">Free estimate</a></div></div>') if i == 0 else ''
    return (f'<article class="hero" style="z-index:{i + 1}">{img(lead(fn), plain(d["title"]), eager=(i < 2))}'
            f'<div class="hero-in">{head}<a class="hero-p" href="{fn}"><span class="n">{i + 1:02d} / {len(ORDER):02d}</span>'
            f'<span class="hero-t">{d["title"]}</span><span class="hero-l">{d["loc"]} · {d["kind"].split(" · ")[-1]}</span>'
            f'<span class="hero-go">View project →</span></a></div></article>')


stack = ''.join(hero(i, fn) for i, fn in enumerate(ORDER))
home_tf = [t for t in TF if not t['dip']][:4]
svc_rows = ''.join(f'<li><a href="services.html#{k}"><span class="n">{i:02d}</span><span class="t">{html.escape(t)}</span><span class="arr">→</span></a></li>'
                   for i, (k, t) in enumerate(SERVICES, 1))
page('index.html', 'Painting With Purpose | House painters in Greater Burlington, Vermont',
     'Residential and commercial painting in Greater Burlington, Vermont. Part of every job helps end homelessness.',
     f'''<h1 class="sr">Painting With Purpose: careful painting for Vermont homes</h1>
<section class="stack">{stack}</section>

<section class="intro">
  {art('panorama', 'wc-hero')}
  <div class="intro-txt">
    <p class="eyebrow">House painters · Greater Burlington, Vermont</p>
    <h2>Careful painting for Vermont homes, <em>with purpose.</em></h2>
    <p class="lede">Prep done right, a clean site every evening, and a share of every job going to help Vermonters find a home.</p>
    <div class="ctas"><a class="btn" href="contact.html">Free estimate</a><a class="tlink" href="work.html">All projects →</a></div>
  </div>
</section>

<section class="bafeat">
  {art('paint-roller', 'wc-roller')}
  <div class="bafeat-media">{ba_frame(home_tf[0])}</div>
  <div class="bafeat-txt">
    <p class="eyebrow">Before &amp; after</p>
    <h2>Same house, same angle.</h2>
    <p>{home_tf[0]["title"]}: {home_tf[0]["note"].lower()}. Drag across the photo to compare the first day of the job with the last.</p>
    <div class="ba-mini">{''.join(f'<a href="transformations.html"><img src="assets/ba/{t["id"]}-after-th.jpg" alt="{t["title"]}, after" loading="lazy"><span>{t["title"]}</span></a>' for t in home_tf[1:4])}</div>
    <a class="tlink" href="transformations.html">All {len(TF)} transformations →</a>
  </div>
</section>

<section class="purpose-band">
  {art('vermont-church-village', 'wc-village')}
  <div class="pb-txt">
    <p class="eyebrow">Our purpose</p>
    <h2>Every job helps a Vermont neighbor find a home.</h2>
    <p>Part of what every client pays goes to CVOEO, the Champlain Valley Office of Economic Opportunity, and straight to helping people find long-term, stable housing.</p>
    <dl class="stats"><div><dt>$15k+</dt><dd>given to CVOEO</dd></div><div><dt>12</dt><dd>people into secure housing</dd></div><div><dt>$0</dt><dd>added to your price</dd></div></dl>
    <a class="tlink" href="purpose.html">Why we do it →</a>
  </div>
  <figure class="pb-ph">{img('assets/img/pwp-1247.jpg', 'The Painting With Purpose tent at a downtown street event', '(max-width: 760px) 100vw, 40vw')}</figure>
</section>

<section class="svc-list">
  {art('paint-brush', 'wc-brush')}
  <div class="sec-t"><p class="eyebrow">Services</p><h2>Five services, one standard.</h2><a class="tlink" href="services.html">Details →</a></div>
  <ul class="rows">{svc_rows}</ul>
</section>

<section class="quote">
  {art('autumn-maple-leaves', 'wc-leaves')}
  <blockquote>“Professional is not a large enough word to describe PWP’s craftsmanship and commitment.”</blockquote>
  <p class="eyebrow">Pat Waterman · Google review</p>
</section>
{ending()}''')

# ---------------------------------------------------------------- work index
cards = ''.join(
    f'<a class="card" href="{fn}"><span class="card-img">{img(lead(fn), plain(P[fn]["title"]), "(max-width: 760px) 100vw, 46vw")}</span>'
    f'<span class="card-t">{P[fn]["title"]}</span><span class="card-l">{P[fn]["loc"]} · {P[fn]["kind"].split(" · ")[-1]}</span></a>'
    for fn in ORDER)
page('work.html', 'Work | Painting With Purpose', 'Homes, storefronts and public buildings painted by Painting With Purpose.',
     f'''<section class="phead">
  {art('white-country-cottage', 'wc-phead')}
  <p class="eyebrow">Work</p>
  <h1>Homes, storefronts and public buildings.</h1>
  <p class="lede">Across Greater Burlington. Most of these photographs were taken by Gabe on the last day of the job.</p>
</section>
<section class="cards">{cards}</section>
{ending()}''', 'work.html')


# ---------------------------------------------------------------- project pages
def frame(kind, a, b, title):
    alt = plain(title)
    if kind == 'full':
        return f'<figure class="pj-full">{img(f"assets/img/{a}.jpg", alt, "(max-width: 760px) 100vw, 70vw")}</figure>'
    return (f'<div class="pj-pair"><figure>{img(f"assets/img/{a}.jpg", alt, "(max-width: 760px) 100vw, 35vw")}</figure>'
            f'<figure>{img(f"assets/img/{b}.jpg", alt, "(max-width: 760px) 100vw, 35vw")}</figure></div>')


for fn, d in P.items():
    groups = ''
    for i, g in enumerate(GROUPS[fn]):
        frames = ''.join(frame(f[0], f[1], f[2] if len(f) > 2 else None, d['title']) for f in g)
        note = f'<p class="pj-note"><span>{i + 1:02d}</span>{d["text"][i]}</p>' if i < len(d['text']) else '<p class="pj-note"></p>'
        groups += f'<div class="pj-group">{note}<div class="pj-frames">{frames}</div></div>'
    facts = d['facts'].replace('<dt>', '<div><dt>').replace('</dd>', '</dd></div>')
    facts += '<div><dt>Photography</dt><dd>Gabe Dunn</dd></div>'
    nxt = d['next']
    body = f'''<section class="pj-hero">{img(lead(fn), plain(d['title']), eager=True)}</section>
<section class="pj-head">
  {art(ART[fn], 'wc-pj')}
  <div><p class="eyebrow">{d['kind']}</p><h1>{d['title']}</h1><p class="loc">{d['loc']}</p></div>
  <p class="lede">{d['lede']}</p>
</section>
<section class="pj-body">{groups}</section>
<section class="pj-about">
  <div><p class="eyebrow">The job</p><dl class="credits">{facts}</dl></div>
  <div><p class="eyebrow">Palette</p><div class="palette">{d['palette']}</div></div>
</section>
<a class="pj-next" href="{nxt[0]}">{img(lead(nxt[0]), plain(nxt[1]), '100vw')}<span class="cap"><span>Next project</span><span class="big">{nxt[1]} →</span></span></a>
{ending()}'''
    page(fn, f'{plain(d["title"])} | Painting With Purpose', plain(d['lede']), body, 'work.html', og=d['hero'])

# ---------------------------------------------------------------- services
SV = {
    'residential': ('Residential painting', 'white-clapboard-porch', 'Interiors and exteriors, from a single room to a full Victorian restoration. Cabinets, trim, siding, porches and the repairs underneath them.',
                    ['Exterior siding, trim and shutters', 'Interior walls, ceilings and trim', 'Cabinets and built-ins', 'Porches, railings and floors'], 'assets/img/pwp-0058-porch.jpg'),
    'commercial': ('Commercial painting', 'vermont-church-village', 'Storefronts, offices, multi-unit and public buildings, worked in phases and off-hours so your doors stay open.',
                   ['Offices, retail and dealerships', 'Libraries and public buildings', 'Property-management repaints', 'Night and weekend scheduling'], 'assets/img/pwp-0995.jpg'),
    'decks': ('Decks & porches', 'mountain-view-porch', 'Cleaning, brightening, stripping where needed, and staining with products made for Vermont winters.',
              ['Washing and brightening', 'Board repair and sanding', 'Penetrating and solid stains', 'Painted porch floors'], 'assets/img/pwp-1371.jpg'),
    'lead': ('Lead-safe work', 'painter-ladder', 'Certified Essential Maintenance Practices inspections for pre-1978 homes and rentals, with lead-safe repair when it’s needed.',
             ['EMP inspections', 'Lead-safe prep and containment', 'HEPA cleanup', 'Documentation for landlords'], 'assets/img/pwp-0058-gable.jpg'),
    'gutters': ('Gutter cleaning', 'autumn-maple-leaves', 'Fall and spring cleanouts that keep water off your siding, away from your foundation, and off fresh paint.',
                ['Fall and spring cleanouts', 'Downspout flushing', 'Leak and hanger checks', 'Debris hauled away'], 'assets/img/pwp-0701.jpg'),
}
rows = ''.join(
    f'''<article class="svc" id="{k}">
  <figure class="svc-ph">{art(a, 'wc-svc')}{img(ph, html.escape(n), '(max-width: 760px) 100vw, 45vw')}</figure>
  <div class="svc-txt"><span class="n">{i:02d}</span><h2>{html.escape(n)}</h2><p>{t}</p><ul class="lines">{''.join(f'<li>{x}</li>' for x in items)}</ul><a class="tlink" href="contact.html">Request an estimate →</a></div>
</article>''' for i, (k, (n, a, t, items, ph)) in enumerate(SV.items(), 1))
page('services.html', 'Services | Painting With Purpose',
     'Residential and commercial painting, deck staining, EMP lead inspections and gutter cleaning in Greater Burlington, Vermont.',
     f'''<section class="phead">
  {art('paint-color-swatches', 'wc-phead')}
  <p class="eyebrow">Services</p>
  <h1>Five services, one standard.</h1>
  <p class="lede">Vetted painters, a clean site every evening, and clear communication from the first call to the final walkthrough.</p>
</section>
<section class="svcs">{rows}</section>
<section class="steps-sec">
  {art('tape-measure', 'wc-tape')}
  <div class="sec-t"><p class="eyebrow">Process</p><h2>How a job runs.</h2></div>
  <ol class="steps">
    <li><span class="n">01</span><h3>Walkthrough</h3><p>We visit, measure, talk through colors and surfaces, and note any repairs.</p></li>
    <li><span class="n">02</span><h3>Written estimate</h3><p>An itemized proposal with scope, products, schedule and price.</p></li>
    <li><span class="n">03</span><h3>Prep and paint</h3><p>Protection first, then careful prep, then paint. The site is cleaned every evening.</p></li>
    <li><span class="n">04</span><h3>Final walkthrough</h3><p>We review every surface together and touch up anything before we call it done.</p></li>
  </ol>
</section>
{ending()}''', 'services.html', og='assets/img/pwp-0058-porch.jpg')

# ---------------------------------------------------------------- purpose
page('purpose.html', 'Purpose | Painting With Purpose',
     'Part of every Painting With Purpose job funds CVOEO’s work to end homelessness in Vermont.',
     f'''<section class="phead">
  {art('white-vermont-farmhouse', 'wc-phead')}
  <p class="eyebrow">Purpose</p>
  <h1>We paint to help end homelessness in Vermont.</h1>
</section>
<figure class="wide-ph">{img('assets/img/pwp-1247.jpg', 'The Painting With Purpose tent at a downtown street event')}{cap('Out in the community', 'Downtown street fair')}</figure>
<section class="split">
  {art('white-country-cottage', 'wc-split')}
  <h2>Community engagement</h2>
  <div>
    <p>Homelessness affects our whole community, and the solutions are few and far between. Part of what every client pays goes to CVOEO, the Champlain Valley Office of Economic Opportunity, and straight to helping people find a long-term, stable home.</p>
    <p>So far that is more than $15,000, twelve people helped into secure housing, and the Joy &amp; Jerry Meyers Cup along the way.</p>
    <ul class="lines"><li><a href="https://www.cvoeo.org/" target="_blank" rel="noopener">About CVOEO ↗</a></li><li><a href="{IG}" target="_blank" rel="noopener">Follow along on Instagram ↗</a></li></ul>
  </div>
</section>
<section class="split">
  <h2>Who we are</h2>
  <div><p>Brothers Gabe and Zach Dunn started Painting With Purpose to prove a painting company could be really good at the work and really good for the community. One of them is on nearly every job, and Gabe takes most of the photographs on this site.</p></div>
</section>
<section class="split">
  {art('lantern-and-stone-wall', 'wc-split')}
  <h2>What we value</h2>
  <dl class="vals"><div><dt>Quality</dt><dd>Prep done right, so the finish lasts.</dd></div><div><dt>Trust and respect</dt><dd>For your home, your time and your neighbors.</dd></div><div><dt>A clean worksite</dt><dd>Protected floors and plants, tidied every evening.</dd></div><div><dt>Clear communication</dt><dd>You always know what’s next and when.</dd></div></dl>
</section>
<section class="quote">
  {art('autumn-maple-leaves', 'wc-leaves')}
  <blockquote>“Their mission for giving back to the homeless community is truly amazing.”</blockquote>
  <p class="eyebrow">Pam Mathe · Google review</p>
</section>
{ending()}''', 'purpose.html', og='assets/img/pwp-1247.jpg')

# ---------------------------------------------------------------- careers
FORMOK = '<p class="form-ok" hidden>Thanks. This demo form isn’t connected yet; on the live site it goes straight to the PWP inbox.</p>'
page('careers.html', 'Careers | Painting With Purpose', 'Painting jobs in Greater Burlington, Vermont, with paid training.',
     f'''<section class="phead">
  {art('leather-tool-belt', 'wc-phead')}
  <p class="eyebrow">Careers</p>
  <h1>Paint with us.</h1>
  <p class="lede">We hire careful people and train them well: prep, cutting in, spraying, lead-safe practice, and how to treat a client’s home.</p>
</section>
<figure class="wide-ph">{img('assets/img/pwp-0631-painter.jpg', 'A painter on a ladder at a red shingle colonial')}{cap('On the job', 'Chittenden County')}</figure>
<section class="split">
  {art('hammer', 'wc-split')}
  <h2>Open roles</h2>
  <div>
    <ul class="lines roles"><li><a href="#apply"><b>Painter</b><span>Full-time · year-round</span><span>Apply →</span></a></li><li><a href="#apply"><b>Crew lead</b><span>Full-time · year-round</span><span>Apply →</span></a></li><li><a href="#apply"><b>Seasonal painter</b><span>May to October</span><span>Apply →</span></a></li></ul>
    <p>Training is paid, including lead-safe certification. Crews are local and home every night, and interiors keep us working through the winter. Every job you finish helps fund housing for Vermonters.</p>
  </div>
</section>
<section class="split" id="apply">
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
</section>''', 'careers.html', og='assets/img/pwp-0631-painter.jpg')

# ---------------------------------------------------------------- contact
towns = ['Burlington', 'South Burlington', 'Winooski', 'Colchester', 'Essex', 'Williston', 'Shelburne', 'Richmond', 'Hinesburg', 'Charlotte']
page('contact.html', 'Contact | Painting With Purpose', 'Request a free painting estimate in Greater Burlington, Vermont.',
     f'''<section class="phead">
  {art('paint-can', 'wc-phead')}
  <p class="eyebrow">Free estimate</p>
  <h1>Tell us about your project.</h1>
  <p class="lede">Free written estimates across Greater Burlington. We’ll set up a walkthrough.</p>
</section>
<section class="split">
  {art('mountain-view-porch', 'wc-split')}
  <div class="c-info">
    <p class="eyebrow">Call or text</p><p class="big"><a href="tel:{TEL}">802-PAINTER</a></p><p>{PHONE}<br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    <p class="eyebrow">Where we paint</p><p>{", ".join(towns)}, and nearby. Outside the list? Ask anyway.</p>
  </div>
  <form class="form" data-form novalidate>
    <label class="field"><span>Name</span><input name="name" autocomplete="name" required></label>
    <label class="field"><span>Phone</span><input name="phone" type="tel" autocomplete="tel"></label>
    <label class="field"><span>Email</span><input name="email" type="email" autocomplete="email" required></label>
    <label class="field"><span>Service</span><select name="service">{"".join(f"<option>{html.escape(v[0])}</option>" for v in SV.values())}</select></label>
    <label class="field"><span>Town</span><select name="town">{"".join(f"<option>{t}</option>" for t in towns)}<option>Other</option></select></label>
    <label class="field"><span>Timing</span><select name="when"><option>As soon as possible</option><option>Within 3 months</option><option>Next season</option><option>Just planning</option></select></label>
    <label class="field"><span>Project</span><textarea name="msg" rows="3" placeholder="Rooms, surfaces, anything we should know"></textarea></label>
    <button class="btn submit" type="submit">Request my estimate</button>
    {FORMOK}
  </form>
</section>
{ending()}''', 'contact.html', og='assets/img/pwp-1371.jpg')

# ---------------------------------------------------------------- before & after
tiles = ''.join(
    f'''<figure class="ba">
  {ba_frame(t)}
  <figcaption><span>{t["title"]}</span><span>{t["note"]}</span></figcaption>
</figure>''' for t in TF)
page('transformations.html', 'Before & After | Painting With Purpose', 'Before and after photos from real Painting With Purpose jobs.',
     f'''<section class="phead">
  {art('paint-roller', 'wc-phead')}
  <p class="eyebrow">Before &amp; after</p>
  <h1>Same house, same angle.</h1>
  <p class="lede">Drag across any photograph to compare the first day of the job with the last.</p>
</section>
<section class="ba-grid">{tiles}</section>
{ending()}''', 'transformations.html')
print('built')

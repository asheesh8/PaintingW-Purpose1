"""Builds the static pages for Demo 1 (minimal, photo-led).

Run from the repo root:  python3 tools/build.py
Page copy lives in this file; project facts live in tools/projects.json and
before/after pairs in tools/transformations.json.
"""
import json, html

P = json.load(open('tools/projects.json'))
TF = json.load(open('tools/transformations.json'))

NAV = [('work.html', 'Work'), ('transformations.html', 'Before & After'), ('services.html', 'Services'),
       ('purpose.html', 'Purpose'), ('careers.html', 'Careers')]

# project order and the frame that leads each one (photo-direction.md)
ORDER = ['project-sigma-phi-house.html', 'project-queen-anne-victorian.html', 'project-lake-cottage.html',
         'project-library.html', 'project-red-shingle-colonial.html', 'project-built-ins-and-porch.html',
         'project-dealership.html']
LEAD = {'project-dealership.html': 'assets/img/pwp-1337.jpg', 'project-lake-cottage.html': 'assets/img/pwp-0701.jpg',
        'project-built-ins-and-porch.html': 'assets/img/pwp-1371.jpg'}
POS = {'assets/img/pwp-0179.jpg': '50% 62%', 'assets/img/pwp-0058.jpg': '72% 40%', 'assets/img/pwp-0701.jpg': '40% 60%',
       'assets/img/pwp-0686.jpg': '50% 30%', 'assets/img/pwp-1247.jpg': '78% 50%', 'assets/img/pwp-1337.jpg': '50% 40%'}


def img(src, alt, sizes='100vw', eager=False, cls=''):
    md = src.replace('.jpg', '-md.jpg')
    import os
    srcset = f' srcset="{md} 1100w, {src} 2400w" sizes="{sizes}"' if os.path.exists(md) else ''
    pos = f' style="object-position:{POS[src]}"' if src in POS else ''
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ''
    return f'<img{c} src="{src}"{srcset} alt="{alt}" {load} decoding="async"{pos}>'


def page(fn, title, desc, body, current=None, og='assets/img/pwp-0179.jpg'):
    nav = ''.join(f'<a href="{h}"{" aria-current=\"page\"" if h == current else ""}>{html.escape(t)}</a>' for h, t in NAV)
    mnav = ''.join(f'<a href="{h}">{html.escape(t)}</a>' for h, t in [('index.html', 'Home')] + NAV + [('contact.html', 'Contact')])
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#FAF9F6">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{og}">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist+Mono:wght@500&family=Geist:wght@400;500&family=Instrument+Serif&display=swap">
<link rel="stylesheet" href="assets/css/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="hdr">
  <div class="wrap">
    <a class="logo" href="index.html" aria-label="Painting With Purpose, home"><img src="assets/logo.png" alt="Painting With Purpose" width="600" height="402"></a>
    <nav class="nav" aria-label="Primary">{nav}<a class="est" href="contact.html"{" aria-current=\"page\"" if current == "contact.html" else ""}>Free estimate</a></nav>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu">Menu</button>
  </div>
</header>
<div class="menu" id="menu" aria-hidden="true">
  <div class="menu-top"><a class="logo" href="index.html"><img src="assets/logo.png" alt="Painting With Purpose" width="600" height="402"></a><button class="menu-close" type="button">Close</button></div>
  <nav class="menu-nav" aria-label="Mobile">{mnav}</nav>
  <p class="meta">802-PAINTER · 802-724-6837</p>
</div>
<main id="main">
{body}
</main>
<footer class="ftr">
  <div class="wrap">
    <div class="ftr-top">
      <a class="logo ftr-logo" href="index.html"><img src="assets/logo.png" alt="Painting With Purpose" width="600" height="402" loading="lazy"></a>
      <div><h4>Contact</h4><p>802-PAINTER<br>802-724-6837<br><a href="mailto:marketing@pwpvt.com">marketing@pwpvt.com</a></p></div>
      <div><h4>Studio</h4><ul><li><a href="work.html">Work</a></li><li><a href="transformations.html">Before &amp; After</a></li><li><a href="services.html">Services</a></li><li><a href="purpose.html">Purpose</a></li><li><a href="careers.html">Careers</a></li></ul></div>
      <div><h4>Follow</h4><ul><li><a href="https://www.instagram.com/paintingwithpurposevt/" target="_blank" rel="noopener">Instagram</a></li><li><a href="https://www.facebook.com/PaintingWithPurposeVT" target="_blank" rel="noopener">Facebook</a></li><li><a href="https://www.cvoeo.org/" target="_blank" rel="noopener">CVOEO</a></li></ul></div>
    </div>
    <div class="ftr-bot meta"><span>© 2026 Painting With Purpose · Greater Burlington, Vermont</span><span>Site by ArkiTech Solutions</span></div>
  </div>
</footer>
<div class="peek" aria-hidden="true"><img alt=""></div>
<script src="assets/js/site.js" defer></script>
</body>
</html>
'''
    open(fn, 'w').write(doc)


def ba(pair, title, cls=''):
    return (f'<div class="ba {cls}" data-ba><div class="layer before"><img src="assets/ba/{pair}-before.jpg" alt="{title}, before" loading="lazy"></div>'
            f'<div class="layer after"><img src="assets/ba/{pair}-after.jpg" alt="{title}, after" loading="lazy"></div>'
            '<span class="tag b">Before</span><span class="tag a">After</span><span class="bar"></span>'
            f'<input type="range" min="0" max="100" value="50" step="0.5" aria-label="Compare before and after: {title}">'
            '<span class="knob"><svg viewBox="0 0 26 26" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 7l-5 6 5 6M17 7l5 6-5 6"/></svg></span></div>')


def ending(line='Planning a project? We’ll walk it with you and send a written estimate.'):
    return f'''<section class="wrap end">
  <p>{line}</p>
  <a class="tlink" href="contact.html">Request a free estimate <span>→</span></a>
</section>'''


def cap(name, where):
    return f'<figcaption class="cap"><span>{name}</span><span>{where}</span></figcaption>'


def card(fn, cls='', sizes='(max-width: 760px) 100vw, 50vw'):
    d = P[fn]
    src = LEAD.get(fn, d['hero'])
    return (f'<a class="card {cls}" href="{fn}" data-tags="{d["kind"].lower()}"><figure><div class="ph">{img(src, d["title"], sizes)}</div>'
            f'{cap(d["title"], d["loc"])}</figure></a>')


# ---------------------------------------------------------------- home
home = f'''<section class="hero">
  {img('assets/img/pwp-0179.jpg', 'Sigma Phi House in Burlington, freshly painted columns and trim', eager=True)}
  <div class="hero-in wrap">
    <h1>Careful painting for Vermont homes and buildings.</h1>
    <a class="tlink light" href="work.html">View work <span>→</span></a>
  </div>
  <span class="hero-cap meta">Sigma Phi House — Burlington</span>
</section>

<section class="wrap intro">
  <div class="intro-txt">
    <span class="meta">Painting With Purpose</span>
    <p class="lead">A painting company in Greater Burlington. We prepare every surface properly, keep a clean site, and give part of every job to ending homelessness in Vermont.</p>
  </div>
  <figure class="intro-ph">{img('assets/img/pwp-1371.jpg', 'A painted porch with a diamond-pattern floor', '(max-width: 760px) 100vw, 40vw')}{cap('Porch ceiling and floor', 'Burlington')}</figure>
</section>

<section class="wrap sel">
  <div class="sec-t"><h2>Selected work</h2><a class="tlink" href="work.html">All projects <span>→</span></a></div>
  <div class="sel-grid">
    {card('project-queen-anne-victorian.html', 's1', '(max-width: 760px) 100vw, 62vw')}
    {card('project-library.html', 's2', '(max-width: 760px) 100vw, 38vw')}
    {card('project-lake-cottage.html', 's3', '(max-width: 760px) 100vw, 62vw')}
  </div>
</section>

<section class="wrap ba-sec">
  <div class="sec-t"><h2>Before and after</h2><a class="tlink" href="transformations.html">All transformations <span>→</span></a></div>
  {ba('ext-05', 'Bungalow in sage', 'wide')}
  <p class="cap"><span>Bungalow in sage — full exterior color change</span><span>Drag to compare</span></p>
</section>

<section class="wrap purp">
  <figure>{img('assets/img/pwp-0631-painter.jpg', 'A painter on a ladder at a red shingle colonial', '(max-width: 760px) 100vw, 40vw')}{cap('On the job', 'Chittenden County')}</figure>
  <div class="purp-txt">
    <span class="meta">Our purpose</span>
    <p class="lead">Part of every job goes to CVOEO, the Champlain Valley Office of Economic Opportunity, to help end homelessness in Vermont.</p>
    <p class="num"><b>$15,000+</b> given so far</p>
    <a class="tlink" href="purpose.html">How it works <span>→</span></a>
  </div>
</section>

<section class="wrap quote">
  <blockquote>“The best experience we’ve ever had with painters.”</blockquote>
  <p class="meta">Barbara Boutsikaris · Google review</p>
</section>

<figure class="strip">{img('assets/img/pwp-0686.jpg', 'A blue lake camp with kayaks on the shore')}</figure>
{ending()}'''
page('index.html', 'Painting With Purpose | Vermont Painting Company',
     'Careful residential and commercial painting across Greater Burlington, Vermont, with part of every job given to ending homelessness.', home)

# ---------------------------------------------------------------- work
grid = ''.join(card(fn, 'tall' if fn in ('project-built-ins-and-porch.html',) else '') for fn in ORDER)
idx = ''.join(f'<a class="prow" href="{fn}" data-img="{LEAD.get(fn, P[fn]["hero"]).replace(".jpg", "-md.jpg")}"><span class="n">{i+1:02d}</span><h3>{P[fn]["title"]}</h3><span class="meta">{P[fn]["kind"]}</span><span class="meta c4">{P[fn]["loc"]}</span></a>' for i, fn in enumerate(ORDER))
work = f'''<section class="wrap phead">
  <span class="meta">Work</span>
  <h1>Homes, storefronts and public buildings.</h1>
  <p>Recent jobs across Chittenden County, photographed by our own crew.</p>
</section>
<section class="wrap">
  <div class="work-grid">{grid}</div>
</section>
<section class="wrap pidx-sec">
  <div class="sec-t"><h2>Index</h2></div>
  <div class="pindex">{idx}</div>
</section>
{ending()}'''
page('work.html', 'Work | Painting With Purpose', 'Recent painting projects across Greater Burlington, Vermont.', work, 'work.html')

# ---------------------------------------------------------------- projects
for i, fn in enumerate(ORDER):
    d = P[fn]
    hero = LEAD.get(fn, d['hero'])
    gal = [s for c, s in d['gallery'] if s not in (hero, 'assets/img/pwp-1343.jpg', 'assets/img/pwp-0735.jpg')]
    if fn == 'project-dealership.html':
        gal = ['assets/img/pwp-1335.jpg']
    if fn == 'project-library.html':
        gal = ['assets/img/pwp-0951.jpg', 'assets/img/pwp-0856.jpg']
    if fn == 'project-lake-cottage.html':
        gal = ['assets/img/pwp-0686-porch.jpg', 'assets/img/pwp-0695.jpg']
    if fn == 'project-built-ins-and-porch.html':
        gal = ['assets/img/pwp-1094.jpg', 'assets/img/pwp-1094-shelves.jpg']
    figs = ''.join(f'<figure class="g{j}">{img(s, d["title"] + " detail", "(max-width: 760px) 100vw, 50vw")}</figure>' for j, s in enumerate(gal[:2]))
    nxt = ORDER[(i + 1) % len(ORDER)]
    body = f'''<section class="pj-hero">{img(hero, d["title"], eager=True)}</section>
<section class="wrap pj-head">
  <div>
    <span class="meta">{d["kind"]}</span>
    <h1>{d["title"]}</h1>
    <p class="lede">{d["lede"]}</p>
  </div>
  <dl class="facts">{d["facts"]}</dl>
</section>
<section class="wrap pj-gal n{len(gal[:2])}">{figs}</section>
<section class="wrap pj-text">
  <div class="palette"><span class="meta">Colors on this job</span><div class="sws">{d["palette"]}</div></div>
  <div>{"".join(f"<p>{t}</p>" for t in d["text"])}</div>
</section>
<section class="wrap pj-next"><span class="meta">Next project</span><a href="{nxt}">{P[nxt]["title"]} <span>→</span></a></section>
{ending()}'''
    page(fn, f'{html.unescape(d["title"])} | Painting With Purpose', html.escape(html.unescape(d['lede'])), body, None, hero)

# ---------------------------------------------------------------- transformations
th = ''.join(f'<button class="tf-th" type="button" data-i="{i}" data-cat="{t["cat"]}" aria-label="Show {t["title"]}"><span class="tf-img"><img src="assets/ba/{t["id"]}-after.jpg" alt="" loading="lazy"><img class="bf" src="assets/ba/{t["id"]}-before.jpg" alt="" loading="lazy"></span><span class="tf-cap"><b>{t["title"]}</b></span></button>' for i, t in enumerate(TF))
chips = ''.join(f'<button class="chipb" type="button" data-tf-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{v}</button>' for k, v in [('all', 'All'), ('exterior', 'Exterior'), ('interior', 'Interior'), ('decks', 'Porches & decks'), ('repair', 'Repairs'), ('commercial', 'Commercial')])
tf = f'''<section class="wrap phead">
  <span class="meta">Before &amp; after</span>
  <h1>Same house, same angle.</h1>
  <p>Drag across a photo to compare. Real jobs, photographed by our crew on the first and last day.</p>
</section>
<section class="wrap tf-stage" data-tf-stage>
  <div class="tf-media">{ba(TF[0]["id"], TF[0]["title"], "wide")}</div>
  <div class="tf-info">
    <span class="meta"><span data-tf-n>01</span> / {len(TF)} · <span data-tf-cat>{TF[0]["cat"]}</span></span>
    <h2 data-tf-title>{TF[0]["title"]}</h2>
    <p class="mute" data-tf-note>{TF[0]["note"]}</p>
    <div class="tf-ctl"><button class="tlink" type="button" data-tf-step="-1" aria-label="Previous transformation"><span>←</span> Previous</button><button class="tlink" type="button" data-tf-step="1" aria-label="Next transformation">Next <span>→</span></button><button class="tlink" type="button" data-tf-peek aria-pressed="false">Show before</button></div>
  </div>
</section>
<section class="wrap tf-list">
  <div class="filters"><div class="chips" role="group" aria-label="Filter transformations">{chips}</div></div>
  <div class="tf-grid">{th}</div>
</section>
<script type="application/json" id="tf-data">{json.dumps(TF)}</script>
{ending()}'''
page('transformations.html', 'Before & After | Painting With Purpose', 'Before and after photos from real Painting With Purpose jobs.', tf, 'transformations.html')

# ---------------------------------------------------------------- services
SV = [('Residential painting', 'Interiors and exteriors, from a single room to a full Victorian restoration. Cabinets, trim, siding, porches and the repairs underneath them.', 'assets/img/pwp-0058-porch.jpg', 'Queen Anne porch'),
      ('Commercial painting', 'Storefronts, offices, multi-unit and public buildings, worked in phases and off-hours so your doors stay open.', 'assets/img/pwp-0995.jpg', 'Library & Community Hall'),
      ('Deck staining & maintenance', 'Cleaning, brightening, stripping where needed, and staining with products made for Vermont winters.', 'assets/img/pwp-1371.jpg', 'Porch floor'),
      ('EMP lead inspections', 'Certified Essential Maintenance Practices inspections for pre-1978 homes and rentals, with lead-safe repair when it’s needed.', 'assets/img/pwp-0058-gable.jpg', 'Victorian gable'),
      ('Gutter cleaning', 'Fall and spring cleanouts that keep water off your siding, away from your foundation, and off fresh paint.', 'assets/img/pwp-0701.jpg', 'After the leaves')]
rows = ''.join(f'<article class="svc"><figure>{img(s, a, "(max-width: 760px) 100vw, 50vw")}</figure><div><span class="meta">{i+1:02d}</span><h2>{html.escape(n)}</h2><p>{t}</p></div></article>' for i, (n, t, s, a) in enumerate(SV))
svc = f'''<section class="wrap phead">
  <span class="meta">Services</span>
  <h1>Five services, one standard.</h1>
  <p>Vetted painters, a clean site every evening, and clear communication from the first call to the final walkthrough.</p>
</section>
<section class="wrap svcs">{rows}</section>
<section class="wrap steps">
  <div class="sec-t"><h2>How a job runs</h2></div>
  <ol>
    <li><b>Walkthrough.</b> We visit, measure, talk through colors and surfaces, and note any repairs.</li>
    <li><b>Written estimate.</b> An itemized proposal with scope, products, schedule and price.</li>
    <li><b>Prep and paint.</b> Protection first, then careful prep, then paint. The site is cleaned every evening.</li>
    <li><b>Final walkthrough.</b> We review every surface together and touch up anything before we call it done.</li>
  </ol>
</section>
{ending()}'''
page('services.html', 'Services | Painting With Purpose', 'Residential and commercial painting, deck staining, EMP lead inspections and gutter cleaning in Greater Burlington, Vermont.', svc, 'services.html')

# ---------------------------------------------------------------- purpose
purpose = f'''<section class="wrap phead">
  <span class="meta">Purpose</span>
  <h1>We paint to help end homelessness in Vermont.</h1>
</section>
<figure class="wrap wide-ph">{img('assets/img/pwp-1247.jpg', 'The Painting With Purpose tent at a downtown street event')}{cap('Out in the community', 'Downtown street fair')}</figure>
<section class="wrap pair">
  <figure>{img('assets/img/pwp-0631.jpg', 'A painter on a ladder at a red shingle colonial', '(max-width: 760px) 100vw, 45vw')}{cap('Red Shingle Colonial', 'Chittenden County')}</figure>
  <div class="prose">
    <p>Homelessness affects our whole community, and the solutions are few and far between. Part of what every client pays goes to CVOEO, the Champlain Valley Office of Economic Opportunity, and straight to helping people find a long-term, stable home.</p>
    <p>So far that is more than $15,000, twelve people helped into secure housing, and the Joy &amp; Jerry Meyers Cup along the way.</p>
    <img class="wc-accent" src="assets/art/wc/white-vermont-farmhouse.jpg" alt="" loading="lazy">
    <p><a class="tlink" href="https://www.cvoeo.org/" target="_blank" rel="noopener">About CVOEO <span>↗</span></a></p>
  </div>
</section>
<section class="wrap vals">
  <div class="sec-t"><h2>What we value</h2></div>
  <dl>
    <dt>Quality</dt><dd>Prep done right, so the finish lasts.</dd>
    <dt>Trust and respect</dt><dd>For your home, your time and your neighbors.</dd>
    <dt>A clean worksite</dt><dd>Protected floors and plants, tidied every evening.</dd>
    <dt>Clear communication</dt><dd>You always know what’s next and when.</dd>
  </dl>
</section>
<section class="wrap quote">
  <blockquote>“Their mission for giving back to the homeless community is truly amazing.”</blockquote>
  <p class="meta">Pam Mathe · Google review</p>
</section>
{ending()}'''
page('purpose.html', 'Purpose | Painting With Purpose', 'Part of every Painting With Purpose job funds CVOEO’s work to end homelessness in Vermont.', purpose, 'purpose.html', 'assets/img/pwp-1247.jpg')

# ---------------------------------------------------------------- careers
FORMOK = '<p class="form-ok" hidden>Thanks. This demo form isn’t connected yet; on the live site it goes straight to the PWP inbox.</p>'
careers = f'''<section class="pj-hero short">{img('assets/img/pwp-0631-painter.jpg', 'A painter on a ladder', eager=True)}</section>
<section class="wrap pj-head">
  <div>
    <span class="meta">Careers</span>
    <h1>Paint with us.</h1>
    <p class="lede">We hire careful people and train them well: prep, cutting in, spraying, lead-safe practice, and how to treat a client’s home.</p>
  </div>
  <dl class="facts"><dt>Work</dt><dd>Year-round, interiors through winter</dd><dt>Training</dt><dd>Paid, including lead-safe certification</dd><dt>Crews</dt><dd>Local, home every night</dd><dt>Purpose</dt><dd>Your work funds housing</dd></dl>
</section>
<section class="wrap roles-sec">
  <div class="sec-t"><h2>Open roles</h2></div>
  <div class="roles">
    <a class="role" href="#apply"><h3>Painter</h3><span class="meta">Full-time · Year-round</span><span>Apply →</span></a>
    <a class="role" href="#apply"><h3>Crew lead</h3><span class="meta">Full-time · Year-round</span><span>Apply →</span></a>
    <a class="role" href="#apply"><h3>Seasonal painter</h3><span class="meta">May to October</span><span>Apply →</span></a>
  </div>
</section>
<section class="wrap form-sec" id="apply">
  <div><h2>Apply</h2><p class="mute">Experience helps, but attitude matters more.</p></div>
  <form class="form" data-form novalidate>
    <div class="field"><label for="a-name">Name</label><input id="a-name" autocomplete="name" required></div>
    <div class="field"><label for="a-phone">Phone</label><input id="a-phone" type="tel" autocomplete="tel"></div>
    <div class="field full"><label for="a-email">Email</label><input id="a-email" type="email" autocomplete="email"></div>
    <div class="field full"><label for="a-role">Role</label><select id="a-role"><option>Painter</option><option>Crew lead</option><option>Seasonal painter</option></select></div>
    <div class="field full"><label for="a-exp">Experience</label><textarea id="a-exp" placeholder="Years painting, certifications, anything else"></textarea></div>
    <div class="full"><button class="btn" type="submit">Send application</button></div>
    {FORMOK}
  </form>
</section>'''
page('careers.html', 'Careers | Painting With Purpose', 'Painting jobs in Greater Burlington, Vermont, with paid training.', careers, 'careers.html', 'assets/img/pwp-0631-painter.jpg')

# ---------------------------------------------------------------- contact
towns = ['Burlington', 'South Burlington', 'Winooski', 'Colchester', 'Essex', 'Williston', 'Shelburne', 'Richmond', 'Hinesburg', 'Charlotte']
contact = f'''<section class="wrap phead">
  <span class="meta">Contact</span>
  <h1>Tell us about your project.</h1>
  <p>Free written estimates across Greater Burlington. We’ll set up a walkthrough.</p>
</section>
<section class="wrap contact">
  <form class="form" data-form novalidate>
    <div class="field"><label for="c-name">Name</label><input id="c-name" autocomplete="name" required></div>
    <div class="field"><label for="c-phone">Phone</label><input id="c-phone" type="tel" autocomplete="tel"></div>
    <div class="field full"><label for="c-email">Email</label><input id="c-email" type="email" autocomplete="email"></div>
    <div class="field full"><span class="lab">What do you need?</span><div class="opts"><input type="checkbox" id="s0" checked><label for="s0">Interior</label><input type="checkbox" id="s1"><label for="s1">Exterior</label><input type="checkbox" id="s2"><label for="s2">Commercial</label><input type="checkbox" id="s3"><label for="s3">Deck staining</label><input type="checkbox" id="s4"><label for="s4">Lead inspection</label><input type="checkbox" id="s5"><label for="s5">Gutters</label></div></div>
    <div class="field"><label for="c-town">Town</label><select id="c-town">{"".join(f"<option>{t}</option>" for t in towns)}<option>Other</option></select></div>
    <div class="field"><label for="c-when">Timing</label><select id="c-when"><option>As soon as possible</option><option>Within 3 months</option><option>Next season</option><option>Just planning</option></select></div>
    <div class="field full"><label for="c-msg">Project details</label><textarea id="c-msg" placeholder="Rooms, surfaces, square footage, anything we should know"></textarea></div>
    <div class="full"><button class="btn" type="submit">Request my estimate</button></div>
    {FORMOK}
  </form>
  <aside>
    <figure>{img('assets/img/pwp-1371.jpg', 'A painted porch', '(max-width: 760px) 100vw, 35vw')}</figure>
    <div class="c-info"><span class="meta">Call</span><p>802-PAINTER · 802-724-6837</p><span class="meta">Where we paint</span><p>{", ".join(towns)}, and nearby. Outside the list? Ask anyway.</p></div>
  </aside>
</section>'''
page('contact.html', 'Contact | Painting With Purpose', 'Request a free painting estimate in Greater Burlington, Vermont.', contact, 'contact.html', 'assets/img/pwp-1371.jpg')
print('built')

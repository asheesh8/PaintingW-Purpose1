"""Builds the static pages for Demo 1 (laid out after birdseyevt.com).

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

# menu, column one: services (big serif), column two: studio pages, column three: estimate
SERVICES = [('residential', 'Residential'), ('commercial', 'Commercial'), ('decks', 'Decks & Porches'),
            ('lead', 'Lead-Safe Work'), ('gutters', 'Gutter Cleaning')]
STUDIO = [('work.html', 'Work'), ('transformations.html', 'Before & After'), ('purpose.html', 'Purpose'),
          ('careers.html', 'Careers'), ('contact.html', 'Contact')]

# home page order (the stack of full-width photos) and each project's lead frame
ORDER = ['project-sigma-phi-house.html', 'project-queen-anne-victorian.html', 'project-lake-cottage.html',
         'project-library.html', 'project-red-shingle-colonial.html', 'project-built-ins-and-porch.html',
         'project-dealership.html']
LEAD = {'project-dealership.html': 'assets/img/pwp-1335.jpg', 'project-lake-cottage.html': 'assets/img/pwp-0695.jpg',
        'project-built-ins-and-porch.html': 'assets/img/pwp-1371.jpg', 'project-library.html': 'assets/img/pwp-0995.jpg'}
POS = {'assets/img/pwp-0179.jpg': '50% 62%', 'assets/img/pwp-0058.jpg': '72% 40%', 'assets/img/pwp-0701.jpg': '40% 60%',
       'assets/img/pwp-0686.jpg': '50% 30%', 'assets/img/pwp-1247.jpg': '78% 50%', 'assets/img/pwp-1337.jpg': '50% 40%',
       'assets/img/pwp-1371.jpg': '50% 62%', 'assets/img/pwp-0995.jpg': '50% 55%'}

# project photo sequence: each group opens with a numbered note; 'full' is one wide frame, 'pair' two tall frames
GROUPS = {
    'project-sigma-phi-house.html': [[('full', 'pwp-0179-pediment')], [('full', 'pwp-0179-door')]],
    'project-queen-anne-victorian.html': [[('full', 'pwp-0058-gable')], [('full', 'pwp-0058-porch')]],
    'project-lake-cottage.html': [[('full', 'pwp-0686'), ('full', 'pwp-0701')], [('full', 'pwp-0686-porch')]],
    'project-library.html': [[('full', 'pwp-0856')], [('pair', 'pwp-0951', 'pwp-0735')]],
    'project-red-shingle-colonial.html': [[('full', 'pwp-0631-windows')], [('pair', 'pwp-0631-painter', 'pwp-0631-windows')]],
    'project-built-ins-and-porch.html': [[('pair', 'pwp-1094', 'pwp-1371')], [('full', 'pwp-1094-shelves')]],
    'project-dealership.html': [[('full', 'pwp-1343')], [('full', 'pwp-1337')]],
}


def img(src, alt, sizes='100vw', eager=False, cls=''):
    md = src.replace('.jpg', '-md.jpg')
    srcset = f' srcset="{md} 1100w, {src} 2400w" sizes="{sizes}"' if os.path.exists(md) else ''
    pos = f' style="object-position:{POS[src]}"' if src in POS else ''
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ''
    return f'<img{c} src="{src}"{srcset} alt="{alt}" {load} decoding="async"{pos}>'


def plain(s):
    return html.unescape(s)


def page(fn, title, desc, body, current=None, dark=False, og='assets/img/pwp-0179.jpg'):
    big = ''.join(f'<li><a href="services.html#{k}">{html.escape(t)}</a></li>' for k, t in SERVICES)
    small = ''.join(f'<li><a href="{h}"{" aria-current=\"page\"" if h == current else ""}>{html.escape(t)}</a></li>' for h, t in STUDIO)
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#F5F4E9">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{og}">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://api.fontshare.com" crossorigin>
<link rel="stylesheet" href="https://api.fontshare.com/v2/css?f[]=gambetta@400,500&amp;f[]=switzer@400,500&amp;display=swap">
<link rel="stylesheet" href="assets/css/site.css">
</head>
<body{' class="dark"' if dark else ''}>
<a class="skip" href="#main">Skip to content</a>
<header class="hdr">
  <a class="logo" href="index.html" aria-label="Painting With Purpose, home"><img src="assets/logo.png" alt="Painting With Purpose" width="600" height="402"></a>
  <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu">Menu</button>
  <nav class="menu" id="menu" aria-label="Main">
    <ul class="menu-big">{big}</ul>
    <ul class="menu-small">{small}</ul>
    <div class="menu-est"><a href="contact.html">Free estimate</a><a href="tel:{TEL}">802-PAINTER</a></div>
  </nav>
</header>
<main id="main">
{body}
</main>
<footer class="ftr">
  <div class="ftr-top">
    <div class="ftr-l">
      <p class="ftr-est">Painting With Purpose</p>
      <p>Greater Burlington<br>Vermont</p>
      <p><a href="tel:{TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      <p><a href="{IG}" target="_blank" rel="noopener">@paintingwithpurposevt</a><br><a href="{FB}" target="_blank" rel="noopener">facebook</a></p>
    </div>
    <ul class="ftr-r"><li><a href="purpose.html">Purpose</a></li><li><a href="careers.html">Careers</a></li><li><a href="contact.html">Contact</a></li><li><a href="transformations.html">Before &amp; After</a></li></ul>
  </div>
  <div class="ftr-bot"><span>© 2026&nbsp; Painting With Purpose</span><span>Site by ArkiTech Solutions</span></div>
</footer>
<script src="assets/js/site.js"></script>
</body>
</html>
'''
    open(fn, 'w').write(doc)


def cap(title, where):
    return f'<span class="cap"><span>{title}</span><span>{where}</span></span>'


def lead(fn):
    return LEAD.get(fn, P[fn]['hero'])


# ---------------------------------------------------------------- home: the stack
stack = ''.join(
    f'<a class="stack-item" href="{fn}">{img(lead(fn), plain(P[fn]["title"]), eager=(i == 0))}{cap(P[fn]["title"], P[fn]["loc"])}</a>'
    for i, fn in enumerate(ORDER))
page('index.html', 'Painting With Purpose | House painters in Greater Burlington, Vermont',
     'Residential and commercial painting in Greater Burlington, Vermont. Part of every job helps end homelessness.',
     f'<h1 class="sr">Painting With Purpose</h1>\n<section class="stack">{stack}</section>')

# ---------------------------------------------------------------- work index
cards = ''.join(
    f'<a class="card" href="{fn}"><span class="card-img">{img(lead(fn), plain(P[fn]["title"]), "(max-width: 760px) 100vw, 50vw")}</span>'
    f'<span class="card-t">{P[fn]["title"]}</span><span class="card-l">{P[fn]["loc"]}</span></a>'
    for fn in ORDER)
page('work.html', 'Work | Painting With Purpose', 'Homes, storefronts and public buildings painted by Painting With Purpose.',
     f'''<section class="intro">
  <h1>Work</h1>
  <p>Homes, storefronts and public buildings across Greater Burlington. Most of these photographs were taken by Gabe on the last day of the job.</p>
</section>
<section class="cards">{cards}</section>''', 'work.html')


# ---------------------------------------------------------------- project pages
def frame(kind, a, b, title):
    alt = plain(title)
    if kind == 'full':
        return f'<figure class="pj-full">{img(f"assets/img/{a}.jpg", alt, "(max-width: 760px) 100vw, 72vw")}</figure>'
    return (f'<div class="pj-pair"><figure>{img(f"assets/img/{a}.jpg", alt, "(max-width: 760px) 50vw, 36vw")}</figure>'
            f'<figure>{img(f"assets/img/{b}.jpg", alt, "(max-width: 760px) 50vw, 36vw")}</figure></div>')


for fn, d in P.items():
    notes = d['text']
    groups = ''
    for i, g in enumerate(GROUPS[fn]):
        frames = ''.join(frame(f[0], f[1], f[2] if len(f) > 2 else None, d['title']) for f in g)
        note = f'<p class="pj-note"><span>{i + 1:02d}.</span>{notes[i]}</p>' if i < len(notes) else '<p class="pj-note"></p>'
        groups += f'<div class="pj-group">{note}<div class="pj-frames">{frames}</div></div>'
    facts = d['facts'].replace('<dt>', '<div><dt>').replace('</dd>', '</dd></div>')
    facts += '<div><dt>Painting</dt><dd>Painting With Purpose</dd></div><div><dt>Photography</dt><dd>Gabe Dunn</dd></div>'
    nxt = d['next']
    body = f'''<section class="pj-hero">{img(lead(fn), plain(d['title']), eager=True)}</section>
<section class="pj-head"><h1>{d['title']}</h1><p class="up">{d['loc']}</p></section>
<section class="pj-body">{groups}</section>
<section class="pj-about">
  <p class="up">About</p>
  <div>
    <h2>{d['lede']}</h2>
    <dl class="credits">{facts}</dl>
  </div>
</section>
<section class="pj-more"><a class="up" href="work.html">See more projects</a><a class="up" href="{nxt[0]}">Next: {nxt[1]} →</a></section>'''
    page(fn, f'{plain(d["title"])} | Painting With Purpose', plain(d['lede']), body, dark=True, og=d['hero'])

# ---------------------------------------------------------------- services
SV = {
    'residential': ('Residential painting', 'Interiors and exteriors, from a single room to a full Victorian restoration. Cabinets, trim, siding, porches and the repairs underneath them.',
                    ['Exterior siding, trim and shutters', 'Interior walls, ceilings and trim', 'Cabinets and built-ins', 'Porches, railings and floors']),
    'commercial': ('Commercial painting', 'Storefronts, offices, multi-unit and public buildings, worked in phases and off-hours so your doors stay open.',
                   ['Offices, retail and dealerships', 'Libraries and public buildings', 'Property-management repaints', 'Night and weekend scheduling']),
    'decks': ('Decks & porches', 'Cleaning, brightening, stripping where needed, and staining with products made for Vermont winters.',
              ['Washing and brightening', 'Board repair and sanding', 'Penetrating and solid stains', 'Painted porch floors']),
    'lead': ('Lead-safe work', 'Certified Essential Maintenance Practices inspections for pre-1978 homes and rentals, with lead-safe repair when it’s needed.',
             ['EMP inspections', 'Lead-safe prep and containment', 'HEPA cleanup', 'Documentation for landlords']),
    'gutters': ('Gutter cleaning', 'Fall and spring cleanouts that keep water off your siding, away from your foundation, and off fresh paint.',
                ['Fall and spring cleanouts', 'Downspout flushing', 'Leak and hanger checks', 'Debris hauled away']),
}
rows = ''.join(
    f'''<section class="split" id="{k}">
  <h2>{html.escape(n)}</h2>
  <div><p>{t}</p><ul class="lines">{''.join(f'<li>{x}</li>' for x in items)}</ul><ul class="lines"><li><a href="contact.html">Request an estimate →</a></li></ul></div>
</section>''' for k, (n, t, items) in SV.items())
page('services.html', 'Services | Painting With Purpose',
     'Residential and commercial painting, deck staining, EMP lead inspections and gutter cleaning in Greater Burlington, Vermont.',
     f'''<section class="split first">
  <h1>Painters for Vermont homes, storefronts and public buildings.</h1>
  <div><p>Vetted painters, a clean site every evening, and clear communication from the first call to the final walkthrough. Every job starts with a free walkthrough and a written, itemized estimate.</p></div>
</section>
{rows}
<section class="split">
  <h2>How a job runs</h2>
  <div><ol class="steps">
    <li><span>01.</span>We visit, measure, talk through colors and surfaces, and note any repairs.</li>
    <li><span>02.</span>You get an itemized proposal with scope, products, schedule and price.</li>
    <li><span>03.</span>Protection first, then careful prep, then paint. The site is cleaned every evening.</li>
    <li><span>04.</span>We review every surface together and touch up anything before we call it done.</li>
  </ol></div>
</section>
<section class="halves">
  <figure>{img('assets/img/pwp-0631-painter.jpg', 'A painter on a ladder at a red shingle colonial', '(max-width: 760px) 100vw, 50vw')}</figure>
  <figure>{img('assets/img/pwp-1094.jpg', 'A slate built-in with matching wainscot', '(max-width: 760px) 100vw, 50vw')}</figure>
</section>''', 'services.html', og='assets/img/pwp-0631-painter.jpg')

# ---------------------------------------------------------------- purpose (Birdseye's company page)
page('purpose.html', 'Purpose | Painting With Purpose',
     'Part of every Painting With Purpose job funds CVOEO’s work to end homelessness in Vermont.',
     f'''<section class="split first">
  <h1>Vermont painters working to end homelessness.</h1>
  <div><p>Painting With Purpose is a Greater Burlington crew of painters who care about the details: protected floors and plants, prep done right, and a site cleaned every evening. Brothers Gabe and Zach Dunn started the company to prove a painting business could be really good at the work and really good for the community. One of them is on nearly every job, and Gabe takes most of the photographs on this site.</p></div>
</section>
<section class="split">
  <h2>Community Engagement</h2>
  <div>
    <p>Homelessness affects our whole community, and the solutions are few and far between. Part of what every client pays goes to CVOEO, the Champlain Valley Office of Economic Opportunity, and straight to helping people find a long-term, stable home.</p>
    <p>So far that is more than $15,000, twelve people helped into secure housing, and the Joy &amp; Jerry Meyers Cup along the way.</p>
    <p>We value quality you can see, trust and respect for your home, a clean worksite and clear communication. You always know what’s next and when.</p>
    <ul class="lines up"><li><a href="https://www.cvoeo.org/" target="_blank" rel="noopener">CVOEO →</a></li><li><a href="{IG}" target="_blank" rel="noopener">Instagram →</a></li><li><a href="{FB}" target="_blank" rel="noopener">Facebook →</a></li></ul>
  </div>
</section>
<section class="halves">
  <figure>{img('assets/img/pwp-1247.jpg', 'The Painting With Purpose tent at a downtown street event', '(max-width: 760px) 100vw, 50vw')}</figure>
  <figure>{img('assets/img/pwp-0631-painter.jpg', 'A painter on a ladder at a red shingle colonial', '(max-width: 760px) 100vw, 50vw')}</figure>
</section>''', 'purpose.html', og='assets/img/pwp-1247.jpg')

# ---------------------------------------------------------------- careers
FORMOK = '<p class="form-ok" hidden>Thanks. This demo form isn’t connected yet; on the live site it goes straight to the PWP inbox.</p>'
page('careers.html', 'Careers | Painting With Purpose', 'Painting jobs in Greater Burlington, Vermont, with paid training.',
     f'''<section class="split first">
  <h1>Careers</h1>
  <div>
    <h2 class="sub">Painting</h2>
    <ul class="lines up"><li><a href="#apply">Painter (full-time, year-round) →</a></li><li><a href="#apply">Crew lead (full-time, year-round) →</a></li></ul>
    <h2 class="sub">Seasonal</h2>
    <ul class="lines up"><li><a href="#apply">Seasonal painter (May to October) →</a></li></ul>
    <p>We hire careful people and train them well: prep, cutting in, spraying, lead-safe practice, and how to treat a client’s home. Training is paid, including lead-safe certification, and crews are local and home every night.</p>
    <p>Interiors keep us working through the winter. And every job you finish helps fund housing for Vermonters through CVOEO.</p>
  </div>
</section>
<section class="wide">{img('assets/img/pwp-0058.jpg', 'A restored Queen Anne Victorian', '100vw')}</section>
<section class="split" id="apply">
  <h2>Apply</h2>
  <form class="form" data-form novalidate>
    <label class="field"><span>Name</span><input name="name" autocomplete="name" required></label>
    <label class="field"><span>Phone</span><input name="phone" type="tel" autocomplete="tel"></label>
    <label class="field"><span>Email</span><input name="email" type="email" autocomplete="email" required></label>
    <label class="field"><span>Role</span><select name="role"><option>Painter</option><option>Crew lead</option><option>Seasonal painter</option></select></label>
    <label class="field"><span>Experience</span><textarea name="exp" rows="3" placeholder="Years painting, certifications, anything else"></textarea></label>
    <button class="submit up" type="submit">Send application →</button>
    {FORMOK}
  </form>
</section>''', 'careers.html', og='assets/img/pwp-0058.jpg')

# ---------------------------------------------------------------- contact
towns = ['Burlington', 'South Burlington', 'Winooski', 'Colchester', 'Essex', 'Williston', 'Shelburne', 'Richmond', 'Hinesburg', 'Charlotte']
page('contact.html', 'Contact | Painting With Purpose', 'Request a free painting estimate in Greater Burlington, Vermont.',
     f'''<section class="split first">
  <h1>Contact</h1>
  <div>
    <p>Free written estimates across Greater Burlington. Tell us about the project and we’ll set up a walkthrough.</p>
    <ul class="lines"><li><a href="tel:{TEL}">802-PAINTER · {PHONE}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li></ul>
    <p class="mute">{", ".join(towns)}, and nearby. Outside the list? Ask anyway.</p>
  </div>
</section>
<section class="split">
  <h2>Request an estimate</h2>
  <form class="form" data-form novalidate>
    <label class="field"><span>Name</span><input name="name" autocomplete="name" required></label>
    <label class="field"><span>Phone</span><input name="phone" type="tel" autocomplete="tel"></label>
    <label class="field"><span>Email</span><input name="email" type="email" autocomplete="email" required></label>
    <label class="field"><span>Service</span><select name="service">{"".join(f"<option>{html.escape(n)}</option>" for n, _, _ in SV.values())}</select></label>
    <label class="field"><span>Town</span><select name="town">{"".join(f"<option>{t}</option>" for t in towns)}<option>Other</option></select></label>
    <label class="field"><span>Timing</span><select name="when"><option>As soon as possible</option><option>Within 3 months</option><option>Next season</option><option>Just planning</option></select></label>
    <label class="field"><span>Project</span><textarea name="msg" rows="3" placeholder="Rooms, surfaces, anything we should know"></textarea></label>
    <button class="submit up" type="submit">Request my estimate →</button>
    {FORMOK}
  </form>
</section>
<section class="wide">{img('assets/img/pwp-1371.jpg', 'A painted porch floor in a two-grey diamond', '100vw')}</section>''', 'contact.html', og='assets/img/pwp-1371.jpg')

# ---------------------------------------------------------------- before & after
def ba_frame(t):
    if t['dip']:  # different angles: show the two frames side by side instead of a slider
        return (f'<div class="ba-frame ba-dip"><img src="assets/ba/{t["id"]}-before.jpg" alt="{t["title"]}, before" loading="lazy" decoding="async">'
                f'<img src="assets/ba/{t["id"]}-after.jpg" alt="{t["title"]}, after" loading="lazy" decoding="async"></div>')
    return f'''<div class="ba-frame" style="--p:50%">
    <img src="assets/ba/{t["id"]}-before.jpg" alt="{t["title"]}, before" loading="lazy" decoding="async">
    <img class="ba-after" src="assets/ba/{t["id"]}-after.jpg" alt="{t["title"]}, after" loading="lazy" decoding="async">
    <span class="ba-line" aria-hidden="true"></span>
    <input class="ba-range" type="range" min="0" max="100" value="50" aria-label="Compare before and after: {t["title"]}">
  </div>'''


tiles = ''.join(
    f'''<figure class="ba">
  {ba_frame(t)}
  <figcaption class="up"><span>{t["title"]}</span><span>{t["note"]}</span></figcaption>
</figure>''' for t in TF)
page('transformations.html', 'Before & After | Painting With Purpose', 'Before and after photos from real Painting With Purpose jobs.',
     f'''<section class="split first">
  <h1>Before &amp; After</h1>
  <div><p>Same house, same angle. Drag across any photograph to compare the first day of the job with the last.</p></div>
</section>
<section class="ba-grid">{tiles}</section>''', 'transformations.html', dark=True)
print('built')

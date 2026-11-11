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
import re

P = json.load(open('tools/projects.json', encoding='utf-8'))
TF = json.load(open('tools/transformations.json', encoding='utf-8'))

PHONE, TEL, EMAIL = '802-724-6837', '+18027246837', 'office@pwpvt.com'
ADDRESS = '133 Elm Street, Office B, Winooski, Vermont'
AREA = 'Vermont, eastern New York and western New Hampshire'
HOURS = [('Monday', '7:30 to 4:00'), ('Tuesday to Friday', '8:00 to 4:00'), ('Saturday and Sunday', 'Closed')]
IG, FB = 'https://www.instagram.com/paintingwithpurposevt/', 'https://www.facebook.com/PaintingWithPurposeVT'
# still to come from the client; each link appears once its URL is filled in
LINKEDIN, FPF, INDEED = '', '', ''
SOCIALS = [(n, u) for n, u in (('Instagram', IG), ('Facebook', FB), ('LinkedIn', LINKEDIN), ('Front Porch Forum', FPF)) if u]

MENU = [('index.html', 'Home'), ('work.html', 'Work'), ('transformations.html', 'Portfolio'), ('services.html', 'Services'),
        ('about.html', 'About'), ('purpose.html', 'Purpose'), ('careers.html', 'Careers'), ('contact.html', 'Contact')]
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


def img(src, alt, sizes='100vw', eager=False, cls='', pos=True):
    md = src.replace('.jpg', '-md.jpg')
    srcset = f' srcset="{md} 1100w, {src} 2400w" sizes="{sizes}"' if os.path.exists(md) else ''
    pos = f' style="object-position:{POS[src]}"' if pos and src in POS else ''
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

# The estimate form posts to the ArkiTech client portal: it saves the lead, texts the PWP team and adds the customer to JobTread.
# The portal only accepts posts from the origins listed for this client (this site's domains and localhost).
PORTAL_LEAD_URL = 'https://bnmntlqjoiqrskjkfzsv.supabase.co/functions/v1/portal-lead'
PORTAL_ORG = 'painting-with-purpose'


# ContractorsRanked badge (Gabe, Nov 10): #1 for painters in Chittenden County, links to their listing
RANKED = ('<a class="ftr-ranked" href="https://www.contractorsranked.com/painters/essex-junction-vt" target="_blank" rel="noopener">'
          '<img src="https://www.contractorsranked.com/badges/contractors-ranked-listed.svg" alt="Listed on ContractorsRanked" width="240" height="80" loading="lazy"></a>')


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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500&family=Instrument+Serif:ital@0;1&display=swap">
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
  <div class="menu-r"><p>Born in Vermont. Serving {AREA}.</p><p><a href="tel:{TEL}">802-PAINTER · {PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p><p>{" · ".join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in SOCIALS)}</p></div>
</div>
<main id="main">
{body}
</main>
<footer class="ftr">
  <div class="ftr-brand"><a class="ftr-logo" href="index.html"><img src="assets/logo-navy-360.png" alt="Painting With Purpose" width="360" height="232" loading="lazy"></a><p>A painting company born in Vermont, for Vermonters.</p><p class="mute">Serving {AREA}.</p>{wc("mountains")}{RANKED}</div>
  <ul class="ftr-links"><li><a href="tel:{TEL}">802-PAINTER</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li class="mute">{ADDRESS}</li>{"".join(f'<li class="mute">{d} · {h}</li>' for d, h in HOURS)}</ul>
  <ul class="ftr-links"><li><a href="work.html">Work</a></li><li><a href="transformations.html">Portfolio</a></li><li><a href="services.html">Services</a></li><li><a href="about.html">About</a></li><li><a href="purpose.html">Purpose</a></li><li><a href="careers.html">Careers</a></li><li><a href="contact.html">Contact</a></li></ul>
  <ul class="ftr-social" aria-label="Follow us">{"".join(f'<li><a href="{u}" target="_blank" rel="noopener">{n}</a></li>' for n, u in SOCIALS)}</ul>
  <p class="ftr-bot"><span>© 2026 Painting With Purpose LLC</span><span>Part of every job goes to CVOEO.</span><span>Site by ArkiTech Solutions</span></p>
</footer>
<script src="assets/js/site.js"></script>
</body>
</html>
'''
    open(fn, 'w', encoding='utf-8').write(doc)


# ---------------------------------------------------------------- home
CTA = 'Request your free consultation today'

# what each kind of job includes, from the client's own checklists
COMMERCIAL_LIST = ['Material and equipment procurement', 'RRP lead-safe practices and documentation', 'Ground, driveway and roof protection',
                   'Rot repair', 'Epoxy repair', 'Carpentry improvements', 'Scraping', 'Sanding', 'Encapsulation', 'Oil priming',
                   'Standard priming', 'Dusting', 'Caulking', 'Wood filling', 'Moisture content testing', 'Masking', 'Spot priming',
                   'Glazing', 'Liquid masking', 'Demasking', 'Staining', 'Painting', 'Pressure washing', 'Window washing', 'Soft washing',
                   'Containment building', 'Touch-up painting', 'Block filling', 'Job site organization and cleanup']
RESIDENTIAL_LIST = ['Material and equipment procurement', 'Floor protection', 'Furniture moving and protection', 'Popcorn ceiling removal',
                    'Popcorn ceiling texture application', 'Drywall repair', 'Plaster repair', 'Spackle patching', 'Hand sanding',
                    'Festool HEPA vacuum sanding', 'Pole sanding', 'Drywall sanding, walls and ceilings', 'Dusting', 'Caulking', 'Caulk removal',
                    'Masking', 'Oil priming', 'Standard priming', 'Shellac priming', 'Painting', 'Spray painting', 'Cabinet refinishing',
                    'Lime washing', 'Staining', 'Clear coating', 'Demasking', 'Containment building', 'Job site organization and cleanup']


def checklist(items):
    return ''.join(f'<li>{html.escape(t)}</li>' for t in items)


# the home "Inside and out" section: two job photos (hover for a closer look), then each scope grouped by stage
INTERIOR_SCOPE = [('Protection & setup', ['Material and equipment procurement', 'Floor protection', 'Furniture moving and protection', 'Masking', 'Containment building']),
                  ('Repairs & surface prep', ['Popcorn ceiling removal', 'Popcorn ceiling texture application', 'Drywall repair', 'Plaster repair', 'Spackle patching',
                                              'Hand sanding', 'Festool HEPA vacuum sanding', 'Pole sanding', 'Drywall sanding, walls and ceilings', 'Dusting', 'Caulking', 'Caulk removal']),
                  ('Paint, stain & specialty finishes', ['Oil priming', 'Standard priming', 'Shellac priming', 'Painting', 'Spray painting', 'Cabinet refinishing',
                                                         'Lime washing', 'Staining', 'Clear coating']),
                  ('Finishing touches', ['Demasking', 'Job site organization and cleanup'])]
EXTERIOR_SCOPE = [('Protection & setup', ['Material and equipment procurement', 'RRP lead-safe practices and documentation', 'Ground, driveway and roof protection',
                                          'Masking', 'Liquid masking', 'Containment building']),
                  ('Repairs & surface prep', ['Rot repair', 'Epoxy repair', 'Carpentry improvements', 'Scraping', 'Sanding', 'Dusting', 'Caulking', 'Wood filling',
                                              'Moisture content testing', 'Glazing', 'Painting', 'Pressure washing', 'Window washing', 'Block filling']),
                  ('Primers & finishes', ['Encapsulation', 'Oil priming', 'Standard priming', 'Spot priming', 'Demasking', 'Staining']),
                  ('Finishing touches', ['Soft washing', 'Touch-up painting', 'Job site organization and cleanup'])]
# (project, eyebrow, heading, image, alt, hover hint, link text, magnifier)
PAINTING_PHOTOS = [('project-library.html', '01 · Ilsley Library', 'Interior', 'assets/img/pwp-0856.jpg',
                    'Bright white walls and timber shelving in the Ilsley Library stacks', 'Hover to see the finish up close.', 'See the Ilsley Library project', True),
                   ('project-dealership.html', '02 · Dealership', 'Exterior', 'assets/img/pwp-1335.jpg',
                    'An auto dealership entrance under a freshly painted red and white canopy', '', 'See the dealership project', False)]
PAINTING_CARDS = [('Interior services', 'Fresh paint for walls and ceilings, refinished cabinets and built-ins, and stained woodwork. We protect floors and furniture and repair drywall and plaster before painting as needed.', INTERIOR_SCOPE),
                  ('Exterior services', 'Painting and staining for homes and commercial buildings. We wash and prep the surfaces and address rot and damaged wood as needed before applying the finish.', EXTERIOR_SCOPE)]


def painting_photo(fn, eyebrow, h, src, alt, hint, link, lens):
    hint = f'\n        <p class="painting-invite">{hint}</p>' if hint else ''
    return f'''    <div class="painting-photo" data-dark{" data-detail-lens" if lens else ""}>
      {img(src, alt, sizes='(max-width: 760px) 100vw, 73vw', pos=False)}
      <div class="painting-photo-title">
        <p class="eyebrow">{eyebrow}</p>
        <h3>{h}</h3>{hint}
        <a class="painting-project-link" href="{fn}">{link} <span aria-hidden="true">↗</span></a>
      </div>
    </div>'''


def painting_card(h, t, scope):
    groups = ''.join(f'''
          <div>
            <dt>{g}</dt>
            <dd>{" · ".join(items)}</dd>
          </div>''' for g, items in scope)
    return f'''    <article class="home-painting-card">
      <h3>{h}</h3>
      <p>{t}</p>
      <div class="painting-scope">
        <p class="eyebrow">Full scope · {sum(len(i) for _, i in scope)} services</p>
        <dl>{groups}
        </dl>
      </div>
    </article>'''


home_painting = f'''<section class="home-painting" aria-labelledby="home-painting-title">
  <p class="eyebrow">Painting &amp; staining</p>
  <h2 id="home-painting-title">Inside and out.</h2>
  <div class="home-painting-grid">
{chr(10).join(painting_photo(*x) for x in PAINTING_PHOTOS)}
  </div>
  <div class="home-painting-services">
{chr(10).join(painting_card(*x) for x in PAINTING_CARDS)}
  </div>
</section>'''


EXPERIENCE = [('Exceptional quality', 'We always inspect our work to ensure our standards and your standards are aligned and met.'),
              ('Trust and respect', 'We treat you and your home with respect and care, as if it were our own. We show up on time and keep our promise to work safely, with precision and quality, every day and with a great attitude.'),
              ('Zero cleanup stress', 'No dust, no tools and no mess. We clean up every day that we’re on the job to ensure your safety and ease of living.'),
              ('Effective communication', 'We are with you every step of the way. We listen to your needs and make sure any change to the project is communicated with you directly, first.')]

# Google reviews, as shown on the client's previous site
REVIEWS = [('The BEST experience we’ve ever had with painters: they were communicative and immediately responsive throughout, they showed up ON TIME with all the equipment, paint, etc., they were clean and tidy, they did the job expertly and within the time frame they estimated, and they were respectful to us and to each other. LOVE THEM!', 'Barbara Boutsikaris'),
           ('Professional is not a large enough word to describe PWP’s craftsmanship and commitment with my recent house painting project. Matt and Josh knew what they were doing, methodically and meticulously got it done, and the results are fantastic!', 'Pat Waterman'),
           ('This house is a Victorian and had deferred maintenance. We are so happy to see it restored. My dad even loved them and he’s not easy to please! Highly recommend this skilled, high tech, high energy, “get it done” painting company.', 'K Raz'),
           ('Our 16 year old kitchen cabinets were very worn and look like new again! You won’t be disappointed… highly recommend them!', 'Lara Militello'),
           ('They helped me fix a crack from a previous painting company and made it look incredibly amazing. They painted shelves and baseboards with precision. Their mission for giving back to the homeless community is truly amazing.', 'Pam Mathe')]

CERTS = [('Certified', ['EPA RRP Certified Firm', 'OSHA 10 compliant', 'Registered Vermont contractor', 'Respirator fit testing',
                        'Google certified']),
         ('Insured and in good standing', ['Commercial general liability and workmanship policy', 'Workers’ compensation policy', 'Umbrella policy',
                                           'Commercial and non-owned auto policy', 'In good standing with the Vermont Secretary of State',
                                           'D-U-N-S Number (Dun &amp; Bradstreet)', 'EMR rating of 0.91 (FY26)',
                                           '100% commercial contractor pre-qualification record']),
         ('Recognized', ['Meyers Cup grand prize champions, 2024', 'UVM business pitch competition grand prize winners, 2023',
                         'Catamount Innovation Fund selection, 2022–2023'])]


def where(fn, place, note):
    """Small caption on each home photo: which job it is and where."""
    return f'<a class="where" href="{fn}"><span class="where-t">{P[fn]["title"]}</span><span class="where-l">{place} · {note}</span></a>'


page('index.html', 'Painting With Purpose · A painting company born in Vermont, for Vermonters',
     f'Residential and commercial painting, staining, sheetrock and IRC compliance inspections across {AREA}.',
     f'''<section class="h1-screen" data-dark>
  <div class="h1-media">
    <picture><source media="(max-aspect-ratio: 4/5)" srcset="assets/hero/hero-poster-tall.jpg"><img src="assets/hero/hero-poster.jpg" alt="" fetchpriority="high" decoding="async"></picture>
    <video class="hero-loop" muted loop playsinline preload="auto" aria-hidden="true" data-src="assets/hero/hero-loop-1080.mp4" data-src-sm="assets/hero/hero-loop-720.mp4" data-src-tall="assets/hero/hero-loop-tall.mp4"></video>
  </div>
  <h1 class="h1-logo"><img src="assets/logo-hero.webp" srcset="assets/logo-hero-800.webp 800w, assets/logo-hero.webp 1600w" sizes="min(72vw, 720px)" alt="Painting With Purpose, residential and commercial services" width="1600" height="1039" fetchpriority="high"></h1>
  <span class="h1-cue" aria-hidden="true"></span>
</section>

<section class="intro">
  <h2>A painting company born in Vermont, for Vermonters.</h2>
  <p class="lede">Painting With Purpose is a professional painting and staining company serving the entire state of Vermont, eastern New York and western New Hampshire. We are award-winning for our precise work and our commitment to enriching Vermont communities through charitable causes that matter to Vermonters.</p>
  {wc('leaves')}
</section>

{home_painting}

<section class="reveal" data-dark>
  <div class="reveal-pin">
    <figure class="reveal-fig">{hero_media('victorian', 'A restored Queen Anne Victorian with layered white porches', clip=False)}</figure>
    <div class="reveal-beat">{where('project-queen-anne-victorian.html', 'Burlington, Vermont', 'Full exterior restoration')}</div>
  </div>
</section>

<section class="inside">
  <div class="inside-media" data-dark>{hero_media('library', 'A library atrium with timber ceilings, a stone wall and glass doors onto fall trees', clip=False)}<div class="inside-beat">{where('project-library.html', 'Middlebury, Vermont', 'Full interior and exterior')}</div></div>
  <div class="inside-items">
    <p class="eyebrow">What we do</p>
    <ul class="inside-list">
      <li><h2>Painting</h2><p>Homes and commercial buildings, inside and out.</p></li>
      <li><h2>Staining</h2><p>Decks, porches and verandas.</p></li>
      <li><h2>Sheetrock</h2><p>Hanging, taping and repairs.</p></li>
      <li><h2>Inspections</h2><p>IRC compliance, from an EPA RRP certified firm.</p></li>
    </ul>
    <p><a class="tlink" href="services.html">All services</a></p>
  </div>
</section>

<section class="why">
  <h2>Why choose Painting With Purpose?</h2>
  <div class="why-txt">
    <p class="big">Finding an available painting company that lives up to your high quality standards can be difficult.</p>
    <p>You want experienced painters, budget-friendly pricing and top quality results. Painting With Purpose is here to fill all of your needs.</p>
    <p>Everybody on our planet seeks a purpose. Here at Painting With Purpose, there’s purpose behind every brush stroke. We design intentional scopes of work and perform every task, from beginning to end, at the highest level.</p>
    <p>1% of your base contract value goes towards the charity of your choosing after a successful closing. Painting With Purpose believes in enriching the community it has sprouted and grown from. We pledge to stick to our Vermont roots, where people help people.</p>
    <p class="why-end">Be a part of continued mission success by hiring the <em class="it">painters with a purpose</em>.</p>
  </div>
</section>

<section class="certs">
  <p class="eyebrow">Certifications &amp; accreditations</p>
  <div class="certs-grid">{"".join(f'<div><h3>{h}</h3><ul>{"".join(f"<li>{c}</li>" for c in cs)}</ul></div>' for h, cs in CERTS)}</div>
</section>

<section class="exp">
  <p class="eyebrow">The PWP experience</p>
  <ol>{"".join(f'<li><h3>{h}</h3><p>{t}</p></li>' for h, t in EXPERIENCE)}</ol>
</section>

<section class="reviews">
  <div class="reviews-head"><h2>Enough of what we have to say.</h2><p class="lede">Hear from our best-in-class clientele.</p></div>
  <ul class="reviews-list">{"".join(f'<li><blockquote>“{q}”</blockquote><p><span>{n}</span><span class="mute">Google review</span></p></li>' for q, n in REVIEWS)}</ul>
</section>

<section class="invite">
  <figure class="invite-media" id="porch-detail" data-dark data-detail-lens>{hero_media('porch', 'A freshly painted covered porch with a diamond pattern in the floor', tall_only=True, clip=False)}</figure>
  <div class="invite-txt">
    <p class="invite-beat"><a href="project-built-ins-and-porch.html">Museum renovation · Middlebury</a></p>
    <h2>{CTA}.</h2>
    <p>Careful prep, a clean site at the end of every day, and a written proposal for your project.</p>
    <p class="invite-links"><a class="tlink" href="contact.html">Request a proposal</a><a href="tel:{TEL}">802-PAINTER</a></p>
  </div>
</section>''', over=True)


# ---------------------------------------------------------------- work: a quiet index, photos appear on hover
def POSATTR(fn):
    return f' style="object-position:{POS[LEAD[fn]]}"' if LEAD[fn] in POS else ''


def peek_src(fn):
    md = LEAD[fn].replace('.jpg', '-md.jpg')
    return md if os.path.exists(md) else LEAD[fn]


def palette_attr(fn):
    """The job's paint colors as name:hex pairs, shown under the photo that follows the cursor."""
    sw = re.findall(r'background:(#[0-9A-Fa-f]{6})"></i><span>([^<]+)</span>', P[fn]['palette'])
    return '|'.join(f'{n}:{c}' for c, n in sw)


rows = ''.join(
    f'<li><a class="prow" href="{fn}" data-peek="{peek_src(fn)}" data-palette="{palette_attr(fn)}">'
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
<div class="peek" aria-hidden="true"><img alt=""><div class="peek-pal"></div></div>''', 'work.html')

# ---------------------------------------------------------------- project pages: one photograph, then words
def story(d):
    """The story behind the job, from the client: add a "story" list of paragraphs to the project in tools/projects.json."""
    return f'<div class="pj-story"><p class="eyebrow">The story</p>{"".join(f"<p>{t}</p>" for t in d["story"])}</div>' if d.get('story') else ''


for i, fn in enumerate(ORDER):
    d = P[fn]
    facts = d['facts'].replace('<dt>', '<div><dt>').replace('</dd>', '</dd></div>') + '<div><dt>Photography</dt><dd>Gabe Dunn</dd></div>'
    nxt = ORDER[(i + 1) % len(ORDER)]
    slot = LEAD[fn].split('/')[-1].replace('-wide.jpg', '') if LEAD[fn].startswith('assets/hero/') else None
    hero = hero_media(slot, plain(d['title']), eager=True, clip=slot != 'sigma') if slot else img(LEAD[fn], plain(d['title']), eager=True)
    more = f'<figure class="pj-more" data-detail-lens>{img(MORE[fn], plain(d["title"]) + ", detail", sizes="(max-width: 760px) 100vw, 70vw")}</figure>\n' if fn in MORE else ''
    lens = ' data-detail-lens' if fn == 'project-dealership.html' else ''
    body = f'''<section class="pj-hero"{lens}>{hero}</section>
<section class="pj-head">
  <p class="eyebrow">{d['kind']}</p>
  <h1>{d['title']}</h1>
  <p class="big">{d['lede']}</p>
</section>
<section class="pj-body">
  <div class="pj-text">{''.join(f'<p>{t}</p>' for t in d['text'])}{story(d)}</div>
  <div class="pj-side"><dl class="credits">{facts}</dl><p class="eyebrow">Palette</p><div class="palette">{d['palette']}</div></div>
</section>
{more}<section class="pj-next"><p class="eyebrow">Next project</p><a href="{nxt}">{P[nxt]['title']} <span>→</span></a></section>'''
    page(fn, f'{plain(d["title"])} · Painting With Purpose', plain(d['lede']), body, 'work.html', og=LEAD[fn])

# ---------------------------------------------------------------- services: words only
# (anchor, name, line under it, photo, alt, what "Learn more" opens: a checklist or a sentence)
SV = [('residential', 'Residential painting', 'We’ll restore the beauty of your home and protect it for many years to come.',
       'assets/img/pwp-0058.jpg', 'A restored Queen Anne Victorian with white porches', ('Interior painting &amp; staining', RESIDENTIAL_LIST)),
      ('commercial', 'Commercial painting', 'High quality painting for the interior and exterior of your commercial property.',
       'assets/img/pwp-0995.jpg', 'A library atrium with timber ceilings and fresh white walls', ('Exterior painting &amp; staining', COMMERCIAL_LIST)),
      ('staining', 'Staining & maintenance', 'Let our team give new life to your deck, porch, or veranda.',
       'assets/ba/deck-01-after.jpg', 'A back deck after washing and a solid stain',
       'Washing, sanding and repair first, then stain or paint for wood, composite and metal decks, porches and verandas.'),
      ('irc', 'IRC compliance inspections', 'Ensure compliance with local jurisdictions to maintain healthy and safe spaces for your tenants.',
       'assets/img/pwp-0058-gable.jpg', 'The painted gable of an older Victorian home',
       'For landlords and property managers. As an EPA RRP Certified Firm, we handle any follow-up work in older buildings lead-safe, from the first scrape.'),
      # TODO: swap in the client's drywall photo when it arrives
      ('sheetrock', 'Sheetrock hanging, taping & repairs', 'Impressive sheetrock services to complement our painting abilities.',
       'assets/ba/int-01-after.jpg', 'A finished stair hall, walls smooth and freshly painted',
       'New board hung and taped, plus repairs to holes, cracks and water damage, finished smooth and ready for paint.')]


def svc_more(k, name, more):
    body = (f'<p class="eyebrow">{more[0]}</p><ul class="svc-list">{checklist(more[1])}</ul>' if isinstance(more, tuple) else f'<p>{more}</p>')
    return f'{body}<a class="tlink" href="contact.html?service={k}#proposal">Request a proposal</a>'


svc_cards = ''.join(f'''<li id="{k}" class="svc-card">
    <figure>{img(src, alt, sizes='(max-width: 760px) 100vw, 50vw')}</figure>
    <span class="n">{i:02d}</span><h2>{html.escape(n)}</h2><p>{t}</p>
    <details><summary>Learn more</summary><div class="svc-more">{svc_more(k, n, more)}</div></details>
  </li>''' for i, (k, n, t, src, alt, more) in enumerate(SV, 1))
SERVICE_MAP = open('tools/service-area.svg', encoding='utf-8').read()
page('services.html', 'Services · Painting With Purpose',
     f'Residential and commercial painting, staining and maintenance, IRC compliance inspections, and sheetrock hanging, taping and repairs across {AREA}.',
     f'''<section class="phead">
  <p class="eyebrow">Commercial &amp; residential services</p>
  <h1>Five services, one standard.</h1>
</section>
<section class="svc"><ul class="svc-grid">{svc_cards}</ul></section>
<section class="steps">
  <p class="eyebrow">How a job runs</p>
  {wc('can')}
  <ol>
    <li><h3>Consultation</h3><p>We visit, measure and talk through colors, surfaces and repairs.</p></li>
    <li><h3>Written proposal</h3><p>Scope, schedule and price, in writing.</p></li>
    <li><h3>Prep and paint</h3><p>Protection first, then prep, then paint. The site is cleaned at the end of every day.</p></li>
    <li><h3>Final walkthrough</h3><p>We always inspect our work to make sure our standards and yours are aligned and met.</p></li>
  </ol>
</section>
<section class="area-map" id="area">
  <div class="area-txt">
    <p class="eyebrow">Where we work</p>
    <h2>All of Vermont, and a little past its borders.</h2>
    <p class="lede">Based in Winooski, we paint across Vermont, in Clinton, Essex, Warren and Washington counties in New York, and in Grafton, Sullivan and Cheshire counties in New Hampshire. Just outside the haze? Ask us anyway.</p>
  </div>
  <figure class="area-fig">{SERVICE_MAP}</figure>
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
  <p>Zach Dunn and Josh Malek started Painting With Purpose in 2022 to show that a painting company could be very good at the work and good for the place it works. In 2024 it won the first Joy and Jerry Meyers Cup at UVM. Today 1% of every base painting contract goes to a charitable cause chosen by the client. <a class="tlink" href="about.html">Our story</a></p>
  <p><a class="tlink" href="https://www.cvoeo.org/" target="_blank" rel="noopener">About CVOEO ↗</a></p>
</section>
<figure class="wc-band">{wc('church')}</figure>
<section class="quote">
  <blockquote>“Their mission for giving back to the homeless community is truly amazing.”</blockquote>
  <p class="eyebrow">Pam Mathe · Google review</p>
</section>''', 'purpose.html')

# ---------------------------------------------------------------- about: Zach's story, by year
# Copy is the polished draft of Zach's Nov 7 text (copy/about-us-v2.md), pending his final revision.
# The three photos are stand-ins until the personal shots arrive: Zach on a job, the crew at the Elm Street shop, the Meyers Cup or CVOEO.
STORY = [('2021', 'How it started', [
    'In October 2021, Zach Dunn was sitting in a marketing management class when someone from Collegiate Entrepreneurs gave a one-minute pitch for an internship that combined painting with running a business. Zach had already run Dunn Brothers Mobile Auto Detailing for two years. When the sign-up sheet came around, he wrote his name on it.',
    'Soon after, he was riding along with the manager who had made the pitch, learning about painting and how the program worked. Over the next few weeks he went to the internship meetings and learned the logistics behind the work.',
    'That same fall, Paul Dragon, president of CVOEO, spoke to Zach’s leadership and organizational behavior class. He talked about his life, his role, and what CVOEO does for the Burlington community. Zach was struck by Paul’s character and his story, and made up his mind to meet him again.',
    'Over the December break, walking through downtown Burlington, Zach saw people shivering at bus stops and on park benches, wearing jacket over jacket. He remembered that CVOEO was one of the organizations helping people without shelter, and realized that what he had learned running his own business could be put to work for them.',
    'By the end of the break, Zach had a job at Job Well Done LLC, a painting company in Burlington, and worked around his classes to learn the trade. There he became friends with Josh, a painter who had recently moved to Vermont and had been painting since high school. They had the same work ethic and the same eye for detail, and by the end of January, Zach could see the friendship becoming a partnership.']),
  ('2022', 'Painting With Purpose', [
    'On February 6, 2022, the State of Vermont granted Zach Dunn and Joshua Malek a partnership for Painting With Purpose LLC. The mission was to beautify the greater Burlington area and help solve Vermont’s homelessness crisis by partnering with CVOEO. A portion of the profit from every job would go to people in shelters working toward permanent housing, to help cover security deposits, first month’s rent and utilities.',
    'The first job came that March: a whole-house interior, with every ceiling, wall, trim and door repainted. Through the summer and fall, a four-person crew completed more than 40 jobs, large and small, and raised more than $10,500 for the cause.']),
  ('2023', 'One hundred jobs', [
    'Zach graduated in the summer of 2023. By then Painting With Purpose had passed 100 jobs, grown to 14 team members, and given $15,000 toward ending homelessness in Vermont.']),
  ('2024', 'The Meyers Cup', [
    'The UVM Grossman School of Business held the first Joy and Jerry Meyers Cup, the largest grand prize of any college entrepreneurship competition in the United States. Zach and Josh, joined by new partner Jake Falanga, spent months preparing. Painting With Purpose took the grand prize: $212,500, plus in-kind services from local businesses that had pledged to support the winner.',
    'The prize moved the company out of sheds and basements and into its own shop and office at the end of Elm Street in Winooski, where it still works from today. Late that year, Jake accepted a job in Connecticut, where he grew up, and agreed to a buyout.']),
  ('Today', 'A wider purpose', [
    'In early 2026, Josh sold his share of the company to Zach, and has since started his own painting business in Colchester, Serenity Painting.',
    'The mission has grown with the company. Every team member is treated with dignity and earns a living wage, and 1% of every base painting contract goes to a charitable cause chosen by the client.'])]
ABOUT_PHOTOS = {'2021': ('assets/img/pwp-0631-painter.jpg', 'A Painting With Purpose painter on a ladder at a red shingle colonial'),
                '2024': ('assets/img/crew-three.jpg', 'Three Painting With Purpose painters on a job, with ladders and drop cloths')}


def chapter(year, h, paras):
    ph = ABOUT_PHOTOS.get(year)
    fig = f'<figure class="ab-photo">{img(ph[0], ph[1], sizes="(max-width: 760px) 100vw, 40vw")}</figure>' if ph else ''
    return f'''<section class="ab-ch{" has-photo" if ph else ""}">
  <div class="ab-yr"><p class="eyebrow">{year}</p><h2>{h}</h2></div>
  <div class="ab-txt">{"".join(f"<p>{t}</p>" for t in paras)}</div>
  {fig}
</section>'''


page('about.html', 'About · Painting With Purpose',
     'Founded in 2022 by Zach Dunn and Josh Malek, winners of the first Meyers Cup, working from Winooski. 1% of every base contract goes to a cause the client chooses.',
     f'''<section class="phead">
  <p class="eyebrow">About us</p>
  <h1>A sign-up sheet, a cold walk, and a friendship on a paint crew.</h1>
  <p class="lede">Zach Dunn and Josh Malek founded Painting With Purpose in February 2022 to paint the greater Burlington area beautifully and help end homelessness in Vermont. Since then the company has completed well over 100 jobs, won the inaugural Joy and Jerry Meyers Cup, and works from its own shop in Winooski.</p>
</section>
<figure class="page-photo">{img('assets/img/pwp-1247.jpg', 'The Painting With Purpose booth at a street fair in a Vermont town', eager=True)}</figure>
{chr(10).join(chapter(*c) for c in STORY)}
<section class="ab-end">
  <p class="big">When you hire Painting With Purpose, you can expect careful work, clear communication, and the knowledge that part of what you pay goes back into the community we all share.</p>
  <p class="invite-links"><a class="tlink" href="contact.html">Request a free consultation</a><a href="tel:{TEL}">802-PAINTER</a></p>
</section>''', 'about.html')

# ---------------------------------------------------------------- careers
PERKS_NOW = ['$18 to $40 an hour', 'Weekly pay', 'Paid lunch, paid uniforms, and paid drives over 30 minutes to the job',
             'Flexible scheduling and vacation', 'Room to grow into a lead role', 'Paid Christmas and Thanksgiving holidays']
PERKS_6MO = ['One week of paid time off', 'Short and long term disability', '$25,000 life insurance policy']
PERKS_LATER = ['Two weeks of paid time off after three years', 'Bonuses', 'Company vehicle and gas card, for some roles']
FORMOK = '<p class="form-ok" role="status" hidden>Thanks. This demo form isn’t connected yet. On the live site it goes straight to the PWP inbox.</p>'
page('careers.html', 'Careers · Painting With Purpose', 'Painter jobs in Vermont. $18 to $40 an hour, weekly pay, paid lunch and room to grow.',
     f'''<section class="phead">
  <p class="eyebrow">Careers</p>
  <h1>Join our growing team of painters.</h1>
  {wc('ladder')}
  <p class="lede">Painting With Purpose is always looking for the right people to join our painting staff. Are you a hard worker and eager to learn? Do you have a passion for painting? Will you bring a supportive attitude to our team? If so, we’d love to hear from you.</p>
  <div class="perks-wrap">
    <div><p class="eyebrow">From day one</p><ul class="perks">{"".join(f"<li>{t}</li>" for t in PERKS_NOW)}</ul></div>
    <div><p class="eyebrow">After six months</p><ul class="perks">{"".join(f"<li>{t}</li>" for t in PERKS_6MO)}</ul></div>
    <div><p class="eyebrow">As you stay</p><ul class="perks">{"".join(f"<li>{t}</li>" for t in PERKS_LATER)}</ul></div>
  </div>
</section>
<figure class="page-photo">{img('assets/img/crew-three.jpg', 'Three Painting With Purpose painters on a job, with ladders and drop cloths', eager=True)}</figure>
<section class="roles">
  <ul><li><a href="#apply"><span class="t">Painter</span><span class="k">Full-time · Vermont</span><span class="go">Apply →</span></a></li></ul>
  {f'<p class="indeed">We also post our openings on <a class="tlink" href="{INDEED}" target="_blank" rel="noopener">Indeed ↗</a></p>' if INDEED else ''}
</section>
<section class="form-sec" id="apply">
  <h2>Join our growing team of painters and tradesmen and women.</h2>
  <form class="form" data-form novalidate>
    <label class="field"><span>Name</span><input name="name" autocomplete="name" required></label>
    <label class="field"><span>Phone</span><input name="phone" type="tel" autocomplete="tel"></label>
    <label class="field"><span>Email</span><input name="email" type="email" autocomplete="email" required></label>
    <label class="field"><span>Town you live in</span><input name="town" autocomplete="address-level2"></label>
    <label class="field"><span>Role</span><select name="role"><option>Painter</option></select></label>
    <label class="field"><span>Years of experience</span><select name="years"><option>Less than 1</option><option>1 to 2</option><option>3 to 5</option><option>6 to 10</option><option>More than 10</option></select></label>
    <label class="field"><span>Experience</span><textarea name="exp" rows="3" placeholder="Where you’ve painted, for how long, and anything else we should know"></textarea></label>
    <button class="btn submit" type="submit">Send application</button>
    {FORMOK}
  </form>
</section>''', 'careers.html')

# ---------------------------------------------------------------- contact: the porch again, as the invitation
HEARD = ['Google', 'Instagram', 'Facebook', 'Front Porch Forum', 'A friend or neighbor', 'Seen us around', 'Other']
MAP_EMBED = 'https://maps.google.com/maps?q=133+Elm+Street,+Winooski,+VT+05404&t=k&z=18&output=embed'
page('contact.html', 'Request a proposal · Painting With Purpose', f'Request your free consultation today. Call 802-PAINTER or send us your project. Serving {AREA}.',
     f'''<section class="contact">
  <figure class="contact-media">{hero_media('porch', 'A freshly painted covered porch', eager=True, tall_only=True)}</figure>
  <div class="contact-txt">
    <p class="eyebrow">Contact us</p>
    <h1 id="proposal">Request a proposal.</h1>
    <p class="lede">Our team is ready to start your next painting project, no matter how big or small. Call or text <a class="tlink" href="tel:{TEL}">802-PAINTER</a>, email <a class="tlink" href="mailto:{EMAIL}">{EMAIL}</a>, or use the form.</p>
    <p class="season">We are currently scheduling exterior painting consultations for projects to perform in exterior season 2027.</p>
    <form class="form" data-form="estimate" data-endpoint="{PORTAL_LEAD_URL}" data-org="{PORTAL_ORG}" novalidate>
      <label class="field"><span>First and last name</span><input name="name" autocomplete="name" required></label>
      <label class="field"><span>Email</span><input name="email" type="email" autocomplete="email" required></label>
      <label class="field"><span>Phone</span><input name="phone" type="tel" autocomplete="tel" inputmode="tel" required></label>
      <label class="field"><span>Address</span><input name="address" autocomplete="street-address" placeholder="Where the work is"></label>
      <label class="field"><span>Service</span><select name="service">{"".join(f'<option data-k="{s[0]}">{html.escape(s[1])}</option>' for s in SV)}<option>Not sure yet</option></select></label>
      <label class="field"><span>Tell us about your project</span><textarea name="msg" rows="3" placeholder="Rooms or surfaces, what you have in mind"></textarea></label>
      <label class="field"><span>Do you have any timing requirements?</span><input name="timing" placeholder="Optional"></label>
      <label class="field"><span>Where did you hear about us?</span><select name="heard"><option value="">Choose one</option>{"".join(f"<option>{h}</option>" for h in HEARD)}</select></label>
      <div class="hp" aria-hidden="true"><label>Leave blank<input name="hp_fax2" tabindex="-1" autocomplete="nope"></label></div>
      <button class="btn submit" type="submit">Request a proposal</button>
      <p class="consent">By sending, you agree Painting With Purpose may call or text you about this request. Message and data rates may apply. Reply STOP to opt out.</p>
      <p class="form-ok" role="status" hidden>Thanks, we have it. Someone from Painting With Purpose will be in touch soon, usually the same day.</p>
      <p class="form-err" role="alert" hidden></p>
    </form>
  </div>
</section>
<section class="visit">
  <div class="visit-txt">
    <p class="eyebrow">General information</p>
    <p class="addr-big">{ADDRESS}</p>
    <dl class="hours">{"".join(f'<div><dt>{d}</dt><dd>{h}</dd></div>' for d, h in HOURS)}</dl>
    <p class="visit-social">{" · ".join(f'<a class="tlink" href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in SOCIALS)}</p>
  </div>
  <div class="visit-map"><iframe src="{MAP_EMBED}" title="Satellite view of the Painting With Purpose office at 133 Elm Street, Winooski" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>
</section>''', 'contact.html', og='assets/hero/porch-tall.jpg')


# ---------------------------------------------------------------- portfolio: one deep collage, the bigger the job the bigger the frame
# Each tile opens the job: its story, its scope and every photo of it, prep included. Sizes: xl and l are the signature
# jobs, t is a tall frame, w a wide one, m a single cell. Order is the reading order; the grid packs the gaps.
NEVER = {'assets/img/pwp-0735.jpg', 'assets/img/pwp-1343.jpg'}
COLLAGE = [('project-sigma-phi-house.html', 'xl'), ('ext-07', 't'), ('com-02', 'l'), ('project-queen-anne-victorian.html', 'xl'),
           ('int-03', 'w'), ('ext-02', 't'), ('project-library.html', 'xl'), ('deck-02', 'm'), ('ext-05', 't'),
           ('project-built-ins-and-porch.html', 'l'), ('int-02', 'w'), ('ext-04', 't'), ('project-red-shingle-colonial.html', 'l'),
           ('int-01', 'm'), ('deck-04', 't'), ('project-lake-cottage.html', 'l'), ('deck-01', 'w'), ('ext-03', 't'), ('ext-06', 't'),
           ('project-dealership.html', 'l'), ('ext-08', 'm'), ('deck-03', 'w'), ('ext-09', 't'), ('int-04', 'm'), ('ext-01', 'm'),
           ('rot-01', 'm'), ('int-05', 'm')]
TFD = {t['id']: t for t in TF}


def thumb(src):
    for v in (src.replace('.jpg', '-md.jpg'), src.replace('.jpg', '-th.jpg')):
        if os.path.exists(v):
            return v
    return src


def job(key):
    """(id, title, eyebrow, note, tile photo, [(photo, label)], project page) for a project page or a transformation."""
    if key in P:
        d = P[key]
        pics = [LEAD[key]] + [g[1] for g in d.get('gallery', [])] + ([MORE[key]] if key in MORE else [])
        pics = [x for i, x in enumerate(pics) if x not in pics[:i] and x not in NEVER]
        return (key.replace('.html', ''), d['title'], d['kind'], d['lede'], LEAD[key], [(x, '') for x in pics], key)
    t = TFD[key]
    return (key, t['title'], t['cat'].capitalize(), t['note'], f'assets/ba/{key}-after.jpg',
            [(f'assets/ba/{key}-after.jpg', 'Finished'), (f'assets/ba/{key}-before.jpg', 'Where it started')], None)


def tile(key, size):
    k, title, eyebrow, note, src, pics, link = job(key)
    return (f'<li class="cl cl-{size}"><button type="button" data-job="{k}" aria-haspopup="dialog">'
            f'<img src="{thumb(src)}" alt="" loading="lazy" decoding="async"{POSATTR(key) if key in P else ""}>'
            f'<span class="cl-cap"><span class="cl-e">{eyebrow}</span><span class="cl-t">{title}</span></span></button></li>')


def job_sheet(key):
    k, title, eyebrow, note, src, pics, link = job(key)
    figs = ''.join(f'<figure>{img(x, plain(title) + ", " + (lab.lower() or "photo " + str(i + 1)), sizes="(max-width: 760px) 100vw, 60vw")}'
                   + (f'<figcaption>{lab}</figcaption>' if lab else '') + '</figure>' for i, (x, lab) in enumerate(pics))
    side = f'<dl class="credits">{P[key]["facts"].replace("<dt>", "<div><dt>").replace("</dd>", "</dd></div>")}</dl>' if link else ''
    more = f'<p><a class="tlink" href="{link}">The full project</a></p>' if link else ''
    return f'''<article class="job" id="job-{k}" hidden>
    <div class="job-pics">{figs}</div>
    <div class="job-txt"><p class="eyebrow">{eyebrow}</p><h2>{title}</h2><p>{note}</p>{side}{more}</div>
  </article>'''


page('transformations.html', 'Portfolio · Painting With Purpose', 'A collage of Painting With Purpose jobs across Vermont, from fraternity houses and libraries to porches and kitchens.',
     f'''<section class="phead">
  <p class="eyebrow">Portfolio</p>
  <h1>Work we sign our name to.</h1>
  <p class="lede">The bigger the job, the bigger the frame. Open any photo for the story, the scope and the prep behind it.</p>
</section>
<section class="collage" aria-label="Portfolio"><ul>{"".join(tile(k, z) for k, z in COLLAGE)}</ul></section>
<dialog class="job-dlg" aria-label="Job details">
  <button class="job-x" type="button" data-close>Close</button>
  {"".join(job_sheet(k) for k, _ in COLLAGE)}
</dialog>''', 'transformations.html')
# ---------------------------------------------------------------- 404 (Vercel serves 404.html for missing paths)
page('404.html', 'Page not found · Painting With Purpose', 'This page could not be found.',
     '''<section class="phead nf">
  <p class="eyebrow">404</p>
  <h1>This page isn’t here.</h1>
  <p class="lede">The link may be old, or the page may have moved.</p>
  <p class="nf-links"><a class="tlink" href="index.html">Home</a><a class="tlink" href="work.html">Work</a><a class="tlink" href="contact.html">Contact</a></p>
</section>''')
# the 404 can be served at any depth, so its links start from the site root
nf = open('404.html', encoding='utf-8').read()
for attr in ('href="', 'src="', 'srcset="'):
    nf = nf.replace(attr + 'assets/', attr + '/assets/')
import re
nf = re.sub(r'href="([a-z0-9-]+\.html)', r'href="/\1', nf)
open('404.html', 'w', encoding='utf-8').write(nf)
print('built')

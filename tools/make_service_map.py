"""Draws the service-area map (tools/service-area.svg) from US Census county shapes.

The shapes come from the us-atlas package (counties-10m.json, TopoJSON). Download it once, then run from the repo root:
  curl -L -o counties-10m.json https://cdn.jsdelivr.net/npm/us-atlas@3.0.1/counties-10m.json
  python -X utf8 tools/make_service_map.py counties-10m.json
build.py inlines the SVG on the services page.
"""
import json
import math
import sys

# all of Vermont, plus these neighbouring counties (FIPS codes)
AREA_STATES = {'50'}
AREA_COUNTIES = {'36019': 'Clinton', '36031': 'Essex', '36113': 'Warren', '36115': 'Washington',
                 '33009': 'Grafton', '33019': 'Sullivan', '33005': 'Cheshire'}
CONTEXT_STATES = {'50', '36', '33', '25', '09', '44', '23'}
WEST, EAST, SOUTH, NORTH = -74.75, -71.05, 42.55, 45.2
W = 760
K = W / ((EAST - WEST) * math.cos(math.radians((SOUTH + NORTH) / 2)))
H = round((NORTH - SOUTH) * K)
CITIES = [('Winooski', 44.4914, -73.1857, 'office'), ('Montpelier', 44.2601, -72.5754, ''), ('Rutland', 43.6106, -72.9726, ''),
          ('Brattleboro', 42.8509, -72.5579, ''), ('St. Johnsbury', 44.4192, -72.0151, ''), ('Plattsburgh', 44.6995, -73.4529, ''),
          ('Glens Falls', 43.3095, -73.6440, ''), ('Lebanon', 43.6423, -72.2518, ''), ('Keene', 42.9337, -72.2781, '')]
STATE_LABELS = [('VERMONT', 44.05, -72.78), ('NEW YORK', 43.05, -74.35), ('NEW HAMPSHIRE', 43.25, -71.6),
                ('MASSACHUSETTS', 42.62, -72.0), ('QUÉBEC', 45.12, -72.9)]


def xy(lon, lat):
    return (lon - WEST) * K * math.cos(math.radians((SOUTH + NORTH) / 2)), (NORTH - lat) * K


def main(src):
    topo = json.load(open(src, encoding='utf-8'))
    sx, sy = topo['transform']['scale']
    tx, ty = topo['transform']['translate']
    arcs = []
    for a in topo['arcs']:
        x = y = 0
        pts = []
        for dx, dy in a:
            x += dx
            y += dy
            pts.append((x * sx + tx, y * sy + ty))
        arcs.append(pts)

    def ring(idx):
        pts = []
        for i in idx:
            seg = arcs[i] if i >= 0 else arcs[~i][::-1]
            pts.extend(seg if not pts else seg[1:])
        return pts

    def path(geom):
        polys = geom['arcs'] if geom['type'] == 'MultiPolygon' else [geom['arcs']]
        out = []
        for poly in polys:
            for r in poly:
                p = [xy(*q) for q in ring(r)]
                out.append('M' + 'L'.join(f'{x:.1f},{y:.1f}' for x, y in p) + 'Z')
        return ''.join(out)

    states = [g for g in topo['objects']['states']['geometries'] if g['id'] in CONTEXT_STATES]
    area = [g for g in topo['objects']['counties']['geometries']
            if g['id'][:2] in AREA_STATES or g['id'] in AREA_COUNTIES]
    area_d = ''.join(path(g) for g in area)
    states_d = ''.join(path(g) for g in states)

    labels = ''.join(f'<text class="sa-st" x="{x:.0f}" y="{y:.0f}">{n}</text>' for n, la, lo in STATE_LABELS for x, y in [xy(lo, la)])
    cities = ''
    for n, la, lo, kind in CITIES:
        x, y = xy(lo, la)
        if kind == 'office':
            cities += f'<circle class="sa-office" cx="{x:.1f}" cy="{y:.1f}" r="5.5"/><text class="sa-city sa-hq" x="{x - 9:.1f}" y="{y + 4:.1f}" text-anchor="end">{n}</text>'
        else:
            cities += f'<circle class="sa-dot" cx="{x:.1f}" cy="{y:.1f}" r="2.5"/><text class="sa-city" x="{x + 7:.1f}" y="{y + 4:.1f}">{n}</text>'

    svg = (f'<svg class="sa-map" viewBox="0 0 {W} {H}" role="img" aria-labelledby="sa-t">'
           f'<title id="sa-t">Service area: all of Vermont, plus Clinton, Essex, Warren and Washington counties in New York '
           f'and Grafton, Sullivan and Cheshire counties in New Hampshire</title>'
           f'<defs><filter id="sa-haze" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="7"/></filter></defs>'
           f'<path class="sa-land" d="{states_d}"/>'
           f'<g class="sa-haze" filter="url(#sa-haze)"><path class="sa-area" d="{area_d}"/></g>'
           f'<path class="sa-lines" d="{states_d}"/>{labels}{cities}</svg>')
    open('tools/service-area.svg', 'w', encoding='utf-8').write(svg)
    print(f'wrote tools/service-area.svg ({len(svg) // 1024} KB, {len(area)} counties)')


main(sys.argv[1])

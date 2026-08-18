# -*- coding: utf-8 -*-
# ─────────────────────────────────────────────────────────────────────────
# PARKED, 13 Aug 2026. The generated topographic maps are out of the live
# site: the owner is supplying route artwork instead, dropped in as
# assets/images/route-map-<slug>.jpg.
#
# Nothing here is called by the build. It is kept whole, and working, because
# the geography in scripts/routes/<slug>.json is real and re-deriving it would
# be wasteful if drawn maps do not work out. To bring it back: re-add the
# routemap import in explore-build.py, swap route_slot() for routemap.render(),
# restore the OpenTopoMap attribution line, and re-run this script per slug.
#
# The attribution is a licence condition of OpenTopoMap (CC-BY-SA). If this
# ever ships again, the credit line ships with it.
# ─────────────────────────────────────────────────────────────────────────
"""Reusable route map and altitude profile, emitted as static inline SVG.

The base is a real topographic image, built once by scripts/make-route-map.py
and committed, so the page never calls a tile server. The overlay projects
every stop and peak into the same Web Mercator frame the tiles were drawn in,
using the bounds in the image's sidecar, which is what makes a village marker
land on the village.

The line between stops is still a schematic, not a traced trail: it wanders a
little so it reads as a drawn route rather than a GPS track it is not.

Nothing here is specific to Everest Base Camp. Feed it another route and its
sidecar and it draws that one.
"""
import io, json, math, os

# deterministic wobble, so a rebuild produces a byte identical map
_SEED = [20260812]


def _rnd():
    _SEED[0] = (_SEED[0] * 1103515245 + 12345) & 0x7FFFFFFF
    return _SEED[0] / 0x7FFFFFFF * 2 - 1          # -1 .. 1


def _mx(lon):
    return (lon + 180.0) / 360.0


def _my(lat):
    r = math.radians(lat)
    return (1.0 - math.log(math.tan(r) + 1.0 / math.cos(r)) / math.pi) / 2.0


class Projection(object):
    """Web Mercator, locked to the base image's own bounds.

    The tiles are Web Mercator, so the overlay has to be too. Anything else
    drifts: over the 44 km this route covers, treating latitude as linear puts
    the top of the map tens of pixels out of place."""

    def __init__(self, meta):
        self.w, self.h = float(meta['width']), float(meta['height'])
        self.x0, self.x1 = _mx(meta['west']), _mx(meta['east'])
        self.y0, self.y1 = _my(meta['north']), _my(meta['south'])

    def xy(self, lat, lon):
        return ((_mx(lon) - self.x0) / (self.x1 - self.x0) * self.w,
                (_my(lat) - self.y0) / (self.y1 - self.y0) * self.h)


def load_meta(slug, repo=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))):
    p = os.path.join(repo, 'assets', 'images', 'map-%s.json' % slug)
    assert os.path.exists(p), 'no base image for %s: run scripts/make-route-map.py %s' % (slug, slug)
    return json.load(io.open(p, encoding='utf-8'))


def _wobbly(points, amp=7.0, per_seg=3):
    """A path through the points with a light hand drawn wander between them."""
    d = ['M %.1f %.1f' % points[0]]
    for i in range(len(points) - 1):
        (x1, y1), (x2, y2) = points[i], points[i + 1]
        dx, dy = x2 - x1, y2 - y1
        ln = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / ln, dx / ln              # unit normal
        for s in range(1, per_seg + 1):
            t = s / float(per_seg)
            # the control point sits half a step back, pushed off the straight line
            tc = t - 0.5 / per_seg
            off = _rnd() * amp * (1 if s < per_seg or i == len(points) - 2 else 0.4)
            cx, cy = x1 + dx * tc + nx * off, y1 + dy * tc + ny * off
            ex, ey = x1 + dx * t, y1 + dy * t
            if s == per_seg:
                ex, ey = x2, y2
            d.append('Q %.1f %.1f %.1f %.1f' % (cx, cy, ex, ey))
    return ' '.join(d)


def _peak(x, y, w, h, wobble=2.0):
    """Line art triangle, base flat, with a small kink so it is not machined."""
    return 'M %.1f %.1f L %.1f %.1f L %.1f %.1f L %.1f %.1f' % (
        x - w / 2, y, x - w * 0.12 + _rnd() * wobble, y - h * 0.62,
        x + _rnd() * wobble, y - h, x + w / 2, y)


def render(route, slug):
    """Return the full figure: map, legend, altitude profile, and a text
    description that carries the same information for a screen reader."""
    stops, peaks, prof = route['stops'], route['peaks'], route['profile']
    meta = load_meta(slug)
    p = Projection(meta)
    W, H = p.w, p.h

    # ── the walked line ───────────────────────────────────────────────────
    main = [s for s in stops if not s.get('spur')]
    spur = [s for s in stops if s.get('spur')]
    pts = [p.xy(s['lat'], s['lon']) for s in main]
    path = _wobbly(pts)

    spur_paths = []
    for s in spur:
        anchor = next(m for m in main if m['name'] == s['from'])
        spur_paths.append(_wobbly([p.xy(anchor['lat'], anchor['lon']), p.xy(s['lat'], s['lon'])],
                                  amp=4.0, per_seg=2))

    out = []
    out.append('<svg class="rm-svg" viewBox="0 0 %.0f %.0f" preserveAspectRatio="xMidYMid meet" '
               'role="img" aria-hidden="true" focusable="false">' % (W, H))
    # the topographic base, self hosted, built by scripts/make-route-map.py
    out.append('  <image class="rm-base" href="assets/images/map-%s.jpg" x="0" y="0" '
               'width="%.0f" height="%.0f" preserveAspectRatio="none"/>' % (slug, W, H))

    # peaks first, they sit behind the route
    # Everest, Lhotse and Nuptse sit within a few kilometres of each other, so
    # the glyphs stay small and each peak carries its own label placement.
    for pk in peaks:
        x, y = p.xy(pk['lat'], pk['lon'])
        w, h = pk.get('w', 52), pk.get('h', 38)
        out.append('  <path class="rm-peak" d="%s"/>' % _peak(x, y, w, h))
        lx, ly = x + pk.get('lx', 0), y + pk.get('ly', 26)
        anc = pk.get('anchor', 'middle')
        out.append('  <text class="rm-peak-name rm-halo" x="%.1f" y="%.1f" text-anchor="%s">%s</text>'
                   % (lx, ly, anc, pk['name']))
        out.append('  <text class="rm-peak-alt rm-alt rm-halo" x="%.1f" y="%.1f" text-anchor="%s">%s m</text>'
                   % (lx, ly + 22, anc, format(pk['alt'], ',')))

    out.append('  <path class="rm-route" d="%s"/>' % path)
    for sp in spur_paths:
        out.append('  <path class="rm-route rm-route--spur" d="%s"/>' % sp)

    # stops
    for s in stops:
        x, y = p.xy(s['lat'], s['lon'])
        anchor = s.get('label', 'left')
        tx = x - 26 if anchor == 'left' else x + 26
        ta = 'end' if anchor == 'left' else 'start'
        if s.get('viewpoint'):
            out.append('  <g class="rm-view"><circle cx="%.1f" cy="%.1f" r="15"/>'
                       '<path d="M %.1f %.1f l 9 -9 l 9 9" /></g>' % (x, y, x - 9, y + 4))
        elif s.get('days'):
            txt = '\u00b7'.join(str(d) for d in s['days'])
            if len(s['days']) > 1:
                w = 20 + 15 * len(txt)
                out.append('  <rect class="rm-stop" x="%.1f" y="%.1f" width="%.1f" height="34" '
                           'rx="17"/>' % (x - w / 2, y - 17, w))
            else:
                out.append('  <circle class="rm-stop" cx="%.1f" cy="%.1f" r="17"/>' % (x, y))
            out.append('  <text class="rm-day" x="%.1f" y="%.1f">%s</text>' % (x, y, txt))
        else:
            out.append('  <circle class="rm-node" cx="%.1f" cy="%.1f" r="8"/>' % (x, y))
        ly = y + s.get('dy', 0)
        out.append('  <text class="rm-place rm-halo" x="%.1f" y="%.1f" text-anchor="%s">%s</text>'
                   % (tx, ly - 1, ta, s.get('short', s['name'])))
        out.append('  <text class="rm-place-alt rm-alt rm-halo" x="%.1f" y="%.1f" text-anchor="%s">%s m</text>'
                   % (tx, ly + 20, ta, format(s['alt'], ',')))
    out.append('</svg>')
    svg_map = '\n'.join(out)

    # ── legend ────────────────────────────────────────────────────────────
    top = max(s['alt'] for s in stops)
    legend = '''<ul class="rm-legend">
    <li><svg class="rm-key" viewBox="0 0 30 16" aria-hidden="true"><path class="rm-route" d="M2 12 Q 9 4 15 9 T 28 5"/></svg>Route</li>
    <li><svg class="rm-key" viewBox="0 0 30 16" aria-hidden="true"><circle class="rm-stop" cx="15" cy="8" r="7"/></svg>Overnight stop, with day</li>
    <li><svg class="rm-key" viewBox="0 0 30 16" aria-hidden="true"><path class="rm-peak" d="M4 14 L 13 3 L 22 14"/></svg>Peak</li>
    <li><svg class="rm-key" viewBox="0 0 30 16" aria-hidden="true"><g class="rm-view"><circle cx="15" cy="8" r="6.5"/><path d="M11 10 l4 -4 l4 4"/></g></svg>Viewpoint</li>
    <li><span class="rm-max">Highest point %s m</span></li>
  </ul>''' % format(top, ',')

    # ── altitude profile ──────────────────────────────────────────────────
    PW, PH = 900.0, 330.0
    ml, mr, mt, mb = 66.0, 30.0, 34.0, 52.0
    days = [d['day'] for d in prof]
    alts = [d['alt'] for d in prof] + [d['touch'] for d in prof if d.get('touch')]
    amin, amax = 0, max(alts)
    amax_r = int(math.ceil(amax / 500.0) * 500)

    def px_(day):
        return ml + (day - days[0]) / float(days[-1] - days[0]) * (PW - ml - mr)

    def py_(alt):
        return PH - mb - (alt - amin) / float(amax_r - amin) * (PH - mt - mb)

    line = [(px_(d['day']), py_(d['alt'])) for d in prof]
    area = 'M %.1f %.1f ' % (line[0][0], PH - mb) + \
           ' '.join('L %.1f %.1f' % xy for xy in line) + \
           ' L %.1f %.1f Z' % (line[-1][0], PH - mb)
    poly = 'M ' + ' L '.join('%.1f %.1f' % xy for xy in line)

    q = ['<svg class="rm-profile" viewBox="0 0 %.0f %.0f" preserveAspectRatio="xMidYMid meet" '
         'role="img" aria-hidden="true" focusable="false">' % (PW, PH)]
    for a in range(0, amax_r + 1, 1000):
        y = py_(a)
        q.append('  <line class="rm-grid" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (ml, y, PW - mr, y))
        q.append('  <text class="rm-axis" x="%.1f" y="%.1f" text-anchor="end">%s</text>'
                 % (ml - 12, y + 5, format(a, ',')))
    q.append('  <path class="rm-area" d="%s"/>' % area)
    q.append('  <path class="rm-line" d="%s"/>' % poly)
    for d in prof:
        x, y = px_(d['day']), py_(d['alt'])
        q.append('  <circle class="rm-dot" cx="%.1f" cy="%.1f" r="4.5"/>' % (x, y))
        q.append('  <text class="rm-axis" x="%.1f" y="%.1f" text-anchor="middle">%d</text>'
                 % (x, PH - mb + 26, d['day']))
        if d.get('touch'):
            ty = py_(d['touch'])
            q.append('  <line class="rm-riser" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (x, y, x, ty))
            q.append('  <circle class="rm-touch" cx="%.1f" cy="%.1f" r="5.5"/>' % (x, ty))
        if d.get('label'):
            # neighbouring days are only ~55 units apart, narrower than the
            # labels, so a crowded pair is separated sideways not just vertically
            ly = py_(d.get('touch') or d['alt']) - 18 + d.get('ldy', 0)
            q.append('  <text class="rm-plabel" x="%.1f" y="%.1f" text-anchor="%s">%s</text>'
                     % (x + d.get('ldx', 0), ly, d.get('lanchor', 'middle'), d['label']))
    q.append('  <text class="rm-axis rm-axis-title" x="%.1f" y="%.1f" text-anchor="middle">Day</text>'
             % ((ml + PW - mr) / 2, PH - 6))
    q.append('</svg>')
    svg_prof = '\n'.join(q)

    # ── the same information, in words ────────────────────────────────────
    words = []
    for s in main:
        bit = '%s at %s metres' % (s['name'], format(s['alt'], ','))
        if s.get('days'):
            bit += ' (night %s)' % (' and '.join(str(d) for d in s['days']))
        words.append(bit)
    for s in spur:
        words.append('a side trip from %s to %s at %s metres' %
                     (s['from'], s['name'], format(s['alt'], ',')))
    desc = ('Route map on a topographic base. The trail runs south to north up the valley: %s. '
            'Peaks in view: %s. The profile chart below plots the altitude slept at on each of '
            'the %d days, rising to a high point of %s metres.'
            % ('; then '.join(words),
               ', '.join('%s at %s metres' % (pk['name'], format(pk['alt'], ',')) for pk in peaks),
               len(prof), format(top, ',')))

    return '''<figure class="routemap" role="group" aria-labelledby="rm-t-%s" aria-describedby="rm-d-%s">
  <figcaption class="rm-caption" id="rm-t-%s">Route and altitude</figcaption>
  <p class="rm-desc" id="rm-d-%s">%s</p>
  <div class="rm-frame">
%s
  </div>
  <p class="rm-credit">%s</p>
  %s
  <div class="rm-frame rm-frame--profile">
%s
  </div>
</figure>''' % (slug, slug, slug, slug, desc, svg_map, meta['attribution'], legend, svg_prof)

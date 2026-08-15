#!/usr/bin/env python3
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
"""Build a self-hosted topographic base image for one journey's route map.

    python3 scripts/make-route-map.py <slug> [--zoom 13] [--budget 400]

Reads scripts/routes/<slug>.json (the stops and peaks, with real coordinates),
works out the bounding box, pulls the OpenTopoMap tiles that cover it, stitches
them, crops to the box and writes:

    assets/images/map-<slug>.jpg     the base image the page ships
    assets/images/map-<slug>.json    its exact geographic bounds and pixel size

The sidecar is what lets the SVG overlay line up with the terrain: the page
projects lat/lon into the same Web Mercator frame the tiles are drawn in, so a
village marker sits on the village.

WHY THE IMAGE IS BAKED IN. The page must never call a tile server at runtime:
that would be a third party request on every visit, it would break offline, and
it leans on someone else's bandwidth forever. This script runs once per journey,
by hand, and the result is committed.

LICENCE. OpenTopoMap is CC-BY-SA and the underlying data is ODbL. The
attribution line under the map on the page is a condition of use, not a
courtesy. Do not remove it.

Tiles are cached under .tilecache/ so a re-run costs the tile server nothing.
"""
import argparse, io, json, math, os, sys, time, urllib.error, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CACHE = os.path.join(REPO, '.tilecache')
TILE = 256
# a real contact string, as the tile usage policy asks for
UA = ('themountaindiaries.com route-map builder/1.0 (one-off static export, '
      'self-hosted result; contact hello@themountaindiaries.com)')
SERVERS = ['a', 'b', 'c']


def lon2px(lon, z):
    return (lon + 180.0) / 360.0 * (2 ** z) * TILE


def lat2px(lat, z):
    r = math.radians(lat)
    return (1.0 - math.log(math.tan(r) + 1.0 / math.cos(r)) / math.pi) / 2.0 * (2 ** z) * TILE


def px2lon(x, z):
    return x / ((2 ** z) * TILE) * 360.0 - 180.0


def px2lat(y, z):
    n = math.pi - 2.0 * math.pi * y / ((2 ** z) * TILE)
    return math.degrees(math.atan(0.5 * (math.exp(n) - math.exp(-n))))


def fetch_tile(z, x, y, pause):
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, '%d_%d_%d.png' % (z, x, y))
    if os.path.exists(path):
        return path, True
    url = 'https://%s.tile.opentopomap.org/%d/%d/%d.png' % (SERVERS[(x + y) % 3], z, x, y)
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read()
            if not data:
                raise IOError('empty body')
            with open(path, 'wb') as f:
                f.write(data)
            time.sleep(pause)          # the tile server is a volunteer project
            return path, False
        except Exception as e:
            if attempt == 2:
                raise SystemExit('tile %d/%d/%d failed: %s' % (z, x, y, e))
            time.sleep(1.5 * (attempt + 1))


def build(slug, zoom, budget_kb, margin, max_width):
    from PIL import Image

    route = json.load(io.open(os.path.join(HERE, 'routes', '%s.json' % slug), encoding='utf-8'))
    pts = [(p['lat'], p['lon']) for p in route['stops'] + route['peaks']]
    lats = [p[0] for p in pts]
    lons = [p[1] for p in pts]
    # Margins are per side: the labels do not sit symmetrically around the
    # route, so neither should the crop. A route file may override any side.
    m = dict(w=margin, e=margin, n=margin, s=margin)
    m.update(route.get('margin') or {})
    span_lat, span_lon = max(lats) - min(lats), max(lons) - min(lons)
    north, south = max(lats) + span_lat * m['n'], min(lats) - span_lat * m['s']
    west, east = min(lons) - span_lon * m['w'], max(lons) + span_lon * m['e']

    # exact pixel window we want, in this zoom's world pixel frame
    x0, x1 = lon2px(west, zoom), lon2px(east, zoom)
    y0, y1 = lat2px(north, zoom), lat2px(south, zoom)
    tx0, tx1 = int(x0 // TILE), int(x1 // TILE)
    ty0, ty1 = int(y0 // TILE), int(y1 // TILE)
    nx, ny = tx1 - tx0 + 1, ty1 - ty0 + 1
    print('%s: bbox %.4f..%.4f N, %.4f..%.4f E' % (slug, south, north, west, east))
    print('  zoom %d, %d x %d = %d tiles' % (zoom, nx, ny, nx * ny))

    sheet = Image.new('RGB', (nx * TILE, ny * TILE))
    cached = 0
    for i, tx in enumerate(range(tx0, tx1 + 1)):
        for j, ty in enumerate(range(ty0, ty1 + 1)):
            path, was_cached = fetch_tile(zoom, tx, ty, 0.12)
            cached += was_cached
            sheet.paste(Image.open(path).convert('RGB'), (i * TILE, j * TILE))
    print('  %d tiles from cache, %d downloaded' % (cached, nx * ny - cached))

    # crop to the exact window
    ox, oy = tx0 * TILE, ty0 * TILE
    box = (int(round(x0 - ox)), int(round(y0 - oy)), int(round(x1 - ox)), int(round(y1 - oy)))
    img = sheet.crop(box)
    full_w, full_h = img.size
    print('  cropped %d x %d px' % (full_w, full_h))

    # The image is decoration under a vector overlay, so it can be resampled
    # down to whatever keeps the file inside budget. Take the largest width and
    # highest quality that fits, rather than a fixed guess.
    best = None
    for w in [x for x in max_width if x <= full_w] or [full_w]:
        h = int(round(full_h * w / float(full_w)))
        small = img.resize((w, h), Image.LANCZOS)
        for q in (82, 78, 74, 70, 66):
            buf = io.BytesIO()
            small.save(buf, 'JPEG', quality=q, optimize=True, progressive=True, subsampling=0)
            kb = buf.tell() / 1024.0
            if kb <= budget_kb:
                best = (kb, w, h, q, buf.getvalue())
                break
        if best:
            break
    if not best:
        raise SystemExit('could not reach %d KB; lower --zoom or widen --budget' % budget_kb)

    kb, w, h, q, blob = best
    out = os.path.join(REPO, 'assets', 'images', 'map-%s.jpg' % slug)
    with open(out, 'wb') as f:
        f.write(blob)
    print('  wrote %s  %d x %d, quality %d, %.0f KB' % (os.path.relpath(out, REPO), w, h, q, kb))

    # the sidecar the overlay projects against
    meta = {
        'slug': slug, 'zoom': zoom,
        'north': px2lat(y0, zoom), 'south': px2lat(y1, zoom),
        'west': px2lon(x0, zoom), 'east': px2lon(x1, zoom),
        'width': w, 'height': h,
        'source': 'OpenTopoMap', 'licence': 'CC-BY-SA',
        'attribution': ('Map data © OpenStreetMap contributors, SRTM · '
                        'Map style © OpenTopoMap (CC-BY-SA)'),
    }
    mp = os.path.join(REPO, 'assets', 'images', 'map-%s.json' % slug)
    io.open(mp, 'w', encoding='utf-8').write(json.dumps(meta, indent=2) + '\n')
    print('  wrote %s' % os.path.relpath(mp, REPO))
    return meta


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('slug')
    ap.add_argument('--zoom', type=int, default=13)
    ap.add_argument('--budget', type=int, default=400, help='max KB for the jpg')
    ap.add_argument('--margin', type=float, default=0.12, help='padding as a fraction of the span')
    ap.add_argument('--widths', default='1600,1400,1200,1050,900')
    a = ap.parse_args()
    build(a.slug, a.zoom, a.budget, a.margin, [int(x) for x in a.widths.split(',')])

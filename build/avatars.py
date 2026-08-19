#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the platform avatar and banner set in brand/avatars/.

    python3 build/avatars.py

Like build/brand.py, this is deliberately NOT part of build/build.py. It reads
the canonical artwork in assets/ and writes committed output.

The avatars are circle-crop safe. Social platforms mask a square upload to a
circle, and the crop is not the same everywhere, so the monogram is scaled to
sit entirely inside a circle of CIRCLE of the canvas diameter. Platforms crop
at roughly 90 to 100 per cent, so that leaves real margin on every side rather
than the letterforms grazing the mask.

Fitting is done on the monogram bounding box diagonal, which is the worst case:
if the diagonal fits the circle, every part of the mark does.
"""
import io
import math
import os
import shutil
import struct
import subprocess
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
ASSETS = os.path.join(REPO, 'assets')
OUT = os.path.join(REPO, 'brand', 'avatars')

CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

SNOW = '#FAFAF7'
INK = '#2E3438'
SIENNA = '#B85C38'

# Fraction of the canvas diameter the monogram must fit inside.
CIRCLE = 0.78

AVATAR_SIZES = [1080, 800, 400, 320, 200]

# name, background, mark, note for the README
COLOURWAYS = [
    ('sienna', SIENNA, SNOW, 'primary, the most distinctive at thumbnail size'),
    ('snow', SNOW, INK, 'light alternative, for pale or busy surroundings'),
]

# label, width, height, wordmark height as a fraction of banner height,
# left margin as a fraction of banner width
BANNERS = [
    ('x-header', 1500, 500, 0.26, 0.073),
    ('linkedin-cover', 1128, 191, 0.38, 0.057),
]

SVG_TPL = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" role="img" '
           'aria-label="%s">%s%s</svg>\n')


def _n(v):
    return ('%.4f' % v).rstrip('0').rstrip('.')


def load(name):
    s = io.open(os.path.join(ASSETS, name), encoding='utf-8').read()
    import re
    d = re.search(r'\sd="([^"]+)"', s).group(1)
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', s).group(1).split()]
    return d, vb


def bg_rect(x0, y0, w, h, fill):
    """Background bled past the viewBox so a rounded pixel canvas cannot leave
    a transparent sliver down the edge. The viewport clips the overspill."""
    b = max(w, h) * 0.02
    return '<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (
        _n(x0 - b), _n(y0 - b), _n(w + 2 * b), _n(h + 2 * b), fill)


def render(svg_text, w, h, dest):
    tmp = os.path.join(OUT, '.render.html')
    io.open(tmp, 'w', encoding='utf-8').write(
        '<html><head><meta charset="utf-8"><style>html,body{margin:0;padding:0;'
        'background:transparent}svg{display:block;width:%dpx;height:%dpx}</style>'
        '</head><body>%s</body></html>' % (w, h, svg_text))
    r = subprocess.run(
        [CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars',
         '--default-background-color=00000000', '--force-device-scale-factor=1',
         '--window-size=%d,%d' % (w, h), '--screenshot=' + dest, 'file://' + tmp],
        capture_output=True, text=True)
    os.remove(tmp)
    if not os.path.exists(dest):
        sys.stderr.write(r.stdout + r.stderr)
        raise SystemExit('render failed: %s' % dest)
    d = open(dest, 'rb').read(24)
    gw, gh = struct.unpack('>II', d[16:24])
    if (gw, gh) != (w, h):
        raise SystemExit('%s came out %dx%d, wanted %dx%d' % (dest, gw, gh, w, h))


def main():
    if not os.path.exists(CHROME):
        raise SystemExit('no Chrome at %s' % CHROME)

    mo_d, mo_vb = load('monogram-tmd.svg')
    wm_d, wm_vb = load('wordmark.svg')
    mw, mh = mo_vb[2], mo_vb[3]
    diag = math.hypot(mw, mh)

    # Square viewBox whose CIRCLE-diameter inscribed circle exactly contains
    # the monogram bounding box.
    span = diag / CIRCLE
    x0 = mw / 2.0 - span / 2.0
    y0 = mh / 2.0 - span / 2.0

    print('circle fit:')
    print('  monogram %.2f x %.2f, bbox diagonal %.3f' % (mw, mh, diag))
    print('  square viewBox side %.4f, circle %.0f%% of canvas' % (span, CIRCLE * 100))
    print('  at 1080 px the monogram is %.1f x %.1f px, %.1f%% of canvas width'
          % (mw / span * 1080, mh / span * 1080, 100 * mw / span))

    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)

    made = []
    print('\navatars:')
    for name, bg, fg, _note in COLOURWAYS:
        svg = SVG_TPL % (
            '%s %s %s %s' % (_n(x0), _n(y0), _n(span), _n(span)),
            'The Mountain Diaries',
            bg_rect(x0, y0, span, span, bg),
            '<path fill="%s" d="%s"/>' % (fg, mo_d))
        sp = os.path.join(OUT, 'avatar-%s.svg' % name)
        io.open(sp, 'w', encoding='utf-8').write(svg)
        made.append(sp)
        for s in AVATAR_SIZES:
            dest = os.path.join(OUT, 'avatar-%s-%d.png' % (name, s))
            render(svg, s, s, dest)
            made.append(dest)
            print('  avatar-%s-%d.png  %d x %d  monogram %.0f px wide'
                  % (name, s, s, s, mw / span * s))

    print('\nbanners:')
    for label, bw, bh, hfrac, mfrac in BANNERS:
        # work in wordmark units: place the wordmark left aligned, vertically
        # centred, on a snow field of the banner aspect
        wm_w, wm_h = wm_vb[2], wm_vb[3]
        target_h = bh * hfrac              # wordmark height in px
        k = target_h / wm_h                # px per wordmark unit
        vb_w, vb_h = bw / k, bh / k        # banner in wordmark units
        left = (bw * mfrac) / k
        vx0 = wm_vb[0] - left
        vy0 = wm_vb[1] - (vb_h - wm_h) / 2.0
        svg = SVG_TPL % (
            '%s %s %s %s' % (_n(vx0), _n(vy0), _n(vb_w), _n(vb_h)),
            'The Mountain Diaries',
            bg_rect(vx0, vy0, vb_w, vb_h, SNOW),
            '<path fill="%s" d="%s"/>' % (INK, wm_d))
        sp = os.path.join(OUT, 'banner-%s.svg' % label)
        io.open(sp, 'w', encoding='utf-8').write(svg)
        made.append(sp)
        dest = os.path.join(OUT, 'banner-%s-%dx%d.png' % (label, bw, bh))
        render(svg, bw, bh, dest)
        made.append(dest)
        clear = target_h * 0.2743          # the DIARIES-line clear space rule
        print('  %-34s wordmark %.0f x %.0f px, left margin %.0f px, '
              'top/bottom %.0f px (clear space needs %.0f)'
              % (os.path.basename(dest), wm_w * k, target_h, bw * mfrac,
                 (bh - target_h) / 2.0, clear))

    write_readme()
    made.append(os.path.join(OUT, 'README.md'))
    zip_set(made)
    print('\navatar set written to %s' % OUT)
    return 0


def zip_set(made):
    dest = os.path.join(OUT, 'tmd-avatars.zip')
    if os.path.exists(dest):
        os.remove(dest)
    rels = sorted(os.path.relpath(p, OUT) for p in made)
    with zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED) as z:
        for rel in rels:
            info = zipfile.ZipInfo('tmd-avatars/' + rel, (2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, open(os.path.join(OUT, rel), 'rb').read())
    print('  %-34s %d files, %d KB'
          % ('tmd-avatars.zip', len(rels), os.path.getsize(dest) // 1024))


def write_readme():
    io.open(os.path.join(OUT, 'README.md'), 'w', encoding='utf-8').write(README)


README = u'''# Platform avatars and banners

Generated by `build/avatars.py` from `assets/monogram-tmd.svg` and
`assets/wordmark.svg`. Do not edit by hand. Re-run:

```
python3 build/avatars.py
```

## Avatars

Square, and safe under a circular crop. The monogram is scaled so its bounding
box fits entirely inside a centred circle of 78 per cent of the canvas
diameter. Platforms mask at roughly 90 to 100 per cent, so nothing comes near
the edge of the mask on any of them.

At 1080 px the monogram is 776 px wide, 71.8 per cent of the canvas.

| Colourway | Background | Monogram | Use |
| --- | --- | --- | --- |
| `avatar-sienna-*` | sienna `#B85C38` | snow `#FAFAF7` | primary. Most distinctive at thumbnail size |
| `avatar-snow-*` | snow `#FAFAF7` | ink `#2E3438` | light alternative |

Sizes, and what each is for:

| File | Platform |
| --- | --- |
| `-1080.png` | the master. Instagram and TikTok upload |
| `-800.png` | WhatsApp |
| `-400.png` | LinkedIn, X |
| `-320.png` | smaller profile slots |
| `-200.png` | list and comment thumbnails |

Always upload the largest the platform accepts and let it downscale. The
smaller PNGs are here for places that reject a large file.

## Banners

Snow background, ink wordmark, left aligned and vertically centred, nothing
else on the canvas.

| File | Intended for |
| --- | --- |
| `banner-x-header-1500x500.png` | X profile header |
| `banner-linkedin-cover-1128x191.png` | LinkedIn company page cover |

Both keep a left margin and top and bottom margins larger than the wordmark
clear space rule, which is 27.4 per cent of the wordmark height.

One caveat these files cannot solve on their own. Both platforms overlay the
profile or company logo on top of the banner, near the lower left, and both
crop the banner differently by viewport. The wordmark is vertically centred
rather than pushed to the bottom left for that reason, but check the result on
a real profile before settling, and be ready to move the wordmark right if the
avatar overlaps it on your account.

## The SVGs

Each avatar colourway and each banner also ships as an SVG. Those are the
scalable source for any size not exported here.
'''


if __name__ == '__main__':
    sys.exit(main())

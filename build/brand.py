#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the brand asset kit in brand/ from the canonical SVGs in assets/.

    python3 build/brand.py

Deliberately NOT part of build/build.py. The site pages are regenerated on
every build; brand/ is committed output that only changes when the canonical
artwork or the brand rules change. Running this is a manual act.

Sources of truth, in order:
  assets/wordmark.svg        ink lockup, three lines, single path
  assets/wordmark-inverse.svg  the same path filled white
  assets/monogram-tmd.svg    the TMD monogram, single line, single path

Everything else in brand/ is derived from those. The geometry constants below
are measured from the path data, not typed in by hand, so re-running after an
artwork change picks up the new measurements.

Rasterising uses headless Chrome, which is the only SVG renderer present on
this machine. If Chrome moves, fix CHROME below.
"""
import io
import os
import re
import shutil
import struct
import subprocess
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
ASSETS = os.path.join(REPO, 'assets')
OUT = os.path.join(REPO, 'brand')

CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

# ─── palette ──────────────────────────────────────────────────────────────
SNOW = '#FAFAF7'
INK = '#2E3438'
SIENNA = '#B85C38'
GLACIER = '#7A93A7'
PINE = '#3E5C4B'
SIENNA_LIFT = '#EEA67C'
WHITE = '#FFFFFF'

PNG_SIZES = [512, 1024, 2048]
AVATAR_SIZES = [400, 800]

# Fraction of the avatar canvas width taken by the monogram. Chosen so the
# clear-space rule holds with room to spare at 400px, checked in verify().
AVATAR_FILL = 0.62

# Monogram clear space, as a fraction of its own height. The wordmark gets a
# measured unit (the DIARIES line); the monogram has no second line to measure,
# so this is a stated rule.
MONOGRAM_CLEAR = 0.25


# ─── geometry, measured from the path data ────────────────────────────────
def _bbox(d):
    """Bounding box of an absolute-command path. The artwork uses M L H V Q Z."""
    xs, ys = [], []
    for cmd, arg in re.findall(r'([MLHVQCZ])([^MLHVQCZ]*)', d):
        n = [float(v) for v in re.findall(r'-?\d*\.?\d+(?:e-?\d+)?', arg)]
        if cmd in 'ML':
            for i in range(0, len(n), 2):
                xs.append(n[i])
                ys.append(n[i + 1])
        elif cmd == 'H':
            xs.extend(n)
        elif cmd == 'V':
            ys.extend(n)
        elif cmd == 'Q':
            for i in range(0, len(n), 4):
                xs += [n[i], n[i + 2]]
                ys += [n[i + 1], n[i + 3]]
        elif cmd == 'C':
            for i in range(0, len(n), 6):
                xs += [n[i], n[i + 2], n[i + 4]]
                ys += [n[i + 1], n[i + 3], n[i + 5]]
    return min(xs), min(ys), max(xs), max(ys)


def _lines(d):
    """Group the glyph subpaths into text lines by vertical overlap."""
    boxes = sorted((_bbox('M' + p) for p in d.split('M') if p.strip()),
                   key=lambda b: b[1])
    lines = []
    for b in boxes:
        for ln in lines:
            if b[1] < ln[1] - 0.5 and b[3] > ln[0] + 0.5:
                ln[0] = min(ln[0], b[1])
                ln[1] = max(ln[1], b[3])
                break
        else:
            lines.append([b[1], b[3]])
    return [(a, z) for a, z in lines]


def load(name):
    s = io.open(os.path.join(ASSETS, name), encoding='utf-8').read()
    d = re.search(r'\sd="([^"]+)"', s).group(1)
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', s).group(1).split()]
    return s, d, vb


# ─── svg emission ─────────────────────────────────────────────────────────
SVG_TPL = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" role="img" '
           'aria-label="%s">%s<path fill="%s" d="%s"/></svg>\n')


def svg(d, vb, fill, label, bg=None, pad=0.0):
    x0, y0, w, h = vb
    if pad:
        x0, y0, w, h = x0 - pad, y0 - pad, w + 2 * pad, h + 2 * pad
    box = ' '.join(('%.2f' % v).rstrip('0').rstrip('.') for v in (x0, y0, w, h))
    return SVG_TPL % (box, label, _bg_rect(bg, x0, y0, w, h), fill, d)


def _bg_rect(bg, x0, y0, w, h):
    """Background rect, bled past the viewBox on every side.

    A PNG canvas is a whole number of pixels, so its aspect almost never equals
    the viewBox aspect exactly. preserveAspectRatio then centres the artwork and
    leaves a sub-pixel sliver of transparency down the edges, which shows up as
    alpha 251 in the corners of what is meant to be a solid panel. The bleed
    covers that. It is invisible in normal use because the SVG viewport clips
    anything outside the viewBox.
    """
    if not bg:
        return ''
    b = max(w, h) * 0.02
    return '<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (
        _n(x0 - b), _n(y0 - b), _n(w + 2 * b), _n(h + 2 * b), bg)


def _n(v):
    return ('%.2f' % v).rstrip('0').rstrip('.')


# ─── rasterising ──────────────────────────────────────────────────────────
def render(svg_text, w, h, dest):
    """Screenshot an SVG at exactly w x h. Transparent where the SVG is."""
    tmp = os.path.join(OUT, '.render.html')
    io.open(tmp, 'w', encoding='utf-8').write(
        '<html><head><meta charset="utf-8"><style>html,body{margin:0;padding:0;'
        'background:transparent}svg{display:block;width:%dpx;height:%dpx}</style>'
        '</head><body>%s</body></html>' % (w, h, svg_text))
    r = subprocess.run(
        [CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars',
         '--default-background-color=00000000', '--force-device-scale-factor=1',
         '--window-size=%d,%d' % (w, h), '--screenshot=' + dest,
         'file://' + tmp],
        capture_output=True, text=True)
    os.remove(tmp)
    if not os.path.exists(dest):
        sys.stderr.write(r.stdout + r.stderr)
        raise SystemExit('render failed: %s' % dest)
    gw, gh = png_size(dest)
    if (gw, gh) != (w, h):
        raise SystemExit('%s came out %dx%d, wanted %dx%d' % (dest, gw, gh, w, h))


def png_size(path):
    d = open(path, 'rb').read(24)
    return struct.unpack('>II', d[16:24])


# ─── build ────────────────────────────────────────────────────────────────
def main():
    if not os.path.exists(CHROME):
        raise SystemExit('no Chrome at %s; brand PNGs cannot be rendered' % CHROME)

    wm_src, wm_d, wm_vb = load('wordmark.svg')
    inv_src, inv_d, _ = load('wordmark-inverse.svg')
    mo_src, mo_d, mo_vb = load('monogram-tmd.svg')

    if wm_d != inv_d:
        raise SystemExit('wordmark and wordmark-inverse are no longer the same '
                         'artwork; the kit assumes one path, two fills')

    wm_lines = _lines(wm_d)
    if len(wm_lines) != 3:
        raise SystemExit('expected 3 wordmark lines, measured %d' % len(wm_lines))
    diaries_h = wm_lines[2][1] - wm_lines[2][0]
    wm_h = wm_vb[3]
    clear_frac = diaries_h / wm_h
    mo_pad = mo_vb[3] * MONOGRAM_CLEAR

    print('measured from the artwork:')
    print('  wordmark   %.2f x %.2f' % (wm_vb[2], wm_h))
    for i, (a, z) in enumerate(wm_lines):
        print('    line %d height %.2f' % (i + 1, z - a))
    print('  clear space = DIARIES line = %.2f = %.1f%% of wordmark height'
          % (diaries_h, clear_frac * 100))
    print('  monogram   %.2f x %.2f, clear space %.2f (%.0f%%)'
          % (mo_vb[2], mo_vb[3], mo_pad, MONOGRAM_CLEAR * 100))

    for sub in ('svg', 'png', 'avatar'):
        p = os.path.join(OUT, sub)
        if os.path.isdir(p):
            shutil.rmtree(p)
        os.makedirs(p)

    made = []

    # lockup, label, path, viewBox, clear-space pad
    lockups = [
        ('wordmark', 'The Mountain Diaries', wm_d, wm_vb, diaries_h),
        ('monogram', 'TMD', mo_d, mo_vb, mo_pad),
    ]
    # variant suffix, fill, background, padded?
    variants = [
        ('ink', INK, None, False),
        ('white', WHITE, None, False),
        ('ink-on-snow', INK, SNOW, True),
    ]

    for name, label, d, vb, pad in lockups:
        for suffix, fill, bg, padded in variants:
            p = pad if padded else 0.0
            text = svg(d, vb, fill, label, bg=bg, pad=p)
            stem = '%s-%s' % (name, suffix)
            sp = os.path.join(OUT, 'svg', stem + '.svg')
            io.open(sp, 'w', encoding='utf-8').write(text)
            made.append(sp)
            aspect = (vb[3] + 2 * p) / (vb[2] + 2 * p)
            for w in PNG_SIZES:
                h = int(round(w * aspect))
                dest = os.path.join(OUT, 'png', '%s-%d.png' % (stem, w))
                render(text, w, h, dest)
                made.append(dest)
                print('  %-34s %4d x %4d' % (os.path.basename(dest), w, h))

    # Square social avatars, monogram only. The vector is the same at every
    # size, so each background gets one SVG and several PNGs.
    for bgname, bg, fill in (('snow', SNOW, INK), ('sienna', SIENNA, WHITE)):
        # a square viewBox in monogram units, monogram centred
        span = mo_vb[2] / AVATAR_FILL
        x0 = mo_vb[0] - (span - mo_vb[2]) / 2.0
        y0 = mo_vb[1] - (span - mo_vb[3]) / 2.0
        text = SVG_TPL % (
            '%s %s %s %s' % (_n(x0), _n(y0), _n(span), _n(span)),
            'TMD', _bg_rect(bg, x0, y0, span, span), fill, mo_d)
        stem = 'avatar-monogram-on-%s' % bgname
        sp = os.path.join(OUT, 'avatar', stem + '.svg')
        io.open(sp, 'w', encoding='utf-8').write(text)
        made.append(sp)
        for w in AVATAR_SIZES:
            mw = w * AVATAR_FILL
            mh = mw * (mo_vb[3] / mo_vb[2])
            dest = os.path.join(OUT, 'avatar', '%s-%d.png' % (stem, w))
            render(text, w, w, dest)
            made.append(dest)
            print('  %-34s %4d x %4d  (monogram %.0f x %.0f)'
                  % (os.path.basename(dest), w, w, mw, mh))

    write_brand_md(wm_vb, mo_vb, diaries_h, clear_frac, mo_pad)
    made.append(os.path.join(OUT, 'BRAND.md'))
    zip_kit(made)
    print('\nbrand kit written to %s' % OUT)
    return 0


def zip_kit(made):
    """Deterministic zip: sorted entries, fixed timestamps, no rebuild churn."""
    dest = os.path.join(OUT, 'tmd-brand-kit.zip')
    if os.path.exists(dest):
        os.remove(dest)
    rels = sorted(os.path.relpath(p, OUT) for p in made)
    with zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED) as z:
        for rel in rels:
            info = zipfile.ZipInfo('tmd-brand-kit/' + rel, (2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, open(os.path.join(OUT, rel), 'rb').read())
    print('  %-34s %d files, %d KB'
          % ('tmd-brand-kit.zip', len(rels), os.path.getsize(dest) // 1024))


def _rgb(hexstr):
    h = hexstr.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def contrast(a, b):
    """WCAG 2.1 contrast ratio between two hex colours."""
    def lum(c):
        def ch(v):
            v /= 255.0
            return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
        r, g, bl = _rgb(c)
        return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(bl)
    la, lb = lum(a), lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


# pairing, foreground, background, what it is cleared for
CONTRAST_PAIRS = [
    ('Ink on snow', INK, SNOW, 'body text'),
    ('Pine on snow', PINE, SNOW, 'body text'),
    ('Sienna lift on ink', SIENNA_LIFT, INK, 'body text on dark surfaces'),
    ('White on sienna', WHITE, SIENNA, 'body text'),
    ('Sienna on snow', SIENNA, SNOW, 'large text and UI only'),
    ('Glacier on snow', GLACIER, SNOW, 'large text and UI only'),
    ('Sienna on ink', SIENNA, INK, 'nothing. Use sienna lift'),
    ('Ink on sienna', INK, SIENNA, 'nothing. Use white'),
]


def contrast_table():
    rows = []
    for name, fg, bg, use in CONTRAST_PAIRS:
        r = contrast(fg, bg)
        grade = 'AA' if r >= 4.5 else ('AA large' if r >= 3.0 else 'fails')
        rows.append('| %s | `%s` on `%s` | %.2f:1 | %s | %s |'
                    % (name, fg, bg, r, grade, use))
    return '\n'.join(rows)


def write_brand_md(wm_vb, mo_vb, diaries_h, clear_frac, mo_pad):
    io.open(os.path.join(OUT, 'BRAND.md'), 'w', encoding='utf-8').write(
        BRAND_MD % {
            'contrast': contrast_table(),
            'wm_w': _n(wm_vb[2]), 'wm_h': _n(wm_vb[3]),
            'mo_w': _n(mo_vb[2]), 'mo_h': _n(mo_vb[3]),
            'diaries': _n(diaries_h),
            'clear_pct': '%.1f' % (clear_frac * 100),
            'mo_pad': _n(mo_pad),
            'mo_pct': '%.0f' % (MONOGRAM_CLEAR * 100),
            'avatar_pct': '%.0f' % (AVATAR_FILL * 100),
        })


BRAND_MD = u'''# The Mountain Diaries, brand kit

Everything here is generated from the canonical artwork by `build/brand.py`.
Do not edit these files by hand. Change `assets/wordmark.svg`,
`assets/wordmark-inverse.svg` or `assets/monogram-tmd.svg`, then re-run:

```
python3 build/brand.py
```

## What is in the kit

```
brand/
  svg/      wordmark and monogram, three colourways each. Six scalable files
  png/      those same six at 512, 1024 and 2048 px wide. Eighteen files
  avatar/   square monogram avatars for social profiles, on snow and on
            sienna, as one SVG each plus 400 and 800 px PNGs
  BRAND.md  this file
  tmd-brand-kit.zip  all of the above, for sending to someone
```

Three colourways, and only three:

| Suffix | Mark | Background | Use it on |
| --- | --- | --- | --- |
| `-ink` | ink `#2E3438` | transparent | snow, white, and any pale photograph |
| `-white` | white `#FFFFFF` | transparent | ink surfaces, sienna, and dark photographs |
| `-ink-on-snow` | ink `#2E3438` | snow `#FAFAF7` | anywhere a solid panel is needed |

The transparent files are cropped tight to the letterforms, so you place the
clear space yourself. The `-on-snow` and avatar files have the clear space
already built into the canvas, because a background flush to the letterforms
would break the rule below on its own. So the mark inside an on-snow PNG is
smaller than the mark in a transparent PNG of the same nominal width: at 512 px
wide the wordmark itself measures 512 px transparent and about 418 px on snow.

## Palette

| Name | Hex | Role |
| --- | --- | --- |
| Snow | `#FAFAF7` | page background, the default surface |
| Ink | `#2E3438` | body text and the primary mark |
| Sienna | `#B85C38` | the accent. Links, rules, the active state |
| Glacier | `#7A93A7` | secondary accent, cool and quiet |
| Pine | `#3E5C4B` | secondary accent, used sparingly |
| Sienna lift | `#EEA67C` | the sienna substitute on dark surfaces only |

Sienna lift exists for one reason. Sienna on ink does not carry enough contrast
to be read comfortably, so on the footer and any other dark panel the accent
lifts to `#EEA67C`. Never use sienna lift on snow, and never use sienna as text
on ink.

### Contrast, measured

WCAG 2.1 ratios, computed from the hex values above rather than eyeballed. AA
is 4.5:1 for body text and 3:1 for large text and UI components.

| Pairing | Colours | Ratio | Grade | Cleared for |
| --- | --- | --- | --- | --- |
%(contrast)s

Two things follow from that table and are worth stating plainly. Sienna on snow
lands at just under the body-text threshold, so it is right for links, rules
and active states but should not carry long passages of small text. And the
sienna avatar uses a white monogram rather than an ink one, because ink on
sienna fails outright.

## Typography

| Role | Family | Weight and width |
| --- | --- | --- |
| Wordmark | Archivo | width 62, weight 900, outlined to paths |
| Headings and body | Source Sans 3 | 400 to 700 |
| Hero headline | Lato | 900 |

The wordmark is outlined, not set live. It carries no webfont dependency and
must never be re-set in Archivo by hand: use the files in this kit.

## Wordmark rules

The lockup is %(wm_w)s x %(wm_h)s units, three lines: THE, MOUNTAIN, DIARIES.
The monogram is %(mo_w)s x %(mo_h)s units.

**Clear space.** Keep clear on all four sides a margin equal to the height of
the DIARIES line, which is %(diaries)s units, or %(clear_pct)s per cent of the
wordmark height. Nothing enters that margin: no text, no rule, no photo edge,
no other logo. For the monogram, use %(mo_pct)s per cent of its height,
%(mo_pad)s units.

**Minimum size.** The wordmark sits 28 px tall in the site navigation, and that
is the smallest comfortable size. The absolute floor is 24 px tall. Rendered
down the scale, 28 px and 24 px both hold: the THE line stays open and the
DIARIES tracking stays even. Below the floor the two tracked lines fill in
progressively, noticeably by 20 px and past saving by 16 px, while MOUNTAIN
carries on looking fine and hides the problem. Below 24 px, use the monogram
instead.

**Never recolour** beyond ink and white. Not sienna, not glacier, not pine, not
a gradient, not a photograph filled into the letterforms. Two colours is the
whole system.

**Never restack.** THE, MOUNTAIN and DIARIES sit in that order at those sizes.
Do not set the three lines side by side, do not drop a line, do not letter
space it further, do not rotate it, do not add a tagline inside the clear
space, and do not put it in a box or a circle.

**Never distort.** Scale proportionally. If a space is the wrong shape for the
wordmark, use the monogram.

## Difficulty scale

Four grades, coarse on purpose, and the same four words everywhere:

**Gentle, Steady, Demanding, Severe.**

Steady journeys ask for honest walking fitness and no more. Demanding adds
altitude endurance: the consecutive-days test at full length. Severe means all
of that plus reserve, the capacity to do the hardest day of your life at 3 am
and still descend well.

Gentle is defined in the scale but no journey currently carries it. That is
deliberate: a grade is not applied until a journey earns it.

A journey with no rating yet shows no rating. Never guess a grade, never
average one, and never soften a grade to make a journey look more accessible.
If a grade and a walker’s training diary disagree, the diary wins.

## Voice

**No em dashes anywhere.** Restructure the sentence instead. An en dash is
allowed only in a numeric range, and the minus sign in a temperature is a minus
sign, not a dash.

**British spelling.** Acclimatisation, not acclimatization. Metres, not meters.
The -ise and -isation endings throughout.

**Curly apostrophes and quotes.** The straight forms belong in code, never in
prose.

**No AI-marker phrasing.** Write like a person who has walked the trail. No
“delve”, no “tapestry”, no “it is worth noting”, no three-item rhetorical
flourishes, no sentence that could have been written about any mountain
anywhere.

**Honesty over polish.** An empty state that says nothing has happened yet
beats a fabricated entry. An unrated journey beats a guessed grade. A missing
photograph beats one that shows the wrong mountain.

## Photography

One photograph, one slot. No image is used twice across the site, which is
enforced by `IMAGE_MAP.md`. Every photograph must genuinely show the region it
illustrates, must be licensed for commercial use without attribution, and must
not show an identifiable face. EXIF and GPS metadata is stripped before a
photograph is placed.
'''


if __name__ == '__main__':
    sys.exit(main())

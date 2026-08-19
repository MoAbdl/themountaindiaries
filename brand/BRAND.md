# The Mountain Diaries, brand kit

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
| Ink on snow | `#2E3438` on `#FAFAF7` | 12.07:1 | AA | body text |
| Pine on snow | `#3E5C4B` on `#FAFAF7` | 7.08:1 | AA | body text |
| Sienna lift on ink | `#EEA67C` on `#2E3438` | 6.24:1 | AA | body text on dark surfaces |
| White on sienna | `#FFFFFF` on `#B85C38` | 4.54:1 | AA | body text |
| Sienna on snow | `#B85C38` on `#FAFAF7` | 4.34:1 | AA large | large text and UI only |
| Glacier on snow | `#7A93A7` on `#FAFAF7` | 3.06:1 | AA large | large text and UI only |
| Sienna on ink | `#B85C38` on `#2E3438` | 2.78:1 | fails | nothing. Use sienna lift |
| Ink on sienna | `#2E3438` on `#B85C38` | 2.78:1 | fails | nothing. Use white |

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

The lockup is 492.44 x 202.48 units, three lines: THE, MOUNTAIN, DIARIES.
The monogram is 162.4 x 68.8 units.

**Clear space.** Keep clear on all four sides a margin equal to the height of
the DIARIES line, which is 55.55 units, or 27.4 per cent of the
wordmark height. Nothing enters that margin: no text, no rule, no photo edge,
no other logo. For the monogram, use 25 per cent of its height,
17.2 units.

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

# build

`index.html`, `explore.html`, `join.html` and `IMAGE_MAP.md` are **generated**.
Do not edit them by hand: change the source here and rebuild.

## Rebuild

```bash
python3 build/build.py
```

That writes all four files. No arguments, no dependencies beyond the Python 3
standard library, and nothing outside this repository.

## Check before pushing

```bash
python3 build/check.py
```

Rebuilds into a temporary directory and diffs against the committed HTML. Exit
0 means the pages match their source; exit 1 prints the drift and leaves the
working tree untouched. Drift means either a generated page was hand edited
(and the edit is about to be lost) or the source changed without a rebuild.

## What is here

| File | Role |
| --- | --- |
| `build.py` | the one command; runs the three steps in order |
| `check.py` | integrity check, rebuild and diff |
| `journeys.py` | the 52 journeys: slug, name, elevation, category, region, country, card photograph |
| `details.py` | the detailed journeys: facts and the owner's approved copy, plus the STYLE rules that copy follows |
| `explore-build.py` | stamps down the base snapshot, performs the index surgery, writes `explore.html`, refreshes the shared nav and footer inside `p3-join.py` |
| `p3-join.py` | generates `join.html` from the index style block plus its own markup |
| `mkimagemap.py` | derives `IMAGE_MAP.md` from what the pages actually reference; fails on a duplicate or a missing file |
| `base/index.base.html` | the pre-surgery index snapshot every build starts from |
| `routemap.py` | PARKED. The generated topographic route maps, kept whole for the day drawn maps do not work out |

`MD_OUT` redirects the generated pages to another directory; assets are always
read from the repository. `check.py` uses it.

## Order matters

`explore-build.py` must run before `p3-join.py`, because join's nav and footer
are lifted from the freshly built index. `mkimagemap.py` runs last, because it
reads all three finished pages.

## The wordmark, and what was lost

The outlined wordmark generator (`hf-build.py`, `glyphs.json`, and the
`wordmark/` lockup data) was lost before the pipeline moved into the repository.
It converted Archivo at `wdth 62` into pure SVG paths.

It is not needed to build the site, and nothing here depends on it, but it
cannot be re-run:

- **The canonical wordmark is now the outlined SVG inside `base/index.base.html`.**
  It is plain paths, no font dependency, and it is what every page ships.
- `assets/wordmark.svg`, `assets/wordmark-inverse.svg` and
  `assets/monogram-tmd.svg` survive as standalone copies of the same artwork.
- The favicon set (`favicon.ico`, `assets/favicon-32.png`,
  `assets/apple-touch-icon.png`) was rendered from the monogram and is committed.

To change the wordmark, edit the paths in the base snapshot, or rebuild the
generator from scratch against Archivo's variable font.

## The route maps

`routemap.py` and `scripts/make-route-map.py` are parked, not dead. They drew a
real OpenTopoMap base with a Web Mercator overlay; the surveyed coordinates in
`scripts/routes/<slug>.json` are still accurate. Both files carry headers
explaining how to switch them back on. If they ever ship again, the OpenTopoMap
attribution line ships with them: it is a licence condition, not a courtesy.

Today the Route section renders `assets/images/route-map-<slug>.jpg` when that
artwork exists, and renders nothing at all when it does not.

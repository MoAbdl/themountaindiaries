"""Build IMAGE_MAP.md from what the pages actually reference.

The rule is one photograph, one slot, site wide. This derives the map from the
markup and the data objects rather than from a hand kept list, so it cannot go
stale, and it exits non-zero if a photograph is used for two different subjects
or if a file that is declared available is not on disk.

"Slot" is the SUBJECT, not the DOM position. A trail's photograph legitimately
appears twice: as the 800px card thumbnail in the trails grid, and as the full
size hero of that trail's own detail view. Those are one slot. Two different
trails sharing a photograph is the thing worth catching, and it is the bug that
was actually found and fixed during the Phase 2 gallery pass.
"""
import io, os, re, sys, collections

# Paths are derived from this file's own location, so the build runs from a
# clone anywhere. MD_OUT lets the integrity check render into a scratch
# directory instead of over the committed pages; assets always come from REPO.
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT = os.environ.get('MD_OUT') or REPO
PAGES = ['index.html', 'explore.html', 'join.html', 'know.html']
IMGDIR = os.path.join(REPO, 'assets', 'images')

SECTIONS = [
    (re.compile(r'<section class="hero" id="hero">'), 'Hero'),
    (re.compile(r'<section[^>]*\bid="story"'), 'The Story'),
    (re.compile(r'<section[^>]*\bid="trails"'), 'Trails grid'),
    (re.compile(r'<section[^>]*\bid="expeditions"'), 'Expeditions grid'),
    (re.compile(r'<section[^>]*\bid="community"'), 'Community'),
    (re.compile(r'<section class="band"'), 'Photo band'),
    (re.compile(r'<footer class="site-footer">'), 'Footer'),
    (re.compile(r'<main class="join-main">'), 'Join page'),
    (re.compile(r'<main class="explore-main">'), 'Explore catalogue'),
    (re.compile(r'<section class="xhead">'), 'Explore header'),
    (re.compile(r'<section class="section section--alt" id="explore-teaser">'), 'Explore teaser'),
    (re.compile(r'\.footer-ridge \{'), 'Footer'),          # placed from CSS
]
# A subject claims every reference after it, until the next subject. Owners are
# namespaced by kind: the Kilimanjaro trail and the Kilimanjaro expedition are
# different subjects that happen to share a slug, and collapsing them reported
# a duplicate that is not one.
SUBJECTS = [
    (re.compile(r'<article class="tcard" data-detail="(trail|expedition)/([a-z0-9-]+)"'), None),
    (re.compile(r'^  ([a-z]+): \{$', re.M), 'trail'),                 # TRAILS keys
    (re.compile(r"\{ key: '[a-z0-9-]+', slug: '([a-z0-9-]+)'"), 'expedition'),
    # A journey owns its photograph wherever it appears: the Explore teaser on
    # index, its catalogue card, and its static catalogue entry are one subject.
    (re.compile(r'class="jcard" href="(?:explore\.html)?#journey/([a-z0-9-]+)"'), 'journey'),
    (re.compile(r'<section class="journey-static" id="journey/([a-z0-9-]+)"'), 'journey'),
]
# a subject label is only valid until the data objects end
END_OF_DATA = re.compile(r'const SLUG_TO_TRAIL')

# Three mountains appear twice on the site: once as a trail you can read about
# and once as a 2026 expedition you can book. They are the same place, so they
# are one subject here, and each deliberately leads with one photograph and
# shows the other in its gallery. Remove a line to have the pair reported.
SAME_SUBJECT = {
    'trail:kili': 'Kilimanjaro',        'expedition:kilimanjaro': 'Kilimanjaro',
    'trail:torres': 'Torres del Paine', 'expedition:torres-del-paine': 'Torres del Paine',
    'trail:hauteroute': 'Haute Route',  'expedition:haute-route': 'Haute Route',
}

refs = collections.defaultdict(list)   # file -> [(page, owner, pos)]
registry = {}
slug_to_key = {}
titles = {}

for page in PAGES:
    s = io.open(os.path.join(OUT, page), encoding='utf-8').read()

    # slug -> data key, so a card and its own detail resolve to one owner
    m = re.search(r'const TRAIL_SLUGS = \{(.*?)\};', s, re.S)
    if m:
        for k, v in re.findall(r"(\w+):\s*'([a-z0-9-]+)'", m.group(1)):
            slug_to_key[v] = k
    for k, name in re.findall(r"^  ([a-z]+): \{\n\s*name: '([^']+)'", s, re.M):
        titles[k] = name
    for sl, name in re.findall(r"slug: '([a-z0-9-]+)', name: '([^']+)'", s):
        titles[sl] = name

    # AVAILABLE_PHOTOS is a registry of what exists, not a placement
    reg = re.search(r'const AVAILABLE_PHOTOS = new Set\(\[(.*?)\]\)', s, re.S)
    if reg:
        registry[page] = set(re.findall(r'([A-Za-z0-9._-]+\.jpg)', reg.group(1)))
        s = s[:reg.start(1)] + ' ' * (reg.end(1) - reg.start(1)) + s[reg.end(1):]

    marks = []
    for rx, name in SECTIONS:
        for mm in rx.finditer(s):
            marks.append((mm.start(), name, False))
    for rx, kind in SUBJECTS:
        for mm in rx.finditer(s):
            k, slug = (mm.group(1), mm.group(2)) if kind is None else (kind, mm.group(1))
            if k == 'trail':
                slug = slug_to_key.get(slug, slug)
            marks.append((mm.start(), '%s:%s' % (k, slug), True))
    marks.sort()
    data_end = END_OF_DATA.search(s)
    data_end = data_end.start() if data_end else len(s)

    for mm in re.finditer(r"assets/images/([A-Za-z0-9._-]+\.jpg)|IMG \+ '([A-Za-z0-9._-]+\.jpg)'"
                          r"|data-photo=\"([A-Za-z0-9._-]+\.jpg)\"", s):
        f = mm.group(1) or mm.group(2) or mm.group(3)
        owner, is_subject = 'Page', False
        for pos, name, subj in marks:
            if pos >= mm.start():
                break
            owner, is_subject = name, subj
        # past the data objects a stale subject label would be wrong
        if is_subject and mm.start() > data_end:
            owner = 'Page'
        refs[f].append((page, owner, mm.start()))


def base(f):
    return f[:-8] + '.jpg' if f.endswith('-800.jpg') else f


groups = collections.defaultdict(list)
for f in refs:
    groups[base(f)].append(f)

on_disk = {f for f in os.listdir(IMGDIR) if f.endswith('.jpg')}
declared = set().union(*registry.values()) if registry else set()
problems = []

for b in sorted(groups):
    slots = {SAME_SUBJECT.get(w, w) for v in groups[b] for _, w, _ in refs[v]}
    if len(slots) > 1:
        problems.append('DUPLICATE  %-30s used by %s' % (b, sorted(slots)))

# A referenced file that is absent AND undeclared is an honest placeholder: it
# renders as a grey block naming the file it waits for. Absent but DECLARED is
# a real break, because the page would try to load it.
placeholders = sorted(f for f in refs if f not in on_disk and f not in declared)
broken = sorted(f for f in refs if f not in on_disk and f in declared)
for f in broken:
    problems.append('BROKEN     %s is declared available but is not on disk' % f)
for f in sorted(declared - on_disk):
    problems.append('BROKEN     %s declared in AVAILABLE_PHOTOS but not on disk' % f)

# A full size original counts as placed when its 800px derivative is the
# thing on the page: the card ships the derivative, the original is its
# source. Only a base with neither reference is genuinely unplaced.
used_bases = {base(f) for f in refs}
orphans = sorted(f for f in on_disk - set(refs)
                 if not f.endswith('-800.jpg') and f not in used_bases)

rows = []
for b in sorted(groups):
    variants = sorted(groups[b])
    owner = refs[variants[0]][0][1]
    label = SAME_SUBJECT.get(owner) or titles.get(owner.split(':')[-1], owner)
    pages = sorted({p for v in variants for p, _, _ in refs[v]})
    rows.append('| `%s` | %s | %s | %s | %d |' % (
        b, label, ', '.join(pages),
        'yes' if any(v.endswith('-800.jpg') for v in variants) else 'no',
        sum(len(refs[v]) for v in variants)))

doc = ['# Image usage map', '',
       'One photograph, one slot, site wide. No photograph is used for two different',
       'subjects.', '',
       'A trail photograph is referenced twice on purpose: once as the 800px card',
       'thumbnail in the grid, and once at full size as the hero of that trail\'s own',
       'detail view. Same subject, same slot, two sizes. The reference count column',
       'shows that, and gallery photographs inside a detail view count once.', '',
       'Generated by `mkimagemap.py`, not maintained by hand. Re-run it after any change',
       'that adds, moves or removes a photograph; it exits non-zero on a duplicate or on',
       'a file that is declared available but missing.', '',
       '| File | Slot | Page | 800px derivative | Refs |',
       '| --- | --- | --- | --- | --- |'] + rows
doc += ['', '%d photographs.' % len(groups), '']
if placeholders:
    doc += ['## Honest placeholders', '',
            'Referenced by name and deliberately absent. Each renders as a flat grey block',
            'naming the file it is waiting for, and claims nothing.', '']
    doc += ['- `%s`' % f for f in placeholders] + ['']
if orphans:
    doc += ['## On disk, not placed', ''] + ['- `%s`' % f for f in orphans] + ['']
io.open(os.path.join(OUT, 'IMAGE_MAP.md'), 'w', encoding='utf-8').write('\n'.join(doc))

print('%d photographs mapped' % len(groups))
print('honest placeholders : %s' % (', '.join(placeholders) or 'none'))
print('on disk, not placed : %s' % (', '.join(orphans) or 'none'))
if problems:
    print('\nPROBLEMS')
    for p in problems:
        print('  ' + p)
    sys.exit(1)
print('\nno duplicates; every declared file is on disk')

# -*- coding: utf-8 -*-
"""Explore catalogue architecture.

Phase 0  lift the blocks that move from index.html to explore.html
Phase 1  index.html surgery: retire the catalogue, add the teaser
Phase 2  generate explore.html
Phase 3  regenerate join.html so all three pages share nav, footer and head
"""
import io, os, re, shutil, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from journeys import rows, EXPEDITION_TABS, TREK_TABS, TK
from details import DETAILS

# Paths are derived from this file's own location, so the build runs from a
# clone anywhere. MD_OUT lets the integrity check render into a scratch
# directory instead of over the committed pages; assets always come from REPO.
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT = os.environ.get('MD_OUT') or REPO
IDX = os.path.join(OUT, 'index.html')

# Phase 1 rewrites index.html in place, so it always starts from the committed
# base snapshot rather than from whatever a previous run left behind.
shutil.copyfile(os.path.join(HERE, 'base', 'index.base.html'), IDX)
J = list(rows())

src = io.open(IDX, encoding='utf-8').read()


def cut(text, start, end, why):
    """Return (text without the span, the span)."""
    a = text.find(start)
    assert a != -1, 'START missing (%s): %r' % (why, start[:60])
    b = text.find(end, a + len(start))
    assert b != -1, 'END missing (%s): %r' % (why, end[:60])
    return text[:a] + text[b:], text[a:b]


def sub(text, old, new, why):
    assert old in text, 'MISSING (%s): %r' % (why, old[:70])
    return text.replace(old, new, 1)


# ══════════════════ PHASE 0 - lift what moves to explore ══════════════════
LIGHTBOX_MARKUP = re.search(r'<!-- LIGHTBOX -->.*?\n</div>\n', src, re.S).group(0)
DETAIL_MARKUP = re.search(r'<!-- DETAIL VIEW .*?\n</div>\n', src, re.S).group(0)
INQUIRY_MARKUP = re.search(r'<!-- INQUIRY OVERLAY -->.*?\n</div>\n\n<!-- NAVIGATION -->', src, re.S).group(0)
INQUIRY_MARKUP = INQUIRY_MARKUP.replace('\n\n<!-- NAVIGATION -->', '')

_, LIGHTBOX_JS = cut(src, '// ═══ LIGHTBOX ═══', '// ═══ CAROUSEL ARROWS', 'lightbox js')
LIGHTBOX_JS = LIGHTBOX_JS.replace('#trail/ routing', '#journey/ routing')
_, INQUIRY_JS = cut(src, '// ═══ INQUIRY PANEL ═══', '// Resolve the URL on first paint', 'inquiry js')
_, PHOTO_JS = cut(src, '// ═══ PHOTO AVAILABILITY ═══', '// ═══ TRAIL DATA ═══', 'photo js')
_, NAV_JS = cut(src, '// ═══ NAV ═══', '// ═══ SINGLE ESCAPE HANDLER ═══', 'nav js')
_, POSTFORM_JS = cut(src, '// ─── BACKEND ──', "document.getElementById('share-form')", 'postForm js')

# ══════════════════════ PHASE 1 - index.html surgery ══════════════════════
s = src

# 1a. nav and hero board re-target
s = sub(s, '<li><a href="#trails" data-spy="trails">Explore</a></li>',
        '<li><a href="explore.html">Explore</a></li>', 'nav explore')
s = sub(s, '''      <!-- re-target to the Know the Mountain section once it exists; it points at
           the community hub meanwhile, and carries no spy so it cannot fight the
           Community link for the active state -->
      <li><a href="#community" onclick="switchTab('share')">Know the Mountain</a></li>''',
        '      <li><a href="know.html">Know the Mountain</a></li>', 'nav know')
# the footer gains the knowledge base and its news anchor
s = sub(s, '''          <li><a href="#community">Community</a></li>
          <!-- re-target to the About Us section once it is written; #story is a stand in -->
          <li><a href="#story">About Us</a></li>''',
        '''          <li><a href="#community">Community</a></li>
          <li><a href="know.html">Know the Mountain</a></li>
          <li><a href="know.html#news">Mountain news</a></li>
          <!-- re-target to the About Us section once it is written; #story is a stand in -->
          <li><a href="#story">About Us</a></li>''', 'footer know + news')
s = sub(s, '      <!-- re-target to the Explore section once it exists -->\n'
           '      <a class="sign-board" href="#trails" style="--tilt:1.2deg"',
        '      <a class="sign-board" href="explore.html" style="--tilt:1.2deg"', 'hero board')
s = sub(s, 'aria-label="Explore the trails"', 'aria-label="Explore the journeys"', 'hero board label')
s = sub(s, '<li><a href="#trails">Expeditions &amp; Trekking</a></li>',
        '<li><a href="explore.html">Expeditions &amp; Trekking</a></li>', 'footer explore')

# 1b. retire the two catalogue sections, leaving one teaser in their place
FEATURED = ['ama-dablam-6812', 'ebc-trek', 'mera-peak-6476']
BY_SLUG = {r['slug']: r for r in J}


def jcard(r, href):
    bits = []
    if r['elevation_m']:
        # an approximate high point says so, on the card as well as in the detail
        bits.append('<span class="jcard-elev">%s%s m</span>'
                    % ('~' if r.get('elev_approx') else '', format(r['elevation_m'], ',')))
    bits.append('<span class="jcard-where">%s &middot; %s</span>' % (r['region'], r['country']))
    # a verified photograph renders as the lazy 800px derivative; a journey
    # without one keeps the placeholder naming the file it waits for
    if r.get('card'):
        media = ('<img class="jcard-img" src="assets/images/%s" alt="" loading="lazy" decoding="async">'
                 % r['card'].replace('.jpg', '-800.jpg'))
    else:
        media = '<div class="photo-slot" data-photo="%s"></div>' % r['photo'].split('/')[-1]
    return ('''        <a class="jcard" href="%s">
          <div class="jcard-media">%s</div>
          <div class="jcard-body">
            <h3 class="jcard-name">%s</h3>
            <p class="jcard-meta">%s</p>
          </div>
        </a>''' % (href, media, r['name'], ''.join(bits)))


TEASER = '''<!-- EXPLORE TEASER -->
<section class="section section--alt" id="explore-teaser">
  <div class="wrap">
    <div class="section-bar">
      <div class="section-head" style="margin-bottom:var(--s-5)">
        <p class="section-kicker">Expeditions and trekking</p>
        <h2 class="section-title">Explore</h2>
        <p class="section-lede">Fifty two journeys, from a first 6,000er to the eight thousand metre peaks.</p>
      </div>
    </div>

    <div class="card-grid">
%s
    </div>

    <p class="teaser-more">
      <a class="link-action" href="explore.html">View all journeys <span aria-hidden="true">&rarr;</span></a>
    </p>
  </div>
</section>
''' % '\n'.join(jcard(BY_SLUG[k], 'explore.html#journey/' + k) for k in FEATURED)

s, _ = cut(s, '<!-- TRAILS -->', '<!-- BAND 2 -->', 'trails section')
KNOW_TEASER = '''<!-- KNOW THE MOUNTAIN TEASER -->
<section class="section" id="know-teaser">
  <div class="wrap">
    <div class="section-head" style="margin-bottom:var(--s-5)">
      <p class="section-kicker">The knowledge base</p>
      <h2 class="section-title">Know the Mountain</h2>
      <p class="section-lede">Altitude, training, gear and judgement: the knowledge base.</p>
    </div>
    <p class="teaser-more">
      <a class="link-action" href="know.html">Read the guides <span aria-hidden="true">&rarr;</span></a>
    </p>
  </div>
</section>
'''

s = sub(s, '<!-- BAND 2 -->', TEASER + '\n' + KNOW_TEASER + '\n<!-- BAND 2 -->', 'teaser in')
s, _ = cut(s, '<!-- EXPEDITIONS -->', '<!-- COMMUNITY -->', 'expeditions section')

# 1c. markup that moves to explore
s = sub(s, LIGHTBOX_MARKUP, '', 'drop lightbox markup')
s = sub(s, DETAIL_MARKUP, '', 'drop detail markup')
s = sub(s, INQUIRY_MARKUP, '', 'drop inquiry markup')

# 1d. JS that moves or dies with the catalogue
for a, b, why in [
    ('// ═══ TRAIL DATA ═══', '// ═══ ROUTES ═══', 'trail + expedition data'),
    ('// ═══ ROUTES ═══', '// ═══ DETAIL VIEW ═══', 'routes'),
    ('// ═══ DETAIL VIEW ═══', '// ═══ LIGHTBOX ═══', 'detail view'),
    ('// ═══ LIGHTBOX ═══', '// ═══ CAROUSEL ARROWS', 'lightbox'),
    ('// ═══ CAROUSEL ARROWS', '// ═══ DISPATCHES ═══', 'carousels'),
    ('// ═══ INQUIRY PANEL ═══', '// Resolve the URL on first paint', 'inquiry'),
]:
    s, _ = cut(s, a, b, why)
s = sub(s, '\n// Resolve the URL on first paint (direct links to a detail page).\napplyRoute();\n', '', 'applyRoute call')

# the Escape chain loses three of its four surfaces
s = sub(s, """document.addEventListener('keydown', (e) => {
  if (e.key !== 'Escape') return;
  if (isLightboxOpen()) { closeLightbox(); return; }
  if (closeNavMenu()) return;
  if (isInquiryOpen()) { closeInquiry(); return; }
  if (detailEl.classList.contains('open')) closeDetail();
});""",
        """document.addEventListener('keydown', (e) => {
  if (e.key !== 'Escape') return;
  closeNavMenu();
});""", 'escape chain')

# photoSlot loses the lightbox and gallery branches: this page has neither
s = sub(s, """function photoSlot(file, opts) {
  opts = opts || {};
  const cls = 'photo-slot' + (opts.cls ? ' ' + opts.cls : '');
  const pos = opts.pos ? `;--pos:${opts.pos}` : '';
  // data-lb marks a real photograph as openable in the lightbox. Placeholders
  // never get one, so an empty slot is not clickable.
  const lb = (opts.lb !== undefined && has(file))
    ? ` data-lb="${opts.lb}" role="button" tabindex="0" aria-label="Open photograph"` : '';
  if (!has(file)) return `<div class="${cls}" data-photo="${file}"></div>`;
  // opts.img renders a real <img> so it can be lazy-loaded. Used for gallery
  // photographs, which sit inside the detail view and are never needed until
  // that view opens.
  if (opts.img) {
    return `<div class="${cls}"${lb} style="--pos:${opts.pos || 'center'}">`
         + `<img class="photo-img" src="${file}" alt="" loading="lazy" decoding="async"></div>`;
  }
  return `<div class="${cls}"${lb} style="--photo:url('${file}')${pos}"></div>`;
}""",
        """function photoSlot(file, opts) {
  opts = opts || {};
  const cls = 'photo-slot' + (opts.cls ? ' ' + opts.cls : '');
  const pos = opts.pos ? `;--pos:${opts.pos}` : '';
  return has(file)
    ? `<div class="${cls}" style="--photo:url('${file}')${pos}"></div>`
    : `<div class="${cls}" data-photo="${file}"></div>`;
}""", 'photoSlot trim')

# Dispatches retires; news comes back inside Know the Mountain later. This
# runs after the block above, because the carousel cut uses the dispatches
# marker as its own end anchor.
s, _ = cut(s, '<!-- DISPATCHES -->', '<!-- BAND 1 -->', 'dispatches section')
s, _ = cut(s, '// ═══ DISPATCHES ═══', '// ═══ COMMUNITY TABS ═══', 'dispatches js')

# 1e. CSS that only the retired catalogue used
s, _ = cut(s, '  .carousel { position: relative; }', '  /* ─── DISPATCHES ─── */', 'carousel css')
s = sub(s, '''  .card-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: var(--s-5); }''',
        '''  .card-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: var(--s-5); }''',
        'card grid width')

# 1f. the journey card, shared by the teaser and the catalogue, lives in the
#     style block index owns so every page inherits it
JCARD_CSS = '''  /* ─── JOURNEY CARD ───
     Used by the Explore teaser here and by every catalogue grid on
     explore.html. The whole card is one link. */
  .jcard {
    display: flex; flex-direction: column;
    background: var(--card);
    border: 1px solid var(--rule);
    border-radius: var(--radius-lg);
    overflow: hidden; text-decoration: none;
    transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
  }
  .jcard:hover { transform: translateY(-3px); box-shadow: var(--shadow-card-hover); border-color: var(--rule-firm); }
  .jcard:focus-visible { outline: 2px solid var(--sienna); outline-offset: 2px; }
  .jcard-media { position: relative; aspect-ratio: 4 / 3; background: var(--placeholder); }
  .jcard-img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; display: block; }
  .jcard-body { display: flex; flex-direction: column; gap: 6px; padding: var(--s-4) var(--s-5) var(--s-5); }
  .jcard-name {
    font-family: var(--font-head); font-size: var(--t-lg); font-weight: 700;
    line-height: 1.2; letter-spacing: -0.01em; color: var(--ink);
  }
  .jcard-meta { display: flex; flex-wrap: wrap; gap: 4px 10px; align-items: baseline; }
  .jcard-elev {
    font-family: var(--font-head); font-size: var(--t-sm); font-weight: 700;
    color: var(--sienna); font-variant-numeric: tabular-nums;
  }
  .jcard-where { font-size: var(--t-sm); color: var(--ink-3); }
  .teaser-more { margin-top: var(--s-6); }

'''
s = sub(s, '  /* ─── DISPATCHES ─── */', JCARD_CSS + '  /* ─── DISPATCHES ─── */', 'jcard css')

# 1g. CSS for components the retired catalogue owned and nothing else uses.
#     The gallery rules stay: they are the lightbox's partner, and the lightbox
#     is kept deliberately for the galleries that come with the first detailed
#     journey. Verified dead by scanning all three pages for each class.
DEAD = ['.dispatch', '.dispatch-media', '.dispatch-body', '.dispatch-title',
        '.dispatch-meta', '.dispatch-excerpt', '.dispatch-grid', '.dispatch-more',
        '.dispatch:hover', '.dispatch[hidden]', '.dispatch-more[hidden]',
        '.tcard', '.tcard-media', '.tcard-body', '.tcard-head', '.tcard-name', '.tcard-loc',
        '.tcard-desc', '.tcard-foot', '.tcard-specs', '.tcard:hover',
        '.spec', '.spec-label', '.spec-dots', '.spec-value', '.spec-value--soft',
        '.spec-panel', '.spec-panel-title',
        '.badge-challenging', '.badge-moderate', '.badge-hard', '.badge-extreme',
        '.region-head', '.region-label', '.region-line',
        '.detail-grid', '.detail-body', '.photo-slot--corner', '.post-image']


def prune_css(css, dead):
    """Drop rules whose whole selector list is dead; trim dead selectors out of
    a shared list rather than deleting a rule some live selector still needs."""
    dead = set(dead)
    out, i, removed = [], 0, []
    for m in re.finditer(r'(?m)^(\s*)([^\n{}]+?)\s*\{([^{}]*)\}\n?', css):
        sels = [x.strip() for x in m.group(2).split(',')]
        if not sels or any(not x.startswith('.') for x in sels):
            continue
        live = [x for x in sels if x not in dead and x.split(':')[0] not in dead]
        if len(live) == len(sels):
            continue
        out.append((m.start(), m.end(), m.group(1) + ', '.join(live) + ' {' + m.group(3) + '}\n' if live else ''))
        removed += [x for x in sels if x not in live]
    for a, b, rep in reversed(out):
        css = css[:a] + rep + css[b:]
    return css, removed


_style = re.search(r'<style>(.*?)</style>', s, re.S)
_new, _gone = prune_css(_style.group(1), DEAD)
s = s[:_style.start(1)] + _new + s[_style.end(1):]
print('pruned %d dead CSS selectors: %s' % (len(_gone), ', '.join(sorted(set(_gone)))))


io.open(IDX, 'w', encoding='utf-8').write(s)
print('index.html rewritten  %d -> %d bytes' % (len(src), len(s)))

# ═════════════════════ PHASE 2 - generate explore.html ════════════════════
idx = s
STYLE = re.search(r'<style>(.*?)</style>', idx, re.S).group(1)
HEAD_LINKS = re.search(r'(<link rel="icon".*?<script>document\.documentElement.*?</script>)', idx, re.S).group(1)
NAV = re.search(r'<nav class="site-nav" id="navbar">.*?</nav>', idx, re.S).group(0)
FOOTER = re.search(r'<footer class="site-footer">.*?</footer>', idx, re.S).group(0)

# nav and footer are index relative; on another page they need the page name
def cross(block):
    block = re.sub(r'href="#(hero|story|community|dispatches|explore-teaser)"', r'href="index.html#\1"', block)
    block = block.replace(' onclick="switchTab(\'share\')"', '')
    return block

NAV_X, FOOTER_X = cross(NAV), cross(FOOTER)
NAV_X = NAV_X.replace('<li><a href="explore.html">Explore</a></li>',
                      '<li><a href="explore.html" class="is-active" aria-current="page">Explore</a></li>')

EXPLORE_CSS = '''
  /* ─── EXPLORE PAGE ─── */
  .explore-main { padding-top: 0; }
  .xhead { position: relative; overflow: hidden; background: var(--placeholder); }
  .xhead-media { position: absolute; inset: 0; }
  /* the placeholder label sits top left rather than dead centre, where it
     would print straight through the title and lede on a narrow screen */
  .xhead-media .photo-slot { height: 100%; align-items: flex-start; justify-content: flex-start; padding: var(--s-4); }
  .xhead-scrim { position: absolute; inset: 0; background: rgba(28,34,38,0.42); }
  .xhead-inner {
    position: relative; z-index: 2;
    max-width: var(--wrap); margin: 0 auto;
    padding: clamp(56px, 9vw, 104px) var(--s-5);
  }
  .xhead-title {
    font-family: var(--font-hero); font-weight: 900;
    font-size: clamp(38px, 6vw, 68px); line-height: 1.04;
    letter-spacing: -0.02em; color: #fff;
    text-shadow: 0 2px 20px rgba(20,24,27,0.35);
  }
  .xhead-lede {
    font-family: var(--font-hero); font-weight: 400;
    font-size: clamp(16px, 2vw, 20px); line-height: 1.5;
    color: #fff; max-width: 52ch; margin-top: var(--s-3);
    text-shadow: 0 1px 14px rgba(20,24,27,0.4);
  }

  /* the two rails */
  .rail-toggle {
    display: flex; gap: 0; margin: var(--s-7) 0 var(--s-5);
    border-bottom: 1px solid var(--rule-firm);
  }
  .rail-btn {
    appearance: none; background: none; border: none; cursor: pointer;
    font-family: var(--font-head); font-size: clamp(15px, 2.1vw, 20px);
    font-weight: 800; letter-spacing: 0.1em; text-transform: uppercase;
    color: var(--ink-3); padding: 0 var(--s-5) var(--s-4);
    border-bottom: 3px solid transparent;
    transition: color 0.15s ease, border-color 0.15s ease;
  }
  .rail-btn:first-child { padding-left: 0; }
  .rail-btn:hover { color: var(--ink-2); }
  .rail-btn[aria-selected="true"] { color: var(--ink); border-bottom-color: var(--sienna); }

  /* category tabs. They scroll sideways on a phone rather than wrapping into
     a block that pushes the grid off the first screen. */
  .cat-tabs {
    display: flex; gap: var(--s-2);
    overflow-x: auto; scrollbar-width: none;
    padding-bottom: var(--s-3); margin-bottom: var(--s-6);
    -webkit-overflow-scrolling: touch;
  }
  .cat-tabs::-webkit-scrollbar { display: none; }
  .cat-btn {
    appearance: none; cursor: pointer; white-space: nowrap;
    font-family: var(--font-head); font-size: var(--t-sm); font-weight: 600;
    letter-spacing: 0.04em;
    color: var(--ink-2); background: var(--card);
    border: 1px solid var(--rule-firm); border-radius: 999px;
    padding: 9px var(--s-4);
    transition: background 0.15s ease, color 0.15s ease, border-color 0.15s ease;
  }
  .cat-btn:hover { border-color: var(--ink-3); color: var(--ink); }
  .cat-btn[aria-selected="true"] { background: var(--sienna); border-color: var(--sienna); color: #fff; }
  .cat-count { opacity: 0.65; font-variant-numeric: tabular-nums; }

  .rail[hidden], .catpanel[hidden] { display: none; }
  .panel-heading {
    font-family: var(--font-head); font-size: var(--t-lg); font-weight: 700;
    color: var(--ink); margin: var(--s-6) 0 var(--s-4);
  }
  .js .panel-heading { display: none; }

  /* With JavaScript off nothing can switch, so every rail and every category
     is shown at once, each under its own heading, and the controls that would
     do nothing are hidden. */
  .no-js .rail-toggle, .no-js .cat-tabs { display: none; }
  .no-js .rail[hidden], .no-js .catpanel[hidden] { display: block; }
  .rail-heading {
    font-family: var(--font-head); font-size: var(--t-2xl); font-weight: 800;
    letter-spacing: 0.06em; text-transform: uppercase;
    color: var(--ink); margin: var(--s-7) 0 var(--s-4);
  }
  .js .rail-heading { display: none; }

  /* The static catalogue entry behind every card. It is what a crawler and a
     reader without JavaScript get; the router hides it and renders the same
     facts into the overlay instead. */
  .journey-static { display: none; }
  .journey-static:target { display: block; }
  .js .journey-static, .js .journey-static:target { display: none; }
  .jstatic-inner {
    max-width: 62ch; margin: var(--s-7) auto;
    padding: var(--s-6); background: var(--card);
    border: 1px solid var(--rule); border-radius: var(--radius-lg);
  }
  .jstatic-inner h2 { font-family: var(--font-head); font-size: var(--t-2xl); font-weight: 700; color: var(--ink); }

  /* catalogue state inside the detail overlay */
  .cat-note {
    margin-top: var(--s-5); padding: var(--s-5);
    background: var(--surface-alt); border: 1px solid var(--rule);
    border-radius: var(--radius); color: var(--ink-2);
    font-size: var(--t-base); line-height: 1.6;
  }
  .fact-strip {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: var(--s-4); margin-top: var(--s-5);
    padding: var(--s-5) 0; border-top: 1px solid var(--rule); border-bottom: 1px solid var(--rule);
  }
  .fact-label {
    font-family: var(--font-head); font-size: 10px; font-weight: 700;
    letter-spacing: 0.14em; text-transform: uppercase; color: var(--ink-3);
  }
  .fact-value { font-family: var(--font-head); font-size: var(--t-lg); font-weight: 700; color: var(--ink); margin-top: 3px; }

  /* ─── KNOWLEDGE BASE SECTIONS ─── */
  .jstatic-title { font-family: var(--font-head); font-size: var(--t-2xl); font-weight: 700; color: var(--ink); }
  .js .detail-slot .fact-strip:first-child { margin-top: 0; }
  .detail-body-text { color: var(--ink-2); line-height: 1.7; max-width: 62ch; }

  .know-list { list-style: none; display: grid; gap: var(--s-4); }
  .know-list li {
    padding-left: var(--s-5); border-left: 2px solid var(--sienna);
    color: var(--ink-2); line-height: 1.6; max-width: 62ch;
  }

  .faq-item { padding: var(--s-4) 0; border-bottom: 1px solid var(--rule); }
  .faq-item:last-child { border-bottom: none; }
  .faq-q { font-family: var(--font-head); font-weight: 600; color: var(--ink); }
  .faq-a { color: var(--ink-2); line-height: 1.6; margin-top: 3px; }

  .jcta {
    margin-top: var(--s-7); padding: var(--s-6);
    background: var(--surface-alt); border: 1px solid var(--rule);
    border-radius: var(--radius-lg); text-align: center;
  }
  .jcta-line { color: var(--ink-2); margin-bottom: var(--s-4); }
  .jcta .btn { cursor: pointer; }

  /* ─── ROUTE ARTWORK SLOT ───
     The route drawing is supplied as artwork, one file per journey, named
     route-map-<slug>.jpg. Until it exists the figure removes itself: an
     onerror handler hides it, so an absent map shows nothing rather than a
     broken image icon or a grey rectangle pretending to be a map. */
  .route-fig { margin: 0; }
  .route-fig[hidden] { display: none; }
  .route-art {
    display: block; width: 100%; height: auto;
    max-height: 80vh; object-fit: contain;
    margin: 0 auto;
    border: 1px solid var(--rule); border-radius: var(--radius-lg);
    background: var(--surface-alt);
  }

  .detail-section { margin-top: var(--s-7); }
  .detail-section-title {
    font-family: var(--font-head); font-size: var(--t-xl); font-weight: 700;
    color: var(--ink); margin-bottom: var(--s-4);
  }
  .hl-list, .cov-list { list-style: none; display: flex; flex-direction: column; gap: var(--s-3); }
  .hl-list li, .cov-list li { position: relative; padding-left: var(--s-5); color: var(--ink-2); line-height: 1.6; }
  .hl-list li::before, .cov-list li::before { content: '\\2726'; position: absolute; left: 0; color: var(--sienna); }
  .day { border-bottom: 1px solid var(--rule); }
  .day summary {
    cursor: pointer; padding: var(--s-4) 0; list-style: none;
    font-family: var(--font-head); font-weight: 600; color: var(--ink);
    display: flex; gap: var(--s-4);
  }
  .day summary::-webkit-details-marker { display: none; }
  .day-n { color: var(--sienna); font-variant-numeric: tabular-nums; }
  .day p { padding: 0 0 var(--s-4); color: var(--ink-2); line-height: 1.6; }
  .two-col { display: grid; grid-template-columns: 1fr 1fr; gap: var(--s-6); }
  @media (max-width: 640px) { .two-col { grid-template-columns: 1fr; } }
'''

# ── static catalogue grids, so every card exists without JavaScript ────────
def grid(items, href_fn):
    return '\n'.join(jcard(r, href_fn(r)) for r in items)


def panels(tabs, pick, kind):
    out = []
    for i, (label, key) in enumerate(tabs):
        items = [r for r in J if pick(r, key)]
        out.append(
            '        <div class="catpanel" id="panel-%s-%s" role="tabpanel"\n'
            '             aria-labelledby="tab-%s-%s"%s>\n'
            '          <h2 class="panel-heading">%s</h2>\n'
            '          <div class="card-grid">\n%s\n          </div>\n'
            '        </div>' % (kind, i, kind, i, '' if i == 0 else ' hidden', label,
                                grid(items, lambda r: '#journey/' + r['slug'])))
    return '\n'.join(out)


def tabstrip(tabs, pick, kind):
    out = []
    for i, (label, key) in enumerate(tabs):
        n = sum(1 for r in J if pick(r, key))
        out.append('          <button class="cat-btn" type="button" role="tab" id="tab-%s-%s"\n'
                   '                  aria-controls="panel-%s-%s" aria-selected="%s" data-rail="%s" data-tab="%s">'
                   '%s <span class="cat-count">%d</span></button>'
                   % (kind, i, kind, i, 'true' if i == 0 else 'false', kind, i, label, n))
    return '\n'.join(out)


EXP_TABS = EXPEDITION_TABS
TRK_TABS = [(t, t) for t in TREK_TABS]
exp_pick = lambda r, key: r['category'] == key
trk_pick = lambda r, key: r['category'] == TK and r['region'] == key

N_EXP = sum(1 for r in J if r['category'] != TK)
N_TRK = sum(1 for r in J if r['category'] == TK)


def esc_amp(v):
    """Escape a bare ampersand without touching an entity that is already
    escaped. Season strings carry a literal & from the copy."""
    return re.sub(r'&(?!#?\w+;)', '&amp;', str(v))


def facts_html(pairs):
    live = [(l, esc_amp(v)) for l, v in pairs if v]
    if not live:
        return ''
    return ('        <div class="fact-strip">\n'
            + '\n'.join('          <div><p class="fact-label">%s</p><p class="fact-value">%s</p></div>'
                        % (l, v) for l, v in live)
            + '\n        </div>')


def cta_html(name):
    """The quiet interest close. The button is a real mailto link in the
    markup, so it works with JavaScript off; the router upgrades it to the
    interest panel when JavaScript is running."""
    subj = name.replace(' ', '%20').replace('&', 'and')
    return '''        <div class="jcta">
          <p class="jcta-line">Groups form each season. Join the interest list and you&rsquo;ll hear first.</p>
          <a class="btn btn-primary" href="mailto:hello@themountaindiaries.com?subject=Interest:%s"
             data-interest="%s">Join the Group <span aria-hidden="true">&rarr;</span></a>
        </div>''' % (subj, esc_attr(name))


def esc_attr(v):
    return v.replace('&', '&amp;').replace('"', '&quot;')


def detailed_body(r, d):
    """The knowledge base frame. No day by day table: the map carries the
    shape of the trip. No pricing and no logistics anywhere."""
    facts = facts_html([
        ('Duration', d.get('duration')),
        # an optional label names the point, where the bare number would
        # invite the wrong reading
        ('Max altitude', ('%s%s m' % ('~' if r.get('elev_approx') else '',
                                       format(r['elevation_m'], ','))
                          + (' (%s)' % d['highPoint'] if d.get('highPoint') else ''))
         if r['elevation_m'] else None),
        ('Difficulty', r.get('difficulty')),
        ('Best season', d.get('season')),
        # the copy may name the range rather than the rail's tab bucket
        ('Region', d.get('regionLabel') or '%s, %s' % (r['region'], r['country'])),
    ])
    know = '\n'.join('            <li>%s</li>' % k for k in d['know'])
    hl = '\n'.join('            <li>%s</li>' % h for h in d['highlights'])
    faq = '\n'.join(
        '            <div class="faq-item"><p class="faq-q">%s</p><p class="faq-a">%s</p></div>'
        % (q, a) for q, a in d['faq'])
    return '''%s
        <div class="detail-section">
          <h3 class="detail-section-title">The journey</h3>
          <p class="detail-lede">%s</p>
        </div>

        <div class="detail-section">
          <h3 class="detail-section-title">Know before you dream</h3>
          <ul class="know-list">
%s
          </ul>
        </div>

        <div class="detail-section">
          <h3 class="detail-section-title">Route</h3>
%s
        </div>

        <div class="detail-section">
          <h3 class="detail-section-title">Highlights</h3>
          <ul class="hl-list">
%s
          </ul>
        </div>

        <div class="detail-section">
          <h3 class="detail-section-title">Gear and preparation</h3>
          <p class="detail-body-text">%s</p>
          <p><a class="link-action" href="know.html#gear">Kit lists and altitude guidance in Know the Mountain <span aria-hidden="true">&rarr;</span></a></p>
        </div>

        <div class="detail-section">
          <h3 class="detail-section-title">Questions</h3>
%s
        </div>

%s''' % (facts, d['journey'], know,
          route_slot(r['slug']), hl, d['gear'], faq, cta_html(r['name']))


def route_slot(slug):
    """The route artwork slot, one file per journey: route-map-<slug>.jpg.

    Until the artwork exists the slot emits no <img> at all. An <img> pointing
    at a missing file would 404 on every visit and flash a broken icon before
    any onerror could hide it; an empty figure costs nothing and shows nothing.
    The expected filename stays in the markup so there is no guessing what to
    drop in, and the next build picks it up automatically."""
    art = 'route-map-%s.jpg' % slug
    if not os.path.exists(os.path.join(REPO, 'assets', 'images', art)):
        return ('          <!-- Route artwork pending. Drop assets/images/%s in\n'
                '               and re-run the build; the slot fills itself. -->\n'
                '          <figure class="route-fig" data-route-art="%s" hidden></figure>'
                % (art, art))
    return '''          <figure class="route-fig" data-route-art="%s">
            <img class="route-art" src="assets/images/%s" alt="Route map" loading="lazy" decoding="async">
          </figure>''' % (art, art)


def catalogue_body(r):
    facts = facts_html([
        ('Elevation', '%s m' % format(r['elevation_m'], ',') if r['elevation_m'] else None),
        ('Region', r['region']), ('Country', r['country'])])
    return '''%s
        <p class="cat-note">Full route notes are being written. Groups form when demand and
        partnerships align. Join the interest list and you&rsquo;ll hear first.</p>
%s''' % (facts, cta_html(r['name']))


def static_entry(r):
    """Every journey's content lives here, in markup. Without JavaScript the
    :target rule reveals it; with JavaScript the router lifts the .jdetail
    block into the overlay, so there is exactly one copy of the content."""
    d = DETAILS.get(r['slug'])
    body = detailed_body(r, d) if d else catalogue_body(r)
    return '''    <section class="journey-static" id="journey/%s">
      <div class="jstatic-inner">
        <h2 class="jstatic-title">%s</h2>
        <div class="jdetail" data-journey="%s">
%s
        </div>
      </div>
    </section>''' % (r['slug'], r['name'], r['slug'], body)


BODY = '''<main class="explore-main">

  <!-- PAGE HEADER -->
  <section class="xhead">
    <div class="xhead-media"><div class="photo-slot" data-photo="explore-header.jpg"></div></div>
    <div class="xhead-scrim" aria-hidden="true"></div>
    <div class="xhead-inner">
      <h1 class="xhead-title">Explore</h1>
      <p class="xhead-lede">Every journey we run or plan to run, from a first 6,000 metre summit
      to the eight thousanders, and the trekking routes that lead to them.</p>
    </div>
  </section>

  <section class="section">
    <div class="wrap">

      <div class="rail-toggle" role="tablist" aria-label="Expeditions or trekking">
        <button class="rail-btn" type="button" role="tab" id="rail-btn-exp"
                aria-controls="rail-exp" aria-selected="true" data-rail-target="exp">Expeditions</button>
        <button class="rail-btn" type="button" role="tab" id="rail-btn-trk"
                aria-controls="rail-trk" aria-selected="false" data-rail-target="trk">Trekking</button>
      </div>

      <!-- EXPEDITIONS RAIL -->
      <div class="rail" id="rail-exp" role="tabpanel" aria-labelledby="rail-btn-exp">
        <h2 class="rail-heading">Expeditions</h2>
        <div class="cat-tabs" role="tablist" aria-label="Expedition categories">
%s
        </div>
%s
      </div>

      <!-- TREKKING RAIL -->
      <div class="rail" id="rail-trk" role="tabpanel" aria-labelledby="rail-btn-trk" hidden>
        <h2 class="rail-heading">Trekking</h2>
        <div class="cat-tabs" role="tablist" aria-label="Trekking regions">
%s
        </div>
%s
      </div>

    </div>
  </section>

  <!-- Static catalogue entries. Hidden while JavaScript runs; revealed by
       :target when it does not, so every #journey/<slug> resolves to real
       content and a crawler sees all %d journeys. -->
%s

</main>''' % (tabstrip(EXP_TABS, exp_pick, 'exp'), panels(EXP_TABS, exp_pick, 'exp'),
              tabstrip(TRK_TABS, trk_pick, 'trk'), panels(TRK_TABS, trk_pick, 'trk'),
              len(J), '\n'.join(static_entry(r) for r in J))

# ── explore JS ────────────────────────────────────────────────────────────
JOURNEY_JS = '''
// ═══ JOURNEYS ═══
// Single source of truth for the catalogue. One entry per journey.
//   status 'catalogue' renders the honest short state
//   status 'detailed'  renders the full template further down
// Elevations are the ones carried in each journey's own name. Combinations
// take the high point of the peaks they name; where no height is stated
// anywhere the field is null and every view simply omits the line.
const JOURNEYS = [
%s
];

const BY_SLUG = {};
JOURNEYS.forEach(j => { BY_SLUG[j.slug] = j; });

const CATEGORY_LABEL = {
  '8000ers': '8000ers', '7000ers': '7000ers', '6000ers': '6000ers', trek: 'Trekking'
};

const journeyPhoto = (j) => IMG + 'journey-' + j.slug + '.jpg';
const metres = (n) => n ? n.toLocaleString('en-US') + ' m' : null;

// ═══ DETAIL VIEW ═══
// A journey gets its own screen at #journey/<slug>. The hash is the single
// source of truth, so the back button and a pasted URL both behave.
const detailEl = document.getElementById('detail-view');
const detailContent = document.getElementById('detail-content');

// The body of every journey already exists in the document, inside its
// .journey-static block. The router moves a copy of that into the overlay
// rather than rebuilding it from the data, so the version a reader without
// JavaScript sees and the version in the overlay cannot drift apart.
function journeyBody(slug) {
  const src = document.querySelector(`.jdetail[data-journey="${CSS.escape(slug)}"]`);
  return src ? src.cloneNode(true) : null;
}

function detailShell(j) {
  return `
  <div class="detail-hero">
    ${photoSlot(journeyPhoto(j), { lb: 0 })}
    <div class="detail-hero-info">
      <div class="detail-hero-inner">
        <p class="detail-region">${j.region} &middot; ${j.country}</p>
        <h1 class="detail-title" id="detail-title">${j.name}</h1>
      </div>
    </div>
  </div>

  <div class="wrap">
    <div class="detail-slot"></div>
    <div class="detail-foot">
      <button class="btn btn-outline" type="button" onclick="closeDetail()">
        <span aria-hidden="true">&larr;</span> All journeys
      </button>
    </div>
  </div>`;
}

function showDetail(slug) {
  const j = BY_SLUG[slug];
  if (!j) { hideDetail(); return false; }
  _detailImages = has(journeyPhoto(j)) ? [{ file: journeyPhoto(j), cap: '' }] : [];
  detailContent.innerHTML = detailShell(j);
  const body = journeyBody(slug);
  if (body) {
    detailContent.querySelector('.detail-slot').appendChild(body);
    // the mailto is the no-JavaScript path; here the panel is better
    const cta = detailContent.querySelector('[data-interest]');
    if (cta) {
      cta.removeAttribute('href');
      cta.setAttribute('role', 'button');
      cta.setAttribute('tabindex', '0');
      const open = () => openInquiry(cta.getAttribute('data-interest'),
                                     cta.getAttribute('data-interest'),
                                     CATEGORY_LABEL[j.category], journeyPhoto(j));
      cta.addEventListener('click', open);
      cta.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); }
      });
    }
  }
  detailEl.classList.add('open');
  detailEl.scrollTop = 0;
  document.body.style.overflow = 'hidden';
  return true;
}

function hideDetail() {
  detailEl.classList.remove('open');
  detailContent.innerHTML = '';
  if (!isInquiryOpen()) document.body.style.overflow = '';
}

function parseHash() {
  const m = /^#journey\\/([a-z0-9-]+)$/.exec(location.hash);
  return m ? m[1] : null;
}

let _routeInit = false;
let _openedFromWithinPage = false;

function applyRoute() {
  const slug = parseHash();
  if (slug) {
    _openedFromWithinPage = _routeInit;
    if (!showDetail(slug)) _openedFromWithinPage = false;
  } else {
    hideDetail();
  }
  _routeInit = true;
}

function closeDetail() {
  if (!parseHash()) { hideDetail(); return; }
  if (_openedFromWithinPage) {
    history.back();                       // keeps the back button honest
  } else {
    // Arrived straight on the detail URL, so there is nothing to go back to.
    history.replaceState(null, '', location.pathname + location.search);
    applyRoute();
  }
}

window.addEventListener('hashchange', applyRoute);
document.getElementById('detail-back').addEventListener('click', closeDetail);

// ═══ RAILS AND CATEGORY TABS ═══
(function () {
  const railBtns = [...document.querySelectorAll('.rail-btn')];
  const rails = { exp: document.getElementById('rail-exp'), trk: document.getElementById('rail-trk') };
  railBtns.forEach(b => b.addEventListener('click', () => {
    const target = b.getAttribute('data-rail-target');
    railBtns.forEach(x => x.setAttribute('aria-selected', String(x === b)));
    Object.keys(rails).forEach(k => { rails[k].hidden = (k !== target); });
  }));

  document.querySelectorAll('.cat-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const rail = btn.getAttribute('data-rail');
      const peers = [...document.querySelectorAll(`.cat-btn[data-rail="${rail}"]`)];
      peers.forEach(p => {
        const on = p === btn;
        p.setAttribute('aria-selected', String(on));
        document.getElementById(p.getAttribute('aria-controls')).hidden = !on;
      });
    });
  });
})();
''' % ('\n'.join(
    "  { slug: '%s', name: '%s', elevation_m: %s, category: '%s', region: '%s', country: '%s',"
    " difficulty: %s, status: '%s' },"
    % (r['slug'], r['name'].replace("'", "\\'"), r['elevation_m'] if r['elevation_m'] else 'null',
       r['category'], r['region'], r['country'].replace("'", "\\'"),
       ("'%s'" % r['difficulty']) if r['difficulty'] else 'null', r['status'])
    for r in J))

# the interest dropdown, every journey grouped by category
OPTGROUPS = []
for label, key in EXP_TABS + [('Trekking', TK)]:
    items = [r for r in J if r['category'] == key]
    OPTGROUPS.append('            <optgroup label="%s">\n%s\n            </optgroup>' % (
        label, '\n'.join('              <option>%s</option>' % r['name'] for r in items)))
JOURNEY_SELECT = '''        <div class="field">
          <label for="inq-journey">Which journey</label>
          <select id="inq-journey" name="expedition" required>
            <option value="">Select a journey</option>
%s
          </select>
        </div>
''' % '\n'.join(OPTGROUPS)

INQ = INQUIRY_MARKUP.replace('''        <div class="field">
          <label for="inq-experience">Your experience level</label>''',
                             JOURNEY_SELECT + '''        <div class="field">
          <label for="inq-experience">Your experience level</label>''')

# openInquiry now preselects the journey, and the submitted value follows the
# dropdown so a visitor can change their mind inside the panel
INQ_JS = INQUIRY_JS.replace("""  document.getElementById('inquiry-form').reset();""",
"""  document.getElementById('inquiry-form').reset();
  // preselect the journey the panel was opened from, if it is in the list
  const sel = document.getElementById('inq-journey');
  const match = [...sel.options].find(o => o.value === subjectName || o.text === subjectName);
  sel.value = match ? match.value || match.text : '';""")
INQ_JS = INQ_JS.replace("      expedition: _currentInquiry,",
                        "      expedition: document.getElementById('inq-journey').value || _currentInquiry,")
INQ_JS = INQ_JS.replace("function showSuccess() {\n  document.getElementById('inquiry-success-name').textContent = _currentInquiry;",
                        "function showSuccess() {\n  document.getElementById('inquiry-success-name').textContent =\n    document.getElementById('inq-journey').value || _currentInquiry;")

PAGE = '''<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Explore &middot; The Mountain Diaries</title>
<meta name="description" content="Every expedition and trekking journey run by The Mountain Diaries, from a first 6,000 metre summit to the eight thousanders.">
''' + HEAD_LINKS + '''
<style>
''' + STYLE.rstrip('\n') + EXPLORE_CSS + '''</style>
</head>
<body>

''' + LIGHTBOX_MARKUP + '''
''' + DETAIL_MARKUP.replace('<span id="detail-back-label">All trails</span>',
                            '<span id="detail-back-label">All journeys</span>') + '''
''' + INQ + '''

''' + NAV_X + '''

''' + BODY + '''

''' + FOOTER_X + '''

<script>
''' + PHOTO_JS.rstrip() + '''

''' + JOURNEY_JS.strip() + '''

''' + LIGHTBOX_JS.strip() + '''

''' + NAV_JS.strip() + '''

// ═══ SINGLE ESCAPE HANDLER ═══
// One listener, most-nested surface first.
document.addEventListener('keydown', (e) => {
  if (e.key !== 'Escape') return;
  if (isLightboxOpen()) { closeLightbox(); return; }
  if (closeNavMenu()) return;
  if (isInquiryOpen()) { closeInquiry(); return; }
  if (detailEl.classList.contains('open')) closeDetail();
});

''' + POSTFORM_JS.strip() + '''

''' + INQ_JS.strip() + '''

// Resolve the URL on first paint (direct links to a journey).
applyRoute();
</script>
</body>
</html>
'''

# the detail router owns the whole card, and each card is already a link
PAGE = PAGE.replace("const isLightboxOpen", "const isLightboxOpen", 1)

io.open(os.path.join(OUT, 'explore.html'), 'w', encoding='utf-8').write(PAGE)
print('explore.html written  %d bytes, %d journeys' % (len(PAGE), len(J)))
print('  expeditions %d in %d tabs, treks %d in %d tabs' % (N_EXP, len(EXP_TABS), N_TRK, len(TRK_TABS)))

# ══════════════ PHASE 3 - keep join.html's generator in sync ══════════════
# p3-join.py owns join.html. Its nav, footer and head links are refreshed from
# index.html here, so a change to any of the three shared parts reaches every
# page from one place.
pj = os.path.join(HERE, 'p3-join.py')
g = io.open(pj, encoding='utf-8').read()
g = re.sub(r'<nav class="site-nav" id="navbar">.*?</nav>', lambda m: NAV_X.replace(
    ' class="is-active" aria-current="page"', ''), g, count=1, flags=re.S)
g = re.sub(r'<footer class="site-footer">.*?</footer>', lambda m: FOOTER_X, g, count=1, flags=re.S)
io.open(pj, 'w', encoding='utf-8').write(g)
print('p3-join.py nav and footer re-synced from index.html')

# -*- coding: utf-8 -*-
"""About, Privacy, Terms and Photo credits.

Plain content pages, generated from index.html's style block plus the shared
nav and footer, exactly like know.py, so they cannot drift from the rest of
the site. Runs after explore-build.py.

Copy follows the STYLE rules in details.py: British spelling, curly
apostrophes and quotes, no em dashes.
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import seo

OUT_DIR = os.environ.get('MD_OUT') or REPO
src = io.open(os.path.join(OUT_DIR, 'index.html'), encoding='utf-8').read()
style = re.search(r'<style>(.*?)</style>', src, re.S).group(1)
head_links = re.search(r'(<link rel="icon".*?<script>document\.documentElement.*?</script>)',
                       src, re.S).group(1)
nav = re.search(r'<nav class="site-nav" id="navbar">.*?</nav>', src, re.S).group(0)
footer = re.search(r'<footer class="site-footer">.*?</footer>', src, re.S).group(0)
nav_js = re.search(r'// ═══ NAV ═══.*?\n\}\)\(\);\n', src, re.S).group(0)


def cross(block):
    block = re.sub(r'href="#(hero|story|community|explore-teaser|know-teaser)"',
                   r'href="index.html#\1"', block)
    return block.replace(' onclick="switchTab(\'share\')"', '')


nav, footer = cross(nav), cross(footer)

CSS = """
  /* ─── CONTENT PAGES ─── */
  .page-main { padding-top: 0; }
  .phead {
    position: relative; overflow: hidden;
    background: var(--surface-alt);
    border-bottom: 1px solid var(--rule);
    padding: clamp(48px, 7vw, 88px) 0 clamp(36px, 5vw, 60px);
  }
  .phead--photo { background: var(--ink); border-bottom: none; padding: clamp(72px, 11vw, 140px) 0 clamp(48px, 7vw, 84px); }
  .phead-media { position: absolute; inset: 0; background-size: cover; background-position: center 40%; }
  .phead-scrim { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(28,34,38,0.25), rgba(28,34,38,0.62)); }
  .phead-inner { position: relative; z-index: 2; max-width: var(--wrap); margin: 0 auto; padding: 0 var(--s-5); }
  .phead-title {
    font-family: var(--font-hero); font-weight: 900;
    font-size: clamp(34px, 5.4vw, 60px); line-height: 1.05;
    letter-spacing: -0.02em; color: var(--ink);
  }
  .phead-lede { font-size: clamp(16px, 2vw, 19px); line-height: 1.55; color: var(--ink-2); max-width: 56ch; margin-top: var(--s-3); }
  .phead--photo .phead-title, .phead--photo .phead-lede { color: #fff; text-shadow: 0 2px 18px rgba(20,24,27,0.35); }
  .page-body { max-width: var(--wrap); margin: 0 auto; padding: clamp(40px, 6vw, 72px) var(--s-5); }
  .prose { max-width: 70ch; }
  .prose h2 {
    font-family: var(--font-head); font-size: clamp(21px, 2.6vw, 27px); font-weight: 800;
    letter-spacing: -0.01em; color: var(--ink);
    margin: var(--s-7) 0 var(--s-3);
  }
  .prose h2:first-child { margin-top: 0; }
  .prose p, .prose li { font-size: var(--t-base); line-height: 1.7; color: var(--ink-2); }
  .prose p + p { margin-top: var(--s-3); }
  .prose ul { margin: var(--s-3) 0 0 1.1em; }
  .prose li + li { margin-top: var(--s-2); }
  .prose a { color: var(--sienna); }
  .prose strong { color: var(--ink); }
  .prose .updated { font-size: var(--t-sm); color: var(--ink-3); margin-bottom: var(--s-6); }
  .pillars { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: var(--s-5); margin: var(--s-6) 0; max-width: none; }
  .pillar { background: var(--card); border: 1px solid var(--rule); border-radius: var(--radius-lg); padding: var(--s-5); box-shadow: var(--shadow-card); }
  .pillar h3 { font-family: var(--font-head); font-size: var(--t-lg); font-weight: 700; color: var(--ink); margin-bottom: var(--s-2); }
  .pillar p { font-size: var(--t-base); line-height: 1.6; color: var(--ink-2); }
  .steps { counter-reset: step; list-style: none; margin: var(--s-4) 0 0; padding: 0; }
  .steps li { counter-increment: step; position: relative; padding-left: 44px; margin-top: var(--s-4); }
  .steps li::before {
    content: counter(step); position: absolute; left: 0; top: 0;
    width: 30px; height: 30px; border-radius: 50%;
    background: var(--sienna); color: #fff;
    font-family: var(--font-head); font-weight: 700; font-size: 14px;
    display: flex; align-items: center; justify-content: center;
  }
  .steps-row { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 0.9fr); gap: clamp(28px, 5vw, 64px); align-items: center; max-width: none; }
  .steps-photo { margin: 0; border-radius: var(--radius-lg); overflow: hidden; box-shadow: var(--shadow-card); background: var(--card); }
  .steps-photo img { display: block; width: 100%; aspect-ratio: 4 / 3; object-fit: cover; }
  .steps-photo figcaption { padding: var(--s-3) var(--s-4); font-size: var(--t-sm); color: var(--ink-3); }
  .steps li { font-size: var(--t-base); line-height: 1.7; color: var(--ink-2); }
  @media (max-width: 860px) { .steps-row { grid-template-columns: 1fr; } }
  .page-cta { display: flex; flex-wrap: wrap; gap: var(--s-3); margin-top: var(--s-7); }
  .credits-table { width: 100%; border-collapse: collapse; font-size: var(--t-sm); margin-top: var(--s-4); }
  .credits-table th, .credits-table td { text-align: left; padding: 10px 12px; border-bottom: 1px solid var(--rule); vertical-align: top; color: var(--ink-2); }
  .credits-table th { font-family: var(--font-head); font-weight: 700; color: var(--ink); background: var(--surface-alt); }
  .credits-table a { color: var(--sienna); }
  .table-scroll { overflow-x: auto; }
"""


def page(filename, title, description, header, body, image=None, active=None):
    n = nav
    if active:
        n = n.replace('<li><a href="%s">' % filename, '<li><a href="%s" class="is-active" aria-current="page">' % filename)
    if image:
        head_html = '''  <section class="phead phead--photo">
    <div class="phead-media" style="background-image:url('%s')" aria-hidden="true"></div>
    <div class="phead-scrim" aria-hidden="true"></div>
    <div class="phead-inner">%s</div>
  </section>''' % (image, header)
    else:
        head_html = '''  <section class="phead">
    <div class="phead-inner">%s</div>
  </section>''' % header
    html = '''<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%s &middot; The Mountain Diaries</title>
%s
%s
<style>
%s%s</style>
</head>
<body>

%s

<main class="page-main">
%s
  <div class="page-body">
%s
  </div>
</main>

%s

<script>
%s
document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeNavMenu(); });
</script>
</body>
</html>
''' % (title, seo.meta(title, description, filename, image or seo.DEFAULT_IMAGE), head_links,
       style.rstrip('\n'), CSS, n, head_html, body, footer, nav_js)
    io.open(os.path.join(OUT_DIR, filename), 'w', encoding='utf-8').write(html)
    print('%s written, %d bytes' % (filename, len(html)))


# ═══════════════════════════════ ABOUT ═══════════════════════════════════
page('about.html', 'About Us',
     'The Mountain Diaries is a UAE trekking and expedition community: local hikes most months, '
     'small groups for the big routes, and honest knowledge about altitude.',
     '''
      <h1 class="phead-title">About Us</h1>
      <p class="phead-lede">A UAE community for people drawn to the high places, and who want to reach them properly.</p>''',
     '''
    <div class="prose">
      <h2>Why we exist</h2>
      <p>The Mountain Diaries began with a question that would not leave: what are you actually made of? The mountains answered it the way they always do, slowly, and by taking away everything that was not needed.</p>
      <p>What came out of it is a community. People across the UAE who walk together on weekends, and who travel together, in small groups, to the ranges they used to only read about.</p>

      <h2>What we do</h2>
    </div>
    <div class="pillars">
      <div class="pillar">
        <h3>Local hikes</h3>
        <p>Most months, from easy wadi walks to long days in the Hajar mountains of Ras Al Khaimah. The best training there is, and the best way to meet the people you will trek with.</p>
      </div>
      <div class="pillar">
        <h3>Expedition groups</h3>
        <p>Small groups for the big routes: Nepal, the Alps, Patagonia, Peru and Kilimanjaro, from a first trek to a first 6,000 metre summit and beyond.</p>
      </div>
      <div class="pillar">
        <h3>Knowledge and stories</h3>
        <p>Honest guidance on altitude, training, gear and judgement, and stories from people who have walked the route before you.</p>
      </div>
    </div>
    <div class="prose">
      <h2>How a group comes together</h2>
    </div>
    <div class="steps-row">
      <ol class="steps">
        <li><strong>Join the community.</strong> It takes a minute, and you will hear about hikes and new journeys first.</li>
        <li><strong>Tell us what calls you.</strong> Every journey page has a Join the Group button. It costs nothing and commits you to nothing.</li>
        <li><strong>We line it up.</strong> When enough people want the same route in the same season, we confirm dates, costs and the plan with licensed local guides and operators.</li>
        <li><strong>You decide.</strong> You see the full itinerary, the price and what it asks of you before you say yes.</li>
      </ol>
      <figure class="steps-photo">
        <img src="assets/images/expedition-ebc.jpg" alt="Mani stones on the trail to Everest Base Camp, with Lhotse and Nuptse ahead" loading="lazy" decoding="async">
        <figcaption>On the trail to Everest Base Camp, Lhotse and Nuptse ahead.</figcaption>
      </figure>
    </div>
    <div class="prose">

      <h2>What we believe</h2>
      <ul>
        <li><strong>Altitude sets the pace.</strong> Fitness gets you to the trailhead. Acclimatisation gets you home. Every itinerary is built around it.</li>
        <li><strong>Honest information, always.</strong> We would rather tell you a route is not right for you yet than sell you a place on it.</li>
        <li><strong>Local people, local guides.</strong> The mountains are someone’s home. We travel with licensed local teams and treat the places we walk with respect.</li>
        <li><strong>Small groups.</strong> Big enough to share the effort and the laughs, small enough that nobody gets left behind.</li>
      </ul>

      <div class="page-cta">
        <a class="btn btn-primary" href="join.html">Join the community <span aria-hidden="true">&rarr;</span></a>
        <a class="btn btn-outline" href="explore.html">Explore the journeys</a>
      </div>
    </div>''', image='assets/images/ebc-valley.jpg', active=True)


# ═══════════════════════════════ PRIVACY ═════════════════════════════════
page('privacy.html', 'Privacy notice',
     'How The Mountain Diaries collects, uses and protects your personal information.',
     '''
      <h1 class="phead-title">Privacy notice</h1>
      <p class="phead-lede">What we collect, why, and what you can ask us to do with it.</p>''',
     '''
    <div class="prose">
      <p class="updated">Last updated 23 November 2026</p>

      <h2>Who we are</h2>
      <p>The Mountain Diaries is a trekking and expedition community based in the United Arab Emirates. You can reach us at <a href="mailto:hello@themountaindiaries.com">hello@themountaindiaries.com</a>. We handle personal data in line with the UAE’s Federal Decree-Law No. 45 of 2021 on the Protection of Personal Data.</p>

      <h2>What we collect</h2>
      <ul>
        <li><strong>When you join the community:</strong> your name, email address, mobile number, experience level and whether you are interested in local UAE hikes.</li>
        <li><strong>When you register interest in a journey:</strong> your name, email address, phone or WhatsApp number, experience level, the journey and any message you add.</li>
        <li><strong>When you share a story:</strong> the name or trail alias you give, your email address, the trail and your story.</li>
      </ul>
      <p>We do not use analytics, advertising cookies or tracking pixels on this site.</p>

      <h2>How we use it</h2>
      <ul>
        <li>To add you to the community and send you the WhatsApp invite.</li>
        <li>To contact you about hikes, expeditions and journeys you have asked about.</li>
        <li>To review your story and, with your agreement, publish it under the name you gave.</li>
      </ul>

      <h2>Where it is kept</h2>
      <p>Form submissions are sent to a private Google Sheet in our own Google account, through Google Apps Script, and we receive an email notification. Google processes this data for us under its own terms. The site also loads its fonts from Google Fonts, which means Google can see your IP address when a page loads.</p>

      <h2>The WhatsApp community</h2>
      <p>If you join our WhatsApp community, your phone number and profile name are visible to the other members, as they are in any WhatsApp group. WhatsApp’s own privacy policy applies to everything shared there.</p>

      <h2>Who we share it with</h2>
      <p>We never sell your details. We only share them with a licensed guide or trek operator when you book a place on a journey, and only what they need to run it safely, such as your name and emergency contact.</p>

      <h2>How long we keep it</h2>
      <p>We keep your details while you are part of the community, and delete them within 30 days of you asking us to, or after two years without any contact.</p>

      <h2>Your rights</h2>
      <p>You can ask us at any time to show you the data we hold about you, correct it, delete it, or stop contacting you. Email <a href="mailto:hello@themountaindiaries.com">hello@themountaindiaries.com</a> and we will reply within 30 days.</p>

      <h2>Under 18s</h2>
      <p>Our forms are for adults. If you are under 18, please ask a parent or guardian to get in touch with us.</p>

      <h2>Changes</h2>
      <p>If we change how we handle your data, we will update this page and the date at the top.</p>
    </div>''')


# ═══════════════════════════════ TERMS ═══════════════════════════════════
page('terms.html', 'Terms of use',
     'The terms for using The Mountain Diaries website and sharing content with us.',
     '''
      <h1 class="phead-title">Terms of use</h1>
      <p class="phead-lede">The short version: use the site well, look after yourself in the mountains, and only share what is yours.</p>''',
     '''
    <div class="prose">
      <p class="updated">Last updated 23 November 2026</p>

      <h2>About this site</h2>
      <p>This website is run by The Mountain Diaries, a trekking and expedition community based in the United Arab Emirates. By using it you agree to these terms.</p>

      <h2>Information, not advice</h2>
      <p>Everything on this site, including the altitude, training and gear guidance, is general information written in good faith. It is not medical advice and it is not a substitute for a doctor, a qualified guide or your own judgement. Mountain travel carries real risk. Talk to a doctor before any high-altitude journey, and make sure your insurance covers the altitude you are going to and helicopter evacuation.</p>

      <h2>Journeys and bookings</h2>
      <p>Journey pages describe routes we run or plan to run. Registering interest is not a booking and creates no obligation on either side. When a group forms, the dates, price, inclusions, cancellation policy and the operator responsible are set out in writing before you pay anything, and those booking terms apply to that journey.</p>

      <h2>Stories and photos you share</h2>
      <p>When you send us a story or a photograph, you confirm it is yours to share. You keep ownership, and you give us permission to edit it for length and to publish it on this site and our community channels with the name you gave. You can ask us to take it down at any time.</p>

      <h2>Our content</h2>
      <p>The text, design and owner photographs on this site belong to The Mountain Diaries. Third-party photographs are used under their own licences, listed on the <a href="credits.html">photo credits</a> page.</p>

      <h2>Links to other sites</h2>
      <p>We link to news, WhatsApp and other services we do not control, and we are not responsible for their content.</p>

      <h2>Law</h2>
      <p>These terms are governed by the laws of the United Arab Emirates.</p>

      <h2>Contact</h2>
      <p>Questions about these terms: <a href="mailto:hello@themountaindiaries.com">hello@themountaindiaries.com</a>.</p>
    </div>''')


# ═══════════════════════════════ CREDITS ═════════════════════════════════
LICENCE_URL = {
    'CC BY 2.0': 'https://creativecommons.org/licenses/by/2.0/',
    'CC BY 3.0': 'https://creativecommons.org/licenses/by/3.0/',
    'CC BY 4.0': 'https://creativecommons.org/licenses/by/4.0/',
    'CC BY-SA 2.5': 'https://creativecommons.org/licenses/by-sa/2.5/',
    'CC BY-SA 3.0': 'https://creativecommons.org/licenses/by-sa/3.0/',
    'CC BY-SA 4.0': 'https://creativecommons.org/licenses/by-sa/4.0/',
}
manifest = json.load(io.open(os.path.join(HERE, 'photo-manifest.json'), encoding='utf-8'))
wm_rows = []
for m in manifest:
    if not os.path.exists(os.path.join(REPO, 'assets', 'images', m['file'])):
        continue
    src_url = 'https://commons.wikimedia.org/wiki/File:' + m['title'].replace(' ', '_')
    lic = m['license']
    lic_html = ('<a href="%s" target="_blank" rel="noopener">%s</a>' % (LICENCE_URL[lic], lic)
                if lic in LICENCE_URL else lic)
    wm_rows.append('          <tr><td>%s</td><td>%s</td><td>%s</td><td><a href="%s" target="_blank" rel="noopener">Wikimedia Commons</a></td></tr>'
                   % (m['alt'], seo.esc(m['author']), lic_html, src_url.replace('"', '%22')))

# Unsplash credits, lifted from the table in assets/images/CREDITS.md
us_rows = []
credits_md = io.open(os.path.join(REPO, 'assets', 'images', 'CREDITS.md'), encoding='utf-8').read()
for f, who, where, sid, url in re.findall(
        r'^\| `([^`]+)` \| ([^|]+?) \| ([^|]+?) \| \[([^\]]+)\]\((https://unsplash\.com/photos/[^)]+)\) \|$',
        credits_md, re.M):
    us_rows.append('          <tr><td>%s</td><td>%s</td><td><a href="%s" target="_blank" rel="noopener">Unsplash</a></td></tr>'
                   % (where, who, url))

page('credits.html', 'Photo credits',
     'Credits and licences for the photographs used on The Mountain Diaries.',
     '''
      <h1 class="phead-title">Photo credits</h1>
      <p class="phead-lede">The photographers whose work brings these journeys to life.</p>''',
     '''
    <div class="prose">
      <p>Photographs from our own Everest Base Camp trek belong to The Mountain Diaries. Every other photograph is used under the licence shown, with thanks to its photographer. Photographs under Creative Commons licences are shown resized and cropped; the original is on its source page.</p>
      <h2>Wikimedia Commons</h2>
    </div>
    <div class="table-scroll">
      <table class="credits-table">
        <thead><tr><th>Photograph</th><th>Photographer</th><th>Licence</th><th>Source</th></tr></thead>
        <tbody>
%s
        </tbody>
      </table>
    </div>
    <div class="prose">
      <h2>Unsplash</h2>
      <p>Used under the <a href="https://unsplash.com/license" target="_blank" rel="noopener">Unsplash License</a>.</p>
    </div>
    <div class="table-scroll">
      <table class="credits-table">
        <thead><tr><th>Location</th><th>Photographer</th><th>Source</th></tr></thead>
        <tbody>
%s
        </tbody>
      </table>
    </div>''' % ('\n'.join(wm_rows), '\n'.join(us_rows)))

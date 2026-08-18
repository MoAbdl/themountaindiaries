# -*- coding: utf-8 -*-
"""Know the Mountain: the knowledge base.

Generated from index.html's style block plus the shared nav and footer, so the
page cannot drift from the rest of the site. Runs after explore-build.py,
because that is what produces the index this reads.

The copy below is the owner's, verbatim. The only markup added inside it is
emphasis on the "Recognise it / Prevent it / Manage it / Who" labels in the
altitude-illness blocks, which are scanning aids in an emergency and change no
words.
"""
import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT_DIR = os.environ.get('MD_OUT') or REPO
SRC = os.path.join(OUT_DIR, 'index.html')
OUT = os.path.join(OUT_DIR, 'know.html')

src = io.open(SRC, encoding='utf-8').read()
style = re.search(r'<style>(.*?)</style>', src, re.S).group(1)
head_links = re.search(r'(<link rel="icon".*?<script>document\.documentElement.*?</script>)',
                       src, re.S).group(1)
nav = re.search(r'<nav class="site-nav" id="navbar">.*?</nav>', src, re.S).group(0)
footer = re.search(r'<footer class="site-footer">.*?</footer>', src, re.S).group(0)


def cross(block):
    """index-relative anchors become cross-document links on this page."""
    block = re.sub(r'href="#(hero|story|community|explore-teaser|know-teaser)"',
                   r'href="index.html#\1"', block)
    return block.replace(' onclick="switchTab(\'share\')"', '')


nav = cross(nav).replace('<li><a href="know.html">Know the Mountain</a></li>',
                         '<li><a href="know.html" class="is-active" aria-current="page">'
                         'Know the Mountain</a></li>')
footer = cross(footer)

# ═══════════════════════════ CHAPTERS ════════════════════════════════════
# Owner's copy, verbatim. b() marks the label runs inside the illness blocks.
CHAPTERS = [
 ('altitude', 'Altitude &amp; the Body',
  "Why this page exists. Altitude is the one variable on every journey we run that does not "
  "care about your fitness, your experience or your schedule. Understanding it is not optional "
  "knowledge; it is the difference between a hard day and an emergency. Read this before you "
  "commit to anything above 3,000 m.",
  [
   ('What altitude actually does',
    "Above 2,500 m the air holds progressively less oxygen in every breath. At Namche, roughly "
    "three quarters of sea level. At Everest Base Camp, about half. Your body can adapt to "
    "this, remarkably well, but adaptation takes time and happens on its own schedule. Fitness "
    "speeds nothing up. Some of the strongest people acclimatise slowest, and nobody can train "
    "for altitude at sea level."),
   ('Acclimatisation, the honest version',
    "The body needs days, not hours, to build more red blood cells and adjust its breathing "
    "chemistry. Everything in how we pace a route follows from three rules: above 3,000 m, "
    "raise your sleeping altitude gradually, not in leaps. Walk high, sleep low: day climbs "
    "above your bed height teach the body faster than staying put. And build in rest days that "
    "are not really rest: gentle height gain, then back down to sleep. This is why our "
    "itineraries carry “extra” days. They are not padding. They are the plan."),
   ('AMS: Acute Mountain Sickness',
    "<b>Recognise it:</b> headache plus one or more of nausea, poor appetite, dizziness, bad "
    "sleep, unusual fatigue. It usually arrives 6 to 12 hours after reaching a new height. "
    "<b>Prevent it:</b> gradual ascent above all; drink steadily; skip alcohol and sleeping "
    "tablets up high; preventive medication exists and is worth discussing with a "
    "travel-medicine doctor before you fly. <b>Manage it:</b> stop ascending. A rest day at the "
    "same altitude resolves most mild cases. Worsening symptoms mean descending, and descending "
    "works. <b>Who gets it:</b> anyone. Previous trips without trouble guarantee nothing, and "
    "youth and fitness are not protection."),
   ('HACE: when the brain swells',
    "<b>Recognise it:</b> AMS that turns sinister: confusion, clumsiness, a walk like "
    "drunkenness, unusual behaviour, crushing lethargy. The stumble test is the classic sign; "
    "someone who cannot walk heel-to-toe in a straight line is in danger. <b>Prevent it:</b> "
    "treat AMS seriously and never ascend with symptoms. HACE is almost always AMS that was "
    "pushed. <b>Manage it:</b> descend immediately, even at night, even carried. Oxygen and "
    "emergency medication help; descent cures. This is a life-threatening emergency measured in "
    "hours. <b>Who:</b> rare below 4,000 m, and almost always preceded by warnings that were "
    "ignored."),
   ('HAPE: when the lungs fill',
    "<b>Recognise it:</b> breathlessness at rest, not just on the move. A cough, sometimes wet. "
    "Crackling breath, blue lips, a chest that will not catch up. It can arrive without AMS "
    "first, often on night two or three at a new height. <b>Prevent it:</b> the same gradual "
    "ascent, plus honesty about respiratory infections; a chest cold at altitude deserves "
    "caution, not bravado. <b>Manage it:</b> descend, oxygen if available, keep the person warm "
    "and upright. Medication exists; descent remains the treatment that works. Another "
    "hours-not-days emergency. <b>Who:</b> the fast ascender, the person with a cold, the one "
    "who says they are fine."),
   ('The golden rules, all of them',
    "Any illness at altitude is altitude illness until proven otherwise. Never ascend with "
    "symptoms. Never leave someone with symptoms alone. Never descend alone. Tell your guide "
    "everything, early: the person who reports a headache at lunch is easy to help; the one who "
    "hides it until dark is not. Summits are optional. Descent is always an option. And the "
    "daily oximeter checks on our journeys are not theatre: trends matter more than numbers, "
    "and the habit of honesty they build is the real safety equipment."),
  ],
  ["Insurance that covers helicopter evacuation at your journey’s altitudes is mandatory on "
   "everything we run. Why, and what to check in a policy, lives in "
   "<a href=\"#judgement\">Reading the Mountain</a>.",
   "None of this replaces medical advice. Talk to a travel-medicine professional before any "
   "journey above 3,000 m, especially with any heart, lung or blood-pressure history."]),

 ('training', 'Training &amp; Preparation',
  "The honest premise. Nobody fails a trek because they could not run a marathon. People fail "
  "because day four feels like day one, and day seven feels like punishment. Mountain fitness "
  "is the ability to do it again tomorrow.",
  [
   ('What the mountain actually asks',
    "Consecutive days of 5 to 7 hours on your feet with 600 to 1,000 m of climbing, carrying 5 "
    "to 8 kg, at decreasing oxygen. Train for that, specifically. Long back-to-back hill days "
    "beat any single heroic workout. Stairs, hills and loaded walking beat the treadmill. "
    "Strong legs descend safely; most trail injuries happen going down, tired."),
   ('The 8 to 12 week shape',
    "Weeks 1 to 4, build the habit: three walks a week, one long. Weeks 5 to 8, add weight and "
    "back-to-back days: the weekend double is the single most useful session in trekking. Weeks "
    "9 to 12, peak with your longest days, then ease off; arrive rested, not wrecked. Already "
    "active? Convert fitness to specificity: cyclists and runners have the engine but not the "
    "descent legs or the pack shoulders."),
   ('Fit for what, exactly',
    "Steady journeys ask for honest walking fitness and no more. Demanding adds altitude "
    "endurance: the consecutive-days test at full length. Severe means all of that plus "
    "reserve: the capacity to do the hardest day of your life at 3 am and still descend well. "
    "If a journey’s grade and your training diary disagree, believe the diary, and tell us; "
    "downgrading a plan is wisdom, not defeat."),
   ('The part nobody trains',
    "Sleep in unfamiliar places, cold mornings, simple food, shared rooms, no shower. Comfort "
    "resilience is trainable too: camp before you commit, walk in rain on purpose. The mind "
    "quits before the legs more often than the reverse."),
  ], []),

 ('gear', 'Gear, Honestly',
  "The philosophy. Gear does not climb mountains, but bad gear ends journeys. The goal is a "
  "system, not a shopping list: layers that work together, boots that are already friends, and "
  "nothing carried that fear packed.",
  [
   ('The layering system, once and properly',
    "Next to skin, a wicking base, never cotton. Then insulation that fits the day: fleece or "
    "light down, doubled up high. Then the shell, real waterproofing with real venting, because "
    "you will wear it in wind more than rain. Legs follow the same logic lighter. The system’s "
    "skill is changing layers early: before the sweat, before the shiver."),
   ('The three tiers, matching our journeys',
    "<b>Trek kit</b> (every Steady and Demanding journey): broken-in boots, the layer system, a "
    "−10 °C comfort sleeping bag where teahouses run cold, poles, 30 to 40 litre pack, "
    "headlamp, water treatment, sun defence for high-altitude light. <b>Climbing kit</b> (the "
    "6,000ers): everything above plus double boots, crampons, harness, ice axe, jumar and "
    "abseil device, expedition mitts, a bag rated −15 °C or better. We advise renting the "
    "technical layer for first summits; conviction before investment. <b>Expedition kit</b> "
    "(the technical peaks and beyond): the long, specific list that deserves a conversation, "
    "not a webpage; it starts when you talk to us."),
   ('What not to buy',
    "The second warm jacket fear wants. Cotton anything. New boots for an old trek. Gadgets "
    "whose batteries die at −10 °C. The heaviest version of everything: on a porter-supported "
    "journey your limit protects someone else’s back, and that matters more than your spare "
    "options."),
  ], []),

 ('judgement', 'Reading the Mountain',
  "The judgement chapter. Skills and fitness get you to the mountain. Judgement gets you home. "
  "Most of it can be borrowed from good leaders while yours grows, but knowing what they are "
  "weighing makes you a better teammate.",
  [
   ('Weather windows',
    "Mountains have their own schedules. Passes and summits are attempted when the window "
    "opens, not when the itinerary says; that is why real plans carry slack and real leaders "
    "seem patient to the point of boredom. The forecast is a probability, the sky is a fact, "
    "and the mountain will still be there."),
   ('Turnaround discipline',
    "Every summit day has a time after which up is no longer safe, decided in daylight and "
    "honoured in the dark. The mountain decides more than the calendar does; the summit is "
    "optional, the descent is not, and the strongest thing said on any mountain is “not today”."),
   ('Insurance, the unglamorous lifesaver',
    "Standard travel policies stop below where our journeys go. What matters: cover to your "
    "journey’s maximum altitude, helicopter evacuation explicitly included, trekking or "
    "climbing named as covered activities, and for climbs, cover that says so in writing. Carry "
    "proof; in an emergency, the policy number moves faster than sympathy. We check this before "
    "every departure because the day it matters, nothing else does."),
   ('Guides, permits and the system',
    "Most regions we travel require licensed guides and permits by law, and the law is right: "
    "the system funds trails, tracks trekkers and feeds rescue. Where rules are looser, we hold "
    "the same standard anyway. The paperwork is part of the mountain."),
  ], []),

 ('respect', 'Respect',
  "The short chapter that outranks the others. The mountains are somebody’s home, workplace and "
  "temple before they are anybody’s adventure.",
  [
   (None,
    "Walk clockwise around stupas, mani walls and chortens. Ask before photographing people; a "
    "smile and a gesture is a complete sentence. Dress modestly in villages and monasteries. "
    "The porter carrying your bag is a professional at the top of a hard trade: fair loads, "
    "fair treatment and genuine thanks are minimums, not virtues. Pack out what you pack in; "
    "above the treeline, decades pass before litter does. Buy local where you can: the teahouse "
    "dal bhat funds the trail more than any permit. And learn ten words of the local language; "
    "they are worth more than any tip."),
  ], []),
]

CHAPTER_NAV = [('altitude', 'Altitude &amp; the Body'), ('training', 'Training &amp; Preparation'),
               ('gear', 'Gear, Honestly'), ('judgement', 'Reading the Mountain'),
               ('respect', 'Respect'), ('news', 'Mountaineering News')]

NEWS_INTRO = ("News from the mountain world: ascents, expeditions, events, and the losses that "
              "mark this pursuit. Curated, linked to source, updated as the mountains make news.")
NEWS_EMPTY = "First dispatches are on their way. The mountains never stay quiet for long."


def chapter_html(cid, title, lede, blocks, feet):
    out = ['  <section class="kchapter" id="%s">' % cid,
           '    <h2 class="kchapter-title">%s</h2>' % title,
           '    <p class="klede">%s</p>' % lede]
    for heading, body in blocks:
        out.append('    <div class="kblock">')
        if heading:
            out.append('      <h3 class="kblock-title">%s</h3>' % heading)
        out.append('      <p>%s</p>' % body)
        out.append('    </div>')
    for f in feet:
        out.append('    <p class="kfoot">%s</p>' % f)
    out.append('  </section>')
    return '\n'.join(out)


CHAPTERS_HTML = '\n\n'.join(chapter_html(*c) for c in CHAPTERS)
NAV_HTML = '\n'.join(
    '      <a class="chapnav-link" href="#%s">%s</a>' % (cid, t) for cid, t in CHAPTER_NAV)

extra_css = """
  /* ─── KNOW THE MOUNTAIN ───
     Same knowledge register as a journey detail: sienna rule under each
     chapter, a readable measure, and rhythm that stays compact so the page
     scans as reference rather than as an essay. */
  .know-main { padding-top: 0; }
  .khead {
    background: var(--surface-alt);
    border-bottom: 1px solid var(--rule);
    padding: clamp(48px, 7vw, 88px) 0 clamp(36px, 5vw, 60px);
  }
  .khead-inner { max-width: var(--wrap); margin: 0 auto; padding: 0 var(--s-5); }
  .khead-title {
    font-family: var(--font-hero); font-weight: 900;
    font-size: clamp(34px, 5.4vw, 60px); line-height: 1.05;
    letter-spacing: -0.02em; color: var(--ink);
  }
  .khead-lede {
    font-size: clamp(16px, 2vw, 19px); line-height: 1.55;
    color: var(--ink-2); max-width: 56ch; margin-top: var(--s-3);
  }

  /* The chapter nav sticks under the fixed site nav. It scrolls sideways on a
     phone rather than wrapping into a block that buries the first chapter. */
  .chapnav {
    position: sticky; top: var(--nav-h); z-index: 500;
    background: var(--surface);
    border-bottom: 1px solid var(--rule);
  }
  .chapnav-inner {
    max-width: var(--wrap); margin: 0 auto; padding: 0 var(--s-5);
    display: flex; gap: var(--s-5);
    overflow-x: auto; scrollbar-width: none;
  }
  .chapnav-inner::-webkit-scrollbar { display: none; }
  .chapnav-link {
    flex-shrink: 0; white-space: nowrap;
    font-family: var(--font-head); font-size: 13px; font-weight: 600;
    letter-spacing: 0.03em; color: var(--ink-2); text-decoration: none;
    padding: 15px 0; border-bottom: 2px solid var(--sienna-0);
    transition: color 0.15s ease, border-color 0.15s ease;
  }
  .chapnav-link:hover { color: var(--sienna); }
  .chapnav-link.is-active { color: var(--ink); border-bottom-color: var(--sienna); }

  .know-body { max-width: var(--wrap); margin: 0 auto; padding: 0 var(--s-5); }
  .kchapter { padding: clamp(44px, 6vw, 72px) 0; border-top: 1px solid var(--rule); }
  .kchapter:first-of-type { border-top: none; }
  /* scroll-margin so an anchored chapter clears both sticky bars */
  .kchapter, .kchapter[id] { scroll-margin-top: calc(var(--nav-h) + 54px); }
  .kchapter-title {
    font-family: var(--font-head); font-size: clamp(22px, 3vw, 30px); font-weight: 800;
    letter-spacing: -0.01em; color: var(--ink);
    padding-bottom: var(--s-3); margin-bottom: var(--s-4);
    border-bottom: 2px solid var(--sienna); display: inline-block;
  }
  .klede {
    font-size: var(--t-lg); line-height: 1.6; color: var(--ink);
    max-width: 68ch; margin-bottom: var(--s-6);
  }
  .kblock { margin-bottom: var(--s-6); max-width: 72ch; }
  .kblock:last-of-type { margin-bottom: 0; }
  .kblock-title {
    font-family: var(--font-head); font-size: var(--t-base); font-weight: 700;
    letter-spacing: 0.02em; color: var(--ink); margin-bottom: var(--s-2);
  }
  .kblock p { color: var(--ink-2); line-height: 1.7; }
  .kblock b { color: var(--ink); font-weight: 700; }
  .kfoot {
    max-width: 72ch; margin-top: var(--s-5);
    padding-left: var(--s-5); border-left: 2px solid var(--sienna);
    font-size: var(--t-sm); line-height: 1.65; color: var(--ink-2);
  }
  .kfoot a { color: var(--sienna); }

  /* ─── NEWS ─── */
  .news-intro { max-width: 68ch; color: var(--ink-2); line-height: 1.7; margin-bottom: var(--s-6); }
  .news-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: var(--s-5); }
  .news-card {
    display: flex; flex-direction: column;
    background: var(--card); border: 1px solid var(--rule);
    border-radius: var(--radius-lg); overflow: hidden; text-decoration: none;
    transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
  }
  .news-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-card-hover); border-color: var(--rule-firm); }
  .news-media { position: relative; aspect-ratio: 16 / 9; background: var(--placeholder); }
  .news-media img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; display: block; }
  .news-body { display: flex; flex-direction: column; gap: var(--s-2); padding: var(--s-5); }
  .news-meta { display: flex; align-items: center; gap: var(--s-3); flex-wrap: wrap; }
  .news-date { font-family: var(--font-head); font-size: var(--t-xs); color: var(--ink-3); font-variant-numeric: tabular-nums; }
  .news-title { font-family: var(--font-head); font-size: var(--t-lg); font-weight: 700; line-height: 1.3; color: var(--ink); }
  .news-source { font-size: var(--t-sm); color: var(--ink-3); margin-top: auto; padding-top: var(--s-3); }
  .news-empty {
    max-width: 60ch; padding: var(--s-6);
    background: var(--surface-alt); border: 1px solid var(--rule);
    border-radius: var(--radius-lg);
    color: var(--ink-2); line-height: 1.7;
  }

  @media (max-width: 640px) {
    .chapnav-inner { gap: var(--s-4); }
    .chapnav-link { font-size: 12px; padding: 13px 0; }
    .kchapter { padding: var(--s-7) 0; }
  }
"""

page = """<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Know the Mountain &middot; The Mountain Diaries</title>
<meta name="description" content="The knowledge behind every journey: altitude and the body, training, gear, judgement and respect, plus news from the mountain world.">
""" + head_links + """
<style>
""" + style.rstrip('\n') + extra_css + """</style>
</head>
<body>

""" + nav + """

<main class="know-main">

  <section class="khead">
    <div class="khead-inner">
      <h1 class="khead-title">Know the Mountain</h1>
      <p class="khead-lede">The knowledge behind every journey: altitude, preparation, judgement and respect.</p>
    </div>
  </section>

  <nav class="chapnav" aria-label="Chapters">
    <div class="chapnav-inner">
""" + NAV_HTML + """
    </div>
  </nav>

  <div class="know-body">

""" + CHAPTERS_HTML + """

  <section class="kchapter" id="news">
    <h2 class="kchapter-title">Mountaineering News</h2>
    <p class="news-intro">""" + NEWS_INTRO + """</p>
    <div id="news-grid">
      <!-- Static empty state. When NEWS has entries the script below replaces
           this; with JavaScript off, whatever is written here is what shows,
           so this block is kept honest by hand alongside the array. -->
      <p class="news-empty">""" + NEWS_EMPTY + """</p>
    </div>
  </section>

  </div>
</main>

""" + footer + """

<script>
// ═══ MOUNTAINEERING NEWS ═══
//
// TO ADD AN ENTRY
//   1. Download the article's preview image and commit it to assets/news/.
//      NEVER hotlink someone else's image: it breaks when they reorganise,
//      it leans on their bandwidth, and it leaks our readers to their logs.
//      Leave `image` null and the card renders text-only, which is fine.
//   2. Add an object to the TOP of NEWS (newest first):
//        { date: '2026-09-14',            // ISO, sorts and formats from this
//          category: 'Summit',            // Summit | Expedition | Event | In Memoriam
//          title: 'Headline as published',
//          source: 'Publication name',
//          url: 'https://...',            // the original article
//          image: 'assets/news/file.jpg'  // or null
//        }
//   3. Run python3 build/build.py, then python3 build/check.py.
//
// Categories carry a badge except In Memoriam, which stays muted on purpose:
// a death is not a highlight, and colour would make it one.
const NEWS = [
];

const NEWS_BADGE = { 'Summit': 'badge-summit', 'Expedition': 'badge-expedition', 'Event': 'badge-event' };

function newsCard(it) {
  const badge = NEWS_BADGE[it.category]
    ? `<span class="badge ${NEWS_BADGE[it.category]}">${it.category}</span>`
    : `<span class="news-date">${it.category}</span>`;
  const when = new Date(it.date + 'T00:00:00').toLocaleDateString('en-GB',
    { day: 'numeric', month: 'short', year: 'numeric' });
  const media = it.image
    ? `<div class="news-media"><img src="${it.image}" alt="" loading="lazy" decoding="async"></div>`
    : '';
  return `<a class="news-card" href="${it.url}" target="_blank" rel="noopener">
    ${media}
    <div class="news-body">
      <div class="news-meta">${badge}<span class="news-date">${when}</span></div>
      <h3 class="news-title">${it.title}</h3>
      <p class="news-source">${it.source}</p>
    </div>
  </a>`;
}

(function () {
  const grid = document.getElementById('news-grid');
  if (!NEWS.length) return;          // the honest empty state is already in the markup
  grid.className = 'news-grid';
  grid.innerHTML = NEWS.slice().sort((a, b) => b.date.localeCompare(a.date)).map(newsCard).join('');
})();

// ═══ CHAPTER NAV ═══
// Marks the chapter you are reading. Sorted by real position, so the order of
// the links does not have to match the order of the sections.
(function () {
  const links = [...document.querySelectorAll('.chapnav-link')];
  const pairs = links.map(a => ({ a, s: document.getElementById(a.getAttribute('href').slice(1)) }))
                     .filter(p => p.s)
                     .sort((x, y) => x.s.offsetTop - y.s.offsetTop);
  if (!pairs.length) return;
  const sync = () => {
    const line = window.scrollY + document.getElementById('navbar').offsetHeight + 80;
    let on = pairs[0].a;
    for (const p of pairs) if (p.s.offsetTop <= line) on = p.a;
    if (window.innerHeight + window.scrollY >= document.body.scrollHeight - 4) {
      on = pairs[pairs.length - 1].a;
    }
    pairs.forEach(p => p.a.classList.toggle('is-active', p.a === on));
  };
  window.addEventListener('scroll', sync, { passive: true });
  window.addEventListener('resize', sync);
  sync();
})();

""" + re.search(r'// ═══ NAV ═══.*?\n\}\)\(\);\n', src, re.S).group(0) + """
// ═══ ESCAPE ═══
document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeNavMenu(); });
</script>
</body>
</html>
"""

io.open(OUT, 'w', encoding='utf-8').write(page)
print('know.html written: %d chapters, %d bytes' % (len(CHAPTERS) + 1, len(page)))

# -*- coding: utf-8 -*-
"""Detailed journeys. A slug in DETAILS renders the knowledge base template;
everything else stays in the honest catalogue state.

────────────────────────────────────────────────────────────────────────────
The prose in EBC['journey'], ['know'], ['highlights'], ['gear'] and ['faq'] is
the owner's approved copy, wording unchanged, normalised to the STYLE rules
below. The route data, the template and the map do not depend on it, so it can
be revised on its own.
────────────────────────────────────────────────────────────────────────────
"""

# ─── STYLE, applies to all journey copy ──────────────────────────────────
# 1. British spelling. acclimatisation, not acclimatization; metres, not
#    meters; -ise and -isation endings throughout.
# 2. Curly apostrophes and quotes. ’ not ', “ ” not ". The straight forms
#    are for code, never for prose.
# 3. No em dashes anywhere; restructure the sentence instead. En dash only in
#    numeric ranges.
# 4. No AI-marker phrasing; write like a person who has walked the trail.
# Approved copy is otherwise reproduced verbatim: en dashes in ranges and the
# minus sign in temperatures are kept as written.
# ─────────────────────────────────────────────────────────────────────────

# The difficulty scale, coarse on purpose. A journey with no rating yet shows
# no rating rather than a guess.
DIFFICULTY = {'ebc-trek': 'Demanding'}
DIFFICULTY_SCALE = ['Gentle', 'Steady', 'Demanding', 'Severe']

# Stops carry their real coordinates. days = nights slept there on the way up.
EBC_ROUTE = {
    # crop margins as a fraction of the span, per side. The west carries the
    # village labels, so it gets the most.
    'margin': {'w': 0.26, 'e': 0.10, 'n': 0.09, 's': 0.07},
    'stops': [
        {'name': 'Lukla',      'alt': 2860, 'lat': 27.687, 'lon': 86.731, 'label': 'left'},
        {'name': 'Phakding',   'alt': 2610, 'lat': 27.741, 'lon': 86.712, 'label': 'left', 'days': [2]},
        {'name': 'Namche',     'alt': 3440, 'lat': 27.804, 'lon': 86.714, 'label': 'left', 'days': [3, 4]},
        {'name': 'Tengboche',  'alt': 3860, 'lat': 27.836, 'lon': 86.764, 'label': 'left', 'days': [5]},
        {'name': 'Dingboche',  'alt': 4410, 'lat': 27.891, 'lon': 86.831, 'label': 'right', 'days': [6, 7]},
        {'name': 'Lobuche',    'alt': 4940, 'lat': 27.947, 'lon': 86.810, 'label': 'left', 'days': [8]},
        {'name': 'Gorak Shep', 'alt': 5164, 'lat': 27.981, 'lon': 86.828, 'label': 'left',
         'days': [9], 'dy': 14},
        {'name': 'Everest Base Camp', 'short': 'Base Camp', 'alt': 5364,
         'lat': 28.002, 'lon': 86.852, 'label': 'right', 'dy': 50},
        # the Kala Patthar morning is an out and back from Gorak Shep
        {'name': 'Kala Patthar', 'alt': 5545, 'lat': 27.995, 'lon': 86.828, 'label': 'left',
         'spur': True, 'from': 'Gorak Shep', 'viewpoint': True, 'dy': -4},
    ],
    # lx / ly / anchor place each label clear of its neighbours; the three
    # summits at the head of the valley are only a few kilometres apart
    'peaks': [
        {'name': 'Everest',    'alt': 8848, 'lat': 27.988, 'lon': 86.925, 'w': 62, 'h': 46,
         'ly': -78},
        # Lhotse sits hard against the east edge, so its label reads inward
        {'name': 'Lhotse',     'alt': 8516, 'lat': 27.962, 'lon': 86.933, 'w': 52, 'h': 38,
         'lx': -22, 'ly': 40, 'anchor': 'end'},
        {'name': 'Nuptse',     'alt': 7861, 'lat': 27.9669, 'lon': 86.8889, 'w': 48, 'h': 32,
         'lx': -22, 'ly': 22, 'anchor': 'end'},
        # Pumori stands directly above Kala Patthar, which is its south ridge,
        # so the label goes left to keep clear of the viewpoint marker
        {'name': 'Pumori',     'alt': 7161, 'lat': 28.0072, 'lon': 86.8250, 'w': 44, 'h': 30,
         'lx': -24, 'ly': -34, 'anchor': 'end'},
        {'name': 'Ama Dablam', 'alt': 6812, 'lat': 27.862, 'lon': 86.861, 'w': 52, 'h': 38,
         'ly': 26},
    ],
    # altitude slept at each night; touch = a higher point reached that day
    'profile': [
        {'day': 1,  'alt': 1400},
        {'day': 2,  'alt': 2610},
        {'day': 3,  'alt': 3440, 'label': 'Namche'},
        {'day': 4,  'alt': 3440},
        {'day': 5,  'alt': 3860},
        {'day': 6,  'alt': 4410, 'label': 'Dingboche'},
        {'day': 7,  'alt': 4410},
        {'day': 8,  'alt': 4940, 'label': 'Lobuche', 'ldx': -10, 'lanchor': 'end'},
        {'day': 9,  'alt': 5164, 'touch': 5364, 'label': 'Base Camp 5,364',
         'ldx': -6, 'ldy': 4, 'lanchor': 'end'},
        {'day': 10, 'alt': 4240, 'touch': 5545, 'label': 'Kala Patthar 5,545'},
        {'day': 11, 'alt': 3440},
        {'day': 12, 'alt': 2860},
        {'day': 13, 'alt': 1400},
        {'day': 14, 'alt': 1400},
        {'day': 15, 'alt': 1400},
    ],
}

EBC = {
    'duration': '15 days',
    'maxAltitude': 5545,
    'season': 'Mar to May, Oct to Nov',
    'route': EBC_ROUTE,

    # ─── APPROVED COPY, supplied 12 Aug 2026, normalised to the STYLE rules
    #     above. The em dashes were restructured out on 13 Aug at the owner's
    #     direction, wording supplied by them. Minus signs in the temperatures
    #     and en dashes in numeric ranges stand. ───────────────────────────
    'journey':
        "The classic walk to the foot of the world’s highest mountain, up the Dudh Koshi "
        "valley through Sherpa villages, monasteries, and glacial moraine. No ropes, no "
        "technical ground: honest fitness and respect for altitude are the entry requirements.",

    'know': [
        "Two acclimatisation days are non-negotiable. The route walks high and sleeps low.",
        "Nights above Lobuche reach −15 °C in season; days below Namche are often "
        "T-shirt warm.",
        "Train 8–12 weeks. The bar: consecutive 6-hour walking days with a light pack.",
        "No TIMS card here. The Khumbu uses its own municipality permit alongside the "
        "national park permit.",
        "Insurance with helicopter-evacuation cover is mandatory for this region.",
    ],

    'highlights': [
        "Sunrise from Kala Patthar with Everest, Nuptse and the Icefall in one frame",
        "Namche Bazaar, the Sherpa capital built into a mountainside amphitheatre",
        "An evening puja at Tengboche Monastery beneath Ama Dablam",
        "The memorial chortens at Thukla Pass, the trail’s quietest moment",
        "First sight of Everest from the ridge above Namche",
    ],

    'gear':
        "A layered cold-weather system rated to −15 °C, broken-in boots, a 30–40L "
        "daypack, a sleeping bag with −10 °C comfort rating, trekking poles, and water "
        "treatment. Full gear guidance and altitude know-how live in Know the Mountain.",

    'faq': [
        ["Do I need climbing experience?",
         "None. It’s a trek: no ropes, no technical ground."],
        ["How fit is fit enough?",
         "Comfortable walking 6 hours on consecutive days. Start training 8–12 weeks out."],
        ["What about altitude sickness?",
         "We pace to prevent it and stay honest about symptoms. Descending is always the "
         "right call."],
        ["Can I join alone?",
         "Most of the group does. That’s the point of a community expedition."],
    ],
    # ─── end of approved copy ─────────────────────────────────────────────
}

# ═══ BATCH 1, supplied 15 Aug 2026 ═══════════════════════════════════════
# Owner's copy, verbatim. regionLabel overrides the fact strip where the
# owner names the range rather than the rail's tab bucket: the Trekking rail
# files these under Everest, the copy calls it the Khumbu, and the copy wins
# on the page.

THREE_PASSES = {
    'duration': '18 days',
    'maxAltitude': 5535,
    'season': 'Mar–May & Oct–Nov',
    'regionLabel': 'Khumbu, Nepal',
    'journey':
        "The complete Khumbu. One long horseshoe over the region’s three great passes, "
        "Kongma La, Cho La and Renjo La, linking Base Camp, the Gokyo lakes and valleys "
        "most EBC trekkers never see.",
    'know': [
        "Three passes above 5,300 m in one route; this is the Khumbu’s toughest standard trek.",
        "Fitness for EBC is the entry point, not the finish line. Expect longer days and "
        "rougher ground.",
        "The Cho La crossing involves a small glacier section; microspikes earn their weight.",
        "Route runs clockwise or anticlockwise; clockwise (Kongma La first) acclimatises "
        "harder but earlier.",
        "Same permits as EBC: national park plus municipality, no TIMS.",
    ],
    'highlights': [
        "Sunrise on Gokyo Ri over the Ngozumpa glacier, Nepal’s longest",
        "Kongma La, the highest and quietest of the three",
        "Everest, Lhotse, Makalu and Cho Oyu in a single Renjo La frame",
        "Base Camp and Kala Patthar, earned the long way",
        "The turquoise Gokyo lakes at 4,700 m",
    ],
    'gear':
        "EBC list plus microspikes, gaiters and a sleeping bag rated to −15 °C comfort. "
        "Full guidance in Know the Mountain.",
    'faq': [
        ["Is it harder than EBC?", "Substantially. Longer, higher, lonelier."],
        ["What experience do I need?", "Strong trekking fitness; no climbing skills."],
        ["Which direction is better?",
         "Clockwise for solitude, anticlockwise for gentler acclimatisation."],
        ["Can I join alone?", "Most of the group comes alone."],
    ],
}

GOKYO = {
    'duration': '12 days',
    'maxAltitude': 5357,
    'season': 'Mar–May & Oct–Nov',
    'regionLabel': 'Khumbu, Nepal',
    'journey':
        "The Khumbu’s quieter masterpiece. Up the valley west of Everest to a chain of "
        "turquoise glacial lakes and a summit viewpoint many rate above Kala Patthar.",
    'know': [
        "Quieter trails than the EBC route once past Namche; teahouses thinner on the ground.",
        "Gokyo Ri at dawn is a hard 2-hour climb; the reward is four 8,000 m peaks in one view.",
        "The lakes sit between 4,700 and 5,000 m; acclimatisation days are built in, not optional.",
        "Winter visits are possible but the lakes freeze and lodges thin out.",
        "Permits as for all Khumbu treks: national park plus municipality.",
    ],
    'highlights': [
        "The third lake at Gokyo village, impossibly turquoise",
        "Everest, Lhotse, Makalu and Cho Oyu from Gokyo Ri",
        "Walking beside the Ngozumpa glacier’s grey moraine sea",
        "Machhermo’s quiet stone-walled yak pastures",
        "A valley that still feels like the Khumbu of thirty years ago",
    ],
    'gear':
        "Standard cold-season Khumbu kit; the EBC list covers it. Details in Know the Mountain.",
    'faq': [
        ["Gokyo or EBC first?",
         "Gokyo for views and quiet, EBC for the name. Many return for the other."],
        ["What is the fitness bar?", "Six-hour days with one steep dawn climb."],
        ["Can it extend to EBC?",
         "Yes, over the Cho La; that becomes the Three Passes’ middle third."],
        ["Joining solo?", "Standard here."],
    ],
}

ANNAPURNA_CIRCUIT = {
    'duration': '13 days',
    'maxAltitude': 5416,
    'season': 'Mar–May & Oct–Nov',
    'journey':
        "Nepal’s great crossing. From subtropical river valleys through Manang’s high desert "
        "to the prayer flags of Thorong La, then down into the ancient pilgrimage country of "
        "Mustang.",
    'know': [
        "The route crosses from lush gorge to Tibetan-plateau landscape in a week; pack for "
        "every climate.",
        "Thorong La day starts around 4 am and climbs 900 m; it is the trek’s single serious test.",
        "Acclimatisation day in Manang (3,540 m) is non-negotiable.",
        "One permit is checked on the ground: the ACAP. Ignore outdated TIMS advice.",
        "Nepal requires a licensed guide for foreign trekkers in this region.",
    ],
    'highlights': [
        "Thorong La at 5,416 m, prayer flags against a huge sky",
        "The Manang valley, high desert beneath Annapurna III",
        "Muktinath, sacred to Hindus and Buddhists both",
        "Apple orchards and stone villages of lower Mustang",
        "Annapurna II catching first light from Upper Pisang",
    ],
    'gear':
        "Four-season layering in one pack: warm-weather kit low, full cold-weather system for "
        "the pass. Guidance in Know the Mountain.",
    'faq': [
        ["How hard is the pass day?",
         "Eight to ten hours, pre-dawn start, honest cold. The rest of the route is gentler."],
        ["Are there roads on the route?",
         "Partly; our staging keeps to trail wherever it exists."],
        ["Best month?", "October for clarity, April for warmth."],
        ["Solo joiners?", "Most of the group."],
    ],
}

ABC = {
    'duration': '9 days',
    'maxAltitude': 4130,
    'season': 'Mar–May & Oct–Nov',
    'journey':
        "A walk into an amphitheatre. Stone staircases through rhododendron forest and Gurung "
        "villages, ending inside a ring of 7,000 and 8,000 m walls.",
    'know': [
        "Lower maximum altitude than the big treks, but the stone-step climbs are relentless; "
        "knees notice.",
        "The Sanctuary sits in avalanche country; season and recent snowfall shape the final "
        "approach.",
        "Spring paints the middle hills red with rhododendron.",
        "ACAP permit, checked at multiple points; licensed guide required.",
        "Cold at Base Camp surprises people: nights below −5 °C even in season.",
    ],
    'highlights': [
        "Dawn inside the Sanctuary, ringed by Annapurna I and Machhapuchhre",
        "The fishtail summit of Machhapuchhre, never climbed and never permitted",
        "Chhomrong’s endless stone staircase, the trek’s honest toll",
        "Gurung hospitality in Ghandruk",
        "Hot springs at Jhinu Danda on the walk out",
    ],
    'gear':
        "Three-season kit with one genuine cold-weather layer for Sanctuary nights. Details in "
        "Know the Mountain.",
    'faq': [
        ["Good first Himalayan trek?", "One of the best."],
        ["Fitness bar?", "Five to six hour days with big staircases."],
        ["Combine with Mardi Himal?", "Yes, they share a trailhead region."],
        ["Altitude risk?",
         "Lower than the big treks, but the last day still climbs fast; we pace it."],
    ],
}

MARDI = {
    'duration': '6 days',
    'maxAltitude': 4500,
    'season': 'Mar–May & Oct–Nov',
    'journey':
        "The short, sharp ridge walk. A forest trail out of Pokhara climbing a single spur to "
        "eye-level views of Machhapuchhre, all in under a week.",
    'know': [
        "The whole route rides one ridgeline; weather moves fast and views come and go in minutes.",
        "Short does not mean soft: High Camp days climb steeply on rough trail.",
        "Lodges are simpler and smaller than the classic routes; book-ahead thinking applies in "
        "peak weeks.",
        "ACAP permit; licensed guide required.",
        "Ideal acclimatisation before a bigger objective, or a complete trek in its own right.",
    ],
    'highlights': [
        "Machhapuchhre close enough to read the snow flutings",
        "Sunrise from the upper viewpoint over the whole Annapurna wall",
        "Cloud-forest trail hung with moss and rhododendron",
        "Pokhara to trailhead in an hour; no internal flights",
        "The Himalaya’s best effort-to-view ratio",
    ],
    'gear':
        "Light three-season kit with one warm layer for viewpoint dawns. Details in Know the "
        "Mountain.",
    'faq': [
        ["Total beginner friendly?", "Yes, with honest walking fitness."],
        ["How cold?", "Viewpoint dawns around −5 °C in season."],
        ["Crowded?", "Busier than it was, still far quieter than ABC."],
        ["Extendable?", "Pairs naturally with ABC for a two-week Annapurna immersion."],
    ],
}

# ═══ BATCH 2, supplied 17 Aug 2026 ═══════════════════════════════════════
# Owner's copy, verbatim. Four of the five are restricted or border regions,
# which is why the permit lines are specific.

UPPER_MUSTANG = {
    'duration': '12 days',
    'maxAltitude': 3810,
    'season': 'Mar–Nov, including monsoon',
    'regionLabel': 'Mustang, Nepal',
    'journey':
        "A walk into a former kingdom. Behind the Annapurna–Dhaulagiri wall lies a high desert "
        "of cave monasteries, wind-carved cliffs and the walled city of Lo Manthang, closed to "
        "outsiders until 1992.",
    'know': [
        "This is a restricted region. The permit is issued per day inside the zone and only "
        "through a registered agency, with a licensed guide.",
        "The rules changed in 2026: solo travellers can now obtain the permit, and pricing "
        "follows your actual days inside.",
        "Mustang sits in the rain shadow, so the monsoon months work here when the rest of "
        "Nepal is soaked.",
        "Altitude stays moderate but the wind is a daily character; afternoons blow hard and cold.",
        "Culture is the point: monasteries, festivals and villages ask for slower walking and "
        "open eyes.",
    ],
    'highlights': [
        "First sight of Lo Manthang’s whitewashed wall across the desert",
        "Cave monasteries painted eight centuries ago",
        "The Kali Gandaki gorge, deepest on Earth by some counts",
        "Tiji Festival in spring, three days of masked ritual",
        "A landscape closer to Tibet than to the Nepal of postcards",
    ],
    'gear':
        "Three-season kit with serious wind protection and sun defence; this is desert trekking "
        "at altitude. Details in Know the Mountain.",
    'faq': [
        ["Why is it restricted?",
         "Border sensitivity and cultural preservation; the permit system keeps numbers low."],
        ["How hard is the walking?", "Moderate days; wind and dryness are the real tests."],
        ["Best time?", "May for Tiji, or the monsoon window when everywhere else drips."],
        ["Solo joiners?",
         "Now possible under the 2026 rules; most of our group comes alone anyway."],
    ],
}

MANASLU_CIRCUIT = {
    'duration': '14 days',
    'maxAltitude': 5106,
    'season': 'Mar–May & Oct–Nov',
    'regionLabel': 'Gorkha, Nepal',
    'journey':
        "The connoisseur’s circuit. Around the world’s eighth-highest mountain through a valley "
        "that opened to outsiders only in 1991, ending over the snows of the Larkya La.",
    'know': [
        "Restricted region: permit through a registered agency, licensed guide mandatory, "
        "priced per week inside the zone.",
        "The Larkya La day starts around 4 am and can carry snow and fixed-line sections late "
        "season.",
        "Villages here are culturally Tibetan; the trail doubles as a pilgrimage route.",
        "Teahouses are simpler than Annapurna’s; expect basic and honest.",
        "Three permits stack here: the restricted-area permit plus both conservation areas the "
        "route crosses.",
    ],
    'highlights': [
        "Manaslu’s double summit from Lho at first light",
        "The Larkya La at 5,106 m, the circuit’s earned crown",
        "Mani walls and monasteries of the Nubri valley",
        "Birendra glacial lake below Samagaon",
        "A circuit with a fraction of Annapurna’s foot traffic",
    ],
    'gear':
        "Full cold-weather system for the pass; microspikes late season. Guidance in Know the "
        "Mountain.",
    'faq': [
        ["Manaslu or Annapurna Circuit?",
         "Manaslu for quiet and Tibetan culture, Annapurna for variety and comfort."],
        ["How hard is the pass?", "Comparable to Thorong La with rougher ground."],
        ["Why the permits?", "The region borders Tibet and stayed closed until 1991."],
        ["Solo joiners?", "Permitted since 2026, guide required; our groups make it moot."],
    ],
}

MANASLU_BC = {
    'duration': '10 days',
    'maxAltitude': 4750,
    'season': 'Mar–May & Oct–Nov',
    'regionLabel': 'Gorkha, Nepal',
    'journey':
        "Up the Budhi Gandaki to Samagaon, then the steep pull to the base camp of the "
        "eighth-highest mountain, with the Nubri valley’s monasteries as the slow reward on the "
        "way.",
    'know': [
        "Same restricted-region rules as the circuit: agency permit, licensed guide, per-week "
        "pricing.",
        "Base Camp day climbs over 1,200 m from Samagaon and returns the same way; it is the "
        "trek’s whole test in one morning.",
        "The route shares the circuit’s approach without crossing the Larkya La, so it suits "
        "tighter timelines.",
        "Expect basic teahouses and genuine remoteness; rescue here is slower than the famous "
        "valleys.",
        "Autumn brings expedition season; Base Camp becomes a working village of tents.",
    ],
    'highlights': [
        "Manaslu filling the sky above Birendra lake",
        "Pungyen Gompa, a monastery under the mountain’s east face",
        "Expedition base camp in season, prayer flags over glacier ice",
        "The Budhi Gandaki gorge, days of river-cut drama",
        "Sama Gaun’s stone lanes and yak trains",
    ],
    'gear':
        "Cold-weather kit for the Base Camp push; the rest is standard three-season. Details in "
        "Know the Mountain.",
    'faq': [
        ["Circuit or Base Camp?",
         "The circuit for the full crossing, Base Camp for depth over distance."],
        ["Fitness bar?", "One very big day; the rest are honest trekking days."],
        ["Can I see climbers?", "In season, yes; Base Camp hums in September and April."],
        ["Solo joiners?", "Same 2026 rules as the circuit."],
    ],
}

LANGTANG = {
    'duration': '8 days',
    # The headline number is the standard walk's high point, Kyanjin Gompa.
    # Tserko Ri at 4,984 m is an optional dawn climb, described in Know and in
    # the FAQ; putting it in the fact strip overstated the trek people book.
    'maxAltitude': 3870,
    'highPoint': 'Kyanjin Gompa',
    'season': 'Mar–May & Oct–Nov',
    'regionLabel': 'Langtang, Nepal',
    'journey':
        "The valley of glaciers, one long day’s drive from Kathmandu. Through forest and yak "
        "pasture to Kyanjin Gompa, ringed by 7,000 m ice, in the region that rebuilt itself "
        "after 2015.",
    'know': [
        "Closest major trek to Kathmandu: no internal flights, one rough scenic drive.",
        "The 2015 earthquake destroyed Langtang village; walking here supports a community that "
        "rebuilt from nothing.",
        "Kyanjin Ri and Tserko Ri are optional dawn climbs; the valley walk itself stays gentler.",
        "National park permit required; licensed guide required.",
        "Cheese from the Kyanjin dairy is a genuine trail institution.",
    ],
    'highlights': [
        "Langtang Lirung’s icefall hanging over the valley",
        "Sunrise from Kyanjin Ri, glaciers on three sides",
        "The rebuilt Langtang village and its memorial",
        "Forest trails alive with langur monkeys",
        "Kyanjin Gompa’s dairy, cheese at 3,870 m",
    ],
    'gear':
        "Standard three-season kit with one warm layer for the optional dawn climbs. Details in "
        "Know the Mountain.",
    'faq': [
        ["Good first trek?", "Yes, among Nepal’s best introductions."],
        ["How hard are the optional peaks?",
         "Tserko Ri is a genuine 5 am, 1,100 m effort; entirely skippable."],
        ["Why Langtang over Annapurna?",
         "Proximity, quiet, and the story of a valley that came back."],
        ["Solo joiners?", "Most of the group."],
    ],
}

LADAKH = {
    'duration': '8 days',
    'maxAltitude': 5260,
    'season': 'Jun–Sep',
    'regionLabel': 'Ladakh, India',
    'journey':
        "The Markha valley crossing in India’s high-altitude desert: Buddhist villages, canyon "
        "trails and a finale over the Kongmaru La with Kang Yatse filling the horizon.",
    'know': [
        "Ladakh runs on the opposite calendar: June to September, when the monsoon drowns Nepal, "
        "is the season here.",
        "Leh sits at 3,500 m; two acclimatisation days there before walking are part of the "
        "plan, not a luxury.",
        "Nights in village homestays replace teahouses; simpler, warmer, more personal.",
        "River crossings punctuate the route in early summer; sandals earn a place in the pack.",
        "Indian visa required; the trek itself crosses a national park with its own fees.",
    ],
    'highlights': [
        "Kongmaru La at 5,260 m, prayer flags over a desert of peaks",
        "Kang Yatse’s 6,400 m pyramid shadowing the upper valley",
        "Homestay evenings in Markha and Hankar",
        "Ancient forts and gompas rising from canyon walls",
        "The moonscape light Ladakh is famous for",
    ],
    'gear':
        "Three-season kit with strong sun protection and cold-morning layers; desert nights "
        "bite. Details in Know the Mountain.",
    'faq': [
        ["Why Ladakh?",
         "A different Himalaya: drier, older-feeling, Buddhist to its bones, and in season when "
         "Nepal is not."],
        ["Fitness bar?",
         "Six-hour days with one big pass; altitude arrives on day one at Leh."],
        ["Homestays really?",
         "Yes, family homes with mattresses and dal; part of the point."],
        ["Solo joiners?", "Most of the group."],
    ],
}

# ═══ BATCH 3, supplied 18 Aug 2026 ═══════════════════════════════════════
# Owner's copy, verbatim. Two carry approximate high points: altApprox renders
# them with a tilde in both the card and the fact strip, because a bare number
# reads as surveyed. regionLabel spans countries for the Alpine pair while the
# tab buckets stay The Alps and South America.

TMB = {
    'duration': '11 days',
    'maxAltitude': 2537,
    'highPoint': 'Grand Col Ferret',
    'season': 'Jun–Sep',
    'regionLabel': 'France, Italy, Switzerland',
    'journey':
        "The Alps’ great circle. Around the Mont Blanc massif through three countries, "
        "sleeping in mountain huts and valley villages, with the white summit turning above "
        "you the whole way round.",
    'know': [
        "Altitude is modest; distance is not. Expect 10 to 15 km days with honest climbs, day "
        "after day.",
        "Huts book out months ahead in July and August; committing early is the whole game.",
        "No permits, no guides required by law; navigation is straightforward on Europe’s "
        "best-marked trail.",
        "Weather swings alpine-fast: snow on the cols is possible any month.",
        "Hut etiquette is its own culture: sheet liners, early lights-out, communal dinners.",
    ],
    'highlights': [
        "Crossing the Grand Col Ferret from Italy into Switzerland",
        "The Aiguilles above Chamonix at last light",
        "Refuge nights, dormitories full of a dozen languages",
        "Courmayeur’s Italian side, all granite and prosciutto",
        "The massif itself, never out of sight for a week",
    ],
    'gear':
        "Light and fast: three-season layers, real rain shells, broken-in boots. No sleeping "
        "bag needed, huts provide blankets. Details in Know the Mountain.",
    'faq': [
        ["Which direction?",
         "Anticlockwise is classic; the crowds agree, which is its one flaw."],
        ["Camping possible?", "Partly; hut-based is simpler and warmer."],
        ["Fitness bar?", "Consecutive full days with 800 to 1,000 m of climb."],
        ["Solo joiners?", "Most of the group."],
    ],
}

HAUTE_ROUTE = {
    'duration': '13 days',
    'maxAltitude': 2987,
    'highPoint': 'Col de Prafleuri',
    'season': 'Jul–Sep',
    'regionLabel': 'France, Switzerland',
    'journey':
        "Chamonix to Zermatt the walker’s way: a high traverse under the Alps’ greatest "
        "collection of 4,000 m peaks, from Mont Blanc’s shadow to the Matterhorn’s doorstep.",
    'know': [
        "Harder than the TMB: higher cols, rougher ground, longer days between comforts.",
        "The season is short; before July snow blocks the passes, after mid-September huts "
        "close.",
        "Some stages carry ladders and fixed chains; a head for exposure helps.",
        "Route flexes daily with weather; good judgement matters more than pace here.",
        "Swiss hut prices sting; budget honestly.",
    ],
    'highlights': [
        "First full sight of the Matterhorn on the walk into Zermatt",
        "The Grand Combin filling the sky for three days",
        "Cabane de Prafleuri and the wild country around it",
        "Turquoise reservoirs and glacier snouts of the Val de Bagnes",
        "Europaweg’s balcony finish, a corridor of ice giants",
    ],
    'gear':
        "TMB kit plus warmer layers and gloves for the high cols; poles near-essential on the "
        "moraine. Details in Know the Mountain.",
    'faq': [
        ["TMB or Haute Route?",
         "TMB to fall in love with the Alps, Haute Route to be tested by them."],
        ["Glacier travel?", "The walker’s route avoids it; no rope needed."],
        ["Fitness bar?", "Big consecutive days at TMB-plus intensity."],
        ["Solo joiners?", "Most of the group."],
    ],
}

TORRES = {
    'duration': '6 days',
    'maxAltitude': 900,
    'altApprox': True,
    'highPoint': 'Base Torres viewpoint',
    'season': 'Oct–Apr',
    'regionLabel': 'Patagonia, Chile',
    'journey':
        "Patagonia’s W: three valleys stitched along the Paine massif’s southern face, granite "
        "towers at one end, the blue chaos of Grey Glacier at the other.",
    'know': [
        "The seasons flip: October to April is the window, southern summer at its wildest.",
        "Altitude is trivial; wind is the mountain here. Gusts past 100 km/h are normal, not "
        "news.",
        "Every campsite and refugio requires advance reservation; the park turns away walkers "
        "without them.",
        "Weather delivers four seasons daily; the towers hide and reveal on their own schedule.",
        "The full O Circuit extends the W into an 8-day loop for those with the days.",
    ],
    'highlights': [
        "The three towers firing red at dawn from Base Torres",
        "Grey Glacier calving into its iceberg-strewn lake",
        "The Valle Francés amphitheatre in full roar",
        "Guanacos and condors against impossible skies",
        "Patagonian light, worth the airfare alone",
    ],
    'gear':
        "Bombproof wind and rain shells over three-season layers; sun protection for the "
        "ozone-thin south. Details in Know the Mountain.",
    'faq': [
        ["How windy really?", "Enough to stagger you on passes; poles stop being optional."],
        ["W or O?", "W for the essentials in six days, O for solitude and the Gardner pass."],
        ["Fitness bar?", "Long distance days, 15 to 20 km, on good trail."],
        ["Solo joiners?", "Most of the group."],
    ],
}

HUAYHUASH = {
    'duration': '11 days',
    'maxAltitude': 5000,
    'altApprox': True,
    'highPoint': 'Punta Cuyoc',
    'season': 'May–Sep',
    'regionLabel': 'Cordillera Huayhuash, Peru',
    'journey':
        "The Andes’ hardest classic. A full circle of a compact, savage range: eight passes "
        "above 4,600 m, turquoise lakes under 6,000 m faces, and the mountains of Touching the "
        "Void.",
    'know': [
        "This is a camping expedition, not a teahouse trek; nights under canvas at 4,000 m plus "
        "for over a week.",
        "Eight high passes in eleven days; there are no easy days, only shorter hard ones.",
        "Communities along the route charge local fees per section; cash and patience both "
        "required.",
        "Remoteness is real: the nearest road is often days away, and rescue is slow.",
        "The dry season is austral winter: brilliant days, nights well below freezing.",
    ],
    'highlights': [
        "Siula Grande’s west face, the wall from Touching the Void",
        "The lake terrace at Carhuacocha, three giants mirrored at dawn",
        "Punta Cuyoc, the circuit’s 5,000 m high point",
        "Hot springs at Viconga, absurd and glorious mid-circuit",
        "A range you circle entirely in eleven days",
    ],
    'gear':
        "Full expedition camping kit: four-season bag, insulated mat, down layers, "
        "altitude-ready everything. Details in Know the Mountain.",
    'faq': [
        ["Hardest thing about it?",
         "The accumulation: pass after pass with no recovery valley."],
        ["Prior experience?", "At least one high-altitude trek; this is a poor first."],
        ["Why not the shorter mini-circuit?",
         "It exists and it’s good; the full circle is the masterpiece."],
        ["Solo joiners?", "Most of the group."],
    ],
}

KILIMANJARO = {
    'duration': '7 days',
    'maxAltitude': 5895,
    'highPoint': 'Uhuru Peak',
    'season': 'Jan–Mar & Jun–Oct',
    'regionLabel': 'Tanzania',
    'journey':
        "The roof of Africa on foot. Through five climate zones from rainforest to arctic "
        "summit ice, ending in the dark hours on the crater rim as the sun rises over the "
        "continent.",
    'know': [
        "No technical climbing, but 5,895 m is serious altitude on a fast schedule; summit "
        "night is the hardest walking most people ever do.",
        "Park rules require a licensed operator with registered guides and crew; independent "
        "climbing is prohibited.",
        "Route choice shapes success: longer itineraries acclimatise better and summit more "
        "often.",
        "Summit night starts near midnight: 6 to 8 hours up in deep cold, then a very long "
        "descent.",
        "Respect for the crew culture matters; porters carry this mountain’s economy.",
    ],
    'highlights': [
        "Sunrise from Uhuru Peak, the ice fields glowing pink",
        "Walking from rainforest to glacier in five days",
        "The Barranco Wall, a scramble that looks worse than it is",
        "Camps above the cloud sea, Mount Meru floating on it",
        "Standing on the highest freestanding mountain on Earth",
    ],
    'gear':
        "Full cold-weather summit kit over trekking layers: expedition gloves, insulated "
        "boots, headlamp with spare batteries. Details in Know the Mountain.",
    'faq': [
        ["Success rate honestly?",
         "Route and pacing dependent; longer routes summit far more often."],
        ["Coldest moment?", "Summit night, −10 to −20 °C with wind."],
        ["Do I need climbing skills?", "None; you need lungs, legs and stubbornness."],
        ["Solo joiners?", "Most of the group."],
    ],
}

DETAILS = {
    'ebc-trek': EBC,
    'three-passes': THREE_PASSES,
    'gokyo-lakes': GOKYO,
    'annapurna-circuit': ANNAPURNA_CIRCUIT,
    'annapurna-base-camp': ABC,
    'mardi-himal': MARDI,
    'upper-mustang': UPPER_MUSTANG,
    'manaslu-circuit': MANASLU_CIRCUIT,
    'manaslu-base-camp': MANASLU_BC,
    'langtang-valley': LANGTANG,
    'ladakh-high-passes': LADAKH,
    'tour-du-mont-blanc': TMB,
    'haute-route-trek': HAUTE_ROUTE,
    'torres-del-paine-trek': TORRES,
    'huayhuash-circuit': HUAYHUASH,
    'kilimanjaro-5895': KILIMANJARO,
}

DIFFICULTY.update({
    # batch 1
    'three-passes': 'Severe',
    'gokyo-lakes': 'Demanding',
    'annapurna-circuit': 'Demanding',
    'annapurna-base-camp': 'Steady',
    'mardi-himal': 'Steady',
    # batch 2
    'upper-mustang': 'Steady',
    'manaslu-circuit': 'Demanding',
    'manaslu-base-camp': 'Demanding',
    'langtang-valley': 'Steady',
    'ladakh-high-passes': 'Demanding',
    # batch 3
    'tour-du-mont-blanc': 'Steady',
    'haute-route-trek': 'Demanding',
    'torres-del-paine-trek': 'Steady',
    'huayhuash-circuit': 'Severe',
    'kilimanjaro-5895': 'Severe',
})

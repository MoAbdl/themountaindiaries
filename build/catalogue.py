# -*- coding: utf-8 -*-
"""OVERVIEW: the mountain itself, for journeys without a full detail entry.

The 8000ers and 7000ers are on the list because people ask about them, not
because a group is scheduled. Until a journey earns full route notes in
details.py, its page carries the facts about the mountain: its character,
the normal route, the season, how long an expedition typically takes and who
climbed it first. Nothing here describes an itinerary we run, so nothing here
promises one.

Follows the STYLE rules in details.py: British spelling, curly apostrophes,
no em dashes.

  about    two or three sentences on the mountain
  route    the normal route as it is climbed today
  season   the main climbing season
  length   typical expedition length, base camp approach included
  first    the first ascent
"""

OVERVIEW = {
    # ── 8000ers ───────────────────────────────────────────────────────
    'everest-8848': {
        'about': "The highest point on Earth, on the border of Nepal and Tibet. From Nepal the climb "
                 "starts at Base Camp on the Khumbu Glacier and runs through the Khumbu Icefall, the "
                 "Western Cwm and the Lhotse Face to the South Col. It asks for 8,000 metre "
                 "experience, weeks of acclimatisation rotations and a summit push measured in hours.",
        'route': 'South Col and Southeast Ridge, from Nepal',
        'season': 'April to May',
        'length': 'About 60 days',
        'first': '1953, Edmund Hillary and Tenzing Norgay',
    },
    'k2-8611': {
        'about': "The second highest mountain in the world, standing alone at the head of the Baltoro "
                 "Glacier in Pakistan’s Karakoram. Steeper, colder and more serious than Everest at "
                 "every stage, with the Bottleneck couloir below the summit the crux of the normal "
                 "route. The trek in past Concordia is one of the great walks on Earth.",
        'route': 'Abruzzi Spur',
        'season': 'June to August',
        'length': 'About 55 to 60 days',
        'first': '1954, Lino Lacedelli and Achille Compagnoni',
    },
    'kangchenjunga-8586': {
        'about': "The third highest mountain, on Nepal’s far eastern border with Sikkim. Remote, "
                 "enormous and climbed far less than its neighbours to the west. The long walk in "
                 "through untouched villages is part of the appeal; the upper mountain is long, "
                 "exposed and committing.",
        'route': 'Southwest Face, from the Yalung Glacier',
        'season': 'April to May',
        'length': 'About 55 days',
        'first': '1955, George Band and Joe Brown',
    },
    'lhotse-8516': {
        'about': "Everest’s neighbour, joined to it by the South Col. The normal route shares the "
                 "Everest climb as far as the Lhotse Face, then breaks away up a steep, narrow couloir "
                 "to the summit. A real 8,000 metre summit with a shorter summit day than Everest.",
        'route': 'West Face, via the Lhotse Couloir',
        'season': 'April to May',
        'length': 'About 50 to 55 days',
        'first': '1956, Fritz Luchsinger and Ernst Reiss',
    },
    'makalu-8485': {
        'about': "The fifth highest mountain, a granite pyramid south-east of Everest. Its four sharp "
                 "ridges make it one of the most striking peaks in the Himalaya and one of the harder "
                 "8,000 metre summits, with technical climbing on the final pyramid.",
        'route': 'Northwest Ridge, via the Makalu La',
        'season': 'April to May',
        'length': 'About 55 days',
        'first': '1955, Lionel Terray and Jean Couzy',
    },
    'cho-oyu-8188': {
        'about': "The sixth highest mountain, on the Nepal and Tibet border west of Everest. Broad, "
                 "comparatively gentle slopes have made it the classic first 8,000 metre peak, "
                 "though nothing at this height is ever easy.",
        'route': 'Northwest Ridge, from Tibet',
        'season': 'September to October',
        'length': 'About 40 days',
        'first': '1954, Herbert Tichy, Sepp Jöchler and Pasang Dawa Lama',
    },
    'dhaulagiri-8167': {
        'about': "The seventh highest mountain, rising almost seven kilometres above the Kali Gandaki "
                 "gorge, the deepest valley on Earth. A serious climb with real avalanche exposure, "
                 "and a long, remote approach around the massif.",
        'route': 'Northeast Ridge',
        'season': 'September to October, or April to May',
        'length': 'About 45 days',
        'first': '1960, Swiss and Austrian expedition including Kurt Diemberger',
    },
    'manaslu-8163': {
        'about': "The eighth highest mountain, in the Gorkha region of central Nepal. Now one of the "
                 "most popular 8,000 metre peaks and often climbed as preparation for Everest. "
                 "Reaching the true summit means crossing a short, exposed ridge beyond the "
                 "foresummit.",
        'route': 'Northeast Face',
        'season': 'September to October',
        'length': 'About 40 days',
        'first': '1956, Toshio Imanishi and Gyalzen Norbu',
    },
    'nanga-parbat-8125': {
        'about': "The western anchor of the Himalaya, in Pakistan. Its Rupal Face is one of the "
                 "tallest mountain walls in the world. The normal route on the Diamir side is steep "
                 "and technical, with rock and ice climbing high on the mountain.",
        'route': 'Kinshofer Route, Diamir Face',
        'season': 'June to July',
        'length': 'About 50 days',
        'first': '1953, Hermann Buhl, alone',
    },
    'annapurna-i-8091': {
        'about': "The first 8,000 metre peak ever climbed, and statistically one of the most dangerous. "
                 "The north side is exposed to avalanches from the hanging glaciers above; it rewards "
                 "patience and a willingness to turn back more than ambition.",
        'route': 'North Face',
        'season': 'April to May',
        'length': 'About 45 days',
        'first': '1950, Maurice Herzog and Louis Lachenal',
    },
    'gasherbrum-i-8080': {
        'about': "Also called Hidden Peak, because it barely shows itself from the Baltoro Glacier. "
                 "Shares its base camp with Gasherbrum II, and the two are often attempted on one "
                 "expedition. Steeper and more serious than its neighbour.",
        'route': 'Japanese Couloir, Northwest Face',
        'season': 'June to August',
        'length': 'About 50 days',
        'first': '1958, Pete Schoening and Andy Kauffman',
    },
    'broad-peak-8051': {
        'about': "A long summit ridge right beside K2, at Concordia in the Karakoram. Often the first "
                 "Karakoram 8,000 metre peak for climbers on their way to K2. The final ridge from "
                 "the foresummit to the main summit is longer than it looks.",
        'route': 'West Spur',
        'season': 'June to August',
        'length': 'About 45 days',
        'first': '1957, Hermann Buhl, Kurt Diemberger, Marcus Schmuck and Fritz Wintersteller',
    },
    'gasherbrum-ii-8034': {
        'about': "The most accessible of the Karakoram 8,000 metre peaks, reached from a base camp on "
                 "the upper Baltoro beyond Concordia. A good first 8,000er in Pakistan, with a "
                 "glacier approach that rewards careful route finding.",
        'route': 'Southwest Ridge',
        'season': 'June to August',
        'length': 'About 45 days',
        'first': '1956, Fritz Moravec, Josef Larch and Hans Willenpart',
    },
    'shisha-pangma-8027': {
        'about': "The lowest of the fourteen 8,000 metre peaks and the only one entirely in Tibet. "
                 "Access depends on Chinese permits, which open and close with little warning. "
                 "The true summit lies along an exposed ridge beyond the central summit.",
        'route': 'North Face and Northwest Ridge',
        'season': 'September to October',
        'length': 'About 40 days',
        'first': '1964, a Chinese expedition led by Xu Jing',
    },

    # ── 7000ers ───────────────────────────────────────────────────────
    'himlung-7126': {
        'about': "A broad snow peak near the Tibetan border, above the hidden Nar and Phu valleys "
                 "north of the Annapurna Circuit. Non-technical by 7,000 metre standards, it has "
                 "become the classic step between a 6,000 metre trekking peak and an 8,000er.",
        'route': 'West Ridge, from the Phu valley',
        'season': 'September to October',
        'length': 'About 30 days',
        'first': '1992, Osamu Hanai, Akio Koizumi and Nima Sherpa',
    },
    'baruntse-7129': {
        'about': "A four-ridged peak between Everest and Makalu, reached through the wild, uninhabited "
                 "Hongu valley. A true expedition with steep sections of fixed line on the summit "
                 "ridge, and views of five of the world’s highest mountains.",
        'route': 'Southeast Ridge',
        'season': 'October, or April to May',
        'length': 'About 30 days',
        'first': '1954, Colin Todd and Geoff Harrow',
    },
    'baruntse-mera': {
        'about': "Mera Peak first, for acclimatisation and a 6,476 metre summit, then over the "
                 "Mera La into the Hongu valley and up Baruntse. Two summits, one long journey, "
                 "and one of the most remote corners of the Khumbu.",
        'route': 'Mera Peak normal route, then Baruntse Southeast Ridge',
        'season': 'October, or April to May',
        'length': 'About 35 days',
        'first': 'Baruntse 1954, Colin Todd and Geoff Harrow',
    },
    'putha-hiunchuli-7246': {
        'about': "The westernmost 7,000 metre peak of the Dhaulagiri range, approached through remote "
                 "Dolpo. A long, glaciated snow climb with little technical difficulty and very few "
                 "other teams, which is exactly why people choose it.",
        'route': 'From the north, via the glacier plateau',
        'season': 'September to October',
        'length': 'About 30 days',
        'first': '1954, Jimmy Roberts and Ang Nyima Sherpa',
    },
    'pumori-7145': {
        'about': "The elegant pyramid that rises directly above Everest Base Camp and Kala Patthar. "
                 "A steep, technical climb on snow and ice with real avalanche risk, and one of the "
                 "most beautiful summits in the Khumbu.",
        'route': 'Southeast Face and Ridge',
        'season': 'October',
        'length': 'About 35 days',
        'first': '1962, Gerhard Lenser',
    },
    'nuptse-7864': {
        'about': "The great wall that closes the Khumbu valley opposite Everest. Every route to its "
                 "summit is a serious technical climb; there is no easy way up, and ascents are rare. "
                 "For experienced alpinists only.",
        'route': 'Technical routes only; no standard line',
        'season': 'October, or April to May',
        'length': 'About 45 days',
        'first': '1961, Dennis Davis and Tashi Sherpa',
    },
    'annapurna-iv-7525': {
        'about': "A high summit on the Annapurna Himal, climbed from the Manang side of the Annapurna "
                 "Circuit. A long snow and ice route along the main ridge, with Annapurna II and the "
                 "Manang valley spread out below.",
        'route': 'North Face and Northwest Ridge',
        'season': 'April to May, or October',
        'length': 'About 35 days',
        'first': '1955, Heinz Steinmetz, Harald Biller and Jürgen Wellenkamp',
    },
}

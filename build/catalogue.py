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
    'annapurna-i-8091': {
        'about': "The first 8,000 metre peak ever climbed, and statistically one of the most dangerous. "
                 "The north side is exposed to avalanches from the hanging glaciers above; it rewards "
                 "patience and a willingness to turn back more than ambition.",
        'route': 'North Face',
        'season': 'April to May',
        'length': 'About 45 days',
        'first': '1950, Maurice Herzog and Louis Lachenal',
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
    'kamet-7756': {
        'about': "The second highest mountain in India, a great pyramid in the Garhwal Himalaya near the "
                 "Tibetan border. When it was first climbed it was the highest summit anyone had ever "
                 "reached. The normal route is a long glacier approach up the East Kamet Glacier to "
                 "Meade’s Col, then the north-east ridge to the top.",
        'route': 'East Kamet Glacier, Meade’s Col and the north-east ridge',
        'season': 'May to June, or September to October',
        'length': 'About 35 to 40 days',
        'first': '1931, Frank Smythe, Eric Shipton, R. L. Holdsworth and Lewa Sherpa',
    },
    'nun-7135': {
        'about': "The highest summit of the Nun Kun massif and the highest peak in Ladakh, rising "
                 "above the Suru valley. A real 7,000 metre expedition with a moderate snow and ice "
                 "line, climbed in the dry Ladakh summer when the rest of the Himalaya is under the "
                 "monsoon.",
        'route': 'West Ridge, from the Shafat Glacier',
        'season': 'July to August',
        'length': 'About 25 to 30 days',
        'first': '1953, Claude Kogan and Pierre Vittoz',
    },
    'trisul-7120': {
        'about': "The trident of Shiva, three summits on one long ridge above the Garhwal foothills. "
                 "Trisul I was the first peak over 7,000 metres ever climbed, and it remained the "
                 "highest summit reached for more than twenty years. Its normal route is a long, "
                 "non-technical snow and glacier climb.",
        'route': 'North-east flank and north ridge',
        'season': 'May to June, or September to October',
        'length': 'About 25 to 30 days',
        'first': '1907, Tom Longstaff, Alexis and Henri Brocherel, and Karbir Burathoki',
    },
    'satopanth-7075': {
        'about': "The high point of the Gangotri group, at the head of the glacier that feeds the "
                 "Ganges. A broad, snowy summit above a dramatic glacier approach, and one of the most "
                 "popular 7,000 metre peaks in India for climbers stepping up from 6,000 metre summits.",
        'route': 'North-east ridge, from the Sundar and Chaturangi glaciers',
        'season': 'May to June, or August to September',
        'length': 'About 22 to 25 days',
        'first': '1947, André Roch, René Dittert, Alexander Graven and Alfred Sutter',
    },

    # ── 6000ers without full route notes ─────────────────────────────
    'kang-yatse-6250': {
        'about': "The throne-shaped peak at the head of the Markha Valley in Ladakh. Kang Yatse II, the "
                 "western summit, is one of the most accessible 6,000 metre peaks in the Himalaya: no "
                 "technical climbing, a beautiful trek in through Buddhist villages, and views across "
                 "the Zanskar and Ladakh ranges from the top.",
        'route': 'Through the Markha Valley to Nimaling, then the west summit',
        'season': 'Mid-June to September',
        'length': 'About 12 to 14 days',
        'first': None,
    },
}

# -*- coding: utf-8 -*-
"""JOURNEYS: the single source of truth for the catalogue.

One entry per journey. Fields:
  slug         URL segment, used by #journey/<slug>
  name         display name
  elevation_m  high point in metres, or None
  category     '8000ers' | '7000ers' | '6000ers' | 'trek'
  region       tab bucket for treks, and the range for expeditions
  country      country or countries
  status       'detailed' | 'catalogue', derived from DETAILS

ELEVATIONS. A slug that states a height gets that height. A combination that
names peaks already in this list gets the HIGH POINT of those peaks. A journey
with a detail entry takes its maxAltitude from there. Everything else is None,
and the card and fact strip omit the line rather than showing a guess.
"""
from details import DETAILS, DIFFICULTY

E8, E7, E6, TK = '8000ers', '7000ers', '6000ers', 'trek'

JOURNEYS = [
    # ── 8000ers ───────────────────────────────────────────────────────
    ('everest-8848',                'Everest',                                           8848,  E8, 'Khumbu',          'Nepal'),
    ('k2-8611',                     'K2',                                                8611,  E8, 'Karakoram',       'Pakistan'),
    ('kangchenjunga-8586',          'Kangchenjunga',                                     8586,  E8, 'Kangchenjunga',   'Nepal'),
    ('lhotse-8516',                 'Lhotse',                                            8516,  E8, 'Khumbu',          'Nepal'),
    ('makalu-8485',                 'Makalu',                                            8485,  E8, 'Makalu Barun',    'Nepal'),
    ('cho-oyu-8188',                'Cho Oyu',                                           8188,  E8, 'Khumbu',          'Nepal'),
    ('dhaulagiri-8167',             'Dhaulagiri I',                                      8167,  E8, 'Dhaulagiri',      'Nepal'),
    ('manaslu-8163',                'Manaslu',                                           8163,  E8, 'Manaslu',         'Nepal'),
    ('nanga-parbat-8125',           'Nanga Parbat',                                      8125,  E8, 'Himalaya',        'Pakistan'),
    ('annapurna-i-8091',            'Annapurna I',                                       8091,  E8, 'Annapurna',       'Nepal'),
    ('gasherbrum-i-8080',           'Gasherbrum I',                                      8080,  E8, 'Karakoram',       'Pakistan'),
    ('broad-peak-8051',             'Broad Peak',                                        8051,  E8, 'Karakoram',       'Pakistan'),
    ('gasherbrum-ii-8034',          'Gasherbrum II',                                     8034,  E8, 'Karakoram',       'Pakistan'),
    ('shisha-pangma-8027',          'Shisha Pangma',                                     8027,  E8, 'Tibet',           'China'),

    # ── 7000ers ───────────────────────────────────────────────────────
    ('himlung-7126',                'Himlung Himal',                                     7126,  E7, 'Manaslu',         'Nepal'),
    ('baruntse-7129',               'Baruntse',                                          7129,  E7, 'Khumbu',          'Nepal'),
    ('baruntse-mera',               'Baruntse and Mera Peak',                            7129,  E7, 'Khumbu',          'Nepal'),
    ('putha-hiunchuli-7246',        'Putha Hiunchuli',                                   7246,  E7, 'Dhaulagiri',      'Nepal'),
    ('pumori-7145',                 'Pumori',                                            7145,  E7, 'Khumbu',          'Nepal'),
    ('nuptse-7864',                 'Nuptse',                                            7864,  E7, 'Khumbu',          'Nepal'),
    ('annapurna-iv-7525',           'Annapurna IV',                                      7525,  E7, 'Annapurna',       'Nepal'),

    # ── 6000ers ───────────────────────────────────────────────────────
    ('ama-dablam-6812',             'Ama Dablam',                                        6812,  E6, 'Khumbu',          'Nepal'),
    ('ama-dablam-lobuche',          'Ama Dablam and Lobuche East',                       6812,  E6, 'Khumbu',          'Nepal'),
    ('ama-dablam-island',           'Ama Dablam and Island Peak',                        6812,  E6, 'Khumbu',          'Nepal'),
    ('three-peaks-ebc',             'Three Peaks and Everest Base Camp',                 None,  E6, 'Khumbu',          'Nepal'),
    ('two-peaks-lobuche-island-ebc', 'Lobuche East, Island Peak and Everest Base Camp',   6189,  E6, 'Khumbu',          'Nepal'),
    ('lobuche-ebc',                 'Lobuche East and Everest Base Camp',                6119,  E6, 'Khumbu',          'Nepal'),
    ('lobuche-6119',                'Lobuche East',                                      6119,  E6, 'Khumbu',          'Nepal'),
    ('island-peak-ebc',             'Island Peak and Everest Base Camp',                 6189,  E6, 'Khumbu',          'Nepal'),
    ('island-peak-6189',            'Island Peak',                                       6189,  E6, 'Khumbu',          'Nepal'),
    ('mera-peak-6476',              'Mera Peak',                                         6476,  E6, 'Hinku',           'Nepal'),
    ('two-peaks-mera-island',       'Mera Peak and Island Peak',                         6476,  E6, 'Hinku',           'Nepal'),
    ('cholatse-6440',               'Cholatse',                                          6440,  E6, 'Khumbu',          'Nepal'),
    ('chulu-west-6419',             'Chulu West',                                        6419,  E6, 'Annapurna',       'Nepal'),
    ('pharchamo-tashi-lapcha',      'Pharchamo via Tashi Lapcha',                        None,  E6, 'Rolwaling',       'Nepal'),
    ('dhampus-6012',                'Dhampus Peak',                                      6012,  E6, 'Dhaulagiri',      'Nepal'),

    # ── Treks. region is the tab bucket ───────────────────────────────
    ('ebc-trek',                    'Everest Base Camp Trek',                            None,  TK, 'Everest',         'Nepal'),
    ('three-passes',                'Everest Three Passes',                              None,  TK, 'Everest',         'Nepal'),
    ('gokyo-lakes',                 'Gokyo Lakes',                                       None,  TK, 'Everest',         'Nepal'),
    ('annapurna-circuit',           'Annapurna Circuit',                                 None,  TK, 'Annapurna',       'Nepal'),
    ('annapurna-base-camp',         'Annapurna Base Camp',                               None,  TK, 'Annapurna',       'Nepal'),
    ('mardi-himal',                 'Mardi Himal',                                       None,  TK, 'Annapurna',       'Nepal'),
    ('upper-mustang',               'Upper Mustang',                                     None,  TK, 'Annapurna',       'Nepal'),
    ('manaslu-circuit',             'Manaslu Circuit',                                   None,  TK, 'Manaslu',         'Nepal'),
    ('manaslu-base-camp',           'Manaslu Base Camp',                                 None,  TK, 'Manaslu',         'Nepal'),
    ('langtang-valley',             'Langtang Valley',                                   None,  TK, 'Langtang',        'Nepal'),
    ('ladakh-high-passes',          'Ladakh High Passes',                                None,  TK, 'Ladakh',          'India'),
    ('tour-du-mont-blanc',          'Tour du Mont Blanc',                                None,  TK, 'The Alps',        'France, Italy and Switzerland'),
    ('haute-route-trek',            'Haute Route, Chamonix to Zermatt',                  None,  TK, 'The Alps',        'France and Switzerland'),
    ('torres-del-paine-trek',       'Torres del Paine Circuit',                          None,  TK, 'South America',   'Chile'),
    ('huayhuash-circuit',           'Huayhuash Circuit',                                 None,  TK, 'South America',   'Peru'),
    ('kilimanjaro-5895',            'Kilimanjaro',                                       5895,  TK, 'Africa',          'Tanzania'),
]

# Tab order. Global Summits is retired: the expeditions rail is pure climbing,
# and the two routes that sat there which are really treks (Torres del Paine
# and the Haute Route) live in the trekking rail.
EXPEDITION_TABS = [('8000ers', E8), ('7000ers', E7), ('6000ers', E6)]
TREK_TABS = ['Everest', 'Annapurna', 'Manaslu', 'Langtang', 'Ladakh',
             'The Alps', 'South America', 'Africa']

# A detailed journey's stated max altitude wins over the slug's number.
HIGH_POINT = {slug: d['maxAltitude'] for slug, d in DETAILS.items() if d.get('maxAltitude')}
# journeys whose high point is an approximation, rendered with a tilde
APPROX_ALT = {slug for slug, d in DETAILS.items() if d.get('altApprox')}

# ─── CARD PHOTOGRAPHS ────────────────────────────────────────────────────
# Only where the photograph genuinely shows that journey's ground. Every entry
# was checked against assets/images/CREDITS.md (for stock, the photographer's
# own location field) or is an owner photograph from the Everest Base Camp
# trek. A journey with no verified photograph keeps its placeholder: a stand-in
# from the wrong valley is worse than a grey box.
#
# Gokyo Lakes is deliberately absent. There is no Gokyo photograph in the
# library, and no other Khumbu shot is honestly a picture of the Gokyo lakes.
CARD_PHOTO = {
    'annapurna-circuit':       'annapurna-circuit.jpg',
    'ebc-trek':                'ebc-trekkers.jpg',
    'haute-route-trek':        'haute-route-matterhorn.jpg',
    'huayhuash-circuit':       'huayhuash-circuit.jpg',
    'kilimanjaro-5895':        'kilimanjaro.jpg',
    'ladakh-high-passes':      'ladakh-high-passes.jpg',
    'manaslu-circuit':         'manaslu-circuit.jpg',
    'mera-peak-6476':          'expedition-mera-peak.jpg',
    'three-passes':            'everest-three-passes.jpg',
    'torres-del-paine-trek':   'torres-del-paine.jpg',
    'tour-du-mont-blanc':      'tour-du-mont-blanc.jpg',
}


def rows():
    for slug, name, elev, cat, region, country in JOURNEYS:
        yield {
            'slug': slug, 'name': name,
            'elevation_m': HIGH_POINT.get(slug, elev), 'category': cat,
            'region': region, 'country': country,
            'status': 'detailed' if slug in DETAILS else 'catalogue',
            'difficulty': DIFFICULTY.get(slug),
            'photo': 'assets/images/journey-%s.jpg' % slug,
            'card': CARD_PHOTO.get(slug),
            # a surveyed number reads as exact; an approximate one has to say so
            'elev_approx': slug in APPROX_ALT,
        }


if __name__ == '__main__':
    import collections
    r = list(rows())
    c = collections.Counter(x['category'] for x in r)
    print('total %d' % len(r))
    for k in (E8, E7, E6, TK):
        print('  %-9s %d' % (k, c[k]))
    print('detailed:', sum(1 for x in r if x['status'] == 'detailed'))
    print('with card photo:', sum(1 for x in r if x['card']))

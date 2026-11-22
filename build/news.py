# -*- coding: utf-8 -*-
"""Mountaineering News, newest first. One source of truth for the Know the
Mountain news grid and the homepage's latest-news list.

TO ADD AN ENTRY: put a new dict at the TOP, then run python3 build/build.py.
  date      ISO date, sorts and formats from this
  category  Summit | Expedition | Event | In Memoriam
  title     the headline as published
  source    publication name
  url       the original article
  image     a file committed to assets/news/, or None. Never hotlink.
"""
NEWS = [
    {'date': '2026-10-17', 'category': 'Summit',
     'title': 'Summits Begin on Ama Dablam, Late Fall’s Most Popular Peak',
     'source': 'ExplorersWeb',
     'url': 'https://explorersweb.com/first-summits-on-ama-dablam-late-falls-most-popular-peak/',
     'image': None},
    {'date': '2026-10-08', 'category': 'Expedition',
     'title': '788 climbers obtain permits to scale 31 peaks this autumn',
     'source': 'Onlinekhabar',
     'url': 'https://english.onlinekhabar.com/788-climbers-obtain-permits-to-scale-31-peaks-this-autumn.html',
     'image': None},
    {'date': '2026-09-22', 'category': 'Expedition',
     'title': 'The summit will wait: weather closes Manaslu season, Dhaulagiri climbers retreat',
     'source': 'The Himalayan Times',
     'url': 'https://thehimalayantimes.com/nepal/the-summit-will-wait-weather-closes-manaslu-season-dhaulagiri-climbers-retreat',
     'image': None},
    {'date': '2026-03-22', 'category': 'Event',
     'title': 'Immigration eases rules for solo trekkers in restricted areas',
     'source': 'The Kathmandu Post',
     'url': 'https://kathmandupost.com/national/2026/03/22/immigration-eases-rules-for-solo-trekkers-in-restricted-areas',
     'image': None},
]


def js_array():
    """NEWS as a JavaScript array literal for know.html."""
    import json
    rows = []
    for n in NEWS:
        rows.append('  { date: %s, category: %s,\n    title: %s,\n    source: %s,\n    url: %s,\n    image: %s },'
                    % (json.dumps(n['date']), json.dumps(n['category']),
                       json.dumps(n['title'], ensure_ascii=False), json.dumps(n['source']),
                       json.dumps(n['url']), json.dumps(n['image'])))
    return 'const NEWS = [\n' + '\n'.join(rows) + '\n];'

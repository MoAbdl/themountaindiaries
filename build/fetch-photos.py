#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fetch the Wikimedia Commons photographs listed in photo-manifest.json.

    python3 build/fetch-photos.py

For every entry whose file is not already in assets/images, downloads the
Commons original at 2400px wide, saves it as the full-size photograph, and
writes the 800px card derivative next to it (<name>-800.jpg). Files already on
disk are left alone, so the script is safe to re-run.

Needs network access and Pillow. It runs in the fetch-photos GitHub Action;
the site build itself never touches the network.
"""
import io
import json
import os
import sys
import time
import urllib.parse
import urllib.request

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
IMAGES = os.path.join(os.path.dirname(HERE), 'assets', 'images')
UA = 'TheMountainDiariesSiteBuild/1.0 (hello@themountaindiaries.com)'


def fetch(title, width):
    url = ('https://commons.wikimedia.org/wiki/Special:FilePath/'
           + urllib.parse.quote(title.replace(' ', '_')) + '?width=%d' % width)
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception as e:  # rate limits and transient errors
            if attempt == 3:
                raise
            time.sleep(5 * (attempt + 1))


def save(img, path, width):
    im = img.copy()
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im.save(path, 'JPEG', quality=82, optimize=True, progressive=True)


def main():
    manifest = json.load(open(os.path.join(HERE, 'photo-manifest.json'), encoding='utf-8'))
    failed = []
    for m in manifest:
        full = os.path.join(IMAGES, m['file'])
        small = full.replace('.jpg', '-800.jpg')
        if os.path.exists(full) and os.path.exists(small):
            continue
        try:
            img = Image.open(io.BytesIO(fetch(m['title'], 2400))).convert('RGB')
        except Exception as e:
            failed.append('%s (%s)' % (m['file'], e))
            continue
        save(img, full, 2400)
        save(img, small, 800)
        print('  fetched %-45s %dx%d' % (m['file'], img.width, img.height))
        time.sleep(1)
    if failed:
        print('FAILED:\n  ' + '\n  '.join(failed))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())

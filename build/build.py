#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild the whole site from source.

    python3 build/build.py

Writes index.html, explore.html, join.html and IMAGE_MAP.md. Everything is
derived, so those four files should never be hand edited: change the source in
build/ and re-run this.

Set MD_OUT to render into a scratch directory instead of over the committed
pages. That is what build/check.py uses to prove the committed HTML still
matches its source.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

# Order matters. explore-build stamps the base snapshot down as index.html,
# performs the index surgery, writes explore.html, and refreshes the shared nav
# and footer inside p3-join.py; p3-join then regenerates join.html from the
# index style block; the image map reads all three finished pages.
STEPS = [
    ('explore-build.py', 'index.html + explore.html'),
    ('p3-join.py', 'join.html'),
    ('know.py', 'know.html'),
    ('mkimagemap.py', 'IMAGE_MAP.md'),
]


def main():
    out = os.environ.get('MD_OUT') or REPO
    os.makedirs(out, exist_ok=True)
    quiet = '--quiet' in sys.argv
    for script, produces in STEPS:
        r = subprocess.run([sys.executable, os.path.join(HERE, script)],
                           capture_output=True, text=True, cwd=HERE)
        if r.returncode != 0:
            sys.stderr.write('%s FAILED\n%s%s\n' % (script, r.stdout, r.stderr))
            return r.returncode
        if not quiet:
            print('  %-20s -> %s' % (script, produces))
    if not quiet:
        print('build complete in %s' % out)
    return 0


if __name__ == '__main__':
    sys.exit(main())

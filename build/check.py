#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prove the committed HTML still matches its source. Run before every push.

    python3 build/check.py

Rebuilds into a temporary directory and diffs the result against the four
generated files in the repo. Exits 0 when they match, 1 when they drift, and
prints the first differing lines so the cause is obvious.

Drift means one of two things, and the fix differs:
  - someone hand edited a generated page, and the edit is about to be lost
  - the source changed and the pages were not rebuilt
Either way, run build/build.py and review the diff before pushing.

The temporary directory is thrown away, so a failing check never touches the
working tree.
"""
import difflib
import io
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
GENERATED = ['index.html', 'explore.html', 'join.html', 'know.html', 'IMAGE_MAP.md']


def main():
    tmp = tempfile.mkdtemp(prefix='md-check-')
    try:
        env = dict(os.environ, MD_OUT=tmp)
        r = subprocess.run([sys.executable, os.path.join(HERE, 'build.py'), '--quiet'],
                           capture_output=True, text=True, env=env)
        if r.returncode != 0:
            sys.stderr.write('build failed\n%s%s\n' % (r.stdout, r.stderr))
            return 2

        drifted = []
        for name in GENERATED:
            committed = os.path.join(REPO, name)
            fresh = os.path.join(tmp, name)
            if not os.path.exists(fresh):
                drifted.append((name, ['build produced no %s' % name]))
                continue
            a = io.open(committed, encoding='utf-8').read().splitlines(True) \
                if os.path.exists(committed) else []
            b = io.open(fresh, encoding='utf-8').read().splitlines(True)
            if a == b:
                print('  ok      %s' % name)
                continue
            diff = list(difflib.unified_diff(a, b, 'committed/' + name, 'rebuilt/' + name, n=1))
            drifted.append((name, diff))

        if not drifted:
            print('\nall generated files match their source')
            return 0

        print('\nDRIFT: %d file(s) differ from a fresh build' % len(drifted))
        for name, diff in drifted:
            print('\n--- %s ---' % name)
            for line in diff[:40]:
                sys.stdout.write(line if line.endswith('\n') else line + '\n')
            if len(diff) > 40:
                print('  ... %d more diff lines' % (len(diff) - 40))
        print('\nRun: python3 build/build.py')
        return 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())

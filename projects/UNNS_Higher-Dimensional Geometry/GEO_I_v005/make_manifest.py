#!/usr/bin/env python3
"""Write MANIFEST.sha256 (sha-256 of every shipped file except the manifest, caches, smoke output and verifier run reports)."""
import os, hashlib
ROOT = os.path.dirname(os.path.abspath(__file__))
SKIP_DIRS = {'__pycache__', 'smoke'}
out = []
for dp, dn, fn in os.walk(ROOT):
    dn[:] = sorted(d for d in dn if d not in SKIP_DIRS)
    for f in sorted(fn):
        p = os.path.join(dp, f); rel = os.path.relpath(p, ROOT).replace(os.sep, '/')
        if rel in ('MANIFEST.sha256',) or rel.startswith('output/reports/verify_') or f.endswith('.pyc') or f.endswith('.zip'): continue
        out.append((rel, hashlib.sha256(open(p, 'rb').read()).hexdigest()))
with open(os.path.join(ROOT, 'MANIFEST.sha256'), 'w') as fh:
    for rel, h in sorted(out): fh.write('%s  %s\n' % (h, rel))
print(len(out), 'files')

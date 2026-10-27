#!/usr/bin/env python3
"""Build-time helper: python3 tools/make_provenance_v11.py PATH_TO_V010_MANIFEST.sha256
Adds to PROVENANCE.json: inherited_v010_sha256 (files byte-identical to the v010 release at the same path), moved_v010_docs (v010 documents moved to docs_v010/), new_in_v011 (everything else)."""
import os, sys, json, hashlib
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
old = {}
for l in open(sys.argv[1]):
    h, p = l.strip().split(None, 1); old[p.lstrip('*')] = h
prov = json.load(open(os.path.join(ROOT, 'PROVENANCE.json')))
inh = {}; moved = {}
for p, h in old.items():
    q = os.path.join(ROOT, p)
    if os.path.exists(q) and sha(q) == h and not p.startswith('docs_v010/') and p != 'PROVENANCE.json': inh[p] = h
    elif os.path.exists(os.path.join(ROOT, 'docs_v010', os.path.basename(p))) and '/' not in p and sha(os.path.join(ROOT, 'docs_v010', os.path.basename(p))) == h: moved[p] = 'docs_v010/' + os.path.basename(p)
prov['inherited_v010_sha256'] = inh; prov['moved_v010_docs'] = moved
allf = []
for dp, dn, fn in os.walk(ROOT):
    dn[:] = [d for d in dn if d not in ('__pycache__', 'smoke')]
    for f in fn:
        rel = os.path.relpath(os.path.join(dp, f), ROOT).replace(os.sep, '/')
        if rel in ('MANIFEST.sha256', 'PROVENANCE.json') or rel.startswith('output/reports/verify_') or f.endswith('.pyc') or f.endswith('.zip'): continue
        allf.append(rel)
prov['new_in_v011'] = sorted(p for p in allf if p not in inh and not p.startswith('docs_v010/'))
json.dump(prov, open(os.path.join(ROOT, 'PROVENANCE.json'), 'w'), indent=1)
print(len(inh), 'inherited', len(moved), 'moved', len(prov['new_in_v011']), 'new')

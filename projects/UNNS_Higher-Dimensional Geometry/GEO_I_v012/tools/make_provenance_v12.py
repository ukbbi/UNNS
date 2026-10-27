#!/usr/bin/env python3
"""Build-time helper: python3 tools/make_provenance_v12.py PATH_TO_V011_MANIFEST.sha256
Adds to PROVENANCE.json: inherited_v011_sha256 (files byte-identical to the v011 release at the same path), moved_v011_docs (v011 root documents now in docs_v011/), new_in_v012 (everything else).
The v010-level keys needed by verify_v011.py are kept."""
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
    if p in ('PROVENANCE.json', 'verify.py', 'RUN_SMOKE.bat', 'RUN_FULL.bat') or p.startswith('output/reports/verify_'): continue
    if os.path.exists(q) and sha(q) == h: inh[p] = h
    elif '/' not in p and p.endswith(('.md', '.tsv')) and os.path.exists(os.path.join(ROOT, 'docs_v011', p)) and sha(os.path.join(ROOT, 'docs_v011', p)) == h: moved[p] = 'docs_v011/' + p
prov['inherited_v011_sha256'] = inh; prov['moved_v011_docs'] = moved
allf = []
for dp, dn, fn in os.walk(ROOT):
    dn[:] = [d for d in dn if d not in ('__pycache__', 'smoke')]
    for f in fn:
        rel = os.path.relpath(os.path.join(dp, f), ROOT).replace(os.sep, '/')
        if rel in ('MANIFEST.sha256', 'PROVENANCE.json') or rel.startswith('output/reports/verify_') or f.endswith('.pyc') or f.endswith('.zip'): continue
        allf.append(rel)
prov['new_in_v012'] = sorted(p for p in allf if p not in inh and not p.startswith('docs_v01'))
json.dump(prov, open(os.path.join(ROOT, 'PROVENANCE.json'), 'w'), indent=1)
print(len(inh), 'inherited', len(moved), 'moved', len(prov['new_in_v012']), 'new')

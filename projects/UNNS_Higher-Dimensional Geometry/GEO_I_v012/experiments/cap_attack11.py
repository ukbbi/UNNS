#!/usr/bin/env python3
"""GEO-I v011 Programme A experiment.  python3 experiments/cap_attack11.py [ONESIDED_DMAX LEMMA_DMAX PENT_DMAX FULL_DMAX]
Writes output/data/v11_cap.json:  one-sided cell family (G11-L3), arithmetic lemma (G11-A), mixed corner pentagon (G11-L4), independent full-box cover (G10-T2 re-run)."""
import os, sys, json, time
from math import gcd
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'); sys.path.insert(0, os.path.join(ROOT, 'theory'))
import cap_cells as K
a = [int(x) for x in sys.argv[1:5]] + [60, 150, 15, 9][len(sys.argv[1:5]):]
OS, LM, PG, FL = a
t0 = time.time(); out = {'release': 'v011', 'params': {'onesided_dmax': OS, 'lemma_dmax': LM, 'pentagon_dmax': PG, 'full_dmax': FL}}
n, bad = K.one_sided_sweep(5, OS); out['onesided'] = {'dmax': OS, 'triples': n, 'failures': bad}
n, bad = K.lemma_scan(LM); out['lemma_G11A'] = {'dmax': LM, 'triples': n, 'failures': bad}
n, sk, bad = K.pentagon_sweep(5, PG); out['pentagon'] = {'dmax': PG, 'nondegenerate_boxes': n, 'degenerate_skipped': sk, 'failures': bad}
nb = 0; bad = []
for d in range(5, FL + 1):
    for s in range(2, d - 1):
        if gcd(s, d) != 1: continue
        for u in range(d):
            for v in range(d):
                if u == v == 0: continue
                nb += 1
                if not K.full_cover(d, s, (d + u, d + v)): bad.append((d, s, u, v))
out['full_cover'] = {'dmax': FL, 'boxes': nb, 'failures': bad}
out['seconds'] = round(time.time() - t0, 1)
json.dump(out, open(os.path.join(ROOT, 'output', 'data', 'v11_cap.json'), 'w'), indent=1)
print({k: (v if not isinstance(v, dict) else {kk: (vv if kk != 'failures' else len(vv)) for kk, vv in v.items()}) for k, v in out.items()})

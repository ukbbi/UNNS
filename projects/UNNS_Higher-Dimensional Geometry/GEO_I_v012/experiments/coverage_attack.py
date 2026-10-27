"""GEO-I v007 Programme A experiments.  Modes:
  acol DMAX OUT          Theorem A-COL machine check (strip cells, lemmas) on all boxes d<=DMAX, Q1 in [d,3d], Q2 in [2d,3d]
  hypll DMAX OUT         classification of the HYP-LL step failures (exact witnesses) for d<=DMAX
  squareless DMIN DMAX OUT [SHARD NSHARD]   adversarial search: for every squareless small box (Q in [d,2d-1]^2, St_LL) decide U=conv(F) with the generic exact routine
Any box with a nonempty exact uncovered region would be a COUNTEREXAMPLE CANDIDATE to G7-C1: it is re-verified (exact rational point z in conv(F)\\U) before being reported."""
import os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
for d_ in ('geometry', 'topology', 'frozen', 'theory'): sys.path.insert(0, os.path.join(HERE, '..', d_))
import coverage_lemmas as CL, coverage as C
from lattice_model import Lat
mode = sys.argv[1]; t0 = time.time()
if mode == 'acol':
    n, bad = CL.verify_Acol(int(sys.argv[2])); res = {'mode': mode, 'dmax': int(sys.argv[2]), 'boxes': n, 'failures': bad}
elif mode == 'hypll':
    r = CL.classify_hypll_steps(int(sys.argv[2])); res = dict(r, mode=mode, dmax=int(sys.argv[2]))
    # split by regime
    big = 0
    from math import gcd
    big = sum(1 for (d, s, q1, q2) in r['failing_other'] if max(q1, q2) >= 2 * d)
    res['failing_other_with_max_ge_2d'] = big
else:
    dmin, dmax = int(sys.argv[2]), int(sys.argv[3]); sh, ns = (int(sys.argv[5]), int(sys.argv[6])) if len(sys.argv) > 6 else (0, 1)
    boxes = 0; sqless = 0; bad = []; k = 0; unresolved = []
    for d in range(dmin, dmax + 1):
        for s in CL.units(d):
            L = None
            for q1 in range(d, 2 * d):
                for q2 in range(d, 2 * d):
                    Q = (q1, q2)
                    if Q == (d, d): continue
                    boxes += 1
                    if not CL.squareless(d, s, Q): continue
                    k += 1
                    if k % ns != sh: continue
                    sqless += 1; L = L or Lat(d, d, d, s)
                    u = C.uncovered(L, Q)
                    if u is None: unresolved.append([d, s, q1, q2])
                    elif len(u) > 0: bad.append([d, s, q1, q2, len(u)])
    res = {'mode': mode, 'range': [dmin, dmax], 'small_boxes': boxes, 'squareless_tested': sqless, 'counterexample_candidates': bad, 'unresolved': unresolved}
res['seconds'] = round(time.time() - t0, 1)
json.dump(res, open(sys.argv[-1] if mode != 'squareless' else sys.argv[4], 'w'), default=str)
print({k: v for k, v in res.items() if k not in ('examples', 'failing_other')})

#!/usr/bin/env python3
"""GEO-I v010 Programme A: bounded test of candidate Euclidean cell-transfer rules.  python3 experiments/sail_attack.py [DMAX]
For every hollow box (Q=(d,d)) and unit s we record the exact Graver-cell data of the frozen cell engine (coverage.complex_data) and test candidate transfer rules
that a continued-fraction induction would need.  A rule is kept only if it holds on EVERY (d,s) tested; each failed rule is written out WITH its counterexamples (G10-L2).
Rules (all are statements about the actual cells, not only about lattice points F):
  R-SYM   cell multiset of (d,s) and (d,s^-1) correspond under the swap (x,y)->(y,x):   counts of 2-cells equal.
  R-MIR   |cells(d,s)| = |cells(d,d-s)|    (mirror s -> -s; excluded at s = d-1 where the hollow structure differs).
  R-EUC   |cells(d,s)| - |cells(s,d mod s)| depends only on the first partial quotient (the naive one-step Euclid transfer).
  R-LAT   the SET of cell generator pairs {(g,h)} of (d,s), mapped by the Euclid unimodular map M_{d,s}, equals that of the reduced lattice (s,d mod s).
Output: output/data/v10_sail_attack.json"""
import os, sys, json
from math import gcd
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
for d in ('geometry', 'topology', 'frozen', 'theory'): sys.path.insert(0, os.path.join(ROOT, d))
import coverage as C
from lattice_model import Lat

def cells(d, s):
    cd = C.complex_data(Lat(d, d, d, s), (d, d))
    return [(tuple(u), tuple(g), tuple(h)) for (u, (g, h)) in (cd['cells'][2] if len(cd['cells']) > 2 else [])]

def gens(d, s): return sorted({tuple(sorted((g, h))) for (_, g, h) in cells(d, s)})

def main(DMAX):
    rec = {}
    for d in range(3, DMAX + 1):
        for s in range(1, d):
            if gcd(d, s) == 1: rec[(d, s)] = (len(cells(d, s)), gens(d, s))
    out = {'dmax': DMAX, 'pairs': len(rec), 'rules': {}}
    # R-SYM
    inv = lambda s, d: next(t for t in range(1, d) if (s * t) % d == 1 % d)
    bad = [(d, s, rec[(d, s)][0], rec[(d, inv(s, d))][0]) for (d, s) in rec if d > 2 and rec[(d, s)][0] != rec[(d, inv(s, d))][0]]
    out['rules']['R-SYM'] = {'holds': not bad, 'counterexamples': bad[:20], 'n_counterexamples': len(bad)}
    bad = [(d, s, rec[(d, s)][0], rec[(d, d - s)][0]) for (d, s) in rec if s != d - 1 and s != 1 and (d, d - s) in rec and rec[(d, s)][0] != rec[(d, d - s)][0]]
    out['rules']['R-MIR'] = {'holds': not bad, 'counterexamples': bad[:20], 'n_counterexamples': len(bad)}
    # R-EUC: difference of cell counts under (d,s)->(s, d mod s) grouped by floor(d/s)
    diffs = {}
    for (d, s), (n, _) in rec.items():
        if s >= 3 and (s, d % s) in rec and d % s >= 1:
            diffs.setdefault(d // s, set()).add(n - rec[(s, d % s)][0])
    bad = {str(q): sorted(v) for q, v in diffs.items() if len(v) > 1}
    out['rules']['R-EUC'] = {'holds': not bad, 'differences_by_first_quotient': {str(q): sorted(v) for q, v in diffs.items()}, 'counterexamples': bad}
    # R-LAT: is the generator-pair set of (d,s) (first coordinates only) in bijection with that of (s, d mod s) after the unimodular Euclid map (x,y)->(x, y - q x)?
    bad = []
    for (d, s), (n, G) in rec.items():
        if s >= 3 and d % s >= 1 and (s, d % s) in rec:
            q = d // s; red = rec[(s, d % s)][1]
            mapped = sorted(tuple(sorted(((a[0], a[1] - q * a[0]) for a in pair))) for pair in G)
            if mapped != red: bad.append((d, s))
    out['rules']['R-LAT'] = {'holds': not bad, 'n_counterexamples': len(bad), 'counterexamples': bad[:20], 'tested': sum(1 for (d, s) in rec if s >= 3 and d % s >= 1)}
    json.dump(out, open(os.path.join(ROOT, 'output', 'data', 'v10_sail_attack.json'), 'w'), indent=1)
    for k, v in out['rules'].items(): print(k, 'HOLDS' if v['holds'] else 'FALSE', v.get('n_counterexamples', ''), str(v.get('counterexamples'))[:160])

if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 18)

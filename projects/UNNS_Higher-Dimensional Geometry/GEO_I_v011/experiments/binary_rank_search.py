"""G6-C3 Programme B: exhaustive search of 0/1 boxes of binary relation lattices (exponent-2 residue groups), k=n coordinates.
Enumerates all multisets of n nonzero columns in F_2^m (m<=MMAX), tests 'minimal non-embedded' (non-embedded, all deletions embedded) and records min witness span.
A refutation of G6-C3 would be a minimal box with min span >= 4.  usage: binary_rank_search.py N MMAX OUT.json"""
import os, sys, json, itertools, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'theory'))
from binary_01 import *
n, mmax, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
t0 = time.time(); seen = set(); hist = {}; ex = {}; tot = 0; maxspan = 0
for m in range(1, mmax + 1):
    for cols in itertools.combinations_with_replacement(range(1, 1 << m), n):
        # rank of columns must be m (otherwise already counted at smaller m)
        r = 0; basis = []
        for c in cols:
            for b in basis: c = min(c, c ^ b)
            if c: basis.append(c); r += 1
        if r != m: continue
        tot += 1
        if not minimal_nonembedded(list(cols)): continue
        a = analyse(list(cols)); sp = a['min_span']
        hist[sp] = hist.get(sp, 0) + 1; ex.setdefault(sp, list(cols))
json.dump({'n': n, 'mmax': mmax, 'columns_sets_tested': tot, 'minimal_boxes_by_min_span': hist, 'example': ex, 'seconds': round(time.time() - t0, 1)}, open(out, 'w'))
print(n, mmax, tot, hist, round(time.time() - t0, 1))

"""GEO-I v007 Programme B: census of minimal non-embedded 0/1 boxes with rank statistics (adversarial search for a rank>=4 minimal box).
usage: rank_counterexamples.py N MMAX OUT.json [SHARD NSHARD]
By Theorem F3 (nullity>=3 for full-support collisions) and the observation that every collision of a minimal box has full support (CHECKED here),
the census is COMPLETE among boxes of nullity >= 3 when MMAX >= N-3 ('complete_nullity_ge3'; complete over ALL boxes only when MMAX >= N-1, 'complete_all_ranks'); a minimal
box whose collisions are all non-full-support is not excluded by proof (hypothesis FS), so the n>=7 censuses are labelled 'complete under FS'; otherwise 'restricted'.  A minimal box with min witness rank >= 4 would be a counterexample
(six-point certificate: columns, non-embedded, all deletions embedded, all witnesses' ranks listed, a rank>=4 witness, exact intersection point)."""
import os, sys, json, itertools, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'theory'))
import binary_01 as B, centre_collisions as CC, rank_reduction as RR
n, mmax, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
sh, ns = (int(sys.argv[4]), int(sys.argv[5])) if len(sys.argv) > 5 else (0, 1)
t0 = time.time(); k = 0; tested = 0; hist = {}; full_only = True; nullhist = {}; types = {}; ex = {}
for m in range(1, mmax + 1):
    for cols in itertools.combinations_with_replacement(range(1, 1 << m), n):
        basis = []
        for c in cols:
            for b in basis: c = min(c, c ^ b)
            if c: basis.append(c)
        if len(basis) != m: continue
        k += 1
        if k % ns != sh: continue
        tested += 1; cols = list(cols)
        if not B.minimal_nonembedded(cols): continue
        cs = CC.collisions(cols); rk = min(RR.witness_rank(n, a, b)[0] for _, a, b in cs)
        hist[rk] = hist.get(rk, 0) + 1; ex.setdefault(rk, cols)
        nl = n - m; nullhist[nl] = nullhist.get(nl, 0) + 1
        for cen, a, b in cs:
            if cen[0] != (1 << n) - 1: full_only = False
            t = (len(a[2]), len(b[2])); t = tuple(sorted(t)); types[str(t)] = types.get(str(t), 0) + 1
json.dump({'n': n, 'mmax': mmax, 'complete_nullity_ge3': mmax >= n - 3 and ns == 1, 'complete_all_ranks': mmax >= n - 1 and ns == 1, 'sets_tested': tested, 'minimal_boxes_by_min_rank': hist, 'nullity_hist': nullhist,
           'collision_types': types, 'all_collisions_full_support': full_only, 'example': ex, 'seconds': round(time.time() - t0, 1)}, open(out, 'w'))
print(n, mmax, tested, hist, nullhist, full_only, round(time.time() - t0, 1))

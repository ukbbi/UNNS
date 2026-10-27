"""GEO-I v008 Programme C: COMPLETE censuses of minimal non-embedded binary 0/1 boxes via two proved reductions:
  B-NULL' (v008): every non-embedded box has nullity n - rank M >= 3   (so only rank m <= n-3 needs searching), and
  B-BASIS (v008): every box of rank m is GL_m(F_2)-equivalent to (e_1..e_m) + (n-m extra columns), so enumerating bases + multisets of extra columns is exhaustive.
usage: rank_attack.py N [MMAX] OUT.json  (default MMAX = N-3 = complete; smaller MMAX is labelled restricted)
Output: representatives tested, minimal ones, minimum-witness-rank histogram, collision-type/rank histogram, FS check, code-invariant classes."""
import os, sys, json, itertools, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'theory'))
import binary_01 as B, centre_collisions as CC, rank_reduction as RR


def basis_sets(n, m):
    es = [1 << i for i in range(m)]
    for extra in itertools.combinations_with_replacement(range(1, 1 << m), n - m): yield es + list(extra)


def fingerprint(cols):
    n = len(cols); C = B.codewords(cols); circ = B.circuits_of(C)
    w = lambda x: bin(x).count('1')
    return (tuple(sorted(w(c) for c in C)), tuple(sorted(w(c) for c in circ)), len(cols))


if __name__ == '__main__':
    n = int(sys.argv[1]); mmax = int(sys.argv[2]) if len(sys.argv) > 3 else n - 3; out = sys.argv[-1]
    t0 = time.time(); tested = 0; minimal = 0; hist = {}; types = {}; classes = {}; fs = True; has22rank3 = True; nonembedded = 0; ex = {}
    for m in range(1, mmax + 1):
        for cols in basis_sets(n, m):
            tested += 1
            if B.is_embedded(cols): continue
            nonembedded += 1
            if not B.minimal_nonembedded(cols): continue
            minimal += 1; rk = []; r22 = False
            for cen, a, b in CC.collisions(cols):
                r = RR.witness_rank(n, a, b)[0]; rk.append(r)
                t = str((len(a[2]), len(b[2])) if len(a[2]) <= len(b[2]) else (len(b[2]), len(a[2]))) + ' rank ' + str(r); types[t] = types.get(t, 0) + 1
                if cen[0] != (1 << n) - 1: fs = False
                if len(a[2]) == 2 and len(b[2]) == 2 and r == 3: r22 = True
            has22rank3 &= r22
            mr = min(rk); hist[mr] = hist.get(mr, 0) + 1; ex.setdefault(mr, cols)
            classes.setdefault(fingerprint(cols), cols)
    res = {'n': n, 'mmax': mmax, 'complete': mmax >= n - 3, 'representatives_tested': tested, 'nonembedded_representatives': nonembedded, 'minimal_representatives': minimal,
           'min_rank_histogram': hist, 'distinct_code_invariant_classes': len(classes), 'all_collisions_full_support': fs, 'every_minimal_has_22_rank3_collision': has22rank3,
           'collision_type_rank_histogram': types, 'example': {str(k): v for k, v in ex.items()}, 'seconds': round(time.time() - t0, 1)}
    json.dump(res, open(out, 'w'), indent=1); print({k: v for k, v in res.items() if k not in ('example', 'collision_type_rank_histogram')})

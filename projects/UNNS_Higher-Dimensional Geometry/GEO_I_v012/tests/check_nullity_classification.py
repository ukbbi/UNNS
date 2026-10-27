"""GEO-I v008: independent cross-check of the nullity-3/4 classification (theory/binary_min.py) against direct basis+extras enumeration (experiments/rank_attack.basis_sets).
Path 1: reduced supports (orbit classification in F_2^k) blown up by B-SERIES.   Path 2: brute-force minimal boxes of rank m = n-k.
Compared as sets of code invariants (weight distribution of C, circuit weights, n)."""
import os, sys, itertools, json
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'); sys.path.insert(0, os.path.join(R, 'theory')); sys.path.insert(0, os.path.join(R, 'experiments'))
import binary_01 as B, binary_min as BM
from rank_attack import basis_sets, fingerprint


def path1(k, n, cls):
    fps = set()
    for o in cls[k]['minimal_reduced_orbits']:
        sig, p = o['support'], o['p']
        if p > n: continue
        for comp in itertools.product(range(1, n - p + 2), repeat=p):
            if sum(comp) != n: continue
            fps.add(fingerprint(BM.blowup_parity_columns(sig, list(comp))))
    return fps


def path2(k, n):
    fps = set(); m = n - k
    for cols in basis_sets(n, m):
        if B.is_embedded(cols) or not B.minimal_nonembedded(cols): continue
        fps.add(fingerprint(cols))
    return fps


def run(nmax=8):
    cls = {k: BM.classify_nullity(k) for k in (3, 4)}; rep = []; ok = True
    for n in range(4, nmax + 1):
        for k in (3, 4):
            if n - k < 1: continue
            a, b = path1(k, n, cls), path2(k, n); good = (a == b); ok &= good
            rep.append({'n': n, 'k': k, 'path1': len(a), 'path2': len(b), 'equal': good})
    return ok, rep


if __name__ == '__main__':
    ok, rep = run(int(sys.argv[1]) if len(sys.argv) > 1 else 8)
    for r in rep: print(r)
    print('ALL EQUAL' if ok else 'MISMATCH')

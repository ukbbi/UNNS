"""G4-T4: classification of the index-4 elementary-2-group lattices in dimension 3 (Klein-four family).
Lambda depends only on the homomorphism Z^3 -> H = Z2^2.  Up to coordinate permutations and Aut(H) there are exactly two surjective
types with all three images non-trivial:  (a,b,ab)  [pairwise distinct]  and  (a,a,b)  [one repeat].  (Images equal to 0 are unit axes: k reduces.)
This module computes the exact atlas of minimal obstruction boxes of both types through the template criterion, for several moduli b
realizing them (the atlas is independent of b), and returns the data."""
import os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
for d_ in ('geometry', 'topology', 'frozen', 'experiments', 'theory'): sys.path.insert(0, os.path.join(HERE, '..', d_))
from math import gcd
from obstruction_templates import Lattice, obstruction_atlas


def types():
    out = {}
    for b in (8, 12, 15, 21, 24):
        us = [r for r in range(2, b) if gcd(r, b) == 1 and r * r % b == 1]
        import itertools
        for res in itertools.combinations_with_replacement(us, 3):
            S = {1}; 
            for r in res: S |= {s * r % b for s in S}
            if len(S) != 4: continue
            kind = 'abc' if len(set(res)) == 3 else 'aab'
            out.setdefault((kind), []).append((b, res))
    return out


def run(bs=(8, 15, 24)):
    res = {}
    for kind, lst in types().items():
        for b, r in lst:
            if b not in bs: continue
            t = time.time(); lat = Lattice(r, b); ts, anti = obstruction_atlas(lat)
            res.setdefault(kind, []).append({'b': b, 'res': list(r), 'minimal_boxes': sorted(map(list, anti)), 'n_templates': len(ts), 't': round(time.time() - t, 1)})
    return res


if __name__ == '__main__':
    print(json.dumps(run(), indent=1))

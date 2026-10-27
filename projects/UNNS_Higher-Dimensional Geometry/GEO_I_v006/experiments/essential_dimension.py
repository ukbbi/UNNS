"""G4-T6 essential dimensionality.  Adjoin a prime with residue 1 mod b (unit axis e_{k+1} in Lambda).
Measured: (E-a) classification  [embedded for all boxes]  of base vs. extended;  (E-b) which new minimal obstruction boxes appear and at which
height q_{k+1};  (E-c) monotonicity: every base obstruction box (q,0) persists.  usage: essential_dimension.py BMAX OUT"""
import os, sys, json, time, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
for d_ in ('geometry', 'topology', 'frozen', 'experiments', 'theory'): sys.path.insert(0, os.path.join(HERE, '..', d_))
from math import gcd
from obstruction_templates import Lattice, obstruction_atlas
from arithmetic_criteria import invariants


def compare(res, b):
    t = time.time()
    _, A0 = obstruction_atlas(Lattice(res, b)); _, A1 = obstruction_atlas(Lattice(tuple(res) + (1,), b))
    A0 = sorted(tuple(a) for a in A0); A1 = sorted(tuple(a) for a in A1)
    k = len(res)
    persist = all(tuple(a) + (0,) in A1 or any(all(m[i] <= a[i] for i in range(k)) and m[k] == 0 for m in A1) for a in A0)
    new = [a for a in A1 if a[k] >= 1]
    inv0, inv1 = invariants(res, b), invariants(tuple(res) + (1,), b)
    return {'b': b, 'res': list(res), 'base_boxes': [list(a) for a in A0], 'ext_boxes': [list(a) for a in A1], 'new_boxes_height>=1': [list(a) for a in new],
            'max_new_height': max([a[k] for a in new], default=0), 'class_same': (not A0) == (not A1), 'direct0': inv0['direct_product'], 'direct1': inv1['direct_product'],
            'persist': persist, 'lowered_threshold': bool(new), 't': round(time.time() - t, 1)}


def main(bmax, out, k=2):
    with open(out, 'w') as f:
        for b in range(2, bmax + 1):
            us = [r for r in range(2, b) if gcd(r, b) == 1]
            for res in itertools.combinations_with_replacement(us, k):
                f.write(json.dumps(compare(res, b)) + '\n'); f.flush()


if __name__ == '__main__':
    main(int(sys.argv[1]), sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 2)

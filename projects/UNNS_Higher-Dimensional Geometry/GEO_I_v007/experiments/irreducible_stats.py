"""G5-C4: irreducible witnesses.  DEFINITION: a witness (c1,c2) at a box is irreducible if no other pair of faces (f1<=c1, f2<=c2) is itself a witness
(non-face pair).  G5-C4 conjectured irreducible witnesses are planar (d_span <= 2).  This script tabulates (d_span, d_support, dims) of irreducible
witnesses at chosen boxes.   usage: irreducible_stats.py OUT.json"""
import os, sys, json, time, collections
HERE = os.path.dirname(os.path.abspath(__file__))
for d_ in ('geometry', 'topology', 'frozen', 'theory'): sys.path.insert(0, os.path.join(HERE, '..', d_))
from obstruction_templates import Lattice
from witness_dimension import witnesses_from_cells, irreducibility

CASES = [('parity3', (2, 2, 2), 3, (2, 2, 2)), ('parity4_min', (2, 2, 2, 2), 3, (1, 1, 1, 1)), ('parity5_ones', (2, 2, 2, 2, 2), 3, (1, 1, 1, 1, 1)),
         ('parity4_2222', (2, 2, 2, 2), 3, (2, 2, 2, 2)), ('klein_abc', (3, 5, 7), 8, (1, 2, 3)), ('mod24_4111', (5, 7, 13, 23), 24, (4, 1, 1, 1))]


def run(out, cases=CASES):
    rows = []
    for name, res, b, m in cases:
        t = time.time(); lat = Lattice(res, b); W = witnesses_from_cells(res, b, m, lat); fl = irreducibility(W)
        irr = [w for w, f in zip(W, fl) if f]
        rows.append({'case': name, 'res': list(res), 'b': b, 'box': list(m), 'witnesses': len(W), 'irreducible': len(irr),
                     'irr_span': dict(collections.Counter(str(w['d_span']) for w in irr)), 'irr_support': dict(collections.Counter(str(w['d_support']) for w in irr)),
                     'irr_dims': dict(collections.Counter('%d-%d' % (len(w['A']), len(w['B'])) for w in irr)),
                     'planar_irreducible_fraction': (sum(1 for w in irr if w['d_span'] <= 2) / len(irr)) if irr else None, 'seconds': round(time.time() - t, 1)})
        print(rows[-1], flush=True)
    json.dump(rows, open(out, 'w'), indent=1)


if __name__ == '__main__':
    run(sys.argv[1])

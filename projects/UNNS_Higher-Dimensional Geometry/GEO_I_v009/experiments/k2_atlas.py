"""E3 (k=2): minimal obstruction boxes of the pure lattices L(d,s) (box measured in scaled units Q).
For general (o1,o2,d,s) the boxes are q >= (a*Q1, c*Q2) with a=o1/d, c=o2/d  (scaling reduction S1)."""
import os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
for d_ in ('geometry', 'topology', 'frozen', 'experiments', 'theory'): sys.path.insert(0, os.path.join(HERE, '..', d_))
from math import gcd
from lattice_model import Lat
from obstruction_templates import LatticeFromLat, obstruction_atlas


def run(dmax, out=None):
    rows = []
    for d in range(1, dmax + 1):
        for s in range(1, d + 1):
            if gcd(s, d) != 1: continue
            L = Lat(d, d, d, s) if d > 1 else Lat(1, 1, 1, 1)
            t = time.time(); ts, anti = obstruction_atlas(LatticeFromLat(L))
            rows.append({'d': d, 's': s, 'minimal_boxes': sorted(map(list, anti)), 'n_templates': len(ts), 't': round(time.time() - t, 1)})
            if out: out.write(json.dumps(rows[-1]) + '\n'); out.flush()
    return rows


if __name__ == '__main__':
    with open(sys.argv[2], 'w') as f: run(int(sys.argv[1]), f)

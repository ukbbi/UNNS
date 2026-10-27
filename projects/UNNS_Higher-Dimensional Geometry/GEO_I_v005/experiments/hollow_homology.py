"""G5-C2: beta_1 at the hollow box (d,d).  Proof checks for s = +-1 (theory/hollow_box.py) and a table of exact beta_1(U) for every (d,s) up to DMAX
by the v004 planar-arrangement route.  usage: hollow_homology.py DMAX OUT.json"""
import os, sys, json, time
from math import gcd
HERE = os.path.dirname(os.path.abspath(__file__))
for d_ in ('geometry', 'topology', 'frozen', 'theory'): sys.path.insert(0, os.path.join(HERE, '..', d_))
from hollow_box import check_s_plus, check_s_minus
from lattice_model import Lat, U_betti

if __name__ == '__main__':
    dmax, out = int(sys.argv[1]), sys.argv[2]; rows = []
    for d in range(2, dmax + 1):
        for s in range(1, d):
            if gcd(s, d) != 1: continue
            t = time.time(); b = U_betti(Lat(d, d, d, s), (d, d))[0]
            rows.append({'d': d, 's': s, 'betti': b, 'beta1_pred': d if (s + 1) % d == 0 else 2, 'seconds': round(time.time() - t, 1)})
    proofs = [check_s_minus(d) for d in range(2, 41)] + [check_s_plus(d) for d in range(3, 41)]
    json.dump({'table': rows, 'proof_checks': proofs, 'proof_ok': all(p['ok'] for p in proofs)}, open(out, 'w'), indent=1, default=str)
    print(all(r['betti'][1] == r['beta1_pred'] for r in rows), all(p['ok'] for p in proofs))

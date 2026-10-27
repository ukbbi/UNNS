"""GEO-I v008 Programme B: hole-disappearance index.  For Q_h = (d,h), h = d..2d, compute exact beta_1(U_{d,s,Q_h}) and the exact uncovered area of conv(F)\\U.
usage: hole_death.py DMIN DMAX OUT.json     (no monotonicity assumed; records the whole sequence and every increase.)
h_first_drop(d,s) = least h with beta_1(U_h) < beta_1(U_d);  h_zero(d,s) = least h with beta_1(U_h) = 0 (and conv(F) = U at that h);  h_stay0 = least h after which beta_1 = 0 for all larger h in the window."""
import os, sys, json, time
from math import gcd
HERE = os.path.dirname(os.path.abspath(__file__))
for d_ in ('geometry', 'topology', 'frozen', 'theory'): sys.path.insert(0, os.path.join(HERE, '..', d_))
import coverage as C
from lattice_model import Lat, U_betti
from fractions import Fraction as Fr


def uncovered_area(d, s, Q):
    pcs = C.uncovered(Lat(d, d, d, s), Q)
    return sum((C.area2(p) for p in pcs), Fr(0)) / 2


def sequence(d, s):
    rows = []
    for h in range(d, 2 * d + 1):
        Q = (d, h); b = U_betti(Lat(d, d, d, s), Q)[0]; a = uncovered_area(d, s, Q)
        rows.append({'h': h, 'betti': list(b), 'uncovered_area': str(a)})
    return rows


def summarise(rows):
    b1 = [r['betti'][1] for r in rows]; hs = [r['h'] for r in rows]
    first_drop = next((h for h, b in zip(hs, b1) if b < b1[0]), None)
    h_zero = next((h for h, b, r in zip(hs, b1, rows) if b == 0 and Fr(r['uncovered_area']) == 0), None)
    h_stay0 = None
    for i in range(len(b1)):
        if all(b == 0 for b in b1[i:]): h_stay0 = hs[i]; break
    increases = [(hs[i], b1[i - 1], b1[i]) for i in range(1, len(b1)) if b1[i] > b1[i - 1]]
    return {'beta1_seq': b1, 'first_drop': first_drop, 'h_zero': h_zero, 'h_stay0': h_stay0, 'increases': increases, 'monotone_nonincreasing': not increases}


if __name__ == '__main__':
    dmin, dmax, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]; res = []
    for d in range(dmin, dmax + 1):
        for s in range(1, d):
            if gcd(s, d) != 1: continue
            t = time.time(); rows = sequence(d, s); sm = summarise(rows)
            res.append({'d': d, 's': s, **sm, 'rows': rows, 'seconds': round(time.time() - t, 1)})
            print(d, s, sm['beta1_seq'], sm['first_drop'], sm['h_zero'], sm['increases'], flush=True)
    json.dump(res, open(out, 'w'), indent=1)

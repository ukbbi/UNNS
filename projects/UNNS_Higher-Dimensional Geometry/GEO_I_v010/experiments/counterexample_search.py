"""G4-C1 counterexamples to the v003 guess  q_i > o_i  =>  beta_1(U_x) = 0   (k = 2).
For each model (d,a,c,s) with a,c >= 2 we realize the relation lattice by (b, residues, primes), take q_i = a_i d + 1 (> o_i, and Q = (d,d)),
and certify beta_1(U) through three independent routes:  (i) v003 geometric pipeline (exact planar arrangement, over Q);
(ii) the pure-model pipeline (scaling reduction S1);  (iii) the nerve of the maximal-cell cover over Q (convex cover => nerve theorem)."""
import os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
for d_ in ('geometry', 'topology', 'frozen', 'experiments', 'theory'): sys.path.insert(0, os.path.join(HERE, '..', d_))
from math import gcd
from fractions import Fraction as Fr
from realization import fibre_complex, fibre_complex_data, cover_cells
from subdivision import planar_subdivision, planar_cells_for_homology
from chain_complex import betti
from homology_compare import betti_nerve
from validation import audit
from lattice_model import Lat, U_betti
from stabilization import realize, data_to_pure, predicted_beta1


def certify(d, a, c, s):
    r = realize(a * d, c * d, d, s, 400)
    if r is None: return {'d': d, 'a': a, 'c': c, 's': s, 'status': 'NO_REPRESENTATIVE_FOUND_b<=400'}
    b, res, primes = r['b'], r['res'], r['primes']
    o = (a * d, c * d); q = (o[0] + 1, o[1] + 1)
    fc = fibre_complex_data(res, q, b)
    cov = cover_cells(fc['cells']); allc = [x for dd in fc['cells'] for x in dd]
    sub = planar_subdivision(cov, fc['F'], refine=allc); cl, bd = planar_cells_for_homology(sub); bU = betti(cl, bd)[0]
    bn, info = betti_nerve(cov, maxdim=2)
    Lp, Q = data_to_pure(o[0], o[1], d, s, q)
    bp, _ = U_betti(Lp, Q)
    a_ = audit(fc)
    x = Fr(primes[0] ** (2 * q[0]) * primes[1] ** (2 * q[1]), b)          # v002 convention: box q_i = floor(e_i / 2)
    fx = fibre_complex(x)
    swap = list(fx['ps']) != list(primes)                                  # coords() sorts the primes; compare after the axis swap
    fxF = sorted((y, x_) for (x_, y) in fx['F']) if swap else sorted(fx['F']); fxq = list(reversed(fx['q'])) if swap else list(fx['q'])
    same = fx['b'] == b and fxq == list(q) and fxF == sorted(fc['F']) and sorted(fx['ps']) == sorted(primes)
    return {'d': d, 'a': a, 'c': c, 's': s, 'b': b, 'residues': list(res), 'primes': list(primes), 'orders': list(o), 'q': list(q), 'x': str(x), 'x_matches_fibre': same,
            'q_gt_o': all(q[i] > o[i] for i in range(2)), 'Q_scaled': list(Q), 'R': len(fc['F']), 'embedded': a_['status'] == 'embedded',
            'betti_U_pipeline_v003': bU, 'betti_U_pure_model': bp, 'betti_nerve_Q': bn, 'predicted_beta1': predicted_beta1(d, s, Q)}


def run(models=((2, 2, 2), (3, 2, 2), (4, 2, 2), (5, 2, 2), (2, 2, 3), (3, 2, 3), (2, 3, 3))):
    out = []
    for d, a, c in models:
        for s in range(1, d + 1):
            if gcd(s, d) != 1: continue
            t = time.time(); r = certify(d, a, c, s); r['t'] = round(time.time() - t, 1); out.append(r)
    return out


if __name__ == '__main__':
    for r in run(): print(json.dumps(r))

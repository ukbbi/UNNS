"""GEO-I v008 Programme A: exhaustive adversarial sweep of the small-box region for d in [DMIN,DMAX]: every unit s, every Q = (d+u,d+v), (u,v) != (0,0), 0<=u,v<d.
Method (path 1): v005 exact all-cells routine coverage.is_hull_covered (exact rational polygon subtraction).  A failure would be a decisive counterexample and is written with the exact leftover polygon.
Also checks G8-S (squareless staircase formula) against the v007 definition, per box.   usage: small_attack.py DMIN DMAX OUT.json [STEP_OFFSET STEP]  (d, s ordered; deterministic)."""
import os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
for d_ in ('geometry', 'topology', 'frozen', 'theory'): sys.path.insert(0, os.path.join(HERE, '..', d_))
import coverage as C
from lattice_model import Lat
import small_box as SB

if __name__ == '__main__':
    dmin, dmax, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    res = {'range': [dmin, dmax], 'boxes': 0, 'covered': 0, 'failures': [], 'by_region': {}, 'squareless': 0, 'staircase_mismatch': 0, 'per_d': {}}; t0 = time.time()
    for d in range(dmin, dmax + 1):
        nb = 0
        for s in SB.units(d):
            m = SB.record_min(d, s); nsq = 0
            for Q in SB.boxes(d):
                ok = C.is_hull_covered(Lat(d, d, d, s), Q); res['boxes'] += 1; nb += 1; res['covered'] += bool(ok)
                rg = SB.region(d, s, Q); res['by_region'][rg] = res['by_region'].get(rg, 0) + 1
                sq = SB.squareless(d, s, Q); nsq += sq; res['squareless'] += sq
                if sq != SB.squareless_staircase(d, s, Q, m): res['staircase_mismatch'] += 1
                if not ok: res['failures'].append({'d': d, 's': s, 'Q': Q, 'leftover': [[(str(x), str(y)) for x, y in p] for p in C.uncovered(Lat(d, d, d, s), Q)]}); print('FAILURE', d, s, Q, flush=True)
            assert nsq == SB.n_squareless(d, s), (d, s, nsq, SB.n_squareless(d, s))
        res['per_d'][d] = nb; open(out + '.progress', 'a').write(json.dumps({'d': d, 'boxes': nb, 'failures_so_far': len(res['failures']), 'squareless_so_far': res['squareless']}) + '\n'); print('d', d, 'boxes', nb, 'fail', len(res['failures']), round(time.time() - t0), 's', flush=True)
    res['seconds'] = round(time.time() - t0, 1); json.dump(res, open(out, 'w'), indent=1)
    print('TOTAL', res['boxes'], 'covered', res['covered'], 'failures', len(res['failures']), 'squareless', res['squareless'], 'staircase_mismatch', res['staircase_mismatch'])

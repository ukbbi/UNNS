"""G5-C1 counterexample-first search + base-window certificates (resumable, deterministic order).
usage: stabilization_search.py DMIN DMAX OUT.jsonl [SHARD NSHARD] [--hollow]
For every type (d,s) (s <= s^-1 mod d) the whole base window W_d = [d,3d-1]^2 minus (d,d) is tested with the exact polygon-subtraction test
(theory/coverage.py).  By the translation lemma S4 this decides U = conv(F) for ALL Q >= (d,d), Q != (d,d).  A violation is recorded with the box,
the exact vertices of the uncovered convex pieces and a rational witness point (their centroid); nothing is skipped.
Row = one finished type; a killed job resumes at the first unfinished type (work counts are reported separately from wall-clock)."""
import os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
for d_ in ('geometry', 'topology', 'frozen', 'theory'): sys.path.insert(0, os.path.join(HERE, '..', d_))
from math import gcd
from lattice_model import Lat, U_betti
from coverage import uncovered


def inv(s, d):
    return next(t for t in range(1, d + 1) if (s * t) % d == 1 % d)


def types(dmin, dmax):
    for d in range(dmin, dmax + 1):
        for s in range(1, d):
            if gcd(s, d) == 1 and inv(s, d) >= s: yield d, s


def certify(d, s, hollow=True):
    L = Lat(d, d, d, s); t0 = time.time(); viol = []; boxes = 0
    sym = inv(s, d) == s                                           # s^2 = 1: the box set is symmetric under swapping the axes
    for q1 in range(d, 3 * d):
        for q2 in range(d, 3 * d):
            if (q1, q2) == (d, d) or (sym and q2 < q1): continue
            boxes += 1; r = uncovered(L, (q1, q2))
            if r:
                P = r[0]; cx = sum(p[0] for p in P) / len(P); cy = sum(p[1] for p in P) / len(P)
                viol.append({'Q': [q1, q2], 'pieces': [[[str(x), str(y)] for x, y in pc] for pc in r[:4]], 'witness': [str(cx), str(cy)]})
    row = {'d': d, 's': s, 'boxes_tested': boxes, 'symmetric': sym, 'violations': viol, 'seconds': round(time.time() - t0, 1)}
    if hollow:
        b, _ = U_betti(L, (d, d)); row['hollow_betti'] = b; row['hollow_pred'] = d if (s + 1) % d == 0 else 2
    return row


if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if not x.startswith('--')]
    dmin, dmax, out = int(a[0]), int(a[1]), a[2]; sh, ns = (int(a[3]), int(a[4])) if len(a) > 4 else (0, 1)
    done = set()
    if os.path.exists(out): done = {(json.loads(l)['d'], json.loads(l)['s']) for l in open(out)}
    with open(out, 'a') as f:
        for k, (d, s) in enumerate(types(dmin, dmax)):
            if k % ns != sh or (d, s) in done: continue
            f.write(json.dumps(certify(d, s)) + '\n'); f.flush()

"""G5-C3 / G5-C4 search.  For lattices Lambda = ker(Z^k -> (Z/b)^x) (k = 3, 4) find all minimal obstruction boxes inside a bound
(independent LP audit as oracle) and tabulate the exact witness table of each (complete, from the actual complex):
d_span, d_support, d_intersection, kinds, essential-coordinate flag.  A box with min_span >= 3 is a counterexample to the weak form of G5-C3.
usage: span_two_search.py K BMAX BOUND OUT.jsonl [orders_max]
Resumable: lattices already in OUT are skipped.  Resource exhaustion -> row with status UNAVAILABLE (never PASS)."""
import os, sys, json, time, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
for d_ in ('geometry', 'topology', 'frozen', 'theory'): sys.path.insert(0, os.path.join(HERE, '..', d_))
from math import gcd
from obstruction_templates import Lattice
from witness_dimension import minimal_boxes, audit_oracle, analyse_box_cells


def _light(res, b):
    from arith import in_lambda, order_mod
    o = [order_mod(r, b) for r in res]
    return o, (lambda a: in_lambda(res, b, a))


def lattice_key(res, b):
    """canonical key of the lattice up to coordinate permutation (orders + residues of Lambda modulo the orders), minimised over permutations."""
    o, mem = _light(res, b); k = len(res)
    pts = [a for a in itertools.product(*[range(x) for x in o]) if mem(a)]
    best = None
    for perm in itertools.permutations(range(k)):
        key = (tuple(o[i] for i in perm), tuple(sorted(tuple(a[i] for i in perm) for a in pts)))
        if best is None or key < best: best = key
    return best, o, len(pts)


def classes(k, bmax, omax):
    seen = {}
    from arith import order_mod
    for b in range(3, bmax + 1):
        units = [r for r in range(2, b) if gcd(r, b) == 1]
        for res in itertools.combinations_with_replacement(units, k):
            if max(order_mod(r, b) for r in res) > omax: continue
            key, o, sz = lattice_key(res, b)
            if key not in seen: seen[key] = {'b': b, 'res': res, 'orders': o, 'direct': sz == 1, 'lam_mod_o': sz}
    return list(seen.values())


def run(k, bmax, bound, out, omax=6):
    done = set()
    if os.path.exists(out):
        for l in open(out):
            r = json.loads(l); done.add((r['b'], tuple(r['res'])))
    cl = classes(k, bmax, omax); print('classes', len(cl), flush=True)
    with open(out, 'a') as f:
        for c in cl:
            if (c['b'], tuple(c['res'])) in done or c['direct']: continue
            t = time.time(); row = dict(c); row['res'] = list(c['res']); row['orders'] = list(c['orders']); row['k'] = k; row['bound'] = bound
            try:
                lat = Lattice(c['res'], c['b']); orc = audit_oracle(c['res'], c['b'])
                mins = minimal_boxes(lat, bound, oracle=orc)
                boxes = []
                for m in mins:
                    r = analyse_box_cells(c['res'], c['b'], m, orc, lat)
                    ex = min(r['witnesses'], key=lambda w: (w['d_span'], w['d_support']), default=None)
                    r.pop('witnesses'); r['example_min_witness'] = ex; boxes.append(r)
                row['status'] = 'OK'; row['minimal_boxes'] = boxes
                row['min_span_ge3_boxes'] = [r['box'] for r in boxes if r['min_span'] is not None and r['min_span'] >= 3]
            except Exception as e:
                row['status'] = 'UNAVAILABLE'; row['error'] = str(e)[:200]
            row['seconds'] = round(time.time() - t, 1); f.write(json.dumps(row) + '\n'); f.flush()


if __name__ == '__main__':
    k, bmax, bound, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    run(k, bmax, bound, out, int(sys.argv[5]) if len(sys.argv) > 5 else 6)

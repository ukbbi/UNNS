"""G5-C3/T5 mandatory families: Klein-four (both types), parity lattices (n=3,4), the mod-24 lattice (5,7,13,23) and extra 4-coordinate
lattices.  For every minimal obstruction box inside the bound: the complete witness table (span / support / intersection) computed from the
actual complex, with the independent LP audit as embeddedness oracle.  Output JSON.
usage: four_dimensional.py OUT.json"""
import os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
for d_ in ('geometry', 'topology', 'frozen', 'theory'): sys.path.insert(0, os.path.join(HERE, '..', d_))
from obstruction_templates import Lattice
from witness_dimension import minimal_boxes, audit_oracle, analyse_box_cells, canon

FAMILIES = [
    ('klein4_abc', (3, 5, 7), 8, 4), ('klein4_aab', (3, 3, 5), 8, 4),
    ('parity3', (2, 2, 2), 3, 3), ('parity4', (2, 2, 2, 2), 3, 3),
    ('mod24_same_parity', (5, 7, 13, 23), 24, 4),
]


def run_family(name, res, b, bound):
    t = time.time(); lat = Lattice(res, b); orc = audit_oracle(res, b)
    mins = minimal_boxes(lat, bound, oracle=orc); rows = []
    for m in mins:
        r = analyse_box_cells(res, b, m, orc, lat)
        ex = min(r['witnesses'], key=lambda w: (w['d_span'], w['d_support']))
        r['example_min_witness'] = ex
        r['witnesses'] = sorted([{k: w[k] for k in ('A', 'B', 'delta', 'kind', 'd_span', 'd_support', 'd_intersection')} for w in r['witnesses']],
                                key=lambda w: (w['d_span'], w['d_support']))[:12]
        rows.append(r)
    return {'family': name, 'res': list(res), 'b': b, 'orders': lat.o, 'bound': bound, 'k': lat.k,
            'minimal_boxes_in_bound': [r['box'] for r in rows], 'boxes': rows, 'seconds': round(time.time() - t, 1),
            'weak_C3_fails_at': [r['box'] for r in rows if r['min_span'] >= 3],
            'essential_boxes': [r['box'] for r in rows if r['essential_coordinate']]}


def run(fams=FAMILIES):
    return [run_family(*f) for f in fams]


if __name__ == '__main__':
    res = run(); json.dump(res, open(sys.argv[1], 'w'), indent=1, default=str)
    for r in res:
        print(r['family'], 'minimal boxes', len(r['minimal_boxes_in_bound']), 'weak-C3 fails at', r['weak_C3_fails_at'], 'essential', r['essential_boxes'][:6], r['seconds'], flush=True)

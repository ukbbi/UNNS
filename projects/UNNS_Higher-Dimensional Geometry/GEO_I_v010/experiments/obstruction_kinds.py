"""G4-T6 / E5: for each minimal obstruction box list the templates realized exactly there with their kind (O-E, O-D, O-T, O-C),
coordinate support and span dimension (support dimension = number of coordinates used, span dimension = rank of the generators).
usage: obstruction_kinds.py OUT.json"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
for d_ in ('geometry', 'topology', 'frozen', 'experiments', 'theory'): sys.path.insert(0, os.path.join(HERE, '..', d_))
from obstruction_templates import Lattice, obstruction_atlas


def kinds(res, b, maxdim=None):
    ts, anti = obstruction_atlas(Lattice(res, b), maxdim)
    out = {}
    for m in anti:
        rows = [t for t in ts if m in t['min_boxes']]
        out[str(m)] = {'kinds': sorted({t['kind'] for t in rows}), 'support_dims': sorted({len(t['support']) for t in rows}), 'span_dims': sorted({t['span_dim'] for t in rows}),
                       'n_templates': len(rows), 'example': {'A': rows[0]['A'], 'B': rows[0]['B'], 'delta': rows[0]['delta']}}
    return out


if __name__ == '__main__':
    data = {'b=5 (2,3)': kinds((2, 3), 5), 'b=8 (3,5,7) Klein-four (a,b,ab)': kinds((3, 5, 7), 8), 'b=8 (3,3,5) Klein-four (a,a,b)': kinds((3, 3, 5), 8),
            'b=3 (2,2,2) parity n=3': kinds((2, 2, 2), 3)}
    json.dump(data, open(sys.argv[1], 'w'), indent=1, default=str)

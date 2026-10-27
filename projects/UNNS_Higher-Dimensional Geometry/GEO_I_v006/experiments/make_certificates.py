"""G5-T6: write machine-checkable witness certificates for (i) every minimal obstruction box with min d_span >= 3 found by span_two_search
(ALL of its witnesses), and (ii) one minimal-span witness for every essential box of the mandatory families.  Every certificate is re-verified
by theory/certificates.verify_certificate (independent code) before it is written.   usage: make_certificates.py OUT.json"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
for d_ in ('geometry', 'topology', 'frozen', 'theory'): sys.path.insert(0, os.path.join(HERE, '..', d_))
from witness_dimension import witnesses_from_cells, audit_oracle
from certificates import make_certificate, verify_certificate
from obstruction_templates import Lattice

DATA = os.path.join(HERE, '..', 'output', 'data')


def run(out):
    cert = {'span_ge3': [], 'essential_families': []}
    for fn in ('span_search_k4.jsonl', 'span_search_k3.jsonl'):
        for l in open(os.path.join(DATA, fn)):
            r = json.loads(l)
            for bx in r.get('minimal_boxes', []):
                if bx['min_span'] is not None and bx['min_span'] >= 3:
                    res, b, m = tuple(r['res']), r['b'], tuple(bx['box']); lat = Lattice(res, b)
                    W = witnesses_from_cells(res, b, m, lat); cs = []
                    for w in W:
                        c = make_certificate(res, b, m, w); ok, info = verify_certificate(c); assert ok, info
                        cs.append({'certificate': c, **info})
                    orc = audit_oracle(res, b)
                    below = [tuple(m[j] - (j == i) for j in range(len(m))) for i in range(len(m)) if m[i] > 0]
                    cert['span_ge3'].append({'res': list(res), 'b': b, 'orders': r['orders'], 'box': list(m), 'n_witnesses': len(W),
                                             'all_witnesses_d_span': sorted({x['d_span'] for x in cs}), 'predecessors_embedded': all(orc(lat, q) for q in below if any(q)),
                                             'certificates': cs})
    fam = json.load(open(os.path.join(DATA, 'four_dimensional_families.json')))
    for f in fam:
        res, b = tuple(f['res']), f['b']
        for bx in f['boxes']:
            if bx['essential_coordinate']:
                m = tuple(bx['box']); W = witnesses_from_cells(res, b, m)
                w = min(W, key=lambda w: (w['d_span'], w['d_support']))
                c = make_certificate(res, b, m, w); ok, info = verify_certificate(c); assert ok, info
                cert['essential_families'].append({'family': f['family'], 'box': list(m), 'certificate': c, **info})
    json.dump(cert, open(out, 'w'), indent=1)
    print(len(cert['span_ge3']), 'span>=3 boxes;', len(cert['essential_families']), 'essential family certificates')


if __name__ == '__main__':
    run(sys.argv[1])

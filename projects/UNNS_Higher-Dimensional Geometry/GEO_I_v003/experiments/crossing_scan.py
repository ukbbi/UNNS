"""Exhaustive k=2 residue scan: for every modulus b, residue pair (r1,r2) mod b and box (q1,q2), compare K_abs with the
geometric image U_x.  Output: one JSON line per case.  usage: crossing_scan.py BMIN BMAX QMAX OUT"""
import os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'geometry')); sys.path.insert(0, os.path.join(HERE, '..', 'topology'))
from math import gcd
from homology_compare import *
from subdivision import *
from chain_complex import betti
import intersections as X

P = 2305843009213693951       # 2^61 - 1 : fast stand-in for Q in bulk scans (rank_p <= rank_Q; exact-Q recheck is done separately)

def edge_audit(fc):
    E = [edge_endpoints(e) for e in edges_of(fc['cells'])]
    cnt = {}; pts = set()
    for i in range(len(E)):
        a = E[i]; ax0, ax1 = sorted((a[0][0], a[1][0]))
        for j in range(i + 1, len(E)):
            bq = E[j]
            if max(bq[0][0], bq[1][0]) < ax0 or min(bq[0][0], bq[1][0]) > ax1: continue
            kind, p = X.seg_relation(a[0], a[1], bq[0], bq[1])
            if kind == 'disjoint': continue
            cnt[kind] = cnt.get(kind, 0) + 1
            if kind == 'interior_cross': pts.add(p)
    return cnt, len(pts)

def run_case(b, r1, r2, q1, q2):
    fc = fibre_complex_data((r1, r2), (q1, q2), b)
    if not fc['F']: return None
    t = time.time()
    babs = betti_abs(fc['cells'], P)[0]
    cov = cover_cells(fc['cells']); allc = [c for d in fc['cells'] for c in d]
    sub = planar_subdivision(cov, fc['F'], refine=allc)
    cl, bd = planar_cells_for_homology(sub)
    bU, d2, eu = betti(cl, bd, P)
    cnt, ncp = edge_audit(fc)
    return {'b': b, 'r': [r1, r2], 'q': [q1, q2], 'R': len(fc['F']), 'cells': [len(c) for c in fc['cells']], 'G': len(fc['G']),
            'abs': babs, 'U': bU, 'edge_rel': cnt, 'n_crossing_points': ncp, 'cover': len(cov), 'sub': [len(sub['vertices']), len(sub['edges']), len(sub['faces'])],
            'ok': bool(d2 and eu), 't': round(time.time() - t, 2)}

if __name__ == '__main__':
    bmin, bmax, qmax, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    with open(out, 'w') as f:
        for b in range(bmin, bmax + 1):
            units = [r for r in range(1, b) if gcd(r, b) == 1] or [1]
            for r1 in units:
                for r2 in units:
                    if r2 < r1: continue
                    for q1 in range(1, qmax + 1):
                        for q2 in range(1, qmax + 1):
                            rec = run_case(b, r1, r2, q1, q2)
                            if rec: f.write(json.dumps(rec) + '\n')
            f.flush()

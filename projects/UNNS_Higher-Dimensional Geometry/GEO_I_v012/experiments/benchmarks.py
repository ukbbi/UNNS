"""E1-E6 mandatory benchmarks (exact)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
for d in ('geometry', 'topology', 'frozen', 'experiments'): sys.path.insert(0, os.path.join(HERE, '..', d))
from fractions import Fraction as Fr
import intersections as X
from realization import fibre_complex, cover_cells, fibre_complex_data
from validation import audit
from homology_compare import betti_abs, betti_nerve, betti_clique
from subdivision import planar_subdivision, planar_cells_for_homology, validate_planar
from chain_complex import betti
from arith import crossing_offsets, graver_complete, group_order, order_mod


def e1():
    x = Fr(82944, 5); fc = fibre_complex(x)
    F = fc['F']; a = audit(fc)
    cov = cover_cells(fc['cells']); allc = [c for d in fc['cells'] for c in d]
    sub = planar_subdivision(cov, F, refine=allc); val = validate_planar(sub, cov, F)
    cl, bd = planar_cells_for_homology(sub); bU = betti(cl, bd)
    rel = X.seg_relation((1, 1), (5, 1), (2, 2), (4, 0))
    off = crossing_offsets((2, 3), 5, (4, 0), (2, -2))        # w in Lambda strictly inside open parallelogram {t g - lam h}
    cl_b, info = betti_clique(F, fc['G'])
    return {'x': str(x), 'primes': fc['ps'], 'q': fc['q'], 'b': fc['b'], 'F': F, 'edges': [[list(u), list(X.add(u, g))] for (u, (g,)) in fc['cells'][1]],
            'cell2': [[list(u), [list(g) for g in gens]] for (u, gens) in fc['cells'][2]],
            'crossing': {'point': [str(c) for c in rel[1]], 'kind': rel[0], 'in_F': (3, 1) in set(F), 'offsets_w_t_lam': [[list(w), str(t), str(l)] for w, t, l in off],
                         'iota': 1 + len(off)},
            'audit': {'status': a['status'], 'edge_relations': a['edge']['relations'], 'cell_pairs': a['cell']['pairs'], 'why': a['cell']['why']},
            'betti_abs_Q': betti_abs(fc['cells'])[0], 'betti_embedded_Q': bU[0], 'betti_clique_Q': cl_b,
            'subdivision': {'vertices': [[str(c) for c in v] for v in sub['vertices']], 'kinds': [sub['prov'][v]['kind'] for v in sub['vertices']],
                            'n_edges': len(sub['edges']), 'n_faces': len(sub['faces']), 'validation': val}}


def e2(tmax=12):
    out = []
    for t in range(tmax + 1):
        x = Fr(2 ** (10 + 2 * t) * 3 ** 4, 5); fc = fibre_complex(x); a = audit(fc); cov = cover_cells(fc['cells']); allc = [c for d in fc['cells'] for c in d]
        sub = planar_subdivision(cov, fc['F'], refine=allc); cl, bd = planar_cells_for_homology(sub); bU = betti(cl, bd)[0]
        F = set(fc['F'])
        out.append({'t': t, 'x': str(x), 'q': fc['q'], 'R': len(F), 'cells': [len(c) for c in fc['cells']],
                    'witness_vertices_present': all(p in F for p in ((1, 1), (5, 1), (2, 2), (4, 0))), 'status': a['status'],
                    'crossing_points': len(a['edge']['crossing_points']), 'has_witness_crossing': ('3', '1') in {tuple(k) for k in a['edge']['crossing_points']} or
                    ('3', '1') in a['edge']['crossing_points'], 'betti_abs': betti_abs(fc['cells'])[0], 'betti_U': bU,
                    'chi_abs': sum((-1) ** j * len(c) for j, c in enumerate(fc['cells']))})
    return out


def e3():
    fc = fibre_complex(Fr(2304, 5)); a = audit(fc)
    return {'F': fc['F'], 'cells': [len(c) for c in fc['cells']], 'edge': fc['cells'][1], 'status': a['status'], 'betti': betti_abs(fc['cells'])[0]}


def _bench(x, expect_cells):
    fc = fibre_complex(x); a = audit(fc)
    cov = cover_cells(fc['cells'])
    bn, info = betti_nerve(cov)
    return {'x': str(x), 'R': len(fc['F']), 'cells': [len(c) for c in fc['cells']], 'expected_cells_v002': expect_cells, 'status': a['status'], 'cell_pairs': a['cell']['pairs'],
            'edge_relations': a['edge']['relations'], 'betti_abs': betti_abs(fc['cells'])[0], 'betti_nerve': bn, 'nerve_info': info, 'k': fc['k'],
            'top_cell': [[list(u), [list(g) for g in gens]] for (u, gens) in fc['cells'][-1]] if len(fc['cells']) == fc['k'] + 1 else None}


def e456():
    return {'E4_3600': _bench(3600, [11, 17, 8, 1]), 'E5_44100': _bench(44100, [15, 28, 18, 4]), 'E6_210pow4': _bench(210 ** 4, [80, 212, 210, 92, 15])}

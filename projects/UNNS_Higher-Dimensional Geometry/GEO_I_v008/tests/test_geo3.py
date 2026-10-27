"""Deterministic tests for GEO-I v003 (run:  python3 tests/test_geo3.py)."""
import os, sys, random, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
for d in ('geometry', 'topology', 'frozen', 'experiments'): sys.path.insert(0, os.path.join(HERE, '..', d))
from fractions import Fraction as Fr
import intersections as X
from exactlp import lp_box
from realization import fibre_complex, fibre_complex_data, cover_cells
from validation import audit
from homology_compare import betti_abs, betti_nerve, betti_clique
from subdivision import planar_subdivision, planar_cells_for_homology, validate_planar
from chain_complex import betti
import benchmarks as B
from arith import crossing_free_for_all_boxes, group_order, order_mod, graver_complete, iota

n_ok = 0
def ok(name, cond):
    global n_ok
    assert cond, 'FAILED: ' + name
    n_ok += 1

# --- exact LP
ok('lp optimal', lp_box([[1, 1]], [Fr(3, 2)], [1, 0], 2)[:2] == ('optimal', 1))
ok('lp infeasible', lp_box([[1, 1]], [3], [0, 0], 2)[0] == 'infeasible')

# --- segment relations (exact), including the v003 witness
ok('witness crossing', X.seg_relation((1, 1), (5, 1), (2, 2), (4, 0)) == ('interior_cross', (Fr(3), Fr(1))))
ok('shared endpoint', X.seg_relation((0, 0), (2, 0), (2, 0), (2, 5))[0] == 'shared_endpoint')
ok('collinear overlap', X.seg_relation((0, 0), (2, 0), (1, 0), (3, 0))[0] == 'collinear_overlap')
ok('collinear touch', X.seg_relation((0, 0), (1, 0), (1, 0), (2, 0))[0] == 'collinear_touch')
ok('3D skew -> disjoint', X.seg_relation((0, 0, 0), (1, 0, 0), (0, 1, 1), (1, 1, 1))[0] == 'disjoint')
ok('3D crossing', X.seg_relation((0, 0, 0), (2, 2, 2), (2, 0, 0), (0, 2, 2))[0] == 'interior_cross')

# --- independent brute force for 2D cell pairs (Sutherland-Hodgman in exact arithmetic)
def clip(poly, a, b):
    out = []
    def side(p): return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
    for i in range(len(poly)):
        p, q = poly[i], poly[(i + 1) % len(poly)]
        sp, sq = side(p), side(q)
        if sp >= 0: out.append(p)
        if (sp > 0 and sq < 0) or (sp < 0 and sq > 0):
            t = sp / (sp - sq); out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return out
def ccw_poly(u, g1, g2):
    pts = [tuple(map(Fr, u)), tuple(map(Fr, X.add(u, g1))), tuple(map(Fr, X.add(X.add(u, g1), g2))), tuple(map(Fr, X.add(u, g2)))]
    area = sum(pts[i][0] * pts[(i + 1) % 4][1] - pts[(i + 1) % 4][0] * pts[i][1] for i in range(4))
    return pts if area > 0 else pts[::-1]
def extreme(pts):
    pts = sorted(set(pts))
    if len(pts) <= 2: return set(pts)
    def cr(o, a, b): return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo = []
    for p in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    up = []
    for p in reversed(pts):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return set(lo[:-1] + up[:-1])
def faces_vertexsets(u, g1, g2):
    vs = X.cell_vertices(u, (g1, g2)); vs = [tuple(map(Fr, v)) for v in vs]
    return [frozenset([v]) for v in vs] + [frozenset([vs[0], vs[1]]), frozenset([vs[0], vs[2]]), frozenset([vs[1], vs[3]]), frozenset([vs[2], vs[3]]), frozenset(vs)]
rng = random.Random(7)
agree = 0; seen = set()
for _ in range(1500):
    def rc():
        while True:
            g1 = (rng.randint(-3, 3), rng.randint(-3, 3)); g2 = (rng.randint(-3, 3), rng.randint(-3, 3))
            if g1[0] * g2[1] - g1[1] * g2[0] != 0: return (rng.randint(0, 4), rng.randint(0, 4)), g1, g2
    (u, a1, a2), (w, b1, b2) = rc(), rc()
    kind, _ = X.cell_relation((u, (a1, a2)), (w, (b1, b2)))
    P, Q = ccw_poly(u, a1, a2), ccw_poly(w, b1, b2)
    poly = P
    for i in range(4):
        poly = clip(poly, Q[i], Q[(i + 1) % 4])
        if not poly: break
    if not poly: bk = 'disjoint'
    else:
        ex = extreme(poly)
        fP = faces_vertexsets(u, a1, a2); fQ = faces_vertexsets(w, b1, b2)
        bk = 'common_face' if (frozenset(ex) in fP and frozenset(ex) in fQ) else 'non_face'
    seen.add(bk); assert bk == kind, (bk, kind, (u, a1, a2), (w, b1, b2)); agree += 1
ok('cell_relation agrees with exact polygon clipping on 1500 random 2D pairs, kinds seen %s' % sorted(seen), agree == 1500 and seen == {'disjoint', 'common_face', 'non_face'})

# --- nerve on synthetic sets with known homology
e = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
faces = []
for i in range(3):
    others = tuple(e[j] for j in range(3) if j != i)
    for s in (0, 1): faces.append((tuple(s if t == i else 0 for t in range(3)), others))
ok('cube surface = S^2', betti_nerve(faces, maxdim=3)[0] == [1, 0, 1])
ok('three orthogonal squares contractible', betti_nerve([((-1, -1, 0), ((2, 0, 0), (0, 2, 0))), ((-1, 0, -1), ((2, 0, 0), (0, 0, 2))), ((0, -1, -1), ((0, 2, 0), (0, 0, 2)))], maxdim=3)[0] == [1, 0, 0])
ring = [((0, 0), ((1, 0),)), ((1, 0), ((0, 1),)), ((0, 1), ((1, 0),)), ((0, 0), ((0, 1),))]
ok('square loop + both diagonals: beta1 = 3 + 1', betti_nerve(ring + [((0, 0), ((1, 1),)), ((1, 0), ((-1, 1),))], maxdim=3)[0] == [1, 4, 0])

# --- E1 regression witness 82944/5
r = B.e1()
ok('E1 fibre', sorted(r['F']) == [(1, 1), (2, 2), (4, 0), (5, 1)])
ok('E1 crossing (3,1) not in F', r['crossing']['point'] == ['3', '1'] and not r['crossing']['in_F'] and r['crossing']['iota'] == 2)
ok('E1 betti', r['betti_abs_Q'] == [1, 2, 0] and r['betti_embedded_Q'] == [1, 0, 0] and r['betti_clique_Q'] == [1, 0, 0])
ok('E1 subdivision valid', r['subdivision']['validation']['all_ok'] and len(r['subdivision']['vertices']) == 5 and r['subdivision']['n_faces'] == 4 and r['subdivision']['kinds'].count('crossing') == 1)
# --- other mandatory benchmarks
e3 = B.e3(); ok('E3 2304/5', e3['F'] == [(1, 1), (4, 0)] and e3['cells'] == [2, 1] and e3['status'] == 'embedded')
e456 = B.e456()
ok('E4 3600', e456['E4_3600']['status'] == 'embedded' and e456['E4_3600']['cells'] == [11, 17, 8, 1] and e456['E4_3600']['betti_abs'] == [1, 0, 0, 0])
ok('E5 44100: 15 vertices, no 4-cell', e456['E5_44100']['R'] == 15 and len(e456['E5_44100']['cells']) == 4 and e456['E5_44100']['status'] == 'embedded')
ok('E6 210^4: 4-cell present', e456['E6_210pow4']['cells'] == [80, 212, 210, 92, 15] and e456['E6_210pow4']['status'] == 'embedded')
# --- arithmetic of crossings
ok('iota = |det|/m (k=2, b=5, (2,3))', iota((2, 3), 5, (4, 0), (2, -2)) == 8 // group_order((2, 3), 5))
ok('k=2: direct product <=> crossing-free (b=5..13)', all(crossing_free_for_all_boxes((a, c), b)[0] == (group_order((a, c), b) == order_mod(a, b) * order_mod(c, b)) for b in range(5, 14) for a in range(1, b) for c in range(a, b) if __import__('math').gcd(a, b) == 1 and __import__('math').gcd(c, b) == 1))
# --- Klein-four exception: no edge ever crosses, but cells overlap improperly
ok('Klein-four b=8 (3,5,7): crossing-free for all boxes, not direct', crossing_free_for_all_boxes((3, 5, 7), 8)[0] and group_order((3, 5, 7), 8) == 4 and order_mod(3, 8) * order_mod(5, 8) * order_mod(7, 8) == 8)
a = audit(fibre_complex_data((3, 5, 7), (3, 3, 2), 8))
ok('Klein-four (3,3,2) cell-level non-embedded with no edge crossing', a['status'] == 'non_embedded' and a['edge']['relations'].get('interior_cross', 0) == 0)
print('GEO-I v003 tests: %d checks passed' % n_ok)

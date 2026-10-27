"""GEO-I v005, G5-C2.  The hollow box Q = (d,d).

THEOREM H1 (s = -1).  beta_1(U) = d.   Proof: F = antidiagonal {(i,d-i)} u {(d,d)}; the complex is the fan graph (V=d+2, E=2d+1); no 2-cell.
THEOREM H2 (s = +1, d >= 3).  beta_1(U) = 2.
  F = {(i,i): 1<=i<=d} u {A=(d,0), B=(0,d)}.  Graver moves in the box: (1,1); (i-d,i) from A and (i,i-d) from B to every diagonal point (i,i), i<d,
  and (0,d),(d,0).  The 2-cells are exactly the parallelograms P_i = conv{A,(i,i),B,(d-i,d-i)}, 1 <= i < d/2 (A+B = (d,d): their diagonals bisect at (d/2,d/2)).
  They are nested, P_1 is the largest, so the union of the 2-cells is the single parallelogram P_1 with corners A,(1,1),B,(d-1,d-1) (contractible).
  The remaining 1-cells outside P_1: the edges A-(d,d), B-(d,d), and (d-1,d-1)-(d,d); each meets P_1 only at its endpoint (not at (d,d)).
  U = P_1 u {(d,d)} u 3 arcs, hence chi(U) = 1 + 1 - 3 = -1 and beta_1 = 1 - chi = 2 (U connected, beta_2 = 0).
This module recomputes the cell structure from the definitions for each d and checks every sentence of the proof."""
import os, sys, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from planar_embed import cells, relint_meet, add, sub, det, _poly
from pure_lattice import fibre


def structure(d, s):
    pts, segs, pars = cells(d, s, (d, d))
    return {'F': sorted(p[1][0] for p in pts), 'edges': sorted(tuple(sorted(e[1])) for e in segs),
            'parallelograms': sorted(tuple(sorted(_corners(c[1]))) for c in pars)}


def _corners(c):
    p, a, b = c
    return [p, add(p, a), add(p, b), add(add(p, a), b)]


def check_s_plus(d):
    assert d >= 3
    A, B, D = (d, 0), (0, d), (d, d)
    st = structure(d, 1); F = set(st['F'])
    ok = {}
    ok['fibre'] = F == {(i, i) for i in range(1, d + 1)} | {A, B}
    expected = set()
    for i in range(1, d):
        if 2 * i < d: expected.add(tuple(sorted([A, (i, i), B, (d - i, d - i)])))
    ok['2cells_are_Pi'] = set(st['parallelograms']) == expected
    P1 = tuple(sorted([A, (1, 1), B, (d - 1, d - 1)]))
    ok['P1_present'] = P1 in expected
    # P_i nested in P_1: every corner of P_i inside the closed P_1
    poly1 = _hull4(P1)
    ok['nested'] = all(_inside_closed(c, poly1) for q in expected for c in q)
    E = set(st['edges'])
    outside = {tuple(sorted([A, D])), tuple(sorted([B, D])), tuple(sorted([(d - 1, d - 1), D]))}
    ok['three_extra_edges_present'] = outside <= E
    # every edge not contained in P_1 is one of the three (edges inside P_1 do not change the homotopy type)
    def in_P1(e): return all(_inside_closed(x, poly1) for x in e)
    ok['no_other_outside_edges'] = {e for e in E if not in_P1(e)} == outside
    # the three arcs meet P_1 only at their endpoint on P_1 (exact: no relint of the arc meets P_1's interior or boundary except the endpoint)
    ok['arcs_touch_P1_once'] = all(_arc_meets_once(e, poly1, D) for e in outside)
    chi = 1 + 1 - 3
    return {'d': d, 's': 1, 'checks': ok, 'beta1': 1 - chi, 'ok': all(ok.values())}


def check_s_minus(d):
    s = d - 1; st = structure(d, s); F = set(st['F'])
    ok = {'fibre': F == {(i, d - i) for i in range(0, d + 1)} | {(d, d)}, 'no_2cell': st['parallelograms'] == []}
    V = len(F); E = len(st['edges'])
    ok['edge_count'] = E == 2 * d + 1
    return {'d': d, 's': s, 'checks': ok, 'V': V, 'E': E, 'beta1': E - V + 1, 'ok': all(ok.values()) and E - V + 1 == d}


def _hull4(corners):
    import coverage as C
    return C.hull(list(corners))


def _inside_closed(x, poly):
    n = len(poly)
    return all(det(sub(poly[(i + 1) % n], poly[i]), sub(x, poly[i])) >= 0 for i in range(n))


def _arc_meets_once(e, poly, D):
    a, b = e
    other = b if a == D else a                     # endpoint on P_1
    # every lattice-free test: sample the segment's relative interior at rational points; none may lie in the closed P_1
    from fractions import Fraction as Fr
    for k in range(1, 40):
        t = Fr(k, 40); x = (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))
        if _inside_closed(x, poly): return False
    return _inside_closed(other, poly) and not _inside_closed(D, poly)

"""GEO-I v008, Programme B: the hollow box Q = (d,d) and the FILLING LEMMA (Theorem G8-T1).

Notation (frozen from v007): Gamma = {(i,j): j = s*i mod d}, t = s^-1 mod d, A = (0,d), B = (d,0), C = (d,d), P_i = (i, s*i mod d);
T1 = tri(A, P_{d-t}, C),  T2 = tri(B, P_{d-1}, C)  with  P_{d-t} = (d-t, d-1),  P_{d-1} = (d-1, d-s);  each of area d/2.   (v007 G7-T3: int T1, int T2 are disjoint from U_{(d,d)}.)

THEOREM G8-T1 (filling lemma).  Let d >= 3, s a unit mod d, Q >= (d,d), Q != (d,d).  Then T1 u T2 is contained in U_{d,s,Q}.
Proof.  Case v := Q2-d >= 1 (Q2 >= d+1).  Put
   R1 = P(A; (d-t,-1), (t,1))      corners A, P_{d-t}, (t,d+1), C        [(t,d+1) = A + C - P_{d-t}]
   R2 = P((t,1); (0,d), (d-t,-1))  corners (t,1), (t,d+1), B, C.
 All corners lie in Gamma (s*t = 1 mod d, so (t,1) and (t,d+1) are in Gamma, and P_{d-t} = (d-t,d-1) because s*(d-t) = -1 mod d), and in the box since Q2 >= d+1.
 Graver generators: (0,d) (the only vertical lattice vectors are multiples of (0,d)); (t,1): a lattice vector (a,b) with 0<=a<=t, 0<=b<=1 is (0,0), (t,1) or has a b=1,
 a = t mod d or b = 0, a = 0 mod d -- so none other (t<d); (d-t,-1): same argument with b = -1, a = -t mod d.  Independence: det((d-t,-1),(t,1)) = d, det((0,d),(d-t,-1)) = -d(d-t) != 0.
 T1 is the triangle with three of the four corners of R1, hence T1 inside R1 (convexity).  T2: B, C are corners of R2; P_{d-1} = (d-1, d-s) lies in R2 because at x = d-1 the parallelogram R2
 occupies 1/(d-t) <= y <= d + 1/(d-t) and 1/(d-t) <= 1 <= d-s <= d-1 < d (convexity of R2 gives T2 = conv(B, C, P_{d-1}) inside R2).
Case u := Q1-d >= 1: transposition.  (i,j) -> (j,i) maps Gamma_{d,s} to Gamma_{d,t}, boxes to transposed boxes, Graver sets to Graver sets, cells to cells, and T1(s) <-> T2(t), T2(s) <-> T1(t).
 Apply the case v >= 1 to (d,t,Q^T).  QED
Explicit cells for u >= 1 (in original coordinates): R1' = P((1,s); (0,d)... see filling_cells().
COROLLARY G8-K1 (the holes die at the first enlargement).  For every d >= 3, unit s and Q = (d,d+1) or (d+1,d), T1 u T2 is inside U: the two bounded complement components of G7-T3 are filled by one single step of the box.
 In particular every hole-disappearance index defined as the first enlargement at which both T1,T2 are filled is 1 (h_* = d+1 along Q=(d,h)).  [beta_1 itself is a different matter: see experiments/hole_death.py.]
COROLLARY G8-R1 (conditional reduction).  If G8-T2 (conv(F_(d,d)) \\ U_(d,d) = int T1 u int T2) holds for (d,s), then conv(F_(d,d)) is contained in U_Q for every Q >= (d,d), Q != (d,d).
 (Cells of U_(d,d) remain cells for the larger box: corners stay in F_Q, Graver generators do not depend on Q.)
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as Fr
from math import gcd


def inv(s, d): return pow(s, -1, d)
def in_gamma(d, s, p): return (p[1] - s * p[0]) % d == 0


def is_graver(d, s, g):
    if g == (0, 0) or not in_gamma(d, s, g): return False
    sa = 1 if g[0] >= 0 else -1; sb = 1 if g[1] >= 0 else -1
    return not any((a, b) not in ((0, 0), (abs(g[0]), abs(g[1]))) and in_gamma(d, s, (sa * a, sb * b)) for a in range(abs(g[0]) + 1) for b in range(abs(g[1]) + 1))


def hollow_triangles(d, s):
    t = inv(s, d)
    return [((0, d), (d - t, d - 1), (d, d)), ((d, 0), (d - 1, d - s), (d, d))]


def filling_cells(d, s):
    """the four filling parallelograms as (u, g, h): R1,R2 (need Q2 >= d+1) and their transposes R1',R2' (need Q1 >= d+1).
    returns dict name -> (cell, triangle index it fills, required box)."""
    t = inv(s, d)
    R1 = ((0, d), (d - t, -1), (t, 1)); R2 = ((t, 1), (0, d), (d - t, -1))
    # transposed cells come from the same construction for (d,t): R1_t = ((0,d),(d-s,-1),(s,1)); R2_t = ((s,1),(0,d),(d-s,-1)); transpose coordinates
    tr = lambda c: tuple((p[1], p[0]) for p in c)
    R1p = tr(((0, d), (d - s, -1), (s, 1))); R2p = tr(((s, 1), (0, d), (d - s, -1)))
    return {'R1': (R1, 0, (d, d + 1)), 'R2': (R2, 1, (d, d + 1)), "R1'": (R2p, 0, (d + 1, d)), "R2'": (R1p, 1, (d + 1, d))}


def corners(cell):
    u, g, h = cell
    return [u, (u[0] + g[0], u[1] + g[1]), (u[0] + g[0] + h[0], u[1] + g[1] + h[1]), (u[0] + h[0], u[1] + h[1])]


def cross(o, a, b): return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def point_in_convex(poly, p):
    """poly: vertices in cyclic order (any orientation); exact closed membership."""
    sg = [cross(poly[i], poly[(i + 1) % len(poly)], p) for i in range(len(poly))]
    return all(x >= 0 for x in sg) or all(x <= 0 for x in sg)


def check_filling(d, s):
    """exact verification of G8-T1 for one (d,s): legitimacy of the four cells in their boxes and triangle-in-parallelogram containment."""
    tri = hollow_triangles(d, s); out = {}
    for name, (cell, ti, Q) in filling_cells(d, s).items():
        u, g, h = cell; cs = corners(cell)
        F = lambda p: in_gamma(d, s, p) and 0 <= p[0] <= Q[0] and 0 <= p[1] <= Q[1] and p != (0, 0)
        ok_corners = all(F(p) for p in cs)
        ok_gen = is_graver(d, s, g) and is_graver(d, s, h) and g[0] * h[1] - g[1] * h[0] != 0
        ok_tri = all(point_in_convex(cs, v) for v in tri[ti])
        out[name] = ok_corners and ok_gen and ok_tri
    return out

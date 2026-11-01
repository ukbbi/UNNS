"""GEO_HD_BRIDGE v003 -- rational-state geometry (R3-A/B).
Source objects are the frozen GEO-I ones (src/frozen/geo2lib.py).  New here: the split of the region-Graver set into
  POSITIVE-PRIMITIVE moves (minimal elements of F), EDGE-REALIZED moves (g = v-u, u,v in F) and DORMANT moves (the rest),
and the F-only reconstruction of the first two classes (theorem R3-T1a)."""
import _paths, itertools
from fractions import Fraction as Fr
from math import gcd
from geo2lib import coords, fibre_points, graver_region, d_value

def record(x):
    """normalised exact record (x is reduced by Fraction)."""
    x = Fr(x); ps, q, b = coords(x)
    F = fibre_points(ps, q, b)
    G = graver_region(ps, q, b)
    return {'x': x, 'ps': ps, 'q': q, 'b': b, 'F': F, 'D': frozenset(d_value(ps, a) for a in F), 'G': G}

def hull_points(u, v, F0):
    lo = [min(a, c) for a, c in zip(u, v)]; hi = [max(a, c) for a, c in zip(u, v)]
    return [w for w in F0 if all(l <= wi <= h for l, wi, h in zip(lo, w, hi))]

def classes_from_F(F, k):
    """positive-primitive and edge-realized Graver vectors computed from F ALONE (no lattice, no box): theorem R3-T1a.
    g=v-u (u,v in F) is conformally minimal iff the hull box of u,v contains no point of F+{0} other than u,v."""
    F0 = list(F) + [tuple([0] * k)]
    pos = [g for g in F if not any(w != g and all(wi <= gi for wi, gi in zip(w, g)) for w in F)]
    edge = set()
    for u in F:
        for v in F:
            if u == v: continue
            if len(hull_points(u, v, F0)) == 2:
                g = tuple(c - a for a, c in zip(u, v)); edge.add(g)
    return set(pos) | {tuple(-c for c in g) for g in pos}, edge

def split_graver(rec):
    k = len(rec['ps']); pos, edge = classes_from_F(rec['F'], k)
    G = set(rec['G']); real = pos | edge
    return {'positive_primitive': sorted(pos & G), 'edge_realized': sorted(edge & G), 'dormant': sorted(G - real),
            'F_only_prediction_ok': (real & G) == (pos | edge) and (pos | edge) <= G}

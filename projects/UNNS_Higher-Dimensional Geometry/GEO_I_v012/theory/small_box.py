"""GEO-I v008, Programme A: the small-box region  S_d = { Q = (d+u, d+v) : 0 <= u,v < d, (u,v) != (0,0) }  and its exact partition.

PARTITION (all integers; s a unit mod d, a_i := s*i mod d):
  bottom  : v = 0, u >= 1          left : u = 0, v >= 1          interior : u,v >= 1.
  m_s(u)  := min_{1<=i<=u} a_i     (record minimum of the first column residues; m_s(u) = d for u = 0).
  squareless (v007 definition): Gamma cap [0,u]x[0,v] = {0}.   THEOREM G8-S (squareless staircase, proved here):  for u,v >= 1,
       Q is squareless  <=>  v < m_s(u).      (all boundary boxes u = 0 or v = 0 are squareless.)
  Proof.  A nonzero point (i,j) of Gamma with 0<=i<=u, 0<=j<=v has i >= 1 (i = 0 forces j = 0 mod d, j<d) and j = a_i; so one exists iff min_{1<=i<=u} a_i <= v.   QED
  Consequently the number of squareless boxes of type (d,s) is  N_sq(d,s) = 2(d-1) + sum_{u=1}^{d-1} (m_s(u) - 1)   (v = 1..m_s(u)-1 for each u >= 1, plus the two boundary rays).
  m_s is a non-increasing step function whose steps are the record minima of s*i mod d = the lower-left Pareto chain of Gamma (continued-fraction convergents of s/d).
EXTENSION POINTS of F_Q over F_(d,d):   R_i = (d+i, a_i) (1<=i<=u),   T_j = (c_j, d+j) (1<=j<=v, c_j = t*j mod d),   K = (d,d) + (Gamma cap [1,u]x[1,v]) (empty iff squareless).
"""
from math import gcd


def units(d): return [s for s in range(1, d) if gcd(s, d) == 1]


def inv(s, d): return pow(s, -1, d)


def a_seq(d, s): return [None] + [(s * i) % d for i in range(1, d)]


def record_min(d, s):
    a = a_seq(d, s); m = [d] * d; cur = d
    for u in range(1, d):
        cur = min(cur, a[u]); m[u] = cur
    return m


def region(d, s, Q):
    u, v = Q[0] - d, Q[1] - d
    if u == 0 and v == 0: return 'hollow'
    if v == 0: return 'bottom'
    if u == 0: return 'left'
    return 'interior'


def squareless(d, s, Q):
    """definition (v007): no nonzero Gamma point in [0,u]x[0,v]."""
    u, v = Q[0] - d, Q[1] - d
    return not any((j - s * i) % d == 0 and (i or j) for i in range(u + 1) for j in range(v + 1))


def squareless_staircase(d, s, Q, m=None):
    """G8-S formula: the same predicate via the record minimum."""
    u, v = Q[0] - d, Q[1] - d
    if u == 0 or v == 0: return True
    m = m or record_min(d, s)
    return v < m[u]


def n_squareless(d, s):
    m = record_min(d, s); return 2 * (d - 1) + sum(m[u] - 1 for u in range(1, d))


def extension_points(d, s, Q):
    u, v = Q[0] - d, Q[1] - d; t = inv(s, d)
    R = [(d + i, (s * i) % d) for i in range(1, u + 1)]
    T = [((t * j) % d, d + j) for j in range(1, v + 1)]
    K = [(d + i, d + j) for i in range(1, u + 1) for j in range(1, v + 1) if (j - s * i) % d == 0]
    return R, T, K


def boxes(d):
    for u in range(d):
        for v in range(d):
            if (u, v) != (0, 0): yield (d + u, d + v)

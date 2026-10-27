"""GEO-I v005: the pure planar lattice Gamma_(d,s) = {(i,j) in Z^2 : j = s*i (mod d)}, scaled box Q=(Q1,Q2).
Everything is exact integer arithmetic.  This module is the single place where the pure model is defined; the v004 `Lat(d,d,d,s)` is
the same object (a = c = 1)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from math import gcd
from lattice_model import Lat


def lat(d, s): return Lat(d, d, d, s % d)


def inv(s, d): return next(t for t in range(1, d + 1) if (s * t) % d == 1 % d)


def in_gamma(d, s, p): return (p[1] - s * p[0]) % d == 0


def fibre(d, s, Q):
    return [(i, j) for i in range(Q[0] + 1) for j in range(Q[1] + 1) if (i or j) and (j - s * i) % d == 0]


def graver(d, s):
    """complete Graver basis (conformally minimal vectors); all components in [-d,d] (|g_i| <= d)."""
    return lat(d, s).graver_complete()


def graver_s_plus(d):  # explicit s = 1
    G = {(1, 1), (-1, -1), (d, 0), (-d, 0), (0, d), (0, -d)}
    for k in range(1, d):
        G |= {(k, -(d - k)), (-k, d - k)}
    return G


def graver_s_minus(d):  # explicit s = -1
    G = {(1, -1), (-1, 1), (d, 0), (-d, 0), (0, d), (0, -d)}
    for k in range(0, d + 1): G |= {(k, d - k), (-k, -(d - k))}
    return G


def types(dmin, dmax):
    """representatives (d,s) up to the symmetry s <-> s^{-1} (coordinate swap)."""
    for d in range(dmin, dmax + 1):
        for s in range(1, d):
            if gcd(s, d) == 1 and inv(s, d) >= s: yield d, s

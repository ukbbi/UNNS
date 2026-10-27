"""GEO-I v004: the *general modular model* for k = 2.

Everything the geometry of a two-axis fibre sees is the relation lattice Lambda = ker(Z^2 -> (Z/b)^x) and the box q.
Lambda contains o1 Z + o2 Z (o_i = ord(r_i)) and is determined by (o1, o2, d, s):
    Lambda = o1 Z (+) o2 Z + Z*(o1/d, s*o2/d),     d | gcd(o1,o2),  s in (Z/d)^x,   [Z^2 : Lambda] = o1*o2/d.
d = 1 is the direct-product case.  Every such lattice is realized by some modulus b and residues r_i (finite abelian groups with two
generators embed in some (Z/b)^x; primes in the classes exist by Dirichlet), so statements about (o1,o2,d,s) are statements about
all rational fibres with these data; a *concrete* rational occurrence fibre is produced separately by `realize`."""
import os, sys, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
for d_ in ('geometry', 'topology', 'frozen', 'experiments'): sys.path.insert(0, os.path.join(HERE, '..', d_))
from math import gcd
from fractions import Fraction as Fr
from geo2lib import build_cells
from realization import cover_cells
from subdivision import planar_subdivision, planar_cells_for_homology
from chain_complex import betti


class Lat:
    __slots__ = ('o1', 'o2', 'd', 's', 'a', 'c', '_G')
    def __init__(self, o1, o2, d=1, s=1):
        assert o1 % d == 0 and o2 % d == 0 and gcd(s, d) == 1 if d > 1 else True
        self.o1, self.o2, self.d, self.s = o1, o2, d, s % d if d > 1 else 0
        self.a, self.c = o1 // d, o2 // d; self._G = None
    @property
    def index(self): return self.o1 * self.o2 // self.d
    def __contains__(self, al):
        x, y = al
        if x % self.a or y % self.c: return False
        t, u = x // self.a, y // self.c
        return (self.s * t - u) % self.d == 0 if self.d > 1 else True
    def __repr__(self): return 'Lat(o=(%d,%d), d=%d, s=%d)' % (self.o1, self.o2, self.d, self.s)
    def graver_complete(self):
        if self._G is None:
            cand = [g for g in itertools.product(range(-self.o1, self.o1 + 1), range(-self.o2, self.o2 + 1)) if any(g) and g in self]
            cand.sort(key=lambda g: (abs(g[0]) + abs(g[1]), g)); G = []
            for g in cand:
                if not any(h[0] * g[0] >= 0 and h[1] * g[1] >= 0 and abs(h[0]) <= abs(g[0]) and abs(h[1]) <= abs(g[1]) for h in G): G.append(g)
            self._G = G
        return self._G
    def graver_region(self, q): return [g for g in self.graver_complete() if abs(g[0]) <= q[0] and abs(g[1]) <= q[1]]
    def fibre(self, q):
        return [(x, y) for x in range(q[0] + 1) for y in range(q[1] + 1) if (x or y) and (x, y) in self]


def lattices(omax, omin=1):
    """all (o1,o2,d,s) up to swapping the axes, o1 <= o2."""
    out = []
    for o1 in range(omin, omax + 1):
        for o2 in range(o1, omax + 1):
            g = gcd(o1, o2)
            for d in range(1, g + 1):
                if g % d: continue
                for s in (range(1, d + 1) if d > 1 else [1]):
                    if d == 1 or gcd(s, d) == 1:
                        if d > 1 and o1 == o2 and s > d - s and False: pass
                        out.append(Lat(o1, o2, d, s))
    return out


def complex_data(L, q):
    F = L.fibre(q)
    if not F: return None
    G = L.graver_region(q)
    cells = build_cells(F, set(G), 2)
    return {'F': F, 'G': G, 'cells': cells}


def U_betti(L, q, field=None, want_sub=False):
    """Betti numbers of the geometric image U (planar union of closed parallelograms/segments) via the exact planar arrangement of the
    cover cells only.  Returns (betti list, info)."""
    cd = complex_data(L, q)
    if cd is None: return None, None
    cov = cover_cells(cd['cells'])
    sub = planar_subdivision(cov, cd['F'])
    cl, bd = planar_cells_for_homology(sub)
    b = betti(cl, bd, field)[0] if field is not None else betti(cl, bd)[0]
    info = {'R': len(cd['F']), 'cover': len(cov), 'cells': [len(c) for c in cd['cells']], 'sub': [len(sub['vertices']), len(sub['edges']), len(sub['faces'])]}
    return b, (info, sub) if want_sub else info

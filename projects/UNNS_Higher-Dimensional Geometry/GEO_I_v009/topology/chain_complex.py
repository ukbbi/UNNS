"""GEO-III.C  exact chain complexes.  Coefficient field: Q (exact Fractions) unless a prime p is requested."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'geometry'))
try:
    from gmpy2 import mpq as Fr          # exact rationals (same results as fractions.Fraction, much faster)
except Exception:                         # pragma: no cover
    from fractions import Fraction as Fr


def rank_Q(cols):
    """exact rank over Q of a list of sparse columns (dict row -> integer/Fraction)."""
    piv = {}; r = 0
    for col in cols:
        c = {k: Fr(v) for k, v in col.items() if v}
        while c:
            p = min(c)
            if p in piv:
                pc = piv[p]; f = c[p] / pc[p]
                for k2, v in pc.items():
                    nv = c.get(k2, 0) - f * v
                    if nv: c[k2] = nv
                    else: c.pop(k2, None)
            else:
                piv[p] = c; r += 1; break
    return r


def rank_p(cols, p):
    piv = {}; r = 0
    for col in cols:
        c = {k: v % p for k, v in col.items() if v % p}
        while c:
            pm = min(c)
            if pm in piv:
                pc = piv[pm]; f = c[pm] * pow(pc[pm], -1, p) % p
                for k2, v in pc.items():
                    nv = (c.get(k2, 0) - f * v) % p
                    if nv: c[k2] = nv
                    else: c.pop(k2, None)
            else:
                piv[pm] = c; r += 1; break
    return r


def betti(cells, bd, field='Q'):
    """cells: list over dimension of lists of hashable cells.  bd(cell) -> dict {face: coeff}.
    returns (betti list, d2_ok, euler_ok)."""
    n = [len(c) for c in cells]
    cols = [None] + [[bd(c) for c in cells[j]] for j in range(1, len(cells))]
    d2 = True
    for j in range(2, len(cells)):
        for c in cells[j]:
            acc = {}
            for f, s in bd(c).items():
                for f2, s2 in bd(f).items(): acc[f2] = acc.get(f2, 0) + s * s2
            if any(acc.values()): d2 = False
    r = [0] * (len(cells) + 1)
    for j in range(1, len(cells)):
        r[j] = rank_Q(cols[j]) if field == 'Q' else rank_p(cols[j], field)
    b = [n[j] - r[j] - r[j + 1] for j in range(len(cells))]
    chi_c = sum((-1) ** j * n[j] for j in range(len(cells))); chi_b = sum((-1) ** j * b[j] for j in range(len(cells)))
    return b, d2, chi_c == chi_b


def simplex_bd(s):
    return {s[:i] + s[i + 1:]: (1 if i % 2 == 0 else -1) for i in range(len(s))}

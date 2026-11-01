"""GEO_HD_BRIDGE v004 -- A4-T1/T2: the arithmetic-activation family and its move complex.
x = P^2/l,  y = (Pq)^2/l,  P = p_1..p_k, p_i = c (mod l), c of exact order k mod prime l, q = c^-1 (mod l) prime.
Relations are kept in UNIVERSAL sparse exponent coordinates (prime -> exponent) so that relations at different
states are comparable (common coordinate embedding).  Only frozen GEO-I objects (record) are used for D, F, Graver."""
import _paths, itertools
from fractions import Fraction as Fr
from math import gcd
from rational_geometry import record, split_graver
from graver_relations import isprime, primes_in_class, primitive_root_of_order
from geo1lib import factor

def evec(d):
    return tuple(sorted(factor(d).items()))

def vsub(a, b):
    r = dict(a)
    for p, e in b: r[p] = r.get(p, 0) - e
    return tuple(sorted((p, e) for p, e in r.items() if e))

def make(k, l, ps, q):
    """validate hypotheses and return exact x,y"""
    assert isprime(l) and (l - 1) % k == 0 and k >= 2
    c = ps[0] % l
    assert all(p % l == c for p in ps) and len(set(ps)) == k and all(isprime(p) for p in ps)
    assert all(pow(c, j, l) != 1 for j in range(1, k)) and pow(c, k, l) == 1
    assert isprime(q) and q not in ps and (q * c) % l == 1
    P = 1
    for p in ps: P *= p
    return Fr(P * P, l), Fr((P * q) ** 2, l), P

def default_instance(k, odd=True):
    l = next(l for l in range(k + 1, 500) if isprime(l) and (l - 1) % k == 0)
    c = primitive_root_of_order(l, k)
    ps = [p for p in primes_in_class(c, l, k + 3, start=3 if odd else 2)][:k]
    cinv = pow(c, -1, l)
    q = next(n for n in range(3, 10 ** 5) if isprime(n) and n % l == cinv and n not in ps)
    return k, l, ps, q

def relations_active(D, g):
    """E_g(D) = {(u,v) in D^2 : e(v)-e(u) = g}"""
    ev = {d: evec(d) for d in D}
    return [(u, v) for u in D for v in D if u != v and vsub(ev[v], ev[u]) == g]

def analyse(k, l, ps, q):
    x, y, P = make(k, l, ps, q)
    rx, ry = record(x), record(y)
    D_x, D_y = set(rx['D']), set(ry['D'])
    expected = {P} | {p * q for p in ps}
    # primitive relations (region Graver) of each state, in universal coordinates
    def univ(rec):
        return {tuple(sorted((p, e) for p, e in zip(rec['ps'], g) if e)) for g in rec['G']}
    Gx, Gy = univ(rx), univ(ry)
    rel = [tuple(sorted(((ps[i], 1), (ps[j], -1)))) for i in range(k) for j in range(k) if i != j]
    rel = [tuple((p, e) for p, e in r) for r in rel]
    # K_move vertices/edges (edge-realized Graver) for y
    sy = split_graver(ry)
    return {'k': k, 'l': l, 'primes': ps, 'q': q, 'P': P, 'x': str(x), 'y': str(y),
            'D_x': sorted(D_x), 'D_y': sorted(D_y), 'D_x_ok': D_x == {P}, 'D_y_ok': D_y == expected,
            'e_i_minus_e_j_in_Gr_x': all(r in Gx for r in rel), 'e_i_minus_e_j_in_Gr_y': all(r in Gy for r in rel),
            'active_at_x': [len(relations_active(D_x, r)) for r in rel][:1], 'all_dormant_at_x': all(not relations_active(D_x, r) for r in rel),
            'all_active_at_y': all(relations_active(D_y, r) for r in rel),
            'Gr_x_size': len(Gx), 'Gr_y_size': len(Gy), 'dormant_x': len(split_graver(rx)['dormant']), 'dormant_y': len(sy['dormant']),
            'edge_realized_y': len(sy['edge_realized']), 'positive_primitive_y': len(sy['positive_primitive'])}

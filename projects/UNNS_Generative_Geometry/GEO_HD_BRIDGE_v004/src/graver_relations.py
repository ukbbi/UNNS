"""R3-A/B/E: explicit infinite families with equal occurrence inventory D and different region-Graver sets.
FAMILY-2 : x_r = (5r)^2/(5r-1),  y_r = (5r)^2/8,  r prime, r = 5 (mod 8).           (Graver sizes 2 vs 4)
FAMILY-k : P = p_1..p_k, p_i = c (mod l), c of exact order k mod prime l = 1 (mod k);  x = P^2/(P-1),  y = P^2/l.  (sizes 2 vs k(k-1)+2)
Existence of the primes is Dirichlet's theorem on primes in arithmetic progressions."""
import _paths
from fractions import Fraction as Fr
from math import gcd
from rational_geometry import record, split_graver
from geo1lib import factor

def isprime(n):
    return n > 1 and all(n % d for d in range(2, int(n ** .5) + 1))

def primes_in_class(res, mod, count, start=2):
    out = []; n = start
    while len(out) < count:
        if isprime(n) and n % mod == res: out.append(n)
        n += 1
    return out

def family2(count=12):
    rs = primes_in_class(5, 8, count, start=13)
    rows = []
    for r in rs:
        x = Fr(25 * r * r, 5 * r - 1); y = Fr(25 * r * r, 8)
        rx, ry = record(x), record(y)
        sx, sy = split_graver(rx), split_graver(ry)
        rows.append({'r': r, 'x': str(x), 'y': str(y), 'ps': rx['ps'], 'q': rx['q'], 'same_ps_q': rx['ps'] == ry['ps'] and rx['q'] == ry['q'],
                     'D_x': sorted(rx['D']), 'D_y': sorted(ry['D']), 'D_equal': rx['D'] == ry['D'] and rx['D'] == {5 * r},
                     'graver_x': len(rx['G']), 'graver_y': len(ry['G']), 'dormant_x': len(sx['dormant']), 'dormant_y': len(sy['dormant']),
                     'dormant_vectors_y': [list(g) for g in sy['dormant']],
                     'lattice_differs': sorted(rx['G']) != sorted(ry['G'])})
    return rows

def primitive_root_of_order(l, k):
    for g in range(2, l):
        if pow(g, (l - 1) // 1, l) == 1 and all(pow(g, (l - 1) // f, l) != 1 for f in factor(l - 1)):
            return pow(g, (l - 1) // k, l)

def familyk(ks=(2, 3, 4, 5)):
    rows = []
    for k in ks:
        l = next(l for l in range(k + 1, 400) if isprime(l) and (l - 1) % k == 0 and l > k)
        c = primitive_root_of_order(l, k)
        assert c is not None and all(pow(c, j, l) != 1 for j in range(1, k)) and pow(c, k, l) == 1
        ps = primes_in_class(c, l, k, start=2)
        P = 1
        for p in ps: P *= p
        assert (P - 1) % l == 0
        x = Fr(P * P, P - 1); y = Fr(P * P, l)
        rx, ry = record(x), record(y); sx, sy = split_graver(rx), split_graver(ry)
        rows.append({'k': k, 'l': l, 'c': c, 'primes': ps, 'P': P, 'b_x': P - 1, 'b_y': l,
                     'D_equal': rx['D'] == ry['D'] == {P}, 'q': rx['q'], 'graver_x': len(rx['G']), 'graver_y': len(ry['G']),
                     'predicted_y': k * (k - 1) + 2, 'dormant_y': len(sy['dormant']), 'dormant_x': len(sx['dormant']),
                     'dormant_y_is_root_system_A': sorted(sy['dormant']) == sorted(tuple(1 if i == a else -1 if i == b else 0 for i in range(k)) for a in range(k) for b in range(k) if a != b)})
    return rows

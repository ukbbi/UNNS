"""GEO_HD_BRIDGE v005 -- A5-T5/T6: collective towers as height filtrations of ONE periodic complex.
x_k = S_k^2/m  (period-start states).  D(x_k) = {d | S_k : d >= 2, d = 1 (mod m)}.  S_k = (fixed part) * p^(e0+k)  (one growing prime p).
K(D(x_k)) is the INDUCED subcomplex of K(D(x_K)), K>=k, on the vertices of p-height <= e0+k (hence K_k subset K_{k+1}: Dead = empty).
Moves: Graver vectors of the lattice Lambda = ker(Z^r -> (Z/m)^*) have l1-norm <= m (Davenport constant of Z/m), so for e0+k >= m the move set is constant."""
import _paths, sys, json, time
from geo1lib import factor, divisors_from
from divisor_complex import complex_of, betti_ranks, edges

def tower_D(S, m):
    ds = divisors_from(factor(S))
    return sorted(d for d in ds if d >= 2 and d % m == 1 % m)

def S11(k): return 2 ** 2 * 3 ** (3 + k) * 5 ** 4
def S5(k): return 126 * 2 ** k

def height(d, p):
    h = 0
    while d % p == 0: d //= p; h += 1
    return h

def row(Sfun, m, k, primes=(2, 2147483647)):
    D = tower_D(Sfun(k), m); K = complex_of(D)
    out = {'k': k, 'nV': len(D), 'f': [len(c) for c in K['cells']]}
    for p in primes:
        f, r, b = betti_ranks(K, p); out['betti_%d' % p] = b
    out['chi'] = sum((-1) ** i * c for i, c in enumerate(out['f']))
    return out

def nested_check(Sfun, m, p, ks):
    """K_k == induced subcomplex of K_kmax on p-height <= (v_p(S_k)) for all k in ks (cell sets)"""
    from transition_calculus import cell_key, cellsets
    kmax = max(ks); Dm = tower_D(Sfun(kmax), m); Km = complex_of(Dm); Cm = cellsets(Km)
    res = {}
    for k in ks:
        D = tower_D(Sfun(k), m); K = complex_of(D); C = cellsets(K)
        h = max(height(d, p) for d in D)
        ok = True
        for j in range(max(len(C), len(Cm))):
            A = set(C[j]) if j < len(C) else set()
            B = {c for c in (Cm[j] if j < len(Cm) else {}) if all(height(v, p) <= h and v in set(D) for v in c)}
            if A != B: ok = False
        res[k] = ok
    return res

if __name__ == '__main__':
    which, K0, K1, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    Sf, m = (S11, 11) if which == '11' else (S5, 5)
    rows = []
    for k in range(K0, K1 + 1):
        t = time.time(); r = row(Sf, m, k); r['sec'] = round(time.time() - t, 2); rows.append(r)
        json.dump(rows, open(out, 'w'))

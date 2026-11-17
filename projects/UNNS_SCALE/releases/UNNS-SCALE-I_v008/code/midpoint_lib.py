"""v008: exact coordinates and necessary conditions for (+-|+-) routes.
Route data (N,q | M,r).  N | Bn, q^2 | Bn(N+1)^2/N, q>=2;  M | B(n+1), r^2 | B(n+1)(M+1)^2/M, r>=2.
Coordinates: v=gcd(N,n), d=N/v (d | B), v'=n/v;  rho=(N+1)/q = P/Q lowest terms.
Midpoint:  z = B n (N+1)^2 (q-1)/(N q^2) = B n rho (N+1-rho)/N."""
import sys, os, math
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction
from exact_lib import factor, _divisors

def all_pairs(B, m):
    """brute: all (N,q) for the number x=B*m (complete divisor enumeration of x and of x1)."""
    x = B * m; fx = factor(x); out = []
    for N in _divisors(fx):
        x1 = x // N * (N + 1) ** 2; f1 = dict(fx)
        for p, e in factor(N).items():
            f1[p] = f1.get(p, 0) - e
            if f1[p] == 0: del f1[p]
        for p, e in factor(N + 1).items(): f1[p] = f1.get(p, 0) + 2 * e
        for q in _divisors(f1, cap=lambda e: e // 2):
            if q >= 2: out.append((N, q))
    return out

def coord_pairs(B, m):
    """independent enumeration through the coordinates (d,v,s,Q): d|B, v|m, P|dv+1, Q^2 | (B/d)(m/v), gcd(P,Q)=1;  q = Q(dv+1)/P >= 2."""
    out = []
    fB = factor(B); fm = factor(m)
    for d in _divisors(fB):
        for v in _divisors(fm):
            if math.gcd(d, m // v) != 1: continue   # canonical split v = gcd(N, m)
            N = d * v; u = N + 1; vp = m // v; cof = (B // d) * vp
            fc = factor(cof)
            Qs = [Q for Q in _divisors(fc, cap=lambda e: e // 2)]
            for P in _divisors(factor(u)):
                for Q in Qs:
                    if math.gcd(P, Q) != 1: continue
                    q = Q * u // P
                    if q >= 2: out.append((N, q))
    return out

def coords(B, n, N, q):
    """return (d, v, vprime, P, Q) for a route label (N,q) at the number n (B*n side)."""
    v = math.gcd(N, n); d = N // v; vp = n // v
    rho = Fraction(N + 1, q); P, Q = rho.numerator, rho.denominator
    return d, v, vp, P, Q

def check_witness(B, n, N, q, M, r, z=None):
    """all lemmas on one route; returns dict of booleans."""
    x = B * n; y = B * (n + 1)
    ok = {}
    ok["legal"] = (x % N == 0 and y % M == 0 and q >= 2 and r >= 2 and (x // N * (N + 1) ** 2) % (q * q) == 0 and (y // M * (M + 1) ** 2) % (r * r) == 0)
    z1 = x // N * (N + 1) ** 2 // (q * q) * (q - 1); z2 = y // M * (M + 1) ** 2 // (r * r) * (r - 1)
    ok["meet"] = z1 == z2 and (z is None or z == z1)
    d, v, vp, P, Q = coords(B, n, N, q); e, w, wp, P2, Q2 = coords(B, n + 1, M, r)
    ok["coord_d_divides_B"] = B % d == 0 and B % e == 0
    ok["P_divides_u"] = (N + 1) % P == 0 and (M + 1) % P2 == 0
    ok["Q2_divides_cofactor"] = ((B // d) * vp) % (Q * Q) == 0 and ((B // e) * wp) % (Q2 * Q2) == 0
    # midpoint law  n*rho*(N+1-rho)/N = (n+1)*rho'*(M+1-rho')/M
    rho = Fraction(N + 1, q); rho2 = Fraction(M + 1, r)
    ok["midpoint_law"] = n * rho * (N + 1 - rho) / N == (n + 1) * rho2 * (M + 1 - rho2) / M
    ok["z_formula"] = z1 == B * n * rho * (N + 1 - rho) / N
    # cleared-denominator equation (reviewer's form)
    ok["cleared_eq"] = n * M * (N + 1) ** 2 * r * r * (q - 1) == (n + 1) * N * (M + 1) ** 2 * q * q * (r - 1)
    # divisibility lemma
    ok["n_divides"] = (N * Q * Q * P2 * P2 * (r - 1)) % n == 0
    ok["n1_divides"] = (M * Q2 * Q2 * P * P * (q - 1)) % (n + 1) == 0
    # integer system (Theorem L'): Bn = Q^2 a N, B(n+1) = Q'^2 a' M, S1: a P(Q(N+1)-P) = a' P'(Q'(M+1)-P'),  S2: Q'^2 a' M - Q^2 a N = B
    a_ = B * n // (N * Q * Q) if (B * n) % (N * Q * Q) == 0 else None; a2 = B * (n + 1) // (M * Q2 * Q2) if (B * (n + 1)) % (M * Q2 * Q2) == 0 else None
    ok["integer_a"] = a_ is not None and a2 is not None
    ok["S2"] = ok["integer_a"] and Q2 * Q2 * a2 * M - Q * Q * a_ * N == B
    ok["S1"] = ok["integer_a"] and a_ * P * (Q * (N + 1) - P) == a2 * P2 * (Q2 * (M + 1) - P2)
    # growth bound
    ok["growth"] = n <= N * (M + 1) ** 2 * q * q * (r - 1)
    return ok

def primes_exactly_once(m, skip):
    """primes l with l || m and l not dividing B (skip = set of primes of B)."""
    return [p for p, e in factor(m).items() if e == 1 and p not in skip]

def absorption(B, n, N, q, M, r):
    """where each prime l || n (l not | B) sits:  'N' | 'M+1' | 'r-1'  and each l || n+1:  'M' | 'N+1' | 'q-1' (all that apply)."""
    sk = set(factor(B)); res = {"n": {}, "n1": {}}
    for l in primes_exactly_once(n, sk):
        res["n"][l] = [name for name, val in (("N", N), ("M+1", M + 1), ("r-1", r - 1)) if val % l == 0]
    for l in primes_exactly_once(n + 1, sk):
        res["n1"][l] = [name for name, val in (("M", M), ("N+1", N + 1), ("q-1", q - 1)) if val % l == 0]
    return res

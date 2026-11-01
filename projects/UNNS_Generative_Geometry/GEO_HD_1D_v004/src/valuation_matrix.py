"""HD-1D v004 builder: SELECT-II valuation-displacement matrix V_A and content vectors.
R(N) = (N+1)^2/N ;  Delta_p(N) = 2 v_p(N+1) - v_p(N) ;  rows of V_A = primes dividing some N(N+1)."""
from fractions import Fraction
from select_history import factor


def delta(N):
    d = {}
    for p, e in factor(N): d[p] = d.get(p, 0) - e
    for p, e in factor(N + 1): d[p] = d.get(p, 0) + 2 * e
    return {p: v for p, v in d.items() if v}


def primes_of_alphabet(A):
    ps = set()
    for N in A:
        ps |= {p for p, _ in factor(N)} | {p for p, _ in factor(N + 1)}
    return sorted(ps)


def matrix(A):
    """V_A as a list of rows (one per prime), columns in the order of A"""
    ps = primes_of_alphabet(A); D = [delta(N) for N in A]
    return ps, [[D[j].get(p, 0) for j in range(len(A))] for p in ps]


def R(N): return Fraction((N + 1) ** 2, N)


def multiplier(A, c):
    out = Fraction(1)
    for N, k in zip(A, c): out *= R(N) ** k
    return out


def displacement(A, c):
    ps, V = matrix(A)
    return [sum(V[i][j] * c[j] for j in range(len(A))) for i in range(len(ps))]


def product_P(A, c):
    """P(c) = prod N^{c_N}"""
    out = 1
    for N, k in zip(A, c): out *= N ** k
    return out

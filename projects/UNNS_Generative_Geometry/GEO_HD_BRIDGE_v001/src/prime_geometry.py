"""HD-C0 / HD-C1: exact valuation-space geometry for SELECT-II (R(N)=(N+1)^2/N), active vs passive prime coordinates."""
from fractions import Fraction
from itertools import permutations


def vp(n, p):
    e = 0
    while n % p == 0:
        n //= p; e += 1
    return e


def factor(n):
    out = {}; p = 2
    while p * p <= n:
        while n % p == 0: out[p] = out.get(p, 0) + 1; n //= p
        p += 1
    if n > 1: out[n] = out.get(n, 0) + 1
    return out


def primes_dividing(n): return sorted(factor(n))


def active_primes(A):
    """primes dividing at least one label (the only primes that can ever be consumed)"""
    s = set()
    for N in A: s |= set(factor(N))
    return sorted(s)


def full_prime_support(A):
    s = set()
    for N in A: s |= set(factor(N)) | set(factor(N + 1))
    return sorted(s)


def delta(N, P): return tuple(2 * vp(N + 1, p) - vp(N, p) for p in P)


def passive_primes(A):
    act = set(active_primes(A))
    return [p for p in full_prime_support(A) if p not in act]


def span_rank(A, P=None):
    """rank over Q of {Delta_P(N) : N in A}"""
    P = P or full_prime_support(A)
    rows = [[Fraction(x) for x in delta(N, P)] for N in A]; r = 0
    for c in range(len(P)):
        piv = next((i for i in range(r, len(rows)) if rows[i][c] != 0), None)
        if piv is None: continue
        rows[r], rows[piv] = rows[piv], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i][c] != 0:
                f = rows[i][c] / rows[r][c]; rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        r += 1
    return r


def traj(m, w, P):
    u = tuple(vp(m, p) for p in P); out = [u]
    for N in w:
        d = delta(N, P); u = tuple(a + b for a, b in zip(u, d)); out.append(u)
    return out


def admissible_full(m, w):
    """direct integer definition: N | state at every step"""
    for N in w:
        if m % N: return False
        m = m // N * (N + 1) ** 2
    return True


def admissible_on(m, w, P):
    """admissibility tested ONLY through the valuations at primes in P: v_p(state) >= v_p(N) for p in P"""
    u = {p: vp(m, p) for p in P}
    for N in w:
        for p in P:
            if u[p] < vp(N, p): return False
        for p in P: u[p] += 2 * vp(N + 1, p) - vp(N, p)
    return True


def words(A, c):
    base = []
    for N, k in zip(A, c): base += [N] * k
    return sorted(set(permutations(base)))

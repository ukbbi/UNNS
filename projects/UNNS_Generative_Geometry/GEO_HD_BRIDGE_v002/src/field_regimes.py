"""G2-C/D: the FIELD-I collective map C(x) = x + L^2/G on its integer regime I (G = 1, equivalently 4 | x).
Frozen definition (src/frozen/geo1lib.py): D(x)={d>=2: d^2|a, d=1 mod b}, L=lcm D, G=gcd{d-1}, C(x)=x+L^2/G.
For an integer x: D(x) = divisors >= 2 of sigma(x) = prod p^floor(v_p/2); x = sigma^2 t with t squarefree.  If sigma is even
(<=> 4 | x) then 2 in D, G = 1, L = sigma and  C(x) = sigma^2 (t+1):   t -> sqf(t+1), sigma -> sigma * u where t+1 = u^2 sqf(t+1).
This is an exact reduction (Theorem B2-T6); everything below is computed from the pair (sigma, t)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frozen'))
from geo1lib import factor, divisors_from, Cstep

RIGID_T = (1, 2, 3)


def split(x):
    """x = sigma^2 * t, t squarefree."""
    f = factor(x); s = 1; t = 1
    for p, e in f.items():
        s *= p ** (e // 2)
        if e % 2:
            t *= p
    return s, t


def sqf_split(n):
    """n = u^2 * r with r squarefree -> (u, r)"""
    return split(n)


def is_regime_I(x):
    return int(x) == x and x >= 4 and x % 4 == 0


def next_pair(sigma, t):
    """one collective step on (sigma, t); returns (sigma', t', carry:int u) -- u>1 is a carry (L changes)."""
    u, r = split(t + 1)
    return sigma * u, r, u


def orbit_pairs(x, n):
    s, t = split(x)
    assert s % 2 == 0
    out = [(s, t, 1)]
    for _ in range(n):
        s, t, u = next_pair(s, t)
        out.append((s, t, u))
    return out


def value(pair):
    s, t = pair[0], pair[1]
    return s * s * t


def direct_orbit(x, n):
    """independent route: iterate the frozen collective step Cstep on the integer itself"""
    xs = [int(x)]
    for _ in range(n):
        y = Cstep(xs[-1])
        xs.append(int(y))
    return xs


def tau(n):
    from math import prod
    return prod(e + 1 for e in factor(n).values())


def births_at_carry(sigma, u):
    """|D(x')| - |D(x)| when sigma -> sigma*u in regime I (D(x) = Div(sigma) minus {1}); all D-members persist (monotone)."""
    return tau(sigma * u) - tau(sigma)


def entry_time_table(T):
    """e(t) = steps until t_n in {1,2,3}, for every squarefree t <= T (depends on t alone); also the reset chain length.  Uses a
    sieve for the largest square divisor.  Returns (e, resets)."""
    N = T + 5
    big = [1] * (N + 1)      # largest u with u^2 | n
    u = 2
    while u * u <= N:
        for k in range(u * u, N + 1, u * u):
            big[k] = u if u > big[k] else big[k]
        u += 1
    # largest u with u^2|n must account for composite squares: loop above takes max u (correct since u^2|n monotone in u)
    def sqf(n): return n // (big[n] ** 2)
    e = {}
    for t0 in range(1, T + 1):
        if sqf(t0) != t0:
            continue
        chain = []; t = t0
        while t not in e and t > 3:
            chain.append(t); t = sqf(t + 1)
        base = e[t] if t in e else 0          # t in {1,2,3} -> 0
        for i, c in enumerate(reversed(chain)):
            e[c] = base + i + 1
    return e


def kappa3(a):
    """least k with f^k(a) <= 3, f(a) = floor(a/4)+1  (FIELD-I v012 T72(iv))"""
    k = 0
    while a > 3:
        a = a // 4 + 1; k += 1
    return k

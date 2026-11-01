"""GEO_HD_BRIDGE v005 -- A5-T2: the STAGE SIEVE.  Exact, simulation-free description of D along a FIELD-I stage.

Setting.  x0 = a/b (lowest terms), D0 = D(x0) non-empty, L = lcm D0, G = gcd{d-1}, G = b*h  (b | G because d = 1 mod b).
FIELD-I step: x -> x + L^2/G.  While D stays equal to D0 the orbit is the progression  x_j = x0 + j L^2/G = Y_j / G,  Y_j = a*h + j*L^2.
The same formula defines the 'virtual' points x0 + j L^2/G for every j >= 0 (also after D has changed).

THEOREM (stage sieve).  For every integer j >= 0 and d >= 2:
      d in D(x0 + j L^2/G)   <=>   Q(d) | a*h + j*L^2,
      Q(d) = lcm( r(d), prod_{p | d} p^(2 v_p(d) + v_p(G)) ),   r(d) = G / gcd(d-1, G).
(gcd(L,G)=1 because every d in D0 is 1 mod G.)  Hence  d joins D at the least j >= 1 solving the LINEAR CONGRUENCE
      L^2 j = -a h  (mod Q(d)),    solvable iff gcd(L^2,Q(d)) | a h  (always, if gcd(d,L)=1).
First-event time  tau_D(x0) = min_{d not in D0} j(d)  <  infinity  for every state with D0 non-empty (take d = a prime p not dividing G L).
"""
from math import gcd, isqrt
from fractions import Fraction as Fr
from geo1lib import fibre_q, Lof, Gof, factor

def stage_data(x0):
    x0 = Fr(x0); D0 = fibre_q(x0)
    if not D0: return None
    L = Lof(D0); G = Gof(D0); a, b = x0.numerator, x0.denominator
    assert G % b == 0 and gcd(L, G) == 1
    return {'x0': x0, 'D0': tuple(D0), 'L': L, 'G': G, 'a': a, 'b': b, 'h': G // b}

_SPF = [0, 1]
def _grow(n):
    global _SPF
    if n < len(_SPF): return
    N = max(n + 1, 2 * len(_SPF)); spf = list(range(N))
    for i in range(2, isqrt(N - 1) + 1):
        if spf[i] == i:
            for j in range(i * i, N, i):
                if spf[j] == j: spf[j] = i
    _SPF = spf

def _fac(d):
    if d < 10 ** 7:
        _grow(d); f = {}
        while d > 1:
            p = _SPF[d]; f[p] = f.get(p, 0) + 1; d //= p
        return f
    return factor(d)

def Qmod(d, G):
    """Q(d) = lcm(r(d), prod_{p|d} p^(2v_p(d)+v_p(G)))"""
    r = G // gcd(d - 1, G)
    q = 1
    for p, e in _fac(d).items():
        g = 0; Gp = G
        while Gp % p == 0: Gp //= p; g += 1
        q *= p ** (2 * e + g)
    return r * q // gcd(r, q)

def solve_lin(c, rhs, m):
    """least j >= 0 with c*j = rhs (mod m), or None"""
    c %= m; rhs %= m
    g = gcd(c, m)
    if rhs % g: return None
    m2 = m // g
    return 0 if m2 == 1 else (rhs // g) * pow(c // g, -1, m2) % m2

def d_set_at(S, j):
    """D of the virtual point x0 + j L^2/G by DIRECT definition (used for validation)"""
    return fibre_q(S['x0'] + j * Fr(S['L'] ** 2, S['G']))

def sieve_j(S, d, jmin=1):
    """least j >= jmin with d in D(x0 + j L^2/G) (None if never)"""
    Q = Qmod(d, S['G']); c = S['L'] ** 2; rhs = -S['a'] * S['h']
    j0 = solve_lin(c, rhs, Q)
    if j0 is None: return None
    m2 = Q // gcd(c % Q if c % Q else Q, Q)
    j = j0
    if j < jmin: j += ((jmin - j + m2 - 1) // m2) * m2
    return j

def first_event(S, jmax):
    """tau_D and the new occurrence set, searching candidates d <= isqrt(numerator at jmax); returns None if no event with j <= jmax"""
    D0 = set(S['D0']); dmax = isqrt(S['a'] * S['h'] + jmax * S['L'] ** 2)
    best = None; arg = []
    for d in range(2, dmax + 1):
        if d in D0: continue
        j = sieve_j(S, d)
        if j is None or j > jmax: continue
        if best is None or j < best: best, arg = j, [d]
        elif j == best: arg.append(d)
    if best is None: return None
    Y = S['a'] * S['h'] + best * S['L'] ** 2
    new = sorted(d for d in range(2, isqrt(Y) + 1) if d not in D0 and Qmod(d, S['G']) and Y % Qmod(d, S['G']) == 0)
    return {'tau': best, 'new': new, 'argmin': arg}

def predicted_D(S, j):
    Y = S['a'] * S['h'] + j * S['L'] ** 2
    return sorted(d for d in range(2, isqrt(Y) + 1) if Y % Qmod(d, S['G']) == 0)


def family_candidate_time(P, ell, p_i, q):
    """closed form (A5-T2, activation family x=P^2/ell): the candidate d = p_i q joins D at step j = u - m, u = least multiple of
    M = lcm( r , q^(2+v_q(P-1)) ) exceeding m = (P-1)/ell,   r = (P-1)/gcd(p_i q - 1, P-1).   (Y_j = P^2 (m+j); p_i^2 | P^2 automatically.)"""
    N = P - 1; m = N // ell; d = p_i * q
    r = N // gcd(d - 1, N); v = 0; t = N
    while t % q == 0: t //= q; v += 1
    e = q ** (2 + v); M = r * e // gcd(r, e)
    return (m // M + 1) * M - m


def proper_divisor_block(ps, ell, q):
    """Proper-divisor obstruction (A5-T1, sufficient condition for BLOCKED, no trajectory enumeration).
    On the line x_u = P^2 u/(P-1) the proper divisor d0 | P (1<d0<P) joins D at u = least multiple of r(d0)=(P-1)/gcd(d0-1,P-1) above m
    (squarefree case t=1).  d0 is never in D(y)={P}u{p_i q}.  If the first such u is <= every A4-type joining time and < q^2 m,
    the first event contains a forbidden occurrence => y is unreachable (Lemma M).   Returns (blocked, u_forb, u_allowed)."""
    P = 1
    for p in ps: P *= p
    N = P - 1; m = N // ell
    divs = [1]
    for p in ps: divs = divs + [d * p for d in divs]
    uf = None
    for d0 in divs:
        if d0 in (1, P): continue
        r = N // gcd(d0 - 1, N)
        u = (m // r + 1) * r
        if uf is None or u < uf: uf = u
    ua = min(m + family_candidate_time(P, ell, p, q) for p in ps)
    return (uf is not None and uf <= ua and uf < q * q * m), uf, ua

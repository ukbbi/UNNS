"""G2-D/E: beyond regime I.  FIELD-I's own theory is NOT re-proved here: T49-T58 (v009) and T69-T73 (v012) describe G > 1.  This module
(i) re-checks the frozen exact eight-step orbit (FIELD-I v009 T50, G = 11) against the frozen collective step,
(ii) proves/tests the scaling-ratio obstruction (a scaling x_{n+P} = rho^2 x_n is a SELECT-II multiplier only for certain rho),
(iii) runs a finite regime census for integers outside regime I."""
import _paths  # noqa
from fractions import Fraction as Fr
from itertools import combinations_with_replacement
from geo1lib import orbit, fibre_q, Lof, Gof, Cstep


def S_k(k):
    return 2 ** 2 * 3 ** (3 + k) * 5 ** 4


def eight_step_check(K=4):
    x0 = Fr(S_k(0) ** 2, 11)
    xs = orbit(x0, 8 * K + 1)
    ok = all(Fr(xs[8 * k + j]) == Fr((j + 1) * S_k(k) ** 2, 11) for k in range(K) for j in range(8))
    ratio = all(Fr(xs[n + 8]) == 9 * Fr(xs[n]) for n in range(8 * (K - 1)))
    L = [Lof(fibre_q(Fr(x))) for x in xs]; G = [Gof(fibre_q(Fr(x))) for x in xs]
    D = [len(fibre_q(Fr(x))) for x in xs]
    carries = [n for n in range(1, len(xs)) if L[n] != L[n - 1]]
    return {'formula_ok': ok, 'x_{n+8}=9x_n': ratio, 'G_all_11': set(G) == {11}, 'L_sequence_sample': L[:3 * 8 + 1:8],
            '|D|_at_period_starts': D[:8 * K:8], 'carry_steps': carries[:K]}


def select_multipliers(maxN=60, maxl=3):
    """set of products prod R(N_i), 1 <= l <= maxl labels N_i <= maxN (as Fractions)"""
    R = {N: Fr((N + 1) ** 2, N) for N in range(1, maxN + 1)}
    out = {}
    for l in range(1, maxl + 1):
        for combo in combinations_with_replacement(range(1, maxN + 1), l):
            v = Fr(1)
            for N in combo: v *= R[N]
            out.setdefault(v, combo)
    return out


def square_multiplier_rho(maxrho=12, maxN=400, maxl=3):
    """for which rho is rho^2 a product of at most maxl SELECT-II multipliers R(N) (arithmetic only; divisibility of states ignored)?"""
    M = select_multipliers(maxN, maxl)
    return {rho: M.get(Fr(rho * rho)) for rho in range(2, maxrho + 1)}


def single_edge_square(maxN=2_000_000):
    """R(N) = rho^2 with rho an integer: N = a^2 forces a | 1 (see proof) -- scan check"""
    out = []
    from math import isqrt
    for N in range(1, maxN):
        num = (N + 1) ** 2
        if num % N == 0:
            q = num // N
            r = isqrt(q)
            if r * r == q: out.append((N, r))
    return out


def regime_census(xmax=400, cap=300):
    """integers 4 <= x <= xmax NOT in regime I with D(x) nonempty: does the orbit reach G = 1 within `cap` steps (then it is rigid from there)?"""
    rows = []
    for x0 in range(4, xmax):
        if x0 % 4 == 0: continue
        D = fibre_q(Fr(x0))
        if not D: continue
        x = Fr(x0); n = 0; hit = None
        while n < cap:
            D = fibre_q(x)
            if not D: hit = ('left_domain', n); break
            if Gof(D) == 1: hit = ('G=1', n); break
            x = x + Fr(Lof(D) ** 2, Gof(D)); n += 1
        rows.append((x0, hit))
    return rows

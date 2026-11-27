#!/usr/bin/env python3
"""ANS-I v015 finite checks. Usage: python3 -B v015_checks.py MODE
Modes: divisor crossover dickman drift balance"""
import sys, os, json
from math import gcd, isqrt, log, exp
import numpy as np
import mpmath as mp

def out(name, d):
    os.makedirs('results', exist_ok=True)
    json.dump(d, open(f'results/v015_{name}.json', 'w'), indent=1)
    print(json.dumps(d, indent=1))

def primes_upto(n):
    s = np.ones(n + 1, bool); s[:2] = False
    for q in range(2, isqrt(n) + 1):
        if s[q]: s[q*q::q] = False
    return np.nonzero(s)[0]

E_GAMMA = float(mp.exp(mp.euler))

def divisor():
    "T48a: D_{a,b}(E) equals its product form and is below prod (1-p^-(a+b))/(1-p^-a)"
    worst = 0.0; bad = 0
    for a, b in ((1.0, 1.0), (0.97, 0.97), (0.7, 0.9), (1.1, 1.1)):
        for E in range(1, 3001):
            D = 0.0; ps = []; n = E; q = 2
            while q * q <= n:
                if n % q == 0:
                    e = 0
                    while n % q == 0: n //= q; e += 1
                    ps.append((q, e))
                q += 1
            if n > 1: ps.append((n, 1))
            for d in range(1, E + 1):
                if E % d == 0:
                    t = d ** (-a)
                    for p, _ in ps:
                        if d % p == 0: t *= 1 - p ** (-b)
                    D += t
            prod = bound = 1.0
            for p, e in ps:
                prod *= 1 + (1 - p**(-b)) * sum(p**(-a*j) for j in range(1, e + 1))
                bound *= (1 - p**(-a-b)) / (1 - p**(-a))
            worst = max(worst, abs(D - prod)); bad += D > bound * (1 + 1e-12)
    out('divisor', dict(E_up_to=3000, exponent_pairs=4, max_difference_from_product_form=worst, bound_violations=bad))

def Ein(t):
    return float(mp.quad(lambda u: (1 - mp.exp(-t*u)) / u if u else t, [0, 1]))

def crossover():
    P = primes_upto(10**7).astype(float); res = {}
    for tau in (-1.0, 0.0, 0.5, 1.0, 2.0, 5.0):
        row = {}
        for X in (10**3, 10**5, 10**7):
            q = P[P <= X]; a = 1 + tau / log(X)
            row[str(X)] = float(np.exp(-np.log1p(-q**(-a)).sum()) / log(X))
        low = 1.0 if tau == 0 else (1 - exp(-tau)) / tau
        up = exp(float(mp.euler) - (0 if tau == 0 else Ein(tau)))
        res[str(tau)] = dict(lower_bound=low, upper_bound=up, prime_product_over_log=row)
    out('crossover', res)

H = 1e-5
def rho_table(umax=12.0):
    n = int(round(umax / H)); m = int(round(1 / H)); r = np.ones(n + 1)
    # u rho'(u) = -rho(u-1), trapezoidal rule
    for i in range(m + 1, n + 1):
        u0, u1 = (i - 1) * H, i * H
        r[i] = r[i-1] - H/2 * (r[i-1-m] / u0 + r[i-m] / u1)
    return r

def dickman():
    r = rho_table()
    cum = np.concatenate([[0], np.cumsum((r[1:] + r[:-1]) / 2) * H])
    I = lambda v: E_GAMMA - cum[int(round(v / H))]
    bstar = 2 / (2 + E_GAMMA); v = 1 / bstar
    closed = E_GAMMA + 1 - v * (2 - log(v))
    res = dict(integral_0_to_12=float(cum[-1]), exp_gamma=E_GAMMA, beta_star=bstar, I_at_1_over_beta_star_numeric=float(I(v)),
               I_closed_form=closed, lower_constant=1 + bstar * closed)
    b = 0.52
    res['condition_beta_I_minus_1_plus_theta_max_over_theta'] = float(max(b * I((1 - t) / b) - (1 - t) for t in np.linspace(0, b, 261)))
    res['beta_used'] = b; res['gain_at_beta_used'] = float(b * I(1 / b))
    out('dickman', res)

def smooth_flags(X, z):
    "boolean array: n<=X is z-smooth"
    rem = np.arange(X + 1, dtype=np.int64)
    for p in primes_upto(z):
        q = int(p)
        while q <= X:
            rem[q::q] //= int(p); q *= int(p)
    s = rem == 1; s[0] = False
    return s

def val(X, p):
    v = np.zeros(X + 1, np.int8); q = p
    while q <= X:
        v[q::q] += 1; q *= p
    return v

def drift():
    "sum of mu(N)(x^-X_p - 1) over the two-layer alphabet, extra letters truncated at 2*10^7"
    X = 2 * 10**7; beta = 0.52; x = 1.01; res = {}
    N = np.arange(X + 1, dtype=float); mu = N / (N + 1)**2
    for Y in (1000, 10000):
        z = int(Y ** beta); s = smooth_flags(X, z); s[:Y + 1] = False
        base = np.zeros(X + 1, bool); base[1:Y + 1] = True
        A = np.nonzero(base | s)[0]
        worst = -1e9; arg = None
        for p in primes_upto(Y + 1):
            p = int(p); W = np.zeros(len(A)); V = np.zeros(len(A)); q = p
            while q <= X + 1:
                W += (A % q == 0); V += ((A + 1) % q == 0); q *= p
            tot = float(mu[A] @ (x ** (W - 2*V) - 1))
            if tot * p > worst: worst = tot * p; arg = p
        res[str(Y)] = dict(z=z, base_mass=float(mu[1:Y+1].sum()), extra_mass_truncated=float(mu[s].sum()),
                           extra_mass_over_log_Y=float(mu[s].sum() / log(Y)), largest_p_times_drift_sum=worst, attained_at_p=arg)
    out('drift', dict(x=x, beta=beta, X=X, results=res))

def balance():
    "heuristic test: p*Pr(p | N+1) against p*Pr(p | N) for Y-smooth N<=X with weight 1/N"
    X = 2 * 10**7; res = {}
    for Y in (100, 300):
        s = smooth_flags(X, Y); A = np.nonzero(s)[0]; w = 1.0 / A; M = w.sum()
        ps = [int(p) for p in primes_upto(Y)]
        groups = {}
        for lo, hi in ((0.5, 0.7), (0.7, 0.9), (0.9, 1.0)):
            sel = [p for p in ps if Y**lo < p <= Y**hi]
            if not sel: continue
            sup = np.mean([p * w[(A + 1) % p == 0].sum() / M for p in sel])
            con = np.mean([p * w[A % p == 0].sum() / M for p in sel])
            groups[f'{lo}-{hi}'] = dict(primes=len(sel), supply_times_p=float(sup), consumption_times_p=float(con),
                                        twice_supply_minus_consumption=float(2*sup - con))
        res[str(Y)] = dict(mass_over_log_Y=float(M / log(Y)), groups=groups)
    out('balance', dict(X=X, note='truncated at X, so the tail of the smooth measure is missing', results=res))

dict(divisor=divisor, crossover=crossover, dickman=dickman, drift=drift, balance=balance)[sys.argv[1]]()

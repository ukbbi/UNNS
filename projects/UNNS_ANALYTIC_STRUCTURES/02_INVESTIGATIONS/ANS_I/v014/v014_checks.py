#!/usr/bin/env python3
"""ANS-I v014 finite checks. Usage: python3 -B v014_checks.py MODE
Modes: composition overlap roles coefficient drift model growth"""
import sys, os, json, random, itertools
from math import gcd, isqrt
import numpy as np
import mpmath as mp

def out(name, d):
    os.makedirs('results', exist_ok=True)
    json.dump(d, open(f'results/v014_{name}.json', 'w'), indent=1)
    print(json.dumps(d, indent=1))

def KE(word):
    "(K,E) built letter by letter from the grammar"
    K = E = 1
    for x in word:
        g = gcd(x, E)
        K, E = K * x // g, (x + 1) ** 2 * E // g
    return K, E

def first_letter_K(word):
    K = 1
    for x in reversed(word): K = x * K // gcd(K, (x + 1) ** 2)
    return K

def composition():
    rng = random.Random(14014); res = {}
    def letter():
        return rng.choice([rng.randint(1, 80), 2 ** rng.randint(1, 9) - rng.randint(0, 1), 3 ** rng.randint(1, 5) - 1]) or 1
    bad = bad_g = bad_K = 0; n = 100000
    for _ in range(n):
        u = [letter() for _ in range(rng.randint(0, 6))]; v = [letter() for _ in range(rng.randint(0, 6))]
        Ku, Eu = KE(u); Kv, Ev = KE(v); K, E = KE(u + v); d = gcd(Eu, Kv)
        bad += (K * d != Ku * Kv) or (E * d != Eu * Ev)
        bad_K += K != first_letter_K(u + v)
        bad_g += gcd(K, E) != gcd(Ku * Kv, Eu * Ev) // d
    res['random_pairs'] = n; res['composition_failures'] = bad
    res['source_two_recursions_disagree'] = bad_K; res['general_gcd_formula_failures'] = bad_g
    b = 0
    for x in range(1, 401):
        for y in range(1, 401):
            K, E = KE([x, y]); b += gcd(K, E) != gcd(x, (y + 1) ** 2)
    res['two_letter_gcd_pairs_up_to_400_failures'] = b
    # bicyclic form per prime, exhaustive on valuations
    b = 0
    for u1, v1, u2, v2 in itertools.product(range(9), repeat=4):
        lhs = (u1 + u2 - min(v1, u2), v1 + v2 - min(v1, u2))
        rhs = (u1 - v1 + max(v1, u2), v2 - u2 + max(v1, u2))
        b += lhs != rhs
    res['bicyclic_form_failures'] = b
    out('composition', res)

def overlap():
    import sympy as sp
    z = sp.symbols('z')
    Phi = lambda v: 1 + (1 - z) * (v // 2 + (v + 1) // 2 * z)
    c = lambda u: (z**3 if u % 2 == 0 else z**2 * (1 - z + z*z)) / (1 + z*z)
    L = lambda u, v: Phi(u) * (1 + z - z**(v + 1)) + z**v * c(u)
    L0 = L(0, 0); ok = True; lead = {}
    for u in range(7):
        for v in range(7):
            corr = (1 - z**v) * (1 + z) * (Phi(u) * c(0) - c(u)) / L0**2
            ok &= sp.simplify(L(u, v) / L0 - L(u, 0) * L(0, v) / L0**2 - corr) == 0
            if 1 <= u <= 4 and 1 <= v <= 3:
                lead[f'{u},{v}'] = str(sp.series(corr, z, 0, 4).removeO())
    out('overlap', dict(identity_u_v_up_to_6=bool(ok), correction_leading_terms=lead))

# ---------- role measures ----------
def letter_law(p, role, V):
    "list of (v_p(a), v_p(a-1), probability) for one middle letter"
    x = p ** (-2/3); y = 1 / p
    dom = [(v, (1 - x) * x**v) for v in range(1, V + 1)]
    oth = [(w, (1 - x) * y**w) for w in range(1, V + 1)]
    rest = (1 - x) * (1 - 2*y) / (1 - y)
    L = [(0, 0, rest)]
    for v, q in dom: L.append((v, 0, q) if role == 'S' else (0, v, q))
    for w, q in oth: L.append((0, w, q) if role == 'S' else (w, 0, q))
    return L

def Lnum(u, v, z):
    Phi = 1 + (1 - z) * (u // 2 + (u + 1) // 2 * z)
    c = (z**3 if u % 2 == 0 else z**2 * (1 - z + z*z)) / (1 + z*z)
    return Phi * (1 + z - z**(v + 1)) + z**v * c

def ER(p, roles, V):
    "E_R[p^(T/3)] with the two end letters summed in closed form"
    z = p ** (-1/3); mid = roles[1:-1]
    if not mid: return Lnum(0, 0, z)
    laws = [letter_law(p, r, V) for r in mid]
    tot = 0.0
    for state in itertools.product(*laws):
        pr = 1.0; K = E = 0                      # p-adic composition of the middle word
        for va, vx, q in state:
            m = min(E, vx); K, E = K + vx - m, E + 2*va - m; pr *= q
        W = sum(2*s[0] for s in state) - E
        tot += pr * p ** (W / 3) * Lnum(K, E, z)
    return tot

def ER_brute(p, roles, V):
    "same expectation from the path formula for the total gcd, all letters enumerated"
    k = len(roles); laws = [letter_law(p, r, V) for r in roles]; tot = 0.0
    for state in itertools.product(*laws):
        pr = 1.0; T = 0; A = 0
        for i, (va, vx, q) in enumerate(state):
            if i > 0: T = min(T + vx, A)
            A += 2*va; pr *= q
        tot += pr * p ** (T / 3)
    return tot

def vmax(p): return max(8, int(np.ceil(16 * np.log(10) / ((1/3) * np.log(p)))))

def roles():
    res = {}; worst2 = worst3 = worstb = 0
    for p in (2, 3, 5, 7, 11, 101):
        z = p ** (-1/3); x = z*z; y = 1/p; V = min(vmax(p), 140)
        L0 = (1 + z*z + z**3) / (1 + z*z); H = 1 - (z**5 + z**6) / (1 + z*z)
        worst2 = max(worst2, abs((1 - y) * ER(p, 'SR', V) - H))
        w = lambda u, v: Lnum(u, v, z) / L0
        W1 = lambda t: sum(w(j, 0) * t**j for j in range(V + 1))
        W2 = lambda t: sum(w(0, 2*j) * t**j for j in range(V + 1))
        E1 = (1-y)*(1-x)*W1(x) + (1-x)*((1-y)*W2(y) - 1)
        E2 = (1-y)*(1-x)*W2(x) + (1-x)*((1-y)*W1(y) - 1)
        worst3 = max(worst3, abs((1-y)**2 * ER(p, 'SRR', V) - H*E1), abs((1-y)**2 * ER(p, 'SSR', V) - H*E2))
    for p in (11, 101):
        V = 14 if p == 11 else 9
        for R in ('SR', 'SRR', 'SSR', 'SSRR'):
            worstb = max(worstb, abs(ER_brute(p, R, V) - ER(p, R, V)))
    res['k2_identity_max_error'] = worst2; res['k3_identity_max_error'] = worst3
    res['closed_form_vs_path_formula_enumeration_max_difference'] = worstb
    tab = {}
    for k in (2, 3, 4, 5):
        for mid in itertools.product('SR', repeat=k - 2):
            R = 'S' + ''.join(mid) + 'R'
            L = sum(1 for i in range(k) for j in range(i+1, k) if R[i] == 'S' and R[j] == 'R')
            vals = {}
            for p in ((101, 1009, 10007) if k < 5 else (1009, 10007)):
                V = 14 if p == 101 else (10 if p == 1009 else 8)
                if k == 5: V = 7
                vals[str(p)] = (ER(p, R, V) - 1 - L / p) * p ** (4/3)
            tab[R] = dict(links=L, scaled_remainder=vals)
    res['E_minus_1_minus_links_over_p_times_p_4_3'] = tab
    out('roles', res)

def coefficient():
    "C_R = prod_p (1-1/p)^L E_R for the maximal assignments; predicted leading coefficients"
    z3 = float(mp.zeta(mp.mpf(2)/3)); res = {}
    primes = [p for p in range(2, 20001) if all(p % q for q in range(2, isqrt(p) + 1))]
    for k, Rs in ((2, ['SR']), (3, ['SRR', 'SSR']), (4, ['SSRR'])):
        L = k*k//4
        cuts = (500, 2000, 8000) if k == 4 else (1000, 4000, 20000)
        data = {}
        for R in Rs:
            logs = []; 
            for p in primes:
                if p > cuts[-1]: break
                V = min(vmax(p), 90 if k == 4 else 120)
                if k == 4 and p > 100: V = 24 if p < 1000 else 14
                logs.append((p, L*np.log1p(-1/p) + np.log(ER(p, R, V))))
            data[R] = logs
        row = {}
        for cut in cuts:
            tot = 0.0
            for R in Rs:
                use = [(p, v) for p, v in data[R] if p <= cut]
                # tail model c4 p^(-4/3) + c5 p^(-5/3), fitted on the largest primes used
                fit = use[-40:]
                M = np.array([[p**(-4/3), p**(-5/3)] for p, _ in fit]); b = np.array([v for _, v in fit])
                c = np.linalg.lstsq(M, b, rcond=None)[0]
                tail = c[0]*(float(mp.primezeta(mp.mpf(4)/3)) - sum(p**(-4/3) for p, _ in use)) \
                     + c[1]*(float(mp.primezeta(mp.mpf(5)/3)) - sum(p**(-5/3) for p, _ in use))
                tot += np.exp(sum(v for _, v in use) + tail)
            row[str(cut)] = z3**k * 3.0**(-L) * tot
        res[f'k{k}_predicted_leading_coefficient_by_prime_cutoff'] = row
    res['k2_proved_value_zeta23^2_H13_over_3_up_to_2e4'] = float(z3**2/3*np.exp(sum(np.log1p(-(p**(-5/3)+p**(-2.0))/(1+p**(-2/3))) for p in primes)))
    res['k3_value_recorded_in_v012'] = -0.759163915931851
    out('coefficient', res)

def drift():
    "E[x^(-X_p)] for letters N<=L with weight (N/(N+1)^2)^s, x=21/20"
    x = 21/20; Lmax = 200000
    N = np.arange(1, Lmax + 2, dtype=np.int64)
    worst = {}
    primes = [p for p in range(2, 200) if all(p % q for q in range(2, isqrt(p) + 1))] + [1009, 10007, 199999]
    for s in (0.51, 0.75, 1.0):
        f = (N[:-1] / (N[:-1] + 1.0)**2) ** s; B = np.cumsum(f); m = -1e9; arg = None
        v = np.zeros(Lmax + 2, dtype=np.int8)
        for p in primes:
            v[:] = 0; pk = p
            while pk <= Lmax + 1: v[pk::pk] += 1; pk *= p
            Xp = 2*v[2:Lmax + 2].astype(float) - v[1:Lmax + 1]
            exc = np.cumsum(f * (x ** (-Xp) - 1)) / B       # E[x^-X] - 1 for every L
            i = 3 + int(np.argmax(exc[3:]))                  # L >= 4
            if exc[i] > m: m = float(exc[i]); arg = [p, i + 1]
        worst[str(s)] = dict(largest_E_minus_1_over_L_from_4=m, attained_at_p_L=arg)
    out('drift', dict(x='21/20', L_up_to=Lmax, primes_tested=len(primes), results=worst))

def model():
    "the same formula for the order-rt model F_{2,2} (independent letters)"
    primes = [p for p in range(2, 20001) if all(p % q for q in range(2, isqrt(p) + 1))]
    def E(p, V):
        x = p**(-2/3); two = np.convolve((1-x)*x**np.arange(V), (1-x)*x**np.arange(V))
        i = np.arange(len(two)); return two @ (p**(np.minimum.outer(2*i, i)/3.0)) @ two
    logs = [(p, 4*np.log1p(-1/p) + np.log(E(p, 200 if p < 10 else (80 if p < 200 else 24)))) for p in primes]
    row = {}
    for cut in (1000, 4000, 20000):
        use = [t for t in logs if t[0] <= cut]; fit = use[-40:]
        M = np.array([[p**(-4/3), p**(-5/3)] for p, _ in fit]); c = np.linalg.lstsq(M, np.array([v for _, v in fit]), rcond=None)[0]
        tail = c[0]*(float(mp.primezeta(mp.mpf(4)/3)) - sum(p**(-4/3) for p, _ in use)) + c[1]*(float(mp.primezeta(mp.mpf(5)/3)) - sum(p**(-5/3) for p, _ in use))
        row[str(cut)] = float(mp.zeta(mp.mpf(2)/3))**4 / 81 * np.exp(sum(v for _, v in use) + tail)
    out('model', dict(F22_role_formula_by_prime_cutoff=row, F22_value_recorded_in_v013=0.0068448))

def growth():
    "finite illustrations of the proof steps for G_k(1); not a verification of the asymptotics"
    res = {}
    # composition inequality G_2 >= G_1^2 on a truncated alphabet
    for L in (10, 100, 1000):
        G1 = sum(1/(N+1)**2 for N in range(1, L+1))
        G2 = sum(gcd((a+1)**2, b) / ((a+1)**2 * (b+1)**2) for a in range(1, L+1) for b in range(1, L+1))
        res[f'truncated_L{L}'] = dict(G1=G1, G2=G2, G2_ge_G1_squared=G2 >= G1*G1)
    # divisor-sum constant C(eps) = prod_p max(1, (1-p^-a)^-1 p^-eps)
    N = 4_000_000; sieve = np.ones(N+1, bool); sieve[:2] = False
    for q in range(2, isqrt(N)+1):
        if sieve[q]: sieve[q*q::q] = False
    P = np.nonzero(sieve)[0].astype(float); tab = {}
    for k in (10, 100, 1000, 10000):
        eps = 1/(k*np.log(k)**2); a = 1 - k*eps
        t = -np.log1p(-P**(-a)) - eps*np.log(P)
        lim = min(N, 1/eps)
        logC = t[(P <= lim) & (t > 0)].sum()
        tab[str(k)] = dict(eps=eps, primes_summed_up_to=lim, C_partial=float(np.exp(logC)), C_over_log_inverse_eps=float(np.exp(logC)/np.log(lim)))
    res['divisor_constant'] = tab; res['exp_gamma'] = float(mp.exp(mp.euler))
    out('growth', res)

dict(composition=composition, overlap=overlap, roles=roles, coefficient=coefficient, drift=drift, model=model, growth=growth)[sys.argv[1]]()

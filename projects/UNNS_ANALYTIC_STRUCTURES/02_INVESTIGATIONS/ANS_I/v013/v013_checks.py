#!/usr/bin/env python3
"""ANS-I v013 finite checks. Usage: python3 -B v013_checks.py MODE
Modes: recursion local numeric roles model margins"""
import sys, os, json, random, itertools
from math import gcd, comb
from fractions import Fraction as Q
import numpy as np
import mpmath as mp

def out(name, d):
    os.makedirs('results', exist_ok=True)
    json.dump(d, open(f'results/v013_{name}.json', 'w'), indent=1)
    print(json.dumps(d, indent=1))

def EK(word):
    "endpoint (grammar order) and minimal source K (first-letter recursion)"
    E = 1
    for x in word:
        E = (x + 1) ** 2 * E // gcd(x, E)
    K = 1
    for x in reversed(word):
        K = x * K // gcd(K, (x + 1) ** 2)
    return E, K

def recursion():
    res = {}
    def test(w):
        x1, mu, P = w[0], w[1:-1], w[-1]
        E, _ = EK(w); Em, Km = EK(mu)
        a, d = x1 + 1, P + 1
        g = gcd(P, Em); h = gcd(P * Km // g, a * a)
        prod = 1
        for x in mu: prod *= (x + 1) ** 2
        G = prod // Em
        pm = 1
        for x in mu: pm *= x
        return E * g * h == (a * d) ** 2 * Em and pm % G == 0 and pm // G == Km
    for k, T in ((3, 30), (4, 14), (5, 7)):
        n = bad = 0
        for w in itertools.product(range(1, T + 1), repeat=k):
            n += 1; bad += not test(w)
        res[f'exhaustive_k{k}_T{T}'] = [n, bad]
    rng = random.Random(13013)
    for k in (4, 5, 6, 8, 12):
        bad = 0
        for _ in range(20000):
            w = [rng.choice([rng.randint(1, 60), 2 ** rng.randint(1, 10) - rng.randint(0, 1),
                             3 ** rng.randint(1, 6) - 1]) or 1 for _ in range(k)]
            bad += not test(w)
        res[f'random_k{k}'] = [20000, bad]
    out('recursion', res)

def Phi(v, z): return 1 + (1 - z) * (v // 2 + (v + 1) // 2 * z)
def cc(u, z): return (z**3 if u % 2 == 0 else z**2 * (1 - z + z * z)) / (1 + z * z)
def L(u, v, z): return Phi(u, z) * (1 + z - z**(v + 1)) + z**v * cc(u, z)

def local():
    mx = 0; mphi = 0
    pts = [(2, 1.5), (3, 0.8 + 2j), (5, 0.6), (7, 0.45 - 1j)]
    for p, s in pts:
        z = p ** (-s)
        for v in range(0, 11):
            ser = sum((1 if j == 0 else p**(j*s) - p**((j-1)*s)) * p**(-2*s*((j+1)//2)) for j in range(v+1))
            mphi = max(mphi, abs(ser - Phi(v, z)))
        for u in range(9):
            for v in range(9):
                f = lambda j: p**(s*min(j, v)) * Phi(u + j - min(j, v), z)
                tot = f(0); prev = f(0); j = 1
                while j < 400:
                    t = z ** (2 * j)
                    if abs(t) < 1e-18 and j > v + 2: break
                    cur = f(j); tot += (cur - prev) * t; prev = cur; j += 1
                mx = max(mx, abs(tot - L(u, v, z)))
    import sympy as sp
    Z = sp.symbols('z'); L0 = (1 + Z**2 + Z**3) / (1 + Z**2)
    w1 = (1 + Z + Z**2) / (1 + Z**2 + Z**3)
    single = {name: sp.simplify(L(u, v, Z) / L0 - w1) == 0 for name, u, v in (('K only', 1, 0), ('E only', 0, 2))}
    old = all(sp.simplify(L(0, 2*b, Z) - (1 + Z - Z**(2*b+1)/(1+Z**2))) == 0 for b in range(1, 6))
    old1 = all(sp.simplify(L(m, 0, Z) - (Phi(m, Z) + cc(m, Z))) == 0 for m in range(1, 6))
    out('local', dict(Phi_max_error=float(mphi), L_max_error=float(mx), L00_is_L0=sp.simplify(L(0,0,Z)-L0) == 0,
        single_state_weights_equal_w=single, reduces_to_v011_w2=old, reduces_to_v011_w1=old1))

def hz(s, a): return float(mp.zeta(s, a))

def numeric():
    s = 2.0; res = {}
    # truncated identity G_4 = zeta(2s) * sum_{mu,P} E(mu P)... - G_3, letters of mu,P <= T
    rows = []
    z2 = hz(2*s, 1)
    for T in (20, 40, 80):
        x = np.arange(1, T+1, dtype=np.int64); a2 = (x+1)**2; fa = (x+1.0)**(-2*s)
        M, N = np.meshgrid(x, x, indexing='ij'); b2 = (M+1)**2
        g = np.gcd(N, b2); Em = b2 * (N+1)**2 // g; Km = M * N // g
        # Phi table
        top = int((Km.max()) * T) + 1
        phi = np.ones(top); 
        for p in range(2, top):
            if all(p % q for q in range(2, int(p**.5)+1)):
                zz = p ** (-s); pk = p; v = 1; prev = 1.0
                while pk < top:
                    cur = Phi(v, zz); phi[pk::pk] *= cur / prev; prev = cur; pk *= p; v += 1
        inner = 0.0; g3 = 0.0; g4 = 0.0
        base = Em.astype(float)**(-s)
        for P in range(1, T+1):
            g1 = np.gcd(P, Em); K = P * Km // g1
            d = (P+1.0)**(-2*s)
            inner += d * np.sum(base * g1**float(s) * phi[K])
            g3 += d * np.sum(base * g1**float(s))
            for i, A in enumerate(a2):
                h = np.gcd(K, A)
                g4 += d * fa[i] * np.sum(base * (g1 * h)**float(s))
        rows.append(dict(T=T, difference=g4 - (z2 * inner - g3), G4_truncated=g4))
        del phi
    res['truncated_identity_s2'] = rows
    # last-letter identity for selected middle words
    s = 1.5; z2 = hz(2*s, 1); worst = 0
    def fac(n):
        r = {}; p = 2
        while p*p <= n:
            while n % p == 0: r[p] = r.get(p, 0)+1; n //= p
            p += 1
        if n > 1: r[n] = r.get(n, 0)+1
        return r
    primes = [p for p in range(2, 200000) if all(p % q for q in range(2, int(p**.5)+1))]
    logL0 = sum(np.log((1+p**(-2*s)+p**(-3*s))/(1+p**(-2*s))) for p in primes)
    P = np.arange(1, 400001, dtype=np.int64)
    mus = [(1, 1), (2, 3), (3, 2), (4, 1), (1, 2), (8, 3), (5, 7), (2, 2, 5)]
    for mu in mus:
        E, K = EK(mu)
        g = np.gcd(P, E); Kn = K * P // g
        top = int(Kn.max()) + 1
        fPhi = np.ones(len(P)); rem = Kn.copy()
        for p in primes:
            if p*p > top: break
            m = rem % p == 0
            if not m.any(): continue
            v = np.zeros(len(P), dtype=np.int64)
            while m.any():
                rem[m] //= p; v[m] += 1; m = rem % p == 0
            zz = p**(-s); tab = np.array([Phi(i, zz) for i in range(v.max()+1)]); fPhi *= tab[v]
        big = rem > 1; zz = rem[big].astype(float)**(-s); fPhi[big] *= 1 + (1-zz)*zz
        lhs = float(np.sum((P+1.0)**(-2*s) * g**s * fPhi))
        fE, fK = fac(E), fac(K); prod = np.exp(logL0)
        for p in set(fE) | set(fK):
            zz = p**(-s); prod *= L(fK.get(p, 0), fE.get(p, 0), zz) / L(0, 0, zz)
        # Delta part: sum_k Lambda(k) k^{-2s} Delta(s,k)
        N = 4000
        f = np.zeros(N+1)
        K1 = np.arange(1, N+1, dtype=np.int64)
        f[1:] = np.gcd(K1, E)**s * fPhi[:N]
        mu_ = np.ones(N+1); comp = np.zeros(N+1, bool)
        for p in primes:
            if p > N: break
            comp[2*p::p] = True; mu_[p::p] *= -1; mu_[p*p::p*p] = 0
        Lam = np.zeros(N+1); phi1 = f.copy()
        phiK = 1.0
        for p, e in fK.items(): phiK *= Phi(e, p**(-s))
        for d in range(1, N+1):
            if mu_[d]: Lam[d::d] += mu_[d] * f[1:N//d+1]
        zs = float(mp.zeta(2*s))
        D = np.array([0.0] + [float(mp.zeta(2*s, 1+mp.mpf(1)/k) - zs) for k in range(1, N+1)])
        k = np.arange(1, N+1)
        dpart = float(np.sum(Lam[1:] * k**(-2*s) * D[1:]))
        rhs = zs * prod + dpart
        worst = max(worst, abs(lhs - rhs))
        res.setdefault('last_letter_s1.5', []).append(dict(mu=list(mu), E=E, K=K, lhs=lhs, rhs=float(rhs), diff=lhs-float(rhs)))
    res['last_letter_worst'] = worst
    out('numeric', res)

def roles():
    res = []
    for k in range(2, 17):
        best = -1; arg = []
        for mid in itertools.product('SR', repeat=k-2):
            r = ('S',) + mid + ('R',)
            c = 0; ns = 0
            for ch in r:
                if ch == 'S': ns += 1
                else: c += ns
            if c > best: best, arg = c, [''.join(r)]
            elif c == best: arg.append(''.join(r))
        res.append(dict(k=k, max_links=best, floor=k*k//4, maximisers=arg))
    k4 = {''.join(('S',) + m + ('R',)): [f'{i+1}{j+1}' for i in range(4) for j in range(i+1, 4)
          if (('S',)+m+('R',))[i] == 'S' and (('S',)+m+('R',))[j] == 'R'] for m in itertools.product('SR', repeat=2)}
    out('roles', dict(table=res, depth4=k4))

def model():
    from math import isqrt
    res = {}
    s = 1.5; z2 = hz(2*s, 1)
    primes = [p for p in range(2, 5000) if all(p % q for q in range(2, isqrt(p)+1))]
    D = 3000
    spf = [0]*(D+1)
    for p in range(2, D+1):
        if spf[p] == 0:
            for m in range(p, D+1, p):
                if spf[m] == 0: spf[m] = p
    def fac(n):
        r = {}
        while n > 1:
            p = spf[n]
            while n % p == 0: r[p] = r.get(p, 0)+1; n //= p
        return r
    from functools import lru_cache
    @lru_cache(None)
    def gl(r, p, e):
        z = p**(-s); tot = 0.0; j = 0
        while True:
            t = comb(e+j+r-1, r-1) * z**(2*j); tot += t; j += 1
            if t < 1e-17: break
        return tot * (1-z*z)**r
    J = [0.0]*(D+1); Ar = {1: [0.0]*(D+1), 2: [0.0]*(D+1)}
    fs = [None] + [fac(d) for d in range(1, D+1)]
    for d in range(1, D+1):
        v = 1.0; rho = 1; a1 = 1.0; a2 = 1.0
        for p, e in fs[d].items():
            v *= p**(e*s) - p**((e-1)*s); h = (e+1)//2; rho *= p**h
            a1 *= gl(1, p, h); a2 *= gl(2, p, h)
        J[d] = v; Ar[1][d] = rho**(-2*s)*a1; Ar[2][d] = rho**(-2*s)*a2
    def qterm(h, q):
        v = q**(-2*s)
        for p, e in fs[q].items(): v *= gl(h, p, e)
        return v
    qt = {h: np.array([0.0] + [qterm(h, q) for q in range(1, D+1)]) for h in (1, 2)}
    d = np.arange(1, D+1)
    for r, t in ((1, 1), (1, 2), (2, 2)):
        w = np.array(J[1:]) * np.array(Ar[r][1:])
        total = z2**(r+t) * float(np.sum(w * qt[t][d]))
        Y = 150
        y = np.arange(1, Y+1); dl = (y+1.0)**(-2*s) - y**(-2.0*s)
        for i in range(1, t+1):
            h = t - i; acc = 0.0
            if i == 1:
                for yy in range(1, Y+1):
                    if h == 0:
                        v = float(np.sum(w[(yy % d) == 0]))
                    else:
                        v = float(np.sum(w * qt[h][d // np.gcd(d, yy)]))
                    acc += dl[yy-1] * v
            else:   # i = 2, h = 0
                cache = {}
                for y1 in range(1, Y+1):
                    for y2 in range(1, Y+1):
                        n = y1*y2
                        if n not in cache:
                            m = d[:min(n, D)]; cache[n] = float(np.sum(w[:len(m)][(n % m) == 0]))
                        acc += dl[y1-1]*dl[y2-1]*cache[n]
            total += comb(t, i) * z2**(r+t-i) * acc
        # direct truncated sums at increasing cut-offs
        direct = {}
        for T in {2: (500, 1000, 2000), 3: (75, 150, 300), 4: (18, 35, 70)}[r+t]:
            x = np.arange(1, T+1, dtype=np.int64)
            wx = (x+1.0)**(-2*s); wa = x**(-2.0*s)
            def fold(k, wt):
                if k == 1: return x, wt
                n = np.multiply.outer(x, x).ravel(); nw = np.multiply.outer(wt, wt).ravel()
                u, inv = np.unique(n, return_inverse=True); return u, np.bincount(inv.ravel(), weights=nw)
            n, nw = fold(r, wa); m, mw = fold(t, wx)
            direct[str(T)] = total - sum(ww * float(np.sum(mw * np.gcd(m, nn*nn)**s)) for nn, ww in zip(n, nw))
        res[f'r{r}_t{t}'] = dict(formula=total, formula_minus_direct_by_letter_cutoff=direct)
    # local factor expansion and leading coefficient
    import sympy as sp
    Z = sp.symbols('z'); N = 5
    def gs(r, e):
        return sum(comb(e+j+r-1, r-1)*Z**(2*j) for j in range(4))*(1-Z**2)**r
    exp = {}
    for r, t in ((1, 1), (1, 2), (2, 2), (2, 3)):
        tot = 1
        for v in range(1, 6):
            h = (v+1)//2
            tot += Z**(2*h+v) * (1-Z) * gs(r, h) * gs(t, v)   # J(p^v) = z^{-v}(1-z)
        ser = sp.Poly(sp.expand(tot), Z)
        exp[f'r{r}_t{t}'] = [int(ser.coeff_monomial(Z**i)) for i in range(5)]
    res['local_factor_coefficients_z0_to_z4'] = exp
    z3 = float(mp.zeta(mp.mpf(2)/3))
    M = 12
    def poly(r, e):
        return sum(comb(e+j+r-1, r-1)*Z**(2*j) for j in range(M//2+1))*(1-Z**2)**r
    tot = 1
    for v in range(1, M):
        h = (v+1)//2
        if 2*h+v <= M+1: tot += Z**(2*h+v)*(1-Z)*poly(2, h)*poly(2, v)
    tot = sp.Poly(sp.expand(tot), Z)
    tr = sum(tot.coeff_monomial(Z**i)*Z**i for i in range(M))
    logser = sp.series(sp.log(tr) + 4*sp.log(1-Z**3), Z, 0, 10).removeO()
    b = {n: float(logser.coeff(Z, n)) for n in range(1, 10)}
    lead = {}
    for cut in (10**3, 10**4, 10**5):
        sieve = np.ones(cut+1, bool); sieve[:2] = False
        for p in range(2, isqrt(cut)+1):
            if sieve[p]: sieve[p*p::p] = False
        ps = np.nonzero(sieve)[0].astype(float); z = ps**(-1/3)
        acc = np.ones_like(z)
        g2 = lambda e: sum((e+j+1)*z**(2*j) for j in range(80))*(1-z*z)**2
        for v in range(1, 60):
            h = (v+1)//2
            acc += z**(2*h+v) * (1-z) * g2(h) * g2(v)
        lf = 4*np.log1p(-1/ps) + np.log(acc)
        corr = sum(b[n]*(float(mp.primezeta(mp.mpf(n)/3)) - float(np.sum(z**n))) for n in range(4, 10))
        lead[str(cut)] = float(z3**4 / 81 * np.exp(np.sum(lf) + corr))
    res['log_factor_coefficients_z1_to_z9'] = b
    res['F22_leading_coefficient_at_one_third_by_prime_cutoff'] = lead
    out('model', res)

def margins():
    d = Q(1, 200); tau = Q(1, 14); Kx = Q(7, 4); h = Q(6, 5); hc = Q(6); th1 = Q(3, 4); th2 = Q(2, 25)
    checks = {}
    def need(name, val): checks[name] = checks.get(name, True) and bool(val)
    for sg in (Q(1,3)-d, Q(1,3), Q(1,3)+d):
        half = Q(1, 2)
        need('P bounded: sigma>3/10', sg > Q(3, 10))
        need('lemma range', Q(1,4) < sg < half)
        need('R domain', sg > Q(2,7))
        need('F1', half > 3*d)
        need('moment F p', (-2*sg+tau)*h - 1 < -1)
        need('moment F p^j', 2*((sg+tau)*h-1) < -1 and (sg+tau)*h < 1)
        need('moment G p', (-2*sg+tau)*hc - 1 < -1)
        need('moment G p^2', 2*tau*hc - 2 < -1)
        for j in range(3, 40): need('moment G p^j', (2-j)*sg*hc + j*tau*hc - j < -1)
        need('moment G slope', hc*(tau-sg) - 1 < 0)
        need('S dyadic', 1 - 3*sg - tau/(2*Kx+1) < 0)
        need('S second part', 2*sg - 6*Kx*d > half)
        for th, (ea, eb, em) in ((th1, (half-3*sg-Kx*sg*(1-th1), -2*sg-Kx*sg*(1-th1), half-4*sg-sg*th1)),
                                 (th2, (-2*sg-Kx*sg*(1-th2), -Kx*sg*(1-th2), -3*sg-sg*th2))):
            need('A/B table a,b', ea < -half and eb < -half); need('A/B table m', em < -1)
        need('B shift 1', -2*sg-1 < -half and -sg-1 < -1)
        need('B shift 2', -Kx*sg*(1-th2) < -half and -2*sg-1-Kx*sg*(1-th2) < -half and -3*sg-1-sg*th2 < -1)
        need('B shift 3', -2*sg-1 < -half and -3*sg-1 < -1)
        need('principal', -1+3*Kx*d < -half and -2*sg+3*Kx*d < -half and -sg-1+3*d < -1)
        need('lemma applies (K>=1)', Kx >= 1)
    need('half-plane step tau=0', (-2*Q(1,3))*h-1 < -1 and 2*(Q(1,3)*h-1) < -1)
    # the UNNS Research Collective's proposed pair, with the original K and Hoelder exponents
    d7, t7 = Q(1,700), Q(1,25)
    owner = dict(moment_F=bool(Q(1,3)+d7+t7 < Q(3,8)), dyadic=bool(3*d7 < t7/9), moment_G=bool(8*t7-2 < -1))
    # exact left side of the dyadic inequality in v012
    v012 = str(Q(1,500) - Q(1,432))
    out('margins', dict(delta=str(d), tau=str(tau), K=str(Kx), holder=[str(h), str(hc)], theta=[str(th1), str(th2)],
        all_hold=all(checks.values()), checks=checks, review_pair_1_700=owner, v012_dyadic_exponent=v012))

dict(recursion=recursion, local=local, numeric=numeric, roles=roles, model=model, margins=margins)[sys.argv[1]]()

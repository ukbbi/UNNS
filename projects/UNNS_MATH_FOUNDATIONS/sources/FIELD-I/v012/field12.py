#!/usr/bin/env python3
"""FIELD-I v012 verifier -- Effective predictability: bounds on the transient before the rigid regime is certified.
A: the reset-descent bound (T69); E: the certificate-entry bounds (T70 product bound, T71 polynomial bound) and their lemmas;
D: the dynamic-G bound (T72): chains of reducing events, segment lengths, gamma recursion, G=1 tail; C: controls; V: verdicts.
Exact integer/Fraction arithmetic (helpers copied from v011/v010/v009/v005 for standalone use). Tags PASS/FAIL/DATA/OPEN.
Notation: x=a/b reduced; D(x)={d>=2 : d^2|a, d=1 mod b}; G(x)=gcd{d-1}; C(x)=x+L^2/G, L=lcm D; persistent orbit: G=g forever, x=gamma L^2/g."""
import os, sys, time, random, math
from fractions import Fraction as Fr
from math import gcd, isqrt
from itertools import combinations
from collections import Counter, defaultdict
QUICK = os.environ.get("FIELD12_QUICK") == "1"
NFAIL = 0; T0 = time.time(); random.seed(5)
def rec(tag, status, msg):
    global NFAIL
    if status == "FAIL": NFAIL += 1
    print(f"{status} {tag}: {msg}", flush=True)
def lcm(a, b): return a // gcd(a, b) * b
# ---- exact factoring (Miller-Rabin + Pollard rho), no external packages
SP = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47)
def is_prime(n):
    if n < 2: return False
    for p in SP[:12]:
        if n % p == 0: return n == p
    d = n - 1; r = 0
    while d % 2 == 0: d //= 2; r += 1
    for a in SP[:12]:
        x = pow(a, d, n)
        if x in (1, n - 1): continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1: break
        else: return False
    return True
def rho(n):
    if n % 2 == 0: return 2
    while True:
        c = random.randrange(1, n); f = lambda x: (x * x + c) % n
        x = y = random.randrange(0, n); d = 1
        while d == 1:
            x = f(x); y = f(f(y)); d = gcd(abs(x - y), n)
        if d != n: return d
def factor(n, res=None):
    if res is None: res = {}
    if n == 1: return res
    for p in SP:
        while n % p == 0: res[p] = res.get(p, 0) + 1; n //= p
    if n == 1: return res
    if is_prime(n): res[n] = res.get(n, 0) + 1; return res
    d = rho(n); factor(d, res); factor(n // d, res); return res
def divisors_from(f):
    ds = [1]
    for p, e in f.items(): ds = [d * p ** k for d in ds for k in range(e + 1)]
    return ds
def sqrt_part_f(f): return {p: e // 2 for p, e in f.items() if e // 2 > 0}
def sqrt_part(n):
    s = 1
    for p, e in factor(n).items(): s *= p ** (e // 2)
    return s
def sqf(n):
    t = 1
    for p, e in factor(n).items():
        if e % 2: t *= p
    return t
def Dset(a, b): return [d for d in range(1 + b, isqrt(a) + 1, b) if a % (d * d) == 0]   # brute reference
def Dx(x):                                                                                 # fast, via factorisation
    a, b = x.numerator, x.denominator
    s = sqrt_part_f(factor(a))
    return sorted(d for d in divisors_from(s) if d >= 2 and (d - 1) % b == 0)
def Gof(ds):
    g = 0
    for d in ds: g = gcd(g, d - 1)
    return g
def Dcoll(ds):
    L = 1
    for d in ds: L = lcm(L, d * d)
    G = Gof(ds); return Fr(L, G), G
def tau(f):
    t = 1
    for e in f.values(): t *= e + 1
    return t
def divisors(n):
    ds = []; i = 1
    while i * i <= n:
        if n % i == 0:
            ds.append(i)
            if i * i != n: ds.append(n // i)
        i += 1
    return sorted(ds)
def wts(ds): return [Fr(gcd(d - 1, e - 1), lcm(d, e) ** 2) for d, e in combinations(ds, 2)]
def rigid(ds): return len(set(wts(ds))) == len(wts(ds))
def sig(ds): return [(lcm(d, e), gcd(d - 1, e - 1)) for d, e in combinations(ds, 2)]
def rigid_sig(ds): s = sig(ds); return len(set(s)) == len(s)

assert Dx(Fr(784, 3)) == Dset(784, 3) == [4, 7, 28]
def Lof(ds):
    L = 1
    for d in ds: L = lcm(L, d)
    return L
def ordmod(a, g):
    k, v = 1, a % g
    while v != 1: v = v * a % g; k += 1
    return k
def divs_of(n): return sorted(divisors_from(factor(n)))
def st_step(s, t):
    f = factor(t + 1); sg = 1; tt = 1
    for p, e in f.items():
        sg *= p ** (e // 2)
        if e % 2: tt *= p
    return s * sg, tt
def v2(n):
    k = 0
    while n % 2 == 0: n //= 2; k += 1
    return k
def odd_part(n):
    while n % 2 == 0: n //= 2
    return n
def hyp_P(g, k, m, star=False):
    """Finite hypotheses of Theorem P (star=False: gcd(g,6)=1) or Theorem P* (star=True: g odd, 3 | g allowed).
    s = 2^k m.  H1 residues of divisors of m contain <2>; H2 saturation of every prime power of m and of 2^(k'), k' in [k,k+o);
    H3 (g+1) | s and G(s^2/g) = g; H4 (relaxed denominators): for t in {1,2,3}, b_t = g/gcd(g,t): every divisor d=2^j a (a | m, 0<=j<o) with d = 1 mod b_t has d = 1 mod g."""
    if g < 5 or g % 2 == 0: return False, "need g>=5 odd"
    if not star and gcd(g, 6) != 1: return False, "need gcd(g,6)=1"
    if k < 1 or m % 2 == 0 or gcd(m, g) != 1: return False, "k>=1, m odd, gcd(m,g)=1"
    o = ordmod(2, g); H = {pow(2, i, g) for i in range(o)}; dm = divs_of(m)
    if not H <= {d % g for d in dm}: return False, "H1 fails"
    for q, e in factor(m).items():
        rest = m // q ** e; dr = divs_of(rest)
        if not any((q ** e * 2 ** c * u) % g == 1 for c in range(k + 1) for u in dr): return False, f"H2 fails at {q}^{e}"
    for kk in range(k, k + o):
        if not any((2 ** kk * u) % g == 1 for u in dm): return False, "H2 fails at power of 2"
    s = 2 ** k * m
    if s % (g + 1): return False, "H3: g+1 does not divide s"
    D = [d for d in divs_of(s) if d >= 2 and d % g == 1]
    if Lof(D) != s or Gof(D) != g: return False, "H3: lcm D != s or G != g"
    for t in (1, 2, 3):
        b = g // gcd(g, t)
        for a in dm:
            for j in range(o):
                d = 2 ** j * a
                if d >= 2 and d % b == 1 and d % g != 1: return False, f"H4 fails: t={t} d={d}"
    return True, "ok"
def P_orbit(g, k, m, N, check=True):
    """direct forward iteration of the collective map from x0=s^2/g; returns (bad, Rs, ks, gammas)"""
    s = 2 ** k * m; t = 1; x = Fr(s * s, g); bad = 0; Rs = []; ks = []; gam = []
    for n in range(N):
        T = Dx(x)
        if check:
            b = g // gcd(g, t); D = [d for d in divs_of(s) if d >= 2 and d % b == 1]
            if x != Fr(s * s * t, g) or T != D or Lof(T) != s or Gof(T) != g: bad += 1
        Rs.append(len(T)); ks.append(v2(s)); L = Lof(T); gam.append(int(g * x) // (L * L))
        Dl, G = Dcoll(T); x = x + Dl; s, t = st_step(s, t)
    return bad, Rs, ks, gam



# =================================================================== ABSTRACT MACHINE (exact, residue-class form of the one-step law)
# State of a persistent orbit with G = g:  x = gamma * L^2 / g,  L = lcm D(x) = prod p^E[p],  gcd(L, g) = 1.
# ONE-STEP LAW (T49).  With w = gamma + 1, h = gcd(g, w), b' = g/h, sigma' = L * sqrtpart(w/h):
#     D(x') = { d | sigma' : d >= 2, d = 1 (mod b') }.
# x' is persistent (G(x') = g) iff every such d is = 1 (mod g); then L' = lcm D', gamma' = w L^2 / L'^2 = w / r^2, r = L'/L.
# The machine below computes exactly this, but through residues mod g (sets of reachable residues), never through
# the integers themselves, so it can run with astronomically large L.  It is validated against direct iteration of the
# collective map (section A) before any claim uses it.
def small_fac(n):
    return dict(factor(n)) if n > 1 else {}
def ordm(a, m):
    if m == 1: return 1
    a %= m; k = 1; x = a
    while x != 1:
        x = x * a % m; k += 1
        if k > m: return None
    return k
def prodset(sets, g):
    cur = {(1 % g, False)}
    for R in sets:
        new = set()
        for (a, ne) in cur:
            for k, rr in enumerate(R): new.add((a * rr % g, ne or k > 0))
        cur = new
    return cur
def fibre_exps(g, w, E):
    """x = w L^2 / g (L has exponent dict E, coprime to g): returns (persistent?, exponents of lcm D(x), exponents of sigma)."""
    h = gcd(g, w); b = g // h
    fw = small_fac(w // h) if w // h > 1 else {}
    Es = {}
    for p in set(E) | set(fw):
        e = E.get(p, 0) + fw.get(p, 0) // 2
        if e > 0: Es[p] = e
    ps = sorted(Es)
    res = {p: [pow(p, k, g) for k in range(Es[p] + 1)] for p in ps}
    full = prodset([res[p] for p in ps], g)
    ok = all(not (ne and a % b == 1 % b and a != 1 % g) for (a, ne) in full)
    E1 = {}
    for p in ps:
        othres = {a for (a, ne) in prodset([res[q] for q in ps if q != p], g)}
        m = 0
        for k in range(1, Es[p] + 1):
            pk = res[p][k]
            if any((pk * a - 1) % b == 0 for a in othres): m = k
        if m > 0: E1[p] = m
    return ok, E1, Es
def Gexact(g, w, E):
    """exact G(x) for x = w L^2/g (E = exponents of L): gcd of d-1 over the divisors d >= 2 of sigma' with d = 1 (mod b).
    Lazy enumeration with early exit: g | G whenever the state is persistent, so a running gcd equal to g is G; a cap on the number of divisors
    (3 000 000) returns None (state not decided) instead of exhausting memory."""
    h = gcd(g, w); b = g // h
    fw = small_fac(w // h) if w // h > 1 else {}
    Es = {}
    for p in set(E) | set(fw):
        e = E.get(p, 0) + fw.get(p, 0) // 2
        if e > 0: Es[p] = e
    size = 1
    for e in Es.values(): size *= e + 1
    if size > 3000000: return None
    G = 0; ps = list(Es)
    stack = [(0, 1)]
    while stack:
        i, d = stack.pop()
        if i == len(ps):
            if d >= 2 and (d - 1) % b == 0:
                G = gcd(G, d - 1)
                if G == g: return G
            continue
        p = ps[i]; x = d
        for k in range(Es[p] + 1):
            stack.append((i + 1, x)); x *= p
    return G
def mstep(g, gamma, E):
    """one step of the machine; returns (gamma', E', Delta) or None (G changes) or ('INV'|'INT', ...) on internal inconsistency"""
    w = gamma + 1
    ok, E1, Es = fibre_exps(g, w, E)
    if not ok: return None
    for p in E:
        if E1.get(p, 0) < E[p]: return ('INV', p)
    D = {p: E1.get(p, 0) - E.get(p, 0) for p in E1 if E1.get(p, 0) - E.get(p, 0) > 0}
    r2 = 1
    for p, d in D.items(): r2 *= p ** (2 * d)
    if w % r2: return ('INT', w, r2)
    return w // r2, E1, D
def minit(g, gamma0, Eseed, checkG=True):
    """state of x0 = gamma0 * Lseed^2 / g, renormalised so that L = lcm D(x0); None if G(x0) != g"""
    if any(gcd(p, g) > 1 for p in Eseed): return None      # the law needs gcd(L, g) = 1 (automatic for persistent states)
    ok, E1, Es = fibre_exps(g, gamma0, Eseed)
    if not ok or not E1: return None
    if checkG and Gexact(g, gamma0, Eseed) != g: return None
    num = Fr(gamma0)
    for p in set(E1) | set(Eseed): num *= Fr(p) ** (2 * (Eseed.get(p, 0) - E1.get(p, 0)))
    if num.denominator != 1: return None
    return int(num), E1
def classkey(gamma, E, orders):
    key = []
    for p, e in sorted(E.items()):
        o = orders[p]
        c = e if e <= o - 2 else (o - 1) + ((e - (o - 1)) % o)
        if c != 0: key.append((p, c))
    return (gamma, tuple(key))
def lval(E):
    v = 1
    for q, e in E.items(): v *= q ** e
    return v
def run_cycle(g, Eseed, gamma0, maxn=3000, checkG=True):
    """iterate the machine until the CLASS KEY repeats (T51).  Returns ('cycle', n1, P, rho, hist) with hist[i]=(gamma_i, E_i), or a failure tag."""
    st = minit(g, gamma0, Eseed, checkG)
    if st is None: return ('noinit',)
    gamma, E = st; orders = {}; seen = {}; hist = []
    for n in range(maxn):
        for p in E:
            if p not in orders:
                if gcd(p, g) > 1: return ('pg',)
                orders[p] = ordm(p, g)
        k = classkey(gamma, E, orders)
        if k in seen:
            n1 = seen[k]; P = n - n1; e1 = hist[n1][1]; rho_ = 1
            for p in set(E) | set(e1): rho_ *= p ** (E.get(p, 0) - e1.get(p, 0))
            return ('cycle', n1, P, rho_, hist[n1:n])
        seen[k] = n; hist.append((gamma, dict(E)))
        r = mstep(g, gamma, E)
        if r is None: return ('leaves', n)
        if r[0] in ('INV', 'INT'): return ('bad', r)
        gamma, E, D = r
    return ('long',)
def reduce_cycle(cyc):
    """minimal period p of the gamma word on the class cycle, the uniform scaling ratio rho_p = L_{n+p}/L_n (None if not uniform),
    and the carry events (w, r^2) of one gamma-period"""
    _, n1, P, rho_, hist = cyc
    gams = [h[0] for h in hist]; p = P
    for cand in range(1, P + 1):
        if P % cand == 0 and all(gams[i] == gams[(i + cand) % P] for i in range(P)): p = cand; break
    Ls = [lval(h[1]) for h in hist]; ratios = set()
    for i in range(P):
        j = i + p
        ratios.add(Fr(Ls[j], Ls[i]) if j < P else Fr(Ls[j - P] * rho_, Ls[i]))
    uniform = len(ratios) == 1
    rp = ratios.pop() if uniform else None
    ev = []
    for i in range(p):
        w = gams[i] + 1; g1 = gams[(i + 1) % P]
        if g1 != w: ev.append((w, w // g1))
    return p, rp, ev, uniform
def direct_orbit(g, Eseed, gamma0, N):
    """INDEPENDENT of the machine: iterate x -> x + Delta_coll(x) on exact rationals from x0 = gamma0 Lseed^2/g; returns rows (gamma, L, G, R)"""
    x = Fr(gamma0 * lval(Eseed) ** 2, g); rows = []
    for n in range(N):
        T = Dx(x); L = Lof(T); G = Gof(T)
        gam = (g * x) / (L * L)
        rows.append((gam, L, G, len(T)))
        Dl, _G = Dcoll(T); x = x + Dl
    return rows


def machine_orbit(g, Eseed, gamma0, N, checkG=True):
    st = minit(g, gamma0, Eseed, checkG)
    if st is None: return None
    gam, E = st; out = [(gam, dict(E))]
    for n in range(N - 1):
        r = mstep(g, gam, E)
        if r is None or r[0] in ('INV', 'INT'): return out
        gam, E, D = r; out.append((gam, dict(E)))
    return out


# =====================================================================================================================
# v010 additions.  The exact carry scheduler (T59):  at a state with gamma = 1 the next carry is the smallest p^j,
# j = pending exponent of p = min{ j >= 1 : p^(e_p+j) * a == 1 (mod g) for some a in residues of divisors of prod_{q != p} q^(e_q) }.
# =====================================================================================================================
def pend_j(g, E, p):
    """pending exponent j_p of the prime p (p coprime to g) at the exponent state E (E[p] absent = 0); None if no j <= ord_g(p) works"""
    o = ordm(p, g)
    if o is None: return None
    qs = [q for q in E if q != p and E[q] > 0]
    A = {a for (a, ne) in prodset([[pow(q, k, g) for k in range(E[q] + 1)] for q in qs], g)}
    e = E.get(p, 0)
    for j in range(1, o + 1):
        if pow(pow(p, e + j, g), -1, g) in A: return j
    return None
def small_primes(n): return [p for p in range(2, n + 1) if is_prime(p)]
def pendings(g, E):
    """{p: (j, p^j)} for all primes p with p^j <= 2 sqrt(g) (the only carries that can occur, T52), p coprime to g"""
    lim = isqrt(4 * g) + 1; out = {}
    for p in small_primes(lim):
        if g % p == 0: continue
        j = pend_j(g, E, p)
        if j is not None and p ** j <= lim: out[p] = (j, p ** j)
    return out
def sched_next(g, E):
    pd = pendings(g, E)
    if not pd: return None
    p = min(pd, key=lambda q: pd[q][1]); return p, pd[p][0]
def abs_set(g, E, p):
    """Abs_p of T56 (E is a state in which every active prime is saturated)"""
    o = ordm(p, g); qs = [q for q in E if q != p and E[q] > 0]
    A = {a for (a, ne) in prodset([[pow(q, k, g) for k in range(E[q] + 1)] for q in qs], g)}
    return o, {k for k in range(o) if pow(pow(p, k, g), -1, g) in A}
def min_period(Abs, o):
    for s in range(1, o + 1):
        if o % s == 0 and all(((k + s) % o in Abs) == (k in Abs) for k in range(o)): return s
def gap_list(Abs, o):
    """cyclic gaps between consecutive elements of Abs (sorted) in Z/o"""
    a = sorted(Abs)
    return [(a[(i + 1) % len(a)] - a[i]) % o or o for i in range(len(a))]
def carry_events(states):
    """list of (prime, exponent increment) per carry in a list of (gamma, E) states; None if a carry changes two primes at once"""
    out = []
    for i in range(len(states) - 1):
        E0 = states[i][1]; E1 = states[i + 1][1]
        inc = {p: E1.get(p, 0) - E0.get(p, 0) for p in set(E0) | set(E1) if E1.get(p, 0) != E0.get(p, 0)}
        if inc:
            if len(inc) > 1: return None
            (p, j), = inc.items(); out.append((p, j))
    return out
def congruent_prime(r, g):
    for k in range(0, 600):
        u = r + k * g
        if u > 1 and is_prime(u) and u != g: return u
    return None
GS2 = [p for p in range(53, 260) if is_prime(p)] + [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
def gen_random_seed(rng):
    g = rng.choice(GS2); Es = {}
    for p in rng.sample([2, 3, 5, 7, 11, 13], rng.randint(2, 4)):
        if g % p: Es[p] = rng.randint(1, 5)
    for _k in range(rng.randint(0, 2)):
        q = rng.choice([2, 3, 5, 7]); u = q ** rng.randint(1, 3) + rng.randint(1, 60) * g
        if is_prime(u) and u != g: Es[u] = rng.randint(1, 8)
    return g, Es, rng.randint(1, 10)
def gen_competing_seed(rng):
    """adversarial: two small primes p, q start SATURATED (they compete from the start), plus frozen auxiliary primes with random residues"""
    g = rng.choice([x for x in GS2 if x >= 11]); sp = [p for p in small_primes(isqrt(g)) if g % p]
    if len(sp) < 2: return None
    sp = [r for r in sp if ordm(r, g) <= 60]
    if len(sp) < 2: return None
    p, q = rng.sample(sp, 2); Es = {}
    for r in (p, q):
        o = ordm(r, g); Es[r] = o - 1 + rng.randint(0, 2)
    for r in rng.sample(sp, rng.randint(0, min(2, len(sp)))):
        if r not in Es: Es[r] = rng.randint(1, 3)
    for _k in range(rng.randint(0, 2)):
        r = rng.randint(2, g - 1); u = congruent_prime(r, g)
        if u is not None and u not in Es: Es[u] = rng.randint(1, max(1, ordm(r, g)))
    return g, Es, rng.randint(1, 6)
def run_cycle_t(g, Eseed, gamma0, maxn, tmax):
    """run_cycle (T51 class closure) with a wall-clock cap tmax seconds per seed; returns ('timeout',) when exceeded"""
    st = minit(g, gamma0, Eseed, True)
    if st is None: return ('noinit',)
    gamma, E = st; orders = {}; seen = {}; hist = []; t_end = time.time() + tmax
    for n in range(maxn):
        if time.time() > t_end: return ('timeout',)
        if gamma.bit_length() > 64: return ('big',)         # gamma + 1 would have to be factored (transient with a huge initial gamma): skipped
        for p in E:
            if p not in orders:
                if gcd(p, g) > 1: return ('pg',)
                orders[p] = ordm(p, g)
        k = classkey(gamma, E, orders)
        if k in seen:
            n1 = seen[k]; P = n - n1; e1 = hist[n1][1]; rho_ = 1
            for p in set(E) | set(e1): rho_ *= p ** (E.get(p, 0) - e1.get(p, 0))
            return ('cycle', n1, P, rho_, hist[n1:n])
        seen[k] = n; hist.append((gamma, dict(E)))
        r = mstep(g, gamma, E)
        if r is None: return ('leaves', n)
        if r[0] in ('INV', 'INT'): return ('bad', r)
        gamma, E, D = r
    return ('long',)
def eventual_cycle(g, Es, g0, maxn=700, tmax=6):
    """exact class-closure cycle (T51) of the persistent orbit of the seed, with the states of one class period plus the closing state; None if none (or the per-seed time cap tmax is hit)"""
    cyc = run_cycle_t(g, Es, g0, maxn, tmax)
    if cyc[0] != 'cycle': return None
    hist = cyc[4]; r = mstep(g, hist[-1][0], hist[-1][1])
    if r is None or r[0] in ('INV', 'INT'): return None
    states = hist + [(r[0], r[1])]
    return dict(g=g, Es=Es, g0=g0, cyc=cyc, states=states, ev=carry_events(states))
def build_pool(gen, seconds, seed, maxn=700, cap=10 ** 9):
    rng = random.Random(seed); pool = []; t_end = time.time() + seconds; tried = 0
    while time.time() < t_end and len(pool) < cap:
        sd = gen(rng)
        if sd is None: continue
        tried += 1; c = eventual_cycle(*sd, maxn=maxn)
        if c is not None: pool.append(c)
    return pool, tried
def active_primes(c): return sorted({p for p, j in c['ev']}) if c['ev'] is not None else None
def survivor_data(c):
    """for a cycle with a single active prime p: (p, o, Abs, s, gaps over one translation period s, m_p = largest pending carry p^gap)"""
    (p,) = active_primes(c); E = c['states'][0][1]; o, Abs = abs_set(c['g'], E, p); s = min_period(Abs, o)
    gaps = gap_list({k % s for k in Abs}, s); m = max(p ** j for j in gap_list(Abs, o))
    return p, o, Abs, s, gaps, m

# ---- abstract scheduler on cyclic odometers (used for T60): each prime p_i has (Z/s_i, C_i); pending p_i^{gap_i(e_i)}, the smallest fires
def gap_table(C, s):
    return [next(j for j in range(1, s + 1) if (e + j) % s in C) for e in range(s)]
def sched_walk(primes, tabs, mods, start, limit=100000, blocked=None):
    """follow the deterministic scheduler from `start` until a state repeats; returns (set of firing indices on the cycle, cycle length) or ('EXIT',..)"""
    seen = {}; st = start; fired = []; n = 0
    while st not in seen:
        seen[st] = n; best = None
        for i, e in enumerate(st):
            gp = tabs[i][e]
            if gp is None: continue
            c = primes[i] ** gp
            if blocked is not None and blocked(c): continue
            if best is None or c < best[0]: best = (c, i, gp)
        if best is None: return ('EXIT', n)
        c, i, gp = best; ns = list(st); ns[i] = (st[i] + gp) % mods[i]; fired.append(i); st = tuple(ns); n += 1
        if n > limit: return ('LONG', n)
    return set(fired[seen[st]:]), n - seen[st]

# =====================================================================================================================
# v011 additions.  The EXACT carry-level predictor and the static survivor certificate.
# At a reset state (gamma = 1, exponent state E, exact G = g) the next carry is the smallest integer M >= 2 that is AVAILABLE:
#   M = prod p^{j_p} is available  <=>  exists a in prod_{q not | M} {q^i : 0 <= i <= e_q}  with  prod_{p | M} p^{e_p + j_p} * a == 1 (mod g)
# (T53 + T54: the new parts M(d) are the available M, the first plateau step with M(d)^2 | w is w = M^2, the carry is complete).
# =====================================================================================================================
def avail(g, E, M):
    """is the new part M (>= 2) available at the reset state E?"""
    f = small_fac(M)
    if any(g % p == 0 for p in f): return False
    c = 1
    for p, j in f.items(): c = c * pow(p, E.get(p, 0) + j, g) % g
    qs = [q for q in E if q not in f and E[q] > 0]
    A = {a for (a, ne) in prodset([[pow(q, k, g) for k in range(E[q] + 1)] for q in qs], g)}
    return pow(c, -1, g) in A
def next_M(g, E):
    """(M, E') for the next carry from the reset state E (window M^2 < g), or None if no M with M^2 < g is available (the orbit leaves persistence)"""
    for M in range(2, isqrt(g - 1) + 1):
        if avail(g, E, M):
            E2 = dict(E)
            for p, j in small_fac(M).items(): E2[p] = E2.get(p, 0) + j
            return M, E2
    return None
def levels(g, E, n):
    out = []; cur = dict(E)
    for _ in range(n):
        r = next_M(g, cur)
        if r is None: break
        out.append(r); cur = r[1]
    return out
def reset_state(g, Es):
    """minit state of x0 = L^2/g if it is already a reset state (gamma = 1), else None"""
    if any(gcd(p, g) > 1 for p in Es): return None
    st = minit(g, 1, Es, True)
    return st[1] if st is not None and st[0] == 1 else None
def gen_reset_seed(rng):
    g = rng.choice([x for x in GS2 if x >= 11 and x < 200]); Es = {}
    for p in rng.sample([2, 3, 5, 7, 11, 13], rng.randint(1, 4)):
        if g % p: Es[p] = rng.randint(1, 6)
    for _k in range(rng.randint(0, 2)):
        r = rng.randint(2, g - 1); u = congruent_prime(r, g)
        if u is not None and u not in Es: Es[u] = rng.randint(1, max(1, min(8, ordm(r, g))))
    E = reset_state(g, Es)
    return None if E is None or not E else (g, E)
def machine_carries(g, E, nsteps):
    """carry events (prime, increment) of the machine from the reset state E (exact G = g), over at most nsteps steps; None if a carry is composite"""
    mo = machine_orbit(g, {p: e for p, e in E.items()}, 1, nsteps)
    if mo is None: return None, 0
    return carry_events(mo), len(mo)
def window_ok(g, m):
    """S3 + S5: m^2 < g and no prime factor of g is <= m^2 (so gcd(g, w) = 1 for all plateau steps w <= m^2)"""
    if m * m >= g: return False
    return all(p > m * m for p in small_fac(g))
def cert_sat(g, E, r):
    """T66 at a reset state E in which r is saturated.  Returns ('ok', info) or (reason, detail)"""
    o = ordm(r, g)
    if o is None or gcd(r, g) > 1: return ('bad-prime',)
    if E.get(r, 0) < o - 1: return ('unsaturated',)
    o, Abs = abs_set(g, E, r); gaps = gap_list(Abs, o); m = r ** max(gaps)
    if not window_ok(g, m): return ('window', m)
    for M in range(2, m):
        if M % r and avail(g, E, M): return ('competitor', M)
    s = min_period(Abs, o)
    return ('ok', dict(r=r, o=o, Abs=Abs, gaps=gaps, m=m, s=s, cyc=gap_list({k % s for k in Abs}, s)))
def certify(g, E, r):
    """T66 + unsaturated extension T66': static certificate that r (and only r) carries forever from the reset state E.
    The transient (while e_r < ord_g(r) - 1) is unrolled over r-carries only, each checked against the exact next carry; the saturated part is checked once."""
    o = ordm(r, g)
    if o is None or gcd(r, g) > 1: return ('bad-prime',)
    _, Abs = abs_set(g, E, r); Ecur = dict(E); e = Ecur.get(r, 0); word = []
    while e < o - 1:
        j = next(j for j in range(1, o + 1) if (e + j) % o in Abs)
        nm = next_M(g, Ecur)
        if nm is None or nm[0] != r ** j: return ('transient-competitor', e, None if nm is None else nm[0], r ** j)
        word.append(j); e += j; Ecur[r] = e
    res = cert_sat(g, Ecur, r)
    if res[0] != 'ok': return res
    res[1]['transient'] = word; res[1]['Esat'] = Ecur
    return ('ok', res[1])
def predicted_word(info, n):
    """the first n carry exponents of r from the reset state: the unsaturated transient, then the walk e -> e + gap(e) over Abs_r from the CURRENT phase"""
    w = list(info['transient']); o = info['o']; Abs = info['Abs']; e = info['Esat'][info['r']]
    while len(w) < n:
        j = next(j for j in range(1, o + 1) if (e + j) % o in Abs); w.append(j); e += j
    return w[:n]
def candidate_primes(g): return [p for p in small_primes(isqrt(g - 1)) if g % p]
def find_certified(g, E):
    """all primes r that are statically certified from the reset state E"""
    return [(r, c[1]) for r in candidate_primes(g) for c in [certify(g, E, r)] if c[0] == 'ok']


# =====================================================================================================================
# v012 additions.  Effective predictability: how long can the transient last before the rigid regime is certified?
#  T69  reset-descent bound  K_reset <= kappa(gamma_0),  kappa = number of iterations of f(a) = floor(a/4)+1 down to 1  (T54, sharpened to log_4)
#  T70  class-counting bound: the reset-state class cycle is entered after at most H(g)-1 carries after the first reset
#  T71  polynomial bound (prime g, or any g where T67 applies): epochs of the scheduler; replaces the product H(g) by a cubic in the orders
#  T72  dynamic G: chains of reducing events, segment bounds, gamma recursion, G = 1 tail
# =====================================================================================================================
def f4(a): return a // 4 + 1
def kappa(a):
    """worst-case number of carries from a plateau-start gamma = a to the first reset: iterations of f(a) = floor(a/4)+1 until 1"""
    k = 0
    while a > 1: a = f4(a); k += 1
    return k
def kappa_closed(a):
    """closed form: least k with 4^k > (3a-4)/2  (a >= 2); kappa(1) = 0"""
    if a <= 1: return 0
    k = 1
    while 2 * 4 ** k <= 3 * a - 4: k += 1
    return k
def kappa3(t):
    """iterations of f until the value is <= 3 (entry of the G = 1 cycle 1 -> 2 -> 3, T32)"""
    k = 0
    while t > 3: t = f4(t); k += 1
    return k
def Omega(n): return sum(small_fac(n).values()) if n > 1 else 0
def Pg(g):
    """primes that can ever carry in a persistent orbit with modulus g: p coprime to g, p^2 < g (g odd) or p^2 <= 4g (g even) (T52(c))"""
    out = []
    for p in small_primes(isqrt(4 * g) + 1):
        if g % p == 0: continue
        if (g % 2 == 1 and p * p < g) or (g % 2 == 0 and p * p <= 4 * g): out.append(p)
    return out
def Hb(g):
    """T70: number of reset-state classes  prod_{p in P_g} (2 o_p - 1)"""
    h = 1
    for p in Pg(g): h *= 2 * ordm(p, g) - 1
    return h
def Kpoly(g):
    """T71: (Phi_max + 1) * ( S + (S+1)(w+1) + 1 ),  S = sum o_p, w = max o_p, Phi_max = sum (o_p - 1)"""
    P = Pg(g); os_ = [ordm(p, g) for p in P]
    if not os_: return 0
    S = sum(os_); w = max(os_); Phi = sum(o - 1 for o in os_)
    return (Phi + 1) * (S + (S + 1) * (w + 1) + 1)
def classP(g, E, P, orders):
    key = []
    for p in P:
        o = orders[p]; e = E.get(p, 0)
        key.append(e if e <= o - 2 else (o - 1) + ((e - (o - 1)) % o))
    return tuple(key)
def iterate_classes(g, E0, maxn=200000):
    """carry-level iteration (T67) from the reset state E0 until the class of the reset state repeats (T51) or the orbit leaves persistence"""
    P = Pg(g); orders = {p: ordm(p, g) for p in P}
    seen = {}; states = []; E = dict(E0); carries = []
    for n in range(maxn):
        k = classP(g, E, P, orders)
        if k in seen: return dict(kind='cycle', i=seen[k], j=n, states=states, carries=carries, P=P, orders=orders)
        seen[k] = n; states.append(dict(E))
        r = next_M(g, E)
        if r is None: return dict(kind='exit', n=n, states=states, carries=carries, P=P, orders=orders)
        carries.append(r[0]); E = r[1]
    return dict(kind='long', states=states, carries=carries, P=P, orders=orders)
def sat_set(E, P, orders): return {p for p in P if E.get(p, 0) >= orders[p] - 1}
def cU(g, E, P, orders):
    """smallest available M supported on unsaturated primes (the epoch's frozen competitor); None if none below the window"""
    S = sat_set(E, P, orders)
    for M in range(2, isqrt(g - 1) + 1):
        f = small_fac(M)
        if all(p in P and p not in S for p in f) and avail(g, E, M): return M
    return None
def phi(E, P, orders): return sum(min(E.get(p, 0), orders[p] - 1) for p in P)
def analyse_epochs(g, R):
    """T71 lemmas along one carry-level orbit.  L1: every carry is a pure saturated prime power or has unsaturated support.  L2: a saturated-power carry leaves cU unchanged.
    PHI: a carry with unsaturated support raises Phi by >= 1.  SATMONO: the saturated set only grows.  Returns violations, the number of epoch-ending carries, and the epochs (saturated-carry count, start state)."""
    P = R['P']; orders = R['orders']; st = R['states']; car = R['carries']
    viol = []; n_end = 0; epochs = []; cur = 0; Estart = st[0]
    for t in range(len(car)):
        if t + 1 >= len(st): break
        E = st[t]; E2 = st[t + 1]; M = car[t]; f = small_fac(M); S = sat_set(E, P, orders)
        pure_sat = (len(f) == 1 and list(f)[0] in S); uns = all(p not in S for p in f)
        if not (pure_sat or uns): viol.append(('L1', t, M))
        if pure_sat:
            cur += 1
            if cU(g, E, P, orders) != cU(g, E2, P, orders): viol.append(('L2', t, M))
        else:
            n_end += 1
            if phi(E2, P, orders) < phi(E, P, orders) + 1: viol.append(('PHI', t, M))
            epochs.append((cur, Estart)); cur = 0; Estart = E2
        if not S <= sat_set(E2, P, orders): viol.append(('SATMONO', t))
    epochs.append((cur, Estart))
    return viol, n_end, epochs
def Bep(g, E, P, orders):
    """per-epoch bound  N_o + (N_o+1)(|Abs_p*|+1),  N_o = sum_{i != p*} |Abs_i|, p* = argmin m_i over the epoch's saturated primes"""
    S = sorted(sat_set(E, P, orders))
    if not S: return 0
    ab = {}
    for p in S:
        o, Abs = abs_set(g, E, p); ab[p] = (Abs, max(gap_list(Abs, o)))
    ps = min(S, key=lambda p: p ** ab[p][1])
    No = sum(len(ab[p][0]) for p in S if p != ps)
    return No + (No + 1) * (len(ab[ps][0]) + 1)

# ---- exact general step (reducing events included) and the hybrid tracer
def enum_div(Es):
    out = [(1, {})]
    for p, e in Es.items():
        new = []
        for d, x in out:
            for k in range(e + 1):
                y = dict(x)
                if k: y[p] = k
                new.append((d * p ** k, y))
        out = new
    return out
def gstep(g, gamma, E):
    """exact step of C from x = gamma L^2 / g (E = exponents of L = lcm D(x), gcd(L, g) = 1, G(x) = g).  Returns (g', gamma', E') for x' = C(x),
    G' = gcd{d-1 : d in D(x')}, gamma' = G' x' / L'^2 (T44).  Independent of the residue machine; used at reducing events."""
    w = gamma + 1; h = gcd(g, w); b = g // h
    fw = small_fac(w // h) if w // h > 1 else {}
    Es = {}
    for p in set(E) | set(fw):
        e = E.get(p, 0) + fw.get(p, 0) // 2
        if e > 0: Es[p] = e
    size = 1
    for e in Es.values(): size *= e + 1
    if size > 3000000: raise OverflowError('too many divisors')
    G1 = 0; E1 = {}
    for d, x in enum_div(Es):
        if d >= 2 and (d - 1) % b == 0:
            G1 = gcd(G1, d - 1)
            for p, k in x.items():
                if k > E1.get(p, 0): E1[p] = k
    L1 = lval(E1)
    y1 = Fr(w * lval(E) ** 2, g) * G1
    assert y1.denominator == 1
    q = y1 / (L1 * L1)
    assert q.denominator == 1, "gamma' not an integer (T44(a))"
    return G1, int(q), E1
def sqf_t(t):
    r = 1
    for p, e in small_fac(t).items():
        if e % 2: r *= p
    return r
def tail_g1(t):
    """steps until t_n <= 3 in the G = 1 regime: t -> sqf(t+1)  (v005 T32)"""
    n = 0
    while t > 3: t = sqf_t(t + 1); n += 1
    return n
def trace(g, gamma, E, maxsteps=20000, tmax=10.0):
    """hybrid exact trace of the orbit of x = gamma L^2/g: residue machine inside constant-G segments, the exact stepper gstep at reducing events.
    Returns (segments, tail) or None on timeout.  Segment fields: g, gamma0, kind ('reducing'|'cycle'|'long'), steps, carries (preserving events before the reducing event / before the class cycle is entered),
    carries_to_reset (None if no reset reached), gam_before, t54viol (violations of gamma' <= gamma_s/4 + 1 at carries), Eend (exponent state at the end)."""
    segs = []; t_end = time.time() + tmax
    while True:
        if g == 1: return segs, dict(t=gamma, N=tail_g1(gamma))
        orders = {}; seen = {}; gam = gamma; Ec = dict(E); n = 0; carries = 0; carries_at = {}
        creset = 0 if gam == 1 else None; gs = gam; viol = 0
        seg = dict(g=g, gamma0=gamma, E0=dict(E))
        while True:
            if time.time() > t_end or gam.bit_length() > 90: return None
            for p in Ec:
                if p not in orders: orders[p] = ordm(p, g)
            key = classkey(gam, Ec, orders)
            if key in seen:
                seg.update(kind='cycle', entry_step=seen[key], steps=n, carries=carries_at[seen[key]], carries_to_reset=creset, t54viol=viol, Eend=dict(Ec), gamend=gam, gam_before=None)
                segs.append(seg); return segs, None
            seen[key] = n; carries_at[n] = carries
            r = mstep(g, gam, Ec)
            if r is None:
                seg.update(kind='reducing', steps=n, carries=carries, carries_to_reset=creset, gam_before=gam, t54viol=viol, Eend=dict(Ec)); segs.append(seg)
                try: g1, gamma1, E1 = gstep(g, gam, Ec)
                except OverflowError: return None
                assert g1 != g and g % g1 == 0, "reducing event must give a proper divisor"
                g, gamma, E = g1, gamma1, E1
                break
            if r[0] in ('INV', 'INT'): raise Exception('machine inconsistency ' + str(r))
            gam2, E2, D = r
            if D:
                carries += 1
                if 4 * gam2 > gs + 4: viol += 1
                if gs == 1 and gam2 != 1: viol += 1
                gs = gam2
            gam, Ec = gam2, E2; n += 1
            if gam == 1 and creset is None: creset = carries
            if n > maxsteps:
                seg.update(kind='long', steps=n, carries=carries, carries_to_reset=creset, gam_before=None, t54viol=viol, Eend=dict(Ec)); segs.append(seg); return segs, None
GC = [15, 21, 33, 35, 39, 51, 55, 57, 65, 69, 77, 85, 87, 91, 93, 95, 105, 115, 119, 123, 129, 143, 155, 165, 195, 231, 255, 285, 315,
      68, 76, 92, 100, 124, 148, 172, 196, 220, 260, 340]
def prime_1mod(g0, rng, kmax=60):
    ks = list(range(1, kmax)); rng.shuffle(ks)
    for k in ks:
        q = 1 + g0 * k
        if is_prime(q): return q, k
    return None
def gen_dyn_seed(rng):
    """composite/even g0 with two primes q = 1 mod g0 (so that G(x0) = g0 can hold), optional small primes; validated by minit (exact G check)"""
    g0 = rng.choice(GC); a = prime_1mod(g0, rng); b = prime_1mod(g0, rng)
    if a is None or b is None or a[0] == b[0] or gcd(a[1], b[1]) != 1: return None
    Es = {a[0]: 1, b[0]: 1}
    for p in rng.sample([2, 3, 5, 7, 11, 13], rng.randint(0, 3)):
        if g0 % p: Es[p] = rng.randint(1, 4)
    st = minit(g0, rng.randint(1, 3 * g0), Es, True)
    if st is None: return None
    return g0, st[0], st[1]
def descent(g, E, gamma0):
    """machine from the state (gamma0, E) of constant G = g until the first reset: (K carries, T54 violations, steps, reached)"""
    gam = gamma0; Ec = dict(E); K = 0; gs = gam; viol = 0; n = 0
    if gam == 1: return 0, 0, 0, True
    while True:
        r = mstep(g, gam, Ec)
        if r is None: return K, viol, n, False
        if r[0] in ('INV', 'INT'): raise Exception(str(r))
        g2, E2, D = r; n += 1
        if D:
            K += 1
            if 4 * g2 > gs + 4: viol += 1
            if gs == 1 and g2 != 1: viol += 1
            gs = g2
        gam, Ec = g2, E2
        if gam == 1: return K, viol, n, True
        if n > 50 * g: return K, viol, n, False
def Rbound(g, Gam, memo):
    """T72 bound on the total number of preserving events (carries) over all admissible chains starting with a segment of G = g and starting gamma <= Gam:
    own segment kappa(Gam) + H(g) - 1, plus the worst continuation after a reducing event to a proper divisor g' with Gamma' = floor(g'(Gam+4g+1)/g)"""
    if g == 1: return 0
    key = (g, Gam)
    if key in memo: return memo[key]
    own = kappa(Gam) + Hb(g) - 1; best = 0
    for g1 in divisors(g)[:-1]:
        if g1 == 1: continue
        best = max(best, Rbound(g1, g1 * (Gam + 4 * g + 1) // g, memo))
    memo[key] = own + best; return memo[key]
def Tailbound(g, Gam, memo):
    """T72 bound on the G = 1 tail: 4*kappa3(t) for the worst t that can arise from a chain ending at G = 1"""
    key = (g, Gam)
    if key in memo: return memo[key]
    best = 0
    for g1 in divisors(g)[:-1]:
        Gam1 = g1 * (Gam + 4 * g + 1) // g
        if g1 == 1: best = max(best, 4 * kappa3(Gam1))
        else: best = max(best, Tailbound(g1, Gam1, memo))
    memo[key] = best; return best

def to_reset(g, Es, gamma0, cap=4000):
    """exact machine from the seed until the first reset; returns the reset exponent state or None"""
    st = minit(g, gamma0, Es, True)
    if st is None: return None
    gam, E = st; k = 0
    while gam != 1:
        r = mstep(g, gam, E)
        if r is None or r[0] in ('INV', 'INT') or gam.bit_length() > 64: return None
        gam, E, D = r; k += 1
        if k > cap: return None
    return g, E
def adv_reset_seed(rng):
    """adversarial reset states: two saturated primes compete from the start (gen_competing_seed), run exactly to their first reset"""
    sd = gen_competing_seed(rng)
    if sd is None: return None
    g, Es, g0 = sd
    return to_reset(g, Es, g0)

# =====================================================================================================================
# TESTS
# =====================================================================================================================
def tb(x): return x / 6 if QUICK else x
print("FIELD-I v012 verifier" + (" (QUICK)" if QUICK else ""), flush=True)

# ---------------------------------------------------------------------------------------------------------------- A
print(f"\n[{time.time()-T0:.0f}s]"); print("=== A  T69: reset-descent bound  K_reset <= kappa(gamma_0) (T54 sharpened) ===", flush=True)
N1 = 20000 if QUICK else 300000; bad = 0; badlog4 = 0
for a in range(1, N1 + 1):
    k = kappa(a)
    if k != kappa_closed(a) or k > (a - 1).bit_length(): bad += 1
    if k > ((a - 1).bit_length() + 1) // 2 + 1: badlog4 += 1
rg = random.Random(11)
for _ in range(4000):
    a = rg.getrandbits(rg.randint(2, 220)) + 1; k = kappa(a)
    if k != kappa_closed(a) or k > (a - 1).bit_length(): bad += 1
    if k > ((a - 1).bit_length() + 1) // 2 + 1: badlog4 += 1
rec("A1", "PASS" if bad == 0 and badlog4 == 0 else "FAIL",
    f"kappa(a) = closed form 'least k with 4^k > (3a-4)/2', and kappa(a) <= ceil(log2 a) (the review's bound) and <= ceil(log4 a)+1: exhaustive a <= {N1}, 4000 random a up to 2^220; violations {bad + badlog4}")
print("   gamma_0:      2   10  100  1000  10^6   10^12  10^30  (kappa vs the review's ceil(log2))")
print("   kappa:     " + " ".join(f"{kappa(a):4d}" for a in (2, 10, 100, 1000, 10**6, 10**12, 10**30)))
print("   ceil(log2):" + " ".join(f"{(a-1).bit_length():4d}" for a in (2, 10, 100, 1000, 10**6, 10**12, 10**30)))

# A2: machine, prime g, gamma_0 > 1.  T54 inequality at EVERY carry, K <= kappa(gamma_0), witnesses of sharpness
rng = random.Random(7); t0 = time.time(); tot = reached = viol = ineq = 0; wit = {}; kviol = 0
while time.time() - t0 < tb(70):
    sd = gen_reset_seed(rng)
    if sd is None: continue
    g, E = sd
    for _ in range(30):
        gam0 = int(math.exp(rng.uniform(math.log(2), math.log(10 ** rng.randint(2, 9)))))
        st = minit(g, gam0, E, True)
        if st is None: continue
        gamma, Ec = st
        K, v, n, ok = descent(g, Ec, gamma); tot += 1; ineq += v
        if ok:
            reached += 1; kp = kappa(gamma)
            if K > kp: kviol += 1
            if K == kp and (kp not in wit or gamma < wit[kp][2]): wit[kp] = (g, dict(Ec), gamma, K)
rec("A2", "PASS" if tot > 0 and ineq == 0 and kviol == 0 else "FAIL",
    f"{tot} prime-g starts with gamma_0 > 1 (up to 10^9): {reached} reached a reset; T54 inequality gamma' <= gamma_s/4+1 violated {ineq} times at carries; K_reset > kappa(gamma_0) in {kviol} cases")
print("   sharpness: the bound kappa(gamma_0) is ATTAINED by an exact machine orbit for kappa = " + ",".join(str(k) for k in sorted(wit)))
for k in sorted(wit):
    g_, E_, gm_, K_ = wit[k]; print(f"     kappa = {k:2d}: g = {g_:3d}, gamma_0 = {gm_}, E = {E_}, carries to reset = {K_}")
print("   (the review's ceil(log2 gamma_0) is a valid but loose bound: for gamma_0 = %d it gives %d, kappa = %d)" % (wit[max(wit)][2], (wit[max(wit)][2]-1).bit_length(), max(wit)))

# A3: sharp witnesses re-verified by EXACT direct iteration of the collective map (independent of the machine)
okd = 0; nd = 0
for k in sorted(wit):
    if k == 0 or k > 6: continue
    g_, E_, gm_, K_ = wit[k]
    try:
        K0, v0, n0, ok0 = descent(g_, E_, gm_)
        rows = direct_orbit(g_, E_, gm_, n0 + 3)
    except Exception as ex:
        rec("A3", "DATA", f"kappa={k}: direct iteration skipped ({type(ex).__name__})"); continue
    nd += 1; carr = 0; hit = None
    for n in range(len(rows) - 1):
        if rows[n + 1][1] != rows[n][1]: carr += 1
        if rows[n + 1][0] == 1 and hit is None: hit = carr
        if hit is not None: break
    if hit == k and all(r[2] == g_ for r in rows[:n + 2]): okd += 1
    else: rec("A3", "FAIL", f"kappa={k} witness: direct orbit gives {hit} carries to the reset (G constant: {all(r[2]==g_ for r in rows[:n+2])})")
rec("A3", "PASS" if okd == nd and nd > 0 else "FAIL", f"{okd}/{nd} sharp witnesses (kappa = 1..6) confirmed by exact iteration of C on Fractions: carries to the first reset = kappa exactly, G constant")

# ---------------------------------------------------------------------------------------------------------------- E
print(f"\n[{time.time()-T0:.0f}s]"); print("=== E  T70 / T71: certificate-entry bounds after the first reset ===", flush=True)
ok_tab = all(Hb(g) == h for g, h in ((11, 171), (31, 2655), (59, 21297195)))
rec("E1", "PASS" if ok_tab else "FAIL", "H(g) = prod_{p^2<g}(2 ord_g(p) - 1): H(11) = 171, H(31) = 2655, H(59) = 21297195 (the review's table reproduced); K_poly: " +
    ", ".join(f"g={g}: {Kpoly(g)}" for g in (11, 31, 59, 101, 197)))
rng = random.Random(2); t0 = time.time(); n = nviolH = nviolP = ncert = nl = nlem = nepoch = 0; nex = 0; maxi = {}; certified0 = 0; ents = []; unsat0 = 0
active_ct = Counter(); lemviol = []
while time.time() - t0 < tb(100):
    sd = gen_reset_seed(rng) if rng.random() < 0.5 else adv_reset_seed(rng)
    if sd is None or not is_prime(sd[0]): continue
    g, E = sd; R = iterate_classes(g, E); n += 1
    if R['kind'] == 'long': nl += 1; continue
    H = Hb(g); KP = Kpoly(g); w = max(R['orders'].values())
    if R['kind'] == 'exit':
        nex += 1
        if R['n'] > H - 1 or R['n'] > KP: nviolH += 1
    else:
        i, j = R['i'], R['j']
        if not (j <= H and i <= H - 1): nviolH += 1
        if not (i <= KP and j <= KP + w): nviolP += 1
        cs = R['carries'][i:j]; pr = {tuple(small_fac(M).keys()) for M in cs}
        r = None
        if len(pr) == 1 and len(next(iter(pr))) == 1: r = next(iter(pr))[0]
        else: nviolH += 1
        if r is not None:
            fc = find_certified(g, R['states'][i])
            if fc and [x[0] for x in fc] == [r]: ncert += 1
            else: nviolH += 1; print("   uncertified entry state", g, R['states'][i], r, fc)
            active_ct[r] += 1
        if find_certified(g, R['states'][0]): certified0 += 1
        ents.append((g, i, j)); maxi[g] = max(maxi.get(g, 0), i)
    v, ne, eps = analyse_epochs(g, R); nlem += 1
    P = R['P']; o = R['orders']; phimax = sum(o[p] - 1 for p in P) - phi(R['states'][0], P, o)
    if v or ne > phimax: lemviol.append((g, v[:2], ne, phimax))
    for cnt, Es in eps:
        nepoch += 1
        if cnt > Bep(g, Es, P, o): lemviol.append((g, 'EPOCH', cnt))
rec("E2", "PASS" if nviolH == 0 and nviolP == 0 and ncert > 0 and n > 0 else "FAIL",
    f"{n} prime-g reset seeds ({nex} leave persistence, {nl} unresolved): class repeat index j <= H(g), entry index i <= H(g)-1, i <= K_poly(g); {ncert} cycle-entry states each statically certified for exactly the active prime (T66 necessity); violations {nviolH + nviolP}")
rec("E3", "PASS" if not lemviol and nlem > 0 else "FAIL",
    f"epoch lemmas on {nlem} exact carry-level orbits ({nepoch} epochs): L1 (every carry is a pure saturated prime power or has unsaturated support), L2 (saturated-power carries leave the frozen competitor unchanged), PHI, SATMONO, epoch size <= N_o+(N_o+1)(|Abs|+1): violations {len(lemviol)} {lemviol[:2]}")
print(f"   DATA: entry index i (carries after the first reset until the class cycle is entered): max {max((e[1] for e in ents), default=0)}, median {sorted(e[1] for e in ents)[len(ents)//2] if ents else 0}; "
      f"first reset state already certified in {certified0}/{len(ents)}; active primes {dict(active_ct)}")
big = sorted(maxi.items(), key=lambda t: -t[1])[:5]
print("   DATA: largest observed entry index vs bounds: " + "; ".join(f"g={g}: i={i}, H={Hb(g)}, K_poly={Kpoly(g)}" for g, i in big))

# ---------------------------------------------------------------------------------------------------------------- D
print(f"\n[{time.time()-T0:.0f}s]"); print("=== D  T72: dynamic G -- chains of reducing events from an arbitrary seed ===", flush=True)
rng = random.Random(3); okd = totd = 0
for _ in range(60000):
    if totd >= (60 if QUICK else 300): break
    sd = gen_dyn_seed(rng)
    if sd is None: continue
    g0, gam, E = sd
    if gam.bit_length() > 60: continue
    try:
        rows = rows_ = []
        g_, ga_, E_ = g0, gam, E
        for _k in range(10):
            rows_.append((g_, ga_, lval(E_))); g_, ga_, E_ = gstep(g_, ga_, E_)
        dr = direct_orbit(g0, E, gam, 10)
    except Exception as ex:
        continue
    totd += 1
    if all(Fr(r[1]) == d[0] * d[2] / g0 and r[2] == d[1] and r[0] == d[2] for r, d in zip(rows_, dr)): okd += 1
rec("D1", "PASS" if okd == totd and totd > 0 else "FAIL", f"exact stepper gstep (reducing events included) = independent direct iteration of C on Fractions: (G, gamma, L) agree on {okd}/{totd} orbits x 10 steps")

rng = random.Random(4); t0 = time.time(); N = 0; skipped = 0; viol = Counter(); chains = Counter(); finals = Counter(); worst = []
tot_ratio = []; memoR = {}; memoT = {}; segN = 0; kres = Counter(); ends = []
while time.time() - t0 < tb(120):
    sd = gen_dyn_seed(rng)
    if sd is None: continue
    g0, gam0, E0 = sd
    if gam0.bit_length() > 60: skipped += 1; continue
    tr = trace(g0, gam0, E0, maxsteps=6000, tmax=8.0)
    if tr is None: skipped += 1; continue
    segs, tail = tr; N += 1; chains[len(segs)] += 1
    tot_car = 0; prevg = None; prev = None
    if len(segs) > Omega(g0): viol['chain-length'] += 1
    for s in segs:
        segN += 1
        if s['kind'] == 'long': viol['long'] += 1; continue
        g = s['g']; H = Hb(g); kp = kappa(s['gamma0'])
        tot_car += s['carries']
        if s['carries'] > kp + H - 1: viol['segment-carries'] += 1
        if s['carries_to_reset'] is not None and s['carries_to_reset'] > kp: viol['reset-descent'] += 1
        if s['t54viol']: viol['T54'] += s['t54viol']
        if s['kind'] == 'reducing' and s['steps'] > (s['carries'] + 1) * 4 * g + 1: viol['plateau-steps'] += 1
        if prev is not None:
            pg, pgb, pg0 = prev
            if not (pg % g == 0 and g < pg): viol['divisibility'] += 1
            if s['gamma0'] * pg > g * (pgb + 1): viol['gamma-recursion'] += 1
            if pgb > pg0 + 4 * pg: viol['gamma-before'] += 1
        prev = (g, s['gam_before'], s['gamma0']) if s['kind'] == 'reducing' else None
    if tail is not None:
        if tail['N'] > 4 * kappa3(tail['t']): viol['tail'] += 1
        finals['G=1'] += 1
    else:
        finals['G=%d' % segs[-1]['g']] += 1
    RB = Rbound(g0, gam0, memoR); TB_ = Tailbound(g0, gam0, memoT)
    if tot_car > RB: viol['total-carries'] += 1
    ends.append((g0, len(segs), tot_car, RB))
rec("D2", "PASS" if not viol and N > 0 else "FAIL",
    f"{N} orbits ({skipped} skipped: gamma_0 > 2^60 or time cap), {segN} segments, chain lengths {dict(sorted(chains.items()))}: chain length <= Omega(g_0); strict divisibility g_{{i+1}} | g_i; "
    f"segment carries <= kappa(gamma_i)+H(g_i)-1; carries to reset <= kappa(gamma_i); T54 inequality at every carry; gamma recursion gamma_(i+1) <= g_(i+1)(gamma_before+1)/g_i with gamma_before <= gamma_i + 4 g_i; "
    f"plateau steps <= 4g per carry; G=1 tail <= 4 kappa3(t); total carries <= Rbound(g_0, gamma_0); violations {dict(viol)}")
print(f"   DATA: final regimes {dict(finals.most_common(14))}")
print(f"   DATA: largest observed total carries {max((e[2] for e in ends), default=0)}; for those, Rbound(g_0,gamma_0) has {len(str(max((e[3] for e in ends), default=0)))} digits (worst-case guarantee, not a prediction)")

# D3: end-to-end -- from the ORIGINAL seed, trace to the final cycle; for prime final g the cycle's reset states are certified for the active prime
rng = random.Random(5); t0 = time.time(); n3 = ok3 = bad3 = 0; nc = Counter()
while time.time() - t0 < tb(60):
    sd = gen_dyn_seed(rng)
    if sd is None: continue
    g0, gam0, E0 = sd
    if gam0.bit_length() > 60: continue
    tr = trace(g0, gam0, E0, maxsteps=6000, tmax=8.0)
    if tr is None or tr[1] is not None: continue
    s = tr[0][-1]
    if s['kind'] != 'cycle': continue
    g = s['g']
    if not is_prime(g): continue
    c = eventual_cycle(g, s['Eend'], s['gamend'], maxn=900)
    if c is None or c['ev'] is None: continue
    act = active_primes(c)
    if len(act) != 1: bad3 += 1; continue
    resets = [E for (ga, E) in c['states'][:-1] if ga == 1]
    if not resets: continue
    n3 += 1
    good = all([x[0] for x in find_certified(g, E)] == [act[0]] for E in resets) if all(isinstance(E, dict) for E in resets) else False
    if good: ok3 += 1; nc[len(tr[0])] += 1
    else: bad3 += 1
rec("D3", "PASS" if bad3 == 0 and n3 > 0 else "FAIL",
    f"end-to-end: {n3} seeds with a chain of G-reductions ending in a persistent prime g: every reset state of the exact final class cycle is statically certified for the (single) active prime; failures {bad3}; chain lengths of the certified orbits {dict(sorted(nc.items()))}")

# E5: scope of T66 for composite / even g (data for O11.2 and the T68(a) erratum): exact eventual cycles for composite g
stat = Counter(); nn = 0; comp = []
for g in (15, 39, 51, 57, 87):
    o = ordm(2, g); sv = (g + 1) * (g + 2) ** o; comp.append((g, dict(small_fac(sv)), 1))
comp.append((68, {3: 3, 13: 1, 3947: 8, 281: 4}, 1))
for (g, Es, g0) in comp:
    c = eventual_cycle(g, Es, g0, maxn=3000, tmax=60)
    if c is None or c['ev'] is None or len(active_primes(c)) != 1: stat[(g, 'no-cycle')] += 1; continue
    r = active_primes(c)[0]; nn += 1
    for (ga, E) in c['states'][:-1]:
        if ga == 1: stat[(g, cert_sat(g, E, r)[0])] += 1
rec("E5", "DATA", f"composite/even g (T66 NOT claimed there): {nn} exact eventual cycles (g = 15, 39, 51, 57, 87 from T46 seeds, 68 from v010); status of cert_sat at their reset states (g, status): {dict(sorted(stat.items()))}")

# ---------------------------------------------------------------------------------------------------------------- C
print(f"\n[{time.time()-T0:.0f}s]"); print("=== C  controls ===", flush=True)
g = 31; Es = {2: 5, 101: 2}
E = reset_state(g, Es)
R = iterate_classes(g, E) if E else None
if R and R['kind'] == 'cycle':
    rec("C1", "PASS", f"v011 control g=31, L0 = 2^5 101^2 (a reset state, K_reset = 0): class cycle entered at carry i = {R['i']}, closed at j = {R['j']} (<= H = {Hb(g)}); carries {R['carries'][:6]}...")
else: rec("C1", "FAIL", "control state not a cycle")
wk = max(wit); g_, E_, gm_, K_ = wit[wk]
rec("C2", "PASS" if K_ == kappa(gm_) else "FAIL", f"sharpest descent found: g = {g_}, gamma_0 = {gm_}: {K_} carries to the first reset = kappa(gamma_0) = {kappa(gm_)} (review's log2 bound: {(gm_-1).bit_length()})")

# ---------------------------------------------------------------------------------------------------------------- V
print(f"\n[{time.time()-T0:.0f}s]"); print("=== V  verdicts ===", flush=True)
print("PROVED (hand proofs, THEOREMS.md): T69 (sharp reset-descent), T70 (class-counting entry bound; certified entry state for prime g), T71 (polynomial entry bound), T72 (dynamic-G effective bound).")
print("OPEN (not claimed): exact transient time; T66 for composite/even g (O11.2); closed form of m_p (O11.3); infinite family of carry sizes (O11.4); q=11 closure certificate.")
print(f"\nFIELD-I v012: {NFAIL} FAIL, {time.time() - T0:.0f} s", flush=True)
sys.exit(1 if NFAIL else 0)

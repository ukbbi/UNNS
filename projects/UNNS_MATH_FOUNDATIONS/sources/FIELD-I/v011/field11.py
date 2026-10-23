#!/usr/bin/env python3
"""FIELD-I v011 verifier -- Prime-Survivor Selection and Static Residue Certification (helpers copied from v010/v009/v005 for standalone use).
M: exact carry-level predictor (T53/T54 as a formula) against the residue machine; B: minimax selection (T64); Q: quotient-residue formula (T65);
S: static survivor certificate (T66): soundness, completeness, uniqueness, negatives, coverage; C: controls; V: verdicts.
Exact integer/Fraction arithmetic. Tags PASS/FAIL/DATA/OPEN.
Notation: x=a/b reduced; D(x)={d>=2 : d^2|a, d=1 mod b}; G(x)=gcd{d-1}; C(x)=x+L^2/G, L=lcm D; persistent orbit: G=g forever, x=gamma L^2/g."""
import os, sys, time, random
from fractions import Fraction as Fr
from math import gcd, isqrt
from itertools import combinations
from collections import Counter, defaultdict
QUICK = os.environ.get("FIELD11_QUICK") == "1"
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
    h = gcd(g, w); b = g // h
    fw = small_fac(w // h) if w // h > 1 else {}
    Es = {}
    for p in set(E) | set(fw):
        e = E.get(p, 0) + fw.get(p, 0) // 2
        if e > 0: Es[p] = e
    ds = [1]
    for p, e in Es.items(): ds = [d * p ** k for d in ds for k in range(e + 1)]
    G = 0
    for d in ds:
        if d >= 2 and (d - 1) % b == 0: G = gcd(G, d - 1)
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

import itertools
def subsets(s): return [frozenset(k for k in range(s) if mask >> k & 1) for mask in range(1, 1 << s)]
# =================================================================== M  the exact carry-level predictor against the residue machine
print("\n##### M. EXACT CARRY-LEVEL PREDICTOR next_M (T53/T54 AS A FORMULA) AGAINST THE RESIDUE MACHINE #####")
rngM = random.Random(1101); seedsM = []; triedM = 0; t_end = time.time() + 60; CAPM = 40 if QUICK else 120
while time.time() < t_end and len(seedsM) < CAPM:
    triedM += 1; sd = gen_reset_seed(rngM)
    if sd is not None: seedsM.append(sd)
nM = nmis = ncomp = nseeds = 0
for (g, E) in seedsM:
    mo = machine_orbit(g, dict(E), 1, 220)
    if mo is None: continue
    idx = [i for i in range(len(mo)) if mo[i][0] == 1]; nseeds += 1
    for a_, b_ in zip(idx, idx[1:]):
        E0 = mo[a_][1]; E1 = mo[b_][1]; nm = next_M(g, E0); nM += 1
        if nm is None or nm[1] != {p: e for p, e in E1.items() if e > 0}: nmis += 1
        elif len(small_fac(nm[0])) > 1: ncomp += 1
rec("M1", "PASS" if nmis == 0 and nM > 0 else "FAIL", f"next_M (smallest AVAILABLE new part M, window M^2 < g) = the machine's next reset state at {nM} reset-to-reset carries of {nseeds} reset seeds (prime g < 200; {triedM} seeds tried): {nmis} mismatches; {ncomp} of the carries were composite (several primes at once, transient)")
rec("M2", "DATA", "consequence (T54): from a reset state EVERY later state of a persistent orbit is a reset state (carries are complete, gamma' = 1), so the whole orbit is the carry-level iteration of next_M -- no partial absorption ever occurs after the first reset")

# =================================================================== B  T64 minimax selection (fixed independent odometers)
print("\n##### B. T64: MINIMAX SELECTION FOR FIXED ODOMETERS, AND THE WINDOWED PERSISTENCE CRITERION #####")
def worst_carry(p, C, s):
    tab = gap_table(C, s); return p ** max(tab[e] for e in C)
# B1 exhaustive: 3 primes, all subsets of Z/s_i (s_i <= 4), all starts
trip = [(2, 3, 5), (2, 3, 7), (3, 5, 7)] if not QUICK else [(2, 3, 5)]
n_sys = n_walk = n_bad = n_multi = 0
for primes in trip:
    for s0 in range(1, 5):
        for s1 in range(1, 5):
            for s2 in range(1, 5):
                mods = (s0, s1, s2)
                for C0 in subsets(s0):
                    for C1 in subsets(s1):
                        for C2 in subsets(s2):
                            sets = (C0, C1, C2); tabs = [gap_table(C, s) for C, s in zip(sets, mods)]
                            ms = [worst_carry(p, C, s) for p, C, s in zip(primes, sets, mods)]; best = ms.index(min(ms)); n_sys += 1
                            for st in itertools.product(*[range(s) for s in mods]):
                                r = sched_walk(primes, tabs, mods, st); n_walk += 1
                                if len(r[0]) != 1: n_multi += 1
                                elif next(iter(r[0])) != best: n_bad += 1
rec("B1", "PASS" if n_bad == 0 and n_multi == 0 else "FAIL", f"EXHAUSTIVE 3-prime odometer systems {trip}, all subsets of Z/s (s <= 4), all start phases: {n_sys} systems, {n_walk} walks; survivor = prime with the smallest worst-case carry m = p^(largest cyclic gap): {n_bad} exceptions; walks with two or more recurrent primes: {n_multi}")
# B2 random k = 2..5 primes, larger moduli
rng = random.Random(64); nw = nb = 0; nsys = 0
for _ in range(800 if QUICK else 4000):
    k = rng.randint(2, 5); primes = tuple(rng.sample([2, 3, 5, 7, 11, 13, 17], k)); mods = tuple(rng.randint(1, 24) for _ in range(k))
    sets = [frozenset(e for e in range(s) if rng.random() < rng.choice([0.15, 0.4, 0.8])) or frozenset([rng.randrange(s)]) for s in mods]
    tabs = [gap_table(C, s) for C, s in zip(sets, mods)]; ms = [worst_carry(p, C, s) for p, C, s in zip(primes, sets, mods)]; best = ms.index(min(ms)); nsys += 1
    for _w in range(8):
        st = tuple(rng.randrange(s) for s in mods); r = sched_walk(primes, tabs, mods, st); nw += 1
        if len(r[0]) != 1 or next(iter(r[0])) != best: nb += 1
rec("B2", "PASS" if nb == 0 else "FAIL", f"random systems with 2..5 primes, moduli up to 24: {nsys} systems, {nw} walks, survivor = argmin m in all but {nb}")
# B3 windowed persistence: the system stays admissible forever (no pending carry >= W is ever forced) iff m_min < W
rng = random.Random(65); nw = nb = nex = nok = 0
for _ in range(800 if QUICK else 4000):
    k = rng.randint(1, 4); primes = tuple(rng.sample([2, 3, 5, 7, 11], k)); mods = tuple(rng.randint(1, 16) for _ in range(k))
    sets = [frozenset(e for e in range(s) if rng.random() < rng.choice([0.2, 0.5, 0.9])) or frozenset([rng.randrange(s)]) for s in mods]
    tabs = [gap_table(C, s) for C, s in zip(sets, mods)]; mmin = min(worst_carry(p, C, s) for p, C, s in zip(primes, sets, mods)); W = rng.choice([3, 5, 9, 17, 33, 65, 129])
    for _w in range(6):
        st = tuple(rng.randrange(s) for s in mods); r = sched_walk(primes, tabs, mods, st, blocked=lambda c, W=W: c >= W); nw += 1
        exits = (r[0] == 'EXIT')
        if exits != (mmin >= W): nb += 1
        nex += exits; nok += (not exits)
rec("B3", "PASS" if nb == 0 and nex > 0 and nok > 0 else "FAIL", f"windowed systems (a pending carry >= W is not allowed = the orbit leaves persistence, T52): {nw} walks ({nok} stay admissible forever, {nex} exit); admissible forever <=> smallest worst-case carry m_min < W: {nb} exceptions")

# =================================================================== Q  T65 quotient-residue formula
print("\n##### Q. T65: Abs_p = S_p + t_p Z FROM THE QUOTIENT (Z/g)* / H, AND m_p = p^maxgap(S_p) #####")
def subgroup_gen(g, gens):
    H = {1 % g}
    for q in gens:
        o = ordm(q, g); H = {(h * pow(q, k, g)) % g for h in H for k in range(o)}
    return H
def quotient_abs(g, p, sat, frozen):
    """sat: primes whose residues generate H (saturated); frozen: {prime: exponent}; returns (o, Abs, t, S)"""
    H = subgroup_gen(g, sat); F = {1 % g}
    for q, e in frozen.items(): F = {(f * pow(q, k, g)) % g for f in F for k in range(e + 1)}
    o = ordm(p, g); t = next(t for t in range(1, o + 1) if pow(p, t, g) in H)
    S = {r_ for r_ in range(t) if any((pow(p, r_, g) * f) % g in H for f in F)}
    return o, {k for k in range(o) if k % t in S}, t, S, H
rng = random.Random(651); nq = nbad = nbad_t = nbad_m = ncomp_g = nprime_t = 0; t_end = time.time() + (15 if QUICK else 60)
GQ = [x for x in range(11, 300) if is_prime(x)] + [15, 21, 33, 35, 39, 51, 55, 57, 65, 68, 69, 85, 87, 91, 95, 111, 115, 119]
while time.time() < t_end:
    g = rng.choice(GQ); sp = [p for p in small_primes(60) if g % p]; p = rng.choice(sp)
    others = [q for q in rng.sample(sp, rng.randint(0, 4)) if q != p]
    sat = [q for q in others if rng.random() < 0.6]; frozen = {q: rng.randint(1, 4) for q in others if q not in sat}
    for _k in range(rng.randint(0, 2)):
        r_ = rng.randint(2, g - 1); u = congruent_prime(r_, g)
        if u is not None and u != p and u not in frozen and u not in sat: frozen[u] = rng.randint(1, 4)
    E = {q: ordm(q, g) - 1 for q in sat}; E.update(frozen)
    if ordm(p, g) is None or any(ordm(q, g) is None for q in E): continue
    E = {q: e for q, e in E.items() if e > 0}
    o, Abs_def = abs_set(g, E, p); o2, Abs_q, t, S, H = quotient_abs(g, p, sat, dict(frozen))
    # saturated primes with exponent o-1 = 0 (order 1) contribute only the identity: consistent with H
    nq += 1; ncomp_g += (not is_prime(g))
    if Abs_def != Abs_q: nbad += 1; continue
    gp = gap_list(Abs_def, o); gs = gap_list(S, t) if t > 0 else [1]
    if max(gp) != max(gs): nbad_m += 1
    if is_prime(g):
        nprime_t += 1
        if t != o // gcd(o, len(H)): nbad_t += 1
rec("Q1", "PASS" if nbad == 0 and nbad_m == 0 and nq > 0 else "FAIL", f"quotient formula vs the definition Abs_p={{k: p^(-k) in <other divisors' residues>}}: {nq} random (g, p, saturated set, frozen set) cases ({ncomp_g} with composite or even g, non-cyclic unit groups): Abs identical in all but {nbad}; maximal gap of Abs_p in Z/o_p equals the maximal gap of S_p in Z/t_p in all but {nbad_m}")
rec("Q2", "PASS" if nbad_t == 0 and nprime_t > 0 else "FAIL", f"prime g: t_p = ord(pH) = o_p / gcd(o_p, |H|) in all but {nbad_t} of {nprime_t} cases")

# =================================================================== S  T66 static survivor certificate
print("\n##### S. T66: STATIC SURVIVOR CERTIFICATE (r carries forever, decided from the finite residue data of ONE reset state) #####")
rngS = random.Random(1166); seedsS = []; triedS = 0; t_end = time.time() + 90; CAPS = 100 if QUICK else 400
while time.time() < t_end and len(seedsS) < CAPS:
    triedS += 1; sd = gen_reset_seed(rngS)
    if sd is not None: seedsS.append(sd)
cert_cases = []; ncand = 0; nmulti = 0; reasons = Counter()
for (g, E) in seedsS:
    oks = []
    for r in candidate_primes(g):
        ncand += 1; c = certify(g, E, r)
        reasons[c[0]] += 1
        if c[0] == 'ok': oks.append((r, c[1]))
    if len(oks) > 1: nmulti += 1
    if oks: cert_cases.append((g, E, oks[0]))
rec("S0", "DATA", f"{len(seedsS)} reset seeds (gamma0 = 1 and every seed exponent attained; prime g < 200; {triedS} seeds tried); {ncand} (seed, candidate prime) pairs tested; verdicts {dict(reasons)}; seeds with a statically certified survivor: {len(cert_cases)}")
rec("S1", "PASS" if nmulti == 0 else "FAIL", f"uniqueness: no reset seed has two statically certified primes ({nmulti} violations; T60 plus T66 predict none)")
# soundness: predicted carry word vs the gamma-level residue machine (independent of next_M)
nsound = nbad = nlong = ntr = nvar = 0
for (g, E, (r, info)) in cert_cases:
    K = min(len(info['transient']) + 2 * len(info['cyc']) + 1, 14)
    word = predicted_word(info, K); steps = sum(r ** (2 * j) - 1 for j in word) + 3
    if steps > 3500: nlong += 1; continue
    mo = machine_orbit(g, dict(E), 1, steps)
    ev = carry_events(mo)
    if ev is None or len(mo) < steps or ev[:K] != [(r, j) for j in word]: nbad += 1
    else:
        nsound += 1; ntr += (len(info['transient']) > 0); nvar += (len(set(info['cyc'])) > 1)
rec("S2", "PASS" if nbad == 0 and nsound > 0 else "FAIL", f"SOUNDNESS: for {nsound} certified seeds the machine's first carries (transient + cycle, up to 14 carries, whole plateaus) equal the predicted word EXACTLY and the orbit stays persistent: {nbad} mismatches ({ntr} with an unsaturated transient, {nvar} with a non-constant repeating gap pattern, {nlong} skipped as too long)")
# targeted soundness with DIVERSE gap patterns: prime 2 saturated in a small-order modulus, frozen auxiliary primes with random residues shape Abs_2
def gen_gap_seed(rng):
    g = rng.choice([x for x in range(17, 300) if is_prime(x) and ordm(2, x) is not None and 3 <= ordm(2, x) <= 14]); o = ordm(2, g)
    Es = {2: o - 1 + rng.randint(0, 2)}
    for _k in range(rng.randint(1, 3)):
        r_ = rng.randint(2, g - 1); u = congruent_prime(r_, g)
        if u is not None and u not in Es: Es[u] = rng.randint(1, max(1, ordm(r_, g)))
    E = reset_state(g, Es)
    return None if E is None else (g, E)
rngG = random.Random(4242); nG = nGbad = nGvar = nGtried = 0; t_end = time.time() + (20 if QUICK else 60); patterns = Counter()
while time.time() < t_end:
    nGtried += 1; sd = gen_gap_seed(rngG)
    if sd is None: continue
    g, E = sd; c = certify(g, E, 2)
    if c[0] != 'ok': continue
    info = c[1]; K = 14; word = predicted_word(info, K); steps = sum(2 ** (2 * j) - 1 for j in word) + 3
    if steps > 3500: continue
    mo = machine_orbit(g, dict(E), 1, steps); ev = carry_events(mo); nG += 1
    var = len(set(info['cyc'])) > 1; nGvar += var
    if var: patterns[tuple(info['cyc'])] += 1
    if ev is None or len(mo) < steps or ev[:K] != [(2, j) for j in word]: nGbad += 1
rec("S2b", "PASS" if nGbad == 0 and nGvar >= 5 else "FAIL", f"SOUNDNESS with diverse repeating gap patterns (prime 2 saturated, ord_g(2) in [3,14], frozen auxiliary primes with random residues): {nG} certified seeds ({nGtried} tried), {nGvar} with a NON-CONSTANT repeating pattern (distinct patterns {len(patterns)}, e.g. {list(patterns)[:4]}); predicted 14-carry words (including the phase offset) equal the machine's exactly: {nGbad} mismatches")
# completeness on eventual cycles of random persistent orbits
POOLC, TRIEDC = build_pool(gen_random_seed, 25 if QUICK else 90, 111)
nres = nokc = 0; bad = Counter(); nmul2 = 0
for c in POOLC:
    a = active_primes(c)
    if a is None or len(a) != 1: continue
    r = a[0]; g = c['g']
    for st in c['states'][:-1]:
        if st[0] != 1: continue
        nres += 1; res = cert_sat(g, st[1], r)
        if res[0] == 'ok': nokc += 1
        else: bad[res[0]] += 1
        # uniqueness among saturated primes
        if sum(1 for q in st[1] if q != r and cert_sat(g, st[1], q)[0] == 'ok') > 0: nmul2 += 1
rec("S3", "PASS" if not bad and nres > 0 and nmul2 == 0 else "FAIL", f"COMPLETENESS (necessity): all {nres} reset states of {len(POOLC)} exact eventual cycles (T51 class closure; {TRIEDC} seeds tried) are certified for the cycle's active prime ({nokc} ok; failures {dict(bad)}); no second prime is ever certified ({nmul2} violations)")
# negatives: a saturated prime that fails with a competitor really does not carry forever
nneg = nneg_ok = 0; t_end = time.time() + (15 if QUICK else 40); rngN = random.Random(77)
while time.time() < t_end:
    sd = gen_reset_seed(rngN)
    if sd is None: continue
    g, E = sd
    for r in candidate_primes(g):
        o = ordm(r, g)
        if E.get(r, 0) >= o - 1 and o <= 30:
            res = cert_sat(g, E, r)
            if res[0] == 'competitor':
                want = 3 * o + 4; lv = levels(g, E, want); nneg += 1; prev = dict(E); nonr = len(lv) < want
                for (M, E2) in lv:
                    if any(E2.get(q, 0) != prev.get(q, 0) for q in set(E2) | set(prev) if q != r): nonr = True
                    prev = E2
                nneg_ok += nonr
rec("S4", "PASS" if nneg == 0 or nneg_ok == nneg else "FAIL", f"NEGATIVES: {nneg} reset states with a saturated prime r (ord <= 30), window ok, but a competing available M <= m_r: in {nneg_ok} the carry-level orbit shows a non-r carry (or leaves persistence) within 3*ord+4 carries (all expected)")
# coverage and time to certification
ncov0 = ncov = nnever = 0; tt = []
for (g, E) in seedsS[: (25 if QUICK else 60)]:
    if find_certified(g, E): ncov0 += 1; tt.append(0); continue
    cur = dict(E); found = None
    for k in range(1, 120):
        nm = next_M(g, cur)
        if nm is None: break
        cur = nm[1]
        sat = [r for r in cur if ordm(r, g) is not None and cur[r] >= ordm(r, g) - 1]
        if any(cert_sat(g, cur, r)[0] == 'ok' for r in sat): found = k; break
    if found is None: nnever += 1
    else: tt.append(found)
tt.sort()
rec("S5", "DATA", f"COVERAGE on {min(len(seedsS), 25 if QUICK else 60)} reset seeds: certified at x0 itself (no carries iterated): {ncov0}; certified after k carry-level steps (k = {tt[len(tt) // 2] if tt else None} median, {max(tt) if tt else None} max); not certified within 120 carries (orbit leaves persistence or the transient is longer): {nnever}")

# end-to-end: the statically predicted survivor and scaling law (from x0 only) against the exact class-closure cycle of the orbit
nS6 = nS6ok = nS6skip = 0; t_end = time.time() + (20 if QUICK else 70)
for (g, E, (r, info)) in cert_cases:
    if time.time() > t_end: break
    c = eventual_cycle(g, dict(E), 1, maxn=900, tmax=4)
    if c is None: nS6skip += 1; continue
    a = active_primes(c); pp, rp, ev, uni = reduce_cycle(c['cyc']); nS6 += 1
    if a == [r] and uni and rp == r ** info['s'] and pp == sum(r ** (2 * j) - 1 for j in info['cyc']): nS6ok += 1
rec("S6", "PASS" if nS6 > 0 and nS6ok == nS6 else "FAIL", f"END-TO-END: for {nS6} certified seeds with a computable exact class-closure cycle ({nS6skip} skipped: closure too long), the eventual active prime, the gamma-period sum(r^(2j)-1) and the scaling factor rho = r^s STATICALLY predicted from x0 equal the exact cycle's: {nS6 - nS6ok} mismatches")

# =================================================================== C  controls
print("\n##### C. CONTROLS #####")
# the attachment's example: g = 31, L0 = 2^5 * 101^2 (x0 = L0^2/31): D(x0) = {32, 404, 163216}
g = 31; E0 = reset_state(31, {2: 5, 101: 2})
Dx0 = sorted(Dx(Fr(326432 ** 2, 31)))
c = certify(31, E0, 2)
okc = (E0 == {2: 5, 101: 2} and Dx0 == [32, 404, 163216] and c[0] == 'ok' and c[1]['gaps'] == [2, 2, 1] and c[1]['m'] == 4 and c[1]['cyc'] == [2, 2, 1])
do = direct_orbit(31, {2: 5, 101: 2}, 1, 70); xs = [Fr(r_[0] * r_[1] ** 2, 31) for r_ in do]
resets = [i for i, r_ in enumerate(do) if r_[0] == 1]
okd = all(r_[2] == 31 for r_ in do) and resets[:4] == [0, 15, 30, 33] and all(xs[i + 33] == 1024 * xs[i] for i in range(len(xs) - 33))
rec("C1", "PASS" if okc and okd else "FAIL", f"g = 31, L0 = 2^5*101^2: D(x0) = {Dx0}; certificate: survivor 2, Abs = {sorted(c[1]['Abs']) if c[0]=='ok' else c}, gaps {c[1]['gaps'] if c[0]=='ok' else None}, m = {c[1]['m'] if c[0]=='ok' else None}, competitor scan M in [3, 3] empty; EXACT direct orbit of C (70 states): G = 31 throughout, resets at {resets[:4]}, x_(n+33) = 2^10 x_n for all n")
CT = [("G = 11, seed 2^2 3^3 5^4 (T50)", 11, {2: 2, 3: 3, 5: 4}, 3, [1] * 3),
      ("G = 31 five-carry, seed 67^2 5 2^5 (T57)", 31, {67: 2, 5: 1, 2: 5}, 5, [1] * 3),
      ("G = 31 mixed carries, seed 2^5 101^2 (same as C1)", 31, {2: 5, 101: 2}, 2, [2, 2, 1])]
for (name, g, Es, rwant, gwant) in CT:
    E = reset_state(g, Es)
    if E is None: rec("C2", "DATA", f"{name}: seed is not a reset state (gamma0 renormalises to > 1); skipped"); continue
    cf = find_certified(g, E); ok_ = len(cf) == 1 and cf[0][0] == rwant
    rec("C2", "PASS" if ok_ else "FAIL", f"{name}: state {E}: certified survivors {[(r, i['cyc'], 'transient ' + str(i['transient'])) for r, i in cf]} (expected prime {rwant})")
# a non-certifiable even-g example: S5 fails (g = 68 has the prime factor 2 <= m^2)
rec("C3", "DATA", "g = 68 (v009 E1): the certificate is not applicable because g has the prime factor 2 <= m^2 (plateau steps w with gcd(g,w) > 1 change the persistence condition); even and composite g are OPEN for static certification")

# =================================================================== V  verdicts
print("\n##### V. STATUS OF O10.1 (WHICH PRIME SURVIVES) #####")
rec("V1", "DATA", "(i) fixed odometer tables: survivor = argmin m, phase independent -- PROVED (T64); (ii) worst-case carries from a known frozen residue background: PROVED by the quotient formula (T65); (iii) static survivor certificate from ONE reset state: PROVED sound and (for saturated survivors, prime g) necessary (T66)")
rec("V2", "OPEN", "O11.1: arbitrary seeds with gamma0 > 1 (not a reset state) and seeds whose transient fires several different primes before the eventual background freezes: the survivor is known only after the carry-level iteration reaches a certified state (coverage and time-to-certificate are DATA above)")
rec("V3", "OPEN", "O11.2: static certification for composite and even g (S5 fails when g has a small prime factor); O11.3: closed-form m_p and the survivor for q-carry families from (g, q) alone")
print(f"\n===== FIELD-I v011 summary: {NFAIL} FAIL, elapsed {time.time() - T0:.1f}s =====")
sys.exit(1 if NFAIL else 0)

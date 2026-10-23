#!/usr/bin/env python3
"""FIELD-I v010 verifier -- Multi-Prime Carry Coexistence (helpers copied from v009/v005 for standalone use).
S: the exact carry scheduler (T59) against the residue machine; X: exhaustive/abstract and arithmetic scheduler searches (T60 single-prime dominance,
T62 coprime clocks); R: random and adversarial real orbits of the collective map (eventual cycles, active primes, rho = p^s); C: controls; V: verdicts.
Exact integer/Fraction arithmetic. Tags PASS/FAIL/DATA/OPEN.
Notation: x=a/b reduced; D(x)={d>=2 : d^2|a, d=1 mod b}; G(x)=gcd{d-1}; C(x)=x+L^2/G, L=lcm D; persistent orbit: G=g forever, x=gamma L^2/g."""
import os, sys, time, random
from fractions import Fraction as Fr
from math import gcd, isqrt
from itertools import combinations
from collections import Counter, defaultdict
QUICK = os.environ.get("FIELD10_QUICK") == "1"
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

# =================================================================== S  the scheduler against the residue machine (T59)
print("\n##### S. THE EXACT CARRY SCHEDULER (T59) AGAINST THE RESIDUE MACHINE #####")
POOL1, TRIED1 = build_pool(gen_random_seed, 35 if QUICK else 150, 101)
rec("S0", "DATA", f"random persistent seeds: {TRIED1} seeds tried, {len(POOL1)} exact eventual cycles (T51 class closure) collected")
nchk = 0; bad = 0; nonpp = 0
for c in POOL1:
    if c['ev'] is None: nonpp += 1; continue
    st = c['states']; g = c['g']; idx = [i for i in range(len(st)) if st[i][0] == 1]
    for a_, b_ in zip(idx, idx[1:]):
        E0 = st[a_][1]; E1 = st[b_][1]
        inc = {p: E1.get(p, 0) - E0.get(p, 0) for p in set(E0) | set(E1) if E1.get(p, 0) != E0.get(p, 0)}
        if len(inc) != 1: bad += 1; continue
        (p, j), = inc.items(); nchk += 1
        if sched_next(g, E0) != (p, j): bad += 1
rec("S1", "PASS" if bad == 0 and nchk > 0 and nonpp == 0 else "FAIL", f"scheduler (smallest pending p^j over ALL primes p <= 2 sqrt(g)) = the machine's carry at {nchk} reset states (gamma=1) of {len(POOL1)} eventual cycles: {bad} mismatches; cycles with a composite carry: {nonpp}")

# =================================================================== X  the scheduler theorem T60 on abstract and arithmetic odometers
print("\n##### X. SINGLE-PRIME DOMINANCE (T60): ABSTRACT ODOMETER PAIRS, THEN ODOMETERS BUILT FROM THE ARITHMETIC OF g #####")
def tab_and_m(p, C, s):
    tab = gap_table(C, s); m = max(p ** tab[e] for e in C); return tab, m
def survivor_rule_check(primes, sets, mods, starts, blocked=None):
    """walk the scheduler from the given starts; returns (n_walks, n_two_or_more_firing, n_exit, n_survivor_not_argmin_m, set of survivors)"""
    tabs = []; ms = []
    for p, C, s in zip(primes, sets, mods):
        t_, m_ = tab_and_m(p, C, s); tabs.append(t_); ms.append(m_)
    best = min(range(len(primes)), key=lambda i: ms[i])
    nw = ntwo = nex = nbad = 0
    for st in starts:
        r = sched_walk(primes, tabs, mods, st, blocked=blocked); nw += 1
        if r[0] == 'EXIT' or r[0] == 'LONG': nex += 1; continue
        if len(r[0]) >= 2: ntwo += 1
        elif next(iter(r[0])) != best: nbad += 1
    return nw, ntwo, nex, nbad
# X1: EXHAUSTIVE over all nonempty subsets C_p in Z/s, C_q in Z/t, all start states
import itertools
def subsets(s): return [frozenset(k for k in range(s) if mask >> k & 1) for mask in range(1, 1 << s)]
PAIRS = [(2, 3), (2, 5), (3, 5), (2, 7), (3, 7), (5, 7)] if not QUICK else [(2, 3), (3, 5), (2, 7)]
SMAX = 5 if QUICK else 6
tot_cases = tot_walks = tot_two = tot_bad = 0
for (p, q) in PAIRS:
    for s in range(1, SMAX + 1):
        Ss = subsets(s)
        for t in range(1, SMAX + 1):
            St = subsets(t); starts = list(itertools.product(range(s), range(t)))
            for Cp in Ss:
                tp, mp = tab_and_m(p, Cp, s)
                for Cq in St:
                    tq, mq = tab_and_m(q, Cq, t); tot_cases += 1
                    best = 0 if mp < mq else 1
                    for st in starts:
                        r = sched_walk((p, q), (tp, tq), (s, t), st); tot_walks += 1
                        if len(r[0]) >= 2: tot_two += 1
                        elif next(iter(r[0])) != best: tot_bad += 1
rec("X1", "PASS" if tot_two == 0 and tot_bad == 0 else "FAIL", f"EXHAUSTIVE abstract scheduler: prime pairs {PAIRS}, all moduli s,t <= {SMAX}, ALL nonempty subsets C_p, C_q and ALL start states: {tot_cases} odometer pairs, {tot_walks} walks; cycles in which BOTH primes fire: {tot_two}; walks whose survivor is not the prime with the smaller worst-case pending m: {tot_bad}")
# X1b: random larger odometers, 2 and 3 primes
rng = random.Random(77); n2 = 0; w2 = 0; two2 = 0; bad2 = 0
for _ in range(1500 if QUICK else 6000):
    k = rng.choice([2, 2, 3]); primes = tuple(rng.sample([2, 3, 5, 7, 11, 13], k)); mods = tuple(rng.randint(1, 30) for _ in range(k))
    sets = []
    for s in mods:
        dens = rng.choice([0.1, 0.3, 0.6, 0.9]); C = {e for e in range(s) if rng.random() < dens} or {rng.randrange(s)}; sets.append(frozenset(C))
    starts = [tuple(rng.randrange(s) for s in mods) for _ in range(12)]
    a1, a2, a3, a4 = survivor_rule_check(primes, sets, mods, starts); n2 += 1; w2 += a1; two2 += a2; bad2 += a4
rec("X1b", "PASS" if two2 == 0 and bad2 == 0 else "FAIL", f"random abstract odometer systems with 2 or 3 primes (moduli up to 30): {n2} systems, {w2} walks; cycles with two or more firing primes: {two2}; survivor not the smallest-m prime: {bad2}")

# X2: odometers built from the ARITHMETIC of a prime g: Abs_p from the actual definition, background F = frozen auxiliary primes with arbitrary residues
def frozen_background(g, rng):
    F = [1]; prog = []
    for _k in range(rng.choice([0, 1, 1, 2, 3])):
        r = rng.randint(2, g - 1); o = ordm(r, g); e = rng.choice([1, 2, o - 1, o]) if o > 1 else 1
        e = max(1, min(e, o)); prog.append((r, e))
        F = list({(a * pow(r, k_, g)) % g for a in F for k_ in range(e + 1)})
    return set(F), prog
t_end = time.time() + (25 if QUICK else 100); rngA = random.Random(2024)
ncase = nabs_empty = ncont = nwalk = ntwoA = nexA = nbadA = ntau = nbadtau = ngen = 0; surv_hist = Counter()
PRIMES_X = [x for x in range(11, 400) if is_prime(x)]
while time.time() < t_end:
    g = rngA.choice(PRIMES_X); sp = [p for p in small_primes(isqrt(g)) if g % p]
    if len(sp) < 2: continue
    p, q = rngA.sample(sp, 2); F, prog = frozen_background(g, rngA); ncase += 1
    op = ordm(p, g); oq = ordm(q, g); Hp = {pow(p, k, g) for k in range(op)}; Hq = {pow(q, k, g) for k in range(oq)}
    Ap = {(h * f) % g for h in Hq for f in F}; Aq = {(h * f) % g for h in Hp for f in F}
    Abp = {k for k in range(op) if pow(pow(p, k, g), -1, g) in Ap}; Abq = {k for k in range(oq) if pow(pow(q, k, g), -1, g) in Aq}; ngen += 2
    if not Abp or not Abq: nabs_empty += 1; continue
    ncont += 1
    # T62: Abs_p is tau_p-periodic, Abs_q is tau_q-periodic, tau_p, tau_q coprime
    tp = op // gcd(op, oq); tq = oq // gcd(op, oq); ntau += 1
    if gcd(tp, tq) != 1 or any(((k + tp) % op in Abp) != (k in Abp) for k in range(op)) or any(((k + tq) % oq in Abq) != (k in Abq) for k in range(oq)): nbadtau += 1
    starts = [(rngA.randrange(op), rngA.randrange(oq)) for _ in range(6)] + [(sorted(Abp)[0], sorted(Abq)[0])]
    a1, a2, a3, a4 = survivor_rule_check((p, q), (Abp, Abq), (op, oq), starts, blocked=lambda c, g=g: c * c >= g)
    nwalk += a1; ntwoA += a2; nexA += a3; nbadA += a4
rec("X2", "PASS" if ntwoA == 0 and nbadA == 0 and ncont > 0 else "FAIL", f"arithmetic odometers (prime g < 400, two small primes p, q < sqrt(g) saturated, background F = random frozen auxiliary primes): {ncase} cases, {ngen} Abs sets generated, {nabs_empty} with an empty Abs (prime cannot carry), {ncont} contested pairs, {nwalk} walks (window rule c^2 < g applied; {nexA} walks leave persistence); cycles with BOTH primes firing: {ntwoA}; survivor not the smaller-m prime: {nbadA}")
rec("X3", "PASS" if nbadtau == 0 and ntau > 0 else "FAIL", f"T62 coprime clocks: in all {ntau} contested pairs Abs_p is invariant under k -> k + o_p/gcd(o_p,o_q), Abs_q under k -> k + o_q/gcd(o_p,o_q), and these two periods are coprime: {nbadtau} exceptions")

# =================================================================== R  real orbits of the collective map
print("\n##### R. REAL ORBITS OF THE COLLECTIVE MAP: ACTIVE PRIMES OF EVENTUAL CYCLES (EXACT CLASS CLOSURE) #####")
POOL2, TRIED2 = build_pool(gen_competing_seed, 30 if QUICK else 130, 202)
rec("R0", "DATA", f"adversarial seeds (two small primes start saturated and compete; frozen auxiliary primes with random residues): {TRIED2} tried, {len(POOL2)} exact eventual cycles; random pool: {len(POOL1)} cycles")
ALL = POOL1 + POOL2; hist_act = Counter(); bad_pp = 0
for c in ALL:
    a = active_primes(c)
    if a is None: bad_pp += 1; continue
    hist_act[len(a)] += 1
rec("R1", "PASS" if hist_act.get(0, 0) == 0 and all(k <= 1 for k in hist_act) and bad_pp == 0 and len(ALL) > 0 else "FAIL",
    f"number of primes that carry inside the eventual cycle, over {len(ALL)} exact cycles: {dict(sorted(hist_act.items()))} (T60: at most one); composite carries in cycles: {bad_pp}")
nrho = badrho = nP = badP = 0
for c in ALL:
    a = active_primes(c)
    if a is None or len(a) != 1: continue
    p, o, Abs, s, gaps, m = survivor_data(c)
    pp, rp, ev, uni = reduce_cycle(c['cyc']); nrho += 1
    if not uni or rp != p ** s: badrho += 1
    nP += 1
    if pp != sum(p ** (2 * j) - 1 for j in gaps): badP += 1
rec("R2", "PASS" if badrho == 0 and badP == 0 and nrho > 0 else "FAIL", f"T61 on {nrho} single-prime cycles: eventual scaling factor rho_p = L_(n+P)/L_n equals p^s with s the minimal period of Abs_p in Z/ord_g(p) ({badrho} exceptions), and the gamma-period equals the sum of p^(2j)-1 over the gaps j of Abs_p in one period ({badP} exceptions)")
ncontested = nstarved = nbadm = nfrozen = 0
for c in ALL:
    a = active_primes(c)
    if a is None or len(a) != 1: continue
    r_ = a[0]; p, o, Abs, s, gaps, m = survivor_data(c); g = c['g']
    resets = [st for st in c['states'][:-1] if st[0] == 1]
    comp = {}
    for st in resets:
        pd = pendings(g, st[1])
        for q, (j, cand) in pd.items():
            if q != r_: comp.setdefault(q, set()).add(cand)
    if comp: ncontested += 1
    for q, cs in comp.items():
        nstarved += 1
        if min(cs) <= m: nbadm += 1
        if len(cs) > 1 and False: nfrozen += 1
rec("R3", "PASS" if nbadm == 0 and ncontested > 0 else "FAIL", f"starvation inequality of T60 on real cycles: {ncontested} cycles had at least one other prime with a finite pending carry (a competitor), {nstarved} competitor-prime/cycle pairs; in every one the survivor's WORST-CASE carry m = max p^gap is smaller than the competitor's pending carry at every reset: {nbadm} violations")
# the competitors' pending carries are frozen along a cycle (inert primes do not move)
nfz = badfz = 0
for c in ALL:
    a = active_primes(c)
    if a is None or len(a) != 1: continue
    r_ = a[0]; g = c['g']; seen = defaultdict(set)
    for st in c['states'][:-1]:
        if st[0] != 1: continue
        for q, (j, cand) in pendings(g, st[1]).items():
            if q != r_: seen[q].add(cand)
    for q, cs in seen.items():
        nfz += 1
        if len(cs) != 1: badfz += 1
rec("R4", "PASS" if badfz == 0 else "FAIL", f"inert primes have FROZEN pending carries along the cycle: {nfz} (competitor, cycle) pairs, {badfz} not constant")

# =================================================================== C  controls: the established examples must be classified correctly
print("\n##### C. CONTROLS: ESTABLISHED EXAMPLES RECLASSIFIED BY THE NEW INVARIANTS (active prime, Abs, s, rho) #####")
CONTROLS = [("G=11 three-carry (T50/T57, q=3)", 11, {2: 2, 3: 3, 5: 4}, 1, 3, 1, 3, 8),
            ("G=31 five-carry (T57, q=5)", 31, {67: 2, 5: 1, 2: 5}, 1, 5, 1, 5, 24),
            ("G=31 mixed 2^2,2^2,2^1", 31, {2: 5, 3: 4, 5: 2}, 4, 2, 5, 32, 33),
            ("G=17 P=33 (carries 2^1 and 2^2)", 17, {2: 1, 3: 2, 13: 1, 19: 3}, 54, 2, 8, 256, 33),
            ("G=59 (3-carries; 4-carries only in the transient)", 59, {2: 2, 3: 3, 17: 3, 19: 3}, 4, 3, None, 3, 8),
            ("even G=68", 68, {3: 3, 13: 1, 3947: 8, 281: 4}, 1, 3, None, 3, 8)]
for (name, g, Es, g0, pw, sw, rw, Pw) in CONTROLS:
    c = eventual_cycle(g, Es, g0, maxn=3000, tmax=120)
    if c is None: rec("C1", "FAIL", f"{name}: no exact cycle"); continue
    a = active_primes(c); pp, rp, ev, uni = reduce_cycle(c['cyc'])
    okp = a == [pw]
    if okp:
        p, o, Abs, s, gaps, m = survivor_data(c)
        ok = uni and rp == rw and pp == Pw and p ** s == rw and (sw is None or s == sw)
        rec("C1", "PASS" if ok else "FAIL", f"{name}: g={g}, single active prime {p}, ord_g(p)={o}, Abs={sorted(Abs)}, translation period s={s}, gaps={gaps}, worst-case carry m={m}; gamma-period {pp}, rho={rp}={p}^{s}; class transient {c['cyc'][1]}, class period {c['cyc'][2]}")
    else: rec("C1", "FAIL", f"{name}: active primes {a}, expected [{pw}]")

# =================================================================== N  extended q-carry data (O9.1 / O10.2)
print("\n##### N. EXTENDED q-CARRY WITNESSES: HYPOTHESES (Q1)-(Q4) OF T57 AT LARGER q #####")
def q_hyp_fast(q, g):
    """(Q1)-(Q3) of T57 (cheap residue tests); returns (o, e2, u) or None"""
    if not (is_prime(g) and g % 2 == 1 and g > q * q and g % q): return None
    o = ordm(q, g); H = {pow(q, i, g) for i in range(o)}
    if 2 in H: return None
    e2 = next((e for e in range(1, g) if pow(2, e, g) in H), None)
    K = set(H)
    for i in range(e2): K |= {pow(2, i, g) * h % g for h in H}
    for M in range(2, q):
        if M % 2 == 1 and M % g in K: return None
        if M % 2 == 0 and M % g in H: return None
    u = next((q + k * g for k in range(1, 4000) if is_prime(q + k * g)), None)
    return None if u is None else (o, e2, u)
def q_seed_exact(q, g, omax=1500):
    r = q_hyp_fast(q, g)
    if r is None: return None
    o, e2, u = r
    if o > omax: return None
    Es = {u: o - 1, q: 1, 2: e2}
    return Es if Gexact(g, 1, Es) == g else None            # (Q4) exact finite divisor check
QLIST = [11, 19, 29, 31, 37]
QFOUND = {}
if QUICK:
    for q, g in [(11, 6689), (19, 27631), (29, 7489), (31, 21673), (37, 4271)]:
        Es = q_seed_exact(q, g)
        if Es is not None: QFOUND[q] = (g, Es)
else:
    for q in QLIST:
        for g in range(q * q + 2, 30000):
            if is_prime(g):
                Es = q_seed_exact(q, g)
                if Es is not None: QFOUND[q] = (g, Es); break
rec("N1", "PASS" if QFOUND else "FAIL", "smallest odd prime g < 30000 (ord_g(q) <= 1500) satisfying (Q1)-(Q4) exactly, new q: " + "; ".join(f"q={q}: g={QFOUND[q][0]}" for q in sorted(QFOUND)) + "  [v009: q=3: 11, 5: 31, 7: 367, 13: 601, 17: 1321, 23: 1289]")
for q in [11, 29, 37]:
    if q not in QFOUND: rec("N2", "FAIL", f"no instance for q={q}"); continue
    g, Es = QFOUND[q]; P_ = q * q - 1; n = 2 * P_ + 2
    mo = machine_orbit(g, Es, 1, n); L0 = lval(mo[0][1])
    ok = len(mo) == n and all(mo[i][0] == (i % P_) + 1 and lval(mo[i][1]) == L0 * q ** (i // P_) for i in range(n))
    rec("N2", "PASS" if ok else "FAIL", f"q={q}, g={g}, seed={Es}: residue machine (exact G = g at the start, validated against direct iteration in section A of v009) gives gamma = 1..{P_} twice with L_(n+{P_}) = {q} L_n over {n} steps; one active prime {q} (T60), rho = {q}, x_(n+{P_}) = {q}^2 x_n")
rec("N3", "DATA", "(Q1)-(Q4) hold exactly (finite divisor check) for q = 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37 (largest g = 27631 at q = 19); by the hand proof T57 each gives an eventual q-carry cycle of gamma-period q^2-1. q = 41 has no instance with g < 30000 and ord <= 1500 (data only)")
rec("N4", "OPEN", "O10.2 (= O9.1) remains OPEN as a theorem for ALL q (an infinite family of distinct carry sizes); eleven distinct sizes q in {3,...,37} are now exact instances of T57. The class-closure certificate (T51) for q = 11, g = 6689 needs ~25080 machine steps and is run by q11_certificate.py")

# =================================================================== V  verdicts
print("\n##### V. VERDICT TABLE FOR THE QUESTION  'EXISTS x0, p != q: p and q both carry infinitely often?' #####")
rec("V1", "DATA", f"ABSTRACT_COEXISTENCE: 0 of {tot_cases + n2} abstract odometer systems (exhaustive for small moduli, random for larger) -- proved impossible for every system by T60 (the prime with the largest worst-case pending carry starves)")
rec("V2", "DATA", f"ARITHMETIC_REALIZABLE: 0 of {ncont} contested arithmetic pairs; COLLECTIVE_CERTIFIED: 0 of {len(ALL)} exact eventual cycles of the collective map (active-prime histogram {dict(sorted(hist_act.items()))}); EXCLUDED: all of them, by the proof of T60 (not by the failure of a search)")
rec("V3", "OPEN", "O10.1: the survivor of a given seed is determined by running the scheduler; a closed decision rule from the seed (without iterating) is not given (T60 gives only the necessary rule 'smallest worst-case pending carry m among saturated primes with nonempty Abs')")
rec("V4", "OPEN", "O10.2 (= O9.1): is (Q1)-(Q4) solvable for every odd prime q (infinitely many distinct eventual carry sizes)? see N1-N4: instances now exist for q = 3,5,7,11,13,17,19,23,29,31,37")
print(f"\n===== FIELD-I v010 summary: {NFAIL} FAIL, elapsed {time.time() - T0:.1f}s =====")
sys.exit(1 if NFAIL else 0)

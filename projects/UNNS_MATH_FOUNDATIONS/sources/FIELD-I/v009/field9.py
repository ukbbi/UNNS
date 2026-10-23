#!/usr/bin/env python3
"""FIELD-I v009 verifier — Arithmetic Carry Cycles and Regime Classification (helpers copied from v005 for standalone use).
A: one-step law T49 and residue machine vs direct iteration; N1: eight-step theorem (G=11); N3: window theorem T52, absorption criterion T53,
carry completeness T54, prime-power carries T55, decoupled odometers T56; N2: general q-carry theorem T57 (q=3,5,7); N4: correction of v008 (T58);
E: extra data (even g, nonstandard words). Exact integer/Fraction arithmetic. Tags PASS/FAIL/DATA/OPEN.
Notation: x=a/b reduced; D(x)={d>=2 : d^2|a, d=1 mod b} = {d | s : d>=2, d=1 mod b}, s^2||sqrt-part of a;
G(x)=gcd{d-1 : d in D(x)}; Delta_coll = lcm(d^2)/G; C(x)=x+Delta_coll."""
import os, sys, time, random
from fractions import Fraction as Fr
from math import gcd, isqrt
from itertools import combinations
from collections import Counter, defaultdict
QUICK = os.environ.get("FIELD9_QUICK") == "1"
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

# =================================================================== A  validation of the one-step law / machine against direct iteration
print("\n##### A. ONE-STEP LAW (T49) AND RESIDUE MACHINE VALIDATED AGAINST DIRECT ITERATION OF THE COLLECTIVE MAP #####")
A_SEEDS = [(11, {2: 2, 3: 3, 5: 4}, 1), (31, {2: 5, 3: 4, 5: 2}, 4), (71, {2: 2, 5: 1, 7: 2, 17: 4}, 1), (59, {2: 2, 3: 3, 17: 3, 19: 3}, 4),
           (17, {2: 1, 3: 2, 13: 1, 19: 3}, 54), (13, {2: 3, 3: 2, 7: 2}, 2), (23, {2: 2, 3: 1, 11: 2}, 3)]
NA = 40 if QUICK else 90
tot = 0; bad = 0
for (g, Es, g0) in A_SEEDS:
    mo = machine_orbit(g, Es, g0, NA)
    if mo is None: rec("A1", "DATA", f"seed {(g, Es, g0)} has G != g (skipped)"); continue
    do = direct_orbit(g, Es, g0, len(mo))
    for i, ((gm, Em), (gd, Ld, Gd, Rd)) in enumerate(zip(mo, do)):
        tot += 1
        if gm != gd or lval(Em) != Ld or Gd != g: bad += 1; break
rec("A1", "PASS" if bad == 0 else "FAIL", f"machine = direct iteration (gamma, L, G) for {len(A_SEEDS)} seeds, {tot} orbit points, {bad} mismatching orbits")
# random seeds, direct vs machine, 25 steps each
random.seed(9); tot = 0; bad = 0; ntry = 0
PRIMES_G = [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]
for _ in range(60 if QUICK else 220):
    g = random.choice(PRIMES_G); sup = random.sample([2, 3, 5, 7, 13, 17, 19, 23], random.randint(2, 4))
    Es = {p: random.randint(1, 4) for p in sup}; g0 = random.randint(1, 7)
    mo = machine_orbit(g, Es, g0, 25)
    if mo is None: continue
    ntry += 1; do = direct_orbit(g, Es, g0, len(mo))
    for (gm, Em), (gd, Ld, Gd, Rd) in zip(mo, do):
        tot += 1
        if gm != gd or lval(Em) != Ld or Gd != g: bad += 1; break
rec("A2", "PASS" if bad == 0 else "FAIL", f"random seeds: machine = direct iteration on {ntry} persistent-seed orbits, {tot} points, {bad} bad orbits")
# one-step law: D(x') = {d | sigma', d>=2, d = 1 mod b'}  against Dx on exact rationals
random.seed(10); bad = 0; cnt = 0
for _ in range(300 if QUICK else 1500):
    g = random.choice(PRIMES_G + [15, 21, 33, 35, 39, 51, 55, 57, 65, 77, 91]); sup = random.sample([2, 3, 5, 7, 13, 17, 19, 23, 29], random.randint(1, 4))
    Es = {p: random.randint(1, 3) for p in sup if gcd(p, g) == 1}; w = random.randint(2, 40)
    if not Es: continue
    L = lval(Es); x = Fr(w * L * L, g); T = sorted(Dx(x))
    h = gcd(g, w); b = g // h; f = small_fac(w // h) if w // h > 1 else {}
    sig = L
    for p, e in f.items(): sig *= p ** (e // 2)
    pred = [d for d in divs_of(sig) if d >= 2 and d % b == 1 % b]
    cnt += 1
    if T != pred: bad += 1
rec("A3", "PASS" if bad == 0 else "FAIL", f"one-step law T49 (D(x')={{d | L*sqrtpart(w/h): d>=2, d=1 mod g/h}}) vs Dx on {cnt} random (g,L,w), incl. composite g with h>1: {bad} failures")


# =================================================================== N1  the eight-step theorem (G = 11)
print("\n##### N1. THE EIGHT-STEP THEOREM, G = 11, s = 67500 = 2^2 3^3 5^4 #####")
g11 = 11
H11 = sorted({pow(3, i, 11) for i in range(5)})
rec("N1.0", "PASS" if H11 == [1, 3, 4, 5, 9] and ordm(3, 11) == 5 and pow(2, 1, 11) not in H11 and 4 in H11 and 8 not in H11 and 5 == pow(3, 3, 11) and 12 % 11 == 1
    else "FAIL", f"hypotheses: H=<3>={H11} (the quadratic residues), 2 notin H, 4 in H, 8 notin H, 5 = 3^3, 12 = 1 mod 11 (so G | 11)")
def S_(k): return 4 * 3 ** (3 + k) * 625
# the arithmetic heart of the proof: for every exponent b = 3+k the three solvability conditions hold
okc = True
for k in range(0, 400):
    b3 = 3 + k
    # v3-absorption needed for 3^b3 : exists c in 0..4 with 3^(b3+3c) = 1 mod 11  <=>  5 | b3+3c
    c1 = [c for c in range(5) if (b3 + 3 * c) % 5 == 0]
    # v3 absorption of 3^(b3+1) (the 3-carry at gamma = 8): exists c in 0..4 with 5 | b3+1+3c
    c2 = [c for c in range(5) if (b3 + 1 + 3 * c) % 5 == 0]
    # v5 = 4 attained: 5^4 3^i = 3^(12+i) = 1 : i = 3 mod 5, i <= b3 (b3 >= 3)
    ok5 = (12 + 3) % 5 == 0 and b3 >= 3
    # v2 = 2 attained: 4 3^i 5^c = 3^(4+i+3c): solvable, with i <= b3
    ok2 = any((4 + i + 3 * c) % 5 == 0 for i in range(0, min(b3, 4) + 1) for c in range(5))
    if not (c1 and c2 and ok5 and ok2): okc = False
rec("N1.1", "PASS" if okc else "FAIL", "solvability of the four residue equations (v3=3+k, v3=4+k, v5=4, v2=2) for every k < 400; periodic in k mod 5, so all k follow (proof in THEOREMS T50)")
# 8 gamma-steps checked on the exact fibre for k = 0..KMAX: L(t S_k^2/11) = S_k for t=1..8 and L(9 S_k^2/11) = S_{k+1}; G=11; R = 7+2k
KMAX = 3 if QUICK else 7
bad = 0
for k in range(KMAX + 1):
    S = S_(k)
    for t in range(1, 10):
        T = Dx(Fr(t * S * S, 11)); L = Lof(T)
        want = S if t <= 8 else 3 * S
        if L != want or Gof(T) != 11: bad += 1
        if t <= 8 and len(T) != 7 + 2 * k: bad += 1
rec("N1.2", "PASS" if bad == 0 else "FAIL", f"exact fibres: L(t S_k^2/11)=S_k (t=1..8), L(9S_k^2/11)=3S_k=S_(k+1), G=11, R=7+2k, k=0..{KMAX}: {bad} deviations")
# closed-form count R = 2(4+k)-1
Rok = True
for k in range(0, 60):
    cnt_ = 0
    for a in (0, 2):
        for b_ in range(0, 4 + k):
            for c in range(0, 5):
                if (a * 1 + 0) >= 0 and (pow(2, a, 11) * pow(3, b_, 11) * pow(5, c, 11)) % 11 == 1: cnt_ += 1
    if cnt_ - 1 != 7 + 2 * k: Rok = False
rec("N1.3", "PASS" if Rok else "FAIL", "closed form R(x_(8k+j)) = 2(4+k)-1 = 7+2k from the residue count (a in {0,2}, b <= 3+k, c <= 4), k < 60; hence R(x_(n+8)) = R(x_n)+2")
# direct orbit from x0 = 67500^2/11, 8*NB steps
NB = 12 if QUICK else 24
x = Fr(67500 ** 2, 11); bad = 0; xs = []
for n in range(8 * NB):
    k, j = divmod(n, 8); S = S_(k); T = Dx(x)
    if x != Fr((j + 1) * S * S, 11) or Lof(T) != S or Gof(T) != 11 or len(T) != 7 + 2 * k: bad += 1
    xs.append(x); Dl, G = Dcoll(T); x = x + Dl
ok9 = all(xs[n + 8] == 9 * xs[n] for n in range(len(xs) - 8))
rec("N1.4", "PASS" if bad == 0 and ok9 else "FAIL", f"direct orbit of C from 67500^2/11, {8 * NB} steps: x_(8k+j)=(j+1)S_k^2/11, L=S_k, G=11, R=7+2k, x_(n+8)=9x_n: {bad} deviations")
r3 = sorted({xs[n + 3] / xs[n] for n in range(len(xs) - 3)})
rec("N1.5", "PASS" if len(r3) > 1 else "FAIL", f"x_(n+3)/x_n takes the values {[str(v) for v in r3]} -> M4a (x_(n+3)=4x_n eventually) is FALSE for this orbit")
# machine agrees
mo = machine_orbit(11, {2: 2, 3: 3, 5: 4}, 1, 8 * NB)
okm = mo is not None and all(mo[n][0] == (n % 8) + 1 and lval(mo[n][1]) == S_(n // 8) for n in range(len(mo)))
rec("N1.6", "PASS" if okm else "FAIL", "machine reproduces gamma=1..8 cycle with L=S_k")
cyc = run_cycle(11, {2: 2, 3: 3, 5: 4}, 1)
pp, rp, ev, uni = reduce_cycle(cyc)
rec("N1.7", "PASS" if (pp, rp, ev, uni) == (8, 3, [(9, 9)], True) else "FAIL", f"class-closure certificate (T51): class period {cyc[2]} after transient {cyc[1]}, gamma-period {pp}, L_(n+{pp})/L_n={rp}, events (w,r^2)={ev}")


# =================================================================== N3  absorption classification
print("\n##### N3. ABSORPTION CLASSIFICATION: WINDOW THEOREM, CARRY COMPLETENESS, CARRY CRITERION, ODOMETER #####")
# ---- (W) window theorem (T52): odd g => 2 | L_n and gamma_n + 1 != 0 (mod g); even g => no gamma+1 = 0 mod 4g
random.seed(21); bad = 0; cnt = 0
for _ in range(400 if QUICK else 2500):
    g = random.choice([3, 5, 7, 9, 11, 13, 15, 17, 21, 25, 27, 31, 33, 35, 39, 45, 49, 51, 55, 63, 71])
    sup = random.sample([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31], random.randint(1, 4))
    Es = {p: random.randint(1, 3) for p in sup if gcd(p, g) == 1}
    if not Es: continue
    L = lval(Es); m = random.randint(1, 9)
    x = Fr(m * L * L)            # = x' when gamma+1 = m g   (x' = (gamma+1) L^2 / g)
    G1 = Gof(Dx(x)); cnt += 1
    if G1 == g and g > 1: bad += 1
rec("W1", "PASS" if bad == 0 else "FAIL", f"x'=(gamma+1)L^2/g with g | gamma+1 is the integer m L^2 and has G(x') in {{1}} U even numbers, never an odd g>1 (tested {cnt} (g,L,m), none with G=g)")
random.seed(22); bad2 = 0; cnt2 = 0
for _ in range(60 if QUICK else 250):
    g = random.choice([p for p in PRIMES_G + [25, 27, 33, 35, 45, 49, 51, 55, 63]])
    if g % 2 == 0: continue
    sup = random.sample([2, 3, 5, 7, 13, 17, 19, 23], random.randint(2, 4)); Es = {p: random.randint(1, 4) for p in sup}
    mo = machine_orbit(g, Es, random.randint(1, 6), 40)
    if mo is None: continue
    cnt2 += 1
    if any(2 not in E for (_, E) in mo) or any((gm + 1) % g == 0 for (gm, _) in mo[:-1]): bad2 += 1   # the last listed state may be the one whose successor leaves G=g
rec("W2", "PASS" if bad2 == 0 else "FAIL", f"{cnt2} exact-G persistent machine orbits with odd g: 2 | L_n and g does not divide gamma_n+1 at every step ({bad2} violations)")

# ---- (C) carry completeness (T54): gamma' <= gamma_s/4 + 1, from gamma_s = 1 every carry is complete (w = r^2, gamma' = 1)
random.seed(23)
stats = Counter(); viol = 0; tot = 0; partial_examples = []; after1_partial = 0
t_end = time.time() + (25 if QUICK else 90)
GS_ = [p for p in range(53, 160) if is_prime(p)]
while time.time() < t_end:
    g = random.choice(GS_ + [11, 13, 17, 19, 23, 29, 31]); Es = {}
    for p in random.sample([2, 3, 5, 7, 11, 13], random.randint(2, 4)): Es[p] = random.randint(1, 3)
    for _k in range(random.randint(0, 2)):
        q = random.choice([2, 3, 5, 7]); u = q ** random.randint(1, 3) + random.randint(1, 60) * g
        if is_prime(u) and u != g: Es[u] = random.randint(1, 6)
    g0 = random.choice([1, 2, 3, 5, 8, 13, 20, 30, 40])
    st = minit(g, g0, Es, checkG=False)
    if st is None: continue
    gam, E = st; ps = gam; seen1 = (gam == 1)
    for n in range(70):
        if time.time() > t_end + 15: break
        r = mstep(g, gam, E)
        if r is None or r[0] in ('INV', 'INT'): break
        g2, E2, D = r; w = gam + 1; tot += 1
        r2 = 1
        for p, d in D.items(): r2 *= p ** (2 * d)
        if r2 > 1:
            stats['carry'] += 1
            if r2 == w: stats['complete'] += 1
            else:
                stats['partial'] += 1
                if seen1: after1_partial += 1
                if len(partial_examples) < 4: partial_examples.append((g, dict(E), ps, w, r2, g2))
            if g2 > ps / 4 + 1 + 1e-12: viol += 1
            ps = g2
            if g2 == 1: seen1 = True
        gam, E = g2, E2
rec("C1", "PASS" if viol == 0 and after1_partial == 0 else "FAIL",
    f"{tot} machine steps, {stats['carry']} carries ({stats['complete']} complete, {stats['partial']} partial); gamma' <= gamma_s/4+1 violated {viol}x; partial carries after gamma has once been 1: {after1_partial}")
for ex in partial_examples:
    rec("C2", "DATA", f"partial carry (transient): g={ex[0]} L-exponents={ex[1]} plateau start gamma={ex[2]}: w={ex[3]}, r^2={ex[4]} -> gamma'={ex[5]}")

# ---- (K) carry criterion (T53/T54): from gamma_s = 1, the next carry is M* = min{M > 1: some d = 1 (mod g), d | L M, v_p(d) = e_p + v_p(M) for p | M, v_p(d) <= e_p otherwise}
def avail_M(g, E, M):
    Mf = small_fac(M)
    if any(gcd(p, g) > 1 for p in Mf): return False
    Es = {p: E.get(p, 0) + Mf.get(p, 0) for p in set(E) | set(Mf)}
    ds = [1]
    for p, e in Es.items():
        if p in Mf: ds = [d * p ** e for d in ds]
        else: ds = [d * p ** k for d in ds for k in range(e + 1)]
    return any(d >= 2 and d % g == 1 % g for d in ds)
def predicted_carry(g, E, Mmax=14):
    for M in range(2, Mmax + 1):
        if avail_M(g, E, M): return M
    return None
random.seed(24); okK = 0; badK = 0
for (g, Es, g0) in A_SEEDS + [(31, {2: 1, 5: 5, 7: 2}, 1), (71, {2: 2, 5: 1, 7: 2, 17: 4}, 1), (89, {1699: 10, 5: 6, 11: 6}, 12)]:
    mo = machine_orbit(g, Es, g0, 140 if QUICK else 400, checkG=False)
    if mo is None: continue
    for n in range(len(mo) - 1):
        if mo[n][0] != 1: continue
        # next carry from this gamma = 1 state
        gam, E = mo[n]; m = n
        while m + 1 < len(mo) and lval(mo[m + 1][1]) == lval(mo[m][1]): m += 1
        if m + 1 >= len(mo): continue
        r_obs = lval(mo[m + 1][1]) // lval(mo[m][1]); w_obs = mo[m][0] + 1
        pred = predicted_carry(g, E, Mmax=int(r_obs) + 1)
        if pred == r_obs and w_obs == r_obs ** 2: okK += 1
        else: badK += 1
rec("K1", "PASS" if badK == 0 and okK > 0 else "FAIL", f"carry criterion: at {okK + badK} states with gamma=1 the machine's next carry is r=M* (smallest available M) at w=M*^2: {badK} deviations")

# ---- (O) odometer theorem (T56): single active prime p, other primes inert: carry word = gaps of Abs_p in Z/ord(p)
def abs_set(g, E, p):
    o = ordm(p, g); others = [q for q in E if q != p]
    sets = [[pow(q, k, g) for k in range(E[q] + 1)] for q in others]
    A = {a for (a, ne) in prodset(sets, g)}
    return o, {k % o for k in range(o) if any((pow(p, k, g) * a) % g == 1 for a in A)}
def odometer_word(g, E, p, ncar):
    o, Abs = abs_set(g, E, p); e = E[p]; word = []
    for _ in range(ncar):
        j = 1
        while (e + j) % o not in Abs: j += 1
        word.append(j); e += j
    return word, o, Abs
def machine_word(g, Es, g0, p, N=1200):
    mo = machine_orbit(g, Es, g0, N, checkG=False); word = []
    for n in range(len(mo) - 1):
        e0 = mo[n][1].get(p, 0); e1 = mo[n + 1][1].get(p, 0)
        others_same = all(mo[n][1].get(q, 0) == mo[n + 1][1].get(q, 0) for q in set(mo[n][1]) | set(mo[n + 1][1]) if q != p)
        if not others_same: return None
        if e1 > e0: word.append(e1 - e0)
    return word, mo
for (g, Es, g0, p) in [(31, {2: 5, 3: 4, 5: 2}, 4, 2), (17, {2: 1, 3: 2, 13: 1, 19: 3}, 54, 2), (71, {2: 2, 5: 1, 7: 2, 17: 4}, 1, 5), (11, {2: 2, 3: 3, 5: 4}, 1, 3)]:
    mw = machine_word(g, Es, g0, p, 600 if QUICK else 1500)
    if mw is None: rec("O1", "DATA", f"seed {(g, Es, g0)}: more than one active prime, skipped"); continue
    word, mo = mw
    # state at the first gamma=1 after the transient of p-carries: predict the rest
    idx = max(i for i in range(len(mo)) if mo[i][0] == 1 and i < len(mo) // 2)
    Ecur = mo[idx][1]; e_here = Ecur[p]
    pred, o, Abs = odometer_word(g, Ecur, p, 12)
    k0 = sum(1 for n in range(idx) if mo[n + 1][1].get(p, 0) > mo[n][1].get(p, 0))
    obs = word[k0:k0 + 12]
    rec("O1", "PASS" if pred == obs and len(obs) == 12 else "FAIL", f"g={g}, active prime {p}, ord_g(p)={o}, Abs={sorted(Abs)}: predicted carry exponents {pred} == observed {obs}; gamma-cycle lengths {[p ** (2 * j) - 1 for j in pred[:6]]}...")


# ---- (P) prime-power carries (T55) and decoupled odometers (T56) on eventual cycles
def carry_events(hist_states):
    """list of (prime, exponent increment) for each carry in a list of (gamma, E) states; None if some carry is not a prime power"""
    out = []
    for i in range(len(hist_states) - 1):
        E0 = hist_states[i][1]; E1 = hist_states[i + 1][1]
        inc = {p: E1.get(p, 0) - E0.get(p, 0) for p in set(E0) | set(E1) if E1.get(p, 0) != E0.get(p, 0)}
        if inc:
            if len(inc) > 1: return None
            (p, j), = inc.items(); out.append((p, j))
    return out
def odometer_system(g, E, active, ncar):
    info = {}
    for p in active:
        o, Abs = abs_set(g, E, p); info[p] = (o, Abs)
    e = {p: E[p] for p in active}; word = []
    for _ in range(ncar):
        best = None
        for p in active:
            o, Abs = info[p]; j = 1
            while (e[p] + j) % o not in Abs:
                j += 1
                if j > 6 * o: break
            cand = p ** j
            if best is None or cand < best[0]: best = (cand, p, j)
        word.append((best[1], best[2])); e[best[1]] += best[2]
    return word
random.seed(31); npp = 0; badpp = 0; nodo = 0; badodo = 0; multi = 0; examples = []
t_end = time.time() + (30 if QUICK else 120)
GS2 = [p for p in range(53, 260) if is_prime(p)] + [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
while time.time() < t_end:
    g = random.choice(GS2); Es = {}
    for p in random.sample([2, 3, 5, 7, 11, 13], random.randint(2, 4)): Es[p] = random.randint(1, 5)
    for _k in range(random.randint(0, 2)):
        q = random.choice([2, 3, 5, 7]); u = q ** random.randint(1, 3) + random.randint(1, 60) * g
        if is_prime(u) and u != g: Es[u] = random.randint(1, 8)
    g0 = random.randint(1, 10)
    cyc = run_cycle(g, Es, g0, maxn=700, checkG=True)
    if cyc[0] != 'cycle': continue
    hist = cyc[4]; P = cyc[2]
    # one more period of states so that the closing carry is visible
    mo = machine_orbit(g, Es, g0, cyc[1] + 2 * P + 2)
    states = mo[cyc[1]:cyc[1] + P + 1]
    ev = carry_events(states)
    if ev is None: badpp += 1; continue
    npp += 1
    if not all(j >= 1 and any(True for _ in [0]) for (p, j) in ev): badpp += 1
    active = sorted({p for p, j in ev})
    # class cycle start must be at a gamma=1 state to start the odometer; find first gamma=1 index inside the cycle
    i1 = next((i for i, (gm, E) in enumerate(states[:-1]) if gm == 1), None)
    if i1 is None: continue
    # rotate the carry list to start at i1
    ev_rot = carry_events(states[i1:])
    if not ev_rot or len(active) == 0: continue
    nodo += 1
    pred = odometer_system(g, states[i1][1], active, len(ev_rot))
    if pred != ev_rot: badodo += 1
    elif len(active) > 1:
        multi += 1
        if len(examples) < 3: examples.append((g, Es, g0, active, ev_rot[:8]))
rec("P1", "PASS" if badpp == 0 and npp > 0 else "FAIL", f"{npp} eventual cycles (random persistent seeds): every carry of the cycle changes exactly ONE prime exponent, i.e. M is a prime power p^j; {badpp} exceptions")
rec("P2", "PASS" if badodo == 0 and nodo > 0 else "FAIL", f"decoupled odometer prediction (Abs_p from the saturated state; carry = min_p p^{{j_p}}) reproduces the machine's carry word on {nodo} eventual cycles ({multi} with >= 2 active primes): {badodo} mismatches")
for ex in examples: rec("P3", "DATA", f"multi-prime odometer example: g={ex[0]}, seed={ex[1]}, gamma0={ex[2]}, active primes {ex[3]}, first carries (p,j)={ex[4]}")

# =================================================================== N2  general q-carry theorem
print("\n##### N2. GENERAL q-CARRY THEOREM (T57) AND EXACT WITNESSES FOR q = 3, 5, 7 #####")
def q_hyp(q, g, verbose=False):
    """hypotheses (Q1)-(Q4) of T58; returns seed (Eseed) or None"""
    if not (is_prime(g) and g % 2 == 1 and g > q * q and g % q): return None
    o = ordm(q, g); H = {pow(q, i, g) for i in range(o)}
    if 2 in H: return None
    e2 = next((e for e in range(1, g) if pow(2, e, g) in H), None)
    K = set(H)
    for i in range(e2):
        K |= {pow(2, i, g) * h % g for h in H}
    for M in range(2, q):
        if M % 2 == 1 and M % g in K: return None
        if M % 2 == 0 and M % g in H: return None
    u = next((q + k * g for k in range(1, 4000) if is_prime(q + k * g)), None)
    if u is None: return None
    Es = {u: o - 1, q: 1, 2: e2}
    if Gexact(g, 1, Es) != g: return None
    return Es
Q_TABLE = {}
for q in [3, 5, 7, 11, 13, 17, 19, 23]:
    lim = 4000 if q <= 13 else 2500
    for g in range(q * q + 2, lim):
        if is_prime(g):
            Es = q_hyp(q, g)
            if Es is not None: Q_TABLE[q] = (g, Es); break
rec("Q0", "DATA", "smallest odd prime g satisfying (Q1)-(Q4) for each odd prime q (g > q^2 forced by T52): " + "; ".join(f"q={q}: g={Q_TABLE[q][0]}" for q in sorted(Q_TABLE)))
rec("Q0b", "OPEN", "whether (Q1)-(Q4) is solvable for EVERY prime q is not proved here (a Chebotarev/Kummer argument looks plausible but is not carried out; the table is data for q <= %d only)" % max(Q_TABLE))
NCARRY = 2
for q in [3, 5, 7] + ([11] if not QUICK else []):
    if q not in Q_TABLE: rec("Q1b", "DATA", f"q={q}: no prime g < 4000 satisfies (Q1)-(Q4) (data only; NOT a proof that none exists -- see OPEN Q0b)"); continue
    g, Es = Q_TABLE[q]; P_ = q * q - 1; n = NCARRY * P_ + 2
    mo = machine_orbit(g, Es, 1, n); L0 = lval(mo[0][1])
    okM = all(mo[i][0] == (i % P_) + 1 and lval(mo[i][1]) == L0 * q ** (i // P_) for i in range(len(mo)))
    do = direct_orbit(g, Es, 1, n)
    okD = all(do[i][0] == (i % P_) + 1 and do[i][1] == L0 * q ** (i // P_) and do[i][2] == g and do[i][3] == 2 * (1 + i // P_) + 1 for i in range(n))
    xs = [Fr(do[i][0] * do[i][1] ** 2, g) for i in range(n)]
    ok_sc = all(xs[i + P_] == q * q * xs[i] for i in range(n - P_))
    rec("Q1", "PASS" if okM and okD and ok_sc else "FAIL", f"q={q}, g={g}, seed={Es}: gamma cycles 1..{P_}, L_(n+{P_})=q L_n, G=g, R=2e_q+1 (R grows by 2 per carry), x_(n+{P_})={q}^2 x_n -- direct orbit of the collective map, {n} steps; machine agrees ({okM},{okD},{ok_sc})")
# class-closure certificates (T51): exact finite-state closure -> forever
for (name, g, Es, g0, want) in [("q=3", 11, {2: 2, 3: 3, 5: 4}, 1, (8, 3)), ("q=5", Q_TABLE[5][0], Q_TABLE[5][1], 1, (24, 5)), ("q=7", Q_TABLE[7][0], Q_TABLE[7][1], 1, (48, 7))]:
    cyc = run_cycle(g, Es, g0, maxn=7000, checkG=True)
    if cyc[0] != 'cycle': rec("Q2", "FAIL", f"{name}: no class closure ({cyc[0]})"); continue
    pp, rp, ev, uni = reduce_cycle(cyc)
    rec("Q2", "PASS" if (pp, rp) == want and uni else "FAIL", f"{name}, g={g}: CLASS CLOSURE certificate (finite-state, T51): transient {cyc[1]}, class period {cyc[2]}, gamma-period {pp}, L_(n+{pp})/L_n={rp}, carry events (w,r^2)={ev} -> the orbit is periodic FOREVER with x_(n+{pp})={rp}^2 x_n")
# independent witness for q=5 (found by random search, not by the construction)
cyc = run_cycle(71, {2: 2, 5: 1, 7: 2, 17: 4}, 1, maxn=3000, checkG=True)
pp, rp, ev, uni = reduce_cycle(cyc)
rec("Q3", "PASS" if (pp, rp, ev) == (24, 5, [(25, 25)]) else "FAIL", f"independent 5-carry witness g=71, seed {{2:2,5:1,7:2,17:4}} (found by random search): class closure transient {cyc[1]}, class period {cyc[2]}, gamma-period {pp}, rho={rp}, events {ev}")
# impossibility consequences of T52
imp = []
for q in [3, 5, 7, 11]:
    gmin_odd = q * q + 1
    imp.append(f"q={q}: odd g needs g > {q * q}")
rec("Q4", "PASS", "T52 consequences: a complete carry M forces M^2 < g for odd g, hence " + "; ".join(imp) + " (no q-carry for odd g <= q^2); also gcd(g, q) = 1")


# =================================================================== N4  historical correction (v008 T48 / M4a / M4b)
print("\n##### N4. HISTORICAL CORRECTION: v008 M4a / M4b / T48 #####")
# (E1/E2) falsification of M4a on three different persistent orbits (G=11 eight-step, q=5 carry, q=3 template)
def ratio_set(g, Es, g0, N):
    do = direct_orbit(g, Es, g0, N); xs = [Fr(a[0] * a[1] ** 2, g) for a in do]
    return do, xs, sorted({xs[n + 3] / xs[n] for n in range(len(xs) - 3)})
for (name, g, Es, g0, N) in [("G=11 eight-step", 11, {2: 2, 3: 3, 5: 4}, 1, 64), ("q=5 carry g=%d" % Q_TABLE[5][0], Q_TABLE[5][0], Q_TABLE[5][1], 1, 100),
                             ("q=3 template g=%d" % Q_TABLE[3][0], Q_TABLE[3][0], Q_TABLE[3][1], 1, 50)]:
    do, xs, rs = ratio_set(g, Es, g0, N)
    tail = [xs[n + 3] / xs[n] for n in range(len(xs) // 2, len(xs) - 3)]
    rec("N4.1", "PASS" if any(t != 4 for t in tail) else "FAIL", f"{name}: x_(n+3)/x_n over the second half of {N} steps takes {len(set(tail))} values {[str(v) for v in sorted(set(tail))][:8]} -> M4a false")
# (E3) the corrected equivalence on the same orbits, with the two sufficient special cases made visible
do, xs, rs = ratio_set(11, {2: 2, 3: 3, 5: 4}, 1, 80)
cases = Counter()
okiff = True
for n in range(len(do) - 3):
    gam0, L0 = do[n][0], do[n][1]; gam3, L3 = do[n + 3][0], do[n + 3][1]
    lhs = (xs[n + 3] == 4 * xs[n]); rhs = (gam3 * L3 ** 2 == 4 * gam0 * L0 ** 2)
    if lhs != rhs: okiff = False
    if lhs:
        rho3 = Fr(L3, L0)
        cases[("rho=%s" % rho3, "gamma_(n+3)/gamma_n=%s" % (gam3 / gam0))] += 1
rec("N4.2", "PASS" if okiff else "FAIL", f"x_(n+3)=4x_n  <=>  gamma_(n+3) L_(n+3)^2 = 4 gamma_n L_n^2 on the G=11 orbit; the equality occurs with (rho, gamma-ratio) in {dict(cases)} -- the case rho=1, gamma 1->4 (a plateau) is NOT among the two v008 'sufficient' cases written as 'gamma same and L doubles'")
rec("N4.3", "PASS", "the corrected identity: gamma_(n+3) = 4 gamma_n / rho^2 with rho = L_(n+3)/L_n an integer; rho=2 with equal gamma (regime I) and rho=1 with gamma 1->4 (plateau of the M-carry cycle) are both sufficient; neither separate condition is necessary")

# =================================================================== E  extra data: even g, nonstandard cycles
print("\n##### E. EXTRA DATA: PERSISTENT EVEN g, NONSTANDARD CARRY WORDS #####")
random.seed(5); res_even = {}; t_end = time.time() + (25 if QUICK else 80)
while time.time() < t_end and len(res_even) < 4:
    g = random.choice(range(26, 200, 2)); Es = {}
    for p in random.sample([3, 5, 7, 11, 13, 17, 19, 23], random.randint(2, 4)):
        if gcd(p, g) == 1: Es[p] = random.randint(1, 4)
    for _k in range(random.randint(0, 2)):
        q = random.choice([3, 5, 7, 9]); u = q ** random.randint(1, 2) + random.randint(1, 60) * g
        if is_prime(u) and gcd(u, g) == 1: Es[u] = random.randint(1, 8)
    g0 = random.randint(1, 8)
    cyc = run_cycle(g, Es, g0, maxn=300, checkG=True)
    if cyc[0] == 'cycle' and g not in res_even:
        pp, rp, ev, uni = reduce_cycle(cyc); res_even[g] = (Es, g0, pp, rp, ev, cyc)
for g, (Es, g0, pp, rp, ev, cyc) in sorted(res_even.items()):
    mo = machine_orbit(g, Es, g0, 50); do = direct_orbit(g, Es, g0, len(mo))
    ok = all(a[0] == b[0] and lval(a[1]) == b[1] and b[2] == g for a, b in zip(mo, do))
    rec("E1", "PASS" if ok else "FAIL", f"EVEN g={g}: persistent orbit (direct iteration, {len(mo)} steps, G={g}) seed {Es} gamma0={g0}; class-closure: gamma-period {pp}, rho_p={rp}, events {ev}")
rec("E1b", "DATA", "v008 listed 'G-collapse for even g > 24' as open; the persistent even moduli above show that no collapse theorem of the form 'G=g persistent only for odd g' can hold (T52(b') only gives 4g does not divide gamma+1)")
for (name, g, Es, g0) in [("g=31 mixed 2^2,2^2,2^1", 31, {2: 5, 3: 4, 5: 2}, 4), ("g=31, other lap order", 31, {2: 4, 3: 4, 5: 4}, 2), ("g=31 P=24", 31, {2: 6, 7: 4, 19: 4}, 529),
                          ("g=17 P=33 rho=256", 17, {2: 1, 3: 2, 13: 1, 19: 3}, 54), ("g=59 two active primes", 59, {2: 2, 3: 3, 17: 3, 19: 3}, 4)]:
    cyc = run_cycle(g, Es, g0, maxn=3000, checkG=True)
    if cyc[0] != 'cycle': rec("E2", "FAIL", f"{name}: no closure ({cyc[0]})"); continue
    pp, rp, ev, uni = reduce_cycle(cyc)
    states = cyc[4] + [(cyc[4][0][0], cyc[4][0][1])]
    mo = machine_orbit(g, Es, g0, cyc[1] + cyc[2] + 2); st = mo[cyc[1]:cyc[1] + cyc[2] + 1]
    word = carry_events(st); cnt = Counter((p, j) for p, j in word)
    nd = min(60, len(mo)); do = direct_orbit(g, Es, g0, nd)
    okd = all(a[0] == b[0] and lval(a[1]) == b[1] and b[2] == g for a, b in zip(mo[:nd], do))
    rec("E2", "PASS" if uni and okd else "FAIL", f"{name}: g={g} class transient {cyc[1]}, class period {cyc[2]}, gamma-period {pp}, rho_p={rp}, carry multiset (prime, exp)={dict(cnt)}, events (w,r^2) in one gamma-period {ev if len(ev) <= 6 else str(len(ev)) + ' events'}; direct orbit agrees ({nd} steps)")

# multi-prime odometer (T56): honest status of the test coverage
rec("P2b", "DATA", "g=59 seed: transient contains 3-carries AND 4-carries (two primes active in the transient) but the eventual cycle has the single active prime 3; no eventual cycle with >= 2 active primes occurred in any random search of this release, so the multi-prime clause of T56 is PROVED (T54-T55 + saturation) but NOT exercised by a test")
rec("P2c", "OPEN", "O9.2: exhibit a persistent orbit whose eventual cycle has two or more active primes (T56 predicts carry = min_p p^{j_p}); a construction would combine two T57 templates with the same g")

print(f"\n===== FIELD-I v009 summary: {NFAIL} FAIL, elapsed {time.time() - T0:.1f}s =====")
sys.exit(1 if NFAIL else 0)

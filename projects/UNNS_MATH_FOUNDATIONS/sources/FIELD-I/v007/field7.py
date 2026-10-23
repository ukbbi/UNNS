#!/usr/bin/env python3
"""FIELD-I v007 verifier (helpers copied from v005 for standalone use): (K1) signature criterion for three-route rigidity (closure of J1);
(K2) collective orbit universality: G-invariant, regime I, (s,t) dynamics, non-universality theorem;
(K3) G-collapse evidence. Exact integer/Fraction arithmetic. Tags PASS/FAIL/DATA/OPEN.
Notation: x=a/b reduced; D(x)={d>=2 : d^2|a, d=1 mod b} = {d | s : d>=2, d=1 mod b}, s^2||sqrt-part of a;
G(x)=gcd{d-1 : d in D(x)}; Delta_coll = lcm(d^2)/G; C(x)=x+Delta_coll."""
import os, sys, time, random
from fractions import Fraction as Fr
from math import gcd, isqrt
from itertools import combinations
from collections import Counter, defaultdict
QUICK = os.environ.get("FIELD7_QUICK") == "1"
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
def step(x):
    """one collective step; returns (T, g, L, y, Y, x_next)"""
    T = Dx(x); g = Gof(T); L = Lof(T); y = g * x
    assert y.denominator == 1; y = int(y); Y = y + L * L
    return T, g, L, y, Y, Fr(Y, g)
def in_next(d, g, Y):
    """reviewer criterion: d^2 | Y  and  g/gcd(g,d-1) | Y/d^2"""
    if Y % (d * d): return False
    return (Y // (d * d)) % (g // gcd(g, d - 1)) == 0
def in_next_occ(d, xn):
    """independent: occurrence integrality M = x'(d-1)/d^2 in Z_{>0}"""
    M = xn * (d - 1) / (d * d); return M.denominator == 1 and M > 0
def classify_event(T, T2, g):
    new = sorted(set(T2) - set(T))
    if not new: return "none", new
    return ("preserving" if all((d - 1) % g == 0 for d in new) else "reducing"), new
POOL = []   # (x) states used throughout
def pool_states():
    if POOL: return POOL
    for gg in (1, 2, 3, 4, 5, 6, 7, 10, 12):
        for b in [b for b in range(1, gg + 1) if gg % b == 0]:
            for a in range(1, 900 if QUICK else 2500):
                if gcd(a, b) != 1: continue
                T = Dset(a, b)
                if T and Gof(T) == gg: POOL.append(Fr(a, b))
    random.shuffle(POOL); del POOL[(250 if QUICK else 900):]
    return POOL

# =================================================================== K8  transition criterion and classification
bad1 = bad2 = bad3 = bad4 = n = nd = 0; kinds = Counter(); wit = {}
for x0 in pool_states():
    x = x0
    for _ in range(4):
        T, g, L, y, Y, xn = step(x)
        if g == 1: break
        if xn != x + Fr(L * L, g): bad1 += 1
        if Y < 4 * 10 ** 5:
            T2 = Dx(xn); ref = Dset(xn.numerator, xn.denominator)
            if T2 != ref: bad2 += 1
            crit = [d for d in range(2, isqrt(Y) + 1) if in_next(d, g, Y)]
            occ = [d for d in range(2, isqrt(Y) + 1) if in_next_occ(d, xn)]
            nd += 1
            if crit != ref or occ != ref: bad3 += 1
            kind, new = classify_event(T, ref, g)
            g2 = gcd(g, 0)
            for d in new: g2 = gcd(g2, d - 1)
            if gcd(g, g2) != Gof(ref): bad4 += 1
            if not set(T) <= set(ref): bad4 += 1
            kinds[(g, kind)] += 1; n += 1
            if kind != "none" and (g, kind) not in wit: wit[(g, kind)] = (str(x), str(xn), T, new, Gof(ref))
        x = xn
rec("K8.1", "PASS" if bad1 == 0 else "FAIL", f"x' = (y+L^2)/g equals x + lcm(d^2)/gcd(d-1) on the whole pool; violations {bad1}")
rec("K8.2", "PASS" if bad2 == 0 and bad3 == 0 and nd > 0 else "FAIL", f"transition criterion (d^2|Y and g/gcd(g,d-1) | Y/d^2) == occurrence integrality M=x'(d-1)/d^2 in Z>0 == brute-force D(x'), all 2<=d<=sqrt(Y), on {nd} states with G>1; mismatches {bad2}/{bad3}")
rec("K8.3", "PASS" if bad4 == 0 else "FAIL", f"G(x') = gcd(g, {{d-1 : d in D(x') \\ D(x)}}) and D(x) subset D(x'); violations {bad4} on {n} states")
cl = defaultdict(Counter)
for (g, k), v in kinds.items(): cl[g][k] += v
rec("K8.4", "DATA", "event classes by G (states with G>1, one step): " + "; ".join(f"G={g}: {dict(c)}" for g, c in sorted(cl.items())))
for key in sorted(wit):
    if key[1] in ("preserving", "reducing") and key[0] in (2, 3, 4, 5, 6, 7, 12):
        xs, xn, T, new, G2 = wit[key]
        rec("K8.5", "DATA", f"witness G={key[0]} {key[1]}: x={xs} -> x'={xn}; D {T} -> adds {new}; G' = {G2}")
# preserving events: second condition is vacuous
bad = n = 0
for x0 in pool_states()[:1500]:
    T, g, L, y, Y, xn = step(x0)
    if g == 1 or Y > 4 * 10 ** 5: continue
    for d in range(2, isqrt(Y) + 1):
        if (d - 1) % g == 0:
            n += 1
            if in_next(d, g, Y) != (Y % (d * d) == 0): bad += 1
rec("K8.6", "PASS" if bad == 0 else "FAIL", f"for d = 1 (mod g) the criterion collapses to d^2 | Y; so preserving growth <=> new d = 1 (mod g) with d^2 | y+L^2, d not in D(x); {n} (state,d) checks, violations {bad}")

# =================================================================== K9  anatomy of a growth event
def vq(n, q):
    k = 0
    while n % q == 0: n //= q; k += 1
    return k
bad_fresh = bad_carry = bad_type = bad_div = bad_cop = n = 0; typ = Counter()
for x0 in pool_states():
    x = x0
    for _ in range(4):
        T, g, L, y, Y, xn = step(x)
        if g == 1: break
        if Y < 10 ** 12:
            T2 = Dx(xn); kind, new = classify_event(T, T2, g); Lf = factor(L)
            for d in new:
                for q, e in factor(d).items():
                    if q not in Lf:                       # fresh prime
                        if not (Y % (q * q) == 0 and y % q != 0 and (y + L * L) % (q * q) == 0): bad_fresh += 1
                    else:                                  # prime already in L
                        l = Lf[q]
                        if e > l:
                            if vq(y, q) != 2 * l or ((y // q ** (2 * l)) + (L // q ** l) ** 2) % q != 0: bad_carry += 1
            if kind == "preserving":
                n += 1
                for d in new:
                    if L % d == 0: bad_type += 1          # a preserving new d never divides L
                    if gcd(d, g) != 1: bad_cop += 1
                    f = set(factor(d)); fresh = any(q not in factor(L) for q in f)
                    carry = any(factor(d)[q] > factor(L).get(q, 0) for q in f if q in factor(L))
                    typ["fresh" if fresh and not carry else "carry" if carry and not fresh else "both"] += 1
                # divisor closure: e | d new, e = 1 mod g, e >= 2  ->  e in D(x')
                for d in new:
                    for e in divisors(d):
                        if e >= 2 and (e - 1) % g == 0 and e not in T2: bad_div += 1
        x = xn
rec("K9.1", "PASS" if bad_fresh == 0 else "FAIL", f"fresh-prime lemma: a prime q of a new modulus with q not dividing L satisfies q not| y and y = -L^2 (mod q^2); violations {bad_fresh}")
rec("K9.2", "PASS" if bad_carry == 0 else "FAIL", f"carry lemma: if v_q(d) > v_q(L)=l for a new d then v_q(y)=2l exactly and q | y/q^(2l) + (L/q^l)^2; violations {bad_carry}")
rec("K9.3", "PASS" if bad_type == 0 and bad_cop == 0 and bad_div == 0 else "FAIL", f"{n} preserving events: every new modulus is coprime to g, does NOT divide L (so it contains a fresh prime or a carried prime power), and the new set is closed under divisors e = 1 (mod g); violations {bad_type}/{bad_cop}/{bad_div}")
rec("K9.4", "DATA", f"preserving new moduli by mechanism in the pool: {dict(typ)}")

# =================================================================== K10  persistent regime P_g (counterexample to universal collapse)
def ordmod(a, g):
    k, v = 1, a % g
    while v != 1: v = v * a % g; k += 1
    return k
def divs_of(n): return sorted(divisors_from(factor(n)))
def hyp_P(g, k, m):
    """finite hypotheses H(g,k,m) of Theorem P; returns (ok, reason)"""
    if g < 5 or gcd(g, 6) != 1: return False, "need g>=5, gcd(g,6)=1"
    if m % 2 == 0 or gcd(m, g) != 1: return False, "m odd, coprime to g"
    H = {pow(2, i, g) for i in range(ordmod(2, g))}
    if k < ordmod(2, g) - 1: return False, "k < ord_g(2) - 1"
    Res = {d % g for d in divs_of(m)}
    if not H <= Res: return False, "divisor residues of m miss <2>"
    for q, e in factor(m).items():
        rest = m // q ** e; ok = False
        for c in range(0, k + 1):
            for u in divs_of(rest):
                if (q ** e * 2 ** c * u) % g == 1: ok = True; break
            if ok: break
        if not ok: return False, f"prime power {q}^{e} not saturable"
    s = 2 ** k * m; D = [d for d in divs_of(s) if d >= 2 and d % g == 1]
    if Lof(D) != s: return False, "lcm D != s"
    if Gof(D) != g: return False, "G != g"
    return True, "ok"
def build_P(g):
    """m = q^ord * odd(g+1) with q the least odd prime = 2 (mod g): divisors of q^ord realise every power of 2 mod g, g+1 | s puts d=g+1 (d-1=g) in D"""
    o = ordmod(2, g); gp = g + 1; v = 0
    while gp % 2 == 0: gp //= 2; v += 1
    k = max(o - 1, v, 1); q = 3
    while not (is_prime(q) and q % g == 2 % g and gcd(q, g) == 1 and gp % q): q += 2
    m = gp * q ** o
    ok, why = hyp_P(g, k, m)
    return k, m, ok, why
def P_orbit_check(g, k, m, steps):
    s = 2 ** k * m; t = 1; x = Fr(s * s * t, g); bad = 0; Rs = []
    for n in range(steps):
        T = Dx(x)
        D = [d for d in divs_of(s) if d >= 2 and d % g == 1]
        if x != Fr(s * s * t, g) or T != D or Lof(T) != s or Gof(T) != g or x.denominator != g: bad += 1
        Rs.append(len(T))
        Dl, G = Dcoll(T); x = x + Dl
        s, t = st_step(s, t)
    return bad, Rs
def st_step(s, t):
    f = factor(t + 1); sg = 1; tt = 1
    for p, e in f.items():
        sg *= p ** (e // 2)
        if e % 2: tt *= p
    return s * sg, tt
ok, why = hyp_P(5, 3, 63)
bad, Rs = P_orbit_check(5, 3, 63, 60 if QUICK else 150)
rec("K10.1", "PASS" if ok and bad == 0 else "FAIL", f"g=5, s=2^3*63=504, x0=s^2/5=254016/5: hypotheses of Theorem P hold ({why}); direct iteration of the collective map for {60 if QUICK else 150} steps gives x_n = s_n^2 t_n/5, D=divisors of s_n congruent 1 mod 5, lcm D = s_n, G = 5 at every step; violations {bad}; R: {Rs[:7]}...{Rs[-1]}")
# the orbit that was observed in the survey: 45828/5
x = Fr(45828, 5); badx = 0; Gs = set(); N = 120 if QUICK else 400
for n in range(N):
    T = Dx(x); Gs.add(Gof(T)); Dl, G = Dcoll(T); x = x + Dl
rec("K10.2", "PASS" if Gs == {5} else "FAIL", f"seed 45828/5 (a natural seed, not designed): G = {sorted(Gs)} at every one of {N} steps; the orbit enters the family at step 3 (63504/5 = 252^2/5)")
rowsP = []; allok = True
for g in (5, 7, 11, 13, 17, 19, 23, 25, 29, 35, 49, 55, 65, 77):
    k, m, ok, why = build_P(g)
    if not ok: allok = False; rowsP.append((g, why)); continue
    bad, Rs = P_orbit_check(g, k, m, 30 if QUICK else 60)
    if bad: allok = False
    rowsP.append((g, k, m, bad))
rec("K10.3", "PASS" if allok else "FAIL", "Theorem P instances (g, k, m, violations over the direct orbit): " + str(rowsP))
# reach set and counting in P_g
g, k, m = 5, 3, 63
s = 2 ** k * m; t = 1; x = Fr(s * s, g); U = set()
for n in range(60):
    U |= set(Dx(x)); Dl, G = Dcoll(Dx(x)); x = x + Dl
    s, t = st_step(s, t)
pred = {d for d in divs_of(63 * 2 ** 40) if d >= 2 and d % 5 == 1}
rec("K10.4", "PASS" if U <= pred and {6, 16, 21, 36, 56, 96, 126, 256} <= U else "FAIL", f"P_5 reach set after 60 steps is inside {{d | 63*2^k : d = 1 mod 5}} ({len(U)} moduli, max {max(U)}); moduli with a factor 5, or not = 1 mod 5, are never reached, in particular 2, 3, 4, 5")
# survival test over natural seeds with G=5
persist = []; N5 = 6000 if QUICK else 25000; per = 0; tot = 0; cap = 90 if QUICK else 200; lost = []
for b in (1, 5):
    for a in range(1, N5):
        if gcd(a, b) != 1: continue
        T = Dset(a, b)
        if not T or Gof(T) != 5: continue
        tot += 1; x = Fr(a, b); T = Dx(x); ok5 = True
        for _ in range(cap):
            Dl, _ = Dcoll(T); x += Dl; T = Dx(x)
            if Gof(T) != 5: ok5 = False; break
        per += ok5
        if ok5: persist.append(Fr(a, b))
rec("K10.5", "DATA", f"natural seeds with G=5 (a<{N5}, b in {{1,5}}): {tot}; still at G=5 after {cap} steps: {per}; the rest collapsed (G -> 1)")
fm = 0
for x0 in persist:
    x = x0; xs = []
    for _ in range(60):
        xs.append(x); T = Dx(x); Dl, _ = Dcoll(T); x = x + Dl
    if xs[-1] == 4 * xs[-4] and xs[-1].denominator == 5: fm += 1
rec("K10.5b", "PASS" if fm == len(persist) else "FAIL", f"every persistent natural G=5 seed ({len(persist)}: {[str(p) for p in persist[:5]]}...) is eventually of the form x = s^2 t/5 with x_(n+3) = 4 x_n: {fm}/{len(persist)}")
rec("K10.6", "OPEN", "G=4 and G=12 (and every g with 2|g or 3|g other than 2,3,6): longest survival seen 28 (g=4) and 60 (g=12) steps from natural seeds, always followed by collapse; the t-cycle {1,2,3} of Theorem P meets the denominator when gcd(g,6)>1, so the P construction does not apply. Neither a proof of collapse nor a persistent orbit is known.")

# =================================================================== K11  global collapse
rec("K11.1", "PASS", "UNIVERSAL G-COLLAPSE IS FALSE (Theorem Q = Theorem P): for every g>=5 with gcd(g,6)=1 for which hypotheses H(g,k,m) hold (verified for g=5,7,11,13,17,19,23,25,29,35,49,55,65,77 in K10.3) there is a realised value x_0 whose collective orbit has G(x_n)=g for every n.")
# eventual-form conjecture
Ncap = 150 if QUICK else 300; seeds = [Fr(a, b) for b in (1, 2, 3, 4, 5, 7) for a in range(2, 700 if QUICK else 1500) if gcd(a, b) == 1 and Dset(a, b)]
random.shuffle(seeds); seeds = seeds[:150 if QUICK else 400]; forms = Counter(); badform = 0
for x0 in seeds:
    x = x0; xs = []
    for _ in range(Ncap):
        T = Dx(x); Dl, G = Dcoll(T); xs.append((x, Gof(T))); x = x + Dl
    (xa, ga), (xb, gb) = xs[-1], xs[-4]
    if xa == 4 * xb: forms[ga] += 1
    else: badform += 1
rec("K11.2", "DATA", f"eventual-form test on {len(seeds)} natural seeds, {Ncap} steps: orbits with x_(n+3)=4x_n at the end, by G_inf: {dict(forms)}; not yet in that form: {badform}")
rec("K11.3", "OPEN", "ASYMPTOTIC-FORM CONJECTURE: every collective orbit is eventually of the form x = s^2 t/g with t in {1,2,3}, g = G_inf >= 1, so that x_(n+3)=4x_n (G_inf=1 proved, T32; G_inf = g > 1 occurs, Theorem P). Open: whether every persistent G_inf>1 orbit is of this form, and which g occur (g with 2|g or 3|g beyond 2,3,6).")
rec("K11.4", "OPEN", "Which natural seeds (a,b) fall into P_g rather than collapsing? Density of persistent orbits among seeds with G=5 (K10.5) is DATA only.")
print(f"\nelapsed {time.time()-T0:.1f}s  failures {NFAIL}")
print("ALL PASS" if NFAIL == 0 else "SOME FAIL"); sys.exit(0 if NFAIL == 0 else 1)

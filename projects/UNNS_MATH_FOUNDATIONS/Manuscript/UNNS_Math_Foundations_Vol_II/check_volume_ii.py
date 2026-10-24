#!/usr/bin/env python3
"""Verification of the statements of Volume II (exact integer / Fraction arithmetic).

Each check recomputes a statement of the volume from the definitions, independently of
the source-record scripts.  Output: PASS/FAIL lines and checks_volume_ii.json.
Usage:  python3 check_volume_ii.py [--quick]
"""
import sys, json, time, random, itertools, math
from fractions import Fraction as Fr
from math import gcd, isqrt
from engine import *
from engine_seeds import gen_reset

QUICK = '--quick' in sys.argv
RES = []
T0 = time.time()

def check(tag, statement, ok, detail=''):
    RES.append({'tag': tag, 'statement': statement, 'pass': bool(ok), 'detail': str(detail)})
    print(('PASS ' if ok else 'FAIL ') + tag + ' | ' + statement + (' | ' + str(detail) if detail else ''), flush=True)

def squarefree_part(n):
    f = factor(n); r = 1
    for p, e in f.items():
        if e % 2: r *= p
    return r

def tau(n):
    t = 1
    for e in factor(n).values(): t *= e + 1
    return t

def seeds(amax, bmax):
    return [Fr(a, b) for b in range(1, bmax + 1) for a in range(1, amax + 1) if gcd(a, b) == 1]

def orbit_states(x0, N):
    """list of (x, D, G, L) along the orbit (stops when the fibre is empty)."""
    x = Fr(x0); out = []
    for _ in range(N):
        D = fibre(x)
        if not D: break
        G, L = Gof(D), Lof(D)
        out.append((x, D, G, L))
        x = x + Fr(L * L, G)
    return out

def machine_orbit(g, gamma, E, N):
    out = [(gamma, dict(E), {})]
    for _ in range(N - 1):
        r = mstep(g, gamma, E)
        if r is None: break
        gamma, E, D = r
        out.append((gamma, dict(E), D))
    return out

def class_vec(g, E):
    v = []
    for p, e in sorted(E.items()):
        o = ordmod(p, g)
        v.append((p, e if e <= o - 2 else (o - 1) + ((e - (o - 1)) % o)))
    return tuple(v)

def find_cycle(g, gamma, E, cap=200000):
    seen = {}; gam = gamma; EE = dict(E); n = 0; states = []
    while n < cap:
        key = (gam, class_vec(g, EE))
        if key in seen: return seen[key], n, states
        seen[key] = n; states.append((gam, dict(EE)))
        r = mstep(g, gam, EE)
        if r is None: return None
        gam, EE, D = r; n += 1
    return None

def q_seed(q, g):
    o = ordmod(q, g); H = {pow(q, k, g) for k in range(o)}
    if 2 in H: return None
    e2 = next(e for e in range(1, ordmod(2, g) + 1) if pow(2, e, g) in H)
    K = {a * h % g for a in {pow(2, k, g) for k in range(ordmod(2, g))} for h in H}
    for M in range(3, q):
        if M % 2 and M % g in K: return None
    for M in range(2, q):
        if M % 2 == 0 and M % g in H: return None
    u = next(u for u in range(q + g, 10 ** 7, g) if is_prime(u))
    return {u: o - 1, q: 1, 2: e2}

def _descent(g, E, gam0):
    gam = gam0; K = 0; n = 0
    if gam == 1: return 0, 0, True
    while True:
        r = mstep(g, gam, E)
        if r is None: return K, n, False
        gam, E, D = r; n += 1
        if D: K += 1
        if gam == 1: return K, n, True
        if n > 50 * g: return K, n, False

def maxgap(S, o):
    a = sorted(S)
    return max(((a[(i + 1) % len(a)] - a[i]) % o) or o for i in range(len(a)))

SEEDS = [x for x in seeds(3000 if QUICK else 7000, 12) if fibre(x)]

# ------------------------------------------------------------------ Chapter 1
def ch1():
    bad = {'reduced': 0, 'gamma': 0, 'den': 0, 'mono': 0, 'gmono': 0}
    for x in SEEDS:
        D = fibre(x); G, L = Gof(D), Lof(D)
        if gcd(L * L, G) != 1: bad['reduced'] += 1
        if (Fr(G) * x / (L * L)).denominator != 1: bad['gamma'] += 1
        if G % x.denominator: bad['den'] += 1
        x1 = x + Fr(L * L, G); D1 = fibre(x1)
        if not set(D) <= set(D1): bad['mono'] += 1
        if Gof(D) % Gof(D1): bad['gmono'] += 1
    n = len(SEEDS)
    check('T17p', f'Delta_coll=L^2/G reduced; gamma=Gx/L^2 integer; b|G ({n} seeds)', bad['reduced'] + bad['gamma'] + bad['den'] == 0, bad)
    check('T31', f'D(x) subset D(C(x)) and G(C(x)) | G(x) ({n} seeds)', bad['mono'] + bad['gmono'] == 0, bad)

    viol18 = viol26 = viol17 = 0; cnt = 0
    for x in SEEDS[:: max(1, len(SEEDS) // (600 if QUICK else 1800))]:
        D = fibre(x); G, L = Gof(D), Lof(D)
        gam = int(Fr(G) * x / (L * L))
        y = x; T = 0
        while True:
            y = y + Fr(L * L, G); T += 1
            if fibre(y) != D: break
            if y != Fr((gam + T) * L * L, G): viol17 += 1
        cnt += 1
        v = G
        def Kd(d): return v * d * d * (-(-gam // (v * d * d))) - gam
        Dset = set(D)
        dmin = next(d for d in range(2, 10 ** 6) if d not in Dset)
        if not (1 <= Kd(dmin) <= v * dmin * dmin - 1 and T <= Kd(dmin)): viol18 += 1
        if dmin > len(D) + 2: viol18 += 1
        k0 = Kd(dmin)
        brute = min(Kd(d) for d in range(2, 80) if d not in Dset)
        bound = isqrt((gam + k0) // v) + 2
        srch = min(Kd(d) for d in range(2, bound + 1) if d not in Dset)
        if T > srch or srch > brute: viol26 += 1
    check('T17', f'plateau law x_(n0+k)=(gamma0+k)L^2/G while D is constant ({cnt} seeds)', viol17 == 0, viol17)
    check('T18', f'growth time T(x) <= K_d <= G d^2-1 for the least d not in D; d_min <= R+2 ({cnt} seeds)', viol18 == 0, viol18)
    check('T26', f'minimum of K_d over all d not in D attained at d <= sqrt((gamma+k0)/G)+1 ({cnt} seeds)', viol26 == 0, viol26)

    seedlist = [Fr(4), Fr(36), Fr(45828, 5), Fr(20736, 5), Fr(81, 4), Fr(220), Fr(504 ** 2, 5), Fr(100)]
    ok19 = ok27 = True; summary = []
    for x0 in seedlist:
        st = orbit_states(x0, 70)
        R = [len(s[1]) for s in st]
        if any(R[i] > R[i + 1] for i in range(len(R) - 1)) or R[-1] <= R[0]: ok19 = False
        v0 = st[0][2]
        first = {}
        for n, r in enumerate(R): first.setdefault(r, n)
        for r in sorted(first):
            if r + 1 in first and R[first[r]] == r and first[r + 1] > first[r] + v0 * (r + 2) ** 2 - 1: ok27 = False
        summary.append((str(x0), R[0], R[-1]))
    check('T19', 'R(x_n) non-decreasing and growing along 8 exact orbits (70 steps each)', ok19, summary)
    check('T27', 'n(r+1) <= n(r)+G_0 (r+2)^2-1 along the same orbits', ok27)
    seq = [len(fibre(Fr(36 * (k + 1)))) for k in range(8)]
    check('T28', 'route-aware orbit 36(k+1): R = 3,3,3,5,3,3,3,5 (R drops from 5 to 3)', seq == [3, 3, 3, 5, 3, 3, 3, 5], seq)

# ------------------------------------------------------------------ Chapter 2
def ch2():
    bad = 0
    for x in SEEDS:
        D = fibre(x); G, L = Gof(D), Lof(D)
        integer4 = x.denominator == 1 and x.numerator % 4 == 0
        if (G == 1) != integer4: bad += 1
        if (G == 1) != (2 in D): bad += 1
        if G % x.denominator or gcd(L, G) != 1: bad += 1
    check('T30', f'b|G, gcd(L,G)=1, G=1 <=> 2 in D <=> x integer divisible by 4 ({len(SEEDS)} seeds)', bad == 0, bad)

    bad = 0; maxentry = 0; cnt = 0
    for x in range(4, 3000 if QUICK else 9000, 4):
        f = factor(x); s = 1; t = 1
        for p, e in f.items(): s *= p ** (e // 2); t *= p ** (e % 2)
        D = fibre(Fr(x))
        if D != [d for d in sorted(divisors_from(factor(s))) if d >= 2]: bad += 1
        if Gof(D) != 1 or Lof(D) != s: bad += 1
        tt = t; n = 0
        while tt > 3: tt = squarefree_part(tt + 1); n += 1
        if n > 4 * kappa3(t): bad += 1
        maxentry = max(maxentry, n)
        y = Fr(x)
        for _ in range(n): y = y + Fr(Lof(fibre(y)) ** 2, Gof(fibre(y)))
        ys = [y]
        for _ in range(6): ys.append(ys[-1] + Fr(Lof(fibre(ys[-1])) ** 2, Gof(fibre(ys[-1]))))
        if any(ys[i + 3] != 4 * ys[i] for i in range(4)): bad += 1
        o = Lof(fibre(ys[0]))
        while o % 2 == 0: o //= 2
        if len(fibre(ys[3])) - len(fibre(ys[0])) != tau(o): bad += 1
        if len(fibre(ys[0])) != tau(Lof(fibre(ys[0]))) - 1: bad += 1
        cnt += 1
    check('T32/L3', f'regime I: D=divisors of s, G=1, entry <= 4*kappa3(t), x_(n+3)=4x_n, R increment tau(odd s) ({cnt} integers)', bad == 0, f'bad={bad}, max entry={maxentry}')

    bad = 0
    for x0 in (4, 72, 60, 140, 12, 500):
        st = orbit_states(Fr(x0), 75)
        ent = next(n for n in range(len(st) - 3) if all(st[i + 3][0] == 4 * st[i][0] for i in range(n, len(st) - 3)))
        oo = st[ent][3]
        while oo % 2 == 0: oo //= 2
        # reach set of the full orbit, restricted to d<=X, versus the formula (valid once enough steps are taken)
        U = set()
        for s in st: U |= set(s[1])
        for X in (10, 100, 1000):
            formula = sum(1 + (X // q).bit_length() - 1 for q in divisors_from(factor(oo)) if q <= X) - 1
            full = len({q * 2 ** k for q in divisors_from(factor(oo)) for k in range(0, 14) if 2 <= q * 2 ** k <= X})
            enum = len({d for d in U if d <= X})
            if full != formula or enum != formula: bad += 1
    check('L4', 'reach counting U(X)=sum_{q|o,q<=X}(1+floor(log2(X/q)))-1 for the G=1 branch (6 orbits, 75 steps)', bad == 0, bad)

    worst = {2: 0, 3: 0, 6: 0}; bad = 0; cnt = {2: 0, 3: 0, 6: 0}
    lim = {2: 7, 3: 2, 6: 29}
    for x in SEEDS:
        D = fibre(x); G = Gof(D)
        if G in lim:
            y = x; n = 0
            while True:
                DD = fibre(y); GG = Gof(DD)
                if GG == 1 or n > 60: break
                y = y + Fr(Lof(DD) ** 2, GG); n += 1
            cnt[G] += 1; worst[G] = max(worst[G], n)
            if n > lim[G]: bad += 1
    check('T34/L2', 'G=2,3,6 collapse to G=1 within 7, 2, 29 steps (all seeds with these G)', bad == 0, f'counts={cnt} worst={worst}')

    bad = 0; cnt = 0
    for x in SEEDS[:: max(1, len(SEEDS) // 1500)]:
        D = fibre(x); G, L = Gof(D), Lof(D)
        if G == 1: continue
        y0 = int(G * x); cnt += 1
        if L % 2 == 1:
            k = next(k for k in range(1, 4 * G + 2) if (y0 + k * L * L) % (4 * G) == 0)
            if k > 4 * G: bad += 1
        elif G % 2 == 1:
            k = next(k for k in range(1, G + 2) if (y0 + k * L * L) % (4 * G) == 0)
            if k > G: bad += 1
    check('L1/T37', f'modular escape: a frozen fibre reaches an integer divisible by 4 within 4G (L odd) or G (L even, G odd) steps ({cnt} seeds)', bad == 0, bad)

    bad35 = bad35a = bad36 = 0; ncheck = 0; npres = 0
    for x in SEEDS[:: max(1, len(SEEDS) // 1000)]:
        D = fibre(x); G, L = Gof(D), Lof(D)
        y = int(G * x); Y = y + L * L
        Dp = fibre(Fr(Y, G))
        for d in range(2, 300):
            crit = (Y % (d * d) == 0) and ((Y // (d * d)) % (G // gcd(G, d - 1)) == 0)
            if crit != (d in Dp): bad35 += 1
        new = [d for d in Dp if d not in D]
        g2 = G
        for d in new: g2 = gcd(g2, d - 1)
        if g2 != Gof(Dp): bad35a += 1
        ncheck += 1
        if new and Gof(Dp) == G:
            npres += 1
            fL = factor(L)
            for d in new:
                if gcd(d, G) != 1 or (L % d == 0): bad36 += 1
                fd = factor(d)
                fresh = [q for q in fd if L % q]
                carried = [q for q in fd if L % q == 0 and fd[q] > fL[q]]
                if not (fresh or carried): bad36 += 1
                for q in carried:
                    l = fL[q]
                    if y % q ** (2 * l) != 0 or y % q ** (2 * l + 1) == 0: bad36 += 1
                for q in fresh:
                    if y % q == 0 or Y % (q * q): bad36 += 1
    check('T35', f"transition criterion d in D(x') <=> d^2|Y and g/gcd(g,d-1) | Y/d^2 ({ncheck} seeds, d<300)", bad35 == 0, bad35)
    check('T35a', "transition identity G(x')=gcd(g,{d-1: d in new})", bad35a == 0, bad35a)
    check('T36', f'anatomy of preserving events: coprime to g, fresh prime or carried prime power ({npres} events)', bad36 == 0, bad36)

# ------------------------------------------------------------------ Chapter 3
def persistent_orbit_ok(g, s, N):
    x = Fr(s * s, g); rows = []
    for n in range(N):
        D = fibre(x); G, L = Gof(D), Lof(D)
        rows.append((G, L, len(D), x))
        x = x + Fr(L * L, G)
    return rows

def ch3():
    glist = [5, 7, 11, 13, 17, 19, 23, 25, 29, 35, 49, 55, 65, 77]
    bad = 0; info = {}
    for g in glist:
        o = ordmod(2, g); s = (g + 1) * (g + 2) ** o
        rows = persistent_orbit_ok(g, s, 12)
        okg = all(r[0] == g for r in rows)
        okg &= all(rows[i + 3][3] == 4 * rows[i][3] for i in range(len(rows) - 3))
        okg &= rows[0][1] == s and rows[3][1] == 2 * s
        if not okg: bad += 1
        info[g] = o
    check('T38/T42', f'persistent regime P_g: x0=s^2/g, s=(g+1)(g+2)^o: G=g, x_(n+3)=4x_n, L=s_n for g in {glist}', bad == 0, f'orders o={info}')
    bad = 0
    for g in glist:
        o = ordmod(2, g); s = (g + 1) * (g + 2) ** o
        k = factor(s).get(2, 0); m = s >> k
        divm = divisors_from(factor(m))
        H1 = {pow(2, j, g) for j in range(o)} <= {d % g for d in divm}
        Ds = [d for d in divisors_from(factor(s)) if d >= 2 and d % g == 1]
        H3 = 0
        for d in Ds: H3 = gcd(H3, (d - 1) // g)
        H2 = all(any(d % q ** e == 0 for d in Ds) for q, e in factor(m).items())
        if not (H1 and H2 and H3 == 1 and gcd(m, g) == 1): bad += 1
    check('T38h', 'hypotheses (H1)-(H3) of T38 hold for the T42 seeds', bad == 0, bad)

    bad = 0
    for g in (15, 39, 51, 57, 87):
        o = ordmod(2, g); s = (g + 1) * (g + 2) ** o
        rows = persistent_orbit_ok(g, s, 15)
        if not all(r[0] == g for r in rows): bad += 1
        if not all(rows[i + 3][3] == 4 * rows[i][3] for i in range(len(rows) - 3)): bad += 1
        m = s
        while m % 2 == 0: m //= 2
        for t in (1, 2, 3):
            bt = g // gcd(g, t)
            for a in divisors_from(factor(m)):
                for j in range(0, o + 1):
                    d = (2 ** j) * a
                    if d % bt == 1 % bt and d % g != 1: bad += 1
    check('T46', 'P*: persistent orbits for g=15,39,51,57,87, hypothesis (H4) verified', bad == 0, bad)

    bad = 0; info = {}
    for g in (13, 19, 25, 55, 15, 39):
        o = ordmod(2, g); s = (g + 1) * (g + 2) ** o
        k = factor(s).get(2, 0); m = s >> k
        A = sum(1 for a in divisors_from(factor(m)) if any(a * pow(2, j, g) % g == 1 for j in range(o)))
        rows = persistent_orbit_ok(g, s, 3 * o * 2 + 1)
        for n in range(3 * o + 1):
            if rows[n + 3 * o][2] - rows[n][2] != A: bad += 1
        info[g] = (o, A)
    check('T43', 'R(x_(n+3o)) - R(x_n) = A_g(m) over two complete periods (g=13,19,25,55,15,39)', bad == 0, info)

    bad = 0; n44 = 0
    pool = []
    for g in (5, 7, 11, 13, 25, 35, 15, 39):
        o = ordmod(2, g); s = (g + 1) * (g + 2) ** o
        for r in persistent_orbit_ok(g, s, 8): pool.append(r[3])
    pool += SEEDS[:: max(1, len(SEEDS) // 500)]
    for x in pool:
        D = fibre(x); G, L = Gof(D), Lof(D)
        y = x * G
        if y.denominator != 1 or int(y) % (L * L): bad += 1; continue
        gam = int(y) // (L * L)
        isint4 = (x.denominator == 1 and x.numerator % 4 == 0)
        if G == 1: pred = True
        elif L % 2 == 1: pred = (gam % (4 * G) == 0)
        elif G % 2 == 1: pred = (gam % G == 0)
        else: pred = None
        if pred is not None and pred != isint4: bad += 1
        if x.denominator != G // gcd(G, gam): bad += 1
        xp = x + Fr(L * L, G); Dp = fibre(xp); Gp, Lp = Gof(Dp), Lof(Dp)
        if Gp == G:
            r = Lp // L
            gp = Fr(Gp) * xp / (Lp * Lp)
            if gp != Fr(gam + 1, r * r): bad += 1
            if G % 2 == 0 and (r % 2 == 0 or (int(gp) - gam - 1) % 8): bad += 1
            if G % 3 == 0 and r % 3 and (int(gp) - gam - 1) % 3: bad += 1
            if G % 6 == 0 and r % 6 and (int(gp) - gam - 1) % 24: bad += 1
        n44 += 1
    check('T44', f'gamma framework (a)-(e) on {n44} states', bad == 0, bad)

    bad = 0; seen = {}; cnt = 0
    for x in SEEDS[:: max(1, len(SEEDS) // (400 if QUICK else 1200))]:
        D = fibre(x); G = Gof(D)
        if G > 1 and 24 % G == 0:
            y = x; n = 0
            while True:
                DD = fibre(y); GG = Gof(DD)
                if GG == 1 or n > 150: break
                y = y + Fr(Lof(DD) ** 2, GG); n += 1
            cnt += 1; seen.setdefault(G, []).append(n)
            if GG != 1: bad += 1
    check('T45', f'orbits with 1<G | 24 all reach G=1 ({cnt} seeds; G in {sorted(seen)}; worst {max(max(v) for v in seen.values()) if seen else 0} steps)', bad == 0 and cnt > 0, bad)
    bad = 0
    for g in (11, 13, 17, 19, 25, 29, 77):
        o = ordmod(2, g); s = (g + 1) * (g + 2) ** o
        for r in persistent_orbit_ok(g, s, 12):
            if int(r[3] * r[0] / (r[1] ** 2)) > 2 * g: bad += 1
    check('T47', 'gamma_n <= 2M along persistent orbits of P_g (M=g since L even)', bad == 0, bad)

# ------------------------------------------------------------------ Chapter 4
def ch4():
    rng = random.Random(2026)
    nmatch = 0; bad = 0
    for _ in range(60 if QUICK else 160):
        sd = gen_reset(rng)
        if not sd: continue
        g, E = sd
        x = state_to_x(g, 1, E)
        mo = machine_orbit(g, 1, E, 14)
        dr = direct(x, len(mo))
        for a, b in zip(mo, dr):
            if a[0] != b[1] or lval(a[1]) != b[2] or b[3] != g: bad += 1
            nmatch += 1
    check('T49', f'one-step law: residue machine = direct iteration of C (gamma, L, G agree on {nmatch} states)', bad == 0, bad)

    bad = 0
    for k in range(0, 3):
        S = 4 * 3 ** (3 + k) * 5 ** 4
        rows = direct(Fr(S * S, 11), 24, keepx=True)
        for j, r in enumerate(rows):
            if r[3] != 11: bad += 1
            if r[4] != 7 + 2 * k + 2 * (j // 8): bad += 1
        for j in range(len(rows) - 8):
            if rows[j + 8][5] != 9 * rows[j][5]: bad += 1
        ratios = sorted({rows[j + 3][5] / rows[j][5] for j in range(len(rows) - 3)})
        if ratios != sorted([Fr(3, 2), Fr(8, 5), Fr(7, 4), Fr(2), Fr(5, 2), Fr(18, 7), Fr(27, 8), Fr(4)]): bad += 1
        for j in range(8):
            if rows[j][5] != Fr((j + 1) * S * S, 11): bad += 1
    for k in list(range(3, 40)) + [100, 399]:
        mo = machine_orbit(11, 1, {2: 2, 3: 3 + k, 5: 4}, 17)
        if [m[0] for m in mo] != [1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8, 1]: bad += 1
        if mo[8][1] != {2: 2, 3: 4 + k, 5: 4}: bad += 1
    check('T50', 'eight-step theorem g=11: x_(8k+j)=(j+1)S_k^2/11, x_(n+8)=9x_n, R=7+2k, eight ratios (direct k<=2, machine k<=399)', bad == 0, bad)

    rng = random.Random(77)
    cycles = []; bad51 = bad52 = bad54 = bad55 = bad59 = bad61 = bad67 = 0
    nsteps = 0; t0 = time.time(); ntr = 0
    while len(cycles) < (30 if QUICK else 60):
        sd = gen_reset(rng)
        if not sd: continue
        g, E = sd
        gam0 = rng.choice([1, 1, 1, rng.randint(2, 4000)])
        nz = normalise(g, gam0, E)
        if nz is None: continue
        gam, E = nz
        fc = find_cycle(g, gam, E)
        if fc is None: continue
        n1, n2, states = fc
        P = n2 - n1
        mo = machine_orbit(g, gam, E, n2 + 2 * P + 2)
        if len(mo) < n2 + 2 * P + 2: continue
        rho = Fr(lval(mo[n2][1]), lval(mo[n1][1]))
        for n in range(n1, n2 + P):
            if mo[n + P][0] != mo[n][0]: bad51 += 1
            if Fr(lval(mo[n + P][1]), lval(mo[n][1])) != rho: bad51 += 1
        for n in range(n1, n1 + P + 1):
            if state_to_x(g, mo[n + P][0], mo[n + P][1]) != rho * rho * state_to_x(g, mo[n][0], mo[n][1]): bad51 += 1
        gps = mo[0][0]
        for n in range(len(mo) - 1):
            ga, Ec, Dc = mo[n]
            if g % 2 == 1 and Ec.get(2, 0) < 1: bad52 += 1; print('T52a', g, n, Ec)
            if g % 2 == 1 and (ga + 1) % g == 0: bad52 += 1; print('T52b', g, n, ga)
            if Dc:
                if ga == 1 and gps == 1:
                    M = 1
                    for p, j in Dc.items(): M *= p ** j
                    if M * M >= g: bad52 += 1; print('T52c', g, n, Dc)
                gps = ga
        gs = mo[0][0]; seen1 = (mo[0][0] == 1)
        for n in range(1, len(mo)):
            ga, Ec, Dc = mo[n]
            if Dc:
                if 4 * ga > gs + 4: bad54 += 1
                if seen1 and ga != 1: bad54 += 1
                if len(Dc) > 1 and seen1 and n >= n2: bad55 += 1
                gs = ga
            if ga == 1: seen1 = True
        for n in range(n1, n2):
            ga, Ec, Dc = mo[n]
            if ga != 1: continue
            nxt = next((k for k in range(n + 1, len(mo)) if mo[k][2]), None)
            if nxt is None: continue
            carry = mo[nxt][2]
            if len(carry) != 1: bad55 += 1
            cand = []
            for p in small_primes(isqrt(4 * g) + 1):
                if g % p == 0: continue
                j = pend_j(g, Ec, p)
                if j is not None: cand.append((p ** j, p, j))
            if not cand: bad59 += 1; continue
            M, p, j = min(cand)
            if carry != {p: j}: bad59 += 1
            nm = next_M(g, Ec)
            if nm is None or nm[1] != mo[nxt][1]: bad67 += 1
        active = {p for p in mo[n2][1] if mo[n2 + P][1].get(p, 0) != mo[n2][1].get(p, 0)}
        if len(active) != 1: bad61 += 1
        else:
            p = next(iter(active))
            o, Abs = abs_set(g, mo[n2][1], p)
            s = min_period(Abs, o)
            gaps = cyc_gaps({k % s for k in Abs}, s)
            Pg_ = sum(p ** (2 * j) - 1 for j in gaps)
            gseq = [m[0] for m in mo[n2:n2 + 3 * P]]
            Pmin = next(q for q in range(1, P + 1) if all(gseq[i + q] == gseq[i] for i in range(len(gseq) - q)))
            Lr = Fr(lval(mo[n2 + Pmin][1]), lval(mo[n2][1]))
            if Pmin != Pg_ or Lr != p ** s: bad61 += 1
            cycles.append((g, p, s, Pmin, p ** s))
        nsteps += len(mo)
    check('T51', f'finite-state closure: every sampled orbit becomes class-periodic, gamma_(n+P)=gamma_n, x_(n+P)=rho^2 x_n ({len(cycles)} orbits, {nsteps} machine states)', bad51 == 0, bad51)
    check('T52', 'window theorem: g odd => 2|L, g does not divide gamma+1, complete carries M^2<g', bad52 == 0, bad52)
    check('T54', "carry completeness: gamma' <= gamma_s/4+1; every carry complete after gamma=1", bad54 == 0, bad54)
    check('T55', 'eventual carries change exactly one prime exponent (prime powers)', bad55 == 0, bad55)
    check('T56/T59', 'scheduler min_p p^(j_p) (odometer law) reproduces every eventual carry', bad59 == 0, bad59)
    check('T67', 'exact carry-level predictor next_M equals the machine at every eventual reset state', bad67 == 0, bad67)
    check('T61', f'single active prime; P_gamma=sum(p^(2j)-1), L ratio = p^s ({len(cycles)} cycles)', bad61 == 0, bad61)
    globals()['CYCLES'] = cycles

    bad = 0; info = {}
    for q, g in [(3, 11), (3, 13), (5, 31), (5, 199), (7, 367)]:
        E0 = q_seed(q, g)
        if E0 is None: bad += 1; continue
        L0 = lval(E0)
        if g <= 400:
            # (Q4) exact G(x0)=g, via the exact divisor enumeration of the square-root part
            if exact_G(g, 1, E0) != g: bad += 1; info[(q, g)] = 'G!=g'; continue
        fc = find_cycle(g, 1, E0)
        n1, n2, st = fc
        mo = machine_orbit(g, 1, E0, 3 * (q * q - 1) + 2)
        want = [(n % (q * q - 1)) + 1 for n in range(len(mo))]
        okq = [m[0] for m in mo] == want
        okq &= all(Fr(lval(mo[n + q * q - 1][1]), lval(mo[n][1])) == q for n in range(len(mo) - (q * q - 1)))
        if not okq: bad += 1
        info[(q, g)] = (E0, 'P=%d' % (q * q - 1), 'class period %d' % (n2 - n1))
    check('T57', 'q-carry theorem instances q=3 (g=11,13), q=5 (g=31,199), q=7 (g=367): x_(n+q^2-1)=q^2 x_n, (Q4) exact', bad == 0, info)
    bad = 0
    for q, g in [(3, 11), (3, 13), (5, 31)]:
        E0 = q_seed(q, g); L0 = lval(E0)
        rows = direct(Fr(L0 * L0, g), q * q * 3, keepx=True)
        for j in range(len(rows) - (q * q - 1)):
            if rows[j + q * q - 1][5] != q * q * rows[j][5]: bad += 1
        if [r[1] for r in rows[:q * q]] != list(range(1, q * q)) + [1]: bad += 1
        for j, r in enumerate(rows):
            if r[4] != 2 * (1 + j // (q * q - 1)) + 1: bad += 1
    check('T57d', 'q-carry orbits (g=11,13,31) confirmed by direct iteration of C: gamma-cycle, x-scaling, R=2e_q+1', bad == 0, bad)

# ------------------------------------------------------------------ Chapters 5-7
def sim_odometers(prims, oms, abss, phases):
    ph = list(phases); seen = {}; log = []
    def gap(i, e):
        o = oms[i]
        for j in range(1, o + 1):
            if (e + j) % o in abss[i]: return j
    n = 0
    while True:
        key = tuple(ph)
        if key in seen: break
        seen[key] = n; n += 1
        c, i = min((prims[i] ** gap(i, ph[i]), i) for i in range(len(prims)))
        log.append(i); ph[i] = (ph[i] + gap(i, ph[i])) % oms[i]
    cyc = log[seen[tuple(ph)]:]
    return set(cyc), len(cyc)

def ch5_7():
    prims = [2, 3, 5]
    subsets = [(o, frozenset(k for k in range(o) if mask >> k & 1)) for o in range(1, 5) for mask in range(1, 2 ** o)]
    bad60 = bad64 = 0; nsys = 0
    for combo in itertools.product(subsets, repeat=3):
        oms = [c[0] for c in combo]; abss = [c[1] for c in combo]
        ms = [prims[i] ** maxgap(abss[i], oms[i]) for i in range(3)]
        star = min(range(3), key=lambda i: ms[i])
        for phases in itertools.product(*[range(o) for o in oms]):
            fired, ln = sim_odometers(prims, oms, abss, phases)
            nsys += 1
            if len(fired) != 1: bad60 += 1
            if fired != {star}: bad64 += 1
    check('T60', f'at most one odometer fires infinitely often ({nsys} (system,phase) pairs: 3 odometers, o<=4, all Abs)', bad60 == 0, bad60)
    check('T64', 'survivor = argmin_i p_i^(maxgap Abs_i) for every phase (same exhaustive set)', bad64 == 0, bad64)
    rng = random.Random(5); bad = 0; n = 0
    PR = [2, 3, 5, 7, 11]
    for _ in range(300 if QUICK else 1500):
        k = rng.randint(2, 5); ps = PR[:k]
        oms = [rng.randint(1, 9) for _ in ps]
        abss = [frozenset(rng.sample(range(o), rng.randint(1, o))) for o in oms]
        ms = [ps[i] ** maxgap(abss[i], oms[i]) for i in range(k)]
        star = min(range(k), key=lambda i: ms[i])
        fired, ln = sim_odometers(ps, oms, abss, [rng.randrange(o) for o in oms])
        n += 1
        if fired != {star}: bad += 1
    check('T64r', f'minimax survivor on {n} random systems with 2-5 odometers (orders up to 9)', bad == 0, bad)

    rng = random.Random(11); bad62 = 0; n62 = 0
    for _ in range(400):
        g = rng.choice([x for x in range(11, 400) if is_prime(x)])
        ps = [p for p in small_primes(60) if g % p]
        p, q = rng.sample(ps, 2)
        op, oq = ordmod(p, g), ordmod(q, g)
        Hq = {pow(q, k, g) for k in range(oq)}
        F = {1}
        for _ in range(rng.randint(0, 3)):
            r = rng.choice(ps); F = {f * pow(r, k, g) % g for f in F for k in range(rng.randint(1, 4))}
        A = {h * f % g for h in Hq for f in F}
        Absp = {k for k in range(op) if pow(pow(p, k, g), -1, g) in A}
        tp = op // gcd(op, oq); tq = oq // gcd(op, oq)
        if any(((k + tp) % op in Absp) != (k in Absp) for k in range(op)): bad62 += 1
        if gcd(tp, tq) != 1: bad62 += 1
        n62 += 1
    check('T62', f'two saturated clocks: Abs_p is tau_p-periodic, tau_p,tau_q coprime ({n62} cases, prime g)', bad62 == 0, bad62)

    bad65 = 0; n65 = 0
    for _ in range(600):
        g = rng.randint(11, 300)
        ps = [p for p in small_primes(60) if g % p == 0 or True]
        ps = [p for p in ps if gcd(p, g) == 1]
        if len(ps) < 4: continue
        p = rng.choice(ps); others = rng.sample([x for x in ps if x != p], 3)
        nsat = rng.randint(1, 2); sat, frozen = others[:nsat], others[nsat:]
        H = {1 % g}; frontier = {1 % g}
        while frontier:
            new = set()
            for a in frontier:
                for r in sat:
                    b = a * r % g
                    if b not in H: H.add(b); new.add(b)
            frontier = new
        F = {1 % g}
        for r in frozen:
            e = rng.randint(0, 3); F = {f * pow(r, k, g) % g for f in F for k in range(e + 1)}
        HF = {h * f % g for h in H for f in F}
        op = ordmod(p, g)
        Absp = {k for k in range(op) if pow(pow(p, k, g), -1, g) in HF}
        t = next(t for t in range(1, op + 1) if pow(p, t, g) in H)
        Sp = {r for r in range(t) if any(pow(p, r, g) * f % g in H for f in F)}
        if {k for k in range(op) if k % t in Sp} != Absp: bad65 += 1
        if is_prime(g):
            if t != op // len(H & {pow(p, k, g) for k in range(op)}): bad65 += 1
        n65 += 1
    check('T65', f'quotient-residue formula Abs_p={{k: k mod t_p in S_p}}, t_p=order of p in (Z/g)*/H ({n65} cases, prime and composite g)', bad65 == 0, bad65)

    rng = random.Random(404); n_cert = 0; bad66 = 0; n_try = 0; multi = 0; t0 = time.time()
    while n_try < (150 if QUICK else 500):
        sd = gen_reset(rng)
        if not sd: continue
        g, E = sd; n_try += 1
        certified = []
        for r in E:
            o = ordmod(r, g)
            if E[r] < o - 1: continue
            o, Abs = abs_set(g, E, r)
            if not Abs: continue
            m = r ** maxgap(Abs, o)
            if m * m >= g: continue
            if any(g % p == 0 for p in small_primes(m * m)): continue
            if any(avail(g, E, M) for M in range(2, m) if gcd(M, r) == 1): continue
            certified.append((r, m, Abs, o))
        if len(certified) > 1: multi += 1
        for (r, m, Abs, o) in certified:
            n_cert += 1
            need = 4 * m * m * len(Abs) + 8
            mo = machine_orbit(g, 1, E, need)
            for k in range(1, len(mo)):
                if mo[k][2] and set(mo[k][2]) != {r}: bad66 += 1
            if len(mo) < need: bad66 += 1
    check('T66', f'static certificate S3-S5 sound: only r carries and the orbit stays persistent ({n_cert} certified states among {n_try} reset seeds)', bad66 == 0 and n_cert > 0, bad66)
    check('T66u', 'uniqueness: never two primes certified at one state', multi == 0, multi)

    bad = 0; n = 0; rng = random.Random(909); t0 = time.time()
    while n < (60 if QUICK else 150):
        sd = gen_reset(rng)
        if not sd: continue
        g, E = sd
        fc = find_cycle(g, 1, E)
        if fc is None: continue
        n1, n2, states = fc
        for (ga, Ec) in states[n1:]:
            if ga != 1: continue
            mo = machine_orbit(g, 1, Ec, 3 * g + 5)
            carries = {p for m in mo[1:] for p in m[2]}
            if len(carries) != 1: continue
            r = next(iter(carries))
            o, Abs = abs_set(g, Ec, r); m = r ** maxgap(Abs, o)
            ok = Ec.get(r, 0) >= o - 1 and m * m < g and not any(avail(g, Ec, M) for M in range(2, m) if gcd(M, r) == 1)
            n += 1
            if not ok: bad += 1
    check('T68a', f'prime g: every eventual reset state is statically certified for the active prime ({n} states)', bad == 0 and n > 0, bad)

    stat = {}; bad = 0
    for g in (15, 39, 51, 57, 87):
        o = ordmod(2, g); s = (g + 1) * (g + 2) ** o
        rows = persistent_orbit_ok(g, s, 9)
        if not all(r[0] == g for r in rows): bad += 1
        m = 2
        fails = any(g % p == 0 for p in small_primes(m * m))
        stat[g] = 'persistent; carry 2 (m=2); S5 fails' if fails else 'S5 holds'
        if not fails: bad += 1
    E68 = {3: 3, 13: 1, 3947: 8, 281: 4}
    fc = find_cycle(68, 1, E68)
    mo = machine_orbit(68, 1, E68, 150)
    dr = direct(state_to_x(68, 1, E68), 16)
    ok68 = fc is not None and len(mo) == 150 and all(r[3] == 68 for r in dr)
    gm = [m[0] for m in mo]
    per = next(q for q in range(1, 100) if all(gm[i + q] == gm[i] for i in range(40, 100)))
    carries = sorted({p for m in mo[60:] for p in m[2]})
    m68 = 3 ** 1
    stat[68] = f'persistent (direct, 16 steps; machine, 150); active carries {carries}; gamma-period {per}; prime factor 2 <= m^2'
    ok68 = ok68 and any(68 % p == 0 for p in small_primes(carries[0] ** 2 * 4))
    check('T73a', 'composite/even g=15,39,51,57,68: persistent orbits exist and S5 fails at the reset states (certificate not available); g=39 and 87 follow the same pattern', bad == 0 and ok68, stat)

    A = lambda k: (2 * 4 ** k + 1) // 3
    bad = 0
    for a in range(1, 300001 if not QUICK else 60001):
        if kappa_closed(a) != (kappa(a) if a <= 20000 else kappa_closed(a)): bad += 1
    # exhaustive agreement of closed form with iteration, in blocks around the thresholds A_k
    for k in range(0, 15):
        for a in range(max(1, A(k) - 3), A(k) + 4):
            if kappa(a) != kappa_closed(a): bad += 1
        if kappa(A(k)) != k or kappa(A(k) + 1) != k + 1: bad += 1
    for a in range(2, 5000):
        if kappa(a) > (a - 1).bit_length(): bad += 1
    vals = [kappa(a) for a in (2, 10, 100, 1000, 10 ** 6)]
    check('T69', 'kappa(a)=least k with 3a <= 2*4^k+1 (thresholds A_k=(2*4^k+1)/3); kappa(2,10,100,1000,10^6)=1,2,4,6,11; kappa <= ceil(log2 a)', bad == 0 and vals == [1, 2, 4, 6, 11], (bad, vals))

    W = json.load(open('witnesses.json'))
    bad = 0; rep = {}
    for k, (g, Es, gam0, K) in sorted(W.items(), key=lambda t: int(t[0])):
        E = {int(p): e for p, e in Es.items()}
        K1, n, ok = _descent(g, E, gam0)
        if not ok or K1 != int(k) or kappa(gam0) != int(k): bad += 1
        rep[int(k)] = (g, gam0, K1)
        if int(k) <= 8:
            rows = direct(state_to_x(g, gam0, E), n + 2)
            carries = sum(1 for i in range(1, n + 1) if rows[i][2] != rows[i - 1][2])
            if rows[n][1] != 1 or carries != int(k) or any(r[3] != g for r in rows[:n + 1]): bad += 1
    check('T69s', 'bound attained: exact orbits needing exactly kappa(gamma0) carries for kappa=1..11 (direct iteration of C for kappa<=8)', bad == 0 and sorted(rep) == list(range(1, 12)), rep)

    vals = {g: (Hclass(g), Kpoly(g)) for g in (11, 31, 59, 101, 197, 211)}
    ok = all(vals[g][0] == v for g, v in {11: 171, 31: 2655, 59: 21297195}.items())
    ok &= vals[11][1] == 2688 and vals[31][1] == 44928 and vals[59][1] == 1243920 and vals[101][1] == 10707144 and vals[197][1] == 229237866
    ok &= vals[211][0] == 24165141422031 and vals[211][1] == 113903360
    check('T70v', 'H(g) and K_poly(g) values for g=11,31,59,101,197,211 (H(211)=24165141422031, K_poly(211)=113903360)', ok, vals)

    rng = random.Random(31337); bad = 0; n = 0; entries = []; t0 = time.time()
    while n < (60 if QUICK else 150):
        sd = gen_reset(rng)
        if not sd: continue
        g, E = sd
        fc = find_cycle(g, 1, E, cap=4000)
        if fc is None: continue
        n1, n2, states = fc
        resets = [i for i, (ga, _) in enumerate(states) if ga == 1]
        ent = sum(1 for i in resets if i < n1)
        Hg, Kp = Hclass(g), Kpoly(g)
        n += 1; entries.append((g, ent, Hg, Kp))
        if ent > Hg - 1 or ent > Kp: bad += 1
    check('T70/T71', f'entry index <= H(g)-1 and <= K_poly(g) on {n} prime-g reset seeds (max observed {max(e[1] for e in entries)})', bad == 0, bad)
    globals()['ENTRIES'] = entries

    rng = random.Random(72); bad = {'chain': 0, 'gamma': 0, 'carry': 0, 'steps': 0, 'tail': 0, 'div': 0}
    norb = nseg = 0; maxchain = 0; t0 = time.time()
    cand = []
    for x in SEEDS[:: max(1, len(SEEDS) // 6000)]:
        G = Gof(fibre(x))
        if G > 1 and G not in (2, 3, 6) and not is_prime(G): cand.append(x)
    rng.shuffle(cand)
    for x0 in cand:
        if norb >= (150 if QUICK else 1000): break
        st = orbit_states(x0, 40)
        if len(st) < 40: continue
        Gs = [s[2] for s in st]
        segs = []; start = 0
        for i in range(1, len(st)):
            if Gs[i] != Gs[i - 1]: segs.append((start, i - 1)); start = i
        segs.append((start, len(st) - 1))
        g0 = Gs[0]; gsv = [Gs[a] for a, b in segs]
        norb += 1; nseg += len(segs)
        if sum(1 for g in gsv if g > 1) > sum(factor(g0).values()): bad['chain'] += 1
        maxchain = max(maxchain, len(segs))
        for a, b in zip(gsv, gsv[1:]):
            if a % b: bad['div'] += 1
        for si, (a, b) in enumerate(segs):
            g = Gs[a]
            if g == 1:
                t = int(st[a][0]) // (st[a][3] ** 2)
                nt = 0; tt = t
                while tt > 3: tt = squarefree_part(tt + 1); nt += 1
                if nt > 4 * kappa3(t): bad['tail'] += 1
                continue
            gam_i = int(st[a][0] * g / st[a][3] ** 2)
            carries = sum(1 for i in range(a + 1, b + 1) if st[i][3] != st[i - 1][3])
            if carries > kappa(gam_i) + Hclass(g) - 1: bad['carry'] += 1
            if (b - a) > (carries + 1) * 4 * g + 1: bad['steps'] += 1
            if si < len(segs) - 1:
                a2 = segs[si + 1][0]; g2 = Gs[a2]
                gam_before = int(st[b][0] * g / st[b][3] ** 2)
                gam_next = int(st[a2][0] * g2 / st[a2][3] ** 2)
                if gam_before > gam_i + 4 * g: bad['gamma'] += 1
                r2 = Fr(st[a2][3], st[b][3]) ** 2
                if Fr(gam_next) != Fr(g2, g) * (gam_before + 1) / r2: bad['gamma'] += 1
                if gam_next > Fr(g2 * (gam_i + 4 * g + 1), g): bad['gamma'] += 1
    check('T72', f'dynamic-G chains: (i)-(iv) as inequalities on {norb} orbits / {nseg} segments from composite or even G0 (max chain length {maxchain})', sum(bad.values()) == 0 and norb > 0, bad)

    def Rrec(g, Gam):
        if g == 1: return 0
        best = 0
        for g2 in [d for d in divisors_from(factor(g)) if 1 < d < g]:
            best = max(best, Rrec(g2, (g2 * (Gam + 4 * g + 1)) // g))
        return kappa(Gam) + Hclass(g) - 1 + best
    check('T72v', 'recursive bound R(g0,gamma0) is an explicit finite number (R(12,5), R(30,17))', Rrec(12, 5) > 0 and Rrec(30, 17) > 0, (Rrec(12, 5), Rrec(30, 17)))

if __name__ == '__main__':
    for fn in (ch1, ch2, ch3, ch4, ch5_7):
        t = time.time(); fn(); print('   [%s %.0fs]' % (fn.__name__, time.time() - t), flush=True)
    n = len(RES); npass = sum(1 for r in RES if r['pass'])
    print('\nSUMMARY: %d/%d checks passed (%.0fs)' % (npass, n, time.time() - T0))
    json.dump({'results': RES, 'passed': npass, 'total': n}, open('checks_volume_ii.run.json' if len(sys.argv) < 2 or '--record' not in sys.argv else 'checks_volume_ii.json', 'w'), indent=1, default=str)
    if npass != n: sys.exit(1)

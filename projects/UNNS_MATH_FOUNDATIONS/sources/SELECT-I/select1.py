#!/usr/bin/env python3
"""SELECT-I: generative operation selection on integer-anchor nest routes.
Route r=(k,d), k>=1, d>=2, value v(r)=k d^2. Deterministic; exact integer arithmetic; standard library only.
Independent of rgg1.py, rgg2.py, rgg21.py (not imported, not modified).
Labels in output: PASS/FAIL = asserted check; DATA = reported count, not asserted."""
import json, sys, itertools
from math import gcd

out, ok_all = {}, True
def check(name, cond, detail=""):
    global ok_all
    ok_all &= bool(cond); out[name] = {"pass": bool(cond), "detail": detail}
    print(("PASS " if cond else "FAIL ") + name + (f" [{detail}]" if detail else ""))
def info(name, detail):
    out[name] = {"data": detail}; print("DATA " + name + f" [{detail}]")

lcm = lambda a, b: a * b // gcd(a, b)
val = lambda r: r[0] * r[1] ** 2
valid = lambda r: r is not None and r[0] >= 1 and r[1] >= 2
def T(q, r):                                   # refinement T_q(k,d)=(k/q^2, dq), defined iff q^2 | k
    return (r[0] // (q * q), r[1] * q) if r[0] % (q * q) == 0 else None
def fibre(m):
    return [(m // (d * d), d) for d in range(2, int(m ** 0.5) + 1) if m % (d * d) == 0]
divides = lambda r, s: s[0] % r[0] == 0 and s[1] % r[1] == 0       # E-order (amplification reachability)

# ---------------- candidate operations ----------------
def J_join(r, s): return (lcm(r[0], s[0]), lcm(r[1], s[1]))
def J_max(r, s):  return max(r, s, key=lambda x: (val(x), x[1]))
def J_min(r, s):  return min(r, s, key=lambda x: (val(x), x[1]))
def J_lexmax(r, s): return max(r, s, key=lambda x: (x[1], x[0]))
def J_mul(r, s):  return (r[0] * s[0], r[1] * s[1])
def J_N(r, s):    return (lcm(r[0], s[0]), 1 + lcm(r[1] - 1, s[1] - 1))
def J_occ(r, s):
    M1, N1, M2, N2 = r[0] * (r[1] - 1), r[1] - 1, s[0] * (s[1] - 1), s[1] - 1
    Mj, Nj = lcm(M1, M2), lcm(N1, N2); return (Mj // Nj, Nj + 1)
def J_ref(r, s):
    L = lcm(r[1], s[1]); return (lcm(val(r), val(s)) // (L * L), L)
def J_mixB(r, s): return (gcd(r[0], s[0]), lcm(r[1], s[1]))
def J_mixA(r, s): g = gcd(r[1], s[1]); return (lcm(r[0], s[0]), g) if g >= 2 else None
def J_meet(r, s): g = gcd(r[1], s[1]); return (gcd(r[0], s[0]), g) if g >= 2 else None
OPS = {"J_join": J_join, "J_max": J_max, "J_min": J_min, "J_lexmax": J_lexmax, "J_mul": J_mul, "J_N": J_N,
       "J_occ": J_occ, "J_ref": J_ref, "J_mixB": J_mixB, "J_mixA": J_mixA, "J_meet": J_meet}

# ================= S1. coordinate rigidity =================
# requirement: g(q d)=q g(d) for primes q, d>=2 (g(d)=f(d-1)); claim g(d)=c d.
def ok_f(f, N=60, qs=(2, 3, 5, 7)):
    return all(f(q * (n + 1) - 1) == q * f(n) for n in range(1, N) for q in qs)
check("S1.1.f(N)=c(N+1) satisfies f(q(N+1)-1)=q f(N)", all(ok_f(lambda n, c=c: c * (n + 1)) for c in (1, 2, 3, 7)))
check("S1.2.f(N)=N, N^2, 2N+1, N+2 and floor(1.5(N+1)) violate it",
      not any(ok_f(f) for f in (lambda n: n, lambda n: n * n, lambda n: 2 * n + 1, lambda n: n + 2, lambda n: (3 * (n + 1)) // 2)))
# finite-range linear system: ratio constraints g(qd)/(qd) = g(d)/d. union-find; any two d1,d2 with lcm<=D must share a component.
D = 240; par = list(range(D + 1))
def find(x):
    while par[x] != x: par[x] = par[par[x]]; x = par[x]
    return x
primes = [p for p in range(2, D + 1) if all(p % t for t in range(2, int(p ** 0.5) + 1))]
for d in range(2, D + 1):
    for q in primes:
        if q * d <= D: par[find(q * d)] = find(d)
okU = all(find(a) == find(b) for a in range(2, 60) for b in range(a + 1, 60) if lcm(a, b) <= D)
check("S1.3.finite-range: every d1,d2 with lcm<=240 lie in one ratio class, so g(d)/d is constant on linked d", okU)
# non-covariance of J_N and J_occ under joint refinement; covariance of J_join
r, s = (4, 2), (4, 3)
ex = (J_N(T(2, r), T(2, s)), T(2, J_N(r, s)), J_join(T(2, r), T(2, s)), T(2, J_join(r, s)))
check("S1.4.worked example r=(4,2),s=(4,3),q=2: J_join (1,12)=(1,12); J_N (1,16) vs (1,6)", ex == ((1, 16), (1, 6), (1, 12), (1, 12)), str(ex))
def cov_fail(op, K=36, Dm=12):
    bad = tot = 0
    for r in itertools.product(range(1, K + 1), range(2, Dm + 1)):
        for s in itertools.product(range(1, K + 1), range(2, Dm + 1)):
            for q in (2, 3):
                a, b = T(q, r), T(q, s)
                if a is None or b is None: continue
                j = op(r, s); lhs = op(a, b); rhs = T(q, j) if valid(j) else None
                tot += 1; bad += (lhs is None or rhs is None or lhs != rhs)
    return bad, tot
cj = cov_fail(J_join); cn = cov_fail(J_N); co = cov_fail(J_occ)
check("S1.5.J_join covariant on all tested pairs; J_N and J_occ are not", cj[0] == 0 and cn[0] > 0 and co[0] > 0,
      f"failures join {cj[0]}/{cj[1]}, J_N {cn[0]}/{cn[1]}, J_occ {co[0]}/{co[1]}")

# ================= S2. generative reachability =================
PR = (2, 3, 5, 7, 11, 13, 17, 19, 23)
def moves(r, mode, KB, DB):
    k, d = r; res = []
    for p in PR:
        if k * p <= KB: res.append((k * p, d))
        if d * p <= DB: res.append((k, d * p))
        if mode >= 1 and k % (p * p) == 0 and d * p <= DB: res.append((k // (p * p), d * p))
        if mode >= 2 and d % p == 0 and d // p >= 2 and k * p * p <= KB: res.append((k * p * p, d // p))
    return res
def reach(src, mode, KB, DB):
    seen = {src}; st = [src]
    while st:
        x = st.pop()
        for y in moves(x, mode, KB, DB):
            if y not in seen: seen.add(y); st.append(y)
    return seen
srcs = [(k, d) for k in range(1, 7) for d in range(2, 7)]
TG = [(k, d) for k in range(1, 25) for d in range(2, 25)]
ok2a = all({t for t in reach(r, 0, 24, 24)} == {t for t in TG if divides(r, t)} for r in srcs)
check("S2.1.amplification-only reachability = divisibility (k|k', d|d'); exact (moves are monotone)", ok2a)
KB, DB = 24 * 24, 48
ok2b = all({t for t in reach(r, 1, KB, DB) if t in set(TG)} == {t for t in TG if t[1] % r[1] == 0 and val(t) % val(r) == 0} for r in srcs)
check("S2.2.amplification + forward refinement: reachable iff d|d' and v|v'", ok2b)
KB2, DB2 = 24 * 24, 6 * 24   # larger d-bound: reaching a prime d' from d needs the intermediate d*d'
ok2c = all({t for t in reach(r, 2, KB2, DB2) if t in set(TG)} == {t for t in TG if val(t) % val(r) == 0} for r in srcs if r[0] <= 3)
check("S2.3.amplification + refinement and inverses: reachable iff v|v' (equal-value routes mutually reachable); sources k<=3", ok2c)

# ================= S3. minimal continuation =================
LEQ = {0: lambda r, t: t[0] % r[0] == 0 and t[1] % r[1] == 0,
       1: lambda r, t: t[1] % r[1] == 0 and val(t) % val(r) == 0,
       2: lambda r, t: val(t) % val(r) == 0}          # predicates verified against BFS in S2
def universe(vmax):
    return [(k, d) for d in range(2, int(vmax ** 0.5) + 1) for k in range(1, vmax // (d * d) + 1)]
def minimal_upper(r, s, mode, *_):
    le = LEQ[mode]
    if mode == 0: C = [(k, d) for k in range(1, 61) for d in range(2, 61)]      # J_join of sources k,d<=6 lies in this box
    else: C = universe(4 * lcm(val(r), val(s)))
    U = [u for u in C if le(r, u) and le(s, u)]
    return [u for u in U if not any(le(w, u) and not le(u, w) for w in U)]
pairs = [(r, s) for r in srcs[:12] for s in srcs[:12]]
ok3a = True
for r, s in pairs:
    m = minimal_upper(r, s, 0, 80, 80); ok3a &= (m == [J_join(r, s)])
check("S3.1.E-order: unique least common continuation = J_join (brute force)", ok3a, f"{len(pairs)} pairs")
ok3b = True; okval = True
for r, s in pairs:
    m = minimal_upper(r, s, 1, 6 * 80, 80); ok3b &= (len(m) == 1 and m[0] == J_ref(r, s)); okval &= (val(J_ref(r, s)) == lcm(val(r), val(s)))
check("S3.2.E+forward-T order: unique least common continuation = J_ref=(lcm(v)/L^2, L), value lcm(v_r,v_s)", ok3b and okval, f"{len(pairs)} pairs")
cnt = 0; ok3c = True
for r, s in pairs:
    m = minimal_upper(r, s, 2, 6 * 80, 80); target = lcm(val(r), val(s))
    ok3c &= (set(m) == set(fibre(target))) ; cnt += len(m) > 1
check("S3.3.E+T and inverses: minimal common continuations = the whole fibre F(lcm(v_r,v_s)); no single route is selected", ok3c, f"{cnt}/{len(pairs)} pairs have >1 minimal continuation")
# separation of fibres: J_join separates, J_ref gives exactly m
oksep = okref = True; n = 0
for m in range(1, 3001):
    F = fibre(m)
    for r, s in itertools.combinations(F, 2):
        n += 1; oksep &= val(J_join(r, s)) > m; okref &= val(J_ref(r, s)) == m
check("S3.4.fibre separation: v(J_join(r,r'))>m for all pairs, v(J_ref(r,r'))=m for all pairs (m<=3000)", oksep and okref, f"{n} same-value pairs")

# ================= S4. discrimination matrix =================
BOX = [(k, d) for k in range(1, 11) for d in range(2, 11)]
GRID = [(k, d) for k in range(1, 25) for d in range(2, 25)]
def props(name, op):
    p = {}
    res = {(r, s): op(r, s) for r in BOX for s in BOX}
    p["closed"] = all(valid(x) for x in res.values())
    p["comm"] = all(res[(r, s)] == res[(s, r)] for r in BOX for s in BOX if valid(res[(r, s)]))
    p["idem"] = all(res[(r, r)] == r for r in BOX)
    ok = True
    for r in BOX:
        for s in BOX:
            a = res[(r, s)]
            if not valid(a): continue
            for t in BOX:
                b = res[(s, t)]
                if not valid(b): continue
                x, y = op(a, t), op(r, b)
                if valid(x) and valid(y) and x != y: ok = False; break
            if not ok: break
        if not ok: break
    p["assoc"] = ok
    p["cov"] = cov_fail(op, K=24, Dm=10)[0] == 0
    p["retention"] = all((not valid(res[(r, s)])) or (divides(r, res[(r, s)]) and divides(s, res[(r, s)])) for r in BOX for s in BOX) and p["closed"]
    p["absorption"] = all(res[(r, s)] == s for r in BOX for s in BOX if divides(r, s))
    sepok = True; any_pair = False
    for m in range(1, 1501):
        for r, s in itertools.combinations(fibre(m), 2):
            any_pair = True; j0 = op(r, r); j1 = op(s, r)     # probe r: does it tell r from r'?
            if not (valid(j0) and valid(j1)) or val(j0) == val(j1): sepok = False
    p["separates_fibres"] = sepok
    byv = {}
    for r in GRID:
        for s in GRID:
            j = op(r, s)
            if valid(j): byv.setdefault((val(r), val(s)), set()).add(val(j))
    p["value_descends"] = all(len(v) == 1 for v in byv.values())
    return p
EXPECT = {  # closed comm idem assoc cov retention absorption separates value_descends
 "J_join":  (1, 1, 1, 1, 1, 1, 1, 1, 0),
 "J_max":   (1, 1, 1, 1, 1, 0, 1, 0, 1),
 "J_min":   (1, 1, 1, 1, 1, 0, 0, 0, 1),
 "J_lexmax":(1, 1, 1, 1, 1, 0, 1, 0, 0),
 "J_mul":   (1, 1, 0, 1, 0, 1, 0, 0, 1),
 "J_N":     (1, 1, 1, 1, 0, 0, 0, 1, 0),
 "J_occ":   (1, 1, 1, 1, 0, 0, 0, 1, 0),
 "J_ref":   (1, 1, 1, 1, 1, 0, 1, 0, 1),
 "J_mixB":  (1, 1, 1, 1, 1, 0, 0, 0, 0),
 "J_mixA":  (0, 1, 1, 1, 0, 0, 0, 0, 0),
 "J_meet":  (0, 1, 1, 1, 0, 0, 0, 0, 0),
}
KEYS = ["closed", "comm", "idem", "assoc", "cov", "retention", "absorption", "separates_fibres", "value_descends"]
MATRIX = {}
for name, op in OPS.items():
    p = props(name, op); MATRIX[name] = tuple(int(p[k]) for k in KEYS)
print("\nDISCRIMINATION MATRIX (1=holds on all tested inputs)\n" + "op        " + " ".join(f"{k[:9]:>9}" for k in KEYS))
for name, row in MATRIX.items(): print(f"{name:<9} " + " ".join(f"{x:>9}" for x in row))
print()
for name in OPS:
    # J_mixA/J_meet are partial: 'closed' fails; their other columns are evaluated only on defined values and are not claimed
    if name in ("J_mixA", "J_meet"):
        check(f"S4.{name}.partial (not closed on the anchor domain)", MATRIX[name][0] == 0)
    else:
        check(f"S4.{name}.matches expected profile", MATRIX[name] == EXPECT[name], str(MATRIX[name]))
core = [n for n in OPS if MATRIX[n][:5] == (1, 1, 1, 1, 1)]
info("S4.algebra+covariance admits", f"{core}")
info("S4.adding retention admits", f"{[n for n in core if MATRIX[n][5]]}")
info("S4.adding retention+absorption admits", f"{[n for n in core if MATRIX[n][5] and MATRIX[n][6]]}")

# ---- order-induced operation (J is the lub of its own order) and which order each semilattice induces ----
def order_of(op):  # r <=_J s iff J(r,s)=s  (box)
    return {(r, s) for r in BOX for s in BOX if op(r, s) == s}
E_order = {(r, s) for r in BOX for s in BOX if divides(r, s)}
ETp_order = {(r, s) for r in BOX for s in BOX if s[1] % r[1] == 0 and val(s) % val(r) == 0}
check("S3.5.order induced by J_join is the amplification order; by J_ref the amplification+forward-refinement order",
      order_of(J_join) == E_order and order_of(J_ref) == ETp_order)
okl = True
for name in ("J_join", "J_ref", "J_max", "J_lexmax", "J_mixB"):
    op = OPS[name]; le = order_of(op)
    for r in BOX[:30]:
        for s in BOX[:30]:
            j = op(r, s)
            if j in set(BOX):
                ub = [u for u in BOX if (r, u) in le and (s, u) in le]
                okl &= (r, j) in le and (s, j) in le and all((j, u) in le for u in ub)
check("S3.6.each semilattice operation is the least upper bound of the order it induces (tested on box)", okl)

# ================= S5. intrinsic nesting vs factor retention =================
# nest iteration on a value: (M (x) N) with M=m integer value, N|m  ->  m' = (m/N)(N+1)^2
okn = True; nn = 0
for m in range(2, 2001):
    for N in range(1, m + 1):
        if m % N == 0:
            mp = (m // N) * (N + 1) ** 2; nn += 1
            okn &= (mp % m == 0) == (N == 1) and (N != 1 or mp == 4 * m)
check("S5.1.iterating the nest rule on its own value: m | m' only for N=1 (m'=4m); every N>1 consumes a factor", okn, f"{nn} (m,N) pairs, m<=2000")
info("S5.2.status", "amplification moves E_{p,k},E_{p,d} are not generated by the nest rule or by T_q; their adoption is a hypothesis (see note)")

json.dump(out, open("select1_report.json", "w"), indent=1, default=str)
print("\nALL PASS" if ok_all else "\nSOME FAILED"); sys.exit(0 if ok_all else 1)

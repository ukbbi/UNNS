#!/usr/bin/env python3
"""RGG-2.1: consolidation of RGG-2. (i) correction: admissibility of mixed operations / fibre is a
join-semilattice, not a lattice; (ii) Single-Probe Fibre Reconstruction Theorem; (iii) coordinate-robustness lemma.
Independent of rgg1.py / rgg2.py (not modified). Exact integer arithmetic."""
import json, sys, itertools
from math import gcd, isqrt, log

out, ok_all = {}, True
def check(name, cond, detail=""):
    global ok_all
    ok_all &= bool(cond); out[name] = {"pass": bool(cond), "detail": detail}
    print(("PASS " if cond else "FAIL ") + name + (f" [{detail}]" if detail else ""))
def info(name, detail):
    out[name] = {"data": detail}; print("DATA " + name + f" [{detail}]")

lcm = lambda a, b: a * b // gcd(a, b)
val = lambda r: r[0] * r[1] ** 2
def fibre(m):
    res, d = [], 2
    while d * d <= m:
        if m % (d * d) == 0: res.append((m // (d * d), d))
        d += 1
    return res
def factor(n):
    f, p = {}, 2
    while p * p <= n:
        while n % p == 0: f[p] = f.get(p, 0) + 1; n //= p
        p += 1
    if n > 1: f[n] = f.get(n, 0) + 1
    return f
def h(m):
    r = 1
    for p, e in factor(m).items(): r *= p ** (e // 2)
    return r
join = lambda r, s: (lcm(r[0], s[0]), lcm(r[1], s[1]))
admissible = lambda r: r[0] >= 1 and r[1] >= 2

LIM = 6000
FIB = {m: fibre(m) for m in range(1, LIM + 1)}
MULTI = [m for m in FIB if len(FIB[m]) >= 2]

# ---------- A. correction: mixed operations and the fibre order ----------
n = bad1 = ok2 = 0; ex = None; okA = True
for m in MULTI:
    for r, r2 in itertools.combinations(FIB[m], 2):
        g, L = gcd(r[1], r2[1]), lcm(r[1], r2[1]); n += 1
        mix1 = (lcm(r[0], r2[0]), g); mix2 = (gcd(r[0], r2[0]), L)
        okA &= (mix1 == (m // g ** 2, g)) and (mix2 == (m // L ** 2, L)) and val(mix1) == m and val(mix2) == m   # algebra (as in RGG-2 9b)
        if not admissible(mix1):
            bad1 += 1; ex = ex or (r, r2, mix1)
        ok2 += admissible(mix2) and mix2 in FIB[m]
check("A1.mixed_algebra_identity (RGG-2 9b, unchanged)", okA)
check("A2.(lcm k,gcd d) inadmissible exactly when g=1; m=72 example (18,2),(8,3)->(72,1)", bad1 == sum(1 for m in MULTI for r, r2 in itertools.combinations(FIB[m], 2) if gcd(r[1], r2[1]) == 1) and (lcm(18, 8), gcd(2, 3)) == (72, 1) and not admissible((72, 1)), f"{bad1}/{n} same-value pairs leave the anchor domain; first {ex}")
check("A3.(gcd k,lcm d) always admissible and inside the fibre", ok2 == n)
# fibre ordered by d-divisibility: join (lcm d) always inside, meet only if gcd d>=2 => join-semilattice, not lattice
okS = True
for m in MULTI:
    F = FIB[m]
    for r, r2 in itertools.combinations(F, 2):
        L = lcm(r[1], r2[1]); jr = (m // L ** 2, L)
        okS &= jr in F and L % r[1] == 0 and L % r2[1] == 0
        # least upper bound within F: every upper bound has d divisible by L
        okS &= all(u[1] % L == 0 for u in F if u[1] % r[1] == 0 and u[1] % r2[1] == 0)
check("A4.fibre_is_join_semilattice_in_d-order (lub = lcm d)", okS)
nolower = sum(1 for m in MULTI for r, r2 in itertools.combinations(FIB[m], 2) if gcd(r[1], r2[1]) == 1)
check("A5.fibre_not_a_lattice: pairs with no lower bound exist", nolower > 0, f"{nolower} same-value pairs with gcd(d,d')=1 have no common lower bound in F(m)")
# lattice after adjoining the formal route (m,1) (d=1, value m)
okL = True
for m in MULTI:
    F = FIB[m] + [(m, 1)]
    for r, r2 in itertools.combinations(F, 2):
        g, L = gcd(r[1], r2[1]), lcm(r[1], r2[1])
        okL &= (m // g ** 2, g) in F and (m // L ** 2, L) in F
check("A6.with_formal_d=1_route_adjoined_the_fibre_is_closed_under_both (lattice)", okL)

# ---------- B. Single-Probe Fibre Reconstruction Theorem ----------
LIM_B = 20000
okB = okInj = okDec = okSq = okVal = True; nfib = 0
for m in range(1, LIM_B + 1):
    F = fibre(m); H = h(m)
    if not F:
        okSq &= (H == 1); continue
    nfib += 1
    s = (m // (H * H), H)
    okB &= admissible(s) and s in F and all(d_ok for d_ok in [True])
    vals = []
    for (k, d) in F:
        okB &= H % d == 0
        j = join((k, d), s)
        okVal &= j == (m // (d * d), H) and val(j) == m * (H // d) ** 2
        vals.append(val(j))
        q = m * H * H // val(j)                       # decoding: d^2 = m h^2 / v(r v s)
        okDec &= isqrt(q) ** 2 == q and isqrt(q) == d
    okInj &= len(set(vals)) == len(F)
check("B1.h(m)=1 iff m squarefree (fibre empty), else s_m admissible and in F(m)", okSq and okB, f"{nfib} nonempty fibres, m<={LIM_B}")
check("B2.r v s_m=(m/d^2,h) and v=m(h/d)^2", okVal)
check("B3.single_probe_injective_on_every_fibre", okInj)
check("B4.exact_decoding: d=sqrt(m h^2/v(r v s_m)), route=(m/d^2,d)", okDec)
check("B5.fibre_of_72", h(72) == 6 and [val(join(r, (2, 6))) for r in fibre(72)] == [648, 288, 72], str([val(join(r, (2, 6))) for r in fibre(72)]))
# generalised probe family: any s with h | d_s and k_s | m/h^2 resolves (probe need not lie in the fibre)
okG = True; nG = 0
for m in MULTI:
    if m > 3000: break
    F, H = FIB[m], h(m)
    for ks in range(1, 41):
        for ds in range(2, 61):
            if ds % H == 0 and (m // (H * H)) % ks == 0:
                nG += 1; okG &= len({val(join(r, (ks, ds))) for r in F}) == len(F)
check("B6.generalised_resolving_probes: h|d_s and k_s|m/h^2 (proved: lcm d=d_s, lcm k=m/d^2)", okG and nG > 0, f"{nG} (fibre,probe) pairs")
# how special are the sufficient conditions? data
tot = res = res_cond = 0
for m in MULTI:
    if m > 3000: break
    F, H = FIB[m], h(m)
    for ks in range(1, 13):
        for ds in range(2, 13):
            tot += 1; r_ok = len({val(join(r, (ks, ds))) for r in F}) == len(F); res += r_ok
            res_cond += (ds % H == 0 and (m // (H * H)) % ks == 0)
info("B7.resolving_probes_in_12x12_grid", f"{res}/{tot} resolve; {res_cond} satisfy the sufficient condition (not claimed necessary)")

# ---------- C. coordinate-robustness lemma ----------
# Lemma: if v is strictly increasing in each coordinate and J(r,s)>=r,s coordinatewise with J(r,r)=r, then equal-value distinct routes are separated: v(J(r,r'))>v(r).
occ = lambda r: (r[0] * (r[1] - 1), r[1] - 1)
def j_N(r, s): return (lcm(r[0], s[0]), lcm(r[1] - 1, s[1] - 1) + 1)
def j_occ(r, s):
    (M, N), (M2, N2) = occ(r), occ(s); Mj, Nj = lcm(M, M2), lcm(N, N2); assert Mj % Nj == 0; return (Mj // Nj, Nj + 1)
vM = lambda M, N: M * (N + 1) ** 2 / N
monok = all(a * b * b < a2 * b * b for a in range(1, 30) for b in range(2, 30) for a2 in [a + 1]) and \
        all(a * b * b < a * (b + 1) ** 2 for a in range(1, 30) for b in range(2, 60))
monoN = all(vM(M, N) < vM(M + 1, N) for M in range(1, 40) for N in range(1, 40)) and all(vM(M, N) < vM(M, N + 1) for M in range(1, 60) for N in range(1, 60))
check("C1.v_strictly_increasing_in_each_coordinate_in_(k,d)_and_(M,N)_charts", monok and monoN)
okC = True; nC = 0
for m in MULTI:
    for r, r2 in itertools.combinations(FIB[m], 2):
        nC += 1
        for op in (join, j_N, j_occ):
            okC &= val(op(r, r2)) > m and val(op(r, r)) == m
check("C2.separation_holds_for_all_three_coordinate_joins", okC, f"{nC} same-value pairs, m<={LIM}")
# single probe s_m under alternative coordinates (data only)
cN = cO = nf = 0
for m in MULTI:
    if m > 6000: break
    F, H = FIB[m], h(m); s = (m // (H * H), H); nf += 1
    cN += len({val(j_N(r, s)) for r in F}) == len(F); cO += len({val(j_occ(r, s)) for r in F}) == len(F)
info("C3.s_m_resolves_under_alternative_joins", f"(k,N): {cN}/{nf} fibres; (M,N): {cO}/{nf} fibres (theorem proved only for (k,d))")

json.dump(out, open("rgg21_report.json", "w"), indent=1, default=str)
print("\nALL PASS" if ok_all else "\nSOME FAILED"); sys.exit(0 if ok_all else 1)

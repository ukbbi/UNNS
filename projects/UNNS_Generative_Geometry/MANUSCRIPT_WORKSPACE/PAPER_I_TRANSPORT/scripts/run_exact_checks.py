import json, sys, random, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lattice_cells import *
from fractions import Fraction as Fr
R = {}
def rec(name, ok, info=""):
    R[name] = {"pass": bool(ok), "info": str(info)}; print(("PASS " if ok else "FAIL "), name, info)

# --- E2-1 : arithmetic of the three-stage orbit, directly from the definition D(x)
from math import gcd
def lcm(a, b): return a*b//gcd(a, b)
def D_of(a, b, cand):
    return sorted(d for d in cand if d >= 2 and a % (d*d) == 0 and (d-1) % b == 0)
def divisors(n):
    ds = [1]
    for p in range(2, int(n**0.5)+2):
        pass
    return [d for d in range(1, n+1) if n % d == 0] if n < 10**6 else None
P = 110
cand = [2**a*5**b*11**c for a in range(3) for b in range(3) for c in range(3)]
a0, b0 = P**4, 3
D0 = D_of(a0, b0, cand); L0 = 1; G0 = 0
for d in D0: L0 = lcm(L0, d); G0 = gcd(G0, d-1)
x1n = 2*P**4; D1 = D_of(x1n, 3, cand); L1 = 1; G1 = 0
for d in D1: L1 = lcm(L1, d); G1 = gcd(G1, d-1)
D2 = D_of(P**4, 1, cand)
rec("E2-1 stage0 |D|=13,L=P^2,G=3", len(D0) == 13 and L0 == P*P and G0 == 3, (len(D0), L0, G0))
rec("E2-1 stage1 D unchanged, x2=P^4", D1 == D0 and L1 == L0 and G1 == G0 and Fr(P**4, 3)+Fr(L0**2, G0) == Fr(2*P**4, 3) and Fr(2*P**4, 3)+Fr(L1**2, G1) == P**4, "")
rec("E2-1 stage2 |D|=26", len(D2) == 26 and set(D0) < set(D2), len(D2))

# --- E2-1 specimen complexes: even-sum vs Z^3, box (2,2,2)
q = (2, 2, 2)
ev = lambda v: sum(v) % 2 == 0
zz = lambda v: True
Ge, Gz = graver(ev, q), graver(zz, q)
rec("E2-5 Graver(Z^3) = {±e_i}", sorted(Gz) == sorted([tuple(s*(i == j) for j in range(3)) for i in range(3) for s in (1, -1)]), len(Gz))
exp = set()
for i in range(3):
    for s in (1, -1):
        exp.add(tuple(2*s*(i == j) for j in range(3)))
for i in range(3):
    for j in range(i+1, 3):
        for s in (1, -1):
            for t in (1, -1):
                v = [0, 0, 0]; v[i] = s; v[j] = t; exp.add(tuple(v))
rec("E2-5 Graver(even-sum) = {±2e_i, ±e_i±e_j}", set(Ge) == exp, len(Ge))
C0, C2 = cells(ev, q), cells(zz, q)
rec("E2-10 f-vectors (13,45,36,3)->(26,51,33,7)", fvec(C0) == (13, 45, 36, 3) and fvec(C2) == (26, 51, 33, 7), (fvec(C0), fvec(C2)))
b0, b2 = betti(C0), betti(C2)
rec("E2-10 Betti(K_abs) (1,6,6,0)->(1,0,0,0) over Q", b0 == [1, 6, 6, 0] and b2 == [1, 0, 0, 0], (b0, b2))
V = lambda C, d: {vertices(c) for c in C[d]}
lost = [d for d in (1, 2, 3) if True]
res = {d: (len(V(C0, d) & V(C2, d)), len(V(C0, d)-V(C2, d)), len(V(C2, d)-V(C0, d))) for d in (1, 2, 3)}
rec("E2-6 cor: no positive-dim cell persists; lost 45/36/3, new 51/33/7", all(res[d][0] == 0 for d in res) and res[1][1:] == (45, 51) and res[2][1:] == (36, 33) and res[3][1:] == (3, 7), res)
# E2-8 lost edges retained: midpoints and quarter points of every source edge lie in U(Z^3)
ok = True
for (u, gens) in C0[1]:
    g = gens[0]
    for t in (Fr(1, 4), Fr(1, 3), Fr(1, 2), Fr(2, 3), Fr(3, 4)):
        p = tuple(Fr(a)+t*b for a, b in zip(u, g))
        if not in_union(C2, p): ok = False
rec("E2-8 sampled points of all 45 lost edges lie in U(Z^3) (check of theorem, not proof)", ok, "")
# E2-9 the witness cell
cw = ((0, 0, 2), ((0, 1, -1), (1, 0, -1)))
rec("E2-9 witness is a source cell, contains (2/3,2/3,2/3), point not in U(Z^3)",
    cw in C0[2] and solve_in_cell(cw, (Fr(2, 3),)*3) and not in_union(C2, (Fr(2, 3),)*3), "")
rec("E2-9 point (1,0,0) in U(Z^3) not in U(even-sum)", in_union(C2, (1, 0, 0)) and not in_union(C0, (1, 0, 0)), "")

# --- P2-TF1 : family 21^{2h}/5 -> 21^{2h}/4
def tf1(h):
    num = 21**(2*h)
    cand = [3**a*7**b for a in range(h+1) for b in range(h+1)]
    D = D_of(num, 5, cand); L = 1; G = 0
    for d in D: L = lcm(L, d); G = gcd(G, d-1)
    Dp = D_of(num, 4, cand)
    return D, L, G, Fr(num, 5)+Fr(L*L, G) == Fr(num, 4)
okA = True
for h in (1, 2, 3, 4):
    D, L, G, eq = tf1(h)
    okA &= (L == 21**h and G == 20 and eq and
            set(D) == {3**a*7**b for a in range(h+1) for b in range(h+1) if (a, b) != (0, 0) and (a-b) % 4 == 0})
rec("P2-TF1(i) D,L,G, C(x_h)=21^{2h}/4 for h=1..4 (direct)", okA, "")
lat = lambda v: (v[0]-v[1]) % 4 == 0
latp = lambda v: (v[0]-v[1]) % 2 == 0
okB = True; info = []
for h in range(1, 13):
    qq = (h, h); Cs, Ct = cells(lat, qq), cells(latp, qq)
    Es, Et = V(Cs, 1), V(Ct, 1)
    kept = len(Es & Et)
    c = [sum(1 for n in range(h) if n % 4 == r) for r in range(4)]
    formula = sum(x*x for x in c)-1
    two = len(V(Cs, 2) & V(Ct, 2))
    Gs = {g for g in graver(lat, qq) if lexpos(g)}; Gt = {g for g in graver(latp, qq) if lexpos(g)}
    okB &= (kept == formula and two == 0 and Gs & Gt == {(1, 1)})
    info.append((h, kept))
rec("P2-TF1(iii,iv) S={±(1,1)}, no 2-cell persists, E_kept=Σc_r^2-1 (h=1..12, direct)", okB, info[-3:])

# --- P5-C1, P5-C2, P5-C3, erratum E1 example, P5-S4(i)
q4 = (2, 4, 2)
src = lambda v: all(x % 2 == 0 for x in v) and (sum(v)//2) % 2 == 0
tgt = lambda v: all(x % 2 == 0 for x in v)
bcc = lambda v: len({x % 2 for x in v}) == 1
Cs = cells(src, q4); Ct = cells(tgt, q4); Cb = cells(bcc, q4)
g, h, u = (0, 2, -2), (2, -2, 0), (0, 2, 2)
cellC1 = (u, tuple(sorted([g, h])))
p = (Fr(2, 3), Fr(5, 3), Fr(5, 3))
rec("P5-C1 Graver(2E3)=2*Graver(E3); C is a 2-cell; p=u+g/6+h/3 in C; p not in U(2Z^3,Q)",
    set(graver(src, q4)) == {tuple(2*x for x in v) for v in graver(ev, (1, 2, 1))}
    and cellC1 in Cs[2] and p == tuple(Fr(a)+Fr(1, 6)*b+Fr(1, 3)*c for a, b, c in zip(u, g, h))
    and solve_in_cell(cellC1, p) and not in_union(Ct, p), "")
rec("P5-C1 axis orders of 2Z^3 are (2,2,2): e_i not in target", not any(tgt(tuple(int(i == j) for j in range(3))) for i in range(3)), "")
pb = (Fr(5, 6), Fr(5, 3), Fr(3, 2))
rec("P5-C3 BCC target: witness (5/6,5/3,3/2) in U(source), not in U(BCC); BCC has no split coordinate",
    in_union(Cs, pb) and not in_union(Cb, pb)
    and all(any(bcc(v) != (bcc(tuple(0 if j == i else v[j] for j in range(3))) and bcc(tuple(v[j] if j == i else 0 for j in range(3))))
                for v in product(range(-3, 4), repeat=3)) for i in range(3)), "")
Ce3 = cells(ev, (1, 2, 1)); Cz3 = cells(zz, (1, 2, 1))
rec("P5-D1 dilation: U(2E3,(2,4,2)) point count test: witness of E3<=Z3 at (1/3,5/6,5/6) -> (2/3,5/3,5/3)",
    any(solve_in_cell(c, (Fr(1, 3), Fr(5, 6), Fr(5, 6))) for c in Ce3[2]) and not in_union(Cz3, (Fr(1, 3), Fr(5, 6), Fr(5, 6))), "")
# erratum E1 counterexample
qE = (2, 2, 2)
L1_ = lambda v: v[0] % 2 == 0 and v[1] % 2 == 0 and v[2] % 2 == 0
L2_ = lambda v: v[2] % 2 == 0
CL, CLp = cells(L1_, qE), cells(L2_, qE)
cE = ((0, 0, 2), ((0, 2, 0), (2, 0, 0)))
rec("E1 erratum: [0,2]^2x{2} is a source cell, (1/2,1/2,2) in U(Λ',Q) (so old (ii) was wrong)",
    cE in CL[2] and in_union(CLp, (Fr(1, 2), Fr(1, 2), 2)), "")
# the planar projection of that cell leaves the origin-excluded planar union
C2p = cells(lambda v: True, (2, 2))
rec("E1: proj of cell contains (1/2,1/2) outside planar U(Z^2,(2,2)) (the origin-excluded slice)", not in_union(C2p, (Fr(1, 2), Fr(1, 2))), "")
# P5-S4(i) pointwise on a few cases: lattices Λ'_2 and k
def s4i(lat2, k, Q):
    lat3 = lambda v: lat2(v[:2]) and v[2] % k == 0
    C3 = cells(lat3, Q); C2d = cells(lambda v: lat2(v), Q[:2])
    # U0: allow origin as corner
    def cells_with_origin(lat2, Q2):
        base = cells(lat2, Q2)
        # origin-allowed: enumerate with F including 0
        G = sorted(g for g in graver(lat2, Q2) if lexpos(g)); F0 = set(fibre(lat2, Q2)) | {(0, 0)}
        out = set()
        for j in (0, 1, 2):
            for gens in combinations(G, j):
                if j and rank(gens) < j: continue
                for u in F0:
                    if all(add(u, tuple(sum(m*g[c] for m, g in zip(mask, gens)) for c in range(2))) in F0 for mask in product((0, 1), repeat=j)):
                        out.add((u, gens))
        return out
    U0 = cells_with_origin(lat2, Q[:2])
    J = Q[2]//k; bad = 0; n = 0
    from fractions import Fraction as Fr
    for x in range(0, 4*Q[0]+1):
        for y in range(0, 4*Q[1]+1):
            for z in range(0, 4*Q[2]+1):
                p = (Fr(x, 4), Fr(y, 4), Fr(z, 4)); n += 1
                lhs = in_union(C3, p)
                pl = p[:2]
                if J == 0: rhs = (p[2] == 0 and in_union(C2d, pl))
                else:
                    rhs = (p[2] <= k and in_union(C2d, pl)) or (k <= p[2] <= k*J and any(solve_in_cell(c, pl) for c in U0))
                bad += (lhs != rhs)
    return n, bad
tot = 0; bd = 0
for lat2, k, Q in [(lambda v: True, 1, (2, 2, 2)), (lambda v: True, 2, (2, 2, 4)), (lambda v: (v[0]+v[1]) % 2 == 0, 1, (2, 2, 2)),
                   (lambda v: (v[0]+v[1]) % 2 == 0, 2, (2, 2, 4)), (lambda v: v[0] % 2 == 0, 2, (2, 2, 2))]:
    n, b = s4i(lat2, k, Q); tot += n; bd += b
rec("P5-S4(i) union identity pointwise on quarter-grids (5 cases)", bd == 0, (tot, bd))

# --- planar monotonicity P5-P1 : sampled corroboration only
random.seed(11)
def rand_lat2(maxidx):
    # sublattice of Z^2 by HNF basis (a,b;0,c)
    while True:
        a = random.randint(1, maxidx); c = random.randint(1, maxidx); b = random.randint(0, a-1)
        if a*c <= maxidx: return (a, b, c)
def mem(H):
    a, b, c = H
    # lattice generated by (a,b),(0,c)
    return lambda v: v[0] % a == 0 and (v[1]-(v[0]//a)*b) % c == 0 if a else False
def sub_of(H1, H2):  # H1 subset of H2 by generators
    return mem(H2)((H1[0], H1[1])) and mem(H2)((0, H1[2]))
checked = viol = 0
for _ in range(120):
    H1 = rand_lat2(8); H2 = rand_lat2(5)
    if not sub_of(H1, H2): continue
    Q = (random.randint(1, 6), random.randint(1, 6))
    Cs_, Ct_ = cells(mem(H1), Q), cells(mem(H2), Q)
    for d in (1, 2):
        for c in list(Cs_[d]):
            for t1 in (0, Fr(1, 3), Fr(1, 2), Fr(2, 3), 1):
                for t2 in (0, Fr(1, 3), Fr(1, 2), Fr(2, 3), 1):
                    u, gens = c
                    ts = (t1, t2)[:d]
                    pnt = tuple(Fr(u[i])+sum(t*gg[i] for t, gg in zip(ts, gens)) for i in range(2))
                    checked += 1
                    if not in_union(Ct_, pnt): viol += 1
rec("P5-P1 sampled corroboration (random nested planar lattices, sample points of all cells)", viol == 0, (checked, viol))
json.dump(R, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "EXACT_CHECKS_PAPER_I.json"), "w"), indent=1)
print(sum(v["pass"] for v in R.values()), "/", len(R), "PASS")
sys.exit(0 if all(v["pass"] for v in R.values()) else 1)

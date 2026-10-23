#!/usr/bin/env python3
"""Deterministic verification for 'Observable Equivalence and Relational Invariants'.
Exact rational arithmetic (fractions) for model H and the Legendre counterexample;
seeded floating-point checks (numpy) for the general theorems. Prints a report."""
import json, sys
from fractions import Fraction as Fr
import numpy as np

out = {}
ok_all = True
def check(name, cond, detail=""):
    global ok_all
    ok_all &= bool(cond)
    out[name] = {"pass": bool(cond), "detail": detail}
    print(("PASS " if cond else "FAIL ") + name + (("  [" + detail + "]") if detail else ""))

# ---------- Model H: R = R^3 (+) R^3, X=(u,v) ----------
rng = np.random.default_rng(20261021)
def Pi(X): return X[:3] + X[3:]            # s = u+v
def h(X):  return X[:3] - X[3:]            # h = u-v
def B(X, Y): return -0.5 * (Pi(X) @ Pi(Y) + h(X) @ h(Y))
def T(X): return np.concatenate([X[3:], X[:3]])

# identity B = -(u.u' + v.v')
errs = []
for _ in range(200):
    X, Y = rng.normal(size=6), rng.normal(size=6)
    errs.append(abs(B(X, Y) + (X[:3] @ Y[:3] + X[3:] @ Y[3:])))
check("H.B_equals_minus_uu_plus_vv", max(errs) < 1e-12, f"max err {max(errs):.2e}")
check("H.T_preserves_Pi", all(np.allclose(Pi(T(X)), Pi(X)) for X in rng.normal(size=(50, 6))))
check("H.T_reverses_h", all(np.allclose(h(T(X)), -h(X)) for X in rng.normal(size=(50, 6))))
check("H.joint_invariance_B(TX,TY)=B(X,Y)",
      max(abs(B(T(X), T(Y)) - B(X, Y)) for X, Y in rng.normal(size=(200, 2, 6))) < 1e-12)
sep = max(abs(B(T(X), Y) - B(X, Y)) for X, Y in rng.normal(size=(200, 2, 6)))
check("H.separate_invariance_FAILS", sep > 0.1, f"max |B(TX,Y)-B(X,Y)| = {sep:.3f}")
# kernel of Pi = {(u,-u)}; span{X-TX} equals it (dimension 3)
D = np.array([X - T(X) for X in rng.normal(size=(40, 6))])
rk = np.linalg.matrix_rank(D, tol=1e-9)
check("H.span{X-TX}_has_dim_3=dim_kerPi", rk == 3, f"rank {rk}")
check("H.span{X-TX}_inside_kerPi", max(np.abs(Pi(d)).max() for d in D) < 1e-12)
# witness: k=(u,-u), Y arbitrary => B(k,Y) = -1/2 h_k.h_Y != 0
k = np.concatenate([[1., 0, 0], [-1., 0, 0]]); Y = np.concatenate([[1., 0, 0], [-1., 0, 0]])
check("H.witness_Pi(k)=0_but_B(k,Y)=-2", np.allclose(Pi(k), 0) and abs(B(k, Y) + 2) < 1e-12, f"B={B(k,Y)}")
# obstruction ranks: rho_L = rank of X-> B(X,.) on ker Pi
K = np.array([np.concatenate([e, -e]) for e in np.eye(3)])
Gram = np.array([[B(k_, np.eye(6)[j]) for j in range(6)] for k_ in K])
check("H.obstruction_rank_rho_L=3", np.linalg.matrix_rank(Gram) == 3)

# ---------- Result I: factorization criterion (random finite-dim) ----------
def factors(Bm, P, tol=1e-9):
    """does Bm = P^T Bbar P for some Bbar ? test via kernel-in-radicals AND direct lstsq"""
    n = Bm.shape[0]
    Kk = np.linalg.svd(P)[2][P.shape[0]:].T if P.shape[0] < n else np.zeros((n, 0))
    krit = (Kk.size == 0) or (np.abs(Bm @ Kk).max() < tol and np.abs(Bm.T @ Kk).max() < tol)
    # direct: solve Bm = P^T Bbar P  (P full row rank)
    Pp = np.linalg.pinv(P)
    Bbar = Pp.T @ Bm @ Pp
    direct = np.abs(P.T @ Bbar @ P - Bm).max() < tol
    return krit, direct
agree = True; n_fact = n_nonfact = 0
for trial in range(300):
    n, m = int(rng.integers(3, 8)), int(rng.integers(1, 3)) + 1
    m = min(m, n - 1)
    P = rng.normal(size=(m, n))
    if trial % 2 == 0:   # construct a factoring B
        Bm = P.T @ rng.normal(size=(m, m)) @ P
    else:                # generic non-factoring B
        Bm = rng.normal(size=(n, n))
    a, b = factors(Bm, P)
    agree &= (a == b); n_fact += a; n_nonfact += (not a)
check("ResultI.criterion_matches_direct_factorization(300 random)", agree,
      f"{n_fact} factoring / {n_nonfact} non-factoring cases")
# one-sided counterexample: kernel in Rad_L but not Rad_R => NOT factoring
n = 4; P = np.array([[1., 0, 0, 0], [0, 1, 0, 0]]); k = np.array([0, 0, 1., 0])
Bm = np.zeros((n, n)); Bm[0, 0] = 1; Bm[0, 2] = 1  # B(e0,e2)=1: e2 in ker; B(e2,.)=0 so in Rad_L; B(.,e2)!=0 so not Rad_R
check("ResultI.one_sided_radical_insufficient",
      np.abs(Bm.T @ k).max() < 1e-12 and np.abs(Bm @ k).max() > 0.5 and not factors(Bm, P)[1])

# ---------- Result III: involution / coinvariant, random ----------
ok = True
for trial in range(200):
    d1, d2 = int(rng.integers(1, 4)), int(rng.integers(1, 4))
    n = d1 + d2
    Tm = np.diag([1.]*d1 + [-1.]*d2)                 # involution, V+ (+) V-
    Q, _ = np.linalg.qr(rng.normal(size=(n, n)))      # random basis change
    Ti = Q @ Tm @ Q.T
    Pm = (np.eye(n) + Ti) / 2                         # projection onto V+ (observable)
    # ker Pi = V-, span{X-TX} = V-
    Bm = rng.normal(size=(n, n))
    # separately invariant projection: B -> Pm^T B Pm  (the only separately invariant ones factor)
    Bs = Pm.T @ Bm @ Pm
    sepinv = np.abs(Ti.T @ Bs - Bs).max() < 1e-9 and np.abs(Bs @ Ti - Bs).max() < 1e-9
    # general joint-invariant: average
    Bj = (Bm + Ti.T @ Bm @ Ti) / 2
    jointinv = np.abs(Ti.T @ Bj @ Ti - Bj).max() < 1e-9
    # block diagonality: B(V+,V-)=0
    Vp = Q[:, :d1]; Vm = Q[:, d1:]
    blockdiag = np.abs(Vp.T @ Bj @ Vm).max() < 1e-9 and np.abs(Vm.T @ Bj @ Vp).max() < 1e-9
    # Result III: sep-inv => factors through Pi
    Pi_rows = Vp.T                                    # Pi: V -> V+ coordinates
    f_sep = factors(Bs, Pi_rows)[0]
    # joint-inv with nonzero V- block does NOT factor
    nz = np.abs(Vm.T @ Bj @ Vm).max() > 1e-6
    f_joint = factors(Bj, Pi_rows)[0]
    ok &= sepinv and jointinv and blockdiag and f_sep and ((not f_joint) == nz)
check("ResultIII+Prop(block-diagonal): 200 random involutions", ok)

# ---------- Legendre family on the free space over S^2 ----------
def P(l, x):
    from numpy.polynomial import legendre as L
    c = np.zeros(l + 1); c[l] = 1; return L.legval(x, c)
# exact rational P3
P3 = lambda x: (5 * x**3 - 3 * x) / 2
half, sq3h_sq = Fr(1, 2), Fr(3, 4)
# exact: B3(X,r(ex)) = -P3(1/2) + (1/2) P3(1) + (sqrt3/2) P3(0);  P3(0)=0 => sqrt3 term vanishes
B3_exact = -P3(half) + half * P3(Fr(1)) + 0
check("Legendre.P3(1/2)=-7/16", P3(half) == Fr(-7, 16), str(P3(half)))
check("Legendre.B3(X,r(ex))=15/16 exact", B3_exact == Fr(15, 16), str(B3_exact))
B1_exact = -half + half * 1 + 0
check("Legendre.B1(X,r(ex))=0 exact", B1_exact == 0)
check("Legendre.corr_60deg_B1=-1/2,B3=+7/16", -half == Fr(-1, 2) and -P3(half) == Fr(7, 16))
check("Legendre.P(++)_B1=1/8", (1 + Fr(-1, 2)) / 4 == Fr(1, 8))
check("Legendre.P(++)_B3=23/64=0.359375", (1 + Fr(7, 16)) / 4 == Fr(23, 64) and float(Fr(23, 64)) == 0.359375)
# numerical cross-check with unit vectors
n = np.array([.5, np.sqrt(3) / 2, 0]); ex = np.array([1., 0, 0]); ey = np.array([0, 1., 0])
Xv = [(1, n), (-.5, ex), (-np.sqrt(3) / 2, ey)]
for l in (1, 3):
    val = sum(-c * P(l, v @ ex) for c, v in Xv)
    print(f"   numeric B_{l}(X,r(ex)) = {val:.12f}")
check("Legendre.numeric_matches", abs(sum(-c*P(3, v@ex) for c, v in Xv) - 15/16) < 1e-12 and abs(sum(-c*P(1, v@ex) for c, v in Xv)) < 1e-12)
# oddness of P_l(l odd): sign reversal property
check("Legendre.odd_l_sign_reversal", all(abs(P(l, -x) + P(l, x)) < 1e-12 for l in (1, 3, 5, 7) for x in np.linspace(-1, 1, 11)))
# obstruction rank on N generic points of S^2
def sphere_points(N, seed):
    r = np.random.default_rng(seed); Z = r.normal(size=(N, 3)); return Z / np.linalg.norm(Z, axis=1, keepdims=True)
N = 120; pts = sphere_points(N, 7)
Gm = pts @ pts.T
Pm_ = pts.T                                          # 3 x N : Pi on coordinates r(a_i) -> a_i
Kb = np.linalg.svd(Pm_)[2][3:].T                     # N x (N-3) basis of ker Pi
ranks = {}
for l in range(1, 8):
    Bl = -P(l, np.clip(Gm, -1, 1))
    # sanity: PSD of -B
    ev = np.linalg.eigvalsh(-Bl); psd = ev.min() > -1e-9
    rho = np.linalg.matrix_rank(Kb.T @ Bl, tol=1e-8)
    ranks[l] = int(rho)
    print(f"   l={l}: rank(B_l|ker Pi)={rho}   (-B_l PSD: {psd})")
check("Legendre.B1_factors(rank 0)", ranks[1] == 0)
check("Legendre.B_l_l>=2_do_not_factor", all(ranks[l] > 0 for l in range(2, 8)))
check("Legendre.obstruction_rank=2l+1 (generic N=120)", all(ranks[l] == 2 * l + 1 for l in range(2, 8)), str(ranks))
out["obstruction_ranks_N120"] = ranks

# ---------- GCT v002 Theorem-3 symmetry conditions for c3(d) = -P3(cos d) ----------
ds = np.linspace(-np.pi, np.pi, 41)
c3 = lambda d: -P(3, np.cos(d))
cond = (abs(c3(0) + 1) < 1e-12 and all(abs(c3(-d) - c3(d)) < 1e-12 and abs(c3(d + np.pi) + c3(d)) < 1e-12 and abs(c3(d)) <= 1 + 1e-12 for d in ds))
check("GCTv002.Thm3_symmetry_conditions_hold_for_c3", cond)

# ---------- coinvariants: diagonal vs factorwise (Z2) ----------
# (V (x) V)_G has dim = dim(V+ (x) V+) + dim(V- (x) V-);  V_G (x) V_G has dim = (dim V+)^2.
d1, d2 = 3, 3
check("Coinvariant.dim_gap=dim(V-)^2 for model H", (d1*d1 + d2*d2) - d1*d1 == d2*d2 == 9)


# ---------- Fig.1 concrete numbers (model H) ----------
Xa = np.array([1., 0, 0, 0, 0, 0]); Xb = T(Xa)
check("Fig1.same_observable_s=(1,0,0)", np.allclose(Pi(Xa), [1, 0, 0]) and np.allclose(Pi(Xb), [1, 0, 0]))
check("Fig1.B(X,X)=-1,B(TX,X)=0,B(TX,TX)=-1",
      abs(B(Xa, Xa) + 1) < 1e-12 and abs(B(Xb, Xa)) < 1e-12 and abs(B(Xb, Xb) + 1) < 1e-12)
# 2-D minimal example of Sec.1
Pi2 = lambda X: X[0]; T2 = lambda X: np.array([X[0], -X[1]]); B2 = lambda X, Y: X @ Y
X1, X2, Y1 = np.array([1., 1]), np.array([1., -1]), np.array([0., 1])
check("Minimal2D.values", Pi2(X1) == Pi2(X2) and B2(X1, Y1) == 1 and B2(X2, Y1) == -1 and B2(X1, X1) == B2(X2, X2) == 2)
# one-sided 2-D example B(X,Y)=x*y'
B3 = np.array([[0., 1], [0, 0]])  # B(X,Y)=X^T B3 Y = x*y'
Kk2 = np.array([[0.], [1.]])
check("OneSided2D.K_in_RadL_not_RadR", np.abs(Kk2.T @ B3).max() == 0 and np.abs(B3 @ Kk2).max() > 0)

# ---------- ell=5 exact ----------
P5 = lambda x: (63 * x**5 - 70 * x**3 + 15 * x) / 8
check("Legendre.l=5_exact", -P5(half) == Fr(-23, 256) and -P5(half) + half * P5(Fr(1)) == Fr(105, 256) and (1 + (-P5(half))) / 4 == Fr(233, 1024),
      f"C={-P5(half)}, B5(X,ex)={-P5(half)+half}, P(++)={(1-P5(half))/4}")

# ---------- relational deficit: formula and minimal completion (random) ----------
def deficit_formula(Bm, K):
    S = np.vstack([Bm @ K, Bm.T @ K]); return np.linalg.matrix_rank(S, tol=1e-9)
okd = True; cnt = 0
for trial in range(300):
    n = int(rng.integers(4, 9)); m = int(rng.integers(1, 3)) + 1
    Pm = rng.normal(size=(m, n)); Kk = np.linalg.svd(Pm)[2][m:].T
    Bm = rng.normal(size=(n, n))
    mode = trial % 3
    if mode == 1:   # make part of K radical on both sides
        c = Kk[:, 0]; Bm = Bm - np.outer(Bm @ c, c) / (c @ c) - np.outer(c, c @ Bm) / (c @ c) + (c @ Bm @ c) * np.outer(c, c) / (c @ c)**2
    if mode == 2:   # symmetric
        Bm = (Bm + Bm.T) / 2
    d = deficit_formula(Bm, Kk)
    rhoL = np.linalg.matrix_rank(Kk.T @ Bm, tol=1e-9); rhoR = np.linalg.matrix_rank(Bm @ Kk, tol=1e-9)
    okd &= (max(rhoL, rhoR) <= d <= rhoL + rhoR)
    if mode == 2: okd &= (d == rhoL == rhoR)
    # minimal completion Psi with delta rows
    S = np.vstack([Bm @ Kk, Bm.T @ Kk]); U, sv, Vt = np.linalg.svd(S, full_matrices=False)
    Q = Vt[:d]                                  # d x dim K
    Psi = Q @ np.linalg.pinv(Kk)                # d x n
    Pfull = np.vstack([Pm, Psi])
    okd &= factors(Bm, Pfull)[1]
    if d > 0 and Psi.shape[0] > 1:              # delta-1 rows must fail
        okd &= not factors(Bm, np.vstack([Pm, Psi[:-1]]))[1]
    cnt += 1
check("Deficit.bounds+formula+minimal_completion (300 random)", okd, f"{cnt} cases")

# ---------- permutation example: joint vs separate invariant forms on R^n ----------
n = 5
def invariant_dim(joint):
    rows = []
    for i in range(n - 1):
        Pm = np.eye(n); Pm[[i, i + 1]] = Pm[[i + 1, i]]
        # constraint on vec(B): joint: P^T B P = B ; separate: P^T B = B and B P = B
        I = np.eye(n)
        if joint: rows.append(np.kron(Pm.T, Pm.T) - np.eye(n * n))   # vec(P^T B P)=(P^T (x) P^T)vec(B) for row-major
        else:
            rows.append(np.kron(Pm.T, I) - np.eye(n * n)); rows.append(np.kron(I, Pm.T) - np.eye(n * n))
    A = np.vstack(rows); return n * n - np.linalg.matrix_rank(A, tol=1e-9)
check("Perm.joint_invariant_forms_dim=2,separate=1", invariant_dim(True) == 2 and invariant_dim(False) == 1,
      f"joint {invariant_dim(True)}, separate {invariant_dim(False)}")
Pm = np.ones((1, n)); Kk = np.linalg.svd(Pm)[2][1:].T
Bperm = np.eye(n) + 0.3 * np.ones((n, n))
check("Perm.deficit=n-1=4", deficit_formula(Bperm, Kk) == n - 1)
# span of {X - T_i X} = sum-zero hyperplane (H2)
D = []
for i in range(n - 1):
    Pt = np.eye(n); Pt[[i, i + 1]] = Pt[[i + 1, i]]
    D += [(np.eye(n) - Pt)[:, j] for j in range(n)]
check("Perm.H2_span{X-T_iX}=ker(sum) (dim 4)", np.linalg.matrix_rank(np.array(D), tol=1e-9) == n - 1)

# ---------- Closure illustration: ideal Helmholtz projector per Fourier mode ----------
kv = np.array([1., 2.]); Pk = np.eye(2) - np.outer(kv, kv) / (kv @ kv); Rk = 2 * Pk - np.eye(2)
Bk = np.eye(2)
okc = np.allclose(Pk @ Pk, Pk) and np.allclose(Pk @ kv, 0) and np.allclose(Rk @ Rk, np.eye(2)) and np.allclose(Pk @ Rk, Pk)
okc &= np.allclose(Rk.T @ Bk @ Rk, Bk) and not np.allclose(Rk.T @ Bk, Bk)
check("Closure.ideal_Helmholtz_per_mode: P idem, R involution, joint-inv, not separate", okc)
check("Closure.deficit=1_per_mode", deficit_formula(Bk, kv.reshape(2, 1)) == 1)


# ---------- four-route table (Example 5.x): exact arithmetic in Q(sqrt3) ----------
class QS:
    """a + b*sqrt(3), a,b rational (Fractions)."""
    def __init__(s, a=0, b=0): s.a, s.b = Fr(a), Fr(b)
    def __add__(s, o): o = o if isinstance(o, QS) else QS(o); return QS(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __neg__(s): return QS(-s.a, -s.b)
    def __sub__(s, o): return s + (-(o if isinstance(o, QS) else QS(o)))
    def __mul__(s, o): o = o if isinstance(o, QS) else QS(o); return QS(s.a * o.a + 3 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__
    def __eq__(s, o): o = o if isinstance(o, QS) else QS(o); return s.a == o.a and s.b == o.b
    def __repr__(s): return f"({s.a}+{s.b}*sqrt3)"
Z, O1, H2, S3 = QS(0), QS(1), QS(Fr(1, 2)), QS(0, Fr(1, 2))      # 0, 1, 1/2, sqrt3/2
dirs4 = [[O1, Z, Z], [Z, O1, Z], [Z, Z, O1], [H2, S3, Z]]
dot = lambda u, v: u[0] * v[0] + u[1] * v[1] + u[2] * v[2]
P3q = lambda t: (5 * t * t * t - 3 * t) * Fr(1, 2)
G1 = [[-dot(dirs4[i], dirs4[j]) for j in range(4)] for i in range(4)]
G3 = [[-P3q(dot(dirs4[i], dirs4[j])) for j in range(4)] for i in range(4)]
kq = [QS(-Fr(1, 2)), QS(0, -Fr(1, 2)), Z, O1]                    # (-1/2, -sqrt3/2, 0, 1)
matvec = lambda G, v: [sum((G[i][j] * v[j] for j in range(4)), QS(0)) for i in range(4)]
Pik = [sum((dirs4[j][c] * kq[j] for j in range(4)), QS(0)) for c in range(3)]
check("FourRoute.k_in_kerPi", all(p == 0 for p in Pik))
check("FourRoute.G1*k=0", all(v == 0 for v in matvec(G1, kq)))
g3k = matvec(G3, kq)
exp3 = [QS(Fr(15, 16)), QS(0, Fr(5, 16)), QS(0), QS(-Fr(15, 16))]
check("FourRoute.G3*k=(15/16,5sqrt3/16,0,-15/16)", all(g3k[i] == exp3[i] for i in range(4)), str(g3k))
check("FourRoute.G3_entries", G3[0][3] == QS(Fr(7, 16)) and G3[1][3] == QS(0, -Fr(3, 16)) and G3[0][1] == 0 and G3[2][3] == 0
      and all(G3[i][i] == QS(-1) for i in range(4)))

G3f = np.array([[float(G3[i][j].a) + float(G3[i][j].b) * np.sqrt(3) for j in range(4)] for i in range(4)])
G1f = np.array([[float(G1[i][j].a) + float(G1[i][j].b) * np.sqrt(3) for j in range(4)] for i in range(4)])
kf = np.array([float(v.a) + float(v.b) * np.sqrt(3) for v in kq]).reshape(4, 1)
check("FourRoute.deficit_B3=1,B1=0", deficit_formula(G3f, kf) == 1 and deficit_formula(G1f, kf) == 0)

# ---------- self-interaction descends iff symmetric B descends ----------
okq = True
for trial in range(100):
    n = int(rng.integers(4, 8)); m = int(rng.integers(1, 3)) + 1
    Pm = rng.normal(size=(m, n)); Kk = np.linalg.svd(Pm)[2][m:].T
    if trial % 2 == 0: Bm = Pm.T @ rng.normal(size=(m, m)) @ Pm; Bm = (Bm + Bm.T) / 2   # factoring, symmetric
    else:              Bm = rng.normal(size=(n, n)); Bm = (Bm + Bm.T) / 2
    Q = lambda z: z @ Bm @ z
    Xs = rng.normal(size=(8, n)); ks = (Kk @ rng.normal(size=(Kk.shape[1], 8))).T
    qdesc = all(abs(Q(xv + kv) - Q(xv)) < 1e-9 for xv, kv in zip(Xs, ks))
    okq &= (qdesc == factors(Bm, Pm)[1])
check("SelfInteraction.Q_descends_iff_B_descends (100 random symmetric)", okq)

# ---------- representatives: induced pairing on O depends on the section unless K subset Rad ----------
okr = True
for trial in range(100):
    H = rng.normal(size=(3, 3))
    # section sigma_H(s) = (s, H s) in (s,h) coordinates of model H; B in (s,h)-coords = -1/2 (s.s' + h.h')
    BsH = -0.5 * (np.eye(3) + H.T @ H)
    X = np.concatenate([[1., 2, 3], H @ np.array([1., 2, 3])]); Y = np.concatenate([[0., 1, -1], H @ np.array([0., 1, -1])])
    okr &= abs(-0.5 * (X[:3] @ Y[:3] + X[3:] @ Y[3:]) - (np.array([1., 2, 3]) @ BsH @ np.array([0., 1, -1]))) < 1e-10
check("Sections.model_H_induced_pairing=-1/2(I+H^T H)", okr)

# ---------- Section 8: generative response profiles ----------
def nullspace(M, tol=1e-9):
    if M.shape[0] == 0: return np.eye(M.shape[1])
    _, sv, vt = np.linalg.svd(M); r = int((sv > tol).sum()); return vt[r:].T
def largest_invariant_in(W, F):
    cur = W
    for _ in range(F.shape[0] + 2):
        if cur.shape[1] == 0: return cur
        Pperp = np.eye(F.shape[0]) - cur @ cur.T          # cur has orthonormal columns
        Nn = nullspace(Pperp @ F @ cur)
        new = cur @ Nn if Nn.shape[1] else np.zeros((F.shape[0], 0))
        if new.shape[1] == cur.shape[1]: return new
        cur = new
    return cur
def same_subspace(A, Bm):
    if A.shape[1] != Bm.shape[1]: return False
    if A.shape[1] == 0: return True
    PA = A @ np.linalg.pinv(A); PB = Bm @ np.linalg.pinv(Bm); return np.allclose(PA, PB, atol=1e-7)
okS = okC = True; nS = 0
for trial in range(300):
    n = int(rng.integers(4, 8)); m = int(rng.integers(1, 3))
    Pm = rng.normal(size=(m, n)); Kb = nullspace(Pm)
    mode = trial % 3
    Bm = rng.normal(size=(n, n))
    if mode == 1: Bm = Pm.T @ rng.normal(size=(m, n))                      # K inside Rad_L (left descends)
    F = rng.normal(size=(n, n)) * 0.7 if trial % 2 == 0 else np.eye(n) + Kb @ rng.normal(size=(Kb.shape[1], n))  # general / observable-preserving
    stack = np.vstack([np.vstack([Pm @ np.linalg.matrix_power(F, k), Bm.T @ np.linalg.matrix_power(F, k)]) for k in range(n)])
    SG = nullspace(stack)                                                  # profile congruence subspace (direct)
    W0 = nullspace(np.vstack([Pm, Bm.T]))                                  # K cap Rad_L
    okS &= same_subspace(SG, largest_invariant_in(W0, F))
    # completeness: K subset S_G  <=>  K invariant under F and K subset Rad_L
    KinSG = np.allclose(SG @ np.linalg.pinv(SG) @ Kb, Kb, atol=1e-7) if SG.shape[1] else (Kb.shape[1] == 0)
    FKinK = np.allclose(Kb @ np.linalg.pinv(Kb) @ F @ Kb, F @ Kb, atol=1e-7)
    KinRadL = np.abs(Bm.T @ Kb).max() < 1e-9
    okC &= (KinSG == (FKinK and KinRadL))
    if trial % 2 == 1: okC &= (FKinK and (KinSG == KinRadL))               # observable-preserving => K invariant
    nS += 1
check("Profile.congruence_subspace=largest_F-invariant_subspace_of_K_cap_RadL (300 random)", okS, f"{nS} cases")
check("Profile.completeness: ~Pi => ~G iff K F-invariant and K in Rad_L (300 random)", okC)

# hidden-sector model vs first-order model under T
PiH = np.hstack([np.eye(3), np.eye(3)]); TH = np.block([[np.zeros((3, 3)), np.eye(3)], [np.eye(3), np.zeros((3, 3))]])
B_H = -np.eye(6); B_1 = -PiH.T @ PiH
def SG_dim(Pm, Bm, F):
    n = F.shape[0]; st = np.vstack([np.vstack([Pm @ np.linalg.matrix_power(F, k), Bm.T @ np.linalg.matrix_power(F, k)]) for k in range(n)])
    return nullspace(st).shape[1]
check("Profile.hidden-sector: S_G=0 (route fully recoverable from profile); first-order: S_G=K (dim 3)",
      SG_dim(PiH, B_H, TH) == 0 and SG_dim(PiH, B_1, TH) == 3)

# identifiability: probes needed = rho_L ; compatible class dimension after m probes
okI = True
for trial in range(200):
    n = int(rng.integers(4, 9)); m = int(rng.integers(1, 3)); Pm = rng.normal(size=(m, n)); Kb = nullspace(Pm); k = Kb.shape[1]
    Bm = rng.normal(size=(n, n))
    if trial % 2: Bm = Bm - (Kb[:, :1] @ (Kb[:, :1].T @ Bm))               # make one K-direction left-radical
    rhoL = np.linalg.matrix_rank(Kb.T @ Bm, tol=1e-9)
    def dimKJ(mp):
        if mp == 0: return k
        Eta = rng.normal(size=(n, mp)); R = (Kb.T @ Bm @ Eta).T            # rows: probe functionals restricted to K
        return k - np.linalg.matrix_rank(R, tol=1e-9)
    okI &= dimKJ(rhoL) == k - rhoL and (rhoL == 0 or dimKJ(rhoL - 1) > k - rhoL)
    # full protocol residual = dim(K cap Rad_L)
    okI &= (k - rhoL) == nullspace(np.vstack([Pm, Bm.T])).shape[1]
check("Identifiability: rho_L generic probes resolve the fibre up to K cap Rad_L; rho_L-1 do not (200 random)", okI)

# admissible fibres: K_A and observable adequacy on A
okA = True
for trial in range(200):
    n = int(rng.integers(5, 9)); m = 2; Pm = rng.normal(size=(m, n)); Kb = nullspace(Pm)
    u = Kb[:, 0]
    base = rng.normal(size=(4, n)); A = []
    for x0 in base:
        A += [x0, x0 + rng.normal() * u, x0 + rng.normal() * u]           # admissible routes: fibres only along u
    A = np.array(A)
    D = [A[i] - A[j] for i in range(len(A)) for j in range(len(A)) if i != j and np.abs(Pm @ (A[i] - A[j])).max() < 1e-9]
    KA = np.array(D)
    Bm = rng.normal(size=(n, n))
    if trial % 2 == 0: Bm = Bm - np.outer(u, u @ Bm)                       # u in Rad_L, other K directions not
    adequate = all(abs((A[i] - A[j]) @ Bm @ eta) < 1e-9 for i in range(len(A)) for j in range(len(A))
                   if np.abs(Pm @ (A[i] - A[j])).max() < 1e-9 for eta in np.eye(n))
    KA_in_RadL = np.abs(KA @ Bm).max() < 1e-9
    okA &= (adequate == KA_in_RadL) and (np.linalg.matrix_rank(KA, tol=1e-9) <= 1) and (trial % 2 == 1 or KA_in_RadL)
    okA &= (np.abs(Kb.T @ Bm).max() > 1e-9)                                # but K itself is NOT inside Rad_L
check("AdmissibleFibres: adequacy on A iff K_A in Rad_L, with K_A a proper subspace of K (200 random)", okA)


# ---- Section 8 (continued): worked examples and gauge invariance ----
# (a) the (u,v) witness: X=(e_x,0), X'=(0,e_x), Y=(e_x,0) with B=-(u.a+v.b)
ex = np.array([1., 0, 0]); z3 = np.zeros(3)
Xa, Xb, Yc = np.concatenate([ex, z3]), np.concatenate([z3, ex]), np.concatenate([ex, z3])
Bm_uv = -np.eye(6)
check("Witness.same_Pi_different_B: Pi(X)=Pi(X')=e_x, B(X,Y)=-1, B(X',Y)=0",
      np.allclose(PiH @ Xa, PiH @ Xb) and np.isclose(Xa @ Bm_uv @ Yc, -1) and np.isclose(Xb @ Bm_uv @ Yc, 0))
# (b) two-dimensional example: dynamics reveals a distinction invisible to Pi and B
P2 = np.array([[1., 0.]]); B2 = np.array([[1., 0.], [0., 0.]]); F1 = np.eye(2); F2 = np.array([[1., 1.], [0., 1.]])
def prof(Pm, Bm, F, X, N=4):
    return [np.concatenate([Pm @ np.linalg.matrix_power(F, k) @ X, (np.linalg.matrix_power(F, k) @ X) @ Bm]) for k in range(N)]
Z = np.array([0., 1.])                                                      # Z in K = ker Pi, and in Rad_L(B)
d_zero = np.abs(B2.T @ Z).max() < 1e-12 and np.abs(P2 @ Z).max() < 1e-12
n1 = max(np.abs(p).max() for p in prof(P2, B2, F1, Z)); n2 = [np.abs(p).max() for p in prof(P2, B2, F2, Z)]
check("Example.dynamics_separates: Z in K cap Rad_L; M1 (F=id) cannot separate Z from 0, M2 (F=shear) does at n>=1",
      d_zero and n1 < 1e-12 and n2[0] < 1e-12 and all(v > 1e-9 for v in n2[1:]) and SG_dim(P2, B2, F1) == 1 and SG_dim(P2, B2, F2) == 0)
# (c) gauge invariance under g with Pi g = Pi
okG = True
for trial in range(200):
    n = int(rng.integers(4, 8)); m = int(rng.integers(1, 3)); Pm = rng.normal(size=(m, n)); Kb = nullspace(Pm)
    Bm = rng.normal(size=(n, n)); Bm = Bm - Kb[:, :1] @ (Kb[:, :1].T @ Bm) if trial % 2 else Bm
    F = rng.normal(size=(n, n)) * 0.7
    g = np.eye(n) + Kb @ rng.normal(size=(Kb.shape[1], n)) * 0.3
    if abs(np.linalg.det(g)) < 1e-3: continue
    gi = np.linalg.inv(g); B_ = gi.T @ Bm @ gi; F_ = g @ F @ gi
    okG &= np.allclose(Pm @ g, Pm)
    X = rng.normal(size=n); eta = rng.normal(size=n)
    for k in range(4):
        Fk = np.linalg.matrix_power(F, k); F_k = np.linalg.matrix_power(F_, k)
        okG &= np.allclose(Pm @ F_k @ (g @ X), Pm @ Fk @ X) and np.isclose((F_k @ (g @ X)) @ B_ @ (g @ eta), (Fk @ X) @ Bm @ eta)
    def dl(Pm, Bm): 
        Kc = nullspace(Pm); return Kc.shape[1] - nullspace(np.vstack([Pm, Bm.T])).shape[1]
    okG &= SG_dim(Pm, Bm, F) == SG_dim(Pm, B_, F_) and dl(Pm, Bm) == dl(Pm, B_)
    okG &= np.linalg.matrix_rank(np.vstack([Kb.T @ Bm, Kb.T @ Bm.T]), tol=1e-9) == np.linalg.matrix_rank(np.vstack([Kb.T @ B_, Kb.T @ B_.T]), tol=1e-9)
check("Gauge: g with Pi g = Pi relabels routes but preserves every protocol output; dim S_G, rho_L, delta invariant (200 random)", okG)
# (d) trivial realisation: V=O, Pi=id gives K=0, delta=0, S_G=0
check("Weak_claim.trivial_realisation: Pi=id has K=0, delta=0, S_G=0 for any B,F", all(
    SG_dim(np.eye(k), rng.normal(size=(k, k)), rng.normal(size=(k, k))) == 0 for k in (2, 3, 5)))


# ---- v2 review regressions ----
# (A) Prop 4.9(c) needs O != 0: V=R, O=0, B=xy has a unique section yet does not descend
K_A = np.array([[1.]]); B_A = np.array([[1.]])
check("Regression.Prop4.9c: O=0 counterexample (unique section, B not descending, K not in Rad)",
      np.abs(B_A @ K_A).max() > 0 and K_A.shape[1] == 1)
# (B) fixed-label vs relabelled outputs under g=(x,2y)
Bq = np.array([[0., 0.], [0., 1.]]); g2 = np.diag([1., 2.]); gi2 = np.linalg.inv(g2); Bg = gi2.T @ Bq @ gi2; ey = np.array([0., 1.])
check("Regression.Prop8.8: fixed-label output 1 vs 1/4; relabelled (g e_y, g e_y) output 1",
      np.isclose(ey @ Bq @ ey, 1) and np.isclose(ey @ Bg @ ey, 0.25) and np.isclose((g2 @ ey) @ Bg @ (g2 @ ey), 1))
# (C) gauge fixing named routes/probes leaves all fixed-label outputs unchanged
okF = True
for trial in range(200):
    n = int(rng.integers(4, 8)); m = int(rng.integers(1, 3)); Pm = rng.normal(size=(m, n)); Kb = nullspace(Pm)
    Bm = rng.normal(size=(n, n)); F = rng.normal(size=(n, n)) * 0.7
    X = rng.normal(size=n); eta = rng.normal(size=n)
    Q, _ = np.linalg.qr(np.stack([X, eta], 1)); proj = np.eye(n) - Q @ Q.T
    g = np.eye(n) + Kb @ rng.normal(size=(Kb.shape[1], n)) @ proj * 0.3
    if abs(np.linalg.det(g)) < 1e-3: continue
    gi = np.linalg.inv(g); B_ = gi.T @ Bm @ gi; F_ = g @ F @ gi
    okF &= np.allclose(g @ X, X) and np.allclose(g @ eta, eta)
    for k in range(4):
        okF &= np.allclose(Pm @ np.linalg.matrix_power(F_, k) @ X, Pm @ np.linalg.matrix_power(F, k) @ X)
        okF &= np.isclose((np.linalg.matrix_power(F_, k) @ X) @ B_ @ eta, (np.linalg.matrix_power(F, k) @ X) @ Bm @ eta)
check("Regression.Prop8.8c: g fixing named routes and probes leaves fixed-label outputs unchanged (200 random)", okF)


# ---- Section 10.1: canonical nest operation M (x) N = MN + M/N + 2M ----
nest = lambda M, N: Fr(M * N) + Fr(M, N) + 2 * M
check("Canonical.nest_identity: M(x)N = M(N+1)^2/N (59x59 exact)", all(nest(M, N) == Fr(M * (N + 1) ** 2, N) for M in range(1, 60) for N in range(1, 60)))
fib72 = [(M, N) for N in range(1, 71) for M in range(1, 73) if nest(M, N) == 72]
check("Canonical.fibre_of_72: exactly (18,1),(16,2),(10,5), all anchors M=kN with k(N+1)^2=72",
      sorted(fib72) == [(10, 5), (16, 2), (18, 1)] and all(M % N == 0 and (M // N) * (N + 1) ** 2 == 72 for M, N in fib72)
      and all(Fr(72 * N, (N + 1) ** 2) < 1 for N in range(70, 400)))
fibs = {}
for N in range(1, 41):
    for M in range(1, 201): fibs.setdefault(nest(M, N), []).append((M, N))
check("Canonical.non_injective: 235 values in (M<=200,N<=40) have >=2 routes", sum(1 for v in fibs.values() if len(v) > 1) == 235)

json.dump(out, open("verify_ri_report.json", "w"), indent=1)
print("\nALL PASS" if ok_all else "\nSOME FAILED"); sys.exit(0 if ok_all else 1)

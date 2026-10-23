#!/usr/bin/env python3
"""RGG-1: first candidate relational generative grammar on UNNS nest anchor routes.
Anchor route r=(k,d), d>=2, k>=1  <->  occurrence (M,N)=(k(d-1), d-1), value k*d^2.
Candidates: J_mul (componentwise product), J_join (componentwise lcm), J_blind (value-only baseline).
Exact integer arithmetic; deterministic. Prints PASS/FAIL, exit 0 iff all pass."""
import json, sys, itertools
from math import gcd
from fractions import Fraction as Fr
import numpy as np

out, ok_all = {}, True
def check(name, cond, detail=""):
    global ok_all
    ok_all &= bool(cond); out[name] = {"pass": bool(cond), "detail": detail}
    print(("PASS " if cond else "FAIL ") + name + (f" [{detail}]" if detail else ""))

lcm = lambda a, b: a * b // gcd(a, b)
val = lambda r: r[0] * r[1] ** 2
occ = lambda r: (r[0] * (r[1] - 1), r[1] - 1)
mul = lambda r, s: (r[0] * s[0], r[1] * s[1])
join = lambda r, s: (lcm(r[0], s[0]), lcm(r[1], s[1]))
def fibre(m):                       # all anchor routes of value m  (|fibre| = R(m))
    d, res = 2, []
    while d * d <= m:
        if m % (d * d) == 0: res.append((m // (d * d), d))
        d += 1
    return res
def Rm(m): return len(fibre(m))
nest = lambda M, N: Fr(M * (N + 1) ** 2, N)

G = [(k, d) for k in range(1, 31) for d in range(2, 31)]
G_small = [(k, d) for k in range(1, 13) for d in range(2, 13)]

# 0. coordinates: anchor occurrence value equals nest value
check("0.anchor_coordinates", all(nest(*occ(r)) == val(r) for r in G))

# 1. J_mul: closure + value is a monoid homomorphism (value-equivalence is a congruence)
check("1.mul_closed_and_value_homomorphism",
      all(val(mul(r, s)) == val(r) * val(s) and mul(r, s)[1] >= 2 for r in G_small for s in G_small))
bad = 0; tot = 0
for m in range(1, 4001):
    F = fibre(m)
    for r, r2 in itertools.combinations(F, 2):
        for s in G_small[:60]:
            tot += 1; bad += val(mul(r, s)) != val(mul(r2, s))
check("1b.mul_value_congruence_no_leak", bad == 0 and tot > 0, f"{tot} same-value route pairs x probes")

# 2. faithfulness (cancellative): same value, different route => different continuation with every probe
faith = True; npairs = 0
for m in range(1, 4001):
    for r, r2 in itertools.combinations(fibre(m), 2):
        npairs += 1
        faith &= all(mul(r, s) != mul(r2, s) for s in G_small[:60])
check("2.mul_faithful_cancellative", faith and npairs > 0, f"{npairs} same-value pairs (rule-imposed, not discovered)")

# 3. J_mul refines the route-blind baseline J_blind(r,s)={t: val t = val r * val s}
ref = True; strict = 0; allp = 0
for r in G_small:
    for s in G_small:
        B = fibre(val(r) * val(s)); allp += 1
        ref &= mul(r, s) in B; strict += len(B) > 1
check("3.J_mul_subset_of_J_blind", ref)
check("3b.blind_ambiguity_frequency", strict > 0, f"|J_blind|>1 for {strict}/{allp} pairs of the 11x11 grid")

# 4. refinement T_q(k,d)=(k/q^2, d q): value-preserving; covariance vs invariance
def T(q, r):
    k, d = r; assert k % (q * q) == 0; return (k // (q * q), d * q)
cov = inv_fail = True; cnt = 0
for r in G:
    for q in (2, 3):
        if r[0] % (q * q): continue
        for s in G_small:
            cnt += 1
            cov &= val(T(q, r)) == val(r) and mul(T(q, r), s) == T(q, mul(r, s))
            if r[0] % (q ** 4) == 0 or s[0] % (q * q) == 0:
                pass
            inv_fail &= (mul(T(q, r), s) != mul(r, s)) and val(mul(T(q, r), s)) == val(mul(r, s))
check("4.refinement_covariance_not_invariance", cov and inv_fail, f"{cnt} cases: T_q(r)s=T_q(rs); route changes, value does not")
joint = all(mul(T(2, r), T(2, s)) == T(4, mul(r, s)) for r in G if r[0] % 16 == 0 for s in G_small if s[0] % 4 == 0)
check("4b.joint_refinement_is_T_{q^2}", joint)

# 5. exponent-lattice linearisation of J_mul: V=Z^{2P}, Pi=(x,y)->x+2y, refinements = translations by K
P = 4
Pi = np.hstack([np.eye(P), 2 * np.eye(P)])
Kb = np.array([np.concatenate([-2 * e, e]) for e in np.eye(P)]).T       # kappa_p=(-2e_p, e_p)
check("5.refinement_translations_span_kerPi", np.abs(Pi @ Kb).max() == 0 and np.linalg.matrix_rank(Kb) == P == 2 * P - np.linalg.matrix_rank(Pi))
def delta(Bm, Km): return np.linalg.matrix_rank(np.vstack([Bm @ Km, Bm.T @ Km]))
rng = np.random.default_rng(20261021)
Z = np.zeros((P, P)); I = np.eye(P)
# polarisation B_Q(r,s)=Q(rs)-Q(r)-Q(s) of quadratic Q on exponent vectors (route product = vector addition)
def polar_gram(Qm):  # Q(z)=z^T Qm z  -> B=Qm+Qm^T
    return Qm + Qm.T
Q_y = np.block([[Z, Z], [Z, I]]); Q_x = np.block([[I, Z], [Z, Z]]); Q_v = Pi.T @ Pi
okp = True
for Qm in (Q_y, Q_x, Q_v):
    a, b = rng.integers(0, 6, 2 * P), rng.integers(0, 6, 2 * P)
    okp &= (a + b) @ Qm @ (a + b) - a @ Qm @ a - b @ Qm @ b == a @ polar_gram(Qm) @ b
check("5b.polarisation_is_bilinear_on_exponent_lattice", okp)
dy, dx, dv = delta(polar_gram(Q_y), Kb), delta(polar_gram(Q_x), Kb), delta(polar_gram(Q_v), Kb)
check("5c.deficits_Q_y=P,Q_x=P,Q_value=0", (dy, dx, dv) == (P, P, 0), f"delta(|y|^2)={dy}, delta(|x|^2)={dx}, delta(|Pi|^2)={dv}")

# 6. adversarial alternative J_join: is value-equivalence a congruence?
leak = tot = 0; ex = None
for m in range(1, 4001):
    for r, r2 in itertools.combinations(fibre(m), 2):
        for s in G_small[:60]:
            tot += 1
            if val(join(r, s)) != val(join(r2, s)):
                leak += 1; ex = ex or (r, r2, s, val(join(r, s)), val(join(r2, s)))
check("6.join_leaks_value_equivalence", leak > 0, f"{leak}/{tot} violating triples; first: r={ex[0]}, r'={ex[1]}, s={ex[2]} -> {ex[3]} vs {ex[4]}")
check("6b.join_is_not_exponent_additive", val(join((2, 3), (2, 3))) != val(mul((2, 3), (2, 3))) and join((2, 3), (2, 3)) == (2, 3))

# 7. field (non-anchor) occurrences: does a value-multiplicative, d-multiplicative continuation exist?
def comp_exists(a, b):
    (M, N), (M2, N2) = a, b; d, d2 = N + 1, N2 + 1
    num = M * M2 * (d * d2 - 1); den = N * N2
    return num % den == 0
anch = lambda a: a[0] % a[1] == 0
occs = [(M, N) for M in range(1, 41) for N in range(1, 41)]
field_pairs = [(a, b) for a in occs[::7] for b in occs[::11] if not (anch(a) and anch(b))]
frac = sum(comp_exists(a, b) for a, b in field_pairs) / len(field_pairs)
anch_ok = all(comp_exists(a, b) for a in occs if anch(a) for b in occs[::13] if anch(b))
check("7.anchor_pairs_always_compose", anch_ok)
check("7b.field_pairs_often_have_no_composition", 0 < frac < 1, f"integer composed occurrence exists for {frac:.3f} of {len(field_pairs)} pairs with a field member (data, not a theorem)")

json.dump(out, open("rgg1_report.json", "w"), indent=1)
print("\nALL PASS" if ok_all else "\nSOME FAILED"); sys.exit(0 if ok_all else 1)

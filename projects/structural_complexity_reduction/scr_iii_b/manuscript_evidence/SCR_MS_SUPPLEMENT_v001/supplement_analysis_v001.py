#!/usr/bin/env python3
"""SCR manuscript supplement (v004): (A) single-flip / boundary-vs-bulk analysis from the certified 4x4 ground witness,
(B) inputs for the Hamiltonian-perturbation bound. READ-ONLY on all frozen files. No optimization, no enumeration of 2^40.

Uses: GAP4_v010/output/real_4x4.txt (frozen couplings and vertex table) and GAP4_v010/physical_energy_v005.py (frozen geometry).
Couplings are used as exact dyadic rationals (float -> Fraction), exactly as in the Lean encoding (kShift = 70).
Usage: python3 supplement_analysis_v001.py <path to scr_iii_b>
"""
import sys, os, json, math, hashlib
from fractions import Fraction
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
G = os.path.join(ROOT, "GAP4_v010"); sys.path.insert(0, G)
import physical_energy_v005 as P
n = 40
raw = open(os.path.join(G, "output", "real_4x4.txt"), "rb").read()
t = raw.decode().split()
assert int(t[0]) == 40 and int(t[1]) == 16
toks = t[2:2 + 780]; vt = t[2 + 780:]
K = [[Fraction(0)] * n for _ in range(n)]
c = 0
for i in range(n):
    for j in range(i + 1, n):
        K[i][j] = K[j][i] = Fraction(float(toks[c])); c += 1
verts = [(int(vt[2 * v]), int(vt[2 * v + 1])) for v in range(16)]
GROUND, TRUE_EXCL, FROZEN_EXCL = 711243241830, 711243241766, 161487427942
sg = lambda idv: [1 if idv >> i & 1 else -1 for i in range(n)]
def H(idv):
    s = sg(idv); return sum(K[i][j] * s[i] * s[j] for i in range(n) for j in range(i + 1, n))
def in_grammar(idv):
    return all(bin(~(idv ^ p) & m).count("1") == 2 for m, p in verts)
E0 = H(GROUND); assert in_grammar(GROUND)
A_J = 1.0095767595046513e-18; KB = 1.380649e-23; kBT = KB * 792.0
to_kBT = lambda x: float(x) * A_J / kBT          # x in units of A
two70 = 2 ** 70
isl = P.source_geometry(4)
nv_of = [sum(1 for m, _ in verts if m >> i & 1) for i in range(n)]     # constrained vertices touching island i
s0 = sg(GROUND)
out = {"inputs": {"real_4x4.txt sha256": hashlib.sha256(raw).hexdigest()}, "E0_over_A_num_over_2^70": int(E0 * two70)}
# ---- A. single flips from the certified ground witness ----
rows = []
for i in range(n):
    idv = GROUND ^ (1 << i)
    d = H(idv) - E0                                   # exact
    h = sum(K[i][j] * s0[j] for j in range(n) if j != i)
    assert d == -2 * s0[i] * h
    rows.append({"island": i, "vertices_touched": nv_of[i], "excluded": (not in_grammar(idv)),
                 "gap_num_over_2^70": int(d * two70), "gap_in_A": float(d), "gap_in_kBT": to_kBT(d)})
assert all(r["excluded"] for r in rows)
bd = [r for r in rows if r["vertices_touched"] == 1]; bk = [r for r in rows if r["vertices_touched"] == 2]
out["n_boundary_islands"] = len(bd); out["n_bulk_islands"] = len(bk)
mb = min(bd, key=lambda r: r["gap_num_over_2^70"]); mk = min(bk, key=lambda r: r["gap_num_over_2^70"])
out["min_boundary_flip"] = mb; out["min_bulk_flip"] = mk
out["max_boundary_flip_kBT"] = max(r["gap_in_kBT"] for r in bd); out["max_bulk_flip_kBT"] = max(r["gap_in_kBT"] for r in bk)
Dnum = 12095447728404694790
out["certified_gap_num_over_2^70"] = Dnum
out["single_flip_min_equals_certified_gap"] = (mb["gap_num_over_2^70"] == Dnum and mb["island"] == 6)
out["flip6_id_equals_true_excluded_id"] = ((GROUND ^ (1 << 6)) == TRUE_EXCL)
out["frozen_excluded_is_flip_of_island"] = [i for i in range(n) if (GROUND ^ (1 << i)) == FROZEN_EXCL]
out["single_flips"] = rows
vidx = lambda i: [k for k, (m, _) in enumerate(verts) if m >> i & 1]
corner_vertices = {0, 3, 12, 15}          # row-major vertex index k = row*4 + col on the 4x4 patch
for r in rows:
    r["vertex_indices"] = vidx(r["island"]); r["touches_corner_vertex"] = bool(set(r["vertex_indices"]) & corner_vertices)
low = sorted(rows, key=lambda r: r["gap_num_over_2^70"])
tier1 = [r for r in low if r["gap_in_kBT"] < 1.0]
out["lowest_tier_islands"] = [r["island"] for r in tier1]
out["lowest_tier_all_touch_corner_vertex"] = all(r["touches_corner_vertex"] for r in tier1)
out["lowest_tier_spread_num_over_2^70"] = tier1[-1]["gap_num_over_2^70"] - tier1[0]["gap_num_over_2^70"]
out["lowest_tier_spread_relative_to_gap"] = out["lowest_tier_spread_num_over_2^70"] / Dnum
out["corner_vertex_islands_count"] = sum(1 for r in rows if r["touches_corner_vertex"])
second = [r for r in low if 1.0 <= r["gap_in_kBT"] < 1.2]
out["second_tier_islands"] = [r["island"] for r in second]
out["second_tier_touch_corner"] = any(r["touches_corner_vertex"] for r in second)
out["one_vertex_flip_range_kBT"] = [min(r["gap_in_kBT"] for r in rows if r["vertices_touched"] == 1), max(r["gap_in_kBT"] for r in rows if r["vertices_touched"] == 1)]
out["two_vertex_flip_range_kBT"] = [min(r["gap_in_kBT"] for r in rows if r["vertices_touched"] == 2), max(r["gap_in_kBT"] for r in rows if r["vertices_touched"] == 2)]
# ---- pair decomposition of the certified witness (flip of island 6) ----
def dist(i, j): return math.hypot(isl[i].x - isl[j].x, isl[i].y - isl[j].y) / P.TEMPLATE["a"]
def decomp(i):
    parts = []
    for j in range(n):
        if j == i: continue
        contrib = -2 * s0[i] * K[i][j] * s0[j]       # change in pair energy when i flips (units of A)
        parts.append({"j": j, "r_over_a": round(dist(i, j), 6), "dE_in_A": float(contrib), "dE_in_kBT": to_kBT(contrib)})
    return sorted(parts, key=lambda p: p["r_over_a"])
def shells(parts):
    sh = {}
    for p in parts:
        key = "%.3f" % p["r_over_a"]; sh.setdefault(key, 0.0); sh[key] += p["dE_in_kBT"]
    return sh
out["decomposition_island6"] = decomp(6); out["decomposition_island6_by_shell_kBT"] = shells(decomp(6))
bi = mk["island"]
out["decomposition_lowest_bulk_island"] = {"island": bi, "pairs": decomp(bi), "by_shell_kBT": shells(decomp(bi))}
def cumul(parts):
    acc = 0.0; res = []; seen = {}
    for p in parts:
        seen.setdefault(p["r_over_a"], []).append(p["dE_in_kBT"])
    for r in sorted(seen):
        acc += sum(seen[r]); res.append({"r_over_a": r, "partners": len(seen[r]), "shell_kBT": sum(seen[r]), "cumulative_kBT": acc})
    return res
out["cumulative_island6"] = cumul(out["decomposition_island6"])
out["cumulative_lowest_two_vertex_island"] = cumul(out["decomposition_lowest_bulk_island"]["pairs"])
out["decomp_sum_check_island6_kBT"] = sum(p["dE_in_kBT"] for p in out["decomposition_island6"])
# ---- B. perturbation-bound inputs ----
sumabsK = sum(abs(K[i][j]) for i in range(n) for j in range(i + 1, n))
out["sum_abs_K_in_A"] = float(sumabsK)
Dnom = Fraction(Dnum, two70)
out["Delta_in_A"] = float(Dnom)
out["Delta_over_sum_abs_K"] = float(Dnom / sumabsK)
# distance ranking of all 780 pairs
pairs = sorted(((dist(i, j), i, j) for i in range(n) for j in range(i + 1, n)))
def trunc_eps(npairs):
    return sum(abs(K[i][j]) for _, i, j in pairs[npairs:])
tr = {}
for npairs in (126,):
    e = trunc_eps(npairs); tr[str(npairs)] = {"retained_pairs": npairs, "removed_sum_abs_K_A": float(e),
        "fraction_of_total": float(e / sumabsK), "two_eps_over_Delta": float(2 * e / Dnom)}
out["truncation_nearest_pairs"] = tr
# shells for reference: cumulative number of pairs within given distance
dists = sorted(set(round(d, 6) for d, _, _ in pairs))[:8]
out["first_distance_shells_r_over_a"] = dists
out["pairs_within_shell_counts"] = {str(d): sum(1 for x, _, _ in pairs if x <= d + 1e-9) for d in dists}
# uniform relative perturbation tolerance and island-dimension perturbations (K changes only; A rescaled consistently)
out["uniform_relative_tolerance_eta_max"] = float(Dnom / (2 * sumabsK))   # |eta|*sum|K| < Delta/2  ->  bound < Delta
T = 792.0; l0, w0, h0 = P.TEMPLATE["l"], P.TEMPLATE["w"], P.TEMPLATE["h"]
pairs_idx = [(i, j) for i in range(n) for j in range(i + 1, n)]
K0 = [P.K_pair(isl[i], isl[j], l0, w0, h0) for i, j in pairs_idx]
A0 = P.A_joule(T)
Dj = float(Dnom) * A_J
dim = {}
for name, f in (("l", (1, 0, 0)), ("w", (0, 1, 0)), ("h", (0, 0, 1))):
    for p in (0.01, 0.05):
        l, w, h = l0 * (1 + p * f[0]), w0 * (1 + p * f[1]), h0 * (1 + p * f[2])
        K1 = [P.K_pair(isl[i], isl[j], l, w, h) for i, j in pairs_idx]
        A1 = P.A_joule(T, l=l, w=w, h=h) if True else A0
        eps = sum(abs(A1 * k1 - A0 * k0) for k0, k1 in zip(K0, K1))
        dim[f"{name} x (1+{p})"] = {"A1_over_A0": A1 / A0, "eps_J": eps, "two_eps_over_Delta": 2 * eps / Dj}
out["dimension_perturbations_worst_case"] = dim
# ---- scale-separated bound: H' = lam*H + R  =>  Delta' in [lam*Delta - 2 sup|R|, lam*Delta + 2 sup|R|] ----
def best_lambda(a, b):
    """minimise sum |a_k - lam*b_k| over lam (weighted median of a_k/b_k with weights |b_k|)."""
    items = sorted(((a_k / b_k), abs(b_k)) for a_k, b_k in zip(a, b) if b_k != 0)
    tot = sum(w for _, w in items); acc = 0.0
    for r, w in items:
        acc += w
        if acc >= tot / 2: return r
KJ0 = [A0 * k for k in K0]
out["scale_separated"] = {}
for name, f in (("l", (1, 0, 0)), ("w", (0, 1, 0)), ("h", (0, 0, 1))):
    for p in (0.01, 0.05):
        l, w, h = l0 * (1 + p * f[0]), w0 * (1 + p * f[1]), h0 * (1 + p * f[2])
        A1 = P.A_joule(T, l=l, w=w, h=h)
        KJ1 = [A1 * P.K_pair(isl[i], isl[j], l, w, h) for i, j in pairs_idx]
        lam = best_lambda(KJ1, KJ0)
        res = sum(abs(a_ - lam * b_) for a_, b_ in zip(KJ1, KJ0))
        out["scale_separated"][f"{name} x (1+{p})"] = {"lambda": lam, "residual_eps_J": res, "two_res_over_lambda_Delta": 2 * res / (lam * Dj)}
trunc_res = {}
for npairs in (126,):
    keep = [(i, j) for _, i, j in pairs[:npairs]]; kk = set(keep)
    a_ = [KJ0[q] if (i, j) in kk else 0.0 for q, (i, j) in enumerate(pairs_idx)]
    lam = best_lambda(a_, KJ0)
    res = sum(abs(x - lam * y) for x, y in zip(a_, KJ0))
    trunc_res[str(npairs)] = {"lambda": lam, "residual_eps_J": res, "two_res_over_lambda_Delta": 2 * res / (lam * Dj)}
out["scale_separated_truncation"] = trunc_res
# persistence of the failure at W = 1 kBT under a general perturbation of sup-norm size eps: need Delta + 2 eps <= W
W_A = kBT / A_J                                   # 1 kBT in units of A
delta4 = float(Dnom) / W_A
out["delta4"] = delta4
out["failure_persistence_eps_max_in_A"] = (1.0 - delta4) * W_A / 2
out["failure_persistence_relative_to_sum_abs_K"] = out["failure_persistence_eps_max_in_A"] / float(sumabsK)
out["sufficiency_persistence_below_W_kBT"] = (float(Dnom) - 2 * 0.0) / W_A   # at eps=0; general: (Delta-2eps)/kBT
out["note"] = ("Worst-case bound |Delta'-Delta| <= 2*eps with eps = sup_s |H'(s)-H(s)| <= sum_{i<j} |A'K'_ij - A K_ij|. "
               "two_eps_over_Delta >= 1 means the bound cannot exclude a gap change as large as the gap itself.")
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "supplement_analysis_v001_output.json"), "w"), indent=1)
print(json.dumps({k: v for k, v in out.items() if k not in ("single_flips", "decomposition_island6", "decomposition_lowest_bulk_island", "decomposition_island6_by_shell_kBT")}, indent=1))
print("single flips (island, vertices touched, gap in kBT):")
for r in sorted(rows, key=lambda r: r["gap_num_over_2^70"]): print(r["island"], r["vertices_touched"], round(r["gap_in_kBT"], 5))

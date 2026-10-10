#!/usr/bin/env python3
"""SCR-III GAP-4x4 witness-and-certification audit v001 (no search of the 4x4 space; witnesses evaluated only).
usage: gap4_audit_v001.py WORKDIR OUT_JSON   (WORKDIR has build/{physical_energy_v005.py,solver_v010_fresh} and run/{real_4x4.txt,GAP4_FIRST_RUN.jsonl,pub1-3.txt})"""
import sys, json, math, random, hashlib, subprocess, pathlib
from fractions import Fraction
from decimal import Decimal, getcontext
import numpy as np
W = pathlib.Path(sys.argv[1]); OUT = sys.argv[2]
sys.dont_write_bytecode = True; sys.path.insert(0, str(W/"build"))
import physical_energy_v005 as P
SV = str(W/"build/solver_v010_fresh"); R = {}
def parse(path):
    t = pathlib.Path(path).read_text().split(); n, nv = int(t[0]), int(t[1]); c = 2
    K = [[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n): K[i][j] = K[j][i] = float(t[c]); c += 1
    vs = [(int(t[c+2*v]), int(t[c+2*v+1])) for v in range(nv)]; assert c+2*nv == len(t); return n, nv, K, vs
def cnt_in(m, p, s):  # number of 'in' arms by serialized masks
    return sum(1 for i in range(len(s)) if (m >> i) & 1 and ((s[i] > 0) == bool((p >> i) & 1)))
n, nv, K, vs = parse(W/"run/real_4x4.txt")
isl = P.source_geometry(4); vp = P.vertex_positions(4); inc = P.incident_islands(isl, vp); pairs = P.K_pairs(isl)
S = math.fsum(abs(k) for _, _, k in pairs)
R["instance"] = dict(n=n, nv=nv, K_equals_geometry=all(K[i][j] == k for i, j, k in pairs), masks_equal_geometry=sorted(m for m, _ in vs) == sorted(sum(1 << i for i in x) for x in inc), S_sum_abs_K=S)
# ---- coupling precision: recompute every K in 60-digit decimal from the same double inputs ----
getcontext().prec = 60
D = lambda x: Decimal(x)
T = P.TEMPLATE; l_, w_, h_ = D(T["l"]), D(T["w"]), D(T["h"])
def Kdec(ei, ej):
    rx, ry = D(ej.x)-D(ei.x), D(ej.y)-D(ei.y); d = (rx*rx+ry*ry).sqrt()
    def inv(a, c):
        sq = (1 + (l_/(3*d))**2 + (l_/(3*d))**2 + Decimal(2)/3*c*l_*(rx*D(ej.ux)+ry*D(ej.uy))/d**2
              - Decimal(2)/3*a*l_*(rx*D(ei.ux)+ry*D(ei.uy))/d**2 - Decimal(2)/9*a*c*l_*l_*(D(ei.ux)*D(ej.ux)+D(ei.uy)*D(ej.uy))/d**2)
        return 1/sq.sqrt()
    return Decimal(3)/16*(w_*h_)/(l_*d)*(inv(1, 1)+inv(-1, -1)-inv(1, -1)-inv(-1, 1))
dk = [abs(D(k)-Kdec(isl[i], isl[j])) for i, j, k in pairs]
sumdk = float(sum(dk)); maxrel = max(float(a/abs(D(k))) for a, (i, j, k) in zip(dk, pairs))
R["coupling_precision"] = dict(sum_abs_dK=sumdk, sum_abs_dK_over_S=sumdk/S, max_rel_error_per_pair=maxrel, energy_shift_bound_per_state=sumdk, gap_shift_bound=2*sumdk,
    note="K doubles treated as the model; recomputing the source formula in 60 digits from the same double inputs bounds how far the double K are from the formula")
# ---- witnesses ----
runs = [json.loads(x) for x in open(W/"run/GAP4_FIRST_RUN.jsonl")]; names = ("ground", "non_grammar"); A = P.A_joule(792.0); kT = P.KB*792.0
Wt = {}
for nm, r in zip(names, runs):
    s = P.decode(r["witness_id"], n); ex = sum(Fraction(k)*s[i]*s[j] for i, j, k in pairs)
    ch = P.vertex_charges_geometric(s, isl, vp); eJ = math.fsum(s[i]*s[j]*P.pair_energy_charge_model_J(isl[i], isl[j], 792.0) for i, j, _ in pairs)
    Wt[nm] = dict(s=s, E=float(ex), exact=ex)
    R.setdefault("witnesses", {})[nm] = dict(id=r["witness_id"], solver_upper=r["upper"], E_exact_rational=float(ex), abs_diff_vs_solver=float(abs(Fraction(r["upper"])-ex)),
        within_tau_1e9_S=float(abs(Fraction(r["upper"])-ex)) <= 1e-9*S, E_charge_position_model_J=eJ, E_K_model_J=float(ex)*A, charge_vs_K_rel_diff=abs(eJ-float(ex)*A)/abs(float(ex)*A),
        geometric_ice_rule_ok=P.ice_ok_geometric(s, isl, vp), geometric_vertex_charges=ch, geometric_violating_vertices=[i for i, q in enumerate(ch) if q],
        mask_violating_vertices=[i for i, (m, p) in enumerate(vs) if cnt_in(m, p, s) != 2])
# mask/geometric vertex order may differ: compare as sets via vertex island sets
mi = {frozenset(i for i in range(n) if (m >> i) & 1): v for v, (m, p) in enumerate(vs)}
for nm in names:
    s = Wt[nm]["s"]; gv = [frozenset(inc[v]) for v in R["witnesses"][nm]["geometric_violating_vertices"]]
    mv = [frozenset(i for i in range(n) if (vs[v][0] >> i) & 1) for v in R["witnesses"][nm]["mask_violating_vertices"]]
    R["witnesses"][nm]["mask_vs_geometric_same_violating_vertex_sets"] = sorted(map(sorted, gv)) == sorted(map(sorted, mv))
E0 = Wt["ground"]["E"]; EN = Wt["non_grammar"]["E"]; dlt = (EN-E0)*A/kT
R["gap"] = dict(delta_A=EN-E0, delta4=dlt, I_R2=[0.790439676056526, 1.0333534753990623], inside_R2=0.790439676056526 <= dlt <= 1.0333534753990623, below_1=dlt < 1,
    margin_to_nearest_R2_edge=min(dlt-0.790439676056526, 1.0333534753990623-dlt), margin_to_1=1-dlt, coupling_precision_delta_shift_bound=2*sumdk*A/kT)
# local optimality (consistency only)
KM = np.array(K); en = lambda s: 0.5*float(np.asarray(s, float) @ KM @ np.asarray(s, float)); idx = np.arange(n)
s0 = np.array(Wt["ground"]["s"], float); e0 = en(s0)
l1 = min(en(np.where(idx == i, -s0, s0)) for i in range(n)); l2 = min(en(np.where((idx == i) | (idx == j), -s0, s0)) for i in range(n) for j in range(i+1, n))
s1 = np.array(Wt["non_grammar"]["s"], float); e1 = en(s1); nb = []
for i in range(n):
    t = s1.copy(); t[i] *= -1; nb.append(t)
    for j in range(i+1, n): t = s1.copy(); t[i] *= -1; t[j] *= -1; nb.append(t)
nbv = [en(t) for t in nb if any(cnt_in(m, p, list(t)) != 2 for m, p in vs)]
R["local_optimality_consistency_only"] = dict(ground_1flip_2flip_min_ok=(l1 >= e0-1e-15 and l2 >= e0-1e-15), nongrammar_violating_neighbours_ok=(min(nbv) >= e1-1e-15), n_violating_neighbours=len(nbv))
# ---- public patches: fresh binary vs independent exhaustive scan vs frozen references ----
REF = {1: 0.009438264173023073, 2: 0.010315265098625195, 3: 0.010212546058288613}; val = {}
for L in (1, 2, 3):
    f = W/("run/pub%d.txt" % L); nn, nvv, KK, vss = parse(f)
    out = [json.loads(x) for x in subprocess.check_output([SV, str(f), "60"], text=True).splitlines()]
    il = P.source_geometry(L); vpl = P.vertex_positions(L); Km = np.zeros((nn, nn))
    for i, j, k in P.K_pairs(il): Km[i, j] = Km[j, i] = k
    best = bestv = np.inf; ch = 1 << min(nn, 20)
    for base in range(0, 1 << nn, ch):
        ids = np.arange(base, min(base+ch, 1 << nn), dtype=np.int64); Sx = (((ids[:, None] >> np.arange(nn)) & 1)*2-1).astype(float)
        e = 0.5*np.einsum('ij,jk,ik->i', Sx, Km, Sx); ok = np.ones(len(ids), bool)
        for m, p in vss:
            ii = [i for i in range(nn) if (m >> i) & 1]; ok &= (sum(((Sx[:, i] > 0) == bool((p >> i) & 1)).astype(int) for i in ii) == 2)
        best = min(best, e.min()); bestv = min(bestv, e[~ok].min())
    rnd = random.Random(7); agree = all(P.ice_ok_geometric(s, il, vpl) == all(cnt_in(m, p, s) == 2 for m, p in vss) for s in ([rnd.choice((-1, 1)) for _ in range(nn)] for _ in range(300)))
    val[L] = dict(nodes=[o["nodes"] for o in out], E0_match_exhaustive=abs(best-out[0]["upper"]) < 1e-14, Enong_match_exhaustive=abs(bestv-out[1]["upper"]) < 1e-14,
        delta_solver=out[1]["upper"]-out[0]["upper"], delta_frozen=REF[L], abs_diff=abs(out[1]["upper"]-out[0]["upper"]-REF[L]), masks_agree_with_geometric_rule_300_random=agree)
val[3]["E0_J_solver"] = None
R["public_validation"] = val
# ---- bound admissibility & violation-filter soundness: exact completion minima ----
def bound_formula(Kx, spin, d, acc, nn):
    l = acc
    for j in range(d, nn):
        l -= abs(sum(Kx[i][j]*spin[i] for i in range(d))); l -= sum(abs(Kx[j][h]) for h in range(j+1, nn))
    return l
def exhaustive_check(L, full):
    f = W/("run/pub%d.txt" % L); nn, nvv, KK, vss = parse(f); Km = np.array(KK); rng = random.Random(20261010); worst = np.inf; nb_ = 0; nviol = 0; viol_bad = 0
    prefs = []
    if full:
        for d in range(0, nn+1):
            for b in range(1 << d): prefs.append([(1 if (b >> i) & 1 else -1) for i in range(d)])
    else:
        for _ in range(400):
            d = rng.randint(4, 20); prefs.append([rng.choice((-1, 1)) for _ in range(d)])
    for pre in prefs:
        d = len(pre); spin = pre+[-1]*(nn-d); acc = math.fsum(KK[i][j]*pre[i]*pre[j] for i in range(d) for j in range(i+1, d)); b = bound_formula(KK, spin, d, acc, nn)
        ids = np.arange(1 << (nn-d), dtype=np.int64); Tm = ((ids[:, None] >> np.arange(nn-d)) & 1)*2-1
        Sx = np.hstack([np.tile(np.array(pre, float), (len(ids), 1)), Tm.astype(float)]); e = 0.5*np.einsum('ij,jk,ik->i', Sx, Km, Sx)
        worst = min(worst, float(e.min()-b)); nb_ += 1
        # violation filter: if the filter says "no violation possible" then no completion may violate
        poss = False
        for m, p in vss:
            c = lf = 0
            for i in range(nn):
                if (m >> i) & 1:
                    if i < d: c += int((spin[i] > 0) == bool((p >> i) & 1))
                    else: lf += 1
            if c > 2 or c+lf < 2 or lf > 0: poss = True; break
        if not poss:
            nviol += 1
            for row in Sx:
                if any(cnt_in(m, p, list(row)) != 2 for m, p in vss): viol_bad += 1
    return dict(prefixes=nb_, min_true_completion_min_minus_bound=worst, bound_admissible=worst >= 0, violation_filter_false_cases=nviol, violating_completions_after_filter_false=viol_bad)
R["bound_and_filter_exact_tests"] = {"2x2_all_prefixes_all_depths": exhaustive_check(2, True), "3x3_400_random_prefixes": exhaustive_check(3, False)}
# ---- analytic floating-point bound (standard model, Higham): u = 2^-53, gamma_k = k u / (1 - k u) ----
u = 2.0**-53; g = lambda k: k*u/(1-k*u); nn = 40
ops_l = nn+sum(nn-j-1 for j in range(nn))         # sequential subtractions into the running bound (<= 820)
e_b = (g(ops_l)+g(nn))*S                          # bound: running sum + acc chain; fields (<= g(39)) are inside the g(ops_l) chain bound
e_best = g(nn)*S                                  # incumbent: nested sum of the assigned-pair terms
guard = 1e-11*max(1.0, S)
R["rounding_analysis"] = dict(model="IEEE-754 binary64, round-to-nearest, no FMA needed (all products are by +-1, hence exact), recursive summation, Higham gamma_k; K read exactly (17 digits)",
    n_ops_running_bound=ops_l, error_bound_of_bound_abs=e_b, error_bound_of_incumbent_abs=e_best, required_guard_abs=e_b+e_best+g(1)*S, actual_guard_abs=guard,
    margin_factor=guard/(e_b+e_best+g(1)*S), S=S,
    prune_soundness_argument="prune iff fl(bound)-guard >= fl(best). Then real_bound >= fl(bound)-e_b >= fl(best)+guard-e_b >= E(best_state)-e_best+guard-e_b >= E(best_state) because guard >= e_b+e_best; so no pruned completion beats the incumbent.",
    ties="a node whose bound equals the incumbent is pruned: degeneracy at the optimum is not enumerated (descriptive only)")
json.dump(R, open(OUT, "w"), indent=1, default=str)
b = R["bound_and_filter_exact_tests"]; w = R["witnesses"]
print(json.dumps(dict(K_equals_geometry=R["instance"]["K_equals_geometry"], masks_equal_geometry=R["instance"]["masks_equal_geometry"],
    witness_ground=dict(diff=w["ground"]["abs_diff_vs_solver"], geom_ok=w["ground"]["geometric_ice_rule_ok"], charge_rel=w["ground"]["charge_vs_K_rel_diff"]),
    witness_nong=dict(diff=w["non_grammar"]["abs_diff_vs_solver"], geom_viol=w["non_grammar"]["geometric_violating_vertices"], same_sets=w["non_grammar"]["mask_vs_geometric_same_violating_vertex_sets"], charge_rel=w["non_grammar"]["charge_vs_K_rel_diff"]),
    gap=R["gap"], coupling=R["coupling_precision"], local=R["local_optimality_consistency_only"], public=val, tests=b, rounding=R["rounding_analysis"]), indent=1, default=str))

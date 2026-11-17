"""D3 -- divisibility hierarchy.  Reads D1 / D1b / D4 results, computes
 (i) pointwise law check  d_B(n) <= d_A(n)  (A | B)  on the survey,
 (ii) certified lower bounds  L(A) = max d over all data at multiples B of A  (valid by the pointwise law),
 (iii) mean route lengths along divisor chains, (iv) the set of scales with certified D_B = 6.
All lower bounds are CERTIFIED (exact finite data); nothing here is a universal supremum except where D_B=6 is forced by the proved bound D_B <= 6."""
import json, os, glob, sys
here = os.path.dirname(os.path.abspath(__file__)); res = os.path.join(here, "..", "results")
surv = sorted(glob.glob(os.path.join(res, "D1b_survey_B*_N*.json")))
data = {}                      # B -> {n: d}
for f in surv:
    s = json.load(open(f))
    for B, ds in s["d"].items():
        data.setdefault(int(B), {}).update({n: d for n, d in enumerate(ds, 1)})
witness = {}                   # B -> max d known from long runs with n
for f in glob.glob(os.path.join(res, "D1_B*_N*.json")):
    r = json.load(open(f)); B = r["B"]
    witness[B] = max(witness.get(B, (0, 0)), (r["finite_max"], int(r["first_witness"][str(r["finite_max"])]["n"])))
for f in glob.glob(os.path.join(res, "D4_smooth_B*.json")):
    r = json.load(open(f)); B = r["B"]
    mx = r["finite_max"]; n = [w["n"] for w in r["d_ge_5_witnesses"] if w["d"] == mx]
    if n: witness[B] = max(witness.get(B, (0, 0)), (mx, n[0]))
for B, ds in data.items():
    m = max(ds.values()); n = min(k for k, v in ds.items() if v == m); witness[B] = max(witness.get(B, (0, 0)), (m, n))

viol = []; checked = 0
Bs = sorted(data)
for A in Bs:
    for B in Bs:
        if B > A and B % A == 0:
            common = data[A].keys() & data[B].keys()
            for n in common:
                checked += 1
                if data[B][n] > data[A][n]: viol.append((A, B, n))
allB = sorted(set(witness))
L = {}
for A in allB:
    best = (0, None, None)
    for B in allB:
        if B % A == 0 and witness[B][0] > best[0]: best = (witness[B][0], B, witness[B][1])
    L[A] = best
D6 = sorted(A for A in allB if L[A][0] == 6)
mean = {}
for B in Bs:
    v = list(data[B].values()); mean[B] = sum(v) / len(v)
out = {"pointwise_law_pairs_checked": checked, "pointwise_law_violations": viol, "surveyed_B": Bs,
       "certified_lower_bound": {str(A): {"L": L[A][0], "witness_scale": L[A][1], "witness_n": L[A][2]} for A in allB},
       "scales_with_certified_D_B_equal_6": D6,
       "mean_route_length_survey": {str(B): round(mean[B], 4) for B in Bs},
       "status": "L(A) CERTIFIED lower bound on D_A (exact distance at a multiple B of A, pointwise law); D_A=6 certified exactly when L(A)=6 (D_A<=6 proved)."}
json.dump(out, open(os.path.join(res, "D3_hierarchy.json"), "w"), indent=1)
print("checked", checked, "violations", len(viol), "D=6 certified for", D6[:30], "...", len(D6))
print({A: L[A][0] for A in allB if A <= 24})

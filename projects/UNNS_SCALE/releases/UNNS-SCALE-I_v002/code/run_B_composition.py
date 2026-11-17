"""v002-B  hierarchical composition: additivity identity and exact level stratification."""
import json, os, random, sys
from scale_lib import factor, merge, neighbours, degree
from boundary_lib import eps_closed, strata, deg_e, mul_e

random.seed(20261116)
res = {"part": "B", "claims": {}}

# ---- B1: eps_{AB}(x) = eps_A(x) + eps_B(Ax) = eps_B(x) + eps_A(Bx) --------------------------------
pairs = [(10, 10), (2, 5), (6, 10), (10**3, 10**3), (10**4, 10**4), (10**6, 10**6), (12, 18), (7, 49), (30, 77)]
b1 = {}; bad = 0
for A, B in pairs:
    fA, fB = factor(A), factor(B); fAB = merge(fA, fB)
    n = 0
    for x in list(range(1, 1200)) + [random.randrange(1200, 10**6) for _ in range(300)]:
        fx = factor(x)
        lhs = eps_closed(fAB, fx)
        r1 = eps_closed(fA, fx) + eps_closed(fB, merge(fA, fx))
        r2 = eps_closed(fB, fx) + eps_closed(fA, merge(fB, fx))
        # enumeration-based reference for the left side: non-lattice neighbours of ABx w.r.t. lattice AB*Z
        nb = neighbours(merge(fAB, fx)); enum = sum(1 for (_, _, v) in nb if v % (A * B) != 0)
        bad += not (lhs == r1 == r2 == enum); n += 1
    b1[f"{A}x{B}"] = {"vertices": n}
res["claims"]["B1_additivity"] = {"pairs": b1, "mismatches": bad}

# ---- B2: level stratification of a vertex neighbourhood ---------------------------------------------
# chain radices [B1..Bd], P_j = B1..Bj, u = P_d x.  neighbours of u in P_j Z \ P_{j+1} Z : strata[j]
def enum_strata(Bs, x):
    P = [1]
    for B in Bs: P.append(P[-1] * B)
    f = factor(x)
    for B in Bs: f = merge(f, factor(B))
    d = len(Bs); cnt = [0] * (d + 1)
    for (_, _, v) in neighbours(f):
        j = 0
        while j < d and v % P[j + 1] == 0: j += 1      # deepest lattice level containing v
        cnt[j] += 1
    return cnt

chains = [[10**6, 10**6], [10**4, 10**4, 10**4], [10**3] * 4, [10**2] * 6, [10] * 12, [10**4, 10**8], [2, 3, 5, 7], [10**6, 10**3, 10**3], [10**3, 10**6, 10**3]]
b2 = {}; bad2 = 0
for Bs in chains:
    fs = [factor(B) for B in Bs]; n = 0; b = 0
    for x in list(range(1, 400)) + [random.randrange(400, 10**5) for _ in range(120)]:
        s_formula = strata(fs, factor(x)); s_enum = enum_strata(Bs, x)
        b += s_formula != s_enum; n += 1
    b2["x".join(map(str, Bs))] = {"vertices": n, "mismatches": b, "profile_at_x=1": strata(fs, {})}
    bad2 += b
res["claims"]["B2_level_stratification"] = {"chains": b2, "mismatches": bad2}

# ---- B3: the 10^12 comparison at x = 1 (infinite graph) ------------------------------------------------
f12 = factor(10**12)
res["claims"]["B3_trillion_decompositions_x1"] = {
    "deg(10^k)": {str(k): deg_e(factor(10**k)) for k in (0, 4, 6, 8, 12)},
    "eps_10^12(1) total": eps_closed(f12, {}),
    "6+6 profile [stay at 10^6-level exits, exits of 10^12 lattice]": strata([factor(10**6)] * 2, {}),
    "4+4+4 profile": strata([factor(10**4)] * 3, {}),
    "sum of non-top strata, 6+6": sum(strata([factor(10**6)] * 2, {})[:2]),
    "sum of non-top strata, 4+4+4": sum(strata([factor(10**4)] * 3, {})[:3]),
}
res["PASS"] = (bad == 0 and bad2 == 0 and
               res["claims"]["B3_trillion_decompositions_x1"]["sum of non-top strata, 6+6"] == 216 ==
               res["claims"]["B3_trillion_decompositions_x1"]["sum of non-top strata, 4+4+4"] == eps_closed(f12, {}))
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "B_composition.json"), "w"), indent=1)
print(json.dumps(res["claims"]["B3_trillion_decompositions_x1"], indent=1))
print("B1 mismatches", bad, "B2 mismatches", bad2, "PASS", res["PASS"]); sys.exit(0 if res["PASS"] else 1)

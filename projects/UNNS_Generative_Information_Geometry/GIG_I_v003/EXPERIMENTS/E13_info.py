"""E13 -- third-boundary information: f_3, J_3 = rank d_3, D_3 = f_3 - J_3 over the census domains; graph-class ambiguity
A_3([G];D) = log2 |R_3([G];D)|  with  R_3([G];D) = { J_3(X) : X in D, swap graph of X isomorphic to G }  (domain-relative, empirical);
the information about J_3 / beta_2 that is NOT carried by the T15 (2-skeleton) data (f_0,f_1,f_2,rank d_1,rank d_2)."""
import math
import time
from collections import Counter, defaultdict
import _path  # noqa: F401
import _recovery as R
import realizability as rz
import boundary_info as bi


entropy, cond_entropy = bi.entropy, bi.cond_entropy


def domain(k, L, quick, extra=()):
    s = R.scan(k, L, budget=None if k <= 5 else (60 if quick else 1500), seed=20260611, extra=extra)
    recs = s["records"]
    found = R.census(k, L)[0]
    d = {"k": k, "L": L, "sets": len(recs), "exhaustive": s["exhaustive"]}
    d["f3_histogram"] = {str(a): b for a, b in sorted(Counter(r["f3"] for r in recs).items())}
    d["J3_histogram"] = {str(a): b for a, b in sorted(Counter(r["J3"] for r in recs).items())}
    d["D3_histogram"] = {str(a): b for a, b in sorted(Counter(r["D3"] for r in recs).items())}
    d["sets_with_D3_positive"] = sum(r["D3"] > 0 for r in recs)
    d["sets_with_beta2_positive"] = sum(r["betti"][2] > 0 for r in recs)
    d["max_beta2"] = max(r["betti"][2] for r in recs)
    d["identity_beta2_eq_f2_minus_r2_minus_r3_on_all"] = all(r["betti"][2] == r["f"][2] - r["ranks"][1] - r["ranks"][2] for r in recs)
    # information beyond the 2-skeleton data
    two = [((r["f"][0], r["f"][1], r["f"][2], r["ranks"][0], r["ranks"][1]), r) for r in recs]
    d["H_J3_given_2skeleton_data_bits"] = round(cond_entropy([(x, r["J3"]) for x, r in two]), 4)
    d["H_f3_given_2skeleton_data_bits"] = round(cond_entropy([(x, r["f"][3]) for x, r in two]), 4)
    d["H_beta2_given_2skeleton_data_bits"] = round(cond_entropy([(x, r["betti"][2]) for x, r in two]), 4)
    d["H_J3_marginal_bits"] = round(entropy(Counter(r["J3"] for r in recs)), 4)
    d["two_skeleton_data_classes"] = len({x for x, _ in two})
    d["two_skeleton_classes_with_several_J3"] = sum(1 for x in {x for x, _ in two} if len({r["J3"] for y, r in two if y == x}) > 1)
    # graph-class ambiguity (exact isomorphism classes; only on exhaustive domains)
    if s["exhaustive"]:
        classes = rz.iso_classes(found, k)[0]
        byrec = {r["mask"]: r for r in recs}
        A3 = []
        amb_f3 = amb_b = 0
        for cl in classes:
            J = {byrec[m]["J3"] for m in cl}
            A3.append(bi.A3(J))
            amb_f3 += len({byrec[m]["f3"] for m in cl}) > 1
            amb_b += len({byrec[m]["betti"] for m in cl}) > 1
        d["graph_classes"] = len(classes)
        d["classes_with_several_J3"] = sum(a > 0 for a in A3)
        d["classes_with_several_f3"] = amb_f3
        d["classes_with_several_Betti"] = amb_b
        d["A3_max_bits"] = max(A3)
        d["A3_mean_bits"] = round(sum(A3) / len(A3), 6)
    else:
        d["graph_classes"] = None
        d["note"] = "partial domain: A_3 is reported only for exhaustive domains; for the sample each checked set is a reconstruction success (E12), hence J_3 is a function of its graph"
    return d


def run(quick=False):
    t0 = time.time()
    plan = [(4, 16), (5, 10), (6, 8)] if quick else [(4, 40), (5, 16), (6, 10)]
    out = {"experiment": "E13", "domains": [domain(k, L, quick) for k, L in plan]}
    out["seconds"] = round(time.time() - t0, 1)
    return out


if __name__ == "__main__":
    import json
    print(json.dumps(run(quick=True), indent=1))

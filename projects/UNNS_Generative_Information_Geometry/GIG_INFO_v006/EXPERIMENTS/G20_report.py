import json, os
import _path
R = os.path.join(_path.ROOT, "RESULTS"); d = json.load(open(os.path.join(R, "D21_minimal_observation.json")))
L = ["# GIG-INFO v006 — synthesis report", "", "## How little of the dead-set nerve decides beta_2 > 0 ?", "",
     f"Exhaustive over the census: {d['regimes']} regimes (full mask excluded), {d['patterns']} distinct dead-set patterns, {d['positive_patterns']} with beta_2>0 ({d['positive_regimes']} regimes). Exact H1 via strong-collapse cores (homotopy-preserving; checked against the full nerve on 355 patterns, 0 mismatches).", "",
     "| observation O | H(Y|O) natural | H(Y|O) balanced | classes |", "|---|---|---|---|"]
for k, v in d["observations"].items():
    L.append(f"| {k} | {v['natural']['H(Y|O)']} | {v['balanced']['H(Y|O)']} | {v['natural']['classes']} |")
L += ["", f"* Positive cores (S6 types: {d['n_positive_core_types']}) have sizes {d['core_size_positive']} vertices; the commonest is the bare hollow triangle.",
      f"* {d['negatives_with_empty_or_point_core']} negative patterns collapse to a point (no homology to compute); negative core size quantiles {d['core_size_negative_quantiles']}.",
      f"* Hollow triangles are common among negatives ({d['negatives_with_Hol_gt_0']} patterns) so their count is not a test.", "",
      "No tested count-level statistic of the nerve (V,E,triangles,hollow count,components, Euler characteristic) gives H(Y|O)=0 on the census; the strong-collapse core does (it is the nerve up to homotopy) and is small for positives. Residual (V,E,Tr): 0.0052 bit balanced."]
open(os.path.join(R, "report.md"), "w").write("\n".join(L)); print("\n".join(L))

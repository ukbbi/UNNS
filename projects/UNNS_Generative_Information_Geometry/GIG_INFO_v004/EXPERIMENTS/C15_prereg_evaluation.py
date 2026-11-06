"""C15 -- evaluation of the SYM-6 pre-registration (THEORY/PREREGISTRATION.md)."""
import json, os
import _path
R = os.path.join(_path.ROOT, "RESULTS")
s = json.load(open(os.path.join(R, "C12_summary.json")))
out = {"SYM6_distinct_systems": s["distinct_masks"], "SYM6_positives_beta2": s["positives_beta2"], "SYM6_positives_beta1": s["positives_beta1"],
       "T1": "UNTESTABLE (registered condition >=50 beta2-positive systems not met: %d)" % s["positives_beta2"], "T2": "UNTESTABLE (no beta2-positive systems)", "T3": "UNTESTABLE (no beta2-positive systems)",
       "note": "No prediction was falsified; none could be tested. The stress sample (508,680 distinct systems, seed 20261112, not registered) also has no system with beta_2>0, beta_3>0 or beta_4>0."}
json.dump(out, open(os.path.join(R, "C15_prereg_evaluation.json"), "w"), indent=1)
print(out)

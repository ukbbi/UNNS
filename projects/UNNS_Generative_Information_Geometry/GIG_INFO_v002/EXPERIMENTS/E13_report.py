import json, os
import _path
R = json.load(open(os.path.join(_path.ROOT, "RESULTS", "E11_equal_count_pairs.json")))
P = json.load(open(os.path.join(_path.ROOT, "CERTIFICATES", "pair_480_800.json")))
L = ["# GIG-INFO v002 report", "", "Domain: 346,859 six-label regimes; Y=1[beta2>0]; 158 positives.",
     "Equal-N cross pairs: %d; same-content pairs: %d (%d positives)." % (R["cross_pairs_equal_N_different_Y"], R["same_content_pairs_equal_N_different_Y"], R["positives_with_a_same_content_partner"]), "",
     "| ensemble | level | classes | mixed | H(Y|O) bits |", "|---|---|---|---|---|"]
for e, v in R["ensembles"].items():
    for lev, x in v.items():
        L.append("| %s | %s | %d | %d | %s |" % (e, lev, x["classes"], x["mixed_classes"], x["H(Y|O)"][:12]))
L += ["", "Positives still sharing signature with an equal-N negative: %s" % R["positives_vs_negatives_remaining"], "",
      "Certified pair: content %s, sources %d (beta2=1) and %d (beta2=0), N=%d both; f-vectors %s vs %s." % (P["content"], P["pair"]["positive_source"], P["pair"]["negative_source"], P["positive"]["N"], P["positive"]["f_vector"], P["negative"]["f_vector"])]
open(os.path.join(_path.ROOT, "RESULTS", "report.md"), "w").write("\n".join(L) + "\n")

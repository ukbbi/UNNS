import json, os
import _path
R = os.path.join(_path.ROOT, "RESULTS")
J = lambda n: json.load(open(os.path.join(R, n)))
e, f13, f18, w = J("H21_evaluation.json"), J("F13_distinct_masks.json"), J("F18_unresolved66.json"), J("F14_sharp_witness.json")
L = ["# GIG-INFO v003 report", "", "## 66 positives unresolved by (N,h1): positives resolved by adding one scalar", "", "| scalar | resolved | still colliding |", "|---|---|---|"]
for k, v in sorted(f18.items(), key=lambda kv: -kv[1]["resolved"]):
    L.append("| %s | %d | %d |" % (k, v["resolved"], v["still_colliding"]))
L += ["", "## sharp witness pairs", "equal (N,h1): %(positive_negative_pairs)d pairs, %(positives_involved)d positives, same-content pairs %(same_content_pairs)d" % w["equal_N_h1"],
      "equal (N,h1,hq): %(positive_negative_pairs)d pairs, %(positives_involved)d positives, same-content pairs %(same_content_pairs)d" % w["equal_N_h1_hq"], "",
      "## held-out H6 (pre-registered)", "", "| signature | mixed classes H6 | positives hidden H6 | mixed classes D u H6 | positives hidden D u H6 |", "|---|---|---|---|---|"]
for n in e["H6_alone"]:
    a, b = e["H6_alone"][n], e["D_union_H6"][n]
    L.append("| %s | %d | %d | %d | %d |" % (n, a["mixed_classes"], a["positives_in_mixed"], b["mixed_classes"], b["positives_in_mixed"]))
L += ["", "P1 confirmed: %s (S_A failed); P2 confirmed: %s" % (e["P1_confirmed"], e["P2_confirmed"]), "", "## H7 seven-label (exploratory, 11 positives)", ""]
for n, v in e["H7_alone_exploratory"].items():
    L.append("- %s: mixed classes %d, positives hidden %d" % (n, v["mixed_classes"], v["positives_in_mixed"]))
open(os.path.join(R, "report.md"), "w").write("\n".join(L) + "\n")

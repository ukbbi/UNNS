import json, os
import _path
R = os.path.join(_path.ROOT, "RESULTS")
J = lambda n: json.load(open(os.path.join(R, n)))
b10, b11, a12, a13, a15, c11, c14 = J("B10_information_profiles.json"), J("B11_out_of_sample.json"), J("A12_scope_hierarchy.json"), J("A13_collision_concordance.json"), J("A15_stronger_signatures.json"), J("C11_symbolic_information.json"), J("C14_beta1_transfer.json")
L = ["# GIG-INFO v004 report", "", "## B. exact information profiles (bits) for Y=1[beta2>0]", ""]
for dom in ("D", "D_union_H6"):
    for mode in ("natural", "balanced"):
        L += ["### %s, %s ensemble (H(Y)=%s)" % (dom, mode, b10[dom][mode]["none"]["H(Y)"][:9]), "", "| observation | H(Y|O) | I(Y;O) | classes | mixed |", "|---|---|---|---|---|"]
        for o, p in b10[dom][mode].items():
            L.append("| %s | %s | %s | %d | %d |" % (o, p["H(Y|O)"][:9], p["I(Y;O)"][:9], p["classes"], p["mixed_classes"]))
        L.append("")
L += ["## B. out-of-sample (balanced test ensemble)", ""]
for t, v in b11.items():
    L += ["### " + t, "", "| model | recovered bits | balanced acc | AUC |", "|---|---|---|---|"]
    for k, x in v["gradient_boosting"].items():
        L.append("| %s | %s | %s | %s |" % (k, x["information_recovered_bits"], x["balanced_accuracy"], x["AUC"]))
    x = v["exact_signature_lookup_with_backoff"]
    L += ["| exact lookup | %s | %s | - |" % (x["information_recovered_bits"], x["balanced_accuracy"]), ""]
L += ["## A. scope of (Q,S2) sufficiency", "", "| class | systems | positives | (Q,S2) mixed/hidden | (N,h1,Q,S2) mixed/hidden | (N,h1,h2) mixed |", "|---|---|---|---|---|---|"]
for tag in ("PF", "VS"):
    L.append("| %s | %d | %d | %d/%d | %d/%d | %d |" % (tag, a12[tag]["distinct_systems"], a12[tag]["positives"], a12[tag]["(Q,S2)"]["mixed_classes"], a12[tag]["(Q,S2)"]["positives_hidden"], a15[tag]["(N,h1,Q,S2)"]["mixed_classes"], a15[tag]["(N,h1,Q,S2)"]["positives_hidden"], a15[tag]["(N,h1,h2)"]["mixed_classes"]))
L += ["| arithmetic (D u H6) | 609983 | 290 | 0/0 | 0/0 | 0 |", "", "## C. symbolic grammar", "", "primary: %(systems)d systems, beta2 positives %(positives)d" % c11["primary_Y2"], "beta1 transfer:"]
for t, v in c14.items():
    L.append("- %s: " % t + ", ".join("%s mixed %d (hidden %d)" % (k, x["mixed_classes"], x["positives_hidden"]) for k, x in v.items() if isinstance(x, dict)))
open(os.path.join(R, "report.md"), "w").write("\n".join(L) + "\n")

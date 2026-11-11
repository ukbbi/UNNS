#!/usr/bin/env python3
"""Turn the verification report into LaTeX macros/tables so the manuscript quotes computed values only."""
import json
import sys
from fractions import Fraction

rep = json.load(open(sys.argv[1]))
out_dir = sys.argv[2]
ck = {c["id"]: c for c in rep["checks"]}

v6 = ck["V6"]["result"]
v8 = ck["V8"]["result"]["fast"]
v4 = ck["V4"]
mean = Fraction(v6["mean"])
res6 = sorted(int(k) for k in v6["d6_by_residue_mod_24"])
M = []
M.append(r"\newcommand{\NMAX}{%d}" % v6["range"][1])
M.append(r"\newcommand{\CountSix}{%d}" % v6["count_d6"])
M.append(r"\newcommand{\MeanD}{%.2f}" % float(mean))
M.append(r"\newcommand{\ReplayMax}{%d}" % v4["cases"])
M.append(r"\newcommand{\TotalCases}{%d}" % rep["total_cases"])
M.append(r"\newcommand{\DSixResidues}{%s}" % ", ".join(str(r) for r in res6))
M.append(r"\newcommand{\BallAThree}{%d}" % v8["radii_3_2"]["size_a"])
M.append(r"\newcommand{\BallBTwo}{%d}" % v8["radii_3_2"]["size_b"])
M.append(r"\newcommand{\BallBThree}{%d}" % v8["radii_3_3"]["size_b"])
M.append(r"\newcommand{\MeetThree}{%d}" % v8["radii_3_3"]["intersection"])
M.append(r"\newcommand{\FirstSix}{%s}" % ", ".join(str(n) for n in v6["first_d6"][:8]))
M.append(r"\newcommand{\VerSha}{%s}" % rep["verifier_sha256"][:16])
open(f"{out_dir}/numbers.tex", "w").write("\n".join(M) + "\n")

# distribution table
dist = v6["distribution"]
lines = [r"\begin{tabular}{@{}lrrrr@{}}", r"\toprule",
         r"$d(n,n+1)$ & " + " & ".join(f"${k}$" for k in sorted(dist, key=int)) + r" \\",
         r"count & " + " & ".join(str(dist[k]) for k in sorted(dist, key=int)) + r" \\",
         r"\bottomrule", r"\end{tabular}"]
# adjust column spec to number of columns
ncol = len(dist)
lines[0] = r"\begin{tabular}{@{}l" + "r" * ncol + r"@{}}"
open(f"{out_dir}/distribution_table.tex", "w").write("\n".join(lines) + "\n")

# checks table
claims = {
    "V1": "closed-form edge test equals the definition",
    "V2": "exact symbolic certificates for the nine identities",
    "V3": "coverage of all residues modulo 24; special paths for $n=1,3$",
    "V4": "plain-integer replay of every identity with edge test",
    "V5": "constructive connectivity paths (context)",
    "V6": "exact distance table, consistency with identity lengths",
    "V7": "independent engine reproduces distances",
    "V8": "lower-bound certificate at $n=163$, two engines",
    "V9": "trivial lower bound $d(n,n+1)\\ge 2$",
}
L = [r"\begin{tabular}{@{}llrl@{}}", r"\toprule", r"check & what it tests & cases & result \\ \midrule"]
for cid in ["V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9"]:
    c = ck[cid]
    L.append(rf"{cid} & {claims[cid]} & {c['cases']} & {'pass' if c['passed'] else 'FAIL'} \\")
L += [r"\bottomrule", r"\end{tabular}"]
open(f"{out_dir}/checks_table.tex", "w").write("\n".join(L) + "\n")
print("numbers written")

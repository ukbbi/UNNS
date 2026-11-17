"""Run every UNNS-SCALE-I gate, check the numbers quoted in THEORY, write the report."""
import json, os, subprocess, sys, hashlib, time
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.join(here, "..")
res_dir = os.path.join(root, "results")
steps = ["run_gate1.py", "run_gate2.py", "run_gate3.py", "run_witness.py"]
status = {}
for s in steps:
    t = time.time()
    p = subprocess.run([sys.executable, os.path.join(here, s)], cwd=here, capture_output=True, text=True)
    status[s] = {"exit": p.returncode, "seconds": round(time.time() - t, 1)}

g1 = json.load(open(os.path.join(res_dir, "gate1.json")))
g2 = json.load(open(os.path.join(res_dir, "gate2.json")))
g3 = json.load(open(os.path.join(res_dir, "gate3_distance.json")))
w = json.load(open(os.path.join(res_dir, "witness_paths.json")))

# numbers quoted in THEORY_v001.md
q = {}
q["e(10^12)=644932606630"] = g2["claims"]["G2f_edge_count_formula"]["e(10^12)"] == 644932606630
q["e(10^6)=643494"] = g2["claims"]["G2f_edge_count_formula"]["e(10^6)"] == 643494
q["deg(10^6)=64, exits=63"] = (g2["claims"]["G2c_worked_example_1e6"]["deg(1e6)"] == 64 and
                              g2["claims"]["G2c_worked_example_1e6"]["exits_from_scaled_copy"] == 63)
q["mean exits 18.9/49.7/87.3/260.2"] = [round(g2["claims"]["G2b_local_boundary_law"][k]["mean_exits"], 1)
                                        for k in ("10", "100", "1000", "1000000")] == [18.9, 49.7, 87.3, 260.2]
q["strict counts 155/120/159/128/83"] = [g3["runs"][k]["stable_strict (scaled < base)"] for k in ("2", "3", "6", "10", "100")] == [155, 120, 159, 128, 83]
q["stable pairs 394/394/297/295/151"] = [g3["runs"][k]["stable_pairs"] for k in ("2", "3", "6", "10", "100")] == [394, 394, 297, 295, 151]
q["certified d(1,2)=5, d(7,8)=4"] = (w["certificates"]["d(1,2)"]["=> exact distance"] == 5 and w["certificates"]["d(7,8)"]["=> exact distance"] == 4)
q["witness paths legal"] = all(v["legal"] for k, v in w.items() if isinstance(v, dict) and "legal" in v)
q["d(163,164)=6"] = g3["sanity_d_163_164_trunc1.2e7"] == 6

allok = all(v["exit"] == 0 for v in status.values()) and all(q.values()) and g1["PASS"] and g2["PASS"] and g3["PASS"]

rep = ["# UNNS-SCALE-I Verification Report v001", "",
       f"Overall: **{'PASS' if allok else 'FAIL'}**", "", "## Scripts", "| script | exit | seconds |", "|---|---|---|"]
rep += [f"| {k} | {v['exit']} | {v['seconds']} |" for k, v in status.items()]
rep += ["", "## Gate verdicts", f"- Gate 1 (representation): {'PASS' if g1['PASS'] else 'FAIL'}",
        f"- Gate 2 (scale embedding, boundary law, obstruction, edge counts): {'PASS' if g2['PASS'] else 'FAIL'}",
        f"- Gate 3 slice (distance non-expansion, no T2 violation): {'PASS' if g3['PASS'] else 'FAIL'}",
        "- Gate 4 (complexity): NOT STARTED", "", "## Numbers quoted in THEORY re-checked against result files"]
rep += [f"- {'OK ' if v else 'MISMATCH'} {k}" for k, v in q.items()]
rep += ["", "## Scope notes",
        "- Gate 3 base distances are truncation-stable upper bounds; only d(1,2)=5 and d(7,8)=4 are exactly certified (untruncated lower bounds).",
        "- Gate 3 strict-shortcut frequencies are experimental.",
        "- Frozen releases were not re-run; only definitions and the single value d(163,164)=6 were used as reference.",
        "- No file in the UNNS GitHub repository was changed; nothing was published."]
open(os.path.join(root, "reports", "VERIFICATION_REPORT_v001.md"), "w").write("\n".join(rep) + "\n")

# integrity sums for the whole project
proj = os.path.abspath(os.path.join(root, ".."))
lines = []
for d, _, fs in sorted(os.walk(proj)):
    for f in sorted(fs):
        if f == "SHA256SUMS.txt" or f.endswith(".pyc"): continue
        p = os.path.join(d, f)
        lines.append(f"{hashlib.sha256(open(p, 'rb').read()).hexdigest()}  {os.path.relpath(p, proj).replace(os.sep, '/')}")
open(os.path.join(proj, "SHA256SUMS.txt"), "w").write("\n".join(lines) + "\n")
print("PASS" if allok else "FAIL"); print(json.dumps(q, indent=1)); sys.exit(0 if allok else 1)

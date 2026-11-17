"""Run all v002 parts, re-check numbers quoted in THEORY v002, check that v001 is unchanged, write report."""
import json, os, subprocess, sys, hashlib, time
sys.dont_write_bytecode = True
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.abspath(os.path.join(here, ".."))
res = os.path.join(root, "results"); proj = os.path.abspath(os.path.join(root, ".."))
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
status = {}
for s in ["run_A_boundary.py", "run_B_composition.py", "run_C_information.py", "run_W_window.py"]:
    t = time.time()
    p = subprocess.run([sys.executable, os.path.join(here, s)], cwd=here, capture_output=True, text=True, env=env)
    status[s] = {"exit": p.returncode, "seconds": round(time.time() - t, 1)}
L = lambda n: json.load(open(os.path.join(res, n)))
A, B, C, W = L("A_boundary.json"), L("B_composition.json"), L("C_information.json"), L("W_window.json")

q = {}
a2 = A["claims"]["A2_asymptotic_mean"]
q["c_B-1 for B=10^6 equals 22.2"] = abs(a2["1000000"]["leading_coeff_c_B_minus_1"] - 22.2) < 1e-9
q["slope(10^6) within 0.01 of 22.2"] = abs(a2["1000000"]["observed_slope_last_two_X"] - 22.2) < 0.01
q["A2 total error < 0.01 at X=4e6 for all B"] = all(abs(v["rows"][-1]["total_err"]) < 0.01 for v in a2.values())
q["A2 table values (mean at 4e6: 27.9522, 39.5917, 160.9865, 126.4490, 379.7874)"] = [round(a2[k]["rows"][-1]["mean_eps"], 4) for k in ("10", "12", "360", "1000", "1000000")] == [27.9522, 39.5917, 160.9865, 126.449, 379.7874]
q["A1 zero mismatches, 13 B values"] = len(A["claims"]["A1_closed_form_vs_enumeration"]) == 13 and all(v["mismatches"] == 0 for v in A["claims"]["A1_closed_form_vs_enumeration"].values())
q["B1 zero mismatches, 9 pairs"] = B["claims"]["B1_additivity"]["mismatches"] == 0 and len(B["claims"]["B1_additivity"]["pairs"]) == 9
q["B2 zero mismatches, 9 chains"] = B["claims"]["B2_level_stratification"]["mismatches"] == 0 and len(B["claims"]["B2_level_stratification"]["chains"]) == 9
ch = B["claims"]["B2_level_stratification"]["chains"]
q["10^12 profiles 153,63,1 / 112,72,32,1"] = ch["1000000x1000000"]["profile_at_x=1"] == [153, 63, 1] and ch["10000x10000x10000"]["profile_at_x=1"] == [112, 72, 32, 1]
q["C: threshold 10 for 10^6; 9 steps not injective; 10 injective"] = C["claims"]["C4_B=10^6"]["t_needed"] == 10 and not C["claims"]["C4_B=10^6"]["9_steps_injective"] and C["claims"]["C4_B=10^6"]["10_steps_injective"]
q["C: C1 formula mismatches 0"] = C["claims"]["C1_formula_mismatches"] == 0
w1 = W["claims"]["W1_vertex_10^6"]; w12 = W["claims"]["W1_vertex_10^12"]; t = W["claims"]["W4_trillion_window"]
q["W: 10^6 has 63 infinite exits, 62 in window; beyond-window neighbour 1000002000001"] = w1["exits_infinite"] == 63 and w1["exits_in_window"] == 62 and w1["lost_beyond_window"][0][2] == 1000002000001
q["W: vertex 10^12 deg 217, window degree 48 (15 in-lattice + 33 exits)"] = w12["deg_infinite"] == 217 and w12["exits_in_window"] == 33 and sum(1 for x in w12["lost_beyond_window"]) == 217 - 48
q["W: trillion table 10^6 (643,494 / 20,054,629)"] = t["1000000"]["both"] == 643494 and t["1000000"]["exactly_one"] == 20054629
q["W: trillion table 10^3 (644,887,919 / 6,193,421,292)"] = t["1000"]["both"] == 644887919 and t["1000"]["exactly_one"] == 6193421292
q["W: trillion table 10^4 (64,478,820 / 1,128,650,367)"] = t["10000"]["both"] == 64478820 and t["10000"]["exactly_one"] == 1128650367
q["W: infinite exit total 349,007,877; lost 328,953,248"] = t["10^6_infinite_exit_total"] == 349007877 and t["10^6_lost_exits_beyond_window"] == 328953248
from math import isqrt
e = lambda Lm: sum(Lm // (m * m) for m in range(2, isqrt(Lm) + 1))
q["W: 'both' = e(floor(L/B)) for the three trillion rows"] = all(t[str(Bv)]["both"] == e(10**12 // Bv) for Bv in (10**3, 10**4, 10**6))
q["W: edge-class closed form equals brute force (8 pairs)"] = len(W["claims"]["W2_edge_classes_vs_brute"]) == 8 and all(v["equal"] for v in W["claims"]["W2_edge_classes_vs_brute"].values())

# v001 integrity: read-only comparison with its own checksum list
v1_status = "v001 checksum list not found"; v1_ok = None
sums = os.path.join(proj, "SHA256SUMS.txt")
if os.path.exists(sums):
    bad = []
    for line in open(sums):
        h, name = line.strip().split("  ", 1)
        p = os.path.join(proj, name)
        if not os.path.exists(p) or hashlib.sha256(open(p, "rb").read()).hexdigest() != h:
            bad.append(name)
    v1_ok = not bad; v1_status = "all v001 files match ../SHA256SUMS.txt" if v1_ok else "DIFFERENT: " + ", ".join(bad)
lib_same = None
v1lib = os.path.join(proj, "UNNS-SCALE-I", "code", "scale_lib.py")
mine = hashlib.sha256(open(os.path.join(here, "scale_lib.py"), "rb").read()).hexdigest()
if os.path.exists(v1lib): lib_same = hashlib.sha256(open(v1lib, "rb").read()).hexdigest() == mine

allok = all(v["exit"] == 0 for v in status.values()) and all(q.values()) and all(x["PASS"] for x in (A, B, C, W)) and (v1_ok in (True, None))
rep = ["# UNNS-SCALE-I v002 Verification Report", "", f"Overall: **{'PASS' if allok else 'FAIL'}**", "",
       "## Scripts", "| script | exit | seconds |", "|---|---|---|"] + [f"| {k} | {v['exit']} | {v['seconds']} |" for k, v in status.items()]
rep += ["", "## Part verdicts"] + [f"- Part {n}: {'PASS' if x['PASS'] else 'FAIL'}" for n, x in zip("ABCW", (A, B, C, W))]
rep += ["- Part D (distance supremum): not started", "- Gate 4: deferred", "", "## Numbers quoted in THEORY v002 re-checked against result files"]
rep += [f"- {'OK ' if v else 'MISMATCH'} {k}" for k, v in q.items()]
rep += ["", "## Baseline protection", f"- v001: {v1_status}", f"- scale_lib.py identical to v001 copy: {lib_same}", f"- scale_lib.py sha-256: {mine}",
        "", "## Scope notes",
        "- The asymptotic law (A4) is proved; the sieve measurements are numerical confirmation up to X = 4,000,000.",
        "- Theorem C concerns deterministic exact reproduction of one move's outer trajectory; it makes no claim about approximate or stochastic models.",
        "- Trillion-window rows come from the proved edge-class formula (checked against brute force at smaller (L, B)); no trillion-scale enumeration was performed.",
        "- No GitHub changes; nothing published."]
open(os.path.join(root, "reports", "VERIFICATION_REPORT_v002.md"), "w").write("\n".join(rep) + "\n")
lines = []
for d, _, fs in sorted(os.walk(root)):
    for f in sorted(fs):
        if f == "SHA256SUMS_v002.txt" or f.endswith(".pyc") or "__pycache__" in d: continue
        p = os.path.join(d, f); lines.append(f"{hashlib.sha256(open(p, 'rb').read()).hexdigest()}  {os.path.relpath(p, root).replace(os.sep, '/')}")
open(os.path.join(root, "SHA256SUMS_v002.txt"), "w").write("\n".join(lines) + "\n")
print("PASS" if allok else "FAIL"); [print(("OK " if v else "XX "), k) for k, v in q.items()]; print(v1_status); sys.exit(0 if allok else 1)

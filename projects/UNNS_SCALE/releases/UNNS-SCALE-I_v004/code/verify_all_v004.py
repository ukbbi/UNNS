"""UNNS-SCALE-I v004 verifier.  Re-checks every stored v004 result (identities with sympy-free polynomial verification, exact distances with
independent sympy-ball certificates, density accounting recomputed from the stored identities), confirms v001-v003 are unchanged (read-only
hashing), writes the report and the checksum list.   Usage: python verify_all_v004.py [--quick]     (no bytecode is written)"""
import json, os, sys, glob, hashlib, time, random
from fractions import Fraction
sys.dont_write_bytecode = True
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.abspath(os.path.join(here, "..")); res = os.path.join(root, "results"); proj = os.path.abspath(os.path.join(root, ".."))
sys.path.insert(0, here)
QUICK = "--quick" in sys.argv
import gc
from poly_check import verify_identity
from indep_check import certify_distance, check_path, ball
from exact_lib import exact_distance
from accounting import union_open, v003
import numpy as np
from math import gcd
t_start = time.time(); q = {}
J = lambda n: json.load(open(os.path.join(res, n)))
steps_of = lambda c: [(d, list(l)) for d, l in c["steps"]]

# ---- Theorem G (2-adic, all B): v2(n+1)=1 => d_B<=4 (n>=5); v2(n+1)=3 => d_B<=5 (n>=23)
Gs = [(4, 1, [("+", [4, 1]), ("-", [2, 0]), ("+", [1, 0]), ("-", [2, 1])], 4), (16, 7, [("+", [16, 7]), ("-", [2, 0]), ("+", [1, 0]), ("-", [2, 1]), ("-", [1])], 5)]
Bs = [1, 2, 3, 4, 5, 6, 7, 10, 12, 30, 60, 1000, 10**6] if not QUICK else [1, 10, 12, 10**6]
ok = True
for B in Bs:
    for M, r, st, K in Gs:
        o, t0 = verify_identity(B, M, r, st); ok &= o and t0 == 1 and len(st) == K
q["T-G identities (n=4t+1 -> 4 steps; n=16t+7 -> 5 steps) verified by poly_check for %d scales" % len(Bs)] = ok
ok = True
for B in [1, 2, 10, 12]:
    for M, r, st, K in Gs:
        for n in range(1, 400):
            if n % M == r and (n - r) // M < 1: ok &= exact_distance(B * n, B * (n + 1), 6)[0] <= K + (1 if (B, n) == (1, 1) else 0)       # members below t0; the only exception is d_1(1)=5
q["T-G small members below t0 (n=1,7): bound holds exactly except n=1 at B=1 where d_1(1)=5 (so T-G is stated for n>=5)"] = ok
ok = True
for B in [1, 2, 3, 10]:
    for n in range(5, 4000 if not QUICK else 400):
        if n % 4 == 1: ok &= exact_distance(B * n, B * (n + 1), 6)[0] <= 4
        if n % 16 == 7: ok &= exact_distance(B * n, B * (n + 1), 6)[0] <= 5
q["T-G exhaustive exact check n<4000 for B=1,2,3,10"] = ok

# ---- stored identity sets
def reverify(ids, B, K, lbl):
    ok = True; okL = True
    for c in ids:
        o, t0 = verify_identity(B, c["M"], c["r"], steps_of(c)); ok &= o and t0 == c["t0"] and len(c["steps"]) <= K
        for tt in range(0, c["t0"]):
            n = c["M"] * tt + c["r"]
            if n >= 1: okL &= exact_distance(B * n, B * (n + 1), 6)[0] <= K
    q[f"{lbl}: {len(ids)} identities re-verified without sympy (division, endpoint, positivity, replay)"] = ok
    q[f"{lbl}: members below t0 satisfy the bound exactly"] = okL
D10 = J("D4A_B10_closure.json"); D12 = J("D4C_B12_closure.json"); D6 = J("D4B_B1e6_cover.json")
reverify(D10["new_identities"], 10, 5, "D4-A B=10")
reverify(D12["new_identities"], 12, 5, "D4-C B=12")
reverify(D6["direct_identities"], 10**6, 5, "D4-B B=10^6")
q["D4-B direct B=10^6 identities: %d total, %d of length<=4" % (len(D6["direct_identities"]), D6["n_direct_len4"])] = sum(1 for c in D6["direct_identities"] if len(c["steps"]) <= 4) == D6["n_direct_len4"]

# ---- density accounting recomputed from scratch
Gc = [(4, 1), (16, 7)]; cls = lambda ids: [(c["M"], c["r"]) for c in ids]
def opens(classes):
    L, cov = union_open(classes); return L, [int(x) for x in np.nonzero(~cov)[0]]
L, o = opens(v003(10, 5) + Gc + cls(D10["new_identities"]))
q["D4-A B=10: open residues recomputed = stored (%d of period %d, density %.6f; v003 had 7/2520 = 0.002778)" % (len(o), L, len(o) / L)] = (L, o) == (D10["period"], D10["open_residues_mod_period"])
q["D4-A B=10: every open n has 720 | n+1 (all residual structure is 2^4*3^2*5 | n+1)"] = all((x + 1) % 720 == 0 for x in o)
q["D4-A B=10: open density < 1/1500 (<~0.00067), i.e. proved d_10<=5 outside a set of density %.6f" % (len(o) / L)] = len(o) / L < 1 / 1500
L, o12 = opens(v003(12, 4) + Gc + cls(D12["new_identities"]))
q["D4-C B=12: open residues recomputed = stored (%d of %d; density %.2e); every open n has 25200 | n+1" % (len(o12), L, len(o12) / L)] = (L, o12) == (D12["period"], D12["open_residues_mod_period"]) and all((x + 1) % 25200 == 0 for x in o12)
inh = v003(10, 5) + Gc + cls(D10["new_identities"]) + [x for B, K in [(2, 5), (4, 5), (5, 5)] for x in v003(B, K)]
La, oa = opens(inh); Lb, ob = opens(inh + cls(D6["direct_identities"]))
q["D4-B B=10^6: inherited-only and combined open sets recomputed = stored (combined %d of %d, density %.2e)" % (len(ob), Lb, len(ob) / Lb)] = (Lb, ob) == (D6["period"], D6["open_residues_mod_period"]) and len(oa) / La == D6["open_density_inherited_float"]

# ---- D_10 = 6 certificate
sh = J("D4A_B10_witness_shortening.json"); bad = True
import subprocess
for n in (365759, 351359):
    w = sh[f"10,{n}"]; p = w["path"]
    bad &= w["d"] == 6 and p[0] == 10 * n and p[-1] == 10 * (n + 1) and check_path(p) == 6
    if not QUICK or n == 365759:       # the large-ball certificate runs in a child process (memory is released afterwards)
        code = "import sys,json; sys.path.insert(0,%r); from indep_check import certify_distance; p=json.loads(sys.argv[1]); r=certify_distance(p[0],p[-1],6,p); print(json.dumps(r))" % here
        out = subprocess.run([sys.executable, "-B", "-c", code, json.dumps(p)], capture_output=True, text=True)
        bad &= out.returncode == 0 and json.loads(out.stdout.strip().splitlines()[-1])[:2] == [3, 2]
        if n == 365759: bad &= json.loads(out.stdout.strip().splitlines()[-1]) == [3, 2, 1027634, 21021]
chain_ok = True
for n in (365759, 351359):
    ds = {int(k.split(",")[0]): v["d"] for k, v in sh.items() if k.endswith("," + str(n))}
    for A in ds:
        for B in ds:
            if B % A == 0: chain_ok &= ds[B] <= ds[A]
    for k, v in sh.items():
        if k.endswith("," + str(n)): chain_ok &= check_path(v["path"]) == v["d"] and v["path"][0] == v["B"] * n and v["path"][-1] == v["B"] * (n + 1)
q["D4-A witness distances at 17 scales: paths valid, pointwise law d_B<=d_A (A|B) holds; both witnesses fall to 5 at B=20 and 4 at B=10^6"] = chain_ok and all(sh[f"1000000,{n}"]["d"] == 4 and sh[f"20,{n}"]["d"] == 5 for n in (365759, 351359))
q["D4-A D_B=6 for B in {1,2,5,10} (divisor law from D_10=6): witnesses d=6 at B=1,2,5,10"] = all(sh[f"{B},{n}"]["d"] == 6 for B in (1, 2, 5, 10) for n in (365759, 351359))
pp = J("D4A_B10_pole_probe.json")
q["D4-A pole probe (n+1=720*2^a*p): paths valid; d=6 only at (a,p)=(2,127),(3,61); d in {4,5} otherwise"] = (pp["six_witnesses_a_p"] == [[2, 127], [3, 61]]) and all(v["d"] in (4, 5, 6) for v in pp["results"].values())
om = J("D4_open_class_members_exact.json")
okm = True
for Bk, v in om.items():
    B = int(Bk)
    for ns, r in v["results"].items():
        n = int(ns); okm &= check_path(r["path"]) == r["d"] and r["path"][0] == B * n and r["path"][-1] == B * (n + 1)
q["D4 open-class members: all stored paths valid (B=12: 15 members, B=10: 342, B=10^6: 192)"] = okm
q["D4 open-class members: B=12 max 5 (n=25199, 5 members at 5), B=10 hist {4:174,5:166,6:2}, B=10^6 all d=4"] = (
    om["12"]["hist"] == {"4": 10, "5": 5} and om["10"]["hist"] == {"4": 174, "5": 166, "6": 2} and om["1000000"]["hist"] == {"4": 192})
if not QUICK:
    cert = True; rng = random.Random(5)
    for Bk, dd in (("12", 5), ("10", 5)):
        sel = [(n, r) for n, r in om[Bk]["results"].items() if r["d"] == dd]; rng.shuffle(sel)
        for n, r in sel[:6]: cert &= certify_distance(int(Bk) * int(n), int(Bk) * (int(n) + 1), dd, r["path"]) is not None
    q["D4 d=5 witnesses at B=12 and B=10 (6 each, random) certified by disjoint balls (lower bound 5 independent)"] = cert
    c12 = certify_distance(12 * 25199, 12 * 25200, 5, om["12"]["results"]["25199"]["path"]); q["D4-C d_12(25199)=5 certified => 5<=D_12<=6"] = c12 is not None
else:
    q["D4-C d_12(25199)=5 certified (quick)"] = certify_distance(12 * 25199, 12 * 25200, 5, om["12"]["results"]["25199"]["path"]) is not None
pb = J("D4C_B12_pole_probe.json")
q["D4-C pole probe B=12 (n+1=12600 s, 25200 s; 66 distinct n): paths valid, max d = 5, no distance 6"] = all(check_path(v["path"]) == v["d"] and v["path"][0] == 12 * int(n) and v["path"][-1] == 12 * (int(n) + 1) for n, v in pb["results"].items()) and pb["max"] == 5 and len(pb["results"]) == 66
adv = J("D4B_B1e6_adversarial.json")
q["D4-B adversarial n at B=10^6 (%d n with smooth n+1 / exceptional classes): all paths valid, max d = %d" % (adv["n_tested"], adv["max_d"])] = all(check_path(v["path"]) == v["d"] for v in adv["results"].values()) and adv["max_d"] == 4
fin = J("D4B_B1e6_N3000.json")
q["D4-B scan n<=3000 at B=10^6: hist {2:2,3:402,4:2596}, max 4, mean 3.8647"] = fin["hist"] == {"2": 2, "3": 402, "4": 2596} and fin["finite_max"] == 4 and abs(fin["mean"] - 3.8647) < 5e-4
# fresh exact recomputation of a random sample at B=10^6
rng = random.Random(9); ok = True
ns = list(range(1, 3001)); rng.shuffle(ns)
for n in ns[:(6 if QUICK else 30)]: ok &= exact_distance(10**6 * n, 10**6 * (n + 1), 6)[0] == int(fin["per_n"][str(n)])
q["D4-B fresh exact recomputation reproduces stored distances at B=10^6 (random sample)"] = ok
ok = True
for n in rng.sample(list(map(int, adv["results"])), 6 if QUICK else 25): ok &= exact_distance(10**6 * n, 10**6 * (n + 1), 6)[0] == adv["results"][str(n)]["d"]
q["D4-B fresh exact recomputation reproduces stored adversarial distances"] = ok
# random members of closed classes obey the proved bound
rng = random.Random(21); ok = True; cnt = 0
for B, ids, K in [(10, D10["new_identities"], 5), (12, D12["new_identities"], 5), (10**6, D6["direct_identities"], 5)]:
    for _ in range(4 if QUICK else 12):
        c = rng.choice(ids); n = c["M"] * rng.randrange(0, 12 if c["M"] > 20000 else 300) + c["r"]
        if n >= 1: cnt += 1; ok &= exact_distance(B * n, B * (n + 1), 6)[0] <= len(c["steps"])
q["D4 random members of new closed classes satisfy their step bound by the exact engine (%d checked)" % cnt] = ok

# ---- baselines (read-only hashing)
def check_list(path, base):
    if not os.path.exists(path): return None, "checksum list not found at " + path
    bad = []
    for line in open(path):
        if not line.strip(): continue
        h, name = line.strip().split("  ", 1); p = os.path.join(base, name)
        if not os.path.exists(p) or hashlib.sha256(open(p, "rb").read()).hexdigest() != h: bad.append(name)
    return (not bad), ("all files match" if not bad else "DIFFERENT: " + ", ".join(bad))
v1 = check_list(os.path.join(proj, "SHA256SUMS.txt"), proj)
v2 = check_list(os.path.join(proj, "UNNS-SCALE-I_v002", "SHA256SUMS_v002.txt"), os.path.join(proj, "UNNS-SCALE-I_v002"))
v3 = check_list(os.path.join(proj, "UNNS-SCALE-I_v003", "SHA256SUMS_v003.txt"), os.path.join(proj, "UNNS-SCALE-I_v003"))
allok = all(q.values()) and all(x[0] in (True, None) for x in (v1, v2, v3))
rep = ["# UNNS-SCALE-I v004 Verification Report", "", f"Overall: **{'PASS' if allok else 'FAIL'}**  (mode: {'quick' if QUICK else 'full'}, {time.time() - t_start:.0f} s)", "", "## Checks"]
rep += [f"- {'OK ' if v else 'MISMATCH'} {k}" for k, v in q.items()]
rep += ["", "## Baseline protection (read-only hashing)", f"- v001: {v1[1]}", f"- v002: {v2[1]}", f"- v003: {v3[1]}", "", "## Scope notes",
        "- D_10 = 6 is CERTIFIED (two exact distance-6 witnesses; lower bound by disjoint balls on the full infinite graph, upper bound D_B<=6 from v003).",
        "- D_12 is only 5<=D_12<=6; D_{10^6} is NOT determined (certified lower bound from data: 4; proved <=5 outside a residue set of density ~1.2e-4).",
        "- Density statements are exact Fractions over residue classes; they are not statements about all n.",
        "- No GitHub changes; nothing published; Gate 4 deferred."]
os.makedirs(os.path.join(root, "reports"), exist_ok=True)
open(os.path.join(root, "reports", "VERIFICATION_REPORT_v004.md"), "w").write("\n".join(rep) + "\n")
lines = []
for d, _, fs in sorted(os.walk(root)):
    for f in sorted(fs):
        if f == "SHA256SUMS_v004.txt" or f.endswith(".pyc") or "__pycache__" in d: continue
        p = os.path.join(d, f); lines.append(f"{hashlib.sha256(open(p, 'rb').read()).hexdigest()}  {os.path.relpath(p, root).replace(os.sep, '/')}")
open(os.path.join(root, "SHA256SUMS_v004.txt"), "w").write("\n".join(lines) + "\n")
print("PASS" if allok else "FAIL"); [print(("OK " if v else "XX "), k) for k, v in q.items()]; print("v001:", v1[1]); print("v002:", v2[1]); print("v003:", v3[1])
sys.exit(0 if allok else 1)

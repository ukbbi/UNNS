"""UNNS-SCALE-I v005 verifier.  Part A: the finite-window theorem  max_{1<=n<=999999} d(10^6 n, 10^6 (n+1)) = 4.
Every n in the window is replayed with plain integer arithmetic (no polynomial machinery): identity members, n=1, and the 614 supplied paths;
each step is checked against the edge rule x=kN -> k(N+1)^2.  Lower bound: complete disjoint balls (sympy).  Baselines v001-v004 are only hashed.
Usage: python verify_all_v005.py [--quick]    (no bytecode is written; --quick replays every 50th identity member)"""
import json, os, sys, glob, hashlib, time, subprocess, random
sys.dont_write_bytecode = True
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.abspath(os.path.join(here, "..")); res = os.path.join(root, "results"); proj = os.path.abspath(os.path.join(root, ".."))
sys.path.insert(0, here)
QUICK = "--quick" in sys.argv
from indep_check import check_path, certify_distance
from poly_check import verify_identity
t_start = time.time(); q = {}; B = 10**6; N = 999999
J = lambda n: json.load(open(os.path.join(res, n)))
A = J("A_window_identities_and_n1.json"); U = J("A_window_uncovered_614.json"); ids = A["identities"]
def ev(l, t):
    v = 0
    for c in l: v = v * t + c
    return v
def replay(x, steps, t):
    """returns (final x, max vertex) or None if some step is not a legal edge"""
    mx = x
    for d, l in steps:
        Nn = ev(l, t)
        if Nn < 1: return None
        if d == "+":
            if x % Nn: return None
            x = x // Nn * (Nn + 1) ** 2
        else:
            qq = Nn + 1
            if qq < 2 or x % (qq * qq): return None
            x = x // (qq * qq) * (qq - 1)
        if x > mx: mx = x
    return x, mx
# 1. symbolic identities (independent polynomial check, as in v004)
ok = True
for c in ids:
    o, t0 = verify_identity(B, c["M"], c["r"], [(d, list(l)) for d, l in c["steps"]]); ok &= o and t0 == c["t0"] and len(c["steps"]) <= 4
q["71 symbolic identities of length <=4 re-verified by poly_check (division, positivity, replay): %d" % len(ids)] = ok and len(ids) == 71
# 2. per-n replay of every identity member in the window
cov = bytearray(N + 2); bad = 0; replays = 0; gmax = 0; gmax_n = None; step = 50 if QUICK else 1
for c in ids:
    M, r = c["M"], c["r"]; t = c["t0"]; k = 0
    while M * t + r <= N:
        n = M * t + r
        if n >= 1 and (k % step == 0 or not QUICK):
            out = replay(B * n, c["steps"], t); replays += 1
            if out is None or out[0] != B * (n + 1): bad += 1
            else:
                cov[n] = 1
                if out[1] > gmax: gmax, gmax_n = out[1], n
        elif n >= 1 and QUICK: cov[n] = 1          # quick mode: membership only
        t += 1; k += 1
q["per-n replay: %d identity-member paths replayed with integer arithmetic, all legal and ending at 10^6(n+1) (bad=%d)" % (replays, bad)] = bad == 0

# 2b. cross-check of the replay against the sympy edge rule (indep_check.check_path) on random identity members
def path_of(x, steps, t):
    P = [x]
    for d, l in steps:
        Nn = ev(l, t)
        x = x // Nn * (Nn + 1) ** 2 if d == "+" else x // (Nn + 1) ** 2 * Nn
        P.append(x)
    return P
rng = random.Random(77); ok = True; cnt = 0
for _ in range(60 if QUICK else 400):
    c = rng.choice(ids); tmax = (N - c["r"]) // c["M"]; t = rng.randint(c["t0"], tmax); n = c["M"] * t + c["r"]
    if n < 1: continue
    P = path_of(B * n, c["steps"], t); cnt += 1; ok &= P[0] == B * n and P[-1] == B * (n + 1) and check_path(P) == len(c["steps"])
q["replay cross-checked against the independent sympy edge test on %d random identity members (full 4-step paths)" % cnt] = ok
n1 = A["n1_exact"]; p = n1["path"]
q["n=1: explicit path of length %d (<=4), valid edges, endpoints 10^6 and 2*10^6" % n1["d"]] = check_path(p) == n1["d"] <= 4 and p[0] == B and p[-1] == 2 * B
R = U["results"]; ok = True
for k, v in R.items():
    m = int(k); ok &= check_path(v["path"]) == v["d"] == 4 and v["path"][0] == B * m and v["path"][-1] == B * (m + 1)
q["the %d supplied paths: every step a legal edge, 4 steps, correct endpoints" % len(R)] = ok and len(R) == 614
# 3. partition of the window
cover_set = {n for n in range(1, N + 1) if cov[n]}
unc = {int(k) for k in R}
if not QUICK:
    q["partition: identity members (%d) + {1} + uncovered (%d) = %d = all of 1..999999, pairwise disjoint" % (len(cover_set) - (1 in cover_set), len(unc), N)] = (
        (cover_set - {1}) & unc == set() and ((cover_set - {1}) | {1} | unc) == set(range(1, N + 1)) and 1 not in unc and len(cover_set - {1}) == 999384 and len(unc) == 614)
else:
    q["partition (quick: membership by residue class; counts only)"] = len(cover_set - {1}) + 1 + len(unc) == N
# 4. lower bound
lb = {}
cert_src = os.path.join(proj, "UNNS-SCALE-I_v004", "results", "D4B_B1e6_N3000.json")
c4 = json.load(open(cert_src))["certificates"]
ok = True
for n_ in ("11", "13"):
    cc = certify_distance(B * int(n_), B * (int(n_) + 1), c4[n_]["d"], c4[n_]["path"]); ok &= c4[n_]["d"] == 4 and cc[0] == 2 and cc[1] == 1
    lb[n_] = cc
q["lower bound: d(10^6 n,10^6(n+1)) = 4 at n=11 and n=13 (disjoint complete balls radii 2,1; sizes %s and %s)" % (lb["11"][2:], lb["13"][2:])] = ok and lb["11"][2:] == (23582, 146) and lb["13"][2:] == (24585, 128)
# 5. excursion statistics (ambient, not induced)
mx614 = max(max(v["path"]) for v in R.values()); mx = max(gmax, mx614, max(p))
q["ambient excursion: largest vertex on any window path = %.3e (identity paths %.3e, supplied paths %.3e): exceeds 10^12 -> ambient-graph theorem" % (mx, gmax, mx614)] = mx > 10**12
thmA = all(q.values()); q["THEOREM A: every n in 1..999999 has d<=4 and d=4 occurs  =>  M_{10^6} = 4 (conjunction of all Part A checks above)"] = thmA

# ---- Part B (exploratory) -- records only; none of these checks is used for Theorem A
from math import gcd
from exact_lib import exact_distance
from sympy import factorint
newk4 = J("B_new_K4_identities.json"); okb = True
for c in newk4:
    o, t0 = verify_identity(B, c["M"], c["r"], [(d, list(l)) for d, l in c["steps"]]); okb &= o and t0 == c["t0"] and len(c["steps"]) <= 4
q["Part B: %d additional K<=4 identities at B=10^6 re-verified by poly_check" % len(newk4)] = okb and len(newk4) == 55
import numpy as np
nn = np.arange(N + 1); vv = np.zeros(N + 1, bool); vv[0] = True
for c in ids + newk4: vv |= (nn % c["M"] == c["r"] % c["M"]) & ((nn - c["r"]) // c["M"] >= c["t0"])
rest = {int(x) for x in np.nonzero(~vv)[0]}
q["Part B: with the 55 new identities the window has %d values of n outside all identity classes (of the 614+1), a subset of the 614 supplied paths" % len(rest)] = len(rest) == 407 and rest <= (unc | {1})
g = 0; sm = 0; shp = {}
for k, v in R.items():
    m = int(k) + 1; g = gcd(g, m); f = factorint(m); sm += all(pp in (2, 3, 5, 7) for pp in f)
    sh = "".join("+" if b > a else "-" for a, b in zip(v["path"], v["path"][1:])); shp[sh] = shp.get(sh, 0) + 1
q["Part B: the 614 exceptional n: gcd(n+1)=180, %d have 7-smooth n+1, path shapes %s (no single shape)" % (sm, dict(sorted(shp.items())))] = g == 180 and sm == 80 and shp == {"++--": 80, "+---": 5, "+--+": 5, "+-+-": 524}
S = J("B_outside_window_scan.json")
q["Part B: outside-window exact scan at B=10^6: %d values (720*2^a*p, smooth 720|n+1, random 180|n+1), max d = %d" % (S["tested"], S["max_d"])] = S["tested"] == 299 and S["max_d"] == 4 and all(v["d"] == 4 for v in S["results"].values())
rng2 = random.Random(3); ks = rng2.sample(list(S["results"]), 4 if QUICK else 25); okr = True
for k in ks: okr &= exact_distance(B * int(k), B * (int(k) + 1), 6)[0] == S["results"][k]["d"]
q["Part B: fresh exact recomputation of %d random scan values agrees" % len(ks)] = okr

# 6. baselines (read-only hashing)
def check_list(path, base):
    if not os.path.exists(path): return None, "checksum list not found at " + path
    bad_ = []
    for line in open(path):
        if not line.strip(): continue
        h, name = line.strip().split("  ", 1); pp = os.path.join(base, name)
        if not os.path.exists(pp) or hashlib.sha256(open(pp, "rb").read()).hexdigest() != h: bad_.append(name)
    return (not bad_), ("all files match" if not bad_ else "DIFFERENT: " + ", ".join(bad_))
bl = [check_list(os.path.join(proj, "SHA256SUMS.txt"), proj)] + [check_list(os.path.join(proj, f"UNNS-SCALE-I_v00{i}", f"SHA256SUMS_v00{i}.txt"), os.path.join(proj, f"UNNS-SCALE-I_v00{i}")) for i in (2, 3, 4)]
allok = all(q.values()) and all(x[0] in (True, None) for x in bl)
rep = ["# UNNS-SCALE-I v005 Verification Report (Part A: trillion-window metric theorem)", "", f"Overall: **{'PASS' if allok else 'FAIL'}**  (mode: {'quick' if QUICK else 'full'}, {time.time() - t_start:.0f} s)", "", "## Checks"]
rep += [f"- {'OK ' if v else 'MISMATCH'} {k}" for k, v in q.items()]
rep += ["", "## Baseline protection (read-only hashing)"] + [f"- {n}: {x[1]}" for n, x in zip(["v001", "v002", "v003", "v004"], bl)]
rep += ["", "## Scope", "- Part A is closed: finite window only; endpoints within 10^12, intermediate vertices may exceed it.", "- Part B (D_{10^6} in {4,5,6}) is exploratory: its checks record data only; no universal conclusion is claimed.", "- No GitHub changes; Gate 4 deferred."]
os.makedirs(os.path.join(root, "reports"), exist_ok=True)
open(os.path.join(root, "reports", "VERIFICATION_REPORT_v005.md"), "w").write("\n".join(rep) + "\n")
lines = []
for d, _, fs in sorted(os.walk(root)):
    for f in sorted(fs):
        if f == "SHA256SUMS_v005.txt" or f.endswith(".pyc") or "__pycache__" in d: continue
        pp = os.path.join(d, f); lines.append(f"{hashlib.sha256(open(pp, 'rb').read()).hexdigest()}  {os.path.relpath(pp, root).replace(os.sep, '/')}")
open(os.path.join(root, "SHA256SUMS_v005.txt"), "w").write("\n".join(lines) + "\n")
print("PASS" if allok else "FAIL"); [print(("OK " if v else "XX "), k) for k, v in q.items()]; [print(n, x[1]) for n, x in zip(["v001", "v002", "v003", "v004"], bl)]
sys.exit(0 if allok else 1)

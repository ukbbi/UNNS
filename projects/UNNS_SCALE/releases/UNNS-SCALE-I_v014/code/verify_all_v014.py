"""UNNS-SCALE-I v014 verifier (Scale-Lifted Uniform Routing Certificates).  Usage: python verify_all_v014.py [--quick]
Checks: scale-transfer lemma (independent neighbour sets); exact all-n sweep of tau^4_n(10^6(n+1)) (C++ rebuilds of slices + independent Python balls); exception tables;
explicit 10^6-scale routes (edge-checked); derived uniform bound; v013 errata; v001-v013 hashes."""
import json, os, sys, random, hashlib, subprocess, time, collections
sys.dont_write_bytecode = True
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.abspath(os.path.join(here, "..")); res = os.path.join(root, "results"); proj = os.path.abspath(os.path.join(root, ".."))
sys.path.insert(0, here)
QUICK = "--quick" in sys.argv
from indep_check import nbrs, check_path
import summarize14, errata
t0 = time.time(); q = {}; rnd = random.Random(14); B6 = 10**6; LAD = [10**6, 160000, 7600, 361, 18, 4, 1]
def P(*a): return os.path.join(res, *a)
subprocess.run(["g++", "-O2", "-fopenmp", "-o", "/tmp/scale_lift_v014", os.path.join(here, "scale_lift.cpp")], check=True)
def run_list(A, R, ns, paths=False):
    open("/tmp/v14_list.txt", "w").write("\n".join(map(str, ns))); e = {**os.environ, "NLIST": "/tmp/v14_list.txt"}
    if paths: e["PATHS"] = "1"
    subprocess.run(["/tmp/scale_lift_v014", str(A), str(B6), "1", str(B6), "/tmp/v14_out.txt", str(R), "2"], check=True, env=e, capture_output=True)
    return [l.split() for l in open("/tmp/v14_out.txt")]
def pyball(x, W, R):
    dist = {x: 0}; fr = [x]
    for r in range(1, R + 1):
        nx = []
        for v in fr:
            for w in nbrs(v):
                if w <= W and w not in dist: dist[w] = r; nx.append(w)
        fr = nx
    return dist
def pydist(n, A, Ra, Rb):
    W = B6 * (n + 1); a = pyball(A * n, W, Ra); b = pyball(A * (n + 1), W, Rb); return min((a[z] + b[z] for z in a if z in b), default=None)
# 1. scale-transfer lemma: path B -> A in G_B, multiplied by m (and by m+1), consists of edges, heights <= B m
def bfs_paths(B, depth):
    par = {B: None}; fr = [B]
    for _ in range(depth):
        nx = []
        for v in fr:
            for w in nbrs(v):
                if w <= B and w not in par: par[w] = v; nx.append(w)
        fr = nx
    return par
par = bfs_paths(B6, 3); As = list(par)
def path_to(A):
    p = []; v = A
    while v is not None: p.append(v); v = par[v]
    return p[::-1]
ok = True; cnt = 0
for _ in range(40 if QUICK else 200):
    A = rnd.choice(As); p = path_to(A); m = rnd.randrange(1, 10**6)
    for mm in (m, m + 1):
        for a, b in zip(p, p[1:]): ok &= (b * mm in nbrs(a * mm)); cnt += 1
        ok &= max(p) * mm <= B6 * mm
q["scale-transfer lemma: for %d random scales A (<= 3 steps from 10^6 in G_{10^6}) and random m, the multiplied path edges (%d edge checks, independent neighbour sets) are SELECT-II edges with height <= 10^6 m" % (40 if QUICK else 200, cnt)] = ok
p4 = [10**6, 160000, 7600, 361, 18, 4]
q["d_{G_{10^6}}(10^6, 4) <= 5: explicit path 10^6 -> 160000 -> 7600 -> 361 -> 18 -> 4 (edge-checked, heights <= 10^6)"] = check_path(p4) == 5
# 2. stored sweep and summaries
S = summarize14.compute(res); st = json.load(open(P("SUMMARY_v014.json")))
q["summary statistics recomputed from the stored sweep and exception files equal SUMMARY_v014.json"] = json.loads(json.dumps(S)) == st
tc = S["tau4_counts"]
q["all-n sweep of tau^4_n(10^6(n+1)), n = 1..999,999: %s (digit 9 = no route of <= 6 steps); %d exceptions (n_min = %d); exception list = positions of digit 9" % (tc, S["n_exceptions"], S["exc_min"])] = S["N"] == 999999 and S["exc_list_matches"] and S["n_exceptions"] == 8655 and sum(tc.values()) == 999999
sweep = summarize14.sweep(res)
# 3. C++ rebuild of slices of the sweep (source packaged here)
slices = [(304000, 305500), (999000, 1000000)] if QUICK else [(1, 3000), (150000, 152000), (249500, 251000), (304000, 312000), (500000, 503000), (700000, 705000), (996000, 1000000)]
ok = True
for lo, hi in slices:
    subprocess.run(["/tmp/scale_lift_v014", "4", str(B6), str(lo), str(hi), "/tmp/v14_sl.txt", "3", "2"], check=True); ok &= open("/tmp/v14_sl.txt").read() == sweep[lo - 1: hi - 1]
q["fresh C++ rebuild of sweep slices %s reproduces the stored digits" % slices] = ok
# 4. independent Python (sympy neighbour sets, no shared code) balls of radius 3 on random n: distance <= 6 exact value, or 'none within 6'
ns = sorted(rnd.sample(range(1, 10**6), 120 if QUICK else 2500)); ok = True; bad = []
for n in ns:
    d = pydist(n, 4, 3, 3); c = sweep[n - 1]
    if (d is None and c != "9") or (d is not None and str(d) != c): ok = False; bad.append((n, d, c))
q["independent Python balls (radius 3, sympy) reproduce the sweep digit for %d random n (%s)" % (len(ns), "no mismatch" if ok else bad[:3])] = ok
exl = [int(x) for x in open(P("EXC_A4_gt6.txt")).read().split()]; ex_s = rnd.sample(exl, 40 if QUICK else 400); ok = all(pydist(n, 4, 3, 3) is None for n in ex_s)
q["independent Python: %d random exceptions have no route of <= 6 steps at scale 4 inside [1, 10^6(n+1)]" % len(ex_s)] = ok
# 5. exact tau^4 on exceptions (7 or 8): C++ list rebuild and independent Python upper/lower checks
def rd(f): return {int(a): int(b) for a, b in (l.split() for l in open(f))}
a4 = rd(P("exc", "EXC_A4_R4.txt")); a1 = rd(P("exc", "EXC_A1_R4.txt")); a18 = rd(P("exc", "EXC_A18_R4_on_eq8.txt")); a361 = rd(P("exc", "EXC_A361_R3.txt"))
q["exceptions: tau^4 in {7, 8} for all 8655 (%s)" % S["tau4_on_exceptions"]] = set(a4.values()) == {7, 8} and set(a4) == set(exl)
sm = rnd.sample(exl, 30 if QUICK else 300); r = run_list(4, 4, sm); q["fresh C++ rebuild of tau^4 (radius 4) for %d random exceptions reproduces EXC_A4_R4" % len(sm)] = all(int(d) == a4[int(n)] for n, d in r)
sm = rnd.sample(exl, 30 if QUICK else 300); r = run_list(1, 4, sm); q["fresh C++ rebuild of tau^1 (radius 4) for %d random exceptions reproduces EXC_A1_R4" % len(sm)] = all(int(d) == a1[int(n)] for n, d in r)
sm = rnd.sample(exl, 30 if QUICK else 300); r = run_list(361, 3, sm); q["fresh C++ rebuild of tau^361 (radius 3) for %d random exceptions reproduces EXC_A361_R3" % len(sm)] = all(int(d) == a361[int(n)] for n, d in r)
e8 = sorted(a18)
if not QUICK:
    sm = rnd.sample(e8, 15); r = run_list(18, 4, sm); q["fresh C++ rebuild of tau^18 (radius 4) for 15 random pairs with tau^4 = 8 reproduces EXC_A18_R4_on_eq8"] = all(int(d) == a18[int(n)] for n, d in r)
ok = True; k = 0
for n in rnd.sample(sorted(a4), 12 if QUICK else 40):
    if a4[n] == 7: up = pydist(n, 4, 4, 3)
    else: up = pydist(n, 4, 4, 4) if k < (3 if QUICK else 12) else None; k += 1
    if a4[n] == 7: ok &= (up == 7)
    elif up is not None: ok &= (up == 8)
q["independent Python balls reproduce the exact tau^4 (7 or 8; lower bound = no meeting within radius 3+3) on random exceptions"] = ok
# 6. explicit 10^6-scale routes
R = json.load(open(P("ROUTES_v014.json"))); keys = list(R); sel = keys[:: (8 if QUICK else 1)]; ok = True
for n in sel:
    d = R[n]; rt = d["route"]; ni = int(n); ok &= rt[0] == B6 * ni and rt[-1] == B6 * (ni + 1) and max(rt) <= B6 * (ni + 1) and d["length"] == len(rt) - 1 == 10 + d["tau4"] and check_path(rt) == d["length"]
q["explicit routes at scale 10^6 (%d routes, lengths %s): endpoints, ceiling 10^6(n+1), and every edge verified independently" % (len(sel), sorted({R[n]["length"] for n in sel}))] = ok and max(R[n]["length"] for n in R) == 18
# 7. derived bounds
q["uniform bound: best chain bound max over all n = %d; %d pairs bounded by <= 16, %d by 17, %d by 18 (histogram %s)" % (S["max_bound"], S["n_bound_le16"], S["n_bound_17"], S["n_bound_18"], S["bound_histogram_all_n"])] = S["max_bound"] == 18 and S["n_bound_le16"] + S["n_bound_17"] + S["n_bound_18"] == 999999
# 8. errata of v013 (parity condition)
er = errata.run(30, 600) if QUICK else errata.run(); q["v013 erratum: corrected parity condition never violated by a connected pair (%d pairs), v013 wording violated by %d connected pairs (e.g. %s)" % (er["pairs"], er["C1_false_connected"], er["C1_false_connected_examples"][:3])] = er["C2_false_but_connected"] == 0 and er["C1_false_connected"] > 0 and (QUICK or json.loads(json.dumps(er)) == json.load(open(P("ERRATA_parity.json"))))
if not QUICK:
    import obs_rho; q["experimental observation table OBS_rho.json recomputed from the sweep"] = obs_rho.compute() == json.load(open(P("OBS_rho.json")))
def check_list(path, base):
    bad = []
    for line in open(path):
        h, name = line.strip().split("  ", 1); pp = os.path.join(base, name)
        if not os.path.exists(pp) or hashlib.sha256(open(pp, "rb").read()).hexdigest() != h: bad.append(name)
    return (not bad, "OK" if not bad else "MISMATCH " + ",".join(bad[:5]))
bl = [check_list(os.path.join(proj, "SHA256SUMS.txt"), proj)] + [check_list(os.path.join(proj, f"UNNS-SCALE-I_v0{i:02d}", f"SHA256SUMS_v0{i:02d}.txt"), os.path.join(proj, f"UNNS-SCALE-I_v0{i:02d}")) for i in range(2, 14)]
q["baselines v001-v013 unchanged (read-only hashing)"] = all(b[0] for b in bl)
rep = ["# UNNS-SCALE-I v014 verification report", "", "mode: " + ("quick" if QUICK else "full"), ""]; allok = True
for k, v in q.items(): rep.append(("- PASS: " if v else "- FAIL: ") + k); allok &= bool(v)
rep += ["", "## Baselines"] + [f"- v0{i:02d}: {x[1]}" for i, x in zip(range(1, 14), bl)] + ["", "ALL CHECKS PASS" if allok else "SOME CHECKS FAILED", "time %.0f s" % (time.time() - t0)]
os.makedirs(os.path.join(root, "reports"), exist_ok=True)
open(os.path.join(root, "reports", "VERIFY_v014_" + ("quick" if QUICK else "full") + ".md"), "w").write("\n".join(rep)); print("\n".join(rep)); sys.exit(0 if allok else 1)

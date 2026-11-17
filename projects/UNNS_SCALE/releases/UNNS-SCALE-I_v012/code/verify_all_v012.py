"""UNNS-SCALE-I v012 verifier (Length-Height Trade-off and Arithmetic Routing).  Usage: python verify_all_v012.py [--quick]
Checks: exact bottleneck-DP frontier rebuilt by the C++ engine; independent Python bidirectional BFS re-derives staircase points;
structural checks over every stored frontier (monotone staircase, parity bound, floor = B(n+1)); ladder distances (C++ re-run, Python cross-check, v010 cross-check);
reduction-transfer lemma; law fits; explicit shortest routes; v001-v011 hashes."""
import json, os, sys, random, hashlib, subprocess, time, math
sys.dont_write_bytecode = True
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.abspath(os.path.join(here, "..")); res = os.path.join(root, "results"); proj = os.path.abspath(os.path.join(root, ".."))
sys.path.insert(0, here)
QUICK = "--quick" in sys.argv
from frontier_io import read_frontier, read_ladder, qn
from hubpath import route
from indep_check import check_path
import law_fit
t0 = time.time(); q = {}; rnd = random.Random(12); B6 = 10**6
def sh(*a, **k): return subprocess.run(list(a), check=True, capture_output=True, text=True, **k).stdout
def P(f): return os.path.join(res, f)
subprocess.run(["g++", "-O2", "-fopenmp", "-o", "/tmp/tau_v012", os.path.join(here, "tau_exact.cpp")], check=True)
subprocess.run(["g++", "-O2", "-o", "/tmp/ladder_v012", os.path.join(here, "ladder.cpp")], check=True)
F = {"100": read_frontier(P("F100.txt")), "1000": read_frontier(P("F1000.txt")), "10000": read_frontier(P("F10000.txt")),
     "1e6": {**read_frontier(P("F1e6_n1_99.txt")), **read_frontier(P("F1e6_n100_199.txt"))}, "9": read_frontier(P("F9_n1_99.txt"))}
Bof = {"100": 100, "1000": 1000, "10000": 10**4, "1e6": B6, "9": 9}
# 1. rebuild exact frontiers with the C++ engine
def rebuild(B, Cmax, n1, n2, st, f, stop=None, th=2):
    a = ["/tmp/tau_v012", str(B), str(Cmax), str(n1), str(n2), str(st), "/tmp/rb.txt"] + ([str(stop)] if stop else [])
    subprocess.run(a, check=True, capture_output=True, env={**os.environ, "OMP_NUM_THREADS": str(th)}); return open("/tmp/rb.txt").read() == open(P(f)).read()
q["fresh C++ rebuild of the exact bottleneck frontier, B=100, n=1..99, Cmax=10^7, reproduces F100.txt byte for byte"] = rebuild(100, 10**7, 1, 99, 1, "F100.txt")
q["fresh C++ rebuild, B=9, n=1..99, Cmax=10^7, reproduces F9_n1_99.txt"] = rebuild(9, 10**7, 1, 99, 1, "F9_n1_99.txt")
if not QUICK:
    q["fresh C++ rebuild, B=1000, n=1..999 (all window pairs of the scaled analogue), Cmax=10^7, reproduces F1000.txt"] = rebuild(1000, 10**7, 1, 999, 1, "F1000.txt")
    q["fresh C++ rebuild, B=10^4, n=7,207,...,9807, Cmax=10^8, reproduces F10000.txt"] = rebuild(10**4, 10**8, 7, 9999, 200, "F10000.txt")
    q["fresh C++ rebuild, B=10^6, n=1..99, Cmax=10^8, reproduces F1e6_n1_99.txt"] = rebuild(B6, 10**8, 1, 99, 1, "F1e6_n1_99.txt")
    q["fresh C++ rebuild, B=999 to ceiling 10^6(n+1), n=1..99, Cmax=10^8, reproduces F999_for1e6_n1_99.txt"] = rebuild(999, 10**8, 1, 99, 1, "F999_for1e6_n1_99.txt", stop=10**6)
# 2. structural checks over every stored frontier
ok = True; npts = 0; floor_ok = True; par_ok = True
for k, D in F.items():
    B = Bof[k]
    for n, (pts, fl) in D.items():
        ls = [l for l, h in pts]; hs = [h for l, h in pts]; npts += len(pts)
        ok &= all(a < b for a, b in zip(ls, ls[1:])) and all(a > b for a, b in zip(hs, hs[1:])) and hs[-1] >= B * (n + 1)
        if fl == "*": floor_ok &= hs[-1] == B * (n + 1)
        par_ok &= all(h >= (qn(n) + 1) ** 2 or h >= B * (n + 1) and False for h in hs[-1:]) or hs[-1] >= (qn(n) + 1) ** 2
        par_ok &= all(h >= (qn(n) + 1) ** 2 for h in hs)
q["all %d stored frontier points: lengths strictly increase, heights strictly decrease, final height >= B(n+1)" % npts] = ok
q["every row flagged * reaches exactly the floor B(n+1): connection ceiling kappa = B(n+1) (scaled analogues B=9?,100,1000,10^4,10^6)".replace("9?,", "")] = floor_ok and all(fl == "*" for k in ("100", "1000", "10000", "1e6") for _, (pts, fl) in F[k].items())
q["parity bound (v011): every frontier height >= (q(n)+1)^2 for all stored rows"] = par_ok
# 3. independent Python re-derivation of staircase points
def tau_py(a, b, C, rmax=9, cap=2500000):
    p = route(a, b, C, rmax=rmax, cap=cap)
    return None if p is None else (len(p) - 1, p)
def indep(k, ns, ths):
    B = Bof[k]; ok = True; cnt = 0
    for n in ns:
        pts, fl = F[k][n]
        for i, (l, h) in enumerate(pts):
            r = tau_py(B * n, B * (n + 1), h)
            if r is None: continue          # cap exceeded: skipped (not counted)
            cnt += 1; ok &= r[0] == l and max(r[1]) <= h and bool(check_path(r[1]))
            if i + 1 < len(pts):
                r2 = tau_py(B * n, B * (n + 1), h - 1)
                if r2 is not None: cnt += 1; ok &= r2[0] == pts[i + 1][0]
    return ok, cnt
ns100 = rnd.sample(sorted(F["100"]), 6 if QUICK else 25); ok, c = indep("100", ns100, None)
q["independent Python bidirectional BFS reproduces %d staircase facts (distance at ceiling H_i equals l_i, at H_i-1 equals l_{i+1}) on B=100" % c] = ok and c > 0
ns1000 = rnd.sample([n for n in sorted(F["1000"]) if n < 400], 4 if QUICK else 15); ok, c = indep("1000", ns1000, None)
q["independent Python BFS reproduces %d staircase facts on B=1000" % c] = ok and c > 0
ns6 = [5, 16, 21, 23, 28, 5] if QUICK else [5, 16, 21, 23, 28, 29, 37, 40, 100, 127, 160]
ok = True; c = 0
for n in ns6:
    pts, fl = F["1e6"][n]; r = tau_py(B6 * n, B6 * (n + 1), B6 * (n + 1), rmax=7, cap=2000000)
    if r: c += 1; ok &= r[0] == pts[-1][0] and max(r[1]) == B6 * (n + 1) and bool(check_path(r[1]))
q["independent Python BFS reproduces the exact confined distance tau_n(kappa) at B=10^6 for %d pairs" % c] = ok and c > 0
# 4. ladder
L = read_ladder(P("LAD_B6_a.txt"), P("LAD_B6_b.txt"), P("LAD_E1.txt"))
mono = True
by = {}
for (n, W), v in L.items(): by.setdefault(n, []).append((W, v))
for n, lst in by.items():
    ex = sorted((W, v) for W, v in lst if isinstance(v, int)); mono &= all(a[1] >= b[1] for a, b in zip(ex, ex[1:]))
    lb = [(W, v[1]) for W, v in lst if isinstance(v, tuple)]
    mono &= all(all(not (W2 >= W and isinstance(v2, int) and v2 < 0) for W2, v2 in lst) for W, _ in lb)
q["ladder (%d (n,W) records): exact distance is non-increasing in the ceiling W for each n" % len(L)] = mono
# re-run C++ ladder on a sample of stored lines
sample = rnd.sample([k for k, v in L.items() if isinstance(v, int) and v <= 8], 6 if QUICK else 25); ok = True
for n, W in sample:
    if os.path.exists("/tmp/lad_chk.txt"): os.remove("/tmp/lad_chk.txt")
    sh("/tmp/ladder_v012", str(B6), "8", "2500000", "/tmp/lad_chk.txt", str(n), str(W)); ok &= int(open("/tmp/lad_chk.txt").read().split()[2]) == L[(n, W)]
q["fresh C++ ladder re-run reproduces %d stored exact distances (B=10^6)" % len(sample)] = ok
# v010 cross check: window distance at 10^12
P1 = [tuple(map(int, l.split())) for l in open(os.path.join(proj, "UNNS-SCALE-I_v010", "results", "P1_window_distance_sample.txt"))]
P1 = [t for t in P1 if 0 <= t[2] <= 5][: (6 if QUICK else 20)]; ok = True
for t in P1:
    if os.path.exists("/tmp/lad_chk.txt"): os.remove("/tmp/lad_chk.txt")
    sh("/tmp/ladder_v012", str(B6), "8", "2500000", "/tmp/lad_chk.txt", str(t[0]), str(10**12)); ok &= int(open("/tmp/lad_chk.txt").read().split()[2]) == t[2]
q["v012 ladder at ceiling 10^12 reproduces the v010 window distances d_W for %d sampled pairs" % len(P1)] = ok
# 5. reduction transfer
def tau_of(pts, C):
    for l, h in pts:
        if h <= C: return l
    return None
viol = 0; tot = 0
for n, (pts, fl) in F["100"].items():
    for l, h in pts:
        t9 = tau_of(F["9"][n][0], h)
        if t9 is not None: tot += 1; viol += l > t9 + 2
R = read_frontier(P("F999_for1e6_n1_99.txt")); viol2 = 0; sl = []
for n, (pts, fl) in R.items():
    t = tau_of(pts, B6 * (n + 1)); ex = F["1e6"][n][0][-1][0]; viol2 += ex > t + 2; sl.append(t + 2 - ex)
q["reduction-transfer lemma tau^{Q^2}_n(C) <= tau^{Q-1}_n(C)+2: B=100 vs 9 (%d exact checks, %d violations); B=10^6 vs 999 (99 pairs, %d violations, slack 0..%d)" % (tot, viol, viol2, max(sl))] = viol == 0 and viol2 == 0
# reduction bounds for larger n (supplementary upper bounds tau^{10^6}_n(kappa) <= tau^{999}_n(Cmax=10^8) + 2)
HI = {}
for l in open(P("F999_hi.txt")):
    r = l.split(); HI[int(r[0])] = ([tuple(map(int, x.split(":"))) for x in r[1:] if ":" in x], r[-1])
ok = True; cnt = 0
for n in sorted(HI)[: (3 if QUICK else 8)]:
    if not HI[n][0]: continue
    sh("/tmp/tau_v012", "999", "100000000", str(n), str(n), "1", "/tmp/one.txt", "1000000"); ok &= open("/tmp/one.txt").read().strip() == (str(n) + " " + " ".join("%d:%d" % t for t in HI[n][0]) + " " + HI[n][1]); cnt += 1
    ex = L.get((n, B6 * (n + 1)))
    if isinstance(ex, int): ok &= ex <= HI[n][0][0][0] + 2
q["reduction-based upper bounds tau^{10^6}_n(kappa) <= tau^999_n + 2 for larger n: %d recomputed by C++, never below the exact ladder value where known" % cnt] = ok
# 6. law fits
S = law_fit.compute(res); st = json.load(open(P("FIT_summary.json")))
q["law fits (tau_n(kappa) ~ a + b ln q(n)) recomputed: %s" % "; ".join("%s: R2=%.2f" % (k[:14], v["R2"]) for k, v in S.items() if isinstance(v, dict))] = S == st and all(v["R2"] > 0.5 for v in S.values() if isinstance(v, dict))
# 7. explicit shortest routes
E = json.load(open(P("SR1.json"))); ok = True
for n, d in E.items():
    p = d["path"]; ok &= p[0] == B6 * int(n) and p[-1] == B6 * (int(n) + 1) and max(p) == B6 * (int(n) + 1) and len(p) - 1 == d["length"] == (F["1e6"][int(n)][0][-1][0] if int(n) in F["1e6"] else L[(int(n), B6 * (int(n) + 1))]) and bool(check_path(p))
q["explicit exact-shortest confined routes (n=%s; lengths %s; minimum vertices %s): edge-checked, length equals the exact DP value, max = B(n+1)" % (",".join(E), [d["length"] for d in E.values()], [d["min_vertex"] for d in E.values()])] = ok
# 8. exact shortest vs v011 hub routes
E1 = json.load(open(os.path.join(proj, "UNNS-SCALE-I_v011", "results", "E1_explicit_routes.json"))); LE = read_ladder(P("LAD_E1.txt")); ok = True; cmp_ = []
for n, p in E1.items():
    ex = LE[(int(n), B6 * (int(n) + 1))]; ok &= isinstance(ex, int) and ex <= len(p) - 1; cmp_.append((len(p) - 1, ex))
q["v011 hub routes vs exact shortest confined distance (hub length, exact): %s -- exact never exceeds the hub route" % cmp_] = ok
def check_list(path, base):
    bad = []
    for line in open(path):
        h, name = line.strip().split("  ", 1); pp = os.path.join(base, name)
        if not os.path.exists(pp) or hashlib.sha256(open(pp, "rb").read()).hexdigest() != h: bad.append(name)
    return (not bad, "OK" if not bad else "MISMATCH " + ",".join(bad[:5]))
bl = [check_list(os.path.join(proj, "SHA256SUMS.txt"), proj)] + [check_list(os.path.join(proj, f"UNNS-SCALE-I_v0{i:02d}", f"SHA256SUMS_v0{i:02d}.txt"), os.path.join(proj, f"UNNS-SCALE-I_v0{i:02d}")) for i in range(2, 12)]
q["baselines v001-v011 unchanged (read-only hashing)"] = all(b[0] for b in bl)
rep = ["# UNNS-SCALE-I v012 verification report", "", "mode: " + ("quick" if QUICK else "full"), ""]; allok = True
for k, v in q.items():
    rep.append(("- PASS: " if v else "- FAIL: ") + k); allok &= bool(v)
rep += ["", "## Baselines"] + [f"- v0{i:02d}: {x[1]}" for i, x in zip(range(1, 12), bl)] + ["", "ALL CHECKS PASS" if allok else "SOME CHECKS FAILED", "time %.0f s" % (time.time() - t0)]
os.makedirs(os.path.join(root, "reports"), exist_ok=True)
open(os.path.join(root, "reports", "VERIFY_v012_" + ("quick" if QUICK else "full") + ".md"), "w").write("\n".join(rep)); print("\n".join(rep)); sys.exit(0 if allok else 1)

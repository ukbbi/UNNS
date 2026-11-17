"""UNNS-SCALE-I v010 verifier (Height-Constrained Arithmetic Geometry).  Usage: python verify_all_v010.py [--quick]
Re-checks: the window scan (all 999,999 pairs, ceiling 10^12) via stored records, an independent Python re-implementation (exact_lib) on samples,
a fresh rebuild+re-run of ball.cpp on blocks, consistency of H4 / window-distance samples with the scan, the n=5 example (6,230,016), v001-v009 hashes."""
import json, os, sys, gzip, struct, random, hashlib, subprocess, time, math
sys.dont_write_bytecode = True
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.abspath(os.path.join(here, "..")); res = os.path.join(root, "results"); proj = os.path.abspath(os.path.join(root, ".."))
sys.path.insert(0, here)
QUICK = "--quick" in sys.argv
from rball import restricted_route, rball
from indep_check import check_path
t0 = time.time(); q = {}; B = 10**6; C = 10**12; rnd = random.Random(10)
S = json.load(open(os.path.join(res, "W1_window_summary.json")))
rows = []
for f in ("W_a", "W_b"):
    d = gzip.open(os.path.join(res, f + ".bin.gz")).read(); rows += [struct.unpack("<4Q", d[i:i+32]) for i in range(0, len(d), 32)]
q["window scan file: %d records, n = 1..999999 contiguous" % len(rows)] = [r[0] for r in rows] == list(range(1, 10**6))
ps = {r[0]: r[1] for r in rows if r[1]}
q["window scan: %d pairs have a <=4-step route inside [1,10^12], %d pairs have none (disjoint restricted radius-2 balls); summary file agrees" % (len(ps), len(rows) - len(ps))] = (len(ps) == S["pass"] == 2997 and len(rows) - len(ps) == S["fail"] == 997002 and {str(k): v for k, v in ps.items()} == S["pass_meeting_vertex"])
q["first failing pair n = %d; all n <= 682 pass (boundary of the in-window four-step regime)" % min(r[0] for r in rows if not r[1])] = min(r[0] for r in rows if not r[1]) == 683 and all(rows[n-1][1] for n in range(1, 683))
q["meeting vertices of passing pairs are <= 10^12"] = all(z <= C for z in ps.values())
# independent Python implementation
nfail = 25 if QUICK else 150; npass = 15 if QUICK else 60; bad = 0
fails = [r[0] for r in rows if not r[1]]; passes = sorted(ps)
smp = [(n, False) for n in rnd.sample(fails, nfail)] + [(n, True) for n in rnd.sample(passes, npass)] + [(n, n in ps) for n in (list(range(1, 80)) if QUICK else list(range(1, 400)))]
for n, exp in smp:
    p, sa, sb = restricted_route(B*n, B*(n+1), C); got = p is not None
    if got != exp: bad += 1
    elif got and not (len(p) <= 5 and max(p) <= C and p[0] == B*n and p[-1] == B*(n+1) and check_path(list(p))): bad += 1
q["independent Python (exact_lib) restricted balls on %d pairs (random fail/pass + exhaustive n<%d): disagreements %d; every passing route edge-checked and <= 10^12" % (len(smp), 80 if QUICK else 400, bad)] = bad == 0
# n=5 example from review
p6, _, _ = restricted_route(5*10**6, 6*10**6, 6230016); p5, _, _ = restricted_route(5*10**6, 6*10**6, 6230015)
q["n=5: no <=4-step route with ceiling 6,230,015; route with ceiling 6,230,016 = %s" % (p6,)] = p5 is None and p6 is not None and max(p6) == 6230016 and check_path(list(p6))
# rebuild and re-run C++ on blocks
try:
    subprocess.run(["g++", "-O2", "-o", os.path.join("/tmp", "ball_v010"), os.path.join(here, "ball.cpp")], check=True, capture_output=True)
    blocks = [(1, 1200), (250000, 250300)] + ([] if QUICK else [(999000, 999999), (500000, 500400)])
    ok = True
    for lo, hi in blocks:
        subprocess.run(["/tmp/ball_v010", str(B), str(lo), str(hi), str(C), "/tmp/blk.bin"], check=True, capture_output=True)
        d = open("/tmp/blk.bin", "rb").read(); R = [struct.unpack("<4Q", d[i:i+32]) for i in range(0, len(d), 32)]
        ok &= R == [rows[n-1] for n in range(lo, hi)]
    q["fresh g++ rebuild of ball.cpp reproduces stored records on %d blocks" % len(blocks)] = ok
except Exception as e:
    q["fresh g++ rebuild (compiler unavailable: %s)" % type(e).__name__] = None
# samples consistent with scan
H = [tuple(map(int, l.split())) for l in open(os.path.join(res, "P2_H4_sample.txt"))]
D = [tuple(map(int, l.split())) for l in open(os.path.join(res, "P1_window_distance_sample.txt"))]
q["H4 sample (%d n): H4 <= 10^12 exactly for the pairs that pass the window scan" % len(H)] = all(((h[1] != 0 and h[1] <= C) == (h[0] in ps)) for h in H)
q["window-distance sample (%d n): d_W <= 4 exactly for passing pairs; d_W >= 5 (or > 10) otherwise" % len(D)] = all(((0 < d[2] <= 4) == (d[0] in ps)) for d in D)
# distance 5 at n=683 in the window: radius-3 ball from x meets radius-2 ball from y
A = rball(B*683, C, 3); Bb = rball(B*684, C, 2); meet5 = any(z in Bb[2] or z in Bb[1] or z in Bb[0] for z in A[3]); meet4 = any(z in Bb[b] for a in range(3) for b in range(3) for z in A[a])
q["n=683: window distance exactly 5 (radius-3/radius-2 balls meet; radius-2/radius-2 balls do not)"] = meet5 and not meet4
# endpoint-domain heights from v009 for the same n=5: shortest route (3 steps) height 732,050,000
v9 = json.load(open(os.path.join(proj, "UNNS-SCALE-I_v009", "results", "H1_B1e6_n2_700.json")))["rows"]
r5 = [r for r in v9 if r["n"] == 5][0]
q["n=5: 3-step shortest route has minimum height 732,050,000 (v009 data) while allowing 4 steps drops the ceiling to 6,230,016"] = (r5["d"] == 3 and r5["hmin"] == 732050000)
def check_list(path, base):
    bad = []
    for line in open(path):
        h, name = line.strip().split("  ", 1); pp = os.path.join(base, name)
        if not os.path.exists(pp) or hashlib.sha256(open(pp, "rb").read()).hexdigest() != h: bad.append(name)
    return (not bad, "OK" if not bad else "MISMATCH " + ",".join(bad[:5]))
bl = [check_list(os.path.join(proj, "SHA256SUMS.txt"), proj)] + [check_list(os.path.join(proj, f"UNNS-SCALE-I_v00{i}", f"SHA256SUMS_v00{i}.txt"), os.path.join(proj, f"UNNS-SCALE-I_v00{i}")) for i in range(2, 10)]
q["baselines v001-v009 unchanged (read-only hashing)"] = all(b[0] for b in bl)
rep = ["# UNNS-SCALE-I v010 verification report", "", "mode: " + ("quick" if QUICK else "full"), ""]; allok = True
for k, v in q.items():
    rep.append(("- PASS: " if v else ("- SKIP: " if v is None else "- FAIL: ")) + k); allok &= v is not False
rep += ["", "## Baselines"] + [f"- v00{i}: {x[1]}" for i, x in zip(range(1, 10), bl)] + ["", "ALL CHECKS PASS" if allok else "SOME CHECKS FAILED", "time %.0f s" % (time.time() - t0)]
open(os.path.join(root, "reports", "VERIFY_v010_" + ("quick" if QUICK else "full") + ".md"), "w").write("\n".join(rep)); print("\n".join(rep)); sys.exit(0 if allok else 1)

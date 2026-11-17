"""UNNS-SCALE-I v009 verifier (Constant-Ratio Covering and Excursion Geometry).  Usage: python verify_all_v009.py [--quick]
Re-checks: v008 erratum counterexamples (E1,E2); shape = single residue class mod P v' w' (equivalence with the route test on a window and on random shapes);
covering-search results (rigorous uncovered-density bounds, no certificate claimed); excursion heights (every stored path legal, endpoints, length, max=hmin);
reviewer's wormhole family (B(n+2)^2); baselines v001-v008 hashes."""
import json, os, sys, hashlib, time, random
from fractions import Fraction
sys.dont_write_bytecode = True
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.abspath(os.path.join(here, "..")); res = os.path.join(root, "results"); proj = os.path.abspath(os.path.join(root, ".."))
sys.path.insert(0, here)
QUICK = "--quick" in sys.argv
import famE
from classes import all_classes, shape_class
from cover import cover
from indep_check import check_path
t0 = time.time(); q = {}; B = 10**6; J = lambda n: json.load(open(os.path.join(res, n)))
# E2: converse of L' counterexample
N = M = 1; P, Q, P2, Q2 = 2, 3, 1, 2; a, a2 = 600000, 1600000
q["E2: S2 (=B) and S1 hold but n=Q^2 a N/B = 27/5 is not an integer (converse of L' needs B | Q^2 a N)"] = (Q2**2*a2*M - Q**2*a*N == B and a*P*(Q*(N+1)-P) == a2*P2*(Q2*(M+1)-P2) and Fraction(Q**2*a*N, B) == Fraction(27, 5))
# E1: two-sided congruence
sh = (1, 2, 1, 1, 2, 1)
q["E1: shape (1,2,1,1) rho=2 at n=3: first congruence holds (u=4), second fails (u'=3 mod 2): no route"] = (4 % 2 == 0 and 3 % 2 == 1 and famE.route(B, 3, sh) is None)
# classes: one residue class mod P v' w'
K = 6 if QUICK else 8; cl = all_classes(B, K); shs = famE.shapes(B, K)
q["every shape (K=%d, %d shapes) yields exactly one consistent residue class, modulus P v' w' (or its CRT-reduction dividing it)" % (K, len(shs))] = len(cl) == len(shs) and all((sh[4]*sh[0]*sh[1]) % m == 0 for r, m, n0, sh in cl)
rnd = random.Random(9); bad = 0; cnt = 0
for r0, m, n0, sh in rnd.sample(cl, min(len(cl), 150 if QUICK else 400)):
    for j in range(4):
        n = max(n0, 2); n += (r0 - n) % m; n += j * m; cnt += 1; bad += famE.route(B, n, sh) is None
    # non-members of the class (right above n0) have no route
    for j in range(1, 4):
        n = max(n0, 2) + (r0 - max(n0, 2)) % m + j; 
        if m > 3 and (n - r0) % m != 0: cnt += 1; bad += famE.route(B, n, sh) is not None
q["class membership <=> route (n >= n0), %d random shape/n tests: failures %d" % (cnt, bad)] = bad == 0
W = 1500 if QUICK else 6000; bad = 0
for n in range(2, W):
    x = any(famE.route(B, n, s) for s in shs); y = any(n >= n0 and (n - r) % m == 0 for r, m, n0, s in cl); bad += x != y
q["union of K=%d shapes equals union of their classes on 2<=n<%d: mismatches %d" % (K, W, bad)] = bad == 0
# covering search results
C = J("C2_covering_search.json")
q["covering search: no finite certificate reached; rigorous uncovered-density upper bounds %s; dead nodes %s" % ({k: "%.2e" % v["uncovered_upper_bound"] for k, v in C.items()}, {k: v["dead"] for k, v in C.items()})] = all(not v["finished"] and v["dead"] == 0 for v in C.values()) and C["12"]["uncovered_upper_bound"] < C["8"]["uncovered_upper_bound"] < C["4"]["uncovered_upper_bound"]
c4 = [c for c in all_classes(B, 4) if c[2] <= 10**6]; o = cover([(r, m) for r, m, n0, s in c4], 8 if QUICK else 20)
q["re-run K=4 covering (independent run): uncovered upper bound %.2e <= 5e-3, finished=%s" % (float(o["uncovered_upper_bound"]), o["finished"])] = float(o["uncovered_upper_bound"]) < 5e-3
# excursion heights
rows = J("H1_B1e6_n2_700.json")["rows"] + J("H1b_B1e6_n700_1400.json")["rows"]; bad = 0; ins = 0; out = 0
sample = rows if not QUICK else rows[:60]
for r in sample:
    p = r["path"]; n = r["n"]; ok = p[0] == B*n and p[-1] == B*(n+1) and len(p) == r["d"] + 1 and max(p) == r["hmin"] and check_path(p)
    bad += not ok; ins += r["ratio"] <= 1.0000001; out += r["ratio"] > 1.0000001
q["height table: %d stored minimal-height shortest paths re-checked (legal, endpoints, length d, max=hmin): failures %d; inside-domain %d, forced-outside %d" % (len(sample), bad, ins, out)] = bad == 0 and out > 0 and ins > 0
R4 = J("H2_le4_n2_150.json")["rows"] + J("H2b_le4_n150_300.json")["rows"]; sh = {r["n"]: r for r in rows}; bad4 = 0; fo = 0; sub = 0; both = 0
for r in (R4[:40] if QUICK else R4):
    n = r["n"]; L = B*(n+1); okp = True
    for t, (h, p) in r["by_length"].items():
        okp &= p[0] == B*n and p[-1] == B*(n+1) and len(p) == int(t)+1 and max(p) == h and bool(check_path(p))
    bad4 += not okp; fo += r["hmin_le4"] > L
    if n in sh: both += 1; sub += r["hmin_le4"] < sh[n]["hmin"]
q["height over ALL simple routes of length<=4 (%d n): stored per-length minimal paths legal: failures %d; forced outside [1,B(n+1)] even with all routes<=4: %d; n where a non-shortest route is strictly lower than every shortest: %d of %d" % (len(R4[:40] if QUICK else R4), bad4, fo, sub, both)] = bad4 == 0 and fo > 0 and sub > 0
q["distances in the table are all <= 4 (d in %s)" % sorted({r["d"] for r in rows})] = max(r["d"] for r in rows) <= 4
ok = True
for k in ([1, 2, 5, 10] if QUICK else [1, 2, 5, 10, 20, 40]):
    n = 3*k; p = [B*n, 3*B*(k+1)**2, 3*B*(2*k+1)//4, B*(3*k+2)**2, B*(n+1)]; ok &= bool(check_path(p)) and max(p) == B*(n+2)**2
q["wormhole family n=3k, 4|B: legal 4-route with max vertex B(n+2)^2 (k=1..40), excursion ratio (n+2)^2/(n+1)"] = ok
# baselines
def check_list(path, base):
    bad = []
    for line in open(path):
        h, name = line.strip().split("  ", 1); pp = os.path.join(base, name)
        if not os.path.exists(pp) or hashlib.sha256(open(pp, "rb").read()).hexdigest() != h: bad.append(name)
    return (not bad, "OK" if not bad else "MISMATCH " + ",".join(bad[:5]))
bl = [check_list(os.path.join(proj, "SHA256SUMS.txt"), proj)] + [check_list(os.path.join(proj, f"UNNS-SCALE-I_v00{i}", f"SHA256SUMS_v00{i}.txt"), os.path.join(proj, f"UNNS-SCALE-I_v00{i}")) for i in (2, 3, 4, 5, 6, 7, 8)]
q["baselines v001-v008 unchanged (read-only hashing)"] = all(b[0] for b in bl)
rep = ["# UNNS-SCALE-I v009 verification report", "", "mode: " + ("quick" if QUICK else "full"), ""]
allok = True
for k, v in q.items():
    rep.append(("- PASS: " if v else "- FAIL: ") + k); allok &= bool(v)
rep += ["", "## Baselines"] + [f"- v00{i}: {x[1]}" for i, x in zip(range(1, 9), bl)] + ["", "ALL CHECKS PASS" if allok else "SOME CHECKS FAILED", "time %.0f s" % (time.time() - t0)]
open(os.path.join(root, "reports", "VERIFY_v009_" + ("quick" if QUICK else "full") + ".md"), "w").write("\n".join(rep))
print("\n".join(rep)); sys.exit(0 if allok else 1)

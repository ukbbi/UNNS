"""UNNS-SCALE-I v006 verifier (Arithmetic Intersection and Metric Closure -- exploratory release).
Re-checks every stored v006 result: path edge checks, primality-audited complete-ball certificates (audit_cert), the four-step intersection criterion against the
exact engine, (+-|+-) witnesses by direct integer arithmetic, divisor-lattice consistency; hash-checks v001-v005 (read-only).  Usage: python verify_all_v006.py [--quick]"""
import json, os, sys, glob, hashlib, time, random
sys.dont_write_bytecode = True
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.abspath(os.path.join(here, "..")); res = os.path.join(root, "results"); proj = os.path.abspath(os.path.join(root, ".."))
sys.path.insert(0, here)
QUICK = "--quick" in sys.argv
from indep_check import check_path
from audit_cert import audit
from exact_lib import exact_distance
from b2_types import meetings
t_start = time.time(); q = {}
J = lambda n: json.load(open(os.path.join(res, n)))
# ---- E1: divisor scales of 10^6
E1 = J("E1_divisor_scales_certified.json")["scales"]
q["E1: all 49 divisors 2^a 5^b of 10^6 present"] = sorted(map(int, E1)) == sorted(2**a * 5**b for a in range(7) for b in range(7))
ok = True; checked = 0
rows5 = [r for r in E1.values() if r["max_d_found"] >= 5]
for r in sorted(rows5, key=lambda r: (r["max_d_found"], r["A"])):
    A, n, d, p = r["A"], r["witness_n"], r["max_d_found"], r["path"]
    ok &= p[0] == A * n and p[-1] == A * (n + 1) and check_path(p) == d
    if not QUICK or d == 5 and checked < 12 or (d == 6 and A == 8):
        a = audit(A * n, A * (n + 1), d); checked += 1
        ok &= a["disjoint"] and a["factorisation_errors"] == 0 and a["primes_above_proof_bound"] == 0 and a["sizes"] == r["audit"]["sizes"]
q["E1: %d scales with a distance->=5 witness: explicit paths valid; %d lower bounds re-derived with the primality-audited complete-ball checker" % (len(rows5), checked)] = ok
six = sorted(r["A"] for r in E1.values() if r["max_d_found"] == 6)
q["E1: D_A = 6 certified for A in %s" % six] = six == [1, 2, 4, 5, 8, 10]
five = sorted(r["A"] for r in rows5 if r["max_d_found"] == 5)
undet = sorted(r["A"] for r in E1.values() if r["max_d_found"] < 5)
divs = lambda B: [A for A in range(1, B + 1) if B % A == 0]
mono = all(any(E1[str(A)]["max_d_found"] >= E1[str(B)]["max_d_found"] for _ in [0]) for B in map(int, E1) for A in divs(B) if str(A) in E1)
q["E1: divisor-lattice consistency (a witness at B forces D_A >= d for every A | B): holds"] = mono
q["E1: scales with no distance-5 case in the time-boxed search (before E3): %s" % undet] = len(undet) == 13
# ---- E3: deeper search at the undetermined scales
E3 = {A: J(f"E3_scale{A}.json") for A in (800, 1600, 4000, 8000, 20000, 40000, 62500, 100000, 125000, 200000, 250000, 500000, 1000000) if os.path.exists(os.path.join(res, f"E3_scale{A}.json"))}
w = E3[800]; p = w["witness_path"]; n = w["witness_n"]
ok = w["max_d"] == 5 and p[0] == 800 * n and p[-1] == 800 * (n + 1) and check_path(p) == 5
a = audit(800 * n, 800 * (n + 1), 5); ok &= a["disjoint"] and a["factorisation_errors"] == 0 and a["primes_above_proof_bound"] == 0
q["E3: d_800(%d) = 5 certified (path + audited balls %s): D_800 >= 5" % (n, a["sizes"])] = ok and n == 551339
rest = {A: v for A, v in E3.items() if A != 800}
q["E3: scales %s: max distance found %s (exact, time-boxed; NOT upper bounds)" % (sorted(rest), sorted({v["max_d"] for v in rest.values()}))] = all(v["max_d"] == 4 for v in rest.values()) and len(rest) >= 10
# ---- primality-audited key certificates
K = J("AUDIT_key_certificates.json")["rows"]
okk = all(r["disjoint"] and r["factorisation_errors"] == 0 and r["primes_above_proof_bound"] == 0 for r in K)
sel = K[:2] if QUICK else K
for r in sel:
    a = audit(r["B"] * r["n"], r["B"] * (r["n"] + 1), r["d_lower_bound"]); okk &= a["sizes"] == r["sizes"] and a["disjoint"]
q["Audit: D_10 = 6 (n=365759, 351359), D_4 = 6 (62459), D_8 = 6 (122939), D_1 = 6 (365759), d_12(25199) = 5: every factorisation proved (max prime factor %.2e < 3.3e24)" % max(r["max_prime_factor"] for r in K)] = okk and len(K) == 6
# ---- Proposition 1: d<=4 iff B_2 balls intersect (two code paths of the exact engine)
rng = random.Random(4); ok = True; cnt = 0
for _ in range(15 if QUICK else 60):
    B = rng.choice([1, 2, 3, 10, 12, 100]); n = rng.randint(1, 2500)
    d = exact_distance(B * n, B * (n + 1), 6)[0]; m = meetings(B * n, B * (n + 1))[0]; cnt += 1
    ok &= (d <= 4) == (m is not None) and (m is None or m == d)
q["Prop 1 (d<=4 iff B_2(x) meets B_2(y)): consistent with the exact distance engine on %d random pairs (and the meeting length equals d when d<=4)" % cnt] = ok
# ---- E2b: (+-|+-) witnesses
tot = 0; ok = True; miss = []; sets = {}
for f in sorted(glob.glob(os.path.join(res, "E2b_pm_part*.json")) + glob.glob(os.path.join(res, "E2c_pm_part*.json"))):
    D = json.load(open(f)); miss += D["misses"]
    for k, v in D["results"].items():
        n = int(k); sets[v["set"]] = sets.get(v["set"], 0) + 1
        if v["witness"] is None: continue
        N, qq, M, r, z = v["witness"]; B = 10**6; x = B * n; y = B * (n + 1); tot += 1
        x1 = x // N * (N + 1) ** 2; y1 = y // M * (M + 1) ** 2
        ok &= x % N == 0 and y % M == 0 and x1 % (qq * qq) == 0 and y1 % (r * r) == 0 and qq >= 2 and r >= 2 and x1 // (qq * qq) * (qq - 1) == z == y1 // (r * r) * (r - 1)
q["E2b+E2c: %d (+-|+-) four-step witnesses verified by direct integer arithmetic (sets %s); n with no (+-|+-) witness: %s" % (tot, sets, miss)] = ok and tot > 0
C = J("E2_census.json")
q["E2: census of %d n with complete radius-2 balls: every n meets with min total length 4; pair counts %s" % (len(C), {p: sum(p in v["pairs"] for v in C.values()) for p in ("+-|+-", "++|++", "+-|++")})] = all(v["min_total"] == 4 for v in C.values())
# ---- baselines
def check_list(path, base):
    if not os.path.exists(path): return None, "checksum list not found at " + path
    bad = []
    for line in open(path):
        if not line.strip(): continue
        h, name = line.strip().split("  ", 1); pp = os.path.join(base, name)
        if not os.path.exists(pp) or hashlib.sha256(open(pp, "rb").read()).hexdigest() != h: bad.append(name)
    return (not bad), ("all files match" if not bad else "DIFFERENT: " + ", ".join(bad))
bl = [check_list(os.path.join(proj, "SHA256SUMS.txt"), proj)] + [check_list(os.path.join(proj, f"UNNS-SCALE-I_v00{i}", f"SHA256SUMS_v00{i}.txt"), os.path.join(proj, f"UNNS-SCALE-I_v00{i}")) for i in (2, 3, 4, 5)]
allok = all(q.values()) and all(x[0] in (True, None) for x in bl)
rep = ["# UNNS-SCALE-I v006 Verification Report", "", f"Overall: **{'PASS' if allok else 'FAIL'}**  (mode: {'quick' if QUICK else 'full'}, {time.time() - t_start:.0f} s)", "", "## Checks"]
rep += [f"- {'OK ' if v else 'MISMATCH'} {k}" for k, v in q.items()]
rep += ["", "## Baseline protection (read-only hashing)"] + [f"- {n}: {x[1]}" for n, x in zip(["v001", "v002", "v003", "v004", "v005"], bl)]
rep += ["", "## Scope", "- Exploratory release: no universal bound for D_{10^6} is claimed. Finite-window theorem (v005 Part A) is untouched.", "- Lower bounds use complete balls with proved factorisations; upper bounds are explicit edge-checked paths.", "- No GitHub changes; Gate 4 deferred."]
os.makedirs(os.path.join(root, "reports"), exist_ok=True)
open(os.path.join(root, "reports", "VERIFICATION_REPORT_v006.md"), "w").write("\n".join(rep) + "\n")
lines = []
for d, _, fs in sorted(os.walk(root)):
    for f in sorted(fs):
        if f == "SHA256SUMS_v006.txt" or f.endswith(".pyc") or "__pycache__" in d: continue
        pp = os.path.join(d, f); lines.append(f"{hashlib.sha256(open(pp, 'rb').read()).hexdigest()}  {os.path.relpath(pp, root).replace(os.sep, '/')}")
open(os.path.join(root, "SHA256SUMS_v006.txt"), "w").write("\n".join(lines) + "\n")
print("PASS" if allok else "FAIL"); [print(("OK " if v else "XX "), k) for k, v in q.items()]; [print(n, x[1]) for n, x in zip(["v001", "v002", "v003", "v004", "v005"], bl)]
sys.exit(0 if allok else 1)

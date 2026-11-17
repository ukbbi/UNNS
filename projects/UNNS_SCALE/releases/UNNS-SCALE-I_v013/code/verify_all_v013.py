"""UNNS-SCALE-I v013 verifier (Scale Descent and Confined-Route Bounds).  Usage: python verify_all_v013.py [--quick]
Checks: lemma edge identities (independent sympy neighbour sets); divisor-lattice embedding data; generalized-descent data; 10^6 scale-chain data;
prime-flip composite bound and prime-family exact data; intervals + explicit routes for the seven v012 capped pairs; C++ re-runs; v001-v012 hashes."""
import json, os, sys, random, hashlib, subprocess, time, collections
sys.dont_write_bytecode = True
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.abspath(os.path.join(here, "..")); res = os.path.join(root, "results"); proj = os.path.abspath(os.path.join(root, ".."))
sys.path.insert(0, here)
QUICK = "--quick" in sys.argv
from frontier_io import read_frontier, read_ladder
from indep_check import nbrs, check_path
from primeflip import adjacency, bfs_path, bound
import summarize
t0 = time.time(); q = {}; rnd = random.Random(13); B6 = 10**6
def P(*a): return os.path.join(res, *a)
def sh(*a, **k): return subprocess.run(list(a), check=True, capture_output=True, text=True, **k).stdout
subprocess.run(["g++", "-O2", "-fopenmp", "-o", "/tmp/tau_v013", os.path.join(here, "tau_exact.cpp")], check=True)
subprocess.run(["g++", "-O2", "-o", "/tmp/ladder_v013", os.path.join(here, "ladder.cpp")], check=True)
env = {**os.environ, "OMP_NUM_THREADS": "2"}
# 1. lemma identities on random instances (independent neighbour sets from sympy divisors)
ok1 = ok2 = ok3 = True; LAD = [10**6, 160000, 7600, 361, 18, 4, 1]
for _ in range(60 if QUICK else 300):
    m = rnd.randrange(1, 10**6); ok1 &= all(LAD[i + 1] * m in nbrs(LAD[i] * m) for i in range(6))
for _ in range(60 if QUICK else 300):
    Bv = rnd.choice([100, 400, 900, 10**4, 10**6, 3600, 8100, 40000, 250000]); ss = [s for s in range(2, 2000) if Bv % (s * s) == 0]; s = rnd.choice(ss); m = rnd.randrange(1, 10**5)
    ok2 &= Bv * (s - 1) // (s * s) * m in nbrs(Bv * m)
for _ in range(60 if QUICK else 300):
    t = rnd.randrange(2, 300); k = rnd.randrange(1, 300); M = rnd.randrange(2, 10**4); a, b = k * (t - 1), k * t * t
    ok3 &= (M * b in nbrs(M * a)) and (M * a in nbrs(M * b))
q["scale ladder 10^6 m -> 160000 m -> 7600 m -> 361 m -> 18 m -> 4 m -> m consists of six edges for every sampled m (independent neighbour sets)"] = ok1
q["generalized descent: B m -- B(s-1)/s^2 m is an edge whenever s^2 | B (sampled B, s, m)"] = ok2
q["multiplier embedding: edges of G_C map to edges under s -> M s (sampled)"] = ok3
# 2. recompute all headline statistics from the stored files
S = summarize.compute(res); st = json.load(open(P("SUMMARY_v013.json")))
q["summary statistics recomputed from stored data equal SUMMARY_v013.json"] = json.loads(json.dumps(S)) == st
L_, D_, C_, Pr = S["lattice"], S["descent"], S["chain"], S["primes"]
q["embedding lemma tau^{D'}_n(M h) <= tau^D_n(h) (M = D'/D): %d exact checks over %d divisor pairs of 10^6, n=1..99: %d violations" % (L_["checks"], L_["divisor_pairs"], L_["violations"])] = L_["violations"] == 0 and L_["checks"] > 80000
q["generalized descent tau^B_n(C) <= tau^A_n(C)+2: %d exact checks over %d (B,s) combinations: %d violations; slack distribution %s" % (D_["checks"], D_["combinations"], D_["violations"], D_["slack_distribution"])] = D_["violations"] == 0
q["scale-chain bound tau^{10^6}_n(C) <= 2i + tau^{A_i}_n(C): %d exact checks (n=1..99, six levels): %d violations; best chain bound - exact: %s" % (C_["checks"], C_["violations"], C_["best_chain_bound_minus_exact"])] = C_["violations"] == 0
for k in ("B=100", "B=1000"):
    r = Pr[k]; q["prime family %s: %d primes, kappa = (p+1)^2 for %d of them; exact tau at the forced ceiling mean %.2f max %d; composite flip bound applicable %d times, never below exact (%d violations), slack mean %.2f" % (k, r["primes"], r["kappa_equals_(p+1)^2"], r["exact_mean"], r["exact_max"], r["composite_applicable"], r["composite_below_exact"], r["slack_mean"])] = r["kappa_equals_(p+1)^2"] == r["primes"] and r["composite_below_exact"] == 0
# 3. C++ rebuilds
def rebuild(Bv, Cmax, n1, n2, f, stop=None, nfile=None):
    a = ["/tmp/tau_v013", str(Bv), str(Cmax), str(n1), str(n2), "1", "/tmp/rb.txt"] + ([str(stop)] if stop else []); e = dict(env)
    if nfile: e["NFILE"] = nfile
    subprocess.run(a, check=True, capture_output=True, env=e)
    new = open("/tmp/rb.txt").read().splitlines(); old = open(f).read().splitlines()
    if nfile: keys = {l.split()[0] for l in new}; old = [l for l in old if l.split()[0] in keys]
    return new == old
lat = [10, 25, 100] if QUICK else [1, 2, 4, 5, 10, 20, 25, 50, 100, 200, 1000, 10000]
q["fresh C++ rebuild of lattice frontiers D=%s (n=1..99) reproduces the stored files" % lat] = all(rebuild(D, max(100 * D, 10000), 1, 99, P("lattice", "F_%d.txt" % D)) for D in lat)
desc = [(100, 2), (400, 4)] if QUICK else [(100, 2), (400, 4), (900, 6), (10000, 100), (10000, 5)]
ok = True
for Bv, s in desc: ok &= rebuild(Bv * (s - 1) // (s * s), 100 * Bv, 1, 99, P("descent", "FA_%d_s%d.txt" % (Bv, s)), stop=Bv) and rebuild(Bv, 100 * Bv, 1, 99, P("descent", "FB_%d.txt" % Bv))
q["fresh C++ rebuild of descent frontiers %s reproduces the stored files" % desc] = ok
pr = sorted(read_frontier(P("FP_100.txt")))[:: (40 if QUICK else 8)]; open("/tmp/nf.txt", "w").write(" ".join(map(str, pr)))
q["fresh C++ rebuild of %d prime-family frontiers at B=100 (cap 10^7) reproduces FP_100.txt rows" % len(pr)] = rebuild(100, 10**7, 1, 1, P("FP_100.txt"), nfile="/tmp/nf.txt")
if not QUICK:
    for A in (361, 4):
        q["fresh C++ rebuild of chain frontier A=%d (B=10^6 headroom, n=1..99, Cmax=10^8) reproduces FC_%d.txt" % (A, A)] = rebuild(A, 10**8, 1, 99, P("chain", "FC_%d.txt" % A), stop=10**6)
    pr = sorted(read_frontier(P("FP_1000.txt")))[::10]; open("/tmp/nf.txt", "w").write(" ".join(map(str, pr)))
    q["fresh C++ rebuild of %d prime-family frontiers at B=1000 reproduces FP_1000.txt rows" % len(pr)] = rebuild(1000, 10**7, 1, 1, P("FP_1000.txt"), nfile="/tmp/nf.txt")
# 4. prime-flip composite: B=10^6 sample, explicit routes
fl = json.load(open(P("FIRSTLEG_B6.json"))); p1 = fl["path_B_to_1"]
q["uniform first leg: 10^6 -> 160000 -> 7600 -> 361 -> 18 -> 4 -> 1 (6 edges, max vertex 10^6), hence p->... leg of the composite route has 6 steps for every prime p > 10^6"] = bool(check_path(p1)) and max(p1) == 10**6
lines = [l.split() for l in open(P("PF_B6.txt"))]; sub = lines[: (40 if QUICK else len(lines))]
adj = adjacency(int(sub[-1][0]) + 3); ok = True; napp = 0
for l in sub:
    p = int(l[0]); r = bound(p, B6, adj)
    if l[1] == "none": ok &= r is None
    else:
        ok &= r is not None and r[0] == int(l[1]) and max(r[1]) == (p + 1) ** 2 and bool(check_path(r[1])); napp += 1
q["composite prime-flip routes at B=10^6 recomputed for %d primes (%d applicable, each explicit route edge-checked, max vertex exactly (p+1)^2 = forced ceiling)" % (len(sub), napp)] = ok
L = {}
for f in ("LAD_pf100.txt", "LAD_pf1000.txt", "LAD_primes.txt"): L.update(read_ladder(P(f)))
sample = [(n, W) for (n, W), v in L.items() if isinstance(v, int) and (W < 10**11 or not QUICK) and n != 1000003]
sample = sample[: (4 if QUICK else len(sample))]; ok = True
for n, W in sample:
    Bv = 100 if W < 10**9 and n < 10**4 else (1000 if n < 10**6 else B6)
    if os.path.exists("/tmp/lc.txt"): os.remove("/tmp/lc.txt")
    sh("/tmp/ladder_v013", str(Bv), "9", "4000000", "/tmp/lc.txt", str(n), str(W)); ok &= int(open("/tmp/lc.txt").read().split()[2]) == L[(n, W)]
q["fresh C++ ladder re-run reproduces %d stored exact prime-family distances at the forced ceiling (p+1)^2" % len(sample)] = ok
# 5. capped pairs
iv = json.load(open(P("CAPPED_intervals.json"))); R = json.load(open(P("CAPPED_routes.json"))); ok = True
for n, d in iv.items(): ok &= d["lower"] <= d["upper"]
for n, d in R.items(): p = d["path"]; ok &= p[0] == B6 * int(n) and p[-1] == B6 * (int(n) + 1) and max(p) <= B6 * (int(n) + 1) and len(p) - 1 == d["length"] >= iv[n]["upper"] and bool(check_path(p))
q["capped v012 pairs: intervals %s consistent; %d explicit routes edge-checked (independent Python search) with max vertex <= B(n+1)" % ({n: (d["lower"], d["upper"]) for n, d in iv.items()}, len(R))] = ok and iv["726925"]["lower"] == iv["726925"]["upper"] == 14
LV = {160000: 1, 7600: 2, 361: 3, 18: 4, 4: 5, 1: 6}; ok = True; cnt = 0
for n, d in iv.items():
    n = int(n); A = d["best_scale"]; dist = d["distances"][str(A)]; ok &= d["upper"] == 2 * LV[A] + dist
    if QUICK and dist > 6: continue
    if os.path.exists("/tmp/lc.txt"): os.remove("/tmp/lc.txt")
    sh("/tmp/ladder_v013", str(A), "8", "4000000", "/tmp/lc.txt", str(n), str(B6 * (n + 1))); ok &= int(open("/tmp/lc.txt").read().split()[2]) == dist; cnt += 1
q["fresh C++ ladder re-run reproduces the %d best-scale distances behind the upper bounds of the capped pairs" % cnt] = ok and cnt > 0
if not QUICK:
    if os.path.exists("/tmp/lc.txt"): os.remove("/tmp/lc.txt")
    sh("/tmp/ladder_v013", str(B6), "8", "2500000", "/tmp/lc.txt", "726925", str(B6 * 726926))
    q["lower bound for the pair n=726925: exhaustive bidirectional search at scale 10^6 (cap 2.5M nodes) finds no route of length <= 13 inside [1, B(n+1)]; hence tau = 14 exactly"] = open("/tmp/lc.txt").read().split()[2].startswith(">13")
def check_list(path, base):
    bad = []
    for line in open(path):
        h, name = line.strip().split("  ", 1); pp = os.path.join(base, name)
        if not os.path.exists(pp) or hashlib.sha256(open(pp, "rb").read()).hexdigest() != h: bad.append(name)
    return (not bad, "OK" if not bad else "MISMATCH " + ",".join(bad[:5]))
bl = [check_list(os.path.join(proj, "SHA256SUMS.txt"), proj)] + [check_list(os.path.join(proj, f"UNNS-SCALE-I_v0{i:02d}", f"SHA256SUMS_v0{i:02d}.txt"), os.path.join(proj, f"UNNS-SCALE-I_v0{i:02d}")) for i in range(2, 13)]
q["baselines v001-v012 unchanged (read-only hashing)"] = all(b[0] for b in bl)
rep = ["# UNNS-SCALE-I v013 verification report", "", "mode: " + ("quick" if QUICK else "full"), ""]; allok = True
for k, v in q.items(): rep.append(("- PASS: " if v else "- FAIL: ") + k); allok &= bool(v)
rep += ["", "## Baselines"] + [f"- v0{i:02d}: {x[1]}" for i, x in zip(range(1, 13), bl)] + ["", "ALL CHECKS PASS" if allok else "SOME CHECKS FAILED", "time %.0f s" % (time.time() - t0)]
os.makedirs(os.path.join(root, "reports"), exist_ok=True)
open(os.path.join(root, "reports", "VERIFY_v013_" + ("quick" if QUICK else "full") + ".md"), "w").write("\n".join(rep)); print("\n".join(rep)); sys.exit(0 if allok else 1)

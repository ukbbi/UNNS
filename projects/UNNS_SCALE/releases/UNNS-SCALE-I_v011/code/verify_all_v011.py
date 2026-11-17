"""UNNS-SCALE-I v011 verifier (Window Connectivity and Arithmetic Excursion Barriers).  Usage: python verify_all_v011.py [--quick]
Checks: barrier theorems (brute force edges, exhaustive finite graphs, scipy cross-check); Kruskal connection-ceiling law on scaled analogues;
window-connectivity certificate for all 10^6 vertices 10^6 m (stored links, explicit gadget/BFS paths, recomputed pair ceilings = max endpoint);
explicit in-domain routes; parity lower bound vs earlier heights; (full) rebuild of the C++ certificate programs; v001-v010 hashes."""
import json, os, sys, gzip, struct, random, hashlib, subprocess, time, math, collections
sys.dont_write_bytecode = True
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.abspath(os.path.join(here, "..")); res = os.path.join(root, "results"); proj = os.path.abspath(os.path.join(root, ".."))
sys.path.insert(0, here)
QUICK = "--quick" in sys.argv
from indep_check import check_path
from hubpath import route
import ceilings
from qn import qvec
t0 = time.time(); q = {}; B = 10**6; C = 10**12; rnd = random.Random(11)
def sh(*a, **k): return subprocess.run(list(a), check=True, capture_output=True, text=True, **k).stdout
# 1. barrier theorem, brute force on all edges of G_Cb
Cb = 100000 if QUICK else 300000
spf = list(range(Cb + 1))
for i in range(2, int(Cb**.5) + 1):
    if spf[i] == i:
        for j in range(i * i, Cb + 1, i):
            if spf[j] == j: spf[j] = i
def vp(x, p):
    e = 0
    while x % p == 0: x //= p; e += 1
    return e
def primes_of(x):
    r = set()
    while x > 1: r.add(spf[x]); x //= spf[x]
    return r
bad = 0; edges = 0; sq = int(Cb**.5)
for t in range(2, sq + 2):
    for k in range(1, Cb // (t * t) + 1):
        a, b = k * (t - 1), k * t * t; edges += 1
        for p in primes_of(a) | primes_of(b) | primes_of(t) | primes_of(t - 1):
            da = vp(b, p) - vp(a, p)
            if p > sq and da != 0: bad += 1                 # large primes exactly conserved
            if da % 2 and not (p | (t - 1) and (p + 1) ** 2 <= b): bad += 1   # parity change needs p | N and a vertex >= (p+1)^2
q["barrier theorem, brute force over all %d edges of G_%d: exact conservation of v_p for p>sqrt(C); parity of v_p changes only across p | N, whose larger endpoint is >= (p+1)^2: violations %d" % (edges, Cb, bad)] = bad == 0
# 2. exhaustive finite graphs (C++), compare with stored
subprocess.run(["g++", "-O2", "-o", "/tmp/comp_v011", os.path.join(here, "comp.cpp")], check=True)
stored = {l.split()[0]: l.strip() for l in open(os.path.join(res, "T1_barrier_exhaustive.txt"))}
ok = True
for Cx in ([10000, 1000000] if QUICK else [10000, 1000000, 30000000]):
    out = sh("/tmp/comp_v011", str(Cx)).strip(); ok &= out == stored["C=%d" % Cx]
    ok &= out.endswith("parity((p+1)^2>C)=0") and "large-prime(v_p exact, p>sqrtC)=0" in out
q["exhaustive finite graphs G_C (C=10^4,10^6%s): every component has constant v_p for p>sqrt(C) and constant parity for (p+1)^2>C; output equals stored" % ("" if QUICK else ",3e7")] = ok
try:
    import numpy as np, scipy.sparse as sp, scipy.sparse.csgraph as cg
    Cs = 10**7; rows = []; cols = []
    for t in range(2, int(Cs**.5) + 1):
        ks = np.arange(1, Cs // (t * t) + 1); rows.append(ks * (t - 1)); cols.append(ks * t * t)
    r = np.concatenate(rows); c = np.concatenate(cols); G = sp.coo_matrix((np.ones(len(r), dtype=np.int8), (r, c)), shape=(Cs + 1, Cs + 1))
    nc, lab = cg.connected_components(G, directed=False); nc -= 1   # vertex 0 isolated
    out = sh("/tmp/comp_v011", str(Cs)).split()[1]
    q["independent scipy connected_components on G_10^7 agrees with the C++ union-find (components %d)" % nc] = out == "components=%d" % nc
except ImportError:
    q["scipy cross-check (scipy unavailable)"] = None
# 3. Kruskal analogues
def loadK(f):
    K = {}
    for l in gzip.open(os.path.join(res, f), "rt"):
        n, k = map(int, l.split()); K[n] = k
    return K
qv = qvec(10**6 + 2); law = lambda Bb, n: max(Bb * (n + 1), (qv[n] + 1) ** 2)
allpar = True; msg = []
for Bb, f, Cmax in ((100, "K_k100.txt.gz", 10**7), (1000, "K_k1000.txt.gz", 2 * 10**8), (10000, "K_k10000.txt.gz", 10**9), (999, "K_k999.txt.gz", 10**9)):
    K = loadK(f); ans = [n for n in K if K[n]]; allpar &= all(K[n] >= (qv[n] + 1) ** 2 for n in ans); msg.append("%d:%d" % (Bb, len(ans)))
q["parity lower bound kappa >= (q(n)+1)^2 holds for every answered pair of the exact Kruskal runs (B:answered = %s)" % ", ".join(msg)] = allpar
ok = True; cnt = 0
for Bb, f in ((1000, "K_k1000.txt.gz"), (10000, "K_k10000.txt.gz")):
    K = loadK(f); ans = [n for n in K if K[n]]; cnt += len(ans); ok &= all(K[n] == law(Bb, n) for n in ans)
K = loadK("K_k100.txt.gz"); a100 = [n for n in K if K[n] and n < 10**4]; ok &= all(K[n] == law(100, n) for n in a100); cnt += len(a100)
q["exact law kappa_B(n) = max(B(n+1), (q(n)+1)^2) on %d answered pairs (B=100 for n<B^2, B=1000, B=10^4): exceptions %s" % (cnt, "none" if ok else "FOUND")] = ok
from sympy import isprime
ok = True; cnt = 0
for Bb, f in ((100, "K_k100.txt.gz"), (1000, "K_k1000.txt.gz"), (10000, "K_k10000.txt.gz")):
    K = loadK(f)
    for n in K:
        if n > Bb and K[n] and isprime(n): cnt += 1; ok &= K[n] == (n + 1) ** 2
q["Theorem E (primes p>B): every route of any length contains a vertex >= (p+1)^2 and the exact ceiling equals (p+1)^2 on %d primes (B=100,1000,10^4)" % cnt] = ok
subprocess.run(["g++", "-O2", "-o", "/tmp/kruskal_v011", os.path.join(here, "kruskal.cpp")], check=True)
for Bb, Cmax, nm, f in [(100, 10**7, 99999, "K_k100.txt.gz")] + ([] if QUICK else [(1000, 2 * 10**8, 199999, "K_k1000.txt.gz")]):
    subprocess.run(["/tmp/kruskal_v011", str(Bb), str(Cmax), str(nm), "/tmp/kv.txt"], check=True, capture_output=True)
    new = {int(l.split()[0]): int(l.split()[1]) for l in open("/tmp/kv.txt")}
    q["fresh Kruskal re-run B=%d reproduces stored connection ceilings (%d pairs)" % (Bb, len(new))] = new == loadK(f)
# 4. window connectivity certificate: stored data consistency and ceilings
S = ceilings.compute(res); stored = json.load(open(os.path.join(res, "CN4_pair_ceilings.json")))
q["pair ceilings recomputed from the link certificates: classes %s; exact connection ceiling = B(n+1) proved for %d of 999,999 pairs; max ceiling %d" % (S["classes"], S["exact_law_proved"], S["max_ceiling"])] = (S == stored and S["exact_law_proved"] == 999999 and S["law_equals_B_n1_everywhere"] and sum(S["classes"].values()) == 10**6 and S["max_ceiling"] <= C)
# explicit stored routes
E = json.load(open(os.path.join(res, "E1_explicit_routes.json"))); ok = True
for n, p in E.items(): ok &= p[0] == B*int(n) and p[-1] == B*(int(n)+1) and max(p) == B*(int(n)+1) and bool(check_path(p))
q["explicit in-domain routes (%d pairs, lengths %s): edge-checked, maximum vertex exactly B(n+1)" % (len(E), sorted(len(p) - 1 for p in E.values()))] = ok
ns = rnd.sample(sorted(int(n) for n in E), 2 if QUICK else 5)
from explicit_routes import pair_route
ok = True
for n in ns:
    p = pair_route(n); ok &= p is not None and bool(check_path(p)) and max(p) <= B*(n+1)
q["fresh Python bidirectional search re-derives explicit hub routes for %d stored pairs" % len(ns)] = ok
# gadget sample
fl = [l.split() for l in open(os.path.join(res, "CN1_vertex_links.txt")) if " flip " in l]; ok = True; ns_ = 12 if QUICK else 60
for t in rnd.sample(fl, ns_):
    m = int(t[0]); p = int(t[2].split("=")[1]); mp = int(t[3].split("=")[1]); s = int(t[4].split("=")[1]); d = int(t[5].split("=")[1]); s0 = 999 * mp; T = C // p
    ph = [s0] if s0 == s else route(s0, s, min(T, 3 * 10**6), rmax=12, cap=500000)
    pth = [B*m] + [v*p for v in (ph or [])] + [s*(p+1)**2, s*d*(p+1-d)]
    ok &= ph is not None and bool(check_path(pth)) and max(pth) <= C and s*d*(p+1-d) <= 10**9 and (p + 1) % d == 0
q["flip-gadget routes B m -> 999 m'p ~> s p -> s(p+1)^2 -> s d (p+1-d) explicit and edge-checked for %d sampled vertices (all <= 10^12, end vertex <= 10^9)" % ns_] = ok
# BFS paths
ok = True; cnt = 0
for f, mult in (("CN2_bfs_links_R3.txt", B), ("CN3b_prime_links_domain.txt", 1)):
    L = [l.split() for l in open(os.path.join(res, f))]
    for t in rnd.sample(L, min(len(L), 60 if QUICK else 400)):
        pth = list(map(int, t[5].split(">"))); m = int(t[0]); cnt += 1
        ok &= pth[0] == mult * m and pth[-1] == int(t[2]) and pth[-1] <= 10**9 and max(pth) <= B * m and bool(check_path(pth))
q["bounded-search links (radius 2-4) to the hub: %d stored paths edge-checked, all vertices <= B m, end vertex <= 10^9" % cnt] = ok
# parity bound vs earlier height data
H = [tuple(map(int, l.split())) for l in open(os.path.join(proj, "UNNS-SCALE-I_v010", "results", "P2_H4_sample.txt"))]
H2 = []
for f in ("H2_le4_n2_150.json", "H2b_le4_n150_300.json"): H2 += [(r["n"], r["hmin_le4"]) for r in json.load(open(os.path.join(proj, "UNNS-SCALE-I_v009", "results", f)))["rows"]]
fin = [(n, h) for n, h, *_ in H if h] + H2
q["every stored minimal-height value (v009: n<=279 all routes <=4; v010: %d finite H4 values) is >= (q(n)+1)^2" % len(fin)] = all(h >= (qv[n] + 1) ** 2 for n, h in fin)
# full: rebuild certificate programs
if not QUICK:
    subprocess.run(["g++", "-O2", "-pthread", "-o", "/tmp/conn_v011", os.path.join(here, "conn.cpp")], check=True)
    subprocess.run(["g++", "-O2", "-pthread", "-o", "/tmp/conn2_v011", os.path.join(here, "conn2.cpp")], check=True)
    sh("/tmp/conn_v011", "/tmp/CN1_new.txt")
    q["fresh rebuild of conn.cpp (exact union-find to 10^9, kappa matrices, flip search) reproduces CN1_vertex_links.txt byte for byte"] = open("/tmp/CN1_new.txt").read() == open(os.path.join(res, "CN1_vertex_links.txt")).read()
    todo = [l.split()[0] + " x" for l in open(os.path.join(res, "CN2_bfs_links_R3.txt"))]; open("/tmp/todo2.txt", "w").write("\n".join(todo) + "\n")
    sh("/tmp/conn2_v011", "/tmp/todo2.txt", "/tmp/CN2_new.txt", "3", "3000000")
    # BFS tie-breaking in unordered containers may differ; compare radius, found flag and path max only
    A = {l.split()[0]: l.split()[1] for l in open("/tmp/CN2_new.txt")}; Bn = {l.split()[0]: l.split()[1] for l in open(os.path.join(res, "CN2_bfs_links_R3.txt"))}
    q["fresh rebuild of conn2.cpp re-links all %d remaining vertices to the hub at the stored radius" % len(Bn)] = A == Bn
def check_list(path, base):
    bad = []
    for line in open(path):
        h, name = line.strip().split("  ", 1); pp = os.path.join(base, name)
        if not os.path.exists(pp) or hashlib.sha256(open(pp, "rb").read()).hexdigest() != h: bad.append(name)
    return (not bad, "OK" if not bad else "MISMATCH " + ",".join(bad[:5]))
bl = [check_list(os.path.join(proj, "SHA256SUMS.txt"), proj)] + [check_list(os.path.join(proj, f"UNNS-SCALE-I_v0{i:02d}", f"SHA256SUMS_v0{i:02d}.txt"), os.path.join(proj, f"UNNS-SCALE-I_v0{i:02d}")) for i in range(2, 11)]
q["baselines v001-v010 unchanged (read-only hashing)"] = all(b[0] for b in bl)
rep = ["# UNNS-SCALE-I v011 verification report", "", "mode: " + ("quick" if QUICK else "full"), ""]; allok = True
for k, v in q.items():
    rep.append(("- PASS: " if v else ("- SKIP: " if v is None else "- FAIL: ")) + k); allok &= v is not False
rep += ["", "## Baselines"] + [f"- v0{i:02d}: {x[1]}" for i, x in zip(range(1, 11), bl)] + ["", "ALL CHECKS PASS" if allok else "SOME CHECKS FAILED", "time %.0f s" % (time.time() - t0)]
open(os.path.join(root, "reports", "VERIFY_v011_" + ("quick" if QUICK else "full") + ".md"), "w").write("\n".join(rep)); print("\n".join(rep)); sys.exit(0 if allok else 1)

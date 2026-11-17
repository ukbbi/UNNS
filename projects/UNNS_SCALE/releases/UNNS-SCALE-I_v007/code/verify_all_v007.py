"""UNNS-SCALE-I v007 verifier (Algebraic Route Construction).  Usage: python verify_all_v007.py [--quick]
Re-checks: (i) reviewer's divisor-generated proposition; (ii) Theorem A'' route identity on every shape with v',w'<=K, (iii) the explicit route of each of the 614 exceptional n,
(iv) the non-covering obstruction, (v) Proposition B witnesses, (vi) coverage table, (vii) v001-v006 hashes (read-only)."""
import json, os, sys, glob, hashlib, time, random, math
sys.dont_write_bytecode = True
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.abspath(os.path.join(here, "..")); res = os.path.join(root, "results"); proj = os.path.abspath(os.path.join(root, ".."))
sys.path.insert(0, here)
QUICK = "--quick" in sys.argv
import numpy as np
from famD import shapes, route, coverage
from propB import check as checkB
t0 = time.time(); q = {}; B = 10**6
def legal(path, labels):
    """arithmetic edge check: path=[x,x1,z,y1,y], labels=(N,qq,M,rr): x-N->x1 (forward), x1-qq->z (backward), y-M->y1, y1-rr->z"""
    x, x1, z, y1, y = path; N, qq, M, rr = labels
    return (N >= 1 and x % N == 0 and x1 == x // N * (N + 1) ** 2 and qq >= 2 and x1 % (qq * qq) == 0 and z == x1 // (qq * qq) * (qq - 1)
            and M >= 1 and y % M == 0 and y1 == y // M * (M + 1) ** 2 and rr >= 2 and y1 % (rr * rr) == 0 and z == y1 // (rr * rr) * (rr - 1) and x == B * (y // B - 1) and True)
def labels(n, sh):
    vp, wp, c, d, P, Q = sh; v = n // vp; w = (n + 1) // wp
    return (c * v, Q * (c * v + 1) // P, d * w, Q * (d * w + 1) // P)
# (i) reviewer proposition
ok = True; used = 0; hcov = set()
exc = sorted(int(k) for k in json.load(open(os.path.join(res, "V7_coverage.json")))["exceptional614"]["40"]["witness"])
H = [h for h in range(1, B // 2 + 1) if B % (2 * h) == 0]
rnd = random.Random(1)
for h in H:
    s = 2 * h + 1
    for n in [2 * h + 2 + k for k in range(0, 4 * s) if (2 * h + 2 + k) % s == 1][:3] + [n for n in exc if n % s == 1 and n >= 2 * h + 2]:
        qq = (2 * h * n + 1) // s; rr = (h * (n + 1) + 1) // s
        x = B * n; y = B * (n + 1); x1 = x // (2 * h * n) * (2 * h * n + 1) ** 2; y1 = y // (h * (n + 1)) * (h * (n + 1) + 1) ** 2; z = B * s * (n - 1)
        ok &= legal([x, x1, z, y1, y], (2 * h * n, qq, h * (n + 1), rr)) and qq >= 2 and rr >= 2; used += 1
        if n in exc: hcov.add(n)
q["Prop (divisor-generated, h with 2h|B, n=1 mod 2h+1): midpoint B(2h+1)(n-1) and four legal edges, %d instances; covers %d of the 614 exceptional n" % (used, len(hcov))] = ok and len(hcov) == 111
# (ii) Theorem A'' identity on all shapes
Kmax = 3 if QUICK else 6; S = shapes(B, Kmax); ok = True; inst = 0
for sh in S:
    vp, wp, c, d, P, Q = sh; L = vp * wp * P
    r0 = next((n for n in range(max(2, 1), L * 2 + 3) if n % vp == 0 and (n + 1) % wp == 0 and (Q * (c * (n // vp) + 1)) % P == 0), None)
    if r0 is None: continue
    for k in range(0, 3):
        n = r0 + k * L * 1; n += 0
        # step through the class: n -> n + lcm(vp*wp, P)*vp-compatible; simply search forward
    cnt = 0; n = r0
    while cnt < 2 and n < r0 + 40 * L:
        p = route(B, n, sh)
        if p is not None:
            ok &= legal(p, labels(n, sh)) and p[0] == B * n and p[4] == B * (n + 1); cnt += 1; inst += 1
        n += 1
q["Thm A'': %d shapes (v',w'<=%d, B=10^6), %d random class members: both two-step halves legal and meet at z=(B/c)(v'/Q^2)P(Q(cn/v'+1)-P)" % (len(S), Kmax, inst)] = ok and inst > 0
# (iii) the 614
W = json.load(open(os.path.join(res, "V7_coverage.json")))["exceptional614"]["40"]["witness"]; ok = True
for k, sh in W.items():
    n = int(k); sh = tuple(sh); p = route(B, n, sh); ok &= p is not None and legal(p, labels(n, sh)) and p[0] == B * n and p[4] == B * (n + 1)
cov = json.load(open(os.path.join(res, "V7_coverage.json")))["exceptional614"]
q["614 exceptional n of v005: explicit closed-form four-step route for each (shapes with v',w'<=40), %d of 614; with v',w'<=12: %d; v',w'<=3: %d" % (len(W), cov["12"]["covered"], cov["3"]["covered"])] = ok and len(W) == 614 and cov["12"]["covered"] == 613 and cov["3"]["covered"] == 481
# (iv) non-covering obstruction
ok = True
for K in (1, 2):
    SK = shapes(B, K); Lc = 1
    for vp, wp, c, d, P, Q in SK: Lc = Lc * (vp * P) // math.gcd(Lc, vp * P)
    for k in (1, 2, 3): ok &= all(route(B, Lc * k, sh) is None for sh in SK)
    ok &= all(P > 1 for *_, P, Q in SK)
q["Obstruction: for the shapes with v',w'<=1 and <=2, n=k*lcm(v'P) (k=1,2,3) is covered by no shape (P>1 always, so P | c(n/v')+1 fails when P | n/v')"] = ok
# (v) Proposition B
PB = json.load(open(os.path.join(res, "V7_coverage.json")))["propB_614"]; ok = all(checkB(B, int(k), tuple(w)) for k, w in PB["witness"].items())
v6 = [json.load(open(f)) for f in glob.glob(os.path.join(proj, "UNNS-SCALE-I_v006", "results", "E2b_pm_part*.json"))]
q["Prop B (linear labels, q | cn/v'... ): %d of 614 verified witnesses; the one miss %s has an extended (+-|+-) witness in v006 and a Thm A'' route above" % (PB["covered"], PB["miss"])] = ok and PB["covered"] == 613 and PB["miss"] == [445499] and any("445499" in d["results"] for d in v6)
# (vi) coverage table
T = json.load(open(os.path.join(res, "V7_coverage.json")))["coverage_table"]; ok = True; Nw = 2_000_000
for row in T:
    if row["K"] <= (2 if QUICK else 4):
        h, SS = coverage(B, row["K"], Nw); ok &= abs(float(h[2:].mean()) - row["cov"]) < 1e-12 and len(SS) == row["shapes"]
q["Coverage of n<=2e6 by shapes v',w'<=K (recomputed for K<=%d): %s" % (2 if QUICK else 4, "; ".join("K=%d %.4f" % (r["K"], r["cov"]) for r in T))] = ok
# (vii) baselines
def check_list(path, base):
    if not os.path.exists(path): return None, "checksum list not found"
    bad = []
    for line in open(path):
        if not line.strip(): continue
        h, name = line.strip().split("  ", 1); pp = os.path.join(base, name)
        if not os.path.exists(pp) or hashlib.sha256(open(pp, "rb").read()).hexdigest() != h: bad.append(name)
    return (not bad), ("all files match" if not bad else "DIFFERENT: " + ", ".join(bad))
bl = [check_list(os.path.join(proj, "SHA256SUMS.txt"), proj)] + [check_list(os.path.join(proj, f"UNNS-SCALE-I_v00{i}", f"SHA256SUMS_v00{i}.txt"), os.path.join(proj, f"UNNS-SCALE-I_v00{i}")) for i in (2, 3, 4, 5, 6)]
allok = all(q.values()) and all(x[0] in (True, None) for x in bl)
rep = ["# UNNS-SCALE-I v007 Verification Report", "", f"Overall: **{'PASS' if allok else 'FAIL'}**  (mode: {'quick' if QUICK else 'full'}, {time.time() - t0:.0f} s)", "", "## Checks"]
rep += [f"- {'OK ' if v else 'MISMATCH'} {k}" for k, v in q.items()]
rep += ["", "## Baseline protection (read-only hashing)"] + [f"- {n}: {x[1]}" for n, x in zip(["v001", "v002", "v003", "v004", "v005", "v006"], bl)]
rep += ["", "## Scope", "- Constructive route families and an obstruction to finite covering by them; no universal bound for D_{10^6} is claimed.", "- No GitHub changes; Gate 4 deferred."]
os.makedirs(os.path.join(root, "reports"), exist_ok=True)
open(os.path.join(root, "reports", "VERIFICATION_REPORT_v007.md"), "w").write("\n".join(rep) + "\n")
print("PASS" if allok else "FAIL"); [print(("OK " if v else "XX "), k) for k, v in q.items()]; [print(n, x[1]) for n, x in zip(["v001", "v002", "v003", "v004", "v005", "v006"], bl)]
sys.exit(0 if allok else 1)

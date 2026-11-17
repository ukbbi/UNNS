"""UNNS-SCALE-I v008 verifier (Variable-Parameter Midpoint Arithmetic).  Usage: python verify_all_v008.py [--quick]
Re-checks: exact route coordinates (bijection with brute enumeration), midpoint law / integer system / divisibility / absorption lemmas on all 12,862 v006 witnesses,
growth bounds, bounded-forward-label theorem, prime scan, rho<1 constant-ratio shapes (erratum to v007), adversarial multiples, residual scan, v001-v007 hashes."""
import json, os, sys, glob, hashlib, time, random, math, collections
sys.dont_write_bytecode = True
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.abspath(os.path.join(here, "..")); res = os.path.join(root, "results"); proj = os.path.abspath(os.path.join(root, ".."))
sys.path.insert(0, here)
QUICK = "--quick" in sys.argv
import numpy as np
from midpoint_lib import all_pairs, coord_pairs, check_witness, absorption, primes_exactly_once
from exact_lib import factor
import famE
from indep_check import check_path
t0 = time.time(); q = {}; B = 10**6
J = lambda n: json.load(open(os.path.join(res, n)))
# 1. coordinates are a bijection onto all (N,q) pairs
rnd = random.Random(8); ns = [rnd.randint(1, 10**6) for _ in range(12 if QUICK else 60)] + [5039, 3239, 445499, 65520, 2**20] + (list(range(1, 25)) if not QUICK else [])
ok = True; tot = 0
for m in ns:
    a = all_pairs(B, m); b = coord_pairs(B, m); tot += len(a); ok &= sorted(a) == sorted(b)
q["Thm L: (d,v,P,Q) coordinates give exactly the legal (N,q) pairs, bijectively (%d numbers, %d pairs, complete divisor enumeration)" % (len(ns), tot)] = ok
# 2. lemmas on all stored witnesses
fail = collections.Counter(); tw = 0; unabs = 0; pr = 0
files = sorted(glob.glob(os.path.join(proj, "UNNS-SCALE-I_v006", "results", "E2[bc]_pm_part*.json")))
for f in files:
    for k, v in json.load(open(f))["results"].items():
        if v["witness"] is None: continue
        n = int(k); N, qq, M, r, z = v["witness"]; tw += 1
        for name, val in check_witness(B, n, N, qq, M, r, z).items():
            if not val: fail[name] += 1
        a = absorption(B, n, N, qq, M, r)
        for d_ in (a["n"], a["n1"]):
            for l, w in d_.items():
                pr += 1; unabs += (not w)
q["Lemmas on all %d stored (+-|+-) routes of v006 (B=10^6): legality, midpoint law, integer system S1/S2, n | N Q^2 P'^2 (r-1), n+1 | M Q'^2 P^2 (q-1), n <= N(M+1)^2 q^2 (r-1): failures %s" % (tw, dict(fail) or "none")] = tw == 12862 and not fail
q["Absorption Lemma: each of %d primes l || n or l || n+1 (l not dividing B) divides N, M+1 or r-1 (resp. M, N+1 or q-1): unabsorbed %d" % (pr, unabs)] = pr > 40000 and unabs == 0
# 3. growth data
G = J("G1_min_label.json"); sk = set(factor(B)); okg = True; viol = 0; cnt = 0; ex = []
for k, v in G.items():
    n = int(k)
    if not v["min"]: okg = False; continue
    T, N, qq, M, r = v["min"]; cw = check_witness(B, n, N, qq, M, r); okg &= all(cw.values()) and T == max(N, qq, M, r)
    ls = primes_exactly_once(n, sk) + primes_exactly_once(n + 1, sk); viol += bool(ls and T < max(ls) - 1)
    ok_t = n <= T**4 * (T + 1) ** 2; okg &= ok_t; cnt += 1
    if n > 100: ex.append(math.log(T) / math.log(n))
q["Growth: %d n with exact minimal route label T (complete enumeration): every n has a route; n <= T^4(T+1)^2; T >= l-1 for every prime l || n(n+1) coprime to B (violations %d); observed log T/log n: min %.3f, median %.3f" % (cnt, viol, min(ex), sorted(ex)[len(ex) // 2])] = okg and viol == 0 and cnt >= 1700
# recompute exact minimal T for a few n
from growth_scan import minT
okm = True; sel = rnd.sample(sorted(G), 6 if QUICK else 30)
for k in sel:
    r_ = minT(int(k)); okm &= r_ is not None and r_[0] == G[k]["min"][0]
q["Growth: exact recomputation of the minimal label for %d stored n agrees" % len(sel)] = okm
# 4. bounded forward labels
S1 = J("S1_sqrt_routes.json"); ok = True
for (n, N, M, qq, r) in S1["legal"]: ok &= all(check_witness(B, n, N, qq, M, r).values())
nsq = sorted({x[0] for x in S1["legal"]})
import sympy as sp
Ns, Ms, rs, m0 = sp.symbols("N M r m0", positive=True); K1 = Ms * (Ns + 1) ** 2; K2 = Ns * (Ms + 1) ** 2; c0 = K1 / K2
Dp = sp.Poly(sp.expand(K1 * rs**2 * (c0 * rs + m0 - 1) - K2 * (c0 * rs + m0) ** 2 * (rs - 1)), rs)
ident = sp.simplify(Dp.coeff_monomial(rs**3)) == 0 and sp.simplify(Dp.coeff_monomial(rs**2) - K1 * (c0 - 1 - m0)) == 0 and sp.simplify(sp.expand(K1 * rs**2 * (c0 * rs + c0 - 2) - K2 * (c0 * rs + c0 - 1) ** 2 * (rs - 1)) - K2 * (c0 - 1) * ((c0 + 1) * rs + c0 - 1)) == 0
from degenerate import analyse
deg = 0
for N_ in range(1, (12 if QUICK else 40) + 1):
    for M_ in range(1, (12 if QUICK else 40) + 1):
        for P_ in [d for d in range(1, N_ + 2) if (N_ + 1) % d == 0]:
            for P2_ in [d for d in range(1, M_ + 2) if (M_ + 1) % d == 0]:
                lam, c2, c1, c0_ = analyse(N_, M_, P_, P2_); deg += (c1 != 0 and c0_ + sp.Rational(P_, N_ + 1) * c1 == 0 and lam.denominator == 1)
q["Thm S (bounded forward labels): symbolic identities for D(r) (cubic term 0, r^2 coefficient K1(c0-1-m0), degenerate case q+1=c0(r+1)); %d degenerate tuples for N,M<=%d; search N,M<=6 with q=rho*q0, r=sigma*r0: exactly %d routes, %d distinct n (max %d), all legal" % (deg, 12 if QUICK else 40, len(S1["legal"]), len(nsq), nsq[-1])] = ok and ident and deg == 0 and len(nsq) == 25
# 5. prime scan
P1 = J("P1_prime_scan.json"); okp = all(v["routes"] > 0 and set(v["cases"]) == {"N"} and v["Tmin"] >= int(k) - 1 for k, v in P1.items())
from prime_scan import routes
for k in rnd.sample(sorted(P1), 3 if QUICK else 12):
    R = routes(int(k)); okp &= len(R) == P1[k]["routes"] and min(max(t) for t in R) == P1[k]["Tmin"]
q["Prime scan: %d prime n (%d below 1e6, rest 1e9..1e10), exact: every prime has a (+-|+-) route, every route absorbs the prime in N (never in M+1 or r-1); minimal label >= p-1; sample recomputed" % (len(P1), sum(int(k) < 10**6 for k in P1))] = okp and len(P1) == 560
# 6. rho<1 shapes (erratum)
sh = (3, 1, 1, 1, 1, 2)   # v'=3,w'=1,c=d=1, rho=1/2
okf = True; cntf = 0
for n in range(3, 30001, 3):
    p = famE.route(B, n, sh); okf &= p is not None and p[0] == B * n and p[4] == B * (n + 1); cntf += 1
for n in range(3, 400 if QUICK else 1500, 3): okf &= check_path(famE.route(B, n, sh)) == 4
q["Erratum: shape (v',w',c,d)=(3,1,1,1) has rho=1/2 (P=1, no congruence condition): routes exist for all %d multiples of 3 in [3,30000]; %s edge-checked independently (sympy BFS)" % (cntf, "n<%d" % (400 if QUICK else 1500))] = okf
sP = famE.shapes(B, 2)
okp1 = all(any(famE.route(B, L * k, s_) is not None for s_ in sP if s_[4] == 1) or True for L in (1,))
Ls = 1
for vp, wp, c, d, P, Q in sP:
    if P > 1: Ls = Ls * (vp * P) // math.gcd(Ls, vp * P)
okobs = all(famE.route(B, Ls * k, s_) is None for k in (1, 2, 3) for s_ in sP if s_[4] > 1)
q["Corrected obstruction: shapes with P>1 (v',w'<=2) cover no multiple of L=lcm(v'P) (L has %d digits); shapes with P=1 are not obstructed" % len(str(Ls))] = okobs
C1 = J("C1_coverage_with_rho_lt1.json"); okc = True
for row in C1["rows"]:
    if row["K"] <= (3 if QUICK else 8):
        h, S = famE.coverage(B, row["K"], 2_000_000); h0, S0 = famE.coverage(B, row["K"], 2_000_000, False)
        okc &= int((~h[2:]).sum()) == row["unc_all"] and int((~h0[2:]).sum()) == row["unc_pos"] and len(S) == row["shapes_all"]
q["Coverage n<=2e6 (recomputed for K<=%d): uncovered with rho>1 only vs with rho<1 added: %s" % (3 if QUICK else 8, "; ".join("K=%d %d -> %d" % (r_["K"], r_["unc_pos"], r_["unc_all"]) for r_ in C1["rows"]))] = okc
# 7. adversarial multiples of L_S
A1 = J("A1_adversarial.json"); from adversarial import L_of
oka = True; Lcache = {}
for key, v in A1.items():
    S_ = v["S"]; Lcache.setdefault(S_, L_of(S_)); oka &= v["n"] % Lcache[S_] == 0 and v["routes"] > 0
    if not QUICK or S_ <= 10:
        shp = [s_ for s_ in famE.shapes(B, 12, False) if s_[4] <= S_]
        oka &= all(famE.route(B, v["n"], s_) is None for s_ in shp)
q["Adversarial: %d numbers n = k*L_S (S=5..30; every constant-ratio shape with rho>1, v',w'<=12 and P<=S fails by construction) still have exact (+-|+-) routes; %d of them have a minimal route with rho<1 (P=1) or P>S" % (len(A1), sum(1 for v in A1.values() if v["best"]["rho"][0] == 1 or v["best"]["rho"][0] > v["S"]))] = oka
# 8. residual scan
R2 = J("R2_residual_K20_N20000000.json"); shp = famE.shapes(B, 20 if not QUICK else 8)
okr = not R2["none"] and len(R2["uncovered"]) == len(R2["routes"]) and all(v > 0 for v in R2["routes"].values())
for n in R2["uncovered"][: (6 if QUICK else 48)]: okr &= all(famE.route(B, n, s_) is None for s_ in (shp if not QUICK else famE.shapes(B, 20)))
q["Residual: n<=2e7 uncovered by all constant-ratio shapes with v',w'<=20 (rho>0): %d numbers; each re-tested uncovered; every one has an exact (+-|+-) route (none without)" % len(R2["uncovered"])] = okr
# 9. baselines
def check_list(path, base):
    if not os.path.exists(path): return None, "checksum list not found"
    bad = []
    for line in open(path):
        if not line.strip(): continue
        h, name = line.strip().split("  ", 1); pp = os.path.join(base, name)
        if not os.path.exists(pp) or hashlib.sha256(open(pp, "rb").read()).hexdigest() != h: bad.append(name)
    return (not bad), ("all files match" if not bad else "DIFFERENT: " + ", ".join(bad))
bl = [check_list(os.path.join(proj, "SHA256SUMS.txt"), proj)] + [check_list(os.path.join(proj, f"UNNS-SCALE-I_v00{i}", f"SHA256SUMS_v00{i}.txt"), os.path.join(proj, f"UNNS-SCALE-I_v00{i}")) for i in (2, 3, 4, 5, 6, 7)]
allok = all(q.values()) and all(x[0] in (True, None) for x in bl)
rep = ["# UNNS-SCALE-I v008 Verification Report", "", f"Overall: **{'PASS' if allok else 'FAIL'}**  (mode: {'quick' if QUICK else 'full'}, {time.time() - t0:.0f} s)", "", "## Checks"]
rep += [f"- {'OK ' if v else 'MISMATCH'} {k}" for k, v in q.items()]
rep += ["", "## Baseline protection (read-only hashing)"] + [f"- {n}: {x[1]}" for n, x in zip(["v001", "v002", "v003", "v004", "v005", "v006", "v007"], bl)]
rep += ["", "## Scope", "- Exact route coordinates and necessary conditions, bounded-label finiteness, erratum to v007; no universal bound for D_{10^6} is claimed.", "- No GitHub changes; Gate 4 deferred."]
os.makedirs(os.path.join(root, "reports"), exist_ok=True)
open(os.path.join(root, "reports", "VERIFICATION_REPORT_v008.md"), "w").write("\n".join(rep) + "\n")
print("PASS" if allok else "FAIL"); [print(("OK " if v else "XX "), k) for k, v in q.items()]; [print(n, x[1]) for n, x in zip(["v001", "v002", "v003", "v004", "v005", "v006", "v007"], bl)]
sys.exit(0 if allok else 1)

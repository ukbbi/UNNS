"""UNNS-SCALE-I v003 verifier.  Re-checks every stored result with code independent of the search engines where possible,
re-checks the numbers quoted in THEORY_v003, confirms v001 and v002 are unchanged (read-only hashing), writes the report and checksum list.
Usage: python verify_all_v003.py [--quick]     (no bytecode is written)"""
import json, os, sys, glob, hashlib, time, random
from fractions import Fraction
sys.dont_write_bytecode = True
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.abspath(os.path.join(here, ".."))
res = os.path.join(root, "results"); proj = os.path.abspath(os.path.join(root, ".."))
sys.path.insert(0, here)
QUICK = "--quick" in sys.argv
from poly_check import verify_identity
from indep_check import certify_distance, check_path, ball
from exact_lib import exact_distance
t_start = time.time()
q = {}; notes = []
J = lambda n: json.load(open(os.path.join(res, n)))

# ---------------------------------------------------------------- D0 elementary laws
ok = True
for N in range(1, 2000):
    ok &= (N + 1) ** 2 >= 4 * N                      # ratio (N+1)^2/N >= 4 for all N >= 1
q["D0 Prop 1.1: edge ratio (N+1)^2/N >= 4 > 2 >= (n+1)/n  (N<2000 exhaustive; identity (N+1)^2-4N=(N-1)^2)"] = ok
surv = {}
for f in sorted(glob.glob(os.path.join(res, "D1b_survey_B*_N*.json"))):
    s = J(os.path.basename(f))
    for B, ds in s["d"].items(): surv.setdefault(int(B), {}).update({n: d for n, d in enumerate(ds, 1)})
viol = checked = 0
for A in surv:
    for B in surv:
        if B > A and B % A == 0:
            for n in surv[A].keys() & surv[B].keys():
                checked += 1; viol += surv[B][n] > surv[A][n]
q["D0 Prop 1.2 pointwise law d_B(n)<=d_A(n), A|B: %d exact pairs, 0 violations" % checked] = viol == 0 and checked == 181500
q["D0: all surveyed distances in {2,..,6}"] = all(2 <= d <= 6 for B in surv for d in surv[B].values())
mu_ok = True
for A in surv:
    for B in surv:
        if B > A and B % A == 0:
            N = min(len(surv[A]), len(surv[B])); mu_ok &= sum(surv[B][n] for n in range(1, N + 1)) <= sum(surv[A][n] for n in range(1, N + 1))
q["D0 Cor 1.3(d): mean route length monotone along divisor pairs (survey)"] = mu_ok

# independent recomputation of small distances (sympy-based balls, no shared code with exact_lib)
def indep_distance(u, v):
    if u == v: return 0
    for D in range(1, 7):
        r = (D + 1) // 2; s = D - r
        _, Bu = ball(u, r); _, Bv = ball(v, s)
        if Bu & Bv: return D
    return 7
random.seed(3); bad = 0; cnt = 0
for B in ([1, 2, 3, 4, 6, 12] if not QUICK else [1, 2]):
    for n in range(1, 13):
        cnt += 1; bad += indep_distance(B * n, B * (n + 1)) != surv[B][n]
q["D0/D1 independent (sympy ball) recomputation matches stored survey: %d pairs" % cnt] = bad == 0
# stored survey vs fresh exact engine
bad = 0; cnt = 0
for B in ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 16, 24, 30, 48] if not QUICK else [1, 12]):
    for n in range(1, 61):
        cnt += 1; bad += exact_distance(B * n, B * (n + 1))[0] != surv[B][n]
q["D1 exact engine reproduces stored survey (%d pairs)" % cnt] = bad == 0

# ---------------------------------------------------------------- D1 tables
D1 = {}
for f in glob.glob(os.path.join(res, "D1_B*_N6000.json")):
    r = json.load(open(f)); D1[r["B"]] = r
q["D1 results present for B=1,2,3,4,5,6,7,8,10,12"] = sorted(D1) == [1, 2, 3, 4, 5, 6, 7, 8, 10, 12]
q["D1 every histogram sums to 6000 and mean matches"] = all(sum(r["hist"].values()) == 6000 and abs(sum(int(k) * v for k, v in r["hist"].items()) / 6000 - r["mean"]) < 1e-9 for r in D1.values())
expected = {1: {"2": 2, "3": 23, "4": 3587, "5": 2280, "6": 108}, 2: {"2": 2, "3": 29, "4": 5105, "5": 864}, 3: {"2": 2, "3": 1513, "4": 3844, "5": 641},
            4: {"2": 2, "3": 35, "4": 5933, "5": 30}, 5: {"2": 2, "3": 31, "4": 4302, "5": 1665}, 6: {"2": 2, "3": 1517, "4": 4354, "5": 127},
            7: {"2": 2, "3": 355, "4": 3920, "5": 1670, "6": 53}, 8: {"2": 2, "3": 37, "4": 5953, "5": 8}, 10: {"2": 2, "3": 37, "4": 5512, "5": 449},
            12: {"2": 2, "3": 1520, "4": 4478}}
q["D1 histograms equal the table quoted in THEORY"] = all(D1[B]["hist"] == expected[B] for B in expected)
cert_ok = True; ncert = 0
for B, r in D1.items():
    for dd, c in r["independent_certificates"].items():
        n = c["n"]; path = c["path"]; d = int(dd)
        cert_ok &= path[0] == B * n and path[-1] == B * (n + 1) and certify_distance(B * n, B * (n + 1), d, path) is not None; ncert += 1
q["D1 independent certificates re-run (explicit path + disjoint balls): %d" % ncert] = cert_ok
q["D1 B=7 attains 6 at n=163 and B=1 at n=163: D_7=6 certified"] = D1[7]["first_witness"]["6"]["n"] == 163 and D1[1]["first_witness"]["6"]["n"] == 163
q["D1 no n<=6000 gives d_12(n)=5 (finite max 4)"] = D1[12]["finite_max"] == 4

# ---------------------------------------------------------------- D2 covers
tot_ident = 0; d2_ok = True; disj_ok = True; dens_ok = True
D2 = {}
for f in sorted(glob.glob(os.path.join(res, "D2_B*_K*.json"))):
    r = json.load(open(f)); B, K = r["B"], r["K"]; D2[(B, K)] = r
    cls = []
    for c in r["identities"]:
        steps = [(d, N) for d, N in c["steps"]]
        okk, info = verify_identity(B, c["M"], c["r"], steps)
        d2_ok &= okk and info == c["t0"] and len(steps) <= K; tot_ident += 1; cls.append((c["M"], c["r"]))
    exc = [(e["M"], e["r"]) for e in r["exceptional_classes_OPEN_for_this_K"]]
    allc = cls + exc
    for i in range(len(allc)):
        for j in range(i + 1, len(allc)):
            from math import gcd
            g = gcd(allc[i][0], allc[j][0])
            if (allc[i][1] - allc[j][1]) % g == 0: disj_ok = False
    dens = sum(Fraction(1, M) for M, _ in cls); edens = sum(Fraction(1, M) for M, _ in exc)
    dens_ok &= dens + edens == 1 and str(dens) == r["density_covered"]
q["D2 all %d identities re-verified without sympy (division, endpoint, positivity, numeric replay)" % tot_ident] = d2_ok
q["D2 covered + exceptional classes are pairwise disjoint (partition of N)"] = disj_ok
q["D2 densities sum to 1 and match stored fractions"] = dens_ok
q["D2 densities as quoted: 12:6299/6300, 2/4:209/210, 10/5:359/360, 6:839/840, 3:247/252"] = (
    D2[(12, 4)]["density_covered"] == "6299/6300" and D2[(2, 5)]["density_covered"] == D2[(4, 5)]["density_covered"] == "209/210" and
    D2[(10, 5)]["density_covered"] == D2[(5, 5)]["density_covered"] == "359/360" and D2[(6, 5)]["density_covered"] == "839/840" and D2[(3, 5)]["density_covered"] == "247/252")
# random cross-check against the exact engine
random.seed(11); bad = 0; cnt = 0
for (B, K), r in D2.items():
    for _ in range(40 if not QUICK else 5):
        c = random.choice(r["identities"]); tt = random.randrange(0, 4000); n = c["M"] * tt + c["r"]
        if n >= 1:
            cnt += 1; bad += exact_distance(B * n, B * (n + 1))[0] > K
q["D2 random members of covered classes (n up to ~10^7) satisfy d_B(n)<=K by the exact engine: %d checked" % cnt] = bad == 0
q["D2 B=12: n=25199 lies in an exceptional class and has d=5"] = (25199 % 12600 == 12599) and (12600, 12599) in [(e["M"], e["r"]) for e in D2[(12, 4)]["exceptional_classes_OPEN_for_this_K"]]
q["D2 worked example in THEORY (B=12, n=6t+1) is the stored identity"] = any(c["M"] == 6 and c["r"] == 1 and c["steps"] == [["+", [12, 2]], ["-", [4, 0]], ["+", [2, 0]], ["-", [6, 2]]] for c in D2[(12, 4)]["identities"])

# ---------------------------------------------------------------- D3 / D4
D3 = J("D3_hierarchy.json")
q["D3 certified D_B=6 list as quoted"] = D3["scales_with_certified_D_B_equal_6"] == [1, 7, 11, 13, 17, 19, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 91]
q["D3 pointwise law: 181500 pairs, 0 violations"] = D3["pointwise_law_pairs_checked"] == 181500 and not D3["pointwise_law_violations"]
q["D3 all D=6 scales are coprime to 30"] = all(__import__("math").gcd(B, 30) == 1 for B in D3["scales_with_certified_D_B_equal_6"])
q["D3 closed under divisors"] = all((d in D3["scales_with_certified_D_B_equal_6"]) for B in D3["scales_with_certified_D_B_equal_6"] for d in range(1, B + 1) if B % d == 0)
d4 = {}
for f in glob.glob(os.path.join(res, "D4_smooth_B*.json")):
    r = json.load(open(f)); d4[r["B"]] = r
q["D4 smooth probe present for B=1,2,4,6,12,24,48"] = sorted(d4) == [1, 2, 4, 6, 12, 24, 48]
cert_ok = True
for B, r in d4.items():
    for w in r["d_ge_5_witnesses"][:3]:
        cert_ok &= check_path(w["path"]) == w["d"] and w["path"][0] == B * w["n"] and w["path"][-1] == B * (w["n"] + 1)
q["D4 witness paths valid (first three d>=5 per B)"] = cert_ok
q["D4 hist quoted: B=12 has 12 d=5, B=24 has 5, B=48 has 2, B=1 has one d=6 (n=171499)"] = (d4[12]["hist"].get("5") == 12 and d4[24]["hist"].get("5") == 5 and d4[48]["hist"].get("5") == 2 and
    d4[1]["hist"].get("6") == 1 and d4[1]["max_witness"]["n"] == 171499 and d4[1]["max_witness"]["d"] == 6)
mw_ok = True
for B, r in d4.items():
    w = r["max_witness"]; mw_ok &= w["path"][0] == B * w["n"] and w["path"][-1] == B * (w["n"] + 1) and check_path(w["path"]) == w["d"]
    if not QUICK: mw_ok &= certify_distance(B * w["n"], B * (w["n"] + 1), w["d"], w["path"]) is not None
q["D4 max witnesses (incl. B=1, n=171499, d=6) re-certified independently" + (" (paths only in quick mode)" if QUICK else "")] = mw_ok
s96 = J("D1b_survey_B96_N500.json")["d"]
q["D4 mean route length by class (gcd(B,6)=1: 4.171, 2|B: 3.971, 3|B: 3.749, 6|B: 3.705)"] = all(
    abs(sum(sum(v) / len(v) for B, v in s96.items() if cond(int(B))) / sum(1 for B in s96 if cond(int(B))) - val) < 5e-4
    for cond, val in [(lambda B: B % 2 and B % 3, 4.171), (lambda B: B % 2 == 0 and B % 3, 3.971), (lambda B: B % 2 and B % 3 == 0, 3.749), (lambda B: B % 6 == 0, 3.705)])
dl = {}
d1 = s96["1"]
for B in (2, 3, 6, 12, 96):
    v = s96[str(B)]; dl[B] = (sum(1 for a, b in zip(d1, v) if a > b) / 500, sum(a - b for a, b in zip(d1, v)) / 500)
q["D4 shortening table (P(delta>0), mean delta): 2:(.200,.208) 3:(.378,.476) 6:(.444,.542) 12:(.460,.560) 96:(.470,.572)"] = all(
    abs(dl[B][0] - p) < 5e-4 and abs(dl[B][1] - m) < 5e-4 for B, (p, m) in {2: (.2, .208), 3: (.378, .476), 6: (.444, .542), 12: (.46, .56), 96: (.47, .572)}.items())
q["D4 exit lemma data: delta>0 never exceeds 2 in the survey"] = all(a - b <= 2 for B in s96 for a, b in zip(s96["1"], s96[B]))

# ---------------------------------------------------------------- baselines
def check_list(path, base):
    if not os.path.exists(path): return None, "checksum list not found at " + path
    bad = []
    for line in open(path):
        if not line.strip(): continue
        h, name = line.strip().split("  ", 1)
        p = os.path.join(base, name)
        if not os.path.exists(p) or hashlib.sha256(open(p, "rb").read()).hexdigest() != h: bad.append(name)
    return (not bad), ("all files match" if not bad else "DIFFERENT: " + ", ".join(bad))
v1_ok, v1_msg = check_list(os.path.join(proj, "SHA256SUMS.txt"), proj)
v2_ok, v2_msg = check_list(os.path.join(proj, "UNNS-SCALE-I_v002", "SHA256SUMS_v002.txt"), os.path.join(proj, "UNNS-SCALE-I_v002"))
allok = all(q.values()) and (v1_ok in (True, None)) and (v2_ok in (True, None))
rep = ["# UNNS-SCALE-I v003 Verification Report", "", f"Overall: **{'PASS' if allok else 'FAIL'}**  (mode: {'quick' if QUICK else 'full'}, {time.time() - t_start:.0f} s)", "",
       "## Checks (each re-derived from stored results; independent code where stated)"]
rep += [f"- {'OK ' if v else 'MISMATCH'} {k}" for k, v in q.items()]
rep += ["", "## Baseline protection (read-only hashing)", f"- v001: {v1_msg}", f"- v002: {v2_msg}",
        "", "## Scope notes",
        "- Finite maxima are CERTIFIED LOWER bounds on D_B, never suprema (THEORY section 0).",
        "- Theorem 3.1 gives upper bounds only on explicit residue classes; the exceptional classes are OPEN at that K.",
        "- D_B < 6 for any B is NOT established; D_B = 6 is certified for the 21 scales listed (and their divisors).",
        "- Sympy-free polynomial verification (poly_check) and sympy-ball certificates (indep_check) share no code with sym_lib / exact_lib.",
        "- No GitHub changes; nothing published; Gate 4 deferred."]
os.makedirs(os.path.join(root, "reports"), exist_ok=True)
open(os.path.join(root, "reports", "VERIFICATION_REPORT_v003.md"), "w").write("\n".join(rep) + "\n")
lines = []
for d, _, fs in sorted(os.walk(root)):
    for f in sorted(fs):
        if f == "SHA256SUMS_v003.txt" or f.endswith(".pyc") or "__pycache__" in d: continue
        p = os.path.join(d, f); lines.append(f"{hashlib.sha256(open(p, 'rb').read()).hexdigest()}  {os.path.relpath(p, root).replace(os.sep, '/')}")
open(os.path.join(root, "SHA256SUMS_v003.txt"), "w").write("\n".join(lines) + "\n")
print("PASS" if allok else "FAIL"); [print(("OK " if v else "XX "), k) for k, v in q.items()]; print("v001:", v1_msg); print("v002:", v2_msg)
sys.exit(0 if allok else 1)

"""ANS-I v001 verification suite and endpoint census. Standard library only.

    python verify.py                 stages A-C (ceiling 100,000)
    python verify.py --stage D       adds ceiling 1,000,000
    python verify.py --stage E       adds ceiling 10,000,000 (needs about 1 GB of memory)
Exit status 0 iff every check passes.
"""
import argparse, csv, gzip, io, json, math, os, platform, sys, time, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from endpoint_engine import endpoint_census, unpack, WIDTH
from ancestry_engine import ancestry_census
from mobius_check import mobius_transform, direct_inversion
import prime_dynamics as pdyn
import dirichlet as ds
import grammar_controls as gc
import generative_record as gen

CEIL = {"A": 1000, "B": 10000, "C": 100000, "D": 1000000, "E": 10000000}
DEPTH = {"A": 4, "B": 6, "C": 8, "D": 9, "E": 11}
OUT = os.path.join(HERE, "results")
CHECKS = []


def check(ident, name, ok, detail=None):
    CHECKS.append({"theorem": ident, "check": name, "status": "PASS" if ok else "FAIL",
                   "detail": detail})
    print("%-4s %-8s %s" % ("PASS" if ok else "FAIL", ident, name), flush=True)


def dump(name, obj):
    with open(os.path.join(OUT, name), "w", newline="\n") as f:
        json.dump(obj, f, indent=1)
        f.write("\n")


def gz_csv(name, header, rows):
    """Deterministic gzip (no timestamp or file name in the header)."""
    with open(os.path.join(OUT, name), "wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as z:
            t = io.TextIOWrapper(z, newline="")
            w = csv.writer(t, lineterminator="\n")
            w.writerow(header)
            w.writerows(rows)
            t.flush()


def stage(letter):
    X = CEIL[letter]
    t0 = time.time()
    a = endpoint_census(X)
    t1 = time.time()
    H = ancestry_census(X)
    t2 = time.time()
    K = DEPTH[letter]
    C = unpack(sum(H))
    argH = max(range(1, X + 1), key=lambda n: sum(unpack(H[n])) if H[n] > 1 else 1)
    A = unpack(sum(a.values()))
    arga = max(a, key=lambda n: (sum(unpack(a[n])), -n))
    maxa, maxH = sum(unpack(a[arga])), sum(unpack(H[argH]))
    if letter == "C":
        gz_csv("endpoint_multiplicities_100000.csv.gz", ["n", "k", "a_k"],
               ((n, k, c) for n in sorted(a) for k, c in enumerate(unpack(a[n])) if c))
        gz_csv("history_counts_100000.csv.gz", ["n", "k", "H_k"],
               ((n, k, c) for n in range(1, X + 1) if H[n] > 1
                for k, c in enumerate(unpack(H[n])) if c))
        direct = all(direct_inversion(H, n) == a.get(n, 0) for n in range(1, 2001))
        check("T02", "direct mu-sum equals forward a_k for n <= 2000", direct)
        extra = analyse_census(a, H, X)
    else:
        extra = None
    inv = mobius_transform(H)
    bad = sum(inv[n] != a.get(n, 0) for n in range(1, X + 1))
    del inv
    t3 = time.time()
    check("T02/T03", "stage %s (X=%d): forward a_k = mu * backward H_k at every n, every depth"
          % (letter, X), bad == 0, {"mismatches": bad})
    check("T03", "stage %s: maximum depth equals floor(log_4 X) = %d" % (letter, K),
          len(A) - 1 == K and 4 ** K <= X < 4 ** (K + 1))
    rec = {"stage": letter, "X": X, "A_k": A, "C_k": C, "A": sum(A), "C": sum(C),
           "distinct_endpoints": len(a), "max_a": [arga, maxa], "max_H": [argH, maxH],
           "log_A_over_log_X": math.log(sum(A)) / math.log(X),
           "log_C_over_log_X": math.log(sum(C)) / math.log(X)}
    dump("census_stage_%s.json" % letter, rec)
    print("     stage %s timings: forward %.1fs backward %.1fs inversion+records %.1fs"
          % (letter, t1 - t0, t2 - t1, t3 - t2), flush=True)
    return rec, extra


def analyse_census(a, H, X):
    # multiplicativity witnesses, depth by depth
    hk = [unpack(H[n]) for n in range(X + 1)]
    get = lambda n, k: hk[n][k] if k < len(hk[n]) else 0
    def witness(f, limit):
        for n in range(2, limit + 1):
            for m in range(2, math.isqrt(n) + 1):
                if n % m == 0 and m < n // m and math.gcd(m, n // m) == 1:
                    q = n // m
                    if f(n) != f(m) * f(q):
                        return {"m": m, "n": q, "f(m)": f(m), "f(n)": f(q), "f(mn)": f(n)}
    wit = {"H": witness(lambda n: sum(hk[n]), X), "a": witness(lambda n: sum(unpack(a.get(n, 0))), X)}
    for k in range(1, 7):
        wit["H_%d" % k] = witness(lambda n: get(n, k), X)
    dump("multiplicativity_witnesses.json", wit)
    check("T06", "exact coprime witnesses found for H, a and H_1..H_6",
          all(v is not None for v in wit.values()), wit)
    # relative size of H(mn) against H(m)H(n) over all coprime non-squarefree pairs
    tally = {"greater": 0, "equal": 0, "less": 0}
    ns = [n for n in range(4, X // 4 + 1) if H[n] > 1]
    for i, m in enumerate(ns):
        if m * m > X:
            break
        for q in ns[i + 1:]:
            if m * q > X:
                break
            if math.gcd(m, q) == 1:
                d = sum(hk[m * q]) - sum(hk[m]) * sum(hk[q])
                tally["greater" if d > 0 else "less" if d < 0 else "equal"] += 1
    dump("coprime_pair_tally.json", {"X": X, "pairs": "coprime, both non-squarefree, mn<=X", **tally})
    # partial sums of G_k against the analytic bounds of T07
    rows, ok = [], True
    for sig in (1.6, 2.0):
        B = ds.B_bracket(min(sig, 1.999999))[1] if sig < 2 else \
            ds.zeta(2.0) - 2 * ds.zeta(3.0) + ds.zeta(4.0)
        part = [0.0] * 10
        for n, v in a.items():
            for k, c in enumerate(unpack(v)):
                part[k] += c * n ** (-sig)
        for k in range(1, 9):
            rows.append({"sigma": sig, "k": k, "partial_G_k": part[k], "B^k": B ** k})
            ok &= part[k] <= B ** k + 1e-12
    dump("depth_partial_sums.json", rows)
    check("T07", "partial sums of G_k lie below B(sigma)^k", ok)
    # prime-coordinate statistics of minimal endpoints
    tot = sum(sum(unpack(v)) for v in a.values())
    stats = []
    for p in (2, 3, 5, 7, 11, 13):
        s = sum(sum(unpack(v)) * pdyn.val(n, p) for n, v in a.items())
        h = sum(sum(unpack(v)) for n, v in a.items() if n % p == 0)
        stats.append({"p": p, "mean_v_p": s / tot, "fraction_divisible": h / tot})
    dump("prime_coordinate_statistics.json", {"X": X, "words": tot, "rows": stats})
    return {"witnesses": wit, "tally": tally}


def analytic(letter):
    res = {}
    lo, hi, ok = ds.sigma_c()
    res["sigma_c"] = [lo, hi]
    check("T09", "enclosure B(lo) > 1 > B(hi), width 1e-8", ok, [lo, hi])
    drift = []
    ok = True
    for M in (2, 5, 10, 50, 200, 1000):
        for sig in (0.6, 1.0, 1.5464):
            B, d = pdyn.drift_table(M, sig)
            ok &= all(x > 0 for x in d.values())
            drift.append({"M": M, "sigma": sig, "B_M": B, "min_drift": min(d.values()),
                          "primes": len(d)})
    res["drift"] = drift
    check("T09", "mean prime-coordinate drift positive for all tested (M, sigma)", ok)
    res["restricted"] = []
    ok = True
    for M, sig, K in ((3, 1.0, 11), (6, 1.0, 7), (6, 1.5, 7)):
        G = pdyn.restricted_Gk(M, sig, K)
        B = sum((N / (N + 1) ** 2) ** sig for N in range(1, M + 1))
        ratios = [G[i + 1] / G[i] for i in range(len(G) - 1)]
        ok &= all(r <= B + 1e-12 for r in ratios) and ratios[-1] > ratios[0]
        res["restricted"].append({"M": M, "sigma": sig, "B_M": B, "G_k": G, "ratios": ratios})
    check("T09", "restricted ratios G_(k+1)/G_k increase toward B_M and stay below it", ok)
    res["saturation"] = [{"M": M, "sigma": s, "length": 200, "samples": 1000,
                          "rows": pdyn.saturation_experiment(M, s, 200, 1000)}
                         for M, s in ((3, 1.0), (6, 1.0))]
    r = res["saturation"][0]["rows"]
    check("T09", "illustration: good-continuation fraction grows with the warm-up length",
          r[-1]["good_fraction"] > r[0]["good_fraction"] and r[-1]["good_fraction"] > 0.5, r)
    # T05
    s = 3.0
    A = 1500
    direct = ds.G2_direct(s, A)
    rep = ds.G2_representation(s, 3000)
    tail = 1.02 / (2 * A ** 2) + 1.0 / A ** 5
    res["T05"] = {"s": s, "direct": direct, "representation": rep, "tail_bound": tail}
    check("T05", "depth-two representation equals direct double sum at s=3 within tail bound",
          -1e-12 <= rep - direct <= tail, res["T05"])
    part, corr, t = ds.kappa(2000000)
    res["kappa"] = {"partial_product": part, "tail_corrected": corr, "log_tail_estimate": t}
    c2 = ds.second_constant()
    rows = []
    for X in (10 ** 5, 10 ** 6, 10 ** 7) + ((10 ** 8,) if letter in "DE" else ()):
        c = ds.A2_count(X)
        residual = c / math.sqrt(X) - corr / 2 * math.log(X)
        rows.append({"X": X, "A_2": c, "residual": residual, "residual_minus_c": residual - c2,
                     "scaled_by_X^(1/6)": (residual - c2) * X ** (1 / 6)})
    res["second_constant"] = c2
    res["A2"] = rows
    gap = [x["residual_minus_c"] for x in rows]
    sc = [x["scaled_by_X^(1/6)"] for x in rows]
    check("T13", "A_2 residual approaches the independently computed constant c "
          "(gap decreases; gap*X^(1/6) within 10%)",
          all(abs(gap[i + 1]) < abs(gap[i]) for i in range(len(gap) - 1))
          and max(sc) <= 1.10 * min(sc) and min(sc) > 0, {"c": c2, "rows": rows})
    dump("analytic.json", res)


def generation():
    """Checks on the generative records and on the source-weighted architecture."""
    X = 100000
    rows, bad = [], 0
    for w, K, Q, E in gen.records(X):
        bad += gen.replay(K, w)[-1] != E or Q * K != E
        rows.append((" ".join(map(str, w)), len(w), K, Q.numerator, Q.denominator, E))
    rows.sort(key=lambda r: (r[5], r[1], [int(t) for t in r[0].split()]))
    gz_csv("generative_records_100000.csv.gz", ["word", "depth", "K", "Q_num", "Q_den", "E"], rows)
    check("T14", "every record (w,K,Q,E) with E <= 100000 replays by actual nesting",
          bad == 0, {"records": len(rows)})
    a, b = 2.0, 2.5                                   # Q^-a K^-b,  s = a,  u = b - a
    B = ds.zeta(2.0) - 2 * ds.zeta(3.0) + ds.zeta(4.0)
    part = {}
    for _, k, K, qn, qd, E in rows:
        part[k] = part.get(k, 0.0) + (qd / qn) ** a * K ** (-b)
    check("T14", "partial sums of F_k at (a,b)=(2,2.5) lie below B(2)^k",
          all(v <= B ** k + 1e-12 for k, v in part.items()))
    wit = gen.aggregation_witness(X)
    check("T14", "witness: distinct histories with equal depth, K and E",
          wit is not None and all(gen.replay(wit["K"], w)[-1] == wit["E"] for w in wit["words"]), wit)
    tops = [10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6, 10 ** 7]
    orbit = [{"X": X1, "histories_from_1": n, "log_ratio": math.log(n) / math.log(X1)}
             for X1, n in zip(tops, gen.orbit_counts(1, tops))]
    check("T15", "orbit counter agrees with the stored records with K = 1 up to 100000",
          orbit[2]["histories_from_1"] == sum(r[2] == 1 for r in rows))
    check("T15", "source-1 histories counted by forward generation (observed values recorded)",
          all(orbit[i]["histories_from_1"] < orbit[i + 1]["histories_from_1"] for i in range(4)),
          orbit)
    memo, ok, longest = {}, True, 0
    for p in range(2, 1000):
        if pdyn.factor(p) == {p: 1}:
            w = gen.prime_word(p, memo)
            ok &= gen.replay(1, w)[-1] % p == 0
            longest = max(longest, len(w))
    check("T15", "an admissible word from source 1 reaches every prime below 1000", ok,
          {"longest_word": longest})
    dump("generation.json", {"records_E_le_100000": len(rows), "aggregation_witness": wit,
                             "source_one_orbit": orbit, "longest_prime_word_below_1000": longest})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=list("ABCDE"), default="C")
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    t0 = time.time()
    suite = unittest.defaultTestLoader.discover(os.path.join(HERE, "tests"))
    r = unittest.TextTestRunner(stream=open(os.devnull, "w")).run(suite)
    check("tests", "%d unit tests (definition oracle and statements)" % r.testsRun,
          r.wasSuccessful(), [str(x[0]) for x in r.failures + r.errors])
    rec = pdyn.check_T03_T04(100000)
    check("T03", "recurrence vs definition lcm for all words with E <= 100000",
          rec["recurrence_mismatch"] == 0, rec)
    check("T04", "valuation recurrence and closed form for the same words",
          rec["valuation_mismatch"] == 0 and rec["closed_form_mismatch"] == 0, rec)
    generation()
    stages = "ABCDE"[: "ABCDE".index(args.stage) + 1]
    records = [stage(x)[0] for x in stages]
    controls = [gc.run_grammar(20000, n, g) for n, g in gc.grammars(20000).items()]
    b = gc.boundaries()
    for c in controls:
        c["sigma_c"] = b.get(c["grammar"])
    dump("controls.json", controls)
    check("T08/G", "nine control grammars: engines agree (X=20000)",
          all(c["engine_mismatches"] == 0 for c in controls))
    check("T08", "closed form 1/(1 - t sum p^-s) for every grammar with all q = 1",
          all(c.get("closed_form_mismatches", 0) == 0 for c in controls))
    analytic(args.stage)
    failed = sum(c["status"] != "PASS" for c in CHECKS)
    dump("verification.json", {"release": "ANS-I v001", "stages": stages,
                               "python": platform.python_version(), "platform": platform.system(),
                               "checks": CHECKS, "passed": len(CHECKS) - failed, "failed": failed,
                               "seconds": round(time.time() - t0, 1)})
    print("\n%d passed, %d failed, %.1f s" % (len(CHECKS) - failed, failed, time.time() - t0))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

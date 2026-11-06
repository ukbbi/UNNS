"""E41 (v007-1) -- the filling-dependence map J_X (GF(2)).
(a) the two v006 dependence witnesses: dim V_X, r_fill(X) = dim im J_X, kernel.
(b) the 202 E30 seed contents x the 12 off-diagonal patterns, X = K(A(K_P)) with K_P the minimal admissible m of the pattern: distribution of r_fill and its relation to 'the pattern survives'.
(c) m-scan: r_fill(X_m) for m = K_P * t, t=1..60, for both witnesses."""
import json, os, collections, time
from math import lcm
import _path
import jmap
from pk import PK
from E30_arith import denominators
P6, P7 = PK(6), PK(7)


def amask(D, m, n):
    return sum(1 << s for s in range(1, n) if m % D[s] == 0)


if __name__ == "__main__":
    t0 = time.time()
    out = {}
    wit = [([2, 3, 8, 9, 14, 15, 20], 33600), ([3, 8, 9, 14, 15, 20, 21], 793800)]
    out["witnesses"] = []
    for C, K in wit:
        r = jmap.J_rank(P6, P7, amask(denominators(C), K, 128), 3)
        out["witnesses"].append({"content": C, "m": K, **{k: v for k, v in r.items() if k not in ("basis", "keep")}})
        scan = {}
        D = denominators(C)
        for t in range(1, 61):
            rr = jmap.J_rank(P6, P7, amask(D, K * t, 128), 3)
            scan[t] = (rr["dim_V"], rr["r_fill"])
        out["witnesses"][-1]["scan_t_to_(dimV,r_fill)"] = scan
        print(C, out["witnesses"][-1]["dim_V"], out["witnesses"][-1]["r_fill"], "scan r values", sorted(set(v[1] for v in scan.values())), flush=True)
    lp = json.load(open(os.path.join(_path._vpath.V005S3, "CERTIFICATES", "lift_pairs.json")))
    pairs = [p for p in lp["pairs"] if not p["diagonal"]]
    for p in pairs:
        z = P7.bits(p["z3_faces"])
        p["Pset"] = [s for s in range(1, 128) if P7.pz(z) >> s & 1]
        p["fams"] = [sum(1 << s for s in f) for f in p["families"]]
    seeds = [tuple(r["content"]) for r in json.load(open(os.path.join(_path._vpath.V005S3, "RESULTS", "E30_arithmetic_census_L30.json")))["records"]]
    hist = collections.Counter()
    tab = collections.Counter()
    for C in seeds:
        D = denominators(list(C))
        for p in pairs:
            K = 1
            for s in p["Pset"]:
                K = lcm(K, D[s])
            A = amask(D, K, 128)
            if not all(f & ~A for f in p["fams"]):
                continue  # pattern does not survive at K
            r = jmap.J_rank(P6, P7, A, 3)
            hist[(r["dim_V"], r["r_fill"])] += 1
            tab[r["r_fill"]] += 1
    out["seed_census"] = {"survivng_pattern_instances": sum(tab.values()), "r_fill_hist": dict(tab), "(dimV,r_fill)_hist": {str(k): v for k, v in hist.items()}}
    print(out["seed_census"])
    out["seconds"] = round(time.time() - t0, 1)
    json.dump(out, open(os.path.join(_path.ROOT, "RESULTS", "E41_J_map.json"), "w"), indent=1)

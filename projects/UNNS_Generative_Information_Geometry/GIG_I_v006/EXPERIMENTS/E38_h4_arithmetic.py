"""E38 (v006-6) -- arithmetic search for a certified H_4 class (identity role map, GF(2)).  Seeds: the 202 seven-label contents with an H_3 hole regime (E30, Lmax=30).  Each seed is extended by an 8th (largest) label x in (max+1 .. XMAX).
For each of the off-diagonal second lifts L2 (E37 constructions) the test is exact: K = lcm_{I in P_L2} D(I); A = {I : D(I) | K}; L2 is a 4-cycle of K(A) by construction; it is a nonzero class iff it is NOT in the span of boundaries of
ALL 5-faces of P_8 with prefix sets in A.  By monotonicity of A(m) a regime m exists iff the test succeeds at m = K."""
import json, os, sys, time
from math import lcm
import _path
import fi
from E30_arith import denominators
import E37_h3_to_h4 as E37
P8 = E37.P8
XMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 40
LIM = int(sys.argv[2]) if len(sys.argv) > 2 else 10**9

LIFTS = []
for pair, i, j in [((0, 1), 0, 1), ((0, 1), 1, 0), ((0, 1), 0, 2)]:
    l2, _, _ = E37.second_lift(pair, i, j)
    Pm = [s for s in range(1, 256) if P8.pz(l2) >> s & 1]
    LIFTS.append({"pair": pair, "fill": [i, j], "bits": l2, "Pset": Pm})

if __name__ == "__main__":
    seeds = [tuple(r["content"]) for r in json.load(open(os.path.join(_path._vpath.V005S3, "RESULTS", "E30_arithmetic_census_L30.json")))["records"]]
    hits, tested, t0 = [], 0, time.time()
    for C in seeds:
        for x in range(max(C) + 1, XMAX + 1):
            if tested >= LIM:
                break
            D = denominators(list(C) + [x])
            for L in LIFTS:
                K = 1
                for s in L["Pset"]:
                    K = lcm(K, D[s])
                A = sum(1 << s for s in range(1, 256) if K % D[s] == 0)
                tested += 1
                if not fi.Bounder(P8, A, 4).contains(L["bits"]):
                    hits.append({"content": list(C) + [x], "pair": list(L["pair"]), "fill": L["fill"], "m": str(K)})
                    print("HIT", hits[-1], flush=True)
        if tested % 300 == 0:
            print("tested", tested, "hits", len(hits), round(time.time() - t0), "s", flush=True)
        if len(hits) >= 5:
            break
    json.dump({"tested": tested, "hits": hits, "XMAX": XMAX, "seconds": round(time.time() - t0, 1)}, open(os.path.join(_path.ROOT, "RESULTS", "E38_h4_arithmetic.json"), "w"), indent=1)
    print("done", tested, len(hits))

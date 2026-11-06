"""E44 (v007-4) -- (a) sandwich for r_fill:  lower <= r_fill <= beta_j(F_X), with lower = dim Z_j(F_X) - dim(Z_j(F_X) cap d C_{j+1}(G_X)), G_X = rho(X_singleton) (J-2: d in ker J_X => d = d rho(w), w admitted).
(b) the second lift: J_X for X = K(A(m)) in P_8 (j=4), kind first and last, for the 8 certified H_4 contents of v006 (E38/E40)."""
import json, os, collections
from math import lcm
import _path
import jmap, fi
from pk import PK
from E30_arith import denominators
P6, P7, P8 = PK(6), PK(7), None
r = 6


def amask(D, m, n):
    return sum(1 << s for s in range(1, n) if m % D[s] == 0)


def rho7(g):
    f = P7.FS[g]
    if (r,) in f:
        h = tuple(b for b in f if b != (r,))
        return P6.IDX[h] if h else None
    return None


def lower_bound(A, d=3):
    ids = jmap.first_ok_faces(P6, P7, d, A)
    Zb = jmap.kernel(P6, ids, d)
    # G_X: rho-images of admitted (d+1)-faces g of P7 with {r} singleton
    G = set()
    for g in range(len(P7.FS)):
        if P7.DIM[g] == d + 1 and not P7.PM[g] & ~A:
            x = rho7(g)
            if x is not None:
                G.add(x)
    bd = []
    for h in G:
        x = 0
        for b in P6.BND[h]:
            x ^= 1 << b
        bd.append(x)
    def rank(vs):
        piv, rk = {}, 0
        for v in vs:
            while v:
                hh = v.bit_length() - 1
                if hh in piv:
                    v ^= piv[hh]
                else:
                    piv[hh] = v
                    rk += 1
                    break
        return rk
    rB = rank(bd)
    rZ = len(Zb)
    rZB = rank(Zb + bd)
    return rZ - (rZ + rB - rZB)  # dim Z - dim(Z cap B)


if __name__ == "__main__":
    out = {}
    lp = json.load(open(os.path.join(_path._vpath.V005S3, "CERTIFICATES", "lift_pairs.json")))
    pairs = [p for p in lp["pairs"] if not p["diagonal"]]
    for p in pairs:
        z = P7.bits(p["z3_faces"])
        p["Pset"] = [s for s in range(1, 128) if P7.pz(z) >> s & 1]
        p["fams"] = [sum(1 << s for s in f) for f in p["families"]]
    seeds = [tuple(x["content"]) for x in json.load(open(os.path.join(_path._vpath.V005S3, "RESULTS", "E30_arithmetic_census_L30.json")))["records"]]
    hist = collections.Counter()
    for C in seeds:
        D = denominators(list(C))
        for p in pairs:
            K = 1
            for s in p["Pset"]:
                K = lcm(K, D[s])
            A = amask(D, K, 128)
            if not all(f & ~A for f in p["fams"]):
                continue
            rf = jmap.J_rank(P6, P7, A, 3)
            lb = lower_bound(A)
            hist[(lb, rf["r_fill"], rf["beta_facet"])] += 1
    out["sandwich_(lower,r_fill,beta)_hist"] = {str(k): v for k, v in sorted(hist.items())}
    out["sandwich_valid"] = all(k[0] <= k[1] <= k[2] for k in hist)
    print(out)
    # second lift
    P8 = PK(8)
    hits = json.load(open(os.path.join(_path._vpath.V006, "RESULTS", "E38_h4_arithmetic.json")))["hits"]
    out["second_lift"] = []
    for h in hits:
        D = denominators(h["content"])
        A = amask(D, int(h["m"]), 256)
        rf = jmap.J_rank(P7, P8, A, 4, "first")
        rl = jmap.J_rank(P7, P8, A, 4, "last")
        rec = {"content": h["content"], "m": h["m"], "first": {k: v for k, v in rf.items() if k not in ("basis", "keep")}, "last": {k: v for k, v in rl.items() if k not in ("basis", "keep")}}
        out["second_lift"].append(rec)
        print(rec, flush=True)
    json.dump(out, open(os.path.join(_path.ROOT, "RESULTS", "E44_sandwich_and_second_lift.json"), "w"), indent=1)

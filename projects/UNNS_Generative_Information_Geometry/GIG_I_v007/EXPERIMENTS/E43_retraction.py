"""E43 (v007-3) -- retraction and injectivity.  rho: C_*(P_{k+1}) -> C_*(P_k), rho(g) = g with rank r deleted if {r} is a singleton block of g, else 0 (dimension preserving).  Over GF(2) rho is a chain map: if r is not a singleton,
the two splits ({r}|U),(U|{r}) of r's block delete to the same face and cancel.  rho o first = id.  If rho maps the admitted cells of X into F_X (condition RET_j: g in X, {r} singleton => first(delete g) in X, in degrees j, j+1, j-1),
then first_* : H_j(F_X) -> H_j(X) is split injective and r_fill(X) = beta_j(F_X).
Checks: (1) rho chain map on all faces of P_7 -> P_6; rho o first = id; (2) RET_3 over the 310 surviving instances (and RET_2, RET_4); (3) r_fill = beta_3(F_X) wherever RET holds."""
import json, os, collections
from math import lcm
import _path
import jmap
import lift as Lf
from pk import PK
from E30_arith import denominators
P6, P7 = PK(6), PK(7)
r = 6


def rho(g):
    f = P7.FS[g]
    if ((r,),) == tuple(b for b in f if b == (r,)) or (r,) in f:
        h = tuple(b for b in f if b != (r,))
        return P6.IDX[h] if h else None
    return None


def amask(D, m, n):
    return sum(1 << s for s in range(1, n) if m % D[s] == 0)


if __name__ == "__main__":
    # (1) chain map check over all faces of P7 of dim 1..6 (rho of dim-0 faces: vertices; all included)
    ok = True
    for g in range(len(P7.FS)):
        lhs = 0
        for b in P7.BND[g]:
            x = rho(b)
            if x is not None:
                lhs ^= 1 << x
        x = rho(g)
        rhs = 0
        if x is not None:
            for b in P6.BND[x]:
                rhs ^= 1 << b
        ok &= lhs == rhs
    left_inverse = all(rho(P7.IDX[((r,),) + P6.FS[f]]) == f for f in range(len(P6.FS)))
    print("rho chain map:", ok, " rho o first = id:", left_inverse, flush=True)
    sing = {d: [(g, P7.PM[g], P7.PM[P7.IDX[((r,),) + P6.FS[rho(g)]]]) for g in range(len(P7.FS)) if P7.DIM[g] == d and rho(g) is not None] for d in (2, 3, 4)}
    lp = json.load(open(os.path.join(_path._vpath.V005S3, "CERTIFICATES", "lift_pairs.json")))
    pairs = [p for p in lp["pairs"] if not p["diagonal"]]
    for p in pairs:
        z = P7.bits(p["z3_faces"])
        p["Pset"] = [s for s in range(1, 128) if P7.pz(z) >> s & 1]
        p["fams"] = [sum(1 << s for s in f) for f in p["families"]]
    seeds = [tuple(x["content"]) for x in json.load(open(os.path.join(_path._vpath.V005S3, "RESULTS", "E30_arithmetic_census_L30.json")))["records"]]
    res = collections.Counter()
    bad_ret_but_equal = 0
    n = 0
    for C in seeds:
        D = denominators(list(C))
        for p in pairs:
            K = 1
            for s in p["Pset"]:
                K = lcm(K, D[s])
            A = amask(D, K, 128)
            if not all(f & ~A for f in p["fams"]):
                continue
            n += 1
            ret = {d: all(not pm & ~A <= 0 or True for (_, pm, _) in []) for d in ()}
            ret = {d: all((pm & ~A) != 0 or (pi & ~A) == 0 for (_, pm, pi) in sing[d]) for d in (2, 3, 4)}
            rf = jmap.J_rank(P6, P7, A, 3, "first")
            res[(ret[2], ret[3], ret[4], rf["r_fill"] == rf["beta_facet"])] += 1
    print(n, dict(res))
    json.dump({"rho_chain_map": ok, "rho_first_identity": left_inverse, "instances": n, "(RET2,RET3,RET4,r_fill==beta_facet)_hist": {str(k): v for k, v in res.items()}}, open(os.path.join(_path.ROOT, "RESULTS", "E43_retraction.json"), "w"), indent=1)

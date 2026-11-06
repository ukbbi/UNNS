"""E42 (v007-2) -- the facet theorem for J_X.  Since the boundary of this permutohedron splits blocks and the block {r} of first(g) is a singleton, d(first g)=first(d g) (S3, LT-0 proof): first is an injective CHAIN MAP of the
prefix complex F_X = K_k(A') (A' = {I : I u {r} in A}, requires {r} in A) onto a subcomplex of X = K_{k+1}(A).  Hence  V_X = Z_j(F_X)  and  J_X = first_* : H_j(F_X) -> H_j(X),  r_fill <= beta_j(F_X).
Checks: (1) chain-map identities for every face of P_5, P_6 (first and last); (2) over the 310 surviving pattern instances + the two witnesses: r_fill <= beta_3(F_X) and the values; same for last."""
import json, os, collections
from math import lcm
import _path
import jmap
from pk import PK
from E30_arith import denominators
P5, P6, P7 = PK(5), PK(6), PK(7)


def chain_map_check(Pk, Pk1):
    ok = True
    for g, f in enumerate(Pk.FS):
        for kind in ("first", "last"):
            img = lambda faces: Pk1.bits([Pk1.IDX[(((Pk.k,),) + x) if kind == "first" else (x + ((Pk.k,),))] for x in faces])
            lhs = 0
            for b in Pk1.BND[Pk1.IDX[(((Pk.k,),) + f) if kind == "first" else (f + ((Pk.k,),))]]:
                lhs ^= 1 << b
            rhs = img([Pk.FS[b] for b in Pk.BND[g]])
            ok &= lhs == rhs
    return ok


def amask(D, m, n):
    return sum(1 << s for s in range(1, n) if m % D[s] == 0)


if __name__ == "__main__":
    out = {"chain_map_P5_P6": chain_map_check(P5, P6), "chain_map_P6_P7": chain_map_check(P6, P7)}
    print(out)
    lp = json.load(open(os.path.join(_path._vpath.V005S3, "CERTIFICATES", "lift_pairs.json")))
    pairs = [p for p in lp["pairs"] if not p["diagonal"]]
    for p in pairs:
        z = P7.bits(p["z3_faces"])
        p["Pset"] = [s for s in range(1, 128) if P7.pz(z) >> s & 1]
        p["fams"] = [sum(1 << s for s in f) for f in p["families"]]
    seeds = [tuple(r["content"]) for r in json.load(open(os.path.join(_path._vpath.V005S3, "RESULTS", "E30_arithmetic_census_L30.json")))["records"]]
    rows = collections.Counter()
    viol = 0
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
            rf = jmap.J_rank(P6, P7, A, 3, "first")
            rl = jmap.J_rank(P6, P7, A, 3, "last")
            viol += (rf["r_fill"] > rf["beta_facet"]) + (rl["r_fill"] > rl["beta_facet"])
            rows[(rf["beta_facet"], rf["r_fill"], rl["beta_facet"], rl["r_fill"])] += 1
    out["instances"] = n
    out["violations_of_r<=beta_facet"] = viol
    out["(beta_first,r_first,beta_last,r_last)_hist"] = {str(k): v for k, v in sorted(rows.items())}
    print(out)
    json.dump(out, open(os.path.join(_path.ROOT, "RESULTS", "E42_facet_theorem.json"), "w"), indent=1)

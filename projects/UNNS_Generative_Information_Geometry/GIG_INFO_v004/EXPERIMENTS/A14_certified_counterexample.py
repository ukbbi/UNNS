"""A14 -- certified counterexample to the sufficiency of (Q,S2) outside the arithmetic class: two prefix-family systems on six labels with equal (N,h1,Q,S2), beta2=1 vs beta2=0, re-derived with definition-level code."""
import json, os
import numpy as np
import _path, v2, geomk
import graph_direct as gd
import history_complex as hc

PERMS = hc.perms(6)

def perms_of(mask):
    return [PERMS[i] for i in range(720) if mask >> i & 1]

if __name__ == "__main__":
    R = os.path.join(_path.ROOT, "RESULTS")
    meta = json.load(open(os.path.join(R, "A15_stronger_signatures.json")))["PF"]["(N,h1,Q,S2)"]["smallest"]
    mp, mn = int(meta["mask_pos"], 16), int(meta["mask_neg"], 16)
    pc = v2.pair_cert
    out = {}
    Ap, An = perms_of(mp), perms_of(mn)
    # is either mask a regime of the arithmetic census (any six-label content in D)?
    census_masks = {r[3] for r in v2.census.enumerate_regimes()}
    out["positive_mask_is_arithmetic_census_regime"] = mp in census_masks
    out["negative_mask_is_arithmetic_census_regime"] = mn in census_masks
    # prefix-family check: the system is exactly the set of orderings whose five prefix sets lie in the family of its own prefix sets
    def prefix_closed(A):
        S = set(A); fam = set()
        for p in A:
            m = 0
            for x in p[:-1]:
                m |= 1 << x; fam.add(m)
        import itertools
        return all(p in S for p in PERMS if all(sum(1 << x for x in p[:j]) in fam for j in range(1, 6)))
    out["positive_is_prefix_family_system"], out["negative_is_prefix_family_system"] = prefix_closed(Ap), prefix_closed(An)
    for tag, A, m in (("positive", Ap, mp), ("negative", An, mn)):
        prof = gd.profile(A)
        by = pc.complex_of(A)
        rec = {k: prof[k] for k in ("N", "E", "sq", "Ss2", "Sds", "Sd2", "SB2", "SB22", "h1", "hq", "h2", "T1_identity_holds_at_every_vertex")}
        rec.update({"mask_hex": hex(m), "f_vector": [len(by.get(d, [])) for d in range(6)], "beta2_rank_route": pc.betti2_by_ranks(by)[0], "beta2_column_route": pc.betti2_by_ranks(by)[1], "betti_hc_engine": list(hc.betti(m, 6))})
        out[tag] = rec
    P, Nn = out["positive"], out["negative"]
    out["equal_N_h1_Q_S2"] = all(P[k] == Nn[k] for k in ("N", "h1", "sq", "Ss2"))
    out["h2_differs"] = P["h2"] != Nn["h2"]
    out["Sds_equal"] = P["Sds"] == Nn["Sds"]
    by = pc.complex_of(Ap)
    zi, pi = pc.find_certificate(by)
    z = [by[2][i] for i in zi]; phi = [by[2][i] for i in pi]
    out["positive"]["certificate"] = {"cycle_2faces": len(z), "cochain_2faces": len(phi), "verified": pc.verify(Ap, z, phi), "cycle": [[list(b) for b in f] for f in z], "cochain": [[list(b) for b in f] for f in phi]}
    out["negative"]["certificate_exists"] = pc.find_certificate(pc.complex_of(An)) is not None
    json.dump(out, open(os.path.join(_path.ROOT, "CERTIFICATES", "counterexample_PF_N_h1_Q_S2.json"), "w"))
    print({k: v for k, v in out.items() if k not in ("positive", "negative")}); print({k: v for k, v in P.items() if k != "certificate"}); print(Nn)

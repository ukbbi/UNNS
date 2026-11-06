"""F15 -- certificates for the sharp witness: content (2,4,5,9,14,15), sources 2520 (beta_2>0) and 3780 (beta_2=0): equal N, equal h1, equal hq, different h2."""
import json, os, hashlib
import _path, v2
import graph_direct as gd
import history_complex as hc

CONTENT, M_POS, M_NEG = (2, 4, 5, 9, 14, 15), 2520, 3780
pc = v2.pair_cert

if __name__ == "__main__":
    out = {"content": list(CONTENT), "positive_source": M_POS, "negative_source": M_NEG}
    A = {}
    for tag, m0 in (("positive", M_POS), ("negative", M_NEG)):
        A[tag] = pc.admissible_orderings(CONTENT, m0)
        by = pc.complex_of(A[tag])
        mask = hc.vertex_mask(A[tag], 6)
        rec = gd.profile(A[tag])
        rec.update({"source": m0, "mask_sha256": hashlib.sha256(str(mask).encode()).hexdigest(), "f_vector": [len(by.get(d, [])) for d in range(6)],
                    "beta2_rank_route": pc.betti2_by_ranks(by)[0], "beta2_column_route": pc.betti2_by_ranks(by)[1], "betti_hc_engine": list(hc.betti(mask, 6))})
        out[tag] = rec
    P, Nn = out["positive"], out["negative"]
    out["equalities"] = {k: P[k] == Nn[k] for k in ("N", "E", "sq", "h1", "hq", "SB2", "Sd2")}
    out["inequalities"] = {k: P[k] != Nn[k] for k in ("h2", "SB22")}
    by = pc.complex_of(A["positive"])
    zi, pi = pc.find_certificate(by)
    z = [by[2][i] for i in zi]; phi = [by[2][i] for i in pi]
    ok, msg = pc.verify(A["positive"], z, phi)
    out["positive"]["certificate"] = {"cycle_2faces": len(z), "cochain_2faces": len(phi), "verified": ok, "message": msg, "cycle": [[list(b) for b in f] for f in z], "cochain": [[list(b) for b in f] for f in phi]}
    out["negative"]["certificate_exists"] = pc.find_certificate(pc.complex_of(A["negative"])) is not None
    json.dump(out, open(os.path.join(_path.ROOT, "CERTIFICATES", "witness_2520_3780.json"), "w"), indent=0)
    print(out["equalities"], out["inequalities"])
    for t in ("positive", "negative"):
        print(t, {k: v for k, v in out[t].items() if k not in ("certificate", "h1", "hq", "h2")}, out[t].get("certificate", {}).get("verified"))
    print("h2 pos", P["h2"]); print("h2 neg", Nn["h2"])

"""E12 -- certificates for the representative same-content pair: content (2,3,4,5,8,15), sources 480 (beta_2=1) and 800 (beta_2=0), both N=396."""
import json, os, hashlib
import _path
import pair_cert as pc
import history_complex as hc

CONTENT, M_POS, M_NEG = (2, 3, 4, 5, 8, 15), 480, 800

def system(m0):
    A = pc.admissible_orderings(CONTENT, m0)
    by = pc.complex_of(A)
    return A, by

if __name__ == "__main__":
    out = {"content": list(CONTENT), "pair": {"positive_source": M_POS, "negative_source": M_NEG}}
    for tag, m0 in (("positive", M_POS), ("negative", M_NEG)):
        A, by = system(m0)
        mask = hc.vertex_mask(A, 6)
        b_ranks = pc.betti2_by_ranks(by)
        out[tag] = {"source": m0, "N": len(A), "mask_sha256": hashlib.sha256(str(mask).encode()).hexdigest(),
                    "f_vector": [len(by.get(d, [])) for d in range(6)], "beta2_rank_route": b_ranks[0], "beta2_column_route": b_ranks[1],
                    "betti_hc_engine": list(hc.betti(mask, 6)), "f_vector_hc_engine": list(hc.f_vector(mask, 6))}
    A, by = system(M_POS)
    zi, pi = pc.find_certificate(by)
    z = [by[2][i] for i in zi]; phi = [by[2][i] for i in pi]
    ok, msg = pc.verify(A, z, phi)
    out["positive"]["certificate"] = {"cycle_2faces": len(z), "cochain_2faces": len(phi), "verified": ok, "message": msg,
                                      "cycle": [[list(b) for b in f] for f in z], "cochain": [[list(b) for b in f] for f in phi]}
    # negative: the SAME z, phi cannot be transported; and the negative system has no certificate
    A2, by2 = system(M_NEG)
    out["negative"]["certificate_exists"] = pc.find_certificate(by2) is not None
    out["N_equal"] = out["positive"]["N"] == out["negative"]["N"]
    out["arithmetic_check"] = {"orderings_positive_source": len(A), "orderings_negative_source": len(A2)}
    json.dump(out, open(os.path.join(_path.ROOT, "CERTIFICATES", "pair_480_800.json"), "w"), indent=0)
    print({k: v for k, v in out.items() if k not in ("positive", "negative")}); 
    for t in ("positive", "negative"):
        print(t, {k: v for k, v in out[t].items() if k != "certificate"}, out[t].get("certificate", {}).get("verified"))

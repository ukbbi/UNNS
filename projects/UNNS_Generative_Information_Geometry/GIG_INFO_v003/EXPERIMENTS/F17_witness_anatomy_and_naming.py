"""F17 -- anatomy of the sharp witness (how different are the two arrangement sets?) and the v002 naming correction for E_distinct."""
import json, os
import _path, v2
import graph_direct as gd

if __name__ == "__main__":
    pc = v2.pair_cert
    C = (2, 4, 5, 9, 14, 15)
    Ap, An = set(pc.admissible_orderings(C, 2520)), set(pc.admissible_orderings(C, 3780))
    cert = json.load(open(os.path.join(_path.ROOT, "CERTIFICATES", "witness_2520_3780.json")))
    byp, byn = pc.complex_of(Ap), pc.complex_of(An)
    f3p, f3n = set(byp[3]), set(byn[3])
    out = {"arrangements_only_in_positive": len(Ap - An), "arrangements_only_in_negative": len(An - Ap), "common_arrangements": len(Ap & An),
           "3faces_only_in_positive": len(f3p - f3n), "3faces_only_in_negative": len(f3n - f3p), "2faces_equal_sets": set(byp[2]) == set(byn[2]) , "2faces_only_in_positive": len(set(byp[2]) - set(byn[2])), "2faces_only_in_negative": len(set(byn[2]) - set(byp[2])),
           "positive_cycle_2faces": cert["positive"]["certificate"]["cycle_2faces"]}
    REGS = v2.census.enumerate_regimes()
    masks = [r[3] for r in REGS]
    out["naming_correction"] = {"v002_E_distinct_size": len(set(masks)), "distinct_labelled_arrangement_sets_(content,mask)": len({(r[0], r[3]) for r in REGS}), "regimes": len(REGS),
                                "statement": "v002 E_distinct is uniform over distinct RANK-INDEXED MASKS (219,146); distinct labelled arrangement sets number 346,859 (every regime). Numbers in v002 are reproducible and unchanged; only the label is corrected."}
    json.dump(out, open(os.path.join(_path.ROOT, "RESULTS", "F17_witness_anatomy.json"), "w"), indent=1)
    print(out)

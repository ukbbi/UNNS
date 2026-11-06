"""F14 -- the sharp witness: a positive and a negative regime with IDENTICAL (N, h1) -- hence equal N, edge count, degree sequence, Sigma d^2 -- but different h2 (hence different Sigma|B2|^2), preferably in the same content and also identical commuting-square profile hq."""
import json, os
import numpy as np
import _path, v2

F = dict(np.load(os.path.join(_path.ROOT, "RESULTS", "features_all.npz")))
Y = (F["beta2"] > 0)
if __name__ == "__main__":
    REGS = v2.census.enumerate_regimes()
    out = {}
    def key(i, names): return tuple(int(x) for k in names for x in np.atleast_1d(F[k][i]))
    for tag, names in (("equal_N_h1", ["N", "hd"]), ("equal_N_h1_hq", ["N", "hd", "hq"])):
        groups = {}
        for i in range(len(Y)):
            if F["N"][i] in POSN if False else True:
                pass
        # restrict to classes containing a positive
        posk = {}
        for i in np.nonzero(Y)[0]:
            posk.setdefault(key(i, names), []).append(int(i))
        cand = []
        for i in range(len(Y)):
            if not Y[i]:
                k = key(i, names)
                if k in posk:
                    for p in posk[k]:
                        cand.append((p, i))
        same = [(p, q) for p, q in cand if REGS[p][0] == REGS[q][0]]
        out[tag] = {"positive_negative_pairs": len(cand), "positives_involved": len({p for p, _ in cand}), "same_content_pairs": len(same), "positives_with_same_content_partner": len({p for p, _ in same}),
                    "all_pairs_differ_in_h2": all(not (F["hb"][p] == F["hb"][q]).all() for p, q in cand), "all_pairs_differ_in_SB22": all(F["SB22"][p] != F["SB22"][q] for p, q in cand),
                    "pairs_equal_SB2": sum(int(F["SB2"][p] == F["SB2"][q]) for p, q in cand), "pairs_equal_sq": sum(int(F["sq"][p] == F["sq"][q]) for p, q in cand)}
        same.sort(key=lambda pq: (F["N"][pq[0]], pq))
        out[tag]["first_same_content_pairs"] = [{"content": list(REGS[p][0]), "L_pos": int(REGS[p][1]), "L_neg": int(REGS[q][1]), "N": int(F["N"][p]), "idx": [p, q]} for p, q in same[:5]]
    json.dump(out, open(os.path.join(_path.ROOT, "RESULTS", "F14_sharp_witness.json"), "w"), indent=1)
    print(json.dumps(out, indent=0)[:3500])

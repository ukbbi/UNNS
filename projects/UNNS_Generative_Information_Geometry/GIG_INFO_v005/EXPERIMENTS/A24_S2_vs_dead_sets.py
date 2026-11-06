"""A24 -- in census D, classes with equal (N,h1,Q,Sds) containing both beta2>0 and beta2=0 regimes: compare S2 and the dead-set structure of positives vs negatives."""
import json, os
from collections import Counter
import numpy as np
import _path, v2, nerve

if __name__ == "__main__":
    REGS = v2.census.enumerate_regimes()
    F = dict(np.load(os.path.join(_path._vpath.PATHS["INFO003"], "RESULTS", "features_all.npz")))
    n = len(F["N"]); Y = F["beta2"] > 0
    M = np.concatenate([F["N"].reshape(n, 1), F["hd"], F["sq"].reshape(n, 1), F["Sds"].reshape(n, 1)], axis=1)
    _, inv = np.unique(M, axis=0, return_inverse=True); inv = inv.reshape(-1)
    size = np.bincount(inv); pos = np.bincount(inv, weights=Y)
    mixed = np.nonzero((pos > 0) & (pos < size))[0]
    out = []
    for c in mixed:
        ids = np.nonzero(inv == c)[0]
        P = [i for i in ids if Y[i]]; Nn = [i for i in ids if not Y[i]]
        def prof(i):
            D = nerve.dead_sets(REGS[i][3])
            return {"idx": int(i), "content": list(REGS[i][0]), "L": int(REGS[i][1]), "S2": int(F["Ss2"][i]), "|D|": len(D), "D_by_size": dict(sorted(Counter(bin(x).count("1") for x in D).items())), "b1_nerve": nerve.nerve_betti(D, 1)[1] if D else 0}
        out.append({"class_N": int(F["N"][ids[0]]), "Q": int(F["sq"][ids[0]]), "Sds": int(F["Sds"][ids[0]]), "positives": [prof(i) for i in P], "negatives": [prof(i) for i in Nn[:6]], "n_neg": len(Nn),
                    "S2_pos_minus_neg": sorted({int(F["Ss2"][i] - F["Ss2"][j]) for i in P for j in Nn})})
    # direction
    diffs = [d for o in out for d in o["S2_pos_minus_neg"]]
    res = {"mixed_classes": len(out), "S2_difference_signs": {"pos>neg": int(sum(d > 0 for d in diffs)), "pos<neg": int(sum(d < 0 for d in diffs)), "equal": int(sum(d == 0 for d in diffs))}, "classes": out}
    json.dump(res, open(os.path.join(_path.ROOT, "RESULTS", "A24_S2_vs_dead_sets.json"), "w"), indent=1)
    print(res["mixed_classes"], res["S2_difference_signs"])
    for o in out:
        print(o["class_N"], o["Q"], o["Sds"], "S2diff", o["S2_pos_minus_neg"], "| pos D", [(p["|D|"], p["D_by_size"]) for p in o["positives"]][:2], "| neg D", [(p["|D|"], p["D_by_size"]) for p in o["negatives"]][:3])

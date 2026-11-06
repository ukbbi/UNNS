"""Utility: recover the masks of all 290 positives (158 in census D, 132 in held-out H6) by deterministic regeneration, verifying order against stored L and N."""
import json, os
import numpy as np
import _path, v2
import source_filtration as sf

def load_positives():
    REGS = v2.census.enumerate_regimes()
    F = dict(np.load(os.path.join(_path._vpath.PATHS["INFO003"], "RESULTS", "features_all.npz")))
    out = []
    for i in np.nonzero(F["beta2"] > 0)[0]:
        out.append({"src": "D", "idx": int(i), "content": tuple(REGS[i][0]), "L": int(REGS[i][1]), "N": int(F["N"][i]), "mask": REGS[i][3]})
    H = dict(np.load(os.path.join(_path._vpath.PATHS["INFO003"], "RESULTS", "H6_features.npz")))
    S = json.load(open(os.path.join(_path._vpath.PATHS["INFO003"], "RESULTS", "H6_summary.json")))
    pos = set(int(i) for i in np.nonzero(H["beta2"] > 0)[0])
    j = 0; seen = 0
    for c in S["contents"]:
        c = tuple(c)
        for r in sf.regimes(c):
            if j in pos:
                assert int(H["L"][j]) == r["L"] and int(H["N"][j]) == r["N"], (j, c)
                out.append({"src": "H6", "idx": j, "content": c, "L": r["L"], "N": r["N"], "mask": r["mask"]})
            j += 1
    assert j == len(H["N"])
    return out, F, REGS

if __name__ == "__main__":
    P, F, R = load_positives()
    print(len(P), sum(p["src"] == "D" for p in P))

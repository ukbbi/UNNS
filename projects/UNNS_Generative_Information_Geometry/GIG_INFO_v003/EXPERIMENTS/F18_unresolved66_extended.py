"""F18 -- for the 66 positives unresolved by (N,h1): which added second-order sum resolves them (extended pool of v003 features)."""
import json, os
import numpy as np
import _path
import F11_minimal_signatures as f11
if __name__ == "__main__":
    F = f11.F
    res = json.load(open(os.path.join(_path.ROOT, "RESULTS", "F11_minimal_signatures.json")))
    unres = res["unresolved_indices"]
    H1 = np.concatenate([F["N"].reshape(-1, 1), F["hd"]], axis=1)
    _, inv = np.unique(H1, axis=0, return_inverse=True); inv = inv.reshape(-1)
    Y = f11.Y
    out = {}
    for extra in ["sq", "hx", "Sq2", "Ss2", "Sds", "Sdq", "Ssq", "SB2", "SB22", "f3"]:
        cnt = 0
        for i in unres:
            same = (inv == inv[i]) & (Y == 0)
            cnt += bool((F[extra][same] == F[extra][i]).any())
        out[extra] = {"still_colliding": cnt, "resolved": len(unres) - cnt}
    json.dump(out, open(os.path.join(_path.ROOT, "RESULTS", "F18_unresolved66.json"), "w"), indent=1)
    print(out)

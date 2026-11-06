"""A11 -- the positives that the weaker signature (Q, sum d*s) leaves in mixed classes, and the (N,h1,Sds) analogue; resolved by S2?  On D, H6, and D u H6."""
import json, os
import numpy as np
import _path, v2
from B10_information_profiles import load, cat

def hidden(F, names):
    n = len(F["N"]); Y = (F["beta2"] > 0)
    M = np.concatenate([F[k].reshape(n, -1) for k in names], axis=1)
    _, inv = np.unique(M, axis=0, return_inverse=True); inv = inv.reshape(-1)
    size = np.bincount(inv); pos = np.bincount(inv, weights=Y)
    mixed = (pos > 0) & (pos < size)
    return np.nonzero(Y & mixed[inv])[0], inv

if __name__ == "__main__":
    D, H6 = load("features_all.npz"), load("H6_features.npz")
    P = cat(D, H6)
    REGS = v2.census.enumerate_regimes()
    out = {}
    for tag, F in (("D", D), ("H6", H6), ("D_union_H6", P)):
        rec = {}
        for nm, names in {"(Q,Sds)": ["sq", "Sds"], "(N,h1,Sds)": ["N", "hd", "Sds"], "(N,h1,Q)": ["N", "hd", "sq"], "(Q,S2)": ["sq", "Ss2"], "(Q,Ssq)": ["sq", "Ssq"], "(Q,Sd2)": ["sq", "Sd2"]}.items():
            h, inv = hidden(F, names)
            rec[nm] = {"hidden_positives": int(len(h))}
        out[tag] = rec
    # detail on the seven (N,h1,Sds) hidden positives in D
    h, inv = hidden(D, ["N", "hd", "Sds"])
    det = []
    Y = D["beta2"] > 0
    for i in h:
        partners = np.nonzero((inv == inv[i]) & (~Y))[0]
        det.append({"idx": int(i), "content": list(REGS[i][0]), "L": int(REGS[i][1]), "N": int(D["N"][i]), "Q": int(D["sq"][i]), "S2": int(D["Ss2"][i]), "Sds": int(D["Sds"][i]), "beta2": int(D["beta2"][i]),
                    "negative_partners": [{"content": list(REGS[j][0]), "L": int(REGS[j][1]), "Q": int(D["sq"][j]), "S2": int(D["Ss2"][j])} for j in partners[:4]], "S2_differs_from_all_partners": bool(all(D["Ss2"][j] != D["Ss2"][i] for j in partners))})
    out["seven_detail_D"] = det
    json.dump(out, open(os.path.join(_path.ROOT, "RESULTS", "A11_seven_hard_positives.json"), "w"), indent=1)
    print({k: v for k, v in out.items() if k != "seven_detail_D"})
    for x in det: print(x["content"], x["L"], x["N"], x["Q"], x["S2"], x["S2_differs_from_all_partners"], [(p["content"] == x["content"], p["S2"]) for p in x["negative_partners"]])

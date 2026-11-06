"""H22 -- (a) what the failed S_A classes look like; (b) non-triviality (singleton-class positives, permutation null within N) for the signatures that held, on D u H6."""
import json, os
import numpy as np
import _path
from H21_evaluate import load, cat, R

if __name__ == "__main__":
    D, H6 = load(os.path.join(R, "features_all.npz")), load(os.path.join(R, "H6_features.npz"))
    P = cat(D, H6)
    n = len(P["N"]); Y = (P["beta2"] > 0).astype(np.int8)
    src = np.array([0] * len(D["N"]) + [1] * len(H6["N"]))
    def cls(names):
        M = np.concatenate([P[k].reshape(n, -1) for k in names], axis=1)
        return np.unique(M, axis=0, return_inverse=True)[1].reshape(-1)
    out = {}
    inv = cls(["N", "SB22"])
    size = np.bincount(inv); pos = np.bincount(inv, weights=Y)
    badc = np.nonzero((pos > 0) & (pos < size))[0]
    ex = []
    for c in badc:
        ix = np.nonzero(inv == c)[0]
        pi = [int(i) for i in ix if Y[i]]; ni = [int(i) for i in ix if not Y[i]]
        ex.append({"N": int(P["N"][ix[0]]), "SB22": int(P["SB22"][ix[0]]), "positives": len(pi), "negatives": len(ni), "positive_sources": [int(P["L"][i]) for i in pi][:3], "negative_sources": [int(P["L"][i]) for i in ni][:3],
                   "differ_in_sq": bool(len({int(P["sq"][i]) for i in ix}) > 1), "differ_in_Ss2": bool(len({int(P["Ss2"][i]) for i in ix}) > 1), "differ_in_hd": bool(len({tuple(P["hd"][i]) for i in ix}) > 1), "from_H6": bool(src[ix].max())})
    out["S_A_mixed_classes"] = ex
    rng = np.random.default_rng(20261110)
    byN = {}
    for i, v in enumerate(P["N"]):
        byN.setdefault(int(v), []).append(i)
    posN = {k: int(Y[ix].sum()) for k, ix in byN.items() if Y[ix].sum()}
    for nm, names in {"S_B (sq,Ss2)": ["sq", "Ss2"], "S_C (Sd2,Ss2)": ["Sd2", "Ss2"], "(N,h1,h2)": ["N", "hd", "hb"]}.items():
        inv = cls(names); size = np.bincount(inv); pos = np.bincount(inv, weights=Y)
        pure = (pos == size) & (pos > 0)
        rec = {"positives_alone_in_class": int(pos[pure & (size == 1)].sum()), "positives_in_pure_classes_size_ge2": int(pos[pure & (size > 1)].sum()), "largest_pure_positive_class": int(size[pure].max())}
        nulls = []
        for _ in range(100):
            y = np.zeros(n, dtype=np.int8)
            for k, c in posN.items():
                y[rng.choice(byN[k], c, replace=False)] = 1
            p2 = np.bincount(inv, weights=y)
            m = (p2 > 0) & (p2 < size)
            nulls.append(int(p2[m].sum()))
        rec["null_positives_in_mixed_classes"] = {"min": min(nulls), "mean": float(np.mean(nulls)), "max": max(nulls), "of_positives": int(Y.sum())}
        out[nm] = rec
        print(nm, rec, flush=True)
    json.dump(out, open(os.path.join(R, "H22_heldout_diagnostics.json"), "w"), indent=1)
    print(json.dumps(out["S_A_mixed_classes"]))

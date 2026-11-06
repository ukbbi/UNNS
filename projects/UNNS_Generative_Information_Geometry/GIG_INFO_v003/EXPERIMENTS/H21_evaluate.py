"""H21 -- evaluate the pre-registered predictions P1, P2 on the held-out sets (and the exploratory H7)."""
import json, os, sys
import numpy as np
import _path

R = os.path.join(_path.ROOT, "RESULTS")
SIGS = {"S_A (N,SB22)": ["N", "SB22"], "S_B (sq,Ss2)": ["sq", "Ss2"], "S_C (Sd2,Ss2)": ["Sd2", "Ss2"], "(N,h1)": ["N", "hd"], "(N,h1,hq)": ["N", "hd", "hq"], "(N,h1,h2)": ["N", "hd", "hb"], "N": ["N"], "f1,sq,hx": ["N", "E", "sq", "hx"]}
WID = {"hd": 8, "hq": 16, "hb": 60, "hdq": 0}


def load(path):
    d = dict(np.load(path))
    for k, w in WID.items():
        if k in d and w:
            x = d[k]
            d[k] = x[:, :w] if x.shape[1] >= w else np.pad(x, ((0, 0), (0, w - x.shape[1])))
    return d


def mixed(F, names):
    n = len(F["N"])
    Y = (F["beta2"] > 0).astype(np.int8)
    M = np.concatenate([F[k].reshape(n, -1) for k in names], axis=1)
    _, inv = np.unique(M, axis=0, return_inverse=True)
    inv = inv.reshape(-1)
    size = np.bincount(inv); pos = np.bincount(inv, weights=Y)
    m = (pos > 0) & (pos < size)
    return {"classes": int(len(size)), "mixed_classes": int(m.sum()), "positives_in_mixed": int(pos[m].sum()), "positives": int(Y.sum()), "regimes": n}


def cat(a, b):
    return {k: np.concatenate([a[k], b[k]]) for k in a if k in b}


if __name__ == "__main__":
    out = {}
    D = load(os.path.join(R, "features_all.npz"))
    if os.path.exists(os.path.join(R, "H6_features.npz")):
        H6 = load(os.path.join(R, "H6_features.npz"))
        P = cat(D, H6)
        out["H6_alone"] = {n: mixed(H6, s) for n, s in SIGS.items()}
        out["D_union_H6"] = {n: mixed(P, s) for n, s in SIGS.items()}
        ok = all(out[w][n]["mixed_classes"] == 0 for w in ("H6_alone", "D_union_H6") for n in ("S_A (N,SB22)", "S_B (sq,Ss2)", "S_C (Sd2,Ss2)"))
        out["P1_confirmed"] = ok
        out["P2_confirmed"] = out["D_union_H6"]["(N,h1)"]["positives_in_mixed"] > 0
    if os.path.exists(os.path.join(R, "H7_features.npz")):
        H7 = load(os.path.join(R, "H7_features.npz"))
        out["H7_alone_exploratory"] = {n: mixed(H7, s) for n, s in SIGS.items()}
    json.dump(out, open(os.path.join(R, "H21_evaluation.json"), "w"), indent=1)
    print(json.dumps(out, indent=0)[:4000])

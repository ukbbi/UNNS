"""B10 -- Experiment B: exact information recovered about Y=1[beta2>0] by N, radius-1 and radius-2 observations, natural and balanced ensembles, from the stored census (D) and held-out (H6) records; plus an out-of-sample (train D -> test H6) predictive check."""
import json, os, sys
import numpy as np
import _path, ent2

R3 = os.path.join(_path._vpath.PATHS["INFO003"], "RESULTS")
WID = {"hd": 8, "hq": 16, "hb": 60}


def load(name):
    d = dict(np.load(os.path.join(R3, name)))
    for k, w in WID.items():
        x = d[k]
        d[k] = x[:, :w] if x.shape[1] >= w else np.pad(x, ((0, 0), (0, w - x.shape[1])))
    return d


def cat(a, b):
    return {k: np.concatenate([a[k], b[k]]) for k in a if k in b}


OBS = {"none": [], "N": ["N"], "(N,h1)": ["N", "hd"], "(N,h1,hq)": ["N", "hd", "hq"], "(N,h1,Q)": ["N", "hd", "sq"], "(Q,S2)": ["sq", "Ss2"], "(N,h1,Q,S2)": ["N", "hd", "sq", "Ss2"], "(N,h1,h2)": ["N", "hd", "hb"], "(N,E,Q,hx)=f0..f2": ["N", "E", "sq", "hx"]}


def sigs(F, names):
    n = len(F["N"])
    if not names:
        return [0] * n
    M = np.concatenate([F[k].reshape(n, -1) for k in names], axis=1)
    _, inv = np.unique(M, axis=0, return_inverse=True)
    return inv.reshape(-1).tolist()


def ensemble_table(F, tag):
    Y = (F["beta2"] > 0).astype(int).tolist()
    out = {"systems": len(Y), "positives": sum(Y)}
    for mode in ("natural", "balanced"):
        out[mode] = {o: ent2.profile(Y, sigs(F, names), mode, 30) for o, names in OBS.items()}
    return out


if __name__ == "__main__":
    D, H6 = load("features_all.npz"), load("H6_features.npz")
    P = cat(D, H6)
    res = {"D": ensemble_table(D, "D"), "H6": ensemble_table(H6, "H6"), "D_union_H6": ensemble_table(P, "P")}
    for k, v in res.items():
        print(k, v["systems"], v["positives"])
        for mode in ("natural", "balanced"):
            print("  ", mode, {o: (p["H(Y|O)"][:7], p["I(Y;O)"][:7]) for o, p in v[mode].items()})
    json.dump(res, open(os.path.join(_path.ROOT, "RESULTS", "B10_information_profiles.json"), "w"), indent=1)

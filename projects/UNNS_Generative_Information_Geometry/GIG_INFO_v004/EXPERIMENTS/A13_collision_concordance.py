"""A13 -- collision concordance: for each domain and signature, over all ORDERED pairs (i,j), i != j, of systems with identical signature and Y_i=1: the fraction with Y_j=1 (partner-positive rate),
compared with the domain base rate P(Y=1) and with the rate among pairs matched only on N.  A structural separation shows partner-positive rate >> base rate; zero mixed classes in a sparse sample need not."""
import json, os, sys
import numpy as np
import _path
from B10_information_profiles import load, cat

R4 = os.path.join(_path.ROOT, "RESULTS")


def stats(F, names, tag):
    n = len(F["N"]); Y = (F["beta2"] > 0).astype(int)
    M = np.concatenate([F[k].reshape(n, -1) for k in names], axis=1)
    _, inv = np.unique(M, axis=0, return_inverse=True); inv = inv.reshape(-1)
    size = np.bincount(inv); pos = np.bincount(inv, weights=Y)
    # ordered pairs with Y_i=1: partners j != i
    partners = (size[inv] - 1)[Y == 1].sum()
    pos_partners = (pos[inv] - 1)[Y == 1].sum()
    return {"positive_systems_with_a_partner": int(((size[inv] > 1) & (Y == 1)).sum()), "positives": int(Y.sum()), "ordered_pairs_from_positives": int(partners), "partner_positive_rate": float(pos_partners / partners) if partners else None, "base_rate": float(Y.mean())}


if __name__ == "__main__":
    out = {}
    D, H6 = load("features_all.npz"), load("H6_features.npz")
    doms = {"AR (census u H6)": cat(D, H6)}
    for tag in ("VS", "PF", "TF"):
        p = os.path.join(R4, "A12_%s_features.npz" % tag)
        if os.path.exists(p):
            d = dict(np.load(p))
            for k, w in {"hd": 8, "hq": 16, "hb": 60}.items():
                x = d[k]; d[k] = x[:, :w] if x.shape[1] >= w else np.pad(x, ((0, 0), (0, w - x.shape[1])))
            doms[tag] = d
    for tag, F in doms.items():
        out[tag] = {nm: stats(F, names, tag) for nm, names in {"(Q,S2)": ["sq", "Ss2"], "(N,SB22)": ["N", "SB22"], "(N,h1,h2)": ["N", "hd", "hb"], "(N,h1)": ["N", "hd"], "N": ["N"]}.items()}
        print(tag, {k: (v["positive_systems_with_a_partner"], v["positives"], None if v["partner_positive_rate"] is None else round(v["partner_positive_rate"], 4), round(v["base_rate"], 4)) for k, v in out[tag].items()}, flush=True)
    json.dump(out, open(os.path.join(R4, "A13_collision_concordance.json"), "w"), indent=1)

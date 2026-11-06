"""D21 -- analysis of C20: which small observations of the dead-set nerve determine Y = 1{beta_2>0} over the whole census (exact H(Y|O), natural and balanced), and the S6-types of strong-collapse cores of the 290 positives."""
import itertools, json, os
from collections import Counter
import numpy as np
import _path, nerve, ent2
from A20_load_positives import load_positives

def cond_entropy(Y, O, w, balanced):
    """exact-up-to-float H(Y|O) in bits; w = multiplicities; balanced => classes re-weighted to total 1/2 each"""
    w = w.astype(float).copy()
    if balanced:
        for y in (0, 1): w[Y == y] /= w[Y == y].sum() * 2
    else: w /= w.sum()
    _, inv = np.unique(O, axis=0, return_inverse=True); inv = inv.reshape(-1)
    tot = np.bincount(inv, weights=w); p1 = np.bincount(inv, weights=w * (Y == 1))
    q = np.where(tot > 0, p1 / np.maximum(tot, 1e-300), 0)
    h = np.where((q > 0) & (q < 1), -(q * np.log2(np.where(q > 0, q, 1)) + (1 - q) * np.log2(np.where(q < 1, 1 - q, 1))), 0)
    return float((tot * h).sum()), int(len(tot))

PERMS = list(itertools.permutations(range(6)))
ACT = [[sum(1 << p[i] for i in range(6) if m >> i & 1) for m in range(64)] for p in PERMS]
def canon_core(facets):
    return min(tuple(sorted(tuple(sorted(t[x] for x in f)) for f in facets)) for t in ACT)

if __name__ == "__main__":
    Z = np.load(os.path.join(_path.ROOT, "RESULTS", "C20_dead_patterns.npz"))
    V, E, comp, Tr, Hol, core, b0, b1, mult = (Z[k] for k in ("V", "E", "comp", "Tr", "Hol", "core", "b0", "b1", "mult"))
    Y = (b1 > 0).astype(int)
    out = {"patterns": int(len(V)), "regimes": int(mult.sum()), "positive_patterns": int(Y.sum()), "positive_regimes": int(mult[Y == 1].sum()), "disconnected_nerve_patterns": int((b0 > 0).sum()),
           "reduced_b1_max": int(b1.max())}
    obs = {"V": np.c_[V], "(V,E)": np.c_[V, E], "(V,E,Tr)": np.c_[V, E, Tr], "euler V-E+Tr": np.c_[V - E + Tr], "(V,E,Hol)": np.c_[V, E, Hol], "Hol": np.c_[Hol], "(Hol,comp)": np.c_[Hol, comp],
           "(V,comp,Hol)": np.c_[V, comp, Hol], "core size": np.c_[core], "(V,E,Tr,Hol,comp)": np.c_[V, E, Tr, Hol, comp], "(core,Hol)": np.c_[core, Hol], "(b0,Euler 2-skeleton)": np.c_[b0, V - E + Tr]}
    res = {}
    for nm, O in obs.items():
        res[nm] = {}
        for mode in ("natural", "balanced"):
            h, n = cond_entropy(Y, O, mult, mode == "balanced"); res[nm][mode] = {"H(Y|O)": round(h, 6), "classes": n}
        print(nm, res[nm], flush=True)
    out["observations"] = res
    # structural facts
    out["positives_with_Hol_0"] = int(((Y == 1) & (Hol == 0)).sum()); out["negatives_with_Hol_gt_0"] = int(((Y == 0) & (Hol > 0)).sum())
    out["core_size_positive"] = {str(k): int(v) for k, v in sorted(Counter(core[Y == 1].tolist()).items())}
    out["core_size_negative_quantiles"] = {str(q): float(np.quantile(core[Y == 0], q)) for q in (0.5, 0.9, 0.99, 1.0)}
    out["negatives_with_empty_or_point_core"] = int(((Y == 0) & (core <= 1)).sum())
    # S6 types of cores of the 290 positives
    P, F, R = load_positives(); types = Counter(); size = {}
    for p in P:
        D = nerve.dead_sets(p["mask"]); v, f = nerve.strong_core(D)
        key = canon_core(f); types[key] += 1; size[key] = len(v)
    out["positive_core_types"] = [{"count": c, "core_vertices": size[k], "facets_up_to_S6": [[bin(x).count("1") for x in f] for f in k]} for k, c in types.most_common()]
    out["n_positive_core_types"] = len(types)
    json.dump(out, open(os.path.join(_path.ROOT, "RESULTS", "D21_minimal_observation.json"), "w"), indent=1)
    print({k: v for k, v in out.items() if k not in ("observations", "positive_core_types")}); print(out["positive_core_types"][:8])

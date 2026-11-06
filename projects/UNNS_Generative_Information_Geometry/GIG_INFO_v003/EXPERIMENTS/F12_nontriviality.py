"""F12 -- is a zero residual informative or merely a fine partition?  For each signature: positives alone in their class (trivial), positives in pure classes of size>=2 (informative),
and a permutation null: positives re-placed uniformly at random among the regimes with the same N (preserves H(Y|N) structure); mixed classes counted for 300 shuffles."""
import json, os
import numpy as np
import _path

F = dict(np.load(os.path.join(_path.ROOT, "RESULTS", "features_all.npz")))
Y = (F["beta2"] > 0).astype(np.int8)
n = len(Y)
SIGS = {"N": ["N"], "N+hd": ["N", "hd"], "N+SB22": ["N", "SB22"], "SB2+SB22": ["SB2", "SB22"], "N+hb": ["N", "hb"], "f-vector": ["N", "E", "sq", "hx", "f3", "f4"], "N+sq+Sq2": ["N", "sq", "Sq2"], "SB22": ["SB22"]}


def classes(names):
    M = np.concatenate([F[k].reshape(n, -1) for k in names], axis=1)
    _, inv = np.unique(M, axis=0, return_inverse=True)
    return inv.reshape(-1)


def stats(inv, y):
    size = np.bincount(inv); pos = np.bincount(inv, weights=y)
    mixed = (pos > 0) & (pos < size)
    pure_pos = (pos == size) & (pos > 0)
    single = pure_pos & (size == 1)
    nontriv = pure_pos & (size > 1)
    return dict(classes=int(len(size)), mixed_classes=int(mixed.sum()), positives_in_mixed=int(pos[mixed].sum()), positives_in_singleton_classes=int(pos[single].sum()), positives_in_pure_classes_size_ge2=int(pos[nontriv].sum()),
                largest_pure_positive_class=int(size[nontriv].max()) if nontriv.any() else 0)


if __name__ == "__main__":
    rng = np.random.default_rng(20261106)
    byN = {}
    for i, v in enumerate(F["N"]):
        byN.setdefault(int(v), []).append(i)
    posN = {k: int(Y[ix].sum()) for k, ix in byN.items() if Y[ix].sum()}
    out = {}
    for name, names in SIGS.items():
        inv = classes(names)
        rec = {"real": stats(inv, Y)}
        mix = []
        for _ in range(300):
            y = np.zeros(n, dtype=np.int8)
            for k, c in posN.items():
                y[rng.choice(byN[k], c, replace=False)] = 1
            mix.append(stats(inv, y)["positives_in_mixed"])
        rec["null_positives_in_mixed_classes"] = {"min": int(min(mix)), "mean": float(np.mean(mix)), "max": int(max(mix)), "shuffles_with_zero": int(sum(m == 0 for m in mix)), "shuffles": 300}
        out[name] = rec
        print(name, rec["real"], rec["null_positives_in_mixed_classes"], flush=True)
    json.dump(out, open(os.path.join(_path.ROOT, "RESULTS", "F12_nontriviality.json"), "w"), indent=1)

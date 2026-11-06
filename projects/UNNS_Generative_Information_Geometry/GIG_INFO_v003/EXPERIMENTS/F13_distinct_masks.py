"""F13 -- the same non-triviality diagnostics on E_mask = one regime per distinct rank-indexed arrangement mask (219,146 masks).  NAMING CORRECTION to v002: its `E_distinct` is uniform over distinct RANK-INDEXED MASKS, not over distinct labelled arrangement sets (those would also separate contents)."""
import json, os
import numpy as np
import _path, v2
import F12_nontriviality as f12

if __name__ == "__main__":
    REGS = v2.census.enumerate_regimes()
    seen, keep = {}, []
    for i, r in enumerate(REGS):
        if r[3] not in seen:
            seen[r[3]] = i; keep.append(i)
    keep = np.array(keep)
    Y = f12.Y[keep]
    out = {"masks": int(len(keep)), "positive_masks": int(Y.sum())}
    rng = np.random.default_rng(20261107)
    n = len(keep)
    N = f12.F["N"][keep]
    byN = {}
    for i, v in enumerate(N):
        byN.setdefault(int(v), []).append(i)
    posN = {k: int(Y[ix].sum()) for k, ix in byN.items() if Y[ix].sum()}
    for name in ("N+hd", "N+SB22", "SB2+SB22", "N+hb", "f-vector", "SB22"):
        M = np.concatenate([f12.F[k][keep].reshape(n, -1) for k in f12.SIGS[name]], axis=1)
        _, inv = np.unique(M, axis=0, return_inverse=True)
        inv = inv.reshape(-1)
        real = f12.stats(inv, Y)
        mix = []
        for _ in range(300):
            y = np.zeros(n, dtype=np.int8)
            for k, c in posN.items():
                y[rng.choice(byN[k], c, replace=False)] = 1
            mix.append(f12.stats(inv, y)["positives_in_mixed"])
        out[name] = {"real": real, "null": {"min": int(min(mix)), "mean": float(np.mean(mix)), "max": int(max(mix)), "shuffles_with_zero": int(sum(m == 0 for m in mix))}}
        print(name, real, out[name]["null"], flush=True)
    json.dump(out, open(os.path.join(_path.ROOT, "RESULTS", "F13_distinct_masks.json"), "w"), indent=1)

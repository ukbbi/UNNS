"""F11 -- smallest separating observables for Y=1[beta2>0] on the six-label census (E_all, all 346,859 regimes).
(a) every subset (size<=4) of the scalar pool is tested for zero residual (mixed classes = classes containing both Y values); hashed screen then exact confirmation.
(b) vector observables; (c) the 66 positives unresolved by (N,h1): which added feature resolves them."""
import itertools, json, os, time
import numpy as np
import _path
import v2

F = dict(np.load(os.path.join(_path.ROOT, "RESULTS", "features_all.npz")))
Y = (F["beta2"] > 0).astype(np.int8)
POOL = ["N", "E", "sq", "hx", "f3", "f4", "Sd2", "Sd3", "Sq2", "SB2", "SB22", "dmax", "dmin", "bmax", "bmin"]
HASHM = np.array([0x9E3779B97F4A7C15, 0xC2B2AE3D27D4EB4F, 0x165667B19E3779F9, 0x27D4EB2F165667C5], dtype=np.uint64)


def mixed(keys):
    u, inv = np.unique(keys, return_inverse=True) if keys.ndim == 1 else np.unique(keys, axis=0, return_inverse=True)
    inv = inv.reshape(-1)
    size = np.bincount(inv)
    pos = np.bincount(inv, weights=Y)
    m = (pos > 0) & (pos < size)
    return int(m.sum()), int(pos[m].sum()), len(u)


def screen(cols):
    with np.errstate(over="ignore"):
        k = np.zeros(len(Y), dtype=np.uint64)
        for c, h in zip(cols, HASHM):
            k = k * np.uint64(1000003) + (F[c].astype(np.uint64) + np.uint64(7)) * h
    return k


if __name__ == "__main__":
    t0 = time.time()
    out = {"pool": POOL, "positives": int(Y.sum())}
    sep = []
    for r in range(1, 5):
        for sub in itertools.combinations(POOL, r):
            nm, npos, ncls = mixed(screen(sub))
            if nm == 0:
                M = np.stack([F[c] for c in sub], 1)
                nm2, _, ncls2 = mixed(M)  # exact confirmation
                if nm2 == 0:
                    sep.append({"features": list(sub), "classes": ncls2})
    minimal = [s for s in sep if not any(set(t["features"]) < set(s["features"]) for t in sep)]
    out["separating_subsets_up_to_4"] = len(sep)
    out["minimal_separating_subsets"] = minimal
    print("minimal:", [m["features"] for m in minimal], round(time.time() - t0), flush=True)
    # best partial: for each size, the subset with the fewest mixed classes / positives hidden
    best = {}
    for r in range(1, 5):
        c = []
        for sub in itertools.combinations(POOL, r):
            nm, npos, ncls = mixed(screen(sub))
            c.append((npos, nm, ncls, sub))
        c.sort()
        best[r] = [{"features": list(x[3]), "positives_in_mixed_classes": x[0], "mixed_classes": x[1], "classes": x[2]} for x in c[:6]]
    out["best_by_size"] = best
    # vector observables
    def vec(names):
        return np.concatenate([F[n].reshape(len(Y), -1) for n in names], axis=1)
    V = {}
    for nm, names in {"hd": ["hd"], "hq": ["N", "hq"], "N_hd": ["N", "hd"], "N_hd_sq": ["N", "hd", "sq"], "N_hd_hq": ["N", "hd", "hq"], "hdq": ["hdq"], "hb": ["hb"], "N_hb": ["N", "hb"], "N_hd_hb": ["N", "hd", "hb"], "fvec": ["N", "E", "sq", "hx", "f3", "f4"]}.items():
        nm_, npos, ncls = mixed(vec(names))
        V[nm] = {"mixed_classes": nm_, "positives_in_mixed_classes": npos, "classes": ncls}
    out["vector_observables"] = V
    # (c) the unresolved-after-radius-1 positives
    H1 = vec(["N", "hd"])
    u, inv = np.unique(H1, axis=0, return_inverse=True)
    inv = inv.reshape(-1)
    size = np.bincount(inv); pos = np.bincount(inv, weights=Y)
    unres = np.nonzero((Y == 1) & (size[inv] > pos[inv]))[0]
    out["unresolved_after_radius1"] = int(len(unres))
    res = {}
    for extra in POOL + ["hq", "hdq", "hb"]:
        cnt = 0
        for i in unres:
            same = (inv == inv[i]) & (Y == 0)
            e = F[extra]
            if e.ndim == 1:
                eq = e[same] == e[i]
            else:
                eq = (e[same] == e[i]).all(1)
            cnt += bool(eq.any())
        res[extra] = int(cnt)
    out["unresolved_positives_still_colliding_after_adding"] = res
    out["unresolved_indices"] = [int(i) for i in unres]
    json.dump(out, open(os.path.join(_path.ROOT, "RESULTS", "F11_minimal_signatures.json"), "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k not in ("unresolved_indices", "best_by_size")}, indent=0)[:3500])
    print(best[1][:2], best[2][:3], best[3][:3])
    print("seconds", round(time.time() - t0))

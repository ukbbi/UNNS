"""A12 -- scope of the (Q,S2) separation across nested classes of history systems on six labels:
  VS  arbitrary vertex subsets of P_6 (any admissible set);
  PF  prefix families: A = orderings all of whose prefix sets lie in a random family of subsets;
  TF  threshold families: A = orderings whose prefix sets satisfy max(0, sum_{l in I} c_{j,l}) <= e_j for j=1..J  (the form taken by arithmetic admissibility with c = 2v_p(l+1)-v_p(l)), random integer weights;
  AR  arithmetic regimes (census D u H6; result imported).
For each: number of distinct systems, positives (beta2>0), mixed classes of (Q,S2), (N,SB22), (N,h1,h2) and positives hidden; smallest certified counterexample for (Q,S2)."""
import itertools, json, os, sys, time
import numpy as np
from multiprocessing import Pool
import _path, geomk
import history_complex as hc

PERMS = np.array(list(itertools.permutations(range(6))))
PREF = np.stack([np.bitwise_or.accumulate(1 << PERMS, axis=1)[:, j] for j in range(5)], axis=1)  # prefix subset bitmasks (720,5), values 1..62
SUBS = np.array([[(s >> b) & 1 for b in range(6)] for s in range(64)])  # (64,6)


def pack(a):
    by = np.packbits(a, axis=1, bitorder="little")
    return [int.from_bytes(by[i].tobytes(), "little") for i in range(a.shape[0]) if a[i].any()]


def gen_VS(rng, R):
    dens = rng.choice([0.4, 0.55, 0.7, 0.85, 0.93], size=R)
    return pack(rng.random((R, 720)) < dens[:, None])


def gen_PF(rng, R):
    pi = rng.choice([0.55, 0.7, 0.8, 0.9, 0.95], size=R)
    fam = rng.random((R, 64)) < pi[:, None]
    fam[:, 0] = True; fam[:, 63] = True
    return pack(fam[:, PREF].all(axis=2))


def gen_TF(rng, R):
    out = []
    vals = np.array([0, 2, 4, -1, -2, -3]); pr = np.array([0.45, 0.15, 0.05, 0.2, 0.1, 0.05])
    for s in range(0, R, 2000):
        r = min(2000, R - s)
        J = rng.integers(1, 4, size=r)
        fam = np.ones((r, 64), dtype=bool)
        for j in range(3):
            c = rng.choice(vals, size=(r, 6), p=pr)
            e = rng.integers(0, 7, size=r)
            sums = np.maximum(0, c @ SUBS.T)  # (r,64)
            cond = sums <= e[:, None]
            fam &= np.where((J > j)[:, None], cond, True)
        fam[:, 0] = True; fam[:, 63] = True
        out += pack(fam[:, PREF].all(axis=2))
    return out


def beta2_(m):
    return hc.betti(m, 6)[2]


def classes(F, names):
    n = len(F["N"]); Y = F["beta2"] > 0
    M = np.concatenate([F[k].reshape(n, -1) for k in names], axis=1)
    _, inv = np.unique(M, axis=0, return_inverse=True); inv = inv.reshape(-1)
    size = np.bincount(inv); pos = np.bincount(inv, weights=Y)
    mixed = (pos > 0) & (pos < size)
    return inv, mixed, int(pos[mixed].sum()), int(mixed.sum())


if __name__ == "__main__":
    t0 = time.time()
    rng = np.random.default_rng(20261114)
    plan = {"VS": (gen_VS, 30000), "PF": (gen_PF, 120000), "TF": (gen_TF, 120000)}
    res = {}
    for tag, (g, R) in plan.items():
        ms = list(dict.fromkeys(g(rng, R)))
        ms = [m for m in ms if m != (1 << 720) - 1]
        with Pool(2) as pool:
            b2 = np.array(pool.map(beta2_, ms, chunksize=200))
        G = geomk.Geom(6)
        parts = {}
        for s in range(0, len(ms), 3000):
            for k_, v in G.features(ms[s:s + 3000]).items():
                parts.setdefault(k_, []).append(v)
        F = {k_: np.concatenate(v) for k_, v in parts.items()}
        F["beta2"] = b2
        np.savez_compressed(os.path.join(_path.ROOT, "RESULTS", "A12_%s_features.npz" % tag), **F, masks_hex=np.array([hex(m) for m in ms]))
        rec = {"distinct_systems": len(ms), "positives": int((b2 > 0).sum())}
        for nm, names in {"(Q,S2)": ["sq", "Ss2"], "(N,SB22)": ["N", "SB22"], "(N,h1,h2)": ["N", "hd", "hb"], "(N,h1)": ["N", "hd"], "N": ["N"]}.items():
            inv, mixed, hid, nm_ = classes(F, names)
            rec[nm] = {"mixed_classes": nm_, "positives_hidden": hid}
            if nm == "(Q,S2)" and nm_:
                # smallest-N mixed class
                best = None
                for c in np.nonzero(mixed)[0]:
                    ix = np.nonzero(inv == c)[0]
                    Nn = int(F["N"][ix[0]])
                    if best is None or Nn < best[0]:
                        best = (Nn, ix)
                ix = best[1]
                pi = [int(i) for i in ix if b2[i] > 0][0]; ni = [int(i) for i in ix if b2[i] == 0][0]
                rec["smallest_counterexample"] = {"N": best[0], "Q": int(F["sq"][pi]), "S2": int(F["Ss2"][pi]), "mask_pos": hex(ms[pi]), "mask_neg": hex(ms[ni]), "beta2_pos": int(b2[pi]), "beta2_neg": int(b2[ni])}
        res[tag] = rec
        print(tag, json.dumps(rec)[:700], round(time.time() - t0), flush=True)
    json.dump(res, open(os.path.join(_path.ROOT, "RESULTS", "A12_scope_hierarchy.json"), "w"), indent=1)

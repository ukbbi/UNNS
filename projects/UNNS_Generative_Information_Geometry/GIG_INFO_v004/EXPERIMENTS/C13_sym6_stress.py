"""C13 -- SYM-6 stress sample (600k digraphs, seed 20261112; NOT part of the registration): random transition digraphs on six distinguishable symbols; Hamiltonian-ordering systems; beta_2 and the observation hierarchy."""
import itertools, json, os, time
import numpy as np
from multiprocessing import Pool
import _path, geomk
import history_complex as hc

PERMS = np.array(list(itertools.permutations(range(6))))
PAIRIDX = PERMS[:, :-1] * 6 + PERMS[:, 1:]  # (720,5)


def betti_(m):
    return list(hc.betti(m, 6))


if __name__ == "__main__":
    t0 = time.time()
    rng = np.random.default_rng(20261112)
    R = 600000
    p = rng.choice([0.45, 0.55, 0.65, 0.75, 0.85], size=R)
    adj = rng.random((R, 36)) < p[:, None]
    masks = {}
    for s in range(0, R, 5000):
        a = adj[s:s + 5000][:, PAIRIDX].all(axis=2)  # (chunk,720)
        by = np.packbits(a, axis=1, bitorder="little")
        for k_ in range(a.shape[0]):
            if a[k_].any():
                masks.setdefault(int.from_bytes(by[k_].tobytes(), "little"), int(p[s + k_] * 100))
    ms = list(masks)
    print("distinct nonempty masks", len(ms), round(time.time() - t0), flush=True)
    with Pool(2) as pool:
        B = pool.map(betti_, ms, chunksize=200)
    G = geomk.Geom(6)
    parts = {}
    for s in range(0, len(ms), 4000):
        f = G.features(ms[s:s + 4000])
        for k_, v in f.items():
            parts.setdefault(k_, []).append(v)
    F = {k_: np.concatenate(v) for k_, v in parts.items()}
    Bn = np.array(B)
    F.update(beta=Bn, beta2=Bn[:, 2], beta1=Bn[:, 1], beta0=Bn[:, 0], pct=np.array([masks[m] for m in ms]))
    np.savez_compressed(os.path.join(_path.ROOT, "RESULTS", "SYM6_stress_features.npz"), **F)
    json.dump({"digraphs": R, "distinct_masks": len(ms), "positives_beta2": int((Bn[:, 2] > 0).sum()), "positives_beta1": int((Bn[:, 1] > 0).sum()), "seconds": round(time.time() - t0, 1)},
              open(os.path.join(_path.ROOT, "RESULTS", "C13_stress_summary.json"), "w"), indent=1)
    print("done", int((Bn[:, 2] > 0).sum()), int((Bn[:, 1] > 0).sum()), round(time.time() - t0), flush=True)

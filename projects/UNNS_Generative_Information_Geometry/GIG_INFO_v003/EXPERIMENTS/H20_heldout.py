"""H20 -- held-out transfer tests (pre-registered in THEORY/PREREGISTRATION.md).  usage: H20_heldout.py 6|7 [procs]"""
import itertools, json, os, random, sys, time
from multiprocessing import Pool
import numpy as np
import _path, v2
import source_filtration as sf
import history_complex as hc
import geomk

def beta2(args):
    mask, k = args
    return hc.betti(mask, k)[2]

def sample(kind):
    if kind == 6:
        allc = [c for c in itertools.combinations(range(1, 23), 6) if c[-1] >= 17]
        return sorted(random.Random(20261108).sample(allc, 6000))
    allc = list(itertools.combinations(range(1, 15), 7))
    return sorted(random.Random(20261109).sample(allc, 120))

if __name__ == "__main__":
    kind = int(sys.argv[1]); procs = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    t0 = time.time()
    contents = sample(kind)
    regs = []
    for C in contents:
        for r in sf.regimes(C):
            regs.append((C, r["L"], r["N"], r["mask"]))
    print("contents", len(contents), "regimes", len(regs), round(time.time() - t0), flush=True)
    with Pool(procs) as pool:
        b2 = pool.map(beta2, [(r[3], kind) for r in regs], chunksize=64)
    print("betti done", round(time.time() - t0), flush=True)
    G = geomk.Geom(kind)
    parts = {}
    CH = 400 if kind == 7 else 4000
    for s in range(0, len(regs), CH):
        f = G.features([r[3] for r in regs[s:s + CH]])
        for k_, v in f.items():
            if k_ in ("hb", "hq", "hd"):
                v = v[:, : {"hb": 60, "hq": 16, "hd": 8}[k_]] if v.shape[1] >= {"hb": 60, "hq": 16, "hd": 8}[k_] else np.pad(v, ((0, 0), (0, {"hb": 60, "hq": 16, "hd": 8}[k_] - v.shape[1])))
            parts.setdefault(k_, []).append(v)
    F = {k_: np.concatenate(v) for k_, v in parts.items()}
    F["beta2"] = np.array(b2)
    F["L"] = np.array([r[1] for r in regs])
    np.savez_compressed(os.path.join(_path.ROOT, "RESULTS", "H%d_features.npz" % kind), **F)
    json.dump({"kind": kind, "contents": [list(c) for c in contents], "regimes": len(regs), "positives": int((F["beta2"] > 0).sum()), "beta2_hist": {str(k_): int((F["beta2"] == k_).sum()) for k_ in sorted(set(F["beta2"].tolist()))}, "seconds": round(time.time() - t0, 1)},
              open(os.path.join(_path.ROOT, "RESULTS", "H%d_summary.json" % kind), "w"), indent=1)
    print("done", round(time.time() - t0), "positives", int((F["beta2"] > 0).sum()), flush=True)

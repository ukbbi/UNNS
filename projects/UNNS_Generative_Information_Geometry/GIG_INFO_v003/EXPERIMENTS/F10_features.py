"""F10 -- local-geometry features for every regime of the six-label census (same order as the frozen v002 census csv); cross-checks T1 against the v002 pure-python ball histograms on a stratified sample."""
import gzip, csv, json, os, sys, time, random, hashlib
import numpy as np
import _path
import v2, geom

if __name__ == "__main__":
    t0 = time.time()
    REGS = v2.census.enumerate_regimes()
    masks = [r[3] for r in REGS]
    parts = {}
    CH = 6000
    for s in range(0, len(masks), CH):
        f = geom.features(masks[s:s + CH])
        for k_, v in f.items():
            parts.setdefault(k_, []).append(v)
        if s % (CH * 10) == 0:
            print(s, round(time.time() - t0), flush=True)
    F = {k_: np.concatenate(v) for k_, v in parts.items()}
    # compare with the census csv f-vector (f1=E, f2=sq+hx)
    rows = []
    with gzip.open(os.path.join(_path._vpath.PATHS["INFO002"], "RESULTS", "census_regimes.csv.gz"), "rt") as f:
        rd = csv.DictReader(f)
        for r in rd:
            rows.append(r)
    assert len(rows) == len(REGS)
    N_csv = np.array([int(r["N"]) for r in rows]); f1 = np.array([int(r["f1"]) for r in rows]); f2 = np.array([int(r["f2"]) for r in rows]); b2 = np.array([int(r["betti2"]) for r in rows])
    f3 = np.array([int(r["f3"]) for r in rows]); f4 = np.array([int(r["f4"]) for r in rows]); f5 = np.array([int(r["f5"]) for r in rows])
    assert (F["N"] == N_csv).all() and (F["E"] == f1).all() and (F["sq"] + F["hx"] == f2).all()
    F.update(f3=f3, f4=f4, f5=f5, beta2=b2, L=np.array([r[1] for r in REGS]))
    # T1 check against pure-python ball histograms
    rng = random.Random(20261106)
    sample = sorted(set(rng.sample(range(len(REGS)), 4000)) | set(np.nonzero(b2 > 0)[0].tolist()))
    bad = 0
    for i in sample:
        h1, h2 = v2.census.ball_histograms(v2.census.adjacency(REGS[i][3]))
        hb = F["hb"][i]
        ref = {int(sz): int(c) for sz, c in h2}
        mine = {v: int(c) for v, c in enumerate(hb) if c}
        bad += ref != mine
        hd = F["hd"][i]
        ref1 = {int(sz): int(c) for sz, c in h1}
        mine1 = {v + 1: int(c) for v, c in enumerate(hd) if c}
        bad += ref1 != mine1
    print("T1 sample", len(sample), "mismatches", bad)
    os.makedirs(os.path.join(_path.ROOT, "RESULTS"), exist_ok=True)
    np.savez_compressed(os.path.join(_path.ROOT, "RESULTS", "features_all.npz"), **F)
    json.dump({"regimes": len(REGS), "T1_sample": len(sample), "T1_mismatches": int(bad), "seconds": round(time.time() - t0, 1),
               "csv_f_vector_agrees": True}, open(os.path.join(_path.ROOT, "RESULTS", "F10_features.json"), "w"), indent=1)

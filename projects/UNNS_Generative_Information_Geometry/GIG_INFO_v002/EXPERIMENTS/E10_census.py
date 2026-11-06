"""E10 -- re-enumerate the whole six-label census (all 8,008 contents with labels <= 16, every source regime) and recompute the Betti vector and f-vector of every regime
with the independent v001 engine (GF(2)).  Compares the recomputed beta_2>0 set with the frozen v004 baseline.  Writes RESULTS/census_regimes.csv.gz (one row per regime) and RESULTS/E10_census.json."""
import csv, gzip, json, os, sys, time, multiprocessing as mp
from collections import Counter
import _path
import census as cs
import history_complex as hc

REGS = None


def job(i):
    m = REGS[i][3]
    return hc.betti(m, 6), hc.f_vector(m, 6)


if __name__ == "__main__":
    t0 = time.time()
    REGS = cs.enumerate_regimes()
    procs = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    with mp.get_context("fork").Pool(procs) as pool:
        res = pool.map(job, range(len(REGS)), chunksize=500)
    frozen, sha, frozen_total = cs.frozen_positive_regimes()
    pos_now = {(REGS[i][0], REGS[i][1]): res[i][0][2] for i in range(len(REGS)) if res[i][0][2] > 0}
    pos_frozen = {(c, L): b for c, L, b in frozen}
    out = {"contents": 8008, "regimes": len(REGS), "frozen_regimes": frozen_total, "regimes_agree_with_frozen_count": len(REGS) == frozen_total,
           "beta2_positive_recomputed": len(pos_now), "beta2_positive_frozen": len(pos_frozen), "positive_sets_identical": pos_now == pos_frozen,
           "beta2_histogram": dict(Counter(r[0][2] for r in res)), "N_range": [min(r[2] for r in REGS), max(r[2] for r in REGS)],
           "frozen_v004_results_sha256": sha, "seconds": round(time.time() - t0, 1)}
    with gzip.open(os.path.join(_path.ROOT, "RESULTS", "census_regimes.csv.gz"), "wt", newline="") as f:
        w = csv.writer(f)
        w.writerow(["content", "L", "N", "betti0", "betti1", "betti2", "betti3", "betti4", "betti5", "f0", "f1", "f2", "f3", "f4", "f5"])
        for (C, L, N, mask), (b, fv) in zip(REGS, res):
            w.writerow(["-".join(map(str, C)), L, N] + list(b) + list(fv))
    json.dump(out, open(os.path.join(_path.ROOT, "RESULTS", "E10_census.json"), "w"), indent=1)
    print(out)

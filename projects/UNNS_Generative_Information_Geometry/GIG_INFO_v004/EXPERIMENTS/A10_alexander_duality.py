"""A10 -- numerical verification of Alexander duality  reduced b_j(K_A) = reduced b_{3-j}(Y_A)  (k=6) on all 158 census positives, all census regimes with beta_1>0 sampled, and random negatives; plus arbitrary random vertex sets (the theorem is not arithmetic)."""
import json, os, random
import numpy as np
import _path, v2, forbidden as fb
import history_complex as hc

if __name__ == "__main__":
    REGS = v2.census.enumerate_regimes()
    F = dict(np.load(os.path.join(_path._vpath.PATHS["INFO003"], "RESULTS", "features_all.npz")))
    rng = random.Random(20261113)
    pos = [int(i) for i in np.nonzero(F["beta2"] > 0)[0]]
    rest = rng.sample([i for i in range(len(REGS)) if F["beta2"][i] == 0 and REGS[i][3] != (1 << 720) - 1], 342)
    tests = [(("census_positive" if i in set(pos) else "census_negative"), REGS[i][3]) for i in pos + rest]
    for _ in range(200):
        dens = rng.choice([0.5, 0.7, 0.85, 0.95])
        m = 0
        for b in range(720):
            if rng.random() < dens:
                m |= 1 << b
        tests.append(("random_vertex_set", m))
    out = {"tested": 0, "mismatches": 0, "by_kind": {}, "beta2_equals_H1_of_Y": 0, "examples_mismatch": []}
    for kind, m in tests:
        if m == (1 << 720) - 1 or m == 0:
            continue
        b = hc.betti(m, 6)
        rb = [b[0] - 1] + list(b[1:5])  # reduced b~_0..b~_4 of K
        yb = fb.reduced_betti(fb.y_simplices(m, 6), 4)  # b~_0..b~_4 of Y
        ok = all(rb[j] == yb[3 - j] for j in range(4)) and rb[4] == 0
        out["tested"] += 1
        d = out["by_kind"].setdefault(kind, [0, 0])
        d[0] += 1; d[1] += int(not ok)
        out["mismatches"] += int(not ok)
        out["beta2_equals_H1_of_Y"] += int(b[2] == yb[1])
        if not ok and len(out["examples_mismatch"]) < 3:
            out["examples_mismatch"].append({"kind": kind, "betti_K": list(b), "reduced_betti_Y": yb})
    json.dump(out, open(os.path.join(_path.ROOT, "RESULTS", "A10_alexander_duality.json"), "w"), indent=1)
    print(out)

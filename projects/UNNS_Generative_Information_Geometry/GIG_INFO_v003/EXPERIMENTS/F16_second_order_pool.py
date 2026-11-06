"""F16 -- which interpretable second-order radius-2 sums carry the information?  Pool of exact local sums (d degree, q square-incidence, s=sum_{u~w}(d(u)-1)); all subsets up to size 4 tested for zero residual on E_all."""
import itertools, json, os
import numpy as np
import _path
import F11_minimal_signatures as f11

POOL = ["N", "E", "sq", "hx", "Sd2", "Sd3", "Sq2", "Ss2", "Sds", "Sdq", "Ssq"]
if __name__ == "__main__":
    F = f11.F
    # identity check: SB22 = sum (1+d+s-q)^2 expanded in the pool sums (integers)
    N, E, sq = F["N"], F["E"], F["sq"]
    expand = N + F["Sd2"] + F["Ss2"] + F["Sq2"] + 2 * (2 * E) + 2 * F["Ss"] - 2 * (4 * sq) + 2 * F["Sds"] - 2 * F["Sdq"] - 2 * F["Ssq"]
    assert (expand == F["SB22"]).all()
    assert (F["SB2"] == N + F["Sd2"] - 4 * sq).all()
    assert (F["Ss"] == F["Sd2"] - 2 * E).all()
    sep = []
    for r in range(1, 5):
        for sub in itertools.combinations(POOL, r):
            nm, npos, ncls = f11.mixed(f11.screen(sub))
            if nm == 0:
                M = np.stack([F[c] for c in sub], 1)
                if f11.mixed(M)[0] == 0:
                    sep.append(list(sub))
    minimal = [s for s in sep if not any(set(t) < set(s) for t in sep)]
    best = {}
    for r in range(1, 5):
        c = sorted((f11.mixed(f11.screen(sub))[1], sub) for sub in itertools.combinations(POOL, r))
        best[r] = [{"features": list(x[1]), "positives_in_mixed_classes": x[0]} for x in c[:5]]
    out = {"pool": POOL, "identities_verified_on_all_346859": ["SB2 = N + Sd2 - 4 sq", "Ss = Sd2 - 2E", "SB22 = N + Sd2 + Ss2 + Sq2 + 4E + 2Ss - 8sq + 2Sds - 2Sdq - 2Ssq"], "minimal_separating_subsets": minimal, "best_by_size": best}
    json.dump(out, open(os.path.join(_path.ROOT, "RESULTS", "F16_second_order_pool.json"), "w"), indent=1)
    print(minimal); print(best)

"""A16 -- structure of the forbidden-flag complex Y for positives vs negatives: 'dead' proper subsets I (every history through the prefix set I is non-admissible), complementary dead pairs, and the dimension of H_1(Y)=beta_2(K)."""
import json, os, random
import numpy as np
import _path, v2, forbidden as fb

def dead_subsets(mask):
    ch = fb.chains(6)
    through = {}
    for i, c in enumerate(ch):
        for I in c:
            through.setdefault(I, []).append(i)
    admiss = {I: any(mask >> i & 1 for i in ids) for I, ids in through.items()}
    return {I for I, a in admiss.items() if not a}

if __name__ == "__main__":
    REGS = v2.census.enumerate_regimes()
    F = dict(np.load(os.path.join(_path._vpath.PATHS["INFO003"], "RESULTS", "features_all.npz")))
    pos = [int(i) for i in np.nonzero(F["beta2"] > 0)[0]]
    rng = random.Random(20261115)
    neg = rng.sample([i for i in range(len(REGS)) if F["beta2"][i] == 0 and REGS[i][3] != (1 << 720) - 1], 2000)
    out = {}
    for tag, ids in (("positives", pos), ("negatives_sample", neg)):
        cnt = {"systems": len(ids), "with_dead_subset": 0, "with_complementary_dead_pair": 0, "with_dead_subsets_of_all_sizes_1_to_5": 0}
        sizes = []
        for i in ids:
            D = dead_subsets(REGS[i][3])
            cnt["with_dead_subset"] += bool(D)
            cnt["with_complementary_dead_pair"] += any(((~I) & 63) in D for I in D)
            sizes.append(len(D))
        cnt["mean_number_of_dead_subsets"] = float(np.mean(sizes))
        out[tag] = cnt
        print(tag, cnt, flush=True)
    json.dump(out, open(os.path.join(_path.ROOT, "RESULTS", "A16_dead_subsets.json"), "w"), indent=1)

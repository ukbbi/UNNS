"""B24 -- the symbolic S/R/N grammar is a pair-adjacency system (consecutive categories must lie in G): the theorem predicts beta_2(K)=0 for ALL 28 multisets x 512 rule sets.  Exhaustive check (with beta_1, beta_3 reported) + direct Y verification on a sample."""
import json, os, random, time
from collections import Counter
import _path, sym, forbidden as fb, adjacency as ad
import history_complex as hc

if __name__ == "__main__":
    t0 = time.time(); seen = {}
    for cats in sym.multisets():
        for m, codes in sym.all_systems(cats).items():
            if m != (1 << 720) - 1: seen.setdefault(m, (cats, codes[0]))
    print("distinct nonempty proper masks", len(seen), round(time.time() - t0), flush=True)
    cnt = Counter(); b2max = 0
    for m in seen:
        b = hc.betti(m, 6); cnt[tuple(b[1:4])] += 1; b2max = max(b2max, b[2])
    out = {"distinct_masks": len(seen), "beta2_max": b2max, "beta_1_2_3_distribution": {str(k): v for k, v in sorted(cnt.items())}}
    rng = random.Random(9); keys = rng.sample(list(seen), 150); bad = 0
    for m in keys:
        yb = fb.reduced_betti(fb.y_simplices(m, 6), 3)
        bad += yb[1] != 0
    out["direct_Y_sample"] = {"tested": 150, "H1_of_Y_nonzero": bad}
    out["seconds"] = round(time.time() - t0)
    json.dump(out, open(os.path.join(_path.ROOT, "RESULTS", "B24_symbolic_theorem_check.json"), "w"), indent=1); print(out)

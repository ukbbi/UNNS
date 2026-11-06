"""E26 -- third round: atlas_v2 (E22 census cycles + E24 false negatives) on fresh held-out contents (seed 26, 500+500 contents, labels <= 40)."""
import json, os, time
import _path
import E24_atlas_coverage as E24
import E25_refine as E25
t0 = time.time()
regimes, classes = E24.law_classes()
prev = json.load(open(os.path.join(_path.ROOT, "RESULTS", "E24_atlas_coverage.json")))["heldout"]
fn = sorted({(tuple(c), x[0]) for c, x in prev["false_negative"]})
classes2, _ = E25.add_cycles(classes, fn)
r = E24.heldout(classes2, 500, 500, seed=26)
out = {k: v for k, v in r.items() if k not in ("false_positive", "false_negative")}
out.update(n_false_positive=len(r["false_positive"]), n_false_negative=len(r["false_negative"]), false_negative=r["false_negative"], seconds=round(time.time() - t0, 1))
json.dump(out, open(os.path.join(_path.ROOT, "RESULTS", "E26_fresh_v2.json"), "w"), indent=1)
print(out)

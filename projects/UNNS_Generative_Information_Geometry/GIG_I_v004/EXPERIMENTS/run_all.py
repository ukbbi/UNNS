"""run all v004 experiments.  python run_all.py [--quick]   E17 (graph reconstruction of a k=7 beta_3 regime) is a separate long job:
python E17_h3_graph.py H3-4 [seconds]; run_all merges RESULTS/E17_*.json if present."""
import glob
import json
import os
import sys
import time
import _path
import E15_parametric
import E16_h3


def main():
    quick = "--quick" in sys.argv
    t0 = time.time()
    out = {"release": "GIG_I_v004", "mode": "quick" if quick else "full"}
    for name, mod in (("E15", E15_parametric), ("E16", E16_h3)):
        t = time.time()
        out[name] = mod.run(quick=quick)
        print(name, "done %.1fs" % (time.time() - t), flush=True)
    out["E17"] = [json.load(open(p)) for p in sorted(glob.glob(os.path.join(_path.RESULTS, "E17_*.json")))]
    out["seconds_total"] = round(time.time() - t0, 1)
    os.makedirs(_path.RESULTS, exist_ok=True)
    fn = "results_quick.json" if quick else "results.json"
    with open(os.path.join(_path.RESULTS, fn), "w") as f:
        json.dump(out, f, indent=1, default=str)
    print("wrote", fn, "total %.1fs" % out["seconds_total"])


if __name__ == "__main__":
    main()

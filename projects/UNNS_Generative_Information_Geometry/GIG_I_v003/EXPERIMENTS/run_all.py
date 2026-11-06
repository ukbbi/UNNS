"""run all v003 experiments.  python run_all.py [--quick]   (quick: minutes; full: roughly an hour on 2 CPUs)"""
import json
import os
import sys
import time
import _path
import E9_faces
import E10_h2
import E11_events
import E12_recovery
import E13_info
import E14_k7


def main():
    quick = "--quick" in sys.argv
    t0 = time.time()
    out = {"release": "GIG_I_v003", "mode": "quick" if quick else "full"}
    for name, mod in (("E9", E9_faces), ("E10", E10_h2), ("E11", E11_events), ("E12", E12_recovery), ("E13", E13_info), ("E14", E14_k7)):
        t = time.time()
        out[name] = mod.run(quick=quick)
        print(name, "done %.1fs" % (time.time() - t), flush=True)
    out["seconds_total"] = round(time.time() - t0, 1)
    os.makedirs(_path.RESULTS, exist_ok=True)
    fn = "results_quick.json" if quick else "results.json"
    with open(os.path.join(_path.RESULTS, fn), "w") as f:
        json.dump(out, f, indent=1, default=str)
    cov = {"E12": [{k: v for k, v in d.items()} for d in out["E12"]["domains"]], "E14": out["E14"]["summary"], "E14_unresolved": out["E14"]["unresolved"],
           "E14_scope": {k: out["E14"][k] for k in ("xmax", "time_budget_s", "symmetry_reduction", "scope")},
           "E9": {"contents_sampled_for_T16_T17": out["E9"]["T17_closed_form_vs_vertex_lcm"]["contents"]}}
    with open(os.path.join(_path.RESULTS, "search_coverage.json" if not quick else "search_coverage_quick.json"), "w") as f:
        json.dump(cov, f, indent=1, default=str)
    print("wrote", fn, "total %.1fs" % out["seconds_total"])


if __name__ == "__main__":
    main()

"""Run E5-E8 and write RESULTS/results.json, search_coverage.json and the certificates.
   python run_all.py            full run (L<=10 and L<=12 for k=6)      python run_all.py --quick   smaller bounds (smoke test)"""
import json
import os
import platform
import sys
import time
import _path
import E5_cycles, E6_realizability, E7_graph_iso, E8_cell_info
import certificates as ce
import cycle_types as ct
import cell_signature as cs
import cube_factor as cf
import history_complex as hc


def main():
    quick = "--quick" in sys.argv
    t0 = time.time()
    out = {"release": "GIG_I_v002", "python": platform.python_version(), "deterministic": True, "seed": 20261105}
    if quick:
        out["E5"] = E5_cycles.run(8, 7)
        out["E6"] = E6_realizability.run(((6, 8),), ((4, 14), (5, 9)))
        e7 = E7_graph_iso.run(((4, 14), (5, 9), (6, 8)))
        out["E8"] = E8_cell_info.run(6, 8)
        name = "results_quick.json"
    else:
        out["E5"] = E5_cycles.run(12, 10)
        out["E6"] = E6_realizability.run()
        e7 = E7_graph_iso.run()
        out["E8"] = E8_cell_info.run(6, 10)
        name = "results.json"
    certs = e7.pop("_certs")
    out["E7"] = e7
    # --- registered certificates
    allc = ct.all_cycles(6)
    pet = next(key for (key, t) in allc if t == "cube-petrie")
    brd = next(key for (key, t) in allc if t == "braid-hexagon")
    z1 = ce.pair_certificate("Z1_petrie_vs_braid", "NON-arithmetic arrangement sets: isomorphic swap graphs (6-cycles), different homology; "
                             "the Petrie vertex set is excluded from SELECT-II by GIG-T11", ("mask", sum(1 << i for i in pet)), ("mask", sum(1 << i for i in brd)),
                             note="shows exactly what the abstract swap graph forgets (generator colours) and what arithmetic admissibility forbids", k=6)
    w5 = ce.pair_certificate("W5_v001_nonisomorphic", "v001 witness W5: equal fine profile through radius 2; swap graphs are NOT isomorphic (exact); T15 explains why",
                             ((2, 3, 9, 15, 21), 189), ((1, 2, 12, 13, 26), 52), k=5)
    w6 = ce.pair_certificate("W6_v001_nonisomorphic", "v001 witness W6: as W5", ((2, 3, 8, 21, 26), 273), ((6, 8, 9, 14, 15), 168), k=5)
    certs += [z1, w5, w6]
    os.makedirs(_path.CERTS, exist_ok=True)
    out["certificates"] = []
    for c in certs:
        errs = ce.verify_certificate(c)
        c["verification_errors"] = errs
        ce.write(c, _path.CERTS)
        out["certificates"].append({"id": c["id"], "verified": not errs, "graph_isomorphic": c["graph_isomorphism"]["isomorphic"],
                                    "betti": [c["A"]["betti"], c["B"]["betti"]], "first_separating_radius": c["first_separating_radius"]})
    out["seconds"] = round(time.time() - t0, 1)
    os.makedirs(_path.RESULTS, exist_ok=True)
    with open(os.path.join(_path.RESULTS, name), "w") as f:
        json.dump(out, f, indent=1, default=str, sort_keys=True)
    cov = {"release": "GIG_I_v002", "domains": out["E6"]["coverage"],
           "isomorphism_search": [{k: d[k] for k in ("k", "L", "sets", "exact_isomorphism_tests", "iso_classes", "exhaustive_domain")} for d in e7["datasets"]],
           "statement": "every domain lists contents = ALL k-subsets of {1..L}; for each content ALL sources are covered by enumerating every divisor pattern of the threshold lcm; no closure caps, no skipped contents."}
    with open(os.path.join(_path.RESULTS, "search_coverage.json" if not quick else "search_coverage_quick.json"), "w") as f:
        json.dump(cov, f, indent=1, sort_keys=True)
    print("wrote", name, "in", out["seconds"], "s")


if __name__ == "__main__":
    main()

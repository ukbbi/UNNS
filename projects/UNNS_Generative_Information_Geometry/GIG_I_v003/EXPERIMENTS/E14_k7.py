"""E14 -- conditional, targeted k=7 probe (NOT a census).  Contents = each beta_2=1 anchor content plus one extra label x (x <= XMAX).
For every content ALL source regimes are enumerated exactly (T12/T18); Betti numbers of the inherited complex are computed for every regime
within the time budget (smallest regimes first); the graph-only reconstruction (T20) is exercised on the smallest regimes only (cost).
The report states content bounds, regime coverage, the (absent) symmetry reduction and every unresolved branch."""
import time
from collections import Counter
import _path  # noqa: F401
import source_filtration as sf
import cell_boundary as cb
import cell_signature as cs
import cell_recognition as cr
from E10_h2 import ANCHORS


def run(quick=False):
    t0 = time.time()
    xmax = 10 if quick else 16
    budget = 70 if quick else 1500
    gbudget = 20 if quick else 400
    gmax_n = 400
    out = {"experiment": "E14", "scope": "conditional targeted probe; anchors' contents extended by one label", "xmax": xmax,
           "time_budget_s": budget, "graph_budget_s": gbudget, "symmetry_reduction": "none used: contents are unordered label sets; regimes deduplicated by arrangement set only",
           "contents": [], "unresolved": []}
    work = []
    for name, (C, _s, _n) in ANCHORS.items():
        for x in range(1, xmax + 1):
            if x in C:
                continue
            work.append((name, tuple(sorted(C + (x,)))))
    gused = 0.0
    done_regs = tot_regs = 0
    for name, C in work:
        regs = sf.regimes(C)
        tot_regs += len(regs)
        rec = {"anchor": name, "content": C, "regimes": len(regs), "betti_computed": 0, "betti_histogram": Counter(), "beta2_positive": [],
               "graph_checked": 0, "graph_matches": 0, "max_N": max(r["N"] for r in regs), "min_N": min(r["N"] for r in regs)}
        for r in regs:
            if time.time() - t0 > budget:
                out["unresolved"].append({"content": C, "regimes_not_computed": len(regs) - rec["betti_computed"]})
                break
            cx = cb.Complex(r["mask"], 7)
            b = cx.betti()
            rec["betti_computed"] += 1
            done_regs += 1
            rec["betti_histogram"][b] += 1
            if b[2] or b[3]:
                rec["beta2_positive"].append({"L": r["L"], "N": r["N"], "betti": b})
            if r["N"] <= gmax_n and gused < gbudget:
                tg = time.time()
                g = cr.graph_complex(cs.adjacency(r["mask"], 7), 7)
                gused += time.time() - tg
                rec["graph_checked"] += 1
                rec["graph_matches"] += (g["f"], g["ranks"], g["betti"]) == (cx.f(), cx.ranks(), b)
        rec["betti_histogram"] = {str(k): v for k, v in sorted(rec["betti_histogram"].items())}
        out["contents"].append(rec)
        if time.time() - t0 > budget:
            done = {tuple(c["content"]) for c in out["contents"]}
            out["unresolved"] += [{"content": c, "regimes_not_computed": "all (content not reached)"} for _, c in work if c not in done]
            break
    out["summary"] = {"contents_planned": len(work), "contents_reached": len(out["contents"]), "regimes_enumerated": tot_regs, "regimes_with_betti": done_regs,
                      "regimes_with_beta2_or_beta3_positive": sum(len(c["beta2_positive"]) for c in out["contents"]),
                      "graph_reconstruction_checked": sum(c["graph_checked"] for c in out["contents"]),
                      "graph_reconstruction_matches": sum(c["graph_matches"] for c in out["contents"]),
                      "unresolved_branches": len(out["unresolved"])}
    out["seconds"] = round(time.time() - t0, 1)
    return out


if __name__ == "__main__":
    import json
    r = run(quick=True)
    print(json.dumps({k: v for k, v in r.items() if k != "contents"}, indent=1))
    for c in r["contents"]:
        print(c["content"], c["regimes"], c["betti_computed"], c["beta2_positive"], c["graph_checked"], c["graph_matches"])

"""E17 -- graph-only reconstruction (v003 T20 recognition) of a k=7 beta_3 regime: compare the face poset derived from the uncoloured graph
with the true one in every dimension.  Very slow (graph_complex on thousands of vertices); reports 'not completed' honestly on timeout.
usage: python E17_h3_graph.py H3-4 [seconds]"""
import json
import os
import signal
import sys
import time
import _path
import threshold_closure as tc
import cell_signature as cs
import cell_recognition as cr
import cell_boundary as cb
import _recovery as R   # v003 helper (true_cells)
import E16_h3


def run(name, budget):
    C, src = E16_h3.CASES[name]
    mask = tc.source_mask(C, src)
    t0 = time.time()
    res = {"experiment": "E17", "case": name, "content": C, "source": src, "N": mask.bit_count(), "budget_s": budget}

    def onalarm(*a):
        raise TimeoutError

    signal.signal(signal.SIGALRM, onalarm)
    signal.alarm(budget)
    try:
        cx = cb.Complex(mask, 7)
        g = cr.graph_complex(cs.adjacency(mask, 7), 7)
        tcells = R.true_cells(mask, 7)
        res.update({"completed": True, "true_f": cx.f(), "graph_f": g["f"], "true_ranks": cx.ranks(), "graph_ranks": g["ranks"],
                    "true_betti": cx.betti(), "graph_betti": g["betti"],
                    "poset_exact_match": all(set(g["cells"].get(d, [])) == tcells.get(d, set()) for d in range(7))})
    except TimeoutError:
        res.update({"completed": False, "note": "time budget exhausted; no conclusion drawn"})
    res["seconds"] = round(time.time() - t0, 1)
    with open(os.path.join(_path.RESULTS, "E17_%s.json" % name), "w") as f:
        json.dump(res, f, indent=1, default=str)
    return res


if __name__ == "__main__":
    print(run(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 3000))

"""E12 -- graph-to-3-cell (and all-dimensional) reconstruction from the UNCOLOURED swap graph (GIG-T20).
Compares the reconstructed face poset with the inherited complex EXACTLY (vertex-set equality, every dimension) on: every realizable set of
the exhaustive domains, a budgeted seeded random sample of the k=6 census, the full P_6, and the two anchors; plus the v002 Z1 pair as a
negative control (non-arithmetic, hypothesis violated)."""
import time
from collections import Counter
import _path  # noqa: F401
import _recovery as R
import threshold_closure as tc
import history_complex as hc
import cell_signature as cs
import cell_boundary as cb
import cell_recognition as cr
import cycle_types as ct


def z1_control():
    allc = ct.all_cycles(6)
    pet = next(key for (key, t) in allc if t == "cube-petrie")
    brd = next(key for (key, t) in allc if t == "braid-hexagon")
    out = {}
    for name, key in (("A_petrie", pet), ("B_braid", brd)):
        mask = sum(1 << i for i in key)
        cx = cb.Complex(mask, 6)
        adj = cs.adjacency(mask, 6)
        g = cr.graph_complex(adj, 6)
        out[name] = {"true_f": cx.f(), "true_betti": cx.betti(), "graph_derived_f": g["f"], "graph_derived_betti": g["betti"],
                     "reconstruction_correct": (g["f"], g["betti"]) == (cx.f(), cx.betti()), "cube_product_property": name != "A_petrie"}
    ident = out["A_petrie"]["graph_derived_f"] == out["B_braid"]["graph_derived_f"]
    wrong = [n for n, v in out.items() if not v["reconstruction_correct"]]
    return {"pair": out, "identical_graph_derived_output": ident, "reconstruction_fails_for": wrong,
            "reading": "isomorphic uncoloured graphs, different true complexes: no graph-only reconstruction can be correct for both; "
                       "the Petrie set violates the cube-product property (v002 T11), so T20's hypothesis is exactly what is needed"}


def t20b(kmax):
    """soundness in the full permutohedron: rooted count of convex induced copies of each face graph equals the number of true faces
    through the root (P_k is vertex-transitive).  k<=7: all face types of dim>=3; k=8: the three 3-face types."""
    import math
    rows = []
    for k in range(4, kmax + 1):
        full = (1 << math.factorial(k)) - 1
        host = cr.Host(cs.adjacency(full, k))
        types = cr.face_types(k, 3) if k <= 7 else [(4,), (3, 2), (2, 2, 2)]
        for bl in types:
            if k == 8 and kmax < 8:
                continue
            raw, conv, exp = cr.rooted_check(k, bl, host)
            rows.append({"k": k, "blocks": list(bl), "dim": sum(b - 1 for b in bl), "induced_copies_through_root": raw,
                         "convex_copies_through_root": conv, "true_faces_through_root": exp, "exact": conv == exp,
                         "spurious_induced_rejected_by_convexity": raw - conv})
    return {"all_exact": all(r["exact"] for r in rows), "rows": rows}


def run(quick=False):
    t0 = time.time()
    out = {"experiment": "E12", "domains": [], "T20b_full_permutohedron_soundness": t20b(7 if quick else 8)}
    full6 = sum(1 << i for i in range(720))
    anchors = [tc.source_mask((2, 3, 4, 5, 8, 9), 288), tc.source_mask((2, 3, 6, 7, 8, 9), 432), tc.source_mask((2, 3, 4, 5, 8, 9), 1440)]
    plan = [(4, 16, None, ()), (5, 10, None, ())] if quick else [(4, 40, None, ()), (5, 16, None, ())]
    plan.append((6, 8, 60, anchors) if quick else (6, 10, 1500, [full6] + anchors))
    for k, L, budget, extra in plan:
        s = R.scan(k, L, budget=budget, seed=20260611, extra=extra)
        rec = s["records"]
        bad = [r for r in rec if not (r["poset_match"] and r["numbers_match"])]
        out["domains"].append({"k": k, "L": L, "realizable_sets_in_domain": s["realizable_sets_in_domain"], "sets_checked": s["sets_checked"],
                               "exhaustive": s["exhaustive"], "poset_exact_matches": sum(r["poset_match"] for r in rec),
                               "f_rank_betti_matches": sum(r["numbers_match"] for r in rec), "failures": len(bad),
                               "boundary_squared_violations": sum(r["boundary_squared"] for r in rec),
                               "vertex_count_range": [min(r["n"] for r in rec), max(r["n"] for r in rec)], "seconds": s["seconds"],
                               "sampling": None if s["exhaustive"] else "seeded random order (seed 20260611) until the time budget; anchors%s first" % (", full P_6" if not quick else "")})
    if not quick:
        # full P_6: 3-faces reproduced from the graph
        g = cr.graph_complex(cs.adjacency(full6, 6), 6)
        by = Counter(len(S) for S in g["cells"][3])
        out["full_P6_graph_derived_3cells_by_vertex_count"] = {str(a): n for a, n in sorted(by.items())}
        out["full_P6_graph_derived_3cells_expected"] = {"8 (cube)": 90, "12 (hexagonal prism)": 360, "24 (truncated octahedron)": 90}
        out["full_P6_graph_derived_f"] = g["f"]
    out["Z1_negative_control"] = z1_control()
    out["seconds"] = round(time.time() - t0, 1)
    return out


if __name__ == "__main__":
    import json
    print(json.dumps(run(quick=True), indent=1))

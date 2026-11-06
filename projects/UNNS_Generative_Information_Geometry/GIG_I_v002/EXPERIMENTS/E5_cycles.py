"""E5 -- six-cycle classification in P_6, cubical factorization (T11) checks and exact realizability of cycle vertex sets."""
import time
from collections import Counter
import _path  # noqa: F401
import _common
import cycle_types as ct
import cube_factor as cf
import history_complex as hc
import threshold_closure as tc
import cell_signature as cs
from itertools import combinations


def run(Lmax=12, Lcycle=10):
    t0 = time.time()
    out = {"experiment": "E5"}
    # ---- classification of all 6-cycles of P_k
    out["classes_by_k"] = {}
    for k in (4, 5, 6, 7, 8):
        cl = ct.cycle_classes(k)
        out["classes_by_k"][k] = dict(Counter(ct.classify(w)[0] for w in cl))
    rows = []
    allc = ct.all_cycles(6)
    cnt = Counter(t for (_, t) in allc)
    for w in ct.cycle_classes(6):
        t, J, ie = ct.classify(w)
        rows.append({"word_1based": [j + 1 for j in w], "type": t, "colours": list(J), "induced_edges": ie,
                     "chordless": ie == 6})
    out["P6_class_table"] = rows
    out["P6_cycle_counts"] = dict(cnt)
    out["P6_total_6cycles"] = len(allc)
    # ---- T11: every realizable set, every commuting cube of dimension >= 2
    found, cov = _common.census(6, Lmax)
    tot_cubes = bad = 0
    hist = Counter()
    for mask in found:
        n, b, h = cf.fast_check(mask, 6)
        tot_cubes += n
        bad += b
        hist.update(h)
    out["T11_exhaustive"] = {"k": 6, "L": Lmax, "realizable_sets": len(found), "cubes_per_set": len(cf.cube_masks(6)),
                             "cube_set_pairs_checked": tot_cubes, "violations": bad,
                             "three_cube_slice_histogram": {str(a): b for a, b in sorted(hist.items())},
                             "forbidden_counts_observed": [a for a in (3, 5, 6, 7) if hist.get(a)]}
    # ---- exact realizability of the vertex set of every 6-cycle: route 1 (direct closure test), contents <= Lcycle
    P = hc.perms(6)
    pidx = hc.perm_index(6)
    contents = [tc.ContentClosure(C) for C in combinations(range(1, Lcycle + 1), 6)]
    per_type = {}
    for (key, t), vs in allc.items():
        mask = sum(1 << i for i in key)
        ex = sum(1 for cc in contents if cc.is_closed(mask))
        d = per_type.setdefault(t, {"cycles": 0, "exactly_realizable_pairs": 0, "cycles_ever_realizable": 0})
        d["cycles"] += 1
        d["exactly_realizable_pairs"] += ex
        d["cycles_ever_realizable"] += 1 if ex else 0
    out["exact_realizability_of_cycle_vertex_sets"] = {"contents": f"6-subsets of 1..{Lcycle}", "per_type": per_type}
    # ---- route 2: enumerate exactly-realizable 6-vertex sets in the census, classify those whose graph is a 6-cycle
    r2 = Counter()
    chordless_in_realizable = Counter()
    for mask in found:
        if mask.bit_count() == 6:
            adj = cs.adjacency(mask, 6)
            if all(len(a) == 2 for a in adj) and cs.graph_only_betti01(adj)[0] == 1:
                # connected 2-regular on 6 vertices = a 6-cycle; find its type via the set
                key = frozenset(i for i in range(720) if mask >> i & 1)
                ts = [t for (kk, t) in allc if kk == key]
                r2[ts[0] if ts else "?"] += 1
    out["census_exact_sixvertex_cycles"] = {"L": Lmax, "counts_by_type": dict(r2)}
    # ---- Petrie obstruction: any realizable set containing the vertices of a Petrie cycle contains its whole cube
    petrie = [(key, vs) for (key, t), vs in allc.items() if t == "cube-petrie"]
    cubes = cf.cube_masks(6, 3)
    contain = viol = 0
    for key, vs in petrie:
        pm = sum(1 << i for i in key)
        cube_of = [cm for cm, d, c in cubes if cm & pm == pm]
        assert len(cube_of) == 1
        cm = cube_of[0]
        for mask in found:
            if mask & pm == pm:
                contain += 1
                if mask & cm != cm:
                    viol += 1
    out["petrie_obstruction"] = {"petrie_cycles": len(petrie), "realizable_sets_containing_a_petrie_vertex_set": contain,
                                 "of_which_missing_part_of_the_cube": viol}
    out["seconds"] = round(time.time() - t0, 1)
    return out


if __name__ == "__main__":
    import json
    print(json.dumps(run(10, 8), indent=1))

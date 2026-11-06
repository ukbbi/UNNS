"""E8 -- higher-dimensional information: independent cell data, T13 reconstruction, T15 graph-only recovery, signature search."""
import time
from collections import Counter
from itertools import combinations
import _path  # noqa: F401
import _common
import cell_signature as cs
import history_complex as hc
import certificates as ce
import cycle_types as ct


def run(k=6, L=10, systole_cap=12, systole_max_sets=80):
    t0 = time.time()
    found, cov = _common.census(k, L)
    classes, recs, st = _common.classes(k, L)
    out = {"experiment": "E8", "k": k, "L": L, "sets": len(found)}
    # --- T13: faces / boundary ranks / Betti reconstructed from the COLOURED graph alone, vs inherited engine
    mism = ident = eul = 0
    data = {}
    for mask in found:
        d = cs.cell_data(mask, k)
        data[mask] = d
        if d["f"] != recs[mask]["f"] or d["betti"] != recs[mask]["betti"]:
            mism += 1
        if all(d["f"][j] - (d["ranks"][j - 1] if j >= 1 else 0) - (d["ranks"][j] if j < k - 1 else 0) == d["betti"][j] for j in range(k)):
            ident += 1
        eul += d["euler_ok"]
    out["T13_coloured_graph_reconstruction"] = {"sets_tested": len(found), "mismatches_with_inherited_complex": mism,
                                                "identity_beta_eq_f_minus_ranks_holds": ident, "euler_checks_passed": eul}
    # --- T15: uncoloured graph -> (beta0, beta1, f2)
    bad = 0
    for mask in found:
        b0, b1, f2 = cs.graph_only_betti01(recs[mask]["adj"])
        d = data[mask]
        if (b0, b1, f2) != (d["betti"][0], d["betti"][1], d["f"][2]):
            bad += 1
    out["T15_graph_only_recovery_of_beta0_beta1_f2"] = {"sets_tested": len(found), "failures": bad}
    # --- Q4: which small signatures determine the Betti vector in the census?
    betti = {m: data[m]["betti"] for m in found}

    def ambiguity(keyf):
        g = {}
        for m in found:
            g.setdefault(keyf(m), set()).add(betti[m])
        return sum(1 for s in g.values() if len(s) > 1), len(g)

    cands = {}
    f_idx = range(k)
    for r in range(1, k + 1):
        for sub in combinations(f_idx, r):
            a, n = ambiguity(lambda m, sub=sub: tuple(data[m]["f"][j] for j in sub))
            cands["f_" + "".join(map(str, sub))] = {"ambiguous_groups": a, "groups": n}
    out["f_subvector_signatures"] = {kk: v for kk, v in cands.items() if v["ambiguous_groups"] == 0}
    out["f_subvector_signatures_count_tested"] = len(cands)
    out["minimal_f_subvectors_determining_betti"] = _minimal_sets(cands, k)
    comp_c = lambda m: len(recs[m]["sizes"])  # number of components
    out["named_signatures"] = {
        "N_only": dict(zip(("ambiguous_groups", "groups"), ambiguity(lambda m: recs[m]["N"]))),
        "graph_cycle_rank_(N,E,components)": dict(zip(("ambiguous_groups", "groups"), ambiguity(lambda m: (recs[m]["N"], recs[m]["E"], comp_c(m))))),
        "full_f_vector": dict(zip(("ambiguous_groups", "groups"), ambiguity(lambda m: data[m]["f"]))),
        "f_vector_plus_graph_class": dict(zip(("ambiguous_groups", "groups"), ambiguity(
            lambda m: (data[m]["f"], next(i for i, cl in enumerate(classes) if m in cl))))) if len(found) < 4000 else "skipped (size)",
    }
    # --- higher Betti numbers present in the census
    hi = [m for m in found if any(betti[m][2:])]
    out["sets_with_beta_ge2"] = [{"N": recs[m]["N"], "betti": betti[m], "f": data[m]["f"], "content": found[m]["content"],
                                  "source_L": ce.source_value_of(found[m])} for m in hi]
    out["betti_vectors_in_census"] = {str(b): n for b, n in sorted(Counter(betti.values()).items())}
    # --- shortest unfilled cycle among sets with beta_1 > 0 (one per isomorphism class)
    seen, lens, used = set(), Counter(), 0
    for cl in classes:
        m = cl[0]
        if betti[m][1] > 0 and used < systole_max_sets:
            used += 1
            lens[cs.shortest_unfilled_cycle(recs[m]["adj"], systole_cap)] += 1
    out["shortest_unfilled_cycle_by_isoclass"] = {"classes_examined": used, "exhaustive_up_to_length": systole_cap,
                                                  "length_distribution": {str(a): b for a, b in sorted(lens.items(), key=lambda x: (x[0] is None, x[0]))}}
    # --- six-cycle census on graph-only data (search priorities 1 and 2)
    p1 = p2 = 0
    for cl in classes:
        m = cl[0]
        r = recs[m]
        if r["N"] <= 30:
            c = cs.six_cycle_census(r["adj"])
            if c["braid"] + c["petrie"] + c["chorded"]:
                p1 += 1
            if c["comp_both"]:
                p2 += 1
    out["search_priority_counts_on_isoclass_representatives"] = {"small_components_N_le_30_with_six_cycles": p1,
                                                                  "components_with_braid_and_nonbraid_six_cycles": p2}
    out["seconds"] = round(time.time() - t0, 1)
    return out


def _minimal_sets(cands, k):
    good = [tuple(int(c) for c in key[2:]) for key, v in cands.items() if v["ambiguous_groups"] == 0]
    good.sort(key=lambda s: (len(s), s))
    mins = []
    for s in good:
        if not any(set(m) <= set(s) for m in mins):
            mins.append(s)
    return [list(m) for m in mins]

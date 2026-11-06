"""E4 -- information versus history topology (GIG-Q1, GIG-Q2).

Sections
  A  inherited GEO-HD-1D examples, rebuilt from the cell rules:  {2,3,8,9}@72 (beta1=1), {2,3,8,9,14}@1008 (beta2=1)
  B  a loop inside a COMPLETE-history fibre:  {2,3,14,15}@210 (squarefree source) and the fibre of its endpoint
  C  certificates: information-equivalent pieces with different topology (exact, recomputed from scratch)
  D  census of realizable admissible sets (k=3,4,5): detection radius of the accessibility profile
  E  finite-exact verification of the proved I_1 / cycle-rank inequality over every census set
Usage:  python E4_topology.py            (default census bounds: k=3 L<=40, k=4 L<=30, k=5 L<=14; about a minute)
        python E4_topology.py --extended (k=4 L<=70, k=5 L<=26; roughly 15-20 minutes; figures quoted in RESULTS/report.md)
"""
import json, sys, time
from fractions import Fraction
from math import log2
import _path
import history_fibres as hf
import swap_graph as sg
import history_complex as hc
import census as cs
import information as inf


# ------------------------------------------------------------------ helpers
def piece_summary(content, m0, rmax=None):
    """exact information + topology summary of the piece (source m0, distinct-label content)."""
    k = len(content)
    A = hc.admissible_arrangements(content, m0)
    # independent check: simulation-based admissibility == threshold-law admissibility
    labs = sorted(content)
    thr_ok = all((hf.threshold(tuple(labs[i] for i in p)) != 0) and ((m0 % hf.threshold(tuple(labs[i] for i in p)) == 0) == (p in set(A)))
                 for p in hc.perms(k))
    mask = hc.vertex_mask(A, k)
    d = cs.mask_data(mask, k)
    ip = inf.information_profile(d["prof"], rmax)
    N = d["N"]
    return {
        "content": list(content), "source": m0, "source_squarefree": hf.is_squarefree(m0), "endpoint": hf_endpoint(content, m0),
        "N": N, "A_bits": inf.fmt(inf.hartley(N), 12), "E_edges": d["E"], "class_sizes": list(d["sizes"]),
        "H(C|T)": inf.fmt(inf.class_entropy(list(d["sizes"])), 12), "H(W|C,T)": inf.fmt(inf.within_class_entropy(list(d["sizes"])), 12),
        "max_component_diameter": d["D"], "degree_multiset": dict(sorted(_count(d["deg"]).items())),
        "P_r": [str(x) for x in d["Pr"]], "I_r_bits": [inf.fmt(x, 12) for x in ip],
        "betti_permutohedral": list(d["betti"]), "betti_cubical": list(d["cubical"]),
        "f_vector": list(hc.f_vector(mask, k)), "n_squares": hc.square_hexagon_counts(mask, k)[0], "n_hexagons": hc.square_hexagon_counts(mask, k)[1],
        "euler_characteristic": hc.euler_characteristic(mask, k), "euler_equals_alternating_betti": hc.euler_characteristic(mask, k) == sum((-1) ** i * b for i, b in enumerate(d["betti"])),
        "threshold_law_agrees_with_simulation": thr_ok, "_mask": mask, "_data": d,
    }


def hf_endpoint(content, m0):
    t = Fraction(m0)
    for N in content:
        t *= hf.R(N)
    assert t.denominator == 1
    return int(t)


def _count(seq):
    out = {}
    for x in seq:
        out[x] = out.get(x, 0) + 1
    return out


def strip(s):
    return {k: v for k, v in s.items() if not k.startswith("_")}


# ------------------------------------------------------------------ A
def section_A():
    res = {}
    for name, c, m in (("loop_2_3_8_9_at_72", (2, 3, 8, 9), 72), ("void_2_3_8_9_14_at_1008", (2, 3, 8, 9, 14), 1008)):
        s = piece_summary(c, m)
        t = s["endpoint"]
        H = sorted(hf.fixed_source_histories(m, t))
        pieces = hf.classify(H)
        rows = []
        for (src, q), hs in sorted(pieces.items(), key=lambda kv: kv[0][1]):
            row = {"content": list(q), "n_histories": len(hs), "distinct_labels": len(set(q)) == len(q)}
            adj = sg.swap_graph(hs)
            row["class_sizes"] = sorted(len(x) for x in sg.components(adj))
            if row["distinct_labels"]:
                k = len(q)
                row["betti_permutohedral"] = list(hc.betti(hc.admissible_arrangements(q, src), k))
            rows.append(row)
        res[name] = {"piece": strip(s), "endpoint": t, "fixed_source_fibre_size": len(H),
                     "fibre_pieces": rows, "fibre_betti_sum_over_distinct_label_pieces": _sum_betti(rows)}
    return res


def _sum_betti(rows):
    tot = None
    for r in rows:
        if "betti_permutohedral" in r:
            b = r["betti_permutohedral"]
            tot = b[:] if tot is None else [x + y for x, y in zip(tot + [0] * (len(b) - len(tot)), b + [0] * (len(tot) - len(b)))]
    return tot


# ------------------------------------------------------------------ B
def section_B():
    s = piece_summary((2, 3, 14, 15), 210)
    t = s["endpoint"]
    H = sorted(hf.complete_histories(t))
    pieces = hf.classify(H)
    piece_classes, topo = {}, {}
    for (src, q), hs in pieces.items():
        adj = sg.swap_graph(hs)
        piece_classes[(src, q)] = sorted(len(x) for x in sg.components(adj))
        if len(set(q)) == len(q):
            topo[(src, q)] = list(hc.betti(hc.admissible_arrangements(q, src), len(q)))
    ch = inf.uniform_chain(piece_classes)
    tally = {}
    for key, b in topo.items():
        tally[str(tuple(b))] = tally.get(str(tuple(b)), 0) + 1
    loops = [{"source": k[0], "content": list(k[1]), "betti": b} for k, b in sorted(topo.items()) if sum(b[1:]) > 0]
    return {
        "source_convention": "complete-history fibre F_t (squarefree sources)", "endpoint": t, "piece": strip(s),
        "fibre_size": len(H), "A_bits": inf.fmt(inf.hartley(len(H)), 12), "n_pieces": len(pieces),
        "n_pieces_distinct_labels": len(topo), "betti_tally_over_distinct_label_pieces": tally, "pieces_with_nontrivial_higher_homology": loops,
        "chain_uniform": {k: (inf.fmt(v, 12) if k != "N" else v) for k, v in ch.items()},
        "n_swap_classes": sum(len(v) for v in piece_classes.values()),
        "largest_piece": max(sum(v) for v in piece_classes.values()),
    }


# ------------------------------------------------------------------ C
CERTIFICATES = [
    {"id": "W1-loop-entropy", "claim": "entropy-level information cannot detect a loop (k=4, complete-history pieces)",
     "A": [(2, 3, 14, 15), 210], "B": [(1, 2, 3, 4), 6], "level": "r=0"},
    {"id": "W2-loop-entropy-inherited", "claim": "entropy-level information cannot detect the inherited loop {2,3,8,9}@72",
     "A": [(2, 3, 8, 9), 72], "B": [(2, 3, 5, 6), 30], "level": "r=0"},
    {"id": "W3-void-radius1", "claim": "even the full one-swap neighbourhood statistics cannot detect the 2-void of {2,3,8,9,14}@1008",
     "A": [(2, 3, 8, 9, 14), 1008], "B": [(1, 2, 3, 5, 7), 105], "level": "r=1"},
    {"id": "W4-loop-radius1", "claim": "one-swap neighbourhood statistics cannot detect a k=5 loop",
     "A": [(2, 3, 8, 9, 10), None], "B": [(1, 2, 3, 5, 9), None], "level": "r=1"},
    {"id": "W5-loop-radius2", "claim": "even radius-2 accessibility statistics cannot detect a loop (k=5): the two sets differ only in one hexagonal 2-cell",
     "A": [(2, 3, 9, 15, 21), 189], "B": [(1, 2, 12, 13, 26), 52], "level": "r=2"},
    {"id": "W6-loop-radius2-complete-history", "claim": "radius-2 statistics cannot detect a loop in a disconnected k=5 piece; A has a squarefree source (complete-history fibre)",
     "A": [(2, 3, 8, 21, 26), 273], "B": [(6, 8, 9, 14, 15), 168], "level": "r=2"},
]


def candidate_sets(content):
    """(source, permutation list) for every distinct realizable admissible set of the content (sources from the lcm closure, ascending)."""
    k = len(content)
    P = hc.perms(k)
    thr = [hf.threshold(tuple(sorted(content)[i] for i in p)) for p in P]
    S = cs.lcm_closure(set(thr), 100000)
    seen = set()
    for m in sorted(S):
        A = tuple(p for p, K in zip(P, thr) if m % K == 0)
        if A and A not in seen:
            seen.add(A)
            yield m, A


def find_source(content, want_betti, N=None, match=None):
    """smallest source whose piece has Betti vector `want_betti`, size N, and (optionally) the same radius-1 fine signature as `match`
    (a mask_data dict)."""
    k = len(content)
    for m, A in candidate_sets(content):
        if (N is None or len(A) == N) and hc.betti(A, k) == want_betti:
            if match is None or cs.truncated_signature(cs.mask_data(hc.vertex_mask(A, k), k), 1) == cs.truncated_signature(match, 1):
                return m
    return None


def section_C():
    out = []
    for c in CERTIFICATES:
        c = json.loads(json.dumps(c))
        if c["A"][1] is None:   # resolve sources deterministically: smallest source realizing the stated size and Betti
            c["A"][1] = find_source(tuple(c["A"][0]), (1, 1, 0, 0, 0), 40)
            ma = piece_summary(tuple(c["A"][0]), c["A"][1])["_data"]
            c["B"][1] = find_source(tuple(c["B"][0]), (1, 0, 0, 0, 0), 40, match=ma)
        a, b = piece_summary(tuple(c["A"][0]), c["A"][1]), piece_summary(tuple(c["B"][0]), c["B"][1])
        da, db = a["_data"], b["_data"]
        r1_equal = cs.truncated_signature(da, 1) == cs.truncated_signature(db, 1)
        rec = {
            "id": c["id"], "claim": c["claim"], "level": c["level"], "A": strip(a), "B": strip(b),
            "same_N": a["N"] == b["N"], "same_class_sizes": a["class_sizes"] == b["class_sizes"],
            "same_H_C_and_H_W_given_C": a["H(C|T)"] == b["H(C|T)"] and a["H(W|C,T)"] == b["H(W|C,T)"],
            "same_fine_signature_r_le_1": r1_equal, "same_E_edges": a["E_edges"] == b["E_edges"],
            "same_I_1": a["I_r_bits"][1] == b["I_r_bits"][1] if len(a["I_r_bits"]) > 1 and len(b["I_r_bits"]) > 1 else None,
            "same_P_2": (da["Pr"][min(2, da["D"])] == db["Pr"][min(2, db["D"])]),
            "same_fine_signature_r_le_2": cs.truncated_signature(da, 2) == cs.truncated_signature(db, 2),
            "same_fine_signature_r_le_3": cs.truncated_signature(da, 3) == cs.truncated_signature(db, 3),
            "same_N_E_squares": (a["N"], a["E_edges"], a["n_squares"]) == (b["N"], b["E_edges"], b["n_squares"]),
            "hexagon_counts_A_B": [a["n_hexagons"], b["n_hexagons"]],
            "betti_A": a["betti_permutohedral"], "betti_B": b["betti_permutohedral"],
            "topologies_differ": a["betti_permutohedral"] != b["betti_permutohedral"],
            "separating_radius": next((r for r in range(0, 12) if cs.truncated_signature(da, r) != cs.truncated_signature(db, r)), None),
        }
        out.append(rec)
    return out


# ------------------------------------------------------------------ D, E
def section_DE(specs):
    D, E = {}, {}
    for k, L, cap in specs:
        t0 = time.time()
        found, skipped = cs.realizable_masks(k, L, cap)
        datas = []
        betti_count, squarefree_count = {}, {}
        i1_ok = b2_ok = eul_ok = True
        for mask, info in found.items():
            d = cs.mask_data(mask, k)
            d["sq"] = info["sq"]
            datas.append(d)
            betti_count[str(d["betti"])] = betti_count.get(str(d["betti"]), 0) + 1
            if info["sq"]:
                squarefree_count[str(d["betti"])] = squarefree_count.get(str(d["betti"]), 0) + 1
            # E: I_1 <= log2(1 + 2E/N) with E = N - b0 + b1(G); equality iff regular. Exact integer test: P_1^(1/N) <= 1+2E/N
            N, Ed, kb0 = d["N"], d["E"], len(d["sizes"])
            P1 = d["Pr"][1] if d["D"] >= 1 else 1
            i1_ok &= (P1 * N ** N <= (N + 2 * Ed) ** N)         # prod(1+deg) <= ((N+2E)/N)^N, in integers
            P_ = hc.perms(k)
            _, adj_ = hc.induced_adjacency({P_[i] for i in range(len(P_)) if mask >> i & 1}, k)
            ok2, maxc, tri = sg.ball2_check(adj_)
            b2_ok &= ok2 and maxc <= 2 and tri
            eul_ok &= (hc.euler_characteristic(mask, k) == sum((-1) ** i * b for i, b in enumerate(d["betti"])))
        key = "k%d_L%d" % (k, L)
        D[key] = {"k": k, "label_bound": L, "closure_cap": cap, "contents_skipped": skipped, "distinct_realizable_sets": len(found),
                  "betti_counts": betti_count, "squarefree_source_realizable_betti_counts": squarefree_count,
                  "detection_table": cs.detection_table(datas, 4), "seconds": round(time.time() - t0, 1)}
        E[key] = {"I1_jensen_bound_holds_for_all_sets": i1_ok, "radius2_ball_formula_holds_for_all_sets": b2_ok,
                  "euler_characteristic_equals_alternating_betti_for_all_sets": eul_ok, "n_sets": len(datas)}
    return D, E


def run(extended=False):
    specs = [(3, 40, 30000), (4, 30, 30000), (5, 14, 20000)]
    if extended:
        specs = [(3, 40, 30000), (4, 70, 30000), (5, 26, 40000)]
    D, E = section_DE(specs)
    return {"A_inherited_examples": section_A(), "B_complete_history_loop": section_B(), "C_certificates": section_C(),
            "D_census": D, "E_I1_inequality_check": E}


if __name__ == "__main__":
    r = run("--extended" in sys.argv)
    print(json.dumps(r, indent=1, default=str))

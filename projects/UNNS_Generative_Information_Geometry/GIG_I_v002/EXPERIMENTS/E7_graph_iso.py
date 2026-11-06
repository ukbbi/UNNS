"""E7 -- exact graph-isomorphism comparison of realizable swap graphs; decisive target  G_A ~ G_B  with  beta(X_A) != beta(X_B)."""
import time
from collections import Counter
import _path  # noqa: F401
import _common
import certificates as ce
import cell_signature as cs
import swap_graph as sg
import history_complex as hc
import census as v1census
from itertools import permutations


def fine_vectors(adj, rmax=10):
    prof = sg.ball_profile(adj)
    return Counter(tuple(sg.ball_size(p, j) for j in range(rmax + 1)) for p in prof), tuple(sorted(len(c) for c in sg.components(adj)))


def sig(fv, r):
    vecs, sizes = fv
    c = Counter()
    for v, n in vecs.items():
        c[v[:r + 1]] += n
    return (sizes, tuple(sorted(c.items())))


def sym_orbit(mask, k, G):
    bits = [i for i in range(mask.bit_length()) if mask >> i & 1]
    out = set()
    for mp in G:
        m = 0
        for i in bits:
            m |= 1 << mp[i]
        out.add(m)
    return out


def run_dataset(k, L, cert_store, rmax=10, orbit=True):
    t0 = time.time()
    found, cov = _common.census(k, L)
    classes, recs, st = _common.classes(k, L)
    res = {"k": k, "L": L, "sets": len(found), "invariant_groups": st["invariant_groups"], "exact_isomorphism_tests": st["exact_comparisons"],
           "iso_classes": st["iso_classes"], "exhaustive_domain": cov["closure_cap_exclusions"] == 0}
    multi = [cl for cl in classes if len(cl) > 1]
    res["iso_classes_with_several_sets"] = len(multi)
    res["sets_in_those_classes"] = sum(len(c) for c in multi)
    res["max_class_size"] = max(len(c) for c in classes)
    dec = [cl for cl in classes if len({recs[m]["betti"] for m in cl}) > 1]
    res["DECISIVE_iso_classes_with_different_betti"] = len(dec)
    res["iso_classes_with_different_f_vector"] = sum(1 for cl in classes if len({recs[m]["f"] for m in cl}) > 1)
    # weisfeiler-lehman collisions: invariant groups that contain more than one exact class
    inv = Counter()
    for cl in classes:
        r = recs[cl[0]]
        inv[(r["N"], r["E"], r["deg"], r["sizes"], r["wl"])] += 1
    res["wl_collisions_nonisomorphic_same_invariants"] = sum(1 for v in inv.values() if v > 1)
    # priority 3: groups sharing order, edges, degree multiset, component sizes with several Betti vectors
    g3 = {}
    for m, r in recs.items():
        g3.setdefault((r["N"], r["E"], r["deg"], r["sizes"]), set()).add(r["betti"])
    res["priority3_groups_with_several_betti"] = sum(1 for s in g3.values() if len(s) > 1)
    # symmetry orbits inside nontrivial classes (coloured-isomorphism ambiguity of the uncoloured graph)
    if orbit and k <= 6:
        P = hc.perms(k)
        pidx = hc.perm_index(k)
        G = []
        for g in permutations(range(k)):
            for rev in (0, 1):
                mp = []
                for p in P:
                    q = tuple(g[x] for x in p)
                    if rev:
                        q = q[::-1]
                    mp.append(pidx[q])
                G.append(mp)
        import graph_iso as gi
        amb = amb_bet = col_amb = col_amb_bet = col_amb_f = 0
        for cl in multi:
            left = list(cl)
            reps = []
            while left:
                o = sym_orbit(left[0], k, G)
                reps.append(left[0])
                left = [m for m in left if m not in o]
            if len(reps) > 1:
                amb += 1
                if len({recs[m]["betti"] for m in cl}) > 1:
                    amb_bet += 1
                # coloured isomorphism (up to the Coxeter-diagram reversal) between orbit representatives
                cc = []
                for m in reps:
                    a, ea = cs.coloured_adjacency(m, k)
                    placed = False
                    for grp in cc:
                        b0, eb0 = cs.coloured_adjacency(grp[0], k)
                        _, ebr = cs.coloured_adjacency(grp[0], k, reverse=True)
                        if gi.find_isomorphism(a, b0, ea, eb0) is not None or gi.find_isomorphism(a, b0, ea, ebr) is not None:
                            grp.append(m)
                            placed = True
                            break
                    if not placed:
                        cc.append([m])
                if len(cc) > 1:
                    col_amb += 1
                    if len({recs[m]["betti"] for cl2 in cc for m in cl2}) > 1:
                        col_amb_bet += 1
                    if len({recs[m]["f"] for cl2 in cc for m in cl2}) > 1:
                        col_amb_f += 1
        res["iso_classes_containing_several_symmetry_orbits"] = amb
        res["of_which_with_different_betti"] = amb_bet
        res["iso_classes_with_several_COLOURED_classes_mod_coxeter"] = col_amb
        res["of_which_with_different_betti_coloured"] = col_amb_bet
        res["of_which_with_different_f_vector_coloured"] = col_amb_f
    # fine signature detection table (C1 / C2 evidence)
    fvs = {m: fine_vectors(recs[m]["adj"], rmax) for m in found}
    det = []
    first_zero = None
    for r in range(rmax + 1):
        groups = {}
        for m in found:
            groups.setdefault(sig(fvs[m], r), set()).add(recs[m]["betti"])
        amb = sum(1 for s in groups.values() if len(s) > 1)
        det.append({"r": r, "fine_groups": len(groups), "groups_with_several_betti": amb})
        if amb == 0 and first_zero is None:
            first_zero = r
    res["fine_signature_detection"] = det
    res["radius_at_which_fine_profile_determines_betti"] = first_zero
    # certificate for the pair that agrees longest (largest radius with an ambiguous group), if any
    best = None
    for r in range(rmax, -1, -1):
        groups = {}
        for m in found:
            groups.setdefault(sig(fvs[m], r), []).append(m)
        for g in groups.values():
            bs = {}
            for m in g:
                bs.setdefault(recs[m]["betti"], m)
            if len(bs) > 1:
                best = (r, list(bs.values())[:2])
                break
        if best:
            break
    if best:
        r, (a, b) = best
        fa, fb = found[a], found[b]
        pair = [(fa["content"], ce.source_value_of(fa)), (fb["content"], ce.source_value_of(fb))]
        cert = ce.pair_certificate(f"K{k}L{L}_closest", f"closest approach: equal fine profile through radius {r}, different Betti", pair[0], pair[1])
        cert_store.append(cert)
        res["closest_approach"] = {"agree_through_radius": r, "first_separating_radius": cert["first_separating_radius"],
                                   "betti": [cert["A"]["betti"], cert["B"]["betti"]],
                                   "contents_sources": [[fa["content"], pair[0][1]], [fb["content"], pair[1][1]]]}
    res["seconds"] = round(time.time() - t0, 1)
    return res


def run(datasets=((4, 40), (5, 16), (6, 10), (6, 12))):
    out = {"experiment": "E7", "datasets": []}
    certs = []
    for k, L in datasets:
        out["datasets"].append(run_dataset(k, L, certs))
    out["_certs"] = certs
    return out

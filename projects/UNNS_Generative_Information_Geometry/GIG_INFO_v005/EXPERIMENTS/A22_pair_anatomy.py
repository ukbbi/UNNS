"""A22 -- forbidden-complex anatomy of the two certified sharp pairs: dead sets, hollow triangles, why the cycle bounds in the negative."""
import json, os, itertools
import _path, nerve
import A21_motifs as M

PAIRS = [((2, 3, 4, 5, 8, 15), 480, 800, "INFO v002 pair"), ((2, 4, 5, 9, 14, 15), 2520, 3780, "INFO v003 witness")]

def lab(I, C): return nerve.label_set(I, C)

if __name__ == "__main__":
    out = {}
    for C, mp, mn, tag in PAIRS:
        rec = {"content": list(C), "positive_source": mp, "negative_source": mn, "tag": tag}
        mP, mN = nerve.arithmetic_mask(C, mp), nerve.arithmetic_mask(C, mn)
        rec["N"] = [mP.bit_count(), mN.bit_count()]
        DP, DN = nerve.dead_sets(mP), nerve.dead_sets(mN)
        rec["prefix_defined"] = [nerve.is_prefix_defined(mP), nerve.is_prefix_defined(mN)]
        rec["Y_betti"] = [nerve.y_betti(mP, 2), nerve.y_betti(mN, 2)]
        rec["nerve_betti"] = [nerve.nerve_betti(DP, 1), nerve.nerve_betti(DN, 1)]
        rec["|D|"] = [len(DP), len(DN)]
        rec["dead_only_in_positive"] = sorted(lab(I, C) for I in DP - DN)
        rec["dead_only_in_negative"] = sorted(lab(I, C) for I in DN - DP)
        rec["forbidden_prefix_sets_sizes"] = [len(nerve.forbidden_prefix_sets(mP)), len(nerve.forbidden_prefix_sets(mN))]
        D1, ht1, nb1 = M.analyse(mP); D2, ht2, nb2 = M.analyse(mN)
        rec["hollow_triangles"] = [len(ht1), len(ht2)]; rec["nonbounding_hollow"] = [len(nb1), len(nb2)]
        rec["nonbounding_hollow_triangles_positive"] = [[lab(x, C) for x in t] for t in nb1]
        rec["hollow_triangles_negative"] = [[lab(x, C) for x in t] for t in ht2]
        # matching: positive nonbounding triangles and which of their vertices are dead in negative
        rec["positive_nb_triangle_vertices_dead_in_negative"] = [[x in DN for x in t] for t in nb1]
        # certificate
        if nb1:
            cert = nerve.cocycle_certificate(DP, list(nb1[0]))
            c_edges = cert[0]
            rec["cocycle_certificate"] = {"cycle": list(nb1[0]), "cocycle_edges": [list(e) for e in c_edges], "verified": nerve.check_cocycle(c_edges, DP, list(nb1[0]))}
        # which cone vertices fill each negative hollow triangle
        fills = []
        for t in ht2:
            cones = [d for d in DN if all(any(all(x in nerve.COMP[z] for x in (a, b, d)) for z in nerve.SUBS) for a, b in itertools.combinations(t, 2))]
            fills.append({"triangle": [lab(x, C) for x in t], "cone_vertices_in_D_neg": [lab(d, C) for d in cones]})
        rec["negative_hollow_fillers"] = fills[:20]
        out[tag] = rec
        print(tag, {k: v for k, v in rec.items() if k not in ("cocycle_certificate", "negative_hollow_fillers", "hollow_triangles_negative")}, flush=True)
    json.dump(out, open(os.path.join(_path.ROOT, "RESULTS", "A22_pair_anatomy.json"), "w"), indent=1)

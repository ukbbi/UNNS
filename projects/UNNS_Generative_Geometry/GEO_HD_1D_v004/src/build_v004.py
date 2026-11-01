"""HD-1D v004 builder: writes results/*.json.   python build_v004.py   (about 2-3 minutes)"""
import os, sys, json, itertools, random, time
from math import gcd, lcm
from fractions import Fraction
from collections import Counter, defaultdict
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
from thresholds import K, threshold_table, split_sources, classes_at
from valuation_matrix import matrix, R, multiplier, displacement, product_P, delta
from integer_kernel import kernel_of_alphabet, graver_candidates, int_kernel
from primitive_moves import fibre_by_length, components
from block_rewrites import word_arrangements, move_blocks, admissible, state_after, rewrite_neighbours
from rewrite_graph import analyse, fibre_contents, divisors_of_P, words_of
from rewrite_complex import build_cubes, betti
from occurrence_events import summary, fibre_sequence


def dump(name, obj):
    with open(os.path.join(ROOT, "results", name), "w") as f: json.dump(obj, f, indent=1, sort_keys=True, default=str)


def v(n, p):
    e = 0
    while n % p == 0: n //= p; e += 1
    return e


def minimal_set(S): return sorted(a for a in S if not any(b != a and a % b == 0 for b in S))


def merger_kernel():
    out = {"alphabets": {}}
    for A in [(1, 2, 3), (1, 2, 8), (2, 3, 8), (1, 2, 3, 8)]:
        ps, V = matrix(A); ker = kernel_of_alphabet(A); gr = [z for z in graver_candidates(A, 8) if next(x for x in z if x) > 0]
        out["alphabets"][str(A)] = {"primes": ps, "V": V, "Z_kernel_basis": [list(z) for z in ker], "graver_box8_up_to_sign": [list(z) for z in gr]}
    # D4-T1 exhaustive in a box: all admissible words of length <= 8 over {1,2,3,8} from source 72*... grouped by endpoint
    A = (1, 2, 3, 8); ps, V = matrix(A); bad = n = 0
    for m in (72, 144, 1296, 2 ** 6 * 3 ** 4):
        by = defaultdict(list)
        def rec(w, s):
            by[s].append(tuple(w.count(N) for N in A))
            if len(w) >= 7: return
            for N in A:
                if s % N == 0:
                    w.append(N); rec(w, s // N * (N + 1) ** 2); w.pop()
        rec([], m)
        for s, cs in by.items():
            for c1, c2 in itertools.combinations(cs, 2):
                n += 1
                if any(sum(V[i][j] * (c1[j] - c2[j]) for j in range(4)) for i in range(len(ps))): bad += 1
        # converse: different endpoints => displacement differs
        keys = list(by)
        for s1, s2 in itertools.combinations(keys[:200], 2):
            c1, c2 = by[s1][0], by[s2][0]
            if all(sum(V[i][j] * (c1[j] - c2[j]) for j in range(4)) == 0 for i in range(len(ps))): bad += 1
    out["D4_T1_box"] = {"pairs_same_endpoint_checked": n, "violations": bad}
    # D4-T2: realization from m = prod N^{|z|}, and minimal sources
    t2 = []
    for A in [(1, 2, 3), (1, 2, 8), (2, 3, 8), (1, 2, 3, 8)]:
        for z in [z for z in graver_candidates(A, 6 if len(A) == 4 else 8) if next(x for x in z if x) > 0]:
            mi, pl = move_blocks(A, z)
            m = 1
            for N, c in zip(A, z): m *= N ** abs(c)
            Wp, Wm = word_arrangements(pl), word_arrangements(mi)
            allok = all(admissible(m, w) for w in Wp + Wm)
            ends = {state_after(m, w) for w in Wp + Wm}
            Kp = minimal_set({K(w) for w in Wp}); Km = minimal_set({K(w) for w in Wm})
            pairs = minimal_set({lcm(a, b) for a in Kp for b in Km})
            t2.append({"alphabet": list(A), "z": list(z), "source": m, "all_arrangements_admissible": allok, "single_endpoint": len(ends) == 1,
                       "minimal_thresholds_plus": Kp, "minimal_thresholds_minus": Km, "minimal_sources_for_the_pair": pairs})
    out["D4_T2"] = t2
    # D4-T4: kernel of {1,2,3} is Z(7,-2,-4)
    A = (1, 2, 3); box = [z for z in itertools.product(range(-30, 31), repeat=3) if any(z) and
                          all(sum(r[j] * z[j] for j in range(3)) == 0 for r in matrix(A)[1])]
    out["D4_T4"] = {"kernel_basis": [list(z) for z in kernel_of_alphabet(A)], "box30_kernel_vectors": len(box),
                    "all_multiples_of_7_-2_-4": all(z[0] % 7 == 0 and z == tuple(z[0] // 7 * x for x in (7, -2, -4)) for z in box)}
    # D-B1
    Aw = (1,) * 7; Bw = (2, 2, 3, 3, 3, 3)
    out["D_B1"] = {"R_identity": [str(R(1) ** 7), str(R(2) ** 2 * R(3) ** 4)], "endpoints": [state_after(4, Aw), state_after(4, Bw)],
                   "K_A": K(Aw), "K_B_this_order": K(Bw), "min_K_over_arrangements_of_B": min(K(w) for w in word_arrangements([(2, 2), (3, 4)])),
                   "admissible_arrangements_of_B_from_4": sum(1 for w in word_arrangements([(2, 2), (3, 4)]) if admissible(4, w)),
                   "fibre_sequence_A": [sorted(F) for F in fibre_sequence(4, Aw)], "fibre_sequence_B": [sorted(F) for F in fibre_sequence(4, Bw)],
                   "complete_from_root_1": [state_after(1, (1,) + Aw), state_after(1, (1,) + Bw)]}
    dump("MERGER_KERNEL.json", out); return out


def rewrite_thresholds():
    random.seed(4); labs = (1, 2, 3, 8); ok = n = 0; bad = 0
    moves = [(1, -4, 0, 2), (7, -2, -4, 0), (3, 1, -2, -1), (4, -3, -2, 1), (2, 5, -2, -3)]
    for _ in range(6000):
        z = random.choice(moves); mi, pl = move_blocks(labs, z); u = random.choice(word_arrangements(mi)); vv = random.choice(word_arrangements(pl))
        p = tuple(random.choice(labs) for _ in range(random.randint(0, 3))); s = tuple(random.choice(labs) for _ in range(random.randint(0, 3)))
        m = random.choice([2 ** a * 3 ** b for a in range(0, 8) for b in range(0, 6)])
        h1, h2 = p + u + s, p + vv + s
        lhs = admissible(m, h1) and admissible(m, h2)
        mid = state_after(m, p)
        rhs1 = mid is not None and admissible(m, h1) and admissible(mid, vv)
        rhs2 = m % lcm(K(h1), K(h2)) == 0
        n += 1; bad += (lhs != rhs2) or (admissible(m, h1) and (lhs != rhs1))
    out = {"tests": n, "violations": bad}
    dump("REWRITE_THRESHOLDS.json", out); return out


def cubes():
    out = {}
    A, B = (1,) * 7, (2, 2, 3, 3, 3, 3)
    for r in range(1, 6):
        ws = []
        for ch in itertools.product((0, 1), repeat=r):
            w = ()
            for c in ch: w += B if c else A
            ws.append((ch, w))
        ends = {state_after(4, w) for _, w in ws}; adm = all(admissible(4, w) for _, w in ws)
        contents = Counter(w.count(2) // 2 for _, w in ws)
        rec = {"vertices": len(ws), "all_admissible": adm, "single_endpoint": ends == {4 ** (7 * r + 1)}, "distinct": len({w for _, w in ws}) == 2 ** r,
               "number_of_contents": len(contents)}
        if r <= 4:
            wl = [w for _, w in ws]
            # one-block replacements only (specific arrangements): the 1-skeleton is exactly the r-cube graph
            blocks = [([A], [B])]
            cells = build_cubes(wl, 4, blocks, maxdim=r)
            rec["cells_by_dim"] = {str(d): len(c) for d, c in sorted(cells.items())}; rec["betti"] = list(betti(cells))
        out[str(r)] = rec
    dump("CUBES.json", out); return out


def saturation_and_dichotomy():
    labels = (1, 2, 3, 8); z = (1, -4, 0, 2); out = {"dichotomy": {}, "saturation": {"checked": 0, "violations": 0}}
    for j in range(1, 9):
        contents = fibre_contents((0, 4, j, 0), z, 2); P, ds = divisors_of_P(labels, contents)
        rows = []
        for d in ds:
            res = analyse(d, labels, [z], contents)
            per = Counter(res["content_of"][cl[0]] for cl in res["swap"]); both = len(set(res["content_of"])) == 2
            a, b = v(d, 2), v(d, 3)
            rows.append({"a": a, "b": b, "words": res["n"], "both": both, "swap_classes": len(res["swap"]), "rewrite_classes": len(res["rewrite"]), "max_swap_per_content": max(per.values()) if per else 0})
            sat = all(d % product_P(labels, c) == 0 for c in contents)
            out["saturation"]["checked"] += 1
            if sat and len(res["rewrite"]) != 1: out["saturation"]["violations"] += 1
        pred_bad = [r for r in rows if r["both"] and ((r["rewrite_classes"] == 1) != (r["b"] >= 1 or r["a"] >= 4))]
        out["dichotomy"][str(j)] = {"P_star": P, "sources": len(rows), "both_nonempty": sum(r["both"] for r in rows), "prediction_violations": len(pred_bad),
                                    "one_swap_class_per_content_everywhere": all(r["max_swap_per_content"] <= 1 for r in rows),
                                    "obstructed_sources": [(r["a"], r["b"]) for r in rows if r["both"] and r["rewrite_classes"] > 1],
                                    "saturation_bound_exponents": [v(P, 2), v(P, 3)]}
    dump("DICHOTOMY.json", out); return out


def completeness_123():
    labels = (1, 2, 3); z = (7, -2, -4); nf = tot = 0; bad = []
    for a in range(0, 2):
        for b in range(0, 5):
            for c in range(0, 9):
                L = min(b // 2, c // 4) + 1
                if L < 2: continue
                contents = fibre_contents((a, b, c), z, L); P, ds = divisors_of_P(labels, contents); nf += 1
                for d in ds:
                    res = analyse(d, labels, [z], contents); tot += 1
                    if res["n"] and len(res["rewrite"]) > 1: bad.append(((a, b, c), L, d))
    out = {"fibres": nf, "fibre_source_pairs": tot, "disconnected": bad, "box": "a<=1, b<=4, c<=8, fibre length >= 2, ALL sources (divisors of P*)"}
    dump("COMPLETENESS_123.json", out); return out


def generators():
    A = (1, 2, 3, 8); z1, z2 = (1, -4, 0, 2), (7, -2, -4, 0)
    gr = [z for z in graver_candidates(A, 8) if next(x for x in z if x) > 0]
    seen = set(); defic = []; nfib = 0; irr = Counter(); nonconf = []; unequal = []
    for c in itertools.product(range(0, 8), repeat=4):
        if sum(c) > 13: continue
        d = tuple(displacement(A, c))
        if d in seen: continue
        seen.add(d); fib = fibre_by_length(A, d, 14); nfib += 1
        two = components(fib, [z1, z2]); full = components(fib, gr)
        if len(two) > len(full): defic.append((len(fib), sum(c), c, len(two), len(full)))
        # content-level oriented system: replace the longer side by the shorter side; irreducible contents
        S = set(fib); irreducible = []
        for x in S:
            red = False
            for z in gr:
                for sg in (1, -1):
                    y = tuple(a + sg * b for a, b in zip(x, z))
                    if y in S and sum(y) < sum(x): red = True
            if not red: irreducible.append(x)
        irr[len(irreducible)] += 1
        if len(irreducible) >= 2 and len({sum(x) for x in irreducible}) > 1: unequal.append(c)
        if len(irreducible) >= 2: nonconf.append((len(fib), sum(min(f) for f in [c]) if False else sum(c), c, sorted(irreducible)))
    defic.sort(); smallest = defic[0]
    # the smallest deficient fibre, operationally
    base = (0, 0, 2, 1); z3 = (3, 1, -2, -1); contents = [base, tuple(a + b for a, b in zip(base, z3))]
    P, ds = divisors_of_P(A, contents); rows = []
    for d in ds:
        r1 = analyse(d, A, [z1, z2], contents); r3 = analyse(d, A, [z3], contents)
        rows.append({"a": v(d, 2), "b": v(d, 3), "words": r1["n"], "classes_with_z1_z2": len(r1["rewrite"]), "classes_with_z3": len(r3["rewrite"])})
    out = {"graver_up_to_sign": [list(z) for z in gr], "fibres_scanned": nfib, "deficient_fibres_for_z1_z2": len(defic), "smallest_deficient": list(smallest[2:]),
           "irreducible_contents_histogram": dict(irr), "fibres_with_irreducibles_of_unequal_length": len(unequal), "smallest_nonconfluent_fibre": sorted(nonconf)[0] if nonconf else None, "operational_table_for_smallest": rows, "P_star": P}
    dump("GENERATORS.json", out); return out


def extended_topology():
    out = {}
    # benchmark: source 4, 1^7 <-> arrangements of 2^2 3^4 (cubical complex, no coherence cells)
    labels = (1, 2, 3); z = (7, -2, -4); contents = fibre_contents((0, 2, 4), z, 2)
    blocks = [(word_arrangements(move_blocks(labels, z)[0]), word_arrangements(move_blocks(labels, z)[1]))]
    res = analyse(4, labels, [z], contents); cells = build_cubes(res["words"], 4, blocks)
    out["benchmark_source_4"] = {"words": res["n"], "swap_classes": len(res["swap"]), "rewrite_classes": len(res["rewrite"]), "cells": {str(d): len(c) for d, c in cells.items()}, "cubical_betti": list(betti(cells))}
    # join example: {2,8,63} <-> {5,9,35} at m = 280: two swap classes on each side, complete bipartite rewrite relation
    labels = (2, 5, 8, 9, 35, 63); z = (-1, 1, -1, 1, 1, -1)
    assert multiplier(labels, [max(-x, 0) for x in z]) == multiplier(labels, [max(x, 0) for x in z])
    contents = [(1, 0, 1, 0, 0, 1), (0, 1, 0, 1, 1, 0)]
    blocks = [(word_arrangements(move_blocks(labels, z)[0]), word_arrangements(move_blocks(labels, z)[1]))]
    ex = {}
    for m in (280, 840):
        res = analyse(m, labels, [z], contents); cells = build_cubes(res["words"], m, blocks)
        ex[str(m)] = {"words": res["n"], "swap_classes": len(res["swap"]), "rewrite_classes": len(res["rewrite"]), "cells": {str(d): len(c) for d, c in cells.items()}, "cubical_betti": list(betti(cells))}
    out["join_example_2_8_63__5_9_35"] = ex
    dump("EXTENDED_TOPOLOGY.json", out); return out


def occurrence():
    out = {"D_B1": {"A": summary(4, (1,) * 7), "B": summary(4, (2, 2, 3, 3, 3, 3))}, "cube_family": {}}
    A, B = (1,) * 7, (2, 2, 3, 3, 3, 3)
    for r in range(1, 6):
        pairs = []; diff = []
        for ch in itertools.product((0, 1), repeat=r):
            w = ()
            for c in ch: w += B if c else A
            s = summary(4, w); pairs.append((s["births"], s["losses"])); diff.append(s["births"] - s["losses"])
        out["cube_family"][str(r)] = {"histories": 2 ** r, "distinct_birth_loss_pairs": len(set(pairs)), "births_minus_losses_values": sorted(set(diff))}
    ps, V = matrix((1, 2, 3, 8)); ker = kernel_of_alphabet((1, 2, 3, 8))
    out["information"] = {"alphabet": [1, 2, 3, 8], "labels": 4, "rank_V": 4 - len(ker), "lost_kernel_rank": len(ker)}
    dump("OCCURRENCE_EVENTS.json", out); return out


if __name__ == "__main__":
    t = time.time(); os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    for f in (merger_kernel, rewrite_thresholds, cubes, saturation_and_dichotomy, generators, extended_topology, occurrence, completeness_123):
        f(); print(f.__name__, "%.0fs" % (time.time() - t), flush=True)

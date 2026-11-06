"""E9 -- exact 3-face grammar of P_6 and exact threshold tables; verification of T16 (block factorization), T17 (face thresholds),
Lemma F (feasible-family law) against direct simulation.  Everything exact integer/Fraction arithmetic."""
import time
import random
from collections import Counter
from itertools import combinations
import _path  # noqa: F401
import history_complex as hc
import threshold_closure as tc
import block_factor as bf
import face_threshold as ft


def run(quick=False, seed=9):
    t0 = time.time()
    out = {"experiment": "E9"}
    # ---- grammar of P_k 3-faces
    gram = {}
    for k in (4, 5, 6, 7):
        g = ft.grammar(k, 3)
        gram[k] = {"x".join(map(str, t)): {"name": ft.TYPE_NAME.get(t), "count": d["count"], "vertices": sorted(d["vertices"]),
                                          "facets": sorted(d["facets"])} for t, d in sorted(g.items())}
    out["grammar_3faces"] = gram
    c6 = {v["name"]: v["count"] for v in gram[6].values()}
    out["P6_3face_total"] = sum(c6.values())
    out["P6_3face_expected"] = {"cube": 90, "hexagonal prism": 360, "truncated octahedron": 90}
    out["P6_3face_reproduced"] = c6 == out["P6_3face_expected"] and sum(c6.values()) == 540
    # ---- threshold tables for the two anchors and for the identity content
    tables = {}
    for name, C in (("anchor_A", (2, 3, 4, 5, 8, 9)), ("anchor_B", (2, 3, 6, 7, 8, 9)), ("identity_1_6", (1, 2, 3, 4, 5, 6))):
        T = ft.threshold_table(C, 3)
        by = {}
        for f, t, K in T:
            by.setdefault(ft.TYPE_NAME[t], Counter())[K] += 1
        tables[name] = {"content": C, "faces": len(T),
                        "threshold_histogram_by_type": {tn: {str(K): n for K, n in sorted(c.items())} for tn, c in by.items()},
                        "thresholds_by_face": [[list(map(list, f)), ft.TYPE_NAME[t], K] for f, t, K in T]}
    out["threshold_tables"] = tables
    # ---- verification: T17 closed form == lcm of vertex thresholds (direct vertex admissibility), all faces, all contents
    rng = random.Random(seed)
    L = 12 if quick else 14
    conts = list(combinations(range(1, L + 1), 6))
    if quick:
        conts = rng.sample(conts, 40)
    else:
        conts = rng.sample(conts, 300)
    conts += [(2, 3, 4, 5, 8, 9), (2, 3, 6, 7, 8, 9), (1, 2, 3, 4, 5, 6)]
    t17 = {"contents": 0, "faces_checked": 0, "violations": 0}
    lemF = {"contents": 0, "violations": 0}
    t16 = {"face_source_pairs": 0, "violations": 0}
    faces6 = ft.faces(6)
    for C in conts:
        K = tc.threshold_values(C)
        D = bf.denominators(C)
        t17["contents"] += 1
        for f, d, _ in faces6:
            if ft.threshold_by_vertices(C, f, K) != ft.threshold_closed_form(C, f, D):
                t17["violations"] += 1
            t17["faces_checked"] += 1
        # Lemma F: K(w)=lcm D(prefix sets) for every arrangement
        P = hc.perms(6)
        lemF["contents"] += 1
        for i, p in enumerate(P):
            if bf.threshold_via_D(C, p, D) != K[i]:
                lemF["violations"] += 1
        # T16: for random sources (divisors of lcm K) and all faces of dim<=3
        Lc = 1
        for x in K:
            Lc = Lc * x // __import__("math").gcd(Lc, x)
        divs = [d for d in range(1, 400) if Lc % d == 0] or [1]
        for m in rng.sample(divs, min(4, len(divs))) + [Lc]:
            mask = tc.source_mask(C, m)
            if mask != bf.admissible_mask_via_chains(C, m):
                lemF["violations"] += 1
            for f, d, _ in faces6:
                if d > 3:
                    continue
                t16["face_source_pairs"] += 1
                if bf.predicted_vertices(C, m, f) != bf.actual_vertices(mask, f, 6):
                    t16["violations"] += 1
    out["T17_closed_form_vs_vertex_lcm"] = t17
    out["LemmaF_feasible_family"] = lemF
    out["T16_block_factorization"] = t16
    out["seconds"] = round(time.time() - t0, 1)
    return out


if __name__ == "__main__":
    import json
    r = run(quick=True)
    r.pop("threshold_tables")
    print(json.dumps(r, indent=1)[:3000])

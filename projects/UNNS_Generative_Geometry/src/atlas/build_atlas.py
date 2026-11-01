#!/usr/bin/env python3
"""GEO-HD-1 / HD-0 / E1 — exact generative atlas builder (standard library only).

Builds results/E1/E1_ATLAS.json for the preregistered benchmark states
SEL_6, SEL_72 and the SELECT-II v002b confluence example t=784.

The atlas keeps the following objects *separate* (never collapsed into each other):
    value           an integer state / numerical output t
    occurrence      (N, M, x) with x = M (N+1)^2 / N         [A0]
    edge            m --N--> T_N(m)                           [A2]
    incoming label  N of the edge entering a value            [A2]
    history         source-rooted labelled path to t          [A2, Vol. I Def. 6.1]
    fibre coord.    exponent vector of d = N + 1 over the active primes  [A0/GEO-I]

Everything is exact integer arithmetic. No file outside --out is written.
Usage:  python build_atlas.py [--out PATH]
"""
import argparse
import hashlib
import json
import sys
from itertools import product

SPEC = "GEO_HD_1_SPEC_v003"
GEO_I_COMMIT = "343f9aef2b6697466058165c5fc2ddf0f00e882b"
FOUNDATIONS_COMMIT = "bb8b12d753c600c597feb00df17fe139c7cc65fa"


# ----------------------------------------------------------------- arithmetic
def factor(n):
    f, p = {}, 2
    while p * p <= n:
        while n % p == 0:
            f[p] = f.get(p, 0) + 1
            n //= p
        p += 1 if p == 2 else 2
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def divisors(n):
    ds = [1]
    for p, e in factor(n).items():
        ds = [d * p ** k for d in ds for k in range(e + 1)]
    return sorted(ds)


def v(n, p):
    c = 0
    while n % p == 0:
        n //= p
        c += 1
    return c


def sqrt_part(m):
    r = 1
    for p, e in factor(m).items():
        r *= p ** (e // 2)
    return r


def T(m, N):
    assert N >= 1 and m % N == 0
    return (m // N) * (N + 1) ** 2


def D(m):
    """index set D(m) = {d >= 2 : d^2 | m}  (b = 1)."""
    return [d for d in divisors(sqrt_part(m)) if d >= 2]


def occurrences(t):
    """all (N, M, t) with t = M (N+1)^2 / N, via the index bijection d = N+1."""
    out = []
    for d in D(t):
        N = d - 1
        assert (t * N) % (d * d) == 0
        out.append((N, t * N // (d * d)))
    return sorted(out)


def preds(t):
    """P(t): predecessor states, with the label of the entering edge."""
    return sorted((M, N) for N, M in occurrences(t))


def is_source(t):
    return not D(t)           # squarefree <=> no predecessor (Vol. I Thm 5.3)


def valuation(m):
    return {str(p): e for p, e in sorted(factor(m).items())}


def vec(m, primes):
    return [v(m, p) for p in primes]


# ------------------------------------------------------------------ histories
_H = {}


def histories(t):
    """complete histories of t: all source-rooted paths, as tuples of states."""
    if t in _H:
        return _H[t]
    hs = []
    if is_source(t):
        hs.append((t,))
    for M, N in preds(t):
        for h in histories(M):
            hs.append(h + (t,))
    hs = sorted(set(hs))
    _H[t] = hs
    return hs


def labels_of(path):
    out = []
    for a, b in zip(path, path[1:]):
        Ns = [N for N in divisors(a) if T(a, N) == b]
        assert len(Ns) == 1
        out.append(Ns[0])
    return out


# ---------------------------------------------------------------- fibre geometry
def rank(rows):
    rows = [list(r) for r in rows]
    r = 0
    ncol = len(rows[0]) if rows else 0
    from fractions import Fraction
    rows = [[Fraction(x) for x in row] for row in rows]
    for c in range(ncol):
        piv = next((i for i in range(r, len(rows)) if rows[i][c] != 0), None)
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i][c] != 0:
                f = rows[i][c] / rows[r][c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        r += 1
    return r


def fibre_geometry(t):
    """exponent-coordinate fibre of the integer t (b = 1) and its coordinate-cell
    complex K_axis: unit faces of the box [0,q] whose corners are all nonzero."""
    f = factor(t)
    primes = [p for p in sorted(f) if f[p] // 2 >= 1]
    q = [f[p] // 2 for p in primes]
    k = len(primes)
    verts = sorted(tuple(a) for a in product(*[range(x + 1) for x in q]) if any(a))
    # index d <-> vertex
    index = {}
    for a in verts:
        d = 1
        for p, e in zip(primes, a):
            d *= p ** e
        index[a] = d
    assert sorted(index.values()) == D(t), "fibre bijection failed"
    counts = {}
    for S in product((0, 1), repeat=k):
        free = [i for i in range(k) if S[i]]
        ranges = [range(q[i] if S[i] else q[i] + 1) if True else None for i in range(k)]
        # i free: base c_i in [0, q_i - 1]; i fixed: c_i in [0, q_i]
        ranges = [range(q[i]) if S[i] else range(q[i] + 1) for i in range(k)]
        for c in product(*ranges):
            corners_ok = True
            for bits in product((0, 1), repeat=len(free)):
                corner = list(c)
                for i, b_ in zip(free, bits):
                    corner[i] += b_
                if not any(corner):
                    corners_ok = False
                    break
            if corners_ok:
                counts[len(free)] = counts.get(len(free), 0) + 1
    dcell = max(counts) if counts else -1
    chi = sum((-1) ** d * c for d, c in counts.items())
    daff = rank([[x - y for x, y in zip(a, verts[0])] for a in verts[1:]]) if len(verts) > 1 else (0 if verts else -1)
    return {
        "primes": primes, "q": q, "lattice": "Z^k (b=1, Graver basis +-e_i)", "k": k,
        "vertices": [list(a) for a in verts],
        "vertex_index_d": {",".join(map(str, a)): index[a] for a in verts},
        "R": len(verts), "d_amb": k, "d_aff": daff, "d_cell": dcell,
        "cells_by_dim": {str(d): counts[d] for d in sorted(counts)},
        "euler_characteristic": chi if counts else None,
        "cell_model": "K_axis: unit coordinate faces avoiding the origin (GEO-I v002 Prop. 1-2; Graver cells for b=1)",
    }


# --------------------------------------------------------------------- atlas
def state_record(m):
    f = factor(m)
    return {
        "value": m, "valuation": valuation(m),
        "is_source": is_source(m), "squarefree": all(e == 1 for e in f.values()),
        "sqrt_part_s": sqrt_part(m), "index_set_D": D(m), "R": len(D(m)),
        "out_degree": len(divisors(m)), "H": len(histories(m)),
    }


def occ_record(N, M, x):
    d = N + 1
    primes = [p for p in sorted(factor(x)) if factor(x)[p] // 2 >= 1]
    return {
        "id": f"O({N},{M},{x})", "N": N, "M": M, "x": x, "d": d,
        "predecessor": M, "incoming_label": N, "edge_id": f"E({M},{N},{x})",
        "fibre_coordinate": {"primes": primes, "alpha": [v(d, p) for p in primes]},
    }


def edge_record(m, N):
    t = T(m, N)
    primes = sorted(set(factor(m)) | set(factor(t)) | set(factor(N)) | set(factor(N + 1)))
    dv = [2 * v(N + 1, p) - v(N, p) for p in primes]
    assert [v(t, p) - v(m, p) for p in primes] == dv
    return {"id": f"E({m},{N},{t})", "source": m, "label": N, "target": t,
            "valuation_displacement": {"primes": primes, "delta": dv}}


def minimal_common_successors(a, b, bound):
    def reach(s):
        seen, stack = {s}, [s]
        while stack:
            u = stack.pop()
            for N in divisors(u):
                w = T(u, N)
                if w <= bound and w not in seen:
                    seen.add(w)
                    stack.append(w)
        return seen
    common = reach(a) & reach(b)
    # a common successor c is minimal iff no other common successor reaches c
    # (edges strictly increase, so everything reaching c is < c <= bound)
    minimal = []
    for c in sorted(common):
        below = False
        for u in sorted(common):
            if u >= c:
                break
            if c in reach(u):
                below = True
                break
        if not below:
            minimal.append(c)
    return minimal


def build():
    benchmarks = {"SEL_6": 6, "SEL_72": 72, "CONFLUENCE_784": 784}
    values = set()
    # SEL_6: the state and its four SELECT-II targets
    values.add(6)
    values |= {T(6, N) for N in divisors(6)}
    # SEL_72: the state, its occurrences' predecessors, every state on a complete history, all outgoing targets
    values.add(72)
    for h in histories(72):
        values |= set(h)
    values |= {T(72, N) for N in divisors(72)}
    # confluence example
    values |= {784, 96, 27, 432}
    values.add(16)                                  # SELECT-II v002b B5 (histories of different lengths)
    values |= {108}                                 # FIELD-I step C(72)
    values = sorted(values)

    states = {str(m): state_record(m) for m in values}

    edges = {}
    occ = {}
    for m in values:
        for N in divisors(m):
            if T(m, N) in values:
                e = edge_record(m, N)
                edges[e["id"]] = e
        for N, M in occurrences(m):
            o = occ_record(N, M, m)
            occ[o["id"]] = o
    # every occurrence <-> exactly one edge (SELECT-II v002a, S2.5); the predecessor may lie outside the value list
    for o in occ.values():
        if o["edge_id"] not in edges:
            e = edge_record(o["M"], o["N"])
            assert e["id"] == o["edge_id"]
            edges[e["id"]] = e

    hist = {}
    for t in (6, 72, 784, 16):
        rows = []
        for h in histories(t):
            lab = labels_of(h)
            last = None
            if len(h) > 1:
                last = f"O({lab[-1]},{h[-2]},{t})"
            rows.append({"id": "H(" + "-".join(map(str, h)) + ")", "states": list(h), "labels": lab,
                         "length": len(h) - 1, "source": h[0], "endpoint": t,
                         "last_edge_occurrence": last})
        hist[str(t)] = rows

    fib = {str(m): fibre_geometry(m) for m in values}

    # ---------------------------------------------------------------- projections
    proj = {}
    # (a) value-level projections of the targets of 6 onto prime coordinates
    def pv(m, ps):
        return [v(m, p) for p in ps]
    proj["sel6_targets_P(2,3,7)"] = {str(m): pv(m, [2, 3, 7]) for m in [6] + [T(6, N) for N in divisors(6)]}
    proj["sel6_collision_example_P(2,3,5)"] = {
        "projection_primes": [2, 3, 5], "colliding_values": [1, 49],
        "images": {"1": pv(1, [2, 3, 5]), "49": pv(49, [2, 3, 5])},
        "note": "49 = T_6(6) is an out-neighbour of 6 whose image under this projection equals that of the source value 1"}
    # (b) history-level projections of the 4 complete histories of 72
    h72 = hist["72"]
    def classes(key):
        d = {}
        for r in h72:
            d.setdefault(json.dumps(key(r)), []).append(r["id"])
        return sorted(sorted(c) for c in d.values())
    proj["histories_72"] = {
        "endpoint": classes(lambda r: r["endpoint"]),
        "endpoint_and_length": classes(lambda r: [r["endpoint"], r["length"]]),
        "source_endpoint_length": classes(lambda r: [r["source"], r["endpoint"], r["length"]]),
        "last_edge_occurrence": classes(lambda r: r["last_edge_occurrence"]),
        "label_sequence": classes(lambda r: r["labels"]),
        "source_and_label_sequence": classes(lambda r: [r["source"], r["labels"]]),
        "full_state_sequence": classes(lambda r: r["states"]),
    }

    # ----------------------------------------------------------- confluence record
    p1, p2 = 96, 27      # predecessors of 784 along routes (k,d) = (16,7) and (1,28)
    mcs5000 = minimal_common_successors(p1, p2, 5000)
    conf = {
        "target": 784,
        "routes": [{"route_k_d": [16, 7], "predecessor": 96, "label": 6},
                   {"route_k_d": [1, 28], "predecessor": 27, "label": 27}],
        "minimal_common_successors_le_784": [c for c in mcs5000 if c <= 784],
        "minimal_common_successors_in_bound_5000": mcs5000,
        "scope_note": ("Frozen v002b C7 lists the minimal merges at or below t=784, i.e. {432,784}. The search to 5000 "
                       "additionally finds minimal common successors above 784 (listed); the set of common successors is "
                       "infinite, so only the bounded statements are exact."),
        "source": "SELECT-II v002b, C7 (data): second incomparable minimal merge for 9/1277 pairs t<=3000",
    }

    # ------------------------------------------------------------- field-I step
    S72 = D(72)
    L = 1
    from math import gcd
    for d in S72:
        L = L * d // gcd(L, d)
    G = 0
    for d in S72:
        G = gcd(G, d - 1)
    field_step = {"scope": "C (FIELD-I collective map), NOT a SELECT-II edge", "x": 72, "L": L, "G": G,
                  "C_x": 72 + L * L // G, "D_x": S72, "D_C_x": D(72 + L * L // G),
                  "is_select_ii_out_neighbour_of_72": (72 + L * L // G) in [T(72, N) for N in divisors(72)]}

    # ---------------------------------------------- regression fibres (GEO-I v002 table)
    regression = {}
    for x in (72, 144, 3600, 44100):
        g = fibre_geometry(x)
        regression[str(x)] = {k: g[k] for k in ("R", "d_amb", "d_aff", "d_cell", "cells_by_dim", "euler_characteristic")}

    # --------------------------------------------- non-identification certificates
    h72 = hist["72"]
    sources_with_label_1 = [s for s in range(1, 12) if is_source(s)]
    cert = [
        {"id": "NI-1", "claim": "a value is not an occurrence",
         "witness": {"value": 72, "occurrences": [o for o in sorted(occ) if occ[o]["x"] == 72]}},
        {"id": "NI-2", "claim": "an occurrence is not a history (last-edge map is not injective)",
         "witness": {"occurrence": "O(2,16,72)", "histories": ["H(1-4-16-72)", "H(3-16-72)"]}},
        {"id": "NI-3", "claim": "a history is not determined by (source, endpoint, length)",
         "witness": {"histories": ["H(1-4-16-72)", "H(1-4-18-72)"], "common": {"source": 1, "endpoint": 72, "length": 3},
                     "distinguished_by": "label sequences (1,1,2) vs (1,2,1) and middle state 16 vs 18"}},
        {"id": "NI-4", "claim": "a history is not determined by its label sequence alone",
         "witness": {"label_sequence": [1], "histories": [f"H({s}-{T(s, 1)})" for s in sources_with_label_1[:4]]}},
        {"id": "NI-5", "claim": "equal fibres do not mean equal values or equal occurrence sets",
         "witness": {"values": [72, 108], "index_sets": [D(72), D(108)],
                     "occurrences_72": occurrences(72), "occurrences_108": occurrences(108)}},
        {"id": "NI-6", "claim": "a FIELD-I collective step is not a SELECT-II edge",
         "witness": {"C(72)": 108, "SELECT_II_out_neighbours_of_72": [T(72, N) for N in divisors(72)]}},
        {"id": "NI-7", "claim": "a finite-prime projection need not be injective on states",
         "witness": {"projection_primes": [2, 3, 5], "values": [1, 49]}},
        {"id": "NI-8", "claim": "SELECT-II edges (between states) and Graver moves (between index vectors inside one fibre) have different vertex types",
         "witness": {"select_ii_vertices_for_72": "integers in V", "graver_vertices_for_72": fibre_geometry(72)["vertices"],
                     "note": "no map between the two edge sets is declared; none may be assumed"}},
    ]

    # --------------------------------------------------------- frozen reproduction
    nonsrc = [t for t in range(2, 200) if not is_source(t)]
    first_H_gt_R = next(t for t in nonsrc if len(histories(t)) > len(D(t)))
    frozen = [
        {"id": "FR-1", "source": "Vol. I Def. 5.1 / S2.1", "claim": "out-neighbours of 6",
         "expected": [24, 27, 32, 49], "computed": sorted(T(6, N) for N in divisors(6))},
        {"id": "FR-2", "source": "Vol. I Thm 1.2 / S2.2 / CTX 3.1", "claim": "occurrences of 72 (N,M)",
         "expected": [[1, 18], [2, 16], [5, 10]], "computed": [list(x) for x in occurrences(72)]},
        {"id": "FR-3", "source": "SELECT-II v002b B2 (S2.12)", "claim": "complete histories of 72",
         "expected": [[1, 4, 16, 72], [1, 4, 18, 72], [3, 16, 72], [10, 72]], "computed": [list(h) for h in histories(72)]},
        {"id": "FR-4", "source": "SELECT-II v002b B5", "claim": "complete histories of 16 (different lengths)",
         "expected": [[1, 4, 16], [3, 16]], "computed": [list(h) for h in histories(16)]},
        {"id": "FR-5", "source": "SELECT-II v002b C4", "claim": "route (k,d)=(8,3) of 72 comes from predecessor 16, which has 2 histories",
         "expected": {"predecessor": 16, "histories": 2}, "computed": {"predecessor": 8 * (3 - 1), "histories": len(histories(16))}},
        {"id": "FR-6", "source": "SELECT-II v002b C7", "claim": "minimal merges <= 784 of preds (96, 27) of routes (16,7),(1,28)",
         "expected": [432, 784], "computed": conf["minimal_common_successors_le_784"]},
        {"id": "FR-7", "source": "SELECT-II v002b C6 (S2.15)", "claim": "72 is a minimal common successor of each pair of predecessors of 72",
         "expected": True, "computed": all(72 in minimal_common_successors(a, b, 72)
                                           for a, b in [(18, 16), (18, 10), (16, 10)])},
        {"id": "FR-8", "source": "SELECT-II v002b B4", "claim": "smallest non-source t with H(t)>R(t) (t<200)",
         "expected": 64, "computed": first_H_gt_R},
        {"id": "FR-9", "source": "GEO-I v002 spec table", "claim": "(R,d_amb,d_aff,d_cell) of 72,144,3600,44100",
         "expected": {"72": [3, 2, 2, 1], "144": [5, 2, 2, 2], "3600": [11, 3, 3, 3], "44100": [15, 4, 4, 3]},
         "computed": {k: [r["R"], r["d_amb"], r["d_aff"], r["d_cell"]] for k, r in regression.items()}},
        {"id": "FR-10", "source": "Vol. I Thm 5.5 / S2.3", "claim": "N = m/gcd(m,t) on every recorded edge",
         "expected": True, "computed": all(e["label"] == e["source"] // __import__("math").gcd(e["source"], e["target"])
                                           for e in edges.values())},
        {"id": "FR-11", "source": "v001 Thm 2.1 (displacement)", "claim": "v(T_N(m)) - v(m) = 2v(N+1) - v(N) on every recorded edge",
         "expected": True, "computed": True},
    ]
    for r in frozen:
        r["pass"] = (r["expected"] == r["computed"])

    atlas = {
        "atlas": "GEO-HD-1 / HD-0 / E1 exact generative atlas",
        "spec": SPEC,
        "sources": {"geo_i_commit": GEO_I_COMMIT, "foundations_commit": FOUNDATIONS_COMMIT,
                    "select_ii_v002b": "projects/UNNS_MATH_FOUNDATIONS/sources/SELECT-II/v002b/ @ " + FOUNDATIONS_COMMIT},
        "benchmark_ids": benchmarks,
        "typed_maps": TYPED_MAPS,
        "states": states, "occurrences": occ, "edges": edges,
        "complete_histories": hist,
        "fibre_geometry": fib,
        "projections": proj,
        "confluence_example": conf,
        "field_I_step_from_72": field_step,
        "regression_fibres_geo_i_v002": regression,
        "non_identification_certificates": cert,
        "frozen_reproduction": frozen,
    }
    return atlas


TYPED_MAPS = [
    {"id": "pi",      "name": "numerical projection", "domain": "O (occurrences)", "codomain": "V (values)",
     "definition": "(N,M,x) -> x", "kind": "inherited A0"},
    {"id": "idx",     "name": "occurrence index", "domain": "O_x", "codomain": "D(x)", "definition": "(N,M,x) -> d = N+1",
     "kind": "inherited A0 (Vol. I Thm 1.2, F.T1): bijection onto D(x)"},
    {"id": "coord",   "name": "fibre coordinate", "domain": "D(x)", "codomain": "Z^k_{>=0} (k active primes of s(x))",
     "definition": "d -> (v_p(d))_p", "kind": "inherited A0/GEO-I: bijection onto F_x for b=1"},
    {"id": "edge",    "name": "occurrence-edge identification", "domain": "O_t", "codomain": "E_in(t) (incoming SELECT-II edges)",
     "definition": "(N,M,t) -> M --N--> t", "kind": "inherited A2 (S2.5, Vol. I Thm 5.3): bijection"},
    {"id": "lab",     "name": "incoming label", "domain": "E", "codomain": "N_{>0}", "definition": "m --N--> t -> N",
     "kind": "inherited A2 (S2.3: N = m/gcd(m,t))"},
    {"id": "eps",     "name": "endpoint map", "domain": "H(t0) or complete histories", "codomain": "V",
     "definition": "path -> last state", "kind": "inherited A2 (Vol. I Def. 6.1)"},
    {"id": "last",    "name": "last-edge map", "domain": "complete histories of t", "codomain": "O_t (t non-source)",
     "definition": "(m0,...,m_l=t) -> occurrence of the last edge", "kind": "HD-0 definition; surjective, not injective (C4)"},
    {"id": "valexp",  "name": "valuation embedding", "domain": "V", "codomain": "(+)_p Z_{>=0}",
     "definition": "m -> (v_p(m))_p", "kind": "inherited A2 (injective: unique factorisation)"},
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="E1_ATLAS.json")
    a = ap.parse_args()
    atlas = build()
    txt = json.dumps(atlas, indent=1, sort_keys=True, ensure_ascii=False) + "\n"
    with open(a.out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(txt)
    print("wrote", a.out, len(txt), "bytes; sha256", hashlib.sha256(txt.encode()).hexdigest())


if __name__ == "__main__":
    main()

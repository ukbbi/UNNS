"""v002-W  finite-window accounting: infinite-graph exits vs exits inside [1, L]."""
import json, os, random, sys
import numpy as np
from math import isqrt
from scale_lib import factor, merge, neighbours
from boundary_lib import eps_closed
from sieve_lib import total_exits_exact, tau_sieve

random.seed(20261116)
res = {"part": "W", "claims": {}}

def e_count(L):
    return sum(L // (m * m) for m in range(2, isqrt(L) + 1))

def edge_classes(L, B):
    """Exact counts for edges of G[1..L] by how many endpoints lie in B*Z.
    Edge {kN, k s}, s=(N+1)^2:  u=kN in lattice <=> (B/gcd(B,N)) | k ;  v=ks in lattice <=> (B/gcd(B,s)) | k ;  both <=> B | k."""
    N = np.arange(1, isqrt(L), dtype=np.int64)
    N = N[(N + 1) ** 2 <= L]
    s = (N + 1) ** 2
    K = L // s
    n_u = int((K // (B // np.gcd(B, N))).sum())
    n_v = int((K // (B // np.gcd(B, s))).sum())
    n_uv = int((K // B).sum())
    total = int(K.sum())
    return {"both": n_uv, "exactly_one": n_u + n_v - 2 * n_uv, "none": total - (n_u + n_v - n_uv), "total": total}

def brute_classes(L, B):
    both = one = none = 0
    N = 1
    while (N + 1) ** 2 <= L:
        s = (N + 1) ** 2
        k = np.arange(1, L // s + 1, dtype=np.int64)
        iu = (k * N) % B == 0; iv = (k * s) % B == 0
        both += int((iu & iv).sum()); one += int((iu ^ iv).sum()); none += int((~iu & ~iv).sum())
        N += 1
    return {"both": both, "exactly_one": one, "none": none, "total": both + one + none}

# W1: the single vertex 10^6 and the top vertex 10^12 in the window [1, 10^12]
L = 10**12
def classify(u, B, L):
    nb = neighbours(factor(u))
    return {"deg_infinite": len(nb),
            "in_lattice": sum(v % B == 0 for (_, _, v) in nb),
            "exits_infinite": sum(v % B != 0 for (_, _, v) in nb),
            "exits_in_window": sum(v % B != 0 and v <= L for (_, _, v) in nb),
            "lost_beyond_window": [list(t) for t in sorted(nb) if t[2] > L]}
res["claims"]["W1_vertex_10^6"] = classify(10**6, 10**6, L)
res["claims"]["W1_vertex_10^12"] = classify(10**12, 10**6, L)
res["claims"]["W1_vertex_10^6"]["N=10^6 forward neighbour"] = (10**6 + 1) ** 2

# W2: closed-form edge classes vs brute force
brute_ok = {}
for (Lb, B) in [(10**6, 10), (10**6, 100), (3 * 10**7, 10), (3 * 10**7, 1000), (10**7, 360), (2 * 10**6, 7), (10**6, 1), (10**6, 10**6)]:
    a, b = edge_classes(Lb, B), brute_classes(Lb, B)
    brute_ok[f"L={Lb},B={B}"] = {"closed": a, "brute": b, "equal": a == b, "total=e(L)": a["total"] == e_count(Lb)}
res["claims"]["W2_edge_classes_vs_brute"] = brute_ok

# W3: bookkeeping  (infinite exits over lattice) = (window exits) + (lost exits)  at small scale
book = {}
for (Lb, B) in [(10**6, 10), (10**6, 100), (2 * 10**6, 1000)]:
    fB = factor(B); inf_tot = win_tot = lost_tot = 0
    for x in range(1, Lb // B + 1):
        fx = factor(x); nb = neighbours(merge(fB, fx))
        inf_tot += sum(v % B != 0 for (_, _, v) in nb)
        win_tot += sum(v % B != 0 and v <= Lb for (_, _, v) in nb)
        lost_tot += sum(v % B != 0 and v > Lb for (_, _, v) in nb)
    cl = edge_classes(Lb, B)
    book[f"L={Lb},B={B}"] = {"infinite_exits": inf_tot, "window_exits": win_tot, "lost_exits": lost_tot,
                             "closed_form_exactly_one": cl["exactly_one"],
                             "infinite_exits_via_eps_sum": total_exits_exact(Lb // B, fB, B),
                             "consistent": inf_tot == win_tot + lost_tot == cl["exactly_one"] + lost_tot and win_tot == cl["exactly_one"]
                                            and inf_tot == total_exits_exact(Lb // B, fB, B)}
res["claims"]["W3_bookkeeping_small"] = book

# W4: the trillion window
tril = {}
for B in (10**3, 10**4, 10**6):
    c = edge_classes(10**12, B)
    tril[str(B)] = {**c, "lattice_vertices": 10**12 // B, "mean_window_exits_per_lattice_vertex": c["exactly_one"] / (10**12 // B),
                    "fraction_of_edges_inside_copy": c["both"] / c["total"], "fraction_with_exactly_one_lattice_endpoint": c["exactly_one"] / c["total"]}
fB6 = factor(10**6)
inf6 = total_exits_exact(10**6, fB6, 10**6)
tril["10^6_infinite_exit_total"] = inf6
tril["10^6_lost_exits_beyond_window"] = inf6 - tril["1000000"]["exactly_one"]
res["claims"]["W4_trillion_window"] = tril
print(json.dumps(res["claims"]["W1_vertex_10^6"], indent=1)); print(json.dumps(tril, indent=1))

res["PASS"] = (res["claims"]["W1_vertex_10^6"]["exits_infinite"] == 63 and res["claims"]["W1_vertex_10^6"]["exits_in_window"] == 62
               and all(v["equal"] and v["total=e(L)"] for v in brute_ok.values())
               and all(v["consistent"] for v in book.values())
               and tril["10^6_lost_exits_beyond_window"] >= 1
               and tril["1000000"]["both"] == 643494 and tril["1000000"]["total"] == 644932606630)
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "W_window.json"), "w"), indent=1)
print("PASS", res["PASS"]); sys.exit(0 if res["PASS"] else 1)

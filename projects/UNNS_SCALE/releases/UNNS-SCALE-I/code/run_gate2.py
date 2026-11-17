"""Gate 2 -- scale embedding and boundary crossing.

T2 (scale-copy): {Bu,Bv} in E  <=>  {u,v} in E  (labels preserved).
T3 (boundary law): at u = Bx
     forward label N | Bx   stays in B*Z  <=>  N | x
     backward label N       stays in B*Z  <=>  (N+1)^2 | x
     deg(Bx) = deg(x) + exits.
T4 (no outer quotient): floor(n/B) does not intertwine T_1 (n -> 4n).
"""
import json, os, sys, random
from scale_lib import (factor, merge, neighbours, degree, tau, sq_count,
                       edge_set, build_graph)

random.seed(20261116)
res = {"gate": 2, "claims": {}}

# ---- G2.a  global induced-subgraph isomorphism on a finite window ----------
glob = {}
L = 300000
E_big = edge_set(L)
for B in [2, 3, 4, 6, 10, 12, 30, 100]:
    M = L // B
    E_small = edge_set(M)
    scaled = {(B * u, B * v) for (u, v) in E_small}
    induced = {(u, v) for (u, v) in E_big if u % B == 0 and v % B == 0}
    glob[str(B)] = {"window": L, "edges_in_copy": len(scaled),
                    "edges_in_induced_subgraph": len(induced),
                    "exactly_equal": scaled == induced}
res["claims"]["G2a_global_isomorphism"] = glob

# ---- G2.b  local law at lattice vertices, up to B = 10^6 (u up to 10^12) ----
def local_check(B, xs):
    fB = factor(B)
    mism = labelmism = degmism = 0
    exits_list = []
    for x in xs:
        fx = factor(x)
        fu = merge(fB, fx)
        nb = neighbours(fu)
        nbx = neighbours(fx)
        u = B * x
        inlat, exits = set(), 0
        for (d, N, v) in nb:
            stays = (v % B == 0)
            pred = (x % N == 0) if d == "+" else (x % ((N + 1) ** 2) == 0)
            if stays != pred:
                mism += 1
            if stays:
                inlat.add((d, N, v // B))
            else:
                exits += 1
        if inlat != nbx:                      # same labels, same directions, v/B
            labelmism += 1
        if degree(fu) != len(nb) or degree(fx) != len(nbx):
            degmism += 1
        if len(nb) != degree(fx) + exits:
            degmism += 1
        exits_list.append(exits)
    return {"vertices_checked": len(xs), "stay/leave_prediction_mismatches": mism,
            "inlattice_neighbourhood_mismatches": labelmism, "degree_mismatches": degmism,
            "min_exits": min(exits_list), "max_exits": max(exits_list),
            "mean_exits": sum(exits_list) / len(exits_list)}

loc = {}
for B in [10, 100, 1000, 10**6]:
    xs = list(range(1, 3001)) + [random.randrange(3001, 10**6) for _ in range(1500)]
    loc[str(B)] = local_check(B, xs)
res["claims"]["G2b_local_boundary_law"] = loc

# ---- G2.c  worked example (x = 1, B = 10^6) and the 4.5M transition --------
f = factor(10**6)
nb = sorted(neighbours(f))
res["claims"]["G2c_worked_example_1e6"] = {
    "tau(1e6)": tau(f), "s(1e6)": sq_count(f), "deg(1e6)": degree(f),
    "deg(1)": 1, "exits_from_scaled_copy": degree(f) - 1,
    "N=1 -> 4e6": ["+", 1, 4 * 10**6] in [list(t) for t in nb],
    "N=2 -> 4.5e6 = (q,r)=(4,500000)": ["+", 2, 4500000] in [list(t) for t in nb],
    "(q,r) of 4.5e6": list(divmod(4500000, 10**6)),
    "in_lattice_neighbours": [list(t) for t in nb if t[2] % 10**6 == 0],
}

# ---- G2.d  obstruction: no outer-coordinate quotient dynamics --------------
obs = {}
ok_all = True
for B in [2, 3, 4, 5, 10, 100, 10**3, 10**6]:
    q = 7
    x, y = B * q, B * q + B - 1                # same block
    T1x, T1y = 4 * x, 4 * y                    # the label-1 move, defined everywhere
    same_block = (x // B == y // B)
    differ = (T1x // B != T1y // B)
    obs[str(B)] = {"x": x, "y": y, "pi(x)=pi(y)": same_block,
                   "pi(T1 x)": T1x // B, "pi(T1 y)": T1y // B, "images_differ": differ}
    ok_all &= same_block and differ
res["claims"]["G2d_no_outer_quotient"] = obs

# ---- G2.e  independent check of the degree formula against the built graph --
adjL = build_graph(L)
deg_bad = [u for u in range(1, 547) if len(adjL[u]) != degree(factor(u))]
res["claims"]["G2e_degree_formula_vs_built_graph"] = {"vertices": "1..546 (all neighbours <= 300000)", "mismatches": len(deg_bad)}

# ---- G2.f  exact edge counts by arithmetic (no enumeration) ------------------
from math import isqrt
def e_count(Lm):
    return sum(Lm // (m * m) for m in range(2, isqrt(Lm) + 1))
chk = {str(Lx): (e_count(Lx) == len(edge_set(Lx))) for Lx in (10, 100, 1000, 12345, 300000)}
res["claims"]["G2f_edge_count_formula"] = {
    "formula": "e(L) = sum_{m=2}^{floor(sqrt L)} floor(L/m^2)", "verified_vs_enumeration": chk,
    "e(10^6)": e_count(10**6), "e(10^12)": e_count(10**12),
    "lattice_copy_edges_in_[1,10^12]_for_B=10^6": e_count(10**6),
    "fraction_of_trillion_window_edges_inside_copy": e_count(10**6) / e_count(10**12),
}
chk_ok = all(chk.values())

# ---- verdict ----------------------------------------------------------------
res["PASS"] = (
    all(v["exactly_equal"] for v in glob.values())
    and all(v["stay/leave_prediction_mismatches"] == 0 and v["inlattice_neighbourhood_mismatches"] == 0
            and v["degree_mismatches"] == 0 for v in loc.values())
    and ok_all and not deg_bad and chk_ok
    and res["claims"]["G2c_worked_example_1e6"]["N=2 -> 4.5e6 = (q,r)=(4,500000)"]
)
out = os.path.join(os.path.dirname(__file__), "..", "results", "gate2.json")
json.dump(res, open(out, "w"), indent=2)
print(json.dumps(res["claims"]["G2a_global_isomorphism"], indent=1))
print(json.dumps(res["claims"]["G2b_local_boundary_law"], indent=1))
print(json.dumps(res["claims"]["G2c_worked_example_1e6"], indent=1))
print("PASS", res["PASS"]); sys.exit(0 if res["PASS"] else 1)

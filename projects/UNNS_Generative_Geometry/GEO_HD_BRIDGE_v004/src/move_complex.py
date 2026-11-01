"""K_move(y), K_axis(y) and K_real for the activation family, exact (GF(2), GF(3), Q ranks)."""
import _paths, itertools
from fractions import Fraction as Fr
from rational_geometry import record, hull_points

def edges_from_F(F, k):
    """hull-rule edges between vertices of F u {0}-excluded: u,v in F with hull box containing no other point of F u {0}.  Vertices = F."""
    F0 = list(F) + [tuple([0] * k)]
    E = set()
    for u, v in itertools.combinations(sorted(F), 2):
        if len(hull_points(u, v, F0)) == 2: E.add((u, v))
    return E

def cells_from_F(F, k, maxdim=3):
    """cubical cells: parallelotope P(u;g1..gj), all 2^j vertices in F, generators from realized edge vectors, j>=2 (cells of dim<=maxdim)."""
    Fs = set(F); out = {1: set(), 2: set(), 3: set()}
    vec_edges = set()
    for u, v in itertools.permutations(sorted(F), 2):
        if len(hull_points(u, v, list(F) + [tuple([0] * k)])) == 2:
            vec_edges.add((u, tuple(a - b for a, b in zip(v, u))))
    gens = {}
    for u, g in vec_edges: gens.setdefault(u, set()).add(g)
    for j in (2, 3):
        if j > maxdim: break
        for u, gs in gens.items():
            for combo in itertools.combinations(sorted(gs), j):
                # independent generators with all 2^j vertices present
                pts = []
                for bits in itertools.product((0, 1), repeat=j):
                    p = tuple(u[i] + sum(b * g[i] for b, g in zip(bits, combo)) for i in range(k)); pts.append(p)
                if all(p in Fs for p in pts) and len(set(pts)) == 2 ** j:
                    out[j].add((u, frozenset(combo)))
    return out

def rank_mod(M, p):
    M = [r[:] for r in M]; rk = 0; rows = len(M); cols = len(M[0]) if M else 0
    for c in range(cols):
        piv = next((i for i in range(rk, rows) if M[i][c] % p), None)
        if piv is None: continue
        M[rk], M[piv] = M[piv], M[rk]; inv = pow(M[rk][c], -1, p)
        M[rk] = [(a * inv) % p for a in M[rk]]
        for i in range(rows):
            if i != rk and M[i][c] % p:
                f = M[i][c]; M[i] = [(a - f * b) % p for a, b in zip(M[i], M[rk])]
        rk += 1
    return rk

def betti_1skeleton(nv, edges, p=2):
    """betti_0, betti_1 of a graph (no 2-cells)."""
    idx = {v: i for i, v in enumerate(sorted(nv))}; ed = sorted(edges)
    if not ed: return [len(nv), 0]
    M = [[0] * len(ed) for _ in nv]
    for j, (u, v) in enumerate(ed): M[idx[u]][j] = -1 % p; M[idx[v]][j] = 1
    r1 = rank_mod(M, p)
    return [len(nv) - r1, len(ed) - r1]

def move_complex(x):
    rec = record(x); k = len(rec['ps']); F = rec['F']
    E = edges_from_F(F, k); C = cells_from_F(F, k)
    return {'vertices': len(F), 'edges': len(E), 'cells2': len(C[2]), 'cells3': len(C[3]), 'F': sorted(F), 'E': sorted(E),
            'betti_gf2': betti_1skeleton(F, E, 2) if not C[2] else None, 'betti_gf3': betti_1skeleton(F, E, 3) if not C[2] else None,
            'axis_edges': sum(1 for u, v in itertools.combinations(sorted(F), 2) if sum(a != b for a, b in zip(u, v)) == 1)}

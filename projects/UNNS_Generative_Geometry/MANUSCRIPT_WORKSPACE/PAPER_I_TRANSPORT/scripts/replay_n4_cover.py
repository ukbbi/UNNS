#!/usr/bin/env python3
"""Independent exact check of the corner-lemma step of the hull theorem for E_3 (n = 4):
      P := [0,2]^3 ∩ {x1+x2+x3 >= 2}  is contained in  U(E_3, [0,4]^3).
Method (all arithmetic in Fraction): subtract the 3-cells of K_abs(E_3,[0,4]^3) one by one from P as convex
H-polytopes (closure convention: Q \\ C is covered by the pieces Q ∩ {a_i x >= b_i} ∩ {a_j x <= b_j, j<i}); pieces with
empty interior are discarded.  If nothing of non-empty interior is left, every point of int P lies in the closed set
∪(3-cells), hence P ⊆ U(E_3,[0,4]^3) because P = cl(int P).  Shares no code with the frozen engines."""
import sys, os, json, time
from fractions import Fraction as Fr
from itertools import combinations, product
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lattice_cells import cells, vertices

def det3(a, b, c):
    return (a[0]*(b[1]*c[2]-b[2]*c[1]) - a[1]*(b[0]*c[2]-b[2]*c[0]) + a[2]*(b[0]*c[1]-b[1]*c[0]))
def cross(a, b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def dot(a, b): return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]

def cell_halfspaces(cell):
    u, gens = cell
    hs = []
    for i in range(3):
        j, k = [x for x in range(3) if x != i]
        n = cross(gens[j], gens[k]); s = dot(n, gens[i])
        if s < 0: n = tuple(-x for x in n); s = -s
        c = dot(n, u)
        hs.append((tuple(-x for x in n), -c))          # n.(x-u) >= 0  <=>  -n.x <= -c
        hs.append((n, c + s))                           # n.(x-u) <= s
    return hs

def vertices_of(hs):
    V = set()
    for (a, b), (c, d), (e, f) in combinations(hs, 3):
        D = det3(a, c, e)
        if D == 0: continue
        # Cramer
        bb = (b, d, f)
        x = tuple(Fr(det3(*[tuple(bb[r] if cc == col else (a, c, e)[r][cc] for cc in range(3)) for r in range(3)]), D) for col in range(3))
        if all(dot(h[0], x) <= h[1] for h in hs): V.add(x)
    return list(V)

def full_dim(V):
    if len(V) < 4: return False
    v0 = V[0]; rows = [tuple(x-y for x, y in zip(v, v0)) for v in V[1:]]
    for t in combinations(rows, 3):
        if det3(*t) != 0: return True
    return False

def simplify(hs, V):
    keep = []
    for h in hs:
        on = [v for v in V if dot(h[0], v) == h[1]]
        if len(on) >= 3 and full_dim_plane(on) and h not in keep: keep.append(h)
    return keep
def full_dim_plane(on):
    v0 = on[0]; rows = [tuple(x-y for x, y in zip(v, v0)) for v in on[1:]]
    for a, b in combinations(rows, 2):
        if cross(a, b) != (0, 0, 0): return True
    return False

def main():
    E3 = lambda v: sum(v) % 2 == 0
    C = cells(E3, (4, 4, 4))
    top = sorted(C[3]); print("3-cells in K_abs(E_3,[0,4]^3):", len(top), "  f-vector:", tuple(len(C[d]) for d in sorted(C)))
    P0 = [((-1, 0, 0), 0), ((0, -1, 0), 0), ((0, 0, -1), 0), ((1, 0, 0), 2), ((0, 1, 0), 2), ((0, 0, 1), 2), ((-1, -1, -1), -2)]
    V0 = vertices_of(P0); assert len(V0) == 7, len(V0)
    pieces = [(P0, V0)]
    t0 = time.time(); steps = 0
    vol = lambda cell: abs(det3(*cell[1]))
    top.sort(key=lambda c: -vol(c))
    for cell in top:
        chs = cell_halfspaces(cell); new = []
        for (hs, V) in pieces:
            if all(all(dot(h[0], v) <= h[1] for h in chs) for v in V): continue        # piece inside the cell
            if any(all(dot(h[0], v) >= h[1] for v in V) for h in chs): new.append((hs, V)); continue   # disjoint interiors
            pre = []
            for h in chs:
                # piece ∩ {h >= } ∩ previous <=
                cut = (tuple(-x for x in h[0]), -h[1])
                hs2 = hs + pre + [cut]
                V2 = vertices_of(hs2)
                if full_dim(V2):
                    new.append((simplify(hs2, V2), V2))
                pre.append(h)
            steps += 1
        pieces = new
        if not pieces: break
    print("cells used until covered:", steps, " pieces left with non-empty interior:", len(pieces), f"  ({time.time()-t0:.1f}s)")
    ok = len(pieces) == 0
    res = dict(statement="[0,2]^3 ∩ {x1+x2+x3>=2} is contained in U(E_3,[0,4]^3)", method="exact polytope subtraction by the 3-cells of K_abs(E_3,[0,4]^3)",
               three_cells=len(top), pieces_left=len(pieces), covered=ok, seconds=round(time.time()-t0, 1),
               scope="replay of the n=4 corner step only; not a re-verification of the release")
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "N4_COVER_REPLAY.json")
    json.dump(res, open(out, "w"), indent=1)
    print("COVERED" if ok else "NOT COVERED")
    # control: the same method on n=2 must leave pieces (the gap)
    C2 = cells(E3, (2, 2, 2)); top2 = sorted(C2[3]); pieces = [(P0, V0)]
    for cell in sorted(top2, key=lambda c: -vol(c)):
        chs = cell_halfspaces(cell); new = []
        for (hs, V) in pieces:
            if all(all(dot(h[0], v) <= h[1] for h in chs) for v in V): continue
            if any(all(dot(h[0], v) >= h[1] for v in V) for h in chs): new.append((hs, V)); continue
            pre = []
            for h in chs:
                cut = (tuple(-x for x in h[0]), -h[1]); hs2 = hs + pre + [cut]; V2 = vertices_of(hs2)
                if full_dim(V2): new.append((simplify(hs2, V2), V2))
                pre.append(h)
        pieces = new
    print("control n=2: 3-cells", len(top2), "pieces left", len(pieces), "(non-zero expected: the gap)")
    res["control_n2_pieces_left"] = len(pieces)
    json.dump(res, open(out, "w"), indent=1)
    return 0 if ok and len(pieces) > 0 else 1
if __name__ == "__main__":
    sys.exit(main())

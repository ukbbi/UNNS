"""GEO-III.B part 1: the three objects  K_abs (abstract), U_x (geometric image), and their raw data.
Reads the frozen v002 engine (frozen/geo2lib.py, byte-identical to GEO_I_v002/geometry/geo2lib.py)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'frozen')); sys.path.insert(0, HERE)
from fractions import Fraction as Fr
from geo2lib import (coords, fibre_points, graver_region, unit_moves, build_cells, boundary, lexpos,
                     d_aff, cell_vertices as v2_vertices, flag_cells, flag_betti)
import intersections as X


def fibre_complex(x, kind='move', kmax=None):
    """returns dict with F, ps, q, b, G (region Graver vectors, both signs), cells (list per dimension) for K_abs (kind='move')
    or the coordinate complex (kind='axis')."""
    ps, q, b = coords(x); k = len(ps)
    F = fibre_points(ps, q, b)
    G = graver_region(ps, q, b)
    moves = set(G) if kind == 'move' else set(unit_moves(k))
    cells = build_cells(F, moves, k if kmax is None else min(k, kmax)) if F else []
    return {'x': Fr(x), 'ps': ps, 'q': q, 'b': b, 'k': k, 'F': F, 'G': G, 'cells': cells}


def facets(cell):
    return list(boundary(cell).keys())


def maximal_cells(cells):
    """abstract-maximal cells: those that are not a facet of another cell."""
    nonmax = set()
    for j in range(1, len(cells)):
        for c in cells[j]:
            for f in facets(c): nonmax.add(f)
    return [c for dim in cells for c in dim if c not in nonmax]


def cover_cells(cells):
    """geometrically maximal convex cells whose union is U_x: abstract-maximal cells with those contained in another removed."""
    mx = maximal_cells(cells)
    mx.sort(key=lambda c: -len(c[1]))
    keep = []
    for c in mx:
        if not any(len(d[1]) >= len(c[1]) and X.cell_in_cell(c, d) for d in keep if d != c):
            keep.append(c)
    return keep


def edges_of(cells):
    return [c for c in cells[1]] if len(cells) > 1 else []


def edge_endpoints(e):
    u, (g,) = e
    return u, X.add(u, g)


def fibre_complex_data(res, q, b, kind='move', kmax=None):
    """Same as fibre_complex but from raw arithmetic data: residues res_i = p_i mod b, boxes q_i, modulus b.
    (Lambda_b depends on p_i only through p_i mod b; by Dirichlet every residue class coprime to b contains primes.)"""
    k = len(q)
    F = fibre_points(list(res), list(q), b)
    G = graver_region(list(res), list(q), b)
    moves = set(G) if kind == 'move' else set(unit_moves(k))
    cells = build_cells(F, moves, k if kmax is None else min(k, kmax)) if F else []
    return {'x': None, 'ps': list(res), 'q': list(q), 'b': b, 'k': k, 'F': F, 'G': G, 'cells': cells}

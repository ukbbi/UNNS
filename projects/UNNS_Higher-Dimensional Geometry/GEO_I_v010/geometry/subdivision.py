"""GEO-III.B  Valid embedded subdivisions with provenance.  Exact rational arithmetic only.

planar_subdivision : any union U of parallelograms / segments in R^2.  K_emb = faces / edges / vertices of the
                     arrangement of all supporting lines of the cover cells (plus a padded bounding box) that lie in U.
                     Every arrangement face is convex, so the result is a genuine face-to-face polyhedral complex.
graph_subdivision  : any union of segments in R^k: split every segment at all crossing points (1-skeleton arrangement).
Auxiliary vertices are never occurrences; each carries a provenance record.
"""
import functools
from math import gcd
from fractions import Fraction as Fr
import intersections as X


def _norm_line(p, g):
    A, B = g[1], -g[0]
    C = A * p[0] + B * p[1]
    d = gcd(gcd(abs(A), abs(B)), abs(C)) or 1
    A, B, C = A // d, B // d, C // d
    if A < 0 or (A == 0 and B < 0): A, B, C = -A, -B, -C
    return (A, B, C)


def _cross(a, b): return a[0] * b[1] - a[1] * b[0]


def _area2(poly):
    s = 0
    for i in range(len(poly)):
        x1, y1 = poly[i]; x2, y2 = poly[(i + 1) % len(poly)]
        s += x1 * y2 - x2 * y1
    return s            # twice the signed area


def _in_cell2(pt, cell):
    return X.point_in_cell(pt, cell)


def planar_subdivision(cover, F, refine=None, pad=1):
    """cover: list of cells ((u), gens) in R^2 (gens of length 1 or 2) whose union is U.  refine: all abstract cells (edges, squares)
    whose supporting lines must be subdivided so that every abstract cell image is a subcomplex (default: cover only).
    F: occurrence points.  Returns dict."""
    allcells = list(refine) if refine is not None else list(cover)
    Fset = set(F)
    xs = [v[0] for c in cover for v in X.cell_vertices(*c)]; ys = [v[1] for c in cover for v in X.cell_vertices(*c)]
    if any(len(u) != 2 for u, _ in cover): raise ValueError('planar_subdivision needs ambient dimension 2')
    x0, x1, y0, y1 = min(xs) - pad, max(xs) + pad, min(ys) - pad, max(ys) + pad
    lines = {}                     # line -> list of original segment ids on it
    segs = []                      # original segments (a,b) with ids
    def reg(p, q):
        g = (q[0] - p[0], q[1] - p[1]); L = _norm_line(p, g)
        sid = len(segs); segs.append((tuple(p), tuple(q))); lines.setdefault(L, []).append(sid)
    for (u, gens) in allcells:
        if len(gens) == 0: continue
        vs = X.cell_vertices(u, gens)
        if len(gens) == 1: reg(vs[0], vs[1])
        else:                                   # 4 sides of the parallelogram
            g1, g2 = gens
            reg(u, X.add(u, g1)); reg(u, X.add(u, g2)); reg(X.add(u, g1), X.add(X.add(u, g1), g2)); reg(X.add(u, g2), X.add(X.add(u, g1), g2))
    for L in ((1, 0, x0), (1, 0, x1), (0, 1, y0), (0, 1, y1)): lines.setdefault(L, [])
    LL = list(lines)
    pts = {}                       # point -> set of line indices
    for i in range(len(LL)):
        A1, B1, C1 = LL[i]
        for j in range(i + 1, len(LL)):
            A2, B2, C2 = LL[j]
            D = A1 * B2 - A2 * B1
            if D == 0: continue
            p = (Fr(C1 * B2 - C2 * B1, D), Fr(A1 * C2 - A2 * C1, D))
            if x0 <= p[0] <= x1 and y0 <= p[1] <= y1:
                pts.setdefault(p, set()).update((i, j))
    for f in Fset:
        p = (Fr(f[0]), Fr(f[1]))
        s = pts.setdefault(p, set())
        for i, (A, B, C) in enumerate(LL):
            if A * p[0] + B * p[1] == C: s.add(i)
    # edges: consecutive points along each line
    adj = {p: [] for p in pts}
    edges = set()
    for i, (A, B, C) in enumerate(LL):
        on = sorted([p for p, s in pts.items() if i in s], key=lambda p: (p[0], p[1]))
        for a, b in zip(on, on[1:]):
            edges.add((a, b)); adj[a].append(b); adj[b].append(a)
    # angular order
    def half(d): return 0 if (d[1] > 0 or (d[1] == 0 and d[0] > 0)) else 1
    def cmp(a, b):
        ha, hb = half(a), half(b)
        if ha != hb: return -1 if ha < hb else 1
        c = _cross(a, b)
        return -1 if c > 0 else (1 if c < 0 else 0)
    order = {}
    for p, nb in adj.items():
        nb = sorted(set(nb), key=functools.cmp_to_key(lambda a, b: cmp((a[0] - p[0], a[1] - p[1]), (b[0] - p[0], b[1] - p[1]))))
        order[p] = nb
    seen = set(); faces = []
    for p in order:
        for q in order[p]:
            if (p, q) in seen: continue
            cyc = []; a, b = p, q
            while (a, b) not in seen:
                seen.add((a, b)); cyc.append(a)
                nb = order[b]; idx = nb.index(a)
                c = nb[(idx - 1) % len(nb)]
                a, b = b, c
            faces.append(cyc)
    bounded = [c for c in faces if _area2(c) > 0]
    outer = [c for c in faces if _area2(c) <= 0]
    cov2 = [c for c in cover if len(c[1]) == 2]; cov1 = [c for c in cover if len(c[1]) == 1]
    def covered_pt(pt): return any(_in_cell2(pt, c) for c in cover)
    cface = []
    for cyc in bounded:
        cx = sum(v[0] for v in cyc) / len(cyc); cy = sum(v[1] for v in cyc) / len(cyc)
        if any(_in_cell2((cx, cy), c) for c in cov2): cface.append(cyc)
    # included edges: boundary of covered faces, or midpoint in a cover cell
    inc = set()
    for cyc in cface:
        for i in range(len(cyc)):
            a, b = cyc[i], cyc[(i + 1) % len(cyc)]; inc.add((a, b) if (a, b) in edges else (b, a))
    for (a, b) in edges:
        if (a, b) in inc: continue
        mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        if covered_pt(mid): inc.add((a, b))
    verts = set(v for e in inc for v in e) | {(Fr(f[0]), Fr(f[1])) for f in Fset}
    # provenance of vertices
    prov = {}
    for v in verts:
        thr = [sid for sid, (a, b) in enumerate(segs) if X.seg_relation(a, b, v, v)[0] != 'disjoint' or _on_seg(a, b, v)]
        kind = 'occurrence' if (v[0].denominator == 1 and v[1].denominator == 1 and (int(v[0]), int(v[1])) in Fset) else ('crossing' if len(thr) >= 2 else 'arrangement')
        prov[v] = {'kind': kind, 'segments': thr}
    return {'vertices': sorted(verts), 'edges': sorted(inc), 'faces': cface, 'prov': prov, 'segs': segs, 'n_lines': len(LL),
            'bbox': (x0, x1, y0, y1), 'outer_faces': len(outer)}


def _on_seg(a, b, v):
    cr = (b[0] - a[0]) * (v[1] - a[1]) - (b[1] - a[1]) * (v[0] - a[0])
    if cr != 0: return False
    return min(a[0], b[0]) <= v[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= v[1] <= max(a[1], b[1])


def planar_cells_for_homology(sub):
    """cells by dimension with oriented boundary dictionaries for chain_complex.betti."""
    V = {v: i for i, v in enumerate(sub['vertices'])}
    E = {e: i for i, e in enumerate(sub['edges'])}
    cells = [list(range(len(V))), list(range(len(E))), list(range(len(sub['faces'])))]
    ev = {i: (V[a], V[b]) for (a, b), i in E.items()}
    def bd(c):
        dim, idx = c
        if dim == 1:
            a, b = ev[idx]; return {(0, b): 1, (0, a): -1}
        out = {}
        cyc = sub['faces'][idx]
        for i in range(len(cyc)):
            a, b = cyc[i], cyc[(i + 1) % len(cyc)]
            if (a, b) in E: out[(1, E[(a, b)])] = out.get((1, E[(a, b)]), 0) + 1
            else: out[(1, E[(b, a)])] = out.get((1, E[(b, a)]), 0) - 1
        return out
    layered = [[(0, i) for i in cells[0]], [(1, i) for i in cells[1]], [(2, i) for i in cells[2]]]
    return layered, (lambda c: {} if c[0] == 0 else bd(c))


def validate_planar(sub, cover, F):
    """independent exact validation of a planar subdivision.  returns dict of named boolean checks."""
    res = {}
    E = sub['edges']
    # V1 faces convex, ccw, nondegenerate
    ok_conv = True
    for cyc in sub['faces']:
        n = len(cyc)
        if _area2(cyc) <= 0: ok_conv = False
        for i in range(n):
            a, b, c = cyc[i], cyc[(i + 1) % n], cyc[(i + 2) % n]
            if _cross((b[0] - a[0], b[1] - a[1]), (c[0] - b[0], c[1] - b[1])) < 0: ok_conv = False
    res['faces_convex_ccw'] = ok_conv
    # V2 edges meet only at common endpoints (exact)
    ok_e = True
    for i in range(len(E)):
        a, b = E[i]
        for j in range(i + 1, len(E)):
            c, d = E[j]
            if max(min(a[0], b[0]), min(c[0], d[0])) > min(max(a[0], b[0]), max(c[0], d[0])): continue
            if max(min(a[1], b[1]), min(c[1], d[1])) > min(max(a[1], b[1]), max(c[1], d[1])): continue
            if not _seg_ok_frac(a, b, c, d): ok_e = False
    res['edges_meet_only_at_endpoints'] = ok_e
    # V3 areas: every 2-cell of the cover is exactly tiled; no face outside the cover
    cov2 = [c for c in cover if len(c[1]) == 2]
    ok_area = True
    for (u, (g1, g2)) in cov2:
        area2 = abs(_cross(g1, g2)) * 2
        tot = 0
        poly_in = [cyc for cyc in sub['faces'] if X.point_in_cell((sum(v[0] for v in cyc) / len(cyc), sum(v[1] for v in cyc) / len(cyc)), (u, (g1, g2)))]
        for cyc in poly_in:
            tot += _area2(cyc)
            if not all(X.point_in_cell(v, (u, (g1, g2))) for v in cyc): ok_area = False
        if tot != area2: ok_area = False
    res['two_cells_exactly_tiled'] = ok_area
    ok_out = all(any(X.point_in_cell((sum(v[0] for v in cyc) / len(cyc), sum(v[1] for v in cyc) / len(cyc)), c) for c in cov2) for cyc in sub['faces'])
    res['no_face_outside_cover'] = ok_out
    # V4 every cover segment is exactly a union of consecutive sub-edges; every complex edge lies in the cover
    ok_seg = True
    Eset = set(E)
    for (u, gens) in cover:
        vs = X.cell_vertices(u, gens)
        segs = [(vs[0], vs[1])] if len(gens) == 1 else [(u, X.add(u, gens[0])), (u, X.add(u, gens[1])), (X.add(u, gens[0]), X.add(X.add(u, gens[0]), gens[1])), (X.add(u, gens[1]), X.add(X.add(u, gens[0]), gens[1]))]
        for (a, b) in segs:
            a = (Fr(a[0]), Fr(a[1])); b = (Fr(b[0]), Fr(b[1]))
            L2 = (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2
            tot = Fr(0)
            for (c, d) in E:
                if _on_seg(a, b, c) and _on_seg(a, b, d):
                    tot += (d[0] - c[0]) ** 2 + (d[1] - c[1]) ** 2 if False else 0
            # use parameter lengths along the segment
            ts = []
            for (c, d) in E:
                if _on_seg(a, b, c) and _on_seg(a, b, d):
                    dx, dy = b[0] - a[0], b[1] - a[1]
                    t1 = ((c[0] - a[0]) * dx + (c[1] - a[1]) * dy) / L2; t2 = ((d[0] - a[0]) * dx + (d[1] - a[1]) * dy) / L2
                    ts.append(tuple(sorted((t1, t2))))
            ts.sort(); cur = Fr(0)
            for t1, t2 in ts:
                if t1 != cur: ok_seg = False; break
                cur = t2
            if cur != 1: ok_seg = False
    res['cover_segments_exactly_subdivided'] = ok_seg
    mid_ok = all(any(X.point_in_cell(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), c) for c in cover) for (a, b) in E)
    res['complex_edges_inside_cover'] = mid_ok
    # V5 every occurrence is a vertex
    Vs = set(sub['vertices'])
    res['occurrences_are_vertices'] = all((Fr(f[0]), Fr(f[1])) in Vs for f in F)
    res['all_ok'] = all(res.values())
    return res


def _seg_ok_frac(a, b, c, d):
    """segments with Fraction endpoints meet only in a common endpoint (or not at all)."""
    # scale to integers
    den = 1
    for p in (a, b, c, d):
        for v in p: den = den * v.denominator // gcd(den, v.denominator)
    A = tuple(int(v * den) for v in a); B = tuple(int(v * den) for v in b); C = tuple(int(v * den) for v in c); D = tuple(int(v * den) for v in d)
    kind, pt = X.seg_relation(A, B, C, D)
    return kind in ('disjoint', 'shared_endpoint', 'collinear_touch')


def graph_subdivision(edges):
    """edges: list of (u,v) integer endpoints in R^k.  Splits all at interior crossings.  Returns dict with vertices (with
    provenance), edges.  Raises if a collinear overlap or endpoint-on-interior is met (cannot occur for Graver edges, Lemma 2/3)."""
    n = len(edges); cuts = [set() for _ in range(n)]; cp = {}
    for i in range(n):
        for j in range(i + 1, n):
            kind, p = X.seg_relation(*edges[i], *edges[j])
            if kind == 'interior_cross':
                cuts[i].add(p); cuts[j].add(p); cp.setdefault(p, set()).update((i, j))
            elif kind in ('endpoint_on_interior', 'collinear_overlap'):
                raise ValueError('degenerate: %s' % kind)
    out = []
    for i, (u, v) in enumerate(edges):
        k = len(u); pts = [tuple(Fr(c) for c in u)] + sorted(cuts[i], key=lambda p: sum((p[c] - u[c]) ** 2 for c in range(k))) + [tuple(Fr(c) for c in v)]
        for a, b in zip(pts, pts[1:]): out.append((a, b))
    verts = set(p for e in out for p in e)
    return {'vertices': sorted(verts), 'edges': out, 'crossings': {p: sorted(s) for p, s in cp.items()}}

"""E2-P3 INDEPENDENT certificate verifier.  Imports nothing from exact_containment.py or from any builder module.
It re-derives every geometric fact it needs (cell vertices, parameters, vertex enumeration of leaf polytopes) from the integer
data in the certificate, using only Fractions.  verify_* return (ok: bool, reason: str)."""
from fractions import Fraction as Fr
from itertools import combinations, product


def _F(x):
    return Fr(x)


def _gauss(M, r):
    n = len(M)
    A = [[Fr(v) for v in row] + [Fr(x)] for row, x in zip(M, r)]
    for c in range(n):
        p = next((i for i in range(c, n) if A[i][c] != 0), None)
        if p is None:
            return None
        A[c], A[p] = A[p], A[c]
        pv = A[c][c]
        A[c] = [v / pv for v in A[c]]
        for i in range(n):
            if i != c and A[i][c] != 0:
                f = A[i][c]
                A[i] = [x - f * y for x, y in zip(A[i], A[c])]
    return [A[i][n] for i in range(n)]


def _dot(a, b):
    return sum(Fr(x) * Fr(y) for x, y in zip(a, b))


def _verts(base, gens):
    out = []
    for bits in product((0, 1), repeat=len(gens)):
        v = [Fr(x) for x in base]
        for b, g in zip(bits, gens):
            if b:
                v = [x + y for x, y in zip(v, g)]
        out.append(tuple(v))
    return out


def _params(base, gens, p):
    m = len(gens)
    d = [Fr(x) - Fr(y) for x, y in zip(p, base)]
    if m == 0:
        return [] if not any(d) else None
    G = [[_dot(a, b) for b in gens] for a in gens]
    t = _gauss(G, [_dot(g, d) for g in gens])
    if t is None:
        return None
    for j in range(len(d)):
        if sum(t[i] * gens[i][j] for i in range(m)) != d[j]:
            return None
    return t


def _in(base, gens, p):
    t = _params(base, gens, p)
    return t is not None and all(0 <= x <= 1 for x in t)


def _independent(gens):
    """integer gens linearly independent?  (Gram determinant nonzero via elimination)"""
    if not gens:
        return True
    G = [[_dot(a, b) for b in gens] for a in gens]
    return _gauss(G, [0] * len(G)) is not None


def _root_hs(base, gens, k):
    """H-description of the source cell, DERIVED HERE and validated on every vertex of the cell."""
    m = len(gens)
    hs = []
    base = [Fr(x) for x in base]
    G = [[_dot(a, b) for b in gens] for a in gens] if m else []
    for i in range(m):
        e = [Fr(int(j == i)) for j in range(m)]
        coef = _gauss(G, e)
        y = [sum(coef[j] * gens[j][c] for j in range(m)) for c in range(k)]
        hs.append(([-v for v in y], -_dot(y, base)))
        hs.append((y, _dot(y, base) + 1))
    # equalities: every unit-like vector orthogonal to the span, via projection of the coordinate axes
    for c in range(k):
        e = [Fr(int(j == c)) for j in range(k)]
        if m:
            co = _gauss(G, [_dot(g, e) for g in gens])
            proj = [sum(co[j] * gens[j][t] for j in range(m)) for t in range(k)]
            n = [e[t] - proj[t] for t in range(k)]
        else:
            n = e
        if any(n):
            hs.append((n, _dot(n, base)))
            hs.append(([-v for v in n], -_dot(n, base)))
    for v in _verts(base, gens):
        for a, c in hs:
            assert _dot(a, v) <= c, "internal: root description invalid"
    return hs


def _vertices(hs, k):
    V = set()
    for sub in combinations(range(len(hs)), k):
        x = _gauss([hs[i][0] for i in sub], [hs[i][1] for i in sub])
        if x is None:
            continue
        if all(_dot(a, x) <= c for a, c in hs):
            V.add(tuple(x))
    return V


def verify_noncontainment(cert, target_cells, k):
    """cert: NONCONTAINMENT certificate; target_cells: list of {'base','gens'} (the COMPLETE list of target cells to defeat)."""
    try:
        sc = cert["source_cell"]
        base, gens = sc["base"], sc["gens"]
        if len(gens) > k or not _independent(gens):
            return False, "source generators not independent"
        w = tuple(Fr(x) for x in cert["witness"])
        t = _params(base, gens, w)
        if t is None or not all(0 <= x <= 1 for x in t):
            return False, "witness not in source cell"
        if [Fr(x) for x in cert["params"]] != t:
            return False, "declared parameters do not reproduce witness"
        viol = {v["target"]: v for v in cert["violations"]}
        if len(viol) != len(target_cells) or set(viol) != set(range(len(target_cells))):
            return False, "violation list does not cover every target cell"
        for j, T in enumerate(target_cells):
            a = [Fr(x) for x in viol[j]["a"]]
            c = Fr(viol[j]["c"])
            for v in _verts(T["base"], T["gens"]):
                if _dot(a, v) > c:
                    return False, "inequality not valid on target cell %d" % j
            if not _dot(a, w) > c:
                return False, "inequality not strictly violated at witness (target %d)" % j
        return True, "ok"
    except Exception as e:  # any malformed certificate is rejected
        return False, "malformed: %r" % (e,)


def verify_containment(cert, target_cells, k):
    """Replay the closed-splitting tree.  Every leaf polytope must have all its vertices in the named target cell."""
    try:
        sc = cert["source_cell"]
        base, gens = sc["base"], sc["gens"]
        if len(gens) > k or not _independent(gens):
            return False, "source generators not independent"
        root = _root_hs(base, gens, k)

        def rec(node, hs, depth):
            if depth > 400:
                return False, "tree too deep"
            if node.get("empty"):
                return (len(_vertices(hs, k)) == 0), "empty leaf has vertices"
            if "leaf" in node:
                T = target_cells[node["leaf"]]
                V = _vertices(hs, k)
                if not V:
                    return True, "ok"          # empty piece
                for v in V:
                    if not _in(T["base"], T["gens"], v):
                        return False, "leaf vertex outside its target cell"
                return True, "ok"
            if "split" in node:
                a = [Fr(x) for x in node["split"][0]]
                c = Fr(node["split"][1])
                ok1, r1 = rec(node["lo"], hs + [(a, c)], depth + 1)
                if not ok1:
                    return False, r1
                return rec(node["hi"], hs + [([-x for x in a], -c)], depth + 1)
            return False, "bad node"

        return rec(cert["tree"], root, 0)
    except Exception as e:
        return False, "malformed: %r" % (e,)


def verify_hull_tree(cert, F, target_cells, k):
    """cert = {hull_halfspaces, tree}.  Checks (1) the root polytope equals conv(F) [every vertex of the root is a point of F and
    every point of F satisfies the root inequalities]; (2) replays the splitting tree: 'leaf' nodes must be inside the named target
    cell, 'gap' nodes must carry a point of the leaf polytope violating one valid inequality of EVERY target cell.
    Returns (ok, reason, n_gap_nodes).  n_gap_nodes == 0 proves U' = conv(F')."""
    try:
        hs0 = [([Fr(x) for x in a], Fr(c)) for a, c in cert["hull_halfspaces"]]
        Fset = set(tuple(Fr(x) for x in p) for p in F)
        for p in Fset:
            if not all(_dot(a, p) <= c for a, c in hs0):
                return False, "F point outside root", -1
        for v in _vertices(hs0, k):
            if v not in Fset:
                return False, "root vertex not in F", -1
        gaps = [0]

        def rec(node, hs):
            if node.get("empty"):
                return (len(_vertices(hs, k)) == 0), "empty leaf has vertices"
            if "leaf" in node:
                T = target_cells[node["leaf"]]
                for v in _vertices(hs, k):
                    if not _in(T["base"], T["gens"], v):
                        return False, "leaf vertex outside target cell"
                return True, "ok"
            if "gap" in node:
                w = tuple(Fr(x) for x in node["gap"]["point"])
                if not all(_dot(a, w) <= c for a, c in hs):
                    return False, "gap point not in its piece"
                viol = {v["target"]: v for v in node["gap"]["violations"]}
                if set(viol) != set(range(len(target_cells))):
                    return False, "gap violations incomplete"
                for j, T in enumerate(target_cells):
                    a = [Fr(x) for x in viol[j]["a"]]
                    c = Fr(viol[j]["c"])
                    if any(_dot(a, v) > c for v in _verts(T["base"], T["gens"])) or not _dot(a, w) > c:
                        return False, "bad violation (target %d)" % j
                gaps[0] += 1
                return True, "ok"
            a = [Fr(x) for x in node["split"][0]]
            c = Fr(node["split"][1])
            ok1, r1 = rec(node["lo"], hs + [(a, c)])
            if not ok1:
                return False, r1
            return rec(node["hi"], hs + [([-x for x in a], -c)])

        ok, r = rec(cert["tree"], hs0)
        return ok, r, gaps[0]
    except Exception as e:
        return False, "malformed: %r" % (e,), -1

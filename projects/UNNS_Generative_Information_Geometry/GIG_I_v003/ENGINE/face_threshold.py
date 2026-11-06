"""GIG-I v003 -- arithmetic activation thresholds of permutohedral faces (GIG-T17) and the exact P_k face grammar.

A face F = (B_1|...|B_r) of P_k contains the arrangements that list B_1 first, then B_2, ... (any order inside a block).
  K_F := lcm_{w in V(F)} K(w)                                  (definition)
  F in X_C(m)  <=>  K_F | m                                     (full-subcomplex rule + threshold law)
Closed form (T17):  K_F = lcm{ D(I) : I in Pref(F) },  Pref(F) = { B_1 u .. u B_{i-1} u U : 1<=i<=r, U subset B_i, U nonempty }
(all prefix sets of vertices of F), D(I) = denominator of R(I).
"""
import _v2path  # noqa: F401
from itertools import combinations
from math import lcm
import history_complex as hc
import threshold_closure as tc
import block_factor as bf


def faces(k):
    """list of (face tuple, dim, vertex-mask) of P_k, from the inherited ordered-partition construction."""
    fs, mask, dim, bnd = hc._complex_data(k)
    return [(fs[i], dim[i], mask[i]) for i in range(len(fs))]


def face_type(face):
    """combinatorial type = sorted tuple of block sizes >1  (e.g. (2,2,2)=cube, (3,2)=hexagonal prism, (4,)=truncated octahedron)."""
    return tuple(sorted((len(B) for B in face if len(B) > 1), reverse=True))


TYPE_NAME = {(2,): "edge", (2, 2): "square", (3,): "hexagon", (2, 2, 2): "cube", (3, 2): "hexagonal prism", (4,): "truncated octahedron"}


def pref_sets(face):
    out = set()
    base = 0
    for B in face:
        for r in range(1, len(B) + 1):
            for U in combinations(B, r):
                m = base
                for x in U:
                    m |= 1 << x
                out.add(m)
        for x in B:
            base |= 1 << x
    return out


def threshold_by_vertices(labels, face, K=None):
    K = K or tc.threshold_values(labels)
    pidx = hc.perm_index(len(labels))
    return lcm(*[K[pidx[v]] for v in hc._face_vertices(face)])


def threshold_closed_form(labels, face, D=None):
    D = D or bf.denominators(labels)
    return lcm(*[D[I] for I in pref_sets(face)])


def face_present(labels, m, face):
    return m % threshold_closed_form(labels, face) == 0


def threshold_table(labels, dim=3):
    """[(face, type, K_F)] for all faces of the given dimension."""
    D = bf.denominators(labels)
    return [(f, face_type(f), threshold_closed_form(labels, f, D)) for f, d, _ in faces(len(labels)) if d == dim]


def grammar(k, dim=3):
    """exact reference of the dim-dimensional faces of P_k: type counts, vertex counts, and facet counts by type."""
    fs, mask, dim_, bnd = hc._complex_data(k)
    out = {}
    for i, f in enumerate(fs):
        if dim_[i] != dim:
            continue
        t = face_type(f)
        d = out.setdefault(t, {"count": 0, "vertices": set(), "facets": set(), "facet_types": set()})
        d["count"] += 1
        d["vertices"].add(bin(mask[i]).count("1"))
        d["facets"].add(len(bnd[i]))
        d["facet_types"].add(tuple(sorted(__import__("collections").Counter(face_type(fs[j]) for j in bnd[i]).items())))
    return out

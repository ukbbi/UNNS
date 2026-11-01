"""E2-P4 independent audit.  Re-derives arithmetic, lattices, fibres, Graver sets and cell complexes from first principles (engine/p2/geometry_audit.py
and engine/audit_p3.py are themselves independent of the builder) and verifies every stored certificate with engine/certificate_check.py.
It imports NOTHING from arithmetic_family / coupled_lattices / exact_containment / target_gap (the E2-P4 builder modules)."""
from fractions import Fraction as Fr
from itertools import product

import _boot  # noqa: F401
import audit_p3 as au
import certificate_check as cc
import geometry_audit as ga

P = (2, 5, 11)


def ind_transition(m):
    x = Fr(2 * 110 ** (4 * m), 9)
    P_, q, b = ga.coords(x)
    x2, L, G, ds = ga.C_brute(x)
    P2, q2, b2 = ga.coords(x2)
    return {"x": x, "x2": x2, "L": L, "G": G, "n_D": len(ds), "primes": P_, "box": q, "b": b, "b2": b2,
            "ok": x2 == Fr(110 ** (4 * m), 3) and P_ == P2 == P and q == q2 == (2 * m,) * 3 and b == 9 and b2 == 3 and G == 9 and L == 110 ** (2 * m)}


def ind_lattices(m):
    q = (2 * m,) * 3
    F9 = ga.fibre(P, q, 9)
    F3 = ga.fibre(P, q, 3)
    ok9 = set(F9) == {e for e in product(range(q[0] + 1), repeat=3) if any(e) and (e[0] - e[1] + e[2]) % 6 == 0}
    ok3 = set(F3) == {e for e in product(range(q[0] + 1), repeat=3) if any(e) and sum(e) % 2 == 0}
    return {"ok": ok9 and ok3 and set(F9) < set(F3), "n_F9": len(F9), "n_F3": len(F3)}


def ind_nonrectangular():
    """|H_b| < prod ord(p_i), by direct enumeration of the residues p1^a p2^b p3^c mod b."""
    out = {}
    for b in (9, 3):
        orders = []
        for p in P:
            r, k = p % b, 1
            while r != 1:
                r = r * p % b
                k += 1
            orders.append(k)
        H = {pow(2, a, b) * pow(5, c, b) * pow(11, d, b) % b for a in range(7) for c in range(7) for d in range(7)}
        prod = orders[0] * orders[1] * orders[2]
        out[str(b)] = {"orders": orders, "H": len(H), "prod": prod, "nonrectangular": len(H) < prod}
    return out


def ind_cells(q, b):
    F, cells = au.independent_cells(P, q, b)
    mx = au.maximal_cells(cells)
    js = [{"base": list(c[0]), "gens": [list(g) for g in c[1]]} for c in mx]
    return F, js


def same_family(a, b):
    return au.as_vertexset_family(a) == au.as_vertexset_family(b)


def verify_forward(rec, q, b, b2):
    """rec = stored {source_maximal, target_maximal, certificates} for U(b) <= U(b2).  Returns (ok, why)."""
    k = len(q)
    F, S = ind_cells(q, b)
    F2, T = ind_cells(q, b2)
    if not same_family(S, rec["source_maximal"]):
        return False, "source maximal cells differ from independent derivation"
    if not same_family(T, rec["target_maximal"]):
        return False, "target maximal cells differ from independent derivation"
    want = {(tuple(c["base"]),) + tuple(tuple(g) for g in c["gens"]) for c in S}
    got = {(tuple(c["source_cell"]["base"]),) + tuple(tuple(g) for g in c["source_cell"]["gens"]) for c in rec["certificates"]}
    if want != got:
        return False, "certificates do not cover every independently derived source maximal cell"
    for c in rec["certificates"]:
        ok, why = cc.verify_containment(c, rec["target_maximal"], k)
        if not ok:
            return False, why
    return True, "ok"


def verify_noncontained(rec, q, b, b2):
    k = len(q)
    F, S = ind_cells(q, b)
    F2, T = ind_cells(q, b2)
    if not same_family(T, rec["target_maximal"]):
        return False, "target maximal cells differ from independent derivation"
    return cc.verify_noncontainment(rec["certificate"], rec["target_maximal"], k)


def verify_point(rec, q, b_union):
    """Stored point certificate: the lattice point is not in U(b_union).  rec['target_maximal'] must equal independent maximal cells."""
    k = len(q)
    F, T = ind_cells(q, b_union)
    if not same_family(T, rec["target_maximal"]):
        return False, "union cells differ from independent derivation"
    w = tuple(Fr(x) for x in rec["certificate"]["witness"])
    if tuple(int(x) for x in rec["point"]) != tuple(int(x) for x in w):
        return False, "witness is not the declared point"
    return cc.verify_noncontainment(rec["certificate"], rec["target_maximal"], k)


def verify_hull(rec, q, b2):
    """Hull-cover tree: returns (ok, why, n_gap_nodes) against INDEPENDENTLY derived fibre and maximal cells."""
    F2, T = ind_cells(q, b2)
    if not same_family(T, rec["target_maximal"]):
        return False, "target maximal cells differ from independent derivation", None
    F2l = [tuple(v) for v in F2]
    return cc.verify_hull_tree({"hull_halfspaces": rec["hull_halfspaces"], "tree": rec["tree"]}, F2l, rec["target_maximal"], len(q))


def ind_lemma_cube(n):
    """Independent restatement of the cube-tiling lemma using the independently computed Graver set of E_3 at box (2,2,2)."""
    G = set(tuple(g) for g in ga.graver(P, (2, 2, 2), 3))
    gens_ok = all(g in G or tuple(-x for x in g) in G for g in ((2, 0, 0), (0, 2, 0), (0, 0, 2)))
    F = set(ga.fibre(P, (n, n, n), 3))
    ok = all(tuple(a + e for a, e in zip(w, d)) in F for w in product(range(0, n - 1, 2), repeat=3) if any(w) for d in product((0, 2), repeat=3))
    return gens_ok and ok

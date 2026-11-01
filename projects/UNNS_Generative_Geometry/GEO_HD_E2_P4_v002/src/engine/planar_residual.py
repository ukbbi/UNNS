"""E2-P3 / P3-E2: planar enumeration, G12-T8 classification and exact verdicts for FIELD-I transitions with k = 2.

Deterministic: states are visited in the fixed order (prime pair, box, b); every resource limit is written to
data/P3_SEARCH_LIMITS.json BEFORE the search; the sweep can be resumed from a (pair, box, b) index without changing the sample."""
import math
import os
import sys
import time
from collections import Counter
from fractions import Fraction as Fr
from itertools import combinations, product

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import coverage_gap as cg  # noqa: E402
import exact_containment as ec  # noqa: E402

lt, ft = cg.lt, cg.ft


def squarefree(r):
    if r == 1:
        return True
    if r >= 10 ** 12:
        return None
    p = 2
    while p <= 10 ** 4:
        if r % p == 0:
            if r % (p * p) == 0:
                return False
            r //= p
        if r == 1:
            return True
        p += 1 if p == 2 else 2
    return math.isqrt(r) ** 2 != r


def same_coords(x2, P, q):
    """True / False / None (undecided): active primes and box of x2 equal (P, q)?"""
    a = x2.numerator
    for p, m in zip(P, q):
        v = 0
        while a % p == 0:
            a //= p
            v += 1
        if v // 2 != m:
            return False
    return squarefree(a)


ORDER_PRODUCT_LIMIT = 20000
TARGET_DENOMINATOR_LIMIT = 2 * 10 ** 6      # multiplicative orders are found by iteration: never iterate to a larger modulus


def states(pool, qmax, bmax, k, odd=False):
    """Deterministic state order.  odd=True also visits numerators with exponent 2q_i+1 (box unchanged)."""
    parities = list(product((0, 1), repeat=k)) if odd else [(0,) * k]
    for P in combinations(pool, k):
        for q in product(range(1, qmax + 1), repeat=k):
            for par in parities:
                a = 1
                for p, m, e in zip(P, q, par):
                    a *= p ** (2 * m + e)
                for b in range(2, bmax + 1):
                    if math.gcd(a, b) == 1:
                        yield P, q, b, a


def screen(P, q, b, a, k):
    """Return (row or None, skip_reason)."""
    x = Fr(a, b)
    ds = ft.D(x)
    if not ds:
        return None, "empty_fibre"
    r = ft.C_step(x)
    x2 = r["next"]
    sc = same_coords(x2, P, q)
    if sc is not True:
        return None, ("coordinates_change" if sc is False else "UNAVAILABLE_coordinates_undecided")
    b2 = x2.denominator
    if b2 > TARGET_DENOMINATOR_LIMIT:
        return None, "UNAVAILABLE_target_denominator_large"
    if math.prod(lt.orders(P, b)) > ORDER_PRODUCT_LIMIT or math.prod(lt.orders(P, b2)) > ORDER_PRODUCT_LIMIT:
        return None, "UNAVAILABLE_order_product_large"
    if lt.describe(P, b)["index"] == 1:
        return None, "source_trivial_lattice"
    rel = lt.relation(P, b, b2)
    if rel == "EQUAL":
        return None, "equal_lattices"
    return {"primes": list(P), "box": list(q), "x": str(x), "x_next": str(x2), "b": b, "b_next": b2, "relation": rel,
            "index_source": lt.describe(P, b)["index"], "index_target": lt.describe(P, b2)["index"]}, None


def evaluate_planar(row, with_reverse=True, node_limit=20000, gap=True):
    """Exact verdict for one planar row (dict as produced by screen)."""
    P, q, b, b2 = tuple(row["primes"]), tuple(row["box"]), row["b"], row["b_next"]
    out = dict(row)
    res, F2, cells2 = cg.geometric_verdict(P, b, b2, q, node_limit)
    out["verdict"] = res["verdict"]
    out["n_source_maximal"], out["n_target_maximal"] = res["n_source_maximal"], res["n_target_maximal"]
    if res["verdict"] == "NOT_CONTAINED":
        out["n_noncontained_source_cells"] = res["n_noncontained_source_cells"]
        out["witness"] = res["certificate"]["witness"]
        out["witness_cell"] = res["certificate"]["source_cell"]
    cl = cg.classify_target_planar(P, b2, q) if b2 > 1 else {"class": "TARGET_Z2_TRIVIAL", "d": 1, "a": 1, "c": 1, "s": 0,
                                                            "Qn": list(q), "verified": True,
                                                            "reason": "target lattice is Z^2"}
    out["target_class"] = cl["class"]
    out["target_normal_form"] = {k: cl[k] for k in ("d", "a", "c", "s", "Qn", "verified")}
    if gap:
        g = cg.coverage_gap_record(P, b2, q, F2, cells2)
        out["hull_covered"] = g.get("hull_covered")
        out["gap_status"] = g["status"]
        out["gap_area"] = g.get("gap_area")
        out["n_gap_pieces"] = g.get("n_gap_pieces")
    if with_reverse and res["verdict"] == "CONTAINED":
        # U' <= U ?  (decides EQUAL vs strict)
        F, G, cells = cg.cells_of(P, b, q)
        back = ec.decide_union(cells2, cells, len(q), node_limit)
        out["reverse_verdict"] = back["verdict"]
        out["union_relation"] = "EQUAL" if back["verdict"] == "CONTAINED" else "U_STRICT_SUBSET_U2"
    return out


def sweep(pool, qmax, bmax, k, start=0, stop=None, progress=None, odd=False):
    rows, skips = [], Counter()
    t0 = time.time()
    n = 0
    for idx, (P, q, b, a) in enumerate(states(pool, qmax, bmax, k, odd)):
        if idx < start:
            continue
        if stop is not None and idx >= stop:
            break
        n += 1
        row, why = screen(P, q, b, a, k)
        if row is None:
            skips[why] += 1
        else:
            rows.append(row)
        if progress and n % 20000 == 0:
            progress("state %d  rows %d  %.0fs" % (idx, len(rows), time.time() - t0))
    return rows, dict(skips), time.time() - t0

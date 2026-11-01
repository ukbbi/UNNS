"""E2-P4 builder-side two-direction union comparison (spec 4.1) on top of the pinned E2-P3 exact engine.
The engine itself (src/engine/exact_containment.py: closed splitting, H-representations, exact Fractions) is NOT modified."""
import json
import time

import _boot  # noqa: F401
import coverage_gap as cg
import exact_containment as ec
import fibre_transport as ft
import e1_cell_transport as ct0
import graver_transport as gt


def side(P, b, q):
    F = cg.fibre_of(P, b, q)
    G = gt.graver_fast(P, b, q)
    Go = ft.oriented(G)
    cx = ct0.build_complex(F, Go, len(q))
    cells = []
    for j in sorted(cx):
        for key, c in cx[j].items():
            cells.append((tuple(c.base), tuple(tuple(g) for g in c.gens)))
    return {"F": F, "G": Go, "cx": cx, "cells": cells}


def census(sd):
    cx = sd["cx"]
    f = [len(cx[j]) for j in sorted(cx)]
    try:
        betti = list(ct0.betti_complex(cx))
    except Exception as e:  # pragma: no cover
        betti = "UNAVAILABLE: %r" % (e,)
    return {"n_fibre": len(sd["F"]), "n_graver_oriented": len(sd["G"]), "f_vector": f, "abstract_betti": betti}


def classify(fwd, rev):
    a, b = fwd["verdict"] == "CONTAINED", rev["verdict"] == "CONTAINED"
    return "EQUAL" if a and b else "SOURCE_CONTAINED" if a else "TARGET_CONTAINED" if b else "INCOMPARABLE"


def compare(P, b, b2, q, node_limit=200000, reverse=True):
    """U(b) vs U(b2) in both directions.  Returns the builder-side result (certificates included)."""
    k = len(q)
    t0 = time.time()
    S, T = side(P, b, q), side(P, b2, q)
    out = {"primes": list(P), "box": list(q), "b": b, "b_next": b2, "census_source": census(S), "census_target": census(T),
           "fibre_inclusion": set(S["F"]) <= set(T["F"])}
    fwd = ec.decide_union(S["cells"], T["cells"], k, node_limit)
    out["forward"] = fwd
    if reverse:
        rev = ec.decide_union(T["cells"], S["cells"], k, node_limit)
        out["reverse"] = rev
        out["classification"] = classify(fwd, rev)
    out["seconds"] = round(time.time() - t0, 2)
    return out


def point_noncontainment(P, b_src, b_tgt, q, point):
    """Certificate that the lattice point `point` (a 0-cell of the source lattice b_src) is NOT in U(b_tgt)."""
    k = len(q)
    T = side(P, b_tgt, q)
    Tmax = ec.geometric_maximal(T["cells"], k)
    targets = [ec.Target(b, gs, k) for b, gs in Tmax]
    from fractions import Fraction as Fr
    w = tuple(Fr(x) for x in point)
    cert = ec.noncontainment_certificate(tuple(point), (), w, targets, k)
    return cert, [t.as_json() for t in targets]

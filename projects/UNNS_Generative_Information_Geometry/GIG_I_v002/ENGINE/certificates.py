"""GIG-I v002 -- independently checkable witness records.

A certificate stores contents, sources, masks, explicit vertex lists, bijections and every number needed to re-check
the claim by calling verify_certificate(), which rebuilds each set from content + source by DIRECT forward simulation
(history_fibres.is_admissible), recomputes face counts / boundary ranks / Betti numbers with the two independent
topology implementations (v001 history_complex and v002 cell_signature) and re-verifies any stated bijection edge by edge.
"""
import _v1path  # noqa: F401
import hashlib
import json
import os
import platform
from math import prod
import history_complex as hc
import history_fibres as hf
import swap_graph as sg
import census as v1census
import threshold_closure as tc
import cell_signature as cs
import graph_iso as gi

SOFTWARE = "GIG_I_v002"
HERE = os.path.dirname(os.path.abspath(__file__))


def _sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def software_hashes():
    out = {}
    for d in (HERE, os.path.join(_v1path.V001, "ENGINE")):
        for fn in sorted(os.listdir(d)):
            if fn.endswith(".py"):
                out[os.path.basename(os.path.dirname(d)) + "/ENGINE/" + fn] = _sha(os.path.join(d, fn))
    return out


def simulate_mask(content, m):
    labs = sorted(content)
    k = len(labs)
    mask = 0
    for i, p in enumerate(hc.perms(k)):
        if hf.is_admissible(m, tuple(labs[j] for j in p)):
            mask |= 1 << i
    return mask


def piece_record(content, m):
    labs = sorted(content)
    k = len(labs)
    mask = simulate_mask(labs, m)
    thr = tc.source_mask(labs, m)
    return _record(mask, k, labs, m, thr)


def mask_record(mask, k, label="non-arithmetic arrangement set"):
    """record for an arbitrary arrangement set (no content / source)."""
    r = _record(mask, k, None, None, None)
    r["note"] = label
    return r


def _record(mask, k, labs, m, thr):
    adj = cs.adjacency(mask, k)
    cd = cs.cell_data(mask, k)
    cc = tc.ContentClosure(labs) if labs else None
    comps = sg.components(adj)
    fv = hc.f_vector(mask, k)
    bt = hc.betti(mask, k)
    verts = [hc.perms(k)[i] for i in range(len(hc.perms(k))) if mask >> i & 1]
    arith = {}
    if labs:
        arith = {"content": labs, "source": m, "source_factorisation": [list(x) for x in hf.factor(m)],
                 "source_squarefree": hf.is_squarefree(m), "mask_by_forward_simulation": hex(mask),
                 "mask_by_threshold_law": hex(thr), "mask_agreement": mask == thr,
                 "closed": cc.is_closed(mask), "minimal_source_L": cc.minimal_source(mask),
                 "L_squarefree": all(e <= 1 for e in cc.exponents(mask).values())}
    else:
        arith = {"content": None, "source": None}
    return {
        **arith, "mask_hex": hex(mask),
        "N": len(adj), "E": sum(map(len, adj)) // 2, "component_sizes": sorted(len(c) for c in comps),
        "degree_sequence": sorted(map(len, adj)),
        "f_vector": list(fv), "f_vector_independent": list(cd["f"]), "boundary_ranks": list(cd["ranks"]),
        "betti": list(bt), "betti_independent": list(cd["betti"]),
        "euler": cd["euler"], "euler_check": cd["euler_ok"],
        "vertices": [list(p) for p in verts],
    }


def _fine(adj):
    comps = sg.components(adj)
    return {"sizes": tuple(sorted(len(c) for c in comps)), "prof": sg.ball_profile(adj)}


def first_separating_radius(adjA, adjB, rmax=12):
    a, b = _fine(adjA), _fine(adjB)
    for r in range(rmax + 1):
        if v1census.truncated_signature(a, r) != v1census.truncated_signature(b, r):
            return r
    return None


def pair_certificate(cid, claim, specA, specB, note="", k=None):
    """specA/specB = (content, source)  or  ('mask', mask_int)  for a non-arithmetic arrangement set."""
    A = mask_record(specA[1], k) if specA[0] == "mask" else piece_record(*specA)
    B = mask_record(specB[1], k) if specB[0] == "mask" else piece_record(*specB)
    k = len(A["content"]) if A["content"] else k
    mA, mB = int(A["mask_hex"], 16), int(B["mask_hex"], 16)
    adjA, adjB = cs.adjacency(mA, k), cs.adjacency(mB, k)
    f = gi.find_isomorphism(adjA, adjB)
    verts_A = [tuple(v) for v in A["vertices"]]
    verts_B = [tuple(v) for v in B["vertices"]]
    iso = {"isomorphic": f is not None}
    if f is not None:
        iso["bijection"] = [[list(verts_A[v]), list(verts_B[f[v]])] for v in range(len(f))]
    else:
        iso["method"] = "exhaustive individualisation-refinement search (graph_iso.find_isomorphism); not a hash"
    df = [(a - b) for a, b in zip(A["f_vector"], B["f_vector"])]
    cert = {
        "id": cid, "claim": claim, "note": note, "k": k, "software": SOFTWARE, "python": platform.python_version(),
        "source_convention": "fixed source m for the stated content; 'source_squarefree' says whether m is a complete-history source",
        "A": A, "B": B, "graph_isomorphism": iso,
        "wl_hash_equal": gi.wl_hash(adjA) == gi.wl_hash(adjB),
        "first_separating_radius": first_separating_radius(adjA, adjB),
        "betti_differ": A["betti"] != B["betti"],
        "f_vector_difference_A_minus_B": df,
        "cells_differing": [{"dimension": d, "A": A["f_vector"][d], "B": B["f_vector"][d]} for d in range(k) if df[d]],
        "boundary_rank_difference_A_minus_B": [a - b for a, b in zip(A["boundary_ranks"], B["boundary_ranks"])],
        "source_hashes": software_hashes(),
    }
    return cert


def verify_piece(rec, k=None):
    errs = []
    content, m = rec["content"], rec["source"]
    if content is not None:
        k = len(content)
        mask = simulate_mask(content, m)
        if hex(mask) != rec["mask_hex"]:
            errs.append("mask != forward simulation")
        if tc.source_mask(content, m) != mask:
            errs.append("threshold law != simulation")
        if hf.is_squarefree(m) != rec["source_squarefree"]:
            errs.append("squarefree flag")
    else:
        mask = int(rec["mask_hex"], 16)
    if list(hc.f_vector(mask, k)) != rec["f_vector"]:
        errs.append("f-vector (v001)")
    cd = cs.cell_data(mask, k)
    if list(cd["f"]) != rec["f_vector"] or list(cd["ranks"]) != rec["boundary_ranks"]:
        errs.append("f-vector / boundary ranks (v002)")
    if list(hc.betti(mask, k)) != rec["betti"] or list(cd["betti"]) != rec["betti"]:
        errs.append("betti")
    if not cd["euler_ok"] or cd["euler"] != rec["euler"]:
        errs.append("euler")
    if any(rec["f_vector"][j] - rec["boundary_ranks"][j - 1] * (j >= 1) - (rec["boundary_ranks"][j] if j < k - 1 else 0)
           != rec["betti"][j] for j in range(k)):
        errs.append("beta_j = f_j - rank d_j - rank d_{j+1}")
    return errs


def verify_certificate(cert):
    errs = [("A: " + e) for e in verify_piece(cert["A"], cert["k"])] + [("B: " + e) for e in verify_piece(cert["B"], cert["k"])]
    k = cert["k"]
    mA, mB = int(cert["A"]["mask_hex"], 16), int(cert["B"]["mask_hex"], 16)
    adjA, adjB = cs.adjacency(mA, k), cs.adjacency(mB, k)
    iso = cert["graph_isomorphism"]
    if iso["isomorphic"]:
        vA = {tuple(p): i for i, p in enumerate(cert["A"]["vertices"])}
        vB = {tuple(p): i for i, p in enumerate(cert["B"]["vertices"])}
        f = [None] * len(vA)
        for a, b in iso["bijection"]:
            f[vA[tuple(a)]] = vB[tuple(b)]
        if None in f or not gi.verify_bijection(adjA, adjB, f):
            errs.append("stated bijection is not a graph isomorphism")
    else:
        if gi.find_isomorphism(adjA, adjB) is not None:
            errs.append("claimed non-isomorphic but an isomorphism exists")
    if (cert["A"]["betti"] != cert["B"]["betti"]) != cert["betti_differ"]:
        errs.append("betti_differ flag")
    return errs


def write(cert, folder):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, cert["id"] + ".json")
    with open(path, "w") as f:
        json.dump(cert, f, indent=1, sort_keys=True, default=str)
    return path


def source_value_of(rec):
    """minimal realizing source L(S) of a census record (see realizability.census)."""
    v = 1
    for q, e in rec["ex"].items():
        v *= q ** e
    return v

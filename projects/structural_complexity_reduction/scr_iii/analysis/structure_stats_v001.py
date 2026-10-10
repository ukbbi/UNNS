from __future__ import annotations
from collections import Counter
from typing import Mapping

from scr_iii.compat import install_scr_ii_path
install_scr_ii_path()
from generator.route_csp_i import structural_view
from grammar.route_grammar import initial_state, evaluate_gates, DEFAULT_TRANSITIONS


def _same_struct(a: Mapping, b: Mapping) -> bool:
    return (
        str(a["symbol"]) == str(b["symbol"]) and
        int(a["phase"]) == int(b["phase"]) and
        int(a["discontinuity"]) == int(b["discontinuity"])
    )


def structure_stats(instance: Mapping) -> dict:
    view = structural_view(instance)
    depth = int(view["depth"])
    meta = instance.get("coupling_metadata", {})
    backbone = [int(x) for x in meta.get("backbone_bits", [])]
    mask = set(int(x) for x in meta.get("mask_layers", []))
    if len(backbone) != depth:
        raise ValueError("Missing/invalid coupling_metadata.backbone_bits")

    distinguishing = []
    for i, layer in enumerate(view["layers"]):
        g = backbone[i]; d = 1 - g
        if not _same_struct(layer["options"][g], layer["options"][d]):
            distinguishing.append(i)

    dset = set(distinguishing)
    coverage = None if not dset else len(mask & dset) / len(dset)

    # Evaluate decoys from the good-path state without using target labels.
    state = initial_state(view)
    n_rej_free = 0
    decoy_fail_gates = Counter()
    for i, layer in enumerate(view["layers"]):
        g = backbone[i]; d = 1 - g
        if i not in mask:
            passed_d, fail_d, _, _ = evaluate_gates(state, layer["options"][d], depth - i - 1, DEFAULT_TRANSITIONS)
            if not passed_d:
                n_rej_free += 1
                decoy_fail_gates[str(fail_d)] += 1
        passed_g, fail_g, _, new_state = evaluate_gates(state, layer["options"][g], depth - i - 1, DEFAULT_TRANSITIONS)
        if not passed_g:
            raise RuntimeError(f"Good path failed frozen grammar at layer {i}: {fail_g}")
        state = new_state

    leaves = 0
    expanded = 0
    gate_evals = Counter()
    first_rejections = Counter()
    state0 = initial_state(view)

    def dfs(i, state):
        nonlocal leaves, expanded
        if i == depth:
            leaves += 1
            return
        expanded += 1
        for bit in (0, 1):
            passed, fail, gates, new_state = evaluate_gates(state, view["layers"][i]["options"][bit], depth - i - 1, DEFAULT_TRANSITIONS)
            for g in gates:
                gate_evals[g] += 1
            if not passed:
                first_rejections[str(fail)] += 1
                continue
            dfs(i + 1, new_state)

    dfs(0, state0)
    N = 1 << depth
    return {
        "L": int(leaves),
        "structural_expanded_nodes": int(expanded),
        "R_leaf_structure": 1.0 - leaves / N,
        "distinguishing_layers": distinguishing,
        "D_count": len(distinguishing),
        "mask_count": len(mask),
        "coverage_C": coverage,
        "N_rej_free": int(n_rej_free),
        "decoy_fail_gates": dict(decoy_fail_gates),
        "structural_gate_evaluations": dict(gate_evals),
        "structural_first_rejections": dict(first_rejections),
    }

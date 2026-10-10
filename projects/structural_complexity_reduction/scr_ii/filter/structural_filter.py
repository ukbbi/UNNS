from __future__ import annotations
from collections import Counter
from typing import Mapping
from generator.route_csp_i import structural_view
from grammar.route_grammar import initial_state, evaluate_gates, DEFAULT_TRANSITIONS

FORBIDDEN_ARITHMETIC_FIELDS = {
    "checksum_modulus", "checksum_target", "cost_min", "cost_max", "terminal_seal",
    "cost", "checksum_weight"
}

def structural_signature(instance: Mapping) -> str:
    import hashlib, json
    view = structural_view(instance)
    raw = json.dumps(view, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()

def walk_prefix(instance: Mapping, bits: str, transitions=None):
    # Only structural_view is consumed here. This is an explicit firewall.
    view = structural_view(instance)
    tr = transitions or DEFAULT_TRANSITIONS
    state = initial_state(view)
    first_fail = None
    gate_counts = Counter()
    for i, ch in enumerate(bits):
        bit = int(ch)
        option = view["layers"][i]["options"][bit]
        passed, fail_gate, gates, new_state = evaluate_gates(
            state, option, view["depth"] - i - 1, tr
        )
        for g in gates:
            gate_counts[g] += 1
        if not passed:
            first_fail = fail_gate
            return False, first_fail, gate_counts, state
        state = new_state
    return True, None, gate_counts, state

from __future__ import annotations
import copy, hashlib, json, random
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

from scr_iii.compat import install_scr_ii_path
from scr_iii.engine_common import sha256_obj, stable_int, q_key, sigma_key
install_scr_ii_path()

from grammar.route_grammar import ALPHABET, DEFAULT_TRANSITIONS
from solver.exact_solver import solve_baseline
from generator.route_csp_i_v002 import (
    CHECKSUM_MODULUS, COST_MIN, COST_MAX, COST_HALF_WIDTH_FACTOR,
    DENSITY_MIN, DENSITY_MAX, MAX_ATTEMPTS, _arith_rng, _merge_attempt as v002_merge_attempt,
)

BENCHMARK = "ROUTE_CSP_C"
VERSION = "v001"
M_MIN = 4
PENALTY_FACTOR = 2


def _structure_with_mirror_u(seed: int, depth: int) -> Dict:
    """v002 structural law plus one unconditional mirror variate per layer."""
    rng = random.Random(int(seed))
    initial_symbol = rng.choice(ALPHABET)
    initial_phase = rng.randrange(3)
    prev_symbol = initial_symbol
    prev_phase = initial_phase
    last_disc: List[int] = []
    layers = []
    backbone_bits = []
    mirror_u = []
    for i in range(int(depth)):
        backbone_bit = rng.randrange(2)
        backbone_bits.append(backbone_bit)
        # Extra unconditional structure-stream variate required by the ratified spec.
        u_i = rng.random()
        mirror_u.append(u_i)
        symbol = rng.choice(DEFAULT_TRANSITIONS[prev_symbol])
        phase = (prev_phase + rng.choice((0, 1))) % 3
        may_disc = sum(last_disc[-3:]) == 0
        disc = 1 if may_disc and rng.random() < 0.12 else 0
        good = {"symbol": symbol, "phase": phase, "discontinuity": disc, "branch_id": backbone_bit}
        other_bit = 1 - backbone_bit
        decoy = {
            "symbol": rng.choice(ALPHABET),
            "phase": rng.randrange(3),
            "discontinuity": 1 if rng.random() < 0.35 else 0,
            "branch_id": other_bit,
        }
        opts = [None, None]
        opts[backbone_bit] = good
        opts[other_bit] = decoy
        layers.append({"index": i, "options": opts})
        prev_symbol = symbol
        prev_phase = phase
        last_disc = (last_disc + [disc])[-3:]
    return {
        "initial_symbol": initial_symbol,
        "initial_phase": initial_phase,
        "layers": layers,
        "backbone_bits": backbone_bits,
        "mirror_u": mirror_u,
    }


def _mask_permutation(seed: int, depth: int) -> List[int]:
    rng = random.Random(stable_int("SCR_III_MASK", int(seed), int(depth)))
    values = list(range(int(depth)))
    rng.shuffle(values)
    return values


def mask_for_q(permutation: Sequence[int], depth: int, q: float) -> List[int]:
    n = int(round(float(q) * int(depth)))
    return list(permutation[:n])


def _structure_for_sigma(base: Mapping, sigma: float) -> Dict:
    layers = copy.deepcopy(base["layers"])
    for i, layer in enumerate(layers):
        if float(base["mirror_u"][i]) < float(sigma):
            good_bit = int(base["backbone_bits"][i])
            decoy_bit = 1 - good_bit
            good = layer["options"][good_bit]
            decoy = layer["options"][decoy_bit]
            decoy["symbol"] = good["symbol"]
            decoy["phase"] = int(good["phase"])
            decoy["discontinuity"] = int(good["discontinuity"])
            # branch_id remains the decoy branch identifier.
    return {
        "initial_symbol": base["initial_symbol"],
        "initial_phase": int(base["initial_phase"]),
        "layers": layers,
    }


def _base_arithmetic(seed: int, depth: int, attempt: int) -> Dict:
    rng = _arith_rng(int(seed), int(attempt))
    arithmetic = []
    for _ in range(int(depth)):
        arithmetic.append([
            {"cost": rng.randint(COST_MIN, COST_MAX), "checksum_weight": rng.randrange(CHECKSUM_MODULUS)},
            {"cost": rng.randint(COST_MIN, COST_MAX), "checksum_weight": rng.randrange(CHECKSUM_MODULUS)},
        ])
    anchor = [rng.randrange(2) for _ in range(int(depth))]
    return {"arithmetic": arithmetic, "anchor": anchor}


def _build_instance_from_parts(
    seed: int,
    depth: int,
    sigma: float,
    q: float,
    attempt: int,
    base_structure: Mapping,
    permutation: Sequence[int],
    anti: bool = False,
) -> Dict:
    depth = int(depth)
    structure = _structure_for_sigma(base_structure, sigma)
    base_arith = _base_arithmetic(seed, depth, attempt)
    arithmetic = copy.deepcopy(base_arith["arithmetic"])
    anchor = list(base_arith["anchor"])
    mask = set(mask_for_q(permutation, depth, q))
    penalty = PENALTY_FACTOR * depth * COST_MAX

    for i in mask:
        good_bit = int(base_structure["backbone_bits"][i])
        decoy_bit = 1 - good_bit
        if anti:
            anchor[i] = decoy_bit
            arithmetic[i][good_bit]["cost"] = penalty
        else:
            anchor[i] = good_bit
            arithmetic[i][decoy_bit]["cost"] = penalty

    anchor_cost = sum(int(arithmetic[i][anchor[i]]["cost"]) for i in range(depth))
    anchor_checksum = sum(int(arithmetic[i][anchor[i]]["checksum_weight"]) for i in range(depth)) % CHECKSUM_MODULUS
    seal = int(anchor[-1])
    half = max(2, round(COST_HALF_WIDTH_FACTOR * depth * COST_MAX))

    layers = []
    for i in range(depth):
        opts = []
        for bit in (0, 1):
            option = dict(structure["layers"][i]["options"][bit])
            option.update(arithmetic[i][bit])
            opts.append(option)
        layers.append({"index": i, "options": opts})

    inst = {
        "benchmark": BENCHMARK,
        "version": VERSION,
        "seed": int(seed),
        "depth": depth,
        "attempt": int(attempt),
        "sigma": float(sigma),
        "q": float(q),
        "initial_symbol": structure["initial_symbol"],
        "initial_phase": int(structure["initial_phase"]),
        "layers": layers,
        "checksum_modulus": CHECKSUM_MODULUS,
        "checksum_target": int(anchor_checksum),
        "cost_min": int(anchor_cost - half),
        "cost_max": int(anchor_cost + half),
        "terminal_seal": seal,
        "coupling_metadata": {
            "construction": "C-MASK-ANTI" if anti else "C-MASK",
            "family_seed": int(seed),
            "accepted_attempt": int(attempt),
            "mask_permutation": list(map(int, permutation)),
            "mask_layers": sorted(map(int, mask)),
            "mask_count": len(mask),
            "free_layers": depth - len(mask),
            "backbone_bits": list(map(int, base_structure["backbone_bits"])),
            "mirror_u": [float(x) for x in base_structure["mirror_u"]],
            "penalty": int(penalty),
            "anti_coupled": bool(anti),
            "structure_stream": "seed_with_unconditional_mirror_u",
            "arithmetic_stream": "v002_seed_attempt",
            "coupling_stream": "sha256_derived_mask_permutation",
        },
        "generator_provenance": {
            "target_selection": "anti_anchor_from_declared_channel" if anti else "anchor_from_declared_channel",
            "structural_filter_consulted_for_acceptance": False,
            "survival_consulted_for_acceptance": False,
        },
    }
    inst["instance_sha256"] = sha256_obj(inst)
    return inst


def build_instance(seed: int, depth: int, sigma: float, q: float, attempt: int, anti: bool = False) -> Dict:
    base = _structure_with_mirror_u(seed, depth)
    perm = _mask_permutation(seed, depth)
    return _build_instance_from_parts(seed, depth, sigma, q, attempt, base, perm, anti=anti)


def _arithmetic_projection(instance: Mapping) -> Dict:
    return {
        "checksum_modulus": int(instance["checksum_modulus"]),
        "checksum_target": int(instance["checksum_target"]),
        "cost_min": int(instance["cost_min"]),
        "cost_max": int(instance["cost_max"]),
        "terminal_seal": int(instance["terminal_seal"]),
        "layers": [[
            {"cost": int(o["cost"]), "checksum_weight": int(o["checksum_weight"])}
            for o in layer["options"]
        ] for layer in instance["layers"]],
    }


def q0_v002_arithmetic_identity(seed: int, depth: int, attempt: int) -> bool:
    base = _structure_with_mirror_u(seed, depth)
    perm = _mask_permutation(seed, depth)
    c = _build_instance_from_parts(seed, depth, 0.0, 0.0, attempt, base, perm, anti=False)
    # v002 structure may differ for the same seed; arithmetic/target projection must be identical.
    v2_struct = {
        "initial_symbol": c["initial_symbol"],
        "initial_phase": c["initial_phase"],
        "layers": [{"index": l["index"], "options": [
            {"symbol": o["symbol"], "phase": o["phase"], "discontinuity": o["discontinuity"], "branch_id": o["branch_id"]}
            for o in l["options"]
        ]} for l in c["layers"]],
    }
    v2 = v002_merge_attempt(seed, depth, v2_struct, attempt)
    return _arithmetic_projection(c) == _arithmetic_projection(v2)


def generate_family(
    seed: int,
    depth: int,
    q_levels: Sequence[float],
    sigma_levels: Sequence[float],
    max_attempts: int = MAX_ATTEMPTS,
    m_min: int = M_MIN,
) -> Dict:
    """Generate one paired family and freeze one arithmetic attempt across every q and sigma."""
    seed = int(seed); depth = int(depth)
    q_levels = tuple(float(q) for q in q_levels)
    sigma_levels = tuple(float(s) for s in sigma_levels)
    base = _structure_with_mirror_u(seed, depth)
    perm = _mask_permutation(seed, depth)
    attempt_log = []

    for attempt in range(int(max_attempts)):
        by_q = {}
        all_ok = True
        q0_identity = q0_v002_arithmetic_identity(seed, depth, attempt)
        for q in q_levels:
            # sigma does not affect arithmetic multiplicity; use sigma=0 for acceptance only.
            inst0 = _build_instance_from_parts(seed, depth, 0.0, q, attempt, base, perm, anti=False)
            baseline = solve_baseline(inst0)
            f = depth - len(mask_for_q(perm, depth, q))
            density_free = baseline["solution_count"] / float(1 << f)
            ok = baseline["solution_count"] >= int(m_min) and DENSITY_MIN <= density_free <= DENSITY_MAX
            by_q[q_key(q)] = {
                "solution_count": int(baseline["solution_count"]),
                "density_free": float(density_free),
                "free_layers": int(f),
                "accepted": bool(ok),
            }
            all_ok = all_ok and ok
        attempt_log.append({"attempt": attempt, "q0_v002_arithmetic_identity": q0_identity, "by_q": by_q, "common_accept": all_ok})
        if not all_ok:
            continue

        instances = {}
        baselines = {}
        for q in q_levels:
            # baseline is identical across sigma; solve once on first sigma instance.
            first = _build_instance_from_parts(seed, depth, sigma_levels[0], q, attempt, base, perm, anti=False)
            baseline = solve_baseline(first)
            baselines[q_key(q)] = baseline
            for sigma in sigma_levels:
                inst = _build_instance_from_parts(seed, depth, sigma, q, attempt, base, perm, anti=False)
                instances[f"sig{sigma_key(sigma)}_q{q_key(q)}"] = inst
        return {
            "status": "ACCEPTED",
            "seed": seed,
            "depth": depth,
            "accepted_attempt": attempt,
            "q_levels": list(q_levels),
            "sigma_levels": list(sigma_levels),
            "mask_permutation": perm,
            "attempt_log": attempt_log,
            "instances": instances,
            "baselines": baselines,
        }

    return {
        "status": "INFEASIBLE_FAMILY",
        "seed": seed,
        "depth": depth,
        "q_levels": list(q_levels),
        "sigma_levels": list(sigma_levels),
        "mask_permutation": perm,
        "attempt_log": attempt_log,
        "instances": {},
        "baselines": {},
    }

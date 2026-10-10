from __future__ import annotations
import copy, math, random
from typing import Dict, List, Mapping
from grammar.route_grammar import ALPHABET, DEFAULT_TRANSITIONS
from engine_common import BENCHMARK, sha256_obj

CHECKSUM_MODULUS = 31
COST_LOW = 1
COST_HIGH = 1_000_000_000

def _valid_backbone_option(rng: random.Random, prev_symbol: str, prev_phase: int, last_disc: List[int]):
    symbol = rng.choice(DEFAULT_TRANSITIONS[prev_symbol])
    phase = (prev_phase + rng.choice((0, 1))) % 3
    may_disc = sum(last_disc[-3:]) == 0
    discontinuity = 1 if may_disc and rng.random() < 0.12 else 0
    return {
        "symbol": symbol,
        "phase": phase,
        "discontinuity": discontinuity,
    }

def _decoy_structural_option(rng: random.Random):
    return {
        "symbol": rng.choice(ALPHABET),
        "phase": rng.randrange(3),
        "discontinuity": 1 if rng.random() < 0.35 else 0,
    }

def _add_arithmetic(rng: random.Random, option: Dict, branch_id: int):
    option = dict(option)
    option["cost"] = rng.randint(COST_LOW, COST_HIGH)
    option["checksum_weight"] = rng.randrange(CHECKSUM_MODULUS)
    option["branch_id"] = int(branch_id)
    return option

def generate_instance(seed: int, depth: int) -> Dict:
    rng = random.Random(int(seed))
    depth = int(depth)
    if depth < 1:
        raise ValueError("depth must be >= 1")

    initial_symbol = rng.choice(ALPHABET)
    initial_phase = rng.randrange(3)
    prev_symbol = initial_symbol
    prev_phase = initial_phase
    last_disc: List[int] = []

    layers = []
    backbone_bits = []
    backbone_cost = 0
    backbone_checksum = 0

    for i in range(depth):
        backbone_bit = rng.randrange(2)
        backbone_bits.append(backbone_bit)

        b_struct = _valid_backbone_option(rng, prev_symbol, prev_phase, last_disc)
        d_struct = _decoy_structural_option(rng)

        opts = [None, None]
        opts[backbone_bit] = _add_arithmetic(rng, b_struct, backbone_bit)
        opts[1 - backbone_bit] = _add_arithmetic(rng, d_struct, 1 - backbone_bit)

        b = opts[backbone_bit]
        backbone_cost += int(b["cost"])
        backbone_checksum = (backbone_checksum + int(b["checksum_weight"])) % CHECKSUM_MODULUS

        prev_symbol = str(b["symbol"])
        prev_phase = int(b["phase"])
        last_disc = (last_disc + [int(b["discontinuity"])])[-3:]

        layers.append({"index": i, "options": opts})

    half_width = max(2, math.floor(0.04 * depth))
    instance = {
        "benchmark": BENCHMARK,
        "version": "v001",
        "seed": int(seed),
        "depth": depth,
        "initial_symbol": initial_symbol,
        "initial_phase": initial_phase,
        "layers": layers,
        "checksum_modulus": CHECKSUM_MODULUS,
        "checksum_target": backbone_checksum,
        "cost_min": backbone_cost - half_width,
        "cost_max": backbone_cost + half_width,
        "terminal_seal": int(backbone_bits[-1]),
        "generator_provenance": {
            "cost_range": [COST_LOW, COST_HIGH],
            "backbone_sha256": sha256_obj(backbone_bits),
            "construction": "structural_metadata_then_arithmetic_target",
        },
    }
    instance["instance_sha256"] = sha256_obj(instance)
    return instance

def structural_view(instance: Mapping) -> Dict:
    # Deliberately strips all forbidden arithmetic/solution fields.
    return {
        "depth": int(instance["depth"]),
        "initial_symbol": instance["initial_symbol"],
        "initial_phase": int(instance["initial_phase"]),
        "layers": [
            {
                "index": int(layer["index"]),
                "options": [
                    {
                        "symbol": opt["symbol"],
                        "phase": int(opt["phase"]),
                        "discontinuity": int(opt["discontinuity"]),
                        "branch_id": int(opt["branch_id"]),
                    }
                    for opt in layer["options"]
                ],
            }
            for layer in instance["layers"]
        ],
    }

def mutate_arithmetic(instance: Mapping, delta: int = 17) -> Dict:
    out = copy.deepcopy(instance)
    out["checksum_target"] = (int(out["checksum_target"]) + delta) % int(out["checksum_modulus"])
    out["cost_min"] += delta * 1000
    out["cost_max"] += delta * 1000
    out["terminal_seal"] = 1 - int(out["terminal_seal"])
    for layer in out["layers"]:
        for opt in layer["options"]:
            opt["cost"] += delta * 12345
            opt["checksum_weight"] = (int(opt["checksum_weight"]) + delta) % int(out["checksum_modulus"])
    return out

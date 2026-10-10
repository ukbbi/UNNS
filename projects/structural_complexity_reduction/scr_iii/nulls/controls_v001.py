from __future__ import annotations
from typing import Mapping
from scr_iii.compat import install_scr_ii_path
from scr_iii.generator.route_csp_c_v001 import build_instance
install_scr_ii_path()
from nulls.controls import solve_n1_random_prefix, frozen_symbol_permutations, frozen_transition_permutations, permuted_transitions


def n1_p_accept(L: int, N: int, depth: int) -> float:
    if L <= 0: return 0.0
    if L >= N: return 1.0
    return (float(L)/float(N)) ** (1.0/int(depth))


def build_n4(instance: Mapping):
    return build_instance(
        int(instance["seed"]), int(instance["depth"]), float(instance["sigma"]), float(instance["q"]),
        int(instance["attempt"]), anti=True
    )

from __future__ import annotations
import hashlib, itertools, math, random, time
from typing import Mapping
from grammar.route_grammar import ALPHABET, DEFAULT_TRANSITIONS
from solver.exact_solver import solve_scr, solution_set_sha256

def _u01(key: str) -> float:
    h = hashlib.sha256(key.encode("utf-8")).digest()
    return int.from_bytes(h[:8], "big") / 2**64

def solve_n1_random_prefix(instance: Mapping, q_accept: float, replicate_seed: int):
    depth = int(instance["depth"])
    solutions = []
    expanded = 0
    leaves = 0
    t0 = time.perf_counter()

    def ok_solution(checksum, cost, last_bit):
        return (
            checksum % int(instance["checksum_modulus"]) == int(instance["checksum_target"])
            and int(instance["cost_min"]) <= cost <= int(instance["cost_max"])
            and int(last_bit) == int(instance["terminal_seal"])
        )

    def dfs(i, checksum, cost, bits):
        nonlocal expanded, leaves
        if i == depth:
            leaves += 1
            if ok_solution(checksum, cost, int(bits[-1])):
                solutions.append(bits)
            return
        expanded += 1
        for bit in (0, 1):
            child = bits + str(bit)
            if _u01(f"{replicate_seed}:{instance['seed']}:{child}") > q_accept:
                continue
            opt = instance["layers"][i]["options"][bit]
            dfs(
                i + 1,
                (checksum + int(opt["checksum_weight"])) % int(instance["checksum_modulus"]),
                cost + int(opt["cost"]),
                child,
            )

    dfs(0, 0, 0, "")
    elapsed = time.perf_counter() - t0
    solutions.sort()
    return {
        "solutions": solutions,
        "solution_count": len(solutions),
        "solution_set_sha256": solution_set_sha256(solutions),
        "expanded_nodes": expanded,
        "leaves_checked": leaves,
        "seconds": elapsed,
    }

def frozen_symbol_permutations():
    # 12 fixed non-identity permutations, lexicographic.
    perms = []
    for p in itertools.permutations(ALPHABET):
        if tuple(p) == ALPHABET:
            continue
        perms.append(dict(zip(ALPHABET, p)))
        if len(perms) == 12:
            break
    return perms

def frozen_transition_permutations():
    # Global destination relabeling preserves every row's out-degree.
    return frozen_symbol_permutations()

def permuted_transitions(mapping):
    return {
        src: tuple(mapping[x] for x in DEFAULT_TRANSITIONS[src])
        for src in ALPHABET
    }

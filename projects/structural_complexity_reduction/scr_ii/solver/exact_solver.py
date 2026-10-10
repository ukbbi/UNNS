from __future__ import annotations
import hashlib, json, math, time
from collections import Counter
from typing import Dict, Iterable, Mapping, Optional
from grammar.route_grammar import initial_state, evaluate_gates, DEFAULT_TRANSITIONS
from generator.route_csp_i import structural_view

def _solution_ok(instance: Mapping, checksum: int, cost: int, last_bit: int) -> bool:
    return (
        checksum % int(instance["checksum_modulus"]) == int(instance["checksum_target"])
        and int(instance["cost_min"]) <= cost <= int(instance["cost_max"])
        and int(last_bit) == int(instance["terminal_seal"])
    )

def solution_set_sha256(solutions):
    payload = "\n".join(sorted(solutions)).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()

def solve_baseline(instance: Mapping) -> Dict:
    depth = int(instance["depth"])
    solutions = []
    expanded = 0
    leaves = 0
    t0 = time.perf_counter()

    def dfs(i: int, checksum: int, cost: int, bits: str):
        nonlocal expanded, leaves
        if i == depth:
            leaves += 1
            if _solution_ok(instance, checksum, cost, int(bits[-1])):
                solutions.append(bits)
            return
        expanded += 1
        for bit in (0, 1):
            opt = instance["layers"][i]["options"][bit]
            dfs(
                i + 1,
                (checksum + int(opt["checksum_weight"])) % int(instance["checksum_modulus"]),
                cost + int(opt["cost"]),
                bits + str(bit),
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

def solve_scr(instance: Mapping, transitions=None, symbol_map=None) -> Dict:
    depth = int(instance["depth"])
    view = structural_view(instance)
    tr = transitions or DEFAULT_TRANSITIONS

    if symbol_map:
        view["initial_symbol"] = symbol_map[view["initial_symbol"]]
        for layer in view["layers"]:
            for opt in layer["options"]:
                opt["symbol"] = symbol_map[opt["symbol"]]

    solutions = []
    expanded = 0
    leaves = 0
    filter_evals = 0
    filter_seconds = 0.0
    first_rejections = Counter()
    gate_evals = Counter()
    state0 = initial_state(view)
    t0 = time.perf_counter()

    def dfs(i: int, checksum: int, cost: int, bits: str, state):
        nonlocal expanded, leaves, filter_evals, filter_seconds
        if i == depth:
            leaves += 1
            if _solution_ok(instance, checksum, cost, int(bits[-1])):
                solutions.append(bits)
            return

        expanded += 1
        for bit in (0, 1):
            s0 = time.perf_counter()
            passed, fail_gate, gates, new_state = evaluate_gates(
                state, view["layers"][i]["options"][bit], depth - i - 1, tr
            )
            filter_seconds += time.perf_counter() - s0
            filter_evals += 1
            for g in gates:
                gate_evals[g] += 1
            if not passed:
                first_rejections[fail_gate] += 1
                continue

            opt = instance["layers"][i]["options"][bit]
            dfs(
                i + 1,
                (checksum + int(opt["checksum_weight"])) % int(instance["checksum_modulus"]),
                cost + int(opt["cost"]),
                bits + str(bit),
                new_state,
            )

    dfs(0, 0, 0, "", state0)
    elapsed = time.perf_counter() - t0
    solutions.sort()
    return {
        "solutions": solutions,
        "solution_count": len(solutions),
        "solution_set_sha256": solution_set_sha256(solutions),
        "expanded_nodes": expanded,
        "leaves_checked": leaves,
        "filter_evaluations": filter_evals,
        "filter_seconds": filter_seconds,
        "first_rejections": dict(first_rejections),
        "gate_evaluations": dict(gate_evals),
        "seconds": elapsed,
    }

def _suffix_arithmetic(instance: Mapping):
    d = int(instance["depth"])
    mod = int(instance["checksum_modulus"])
    min_cost = [0] * (d + 1)
    max_cost = [0] * (d + 1)
    residues = [set() for _ in range(d + 1)]
    residues[d] = {0}
    for i in range(d - 1, -1, -1):
        opts = instance["layers"][i]["options"]
        min_cost[i] = min(int(o["cost"]) for o in opts) + min_cost[i + 1]
        max_cost[i] = max(int(o["cost"]) for o in opts) + max_cost[i + 1]
        r = set()
        for o in opts:
            w = int(o["checksum_weight"])
            for tail in residues[i + 1]:
                r.add((w + tail) % mod)
        residues[i] = r
    return min_cost, max_cost, residues

def solve_solver_native(instance: Mapping) -> Dict:
    depth = int(instance["depth"])
    mod = int(instance["checksum_modulus"])
    min_cost, max_cost, residues = _suffix_arithmetic(instance)
    solutions = []
    expanded = 0
    leaves = 0
    pruned = 0
    t0 = time.perf_counter()

    def feasible(i: int, checksum: int, cost: int) -> bool:
        lo = cost + min_cost[i]
        hi = cost + max_cost[i]
        if hi < int(instance["cost_min"]) or lo > int(instance["cost_max"]):
            return False
        need = (int(instance["checksum_target"]) - checksum) % mod
        return need in residues[i]

    def dfs(i: int, checksum: int, cost: int, bits: str):
        nonlocal expanded, leaves, pruned
        if not feasible(i, checksum, cost):
            pruned += 1
            return
        if i == depth:
            leaves += 1
            if _solution_ok(instance, checksum, cost, int(bits[-1])):
                solutions.append(bits)
            return
        expanded += 1
        for bit in (0, 1):
            opt = instance["layers"][i]["options"][bit]
            dfs(
                i + 1,
                (checksum + int(opt["checksum_weight"])) % mod,
                cost + int(opt["cost"]),
                bits + str(bit),
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
        "pruned_prefixes": pruned,
        "seconds": elapsed,
    }

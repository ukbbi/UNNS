from __future__ import annotations
import random, time
from typing import Mapping, Sequence

from scr_iii.compat import install_scr_ii_path
from scr_iii.engine_common import stable_int
from scr_iii.analysis.stats_v001 import spearman
install_scr_ii_path()
from generator.route_csp_i import structural_view
from grammar.route_grammar import initial_state, evaluate_gates, DEFAULT_TRANSITIONS


def _solution_ok(instance, checksum, cost, last_bit):
    return (
        checksum % int(instance["checksum_modulus"]) == int(instance["checksum_target"])
        and int(instance["cost_min"]) <= cost <= int(instance["cost_max"])
        and int(last_bit) == int(instance["terminal_seal"])
    )


def sample_prefixes(instance: Mapping, count: int, h: int, estimator_seed: int):
    n = 1 << int(h)
    rng = random.Random(stable_int("E2", estimator_seed, instance["seed"], instance["depth"], instance.get("sigma"), instance.get("q")))
    idx = sorted(rng.sample(range(n), int(count)))
    return [format(i, f"0{h}b") for i in idx]


def solve_sampled_subtrees(instance: Mapping, prefixes: Sequence[str]):
    depth = int(instance["depth"]); h = len(prefixes[0]) if prefixes else 0
    prefix_set = set(prefixes)
    view = structural_view(instance)
    bsol = []; ssol = []
    sampled_leaves = len(prefix_set) * (1 << (depth-h))
    scr_admitted_leaves = 0
    t0 = time.perf_counter()

    def arithmetic_for_prefix(bits):
        checksum = 0; cost = 0
        for i,ch in enumerate(bits):
            bit = int(ch); o = instance["layers"][i]["options"][bit]
            checksum = (checksum + int(o["checksum_weight"])) % int(instance["checksum_modulus"])
            cost += int(o["cost"])
        return checksum, cost

    def baseline_tail(i, checksum, cost, bits):
        if i == depth:
            if _solution_ok(instance, checksum, cost, int(bits[-1])):
                bsol.append(bits)
            return
        for bit in (0,1):
            o=instance["layers"][i]["options"][bit]
            baseline_tail(i+1,(checksum+int(o["checksum_weight"]))%int(instance["checksum_modulus"]),cost+int(o["cost"]),bits+str(bit))

    def scr_tail(i, checksum, cost, bits, state):
        nonlocal scr_admitted_leaves
        if i == depth:
            scr_admitted_leaves += 1
            if _solution_ok(instance, checksum, cost, int(bits[-1])):
                ssol.append(bits)
            return
        for bit in (0,1):
            passed, _, _, ns = evaluate_gates(state, view["layers"][i]["options"][bit], depth-i-1, DEFAULT_TRANSITIONS)
            if not passed: continue
            o=instance["layers"][i]["options"][bit]
            scr_tail(i+1,(checksum+int(o["checksum_weight"]))%int(instance["checksum_modulus"]),cost+int(o["cost"]),bits+str(bit),ns)

    for prefix in prefixes:
        cs,cost = arithmetic_for_prefix(prefix)
        baseline_tail(h,cs,cost,prefix)
        # advance structural state along prefix; if rejected, SCR has zero in this subtree.
        state=initial_state(view); ok=True
        for i,ch in enumerate(prefix):
            bit=int(ch)
            passed,_,_,ns=evaluate_gates(state,view["layers"][i]["options"][bit],depth-i-1,DEFAULT_TRANSITIONS)
            if not passed:
                ok=False; break
            state=ns
        if ok:
            scr_tail(h,cs,cost,prefix,state)
    elapsed=time.perf_counter()-t0
    bset=set(bsol); sset=set(ssol); m=len(bset); inter=len(bset&sset)
    r = inter/m if m else None
    non_denom = sampled_leaves-m
    a0=(scr_admitted_leaves-inter)/non_denom if non_denom>0 else None
    ei=None if a0 is None or abs(1-a0)<1e-15 or r is None else (r-a0)/(1-a0)
    return {
        "prefix_depth": h,
        "prefix_count": len(prefixes),
        "sampled_leaves": sampled_leaves,
        "baseline_solutions": m,
        "scr_solutions": len(sset),
        "scr_admitted_leaves": scr_admitted_leaves,
        "recall_hat": r,
        "a0_hat": a0,
        "EI_hat": ei,
        "seconds": elapsed,
    }


def mae(pairs):
    vals=[abs(float(a)-float(b)) for a,b in pairs if a is not None and b is not None]
    return sum(vals)/len(vals) if vals else None

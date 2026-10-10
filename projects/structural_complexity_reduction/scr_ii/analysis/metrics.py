from __future__ import annotations
import math, statistics
from typing import Iterable, Mapping

def cell_metrics(baseline: Mapping, scr: Mapping, depth: int):
    preserve = baseline["solutions"] == scr["solutions"]
    nodes_b = int(baseline["expanded_nodes"])
    nodes_s = int(scr["expanded_nodes"])
    r_node = 1.0 - (nodes_s / nodes_b if nodes_b else 1.0)
    leaves_b = int(baseline["leaves_checked"])
    leaves_s = int(scr["leaves_checked"])
    r_leaf = 1.0 - (leaves_s / leaves_b if leaves_b else 1.0)
    t_b = float(baseline["seconds"])
    t_s = float(scr["seconds"])
    g_time = t_b / t_s if t_s > 0 else float("inf")
    b_eff_base = math.exp(math.log(max(nodes_b, 1)) / max(int(depth), 1))
    b_eff_scr = math.exp(math.log(max(nodes_s, 1)) / max(int(depth), 1))
    return {
        "solution_preserved": preserve,
        "r_node": r_node,
        "r_leaf": r_leaf,
        "g_time": g_time,
        "b_eff_baseline": b_eff_base,
        "b_eff_scr": b_eff_scr,
    }

def median(xs):
    return statistics.median(list(xs))

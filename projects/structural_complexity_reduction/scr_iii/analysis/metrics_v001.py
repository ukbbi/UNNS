from __future__ import annotations
from collections import Counter
from pathlib import Path
import gzip, json
from typing import Mapping

from scr_iii.compat import install_scr_ii_path
install_scr_ii_path()
from filter.structural_filter import walk_prefix


def preservation_metrics(instance: Mapping, baseline: Mapping, scr: Mapping, structure: Mapping, t_encode: float = 0.0, c1: Mapping | None = None) -> dict:
    bset = set(baseline["solutions"]); sset = set(scr["solutions"])
    inter = len(bset & sset)
    m = len(bset)
    L = int(structure["L"])
    N = 1 << int(instance["depth"])
    recall = inter / m if m else (1.0 if not sset else 0.0)
    leak = m - inter
    extras = len(sset - bset)
    denom_non = N - m
    a0 = (L - inter) / denom_non if denom_non > 0 else None
    if a0 is None or abs(1.0 - a0) < 1e-15:
        ei = None
    else:
        ei = (recall - a0) / (1.0 - a0)
    nodes_b = int(baseline["expanded_nodes"]); nodes_s = int(scr["expanded_nodes"])
    leaves_b = int(baseline["leaves_checked"]); leaves_s = int(scr["leaves_checked"])
    if leaves_s != L:
        raise RuntimeError(f"Structural leaf count mismatch: pre-solve L={L} solve_scr={leaves_s}")
    r_node = 1.0 - (nodes_s / nodes_b if nodes_b else 1.0)
    r_leaf = 1.0 - (leaves_s / leaves_b if leaves_b else 1.0)
    t_b = float(baseline["seconds"]); t_s = float(scr["seconds"])
    g_time = t_b / t_s if t_s > 0 else float("inf")
    g_e2e = t_b / (t_s + float(t_encode)) if (t_s + float(t_encode)) > 0 else float("inf")
    exact = bset == sset
    validity_eligible = L >= m and r_leaf >= 0.25
    if not exact:
        verdict = "PRESERVATION_FAIL"
    elif r_node < 0.25:
        verdict = "NO_MATERIAL_REDUCTION"
    elif g_time < 1.10:
        verdict = "REDUCTION_WITHOUT_NET_GAIN"
    else:
        verdict = "VALID_STRUCTURAL_REDUCTION"
    out = {
        "solution_count_baseline": m,
        "solution_count_scr": len(sset),
        "solution_recall": recall,
        "leak_count": leak,
        "extra_solution_count": extras,
        "exact_preservation": exact,
        "non_solution_admission_a0": a0,
        "excess_inclusion_EI": ei,
        "nodes_baseline": nodes_b,
        "nodes_scr": nodes_s,
        "leaves_baseline": leaves_b,
        "leaves_scr": leaves_s,
        "r_node": r_node,
        "r_leaf": r_leaf,
        "seconds_baseline": t_b,
        "seconds_scr_total": t_s,
        "filter_seconds": float(scr.get("filter_seconds", 0.0)),
        "t_encode": float(t_encode),
        "g_time": g_time,
        "g_time_end_to_end": g_e2e,
        "solution_set_sha256_baseline": baseline.get("solution_set_sha256"),
        "solution_set_sha256_scr": scr.get("solution_set_sha256"),
        "population_A": True,
        "population_V": bool(validity_eligible),
        "exact_tier_infeasible": bool(L < m),
        "cell_verdict": verdict,
    }
    if c1 is not None:
        c1_exact = list(c1["solutions"]) == list(baseline["solutions"])
        out.update({
            "c1_exact": c1_exact,
            "solution_count_c1": int(c1["solution_count"]),
            "nodes_c1": int(c1["expanded_nodes"]),
            "seconds_c1": float(c1["seconds"]),
            "c1_g_time": t_b / float(c1["seconds"]) if float(c1["seconds"]) > 0 else float("inf"),
            "solution_set_sha256_c1": c1.get("solution_set_sha256"),
        })
    return out


def write_solution_loss_ledger(path: Path, instance: Mapping, baseline: Mapping, scr: Mapping) -> dict:
    missing = sorted(set(baseline["solutions"]) - set(scr["solutions"]))
    counts = Counter()
    no_fail = 0
    path.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(path, "wt", encoding="utf-8") as f:
        for bits in missing:
            passed, fail_gate, _, _ = walk_prefix(instance, bits)
            if passed:
                fail_gate = "NO_STRUCTURAL_FAIL"
                no_fail += 1
            counts[str(fail_gate)] += 1
            f.write(json.dumps({"solution": bits, "first_failing_gate": fail_gate}, sort_keys=True) + "\n")
    return {"missing_solutions": len(missing), "first_failing_gate_counts": dict(counts), "no_structural_fail": no_fail}

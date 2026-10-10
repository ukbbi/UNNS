from __future__ import annotations

import json
import math
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
SCRII = HERE.parents[1]
sys.path.insert(0, str(SCRII))

from engine_common import safe_write_json, sha256_file
from generator.route_csp_i_v002 import generate_instance
from solver.exact_solver import solve_scr, solve_solver_native

ENGINE = "SCR_II_ENGINE_v002_PRIMARY_v001"
BENCHMARK = "ROUTE_CSP_I/v002"
PREREG = "SCR_II_PREREG_v002"

OUT = SCRII / "output" / "v002_primary"
CKPT_DIR = SCRII / "output" / "checkpoints"
FINAL = OUT / "PRIMARY_RESULT_v002.json"
FINAL_SHA = OUT / "PRIMARY_RESULT_v002.json.sha256"
PROGRESS = OUT / "RUN_PROGRESS_v002.json"
CHECKPOINT = CKPT_DIR / "SCR_II_V002_PRIMARY_checkpoint.json"
CHECKPOINT_DONE = CKPT_DIR / "SCR_II_V002_PRIMARY_checkpoint.completed.json"

def _solution_recall(base, scr):
    b = set(base["solutions"])
    s = set(scr["solutions"])
    if not b:
        return 1.0 if not s else 0.0
    return len(b & s) / len(b)

def _extra_solution_count(base, scr):
    return len(set(scr["solutions"]) - set(base["solutions"]))

def _fit_slope(records, key):
    ds = (14, 16, 18)
    ys = []
    for d in ds:
        vals = [float(r[key]) for r in records if int(r["depth"]) == d]
        ys.append(statistics.median(vals))
    logs = [math.log2(max(v, 1.0)) for v in ys]
    xm = statistics.mean(ds)
    ym = statistics.mean(logs)
    denom = sum((x - xm) ** 2 for x in ds)
    return sum((x - xm) * (y - ym) for x, y in zip(ds, logs)) / denom

def aggregate(records):
    by_depth = {d: [r for r in records if int(r["depth"]) == d] for d in (14, 16, 18)}

    preservation_failures = sum(not bool(r["solution_preserved"]) for r in records)
    if preservation_failures:
        verdict = "PRESERVATION_FAIL"
    elif any(statistics.median(r["r_node"] for r in by_depth[d]) < 0.25 for d in by_depth):
        verdict = "NO_MATERIAL_REDUCTION"
    elif statistics.median(r["g_time"] for r in by_depth[16]) < 1.10 or \
         statistics.median(r["g_time"] for r in by_depth[18]) < 1.10:
        verdict = "REDUCTION_WITHOUT_NET_GAIN"
    else:
        verdict = "COMPUTATIONAL_TRANSFER_CONFIRMED"

    alpha_base = _fit_slope(records, "nodes_baseline")
    alpha_scr = _fit_slope(records, "nodes_scr")
    delta_alpha = alpha_base - alpha_scr
    reductions = {
        str(d): statistics.median(r["r_node"] for r in by_depth[d])
        for d in by_depth
    }

    scaling_signal = (
        verdict == "COMPUTATIONAL_TRANSFER_CONFIRMED"
        and delta_alpha >= 0.05
        and reductions["18"] >= reductions["14"] - 0.05
    )
    final_verdict = "TRANSFER_WITH_SCALING_SIGNAL" if scaling_signal else verdict

    depth_summary = {}
    for d, rows in by_depth.items():
        depth_summary[str(d)] = {
            "cells": len(rows),
            "preservation_passes": sum(bool(r["solution_preserved"]) for r in rows),
            "median_solution_count_baseline": statistics.median(r["solution_count_baseline"] for r in rows),
            "median_solution_recall": statistics.median(r["solution_recall"] for r in rows),
            "min_solution_recall": min(r["solution_recall"] for r in rows),
            "median_r_node": statistics.median(r["r_node"] for r in rows),
            "median_r_leaf": statistics.median(r["r_leaf"] for r in rows),
            "median_g_time": statistics.median(r["g_time"] for r in rows),
            "median_c1_g_time_vs_baseline": statistics.median(r["c1_g_time"] for r in rows),
        }

    return {
        "primary_verdict": final_verdict,
        "base_verdict": verdict,
        "preservation_failures": preservation_failures,
        "preservation_passes": len(records) - preservation_failures,
        "median_solution_recall": statistics.median(r["solution_recall"] for r in records),
        "minimum_solution_recall": min(r["solution_recall"] for r in records),
        "maximum_solution_recall": max(r["solution_recall"] for r in records),
        "median_r_node": statistics.median(r["r_node"] for r in records),
        "median_r_leaf": statistics.median(r["r_leaf"] for r in records),
        "median_g_time": statistics.median(r["g_time"] for r in records),
        "scaling": {
            "alpha_baseline": alpha_base,
            "alpha_scr": alpha_scr,
            "delta_alpha": delta_alpha,
            "exploratory_scaling_signal": scaling_signal,
        },
        "by_depth": depth_summary,
    }

def _load_checkpoint():
    if not CHECKPOINT.exists():
        return []
    data = json.loads(CHECKPOINT.read_text(encoding="utf-8"))
    return list(data.get("records", []))

def _preflight():
    prereg = SCRII / PREREG
    required = [
        prereg / "PREREG.md",
        prereg / "SEEDS.json",
        prereg / "config" / "prereg_v002.json",
        prereg / "SHA256SUMS.txt",
        SCRII / "output" / "v002_calibration" / "CALIBRATION_v002.json",
    ]
    audit_dir = SCRII / "output" / "v002_design_audit"
    audit_files = list(audit_dir.glob("DESIGN_AUDIT_v002_PASS.json"))
    missing = [str(p.relative_to(SCRII)) for p in required if not p.exists()]
    if not audit_files:
        missing.append("output/v002_design_audit/DESIGN_AUDIT_v002_PASS.json")
    if missing:
        raise RuntimeError("Primary blocked; missing prerequisites: " + ", ".join(missing))

    cfg = json.loads((prereg / "config" / "prereg_v002.json").read_text(encoding="utf-8"))
    if cfg.get("status") != "FROZEN_BEFORE_PRIMARY":
        raise RuntimeError("Primary blocked; v002 preregistration is not frozen.")

    return {
        "preregistration": PREREG,
        "config_sha256": sha256_file(prereg / "config" / "prereg_v002.json"),
        "seeds_sha256": sha256_file(prereg / "SEEDS.json"),
        "calibration_sha256": sha256_file(SCRII / "output" / "v002_calibration" / "CALIBRATION_v002.json"),
        "design_audit_sha256": sha256_file(audit_files[0]),
    }

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    CKPT_DIR.mkdir(parents=True, exist_ok=True)

    if FINAL.exists():
        print("SCR-II v002 primary is already complete/frozen.")
        print("Rerun refused:", FINAL)
        return 2

    preflight = _preflight()
    prereg = SCRII / PREREG
    seeds = json.loads((prereg / "SEEDS.json").read_text(encoding="utf-8"))

    grid = []
    for d in (14, 16, 18):
        for seed in seeds["primary"][f"depth_{d}"]:
            grid.append((d, int(seed)))

    records = _load_checkpoint()
    done = {(int(r["depth"]), int(r["seed"])) for r in records}

    safe_write_json(PROGRESS, {
        "engine": ENGINE,
        "status": "RUNNING",
        "completed_cells": len(records),
        "total_cells": len(grid),
        "message": "SCR-II v002 primary in progress",
    })

    for idx, (depth, seed) in enumerate(grid, 1):
        if (depth, seed) in done:
            print(f"[{idx}/30] d={depth} seed={seed} already checkpointed")
            continue

        print(f"[{idx}/30] d={depth} seed={seed}: generating multiplicity-controlled instance")
        inst, baseline, attempts = generate_instance(seed, depth)

        density = baseline["solution_count"] / (1 << depth)
        if not (0.02 <= density <= 0.04):
            raise RuntimeError(f"Multiplicity band violation seed={seed} depth={depth}: {density}")

        print(f"    baseline exact solutions={baseline['solution_count']} density={density:.6f} accepted_attempt={inst['attempt']}")
        scr = solve_scr(inst)
        c1 = solve_solver_native(inst)

        preserved = (scr["solutions"] == baseline["solutions"])
        recall = _solution_recall(baseline, scr)
        extras = _extra_solution_count(baseline, scr)

        nodes_b = int(baseline["expanded_nodes"])
        nodes_s = int(scr["expanded_nodes"])
        leaves_b = int(baseline["leaves_checked"])
        leaves_s = int(scr["leaves_checked"])

        r_node = 1.0 - (nodes_s / nodes_b if nodes_b else 1.0)
        r_leaf = 1.0 - (leaves_s / leaves_b if leaves_b else 1.0)

        t_b = float(baseline["seconds"])
        t_s = float(scr["seconds"])
        g_time = t_b / t_s if t_s > 0 else float("inf")

        c1_preserved = (c1["solutions"] == baseline["solutions"])
        c1_g = t_b / float(c1["seconds"]) if float(c1["seconds"]) > 0 else float("inf")

        row = {
            "engine": ENGINE,
            "benchmark": BENCHMARK,
            "preregistration": PREREG,
            "seed": seed,
            "depth": depth,
            "instance_sha256": inst["instance_sha256"],
            "accepted_arithmetic_attempt": int(inst["attempt"]),
            "solution_density": density,
            "solution_count_baseline": int(baseline["solution_count"]),
            "solution_count_scr": int(scr["solution_count"]),
            "solution_count_c1": int(c1["solution_count"]),
            "solution_set_sha256_baseline": baseline["solution_set_sha256"],
            "solution_set_sha256_scr": scr["solution_set_sha256"],
            "solution_set_sha256_c1": c1["solution_set_sha256"],
            "solution_preserved": preserved,
            "solution_recall": recall,
            "extra_solution_count_scr": extras,
            "nodes_baseline": nodes_b,
            "nodes_scr": nodes_s,
            "nodes_c1": int(c1["expanded_nodes"]),
            "leaves_baseline": leaves_b,
            "leaves_scr": leaves_s,
            "leaves_c1": int(c1["leaves_checked"]),
            "r_node": r_node,
            "r_leaf": r_leaf,
            "seconds_baseline": t_b,
            "seconds_scr_total": t_s,
            "filter_seconds": float(scr["filter_seconds"]),
            "g_time": g_time,
            "c1_solution_preserved": c1_preserved,
            "c1_seconds": float(c1["seconds"]),
            "c1_g_time": c1_g,
            "gate_first_rejections": scr["first_rejections"],
            "gate_evaluations": scr["gate_evaluations"],
            "cell_verdict": "PRESERVED" if preserved else "PRESERVATION_FAIL",
        }

        records.append(row)
        safe_write_json(CHECKPOINT, {
            "engine": ENGINE,
            "preregistration": PREREG,
            "preflight": preflight,
            "completed_cells": len(records),
            "total_cells": 30,
            "records": records,
        })
        safe_write_json(PROGRESS, {
            "engine": ENGINE,
            "status": "RUNNING",
            "completed_cells": len(records),
            "total_cells": 30,
            "current_depth": depth,
            "current_seed": seed,
            "last_solution_recall": recall,
            "last_cell_verdict": row["cell_verdict"],
        })

        print(
            f"    SCR solutions={scr['solution_count']} recall={recall:.6f} "
            f"preserved={preserved} R_node={r_node:.4f} G_time={g_time:.3f}x"
        )

    aggregate_result = aggregate(records)
    final = {
        "engine": ENGINE,
        "benchmark": BENCHMARK,
        "preregistration": PREREG,
        "status": "COMPLETE",
        "primary_grid_cells": 30,
        "preflight": preflight,
        "aggregate": aggregate_result,
        "records": records,
        "interpretation_boundary": (
            "v002 tests transfer to an independently generated arithmetic exact-solution set. "
            "A preservation failure establishes non-transfer for this benchmark and does not invalidate SCR-I."
        ),
    }
    safe_write_json(FINAL, final)
    FINAL_SHA.write_text(sha256_file(FINAL) + "  PRIMARY_RESULT_v002.json\n", encoding="utf-8")

    safe_write_json(PROGRESS, {
        "engine": ENGINE,
        "status": "COMPLETE",
        "completed_cells": 30,
        "total_cells": 30,
        "primary_verdict": aggregate_result["primary_verdict"],
        "preservation_failures": aggregate_result["preservation_failures"],
        "median_solution_recall": aggregate_result["median_solution_recall"],
    })

    if CHECKPOINT.exists():
        try:
            CHECKPOINT.replace(CHECKPOINT_DONE)
        except PermissionError:
            # Persistence helper has already protected data; leave live checkpoint if Windows locks rename.
            pass

    print("")
    print("SCR-II v002 PRIMARY COMPLETE")
    print("VERDICT:", aggregate_result["primary_verdict"])
    print("Preservation passes:", aggregate_result["preservation_passes"], "/ 30")
    print("Median solution recall:", f"{aggregate_result['median_solution_recall']:.6f}")
    print("Median node reduction:", f"{aggregate_result['median_r_node']:.6f}")
    print("Median time gain:", f"{aggregate_result['median_g_time']:.3f}x")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations
import json, math, statistics, sys, time
from pathlib import Path
HERE=Path(__file__).resolve()
SCRII=HERE.parents[1]
sys.path.insert(0,str(SCRII))

from engine_common import safe_write_json, ENGINE_VERSION
from generator.route_csp_i import generate_instance
from solver.exact_solver import solve_baseline, solve_scr
from analysis.metrics import cell_metrics

def main():
    seeds = json.loads((SCRII/"SCR_II_PREREG_v001"/"SEEDS.json").read_text(encoding="utf-8"))
    rows=[]
    q_values=[]
    preserve_failures=0

    for depth in (8,10,12):
        for seed in seeds["calibration"][f"depth_{depth}"]:
            inst=generate_instance(seed,depth)
            b=solve_baseline(inst)
            s=solve_scr(inst)
            m=cell_metrics(b,s,depth)
            if not m["solution_preserved"]:
                preserve_failures += 1
            survival = s["leaves_checked"]/b["leaves_checked"]
            q = survival**(1.0/depth) if survival>0 else 0.0
            q_values.append(q)
            rows.append({
                "seed":seed,"depth":depth,"instance_sha256":inst["instance_sha256"],
                "baseline_solution_count":b["solution_count"],
                "scr_solution_count":s["solution_count"],
                "solution_preserved_diagnostic":m["solution_preserved"],
                "baseline_leaves":b["leaves_checked"],"scr_leaves":s["leaves_checked"],
                "leaf_survival":survival,"per_edge_acceptance_estimate":q,
                "r_node":m["r_node"],"g_time":m["g_time"],
            })
            print(f"cal d={depth} seed={seed} solutions={b['solution_count']} preserve={m['solution_preserved']} leaf_survival={survival:.6f}")

    q_accept=statistics.median(q_values)
    out={
        "engine":ENGINE_VERSION,
        "benchmark":"ROUTE_CSP_I",
        "calibration_only":True,
        "primary_seeds_inspected":False,
        "rows":rows,
        "n1_q_accept":q_accept,
        "preservation_diagnostic_failures":preserve_failures,
        "note":"Preservation diagnostics are recorded but do not tune or alter frozen grammar/thresholds."
    }
    safe_write_json(SCRII/"output"/"calibration"/"CALIBRATION_v001.json",out)
    safe_write_json(SCRII/"output"/"calibration"/"N1_RATE_v001.json",{
        "method":"median_per_edge_acceptance_from_calibration_leaf_survival",
        "q_accept":q_accept,
        "source_cells":len(rows),
        "primary_seeds_inspected":False
    })
    print(f"N1 q_accept={q_accept:.8f}")
    print(f"Calibration preservation diagnostic failures={preserve_failures}/{len(rows)}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())

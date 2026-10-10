from __future__ import annotations
import json, math, statistics, sys, time
from pathlib import Path
HERE=Path(__file__).resolve()
SCRII=HERE.parents[1]
sys.path.insert(0,str(SCRII))

from engine_common import safe_write_json, sha256_file, ENGINE_VERSION
from generator.route_csp_i import generate_instance
from solver.exact_solver import solve_baseline, solve_scr, solve_solver_native
from nulls.controls import solve_n1_random_prefix, frozen_symbol_permutations, frozen_transition_permutations, permuted_transitions
from analysis.metrics import cell_metrics

CHECKPOINT=SCRII/"output"/"checkpoints"/"SCR_II_PRIMARY_checkpoint.json"
FINAL=SCRII/"output"/"primary"/"PRIMARY_RESULT_v001.json"
PROGRESS=SCRII/"output"/"primary"/"RUN_PROGRESS_v001.json"

def aggregate_verdict(records):
    if any(not r["solution_preserved"] for r in records):
        return "PRESERVATION_FAIL"

    by_depth={}
    for d in (14,16,18):
        by_depth[d]=[r for r in records if r["depth"]==d]

    if any(statistics.median(r["r_node"] for r in by_depth[d]) < 0.25 for d in by_depth):
        return "NO_MATERIAL_REDUCTION"

    if statistics.median(r["g_time"] for r in by_depth[16]) < 1.10 or statistics.median(r["g_time"] for r in by_depth[18]) < 1.10:
        return "REDUCTION_WITHOUT_NET_GAIN"

    verdict="COMPUTATIONAL_TRANSFER_CONFIRMED"
    # Exploratory scaling: OLS slope of log2 median nodes vs depth.
    ds=[14,16,18]
    mb=[statistics.median(r["nodes_baseline"] for r in by_depth[d]) for d in ds]
    ms=[statistics.median(r["nodes_scr"] for r in by_depth[d]) for d in ds]
    def slope(ys):
        xs=ds; y=[math.log2(max(v,1)) for v in ys]
        xm=sum(xs)/3; ym=sum(y)/3
        return sum((x-xm)*(yy-ym) for x,yy in zip(xs,y))/sum((x-xm)**2 for x in xs)
    da=slope(mb)-slope(ms)
    reductions=[statistics.median(r["r_node"] for r in by_depth[d]) for d in ds]
    if da>=0.05 and reductions[-1] >= reductions[0]-0.05:
        verdict="TRANSFER_WITH_SCALING_SIGNAL"
    return verdict

def main():
    if FINAL.exists():
        print("Primary result already exists. SCR-II primary rerun is disabled.")
        return 2

    prereg=SCRII/"SCR_II_PREREG_v001"
    seeds=json.loads((prereg/"SEEDS.json").read_text(encoding="utf-8"))
    cal_path=SCRII/"output"/"calibration"/"N1_RATE_v001.json"
    audit_path=SCRII/"output"/"design_audit"/"DESIGN_AUDIT_PASS.json"
    if not cal_path.exists():
        print("BLOCKED: run RUN_SCR_II_CALIBRATION.bat first."); return 3
    if not audit_path.exists():
        print("BLOCKED: run RUN_SCR_II_AUDIT.bat first."); return 4
    q_accept=float(json.loads(cal_path.read_text(encoding="utf-8"))["q_accept"])

    records=[]
    null_rows=[]
    if CHECKPOINT.exists():
        ck=json.loads(CHECKPOINT.read_text(encoding="utf-8"))
        records=ck.get("records",[])
        null_rows=ck.get("null_rows",[])
    done={(int(r["depth"]),int(r["seed"])) for r in records}

    grid=[]
    for d in (14,16,18):
        for seed in seeds["primary"][f"depth_{d}"]:
            grid.append((d,seed))

    total=len(grid)
    for idx,(depth,seed) in enumerate(grid,1):
        if (depth,seed) in done:
            print(f"[{idx}/{total}] d={depth} seed={seed} already checkpointed")
            continue

        print(f"[{idx}/{total}] PRIMARY d={depth} seed={seed}")
        inst=generate_instance(seed,depth)
        b=solve_baseline(inst)
        s=solve_scr(inst)
        c1=solve_solver_native(inst)
        m=cell_metrics(b,s,depth)

        row={
            "engine":ENGINE_VERSION,"benchmark":"ROUTE_CSP_I","preregistration":"SCR_II_PREREG_v001",
            "seed":seed,"depth":depth,"instance_sha256":inst["instance_sha256"],
            "solution_count_baseline":b["solution_count"],"solution_count_scr":s["solution_count"],
            "solution_set_sha256_baseline":b["solution_set_sha256"],
            "solution_set_sha256_scr":s["solution_set_sha256"],
            "solution_preserved":m["solution_preserved"],
            "nodes_baseline":b["expanded_nodes"],"nodes_scr":s["expanded_nodes"],
            "leaves_baseline":b["leaves_checked"],"leaves_scr":s["leaves_checked"],
            "r_node":m["r_node"],"r_leaf":m["r_leaf"],
            "seconds_baseline":b["seconds"],"seconds_scr_total":s["seconds"],
            "filter_seconds":s["filter_seconds"],"g_time":m["g_time"],
            "b_eff_baseline":m["b_eff_baseline"],"b_eff_scr":m["b_eff_scr"],
            "gate_first_rejections":s["first_rejections"],
            "c1_solution_preserved":c1["solutions"]==b["solutions"],
            "c1_nodes":c1["expanded_nodes"],"c1_seconds":c1["seconds"],
        }

        # N1: 50 matched-budget random-prefix controls, q frozen from calibration.
        for rep in range(50):
            n=solve_n1_random_prefix(inst,q_accept,2026103001+rep)
            null_rows.append({
                "type":"N1_RANDOM_PREFIX","seed":seed,"depth":depth,"replicate":rep,
                "solution_preserved":n["solutions"]==b["solutions"],
                "nodes":n["expanded_nodes"],"leaves":n["leaves_checked"],"seconds":n["seconds"]
            })

        # N2: 12 symbol shuffles.
        for rep,mapping in enumerate(frozen_symbol_permutations()):
            n=solve_scr(inst,symbol_map=mapping)
            null_rows.append({
                "type":"N2_SYMBOL_SHUFFLE","seed":seed,"depth":depth,"replicate":rep,
                "solution_preserved":n["solutions"]==b["solutions"],
                "nodes":n["expanded_nodes"],"leaves":n["leaves_checked"],"seconds":n["seconds"]
            })

        # N3: 12 degree-preserving transition permutations.
        for rep,mapping in enumerate(frozen_transition_permutations()):
            n=solve_scr(inst,transitions=permuted_transitions(mapping))
            null_rows.append({
                "type":"N3_TRANSITION_PERMUTE","seed":seed,"depth":depth,"replicate":rep,
                "solution_preserved":n["solutions"]==b["solutions"],
                "nodes":n["expanded_nodes"],"leaves":n["leaves_checked"],"seconds":n["seconds"]
            })

        row["cell_verdict"] = (
            "PRESERVED" if row["solution_preserved"] else "PRESERVATION_FAIL"
        )
        records.append(row)
        safe_write_json(CHECKPOINT,{"engine":ENGINE_VERSION,"records":records,"null_rows":null_rows})
        safe_write_json(PROGRESS,{"status":"RUNNING","completed_cells":len(records),"total_cells":total,
                                  "current_depth":depth,"current_seed":seed})
        print(f"    solutions={b['solution_count']} preserve={row['solution_preserved']} R_node={row['r_node']:.4f} G_time={row['g_time']:.3f}")

    verdict=aggregate_verdict(records)
    final={
        "engine":ENGINE_VERSION,"benchmark":"ROUTE_CSP_I","preregistration":"SCR_II_PREREG_v001",
        "status":"COMPLETE","primary_verdict":verdict,"records":records,"null_rows":null_rows,
        "n1_q_accept":q_accept,"primary_seeds_inspected":True
    }
    safe_write_json(FINAL,final)
    safe_write_json(PROGRESS,{"status":"COMPLETE","completed_cells":len(records),"total_cells":total,
                              "primary_verdict":verdict})
    (SCRII/"output"/"primary"/"PRIMARY_RESULT_v001.json.sha256").write_text(
        sha256_file(FINAL)+"  PRIMARY_RESULT_v001.json\n",encoding="utf-8")
    if CHECKPOINT.exists():
        CHECKPOINT.rename(SCRII/"output"/"checkpoints"/"SCR_II_PRIMARY_checkpoint.completed.json")
    print("SCR-II PRIMARY COMPLETE:",verdict)
    return 0

if __name__=="__main__":
    raise SystemExit(main())

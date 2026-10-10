from pathlib import Path
import json, statistics, sys
HERE=Path(__file__).resolve()
SCRII=HERE.parents[1]
sys.path.insert(0,str(SCRII))
from engine_common import safe_write_json
from generator.route_csp_i_v002 import generate_instance
from solver.exact_solver import solve_scr

def main():
    seeds=json.loads((SCRII/"SCR_II_PREREG_v002"/"SEEDS.json").read_text(encoding="utf-8"))
    rows=[]
    for depth in (8,10,12):
        for seed in seeds["calibration"][f"depth_{depth}"]:
            inst,base,attempts=generate_instance(seed,depth)
            scr=solve_scr(inst)
            row={
                "seed":seed,"depth":depth,"accepted_attempt":inst["attempt"],
                "solution_count":base["solution_count"],
                "solution_density":base["solution_count"]/(1<<depth),
                "scr_solution_count_diagnostic":scr["solution_count"],
                "scr_exact_preservation_diagnostic":scr["solutions"]==base["solutions"],
                "primary_seed":False
            }
            rows.append(row)
            print(row)
    out={
        "status":"COMPLETE","benchmark":"ROUTE_CSP_I/v002",
        "primary_seeds_inspected":False,"rows":rows,
        "solution_count_ranges":{
            str(d):[
                min(r["solution_count"] for r in rows if r["depth"]==d),
                max(r["solution_count"] for r in rows if r["depth"]==d)
            ] for d in (8,10,12)
        },
        "preservation_diagnostic_passes":sum(r["scr_exact_preservation_diagnostic"] for r in rows)
    }
    safe_write_json(SCRII/"output"/"v002_calibration"/"CALIBRATION_v002.json",out)
    print("v002 calibration complete; primary seeds inspected: NO")
    return 0

if __name__=="__main__":
    raise SystemExit(main())

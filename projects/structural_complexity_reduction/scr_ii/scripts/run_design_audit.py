from __future__ import annotations
import json, sys
from pathlib import Path
HERE=Path(__file__).resolve()
SCRII=HERE.parents[1]
sys.path.insert(0,str(SCRII))

from engine_common import safe_write_json, sha256_obj, ENGINE_VERSION
from generator.route_csp_i import generate_instance, structural_view, mutate_arithmetic
from filter.structural_filter import structural_signature
from solver.exact_solver import solve_baseline, solve_scr, solve_solver_native

def main():
    seeds=json.loads((SCRII/"SCR_II_PREREG_v001"/"SEEDS.json").read_text(encoding="utf-8"))
    depth=json.loads((SCRII/"config"/"engine_v001.json").read_text(encoding="utf-8"))["design_audit_depth"]
    rows=[]
    ok=True
    for seed in seeds["design_audit"]:
        a=generate_instance(seed,depth)
        b=generate_instance(seed,depth)
        deterministic = a==b

        mutated=mutate_arithmetic(a)
        firewall = structural_signature(a)==structural_signature(mutated)

        base=solve_baseline(a)
        scr=solve_scr(a)
        native=solve_solver_native(a)
        native_exact = native["solutions"]==base["solutions"]

        row={
            "seed":seed,"depth":depth,"deterministic":deterministic,
            "filter_arithmetic_firewall":firewall,
            "baseline_solution_count":base["solution_count"],
            "scr_solution_count":scr["solution_count"],
            "scr_preservation_diagnostic":scr["solutions"]==base["solutions"],
            "solver_native_exact":native_exact
        }
        rows.append(row)
        ok = ok and deterministic and firewall and native_exact and base["solution_count"]>=1
        print(row)

    out={"engine":ENGINE_VERSION,"ok":ok,"primary_seeds_inspected":False,"rows":rows}
    safe_write_json(SCRII/"output"/"design_audit"/("DESIGN_AUDIT_PASS.json" if ok else "DESIGN_AUDIT_FAIL.json"),out)
    print("SCR-II design audit:", "PASS" if ok else "FAIL")
    return 0 if ok else 1

if __name__=="__main__":
    raise SystemExit(main())

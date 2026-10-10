from pathlib import Path
import copy, json, sys
HERE=Path(__file__).resolve()
SCRII=HERE.parents[1]
sys.path.insert(0,str(SCRII))
from engine_common import safe_write_json
from generator.route_csp_i_v002 import generate_instance, structural_view
from solver.exact_solver import solve_scr, solve_solver_native

def structural_digest(instance):
    import hashlib, json
    raw=json.dumps(structural_view(instance),sort_keys=True,separators=(",",":")).encode()
    return hashlib.sha256(raw).hexdigest()

def main():
    seeds=json.loads((SCRII/"SCR_II_PREREG_v002"/"SEEDS.json").read_text(encoding="utf-8"))
    rows=[]
    implementation_ok=True
    for seed in seeds["design_audit"]:
        a,base,_=generate_instance(seed,12)
        b,base2,_=generate_instance(seed,12)
        deterministic=(a==b and base["solutions"]==base2["solutions"])

        mutated=copy.deepcopy(a)
        mutated["checksum_target"]=(mutated["checksum_target"]+1)%mutated["checksum_modulus"]
        mutated["cost_min"]+=1234; mutated["cost_max"]+=1234
        mutated["terminal_seal"]=1-mutated["terminal_seal"]
        for layer in mutated["layers"]:
            for opt in layer["options"]:
                opt["cost"]+=777
                opt["checksum_weight"]=(opt["checksum_weight"]+2)%mutated["checksum_modulus"]
        firewall=(structural_digest(a)==structural_digest(mutated))

        native=solve_solver_native(a)
        native_exact=(native["solutions"]==base["solutions"])
        scr=solve_scr(a)
        density=base["solution_count"]/(1<<12)
        multiplicity_ok=(0.02<=density<=0.04)

        row={
            "seed":seed,"depth":12,"deterministic":deterministic,
            "multiplicity_ok":multiplicity_ok,
            "solution_count":base["solution_count"],
            "solution_density":density,
            "filter_arithmetic_firewall":firewall,
            "solver_native_exact":native_exact,
            "scr_solution_count_diagnostic":scr["solution_count"],
            "scr_exact_preservation_diagnostic":scr["solutions"]==base["solutions"],
            "primary_seed":False
        }
        rows.append(row)
        implementation_ok=implementation_ok and deterministic and multiplicity_ok and firewall and native_exact
        print(row)

    out={
        "implementation_audit":"PASS" if implementation_ok else "FAIL",
        "primary_seeds_inspected":False,
        "preservation_diagnostic_passes":sum(r["scr_exact_preservation_diagnostic"] for r in rows),
        "rows":rows,
        "note":"Preservation diagnostics are outcome-bearing design diagnostics but are forbidden from tuning the frozen v002 benchmark."
    }
    name="DESIGN_AUDIT_v002_PASS.json" if implementation_ok else "DESIGN_AUDIT_v002_FAIL.json"
    safe_write_json(SCRII/"output"/"v002_design_audit"/name,out)
    print("SCR-II v002 implementation audit:",out["implementation_audit"])
    print("SCR exact-preservation diagnostic passes:",out["preservation_diagnostic_passes"],"/",len(rows))
    return 0 if implementation_ok else 1

if __name__=="__main__":
    raise SystemExit(main())

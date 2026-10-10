from __future__ import annotations
import json, time

from scr_iii.compat import install_scr_ii_path
from scr_iii.engine_common import safe_write_json, write_json_gz, cell_id, sha256_file
from scr_iii.engine_v002_common import output_root_v002, scr_iii_root, load_seeds_v002, Q_LEVELS_V002, SIGMA_LEVELS_V002, PRIMARY_DEPTHS_V002, MAX_ATTEMPTS_V002
from scr_iii.generator.route_csp_c_v001 import generate_family, build_instance
from scr_iii.analysis.structure_stats_v001 import structure_stats
from scr_iii.analysis.metrics_v001 import preservation_metrics, write_solution_loss_ledger
install_scr_ii_path()
from solver.exact_solver import solve_scr, solve_solver_native, solve_baseline
from generator.route_csp_i import structural_view
from generator.route_csp_i_v002 import generate_instance as generate_v002


def main_cell(inst, baseline, outroot):
    t0=time.perf_counter(); structural_view(inst); tenc=time.perf_counter()-t0
    st=structure_stats(inst); scr=solve_scr(inst); c1=solve_solver_native(inst)
    m=preservation_metrics(inst,baseline,scr,st,tenc,c1)
    cid=cell_id(inst["depth"],inst["seed"],inst["sigma"],inst["q"])
    ip=outroot/"instances"/f"{cid}.json.gz"; write_json_gz(ip,inst)
    lp=outroot/"loss_ledger"/f"{cid}.jsonl.gz"; ledger=write_solution_loss_ledger(lp,inst,baseline,scr)
    return {"engine":"SCR_III_ENGINE_v002","benchmark":"ROUTE_CSP_C/v001","cell_id":cid,"seed":int(inst["seed"]),"depth":int(inst["depth"]),"sigma":float(inst["sigma"]),"q":float(inst["q"]),"attempt":int(inst["attempt"]),"instance_sha256":inst["instance_sha256"],**st,**m,"loss_ledger":ledger,"instance_path":str(ip.relative_to(scr_iii_root())).replace("\\","/"),"loss_ledger_path":str(lp.relative_to(scr_iii_root())).replace("\\","/")}


def main():
    root=output_root_v002(); out=root/"primary"; out.mkdir(parents=True,exist_ok=True)
    ad=root/"audit"; freeze_path=ad/"AUDIT_FREEZE_v002.json"
    if not freeze_path.exists():
        print("v002 primary blocked: AUDIT_FREEZE_v002.json absent. Review PASS audit, then run RUN_SCR_III_V002_FREEZE_AUDIT.bat."); return 2
    freeze=json.loads(freeze_path.read_text(encoding="utf-8")); ar=ad/freeze["audit_result"]; ap=ad/"AUDIT_PASS_v002.json"
    if not ar.exists() or not ap.exists() or sha256_file(ar)!=freeze["audit_result_sha256"] or sha256_file(ap)!=freeze["audit_pass_sha256"]:
        print("v002 primary blocked: audit files changed after freeze."); return 2
    final=out/"PRIMARY_RESULT_v002.json"
    if final.exists(): print("v002 primary already complete; rerun refused:",final); return 2
    seeds=load_seeds_v002(); checkpoint=out/"PRIMARY_CHECKPOINT_v002.json"
    state=json.loads(checkpoint.read_text(encoding="utf-8")) if checkpoint.exists() else {"completed_families":[],"accepted_families":[],"main_cells":[],"A0":[],"Z0":[],"infeasible_families":[]}
    done=set(state["completed_families"])
    for depth in PRIMARY_DEPTHS_V002:
        for seed in seeds["primary"][f"depth_{depth}"]:
            famkey=f"d{depth}_s{seed}"
            if famkey in done: continue
            print(f"PRIMARY v002 {famkey}: generating paired family")
            fam=generate_family(seed,depth,Q_LEVELS_V002,SIGMA_LEVELS_V002,max_attempts=MAX_ATTEMPTS_V002)
            try:
                a0,b0,_=generate_v002(seed,depth); sa0=solve_scr(a0); c10=solve_solver_native(a0)
                state["A0"].append({"depth":depth,"seed":int(seed),"m":b0["solution_count"],"L":sa0["leaves_checked"],"exact":sa0["solutions"]==b0["solutions"],"c1_exact":c10["solutions"]==b0["solutions"]})
            except Exception as e:
                state["A0"].append({"depth":depth,"seed":int(seed),"error":str(e)})
            if fam["status"]!="ACCEPTED":
                state["infeasible_families"].append({"depth":depth,"seed":int(seed),"attempts_examined":len(fam["attempt_log"])})
                state["completed_families"].append(famkey); safe_write_json(checkpoint,state); continue
            state["accepted_families"].append({"depth":depth,"seed":int(seed),"accepted_attempt":int(fam["accepted_attempt"])})
            att=int(fam["accepted_attempt"])
            z=build_instance(seed,depth,1.0,0.0,att); bz=solve_baseline(z); sz=solve_scr(z); stz=structure_stats(z); c1z=solve_solver_native(z); mz=preservation_metrics(z,bz,sz,stz,0.0,c1z)
            state["Z0"].append({"depth":depth,"seed":int(seed),"attempt":att,**stz,**mz})
            for sigma in SIGMA_LEVELS_V002:
                for q in Q_LEVELS_V002:
                    inst=fam["instances"][f"sig{sigma:.1f}_q{q:.1f}"]; base=fam["baselines"][f"{q:.1f}"]
                    row=main_cell(inst,base,out); state["main_cells"].append(row)
                    print(f"  sig={sigma:.1f} q={q:.1f} C={row.get('coverage_C')} recall={row['solution_recall']:.4f} exact={row['exact_preservation']} Rnode={row['r_node']:.4f} G={row['g_time']:.3f}")
            state["completed_families"].append(famkey); safe_write_json(checkpoint,state)
    result={"engine":"SCR_III_ENGINE_v002","benchmark":"ROUTE_CSP_C/v001","status":"COMPLETE","planned_main_cells":900,"generated_main_cells":len(state["main_cells"]),"accepted_families":state["accepted_families"],"infeasible_families":state["infeasible_families"],"main_cells":state["main_cells"],"A0":state["A0"],"Z0":state["Z0"]}
    safe_write_json(final,result); safe_write_json(out/"PRIMARY_COMPLETE_v002.json",{"status":"COMPLETE","generated_main_cells":len(state["main_cells"]),"accepted_family_count":len(state["accepted_families"]),"infeasible_family_count":len(state["infeasible_families"])})
    print("SCR-III v002 primary COMPLETE. Main cells:",len(state["main_cells"])); return 0

if __name__=="__main__": raise SystemExit(main())

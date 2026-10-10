from __future__ import annotations
import json, time
from pathlib import Path
from scr_iii.compat import install_scr_ii_path
from scr_iii.engine_common import scr_iii_root, safe_write_json, write_json_gz, cell_id, sha256_file
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
    cid=cell_id(inst['depth'],inst['seed'],inst['sigma'],inst['q'])
    ip=outroot/'instances'/f'{cid}.json.gz'; write_json_gz(ip,inst)
    lp=outroot/'loss_ledger'/f'{cid}.jsonl.gz'; ledger=write_solution_loss_ledger(lp,inst,baseline,scr)
    row={"engine":"SCR_III_ENGINE_v001","benchmark":"ROUTE_CSP_C/v001","cell_id":cid,"seed":int(inst['seed']),"depth":int(inst['depth']),"sigma":float(inst['sigma']),"q":float(inst['q']),"attempt":int(inst['attempt']),"instance_sha256":inst['instance_sha256'],**st,**m,"loss_ledger":ledger,"instance_path":str(ip.relative_to(scr_iii_root())).replace('\\','/'),"loss_ledger_path":str(lp.relative_to(scr_iii_root())).replace('\\','/')}
    return row


def main():
    s3=scr_iii_root(); out=s3/'output'/'primary'; out.mkdir(parents=True,exist_ok=True)
    audit_dir=s3/'output'/'audit'; freeze_path=audit_dir/'AUDIT_FREEZE_v001.json'
    if not freeze_path.exists():
        print('Primary blocked: AUDIT_FREEZE_v001.json is absent. Run RUN_SCR_III_FREEZE_AUDIT.bat after reviewing the PASS audit.'); return 2
    freeze=json.loads(freeze_path.read_text())
    ar=audit_dir/freeze['audit_result']; ap=audit_dir/'AUDIT_PASS_v001.json'
    if not ar.exists() or not ap.exists() or sha256_file(ar)!=freeze['audit_result_sha256'] or sha256_file(ap)!=freeze['audit_pass_sha256']:
        print('Primary blocked: audit files changed after freeze.'); return 2
    final=out/'PRIMARY_RESULT_v001.json'
    if final.exists():
        print('Primary already complete; rerun refused:',final); return 2
    seeds=json.loads((s3/'SCR_III_PREREG_v001'/'SEEDS_v001.json').read_text())
    cfg=json.loads((s3/'SCR_III_PREREG_v001'/'config'/'prereg_v001.json').read_text())
    checkpoint=out/'PRIMARY_CHECKPOINT_v001.json'
    state=json.loads(checkpoint.read_text()) if checkpoint.exists() else {"completed_families":[],"main_cells":[],"A0":[],"Z0":[],"infeasible_families":[]}
    done=set(state['completed_families'])
    for depth in cfg['primary_depths']:
        for seed in seeds['primary'][f'depth_{depth}']:
            famkey=f'd{depth}_s{seed}'
            if famkey in done: continue
            print(f'PRIMARY {famkey}: generating paired family')
            fam=generate_family(seed,depth,cfg['q_primary'],cfg['sigma_main'])
            # A0 always attempted independently.
            try:
                a0,b0,_=generate_v002(seed,depth); sa0=solve_scr(a0); c10=solve_solver_native(a0)
                state['A0'].append({"depth":depth,"seed":seed,"m":b0['solution_count'],"L":sa0['leaves_checked'],"exact":sa0['solutions']==b0['solutions'],"c1_exact":c10['solutions']==b0['solutions']})
            except Exception as e:
                state['A0'].append({"depth":depth,"seed":seed,"error":str(e)})
            if fam['status']!='ACCEPTED':
                state['infeasible_families'].append({"depth":depth,"seed":seed,"attempts_examined":len(fam['attempt_log'])})
                state['completed_families'].append(famkey); safe_write_json(checkpoint,state); continue
            att=int(fam['accepted_attempt'])
            # Z0 paired anchor
            z=build_instance(seed,depth,1.0,0.0,att); bz=solve_baseline(z); sz=solve_scr(z); stz=structure_stats(z); c1z=solve_solver_native(z)
            mz=preservation_metrics(z,bz,sz,stz,0.0,c1z)
            state['Z0'].append({"depth":depth,"seed":seed,"attempt":att,**stz,**mz})
            for sigma in cfg['sigma_main']:
                for q in cfg['q_primary']:
                    inst=fam['instances'][f'sig{sigma:.1f}_q{q:.1f}']; base=fam['baselines'][f'{q:.1f}']
                    row=main_cell(inst,base,out); state['main_cells'].append(row)
                    print(f"  sig={sigma:.1f} q={q:.1f} recall={row['solution_recall']:.4f} exact={row['exact_preservation']} Rnode={row['r_node']:.4f} G={row['g_time']:.3f}")
            state['completed_families'].append(famkey); safe_write_json(checkpoint,state)
    result={"engine":"SCR_III_ENGINE_v001","benchmark":"ROUTE_CSP_C/v001","status":"COMPLETE","planned_main_cells":600,"generated_main_cells":len(state['main_cells']),"infeasible_families":state['infeasible_families'],"main_cells":state['main_cells'],"A0":state['A0'],"Z0":state['Z0']}
    safe_write_json(final,result)
    safe_write_json(out/'PRIMARY_COMPLETE_v001.json',{"status":"COMPLETE","generated_main_cells":len(state['main_cells']),"infeasible_family_count":len(state['infeasible_families'])})
    print('SCR-III primary COMPLETE. Main cells:',len(state['main_cells']))
    return 0
if __name__=='__main__': raise SystemExit(main())

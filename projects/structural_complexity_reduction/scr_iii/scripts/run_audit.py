from __future__ import annotations
import json, math, statistics, sys, time
from pathlib import Path
from scr_iii.compat import install_scr_ii_path
from scr_iii.engine_common import scr_iii_root, safe_write_json, cell_id, stable_int
from scr_iii.generator.route_csp_c_v001 import generate_family, build_instance, q0_v002_arithmetic_identity
from scr_iii.analysis.structure_stats_v001 import structure_stats
from scr_iii.analysis.metrics_v001 import preservation_metrics
from scr_iii.analysis.trend_test_v001 import blocked_permutation_trend
from scr_iii.nulls.controls_v001 import build_n4
install_scr_ii_path()
from solver.exact_solver import solve_scr, solve_solver_native, solve_baseline
from generator.route_csp_i import structural_view
from generator.route_csp_i_v002 import generate_instance as generate_v002


def _cell(inst, baseline):
    t0=time.perf_counter(); structural_view(inst); tenc=time.perf_counter()-t0
    st=structure_stats(inst); scr=solve_scr(inst); c1=solve_solver_native(inst)
    m=preservation_metrics(inst,baseline,scr,st,tenc,c1)
    return {**m,**st,"seed":int(inst['seed']),"depth":int(inst['depth']),"sigma":float(inst['sigma']),"q":float(inst['q']),"attempt":int(inst['attempt']),"instance_sha256":inst['instance_sha256']}


def main():
    s3=scr_iii_root(); out=s3/'output'/'audit'; pre=out/'PREFLIGHT_PASS_v001.json'
    if not pre.exists():
        print('Audit blocked: run RUN_SCR_III_VALIDATE.bat first.'); return 2
    seeds=json.loads((s3/'SCR_III_PREREG_v001'/'SEEDS_v001.json').read_text())
    cfg=json.loads((s3/'SCR_III_PREREG_v001'/'config'/'prereg_v001.json').read_text())
    rows=[]; family_rows=[]; n4_eis=[]; z0_rows=[]; a0_rows=[]; q0_identity_all=True
    for depth in (10,12):
        qs=cfg['audit_q'][str(depth)]
        for seed in seeds['audit'][f'depth_{depth}']:
            fam=generate_family(seed,depth,qs,cfg['sigma_main'])
            family_rows.append({"depth":depth,"seed":seed,"status":fam['status'],"accepted_attempt":fam.get('accepted_attempt'),"attempts_examined":len(fam['attempt_log'])})
            q0_identity_all=q0_identity_all and all(x['q0_v002_arithmetic_identity'] for x in fam['attempt_log'])
            # independent A0 anchor, even if C-MASK family infeasible
            try:
                a0,base0,_=generate_v002(seed,depth); s0=solve_scr(a0)
                a0_rows.append({"depth":depth,"seed":seed,"L":s0['leaves_checked'],"m":base0['solution_count'],"exact":s0['solutions']==base0['solutions']})
            except Exception as e:
                a0_rows.append({"depth":depth,"seed":seed,"error":str(e)})
            if fam['status']!='ACCEPTED': continue
            att=int(fam['accepted_attempt'])
            # Z0 once per family
            z=build_instance(seed,depth,1.0,0.0,att); bz=solve_baseline(z); sz=solve_scr(z)
            z0_rows.append({"depth":depth,"seed":seed,"exact":sz['solutions']==bz['solutions'],"L":sz['leaves_checked'],"N":1<<depth})
            for sigma in cfg['sigma_main']:
                for q in qs:
                    inst=fam['instances'][f"sig{sigma:.1f}_q{q:.1f}"]; base=fam['baselines'][f"{q:.1f}"]
                    row=_cell(inst,base); rows.append(row)
                    n4=build_n4(inst); bn4=solve_baseline(n4); sn4=solve_scr(n4); st4=structure_stats(n4)
                    mn4=preservation_metrics(n4,bn4,sn4,st4,0.0,None)
                    if mn4['excess_inclusion_EI'] is not None: n4_eis.append(mn4['excess_inclusion_EI'])
    # Gates
    pg={}
    pg['PG1']={"pass":q0_identity_all,"detail":"q=0 arithmetic/target projection identical to frozen v002 for every examined attempt; preflight source lock already passed"}
    pg2_pass=q0_identity_all and all('error' not in x for x in a0_rows)
    pg['PG2']={"pass":pg2_pass,"detail":"deterministic q=0 arithmetic identity is stronger than equivalence in law"}
    acceptance={}
    for d in (10,12):
        rs=[r for r in family_rows if r['depth']==d]; rate=sum(r['status']=='ACCEPTED' for r in rs)/len(rs)
        acceptance[str(d)]=rate
    pg['PG3']={"pass":all(v>=0.5 for v in acceptance.values()),"acceptance_by_depth":acceptance,"closure":False}
    feasibility={}; pg4=True
    for sigma in cfg['sigma_main']:
        best=0.0; detail={}
        for q in sorted(set(r['q'] for r in rows if r['sigma']==sigma)):
            vals=[r for r in rows if r['sigma']==sigma and r['q']==q]
            rate=sum(r['L']>=r['solution_count_baseline'] for r in vals)/len(vals) if vals else 0.0
            detail[f"{q:.1f}"]=rate; best=max(best,rate)
        feasibility[f"{sigma:.1f}"]=detail; pg4=pg4 and best>=0.9
    pg['PG4']={"pass":pg4,"feasibility":feasibility,"closure":False}
    trend={}; pg5=True
    trend_seed=int(seeds['trend_permutation_seed'])
    for d in (10,12):
        for sigma in cfg['sigma_main']:
            panel=[r for r in rows if r['depth']==d and r['sigma']==sigma]
            res=blocked_permutation_trend(panel,100000,stable_int(trend_seed,d,sigma)); trend[f"d{d}_sig{sigma:.1f}"]=res
            pg5=pg5 and res['p_one_sided']<0.10 and res['statistic_T']>0
    pg['PG5']={"pass":pg5,"panels":trend}
    med_n4=statistics.median(n4_eis) if n4_eis else None
    pg['PG6']={"pass":med_n4 is not None and med_n4<=0,"median_EI":med_n4}
    pg['PG7']={"pass":bool(z0_rows) and all(r['exact'] and r['L']==r['N'] for r in z0_rows),"cells":len(z0_rows)}
    pg['PG8']={"pass":bool(rows) and all(r.get('c1_exact') for r in rows),"cells":len(rows)}
    cond_means=[]
    for d in (10,12):
        for sigma in cfg['sigma_main']:
            for q in cfg['audit_q'][str(d)]:
                vals=[r['solution_recall'] for r in rows if r['depth']==d and r['sigma']==sigma and r['q']==q]
                if vals: cond_means.append(sum(vals)/len(vals))
    pg['PG9']={"pass":any(0.1<x<0.9 for x in cond_means),"condition_mean_recall":cond_means}
    closure_fail=[]
    for g in ('PG1','PG2','PG5','PG6','PG7','PG8','PG9'):
        if not pg[g]['pass']: closure_fail.append(g)
    status='PASS' if not closure_fail else 'CLOSED_PRE_PRIMARY'
    result={"engine":"SCR_III_ENGINE_v001","stage":"AUDIT","status":status,"closure_failures":closure_fail,"gates":pg,"families":family_rows,"main_cells":rows,"A0":a0_rows,"Z0":z0_rows,"n4_median_EI":med_n4}
    safe_write_json(out/'AUDIT_RESULT_v001.json',result)
    if status=='PASS':
        safe_write_json(out/'AUDIT_PASS_v001.json',{"engine":"SCR_III_ENGINE_v001","status":"PASS","audit_result":"AUDIT_RESULT_v001.json","gates":pg})
        print('SCR-III audit: PASS'); return 0
    print('SCR-III audit CLOSED_PRE_PRIMARY:',','.join(closure_fail)); return 3
if __name__=='__main__': raise SystemExit(main())

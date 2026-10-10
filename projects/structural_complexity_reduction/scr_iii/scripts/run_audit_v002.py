from __future__ import annotations
import statistics, time

from scr_iii.compat import install_scr_ii_path
from scr_iii.engine_common import safe_write_json, stable_int, sha256_file
from scr_iii.engine_v002_common import (
    output_root_v002, load_seeds_v002, Q_LEVELS_V002, SIGMA_LEVELS_V002,
    AUDIT_DEPTH_V002, MAX_ATTEMPTS_V002, N_DOSE_MIN_V002,
)
from scr_iii.generator.route_csp_c_v001 import generate_family, build_instance
from scr_iii.analysis.structure_stats_v001 import structure_stats
from scr_iii.analysis.metrics_v001 import preservation_metrics
from scr_iii.analysis.trend_test_v002 import blocked_permutation_coverage_trend
from scr_iii.nulls.controls_v001 import build_n4
install_scr_ii_path()
from solver.exact_solver import solve_scr, solve_solver_native, solve_baseline
from generator.route_csp_i import structural_view
from generator.route_csp_i_v002 import generate_instance as generate_v002


def _cell(inst, baseline, st=None):
    t0 = time.perf_counter(); structural_view(inst); tenc = time.perf_counter() - t0
    st = st if st is not None else structure_stats(inst)
    scr = solve_scr(inst); c1 = solve_solver_native(inst)
    m = preservation_metrics(inst, baseline, scr, st, tenc, c1)
    return {**m, **st, "seed": int(inst["seed"]), "depth": int(inst["depth"]), "sigma": float(inst["sigma"]), "q": float(inst["q"]), "attempt": int(inst["attempt"]), "instance_sha256": inst["instance_sha256"]}


def main():
    out = output_root_v002() / "audit"; out.mkdir(parents=True, exist_ok=True)
    pre = output_root_v002() / "preflight" / "ENGINE_PREFLIGHT_PASS_v002.json"
    acc = output_root_v002() / "preflight" / "ACCEPTANCE_PREFLIGHT_v002.json"
    if not pre.exists() or not acc.exists():
        print("Audit blocked: validation and acceptance preflight must both be complete.")
        return 2
    final = out / "AUDIT_RESULT_v002.json"
    if final.exists():
        print("v002 audit already complete; rerun refused:", final)
        return 2
    seeds = load_seeds_v002()
    depth = AUDIT_DEPTH_V002
    rows=[]; family_rows=[]; z0_rows=[]; a0_rows=[]; n4_eis=[]; q0_identity_all=True
    dose_meta = {f"{s:.1f}": {} for s in SIGMA_LEVELS_V002}

    for seed in seeds["audit"]["depth_14"]:
        fam = generate_family(seed, depth, Q_LEVELS_V002, SIGMA_LEVELS_V002, max_attempts=MAX_ATTEMPTS_V002)
        family_rows.append({"depth":depth,"seed":int(seed),"status":fam["status"],"accepted_attempt":fam.get("accepted_attempt"),"attempts_examined":len(fam["attempt_log"])})
        q0_identity_all = q0_identity_all and all(x["q0_v002_arithmetic_identity"] for x in fam["attempt_log"])
        try:
            a0, b0, _ = generate_v002(seed, depth); s0=solve_scr(a0)
            a0_rows.append({"depth":depth,"seed":int(seed),"L":s0["leaves_checked"],"m":b0["solution_count"],"exact":s0["solutions"]==b0["solutions"]})
        except Exception as e:
            a0_rows.append({"depth":depth,"seed":int(seed),"error":str(e)})
        if fam["status"] != "ACCEPTED":
            print(f"AUDIT seed={seed}: INFEASIBLE_FAMILY")
            continue
        att=int(fam["accepted_attempt"])
        z=build_instance(seed,depth,1.0,0.0,att); bz=solve_baseline(z); sz=solve_scr(z)
        z0_rows.append({"depth":depth,"seed":int(seed),"exact":sz["solutions"]==bz["solutions"],"L":sz["leaves_checked"],"N":1<<depth})

        # Compute structure-only dose delivery BEFORE target-survival cells are solved.
        pre_stats = {}
        for sigma in SIGMA_LEVELS_V002:
            vals=[]
            for q in Q_LEVELS_V002:
                inst=fam["instances"][f"sig{sigma:.1f}_q{q:.1f}"]
                st=structure_stats(inst); pre_stats[(sigma,q)] = st
                c=st.get("coverage_C")
                vals.append(0.0 if c is None else float(c))
            dose_meta[f"{sigma:.1f}"][str(seed)] = {"dose_delivered": max(vals)>0.0, "coverage_by_q": {f"{q:.1f}": vals[j] for j,q in enumerate(Q_LEVELS_V002)}}

        for sigma in SIGMA_LEVELS_V002:
            for q in Q_LEVELS_V002:
                inst=fam["instances"][f"sig{sigma:.1f}_q{q:.1f}"]; base=fam["baselines"][f"{q:.1f}"]
                row=_cell(inst,base,pre_stats[(sigma,q)]); rows.append(row)
                n4=build_n4(inst); bn4=solve_baseline(n4); sn4=solve_scr(n4); st4=structure_stats(n4)
                mn4=preservation_metrics(n4,bn4,sn4,st4,0.0,None)
                if mn4["excess_inclusion_EI"] is not None: n4_eis.append(mn4["excess_inclusion_EI"])
        print(f"AUDIT seed={seed}: ACCEPTED attempt={att}")

    pg={}
    pg["PG1"]={"pass":q0_identity_all,"detail":"q=0 arithmetic/target projection identity retained; source lock passed in validation"}
    pg["PG2"]={"pass":q0_identity_all and all("error" not in x for x in a0_rows),"detail":"A0 generated without error; q=0 arithmetic identity retained"}
    rate=sum(r["status"]=="ACCEPTED" for r in family_rows)/len(family_rows)
    pg["PG3"]={"pass":rate>=0.5,"acceptance_by_depth":{"14":rate},"closure":False}
    feasibility={}; pg4=True
    for sigma in SIGMA_LEVELS_V002:
        best=0.0; detail={}
        for q in Q_LEVELS_V002:
            vals=[r for r in rows if r["sigma"]==sigma and r["q"]==q]
            rr=sum(r["L"]>=r["solution_count_baseline"] for r in vals)/len(vals) if vals else 0.0
            detail[f"{q:.1f}"]=rr; best=max(best,rr)
        feasibility[f"{sigma:.1f}"]=detail; pg4=pg4 and best>=0.9
    pg["PG4"]={"pass":pg4,"feasibility":feasibility,"closure":False}

    dose_counts={}; informative={}
    for sigma in SIGMA_LEVELS_V002:
        k=f"{sigma:.1f}"
        n=sum(1 for x in dose_meta[k].values() if x["dose_delivered"])
        dose_counts[k]=n; informative[k]=n>=N_DOSE_MIN_V002
    pg["PG5a"]={"pass":all(informative.values()),"n_dose_min":N_DOSE_MIN_V002,"dose_delivered_accepted_families":dose_counts,"informative":informative}

    trend={}; pg5=True
    trend_seed=int(seeds["analysis_rng"]["audit_trend_permutation_seed"])
    for sigma in SIGMA_LEVELS_V002:
        k=f"{sigma:.1f}"
        delivered={int(seed) for seed,x in dose_meta[k].items() if x["dose_delivered"]}
        panel=[r for r in rows if r["sigma"]==sigma and int(r["seed"]) in delivered]
        if not informative[k]:
            trend[f"d14_sig{k}"]={"status":"PANEL_DOSE_UNRESOLVED","dose_families":len(delivered)}; pg5=False; continue
        res=blocked_permutation_coverage_trend(panel,100000,stable_int(trend_seed,depth,sigma,"C"))
        res["dose_families"]=len(delivered); trend[f"d14_sig{k}"]=res
        pg5=pg5 and res["p_one_sided"]<0.10 and res["statistic_T_C"]>0
    pg["PG5"]={"pass":pg5 and pg["PG5a"]["pass"],"panels":trend}

    med_n4=statistics.median(n4_eis) if n4_eis else None
    pg["PG6"]={"pass":med_n4 is not None and med_n4<=0,"median_EI":med_n4}
    pg["PG7"]={"pass":bool(z0_rows) and all(r["exact"] and r["L"]==r["N"] for r in z0_rows),"cells":len(z0_rows)}
    pg["PG8"]={"pass":bool(rows) and all(r.get("c1_exact") for r in rows),"cells":len(rows)}
    cond_means=[]
    for sigma in SIGMA_LEVELS_V002:
        for q in Q_LEVELS_V002:
            vals=[r["solution_recall"] for r in rows if r["sigma"]==sigma and r["q"]==q]
            if vals: cond_means.append(sum(vals)/len(vals))
    pg["PG9"]={"pass":any(0.1<x<0.9 for x in cond_means),"condition_mean_recall":cond_means}

    closure=[]
    for g in ("PG1","PG2","PG6","PG7","PG8","PG9"):
        if not pg[g]["pass"]: closure.append(g)
    if not pg["PG5a"]["pass"]:
        closure.append("DOSE_NOT_RESOLVED")
    elif not pg["PG5"]["pass"]:
        closure.append("COUPLING_NOT_INDUCED")
    status="PASS" if not closure else "CLOSED_PRE_PRIMARY"
    result={
        "engine":"SCR_III_ENGINE_v002","stage":"AUDIT_V002","status":status,"closure_failures":closure,
        "gates":pg,"families":family_rows,"dose_delivery":dose_meta,"main_cells":rows,"A0":a0_rows,"Z0":z0_rows,
        "n4_median_EI":med_n4,
        "acceptance_preflight_sha256":sha256_file(acc),
    }
    safe_write_json(final,result)
    if status=="PASS":
        safe_write_json(out/"AUDIT_PASS_v002.json",{"engine":"SCR_III_ENGINE_v002","status":"PASS","audit_result":"AUDIT_RESULT_v002.json","gates":pg})
        print("SCR-III v002 audit: PASS")
        return 0
    print("SCR-III v002 audit CLOSED_PRE_PRIMARY:", ",".join(closure))
    return 3

if __name__=="__main__":
    raise SystemExit(main())

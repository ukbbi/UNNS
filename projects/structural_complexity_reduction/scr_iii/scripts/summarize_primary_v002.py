from __future__ import annotations
import json, statistics
from scr_iii.engine_v002_common import output_root_v002, load_seeds_v002, SIGMA_LEVELS_V002, Q_LEVELS_V002, N_DOSE_MIN_V002, N_ACC_MIN_V002
from scr_iii.engine_common import safe_write_json, stable_int
from scr_iii.analysis.trend_test_v002 import blocked_permutation_coverage_trend
from scr_iii.analysis.stats_v001 import holm_adjust, spearman, clopper_pearson


def _dose_seed_set(rows, depth, sigma):
    seeds=sorted(set(int(r["seed"]) for r in rows if int(r["depth"])==depth and float(r["sigma"])==sigma))
    out=set()
    for seed in seeds:
        vals=[]
        for r in rows:
            if int(r["depth"])==depth and float(r["sigma"])==sigma and int(r["seed"])==seed:
                c=r.get("coverage_C"); vals.append(0.0 if c is None else float(c))
        if vals and max(vals)>0: out.add(seed)
    return out


def main():
    root=output_root_v002(); pp=root/"primary"/"PRIMARY_RESULT_v002.json"; np=root/"nulls"/"NULL_RESULT_v002.json"; ep=root/"estimators"/"ESTIMATOR_RESULT_v002.json"
    missing=[p.name for p in (pp,np,ep) if not p.exists()]
    if missing: print("v002 summary blocked; missing:",", ".join(missing)); return 2
    primary=json.loads(pp.read_text(encoding="utf-8")); nulls=json.loads(np.read_text(encoding="utf-8")); est=json.loads(ep.read_text(encoding="utf-8")); seeds=load_seeds_v002(); rows=primary["main_cells"]
    panels=[]; rawp=[]; informative_indices=[]; unresolved=False
    base_seed=int(seeds["analysis_rng"]["primary_trend_permutation_seed"])
    for d in (14,16,18):
        for sigma in SIGMA_LEVELS_V002:
            ds=_dose_seed_set(rows,d,sigma); panel=[r for r in rows if int(r["depth"])==d and float(r["sigma"])==sigma and int(r["seed"]) in ds]
            item={"depth":d,"sigma":sigma,"dose_families":len(ds),"informative":len(ds)>=N_DOSE_MIN_V002}
            if not item["informative"]:
                item.update({"status":"PANEL_DOSE_UNRESOLVED","p_one_sided":None,"p_holm":None,"pass":False}); unresolved=True
            else:
                tr=blocked_permutation_coverage_trend(panel,100000,stable_int(base_seed,d,sigma,"C")); item.update(tr); rawp.append(tr["p_one_sided"]); informative_indices.append(len(panels))
            panels.append(item)
    adj=holm_adjust(rawp) if rawp else []
    for idx,a in zip(informative_indices,adj):
        panels[idx]["p_holm"]=a; panels[idx]["pass"]=panels[idx]["statistic_T_C"]>0 and a<=0.05
    H1=(not unresolved) and all(p.get("pass",False) for p in panels)

    c1pass=bool(rows) and all(r.get("c1_exact") for r in rows)
    c1rows=[r for r in rows if r.get("coverage_C")==1.0 and r.get("population_V")]; H3a=all(r["exact_preservation"] for r in c1rows)
    leak3=[r for r in rows if int(r.get("N_rej_free",0))>=3]; pexact3=sum(r["exact_preservation"] for r in leak3)/len(leak3) if leak3 else None; H3b=pexact3 is None or pexact3<=0.20

    cond=[]
    for d in (14,16,18):
        for sigma in SIGMA_LEVELS_V002:
            for q in Q_LEVELS_V002:
                x=[r for r in rows if int(r["depth"])==d and float(r["sigma"])==sigma and float(r["q"])==q]
                n=len(x); exact=sum(r["exact_preservation"] for r in x); v=sum(r["population_V"] for r in x)
                medrn=statistics.median([r["r_node"] for r in x]) if x else None; medg=statistics.median([r["g_time"] for r in x]) if x else None
                under=n<N_ACC_MIN_V002
                valid=(not under) and v==n and exact==n and medrn is not None and medrn>=0.25 and medg is not None and medg>=1.10
                high=(not under) and n>0 and exact/n>=0.90 and medrn is not None and medrn>=0.25 and medg is not None and medg>=1.10
                cond.append({"depth":d,"sigma":sigma,"q":q,"accepted_n":n,"UNDERPOWERED_CONDITION":under,"population_V":v,"exact":exact,"cp95":clopper_pearson(exact,n) if n else [None,None],"median_r_node":medrn,"median_g_time":medg,"VALID_STRUCTURAL_REDUCTION":valid,"HIGH_RELIABILITY_REDUCTION":high})

    transfer=False; setting=None
    for sigma in SIGMA_LEVELS_V002:
        for q in Q_LEVELS_V002:
            xx=[c for c in cond if c["sigma"]==sigma and c["q"]==q]
            if len(xx)==3 and all(c["VALID_STRUCTURAL_REDUCTION"] for c in xx): transfer=True; setting={"sigma":sigma,"q":q}; break
        if transfer: break
    cv=[(r["coverage_C"],r["solution_recall"]) for r in rows if r.get("coverage_C") is not None]; cs=spearman([x[0] for x in cv],[x[1] for x in cv]) if len(cv)>1 else None
    H4=bool(est["H4_pass"]); H5=bool(nulls["H5_pass"]) and c1pass
    law=H1 and H4 and H5 and c1pass
    verdict="TRANSFER_CONFIRMED" if transfer else ("COUPLING_LAW_CANDIDATE" if law else "COUPLING_MAP_ONLY")
    final={"engine":"SCR_III_ENGINE_v002","status":"COMPLETE","study_verdict":verdict,"TRANSFER_CONFIRMED":transfer,"transfer_setting":setting,"COUPLING_LAW_CANDIDATE":law,"H1":H1,"H1_panels":panels,"H3a":H3a,"H3a_cells":len(c1rows),"H3b":H3b,"Pexact_Nrej_free_ge3":pexact3,"H4":H4,"H5":H5,"C1_pass":c1pass,"Spearman_C_recall":cs,"condition_verdicts":cond,"generated_main_cells":len(rows),"accepted_families":primary.get("accepted_families",[]),"infeasible_families":primary.get("infeasible_families",[])}
    out=root/"reports"; out.mkdir(parents=True,exist_ok=True); safe_write_json(out/"FINAL_ANALYSIS_v002.json",final)
    lines=["# SCR-III-A v002 Summary","",f"**Study verdict:** `{verdict}`","",f"Generated main cells: {len(rows)} / 900",f"H1 realized-C dose response: {'PASS' if H1 else 'FAIL'}",f"H3a construction anchor: {'PASS' if H3a else 'FAIL'}",f"H3b free-rejecting-layer prediction: {'PASS' if H3b else 'FAIL'}",f"H4 applicability estimators: {'PASS' if H4 else 'FAIL'}",f"H5 controls: {'PASS' if H5 else 'FAIL'}",f"Spearman(C, recall): {cs}","","## H1 panels",""]
    for p in panels: lines.append(f"- d={p['depth']} σ={p['sigma']:.1f}: dose families={p['dose_families']}, informative={p['informative']}, p={p.get('p_one_sided')}, Holm={p.get('p_holm')}, pass={p.get('pass')}")
    lines += ["","## Condition verdicts",""]
    for c in cond: lines.append(f"- d={c['depth']} σ={c['sigma']:.1f} q={c['q']:.1f}: accepted={c['accepted_n']}, exact={c['exact']}/{c['accepted_n']}, V={c['population_V']}/{c['accepted_n']}, UNDERPOWERED={c['UNDERPOWERED_CONDITION']}, VALID={c['VALID_STRUCTURAL_REDUCTION']}, HIGH_RELIABILITY={c['HIGH_RELIABILITY_REDUCTION']}")
    (out/"SUMMARY_v002.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print("SCR-III-A v002 SUMMARY:",verdict); return 0

if __name__=="__main__": raise SystemExit(main())

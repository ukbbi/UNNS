from __future__ import annotations
import json, statistics
from collections import defaultdict
from pathlib import Path
from scr_iii.engine_common import scr_iii_root, safe_write_json, stable_int
from scr_iii.analysis.trend_test_v001 import blocked_permutation_trend
from scr_iii.analysis.stats_v001 import holm_adjust, spearman, clopper_pearson


def main():
    s3=scr_iii_root(); pp=s3/'output'/'primary'/'PRIMARY_RESULT_v001.json'; np=s3/'output'/'nulls'/'NULL_RESULT_v001.json'; ep=s3/'output'/'estimators'/'ESTIMATOR_RESULT_v001.json'
    missing=[p.name for p in (pp,np,ep) if not p.exists()]
    if missing: print('Summary blocked; missing:',', '.join(missing)); return 2
    primary=json.loads(pp.read_text()); nulls=json.loads(np.read_text()); est=json.loads(ep.read_text()); seeds=json.loads((s3/'SCR_III_PREREG_v001'/'SEEDS_v001.json').read_text())
    rows=primary['main_cells']; panels=[]; rawp=[]
    for d in (14,16,18):
        for sigma in (0.8,0.9):
            x=[r for r in rows if int(r['depth'])==d and float(r['sigma'])==sigma]
            tr=blocked_permutation_trend(x,100000,stable_int(seeds['trend_permutation_seed'],d,sigma)); panels.append({"depth":d,"sigma":sigma,**tr}); rawp.append(tr['p_one_sided'])
    adj=holm_adjust(rawp)
    for p,a in zip(panels,adj): p['p_holm']=a; p['pass']=p['statistic_T']>0 and a<=0.05
    H1=all(p['pass'] for p in panels)
    c1cells=[r for r in rows if r.get('c1_exact')]; c1pass=len(c1cells)==len(rows) and bool(rows)
    c1anchors=all(x.get('c1_exact',True) for x in primary.get('Z0',[]))
    c1pass=c1pass and c1anchors
    c1_rows=[r for r in rows if r.get('coverage_C')==1.0 and r.get('population_V')]
    H3a=all(r['exact_preservation'] for r in c1_rows)
    leak3=[r for r in rows if int(r.get('N_rej_free',0))>=3]
    pexact3=sum(r['exact_preservation'] for r in leak3)/len(leak3) if leak3 else None
    H3b=pexact3 is None or pexact3<=0.20
    cond=[]
    for d in (14,16,18):
        for sigma in (0.8,0.9):
            for q in (0.0,0.1,0.2,0.3,0.4):
                x=[r for r in rows if int(r['depth'])==d and float(r['sigma'])==sigma and float(r['q'])==q]
                exact=sum(r['exact_preservation'] for r in x); v=sum(r['population_V'] for r in x); n=len(x)
                medrn=statistics.median([r['r_node'] for r in x]) if x else None; medg=statistics.median([r['g_time'] for r in x]) if x else None
                valid=n==20 and v==20 and exact==20 and medrn>=0.25 and medg>=1.10
                high=n==20 and exact>=18 and medrn>=0.25 and medg>=1.10
                cond.append({"depth":d,"sigma":sigma,"q":q,"n":n,"population_V":v,"exact":exact,"cp95":clopper_pearson(exact,n) if n else [None,None],"median_r_node":medrn,"median_g_time":medg,"VALID_STRUCTURAL_REDUCTION":valid,"HIGH_RELIABILITY_REDUCTION":high and not valid})
    transfer=False; transfer_setting=None
    for sigma in (0.8,0.9):
        for q in (0.0,0.1,0.2,0.3,0.4):
            xs=[c for c in cond if c['sigma']==sigma and c['q']==q]
            if len(xs)==3 and all(c['VALID_STRUCTURAL_REDUCTION'] for c in xs): transfer=True; transfer_setting={"sigma":sigma,"q":q}
    cv=[(r['coverage_C'],r['solution_recall']) for r in rows if r.get('coverage_C') is not None]
    c_spear=spearman([x[0] for x in cv],[x[1] for x in cv]) if len(cv)>1 else None
    H4=bool(est['H4_pass']); H5=bool(nulls['H5_pass']) and c1pass
    law=H1 and H4 and H5 and (c_spear is not None and c_spear>0)
    verdict='TRANSFER_CONFIRMED' if transfer else ('COUPLING_LAW_CANDIDATE' if law else 'COUPLING_MAP_ONLY')
    final={"engine":"SCR_III_ENGINE_v001","status":"COMPLETE","study_verdict":verdict,"TRANSFER_CONFIRMED":transfer,"transfer_setting":transfer_setting,"COUPLING_LAW_CANDIDATE":law,"H1":H1,"H1_panels":panels,"H3a":H3a,"H3a_cells":len(c1_rows),"H3b":H3b,"Pexact_Nrej_free_ge3":pexact3,"H4":H4,"H5":H5,"C1_pass":c1pass,"Spearman_C_recall":c_spear,"condition_verdicts":cond,"generated_main_cells":len(rows),"infeasible_families":primary['infeasible_families']}
    out=s3/'output'/'reports'; out.mkdir(parents=True,exist_ok=True); safe_write_json(out/'FINAL_ANALYSIS_v001.json',final)
    lines=['# SCR-III-A v001 Summary','',f"**Study verdict:** `{verdict}`",'',f"Generated main cells: {len(rows)} / 600",f"H1 paired dose response: {'PASS' if H1 else 'FAIL'}",f"H3a construction anchor: {'PASS' if H3a else 'FAIL'}",f"H3b free-rejecting-layer prediction: {'PASS' if H3b else 'FAIL'}",f"H4 applicability estimators: {'PASS' if H4 else 'FAIL'}",f"H5 controls: {'PASS' if H5 else 'FAIL'}",f"Spearman(C, recall): {c_spear}",'','## Condition verdicts','']
    for c in cond: lines.append(f"- d={c['depth']} σ={c['sigma']:.1f} q={c['q']:.1f}: exact {c['exact']}/{c['n']}, V={c['population_V']}/{c['n']}, VALID={c['VALID_STRUCTURAL_REDUCTION']}, HIGH_RELIABILITY={c['HIGH_RELIABILITY_REDUCTION']}")
    (out/'SUMMARY_v001.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print('SCR-III-A SUMMARY:',verdict); return 0
if __name__=='__main__': raise SystemExit(main())

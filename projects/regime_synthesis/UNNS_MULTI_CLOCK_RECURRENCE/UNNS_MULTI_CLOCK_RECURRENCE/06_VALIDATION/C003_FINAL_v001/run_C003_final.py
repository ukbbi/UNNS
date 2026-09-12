#!/usr/bin/env python3
"""
Reproduce C003_FINAL_v001 using the ACTUAL project layout.

This script auto-detects the project root from its own path, so it can be launched:
  - from the project root,
  - from 06_VALIDATION/C003_FINAL_v001,
  - by an absolute Python command,
without changing directories first.

Reads:
  <root>/05_METHODS/rep_study_v002.py
  <root>/05_METHODS/rep_study_config_v002.json
  <root>/05_METHODS/grammar_dev_v001.py
  <root>/05_METHODS/grammar_dev_config_v001.json
  <root>/05_METHODS/mc_grammar_v001.py

  <root>/06_VALIDATION/C003_FINAL_v001/INGEST/TC_P01_C003.csv
  <root>/06_VALIDATION/C003_FINAL_v001/INGEST/TC_P01_C003_CTRL.csv

Writes:
  <root>/08_OUTPUTS/C003_FINAL_v001/REPRO/

Historical one-shot outputs are never overwritten.
"""
from pathlib import Path
import json, importlib.util
import numpy as np
import pandas as pd

def find_project_root():
    """
    Script lives at:
      <root>/06_VALIDATION/C003_FINAL_v001/<script>.py
    Therefore parents[2] is the actual UNNS_MULTI_CLOCK_RECURRENCE root.
    """
    here = Path(__file__).resolve()
    root = here.parents[2]
    required = [
        root / "05_METHODS" / "rep_study_v002.py",
        root / "05_METHODS" / "grammar_dev_v001.py",
        root / "05_METHODS" / "mc_grammar_v001.py",
    ]
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        raise SystemExit(
            "Could not resolve UNNS_MULTI_CLOCK_RECURRENCE root from script location.\n"
            "Missing:\n  " + "\n  ".join(missing)
        )
    return root


ROOT=find_project_root()
VAL=ROOT/"06_VALIDATION"/"C003_FINAL_v001"
ING=VAL/"INGEST"
OUT=ROOT/"08_OUTPUTS"/"C003_FINAL_v001"/"REPRO"
OUT.mkdir(parents=True,exist_ok=True)

R=1.618

def import_file(name,path):
    sp=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(sp)
    sp.loader.exec_module(mod)
    return mod

rep=import_file("rep_v002",ROOT/"05_METHODS"/"rep_study_v002.py")
dev=import_file("dev_v001",ROOT/"05_METHODS"/"grammar_dev_v001.py")
gram=import_file("gram_v001",ROOT/"05_METHODS"/"mc_grammar_v001.py")

rep_cfg=json.loads((ROOT/"05_METHODS"/"rep_study_config_v002.json").read_text(encoding="utf-8"))
dev_cfg=json.loads((ROOT/"05_METHODS"/"grammar_dev_config_v001.json").read_text(encoding="utf-8"))

def analyze_once(rid,x,Y,r):
    jrows=rep.jpr_scan(
        x,Y,r,rep_cfg["joint_phase_recurrence"],rid,
        rep_cfg["joint_phase_recurrence"]["max_pairs_base"]
    )
    j1=[q for q in jrows if q["depth"]==1][0]
    jf=max([q for q in jrows if q["depth"]>=2],key=lambda q:q["JPR_gain"])
    J_frac=float(jf["JPR_gain"]-j1["JPR_gain"])

    crows=rep.fc_scan(x,Y,r,rep_cfg["fractional_cover"])
    cb=max(crows,key=lambda q:q["FC_frac_total_gain"])
    M_frac=float(cb["FC_frac_mixed_gain"])

    max_n=int(dev_cfg["qualification_grid"]["max_samples"])
    xq,Yq,stride=dev.qualification_grid(x,Y,max_n)
    budget=int(dev_cfg["qualification_grid"]["jpr_pair_budget"])
    JS=int(dev_cfg["null_engine"]["JPR_surrogates_per_model"])
    FS=int(dev_cfg["null_engine"]["FC_surrogates_per_model"])
    BASE=int(dev_cfg["seed"])

    ii,jj=dev.sample_pairs(xq,r,budget,dev.stable_seed(rid,BASE,101))
    masks=dev.near_masks(xq,r,ii,jj)
    jp,jc,jd=dev.jpr_metrics(Yq,ii,jj,masks)

    rng=np.random.default_rng(
        dev.stable_seed(rid+"|PHASE_LABEL_PERMUTE",BASE,301)
    )
    pnull=[]
    for _ in range(JS):
        pm=dev.near_masks(xq[rng.permutation(len(xq))],r,ii,jj)
        a,_,_=dev.jpr_metrics(Yq,ii,jj,pm)
        pnull.append(a)
    pstat=dev.empirical(jp,pnull)

    sets=dev.fc_sets(r)
    caches={k:dev.build_cv_cache(rep,xq,v) for k,v in sets.items()}
    one=Yq[None,:,:]
    parent=float(dev.cv_r2_batch(one,caches["parent"])[0])

    qvals={}
    for d in (2,3,4):
        ar=float(dev.cv_r2_batch(one,caches[f"axis_{d}"])[0])
        fu=float(dev.cv_r2_batch(one,caches[f"full_{d}"])[0])
        qvals[d]={"total":fu-parent,"mixed":fu-ar}

    dstar=max((2,3,4),key=lambda d:qvals[d]["total"])
    mqual=qvals[dstar]["mixed"]

    batch=dev.generate_batch(
        Yq,"FOURIER_PHASE",FS,xq,
        dev.stable_seed(rid+"|FC|FOURIER_PHASE",BASE,701)
    )
    par=dev.cv_r2_batch(batch,caches["parent"])
    totals=np.zeros((FS,3))
    mixed=np.zeros((FS,3))

    for j,d in enumerate((2,3,4)):
        ar=dev.cv_r2_batch(batch,caches[f"axis_{d}"])
        fu=dev.cv_r2_batch(batch,caches[f"full_{d}"])
        totals[:,j]=fu-par
        mixed[:,j]=fu-ar

    bi=np.argmax(totals,axis=1)
    mnull=mixed[np.arange(FS),bi]
    mstat=dev.empirical(mqual,mnull)

    mrob={}
    for variant in [
        "ORIGIN_SHIFT","CLOCK_EXCHANGE","AFFINE_STATE",
        "DOWNSAMPLE_5","PREFIX_0.75","NOISE_0.02SD"
    ]:
        xv,Yv,rv=rep.transform_variant(variant,x,Y,r,rep_cfg,rid)
        cr=rep.fc_scan(xv,Yv,rv,rep_cfg["fractional_cover"])
        br=max(cr,key=lambda q:q["FC_frac_total_gain"])
        mrob[variant]=float(br["FC_frac_mixed_gain"])

    evaluator_input={
        "domain_valid":True,
        "ratio_qualified_v001":True,
        "P_phase_label_p_upper":float(pstat["p_upper"]),
        "J_frac":J_frac,
        "M_frac":M_frac,
        "M_fourier_p_upper":float(mstat["p_upper"]),
        "M_robustness":mrob,
        "collective_annotation":"COLLECTIVE_NOT_ASSESSED",
    }
    verdict=gram.evaluate(evaluator_input)

    return {
        "JPR_parent_gain":float(j1["JPR_gain"]),
        "J_frac":J_frac,
        "J_best_fractional_depth":int(jf["depth"]),
        "FC_frac_total_gain":float(cb["FC_frac_total_gain"]),
        "M_frac":M_frac,
        "FC_best_fractional_depth":int(cb["depth"]),
        "P_phase_label_p_upper":float(pstat["p_upper"]),
        "P_phase_label_percentile":float(pstat["observed_percentile"]),
        "M_fourier_p_upper":float(mstat["p_upper"]),
        "M_fourier_percentile":float(mstat["observed_percentile"]),
        "qualification_n":int(len(xq)),
        "M_robustness":mrob,
        "M_robust_min":float(min(mrob.values())),
        "temporal_state":verdict["temporal_state"],
        "failure_flags":verdict["failure_flags"],
        "collective_annotation":verdict["collective_annotation"],
    }

source_specs={
    "TC_P01_C003":{
        "historical_role":"ROBUST_MULTI_CLOCK_CANDIDATE",
        "source_figure":"Fig.1d",
    },
    "TC_P01_C003_CTRL":{
        "historical_role":"SHORT_INTERACTION_BREAKDOWN_CONTROL",
        "source_figure":"Fig.1b",
    },
}

results=[]
for rid in ["TC_P01_C003","TC_P01_C003_CTRL"]:
    q=pd.read_csv(ING/f"{rid}.csv")
    x=q["source_cycles_tau2"].to_numpy(float)
    Y=q[["polarization"]].to_numpy(float)

    res=analyze_once(rid,x,Y,R)
    res.update({
        "id":rid,
        "historical_role":source_specs[rid]["historical_role"],
        "source_figure":source_specs[rid]["source_figure"],
        "source_n":len(q),
        "ratio":R,
    })
    results.append(res)
    (OUT/f"{rid}_DETAIL.json").write_text(
        json.dumps(res,indent=2),encoding="utf-8"
    )

rows=[]
for r in results:
    d={k:v for k,v in r.items() if k not in ["M_robustness","failure_flags"]}
    d["failure_flags"]=";".join(r["failure_flags"])
    rows.append(d)

rdf=pd.DataFrame(rows)
rdf.to_csv(OUT/"C003_FINAL_RESULTS.csv",index=False)
(OUT/"C003_FINAL_RESULTS.json").write_text(
    json.dumps(results,indent=2),encoding="utf-8"
)

print("Project root:", ROOT)
print("Reproduction output:", OUT)
print()
print(rdf[[
    "id","P_phase_label_p_upper","J_frac","M_frac",
    "M_fourier_p_upper","M_robust_min","temporal_state","failure_flags"
]].to_string(index=False))

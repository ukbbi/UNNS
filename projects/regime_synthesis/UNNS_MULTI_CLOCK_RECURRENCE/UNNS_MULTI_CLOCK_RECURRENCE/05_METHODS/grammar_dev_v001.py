#!/usr/bin/env python3
import argparse
import csv
import hashlib
import importlib.util
import io
import json
import math
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd


def sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(1<<20),b""):
            h.update(chunk)
    return h.hexdigest()


def stable_seed(text, base, offset=0):
    h=hashlib.sha256(text.encode("utf-8")).hexdigest()
    return (base + offset + int(h[:8],16)) % (2**32-1)


def robust_scale(Y):
    med=np.median(Y,axis=0)
    mad=1.4826*np.median(np.abs(Y-med),axis=0)
    std=np.std(Y,axis=0)
    scale=np.where(mad>1e-12,mad,np.where(std>1e-12,std,1.0))
    return (Y-med)/scale


def qualification_grid(x,Y,max_n):
    n=len(x)
    stride=max(1,math.ceil(n/max_n))
    idx=np.arange(0,n,stride,dtype=int)
    return x[idx],Y[idx],stride


def sample_pairs(x,r,budget,seed):
    n=len(x);rng=np.random.default_rng(seed)
    oi=[];oj=[];batch=max(20000,budget);attempts=0
    while len(oi)<budget and attempts<200:
        a=rng.integers(0,n,size=batch)
        b=rng.integers(0,n,size=batch)
        lo=np.minimum(a,b);hi=np.maximum(a,b)
        dx=np.abs(x[hi]-x[lo])
        valid=(lo<hi)&(np.minimum(dx,np.abs(r*dx))>=1.0)
        oi.extend(lo[valid].tolist());oj.extend(hi[valid].tolist())
        attempts+=1
    if len(oi)<budget:
        raise RuntimeError("Could not sample enough JPR pairs.")
    return np.asarray(oi[:budget]),np.asarray(oj[:budget])


def torus_distance(xlabels,r,d,ii,jj):
    dx=(xlabels[jj]-xlabels[ii])/float(d)
    da=np.abs(dx-np.round(dx))
    db=np.abs(r*dx-np.round(r*dx))
    return np.sqrt(da*da+db*db)/math.sqrt(0.5)


def near_masks(xlabels,r,ii,jj):
    out={}
    for d in (1,2,3,4):
        tor=torus_distance(xlabels,r,d,ii,jj)
        out[d]=tor<=np.quantile(tor,0.01)
    return out


def jpr_metrics(Y,ii,jj,masks):
    Z=robust_scale(Y)
    state=np.sqrt(np.mean((Z[ii]-Z[jj])**2,axis=1))
    med=float(np.median(state)+1e-30)
    gains={d:1-float(np.median(state[m]))/med for d,m in masks.items()}
    parent=gains[1]
    dstar=max((2,3,4),key=lambda d:gains[d])
    return parent,gains[dstar]-parent,dstar


def block_permutation(n,block_len,rng):
    blocks=[np.arange(i,min(n,i+block_len)) for i in range(0,n,block_len)]
    order=rng.permutation(len(blocks))
    return np.concatenate([blocks[k] for k in order])


def fourier_phase_surrogate(Y,rng):
    n=Y.shape[0]
    F=np.fft.rfft(Y,axis=0)
    phase=rng.uniform(0,2*np.pi,size=F.shape[0])
    phase[0]=0.0
    if n%2==0:
        phase[-1]=0.0
    return np.fft.irfft(F*np.exp(1j*phase)[:,None],n=n,axis=0)


def empirical(obs,vals):
    v=np.asarray(vals,float)
    return {
        "observed":float(obs),
        "null_median":float(np.median(v)),
        "null_q05":float(np.quantile(v,0.05)),
        "null_q95":float(np.quantile(v,0.95)),
        "p_upper":float((1+np.sum(v>=obs))/(len(v)+1)),
        "p_lower":float((1+np.sum(v<=obs))/(len(v)+1)),
        "observed_percentile":float((np.sum(v<obs)+0.5*np.sum(v==obs))/len(v)),
        "null_n":int(len(v)),
    }


def fc_sets(r):
    pa=[1.0,r];pm=[abs(r-1.0),r+1.0]
    out={"parent":pa+pm}
    for d in (2,3,4):
        fa=[1/d,r/d];fm=[abs(r-1)/d,(r+1)/d]
        out[f"axis_{d}"]=pa+pm+fa
        out[f"full_{d}"]=pa+pm+fa+fm
    return out


def build_cv_cache(rep,x,freqs,k=5,alpha=1e-9):
    X=rep.features(x,freqs)
    n=len(x);bounds=np.linspace(0,n,k+1,dtype=int);cache=[]
    for i in range(k):
        te=np.arange(bounds[i],bounds[i+1])
        tr=np.r_[np.arange(0,bounds[i]),np.arange(bounds[i+1],n)]
        Xt=X[tr];A=Xt.T@Xt;reg=np.eye(A.shape[0])*alpha;reg[0,0]=0.0
        T=np.linalg.solve(A+reg,Xt.T)
        cache.append((tr,te,T,X[te]))
    return cache


def cv_r2_batch(Ybatch,cache):
    S,n,dim=Ybatch.shape;fold=[]
    for tr,te,T,Xte in cache:
        flat=Ybatch[:,tr,:].transpose(1,0,2).reshape(len(tr),S*dim)
        beta=T@flat
        pred=(Xte@beta).reshape(len(te),S,dim).transpose(1,0,2)
        truth=Ybatch[:,te,:]
        mean=truth.mean(axis=1,keepdims=True)
        ss=np.sum((truth-mean)**2,axis=1)
        err=np.sum((truth-pred)**2,axis=1)
        fold.append((1-err/(ss+1e-30)).mean(axis=1))
    return np.mean(np.stack(fold,axis=1),axis=1)


def generate_batch(Y,model,S,x,seed):
    rng=np.random.default_rng(seed);n,dim=Y.shape
    out=np.empty((S,n,dim),float)
    dx=float(np.median(np.diff(x)))
    bl=max(4,int(round(1.0/max(dx,1e-12))))
    bl=min(bl,max(4,n//4))
    for s in range(S):
        if model=="TIME_PERMUTE":
            out[s]=Y[rng.permutation(n)]
        elif model=="BLOCK_SHUFFLE":
            out[s]=Y[block_permutation(n,bl,rng)]
        elif model=="FOURIER_PHASE":
            out[s]=fourier_phase_surrogate(Y,rng)
        else:
            raise ValueError(model)
    return out


def auc_pair(pos,ctrl):
    wins=0.0;tot=0
    for a in np.asarray(pos,float):
        for b in np.asarray(ctrl,float):
            wins+=1.0 if a>b else 0.5 if a==b else 0.0
            tot+=1
    return wins/tot if tot else float("nan")


def zhu_ratio_inventory(raw_zip):
    with zipfile.ZipFile(raw_zip,"r") as z:
        names=z.namelist()
        a=[n for n in names if n.startswith("数据/fig4/fig4(a)/") and n.endswith(".csv")]
        b=[n for n in names if n.startswith("数据/fig4/fig4(b)/") and n.endswith(".csv")]
        xlsx=[n for n in names if n in [
            "数据/fig4/fig4(c).xlsx","数据/fig4/fig4(d).xlsx",
            "数据/fig4/fig4(e).xlsx","数据/fig4/fig4(f).xlsx"]]
        headers={}
        for n in [a[len(a)//2],b[len(b)//2]]:
            headers[n]=z.read(n).decode("utf-8","replace").splitlines()[0]
        ns={"m":"http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
        xm={}
        for n in xlsx:
            raw=z.read(n)
            with zipfile.ZipFile(io.BytesIO(raw),"r") as xz:
                xml=ET.fromstring(xz.read("xl/worksheets/sheet1.xml"))
                dim=xml.find("m:dimension",ns).attrib.get("ref")
                vals=[]
                for row in xml.findall(".//m:sheetData/m:row",ns):
                    cells=row.findall("m:c",ns)
                    if cells:
                        v=cells[0].find("m:v",ns)
                        if v is not None:
                            try: vals.append(float(v.text))
                            except: pass
                xm[n]={"sha256":hashlib.sha256(raw).hexdigest(),
                       "sheet_dimension":dim,
                       "first_column_min":float(min(vals)) if vals else None,
                       "first_column_max":float(max(vals)) if vals else None,
                       "interpretation":"two-column Fourier spectrum; not time domain"}
    return {
        "inventory_id":"ZHU_RATIO_INVENTORY_v001",
        "source_archive_sha256":sha256(raw_zip),
        "figure4":{
            "fig4a_spectral_sweep":{"files":len(a),"modulation_range_khz":[89.0,91.0],
                "step_khz":0.010,"fixed_f2_khz":40.0,
                "incommensurate_target":{"f1_khz":40*math.sqrt(5),
                    "f2_over_f1":1/math.sqrt(5),"paper_panel":"Fig.4(d)"},
                "sample_header":headers[a[len(a)//2]],"data_kind":"FOURIER_SPECTRAL_PHASE_DIAGRAM"},
            "fig4b_spectral_sweep":{"files":len(b),"modulation_range_khz":[89.0,91.0],
                "step_khz":0.010,"fixed_f2_khz":60.0,
                "incommensurate_target":{"f1_khz":40*math.sqrt(5),
                    "f2_over_f1":3/(2*math.sqrt(5)),"paper_panel":"Fig.4(f)"},
                "sample_header":headers[b[len(b)//2]],"data_kind":"FOURIER_SPECTRAL_PHASE_DIAGRAM"},
            "single_spectra":xm},
        "time_domain_records_found_for_non_golden_ratios":False,
        "eligible_for_JPR_or_FC_time_domain_qualification":False,
        "reason":"Fig.4 records are Fourier spectra/spectral phase diagrams; inverse reconstruction is prohibited.",
        "frequency_lattice_descriptive_use_possible":True,
        "c003_used":False,
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--root",default=".")
    args=ap.parse_args()
    root=Path(args.root).resolve()

    cfg=json.loads((root/"05_METHODS/grammar_dev_config_v001.json").read_text())
    rs=root/"05_METHODS/rep_study_v002.py"
    sp=importlib.util.spec_from_file_location("rep_v002",rs)
    rep=importlib.util.module_from_spec(sp);sp.loader.exec_module(rep)

    corpus=pd.read_csv(root/"04_CORPUS/REP_CORPUS_v002.csv")
    core=corpus[corpus.panel=="CORE_FOUR_REP"].copy()
    full_rep=pd.read_csv(root/"08_OUTPUTS/REP_STUDY_v002/FOUR_REP_RESULTS.csv")
    robust=pd.read_csv(root/"08_OUTPUTS/REP_STUDY_v002/ROBUSTNESS_SUMMARY.csv")
    collective=pd.read_csv(root/"08_OUTPUTS/REP_STUDY_v002/COLLECTIVE_CONTEXT.csv")
    collective["source"]="LUO_2026"

    out=root/"08_OUTPUTS/GRAMMAR_DEV_v001"
    detail=out/"RECORD_DETAILS";detail.mkdir(parents=True,exist_ok=True)
    zdir=root/"06_VALIDATION/ZHU_2026/RATIO_INVENTORY_v001";zdir.mkdir(parents=True,exist_ok=True)

    MAX_N=cfg["qualification_grid"]["max_samples"]
    BUDGET=cfg["qualification_grid"]["jpr_pair_budget"]
    JS=cfg["null_engine"]["JPR_surrogates_per_model"]
    FS=cfg["null_engine"]["FC_surrogates_per_model"]
    BASE=cfg["seed"]

    null_rows=[];qual=[];grids=[]
    for _,row in core.iterrows():
        rid=row.id
        x0,Y0,r=rep.load_core(root,row)
        x,Y,stride=qualification_grid(x0,Y0,MAX_N)
        ii,jj=sample_pairs(x,r,BUDGET,stable_seed(rid,BASE,101))
        masks=near_masks(x,r,ii,jj)
        jp,jc,jd=jpr_metrics(Y,ii,jj,masks)

        sets=fc_sets(r)
        caches={k:build_cv_cache(rep,x,v) for k,v in sets.items()}
        one=Y[None,:,:]
        parent=float(cv_r2_batch(one,caches["parent"])[0])
        fv={}
        for d in (2,3,4):
            a=float(cv_r2_batch(one,caches[f"axis_{d}"])[0])
            f=float(cv_r2_batch(one,caches[f"full_{d}"])[0])
            fv[d]={"axis":a,"full":f,"total":f-parent,"mixed":f-a}
        fd=max((2,3,4),key=lambda d:fv[d]["total"])
        ft=fv[fd]["total"];fm=fv[fd]["mixed"]

        grids.append({"id":rid,"source":row.source,"role":row.role,
            "source_n":len(x0),"qualification_n":len(x),"stride":stride,"state_dim":Y.shape[1],
            "JPR_parent_gain":jp,"JPR_cover_advantage":jc,"JPR_best_fractional_depth":jd,
            "FC_parent_full_r2":parent,"FC_frac_total_gain":ft,
            "FC_frac_mixed_gain":fm,"FC_best_fractional_depth":fd})

        draws={}
        for model in cfg["jpr_null_models"]:
            vp=[];vc=[];rng=np.random.default_rng(stable_seed(rid+"|"+model,BASE,301))
            dx=float(np.median(np.diff(x)));bl=max(4,int(round(1.0/max(dx,1e-12))))
            bl=min(bl,max(4,len(x)//4))
            for _ in range(JS):
                if model=="PHASE_LABEL_PERMUTE":
                    pm=near_masks(x[rng.permutation(len(x))],r,ii,jj)
                    a,b,_=jpr_metrics(Y,ii,jj,pm)
                else:
                    if model=="TIME_PERMUTE": Ys=Y[rng.permutation(len(x))]
                    elif model=="BLOCK_SHUFFLE": Ys=Y[block_permutation(len(x),bl,rng)]
                    elif model=="FOURIER_PHASE": Ys=fourier_phase_surrogate(Y,rng)
                    else: raise ValueError(model)
                    a,b,_=jpr_metrics(Ys,ii,jj,masks)
                vp.append(a);vc.append(b)
            for metric,obs,vals in [
                ("JPR_parent_gain",jp,vp),("JPR_cover_advantage",jc,vc)]:
                null_rows.append({"id":rid,"source":row.source,"role":row.role,
                    "representation":"JPR","null_model":model,"metric":metric,**empirical(obs,vals)})
            draws[model]={"JPR_parent_gain":vp,"JPR_cover_advantage":vc}

        for model in cfg["fc_null_models"]:
            batch=generate_batch(Y,model,FS,x,stable_seed(rid+"|FC|"+model,BASE,701))
            par=cv_r2_batch(batch,caches["parent"])
            totals=np.zeros((FS,3));mixed=np.zeros((FS,3))
            for j,d in enumerate((2,3,4)):
                a=cv_r2_batch(batch,caches[f"axis_{d}"])
                f=cv_r2_batch(batch,caches[f"full_{d}"])
                totals[:,j]=f-par;mixed[:,j]=f-a
            bi=np.argmax(totals,axis=1)
            bt=totals[np.arange(FS),bi];bm=mixed[np.arange(FS),bi]
            for metric,obs,vals in [
                ("FC_parent_full_r2",parent,par),
                ("FC_frac_total_gain",ft,bt),
                ("FC_frac_mixed_gain",fm,bm)]:
                null_rows.append({"id":rid,"source":row.source,"role":row.role,
                    "representation":"FC","null_model":model,"metric":metric,**empirical(obs,vals)})
            draws["FC_"+model]={"FC_parent_full_r2":par.tolist(),
                "FC_frac_total_gain":bt.tolist(),"FC_frac_mixed_gain":bm.tolist()}

        rdf=pd.DataFrame([q for q in null_rows if q["id"]==rid])
        def mn(metric):
            s=rdf[rdf.metric==metric].observed_percentile
            return float(s.min()) if len(s) else None
        qual.append({"id":rid,"source":row.source,"role":row.role,
            "JPR_parent_min_null_percentile":mn("JPR_parent_gain"),
            "JPR_cover_min_null_percentile":mn("JPR_cover_advantage"),
            "FC_parent_min_null_percentile":mn("FC_parent_full_r2"),
            "FC_total_min_null_percentile":mn("FC_frac_total_gain"),
            "FC_mixed_min_null_percentile":mn("FC_frac_mixed_gain"),
            "JPR_cover_observed":jc,"FC_mixed_observed":fm,"FC_total_observed":ft})
        (detail/f"{rid}.json").write_text(json.dumps({"grid":grids[-1],"null_draws":draws},
            indent=2,allow_nan=True))

    ndf=pd.DataFrame(null_rows);qdf=pd.DataFrame(qual);gdf=pd.DataFrame(grids)
    group=(ndf.groupby(["role","representation","null_model","metric"],as_index=False)
        .agg(records=("id","nunique"),observed_median=("observed","median"),
             null_median_of_medians=("null_median","median"),
             observed_percentile_median=("observed_percentile","median"),
             p_upper_median=("p_upper","median"),p_lower_median=("p_lower","median")))

    positive=full_rep[full_rep.role=="DTQC_POSITIVE"]
    metrics=["JPR_parent_gain","JPR_cover_advantage","FC_parent_full_r2",
             "FC_frac_mixed_gain","FC_frac_total_gain"]
    disc=[]
    for role in cfg["control_discrimination"]["control_roles"]:
        c=full_rep[full_rep.role==role]
        for metric in metrics:
            disc.append({"positive_role":"DTQC_POSITIVE","control_role":role,"metric":metric,
                "n_positive":len(positive),"n_control":len(c),
                "positive_median":float(positive[metric].median()),
                "control_median":float(c[metric].median()),
                "median_difference":float(positive[metric].median()-c[metric].median()),
                "AUC_P_positive_gt_control":float(auc_pair(positive[metric],c[metric]))})
    ddf=pd.DataFrame(disc)
    role=full_rep.groupby("role",as_index=False)[metrics].median()
    rcopy=robust.copy()
    rcopy["source_artifact"]="MC_REP_STUDY_v002"
    rcopy["source_sha256"]=sha256(root/"08_OUTPUTS/REP_STUDY_v002/ROBUSTNESS_SUMMARY.csv")

    outputs=[("QUAL_GRID_RESULTS",gdf),("NULL_RESULTS",ndf),("NULL_GROUP_SUMMARY",group),
             ("RECORD_QUALIFICATION",qdf),("CONTROL_DISCRIMINATION",ddf),
             ("ROLE_COORDINATES",role),("ROBUSTNESS_CARRYFORWARD",rcopy),
             ("COLLECTIVE_CONTEXT",collective)]
    for name,df in outputs:
        df.to_csv(out/f"{name}.csv",index=False)
        (out/f"{name}.json").write_text(json.dumps(df.to_dict(orient="records"),
            indent=2,allow_nan=True))

    zraw=root/"02_RAW/ZHU_2026/data.zip"
    zinv=zhu_ratio_inventory(zraw)
    (zdir/"ZHU_RATIO_INVENTORY_v001.json").write_text(json.dumps(zinv,indent=2,ensure_ascii=False))
    (zdir/"ZHU_RATIO_INVENTORY_v001.md").write_text(
        "# Zhu unused-ratio inventory v001\n\n"
        "The public Fig.4 data include the ratios `1/sqrt(5)` and `3/(2 sqrt(5))`, "
        "but only as Fourier spectra / spectral phase diagrams. They are not admissible "
        "time-domain inputs for JPR or FC without synthetic inverse reconstruction.\n"
    )

    qfiles=[out/f"{n}.csv" for n,_ in outputs]+[zdir/"ZHU_RATIO_INVENTORY_v001.json"]
    lines=["MC_GRAMMAR_DEV_v001 QUANTITATIVE LOCK",
           "Written before findings / coordinate qualification interpretation.",""]
    for p in qfiles: lines.append(f"{sha256(p)}  {p.relative_to(root).as_posix()}")
    (out/"QUANT_LOCK_SHA256.txt").write_text("\n".join(lines)+"\n")

    audit={"version":"MC_GRAMMAR_DEV_v001","status":"PASS_QUALIFICATION_STAGE_COMPLETE",
        "stage_completed":"nulls + robustness + control discrimination",
        "core_records":len(core),"jpr_surrogates_per_model":JS,
        "fc_surrogates_per_model":FS,"qualification_max_samples":MAX_N,
        "jpr_pair_budget":BUDGET,"thresholds_defined":0,"verdicts_emitted":0,
        "grammar_selected":False,"grammar_frozen":False,"c003_loaded":False,
        "zhu_other_ratios_time_domain_eligible":False,
        "quant_lock_sha256":sha256(out/"QUANT_LOCK_SHA256.txt")}
    (out/"AUDIT.json").write_text(json.dumps(audit,indent=2))
    print(json.dumps(audit,indent=2))


if __name__=="__main__":
    main()

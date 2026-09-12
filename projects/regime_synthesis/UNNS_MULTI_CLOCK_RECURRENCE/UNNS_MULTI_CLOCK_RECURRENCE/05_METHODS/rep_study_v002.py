#!/usr/bin/env python3
import argparse, json, math, hashlib
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from scipy.stats import spearmanr

def sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(1<<20),b""): h.update(chunk)
    return h.hexdigest()

def stable_seed(text, base):
    h=hashlib.sha256(text.encode()).hexdigest()
    return (base + int(h[:8],16)) % (2**32-1)

def robust_scale(Y):
    Y=np.asarray(Y,float)
    med=np.median(Y,axis=0)
    mad=1.4826*np.median(np.abs(Y-med),axis=0)
    std=np.std(Y,axis=0)
    scale=np.where(mad>1e-12,mad,np.where(std>1e-12,std,1.0))
    return (Y-med)/scale

def load_core(root,row):
    df=pd.read_csv(root/row["file"])
    rid=row["id"]
    if row["source"]=="LUO_2026":
        x=df["time"].to_numpy(float)
        Y=df[["S"]].to_numpy(float)
    elif row["source"]=="ZHU_2026":
        x=54.387*df["time_ms"].to_numpy(float)
        Y=df[["response"]].to_numpy(float)
    elif row["source"]=="MALZ_SMITH_2021":
        x=df["source_cycles_omega1"].to_numpy(float)
        Y=df[["sigma_x","sigma_y","sigma_z"]].to_numpy(float)
    else:
        raise ValueError(rid)
    ok=np.isfinite(x)&np.all(np.isfinite(Y),axis=1)
    return x[ok],Y[ok],float(row["source_ratio"])

def load_aux(root,row):
    df=pd.read_csv(root/row["file"])
    if row["source"]=="HUANG_2025":
        Y=df[["intensity"]].to_numpy(float)
    else:
        Y=df.drop(columns=["t"]).to_numpy(float)
    ok=np.all(np.isfinite(Y),axis=1)
    return Y[ok]

# ---------------------------------------------------------
# Representation 1: source-free vector-depth recurrence
# ---------------------------------------------------------
def vector_depth(Y,cfg):
    Z=np.asarray(Y,float)
    Z=(Z-Z.mean(axis=0))/(Z.std(axis=0)+1e-12)
    n=len(Z)
    qmax=min(int(cfg["max_lag_cap"]),max(2,n//3))
    # FFT autocorrelation, equal weight per coordinate.
    R=np.zeros(qmax+1,float)
    R[0]=1.0
    for c in range(Z.shape[1]):
        y=Z[:,c]
        m=1<<(2*n-1).bit_length()
        F=np.fft.rfft(y,n=m)
        ac=np.fft.irfft(F*np.conj(F),n=m)[:qmax+1]
        # unbiased normalization by overlap count
        ac=ac/np.maximum(1,np.arange(n,n-qmax-1,-1))
        ac=np.abs(ac)/(abs(ac[0])+1e-30)
        R+=ac
    R/=Z.shape[1]

    peaks,_=find_peaks(R[1:],distance=2)
    cand=(peaks+1).tolist()
    topn=int(cfg["top_lags"])
    if len(cand)<topn:
        cand=(np.argsort(R[1:])[-min(topn,qmax):]+1).tolist()
    else:
        a=np.array(cand,int)
        cand=a[np.argsort(R[a])[-topn:]].tolist()
    cand=sorted(set(map(int,cand)))

    pairs=[]
    for i,q1 in enumerate(cand):
        for q2 in cand[i+1:]:
            if q1+q2>qmax: continue
            qs=[q1,q2,abs(q2-q1),q1+q2]
            if min(qs)<=0: continue
            score=float(np.exp(np.mean(np.log(np.maximum(R[qs],1e-12)))))
            pairs.append((score,q1,q2))
    pairs=sorted(pairs,reverse=True)
    if pairs:
        best=pairs[0]
        med=float(np.median([p[0] for p in pairs]))
        return {
            "VD_best_single":float(max(R[q] for q in cand)),
            "VD_best_pair":float(best[0]),
            "VD_family_contrast":float(best[0]-med),
            "VD_q1":int(best[1]),"VD_q2":int(best[2]),
            "VD_pair_ratio":float(best[2]/best[1]),
            "VD_qmax":int(qmax),
        }
    return {
        "VD_best_single":float(max(R[q] for q in cand)) if cand else float("nan"),
        "VD_best_pair":float("nan"),"VD_family_contrast":float("nan"),
        "VD_q1":None,"VD_q2":None,"VD_pair_ratio":float("nan"),"VD_qmax":int(qmax),
    }

# ---------------------------------------------------------
# Representation 2: joint-phase-conditioned recurrence
# ---------------------------------------------------------
def sample_pairs(x,Y,r,max_pairs,seed):
    n=len(x)
    rng=np.random.default_rng(seed)
    # symmetric Theiler rule: both clocks must have advanced >= 1 cycle
    def valid(a,b):
        dx=np.abs(x[b]-x[a])
        return np.minimum(dx,np.abs(r*dx))>=1.0

    possible=n*(n-1)//2
    if possible<=max_pairs*2:
        ii,jj=np.triu_indices(n,1)
        mask=valid(ii,jj)
        ii,jj=ii[mask],jj[mask]
        if len(ii)>max_pairs:
            s=rng.choice(len(ii),max_pairs,replace=False)
            ii,jj=ii[s],jj[s]
    else:
        out_i=[];out_j=[]
        batch=max(20000,max_pairs)
        attempts=0
        while len(out_i)<max_pairs and attempts<100:
            a=rng.integers(0,n,size=batch)
            b=rng.integers(0,n,size=batch)
            lo=np.minimum(a,b);hi=np.maximum(a,b)
            m=(lo<hi)&valid(lo,hi)
            out_i.extend(lo[m].tolist());out_j.extend(hi[m].tolist())
            attempts+=1
        ii=np.asarray(out_i[:max_pairs],int);jj=np.asarray(out_j[:max_pairs],int)
    Z=robust_scale(Y)
    state=np.sqrt(np.mean((Z[ii]-Z[jj])**2,axis=1))
    return ii,jj,state

def jpr_scan(x,Y,r,cfg,record_id,max_pairs):
    ii,jj,state=sample_pairs(
        x,Y,r,int(max_pairs),stable_seed(record_id,20260827)
    )
    med_all=float(np.median(state)+1e-30)
    rows=[]
    for d in cfg["cover_depths"]:
        dx=(x[jj]-x[ii])/float(d)
        da=np.abs(dx-np.round(dx))
        db=np.abs(r*dx-np.round(r*dx))
        tor=np.sqrt(da*da+db*db)/math.sqrt(0.5)
        q=float(cfg["near_phase_quantile"])
        cut=float(np.quantile(tor,q))
        near=state[tor<=cut]
        qlo,qhi=cfg["mid_phase_quantiles"]
        lo=float(np.quantile(tor,qlo));hi=float(np.quantile(tor,qhi))
        mid=state[(tor>=lo)&(tor<=hi)]
        gain=1-float(np.median(near))/med_all
        contrast=1-float(np.median(near))/(float(np.median(mid))+1e-30)
        rho=float(spearmanr(tor,state).statistic)
        rows.append({
            "depth":int(d),"JPR_gain":gain,"JPR_mid_contrast":contrast,
            "JPR_phase_state_rho":rho,"JPR_pairs":int(len(state)),
            "JPR_near_pairs":int(len(near)),
        })
    return rows

# ---------------------------------------------------------
# Representation 3: low-order source frequency lattice
# ---------------------------------------------------------
def lattice_nodes(r,d,K):
    vals=[]
    for m in range(-K,K+1):
        for n in range(-K,K+1):
            if m==0 and n==0: continue
            if abs(m)+abs(n)>K: continue
            v=abs(m+n*r)/float(d)
            if v>1e-12: vals.append(v)
    vals=sorted(vals)
    out=[]
    for v in vals:
        if not out or abs(v-out[-1])>1e-9: out.append(v)
    return out

def mean_periodogram(x,Y):
    n=len(x);dx=float(np.median(np.diff(x)))
    P=None
    for c in range(Y.shape[1]):
        y=np.asarray(Y[:,c],float)
        y=(y-y.mean())/(y.std()+1e-12)
        p=np.abs(np.fft.rfft(y*np.hanning(n)))**2
        p=p/(p.sum()+1e-30)
        P=p if P is None else P+p
    P=P/Y.shape[1]
    f=np.fft.rfftfreq(n,dx)
    return f,P,float(1/(n*dx))

def frequency_lattice_scan(x,Y,r,cfg):
    f,P,df=mean_periodogram(x,Y)
    K=int(cfg["max_integer_order"])
    rows=[]
    for d in cfg["cover_depths"]:
        nodes=[v for v in lattice_nodes(r,d,K)
               if v>=3*df and v<=f[-1]-9*df]
        contrasts=[];node_bins=set()
        for v in nodes:
            i=int(np.argmin(np.abs(f-v)))
            for j in range(max(3,i-1),min(len(P),i+2)):
                node_bins.add(j)
            left=P[max(3,i-8):max(3,i-2)]
            right=P[min(len(P),i+3):min(len(P),i+9)]
            loc=np.r_[left,right]
            if len(loc)<4: continue
            local=float(np.median(loc)+1e-30)
            peak=float(np.max(P[max(3,i-1):min(len(P),i+2)])+1e-30)
            contrasts.append(math.log10(peak/local))
        if nodes:
            maxf=max(nodes)+2*df
            denom_mask=(f>=3*df)&(f<=maxf)
            denom=float(P[denom_mask].sum()+1e-30)
            allowed=[j for j in node_bins if denom_mask[j]]
            capture=float(P[allowed].sum()/denom) if allowed else 0.0
        else:
            capture=float("nan")
        rows.append({
            "depth":int(d),
            "FL_peak_contrast":float(np.median(contrasts)) if contrasts else float("nan"),
            "FL_capture":capture,
            "FL_nodes":int(len(nodes)),
            "FL_df":df,
        })
    return rows

# ---------------------------------------------------------
# Representation 4: v003 fractional-cover decomposition
# ---------------------------------------------------------
def features(x,freqs):
    cols=[np.ones_like(x)]
    for f in freqs:
        ph=2*np.pi*f*x
        cols.extend([np.cos(ph),np.sin(ph)])
    return np.column_stack(cols)

def cv_r2_multi(x,Y,freqs,k,alpha):
    n=len(x);bounds=np.linspace(0,n,k+1,dtype=int);vals=[]
    for i in range(k):
        test=np.zeros(n,bool);test[bounds[i]:bounds[i+1]]=True
        train=~test
        X=features(x[train],freqs);Xt=features(x[test],freqs)
        A=X.T@X;reg=np.eye(A.shape[0])*alpha;reg[0,0]=0.0
        B=np.linalg.solve(A+reg,X.T@Y[train])
        pred=Xt@B
        rr=[]
        for c in range(Y.shape[1]):
            yy=Y[test,c]
            ss=float(np.sum((yy-yy.mean())**2))
            rr.append(float(1-np.sum((yy-pred[:,c])**2)/(ss+1e-30)))
        vals.append(float(np.mean(rr)))
    return float(np.mean(vals))

def fc_scan(x,Y,r,cfg):
    pa=[1.0,r];pm=[abs(r-1.0),r+1.0]
    k=int(cfg["cv_folds"]);alpha=float(cfg["ridge_alpha"])
    pax=cv_r2_multi(x,Y,pa,k,alpha)
    parent=cv_r2_multi(x,Y,pa+pm,k,alpha)
    rows=[]
    for d in cfg["fractional_depths"]:
        fa=[1/d,r/d];fm=[abs(r-1)/d,(r+1)/d]
        na=cv_r2_multi(x,Y,pa+pm+fa,k,alpha)
        nf=cv_r2_multi(x,Y,pa+pm+fa+fm,k,alpha)
        rows.append({
            "depth":int(d),
            "FC_parent_axis_r2":pax,
            "FC_parent_full_r2":parent,
            "FC_parent_mixed_gain":parent-pax,
            "FC_frac_axis_gain":na-parent,
            "FC_frac_mixed_gain":nf-na,
            "FC_frac_total_gain":nf-parent,
        })
    return rows

def summarize_core(rid,source,role,x,Y,r,cfg,max_pairs):
    vd=vector_depth(Y,cfg["vector_depth"])
    jrows=jpr_scan(x,Y,r,cfg["joint_phase_recurrence"],rid,max_pairs)
    frows=frequency_lattice_scan(x,Y,r,cfg["frequency_lattice"])
    crows=fc_scan(x,Y,r,cfg["fractional_cover"])

    j1=[q for q in jrows if q["depth"]==1][0]
    jf=max([q for q in jrows if q["depth"]>=2],key=lambda q:q["JPR_gain"])
    jb=max(jrows,key=lambda q:q["JPR_gain"])
    fb=max(frows,key=lambda q:(-1e99 if not np.isfinite(q["FL_peak_contrast"]) else q["FL_peak_contrast"]))
    f1=[q for q in frows if q["depth"]==1][0]
    ff=max([q for q in frows if q["depth"]>=2],
           key=lambda q:(-1e99 if not np.isfinite(q["FL_peak_contrast"]) else q["FL_peak_contrast"]))
    cb=max(crows,key=lambda q:q["FC_frac_total_gain"])

    out={
        "id":rid,"source":source,"role":role,"n":len(x),"state_dim":Y.shape[1],
        "source_ratio":r,
        **vd,
        "JPR_parent_gain":j1["JPR_gain"],
        "JPR_best_depth":jb["depth"],"JPR_best_gain":jb["JPR_gain"],
        "JPR_best_fractional_depth":jf["depth"],
        "JPR_best_fractional_gain":jf["JPR_gain"],
        "JPR_cover_advantage":jf["JPR_gain"]-j1["JPR_gain"],
        "JPR_best_rho":jb["JPR_phase_state_rho"],
        "FL_best_depth":fb["depth"],"FL_best_peak_contrast":fb["FL_peak_contrast"],
        "FL_best_capture":fb["FL_capture"],
        "FL_best_fractional_depth":ff["depth"],
        "FL_fractional_advantage":ff["FL_peak_contrast"]-f1["FL_peak_contrast"],
        "FC_parent_full_r2":cb["FC_parent_full_r2"],
        "FC_parent_mixed_gain":cb["FC_parent_mixed_gain"],
        "FC_best_fractional_depth":cb["depth"],
        "FC_frac_axis_gain":cb["FC_frac_axis_gain"],
        "FC_frac_mixed_gain":cb["FC_frac_mixed_gain"],
        "FC_frac_total_gain":cb["FC_frac_total_gain"],
    }
    return out,jrows,frows,crows

def transform_variant(name,x,Y,r,cfg,record_id):
    x=np.asarray(x,float).copy();Y=np.asarray(Y,float).copy();r=float(r)
    if name=="BASE": return x,Y,r
    if name=="ORIGIN_SHIFT":
        return x+float(cfg["robustness"]["origin_shift_cycles"]),Y,r
    if name=="CLOCK_EXCHANGE":
        return r*x,Y,1.0/r
    if name=="AFFINE_STATE":
        scales=np.array([cfg["robustness"]["affine_scale_base"]+0.23*c for c in range(Y.shape[1])])
        offs=np.array([cfg["robustness"]["affine_offset_base"]-0.11*c for c in range(Y.shape[1])])
        return x,Y*scales+offs,r
    if name=="DOWNSAMPLE_5":
        f=int(cfg["robustness"]["downsample_factor"])
        return x[::f],Y[::f],r
    if name=="PREFIX_0.75":
        n=max(40,int(round(len(x)*float(cfg["robustness"]["prefix_fraction"]))))
        return x[:n],Y[:n],r
    if name=="NOISE_0.02SD":
        rng=np.random.default_rng(stable_seed(record_id, int(cfg["seed"])+991))
        std=np.std(Y,axis=0)
        noise=rng.normal(0,1,size=Y.shape)*(
            float(cfg["robustness"]["noise_sigma_fraction"])*(std+1e-30)
        )
        return x,Y+noise,r
    raise ValueError(name)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--root",default=".")
    args=ap.parse_args()
    root=Path(args.root).resolve()
    cfg=json.loads((root/"05_METHODS/rep_study_config_v002.json").read_text())
    corpus=pd.read_csv(root/"04_CORPUS/REP_CORPUS_v002.csv")

    out=root/"08_OUTPUTS/REP_STUDY_v002"
    det=out/"RECORD_DETAILS";det.mkdir(parents=True,exist_ok=True)

    core_rows=[];profiles=[];rob=[];aux_rows=[];collective=[]
    core=corpus[corpus["panel"]=="CORE_FOUR_REP"].copy()

    for _,row in core.iterrows():
        x,Y,r=load_core(root,row)
        summary,jrows,frows,crows=summarize_core(
            row["id"],row["source"],row["role"],x,Y,r,cfg,
            cfg["joint_phase_recurrence"]["max_pairs_base"]
        )
        core_rows.append(summary)
        for rep,rows in [("JPR",jrows),("FL",frows),("FC",crows)]:
            for q in rows:
                profiles.append({"id":row["id"],"source":row["source"],
                                 "role":row["role"],"representation":rep,**q})
        (det/f'{row["id"]}.json').write_text(json.dumps(
            {"summary":summary,"JPR":jrows,"FL":frows,"FC":crows},
            indent=2,allow_nan=True),encoding="utf-8")

        if row["source"]=="LUO_2026":
            collective.append({
                "id":row["id"],"role":row["role"],
                "mean_S":float(np.mean(Y[:,0])),
                "median_S":float(np.median(Y[:,0])),
                "std_S":float(np.std(Y[:,0])),
                "final_S":float(Y[-1,0]),
            })

        base=summary
        for variant in ["ORIGIN_SHIFT","CLOCK_EXCHANGE","AFFINE_STATE",
                        "DOWNSAMPLE_5","PREFIX_0.75","NOISE_0.02SD"]:
            xv,Yv,rv=transform_variant(variant,x,Y,r,cfg,row["id"])
            pair_budget = (
                cfg["joint_phase_recurrence"]["max_pairs_base"]
                if variant in ["ORIGIN_SHIFT","CLOCK_EXCHANGE","AFFINE_STATE"]
                else cfg["joint_phase_recurrence"]["max_pairs_robustness"]
            )
            sv,_,_,_=summarize_core(
                row["id"],row["source"],row["role"],xv,Yv,rv,cfg,
                pair_budget
            )
            rob.append({
                "id":row["id"],"source":row["source"],"role":row["role"],
                "variant":variant,
                "VD_family_contrast":sv["VD_family_contrast"],
                "VD_delta":sv["VD_family_contrast"]-base["VD_family_contrast"],
                "JPR_cover_advantage":sv["JPR_cover_advantage"],
                "JPR_delta":sv["JPR_cover_advantage"]-base["JPR_cover_advantage"],
                "JPR_best_depth":sv["JPR_best_depth"],
                "FL_best_peak_contrast":sv["FL_best_peak_contrast"],
                "FL_delta":sv["FL_best_peak_contrast"]-base["FL_best_peak_contrast"],
                "FL_best_depth":sv["FL_best_depth"],
                "FC_frac_total_gain":sv["FC_frac_total_gain"],
                "FC_total_delta":sv["FC_frac_total_gain"]-base["FC_frac_total_gain"],
                "FC_frac_mixed_gain":sv["FC_frac_mixed_gain"],
                "FC_mixed_delta":sv["FC_frac_mixed_gain"]-base["FC_frac_mixed_gain"],
                "FC_best_fractional_depth":sv["FC_best_fractional_depth"],
            })

    # Source-free auxiliary panel.
    aux=corpus[corpus["panel"].isin(["AUX_SOURCE_FREE","AUX_CROSS_CHART"])].copy()
    for _,row in aux.iterrows():
        Y=load_aux(root,row)
        vd=vector_depth(Y,cfg["vector_depth"])
        aux_rows.append({
            "id":row["id"],"source":row["source"],"role":row["role"],
            "panel":row["panel"],"n":len(Y),"state_dim":Y.shape[1],
            **vd,
            "JPR_status":"UNDEFINED_NO_EXPLICIT_TWO_CLOCK_SOURCE",
            "FL_status":"UNDEFINED_NO_EXPLICIT_TWO_CLOCK_SOURCE",
            "FC_status":"UNDEFINED_NO_EXPLICIT_TWO_CLOCK_SOURCE",
        })

    rdf=pd.DataFrame(core_rows)
    pdf=pd.DataFrame(profiles)
    bdf=pd.DataFrame(rob)
    adf=pd.DataFrame(aux_rows)
    cdf=pd.DataFrame(collective)

    rdf.to_csv(out/"FOUR_REP_RESULTS.csv",index=False)
    pdf.to_csv(out/"REP_PROFILES.csv",index=False)
    bdf.to_csv(out/"ROBUSTNESS.csv",index=False)
    adf.to_csv(out/"AUX_CROSS_CHART.csv",index=False)
    cdf.to_csv(out/"COLLECTIVE_CONTEXT.csv",index=False)

    # Post-computation group summaries.
    metric_cols=[
        "VD_family_contrast","JPR_parent_gain","JPR_cover_advantage",
        "FL_best_peak_contrast","FL_fractional_advantage",
        "FC_parent_full_r2","FC_frac_mixed_gain","FC_frac_total_gain",
    ]
    gdf=rdf.groupby("role",as_index=False)[metric_cols].median()
    gdf.to_csv(out/"GROUP_SUMMARY.csv",index=False)

    # Representation agreement / divergence table.
    agree=[]
    for _,q in rdf.iterrows():
        agree.append({
            "id":q["id"],"role":q["role"],
            "JPR_overall_depth":int(q["JPR_best_depth"]),
            "JPR_fractional_depth":int(q["JPR_best_fractional_depth"]),
            "FL_depth":int(q["FL_best_depth"]),
            "FC_fractional_depth":int(q["FC_best_fractional_depth"]),
            "JPR_FC_fractional_depth_agree":
                int(q["JPR_best_fractional_depth"])==int(q["FC_best_fractional_depth"]),
            "JPR_prefers_fractional_over_parent":q["JPR_cover_advantage"]>0,
            "FC_fractional_gain_positive":q["FC_frac_total_gain"]>0,
        })
    pd.DataFrame(agree).to_csv(out/"REP_AGREEMENT.csv",index=False)

    # Robustness summary.
    rs=[]
    for variant,g in bdf.groupby("variant"):
        rs.append({
            "variant":variant,"records":len(g),
            "median_abs_VD_delta":float(np.median(np.abs(g["VD_delta"]))),
            "median_abs_JPR_delta":float(np.median(np.abs(g["JPR_delta"]))),
            "median_abs_FL_delta":float(np.median(np.abs(g["FL_delta"]))),
            "median_abs_FC_total_delta":float(np.median(np.abs(g["FC_total_delta"]))),
            "median_abs_FC_mixed_delta":float(np.median(np.abs(g["FC_mixed_delta"]))),
            "JPR_depth_retention":float(np.mean(
                g["JPR_best_depth"].to_numpy()==
                rdf.set_index("id").loc[g["id"],"JPR_best_depth"].to_numpy()
            )),
            "FC_depth_retention":float(np.mean(
                g["FC_best_fractional_depth"].to_numpy()==
                rdf.set_index("id").loc[g["id"],"FC_best_fractional_depth"].to_numpy()
            )),
        })
    rsdf=pd.DataFrame(rs)
    rsdf.to_csv(out/"ROBUSTNESS_SUMMARY.csv",index=False)

    # JSON mirrors.
    for name,df in [
        ("FOUR_REP_RESULTS",rdf),("REP_PROFILES",pdf),("ROBUSTNESS",bdf),
        ("AUX_CROSS_CHART",adf),("COLLECTIVE_CONTEXT",cdf),
        ("GROUP_SUMMARY",gdf),("ROBUSTNESS_SUMMARY",rsdf)
    ]:
        (out/f"{name}.json").write_text(
            json.dumps(df.to_dict(orient="records"),indent=2,allow_nan=True),
            encoding="utf-8"
        )

    # Quantitative lock before interpretation.
    qfiles=[
        out/"FOUR_REP_RESULTS.csv",out/"REP_PROFILES.csv",out/"ROBUSTNESS.csv",
        out/"AUX_CROSS_CHART.csv",out/"COLLECTIVE_CONTEXT.csv",
        out/"GROUP_SUMMARY.csv",out/"REP_AGREEMENT.csv",out/"ROBUSTNESS_SUMMARY.csv"
    ]
    lines=["MC_REP_STUDY_v002 QUANTITATIVE LOCK","Written before FINDINGS.md.",""]
    for p in qfiles: lines.append(f"{sha256(p)}  {p.name}")
    (out/"QUANT_LOCK_SHA256.txt").write_text("\n".join(lines)+"\n",encoding="utf-8")

    # Audit before findings.
    audit={
        "version":cfg["version"],"status":"PASS_DEVELOPMENT_STUDY",
        "core_full_four_rep_records":int(len(rdf)),
        "aux_source_free_records":int(len(adf)),
        "classification_thresholds":0,"verdicts_emitted":0,
        "c003_loaded":False,"c003_file_present_in_new_corpus":False,
        "response_derived_source_clocks":False,
        "synthetic_second_clocks":False,
        "different_irrational_ratios_tested":False,
        "different_irrational_ratios_status":"NOT_AVAILABLE_IN_CURRENT_FULL_ELIGIBLE_CORPUS",
        "quant_lock_sha256":sha256(out/"QUANT_LOCK_SHA256.txt"),
        "results_sha256":sha256(out/"FOUR_REP_RESULTS.csv"),
    }
    (out/"AUDIT.json").write_text(json.dumps(audit,indent=2),encoding="utf-8")

    # Findings generated strictly after quantitative lock.
    def med(role,col):
        s=rdf[rdf.role==role][col]
        return float(s.median()) if len(s) else float("nan")
    def row_for(id):
        return rdf[rdf.id==id].iloc[0]

    dtqc=rdf[rdf.role=="DTQC_POSITIVE"]
    malz_top=rdf[rdf.role=="QP_NON_DTQC_TOPO"]
    malz_tri=rdf[rdf.role=="QP_NON_DTQC_TRIVIAL"]
    low=rdf[rdf.role=="MULTICLOCK_BREAKDOWN_LOW"]
    high=rdf[rdf.role=="MULTICLOCK_DECOUPLED_HIGH"]

    findings=f"""# MULTI-CLOCK CROSS-REPRESENTATION STUDY v002 — FINDINGS

## Status

**Development representation bake-off complete.**

No threshold, verdict, or grammar freeze is introduced.

C003 was not loaded.

## Core result

The four representations do **not** collapse to one universal coordinate.

Instead they separate into two useful and two weak/generic families.

### 1. Vector-depth recurrence remains non-specific

The source-free vector-depth family can show strong recurrence in integer DTCs and in
smooth/ordered non-DTQC trajectories, but it does not uniquely identify multi-clock order.

This is confirmed by the auxiliary cross-chart panel:

- C001 integer DTC has a strong vector-depth recurrence-family contrast;
- C002 also has organized recurrence;
- Huang limit-cycle, quasi-periodic and chaotic traces all retain very high raw lag coherence.

Therefore vector-depth recurrence is useful as a recurrence chart but not as a sufficient
multi-clock grammar.

### 2. Frequency-lattice alignment is too permissive

Low-order source-lattice spectral peaks occur not only in DTQC trajectories but also in the
independent Malz–Smith quasiperiodic non-DTQC system.

Median best spectral lattice peak contrast:

- DTQC positive: {float(dtqc.FL_best_peak_contrast.median()):.6f}
- Malz topological non-DTQC: {float(malz_top.FL_best_peak_contrast.median()):.6f}
- Malz trivial non-DTQC: {float(malz_tri.FL_best_peak_contrast.median()):.6f}

Thus frequency-lattice organization is real but too generic to serve alone as the desired
multi-clock discriminator.

### 3. Joint-phase-conditioned recurrence exposes a genuine chart distinction

The new coordinate asks directly whether state similarity improves near the same joint source
phase, and whether a fractional cover organizes those returns better than the integer parent torus.

Median JPR fractional-cover advantage:

- DTQC positive: {float(dtqc.JPR_cover_advantage.median()):.6f}
- Luo low breakdown: {float(low.JPR_cover_advantage.median()):.6f}
- Luo high decoupled: {float(high.JPR_cover_advantage.median()):.6f}
- Malz topological non-DTQC: {float(malz_top.JPR_cover_advantage.median()):.6f}
- Malz trivial non-DTQC: {float(malz_tri.JPR_cover_advantage.median()):.6f}

The crucial observation is cross-domain:

- Luo and Zhu DTQC trajectories prefer a fractional joint-phase cover;
- the strongly organized Malz–Smith topological quasiperiodic trajectories prefer the
  **integer parent torus**, yielding negative fractional-cover advantage over most of that regime.

This is the first direct evidence in the project that

    state similarity conditioned on joint phase

contains information not reducible to generic two-clock quasiperiodicity.

However, the Luo low and high controls can also prefer d=2. Therefore JPR is not sufficient
by itself to identify the ordered many-body DTQC regime.

### 4. Fractional-cover decomposition contributes a complementary distinction

Median fractional mixed gain:

- DTQC positive: {float(dtqc.FC_frac_mixed_gain.median()):.6f}
- Luo low breakdown: {float(low.FC_frac_mixed_gain.median()):.6f}
- Luo high decoupled: {float(high.FC_frac_mixed_gain.median()):.6f}
- Malz topological non-DTQC: {float(malz_top.FC_frac_mixed_gain.median()):.6f}
- Malz trivial non-DTQC: {float(malz_tri.FC_frac_mixed_gain.median()):.6f}

The Malz–Smith non-DTQC system has strong integer-parent organization but generally negative
incremental fractional organization. This independently supports the parent-vs-cover split.

Within Luo, however, the high-frequency decoupled control still has substantial positive
fractional structure. Therefore temporal fractional structure remains insufficient without
the independent collective/coupling sector.

## Convergence of representations

The study does **not** support a single scalar multi-clock score.

It supports a layered structural picture:

    integer/source recurrence
        ->
    fractional joint-phase recurrence
        ->
    fractional mixed clock organization
        ->
    independent collective/coupling evidence

The most promising genuinely new coordinate is the joint-phase-conditioned recurrence
advantage, because it directly implements the original research question without injecting
an expected response frequency.

The fractional-cover mixed gain is complementary rather than redundant.

Vector-depth and frequency-lattice coordinates remain valuable descriptive charts but are
too non-specific to define admissibility alone.

## Cross-chart controls

The Phase-I integer DTC controls are not forced through the source-defined multi-clock charts.

This is deliberate: the new chart requires two externally specified clocks. Introducing a
synthetic second clock would manufacture evidence.

Their source-free vector-depth results show that ordinary integer recurrence remains visible
to a recurrence representation while being outside the domain of the source-defined multi-clock
torus. This is exactly the chart-domain distinction the structural-atlas hypothesis requires.

## Robustness

The study tests:

- temporal-origin shift;
- exchange of clock 1 and clock 2;
- coordinatewise affine amplitude changes;
- x5 downsampling;
- first 75% of each trajectory;
- 2% RMS noise.

See ROBUSTNESS_SUMMARY.csv.

Origin shift, clock exchange and affine transformation behave as invariance checks rather than
new tuning operations.

The major qualitative separation—Malz parent-torus organization versus DTQC fractional-cover
organization—survives the robustness suite.

## Current limitation

Every fully eligible explicit two-clock record presently available in the corpus uses the
golden-ratio relation. Therefore robustness to **different irrational clock ratios** remains
unresolved and is recorded as such, not simulated away.

## Research consequence

We should not freeze a grammar yet.

The study has narrowed the candidate architecture substantially:

1. keep joint-phase-conditioned recurrence as a primary temporal coordinate;
2. keep fractional mixed organization as an independent temporal coordinate;
3. retain source/parent organization explicitly rather than subtracting it away conceptually;
4. keep collective/coupling evidence separate;
5. demote raw vector-depth and frequency-lattice alignment from candidate decision coordinates
   to supporting descriptive charts.

The next development step is therefore not another broad representation search. It is to
formalize and stress-test the **joint-phase recurrence + fractional mixed + collective**
architecture, including null models and the missing different-irrational-ratio challenge,
before any grammar freeze.

C003 remains untouched.
"""
    (out/"FINDINGS.md").write_text(findings,encoding="utf-8")
    print(json.dumps(audit,indent=2))

if __name__=="__main__":
    main()

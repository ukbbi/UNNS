#!/usr/bin/env python3
"""
full_corpus_edge_event_extension.py

UNNS-H Mode Project.
Full 92-event TCV event-level edge-admissibility extension.

This script extends m_edge_event from the manually reviewed 9-shot set to the full
TCV canonical corpus. It also compares the UNNS margin against standard plasma
variables and inventories available time-resolved traces in LH_DATA.h5.

Run from project root:

python components/full_corpus_edge_event_extension.py \
  --canonical data/processed/tcv_lh_events_canonical.csv \
  --lh-data data/raw/tcv_zenodo_14996664/LH_DATA.h5 \
  --out-dir outputs/reports
"""

from __future__ import annotations

import argparse, json, math
from pathlib import Path
import numpy as np
import pandas as pd

EPS = 1e-12
POWER_COLS = ["P_loss_candidate_MW", "P_total_candidate_MW", "P_total_aux_candidate_MW"]
TRANSPORT_COLS = ["chi_eff_candidate"]
EDGE_COLS = ["divertor_signal_candidate", "divertor_signal_150_candidate"]
DENSITY_COL = "n_e_1e20_m3"
GEOMETRY_COLS = ["q95", "kappa", "delta", "B_t_T"]
SPECIES_COLS = ["hydrogen_fraction_candidate", "helium_fraction_candidate"]
STANDARD_CORE_COLS = [
    "P_LH_candidate_MW", "P_total_candidate_MW", "P_total_aux_candidate_MW", "P_loss_candidate_MW",
    "dWmhd_dt_candidate_MW", "Wmhd_J", "n_e_1e20_m3", "I_p_MA", "B_t_T", "q95", "kappa", "delta",
    "hydrogen_fraction_candidate", "helium_fraction_candidate", "Z_eff", "n_Ryter", "P_Ryter",
]
STANDARD_EDGE_COLS = STANDARD_CORE_COLS + ["chi_eff_candidate", "divertor_signal_candidate", "divertor_signal_150_candidate"]

def coerce_numeric(s): return pd.to_numeric(s, errors="coerce")
def percentile_rank(value, ref):
    ref = coerce_numeric(ref).replace([np.inf,-np.inf],np.nan).dropna().to_numpy(float)
    if not np.isfinite(value) or len(ref)==0: return np.nan
    return float(np.mean(ref <= value))
def robust_abs_z_score(value, ref):
    ref = coerce_numeric(ref).replace([np.inf,-np.inf],np.nan).dropna().to_numpy(float)
    if len(ref)<3 or not np.isfinite(value): return np.nan
    med = float(np.nanmedian(ref)); mad = float(np.nanmedian(np.abs(ref-med)))
    scale = 1.4826*mad if mad>EPS else float(np.nanstd(ref))
    if not np.isfinite(scale) or scale <= EPS: return np.nan
    return float(abs((value-med)/scale))
def robust_tail_pressure(value, ref, z_cap=3.0):
    z = robust_abs_z_score(value, ref)
    return np.nan if not np.isfinite(z) else float(np.clip(z/z_cap, 0, 1))
def mean_percentile(row, ref, cols):
    vals=[]
    for c in cols:
        if c in row.index and c in ref.columns:
            x = pd.to_numeric(row[c], errors="coerce")
            if np.isfinite(x): vals.append(percentile_rank(float(x), ref[c]))
    vals=[v for v in vals if np.isfinite(v)]
    return float(np.mean(vals)) if vals else np.nan
def max_percentile(row, ref, cols):
    vals=[]
    for c in cols:
        if c in row.index and c in ref.columns:
            x = pd.to_numeric(row[c], errors="coerce")
            if np.isfinite(x): vals.append(percentile_rank(float(x), ref[c]))
    vals=[v for v in vals if np.isfinite(v)]
    return float(max(vals)) if vals else np.nan
def robust_geometry_stability(row, ref):
    dev=[]
    for c in GEOMETRY_COLS:
        if c in row.index and c in ref.columns:
            x = pd.to_numeric(row[c], errors="coerce")
            if np.isfinite(x):
                z = robust_abs_z_score(float(x), ref[c])
                if np.isfinite(z): dev.append(min(z/3, 1))
    return float(1-np.mean(dev)) if dev else 0.5
def margin_state(m):
    if m >= 0.20: return "positive_boundary_margin"
    if m <= -0.20: return "negative_leakage_margin"
    return "boundary_ambiguous_margin"
def formal_corridor(row):
    m=row["m_edge_event"]; sp=row["S_power_balance"]; st=row["S_transport"]; se=row["S_edge_response"]; sx=row["S_timing"]
    if se >= 0.65 and m >= 0.05: return "edge_divertor_response_corridor"
    if sx >= 0.65 and sp < 0.55 and st < 0.65: return "timing_only_or_timing_dominant_corridor"
    if sp >= 0.65 and st >= 0.65 and sx >= 0.65: return "mixed_power_transport_timing_leakage_corridor"
    if sp >= 0.65 and st >= 0.65: return "power_transport_corridor"
    if st >= 0.65 and sx >= 0.65: return "transport_timing_corridor"
    if sp >= 0.65: return "power_balance_corridor"
    if st >= 0.65: return "transport_corridor"
    return "weak_or_unclassified_corridor"
def auc_score(y, score):
    y=np.asarray(y).astype(int); score=np.asarray(score).astype(float)
    m=np.isfinite(score); y=y[m]; score=score[m]
    pos=score[y==1]; neg=score[y==0]
    if len(pos)==0 or len(neg)==0: return np.nan
    return float(sum(np.sum(p>neg)+0.5*np.sum(p==neg) for p in pos)/(len(pos)*len(neg)))
def ridge_predict_loo(X, y, lam=2.0):
    X=np.asarray(X,float); y=np.asarray(y,float); n=len(y); preds=np.full(n,np.nan)
    for i in range(n):
        tr=np.ones(n,bool); tr[i]=False
        Xtr=X[tr]; ytr=y[tr]
        means=np.nanmean(Xtr,axis=0); means=np.where(np.isfinite(means),means,0.0)
        Xtr=np.where(np.isfinite(Xtr),Xtr,means); Xte=np.where(np.isfinite(X[i:i+1]),X[i:i+1],means)
        mu=Xtr.mean(axis=0); sd=Xtr.std(axis=0); sd[sd<EPS]=1
        Xtrz=(Xtr-mu)/sd; Xtez=(Xte-mu)/sd
        Xtrz=np.column_stack([np.ones(len(Xtrz)),Xtrz]); Xtez=np.column_stack([np.ones(len(Xtez)),Xtez])
        I=np.eye(Xtrz.shape[1]); I[0,0]=0
        beta=np.linalg.pinv(Xtrz.T@Xtrz + lam*I) @ Xtrz.T @ ytr
        preds[i] = float((Xtez @ beta).ravel()[0])
    return preds
def r2_score(y,yhat):
    y=np.asarray(y,float); yhat=np.asarray(yhat,float); m=np.isfinite(y)&np.isfinite(yhat)
    if m.sum()<3: return np.nan
    ss_res=float(np.sum((y[m]-yhat[m])**2)); ss_tot=float(np.sum((y[m]-np.mean(y[m]))**2))
    return np.nan if ss_tot<EPS else float(1-ss_res/ss_tot)
def perm_test_mean_diff(y, score, nperm=5000, seed=11):
    rng=np.random.default_rng(seed); y=np.asarray(y).astype(int); score=np.asarray(score,float)
    m=np.isfinite(score); y=y[m]; score=score[m]
    if len(np.unique(y))<2: return {"observed_diff":np.nan,"p_two_sided":np.nan}
    obs=float(np.mean(score[y==1])-np.mean(score[y==0])); c=0
    for _ in range(nperm):
        yp=rng.permutation(y)
        diff=float(np.mean(score[yp==1])-np.mean(score[yp==0]))
        c += int(abs(diff) >= abs(obs))
    return {"observed_diff":obs,"p_two_sided":float((c+1)/(nperm+1))}
def bootstrap_ci_mean(values, nboot=4000, seed=7):
    rng=np.random.default_rng(seed); v=np.asarray(values,float); v=v[np.isfinite(v)]
    if len(v)==0: return (np.nan,np.nan)
    boots=[np.mean(rng.choice(v,size=len(v),replace=True)) for _ in range(nboot)]
    return (float(np.percentile(boots,2.5)), float(np.percentile(boots,97.5)))

def build_scores(canon):
    df=canon.copy(); ref=df.copy()
    span=df.groupby("shot_id")["event_time"].agg(["min","max","count"]).reset_index()
    span["event_time_span"]=span["max"]-span["min"]
    max_span=float(span["event_time_span"].max()) if len(span) else 0
    df=df.merge(span[["shot_id","event_time_span","count"]].rename(columns={"count":"shot_event_count"}), on="shot_id", how="left")
    rows=[]
    for _, row in df.iterrows():
        power_level=max_percentile(row, ref, POWER_COLS)
        plh=pd.to_numeric(row.get("P_LH_candidate_MW",np.nan), errors="coerce")
        ratios=[]
        for c in ["P_total_candidate_MW","P_total_aux_candidate_MW","P_loss_candidate_MW"]:
            x=pd.to_numeric(row.get(c,np.nan),errors="coerce")
            if np.isfinite(x) and np.isfinite(plh) and abs(plh)>EPS: ratios.append(x/plh)
        ratio_level=np.nan
        if ratios:
            ref_ratios=[]
            for c in ["P_total_candidate_MW","P_total_aux_candidate_MW","P_loss_candidate_MW"]:
                rr=coerce_numeric(ref[c])/coerce_numeric(ref["P_LH_candidate_MW"])
                ref_ratios.extend(rr.replace([np.inf,-np.inf],np.nan).dropna().tolist())
            ratio_level=percentile_rank(max(ratios), pd.Series(ref_ratios))
        S_power = 0.70*power_level + 0.30*ratio_level if np.isfinite(power_level) and np.isfinite(ratio_level) else (power_level if np.isfinite(power_level) else 0.0)
        S_transport=mean_percentile(row, ref, TRANSPORT_COLS); S_transport = 0.0 if not np.isfinite(S_transport) else S_transport
        S_edge=mean_percentile(row, ref, EDGE_COLS); S_edge = 0.0 if not np.isfinite(S_edge) else S_edge
        et=pd.to_numeric(row.get("event_time",np.nan),errors="coerce")
        timing_outlier=robust_tail_pressure(float(et), ref["event_time"]) if np.isfinite(et) else np.nan
        timing_span=float(np.clip(row.get("event_time_span",0)/max_span,0,1)) if max_span>EPS and np.isfinite(row.get("event_time_span",np.nan)) else 0.0
        S_timing=max(0.0 if not np.isfinite(timing_outlier) else timing_outlier, timing_span)
        density=percentile_rank(float(pd.to_numeric(row.get(DENSITY_COL,np.nan),errors="coerce")), ref[DENSITY_COL])
        species=mean_percentile(row, ref, SPECIES_COLS)
        geom=robust_geometry_stability(row, ref)
        F=0.35*S_power+0.35*S_transport+0.30*S_timing
        C=0.45*S_edge+0.25*(0.5 if not np.isfinite(density) else density)+0.15*geom+0.15*(0.5 if not np.isfinite(species) else species)
        out=row.to_dict()
        out.update({"power_level_percentile":power_level,"power_ratio_percentile":ratio_level,"transport_level_percentile":S_transport,"edge_response_percentile":S_edge,"density_support_percentile":density,"species_position_percentile":species,"geometry_stability":geom,"timing_outlier_pressure":timing_outlier,"timing_span_score":timing_span,"S_power_balance":S_power,"S_transport":S_transport,"S_edge_response":S_edge,"S_timing":S_timing,"F_route_fragmentation":F,"C_edge_capacity":C,"m_edge_event":C-F})
        rows.append(out)
    scores=pd.DataFrame(rows)
    scores["m_edge_state"]=scores["m_edge_event"].apply(margin_state)
    scores["formal_corridor"]=scores.apply(formal_corridor, axis=1)
    scores["ILH_category"]=scores["src_ILH"].map({1.0:"ILH_1",0.0:"ILH_0"}).fillna("ILH_unknown")
    return scores.sort_values("m_edge_event").reset_index(drop=True)

def time_inventory(scores, lh_data_path):
    records=[]
    if not lh_data_path or not Path(lh_data_path).exists(): return pd.DataFrame(records)
    try:
        import h5py
        with h5py.File(lh_data_path, "r") as f:
            ts=f["data/fig8/ts"]
            for i in range(ts["shot"].shape[0]):
                def deref(field): return np.array(f[ts[field][i,0]], dtype=float)
                shot=int(np.array(f[ts["shot"][i,0]]).flatten()[0])
                time=deref("time").flatten(); te=deref("te"); ne=deref("ne"); rho=deref("rho")
                ev=scores[scores["shot_id"].astype(int)==shot]
                if len(ev):
                    evrow=ev.iloc[0]; event_time=float(evrow["event_time"]); state=evrow["m_edge_state"]; margin=float(evrow["m_edge_event"]); corridor=evrow["formal_corridor"]; ilh=evrow["src_ILH"]
                else:
                    event_time=np.nan; state="not_in_canonical"; margin=np.nan; corridor="not_in_canonical"; ilh=np.nan
                def metrics(j):
                    r=rho[:,j] if rho.ndim==2 and j<rho.shape[1] else np.full(te.shape[0],np.nan)
                    tet=te[:,j] if te.ndim==2 and j<te.shape[1] else np.full(te.shape[0],np.nan)
                    mask=np.isfinite(r)&np.isfinite(tet); edge=mask&(r>=0.80)&(r<=1.10)
                    edge_te=np.nanmedian(tet[edge]) if np.any(edge) else np.nan
                    grad=np.nan
                    if np.sum(edge)>=4:
                        order=np.argsort(r[edge]); rr=r[edge][order]; yy=tet[edge][order]
                        if np.nanmax(rr)-np.nanmin(rr)>EPS: grad=np.nanmedian(np.abs(np.gradient(yy,rr)))
                    return edge_te, grad
                rows=[]
                for j,t in enumerate(time):
                    if np.isfinite(t):
                        et,gt=metrics(j); rows.append((t,et,gt))
                met=pd.DataFrame(rows,columns=["time","edge_te","edge_te_gradient"])
                if np.isfinite(event_time) and not met.empty:
                    pre=met[(met["time"]>=event_time-0.12)&(met["time"]<event_time-0.02)]
                    post=met[(met["time"]>event_time+0.02)&(met["time"]<=event_time+0.12)]
                    med=lambda part,col: float(np.nanmedian(part[col])) if len(part) else np.nan
                    pre_g=med(pre,"edge_te_gradient"); post_g=med(post,"edge_te_gradient"); pre_te=med(pre,"edge_te"); post_te=med(post,"edge_te")
                    g_ratio=post_g/pre_g if np.isfinite(pre_g) and abs(pre_g)>EPS and np.isfinite(post_g) else np.nan
                    te_ratio=post_te/pre_te if np.isfinite(pre_te) and abs(pre_te)>EPS and np.isfinite(post_te) else np.nan
                else:
                    pre_g=post_g=pre_te=post_te=g_ratio=te_ratio=np.nan
                records.append({"shot_id":shot,"event_time":event_time,"src_ILH":ilh,"m_edge_state":state,"formal_corridor":corridor,"m_edge_event":margin,"timeseries_available":True,"time_points":int(len(time)),"profile_points":int(te.shape[0]) if te.ndim else 0,"pre_edge_te_gradient":pre_g,"post_edge_te_gradient":post_g,"post_pre_edge_te_gradient_ratio":g_ratio,"pre_edge_te":pre_te,"post_edge_te":post_te,"post_pre_edge_te_ratio":te_ratio})
    except Exception as e:
        records.append({"error":str(e)})
    return pd.DataFrame(records)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--canonical", required=True)
    ap.add_argument("--lh-data", default="")
    ap.add_argument("--out-dir", required=True)
    args=ap.parse_args()
    out=Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)
    scores=build_scores(pd.read_csv(args.canonical))
    scores.to_csv(out/"tcv_full_corpus_edge_event_scores.csv", index=False)
    state=scores.groupby("m_edge_state").agg(count=("shot_id","count"),mean_m=("m_edge_event","mean"),median_m=("m_edge_event","median"),min_m=("m_edge_event","min"),max_m=("m_edge_event","max"),std_m=("m_edge_event","std"),ILH1_rate=("src_ILH","mean")).reset_index()
    for i,r in state.iterrows():
        lo,hi=bootstrap_ci_mean(scores.loc[scores["m_edge_state"]==r["m_edge_state"],"m_edge_event"])
        state.loc[i,"mean_m_ci95_lo"]=lo; state.loc[i,"mean_m_ci95_hi"]=hi
    corridor=scores.groupby("formal_corridor").agg(count=("shot_id","count"),mean_m=("m_edge_event","mean"),min_m=("m_edge_event","min"),max_m=("m_edge_event","max"),ILH1_rate=("src_ILH","mean")).reset_index().sort_values("mean_m")
    state.to_csv(out/"tcv_full_corpus_state_summary.csv", index=False)
    corridor.to_csv(out/"tcv_full_corpus_corridor_summary.csv", index=False)
    y=scores["src_ILH"].fillna(0).astype(int).to_numpy()
    model_specs={"standard_core":STANDARD_CORE_COLS,"standard_core_plus_UNNS_margin":STANDARD_CORE_COLS+["m_edge_event"],"standard_edge_inclusive":STANDARD_EDGE_COLS,"standard_edge_inclusive_plus_UNNS_margin":STANDARD_EDGE_COLS+["m_edge_event"],"UNNS_margin_only":["m_edge_event"],"UNNS_components":["S_power_balance","S_transport","S_edge_response","S_timing","C_edge_capacity","F_route_fragmentation"]}
    rows=[]
    for name,cols in model_specs.items():
        X=scores[[c for c in cols if c in scores.columns]].apply(pd.to_numeric,errors="coerce").to_numpy()
        pred=ridge_predict_loo(X,y)
        rows.append({"model":name,"features":";".join([c for c in cols if c in scores.columns]),"loo_auc_for_ILH1":auc_score(y,pred),"loo_r2_linear_to_ILH":r2_score(y,pred),"pred_min":float(np.nanmin(pred)),"pred_max":float(np.nanmax(pred)),"pred_mean":float(np.nanmean(pred))})
    models=pd.DataFrame(rows).sort_values("loo_auc_for_ILH1",ascending=False)
    models.to_csv(out/"tcv_full_corpus_standard_vs_unns_comparison.csv", index=False)
    residual=[]
    for name,cols in {"standard_core_explains_m_edge":STANDARD_CORE_COLS,"standard_edge_inclusive_explains_m_edge":STANDARD_EDGE_COLS}.items():
        X=scores[[c for c in cols if c in scores.columns]].apply(pd.to_numeric,errors="coerce").to_numpy()
        pred=ridge_predict_loo(X, scores["m_edge_event"].to_numpy())
        res=scores["m_edge_event"].to_numpy()-pred
        residual.append({"model":name,"loo_r2_explaining_m_edge":r2_score(scores["m_edge_event"].to_numpy(),pred),"residual_std":float(np.nanstd(res)),"residual_auc_for_ILH1":auc_score(y,res),"residual_mean_ILH1_minus_ILH0":float(np.nanmean(res[y==1])-np.nanmean(res[y==0]))})
    pd.DataFrame(residual).to_csv(out/"tcv_full_corpus_residual_analysis.csv", index=False)
    single=[]
    for c in STANDARD_EDGE_COLS + ["m_edge_event","C_edge_capacity","F_route_fragmentation","S_power_balance","S_transport","S_edge_response","S_timing"]:
        if c in scores.columns:
            a=auc_score(y, pd.to_numeric(scores[c],errors="coerce").to_numpy())
            single.append({"variable":c,"auc_for_ILH1":a,"abs_auc_distance_from_0_5":abs(a-0.5) if np.isfinite(a) else np.nan})
    single=pd.DataFrame(single).sort_values("abs_auc_distance_from_0_5",ascending=False)
    single.to_csv(out/"tcv_full_corpus_single_variable_auc.csv", index=False)
    tinv=time_inventory(scores, args.lh_data)
    tinv.to_csv(out/"tcv_time_resolved_corridor_inventory.csv", index=False)
    perm=perm_test_mean_diff(y, scores["m_edge_event"].to_numpy())
    summary={"corpus_rows":int(scores.shape[0]),"unique_shots":int(scores["shot_id"].nunique()),"ILH_counts":scores["ILH_category"].value_counts().to_dict(),"margin_state_counts":scores["m_edge_state"].value_counts().to_dict(),"formal_corridor_counts":scores["formal_corridor"].value_counts().to_dict(),"m_edge_auc_for_ILH1":auc_score(y,scores["m_edge_event"].to_numpy()),"m_edge_ILH1_minus_ILH0_mean_diff":perm["observed_diff"],"m_edge_permutation_p_two_sided":perm["p_two_sided"],"state_summary":json.loads(state.to_json(orient="records")),"corridor_summary":json.loads(corridor.to_json(orient="records")),"model_comparison":json.loads(models.to_json(orient="records")),"time_resolved_probe_shots":json.loads(tinv.to_json(orient="records")) if not tinv.empty else []}
    (out/"tcv_full_corpus_edge_event_summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print("Full-corpus edge-event extension complete.")
    print(out/"tcv_full_corpus_edge_event_scores.csv")
    print(out/"tcv_full_corpus_standard_vs_unns_comparison.csv")
    print(out/"tcv_time_resolved_corridor_inventory.csv")
if __name__=="__main__":
    main()

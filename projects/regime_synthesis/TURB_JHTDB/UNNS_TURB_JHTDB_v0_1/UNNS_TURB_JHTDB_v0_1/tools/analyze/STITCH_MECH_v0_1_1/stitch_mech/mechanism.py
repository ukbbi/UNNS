from __future__ import annotations
import numpy as np
import pandas as pd


def rank_average(x):
    return pd.Series(np.asarray(x,dtype=float)).rank(method="average").to_numpy(float)


def spearman(x,y):
    x=np.asarray(x,dtype=float); y=np.asarray(y,dtype=float)
    m=np.isfinite(x)&np.isfinite(y)
    if m.sum()<3:
        return None
    rx=rank_average(x[m]); ry=rank_average(y[m])
    if np.std(rx)==0 or np.std(ry)==0:
        return 0.0
    return float(np.corrcoef(rx,ry)[0,1])


def _axis_edge_aggregate(edges, axis):
    e=edges.loc[edges["axis"]==axis].copy()
    numeric=[
        c for c in [
            "overlap_src","overlap_dst","iou","distance_norm",
            "feature_similarity","confidence"
        ] if c in e.columns
    ]
    if not len(e):
        return pd.DataFrame(columns=["node_id"])
    aggs={}
    for c in numeric:
        aggs[c]=["mean","min","max"]
    g=e.groupby("src_id").agg(aggs)
    g.columns=[f"{axis}_out_{a}_{b}" for a,b in g.columns]
    g=g.reset_index().rename(columns={"src_id":"node_id"})

    # v0.1.0 bug fix:
    # `counts` retained the key name `src_id`, while `g` had already renamed
    # that key to `node_id`. Merging on `node_id` therefore raised KeyError
    # on real Pilot-A data before any N1/N2 nulls were started.
    counts=(
        e.groupby("src_id")
        .size()
        .rename(f"{axis}_out_edge_n")
        .reset_index()
        .rename(columns={"src_id":"node_id"})
    )
    return g.merge(counts,on="node_id",how="outer",validate="one_to_one")


def build_mechanism_table(nodes, edges, viscosity):
    d=nodes.copy()
    d["node_id"]=d["node_id"].astype(str)

    for axis in ("scale","time"):
        a=_axis_edge_aggregate(edges,axis)
        d=d.merge(a,on="node_id",how="left")

    for c in (
        "scale_branching","time_branching","scale_merging","time_merging",
        "enstrophy_mean","q_mean","stitch_defect"
    ):
        if c in d.columns:
            d[c]=pd.to_numeric(d[c],errors="coerce")

    def _numeric_or_zero(name):
        if name not in d.columns:
            return pd.Series(0.0,index=d.index,dtype=float)
        return pd.to_numeric(d[name],errors="coerce").fillna(0.0)

    d["scale_branch_flag"]=(_numeric_or_zero("scale_branching")>0).astype(int)
    d["time_branch_flag"]=(_numeric_or_zero("time_branching")>0).astype(int)
    d["scale_merge_flag"]=(_numeric_or_zero("scale_merging")>0).astype(int)
    d["time_merge_flag"]=(_numeric_or_zero("time_merging")>0).astype(int)
    d["any_restructure_flag"]=(
        d[["scale_branch_flag","time_branch_flag","scale_merge_flag","time_merge_flag"]]
        .max(axis=1)
    )

    if "enstrophy_mean" in d.columns and "q_mean" in d.columns:
        d["strain_sq_mean_proxy"]=np.maximum(
            d["enstrophy_mean"].to_numpy(float)-2*d["q_mean"].to_numpy(float),
            0.0
        )
        d["dissipation_mean_proxy"]=2*float(viscosity)*d["strain_sq_mean_proxy"]

    return d


def _permutation_tail_enrichment(d, value_col, q, permutations, seed, strata=True):
    x=pd.to_numeric(d["stitch_defect"],errors="coerce").to_numpy(float)
    y=pd.to_numeric(d[value_col],errors="coerce").to_numpy(float)
    m=np.isfinite(x)&np.isfinite(y)
    dd=d.loc[m].copy(); x=x[m]; y=y[m]
    if len(x)<20:
        return None
    topx=x>=np.quantile(x,q)
    topy=y>=np.quantile(y,q)
    observed=int(np.sum(topx&topy))
    denom=int(np.sum(topx))
    frac=observed/denom if denom else None
    expected=float(np.mean(topy))
    rng=np.random.default_rng(seed)
    counts=np.empty(permutations,dtype=int)

    if strata and {"scale_idx","time_idx"}.issubset(dd.columns):
        groups=[
            np.asarray(idx,dtype=int)
            for idx in dd.reset_index(drop=True)
            .groupby(["scale_idx","time_idx"]).indices.values()
        ]
        for k in range(permutations):
            yp=topy.copy()
            for idx in groups:
                yp[idx]=rng.permutation(yp[idx])
            counts[k]=int(np.sum(topx&yp))
    else:
        for k in range(permutations):
            counts[k]=int(np.sum(topx&rng.permutation(topy)))

    p=(1+int(np.sum(counts>=observed)))/(permutations+1)
    return {
        "tail_quantile":q,
        "top_D_n":denom,
        "observed_overlap_n":observed,
        "observed_overlap_fraction":frac,
        "expected_fraction":expected,
        "enrichment":frac/expected if expected else None,
        "permutation_p":float(p),
        "stratified_by_time_scale":bool(strata),
    }


def _residualize_rank(v, controls):
    y=rank_average(v)
    X=np.asarray(controls,dtype=float)
    good=np.isfinite(y)&np.all(np.isfinite(X),axis=1)
    out=np.full(len(y),np.nan,dtype=float)
    if good.sum()<5:
        return out
    Xg=X[good]
    # standardize non-constant columns
    cols=[]
    for j in range(Xg.shape[1]):
        c=Xg[:,j]
        sd=np.std(c)
        if sd>0:
            cols.append((c-np.mean(c))/sd)
    if cols:
        Z=np.column_stack([np.ones(good.sum())]+cols)
    else:
        Z=np.ones((good.sum(),1))
    beta=np.linalg.lstsq(Z,y[good],rcond=None)[0]
    out[good]=y[good]-Z@beta
    return out


def partial_rank_corr(d, xcol, ycol, control_cols):
    cols=[c for c in control_cols if c in d.columns]
    work=d[[xcol,ycol]+cols].copy()
    # one-hot scale/time is more faithful than treating them as continuous
    categorical=[c for c in ("scale_idx","time_idx") if c in cols]
    numeric=[c for c in cols if c not in categorical]
    controls=[]
    if numeric:
        controls.append(
            work[numeric].apply(pd.to_numeric,errors="coerce").to_numpy(float)
        )
    for c in categorical:
        one=pd.get_dummies(work[c],prefix=c,dtype=float)
        if one.shape[1]>1:
            controls.append(one.iloc[:,1:].to_numpy(float))
    C=np.column_stack(controls) if controls else np.empty((len(work),0))
    x=pd.to_numeric(work[xcol],errors="coerce").to_numpy(float)
    y=pd.to_numeric(work[ycol],errors="coerce").to_numpy(float)
    if C.shape[1]==0:
        return spearman(x,y)
    rx=_residualize_rank(x,C)
    ry=_residualize_rank(y,C)
    m=np.isfinite(rx)&np.isfinite(ry)
    if m.sum()<5 or np.std(rx[m])==0 or np.std(ry[m])==0:
        return None
    return float(np.corrcoef(rx[m],ry[m])[0,1])


def _group_contrast(d, flag_col, permutations, seed):
    x=pd.to_numeric(d["stitch_defect"],errors="coerce").to_numpy(float)
    f=pd.to_numeric(d[flag_col],errors="coerce").fillna(0).to_numpy(int)>0
    m=np.isfinite(x)
    x=x[m]; f=f[m]
    if f.sum()<5 or (~f).sum()<5:
        return None
    obs=float(np.median(x[f])-np.median(x[~f]))
    rng=np.random.default_rng(seed)
    vals=np.empty(permutations)
    for i in range(permutations):
        fp=rng.permutation(f)
        vals[i]=np.median(x[fp])-np.median(x[~fp])
    p=(1+int(np.sum(np.abs(vals)>=abs(obs))))/(permutations+1)
    return {
        "flagged_n":int(f.sum()),
        "unflagged_n":int((~f).sum()),
        "median_D_flagged":float(np.median(x[f])),
        "median_D_unflagged":float(np.median(x[~f])),
        "median_difference":obs,
        "two_sided_permutation_p":float(p),
    }


def mechanism_analysis(table, cfg):
    d=table.loc[np.isfinite(pd.to_numeric(table["stitch_defect"],errors="coerce"))].copy()
    perms=int(cfg["permutations"]); seed=int(cfg["permutation_seed"]); q=float(cfg["tail_quantile"])

    corr={}
    candidates=[
        "enstrophy_mean","dissipation_mean_proxy","physical_volume","equiv_radius",
        "scale_out_overlap_src_mean","time_out_overlap_src_mean",
        "scale_out_iou_mean","time_out_iou_mean",
        "scale_out_distance_norm_mean","time_out_distance_norm_mean",
        "scale_out_feature_similarity_mean","time_out_feature_similarity_mean",
    ]
    for c in candidates:
        if c in d.columns:
            corr[c]=spearman(
                pd.to_numeric(d["stitch_defect"],errors="coerce"),
                pd.to_numeric(d[c],errors="coerce")
            )

    controls=cfg.get("partial_rank_controls",[])
    partial={}
    for c in ("enstrophy_mean","dissipation_mean_proxy"):
        if c in d.columns:
            partial[c]=partial_rank_corr(d,"stitch_defect",c,controls)

    tail={}
    for c in ("enstrophy_mean","dissipation_mean_proxy"):
        if c in d.columns:
            tail[c]=_permutation_tail_enrichment(
                d,c,q,perms,seed+(1 if c=="dissipation_mean_proxy" else 0),True
            )

    restructure={}
    for i,c in enumerate(
        ["scale_branch_flag","time_branch_flag","scale_merge_flag",
         "time_merge_flag","any_restructure_flag"]
    ):
        if c in d.columns:
            restructure[c]=_group_contrast(d,c,perms,seed+100+i)

    return {
        "eligible_nodes":int(len(d)),
        "spearman_D_vs_features":corr,
        "geometry_conditioned_partial_rank":partial,
        "high_D_tail_enrichment":tail,
        "branch_merge_contrasts":restructure,
        "interpretation_note":(
            "Partial-rank values condition on scale, time, route-overlap geometry, "
            "distance/feature compatibility, and branch/merge flags. They test whether "
            "physical intensity retains association with D_square after those controls."
        ),
    }

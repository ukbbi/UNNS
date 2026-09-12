from __future__ import annotations
import hashlib
import random
import numpy as np
import pandas as pd


def graph_signature(edges: pd.DataFrame) -> str:
    triples = sorted(
        (str(a), str(s), str(d))
        for s, d, a in edges[["src_id", "dst_id", "axis"]].itertuples(
            index=False, name=None
        )
    )
    payload = "\n".join(f"{a}|{s}|{d}" for a, s, d in triples).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _node_maps(objects):
    o = objects.set_index("node_id")
    xyz = {
        str(i): (float(r.cx), float(r.cy), float(r.cz))
        for i, r in o[["cx", "cy", "cz"]].iterrows()
    }
    radius = {
        str(i): float(v)
        for i, v in o["equiv_radius"].items()
    }
    ens = {
        str(i): float(v)
        for i, v in o["enstrophy_mean"].items()
    }
    layer = {
        str(i): (int(r.scale_idx), int(r.time_idx))
        for i, r in o[["scale_idx", "time_idx"]].iterrows()
    }
    return xyz, radius, ens, layer


def pair_geometry(src, dst, xyz, radius, ens):
    a = xyz[src]; b = xyz[dst]
    dx=a[0]-b[0]; dy=a[1]-b[1]; dz=a[2]-b[2]
    dist=(dx*dx+dy*dy+dz*dz) ** 0.5
    denom=radius[src]+radius[dst]
    dn=dist/denom if denom > 0 else float("inf")
    x=ens[src]; y=ens[dst]
    fs=(min(x,y)/max(x,y)) if x > 0 and y > 0 else 0.0
    return float(dn), float(fs)


def validate_stored_geometry(objects, edges, tol_distance=5e-6, tol_feature=5e-6):
    xyz, radius, ens, _ = _node_maps(objects)
    max_d=max_f=0.0
    checked_d=checked_f=0
    for r in edges.itertuples(index=False):
        src=str(r.src_id); dst=str(r.dst_id)
        dn, fs=pair_geometry(src,dst,xyz,radius,ens)
        if hasattr(r, "distance_norm") and np.isfinite(float(r.distance_norm)):
            max_d=max(max_d, abs(dn-float(r.distance_norm))); checked_d+=1
        if hasattr(r, "feature_similarity") and np.isfinite(float(r.feature_similarity)):
            max_f=max(max_f, abs(fs-float(r.feature_similarity))); checked_f+=1
    if checked_d and max_d > tol_distance:
        raise ValueError(f"distance_norm recomputation mismatch: max error={max_d:.3e}")
    if checked_f and max_f > tol_feature:
        raise ValueError(f"feature_similarity recomputation mismatch: max error={max_f:.3e}")
    return {
        "distance_checked": checked_d,
        "distance_max_abs_error": max_d,
        "feature_checked": checked_f,
        "feature_max_abs_error": max_f,
    }


def _bin_edges(values, requested_bins):
    a=np.asarray(values,dtype=float)
    a=a[np.isfinite(a)]
    if not len(a):
        return np.array([-np.inf,np.inf])
    qs=np.linspace(0,1,max(1,int(requested_bins))+1)
    cuts=np.unique(np.quantile(a,qs))
    if len(cuts) <= 1:
        return np.array([-np.inf,np.inf])
    cuts=cuts.astype(float)
    cuts[0]=-np.inf; cuts[-1]=np.inf
    return cuts


def _bin_id(value, cuts):
    return int(np.searchsorted(cuts, value, side="right")-1)


def _prepare_groups(objects, edges, distance_bins, feature_bins=None):
    xyz, radius, ens, layer=_node_maps(objects)
    groups={}
    for i,r in edges.reset_index(drop=True).iterrows():
        src=str(r["src_id"])
        axis=str(r["axis"])
        s,t=layer[src]
        key=(axis,s,t)
        groups.setdefault(key,[]).append(i)

    distance_cuts={}
    feature_cuts={}
    edge_dist={}
    edge_feat={}
    for key,inds in groups.items():
        ds=[]; fs=[]
        for i in inds:
            r=edges.iloc[i]
            d,f=pair_geometry(str(r.src_id),str(r.dst_id),xyz,radius,ens)
            edge_dist[i]=d; edge_feat[i]=f
            ds.append(d); fs.append(f)
        distance_cuts[key]=_bin_edges(ds,distance_bins)
        if feature_bins is not None:
            feature_cuts[key]=_bin_edges(fs,feature_bins)

    return xyz,radius,ens,layer,groups,distance_cuts,feature_cuts,edge_dist,edge_feat


def rewire_stratified(
    objects,
    edges,
    *,
    seed,
    swaps_per_edge,
    distance_bins,
    feature_bins=None,
):
    rng=random.Random(int(seed))
    out=edges.copy().reset_index(drop=True)
    (
        xyz,radius,ens,layer,groups,d_cuts,f_cuts,
        edge_dist,edge_feat
    )=_prepare_groups(objects,out,distance_bins,feature_bins)

    attempts_total=accepted_total=0
    group_diag=[]

    for key,inds in groups.items():
        if len(inds)<2:
            group_diag.append({"group":key,"edges":len(inds),"attempts":0,"accepted":0})
            continue

        pairs={(str(out.at[i,"src_id"]),str(out.at[i,"dst_id"])) for i in inds}
        attempts=max(10,int(float(swaps_per_edge)*len(inds)))
        accepted=0

        # Original stratum labels stay attached to edge rows. That is the
        # constraint being preserved during endpoint swaps.
        dlabels={
            i:_bin_id(edge_dist[i],d_cuts[key]) for i in inds
        }
        flabels={
            i:_bin_id(edge_feat[i],f_cuts[key]) for i in inds
        } if feature_bins is not None else None

        for _ in range(attempts):
            attempts_total+=1
            i,j=rng.sample(inds,2)
            a=str(out.at[i,"src_id"]); x=str(out.at[i,"dst_id"])
            b=str(out.at[j,"src_id"]); y=str(out.at[j,"dst_id"])
            if a==b or x==y:
                continue
            p1=(a,y); p2=(b,x)
            if p1 in pairs or p2 in pairs:
                continue

            d1,f1=pair_geometry(a,y,xyz,radius,ens)
            d2,f2=pair_geometry(b,x,xyz,radius,ens)
            if _bin_id(d1,d_cuts[key]) != dlabels[i]:
                continue
            if _bin_id(d2,d_cuts[key]) != dlabels[j]:
                continue
            if feature_bins is not None:
                if _bin_id(f1,f_cuts[key]) != flabels[i]:
                    continue
                if _bin_id(f2,f_cuts[key]) != flabels[j]:
                    continue

            pairs.discard((a,x)); pairs.discard((b,y))
            pairs.add(p1); pairs.add(p2)
            out.at[i,"dst_id"]=y
            out.at[j,"dst_id"]=x

            # Pair-specific geometry is recomputed. Source-attached confidence
            # remains on the row, exactly as in ROUTE-I's endpoint-swap null.
            if "distance_norm" in out.columns:
                out.at[i,"distance_norm"]=d1
                out.at[j,"distance_norm"]=d2
            if "feature_similarity" in out.columns:
                out.at[i,"feature_similarity"]=f1
                out.at[j,"feature_similarity"]=f2

            accepted+=1; accepted_total+=1

        group_diag.append({
            "group":"|".join(map(str,key)),
            "edges":len(inds),
            "attempts":attempts,
            "accepted":accepted,
            "mobility_fraction":accepted/attempts if attempts else 0.0,
        })

    return out,{
        "attempts":attempts_total,
        "accepted":accepted_total,
        "mobility_fraction":accepted_total/attempts_total if attempts_total else 0.0,
        "graph_signature":graph_signature(out),
        "mobile_groups":sum(1 for g in group_diag if g.get("accepted",0)>0),
        "transition_groups":len(groups),
        "group_diagnostics":group_diag,
    }

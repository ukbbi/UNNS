from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
import io
import json
import hashlib
import math
import os
import shutil
import time
import zipfile

import numpy as np
import pandas as pd

from .route_math import run_metrics
from .nulls import (
    rewire_stratified, graph_signature, validate_stored_geometry
)
from .mechanism import build_mechanism_table, mechanism_analysis


def sha256_file(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):
            h.update(b)
    return h.hexdigest()


def find_project_root(start, relative_run):
    cur=Path(start).resolve()
    for p in [cur]+list(cur.parents):
        if (p/relative_run).exists():
            return p
    raise FileNotFoundError(
        f"Could not locate project root containing {relative_run}"
    )


def _member(names, basename):
    hits=[n for n in names if n.endswith("/"+basename) or n==basename]
    if len(hits)!=1:
        raise ValueError(f"Expected exactly one {basename}, found {hits}")
    return hits[0]


def load_frozen_run(run_zip, expected_sha):
    found=sha256_file(run_zip)
    if found.lower()!=expected_sha.lower():
        raise ValueError(
            "Frozen ROUTE-I run checksum mismatch.\n"
            f"Expected: {expected_sha}\nFound:    {found}"
        )
    with zipfile.ZipFile(run_zip,"r") as zf:
        names=zf.namelist()
        raw={b:zf.read(_member(names,b)) for b in (
            "NODES.parquet","EDGES.parquet","NULLS.csv","RESULT.json","RUN.json"
        )}
    nodes=pd.read_parquet(io.BytesIO(raw["NODES.parquet"]))
    edges=pd.read_parquet(io.BytesIO(raw["EDGES.parquet"]))
    nulls=pd.read_csv(io.BytesIO(raw["NULLS.csv"]))
    result=json.loads(raw["RESULT.json"])
    run=json.loads(raw["RUN.json"])
    return nodes,edges,nulls,result,run,found


def empirical_low(real, vals):
    a=np.asarray([v for v in vals if v is not None and np.isfinite(v)],dtype=float)
    if not len(a):
        return None
    mu=float(np.mean(a)); sd=float(np.std(a,ddof=1)) if len(a)>1 else 0.0
    z=(mu-real)/sd if sd>0 else (math.inf if real<mu else 0.0)
    p=(1+int(np.sum(a<=real)))/(len(a)+1)
    return {
        "real":float(real),"null_mean":mu,"null_std":sd,
        "favorable_z":float(z),"p_favorable":float(p),"n_null":int(len(a)),
        "real_to_null_mean_ratio":float(real/mu) if mu else None,
    }


def null_quality(df, real_sig, quality_cfg):
    n=len(df)
    if not n:
        return {"usable":False,"flags":["NO_NULLS"]}
    attempts=int(df["swap_attempts"].sum())
    accepted=int(df["swap_accepted"].sum())
    mean_m=float(df["mobility_fraction"].mean())
    uniq=int(df["graph_signature"].nunique())
    uf=uniq/n
    rm=float((df["graph_signature"]==real_sig).mean())
    flags=[]
    if mean_m<float(quality_cfg["min_mean_mobility_fraction"]):
        flags.append("LOW_MOBILITY")
    if uf<float(quality_cfg["min_unique_graph_fraction"]):
        flags.append("LOW_DIVERSITY")
    if rm>float(quality_cfg["max_real_graph_match_fraction"]):
        flags.append("REAL_CLONE_DOMINATED")
    return {
        "swap_attempts_total":attempts,
        "swap_accepted_total":accepted,
        "mean_mobility_fraction":mean_m,
        "unique_graphs":uniq,
        "unique_graph_fraction":uf,
        "real_graph_match_fraction":rm,
        "flags":flags,
        "usable":not flags,
    }


def _run_null_family(
    name, cfg, objects, edges, out_csv, quality_cfg, progress=print
):
    count=int(cfg["count"])
    seed0=int(cfg["seed"])
    existing=pd.DataFrame()
    if out_csv.exists():
        existing=pd.read_csv(out_csv)
        if len(existing):
            progress(f"[{name}] resuming from {len(existing)}/{count} completed nulls")

    rows=existing.to_dict("records") if len(existing) else []
    done_seeds={int(r["seed"]) for r in rows if "seed" in r}
    started=time.time()

    for i in range(count):
        seed=seed0+i+1
        if seed in done_seeds:
            continue
        rew,mob=rewire_stratified(
            objects,edges,
            seed=seed,
            swaps_per_edge=float(cfg["swaps_per_edge"]),
            distance_bins=int(cfg["distance_bins"]),
            feature_bins=(int(cfg["feature_bins"]) if "feature_bins" in cfg else None),
        )
        metrics,_,_,_=run_metrics(objects,rew)
        row={
            "null_index":i+1,
            "seed":seed,
            "swap_attempts":mob["attempts"],
            "swap_accepted":mob["accepted"],
            "mobility_fraction":mob["mobility_fraction"],
            "graph_signature":mob["graph_signature"],
            **metrics,
        }
        rows.append(row)
        pd.DataFrame(rows).sort_values("null_index").to_csv(out_csv,index=False)

        elapsed=time.time()-started
        completed=len(rows)
        rate=elapsed/max(1,completed-len(existing))
        remain=max(0,count-completed)
        progress(
            f"[{name}] {completed}/{count}  mobility={mob['mobility_fraction']:.4f}  "
            f"D={metrics['stitch_defect']:.6f}  ETA≈{rate*remain/60:.1f} min"
        )

    df=pd.DataFrame(rows).sort_values("null_index").reset_index(drop=True)
    return df


def write_html(report, path):
    h=report["hierarchy"]
    mech=report["mechanism"]
    def f(x,d=6):
        return "—" if x is None else f"{x:.{d}g}"
    rows=""
    for k in ("N0","N1","N2"):
        x=h[k]
        rows+=(
            f"<tr><td>{k}</td><td>{f(x.get('null_mean'))}</td>"
            f"<td>{f(x.get('favorable_z'))}</td><td>{f(x.get('p_favorable'))}</td>"
            f"<td>{x.get('quality_label','')}</td></tr>"
        )
    partial=mech.get("geometry_conditioned_partial_rank",{})
    html=f"""<!doctype html><meta charset="utf-8"><title>STITCH-MECH v0.1</title>
<style>
body{{font-family:system-ui;background:#07101c;color:#cfe5ff;margin:32px;line-height:1.45}}
h1,h2{{color:#39e6c8}} code{{color:#82cfff}} table{{border-collapse:collapse;width:100%;max-width:1000px}}
td,th{{border:1px solid #26405c;padding:8px;text-align:left}} .verdict{{font-size:22px;color:#39e6c8}}
.note{{max-width:1000px;color:#91a9c0}}
</style>
<h1>STITCH-MECH v0.1 — JHTDB Pilot A</h1>
<p class="verdict">{report['mechanistic_verdict']}</p>
<h2>Scale–time stitching under harder nulls</h2>
<p>Real mean D□ = <b>{f(report['real']['stitch_defect'])}</b></p>
<table><tr><th>Control</th><th>Null mean D□</th><th>Fav z</th><th>p</th><th>Quality</th></tr>{rows}</table>
<h2>Object-level mechanism</h2>
<p>Eligible source objects: {mech['eligible_nodes']}</p>
<p>Geometry-conditioned partial rank ρ(D□, enstrophy) = <b>{f(partial.get('enstrophy_mean'))}</b><br>
Geometry-conditioned partial rank ρ(D□, dissipation proxy) = <b>{f(partial.get('dissipation_mean_proxy'))}</b></p>
<p class="note">{mech['interpretation_note']}</p>
<h2>Interpretation boundary</h2>
<p class="note">{report['claim_boundary']}</p>
"""
    path.write_text(html,encoding="utf-8")


def run(config_path, project_root=None, progress=print):
    cfg=json.loads(Path(config_path).read_text(encoding="utf-8"))
    rel=Path(cfg["frozen_run"]["relative_path"])
    if project_root is None:
        project_root=find_project_root(Path(config_path).parent,rel)
    project_root=Path(project_root).resolve()
    run_zip=project_root/rel

    analysis_dir=project_root/Path(cfg["outputs"]["analysis_relative_dir"])
    records_dir=project_root/Path(cfg["outputs"]["records_relative_dir"])
    tables_dir=project_root/Path(cfg["outputs"]["tables_relative_dir"])
    for d in (analysis_dir,records_dir,tables_dir):
        d.mkdir(parents=True,exist_ok=True)

    progress("[SOURCE] loading frozen ROUTE-I run...")
    objects,edges,n0_nulls,route_result,run_record,run_sha=load_frozen_run(
        run_zip,cfg["frozen_run"]["sha256"]
    )
    if route_result["meta"]["version"]!=cfg["frozen_run"]["route_i_version"]:
        raise ValueError("Unexpected ROUTE-I version.")

    geom_check=validate_stored_geometry(objects,edges)
    progress(
        f"[SOURCE] geometry recomputation PASS; "
        f"distance max error={geom_check['distance_max_abs_error']:.3e}, "
        f"feature max error={geom_check['feature_max_abs_error']:.3e}"
    )

    real_metrics,_,_,_=run_metrics(objects,edges)
    frozen_real=float(route_result["structure"]["stitch"]["mean_defect"])
    if abs(real_metrics["stitch_defect"]-frozen_real)>1e-12:
        raise ValueError(
            f"ROUTE-I metric reproduction failed: {real_metrics['stitch_defect']} vs {frozen_real}"
        )
    progress(f"[REAL] D_square mean reproduced exactly: {frozen_real:.12f}")

    # Object-level mechanism analysis is independent of null generation.
    mech_table=build_mechanism_table(
        objects,edges,float(cfg["mechanism"]["viscosity"])
    )
    mech=mechanism_analysis(mech_table,cfg["mechanism"])
    mech_table.to_csv(tables_dir/"STITCH_MECH_OBJECTS.csv",index=False)
    progress("[MECHANISM] object-level conditional analysis complete.")

    # N0 is imported, not regenerated.
    n0_test=empirical_low(
        frozen_real,
        pd.to_numeric(n0_nulls["stitch_defect"],errors="coerce")
    )

    real_sig=graph_signature(edges)
    quality_cfg=cfg["null_hierarchy"]["quality"]

    n1_csv=tables_dir/"STITCH_N1_NULLS.csv"
    n2_csv=tables_dir/"STITCH_N2_NULLS.csv"

    progress("[N1] distance-stratified null ensemble...")
    n1=_run_null_family(
        "N1",cfg["null_hierarchy"]["N1"],objects,edges,n1_csv,quality_cfg,progress
    )
    q1=null_quality(n1,real_sig,quality_cfg)
    n1_test=empirical_low(frozen_real,n1["stitch_defect"])

    progress("[N2] distance+feature-stratified null ensemble...")
    n2=_run_null_family(
        "N2",cfg["null_hierarchy"]["N2"],objects,edges,n2_csv,quality_cfg,progress
    )
    q2=null_quality(n2,real_sig,quality_cfg)
    n2_test=empirical_low(frozen_real,n2["stitch_defect"])

    hierarchy={
        "N0":{**n0_test,"quality_label":"FROZEN ROUTE-I CONTROL"},
        "N1":{**n1_test,"quality":q1,"quality_label":"PASS" if q1["usable"] else "UNDERRESOLVED"},
        "N2":{**n2_test,"quality":q2,"quality_label":"PASS" if q2["usable"] else "UNDERRESOLVED"},
    }

    alpha=float(run_record["manifest"]["inference"]["alpha"])
    if not q2["usable"]:
        verdict="N2_UNDERRESOLVED"
    elif n2_test["p_favorable"]<=alpha:
        verdict="SURVIVES_LOCAL_GEOMETRY_CONTROL"
    else:
        verdict="NOT_DISTINGUISHABLE_FROM_LOCAL_GEOMETRY_CONTROL"

    report={
        "tool":{"name":"STITCH_MECH","version":"0.1.1"},
        "created_utc":datetime.now(timezone.utc).isoformat(),
        "project":cfg["project"],
        "pilot":cfg["pilot"],
        "source":{
            "run_zip":str(run_zip),
            "run_sha256":run_sha,
            "route_i_version":route_result["meta"]["version"],
            "route_i_verdict":route_result["verdict"]["class"],
            "geometry_recomputation_check":geom_check,
        },
        "real":real_metrics,
        "hierarchy":hierarchy,
        "mechanism":mech,
        "mechanistic_verdict":verdict,
        "claim_boundary":(
            "The null hierarchy tests whether low D_square survives increasingly local "
            "route controls available from the frozen object/edge tables. N1/N2 preserve "
            "degree and route layers while constraining recomputed centroid geometry; N2 "
            "also constrains enstrophy-based feature similarity. They do NOT preserve exact "
            "voxel overlap/Iou because voxel masks are not part of the frozen ROUTE-I run. "
            "Survival therefore rejects these graph-local geometric explanations, not every "
            "possible field-level geometric surrogate."
        ),
        "next_if_positive":(
            "Replicate the frozen protocol on an independent JHTDB cutout/time window, "
            "then build a field-level surrogate control if the result persists."
        ),
        "config":cfg,
    }

    report_json=analysis_dir/"REPORT.json"
    report_json.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    write_html(report,analysis_dir/"REPORT.html")

    summary=pd.DataFrame([
        {"control":"REAL","mean_D":frozen_real,"p_favorable":None,"quality":"REAL"},
        {"control":"N0","mean_D":n0_test["null_mean"],"p_favorable":n0_test["p_favorable"],"quality":"FROZEN"},
        {"control":"N1","mean_D":n1_test["null_mean"],"p_favorable":n1_test["p_favorable"],"quality":"PASS" if q1["usable"] else "UNDERRESOLVED"},
        {"control":"N2","mean_D":n2_test["null_mean"],"p_favorable":n2_test["p_favorable"],"quality":"PASS" if q2["usable"] else "UNDERRESOLVED"},
    ])
    summary.to_csv(tables_dir/"STITCH_NULL_HIERARCHY.csv",index=False)

    # Record copy and bundle.
    shutil.copy2(report_json,records_dir/"STITCH_MECH_REPORT.json")
    bundle=records_dir/"STITCH_MECH_RESULT.zip"
    with zipfile.ZipFile(bundle,"w",zipfile.ZIP_DEFLATED) as zf:
        for p in [
            analysis_dir/"REPORT.json",analysis_dir/"REPORT.html",
            tables_dir/"STITCH_NULL_HIERARCHY.csv",
            tables_dir/"STITCH_MECH_OBJECTS.csv",
            n1_csv,n2_csv,
        ]:
            zf.write(p,p.name)

    progress("")
    progress("[COMPLETE]")
    progress(f"  mechanistic verdict: {verdict}")
    progress(f"  report: {analysis_dir/'REPORT.html'}")
    progress(f"  bundle: {bundle}")
    return report

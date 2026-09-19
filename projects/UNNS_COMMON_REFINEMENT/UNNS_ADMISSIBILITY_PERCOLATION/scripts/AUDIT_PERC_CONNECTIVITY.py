#!/usr/bin/env python3
from pathlib import Path
import csv, json, math

ROOT = Path(__file__).resolve().parents[1]
INPUT_DIR = ROOT / "inputs" / "struc_perc_i"
BATCH_CSV = ROOT / "outputs" / "struc_perc_i" / "STRUC_PERC_BATCH_RESULTS.csv"
OUT_CSV = ROOT / "outputs" / "records" / "PERC_CONNECTIVITY_AUDIT.csv"
OUT_JSON = ROOT / "outputs" / "records" / "PERC_CONNECTIVITY_AUDIT.json"

REL_ZERO_TOL = 1e-12

def median(xs):
    s=sorted(xs); n=len(s); m=n//2
    return s[m] if n%2 else (s[m-1]+s[m])/2

def chamber_iqr(xs):
    s=sorted(xs)
    q1=s[math.floor(0.25*(len(s)-1))]
    q3=s[math.floor(0.75*(len(s)-1))]
    return q3-q1, q1, q3

def read_ladder(path):
    with path.open(encoding="utf-8") as f:
        rows=list(csv.DictReader(f))
    return [float(r["value"]) for r in rows]

def comp_sizes(gaps, eps):
    s=sorted(gaps)
    sizes=[]
    start=0
    for i in range(1,len(s)):
        if s[i]-s[i-1] > eps:
            sizes.append(i-start); start=i
    sizes.append(len(s)-start)
    return sorted(sizes, reverse=True)

def classify(gaps, scale):
    sizes=comp_sizes(gaps,scale)  # kappa = 1
    n=len(gaps)
    giant=sizes[0]/n
    isolated=sum(x==1 for x in sizes)
    iso_frac=isolated/n
    secondary=(sizes[1]/n) if len(sizes)>1 else 0
    if len(sizes)==1:
        return "FULL_PERCOLATION", giant, isolated, iso_frac
    if giant>=0.995 and iso_frac<0.005:
        return "GIANT_COMPONENT_PERCOLATION", giant, isolated, iso_frac
    if giant>=0.95 and secondary<=0.01:
        return "TAIL_FRAGMENTATION", giant, isolated, iso_frac
    return "HARD_FRAGMENTATION", giant, isolated, iso_frac

def outlier_max_ratio(gaps, med, scale):
    threshold=max(10*med,5*scale)
    vals=[g/med for g in gaps if g>threshold]
    return max(vals) if vals else 0.0

def simulate_extension(gaps, med, scale, current_giant, tier):
    if tier in ("FULL_PERCOLATION","GIANT_COMPONENT_PERCOLATION"):
        return [], None, None
    max_ratio=outlier_max_ratio(gaps,med,scale)
    sc=min(max_ratio if max_ratio else 1.0,1e6)
    targets=sorted(set([2.0,10.0,math.sqrt(sc),sc]))
    prev=current_giant
    prevprev=None
    hist=[]
    connect=None
    plateau=None
    for mult in targets:
        sizes=comp_sizes(gaps,mult*scale)
        ratio=sizes[0]/len(gaps)
        connected=len(sizes)==1
        hist.append({"kappa":mult,"giant_ratio":ratio,"n_components":len(sizes),"connected":connected})
        if connected and connect is None:
            connect=mult
        if prevprev is not None:
            growth=ratio-prevprev
            rel=(growth/prevprev) if prevprev>0 else growth
            if growth<1e-4 or rel<1e-3:
                plateau=mult
                break
        prevprev=prev
        prev=ratio
        if connect:
            break
    return hist,connect,plateau

def exact_connectivity_threshold(gaps, scale):
    s=sorted(gaps)
    max_adj=max((s[i]-s[i-1] for i in range(1,len(s))), default=0.0)
    return (max_adj/scale if scale>0 else None), max_adj

def main():
    with BATCH_CSV.open(encoding="utf-8") as f:
        batch={r["name"].replace(".csv",""):r for r in csv.DictReader(f)}

    rows=[]
    detail=[]
    verdict_matches=0

    for path in sorted(INPUT_DIR.glob("*.csv")):
        cid=path.stem
        L=read_ladder(path)
        gaps=[L[i+1]-L[i] for i in range(len(L)-1)]
        med=median(gaps)
        iqr,q1,q3=chamber_iqr(gaps)
        chamber_scale=iqr if iqr>0 else med

        tier,giant,isolated,iso_frac=classify(gaps,chamber_scale)
        hist,ext_connect,plateau=simulate_extension(gaps,med,chamber_scale,giant,tier)
        final_tier="FULL_PERCOLATION" if ext_connect is not None else tier

        exact_k,max_adj=exact_connectivity_threshold(gaps,chamber_scale)

        rel_iqr=abs(iqr)/max(abs(med),1e-300)
        effective_zero=(iqr>0 and rel_iqr<=REL_ZERO_TOL)
        tol_scale=med if effective_zero else chamber_scale
        exact_k_tol,_=exact_connectivity_threshold(gaps,tol_scale)

        b=batch[cid]
        batch_tier=b["verdict"]
        if batch_tier==final_tier:
            verdict_matches+=1

        row={
            "case_id":cid,
            "batch_verdict":batch_tier,
            "simulated_batch_verdict":final_tier,
            "median_gap":med,
            "chamber_iqr":iqr,
            "relative_iqr_to_median":rel_iqr,
            "effective_zero_iqr_flag":effective_zero,
            "chamber_scale":chamber_scale,
            "base_giant_ratio":giant,
            "adaptive_plateau_kappa":plateau,
            "adaptive_connect_kappa":ext_connect,
            "exact_graph_kappa_connect":exact_k,
            "tolerance_fallback_scale":tol_scale,
            "exact_graph_kappa_connect_with_tol_fallback":exact_k_tol,
            "max_sorted_gap_separation":max_adj,
        }
        rows.append(row)
        detail.append({
            **row,
            "adaptive_extension_trace":hist,
        })

    OUT_CSV.parent.mkdir(parents=True,exist_ok=True)
    with OUT_CSV.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)

    report={
        "status":"PASS",
        "purpose":"audit STRUC-PERC-I batch verdicts against the chamber's own full-pairwise threshold graph",
        "n_cases":len(rows),
        "batch_verdicts_reproduced":verdict_matches,
        "relative_zero_tolerance":REL_ZERO_TOL,
        "key_findings":{
            "nonfull_batch_cases":[r["case_id"] for r in rows if r["batch_verdict"]!="FULL_PERCOLATION"],
            "effective_zero_iqr_cases":[r["case_id"] for r in rows if r["effective_zero_iqr_flag"]],
            "premature_plateau_cases":[
                r["case_id"] for r in rows
                if r["batch_verdict"]!="FULL_PERCOLATION"
                and r["adaptive_plateau_kappa"] is not None
                and r["exact_graph_kappa_connect"] is not None
                and r["exact_graph_kappa_connect"]>r["adaptive_plateau_kappa"]
                and not r["effective_zero_iqr_flag"]
            ]
        },
        "cases":detail
    }
    OUT_JSON.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report["key_findings"],indent=2))
    print(f"Reproduced batch verdicts: {verdict_matches}/{len(rows)}")

if __name__=="__main__":
    main()

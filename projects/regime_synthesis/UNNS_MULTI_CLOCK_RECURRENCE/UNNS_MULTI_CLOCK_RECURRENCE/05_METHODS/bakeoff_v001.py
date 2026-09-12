#!/usr/bin/env python3
import argparse, json, math, itertools, hashlib
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from scipy.spatial import cKDTree

def load_cfg(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def load_record(root,row):
    df=pd.read_csv(root/row["file"])
    ycol=[c for c in df.columns if c not in ("sample_index","time")][0]
    t=df["time"].to_numpy(float); y=df[ycol].to_numpy(float)
    mask=np.isfinite(t)&np.isfinite(y)
    return t[mask],y[mask],ycol

def fft_peaks(t,y,cfg,search_n):
    n=len(y); dt=float(np.median(np.diff(t)))
    z=(y-np.mean(y))/(np.std(y)+1e-30)
    power=np.abs(np.fft.rfft(z*np.hanning(n)))**2
    freq=np.fft.rfftfreq(n,dt)
    power[:3]=0.0
    peaks,_=find_peaks(power,distance=2)
    if len(peaks)==0:
        peaks=np.argsort(power[3:])[-search_n:]+3
    top=peaks[np.argsort(power[peaks])[-search_n:]][::-1]
    return freq,power,top,1/(n*dt)

def infer_basis(t,y,cfg):
    freq,power,top,dfreq=fft_peaks(t,y,cfg,cfg["independent_basis_search_peaks"])
    f1=float(freq[top[0]]); p1=float(power[top[0]])
    f2=None;p2=None
    tol=cfg["harmonic_tolerance_fft_bins"]*dfreq
    for idx in top[1:]:
        c=float(freq[idx])
        maxk=max(2,int(math.ceil(max(c/f1,f1/c)))+1)
        err1=min(abs(c-k*f1) for k in range(1,maxk+1))
        err2=min(abs(f1-k*c) for k in range(1,maxk+1))
        if min(err1,err2)>tol:
            f2=c;p2=float(power[idx]);break
    if f2 is None and len(top)>1:
        f2=float(freq[top[1]]);p2=float(power[top[1]])
    topn=min(cfg["spectrum_top_peaks"],len(top))
    details=[{"frequency":float(freq[i]),"relative_power":float(power[i]/(p1+1e-30))}
             for i in top[:topn]]
    total=float(power[3:].sum()+1e-30)
    concentration=float(sum(power[i] for i in top[:min(10,len(top))])/total)
    return {"f1":f1,"f2":f2,"f2_rel_power":float(p2/(p1+1e-30)),
            "df":float(dfreq),"spectral_concentration_top10":concentration,
            "top_peaks":details}

def lattice(t,y,b,cfg):
    freq,power,top,dfreq=fft_peaks(t,y,cfg,cfg["spectrum_top_peaks"])
    top=top[:cfg["spectrum_top_peaks"]]
    pf=freq[top]; pp=power[top]; w=pp/(pp.sum()+1e-30)
    f1,f2=b["f1"],b["f2"]
    pred1=np.array([k*f1 for k in range(1,cfg["lattice_harmonic_order_1d"]+1)])
    e1=np.min(np.abs(pf[:,None]-pred1[None,:]),axis=1)/dfreq
    coeff=[(m,n) for m in range(-cfg["lattice_order"],cfg["lattice_order"]+1)
                 for n in range(-cfg["lattice_order"],cfg["lattice_order"]+1)
                 if not (m==0 and n==0)]
    vals=np.abs(np.array([m*f1+n*f2 for m,n in coeff],float))
    vals=vals[vals>0.25*dfreq]
    e2=np.min(np.abs(pf[:,None]-vals[None,:]),axis=1)/dfreq
    r1=float(np.sum(w*np.minimum(e1,50)))
    r2=float(np.sum(w*np.minimum(e2,50)))
    ratio=max(f1,f2)/min(f1,f2)
    best=(1e9,None,None)
    for q in range(1,9):
        for p in range(1,33):
            d=abs(ratio-p/q)
            if d<best[0]:best=(d,p,q)
    return {"lattice_1d_resid_bins":r1,"lattice_2d_resid_bins":r2,
            "lattice_gain_bins":r1-r2,
            "lattice_weighted_coverage_2bins":float(np.sum(w*(e2<=2))),
            "basis_ratio":float(ratio),"ratio_rational_distance_q8":float(best[0]),
            "nearest_rational_q8":f"{best[1]}/{best[2]}"}

def torus(t,y,b,cfg):
    f1,f2=b["f1"],b["f2"]
    n=len(y)
    idx=np.linspace(0,n-1,min(n,cfg["torus_max_points"]),dtype=int)
    tt=t[idx]-t[idx][0]
    yy=y[idx].astype(float); yy=(yy-yy.mean())/(yy.std()+1e-30)
    def features(freqs):
        cols=[]
        for f in freqs:
            th=2*np.pi*f*tt
            cols.extend([np.cos(th),np.sin(th)])
        return np.column_stack(cols)
    def score(X):
        tree=cKDTree(X)
        _,nbr=tree.query(X,k=min(cfg["torus_knn_k"]+1,len(X)))
        nbr=nbr[:,1:]
        pred=yy[nbr].mean(axis=1)
        return float(1-np.mean((yy-pred)**2)/(np.var(yy)+1e-30)),nbr
    s1,_=score(features([f1]));s2,_=score(features([f2]));s12,nbr=score(features([f1,f2]))
    rng=np.random.default_rng(cfg["seed"])
    null=[]
    for _ in range(cfg["torus_shuffle_surrogates"]):
        yp=rng.permutation(yy); pred=yp[nbr].mean(axis=1)
        null.append(1-np.mean((yp-pred)**2)/(np.var(yp)+1e-30))
    return {"torus_r2_f1":s1,"torus_r2_f2":s2,"torus_r2_2d":s12,
            "torus_gain_over_best_1d":float(s12-max(s1,s2)),
            "torus_shuffle_mean":float(np.mean(null)),
            "torus_excess_over_shuffle":float(s12-np.mean(null))}

def recurrence(t,y,b,cfg):
    z=(y-y.mean())/(y.std()+1e-30); n=len(z)
    m=1<<(2*n-1).bit_length()
    F=np.fft.rfft(z,n=m)
    ac=np.fft.irfft(F*np.conj(F),n=m)[:n]
    ac=ac/(ac[0]+1e-30); R=np.abs(ac)
    dt=float(np.median(np.diff(t)))
    carrier=max(2,1/(b["f1"]*dt))
    min_lag=max(2,int(round(cfg["recurrence_min_lag_fraction_of_carrier_period"]*carrier)))
    qmax=min(cfg["recurrence_max_lag_cap"],n//5)
    if min_lag>=qmax:min_lag=2
    vals=R[min_lag:qmax+1]
    peaks,_=find_peaks(vals,distance=2)
    if len(peaks):
        cand=peaks[np.argsort(vals[peaks])[-cfg["recurrence_top_lags"]:]][::-1]+min_lag
    else:
        cand=np.argsort(vals)[-cfg["recurrence_top_lags"]:]+min_lag
    best_single=float(max(R[q] for q in cand))
    best=(-1,None,None)
    for q1,q2 in itertools.combinations(sorted(map(int,cand)),2):
        if q1+q2>qmax:continue
        qs=[q1,q2,abs(q2-q1),q1+q2]
        rs=[max(R[q],1e-12) for q in qs if q>0]
        sc=float(np.exp(np.mean(np.log(rs))))
        if sc>best[0]:best=(sc,q1,q2)
    return {"rec_min_lag":int(min_lag),"rec_qmax":int(qmax),
            "rec_best_single":best_single,
            "rec_best_pair":float(best[0]) if best[1] else float("nan"),
            "rec_q1":best[1],"rec_q2":best[2],
            "rec_pair_ratio":float(best[2]/best[1]) if best[1] else float("nan"),
            "rec_top_lags":[{"q":int(q),"coherence":float(R[q])} for q in cand]}

def sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(1<<20),b""):h.update(chunk)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--root",default=".")
    args=ap.parse_args()
    root=Path(args.root).resolve()
    cfg=load_cfg(root/"05_METHODS/bakeoff_config.json")
    corpus=pd.read_csv(root/"04_CORPUS/CORPUS_v001.csv")
    corpus=corpus[corpus["status"]=="INGESTED"].copy()
    out=root/"08_OUTPUTS/BAKEOFF_v001"
    det=out/"RECORD_DETAILS";det.mkdir(parents=True,exist_ok=True)
    rows=[]
    for _,row in corpus.iterrows():
        t,y,ycol=load_record(root,row)
        b=infer_basis(t,y,cfg); lat=lattice(t,y,b,cfg); tor=torus(t,y,b,cfg); rec=recurrence(t,y,b,cfg)
        rr={"id":row["id"],"source":row["source"],"role":row["role"],
            "observable":row["observable"],"regime":row["regime"],"n":len(y),
            "f1":b["f1"],"f2":b["f2"],"f2_rel_power":b["f2_rel_power"],
            "spectral_concentration_top10":b["spectral_concentration_top10"],
            **lat,**tor,**{k:v for k,v in rec.items() if k!="rec_top_lags"}}
        rows.append(rr)
        (det/f'{row["id"]}.json').write_text(json.dumps(
            {"basis":b,"lattice":lat,"torus":tor,"recurrence":rec},indent=2,allow_nan=True),
            encoding="utf-8")
    df=pd.DataFrame(rows)
    df.to_csv(out/"BAKEOFF_RESULTS.csv",index=False)
    (out/"BAKEOFF_RESULTS.json").write_text(json.dumps(rows,indent=2,allow_nan=True),encoding="utf-8")
    audit={"version":cfg["version"],"seed":cfg["seed"],"records":len(rows),
           "classification_thresholds":0,"verdicts_emitted":0,
           "c003_loaded":False,"zhu_holdout_loaded":False,"moon_loaded":False,
           "status":"PASS_DIAGNOSTIC_ONLY",
           "results_sha256":sha256(out/"BAKEOFF_RESULTS.csv")}
    (out/"BAKEOFF_AUDIT.json").write_text(json.dumps(audit,indent=2),encoding="utf-8")
    print(json.dumps(audit,indent=2))

if __name__=="__main__":
    main()

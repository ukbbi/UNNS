#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, hashlib, json, math, sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import least_squares
from scipy.special import k0
import scipy

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

class EMTError(RuntimeError):
    pass

def sha256_file(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):
            h.update(b)
    return h.hexdigest()

def family_basis(name,x,lam):
    if name=="exponential":
        return np.exp(-x/lam)
    if name=="bessel_K0":
        return k0(x/lam)
    raise EMTError(name)

def fit_family(family, positive, x, y, sig, R):
    seeds=[R*m for m in (1/16,1/8,1/4,1/2,1,2)]
    ymin=max(float(np.min(y)),0.0)
    deltas=[0.0] if not positive else [0.0,0.25*ymin,0.5*ymin,1.0*ymin]
    best=None
    for lam0 in seeds:
        b0=family_basis(family,x,lam0)
        A0=max(float(np.median(np.maximum(y,1e-14)/np.maximum(b0,1e-14))),1e-12)
        for d0 in deltas:
            p0=np.array([A0,lam0,d0]) if positive else np.array([A0,lam0])
            lb=np.zeros_like(p0); lb[1]=1e-9
            ub=np.full_like(p0,np.inf)
            def res(p):
                A,lam=p[:2]
                delta=p[2] if positive else 0.0
                pred=delta+A*family_basis(family,x,lam)
                return (y-pred)/sig
            try:
                z=least_squares(res,p0,bounds=(lb,ub),xtol=1e-13,ftol=1e-13,gtol=1e-13,max_nfev=30000)
            except Exception:
                continue
            chi=float(np.sum(z.fun*z.fun))
            if np.isfinite(chi) and (best is None or chi<best["chi2"]):
                best={"chi2":chi,"p":z.x}
    if best is None:
        raise EMTError(f"fit failed: {family}, positive={positive}")
    n=len(y); kpar=3 if positive else 2
    if n-kpar-1<=0:
        raise EMTError("AICc undefined")
    aicc=best["chi2"]+2*kpar+2*kpar*(kpar+1)/(n-kpar-1)
    p=best["p"]
    return {
        "family":family,"floor":"positive" if positive else "zero","n":n,"k":kpar,
        "chi2":best["chi2"],"aicc":float(aicc),"A":float(p[0]),"lambda_fm":float(p[1]),
        "delta":float(p[2]) if positive else 0.0
    }

def cls(delta,thr=6.0):
    if delta>=thr:return "ZERO"
    if delta<=-thr:return "POSITIVE"
    return "UNDECIDED"

def material_path(ylo,yhi):
    return not any(ylo[i+1]>yhi[i] for i in range(len(ylo)-1))

def write_csv(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    if not rows:return
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys()));w.writeheader();w.writerows(rows)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--project-root",type=Path,default=Path("."))
    ap.add_argument("--validate-only",action="store_true")
    args=ap.parse_args()
    root=args.project_root.resolve()
    cfg=json.loads((Path(__file__).resolve().parent/"EMT_I_CONFIG.json").read_text(encoding="utf-8"))
    inp=root/cfg["input_common_csv"]
    if not inp.exists():raise EMTError(f"missing {inp}")
    if sha256_file(inp)!=cfg["expected_common_csv_sha256"]:raise EMTError("EMT common CSV hash mismatch")

    df=pd.read_csv(inp)
    comps=cfg["components"]
    required=["point_index","r_fm"]+[f"{c}_GeV_fm3" for c in comps]+[f"{c}_err_GeV_fm3" for c in comps]
    if not set(required).issubset(df.columns):raise EMTError("missing required columns")
    if len(df)!=185:raise EMTError(f"expected 185 rows, got {len(df)}")
    r=df.r_fm.to_numpy(float)
    if not np.all(np.diff(r)>0):raise EMTError("r grid not strictly increasing")

    R=cfg["R_fm"]; hbarc=cfg["hbar_c_GeV_fm"]; scale=R**4/hbarc
    Y=np.column_stack([df[f"{c}_GeV_fm3"].to_numpy(float) for c in comps])
    S=np.column_stack([df[f"{c}_err_GeV_fm3"].to_numpy(float) for c in comps])
    if not np.all(np.isfinite(Y)) or not np.all(S>0):raise EMTError("invalid data/errors")

    absY=np.abs(Y)
    D=scale*np.sqrt(np.mean(Y*Y,axis=1))
    Dmin=scale*np.sqrt(np.mean(np.maximum(absY-S,0.0)**2,axis=1))
    Dmax=scale*np.sqrt(np.mean((absY+S)**2,axis=1))
    Dsig=(Dmax-Dmin)/2
    Dsig=np.maximum(Dsig,1e-12)

    tail=r>=cfg["tail_cut_fm"]-1e-12
    if int(tail.sum())<8:raise EMTError("too few tail points")

    if args.validate_only:
        print("EMT-I chamber validation: PASS")
        print("input sha256:",sha256_file(inp))
        print("rows:",len(df))
        print("tail points:",int(tail.sum()))
        print("native common grid: yes; interpolation: none")
        print("No scientific fit performed (--validate-only).")
        return 0

    fit_rows=[]; norm_classes={}
    for cut_name,drop in (("PRIMARY_TAIL",False),("DROP_FIRST_TAIL_POINT",True)):
        inds=np.where(tail)[0]
        if drop:inds=inds[1:]
        x=r[inds]; y=D[inds]; sig=Dsig[inds]
        norm_classes[cut_name]={}
        for fam in cfg["families"]:
            f0=fit_family(fam,False,x,y,sig,R)
            fd=fit_family(fam,True,x,y,sig,R)
            delta=fd["aicc"]-f0["aicc"]
            c=cls(delta,cfg["delta_AICc_decisive"])
            norm_classes[cut_name][fam]=c
            for z in (f0,fd):
                fit_rows.append({"target":"D_EMT","tail_cut":cut_name,**z,
                                 "delta_AICc_floor_minus_zero":delta,"classification":c})

    path_ok=material_path(Dmin,Dmax)

    component_rows=[]; component_labels={}
    for j,cname in enumerate(comps):
        mag=np.abs(Y[:,j]); sig=S[:,j]
        lo=np.maximum(mag-sig,0.0); hi=mag+sig
        cpath=material_path(lo,hi)
        cclasses={}
        for cut_name,drop in (("PRIMARY_TAIL",False),("DROP_FIRST_TAIL_POINT",True)):
            inds=np.where(tail)[0]
            if drop:inds=inds[1:]
            cclasses[cut_name]={}
            for fam in cfg["families"]:
                f0=fit_family(fam,False,r[inds],mag[inds],sig[inds],R)
                fd=fit_family(fam,True,r[inds],mag[inds],sig[inds],R)
                delta=fd["aicc"]-f0["aicc"]
                cc=cls(delta,cfg["delta_AICc_decisive"])
                cclasses[cut_name][fam]=cc
                component_rows.append({
                    "component":cname,"tail_cut":cut_name,"family":fam,
                    "delta_AICc_floor_minus_zero":delta,"classification":cc,
                    "path_vacuum_directed":cpath
                })
        vals=[cclasses[t][f] for t in cclasses for f in cfg["families"]]
        if all(v=="POSITIVE" for v in vals):
            label="NONZERO-FLOOR"
        elif all(v=="ZERO" for v in vals) and cpath:
            label="VACUUM-DIRECTED"
        elif not cpath:
            label="NONMONOTONE"
        else:
            label="UNCERTAINTY-LIMITED"
        component_labels[cname]=label

    vals=[norm_classes[t][f] for t in norm_classes for f in cfg["families"]]
    any_comp_floor=any(v=="NONZERO-FLOOR" for v in component_labels.values())

    if all(v=="POSITIVE" for v in vals):
        outcome="EMT-REPRESENTATION-SPLIT" if any(v=="VACUUM-DIRECTED" for v in component_labels.values()) else "EMT-POSITIVE-FLOOR"
    elif all(v=="ZERO" for v in vals) and path_ok:
        outcome="EMT-REPRESENTATION-SPLIT" if any_comp_floor else "EMT-CONTINUITY-CONSISTENT"
    elif any_comp_floor and any(v=="ZERO" for v in vals):
        outcome="EMT-REPRESENTATION-SPLIT"
    else:
        outcome="EMT-UNCERTAINTY-LIMITED"

    dist_rows=[]
    for i in range(len(df)):
        dist_rows.append({"point_index":int(df.point_index.iloc[i]),"r_fm":float(r[i]),
                          "D_EMT":float(D[i]),"D_min":float(Dmin[i]),"D_max":float(Dmax[i]),
                          "D_sigma_fit":float(Dsig[i])})
    outs=cfg["outputs"]
    write_csv(root/outs["distance_csv"],dist_rows)
    write_csv(root/outs["fits_csv"],fit_rows)
    write_csv(root/outs["components_csv"],component_rows)

    p=root/outs["profile_png"];p.parent.mkdir(parents=True,exist_ok=True)
    fig=plt.figure(figsize=(8.4,5.3));ax=fig.add_subplot(111)
    for j,c in enumerate(comps):
        ax.errorbar(r,Y[:,j],yerr=S[:,j],marker=".",linestyle="none",label=c,alpha=.75)
    ax.axhline(0,linewidth=1);ax.axvline(cfg["tail_cut_fm"],linestyle="--",linewidth=1)
    ax.set_xlabel("r [fm]");ax.set_ylabel("EMT component [GeV/fm^3]")
    ax.set_title("Yanagihara 2019 EMT-I: independent vacuum-subtracted representation")
    ax.legend();ax.grid(True,alpha=.2);fig.tight_layout();fig.savefig(p,dpi=180);plt.close(fig)

    p=root/outs["distance_png"];p.parent.mkdir(parents=True,exist_ok=True)
    fig=plt.figure(figsize=(8.4,5.3));ax=fig.add_subplot(111)
    ax.plot(r,D)
    ax.fill_between(r,Dmin,Dmax,alpha=.2)
    ax.axhline(0,linewidth=1);ax.axvline(cfg["tail_cut_fm"],linestyle="--",linewidth=1)
    ax.set_xlabel("r [fm]");ax.set_ylabel("dimensionless D_EMT")
    ax.set_title("EMT-I structural distance to vacuum")
    ax.grid(True,alpha=.2);fig.tight_layout();fig.savefig(p,dpi=180);plt.close(fig)

    def delta(cut,fam):
        rr=[z for z in fit_rows if z["target"]=="D_EMT" and z["tail_cut"]==cut and z["family"]==fam]
        return rr[0]["delta_AICc_floor_minus_zero"]

    report=f"""# EMT-I Primary Report

**Source:** `YANAGIHARA_2019_EMT`  
**Primary geometry:** `R = {R:.2f} fm`  
**Outcome:** **{outcome}**

## Geometry / extraction

- common native coordinates: 185
- interpolation: none
- measured support: {r[0]:.9g} to {r[-1]:.9g} fm
- primary tail cut: {cfg["tail_cut_fm"]:.3f} fm
- tail coordinates: {int(tail.sum())}

## Structural path

- four-component norm path: {"VACUUM-DIRECTED" if path_ok else "NONMONOTONE"}

## Floor-model comparison

| tail | family | Delta AICc (floor - zero) | class |
|---|---|---:|---|
| PRIMARY | exponential | {delta("PRIMARY_TAIL","exponential"):.8g} | {norm_classes["PRIMARY_TAIL"]["exponential"]} |
| PRIMARY | K0 | {delta("PRIMARY_TAIL","bessel_K0"):.8g} | {norm_classes["PRIMARY_TAIL"]["bessel_K0"]} |
| DROP-FIRST | exponential | {delta("DROP_FIRST_TAIL_POINT","exponential"):.8g} | {norm_classes["DROP_FIRST_TAIL_POINT"]["exponential"]} |
| DROP-FIRST | K0 | {delta("DROP_FIRST_TAIL_POINT","bessel_K0"):.8g} | {norm_classes["DROP_FIRST_TAIL_POINT"]["bessel_K0"]} |

Decisive threshold: `|Delta AICc| >= 6`.

## Component checks

""" + "\n".join(f"- `{k}`: **{v}**" for k,v in component_labels.items()) + """

## Scope

This is an independent continuum EMT structural-vacuum result. It is not a claim that the physical Yang-Mills Hamiltonian mass gap closes.
"""
    rp=root/outs["report_md"];rp.parent.mkdir(parents=True,exist_ok=True);rp.write_text(report,encoding="utf-8")
    jp=root/outs["run_json"];jp.parent.mkdir(parents=True,exist_ok=True)
    jp.write_text(json.dumps({
        "schema":"UNNS_EMT_I_RUN_v1","run_utc":datetime.now(timezone.utc).isoformat(),
        "outcome":outcome,"input_sha256":sha256_file(inp),"path_vacuum_directed":path_ok,
        "norm_classes":norm_classes,"component_labels":component_labels,
        "software":{"python":sys.version,"numpy":np.__version__,"scipy":scipy.__version__}
    },indent=2)+"\n",encoding="utf-8")
    print("EMT-I complete:",outcome)
    print("Report:",rp)

if __name__=="__main__":
    try:
        raise SystemExit(main())
    except EMTError as e:
        print("EMT-I ERROR:",e,file=sys.stderr)
        raise SystemExit(2)

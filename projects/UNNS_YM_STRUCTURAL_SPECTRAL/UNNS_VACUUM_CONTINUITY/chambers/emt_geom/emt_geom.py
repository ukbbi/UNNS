#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, json, math, csv, sys
from datetime import datetime, timezone
import numpy as np, pandas as pd
from scipy.optimize import least_squares
from scipy.special import k0

class E(Exception): pass
def sha(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()
def basis(f,x,l):
    if f=="exponential": return np.exp(-x/l)
    if f=="bessel_K0": return k0(x/l)
    raise E(f)
def fit(f,pos,x,y,s,R):
    best=None; ymin=max(float(np.min(y)),0.0)
    for l0 in [R*m for m in (1/16,1/8,1/4,1/2,1,2)]:
        b0=basis(f,x,l0); A0=max(float(np.median(np.maximum(y,1e-14)/np.maximum(b0,1e-14))),1e-12)
        ds=[0.0] if not pos else [0,.25*ymin,.5*ymin,1*ymin]
        for d0 in ds:
            p0=np.array([A0,l0,d0]) if pos else np.array([A0,l0])
            lb=np.zeros_like(p0); lb[1]=1e-9; ub=np.full_like(p0,np.inf)
            def res(p):
                A,l=p[:2]; d=p[2] if pos else 0
                return (y-(d+A*basis(f,x,l)))/s
            try: z=least_squares(res,p0,bounds=(lb,ub),xtol=1e-13,ftol=1e-13,gtol=1e-13,max_nfev=30000)
            except Exception: continue
            chi=float(np.sum(z.fun*z.fun))
            if np.isfinite(chi) and (best is None or chi<best["chi2"]): best={"chi2":chi,"p":z.x}
    if best is None: raise E("fit failed")
    n=len(y); k=3 if pos else 2
    if n-k-1<=0: raise E("AICc undefined")
    a=best["chi2"]+2*k+2*k*(k+1)/(n-k-1); p=best["p"]
    return {"chi2":best["chi2"],"aicc":float(a),"A":float(p[0]),"lambda_fm":float(p[1]),
            "delta":float(p[2]) if pos else 0.0,"floor":"positive" if pos else "zero","n":n,"k":k}
def cls(d,thr):
    return "ZERO" if d>=thr else ("POSITIVE" if d<=-thr else "UNDECIDED")
def path(lo,hi):
    return not any(lo[i+1]>hi[i] for i in range(len(lo)-1))
def write_csv(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys()));w.writeheader();w.writerows(rows)

ap=argparse.ArgumentParser();ap.add_argument("--project-root",type=Path,default=Path("."));ap.add_argument("--validate-only",action="store_true")
args=ap.parse_args();root=args.project_root.resolve()
cfg=json.loads((Path(__file__).resolve().parent/"EMT_GEOM_CONFIG.json").read_text())
comps=["epsilon","sigma_zz","sigma_rr","sigma_theta"]
fitrows=[]; comprows=[]; results={}

for gid,g in cfg["geometries"].items():
    p=root/g["input"]
    if not p.exists(): raise E(f"missing {p}")
    if sha(p)!=g["sha256"]: raise E(f"{gid} input hash mismatch")
    df=pd.read_csv(p)
    if len(df)!=185: raise E(f"{gid} expected 185 rows")
    r=df.r_fm.to_numpy(float); R=g["R_fm"]; scale=R**4/cfg["hbar_c_GeV_fm"]
    Y=np.column_stack([df[f"{c}_GeV_fm3"].to_numpy(float) for c in comps])
    S=np.column_stack([df[f"{c}_err_GeV_fm3"].to_numpy(float) for c in comps])
    A=np.abs(Y); D=scale*np.sqrt(np.mean(Y*Y,axis=1))
    lo=scale*np.sqrt(np.mean(np.maximum(A-S,0)**2,axis=1)); hi=scale*np.sqrt(np.mean((A+S)**2,axis=1))
    ds=np.maximum((hi-lo)/2,1e-12); pk=path(lo,hi)
    tail=r>=g["tail_cut_fm"]-1e-12
    if args.validate_only:
        results[gid]={"rows":len(df),"tail_points":int(tail.sum()),"path":pk}; continue
    normcls={}
    for cut,drop in (("PRIMARY",False),("DROP_FIRST",True)):
        inds=np.where(tail)[0]; inds=inds[1:] if drop else inds
        normcls[cut]={}
        for fam in cfg["families"]:
            z=fit(fam,False,r[inds],D[inds],ds[inds],R); q=fit(fam,True,r[inds],D[inds],ds[inds],R)
            delta=q["aicc"]-z["aicc"]; c=cls(delta,cfg["delta_AICc_decisive"]); normcls[cut][fam]=c
            for m in (z,q): fitrows.append({"geometry":gid,"R_fm":R,"target":"D_EMT","tail_cut":cut,"family":fam,
                **m,"delta_AICc_floor_minus_zero":delta,"classification":c})
    labels={}
    for j,cname in enumerate(comps):
        mag=np.abs(Y[:,j]); sig=S[:,j]; clo=np.maximum(mag-sig,0); chi=mag+sig; cpath=path(clo,chi); cc=[]
        for cut,drop in (("PRIMARY",False),("DROP_FIRST",True)):
            inds=np.where(tail)[0]; inds=inds[1:] if drop else inds
            for fam in cfg["families"]:
                z=fit(fam,False,r[inds],mag[inds],sig[inds],R); q=fit(fam,True,r[inds],mag[inds],sig[inds],R)
                delta=q["aicc"]-z["aicc"]; c=cls(delta,cfg["delta_AICc_decisive"]); cc.append(c)
                comprows.append({"geometry":gid,"R_fm":R,"component":cname,"tail_cut":cut,"family":fam,
                    "delta_AICc_floor_minus_zero":delta,"classification":c,"path_vacuum_directed":cpath})
        labels[cname]="NONZERO-FLOOR" if all(v=="POSITIVE" for v in cc) else \
                      ("VACUUM-DIRECTED" if all(v=="ZERO" for v in cc) and cpath else \
                       ("NONMONOTONE" if not cpath else "UNCERTAINTY-LIMITED"))
    nv=[normcls[t][f] for t in normcls for f in cfg["families"]]
    anyfloor=any(v=="NONZERO-FLOOR" for v in labels.values())
    if all(v=="POSITIVE" for v in nv):
        out="EMT-POSITIVE-FLOOR"
    elif all(v=="ZERO" for v in nv) and pk and not anyfloor:
        out="EMT-CONTINUITY-CONSISTENT"
    elif anyfloor and any(v=="ZERO" for v in nv):
        out="EMT-REPRESENTATION-SPLIT"
    else:
        out="EMT-UNCERTAINTY-LIMITED"
    results[gid]={"R_fm":R,"tail_points":int(tail.sum()),"path_vacuum_directed":pk,"norm_classes":normcls,
                  "component_labels":labels,"outcome":out}

if args.validate_only:
    print("EMT secondary-geometry validation: PASS")
    for gid,v in results.items(): print(gid,v)
    print("No scientific fit performed (--validate-only).")
    raise SystemExit(0)

outs=[results[k]["outcome"] for k in ("R046","R092")]
nofloor=all(results[k]["path_vacuum_directed"] and results[k]["outcome"]!="EMT-POSITIVE-FLOOR"
            and all(v!="NONZERO-FLOOR" for v in results[k]["component_labels"].values()) for k in ("R046","R092"))
if nofloor: synthesis="GEOMETRY-ROBUST-NO-FLOOR"
elif all(o=="EMT-POSITIVE-FLOOR" for o in outs): synthesis="GEOMETRY-POSITIVE-FLOOR"
elif ("EMT-POSITIVE-FLOOR" in outs) or ("EMT-REPRESENTATION-SPLIT" in outs): synthesis="GEOMETRY-SPLIT"
else: synthesis="GEOMETRY-UNCERTAINTY-LIMITED"

write_csv(root/cfg["outputs"]["fits"],fitrows);write_csv(root/cfg["outputs"]["components"],comprows)
rp=root/cfg["outputs"]["report"];rp.parent.mkdir(parents=True,exist_ok=True)
lines=["# Yanagihara EMT Secondary Geometry Report","",f"**Synthesis:** **{synthesis}**","",
       "The primary `R=0.69 fm` verdict remains `EMT-UNCERTAINTY-LIMITED`.",""]
for gid in ("R046","R092"):
    v=results[gid]
    lines += [f"## {gid} — R={v['R_fm']:.2f} fm",
              f"- outcome: **{v['outcome']}**",
              f"- four-component norm path: {'VACUUM-DIRECTED' if v['path_vacuum_directed'] else 'NONMONOTONE'}",
              f"- tail points: {v['tail_points']}",
              f"- components: {v['component_labels']}",""]
rp.write_text("\n".join(lines)+"\n",encoding="utf-8")
jp=root/cfg["outputs"]["run_json"];jp.parent.mkdir(parents=True,exist_ok=True)
jp.write_text(json.dumps({"schema":"UNNS_EMT_GEOM_RUN_v1","run_utc":datetime.now(timezone.utc).isoformat(),
                          "synthesis":synthesis,"primary_R069_locked":"EMT-UNCERTAINTY-LIMITED","geometries":results},indent=2)+"\n",encoding="utf-8")
print("EMT geometry checks complete:",synthesis)
print("Report:",rp)

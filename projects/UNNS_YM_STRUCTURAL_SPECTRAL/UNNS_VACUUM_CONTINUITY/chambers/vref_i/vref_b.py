#!/usr/bin/env python3
from __future__ import annotations

import argparse, csv, hashlib, json, math, platform, sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

try:
    from scipy.interpolate import PchipInterpolator
    from scipy.optimize import least_squares
    from scipy.special import k0
    import scipy
except Exception as exc:
    raise SystemExit(
        "VREF-I/B requires SciPy. Run INSTALL_VREF_B_DEPS.bat first.\n"
        f"Import error: {exc}"
    )

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except Exception as exc:
    raise SystemExit(f"Matplotlib import failed: {exc}")


class VREFBError(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def load_cfg(script_dir: Path) -> dict:
    p = script_dir / "VREF_B_CONFIG.json"
    if not p.exists():
        raise VREFBError(f"Missing config: {p}")
    return json.loads(p.read_text(encoding="utf-8"))


def read_points(path: Path):
    import pandas as pd
    df = pd.read_csv(path)
    required = {
        "source_id","refinement","beta","point_index","x_fm","E_GeV2",
        "published_error_GeV2","eps_quant_GeV2","fit_sigma_GeV2"
    }
    if not required.issubset(df.columns):
        raise VREFBError(f"Missing CSV columns: {sorted(required-set(df.columns))}")
    if len(df) != 22:
        raise VREFBError(f"Expected 22 extracted rows, got {len(df)}")
    for c in ["x_fm","E_GeV2","published_error_GeV2","eps_quant_GeV2","fit_sigma_GeV2"]:
        if not np.all(np.isfinite(df[c].to_numpy(float))):
            raise VREFBError(f"Non-finite values in {c}")
    return df


def interp_linear(x, y, xq):
    if np.min(xq) < np.min(x)-1e-12 or np.max(xq) > np.max(x)+1e-12:
        raise VREFBError("Extrapolation requested")
    return np.interp(xq, x, y)


def rms(v):
    v = np.asarray(v, float)
    return float(np.sqrt(np.mean(v*v)))


def rms_box(z, s):
    a = np.maximum(np.abs(z)-s, 0.0)
    b = np.abs(z)+s
    return rms(a), rms(b)


def make_common(r1, r2, hbarc, d_fm, mode):
    xmax = min(r1["x"].max(), r2["x"].max())
    mask = r1["x"] <= xmax + 1e-12
    xg = r1["x"][mask]
    e1 = r1["E"][mask]
    p1 = r1["pub"][mask]

    if mode == "linear":
        e2 = interp_linear(r2["x"], r2["E"], xg)
    elif mode == "pchip":
        e2 = PchipInterpolator(r2["x"], r2["E"], extrapolate=False)(xg)
    else:
        raise VREFBError(mode)

    p2 = interp_linear(r2["x"], r2["pub"], xg)
    scale = (d_fm/hbarc)**2
    return {
        "x": xg,
        "E1": e1, "E2": np.asarray(e2,float),
        "pub1": p1, "pub2": p2,
        "z1": scale*e1, "z2": scale*np.asarray(e2,float),
        "sz1": scale*np.sqrt(p1*p1 + r1["epsq"]**2),
        "sz2": scale*np.sqrt(p2*p2 + r2["epsq"]**2),
    }


def path_windows(common, m=5):
    rows=[]
    for ref in ("R1","R2"):
        z = common["z1"] if ref=="R1" else common["z2"]
        s = common["sz1"] if ref=="R1" else common["sz2"]
        for k in range(len(z)-m+1):
            zz=z[k:k+m]; ss=s[k:k+m]
            d=rms(zz); lo,hi=rms_box(zz,ss)
            rows.append({"refinement":ref,"window":k,
                         "start_x_fm":common["x"][k],
                         "end_x_fm":common["x"][k+m-1],
                         "D_RMS":d,"D_min":lo,"D_max":hi})
    return rows


def path_ok(rows):
    for ref in ("R1","R2"):
        rr=[r for r in rows if r["refinement"]==ref]
        rr=sorted(rr,key=lambda q:q["window"])
        for a,b in zip(rr[:-1],rr[1:]):
            if b["D_min"] > a["D_max"]:
                return False
    return True


def family_basis(name, x, lam):
    if name=="exponential":
        return np.exp(-x/lam)
    if name=="bessel_K0":
        return k0(x/lam)
    raise VREFBError(name)


def fit_model(family, positive_floor, data, d_fm, cfg):
    x=data["x"]; y=data["y"]; sig=data["sig"]; rid=data["rid"]
    ymin=max(float(np.min(y)),0.0)
    lams=[d_fm*m for m in cfg["fit"]["lambda_seed_multiples_of_d"]]
    deltas=[0.0] if not positive_floor else [
        f*ymin for f in cfg["fit"]["positive_floor_delta_seed_fractions_of_min_tail_y"]
    ]
    best=None

    for lam0 in lams:
        basis=family_basis(family,x,lam0)
        for delta0 in deltas:
            A=[]
            for r in (0,1):
                mm=rid==r
                denom=np.maximum(basis[mm],1e-12)
                guess=np.median(np.maximum(y[mm]-delta0,1e-10)/denom)
                A.append(max(float(guess),1e-10))
            if positive_floor:
                p0=np.array([A[0],A[1],lam0,max(delta0,0.0)])
                lb=np.array([0.0,0.0,1e-8,0.0])
                ub=np.array([np.inf,np.inf,np.inf,np.inf])
            else:
                p0=np.array([A[0],A[1],lam0])
                lb=np.array([0.0,0.0,1e-8])
                ub=np.array([np.inf,np.inf,np.inf])

            def residual(p):
                A1,A2,lam=p[:3]
                delta=p[3] if positive_floor else 0.0
                b=family_basis(family,x,lam)
                pred=delta + np.where(rid==0,A1,A2)*b
                return (y-pred)/sig

            try:
                res=least_squares(
                    residual,p0,bounds=(lb,ub),
                    xtol=cfg["fit"]["least_squares_xtol"],
                    ftol=cfg["fit"]["least_squares_ftol"],
                    gtol=cfg["fit"]["least_squares_gtol"],
                    max_nfev=cfg["fit"]["max_nfev"]
                )
            except Exception:
                continue
            chi=float(np.sum(res.fun**2))
            if not np.isfinite(chi):
                continue
            if best is None or chi < best["chi2"]:
                p=res.x
                best={"chi2":chi,"params":p,"success":bool(res.success)}

    if best is None:
        raise VREFBError(f"No converged fit for {family}, positive={positive_floor}")

    n=len(y); kpar=4 if positive_floor else 3
    if n-kpar-1 <= 0:
        raise VREFBError(f"AICc undefined: n={n}, k={kpar}")
    aicc=best["chi2"]+2*kpar+(2*kpar*(kpar+1))/(n-kpar-1)
    p=best["params"]
    return {
        "family":family,
        "floor":"positive" if positive_floor else "zero",
        "chi2":best["chi2"],"aicc":float(aicc),"n":n,"k":kpar,
        "A1":float(p[0]),"A2":float(p[1]),"lambda_fm":float(p[2]),
        "delta_GeV2":float(p[3]) if positive_floor else 0.0,
    }


def build_tail(r1,r2,xmax,tail_cut,drop_first=False):
    pieces=[]
    for idx,r in enumerate((r1,r2)):
        mask=(r["x"]>=tail_cut-1e-12)&(r["x"]<=xmax+1e-12)
        inds=np.where(mask)[0]
        if drop_first:
            inds=inds[1:]
        for i in inds:
            pieces.append((r["x"][i],r["E"][i],r["fitsig"][i],idx))
    if not pieces:
        raise VREFBError("No tail points")
    arr=np.array(pieces,float)
    return {"x":arr[:,0],"y":arr[:,1],"sig":arr[:,2],"rid":arr[:,3].astype(int)}


def floor_class(delta_aicc, thr):
    if delta_aicc >= thr: return "ZERO"
    if delta_aicc <= -thr: return "POSITIVE"
    return "UNDECIDED"


def write_csv(path, rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    if not rows: return
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--project-root",type=Path,default=None)
    ap.add_argument("--validate-only",action="store_true")
    args=ap.parse_args()

    script_dir=Path(__file__).resolve().parent
    cfg=load_cfg(script_dir)
    root=args.project_root.resolve() if args.project_root else script_dir.parent.parent.resolve()

    csvp=root/cfg["input"]["points_csv"]
    jsp=root/cfg["input"]["extract_json"]
    if not csvp.exists() or not jsp.exists():
        raise VREFBError("Missing deterministic extraction outputs")
    if sha256_file(csvp)!=cfg["input"]["expected_points_csv_sha256"]:
        raise VREFBError("Extracted CSV SHA-256 mismatch")
    meta=json.loads(jsp.read_text(encoding="utf-8"))
    if meta.get("status")!="EXTRACTION-VALID":
        raise VREFBError("Extraction JSON is not EXTRACTION-VALID")
    if meta.get("output_csv",{}).get("sha256")!=cfg["input"]["expected_points_csv_sha256"]:
        raise VREFBError("Extraction JSON/CSV hash disagreement")

    df=read_points(csvp)
    rs={}
    for ref in ("R1","R2"):
        q=df[df["refinement"]==ref].sort_values("x_fm")
        if len(q)!=11: raise VREFBError(f"{ref}: expected 11 rows")
        rs[ref]={
            "x":q["x_fm"].to_numpy(float),
            "E":q["E_GeV2"].to_numpy(float),
            "pub":q["published_error_GeV2"].to_numpy(float),
            "fitsig":q["fit_sigma_GeV2"].to_numpy(float),
            "epsq":float(q["eps_quant_GeV2"].iloc[0]),
        }

    hbarc=cfg["physics"]["hbar_c_GeV_fm"]; d=cfg["physics"]["d_fm"]
    clin=make_common(rs["R1"],rs["R2"],hbarc,d,"linear")
    cpch=make_common(rs["R1"],rs["R2"],hbarc,d,"pchip")
    xmax=min(rs["R1"]["x"].max(),rs["R2"]["x"].max())
    tailcut=cfg["physics"]["tail_cut_fm"]

    if args.validate_only:
        n1=int(np.sum((rs["R1"]["x"]>=tailcut)&(rs["R1"]["x"]<=xmax)))
        n2=int(np.sum((rs["R2"]["x"]>=tailcut)&(rs["R2"]["x"]<=xmax)))
        print("VREF-I/B chamber validation: PASS")
        print(f"CSV sha256: {sha256_file(csvp)}")
        print(f"common-grid points: {len(clin['x'])}")
        print(f"common support xmax: {xmax:.9f} fm")
        print(f"native primary-tail points: R1={n1}, R2={n2}")
        print(f"numpy={np.__version__}; scipy={scipy.__version__}; matplotlib={matplotlib.__version__}")
        print("No scientific fit was performed (--validate-only).")
        return 0

    m=cfg["vref"]["window_points"]
    winlin=path_windows(clin,m); winpch=path_windows(cpch,m)
    ok_lin=path_ok(winlin); ok_pch=path_ok(winpch)
    interpolation_sensitive=(ok_lin!=ok_pch)

    # Common-grid refinement diagnostic
    refrows=[]
    qvals=[]
    tail_indices=np.where(clin["x"]>=tailcut-1e-12)[0]
    epsq=rs["R1"]["epsq"]
    for j in tail_indices:
        denom=math.sqrt(clin["pub1"][j]**2+clin["pub2"][j]**2+epsq**2)
        q=(clin["E1"][j]-clin["E2"][j])/denom
        qvals.append(q)
        refrows.append({
            "j":int(j),"x_fm":float(clin["x"][j]),
            "E_R1_GeV2":float(clin["E1"][j]),
            "E_R2_linear_GeV2":float(clin["E2"][j]),
            "Q":float(q)
        })
    mismatch=False
    thr=cfg["refinement_consistency"]["Q_threshold"]
    for a,b in zip(qvals[:-1],qvals[1:]):
        if abs(a)>=thr and abs(b)>=thr and np.sign(a)==np.sign(b):
            mismatch=True
    chi_ref=float(np.sum(np.asarray(qvals)**2))
    red_ref=chi_ref/len(qvals) if qvals else float("nan")

    fitrows=[]
    classes={}
    for cutname,drop in (("PRIMARY_TAIL",False),("DROP_FIRST_TAIL_POINT",True)):
        data=build_tail(rs["R1"],rs["R2"],xmax,tailcut,drop_first=drop)
        classes[cutname]={}
        for fam in cfg["tail_models"]["families"]:
            f0=fit_model(fam,False,data,d,cfg)
            fd=fit_model(fam,True,data,d,cfg)
            delta=fd["aicc"]-f0["aicc"]
            cls=floor_class(delta,cfg["tail_models"]["delta_AICc_decisive"])
            classes[cutname][fam]=cls
            for obj in (f0,fd):
                row={"tail_cut":cutname,**obj}
                row["delta_AICc_floor_minus_zero"]=float(delta)
                row["family_classification"]=cls
                fitrows.append(row)

    # Outcome priority
    if interpolation_sensitive:
        outcome="INTERPOLATION-SENSITIVE"
    elif mismatch:
        outcome="REFINEMENT-INDETERMINATE"
    else:
        pE=classes["PRIMARY_TAIL"]["exponential"]
        pK=classes["PRIMARY_TAIL"]["bessel_K0"]
        sE=classes["DROP_FIRST_TAIL_POINT"]["exponential"]
        sK=classes["DROP_FIRST_TAIL_POINT"]["bessel_K0"]
        if (pE,pK) in (("ZERO","POSITIVE"),("POSITIVE","ZERO")) or \
           (sE,sK) in (("ZERO","POSITIVE"),("POSITIVE","ZERO")):
            outcome="MODEL-SPLIT"
        elif pE==pK==sE==sK=="POSITIVE":
            outcome="ISOLATION-SUPPORTED"
        elif pE==pK==sE==sK=="ZERO" and ok_lin and ok_pch:
            outcome="CONTINUITY-SUPPORTED"
        else:
            outcome="UNCERTAINTY-LIMITED"

    # Tables
    commonrows=[]
    for j,x in enumerate(clin["x"]):
        commonrows.append({
            "j":j,"x_fm":float(x),
            "E_R1_GeV2":float(clin["E1"][j]),
            "E_R2_linear_GeV2":float(clin["E2"][j]),
            "E_R2_pchip_GeV2":float(cpch["E2"][j]),
            "pub_R1_GeV2":float(clin["pub1"][j]),
            "pub_R2_interp_GeV2":float(clin["pub2"][j]),
        })
    winrows=[]
    for mode,rows in (("linear",winlin),("pchip",winpch)):
        for r in rows: winrows.append({"interpolation":mode,**r})

    outs=cfg["outputs"]
    write_csv(root/outs["common_csv"],commonrows)
    write_csv(root/outs["windows_csv"],winrows)
    write_csv(root/outs["fits_csv"],fitrows)
    write_csv(root/outs["refinement_csv"],refrows)

    # Figures
    p=root/outs["profile_png"]; p.parent.mkdir(parents=True,exist_ok=True)
    fig=plt.figure(figsize=(8,5.2)); ax=fig.add_subplot(111)
    for ref in ("R1","R2"):
        rr=rs[ref]
        ax.errorbar(rr["x"],rr["E"],yerr=rr["pub"],marker="o",capsize=2,label=ref)
    ax.axhline(0,linewidth=1)
    ax.axvline(tailcut,linestyle="--",linewidth=1)
    ax.set_xlabel(r"$x_t$ [fm]"); ax.set_ylabel(r"$E_l$ [GeV$^2$]")
    ax.set_title("VREF-I/B native vacuum-referenced profiles"); ax.legend()
    ax.grid(True,alpha=0.25); fig.tight_layout(); fig.savefig(p,dpi=180); plt.close(fig)

    p=root/outs["distance_png"]; p.parent.mkdir(parents=True,exist_ok=True)
    fig=plt.figure(figsize=(8,5.2)); ax=fig.add_subplot(111)
    for ref in ("R1","R2"):
        rr=[r for r in winlin if r["refinement"]==ref]
        ax.errorbar([r["start_x_fm"] for r in rr],[r["D_RMS"] for r in rr],
                    yerr=np.array([[r["D_RMS"]-r["D_min"] for r in rr],
                                   [r["D_max"]-r["D_RMS"] for r in rr]]),
                    marker="o",capsize=2,label=ref)
    ax.set_xlabel("window start [fm]"); ax.set_ylabel(r"$D_{\rm VREF}$")
    ax.set_title("VREF-I/B fixed-width structural distance"); ax.legend()
    ax.grid(True,alpha=0.25); fig.tight_layout(); fig.savefig(p,dpi=180); plt.close(fig)

    # Report
    def dA(cut,fam):
        rr=[r for r in fitrows if r["tail_cut"]==cut and r["family"]==fam]
        return rr[0]["delta_AICc_floor_minus_zero"]
    report=f"""# VREF-I/B Primary Report

**Source:** `CEA_2017_SU3`  
**Outcome:** **{outcome}**

## Integrity

- deterministic extraction: VALID
- extracted CSV SHA-256: `{sha256_file(csvp)}`
- rows: 22
- common-grid points: {len(clin['x'])}
- common support: 0 to {xmax:.9f} fm
- primary tail cut: x >= {tailcut:.3f} fm

## VREF path

- linear path: {"VACUUM-DIRECTED" if ok_lin else "PATH-NONMONOTONE"}
- PCHIP path: {"VACUUM-DIRECTED" if ok_pch else "PATH-NONMONOTONE"}
- interpolation-sensitive: {str(interpolation_sensitive).lower()}

## Refinement diagnostic

- tail common-grid points: {len(qvals)}
- chi2_ref / N_tail: {red_ref:.8g}
- structured mismatch: {str(mismatch).lower()}

## Floor-model comparison

| tail | family | Delta AICc = floor - zero | classification |
|---|---|---:|---|
| PRIMARY | exponential | {dA("PRIMARY_TAIL","exponential"):.8g} | {classes["PRIMARY_TAIL"]["exponential"]} |
| PRIMARY | K0 | {dA("PRIMARY_TAIL","bessel_K0"):.8g} | {classes["PRIMARY_TAIL"]["bessel_K0"]} |
| DROP-FIRST | exponential | {dA("DROP_FIRST_TAIL_POINT","exponential"):.8g} | {classes["DROP_FIRST_TAIL_POINT"]["exponential"]} |
| DROP-FIRST | K0 | {dA("DROP_FIRST_TAIL_POINT","bessel_K0"):.8g} | {classes["DROP_FIRST_TAIL_POINT"]["bessel_K0"]} |

Decisive threshold: `|Delta AICc| >= 6`.

Positive Delta AICc favors zero floor. Negative Delta AICc favors positive floor.

## Scope

This is a structural-vacuum-accessibility verdict in the frozen VREF representation. It is not a verdict that the physical Yang-Mills Hamiltonian mass gap vanishes or closes.
"""
    rp=root/outs["report_md"]; rp.parent.mkdir(parents=True,exist_ok=True); rp.write_text(report,encoding="utf-8")

    run={
        "schema":"UNNS_VREF_I_B_RUN_v1",
        "run_utc":datetime.now(timezone.utc).isoformat(),
        "outcome":outcome,
        "input_csv_sha256":sha256_file(csvp),
        "path":{"linear":ok_lin,"pchip":ok_pch,"interpolation_sensitive":interpolation_sensitive},
        "refinement":{"q":qvals,"chi2_per_tail_point":red_ref,"structured_mismatch":mismatch},
        "floor_classes":classes,
        "software":{"python":sys.version,"numpy":np.__version__,"scipy":scipy.__version__,"matplotlib":matplotlib.__version__},
        "outputs":outs
    }
    jp=root/outs["run_json"]; jp.parent.mkdir(parents=True,exist_ok=True)
    jp.write_text(json.dumps(run,indent=2)+"\n",encoding="utf-8")

    print(f"VREF-I/B complete: {outcome}")
    print(f"Report: {rp}")
    return 0


if __name__=="__main__":
    try:
        raise SystemExit(main())
    except VREFBError as exc:
        print(f"VREF-I/B ERROR: {exc}",file=sys.stderr)
        raise SystemExit(2)

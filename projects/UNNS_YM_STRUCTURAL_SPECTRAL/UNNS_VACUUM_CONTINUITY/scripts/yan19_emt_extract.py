#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, json
import fitz
import pandas as pd
import numpy as np

SOURCE_SHA = "fe549266b6a2483aa0c0104835ddf3215a9b2d8812110aacb86ea2368aa10423"
R_FM = 0.69
PANEL = fitz.Rect(550.7438, 10.7, 1052.9437, 382.148)
X_ZERO = 576.0344
X_TICK_01 = 648.2934
Y_ZERO = 367.3885
Y_TICK_2 = 318.1901

COLORS = {
    "epsilon": (0.8392156958580017,0.15294118225574493,0.1568627506494522),
    "sigma_zz": (0.12156862765550613,0.46666666865348816,0.7058823704719543),
    "T_rr": (1.0,0.49803921580314636,0.054901961237192154),
    "T_theta": (0.1725490242242813,0.6274510025978088,0.1725490242242813),
}
SIGNS = {"epsilon":1.0,"sigma_zz":1.0,"T_rr":-1.0,"T_theta":-1.0}
PHYS = {"epsilon":"epsilon","sigma_zz":"sigma_zz","T_rr":"sigma_rr","T_theta":"sigma_theta"}
PLOT_LABEL = {"epsilon":"-T44","sigma_zz":"-Tzz","T_rr":"Trr","T_theta":"Ttheta"}

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def rect_match(a,b,tol=0.03):
    return a is not None and max(abs(a.x0-b.x0),abs(a.x1-b.x1),abs(a.y0-b.y0),abs(a.y1-b.y1)) < tol

def color_match(a,b,tol=1e-6):
    return a is not None and max(abs(a[i]-b[i]) for i in range(3)) < tol

def x_to_fm(x):
    return (x-X_ZERO)*0.1/(X_TICK_01-X_ZERO)

def y_to_val(y):
    return (Y_ZERO-y)*2.0/(Y_ZERO-Y_TICK_2)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--project-root",type=Path,default=Path("."))
    args=ap.parse_args()
    root=args.project_root.resolve()
    src=root/"data"/"raw"/"yanagihara_2019"/"mid_separates.pdf"
    if not src.exists():
        raise SystemExit(f"Missing {src}")
    if sha(src)!=SOURCE_SHA:
        raise SystemExit("mid_separates.pdf SHA-256 mismatch")

    page=fitz.open(src)[0]
    ds=page.get_drawings(extended=True)
    active={}
    markers={k:[] for k in COLORS}
    caps={k:[] for k in COLORS}

    for d in ds:
        lvl=int(d.get("level",0))
        for k in list(active):
            if k>=lvl: active.pop(k,None)
        if d["type"]=="clip":
            active[lvl]=d.get("scissor")
            continue
        if not rect_match(active.get(1),PANEL):
            continue
        r=d.get("rect")
        if r is None: continue
        series=next((n for n,c in COLORS.items() if color_match(d.get("color"),c)),None)
        if series is None: continue
        cx=(r.x0+r.x1)/2; cy=(r.y0+r.y1)/2
        if d["type"]=="s" and abs(r.width-15)<0.03 and abs(r.height-15)<0.03 and PANEL.x0<=cx<=PANEL.x1 and PANEL.y0<=cy<=PANEL.y1:
            markers[series].append((cx,cy))
        elif d["type"]=="fs" and abs(r.width-24)<0.03 and r.height<0.03 and PANEL.x0<=cx<=PANEL.x1:
            caps[series].append((cx,cy))

    rows=[]; grids={}
    for series in COLORS:
        ms=sorted(markers[series],key=lambda q:q[0])
        if len(ms)!=185 or len(caps[series])!=370:
            raise SystemExit(f"{series} count check failed: markers={len(ms)}, caps={len(caps[series])}")
        grid=[]
        for idx,(cx,cy) in enumerate(ms):
            pair=[(x,y) for x,y in caps[series] if abs(x-cx)<0.001]
            if len(pair)!=2:
                raise SystemExit(f"{series} point {idx} cap match failed")
            ys=sorted(y for _,y in pair)
            if abs((ys[0]+ys[1])/2-cy)>0.001:
                raise SystemExit(f"{series} point {idx} midpoint check failed")
            r_fm=x_to_fm(cx); pv=y_to_val(cy)
            err=((ys[1]-ys[0])/2)*2.0/(Y_ZERO-Y_TICK_2)
            rows.append({
                "source_id":"YANAGIHARA_2019_EMT","R_fm":R_FM,"point_index":idx,"r_fm":r_fm,
                "source_series":series,"plotted_quantity":PLOT_LABEL[series],
                "physical_component":PHYS[series],"plot_value_GeV_fm3":pv,
                "physical_value_GeV_fm3":SIGNS[series]*pv,"error_GeV_fm3":err,
                "X_page_pt":cx,"Y_page_pt":cy,"Yerr_low_page_pt":ys[0],"Yerr_high_page_pt":ys[1]
            })
            grid.append(r_fm)
        grids[series]=np.asarray(grid)

    base=grids["epsilon"]
    for series,g in grids.items():
        if len(g)!=len(base) or np.max(np.abs(g-base))>1e-12:
            raise SystemExit("Cross-component native grid mismatch")

    out=root/"data"/"derived"/"yanagihara_2019"
    out.mkdir(parents=True,exist_ok=True)
    pts=pd.DataFrame(rows)
    pts.to_csv(out/"YAN19_EMT_POINTS.csv",index=False,float_format="%.15g")

    common=pd.DataFrame({"point_index":np.arange(len(base)),"r_fm":base})
    for comp in ["epsilon","sigma_zz","sigma_rr","sigma_theta"]:
        q=pts[pts.physical_component==comp].sort_values("point_index")
        common[f"{comp}_GeV_fm3"]=q.physical_value_GeV_fm3.to_numpy(float)
        common[f"{comp}_err_GeV_fm3"]=q.error_GeV_fm3.to_numpy(float)
    common.to_csv(out/"YAN19_EMT_COMMON.csv",index=False,float_format="%.15g")

    rec={
        "schema":"YAN19_EMT_EXTRACT_v1","status":"EXTRACTION-VALID","source_pdf_sha256":SOURCE_SHA,
        "R_fm":R_FM,"points_per_component":185,"common_native_grid":True,
        "interpolation_required":False,"r_min_fm":float(base[0]),"r_max_fm":float(base[-1]),
        "primary_tail_cut_fm":R_FM/2,"primary_tail_points":int((base>=R_FM/2).sum()),
        "scientific_fit_performed":False
    }
    (out/"YAN19_EMT_EXTRACT.json").write_text(json.dumps(rec,indent=2)+"\n",encoding="utf-8")
    print("YANAGIHARA EMT extraction: EXTRACTION-VALID")
    print("185 common native points per component")
    print("No scientific EMT-I fit was performed.")

if __name__=="__main__":
    main()

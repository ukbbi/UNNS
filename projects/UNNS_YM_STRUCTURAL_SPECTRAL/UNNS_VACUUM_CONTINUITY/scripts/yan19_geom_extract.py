#!/usr/bin/env python3
from pathlib import Path
import fitz, hashlib, json
import pandas as pd
import numpy as np

SOURCE_SHA="fe549266b6a2483aa0c0104835ddf3215a9b2d8812110aacb86ea2368aa10423"
Y_ZERO=367.38848876953125
Y_TICK_2=318.1900939941406
PANELS={'R046': {'R_fm': 0.46, 'rect': [48.54375076293945, 10.699981689453125, 550.7437744140625, 382.14801025390625], 'x_zero': 73.83439636230469, 'x_tick_01': 146.09339904785156}, 'R092': {'R_fm': 0.92, 'rect': [1052.9437255859375, 10.699981689453125, 1555.143798828125, 382.14801025390625], 'x_zero': 1078.234375, 'x_tick_01': 1150.493408203125}}
COLORS={'epsilon': (0.8392156958580017, 0.15294118225574493, 0.1568627506494522), 'sigma_zz': (0.12156862765550613, 0.46666666865348816, 0.7058823704719543), 'T_rr': (1.0, 0.49803921580314636, 0.054901961237192154), 'T_theta': (0.1725490242242813, 0.6274510025978088, 0.1725490242242813)}
SIGNS={'epsilon': 1.0, 'sigma_zz': 1.0, 'T_rr': -1.0, 'T_theta': -1.0}
PHYS={'epsilon': 'epsilon', 'sigma_zz': 'sigma_zz', 'T_rr': 'sigma_rr', 'T_theta': 'sigma_theta'}
PLOT_LABEL={'epsilon': '-T44', 'sigma_zz': '-Tzz', 'T_rr': 'Trr', 'T_theta': 'Ttheta'}

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rect_match(a,b,tol=.03):
    return a is not None and max(abs(a.x0-b.x0),abs(a.x1-b.x1),abs(a.y0-b.y0),abs(a.y1-b.y1))<tol
def color_match(a,b,tol=1e-6):
    return a is not None and max(abs(a[i]-b[i]) for i in range(3))<tol

root=Path(__file__).resolve().parent.parent
src=root/"data"/"raw"/"yanagihara_2019"/"mid_separates.pdf"
if not src.exists(): raise SystemExit(f"Missing {src}")
if sha(src)!=SOURCE_SHA: raise SystemExit("mid_separates.pdf SHA-256 mismatch")

page=fitz.open(src)[0]
drawings=page.get_drawings(extended=True)
out=root/"data"/"derived"/"yanagihara_2019"/"geom"
out.mkdir(parents=True,exist_ok=True)

for gid,meta in PANELS.items():
    panel=fitz.Rect(*meta["rect"])
    markers={k:[] for k in COLORS}; caps={k:[] for k in COLORS}; active={}
    for d in drawings:
        lvl=int(d.get("level",0))
        for k in list(active):
            if k>=lvl: active.pop(k,None)
        if d["type"]=="clip":
            active[lvl]=d.get("scissor"); continue
        if not rect_match(active.get(1),panel): continue
        r=d.get("rect")
        if r is None: continue
        series=next((n for n,c in COLORS.items() if color_match(d.get("color"),c)),None)
        if series is None: continue
        cx=(r.x0+r.x1)/2; cy=(r.y0+r.y1)/2
        if d["type"]=="s" and abs(r.width-15)<.03 and abs(r.height-15)<.03 and panel.x0<=cx<=panel.x1 and panel.y0<=cy<=panel.y1:
            markers[series].append((cx,cy))
        elif d["type"]=="fs" and abs(r.width-24)<.03 and r.height<.03 and panel.x0<=cx<=panel.x1:
            caps[series].append((cx,cy))

    def xf(x): return (x-meta["x_zero"])*.1/(meta["x_tick_01"]-meta["x_zero"])
    def yf(y): return (Y_ZERO-y)*2.0/(Y_ZERO-Y_TICK_2)
    rows=[]; grids={}
    for series in COLORS:
        ms=sorted(markers[series],key=lambda q:q[0])
        if len(ms)!=185 or len(caps[series])!=370:
            raise SystemExit(f"{gid} {series} count check failed")
        g=[]
        for i,(cx,cy) in enumerate(ms):
            pair=[(x,y) for x,y in caps[series] if abs(x-cx)<.001]
            if len(pair)!=2: raise SystemExit("cap match failed")
            ys=sorted(y for _,y in pair)
            if abs((ys[0]+ys[1])/2-cy)>.001: raise SystemExit("midpoint check failed")
            pv=yf(cy); err=((ys[1]-ys[0])/2)*2.0/(Y_ZERO-Y_TICK_2)
            rows.append({"source_id":"YANAGIHARA_2019_EMT","geometry_id":gid,"R_fm":meta["R_fm"],
                "point_index":i,"r_fm":xf(cx),"source_series":series,"plotted_quantity":PLOT_LABEL[series],
                "physical_component":PHYS[series],"plot_value_GeV_fm3":pv,
                "physical_value_GeV_fm3":SIGNS[series]*pv,"error_GeV_fm3":err})
            g.append(xf(cx))
        grids[series]=np.asarray(g)
    base=grids["epsilon"]
    for s,g in grids.items():
        if np.max(np.abs(g-base))>1e-12: raise SystemExit("grid mismatch")
    pts=pd.DataFrame(rows)
    pts.to_csv(out/f"{gid}_POINTS.csv",index=False,float_format="%.15g")
    common=pd.DataFrame({"point_index":np.arange(185),"r_fm":base})
    for comp in ["epsilon","sigma_zz","sigma_rr","sigma_theta"]:
        q=pts[pts.physical_component==comp].sort_values("point_index")
        common[f"{comp}_GeV_fm3"]=q.physical_value_GeV_fm3.to_numpy(float)
        common[f"{comp}_err_GeV_fm3"]=q.error_GeV_fm3.to_numpy(float)
    common.to_csv(out/f"{gid}_COMMON.csv",index=False,float_format="%.15g")
    print(gid,"EXTRACTION-VALID","tail points",int((base>=meta["R_fm"]/2).sum()))

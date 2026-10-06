#!/usr/bin/env python3
"""Rebuild SS23_B4 Class-B digitization and common-grid inputs.

Requires: Python 3.10+, PyMuPDF, numpy, pandas, scipy.
Input: data/raw/ss23/ss23.pdf
This script extracts vector marker geometry from the publication PDF; it does not OCR the figure.
"""
from pathlib import Path
import fitz, math, json
import numpy as np, pandas as pd
from scipy.interpolate import PchipInterpolator

ROOT=Path(__file__).resolve().parents[2]
PDF=ROOT/"data"/"raw"/"ss23"/"ss23.pdf"
OUT=ROOT/"data"/"derived"/"corr_i"/"ym3b"/"ss23"
COMMON=np.array([0.31,0.36,0.41,0.46,0.51,0.56,0.61])
INFO={
"6.20":("b620",10,9,(0.,0.,0.),(118.01799774169922,50.725990295410156,290.9429931640625,171.77398681640625),1.8,8,7.38),
"6.40":("b640",10,10,(1.,0.,0.),(118.01799774169922,394.1730041503906,290.9429931640625,515.2210083007812),1.4,10,9.74),
"6.71":("b671",11,11,(0.,0.,1.),(118.01799774169922,50.759986877441406,290.9429931640625,171.8079833984375),1.0,12,14.49),
"6.93":("b693",11,12,(0.,0.545098066329956,0.),(118.01799774169922,400.7749938964844,290.9429931640625,521.822998046875),0.8,16,19.48),
}
def circles(page,color,bb):
    x0,y0,x1,y1=bb; q=[]
    for i,d in enumerate(page.get_drawings()):
        r=d["rect"]; its=d["items"]
        if d.get("color")==color and r.x0>=x0-1 and r.x1<=x1+1 and r.y0>=y0-1 and r.y1<=y1+1:
            if 4.5<r.width<6 and 4.5<r.height<6 and len(its)==4 and all(a[0]=="c" for a in its):
                q.append(((r.x0+r.x1)/2,(r.y0+r.y1)/2))
    return sorted(q)
def progression(q,tmax):
    best=None
    for a in q:
      for z in q:
        if z[0]<=a[0]: continue
        s=(z[0]-a[0])/tmax
        if s<5: continue
        m=[]; e=0
        for t in range(tmax+1):
            trg=a[0]+t*s; c=min(q,key=lambda v:abs(v[0]-trg)); m.append(c); e+=abs(c[0]-trg)
        if best is None or e<best[0]: best=(e,m)
    return best[1]
def errbar(page,color,x,y):
    s=[]
    for d in page.get_drawings():
        if d.get("color")!=color: continue
        r=d["rect"]
        if abs(r.x0-x)<.03 and abs(r.x1-x)<.03 and r.height>0 and (abs(r.y0-y)<.12 or abs(r.y1-y)<.12):
            s.append((r.y0,r.y1))
    return (min(a for a,b in s),max(b for a,b in s)) if s else (y,y)
doc=fitz.open(PDF)
for beta,(sid,pno,fig,color,bb,ymax,tmax,r0a) in INFO.items():
    page=doc[pno]; pts=progression(circles(page,color,bb),tmax)
    rows=[]
    for t,(x,y) in enumerate(pts):
        m=(bb[3]-y)/(bb[3]-bb[1])*ymax
        yl,yh=errbar(page,color,x,y)
        hi=(bb[3]-yl)/(bb[3]-bb[1])*ymax; lo=(bb[3]-yh)/(bb[3]-bb[1])*ymax
        rows.append((t,m,m-lo,hi-m))
    d=pd.DataFrame(rows,columns=["t_over_a","meff","graph_err_minus","graph_err_plus"])
    (OUT/"digitized").mkdir(parents=True,exist_ok=True); d.to_csv(OUT/"digitized"/f"{sid}_meff.csv",index=False)
    lam=[1.]
    for m in d.meff: lam.append(lam[-1]*math.exp(-m))
    lam=np.array(lam); u=np.arange(len(lam))/r0a
    c=np.exp(np.interp(COMMON,u,np.log(lam))); c/=c[0]
    p=np.exp(PchipInterpolator(u,np.log(lam))(COMMON)); p/=p[0]
    (OUT/"common").mkdir(parents=True,exist_ok=True)
    (OUT/"common_pchip").mkdir(parents=True,exist_ok=True)
    pd.DataFrame({"t":COMMON,"corr":c,"channel":f"ss23_{sid}_B"}).to_csv(OUT/"common"/f"{sid}.csv",index=False)
    pd.DataFrame({"t":COMMON,"corr":p,"channel":f"ss23_{sid}_B_pchip"}).to_csv(OUT/"common_pchip"/f"{sid}.csv",index=False)
print("SS23_B4 rebuild complete.")

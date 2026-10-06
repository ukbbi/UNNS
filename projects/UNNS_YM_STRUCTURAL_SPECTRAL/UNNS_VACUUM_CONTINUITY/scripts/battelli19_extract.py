#!/usr/bin/env python3
from pathlib import Path
import re, tarfile, hashlib
import pandas as pd
import numpy as np

ARCHIVE_SHA="e4ffd183a5d995862b19b2e4ce73e812f5cc102b67dad8174a7a6a8b1ba14b15"
EPS_SHA="a211dc25d56e68d7e03638a120ade1b76fbd77a752a29f3c85fe2dcc79acbc70"

root=Path(__file__).resolve().parent.parent
archive=root/"data"/"raw"/"battelli_2019"/"arXiv-1903.10463v2.tar.gz"
out=root/"data"/"derived"/"battelli_2019"
out.mkdir(parents=True,exist_ok=True)

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

if not archive.exists():
    raise SystemExit(f"Missing {archive}")
if sha(archive)!=ARCHIVE_SHA:
    raise SystemExit("Battelli source archive SHA-256 mismatch")

with tarfile.open(archive,"r:gz") as tf:
    eps=tf.extractfile("el_withz.eps").read()
if hashlib.sha256(eps).hexdigest()!=EPS_SHA:
    raise SystemExit("el_withz.eps SHA-256 mismatch")

text=eps.decode("latin1")
anchor="n\n0.1500 0.1500 m\n1.1500 0.1500 l\ns"
end=text.find(anchor)
if end<0:
    raise SystemExit("Plot frame anchor not found")
block=text[:end]

pat=re.compile(
    r"\[/DeviceRGB\]\s+SCS\s+(Color\d+)\s+SC|"
    r"n\s+([0-9.]+)\s+([0-9.]+)\s+m\s+([0-9.]+)\s+([0-9.]+)\s+l\s+s"
)
events=[]; color=None
for m in pat.finditer(block):
    if m.group(1):
        color=m.group(1)
    else:
        x1,y1,x2,y2=map(float,m.group(2,3,4,5))
        events.append((color,x1,y1,x2,y2))

meta={
 "Color1":("B1",6.0,0.0931,4,5),
 "Color2":("B2",6.2601,0.0621,6,7),
 "Color4":("B3",6.47466,0.0456,8,6),
}
X0=0.1976; X4=1.1500; Y0=0.2136; Y20=0.8500
xf=lambda x:(x-X0)*0.4/(X4-X0)
yf=lambda y:(y-Y0)*20.0/(Y20-Y0)

rows=[]
for col,(ref,beta,a,d,expected) in meta.items():
    groups={}
    for c,x1,y1,x2,y2 in events:
        if c!=col or abs(x1-x2)>1e-8 or abs(y2-y1)>0.08: continue
        if x1<X0-1e-4 or x1>X4+1e-4: continue
        groups.setdefault(round(x1,4),[]).append((y1,y2))
    pts=[]
    for x,ss in sorted(groups.items()):
        if len(ss)!=2: continue
        ep=[v for pair in ss for v in pair]
        uniq=sorted(set(round(v,4) for v in ep))
        cc=[u for u in uniq if sum(abs(v-u)<5e-5 for v in ep)>=2]
        if not cc: continue
        yc=cc[0]
        pts.append((x,yc,min(ep),max(ep)))
    if len(pts)!=expected:
        raise SystemExit(f"{col} expected {expected} points, found {len(pts)}")
    for i,(x,y,lo,hi) in enumerate(pts):
        rows.append({
          "source_id":"BATTELLI_2019_SU3","refinement":ref,"beta":beta,
          "a_fm":a,"d_over_a":d,"point_index":i,
          "X_plot":x,"Y_plot":y,"Y_low_plot":lo,"Y_high_plot":hi,
          "d_t_fm":xf(x),"ZL_EL_div3_fm2":yf(y),
          "error_fm2":(yf(hi)-yf(lo))/2
        })

df=pd.DataFrame(rows)
df.to_csv(out/"BATTELLI_POINTS.csv",index=False,float_format="%.15g")
for ref in ("B1","B2","B3"):
    q=df[(df.refinement==ref)&(df.d_t_fm>1e-5)].sort_values("d_t_fm")
    pd.DataFrame({"value":q.ZL_EL_div3_fm2.to_numpy(float)}).to_csv(
        out/f"{ref}_POS.csv",index=False,float_format="%.15g"
    )
print("Battelli unsmoothed extraction: VALID")
print(df.groupby("refinement").size().to_dict())
print("Admitted d_t>0 ladder sizes:",
      {r:int(((df.refinement==r)&(df.d_t_fm>1e-5)).sum()) for r in ("B1","B2","B3")})

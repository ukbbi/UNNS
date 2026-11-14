import sys, os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from paths import *
"""Iterate the certified return map from the table; step counts from steps = L0(a,rho)+4620 t."""
import json, csv, sys
D=json.load(open(INH+'/concrete_itineraries.json'))
# check affine step counts
bad=0; L0={}
for a in (0,1):
  for rho in range(98):
    st=[D[f'{a},{rho},{t}']['steps'] for t in range(8)]
    L0[(a,rho)]=st[0]
    if any(st[t]!=st[0]+4620*t for t in range(8)): bad+=1
print('step-affine violations',bad)
tab={}
for r in csv.DictReader(open(INH+'/return_map_table_audit.csv')):
    a,rho=int(r['a']),int(r['rho']); tab[(a,rho)]=(int(r['a_next']),int(r['zprime_t0']),int(r['slope']))
def R(a,z):
    rho=(z-50000)%98; t=(z-50000)//98
    an,z0,sl=tab[(a,rho)]
    zp=z0+sl*t; steps=L0[(a,rho)]+4620*t
    return an,zp,steps
a,z,n=1,1269113,1039587
rows=[(0,a,z,n,None)]
for j in range(1,8):
    an,zp,st=R(a,z); n+=st; a,z=an,zp
    rows.append((j,a,z,n,st))
for r in rows: print(r)
json.dump(rows,open(OUTD+'/predicted_returns.json','w'))

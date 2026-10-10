#!/usr/bin/env python3
"""Exact-rational recheck of the 2x2 bound-admissibility test (float noise correction). usage: script pub2.txt"""
import sys, numpy as np
from fractions import Fraction
t=open(sys.argv[1]).read().split(); n=int(t[0]); c=2
K=[[0.0]*n for _ in range(n)]
for i in range(n):
    for j in range(i+1,n): K[i][j]=K[j][i]=float(t[c]); c+=1
KM=np.array(K); Kf=[[Fraction(x) for x in r] for r in K]
def bx(pre,d):
    l=sum(Kf[i][j]*pre[i]*pre[j] for i in range(d) for j in range(i+1,d))
    for j in range(d,n):
        l-=abs(sum(Kf[i][j]*pre[i] for i in range(d))); l-=sum(abs(Kf[j][h]) for h in range(j+1,n))
    return l
sus=[]
for d in range(n):
    for b in range(1<<d):
        pre=[(1 if (b>>i)&1 else -1) for i in range(d)]
        ids=np.arange(1<<(n-d),dtype=np.int64); T=((ids[:,None]>>np.arange(n-d))&1)*2-1
        S=np.hstack([np.tile(np.array(pre,float),(len(ids),1)),T.astype(float)]); e=0.5*np.einsum('ij,jk,ik->i',S,KM,S)
        if float(e.min())-float(bx(pre,d))<1e-12: sus.append((pre,d))
worst=None
for pre,d in sus:
    best=min(sum(Kf[i][j]*s[i]*s[j] for i in range(n) for j in range(i+1,n)) for s in (pre+[(1 if (b2>>i)&1 else -1) for i in range(n-d)] for b2 in range(1<<(n-d))))
    sl=best-bx(pre,d); worst=sl if worst is None or sl<worst else worst
print({"near_tight_prefixes":len(sus),"exact_rational_min_slack":float(worst),"admissible":worst>=0})

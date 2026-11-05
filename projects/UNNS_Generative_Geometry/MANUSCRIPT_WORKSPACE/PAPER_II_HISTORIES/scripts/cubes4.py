import sys,json,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from engine import *
hs=histories(72**4); hset=set(hs); maxc=0; classes_par={}
idx={h:i for i,h in enumerate(hs)}; par=list(range(len(hs)))
def f(x):
    while par[x]!=x: par[x]=par[par[x]];x=par[x]
    return x
for (s,w) in hs:
    legal=[]
    for i in range(len(w)-1):
        if w[i]!=w[i+1]:
            v=(s,w[:i]+(w[i+1],w[i])+w[i+2:])
            if v in hset: par[f(idx[(s,w)])]=f(idx[v]); legal.append(i)
    c=0;last=-5
    for i in legal:
        if i>last+1:c+=1;last=i
    maxc=max(maxc,c)
json.dump({'histories':len(hs),'classes':len({f(i) for i in range(len(hs))}),'maxcube':maxc},open('../results/r4.json','w'))

import sys,json,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from engine import *
R={}
def hist_classes(t,d,mode):
    hs=histories(t); hset=set(hs); idx={h:i for i,h in enumerate(hs)}; par=list(range(len(hs)))
    def f(x):
        while par[x]!=x: par[x]=par[par[x]];x=par[x]
        return x
    for (s,w) in hs:
        st=run(s,w)
        for i in range(len(w)-1):
            if w[i]!=w[i+1]:
                v=(s,w[:i]+(w[i+1],w[i])+w[i+2:])
                if v not in hset: continue
                st2=run(*v)
                a,b=st[i+1],st2[i+1]
                inA=(a%(d*d)==0); inB=(b%(d*d)==0)
                if d is not None and mode=='preserve' and inA!=inB: continue
                if mode=='after' and inA!=inB and any(x%(d*d)==0 for x in st[:i+1]): continue
                par[f(idx[(s,w)])]=f(idx[v])
    return len({f(i) for i in range(len(hs))})
tab={}
for r in (1,2,3):
    tab[r]={}
    for d in (2,3,4,8):
        tab[r][f'preserve_{d}']=hist_classes(72**r,d,'preserve')
    for d in (2,3):
        tab[r][f'after_{d}']=hist_classes(72**r,d,'after')
    tab[r]['d12']=hist_classes(72**r,12,'preserve') if r<=3 else None
    tab[r]['d36']=hist_classes(72**r,36,'preserve') if r<=3 else None
R['persistence']=tab
json.dump(R,open('../results/RESULTS_II_part5.json','w'),indent=1)
print(tab)

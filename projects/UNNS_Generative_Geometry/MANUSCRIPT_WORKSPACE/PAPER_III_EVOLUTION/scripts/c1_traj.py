"""trajectories: 8-step and 375-step; activation family instances"""
import sys, json, time; sys.path.insert(0,'.')
from eng3 import *
R={}
def traj(x,y,maxn):
    x=Fr(x); y=Fr(y); o=[x]; ev=[]; 
    prevD=Dset(x)
    for n in range(1,maxn+1):
        z=C(o[-1]); o.append(z)
        D=Dset(z)
        if D!=prevD:
            ev.append({'step':n,'D_before':prevD,'D_after':D,'new':[d for d in D if d not in prevD]}); prevD=D
        if z==y: return o,ev,n
    return o,ev,None
def famstate(ell,ps,q):
    P=1
    for p in ps: P*=p
    return Fr(P*P,ell),Fr((P*q)**2,ell),P
R['inst']=[]
for (ell,ps,q) in [(3,[5,11],17),(7,[23,37,79],11),(5,[7,17,37,47],3),(11,[37,59,103,191,257],3)]:
    x,y,P=famstate(ell,ps,q); k=len(ps)
    Dx=Dset(x); Dy=Dset(y)
    K=complex_of(Dy); f,r,b=betti(K,2); f2,r2,b2=betti(K,2147483647)
    R['inst'].append({'ell':ell,'ps':ps,'q':q,'P':P,'Dx':Dx,'Dy':Dy,'f':f,'betti2':b,'bettiP':b2,'k':k,'pred':k*(k-1)//2, 'nE':len(K['E'])})
    print(R['inst'][-1]['ell'],Dx,Dy,f,b)
# 8-step
o,ev,n=traj(Fr(3025,3),Fr(12100,3),20)
R['t8']={'n':n,'orbit':[str(t) for t in o],'dens':[t.denominator for t in o],'events':ev,
 'D':[Dset(t) for t in o],'betti':[bettiD(Dset(t)) for t in o],
 'moves':[sorted(edges(Dset(t))) for t in o]}
print(n,R['t8']['dens'])
# 375-step
t0=time.time()
x,y,P=famstate(7,[11,53,67],2)
o,ev,n=traj(x,y,500)
R['t375']={'n':n,'x':str(x),'y':str(y),'events':ev,'sec':time.time()-t0}
print(n,ev,time.time()-t0)
for e in ev:
    e['betti_before']=bettiD(e['D_before']); e['betti_after']=bettiD(e['D_after'])
    print(e['step'],e['betti_before'],e['betti_after'])
json.dump(R,open('../results/c1_traj.json','w'),default=str)

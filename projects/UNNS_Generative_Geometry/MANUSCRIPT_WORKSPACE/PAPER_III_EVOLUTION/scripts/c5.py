import sys, json, time; sys.path.insert(0,'.')
from eng3 import *
from grav import *
R={}
# --- R3-T1 two-prime family: x_r=25 r^2/(5r-1), y_r=25 r^2/8, r = 5 mod 8
fam=[]
for r in [13,29,37,53,61,101]:
    x=Fr(25*r*r,5*r-1); y=Fr(25*r*r,8)
    ps,bx,gx=region_graver(x); ps2,by,gy=region_graver(y)
    fam.append({'r':r,'Dx':Dset(x),'Dy':Dset(y),'Grx':gx,'Gry':gy,'primes':ps,'boxx':bx,'boxy':by})
R['R3T1_k2']=fam
print([ (f['r'],f['Dx'],f['Dy'],len(f['Grx']),len(f['Gry'])) for f in fam])
# --- family k: x=P^2/(P-1), y=P^2/ell
fk=[]
for (ell,ps_) in [(3,[5,11]),(7,[23,37,79]),(5,[7,17,37,47])]:
    P=1
    for p in ps_: P*=p
    x=Fr(P*P,P-1); y=Fr(P*P,ell)
    _,_,gx=region_graver(x)
    if len(ps_)<=4:
        _,_,gy=region_graver(y)
    fk.append({'ell':ell,'ps':ps_,'Dx':Dset(x),'Dy':Dset(y),'nGrx':len(gx),'nGry':len(gy),'pred_x':2,'pred_y':len(ps_)*(len(ps_)-1)+2})
R['R3T1_fk']=fk; print(fk)
# --- R3-T2 two primes: seven types
types={}
import itertools
cnt=0
for p in [2,3,5,7,11,13]:
    for r in [3,5,7,11,13,17,19,23]:
        if r<=p: continue
        for b in range(2,120):
            if gcd(p*r,b)!=1: continue
            x=Fr((p*r)**2,b)
            bits=[ (p-1)%b==0,(r-1)%b==0,(p*r-1)%b==0,(p-r)%b==0 ]
            ps,box,gr=region_graver(x)
            # predicted
            A,B,C,E=bits
            if A and B: assert C and E
            pred=set()
            if A: pred|={(1,0),(-1,0)}
            if B: pred|={(0,1),(0,-1)}
            if not(A or B):
                if C: pred|={(1,1),(-1,-1)}
                if E: pred|={(1,-1),(-1,1)}
            ok = set(gr)==pred; cnt+=1
            t=''.join(n for n,v in zip('ABCE',bits) if v) or 'none'
            types[t]=types.get(t,0)+1
            assert ok,(p,r,b,gr,pred)
R['R3T2']={'n':cnt,'types':types}; print('R3T2',cnt,types)
# --- integer collapse B2-T1: boxes
from itertools import product
bad=0; ncheck=0
for m in range(4,3000):
    if not Dset(m): continue
    D=Dset(m); K=complex_of(D); f,r,b=betti(K,2)
    qs=sorted(factor(sqpart(m)).values()); k=len(qs)
    nF=1
    for q_ in qs: nF*=(q_+1)
    ncells=1
    for q_ in qs: ncells*=(2*q_+1)
    ncells-=2**k
    while b and b[-1]==0 and len(b)>1: b=b[:-1]
    ok=(len(D)==nF-1 and sum(f)==ncells and b==[1])
    ncheck+=1
    if not ok: bad+=1
    if ncheck>=700: break
R['B2T1']={'checked':ncheck,'bad':bad}; print('B2T1',ncheck,bad)
json.dump(R,open('../results/c5.json','w'),default=str)

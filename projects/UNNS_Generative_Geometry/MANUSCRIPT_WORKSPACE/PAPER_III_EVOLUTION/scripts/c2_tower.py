import sys, json, time; sys.path.insert(0,'.')
from eng3 import *
def tD(S,m): return sorted(d for d in divisors(factor(S)) if d>=2 and d%m==1%m)
S11=lambda k: 2**2*3**(3+k)*5**4
S5=lambda k: 126*2**k
which=sys.argv[1]; K1=int(sys.argv[2])
Sf,m=(S11,11) if which=='11' else (S5,5)
rows=[]
for k in range(0,K1+1):
    t=time.time(); D=tD(Sf(k),m); K=complex_of(D); f,r,b=betti(K,2); 
    _,_,b2=betti(K,2147483647,check=False)
    assert b==b2
    rows.append({'k':k,'nV':len(D),'f':f,'b':b}); 
    json.dump(rows,open('../results/tower%s.json'%which,'w'))
    print(k,len(D),f,b,round(time.time()-t,2),flush=True)

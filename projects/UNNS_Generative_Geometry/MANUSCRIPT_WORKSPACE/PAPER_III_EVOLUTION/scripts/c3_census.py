import sys, json, time; sys.path.insert(0,'.')
from eng3 import *
from trans3 import analyse, etype
l=int(sys.argv[1]); Smax=int(sys.argv[2]); nsteps=24
def inclass(S,l):
    if gcd(S,l)!=1: return False
    D=[d for d in divisors(factor(S)) if d>=2 and d%l==1%l]
    if not D: return False
    L,G=LG(D); return L==S and G==l
rows=[]; orbits=0; t0=time.time()
for S in range(2,Smax):
    if not inclass(S,l): continue
    orbits+=1; cur=Fr(S*S,l); Ds=[]
    for n in range(nsteps+1):
        D=Dset(cur); Ds.append(tuple(D))
        if not D: break
        L,G=LG(D); cur=cur+Fr(L*L,G)
    for n in range(len(Ds)-1):
        if Ds[n]!=Ds[n+1]:
            t=analyse(Ds[n],Ds[n+1]); t.update({'l':l,'S':S,'n':n,'type':etype(t)}); t['chk']=all(t['chk'].values())
            t['nD']=len(Ds[n]); t['nD2']=len(Ds[n+1])
            rows.append(t)
    json.dump({'orbits':orbits,'rows':rows,'done_S':S},open('../results/census_l%d.json'%l,'w'))
print(l,orbits,len(rows),time.time()-t0)

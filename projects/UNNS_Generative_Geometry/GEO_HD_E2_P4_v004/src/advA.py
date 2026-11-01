import sys, json, time, random
sys.path.insert(0,'/mnt/user-data/outputs/GEO_HD_E2_P4_v002/src')
import _boot
lm=_boot.p4('lattice_model'); zv=_boot.p4('zero_vertex')
import exact_containment as ec
from itertools import product
from multiprocessing import Pool
NMAX=int(sys.argv[1]); QM=int(sys.argv[2]); TL=float(sys.argv[3]); out=sys.argv[4]
lats=[(n,B) for n in range(1,NMAX+1) for B in lm.hnf2(n)]
pairs=[(B,Bp) for n,B in lats for n2,Bp in lats if n2<n and n%n2==0 and all(lm.member2(Bp)(r) for r in B)]
random.seed(1); random.shuffle(pairs)
boxes=[q for q in product(range(1,QM+1),repeat=2)]
def work(a):
    B,Bp,t0=a
    if time.time()-t0>TL: return None
    inL,outL=lm.member2(B),lm.member2(Bp); res=[]
    for q in boxes:
        F,cs=lm.cells_of_member(inL,q)
        if not F: continue
        Smax=ec.geometric_maximal(cs,2)
        n,fl=zv.screen_cells(Smax,outL)
        rec=[list(q),n,len(fl)]
        if fl:
            F2,ct=lm.cells_of_member(outL,q)
            r=ec.decide_union(cs,ct,2,100000)
            rec.append(r['verdict'])
            if r['verdict']!='CONTAINED': rec.append(r['certificate']['witness'])
        res.append(rec)
    return [B,Bp,res]
if __name__=='__main__':
    t0=time.time()
    with Pool(2) as p: R=p.map(work,[(B,Bp,t0) for B,Bp in pairs],chunksize=8)
    R=[r for r in R if r]
    runs=[x for r in R for x in r[2]]
    fl=[(r[0],r[1],x) for r in R for x in r[2] if x[2]>0]
    bad=[f for f in fl if f[2][3]!='CONTAINED']
    json.dump({'n_pairs_total':len(pairs),'n_pairs_done':len(R),'n_runs':len(runs),'n_flagged_runs':len(fl),'n_flagged_failures':len(bad),'failures':bad,'flagged_examples':fl[:40],'zfree_failures':'none by P4-Z1'},open(out,'w'))
    print(len(pairs),len(R),len(runs),len(fl),len(bad),time.time()-t0)

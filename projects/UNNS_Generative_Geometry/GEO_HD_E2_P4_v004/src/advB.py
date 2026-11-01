import sys, json, time, random
sys.path.insert(0,'/mnt/user-data/outputs/GEO_HD_E2_P4_v003/src')
import _boot
lm=_boot.p4('lattice_model'); zv=_boot.p4('zero_vertex')
import exact_containment as ec
from itertools import product
TL=float(sys.argv[1]); seed=int(sys.argv[2]); out=sys.argv[3]; NT=int(sys.argv[4]); NS=int(sys.argv[5])
random.seed(seed)
lat={n:lm.hnf3(n) for n in range(1,NS+1)}
tg=[(n,B) for n in range(2,NT+1) for B in lat[n] if not lm.free_coordinates3(lm.member3(B))]
print('no-free targets',len(tg),flush=True)
boxes=[q for q in product((1,2,3),repeat=3) if sum(q)<=8]
t0=time.time(); stats=dict(runs=0,flagged=0,exact=0,contained=0,fail=0,exh=0); fails=[]; ex=[]
while time.time()-t0<TL:
    n2,Bp=random.choice(tg); fp=lm.member3(Bp)
    ks=[k for k in range(2,NS//n2+1)]
    if not ks: continue
    n=n2*random.choice(ks)
    cand=[B for B in lat[n] if all(fp(r) for r in B)]
    if not cand: continue
    B=random.choice(cand); q=random.choice(boxes)
    inL=lm.member3(B)
    F,cs=lm.cells_of_member(inL,q)
    if not F: continue
    S=ec.geometric_maximal(cs,3); nn,fl=zv.screen_cells(S,fp)
    stats['runs']+=1
    if not fl: continue
    stats['flagged']+=1
    F2,ct=lm.cells_of_member(fp,q)
    try:
        r=ec.decide_union(cs,ct,3,40000)
    except Exception as e:
        stats['exh']+=1; continue
    stats['exact']+=1
    if r['verdict']=='CONTAINED': stats['contained']+=1
    else:
        stats['fail']+=1; fails.append({'B':B,'Bp':Bp,'q':q,'witness':r['certificate']['witness']})
    if len(ex)<20: ex.append({'B':B,'Bp':Bp,'q':q,'verdict':r['verdict'],'nzv':len(fl)})
json.dump({'stats':stats,'fails':fails,'examples':ex,'targets_no_free':len(tg),'limits':{'NT':NT,'NS':NS,'seed':seed,'TL':TL}},open(out,'w'))
print(stats,len(fails))

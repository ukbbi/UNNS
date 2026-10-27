"""v010 Programme C: adversarial search for non-embedded boxes without a double 2-circuit decomposition (W2), hence candidates for r_min >= 4.
Random reduced supports of PG(k-1,2) (k = 6..9), made non-embedded by the partition criterion, then SHORTENED coordinate by coordinate (the box deletion of v006: restrict to words vanishing at the
coordinate) until minimal; every minimal box found is tested for W2 (a rank-3 witness exists whenever W2 holds and nullity >= 3: G10-L5).  usage: rank_attack6.py K N SEED OUT.json"""
import sys,random,time,json; sys.path.insert(0,'theory')
import binary5 as B5, binary6 as B6
k=int(sys.argv[1]); N=int(sys.argv[2]); rng=random.Random(int(sys.argv[3])); out=sys.argv[4]
pts=list(range(1,1<<k)); stats={}; bad=[]; t0=time.time(); starts=0; skipped=0
def dim(C):
    import math; return int(math.log2(len(C)))
for it in range(N):
    p=rng.randint(k+2,min(3*k,len(pts)))
    while True:
        sig=rng.sample(pts,p)
        if B5.rank_of(sig)==k: break
    C=B5.code_masks(sig)
    try:
        if not B6.non_embedded(C): continue
    except MemoryError: skipped+=1; continue
    starts+=1; n=len(sig); alive=list(range(n)); changed=True
    while changed:
        changed=False; order=alive[:]; rng.shuffle(order)
        for j in order:
            C2=[c for c in C if not (c>>j)&1]
            if B6.non_embedded(C2): C=C2; alive.remove(j); changed=True; break
    kk=dim(C); n_=len(alive)
    w2=B6.double_two_decomposition(C) is not None
    key='%d,%d'%(kk,n_); stats.setdefault(key,[0,0]); stats[key][0]+=1; stats[key][1]+=w2
    if not w2:
        bad.append({'nullity':kk,'alive':alive,'code':C}); print('NO W2',kk,n_,flush=True)
res={'k_start':k,'starts_non_embedded':starts,'minimal_found_by_(nullity,support)':stats,'no_W2':len(bad),'seconds':round(time.time()-t0,1)}
json.dump({'summary':res,'counterexample_candidates':bad},open(out,'w'))
print(res)

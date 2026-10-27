import sys,json,pickle,time; sys.path.insert(0,'theory')
import binary_min as BM, binary_01 as B, centre_collisions as CC, rank_reduction as RR
import binary5 as B5
r=pickle.load(open('output/data/v9_orbits_k5.pkl','rb'))
mine={tuple(x[1]):x[2] for x in json.load(open('output/data/v9_binary5.json'))}
sp=[R for m in sorted(r) for R in r[m] if B5.rank_of(list(R))==5]
bad=0; chk=0; t=time.time()
for R in sp:
    sig=list(R)
    if len(sig)>16: continue                      # v008 path enumerates 2^n words
    cols=BM.code_to_parity_columns(sig,len(sig)); chk+=1
    m = (not B.is_embedded(cols)) and B.minimal_nonembedded(cols)
    if m!=(R in mine): bad+=1; print('DISAGREE',R)
    if m:
        rk=min(RR.witness_rank(len(cols),a,b)[0] for c,a,b in CC.collisions(cols))
        if rk!=mine[R]: bad+=1; print('RANK DISAGREE',R,rk,mine[R])
print('checked',chk,'disagreements',bad,round(time.time()-t,1))
json.dump({'checked':chk,'disagreements':bad,'max_p':16},open('output/data/v9_binary5_crosscheck.json','w'))

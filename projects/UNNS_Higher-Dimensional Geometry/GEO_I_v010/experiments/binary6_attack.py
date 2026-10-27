"""v010 Programme C: minimal non-embedded boxes of nullity 6 via the full-support affine reduction (G10-A1) and the partition criterion (G10-E1).
Steps: orbits of subsets of AG(5,2) (381 non-empty, = Burnside 382 incl. empty); keep affinely spanning; minimality by shortening; ranks by the cell engine."""
import sys,time,pickle,json; sys.path.insert(0,'theory')
import binary5 as B5, binary6 as B6
m=int(sys.argv[1]); k=m+1
r=pickle.load(open('output/data/v10_affine_orbits_m%d.pkl'%m,'rb'))
rows=[]; nspan=0; nne=0; t0=time.time()
for size in sorted(r):
    for R in r[size]:
        if B5.rank_of(list(R))!=k: continue
        nspan+=1; C=B5.code_masks(list(R)); n=len(R)
        if not B6.non_embedded(C): continue
        nne+=1
        if not all(not B6.non_embedded(B5.delete(C,i)) for i in range(n)): continue
        wr=B6.rank3_witness(C,n); w2=wr is not None; mr=wr[0] if wr else B5.min_rank(C,n)  # explicit rank-3 witness + B-LOW (rank>=3) gives min_rank=3 without enumerating all collisions
        circ=B5.circuits_of_code(C); full=(1<<n)-1
        two=sum(1 for S,U in B5.disjoint_families(circ) if U==full and len(S)==2)
        rows.append({'p':n,'support':list(R),'min_rank':mr,'W2':w2,'two_circuit_partitions_of_1':two,'circuits':len(circ)})
        print(n,mr,w2,two,flush=True)
out={'k':k,'affine_orbits_nonempty':sum(len(v) for v in r.values()),'spanning':nspan,'non_embedded':nne,'minimal':rows,'seconds':round(time.time()-t0,1)}
json.dump(out,open('output/data/v10_binary%d.json'%k,'w'),indent=1)
print('k',k,'spanning',nspan,'non-embedded',nne,'minimal',len(rows),'ranks',sorted({x['min_rank'] for x in rows}),'all W2',all(x['W2'] for x in rows),out['seconds'])

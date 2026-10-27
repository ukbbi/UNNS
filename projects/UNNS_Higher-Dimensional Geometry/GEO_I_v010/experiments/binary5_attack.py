import sys,time,pickle,json; sys.path.insert(0,'theory')
import binary5 as B5
r=pickle.load(open('output/data/v9_orbits_k5.pkl','rb'))
sp=[R for m in sorted(r) for R in r[m] if B5.rank_of(list(R))==5]
res=[]; t=time.time()
for R in sp:
    sig=list(R); n=len(sig); C=B5.code_masks(sig)
    if B5.embedded(C): continue
    if not all(B5.embedded(B5.delete(C,i)) for i in range(n)): continue
    res.append((n,R,B5.min_rank(C,n)))
    print(n,R,res[-1][2],flush=True)
print('minimal nullity5 orbits',len(res),'ranks',sorted(set(x[2] for x in res)),round(time.time()-t,1))
json.dump([[n,list(R),mr] for n,R,mr in res],open('output/data/v9_binary5.json','w'))

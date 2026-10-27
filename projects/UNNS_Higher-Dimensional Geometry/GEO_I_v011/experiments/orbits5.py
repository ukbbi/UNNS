import sys,time,json,pickle; sys.path.insert(0,'theory')
import binary5 as B5
t=time.time(); r=B5.orbit_representatives(5,verbose=True)
pickle.dump(r,open('output/data/v9_orbits_k5.pkl','wb'))
sp=[R for m in r for R in r[m] if B5.rank_of(list(R))==5]
print('total',sum(len(v) for v in r.values()),'spanning',len(sp),round(time.time()-t,1))

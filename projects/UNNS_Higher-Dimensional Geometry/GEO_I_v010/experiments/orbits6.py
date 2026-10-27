"""v010: orbits of subsets of AG(5,2) under AGL(5,2) (= candidate reduced supports of minimal boxes of nullity 6, by G10-A1)."""
import sys,time,pickle; sys.path.insert(0,'theory')
import binary6 as B6
m=int(sys.argv[1]); t=time.time(); r=B6.affine_orbit_representatives(m,verbose=True)
pickle.dump(r,open('output/data/v10_affine_orbits_m%d.pkl'%m,'wb'))
print('total',sum(len(v) for v in r.values()),round(time.time()-t,1))

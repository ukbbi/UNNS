"""v010: independent cross-check of the criterion-based classification (binary6_attack.py) by the cell-based engine of v009 (binary5: cells, cosets, centre collisions).
usage: binary6_crosscheck.py M   (M = 5 for nullity 6)"""
import sys,pickle,json,time; sys.path.insert(0,'theory')
import binary5 as B5, binary6 as B6
m=int(sys.argv[1]); k=m+1; r=pickle.load(open('output/data/v10_affine_orbits_m%d.pkl'%m,'rb'))
mine={tuple(x['support']) for x in json.load(open('output/data/v10_binary%d.json'%k))['minimal']}
bad=[]; chk=0; t0=time.time()
for s in sorted(r):
    for R in r[s]:
        if B5.rank_of(list(R))!=k: continue
        C=B5.code_masks(list(R)); n=len(R); chk+=1
        ne_cells = not B5.embedded(C); ne_crit = B6.non_embedded(C)
        mn_cells = ne_cells and all(B5.embedded(B5.delete(C,i)) for i in range(n))
        if ne_cells!=ne_crit or mn_cells!=(R in mine): bad.append((R,ne_cells,ne_crit,mn_cells))
out={'k':k,'checked':chk,'disagreements':len(bad),'seconds':round(time.time()-t0,1)}
json.dump(out,open('output/data/v10_binary%d_crosscheck.json'%k,'w')); print(out,bad[:2])

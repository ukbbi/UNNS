"""Erratum E1 regression: corrected P5-S4(ii) criterion vs old, against the pinned exact engine, on ALL cells (not only hard cells). Needs the v005 folder next to this one."""
import sys, os, time, json
V5=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','GEO_HD_E2_P4_v005','src')
sys.path.insert(0,V5); sys.path.insert(0,V5+'/engine')
import mini, geo3, split_slab as ss, _boot, planar_audit as pa
lm=_boot.p4("lattice_model"); ec=lm.ec
def crit_corrected(base,gens,k,ctx):
    V=mini.corners(tuple(base),[tuple(g) for g in gens])
    if min(v[2] for v in V)>=k: return True
    return ss.criterion_contained(base,gens,k,ctx)
t0=time.time(); st=dict(cells=0,old_wrong=0,new_wrong=0,below_k_free=0); ex=[]
for L2 in (((1,0),(0,1)),((1,1),(0,2)),((1,0),(0,2))):
  for k in (1,2):
    Bp=ss.split_basis(L2,k)
    for Q in ((2,2,2*k),(2,2,3*k),(3,2,2*k)):
      pc={}
      F,csp=lm.cells_of_member(lambda v:geo3.member(Bp,v),Q)
      T=[ec.Target(b,g,3) for b,g in ec.geometric_maximal(csp,3)]
      for M in geo3.hnf3_enum(2):
        B=geo3.sublattice(Bp,M)
        Fs,cs=lm.cells_of_member(lambda v,B=B:geo3.member(B,v),Q)
        for (base,gens) in cs:
          if time.time()-t0>150: break
          base=tuple(int(x) for x in base); gs=[tuple(int(x) for x in g) for g in gens]
          import numpy as np
          QC=tuple(max(Q[i],0) for i in range(3))
          ctx=ss._planar_context(L2,(Q[0],Q[1]),pc)
          eng=ec.decide_cell(base,tuple(gs),T,3,node_limit=50000)["verdict"]=="CONTAINED"
          o=ss.criterion_contained(base,gs,k,ctx); n=crit_corrected(base,gs,k,ctx)
          st['cells']+=1; st['old_wrong']+=(o!=eng); st['new_wrong']+=(n!=eng)
          if o!=eng and len(ex)<5: ex.append(dict(L2=L2,k=k,Q=Q,base=base,gens=gs))
print(st,ex[:3],round(time.time()-t0))
json.dump(dict(stats=st,examples=ex),open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'ALLCELLS_RESULT.json'),'w'),default=str)
assert st['new_wrong']==0 and st['old_wrong']>0

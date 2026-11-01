"""Erratum E1: the audit counterexample (cell [0,2]^2 x {2})."""
import sys, os
V5=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','GEO_HD_E2_P4_v005','src')
sys.path.insert(0,V5); sys.path.insert(0,V5+'/engine')
from fractions import Fraction as Fr
import mini, geo3, split_slab as ss, _boot
lm=_boot.p4("lattice_model"); ec=lm.ec
L2=((1,0),(0,1)); k=2; Q=(2,2,2)
Bp=ss.split_basis(L2,k); B=geo3.sublattice(Bp,((2,0,0),(0,2,0),(0,0,1)))  # 2Z^2 + 2Z : index 4 in Z^2+2Z
print("Bp",Bp,"B",B)
mB=lambda v:geo3.member(B,v); mBp=lambda v:geo3.member(Bp,v)
base=(0,0,2); gens=[(2,0,0),(0,2,0)]
print("source cell valid:", mini.is_cell_of(mB,Q,base,gens))
F,cs=lm.cells_of_member(mBp,Q)
T=[ec.Target(b,g,3) for b,g in ec.geometric_maximal(cs,3)]
dec=ec.decide_cell(base,tuple(gens),T,3,node_limit=50000); print("engine:",dec["verdict"])
pc={}; ctx=ss._planar_context(L2,(2,2),pc)
print("closed criterion:",ss.criterion_contained(base,gens,k,ctx))
# corrected: open z<k  -> cell lies at z=k: nothing below -> vacuously contained
c3,_,_=mini.cells(mBp,Q)
print("mini union contains (1/2,1/2,2):",mini.in_union(c3,(Fr(1,2),Fr(1,2),Fr(2))))

assert dec['verdict']=='CONTAINED' and ss.criterion_contained(base,gens,k,ctx) is False
print('ERRATUM E1 REGRESSION: PASS (engine CONTAINED, v005 closed-truncation criterion says NOT contained)')

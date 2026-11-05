# cross-check: edges of K(D) from the divisor-interval rule == edges from lattice region-Graver
import sys; sys.path.insert(0,'.')
from eng3 import *
from grav import *
from fractions import Fraction as Fr
def lattice_edges(x):
    ps,box,gr=region_graver(x); _,F=fibre(x); Fs=set(F)
    grs=set(gr); E=set()
    for u in F:
        for g in gr:
            v=tuple(a+b for a,b in zip(u,g))
            if v in Fs and lexpos(g):
                E.add((u,v))
    return ps,E
def rule_edges(x):
    D=Dset(x); ps=active_primes(x.numerator)
    ex=lambda d:tuple(factor(d).get(p,0) for p in ps)
    return ps,{(ex(u),ex(v)) for (u,v) in edges(D)}
def norm(E):
    out=set()
    for u,v in E:
        out.add((u,v) if u<v else (v,u))
    return out
tot=0;bad=0
states=[]
for x0 in [Fr(3025,3),Fr(126**2,5),Fr(1890**2,29),Fr(36**2,5),Fr(176**2,7),Fr(2**2*3**3*5**4)**2/11 if False else Fr((2**2*3**3*5**4)**2,11)]:
    o=orbit(x0,30)
    states+=o
for t in states:
    if t.numerator>10**13: continue
    try:
        ps1,E1=lattice_edges(t); ps2,E2=rule_edges(t)
    except Exception as e:
        print('err',t,e); continue
    tot+=1
    if norm(E1)!=norm(E2): bad+=1; print('MISMATCH',t)
print('states',tot,'mismatches',bad)

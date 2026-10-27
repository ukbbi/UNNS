import sys; sys.path.insert(0,'theory'); sys.path.insert(0,'geometry'); sys.path.insert(0,'topology'); sys.path.insert(0,'frozen')
import coverage as C
from lattice_model import Lat
from fractions import Fraction as Fr
def area2(c): u,g,h=c; return abs(g[0]*h[1]-g[1]*h[0])
def cells(d,s): return [(u,g,h) for (u,(g,h)) in C.complex_data(Lat(d,d,d,s),(d,d))['cells'][2]]
def greedy(d,s):
    cs=sorted(cells(d,s),key=lambda c:-area2(c))
    F=sorted(C.complex_data(Lat(d,d,d,s),(d,d))['F']); Hv=C.hull(F)
    rem=[[(C.mpq(x),C.mpq(y)) for x,y in Hv]]; used=[]
    for c in cs:
        u,g,h=c; hp=C.cell_halfplanes(u,g,h); new=[]; hit=False
        for pc in rem:
            r=pc
            for (a,b,cc) in hp:
                o=C.clip(r,-a,-b,-cc)
                if len(o)>=3 and C.area2(o)>0: new.append(o)
                r=C.clip(r,a,b,cc)
                if len(r)<3 or C.area2(r)<=0: r=None;break
            if r is not None and len(r)>=3 and C.area2(r)>0: hit=True
        if hit: used.append(c)
        rem=new
    return used,rem
if __name__=='__main__':
    s=int(sys.argv[1])
    from math import gcd
    for d in range(int(sys.argv[2]),int(sys.argv[3])):
        if gcd(d,s)!=1: continue
        used,rem=greedy(d,s); print(d,s,'cells used',len(used),'distinct generator pairs',len({(c[1],c[2]) for c in used}),'leftover pieces',len(rem))

def detail(d, s):
    used, rem = greedy(d, s)
    from fractions import Fraction
    la = sum(Fraction(C.area2(p), 2) for p in rem)
    return used, la

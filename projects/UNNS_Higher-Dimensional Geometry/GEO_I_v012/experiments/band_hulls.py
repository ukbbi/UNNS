"""GEO-I v007 Programme A (observation, CHECKED not proved): for every NON-squareless small box Q=(d+r1,d+r2) (r1,r2 in [0,d-1], not both 0), conv(F) is the union of the hulls of
the vertical band (columns i with s*i mod d <= r2) and the horizontal band (rows j with t*j mod d <= r1).  Exact polygon subtraction.  usage: band_hulls.py DMAX OUT.json"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
for d_ in ('geometry', 'topology', 'frozen', 'theory'): sys.path.insert(0, os.path.join(HERE, '..', d_))
import modular_layers as ML, coverage as C
from math import gcd
from fractions import Fraction
def squareless(d,s,r): return not any(((j-s*i)%d==0) and (i or j) for i in range(r[0]+1) for j in range(r[1]+1))
def convex_pieces_minus(H,sub_polys):
    pieces=[[(C.mpq(x),C.mpq(y)) for x,y in H]]
    for P in sub_polys:
        if len(P)<3: continue
        if C.area2(P)<0: P=P[::-1]
        # halfplanes of convex P (ccw): interior left of each edge
        hp=[]
        n=len(P)
        for k in range(n):
            p,q=P[k],P[(k+1)%n]; a=-(q[1]-p[1]); b=(q[0]-p[0]); c=a*p[0]+b*p[1]; hp.append((-a,-b,-c))   # keep a x+b y <= c form: interior is  -a x - b y <= -c
        new=[]
        for pc in pieces:
            rem=pc
            for (a,b,c) in hp:
                outp=C.clip(rem,-a,-b,-c)
                if len(outp)>=3 and C.area2(outp)>0: new.append(outp)
                rem=C.clip(rem,a,b,c)
                if len(rem)<3 or C.area2(rem)<=0: rem=None;break
        pieces=new
    return pieces
def bands(d,s,Q):
    F=ML.fibre(d,s,Q)
    cols=sorted({p[0] for p in F if (p[1]-0)>=0})
    r2=Q[1]-d; r1=Q[0]-d
    Dx=[i for i in range(1,Q[0]+1) if (s*i)%d<=r2]
    t=next(t for t in range(1,d+1) if s*t%d==1%d)
    Dy=[j for j in range(1,Q[1]+1) if (t*j)%d<=r1]
    VBp=[p for p in F if Dx[0]<=p[0]<=Dx[-1]]; HBp=[p for p in F if Dy[0]<=p[1]<=Dy[-1]]
    return C.hull(sorted(set(VBp))),C.hull(sorted(set(HBp)))
if __name__=='__main__':
    dmax=int(sys.argv[1]); bad=[];tot=0
    for d in range(3,dmax+1):
        for s in range(1,d):
            if gcd(s,d)!=1: continue
            for r1 in range(d):
                for r2 in range(d):
                    if (r1,r2)==(0,0) or squareless(d,s,(r1,r2)): continue
                    Q=(d+r1,d+r2); F=ML.fibre(d,s,Q); H=C.hull(sorted(F))
                    V,Hh=bands(d,s,Q); tot+=1
                    L=convex_pieces_minus(H,[[(C.mpq(x),C.mpq(y)) for x,y in V],[(C.mpq(x),C.mpq(y)) for x,y in Hh]])
                    if L: bad.append((d,s,Q,len(L)))
    json.dump({'dmax':dmax,'boxes':tot,'failures':bad},open(sys.argv[2],'w')); print(tot,len(bad))

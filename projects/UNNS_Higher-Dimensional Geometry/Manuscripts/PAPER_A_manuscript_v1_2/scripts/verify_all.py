"""Finite checks accompanying Paper A (Section 21, Appendix I). Support only; never used as proof.
Geometric tests use shapely (floating point, tolerance 1e-9 on areas): they are numerical tests, not exact certificates.
Usage: python3 verify_all.py [smoke|full]"""
import sys, itertools
from math import gcd
from geo import *
from shapely.geometry import LineString
mode = sys.argv[1] if len(sys.argv)>1 else 'smoke'
DMAX = 8 if mode=='smoke' else 12
TOL=1e-9
def units(d): return [s for s in range(1,d) if gcd(s,d)==1]
res={}
# T1: cap cover by explicit family + old cells + fillers (nonspecial, d>=5, small boxes)
n=bad=0
for d in range(5,DMAX+1):
    for s in units(d):
        if s in (1,d-1): continue
        for u in range(d):
            for v in range(d):
                if (u,v)==(0,0): continue
                n+=1
                if check_cover(d,s,(d+u,d+v))>TOL: bad+=1
res['cap_cover_boxes']=(n,bad)
# T2: Pareto inequality (Lemma arith), nonspecial
n=bad=0
D2 = 40 if mode=='smoke' else 120
for d in range(5,D2+1):
    for s in units(d):
        if s in (1,d-1): continue
        t=pow(s,-1,d); a=d-s; c=d-t
        for x in range(1,d):
            r=(s*x)%d
            # (x,y) Pareto-minimal: no (x',y') in Gamma, 0<x'<=x, 0<y'<=y other than itself, y=r
            y=r
            if y==0: continue
            if any(0<(s*x2)%d<=y for x2 in range(1,x)): continue
            n+=1
            if max(y+a*x, x+c*y) < x*y: bad+=1
res['pareto_points']=(n,bad)
# T3: boundary steps are Graver (Lemma reflection), several boxes
n=bad=0
for d in range(3,DMAX+1):
    for s in units(d):
        for Q in [(d,d),(d+1,d+2),(2*d,d+1),(2*d+1,3*d+1),(3*d,3*d)]:
            F=Fpts(d,s,Q); G=set(graver(d,s,Q[0],Q[1])); G|={(-x,-y) for x,y in G}
            pts=ccw_boundary_points(d,s,Q,F)
            for p,q in zip(pts,pts[1:]+pts[:1]):
                n+=1
                if (q[0]-p[0],q[1]-p[1]) not in G: bad+=1
res['boundary_steps']=(n,bad)
# T4: universal theorem: U_Q = conv F_Q for all Q with Q>=(d,d), Q!=(d,d), small d
n=bad=0
DU = 6 if mode=='smoke' else 8
for d in range(2,DU+1):
    for s in units(d):
        for q1 in range(d,2*d+2):
            for q2 in range(d,2*d+2):
                if (q1,q2)==(d,d): continue
                F,G,pars,segs=cells_all(d,s,(q1,q2))
                H=hull_poly(F)
                polys=[Polygon(p) for p in pars if Polygon(p).is_valid]
                U=unary_union(polys+[LineString(sg) for sg in segs]) if False else unary_union(polys)
                n+=1
                miss=H.difference(U.buffer(1e-9))
                # segments may supply lower-dimensional parts; only 2-dim defect is tested here
                if miss.area>TOL: bad+=1
res['universal_boxes']=(n,bad)
for k,v in res.items(): print(f"{k}: {v[0]} tested, {v[1]} failures")

"""Exact-coordinate geometry library for Paper A figures (integer arithmetic; shapely only for area checks)."""
import itertools
from math import gcd
from shapely.geometry import Polygon, MultiPoint, Point
from shapely.ops import unary_union

def inv(s,d): return pow(s,-1,d)

def Fpts(d,s,Q):
    return {(i,j) for i in range(Q[0]+1) for j in range(Q[1]+1) if (j-s*i)%d==0 and (i,j)!=(0,0)}

def graver(d,s,R1,R2):
    V=[(i,j) for i in range(-R1,R1+1) for j in range(-R2,R2+1) if (i,j)!=(0,0) and (j-s*i)%d==0]
    G=[]
    for g in V:
        if not any(h!=g and h[0]*g[0]>=0 and h[1]*g[1]>=0 and abs(h[0])<=abs(g[0]) and abs(h[1])<=abs(g[1]) for h in V):
            G.append(g)
    return G

def cells_all(d,s,Q):
    """All admissible parallelograms (as corner 4-tuples w,w+g,w+g+h,w+h) and Graver segments."""
    F=Fpts(d,s,Q); G=graver(d,s,Q[0],Q[1])
    pars=[]; 
    for w in F:
        for g,h in itertools.combinations(G,2):
            if g[0]*h[1]-g[1]*h[0]==0: continue
            a=(w[0]+g[0],w[1]+g[1]); b=(w[0]+h[0],w[1]+h[1]); c=(a[0]+h[0],a[1]+h[1])
            if a in F and b in F and c in F: pars.append((w,a,c,b))
    segs=[]
    Gs=set(G)
    for p in F:
        for q in F:
            if p<q and (q[0]-p[0],q[1]-p[1]) in Gs|{(-x,-y) for x,y in Gs}: segs.append((p,q))
    return F,G,pars,segs

def hull_poly(F): return MultiPoint(sorted(F)).convex_hull

def ccw_boundary_points(d,s,Q,F=None):
    """All lattice points of F on the boundary of H_Q, ccw, starting at B=(d,0)."""
    F=F or Fpts(d,s,Q); H=hull_poly(F)
    ring=list(H.exterior.coords)[:-1]
    # orient ccw
    area=sum(ring[i][0]*ring[(i+1)%len(ring)][1]-ring[(i+1)%len(ring)][0]*ring[i][1] for i in range(len(ring)))
    if area<0: ring=ring[::-1]
    ext=H.exterior
    pts=[p for p in F if ext.distance(Point(p))<1e-9]
    # parameter along ccw ring
    from shapely.geometry import LineString
    ringls=LineString(ring+[ring[0]])
    pts.sort(key=lambda p: ringls.project(Point(p)))
    k=pts.index((d,0)); pts=pts[k:]+pts[:k]
    return pts

def omega(d,s,Q):
    pts=ccw_boundary_points(d,s,Q)
    k=pts.index((0,d)); return pts[:k+1]

def cls(p,d):
    x,y=p
    if x>=d and y<d: return 'R'
    if x>=d and y>=d: return 'C'
    if x<d and y>=d: return 'T'
    return 'N'

def cross(a,b): return a[0]*b[1]-a[1]*b[0]

def cap_family(d,s,Q):
    """The explicit cap cells of the paper (Section 15): returns dict family-> list of corner 4-tuples."""
    t=inv(s,d); a=d-s; c=d-t; u=Q[0]-d; v=Q[1]-d
    Om=omega(d,s,Q)
    fam={'L':[],'D':[],'bottom':[],'left':[]}
    for w,w2 in zip(Om,Om[1:]):
        e=(w2[0]-w[0],w2[1]-w[1])
        if w[0]>=d and w2[0]>=d and w!=(d,0):
            fam['L'].append((w,w2,(w2[0]-d,w2[1]),(w[0]-d,w[1])))
        if w[1]>=d and w2[1]>=d and w2!=(0,d):
            fam['D'].append((w,w2,(w2[0],w2[1]-d),(w[0],w[1]-d)))
    def bottom(d,s,u):
        t=inv(s,d); a=d-s; c=d-t
        r=[(s*i)%d for i in range(1,u+1)]
        y=min(r); x=r.index(y)+1; M=(x,y)
        g=(1,-a) if cross((1,-a),M)>=x*y else (c,-1)
        assert cross(g,M)>=x*y
        B=(d,0); w=(B[0]-g[0],B[1]-g[1])
        return M,g,(w,(B[0],B[1]),(B[0]+M[0],B[1]+M[1]),(w[0]+M[0],w[1]+M[1]))
    if u>=1:
        M,g,cell=bottom(d,s,u); fam['bottom'].append(cell); fam['_M']=M; fam['_g']=g
    if v>=1:
        M2,g2,cell=bottom(d,t,v)
        fam['left'].append(tuple((p[1],p[0]) for p in cell)); fam['_M2']=(M2[1],M2[0]); fam['_g2']=(g2[1],g2[0])
    return fam

def union(polys): return unary_union([Polygon(p) for p in polys])

def check_cover(d,s,Q):
    F,G,pars,segs=cells_all(d,s,(d,d))
    H=hull_poly(Fpts(d,s,Q))
    fam=cap_family(d,s,Q)
    cap=[p for k in ('L','D','bottom','left') for p in fam[k]]
    U=unary_union([Polygon(p) for p in pars+cap])
    return H.area-U.intersection(H).area

def fill_cells(d,s,Q):
    """Hole-filling cells R1,R2 (Prop. hole filling) and their transposes; returns corner 4-tuples."""
    t=inv(s,d); out=[]
    def mk(t_):
        A=(0,d); C=(d,d)
        R1=(A,(d-t_,d-1),(t_,d+1),C)             # A, A+(d-t,-1), A+(d-t,-1)+(t,1)?  order for polygon: A,P,(t,d+1)?? fixed below
        # R1 = P(A;(d-t,-1),(t,1)) corners A, A+g, A+g+h, A+h
        g=(d-t_,-1); h=(t_,1)
        R1=(A,(A[0]+g[0],A[1]+g[1]),(A[0]+g[0]+h[0],A[1]+g[1]+h[1]),(A[0]+h[0],A[1]+h[1]))
        w=(t_,1); g2=(0,d); h2=(d-t_,-1)
        R2=(w,(w[0]+g2[0],w[1]+g2[1]),(w[0]+g2[0]+h2[0],w[1]+g2[1]+h2[1]),(w[0]+h2[0],w[1]+h2[1]))
        return [R1,R2]
    if Q[1]>=d+1: out+=mk(t)
    if Q[0]>=d+1: out+=[tuple((p[1],p[0]) for p in c) for c in mk(inv(t,d))]
    return out

def check_cover(d,s,Q,return_union=False):
    F,G,pars,segs=cells_all(d,s,(d,d))
    H=hull_poly(Fpts(d,s,Q))
    fam=cap_family(d,s,Q)
    cap=[p for k in ('L','D','bottom','left') for p in fam[k]]
    allc=pars+cap+fill_cells(d,s,Q)
    U=unary_union([Polygon(p) for p in allc])
    r=H.area-U.intersection(H).area
    return (r,U,H,fam) if return_union else r

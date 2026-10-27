"""GEO-I v011, Programme A.  Exact cap toolkit (Fractions): Graver cells of Gamma_{d,s}, hull H_Q, cap C_Q = H_Q minus H_0.

Contents
  * generic cell engine of this release (independent of theory/coverage.py and theory/modular_sail.py): fibreQ, graver_list, cells_of, hull, clip, subtract, uncovered;
  * G11-L3 (one-sided cap, Q=(d+u,d), 1<=u<d): proof_cells_onesided -- the explicit cell family (horizontal sweep cells along the right boundary chain of
    W_u = conv({0,(0,d)} u {(i, s i mod d): 1<=i<=u}) from the record minimum M to A=(0,d), plus ONE bottom cell P(B-g; g, M) with g in {g1=(1,s-d), u*=(d-t,-1)});
    verify() checks legitimacy of every cell (corners in F_Q, Graver by scan) and the exact cover of the cap polygon B+W_u;
  * G11-A (arithmetic lemma behind the bottom cell): lemma_ok(d,s,u);
  * G11-L4 (mixed corner): corner_pentagon -- the pentagon (E,(d,E_y),C,(E'_x,d),E') cut off by the bridging hull edge E E' of H_Q for Q=(d+u,d+v), u,v>=1;
  * full_cover(d,s,Q): H_Q is covered by the union of all cells (CHECKED statement G10-T2 re-run with this independent engine).
Status of every statement: see CAP.md / THEOREM_REGISTRY.tsv.  Nothing here is imported by the frozen modules."""

from fractions import Fraction as Fr
from math import gcd
import itertools
def inv(s,d): return pow(s,-1,d)
def in_gamma(d,s,p): return (p[1]-s*p[0])%d==0
def fibreQ(d,s,Q):
    return {(x,y) for x in range(Q[0]+1) for y in range(Q[1]+1) if (x or y) and (y-s*x)%d==0}
def graver_list(d,s):
    """all Graver vectors with lexpos, components in [-d,d]"""
    cand=[(a,b) for a in range(0,d+1) for b in range(-d,d+1) if (a or b>0) and (b-s*a)%d==0 and (a,b)>(0,0)]
    G=[]
    for g in cand:
        ok=True
        for h in cand:
            if h!=g and h[0]*g[0]>=0 and h[1]*g[1]>=0 and abs(h[0])<=abs(g[0]) and abs(h[1])<=abs(g[1]): ok=False;break
        if ok: G.append(g)
    return G
def cells_of(d,s,Q,G=None,F=None):
    F=F or fibreQ(d,s,Q); G=G or graver_list(d,s)
    out=[]
    for u in F:
        for i,g in enumerate(G):
            ug=(u[0]+g[0],u[1]+g[1])
            if ug not in F: continue
            for h in G[i+1:]:
                if g[0]*h[1]-g[1]*h[0]==0: continue
                uh=(u[0]+h[0],u[1]+h[1]); ugh=(ug[0]+h[0],ug[1]+h[1])
                if uh in F and ugh in F: out.append((u,g,h))
    return out
def corners(c):
    u,g,h=c; return [u,(u[0]+g[0],u[1]+g[1]),(u[0]+g[0]+h[0],u[1]+g[1]+h[1]),(u[0]+h[0],u[1]+h[1])]
def cross(o,a,b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
def hull(P):
    P=sorted(set(P))
    lo=[]
    for p in P:
        while len(lo)>=2 and cross(lo[-2],lo[-1],p)<=0: lo.pop()
        lo.append(p)
    up=[]
    for p in reversed(P):
        while len(up)>=2 and cross(up[-2],up[-1],p)<=0: up.pop()
        up.append(p)
    return lo[:-1]+up[:-1]
def area2(P): return sum(P[i][0]*P[(i+1)%len(P)][1]-P[(i+1)%len(P)][0]*P[i][1] for i in range(len(P)))
def clip(P,a,b,c):
    out=[];n=len(P)
    for i in range(n):
        p,q=P[i],P[(i+1)%n]; fp=a*p[0]+b*p[1]+c; fq=a*q[0]+b*q[1]+c
        if fp>=0: out.append(p)
        if (fp>0 and fq<0) or (fp<0 and fq>0):
            t=Fr(fp)/(fp-fq); out.append((p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1])))
    return out
def halfplanes(poly):
    P=[(Fr(x),Fr(y)) for x,y in poly]
    if area2(P)<0: P=P[::-1]
    out=[]
    for i in range(len(P)):
        p,q=P[i],P[(i+1)%len(P)]; a=-(q[1]-p[1]); b=q[0]-p[0]; out.append((a,b,-(a*p[0]+b*p[1])))
    return out
def subtract(pieces,region):
    new=[]
    for pc in pieces:
        r=pc
        for (a,b,c) in region:
            o=clip(r,-a,-b,-c)
            if len(o)>=3 and area2(o)>0: new.append(o)
            r=clip(r,a,b,c)
            if len(r)<3 or area2(r)<=0: r=None;break
    return new
def uncovered(poly,cells):
    pieces=[[(Fr(x),Fr(y)) for x,y in poly]]
    for c in cells:
        pieces=subtract(pieces,halfplanes(corners(c)))
        if not pieces: return []
    return pieces
def pip(poly,pt):
    """closed point in convex polygon (ccw) test, exact"""
    P=[(Fr(x),Fr(y)) for x,y in poly]
    if area2(P)<0: P=P[::-1]
    return all(cross(P[i],P[(i+1)%len(P)],pt)>=0 for i in range(len(P)))



def graver_scan(d,s,g):
    """g in Gamma is Graver iff no other nonzero lattice vector lies in the closed box between 0 and g (same sign pattern)"""
    if g==(0,0) or (g[1]-s*g[0])%d: return False
    sa=1 if g[0]>=0 else -1; sb=1 if g[1]>=0 else -1
    return not any((a,b) not in ((0,0),(abs(g[0]),abs(g[1]))) and (sb*b-s*sa*a)%d==0 for a in range(abs(g[0])+1) for b in range(abs(g[1])+1))

def norm_cell(c4):
    """corners (a parallelogram given by 4 corner points) -> (u,g,h)"""
    S=sorted(set(c4)); u=S[0]; rest=S[1:]
    for o in rest:
        b,c=[x for x in rest if x!=o]
        if (u[0]+o[0],u[1]+o[1])==(b[0]+c[0],b[1]+c[1]):
            return (u,(b[0]-u[0],b[1]-u[1]),(c[0]-u[0],c[1]-u[1]))
    raise ValueError

def proof_cells_onesided(d,s,u):
    t=inv(s,d); a=[None]+[(s*i)%d for i in range(1,d)]
    # M = record-min point over i<=u
    xm,ym=1,a[1]
    for i in range(1,u+1):
        if a[i]<ym: xm,ym=i,a[i]
    M=(xm,ym)
    Y=[(0,0),(0,d)]+[(i,a[i]) for i in range(1,u+1)]
    H=hull(Y)           # ccw
    Gam=[(x,y) for x in range(u+1) for y in range(d+1) if (y-s*x)%d==0]
    n=len(H); i0=H.index((0,0)); bpts=[]
    for k in range(n):
        p,q=H[(i0+k)%n],H[(i0+k+1)%n]
        on=sorted((x for x in Gam if cross(p,q,x)==0 and min(p[0],q[0])<=x[0]<=max(p[0],q[0]) and min(p[1],q[1])<=x[1]<=max(p[1],q[1])),key=lambda x:(x[0]-p[0])**2+(x[1]-p[1])**2)
        bpts+=[x for x in on if x!=p] if k>0 else on
    # bpts: boundary Gamma points ccw starting at origin
    assert bpts[0]==(0,0) and bpts[1]==M,'first boundary point after origin is not M'
    chain=[]
    for x in bpts[1:]:
        chain.append(x)
        if x==(0,d): break
    cells=[]
    for w,w2 in zip(chain,chain[1:]):
        cells.append(norm_cell([w,w2,(w[0]+d,w[1]),(w2[0]+d,w2[1])]))
    # bottom triangle: choose g1 or u*
    B=(d,0); x_,y_=M
    g1=(1,s-d); us=(d-t,-1)
    def cr(g): return g[0]*y_-g[1]*x_
    if cr(g1)>=x_*y_: g=g1
    elif cr(us)>=x_*y_: g=us
    else: raise AssertionError('lemma fails')
    p=(B[0]-g[0],B[1]-g[1])
    cells.append(norm_cell([p,B,(p[0]+x_,p[1]+y_),(B[0]+x_,B[1]+y_)]))
    return cells,M,g

def verify(d,s,u):
    Q=(d+u,d); F=fibreQ(d,s,Q)
    cells,M,g=proof_cells_onesided(d,s,u)
    for (uu,gg,hh) in cells:
        cs=corners((uu,gg,hh))
        assert all(c in F for c in cs),('corner outside F',uu,gg,hh)
        assert graver_scan(d,s,gg) and graver_scan(d,s,hh),('not graver',gg,hh)
        assert gg>(0,0) and hh>(0,0) and gg[0]*hh[1]-gg[1]*hh[0]!=0
    # cap polygon = conv(F_Q) minus H0 ; test coverage of cap = B + W_u
    Wp=hull([(0,0),(0,d)]+[(i,(s*i)%d) for i in range(1,u+1)])
    cap=[(x+d,y) for x,y in Wp]
    unc=uncovered(cap,cells)
    # also confirm hull(F_Q) == H0 u cap by area: area(HQ)=area(H0)+area(cap)
    HQ=hull(list(F)); H0=hull(list(fibreQ(d,s,(d,d))))
    assert area2(HQ)==area2(H0)+area2(cap),'hull decomposition fails'
    return len(unc)==0,len(cells)



def bridging(d,s,u,v):
    Q=(d+u,d+v); F=fibreQ(d,s,Q); H=hull(list(F)); n=len(H)
    # ccw order; find edge crossing x=d from x>=d to x<d with... : last vertex with x>=d then next with x<d (going ccw from B)
    iB=H.index((d,0)); 
    E=None
    for k in range(n):
        p=H[(iB+k)%n]; q=H[(iB+k+1)%n]
        if p[0]>=d and q[0]<d and k>0:
            E,Ep=p,q;break
    return F,H,E,Ep
def pent(d,s,u,v):
    F,H,E,Ep=bridging(d,s,u,v)
    C=(d,d)
    return [E,(d,E[1]),C,(Ep[0],d),Ep],E,Ep,F
def analyse(d,s,u,v,verbose=True):
    P,E,Ep,F=pent(d,s,u,v); C=(d,d)
    Q=(d+u,d+v); G=graver_list(d,s)
    # polygon may be degenerate if E has y>=d or Ep has x>=d etc.
    if E[1]>=d or Ep[0]>=d: return None
    cells=cells_of(d,s,Q,G,F)
    pp=[(Fr(x),Fr(y)) for x,y in P]
    # P is a simple pentagon but non-convex (reflex at C): split into two convex pieces by diagonal C->E'?? use triangulation fan from C? do: pieces = tri(E,(d,yE),C), tri(E,C,E'), tri(C,(xE',d),E')
    pieces=[[E,(d,E[1]),C],[E,C,Ep],[C,(Ep[0],d),Ep]]
    pieces=[[(Fr(x),Fr(y)) for x,y in pc] for pc in pieces if area2([(Fr(x),Fr(y)) for x,y in pc])!=0]
    pieces=[pc if area2(pc)>0 else pc[::-1] for pc in pieces]
    rel=[]
    for c in cells:
        pc=corners(c)
        ar=0
        for tri in pieces:
            r=tri
            for (aa,bb,cc) in halfplanes(pc):
                r=clip(r,aa,bb,cc)
                if len(r)<3 or area2(r)<=0: r=None;break
            if r: ar+=area2(r)
        if ar>0: rel.append((c,ar))
    rel.sort(key=lambda x:-x[1])
    cur=pieces; chosen=[]
    for c,ar in rel:
        nxt=[]
        for pc in cur: nxt+=subtract([pc],halfplanes(corners(c)))
        if sum(area2(p) for p in nxt)<sum(area2(p) for p in cur):
            chosen.append(c); cur=nxt
        if not cur: break
    return dict(E=E,Ep=Ep,covered=not cur,chosen=chosen)


# ---------------------------------------------------------------------------------------------------------------- v011 API
corner_pentagon = analyse


def lemma_ok(d, s, u):
    """G11-A: for M=(x,y) the record minimum of a_i = s i mod d over 1<=i<=u,  max( cr(g1,M), cr(u*,M) ) >= x*y,
    cr(g1,M) = y + x(d-s), cr(u*,M) = (d-t) y + x.  (This is exactly the condition under which the bottom cell contains the bottom triangle of the cap.)"""
    t = inv(s, d); xm, ym = 1, s % d
    for i in range(1, u + 1):
        a = (s * i) % d
        if a < ym: xm, ym = i, a
    return max(ym + xm * (d - s), (d - t) * ym + xm) >= xm * ym


def lemma_scan(dmax, dmin=5):
    """all unit pairs 2<=s<=d-2 and 1<=u<d; returns (triples, failures)"""
    n = 0; bad = []
    for d in range(dmin, dmax + 1):
        for s in range(2, d - 1):
            if gcd(s, d) != 1: continue
            t = inv(s, d); xm, ym = 1, s
            for u in range(1, d):
                a = (s * u) % d
                if a < ym: xm, ym = u, a
                n += 1
                if max(ym + xm * (d - s), (d - t) * ym + xm) < xm * ym: bad.append((d, s, u))
    return n, bad


def full_cover(d, s, Q):
    """True iff conv(F_Q) minus the union of all legitimate cells is empty (exact).  Q=(d+u,d+v)."""
    F = fibreQ(d, s, Q); H = hull(list(F))
    return len(uncovered(H, cells_of(d, s, Q, graver_list(d, s), F))) == 0


def one_sided_sweep(dmin, dmax):
    n = 0; bad = []
    for d in range(dmin, dmax + 1):
        for s in range(2, d - 1):
            if gcd(s, d) != 1: continue
            for u in range(1, d):
                ok, _ = verify(d, s, u); n += 1
                if not ok: bad.append((d, s, u))
    return n, bad


def pentagon_sweep(dmin, dmax):
    n = 0; skipped = 0; bad = []
    for d in range(dmin, dmax + 1):
        for s in range(2, d - 1):
            if gcd(s, d) != 1: continue
            for u in range(1, d):
                for v in range(1, d):
                    r = analyse(d, s, u, v)
                    if r is None: skipped += 1; continue
                    n += 1
                    if not r['covered']: bad.append((d, s, u, v))
    return n, skipped, bad

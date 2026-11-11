"""State-function audit.  For every route step, test (in this order) whether the label N is
 const | poly(deg<=3) in S_before | poly in S_after | poly in x0 (route start) | algebraic relation P(N,V)=0, deg_N,deg_V<=3 for V in S_before,S_after,x0.
'found' = an expression exists in this vocabulary and was verified at ALL sample points (>=26).  'not-found' does NOT mean necessary."""
from fractions import Fraction
import itertools
def newton_ok(xs,ys,deg):
    """True iff the unique interpolant has degree <= deg (all divided differences of order>deg vanish)."""
    n=len(xs); d=[Fraction(y) for y in ys]
    for order in range(1,n):
        d=[(d[i+1]-d[i])/(xs[i+order]-xs[i]) for i in range(n-order)]
        if order>deg and any(v!=0 for v in d): return False
    return True
def nullspace_dim(rows):
    """exact rank over Q by Fraction elimination; returns number of columns - rank"""
    M=[[Fraction(v) for v in r] for r in rows]; nc=len(M[0]); rank=0; col=0
    for col in range(nc):
        piv=None
        for r in range(rank,len(M)):
            if M[r][col]!=0: piv=r;break
        if piv is None: continue
        M[rank],M[piv]=M[piv],M[rank]; pv=M[rank][col]
        M[rank]=[v/pv for v in M[rank]]
        for r in range(len(M)):
            if r!=rank and M[r][col]!=0:
                f=M[r][col]; M[r]=[a-f*b for a,b in zip(M[r],M[rank])]
        rank+=1
    return nc-rank
def alg_relation(Ns,Vs,maxdeg=3):
    for dn,dv in [(1,1),(1,2),(2,1),(2,2),(1,3),(3,1),(2,3),(3,2),(3,3),(1,4),(2,4),(1,5),(2,5),(3,4)]:
        cols=[(i,j) for i in range(dn+1) for j in range(dv+1)]
        if len(Vs)<len(cols)+4: continue
        rows=[[N**i*V**j for i,j in cols] for N,V in zip(Ns,Vs)]
        if nullspace_dim(rows)>0: return (dn,dv)
    return None
def classify(Ns,Sb,Sa,X0):
    if len(set(Ns))==1: return ("const",None)
    for nm,V in (("S_before",Sb),("S_after",Sa),("x0",X0)):
        for d in (1,2,3):
            if newton_ok(V,Ns,d) if len(set(V))==len(V) else False: return ("poly:"+nm,d)
    for nm,V in (("S_before",Sb),("S_after",Sa),("x0",X0)):
        r=alg_relation(Ns,V)
        if r: return ("alg:"+nm,r)
    return ("not-found",None)
def audit_family(samples):
    """samples: list over sample points of dict(steps=[(sign,N,Sb,Sa)...], x0=...). returns per-step classification list."""
    m=len(samples[0]['steps']); out=[]
    for i in range(m):
        Ns=[s['steps'][i][1] for s in samples]; Sb=[s['steps'][i][2] for s in samples]
        Sa=[s['steps'][i][3] for s in samples]; X0=[s['x0'] for s in samples]
        out.append(classify(Ns,Sb,Sa,X0))
    return out

def in_field(Ns,Xs,Ls,maxd=7):
    """is N in Q[x,L]?  N = sum_{i<=d} (al_i x^i + be_i x^i L); returns minimal d or None"""
    for d in range(0,maxd+1):
        cols=[(i,e) for i in range(d+1) for e in (0,1)]
        if len(Ns)<len(cols)+4: return None
        rows=[[x**i*(L**e) for i,e in cols]+[N] for x,L,N in zip(Xs,Ls,Ns)]
        # N in column span <=> rank([A|N])==rank(A)
        A=[r[:-1] for r in rows]
        if nullspace_dim(rows)==nullspace_dim(A)+1: return d
    return None

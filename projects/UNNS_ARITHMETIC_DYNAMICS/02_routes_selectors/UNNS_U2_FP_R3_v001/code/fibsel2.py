"""Fibonacci successor selector v2 under R3' (fixed algebraic-monotone recovery).
Reads only: current integer x and finite control state (class r, step i | small table (k,j) ).
Operations: + - * exact division by constants, comparison, isqrt, residue mod 24, exact radical sign tests (radical.py)."""
import json, os
from fractions import Fraction
from math import isqrt
import sympy as sp
from fibparam import F
from radical import ACC, sign_radical, horner, sgn
import fibcert2
HERE=os.path.dirname(os.path.abspath(__file__)); DATA=HERE+"/../data"
bsym=fibcert2.b
def _pint(expr):
    """polynomial in b with rational coeffs -> (integer coeff list high->low, common denominator)"""
    p=sp.Poly(sp.sympify(expr),bsym); cs=[sp.Rational(c) for c in p.all_coeffs()]
    d=1
    for c in cs: d=d*int(c.q)//__import__('math').gcd(d,int(c.q))
    return [int(c*d) for c in cs],d
class Class:
    def __init__(s,cert):
        s.eps=cert['eps']; s.sign=[sg for sg,_ in cert['searchnames']]
        s.S=[(_pint(a),_pint(b_)) for a,b_ in cert['states_ring']]
        s.N=[(_pint(a),_pint(b_)) for a,b_ in cert['labels_ring']]
    def cmp_state(s,i,t,x):
        """sign(G_i(t)-x) exactly, G_i=p0+p1*alpha_eps; t integer"""
        (c0,d0),(c1,d1)=s.S[i]
        P0=horner(c0,t); P1=horner(c1,t)
        P=2*d1*P0-d0*t*P1-2*d0*d1*x          # 2*d0*d1*(p0 - t p1/2 - x)
        Q=d0*P1                                # 2*d0*d1*(p1/2) = d0*p1_int
        D=5*t*t+4*s.eps; ACC.mults+=3
        return sign_radical(P,Q,D)
    def recover(s,i,x):
        """unique t>=40 with G_i(t)=x: exponential search for a bracket, then bisection (all comparisons exact)"""
        lo,hi=40,41
        if s.cmp_state(i,lo,x)>0: return None
        while s.cmp_state(i,hi,x)<0:
            ACC.iters+=1; lo=hi; hi*=2
        while lo<hi:
            ACC.iters+=1; mid=(lo+hi)//2
            if s.cmp_state(i,mid,x)<0: lo=mid+1
            else: hi=mid
        return lo if s.cmp_state(i,lo,x)==0 else None
    def label(s,i,t):
        """N_i = q0(t)+q1(t)*alpha(t); alpha(t)=F_{h-1} exactly at recovered t (isqrt exact)"""
        ACC.isqrts+=1; D=5*t*t+4*s.eps; r=isqrt(D)
        if r*r!=D or (r-t)%2: return None
        a=(r-t)//2
        (c0,d0),(c1,d1)=s.N[i]
        v=Fraction(horner(c0,t),d0)+Fraction(horner(c1,t),d1)*a
        return int(v) if v.denominator==1 and v>0 else None
CLS={int(r):Class(c) for r,c in json.load(open(DATA+"/class_certificates.json")).items()}
SMALLP=json.load(open(DATA+"/small_fib_paths.json"))
def edge_label(u,v):
    """(sign,N) of the edge u->v (exact)."""
    if v>u: a,b_,sg=u,v,'+'
    else: a,b_,sg=v,u,'-'            # edge {a,b_} with b_=a(N+1)^2/N
    # N^2 a + (2a-b_) N + a = 0
    disc=(b_-2*a)**2-4*a*a
    r=isqrt(disc); assert r*r==disc
    num=(b_-2*a)+r; assert num%(2*a)==0
    N=num//(2*a); assert a*(N+1)**2==b_*N
    return sg,N
SMALL={}      # value -> list of (sign,N)
for k,v in SMALLP.items():
    p=v['path']; SMALL[p[0]]=[edge_label(p[i],p[i+1]) for i in range(len(p)-1)]
KTAB={}
for k in range(24): KTAB[(F[k]%24,F[k+1]%24)]=k
REJECT="REJECT"
def is_square(n):
    r=isqrt(n); return r*r==n
def membership(x):
    """returns (L, eps_sign) with 5x^2+4(-1)^k=L^2, or None.  Authorized ops: isqrt, comparison."""
    ACC.isqrts+=2
    for sg in (1,-1):
        t=5*x*x+4*sg
        if t>0 and is_square(t):
            L=isqrt(t)
            if (x+L)%2==0: return L,sg
    return None
def route(x):
    """full selector run from READY.  returns (final, moves, status)"""
    if x in SMALL:
        S=x;mv=[]
        for sg,N in SMALL[x]:
            S=S//N*(N+1)**2 if sg=='+' else S*N//(N+1)**2; mv.append((sg,N))
        return S,mv,"small-table"
    m=membership(x)
    if m is None: return None,[],REJECT
    L,sg=m; y=(x+L)//2
    key=(x%24,y%24)
    if key not in KTAB: return None,[],REJECT
    r=KTAB[key]%12; C=CLS[r]; S=x; mv=[]
    for i,sgn_ in enumerate(C.sign):
        t=C.recover(i,S)
        if t is None: return None,mv,"recovery-failed"
        N=C.label(i,t)
        if N is None: return None,mv,"label-failed"
        if sgn_=='+':
            if S%N: return None,mv,"illegal"
            S=S//N*(N+1)**2
        else:
            if S%((N+1)**2): return None,mv,"illegal"
            S=S*N//(N+1)**2
        mv.append((sgn_,N))
    return S,mv,"route"

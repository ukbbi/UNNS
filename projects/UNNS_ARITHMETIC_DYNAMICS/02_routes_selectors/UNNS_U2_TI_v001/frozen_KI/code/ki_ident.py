"""KI-1: exact identities.  Everything here is symbolic over Q; no sampling.
A 'family' provides: comps(expr) -> tuple of polynomials (zero iff expr is 0 in the ring), sign_pos(expr) -> +1/-1/None
(constant sign for ALL real parameter values >= start), start, var."""
import sympy as sp
from ki_core import a,b,t
from sympy import Rational as R
def _poly_sign_ray(p,var,start):
    """exact (Sturm): +1/-1 if p(var)!=0 for all real var>=start, else None; 0 if p==0"""
    p=sp.Poly(sp.expand(p),var)
    if p.is_zero: return 0
    if p.degree()==0:
        c=p.LC(); return 1 if c>0 else -1
    v0=p.eval(start)
    if v0==0: return None
    if p.count_roots(start,sp.oo)>0: return None
    return 1 if v0>0 else -1
class FibFam:
    var=b; start=40; name="fib"
    def __init__(s,eps): s.eps=eps; s.D=5*b**2+4*eps
    def comps(s,expr):
        q,r=sp.div(sp.Poly(sp.expand(expr),a),sp.Poly(a**2+a*b-b**2-s.eps,a))
        pr=sp.Poly(r.as_expr(),a); return (sp.expand(pr.coeff_monomial(1)),sp.expand(pr.coeff_monomial(a)))
    def sign_pos(s,expr):
        """sign of e0+e1*alpha, alpha=(sqrt(D)-b)/2>0, for all real b>=40 (sufficient test; None = not certified)"""
        e0,e1=s.comps(expr); P=sp.expand(2*e0-b*e1); Q=e1
        sP=_poly_sign_ray(P,b,40); sQ=_poly_sign_ray(Q,b,40)
        if sP is None or sQ is None: return None
        if sQ==0: return sP
        if sP==0: return sQ
        if sP==sQ: return sP
        sd=_poly_sign_ray(sp.expand(P**2-Q**2*s.D),b,40)
        if sd is None or sd==0: return None
        return sP if sd>0 else sQ
class PolyFam:
    var=t; name="poly"
    def __init__(s,t0): s.start=t0
    def comps(s,expr): return (sp.expand(expr),)
    def sign_pos(s,expr): return _poly_sign_ray(expr,t,s.start)
def _coeff_eqs(fam,expr):
    eqs=[]
    for c in fam.comps(expr):
        c=sp.expand(c)
        if c==0: continue
        eqs+=list(sp.Poly(c,fam.var).all_coeffs())
    return eqs
def is_zero(fam,expr): return all(c==0 for c in (sp.expand(x) for x in fam.comps(expr)))
def find_const(fam,N):
    c=sp.Symbol('c'); eqs=_coeff_eqs(fam,N-c)
    if not eqs: return sp.Integer(0)
    sol=sp.solve(eqs,c,dict=True)
    return sol[0][c] if sol else None
def find_affine(fam,N,S):
    c0,c1=sp.symbols('c0 c1'); eqs=_coeff_eqs(fam,N-c1*S-c0)
    if not eqs: return (sp.Integer(0),sp.Integer(0))
    sol=sp.solve(eqs,[c0,c1],dict=True)
    if not sol or c0 not in sol[0] or c1 not in sol[0]: return None
    return (sol[0][c0],sol[0][c1])
def find_quad(fam,N,S,maxj=1):
    """relation sum_{i<=2,j<=1} k_ij N^i S^j = 0 ; returns coefficient dict (one rational nullspace vector) or None.
    Requires the N^2-part nonzero (A2 != 0 as polynomial in S)."""
    ks={(i,j):sp.Symbol(f"k{i}{j}") for i in range(3) for j in range(maxj+1)}
    expr=sum(ks[i,j]*N**i*S**j for (i,j) in ks)
    eqs=_coeff_eqs(fam,expr); unk=list(ks.values())
    if not eqs: return None
    A,_=sp.linear_eq_to_matrix(eqs,unk); ns=A.nullspace()
    best=None
    for v in ns:
        d={k:v[idx] for idx,k in enumerate(ks)}
        if any(d[(2,j)]!=0 for j in range(maxj+1)): best=d; break
    if best is None: return None
    den=sp.ilcm(*[sp.Rational(x).q for x in best.values()]); best={k:sp.Rational(v*den) for k,v in best.items()}
    return best
def certify_quad(fam,N,S,rel):
    """A2(S)N^2+A1(S)N+A0(S)=0, A_i=k_i0+k_i1 S. W=2A2 N+A1 ; Delta=A1^2-4A2A0.
    certify: relation identity, W^2=Delta(S) identity, A2(S) constant sign (nonvanishing), sign of W constant."""
    maxj=max(j for (_,j) in rel)
    A=[sum(rel[(i,j)]*S**j for j in range(maxj+1)) for i in range(3)]
    ok_rel=is_zero(fam,A[2]*N**2+A[1]*N+A[0])
    W=sp.expand(2*A[2]*N+A[1]); Delta=sp.expand(A[1]**2-4*A[2]*A[0])
    ok_sq=is_zero(fam,W**2-Delta)
    sA2=fam.sign_pos(A[2]); sW=fam.sign_pos(W)
    return dict(rel=rel,ok_relation=ok_rel,ok_square=ok_sq,sign_A2=sA2,sign_W=sW,
                certified=bool(ok_rel and ok_sq and sA2 not in (None,0) and sW not in (None,0)))
def analyse_step(fam,N,S):
    c=find_const(fam,N)
    if c is not None and is_zero(fam,N-c): return dict(kind="const",value=c)
    f=find_affine(fam,N,S)
    if f is not None and is_zero(fam,N-f[0]-f[1]*S):
        return dict(kind="affine",c0=f[0],c1=f[1],sign_c1=1 if f[1]>0 else -1,certified=True)
    rel=find_quad(fam,N,S)
    if rel is not None:
        r=certify_quad(fam,N,S,rel); r["kind"]="quad"; return r
    return dict(kind="none")

"""KI-2: exact degree of a label over the state.  For N,S in K=Q(m) (m = rational parameter: the conic parameter for the Cassini ring,
t for the square families) compute d = [Q(S,N):Q(S)] = minimal N-degree of a polynomial relation F(N,S)=0 over Q.
Negative statements ('no relation with deg_N <= d-1') are certified by rank computations mod a prime (rank_p <= rank_Q, so a trivial
nullspace mod p implies trivial over Q) using exactly the sample points on the curve; the minimal relation found is then checked as an
exact rational-function identity by evaluation at more points than its degree bound."""
import sympy as sp
from fractions import Fraction
from ki_core import a,b,t,m
P1=(1<<61)-1   # Mersenne prime for rank certificates
def fib_param(eps):
    """rational parametrization of X^2-5Y^2=4eps, X=2a+b, Y=b.  returns (Yexpr(m), Xexpr(m))"""
    if eps==1: return (4*m/(5-m**2), (10+2*m**2)/(5-m**2))
    return ((m**2-2*m+5)/(m**2-5), (-m**2+10*m-5)/(m**2-5))
def to_rational_fn(fam,expr,eps=None):
    """return sympy rational function of m for a ring element expr (Fib: in a,b ; squares: in t)"""
    if fam=="fib":
        Y,X=fib_param(eps); return sp.cancel(sp.together(expr.subs({a:(X-Y)/2,b:Y},simultaneous=True)))
    return sp.cancel(expr.subs(t,m))
def rf_degree(f):
    n,d=sp.fraction(sp.cancel(f)); return max(sp.Poly(n,m).degree(),sp.Poly(d,m).degree())
def values(fn,fS,mvals):
    """exact (N,S) at rational m values (skip poles)"""
    nn,nd=sp.fraction(fn); sn,sd=sp.fraction(fS); pn=sp.lambdify(m,nn,'sympy'); out=[]
    Nn=sp.Poly(nn,m); Nd=sp.Poly(nd,m); Sn=sp.Poly(sn,m); Sd=sp.Poly(sd,m)
    for mv in mvals:
        mv=sp.Rational(mv)
        dN,dS=Nd.eval(mv),Sd.eval(mv)
        if dN==0 or dS==0: continue
        out.append((Fraction(int((Nn.eval(mv)/dN).p),int((Nn.eval(mv)/dN).q)),Fraction(int((Sn.eval(mv)/dS).p),int((Sn.eval(mv)/dS).q))))
    return out
def _modp(fr,p): return fr.numerator%p*pow(fr.denominator%p,-1,p)%p
def nullity_modp(rows,ncols,p=P1):
    M=[r[:] for r in rows]; rank=0
    for col in range(ncols):
        piv=None
        for r in range(rank,len(M)):
            if M[r][col]%p: piv=r;break
        if piv is None: continue
        M[rank],M[piv]=M[piv],M[rank]; inv=pow(M[rank][col],-1,p); M[rank]=[x*inv%p for x in M[rank]]
        for r in range(len(M)):
            if r!=rank and M[r][col]%p:
                f=M[r][col]; M[r]=[(x-f*y)%p for x,y in zip(M[r],M[rank])]
        rank+=1
    return ncols-rank
def min_relation_degree(pts,dnmax,dsmax,p=P1):
    """smallest dn<=dnmax such that a nonzero relation sum_{i<=dn,j<=dsmax} k_ij N^i S^j vanishes on all pts (mod p).  returns dn or None"""
    for dn in range(1,dnmax+1):
        cols=[(i,j) for i in range(dn+1) for j in range(dsmax+1)]
        if len(pts)<len(cols)+8: raise ValueError("need more points")
        rows=[[pow(_modp(N,p),i,p)*pow(_modp(S,p),j,p)%p for (i,j) in cols] for N,S in pts]
        if nullity_modp(rows,len(cols),p)>0: return dn
    return None
def exact_relation(pts,dn,ds):
    cols=[(i,j) for i in range(dn+1) for j in range(ds+1)]
    M=sp.Matrix([[sp.Rational(N.numerator,N.denominator)**i*sp.Rational(S.numerator,S.denominator)**j for (i,j) in cols] for N,S in pts])
    from sympy.polys.matrices import DomainMatrix
    dm=DomainMatrix.from_Matrix(M).convert_to(sp.QQ); ns=dm.nullspace().to_Matrix()
    return cols,ns

def certify_min_relation(fn,fS,d,dN,dS,extra=12):
    """exact: a relation F(N,S)=0 with deg_N=d (deg_S<=dN) exists over Q and is an identity in Q(m); returns dict"""
    cols=[(i,j) for i in range(d+1) for j in range(dN+1)]
    mv=[sp.Rational(k,5)+sp.Rational(1,3) for k in range(1,len(cols)+extra+80)]
    pts=values(fn,fS,mv)
    from sympy.polys.matrices import DomainMatrix
    sub=pts[:len(cols)+extra]
    M=sp.Matrix([[sp.Rational(N.numerator,N.denominator)**i*sp.Rational(S.numerator,S.denominator)**j for (i,j) in cols] for N,S in sub])
    ns=DomainMatrix.from_Matrix(M).convert_to(sp.QQ).nullspace().to_Matrix()
    if ns.rows==0: return dict(exists=False)
    vec=ns.row(0); den=sp.ilcm(*[x.q for x in vec]); vec=[sp.Integer(x*den) for x in vec]
    ks={c:vec[idx] for idx,c in enumerate(cols)}
    bound=d*dN+dN*dS      # degree bound of numerator polynomial  (ds<=dN)
    need=bound+1
    mv2=[sp.Rational(k,11)+sp.Rational(2,7) for k in range(1,need+60)]
    pts2=values(fn,fS,mv2)
    if len(pts2)<need: raise ValueError("not enough points")
    ok=True
    for N,S in pts2[:need]:
        val=sum(int(k)*(N**i)*(S**j) for (i,j),k in ks.items())
        if val!=0: ok=False;break
    # irreducibility is not needed: minimality of d comes from the mod-p lower bound
    deg_s=max(j for (i,j),k in ks.items() if k!=0); deg_n=max(i for (i,j),k in ks.items() if k!=0)
    return dict(exists=True,identity_verified=ok,points_checked=need,deg_n=deg_n,deg_s=deg_s,nullity=ns.rows,
                max_coeff_digits=max(len(str(abs(int(k)))) for k in ks.values()))

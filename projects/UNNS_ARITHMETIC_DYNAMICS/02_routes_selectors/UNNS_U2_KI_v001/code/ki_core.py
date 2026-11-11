"""U2-KI core: symbolic states/labels of every audited route step, exact rings, rational points.
Fibonacci: ring R_eps=Q[b][a]/(a^2+ab-b^2-eps); states/labels from the frozen FP-SYM certificates.
Squares direct: Q[t]; wrapper: Q[t] via the frozen U2-001 identities.  All objects are sympy expressions."""
import json, os, sys
import sympy as sp
from fractions import Fraction
HERE=os.path.dirname(os.path.abspath(__file__)); BASE=HERE+"/../baseline_R3_frozen"; DATA=BASE+"/data"
sys.path.insert(0,BASE+"/code"); sys.path.insert(0,BASE+"/code/sq")
a,b,t,m=sp.symbols('a b t m')
def red(expr,eps):
    """reduce polynomial in a,b modulo a^2 = -ab + b^2 + eps  -> (u(b), v(b)) with expr = u + v*a"""
    e=sp.expand(expr); p=sp.Poly(e,a); res=sp.Integer(0)
    # replace powers of a iteratively
    rel=-a*b+b**2+eps
    pw={0:sp.Integer(1),1:a}
    mx=p.degree()
    for k in range(2,mx+1): pw[k]=sp.expand(sp.expand(a*pw[k-1]).subs(a**2,rel)) if False else None
    # explicit reduction by polynomial remainder
    q,r=sp.div(sp.Poly(e,a),sp.Poly(a**2+a*b-b**2-eps,a))
    r=r.as_expr(); r=sp.expand(r)
    pr=sp.Poly(r,a)
    return sp.expand(pr.coeff_monomial(1)),sp.expand(pr.coeff_monomial(a))
class Ring:
    """element = (u,v): u + v*a  (Fibonacci ring, eps) ; for squares use a pure polynomial ring (v==0)."""
    def __init__(s,eps): s.eps=eps
    def el(s,expr):
        u,v=red(expr,s.eps); return (u,v)
    def expr(s,e): return e[0]+e[1]*a
def load_fib():
    C=json.load(open(DATA+"/class_certificates.json")); out={}
    for r,c in C.items():
        r=int(r); eps=c['eps']; R=Ring(eps)
        S=[R.el(sp.sympify(u,locals={'b':b,'a':a})+sp.sympify(v,locals={'b':b,'a':a})*a) for u,v in c['states_ring']]
        N=[R.el(sp.sympify(u,locals={'b':b,'a':a})+sp.sympify(v,locals={'b':b,'a':a})*a) for u,v in c['labels_ring']]
        out[r]=dict(eps=eps,R=R,signs=[sg for sg,_ in c['searchnames']],S=S,N=N,hres=c['hres'])
    return out
def load_sq_direct():
    D=json.load(open(DATA+"/sq/square_identities.json"))["classes"]; out={}
    for rs,v in D.items():
        r=int(rs); n=24*t+r; S=sp.expand(n**2); Ss=[S]; Ns=[]; sg=[]
        for s,Nstr in v["steps"]:
            N=sp.sympify(Nstr,locals={'t':t}); Ns.append(sp.expand(N)); sg.append(s)
            S=sp.cancel(S*(N+1)**2/N) if s=='+' else sp.cancel(S*N/(N+1)**2)
            Ss.append(sp.expand(S))
        out[r]=dict(t0=v["t0"],signs=sg,S=Ss[:-1],N=Ns,Sfinal=Ss[-1],n=n)
    return out
def load_sq_wrapper():
    import u1_bnd_lib as L
    out={}
    for ident in L.IDENTITIES:
        M,r=ident['M'],ident['r']; t0=[t0 for (nm,M2,r2,t0,st) in L._I if nm==ident['name']][0]
        tt=L.T; mm=M*tt+r; nn=mm+1
        S=sp.expand(nn**2); Ss=[];Ns=[];sg=[]
        Ns.append(sp.expand(mm)); sg.append('-'); Ss.append(S); S=sp.expand(mm)
        for s,e in ident['steps']:
            Ss.append(sp.expand(S)); Ns.append(sp.expand(e)); sg.append(s)
            S=sp.cancel(S*(e+1)**2/e) if s=='+' else sp.cancel(S*e/(e+1)**2)
        S=sp.expand(S); assert sp.simplify(S-(mm+1))==0
        Ss.append(S); Ns.append(S); sg.append('+')
        out[ident['name']]=dict(t0=t0,signs=sg,S=[x.subs(tt,t) for x in Ss],N=[x.subs(tt,t) for x in Ns],M=M,r=r)
    return out

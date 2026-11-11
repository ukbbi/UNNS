"""Symbolic certifier for Fibonacci path families in the quotient ring
K_eps = Q(b)[a]/(a^2 + a b - b^2 - eps), eps = (-1)^h, (a,b)=(F_{h-1},F_h).
Elements are pairs (p0,p1) of rational functions in b meaning p0 + p1*a.
All arithmetic is exact (sympy rational functions)."""
import sympy as sp, json, sys
b=sp.symbols('b')
class K:
    def __init__(s,eps):
        s.eps=eps
        # a^2 = eps + b^2 - b a ;  conj(a) = -b - a ; N(a) = -(b^2+eps)
    def c(s,e): return sp.cancel(sp.together(e))
    def norm(s,e):
        p0,p1=e; eps=s.eps
        return s.c(p0*p0 - b*p0*p1 - (b*b+eps)*p1*p1)
    def mul(s,u,v):
        p0,p1=u;q0,q1=v
        # (p0+p1 a)(q0+q1 a)= p0q0 + (p0q1+p1q0)a + p1q1 a^2, a^2=eps+b^2-b a
        t=p1*q1
        return (s.c(p0*q0+t*(s.eps+b*b)), s.c(p0*q1+p1*q0-t*b))
    def conj(s,e): p0,p1=e; return (s.c(p0-b*p1), s.c(-p1))
    def inv(s,e):
        n=s.norm(e); cj=s.conj(e); return (s.c(cj[0]/n), s.c(cj[1]/n))
    def add(s,u,v): return (s.c(u[0]+v[0]),s.c(u[1]+v[1]))
    def sub(s,u,v): return (s.c(u[0]-v[0]),s.c(u[1]-v[1]))
    def sc(s,u,r): return (s.c(u[0]*r),s.c(u[1]*r))
    def const(s,r): return (sp.Rational(r),sp.Integer(0))
    def iszero(s,u): return u[0]==0 and u[1]==0
    def div(s,u,v): return s.mul(u,s.inv(v))
A_=lambda: (sp.Integer(0),sp.Integer(1))
B_=lambda: (b,sp.Integer(0))
def lin(K_,ca,cb,c0,d=1):
    return (sp.Rational(c0,d)+sp.Rational(cb,d)*b, sp.Rational(ca,d))
def setup(kind):
    """returns (K, x, y, eps) with x=F_k, y=F_{k+1} in the ring."""
    if kind=='A' or kind=='C':   # k=2h, h parity: A h even(eps=+1), C h odd (eps=-1)
        eps=1 if kind=='A' else -1
        R=K(eps); a=A_(); bb=B_()
        two_a_b=R.add(R.sc(a,2),bb)               # L_h = 2a+b
        x=R.mul(bb,two_a_b)                          # F_{2h}=b(2a+b)
        c=R.add(a,bb)
        y=R.add(R.mul(bb,bb),R.mul(c,c))             # F_{2h+1}=b^2+c^2
        return R,x,y,eps
    else:                        # B: k=2h+1, h odd (eps=-1)
        eps=-1
        R=K(eps); a=A_(); bb=B_(); c=R.add(a,bb)
        x=R.add(R.mul(bb,bb),R.mul(c,c))             # F_{2h+1}
        y=R.mul(c,R.add(a,R.sc(bb,3)))               # F_{2h+2}=c(a+3b)
        return R,x,y,eps
def evalLabel(R,expr_str,x,y):
    X,Y=sp.symbols('x y')
    e=sp.sympify(expr_str,locals={'x':X,'y':Y})
    # polynomial in x,y with rational coeffs
    P=sp.Poly(sp.expand(e),X,Y)
    out=R.const(0)
    for (i,j),co in P.terms():
        t=R.const(co)
        for _ in range(i): t=R.mul(t,x)
        for _ in range(j): t=R.mul(t,y)
        out=R.add(out,t)
    return out
def certify(kind,labels):
    R,x,y,eps=setup(kind)
    s=x; states=[x]; steps=[]
    for sign,lab in labels:
        N=evalLabel(R,lab,x,y)
        N1=R.add(N,R.const(1)); N1sq=R.mul(N1,N1)
        if sign=='+': s=R.div(R.mul(s,N1sq),N)
        else:         s=R.div(R.mul(s,N),N1sq)
        states.append(s); steps.append((sign,lab,N))
    ok=R.iszero(R.sub(s,y))
    return R,x,y,states,steps,ok
def show(e):
    p0,p1=e
    return "(%s) + (%s)*a"%(sp.factor(p0),sp.factor(p1))
if __name__=="__main__":
    d=json.load(open('../data/fibonacci_identities_raw.json'))
    for kind,key in (('A','4'),('B','7'),('C','10')):
        R,x,y,st,steps,ok=certify(kind,d[key]['labels'])
        print(kind,key,"final state == y symbolically:",ok)
        for i,s in enumerate(st): print("  s%d ="%i,show(s))

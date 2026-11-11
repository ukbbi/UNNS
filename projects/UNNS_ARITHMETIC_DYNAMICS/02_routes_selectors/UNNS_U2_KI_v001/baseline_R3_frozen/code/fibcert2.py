import sympy as sp, json, math
from fibcert import *
def pisano(m):
    if m==1: return 1
    a,b=0,1
    for i in range(1,6*m+10):
        a,b=b,(a+b)%m
        if a==0 and b==1: return i
def fibs(n):
    F=[0,1]
    while len(F)<n: F.append(F[-1]+F[-2])
    return F
F=fibs(4000)
def lam(e):
    p0,p1=e
    return sp.lambdify(b,[sp.together(p0),sp.together(p1)],modules=[{}]) 
def den_lcm(e):
    d=1
    for p in e:
        for co in sp.Poly(sp.numer(sp.together(p)),b).all_coeffs(): pass
        dn=sp.denom(sp.together(p))
        # denominator must be a pure integer constant
        assert dn.is_Integer, ("nonconstant denominator",dn)
        d=math.lcm(d,int(dn))
    return d
def evalq(e,A,B):
    p0,p1=e
    n0=sp.Poly(sp.numer(sp.together(p0)),b); d0=int(sp.denom(sp.together(p0)))
    n1=sp.Poly(sp.numer(sp.together(p1)),b); d1=int(sp.denom(sp.together(p1)))
    v0=0
    for co in n0.all_coeffs(): v0=v0*B+int(co)
    v1=0
    for co in n1.all_coeffs(): v1=v1*B+int(co)
    from fractions import Fraction
    return Fraction(v0,d0)+Fraction(v1,d1)*A
def shift_nonneg(poly,b0):
    q=sp.Poly(poly.as_expr().subs(b,b+b0),b)
    return all(co>=0 for co in q.all_coeffs())
def positive_eventually(e,b0=40):
    """e=p0+p1 a >0 for all (a,b) with b>=b0 and a/b in [1/2,2/3] (true for h>=3): check both endpoint polys."""
    res=[]
    for r in (sp.Rational(1,2),sp.Rational(2,3)):
        q=sp.Poly(sp.together(e[0]+e[1]*r*b),b)
        num=sp.Poly(sp.numer(sp.together(e[0]+e[1]*r*b)),b)
        den=sp.denom(sp.together(e[0]+e[1]*r*b))
        res.append(shift_nonneg(num,b0) and sp.denom(den)==1 and den>0 and num.LC()>0)
    return all(res)
def mono_eventually(e,b0=40):
    p0,p1=e
    P0=sp.Poly(sp.numer(sp.together(p0)),b); d0=sp.denom(sp.together(p0))
    P1=sp.Poly(sp.numer(sp.together(p1)),b); d1=sp.denom(sp.together(p1))
    ok0=shift_nonneg(P0.diff(b),b0)
    ok1=shift_nonneg(P1,b0) and shift_nonneg(P1.diff(b),b0)
    return ok0 and ok1
def run(kind,key,hclass,hmod):
    d=json.load(open('../data/fibonacci_identities_raw.json'))
    R,x,y,states,steps,ok=certify(kind,d[key]['labels'])
    objs=[('s%d'%i,s) for i,s in enumerate(states)]+[('N%d'%(i+1),st[2]) for i,st in enumerate(steps)]
    D=1
    for n,e in objs: D=math.lcm(D,den_lcm(e))
    per=pisano(D)
    period=math.lcm(per,hmod)
    # integrality over one full period (and a second period as margin)
    integ=True
    for n,e in objs:
        for h in range(hclass%hmod+hmod*0+ (hmod*((4)//hmod+1)), 0,-1) if False else []:
            pass
    hs=[h for h in range(4,4+2*period) if h%hmod==hclass]
    for n,e in objs:
        for h in hs:
            v=evalq(e,F[h-1],F[h])
            if v.denominator!=1: integ=False
    pos=all(positive_eventually(e) for n,e in objs)
    mono=all(mono_eventually(e) for n,e in objs if n.startswith('s'))
    # numeric legality replay
    legal=True
    X=None
    for h in [h for h in range(4,900) if h%hmod==hclass]:
        k=(2*h if kind!='B' else 2*h+1)
        s=F[k]; yy=F[k+1]
        for i,(sign,lab,N) in enumerate(steps):
            Nv=evalq(N,F[h-1],F[h]); assert Nv.denominator==1 and Nv>0
            Nv=int(Nv)
            if sign=='+':
                if s%Nv: legal=False
                s=s*(Nv+1)**2//Nv
            else:
                if s%((Nv+1)**2): legal=False
                s=s*Nv//(Nv+1)**2
        if s!=yy: legal=False
    return dict(kind=kind,k_class=key,symbolic_final_equals_y=bool(ok),denominator_lcm=D,pisano_period=per,
                integrality_all_states_and_labels=integ,positivity_all=pos,monotone_states=mono,numeric_legal_replay=legal,
                n_states=len(states),n_steps=len(steps))
if __name__=="__main__":
    out=[run('A','4',2,6),run('B','7',3,6),run('C','10',5,6)]
    for r in out: print(r)
    json.dump(out,open('../reports/family_certificates.json','w'),indent=1)

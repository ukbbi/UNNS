"""Certify any validated path class: fit labels to ring elements p0(b)+p1(b)a, prove chain in the quotient ring, then
integrality (Pisano period), positivity (shifted-coefficient test), monotonicity of states."""
import sympy as sp, json, math, sys
from fractions import Fraction
from fibcert import K,b,A_,B_
from fibcert2 import pisano,evalq,positive_eventually,mono_eventually,den_lcm,F
import fibresolve
def fit_label(vals_by_h,eps,deg=6):
    """vals_by_h: dict h->int. Fit N=sum_i (al_i b^i + be_i a b^i), i<=deg. Exact rational; verify on all samples."""
    hs=sorted(vals_by_h)
    n=2*(deg+1)
    rows=[];rhs=[]
    for h in hs:
        a,bb=F[h-1],F[h]
        rows.append([bb**i for i in range(deg+1)]+[a*bb**i for i in range(deg+1)]); rhs.append(vals_by_h[h])
    M=sp.Matrix(rows[:n]); v=sp.Matrix(rhs[:n])
    try: sol=M.LUsolve(v)
    except Exception: return None
    for rw,rv in zip(rows,rhs):
        if sum(sp.Rational(c)*s for c,s in zip(rw,sol))!=rv: return None
    p0=sum(sol[i]*b**i for i in range(deg+1)); p1=sum(sol[deg+1+i]*b**i for i in range(deg+1))
    return (sp.nsimplify(p0),sp.nsimplify(p1))
def setup_ring(r):
    odd=(r%2==1); hres=(r//2)%6; eps=(-1)**hres
    R=K(eps); a=A_(); bb=B_(); c=R.add(a,bb)
    if not odd:
        x=R.mul(bb,R.add(R.sc(a,2),bb)); y=R.add(R.mul(bb,bb),R.mul(c,c))
    else:
        x=R.add(R.mul(bb,bb),R.mul(c,c)); y=R.mul(c,R.add(a,R.sc(bb,3)))
    return R,x,y,eps,hres
def certify_class(P,r,steps,nf,name=None):
    assert P==12
    R,x,y,eps,hres=setup_ring(r)
    # label sequences
    ks=[k for k in range(r+12*2,r+12*40,12)]
    seqs={}
    for k in ks:
        good,Ns=fibresolve.replay(steps,nf,k); assert good
        seqs[k]=Ns
    Ls=[]
    for i in range(len(steps)):
        vals={(k//2):seqs[k][i] for k in ks}
        fit=fit_label(vals,eps)
        if fit is None: return dict(class_r=r,fit_failed_at=i)
        Ls.append(fit)
    s=x;states=[x]
    for (sign,lab),N in zip(steps,Ls):
        N1=R.add(N,R.const(1)); N1sq=R.mul(N1,N1)
        s=R.div(R.mul(s,N1sq),N) if sign=='+' else R.div(R.mul(s,N),N1sq)
        states.append(s)
    ok=R.iszero(R.sub(s,y))
    objs=[('s%d'%i,e) for i,e in enumerate(states)]+[('N%d'%(i+1),e) for i,e in enumerate(Ls)]
    try:
        D=1
        for n,e in objs: D=math.lcm(D,den_lcm(e))
    except AssertionError as ex:
        return dict(class_r=r,symbolic_final_equals_y=bool(ok),nonconstant_denominator=str(ex))
    per=pisano(D); hs=[h for h in range(4,4+2*math.lcm(per,6)+6) if h%6==hres]
    integ=all(evalq(e,F[h-1],F[h]).denominator==1 for n,e in objs for h in hs)
    pos=all(positive_eventually(e) for n,e in objs)
    mono=all(mono_eventually(e) for n,e in objs if n.startswith('s'))
    # exact legality replay straight from the integer definition (all class h>=3 up to 700)
    legal=True
    for h in [h for h in range(3,700) if h%6==hres]:
        k=2*h if r%2==0 else 2*h+1
        s_=F[k]
        for (sign,lab),N in zip(steps,Ls):
            Nv=evalq(N,F[h-1],F[h]); 
            if Nv.denominator!=1 or Nv<=0: legal=False;break
            Nv=int(Nv)
            if sign=='+':
                if s_%Nv: legal=False;break
                s_=s_*(Nv+1)**2//Nv
            else:
                if s_%((Nv+1)**2): legal=False;break
                s_=s_*Nv//(Nv+1)**2
        if s_!=F[k+1]: legal=False
    return dict(class_r=r,length=len(steps),symbolic_final_equals_y=bool(ok),denominator_lcm=D,pisano_period=per,
        integrality_all_states_and_labels=integ,positivity_all=pos,monotone_states=mono,numeric_legal_replay=legal,
        labels=[[sg,str(sp.factor(N[0]))+" + ("+str(sp.factor(N[1]))+")*a"] for (sg,_),N in zip(steps,Ls)],
        searchnames=steps,
        states_ring=[[str(sp.expand(e[0])),str(sp.expand(e[1]))] for e in states],
        labels_ring=[[str(sp.expand(e[0])),str(sp.expand(e[1]))] for e in Ls],eps=eps,hres=hres)
if __name__=="__main__":
    import fibsearch2
    out=[]
    for r in (2,3,6,8):
        res=fibsearch2.search2(12,r,8)
        o=certify_class(12,r,res["steps"],res["nf"]); out.append(o)
        print({k:v for k,v in o.items() if k not in("labels","searchnames")},flush=True)
    json.dump(out,open('../reports/new_class_certificates.json','w'),indent=1)

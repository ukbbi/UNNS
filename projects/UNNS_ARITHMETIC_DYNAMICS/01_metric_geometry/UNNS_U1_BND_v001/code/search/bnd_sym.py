import sys, time, json
from math import isqrt
import sympy as sp
from bnd_param import build_points, vocab, make_neighbors
t=sp.symbols('t')
def search_states(M,r,K,J=10,seed=1,node_cap=600000):
    pts=build_points(M,r,J,seed)
    E=vocab(pts); nbrs=make_neighbors(E,J)
    A=tuple(pts);B=tuple(n+1 for n in pts)
    def grow(front,dist,par,d):
        nxt=[]
        for S in front:
            for nv,lab in nbrs(S).items():
                if nv not in dist:
                    dist[nv]=d;par[nv]=S;nxt.append(nv)
                    if len(dist)>node_cap: return nxt,True
        return nxt,False
    da={A:0};pa={A:None};fa=[A];db={B:0};pb={B:None};fb=[B];ra=rb=0
    for step in range(1,K+1):
        if len(da)<=len(db): fa,cap=grow(fa,da,pa,ra+1);ra+=1
        else: fb,cap=grow(fb,db,pb,rb+1);rb+=1
        if cap: return None,pts,"cap"
        small,large=(da,db) if len(da)<len(db) else (db,da)
        hits=[v for v in small if v in large]
        if hits:
            v=min(hits,key=lambda x:da.get(x,99)+db.get(x,99))
            def chain(par,v):
                out=[v]
                while par[v] is not None: v=par[v];out.append(v)
                return out
            f=chain(pa,v)[::-1]; g=chain(pb,v)[1:]
            return f+g,pts,"ok"
    return None,pts,"none"
def label_vec(X,Y):
    """edge between state vectors X,Y -> ('+',N) if Y=fwd(X,N) else ('-',N) if X=fwd(Y,N)"""
    if all(y>x for x,y in zip(X,Y)): d='+';lo,hi=X,Y
    elif all(x>y for x,y in zip(X,Y)): d='-';lo,hi=Y,X
    else: return None
    Ns=[]
    for x,y in zip(lo,hi):
        disc=y*y-4*x*y;rt=isqrt(disc)
        assert rt*rt==disc
        num=(y-2*x)+rt;assert num%(2*x)==0
        Ns.append(num//(2*x))
    return d,Ns
def symbolic(M,r,states,pts):
    tj=[(n-r)//M for n in pts]
    L=len(states)-1
    S=[sp.interpolate(list(zip(tj,[s[j] for s in [st]])) if False else list(zip(tj,list(st))),t) for st in states]
    S=[sp.expand(sp.Poly(x,t).as_expr()) for x in S]
    steps=[];ok=True;notes=[]
    for i in range(L):
        lv=label_vec(states[i],states[i+1])
        d,Ns=lv
        N=sp.expand(sp.interpolate(list(zip(tj,Ns)),t))
        lo,hi=(S[i],S[i+1]) if d=='+' else (S[i+1],S[i])
        # identity: hi = lo/N*(N+1)^2
        ident=sp.cancel(hi-lo/N*(N+1)**2)
        if ident!=0: ok=False;notes.append(f"step {i}: identity fails")
        # divisibility: lo/N and hi/(N+1)^2 must be integer-valued polynomials
        for name,num,den in (("lo/N",lo,N),("hi/(N+1)^2",hi,(N+1)**2)):
            q,rem=sp.div(sp.Poly(num,t),sp.Poly(den,t))
            if rem.as_expr()!=0: ok=False;notes.append(f"step {i}: {name} not polynomial")
            else:
                deg=q.degree();vals=[q.as_expr().subs(t,k) for k in range(0,max(deg,0)+1)]
                if not all(sp.Rational(v).q==1 for v in vals): ok=False;notes.append(f"step {i}: {name} not integer-valued")
        steps.append((d,sp.factor(N)))
    return ok,S,steps,notes
if __name__=="__main__":
    M,r,K=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
    st,pts,msg=search_states(M,r,K)
    if st is None: print(M,r,"no path",msg);sys.exit()
    ok,S,steps,notes=symbolic(M,r,st,pts)
    n=M*t+r
    print(f"n={M}t+{r}: length {len(st)-1}, symbolic check {'PASS' if ok else 'FAIL'}",notes)
    for i,(d,N) in enumerate(steps): print("  step",i+1,d,"N =",N,"   state:",sp.factor(S[i+1]))

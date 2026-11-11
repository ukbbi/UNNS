import re, json, sys
from math import isqrt
from fibparam import F
ATOM={"a":(1,0),"b":(0,1),"c":(1,1),"Lh1":(1,3),"Lhm":(-1,2),"Lh":(2,1),"Fh2":(1,2),"Fh3":(2,3)}
def aval(tok,a,b):
    m=re.fullmatch(r"(Lh1|Lhm|Lh|Fh2|Fh3|a|b|c)([+-]1)?",tok)
    u,v=ATOM[m.group(1)]; return u*a+v*b+(int(m.group(2)) if m.group(2) else 0)
def val(expr,x,y,a,b):
    if re.fullmatch(r"\d+",expr): return int(expr)
    m=re.fullmatch(r"\((-?\d+)a([+-]\d+)b([+-]\d+)\)/(\d+)",expr)
    if m:
        u,v,w,d=map(int,m.groups()); n=u*a+v*b+w; assert n%d==0; return n//d
    m=re.fullmatch(r"\((-?\d+)x([+-]\d+)y([+-]\d+)\)/(\d+)",expr)
    if m:
        u,v,w,d=map(int,m.groups()); n=u*x+v*y+w; assert n%d==0; return n//d
    m=re.fullmatch(r"\[(\d+)\*([^*]+)\*([^*]+)\]",expr)
    if m: return int(m.group(1))*aval(m.group(2),a,b)*aval(m.group(3),a,b)
    raise ValueError(expr)
def Nof(sign,lab,S,x,y,a,b):
    """N from exploring-direction state S."""
    if lab.startswith("S/"): e=lab[2:]; v=val(e,x,y,a,b); assert S%v==0; return S//v
    if lab.startswith("q=sqrt(S/"): e=lab[len("q=sqrt(S/"):-1]; v=val(e,x,y,a,b); t=S//v; q=isqrt(t); assert S%v==0 and q*q==t; return q-1
    if lab.startswith("q="): return val(lab[2:],x,y,a,b)-1
    return val(lab,x,y,a,b)
def move(sign,N,S):
    if sign=="+": assert S%N==0; return S//N*(N+1)**2
    assert S%((N+1)**2)==0; return S//((N+1)**2)*N
def replay(steps,nf,k):
    h=k//2; a,b=F[h-1],F[h]; x,y=F[k],F[k+1]
    S=x; Ns=[]
    for sign,lab in steps[:nf]:
        N=Nof(sign,lab,S,x,y,a,b); S=move(sign,N,S); Ns.append(N)
    T=y; gN=[]
    for sign,lab in reversed(steps[nf:]):
        osign="+" if sign=="-" else "-"       # exploring direction sign
        N=Nof(osign,lab,T,x,y,a,b); T=move(osign,N,T); gN.append(N)
    gN=gN[::-1]
    return S==T, Ns+gN
def run(P,r,steps,nf,kmax=1500):
    ok=True;n=0;seqs=[]
    for k in range(r+P*3,kmax,P):
        try:
            good,Ns=replay(steps,nf,k)
        except (AssertionError,ValueError,ZeroDivisionError): good=False;Ns=None
        n+=1;ok&=good
        if not good: return False,k
        seqs.append((k,Ns))
    return ok,seqs
if __name__=="__main__":
    res=json.loads(sys.argv[1]); ok,s=run(res["P"],res["r"],res["steps"],res["nf"])
    print(ok, s if ok is False else len(s))

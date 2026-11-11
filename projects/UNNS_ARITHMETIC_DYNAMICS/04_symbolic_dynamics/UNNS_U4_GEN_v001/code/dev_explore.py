"""DEVELOPMENT EXPLORATION (pre-registration, logged). Prime-chip dynamics on exponent vectors."""
import sympy,sys,json
from functools import lru_cache
@lru_cache(None)
def fac(n): return tuple(sorted(sympy.factorint(n).items()))
def init(x): return dict(sympy.factorint(x))
def step(e,p):
    e=dict(e);e[p]-=1
    if e[p]==0: del e[p]
    for q,k in fac(p+1): e[q]=e.get(q,0)+2*k
    return e
RULES={
 'spf':lambda e,h:min(e),
 'lpf':lambda e,h:max(e),
 'maxexp_small':lambda e,h:min(e,key=lambda p:(-e[p],p)),
 'maxexp_large':lambda e,h:min(e,key=lambda p:(-e[p],-p)),
 'minexp_small':lambda e,h:min(e,key=lambda p:(e[p],p)),
 'minexp_large':lambda e,h:min(e,key=lambda p:(e[p],-p)),
 'oddexp_small':lambda e,h:min([p for p in e if e[p]%2] or list(e)),
 'rotate_next':lambda e,h:(min([p for p in e if p>h] or [min(e)]) if h else min(e)),
 'rotate_prev':lambda e,h:(max([p for p in e if p<h] or [max(e)]) if h else max(e)),
}
def period_tail(w,maxp=300,tail=1500):
    t=w[-tail:]
    for p in range(1,maxp+1):
        if all(t[i]==t[i+p] for i in range(len(t)-p)): return p
    return None
def run(x,rule,H=3000):
    e=init(x);w=[];h=0
    for _ in range(H):
        if not e: return None
        p=RULES[rule](e,h);w.append(p);h=p;e=step(e,p)
    return w
if __name__=="__main__":
    for r in RULES:
        res={}
        for x in range(2,40):
            w=run(x,r)
            if w is None: res[x]='dead';continue
            res[x]=period_tail(w)
        vals=sorted(set(map(str,res.values())))
        print(r,vals, {k:v for k,v in list(res.items())[:6]})

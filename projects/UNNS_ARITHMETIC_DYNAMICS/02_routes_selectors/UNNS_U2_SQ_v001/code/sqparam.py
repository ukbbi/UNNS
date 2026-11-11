import sys, random, itertools, time
from math import isqrt
def build_points(M,r,J,seed):
    rng=random.Random(seed); ts=set()
    while len(ts)<J: ts.add(rng.randint(10**4,10**6))
    return [r+M*t for t in sorted(ts)]
def vocab(pts):
    E={}                               # vector -> string
    J=len(pts)
    for c in range(1,25): E.setdefault(tuple([c]*J),str(c))
    lin=[]
    for a in (1,2,3,4,6,8,12):
        for b in range(-12,13):
            for c in (1,2,3,4,6,8,12,24):
                vals=[]
                for n in pts:
                    num=a*n+b
                    if num<=0 or num%c: vals=None;break
                    vals.append(num//c)
                if vals:
                    v=tuple(vals)
                    if v not in E: E[v]=f"({a}n{b:+d})/{c}"; lin.append(v)
    small=[]
    for a in (1,2):
        for b in range(-2,3):
            for c in (1,2,4):
                vals=[]
                for n in pts:
                    num=a*n+b
                    if num<=0 or num%c: vals=None;break
                    vals.append(num//c)
                if vals: small.append((tuple(vals),f"({a}n{b:+d})/{c}"))
    for (u,su),(w,sw) in itertools.combinations_with_replacement(small,2):
        v=tuple(x*y for x,y in zip(u,w))
        if v not in E: E[v]=f"[{su}*{sw}]"
    return E
def make_neighbors(E,J):
    items=list(E.items())
    cons=[(v,s) for v,s in items if s.isdigit()]
    def nbrs(S):
        out={}
        # forward with N = e
        for v,s in items:
            if all(x%y==0 for x,y in zip(S,v)):
                nv=tuple(x//y*(y+1)**2 for x,y in zip(S,v))
                if nv!=S: out.setdefault(nv,('+',s))
        # forward with N = S/e
        for v,s in items:
            if s.isdigit() or True:
                if all(x%y==0 for x,y in zip(S,v)):
                    N=tuple(x//y for x,y in zip(S,v))
                    nv=tuple(x//n*(n+1)**2 for x,n in zip(S,N))
                    if nv!=S: out.setdefault(nv,('+',f"S/{s}"))
        # inverse with q=N+1 in E
        for v,s in items:
            if all(y>=2 and x%(y*y)==0 for x,y in zip(S,v)):
                nv=tuple(x//(y*y)*(y-1) for x,y in zip(S,v))
                out.setdefault(nv,('-',f"q={s}"))
        # inverse with q = sqrt(S/e)
        for v,s in items:
            if all(x%y==0 for x,y in zip(S,v)):
                qs=[]
                ok=True
                for x,y in zip(S,v):
                    t=x//y;q=isqrt(t)
                    if q*q!=t or q<2: ok=False;break
                    qs.append(q)
                if ok:
                    nv=tuple(y*(q-1) for y,q in zip(v,qs))
                    out.setdefault(nv,('-',f"q=sqrt(S/{s})"))
        return out
    return nbrs
def search(M,r,K=6,J=4,seed=1,node_cap=400000,verbose=False):
    pts=build_points(M,r,J,seed)
    E=vocab(pts); nbrs=make_neighbors(E,J)
    A=tuple(n*n for n in pts); B=tuple((n+1)**2 for n in pts)
    def grow(front,dist,par,d):
        nxt=[]
        for S in front:
            for nv,lab in nbrs(S).items():
                if nv not in dist:
                    dist[nv]=d;par[nv]=(S,lab);nxt.append(nv)
                    if len(dist)>node_cap: return nxt,True
        return nxt,False
    da={A:0};pa={A:None};fa=[A]
    db={B:0};pb={B:None};fb=[B]
    ra=rb=0
    if A==B: return 0,[]
    for t in range(1,K+1):
        # grow the smaller side
        if len(da)<=len(db):
            fa,capped=grow(fa,da,pa,ra+1);ra+=1
        else:
            fb,capped=grow(fb,db,pb,rb+1);rb+=1
        if capped: return None,f"cap at t={t} sizes {len(da)},{len(db)}"
        small,large=(da,db) if len(da)<len(db) else (db,da)
        hits=[v for v in small if v in large]
        if hits:
            v=min(hits,key=lambda x:da.get(x,99)+db.get(x,99))
            def chain(par,v):
                out=[]
                while par[v] is not None:
                    p,lab=par[v];out.append((lab));v=p
                return out[::-1]
            f=chain(pa,v); g=chain(pb,v)
            g=[('-' if l[0]=='+' else '+',l[1]) for l in reversed(g)]
            return da[v]+db[v], f+g, len(f)
    return None,"none within K"
if __name__=="__main__":
    import multiprocessing as mp
    M,K=int(sys.argv[1]),int(sys.argv[2]); J=int(sys.argv[3]) if len(sys.argv)>3 else 4
    def run(r):
        t0=time.time()
        try: res=search(M,r,K,J=J)
        except Exception as e: res=(None,repr(e))
        return r,res,round(time.time()-t0,1)
    import json
    with mp.Pool(2) as p:
        for r,res,dt in p.imap_unordered(run,range(M)):
            print(json.dumps([M,r,res,dt]),flush=True)

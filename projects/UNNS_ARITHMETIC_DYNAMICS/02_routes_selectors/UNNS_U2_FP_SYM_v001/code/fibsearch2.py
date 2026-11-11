"""Lucas-factorised vocabulary search: labels are forms in (a,b)=(F_{h-1},F_h), h=floor(k/2)."""
import sys, time, itertools, json
from math import isqrt
from fibparam import F, nbrs_factory
def atoms(pts_ab):
    # atom name -> (u,v) meaning u*a+v*b
    return {"a":(1,0),"b":(0,1),"c":(1,1),"Lh":(2,1),"Lh1":(1,3),"Lhm":(-1,2),"Fh2":(1,2),"Fh3":(2,3)}
def vocab2(pts_ab, pts_xy, maxprod=True):
    J=len(pts_ab); E={}
    def put(vals,name):
        v=tuple(vals)
        if any(t<=0 for t in v): return
        if v not in E: E[v]=name
    for c in range(1,13): put([c]*J,str(c))
    # linear forms
    for u in range(-3,4):
        for v in range(-3,4):
            for w in range(-2,3):
                if u==0 and v==0: continue
                for d in (1,2,3,4,5,6,8,12):
                    vals=[]
                    for (a,b) in pts_ab:
                        n=u*a+v*b+w
                        if n<=0 or n%d: vals=None;break
                        vals.append(n//d)
                    if vals: put(vals,f"({u}a{v:+d}b{w:+d})/{d}")
    # (x,y) forms of old vocabulary
    for u in range(-3,4):
        for v in range(-3,4):
            for w in range(-2,3):
                if u==0 and v==0: continue
                for d in (1,2,3,4,6,8,12,24):
                    vals=[]
                    for (x,y) in pts_xy:
                        n=u*x+v*y+w
                        if n<=0 or n%d: vals=None;break
                        vals.append(n//d)
                    if vals: put(vals,f"({u}x{v:+d}y{w:+d})/{d}")
    # products of atoms (possibly +-1 shifted) with small constants
    A=atoms(pts_ab)
    def aval(nm,sh=0):
        u,v=A[nm]; return [u*a+v*b+sh for (a,b) in pts_ab]
    items=[]
    for nm in A:
        for sh in (0,-1,1):
            vv=aval(nm,sh)
            if all(t>0 for t in vv): items.append((tuple(vv),nm+("" if sh==0 else f"{sh:+d}")))
    for (u,su),(w,sw) in itertools.combinations_with_replacement(items,2):
        for cst in (1,2,3,4,5):
            put([cst*p*q for p,q in zip(u,w)],f"[{cst}*{su}*{sw}]")
    return E
def search2(P,r,K=7,J=3,node_cap=120000,tlimit=300,h0=4):
    ks=[r+P*j for j in range(h0,h0+J)]
    pts_xy=[(F[k],F[k+1]) for k in ks]
    pts_ab=[(F[k//2-1],F[k//2]) for k in ks]
    E=vocab2(pts_ab,pts_xy); nb=nbrs_factory(E,J); t0=time.time()
    A=tuple(x for x,y in pts_xy); B=tuple(y for x,y in pts_xy)
    da={A:0};pa={A:None};fa=[A];db={B:0};pb={B:None};fb=[B];ra=rb=0
    def grow(front,dist,par,d):
        nxt=[]
        for S in front:
            if time.time()-t0>tlimit: return nxt,True
            for nv,lab in nb(S).items():
                if nv not in dist:
                    dist[nv]=d;par[nv]=(S,lab);nxt.append(nv)
                    if len(dist)>node_cap: return nxt,True
        return nxt,False
    for it in range(K):
        if len(da)<=len(db): fa,cap=grow(fa,da,pa,ra+1);ra+=1
        else: fb,cap=grow(fb,db,pb,rb+1);rb+=1
        small,large=(da,db) if len(da)<len(db) else (db,da)
        hits=[v for v in small if v in large]
        if hits:
            v=min(hits,key=lambda z:da.get(z,99)+db.get(z,99))
            def chain(par,v):
                o=[]
                while par[v] is not None: p,l=par[v];o.append(l);v=p
                return o[::-1]
            f=chain(pa,v);g=chain(pb,v);g=[("-" if l[0]=="+" else "+",l[1]) for l in reversed(g)]
            return dict(P=P,r=r,length=da[v]+db[v],steps=f+g,nf=len(f),vocab=len(E))
        if cap: return dict(P=P,r=r,length=None,status="cap/time",sizes=(len(da),len(db)),vocab=len(E))
    return dict(P=P,r=r,length=None,status="none",vocab=len(E),sizes=(len(da),len(db)))
if __name__=="__main__":
    P,r,K=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
    t=time.time();res=search2(P,r,K);res["sec"]=round(time.time()-t,1);print(json.dumps(res),flush=True)

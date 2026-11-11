import sys,json,time,re
import fibsearch2
from fibsearch2 import *
from fibparam import F, nbrs_factory
from fibresolve import run
def small_vocab(E):
    out={}
    for v,nm in E.items():
        if nm.startswith("["): out[v]=nm; continue
        if re.fullmatch(r"\d+",nm): out[v]=nm; continue
        m=re.fullmatch(r"\((-?\d+)[ax]([+-]\d+)[by]([+-]\d+)\)/(\d+)",nm)
        if m:
            u,w_,c,d=map(int,m.groups())
            if abs(u)<=2 and abs(w_)<=2 and abs(c)<=1 and d in (1,2,4): out[v]=nm
    return out
def search3(P,r,K,J=3,node_cap=4000000,tlimit=3400,h0=4):
    ks=[r+P*j for j in range(h0,h0+J)]
    pts_xy=[(F[k],F[k+1]) for k in ks]; pts_ab=[(F[k//2-1],F[k//2]) for k in ks]
    E=small_vocab(vocab2(pts_ab,pts_xy)); nb=nbrs_factory(E,J); t0=time.time()
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
        print("level",it,len(da),len(db),flush=True)
        if cap: return dict(P=P,r=r,length=None,status="cap/time",sizes=(len(da),len(db)),vocab=len(E))
    return dict(P=P,r=r,length=None,status="none",vocab=len(E),sizes=(len(da),len(db)))
if __name__=="__main__":
    P,K,r=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
    t=time.time(); res=search3(P,r,K)
    if res.get("length"):
        ok,s=run(P,r,res["steps"],res["nf"]); res["validated"]=bool(ok is True)
    res["sec"]=round(time.time()-t,1); print(json.dumps(res),flush=True)

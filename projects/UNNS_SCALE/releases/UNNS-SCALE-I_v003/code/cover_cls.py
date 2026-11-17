import sys, json, time
from cover2 import *
def run(B,K,M,r,max_M,budget,cap=300000):
    t0=time.time(); todo=[(M,r)]; done=[]; unres=[]
    with Pool(2) as pool:
        while todo and time.time()-t0<budget:
            batch,todo=todo[:64],todo[64:]
            for st,M_,r_,d in pool.map(work,[(B,m,rr,K,cap) for m,rr in batch]):
                if st=="ok": done.append(d)
                else:
                    p=next_split(M_,max_M)
                    if p is None: unres.append((M_,r_))
                    else: todo+=[(M_*p,r_+M_*i) for i in range(p)]
    return done,unres,todo
if __name__=="__main__":
    B,K,M,r,maxM,bud=map(int,sys.argv[1:7])
    d,u,t=run(B,K,M,r,maxM,bud)
    from fractions import Fraction
    print(len(d),len(u),len(t),[ (x["M"],x["r"],x["length"],x["t0"]) for x in d][:20], u[:10]); json.dump({"done":d,"unresolved":u,"pending":t}, open(f"/tmp/cls_{B}_{K}_{M}_{r}.json","w"))

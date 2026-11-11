import sys,json,time
import fibsearch2
from fibresolve import run
P=int(sys.argv[1]);K=int(sys.argv[2]);rs=[int(t) for t in sys.argv[3].split(",")]
for r in rs:
    t=time.time()
    res=fibsearch2.search2(P,r,K,node_cap=600000,tlimit=1500)
    if res.get("length"):
        ok,s=run(P,r,res["steps"],res["nf"]); res["validated"]=bool(ok is True); res["nvals"]=len(s) if ok is True else None
    res["sec"]=round(time.time()-t,1)
    print(json.dumps(res),flush=True)

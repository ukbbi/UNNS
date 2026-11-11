import json,sys
from fibcert3 import certify_class
lines=[json.loads(l) for f in sys.argv[2:] for l in open(f) if l.startswith('{')]
out=[]
for res in lines:
    if not res.get("length"): print("no path for r=",res["r"]); continue
    o=certify_class(12,res["r"],[tuple(s) for s in res["steps"]],res["nf"]); out.append(o)
    print({k:v for k,v in o.items() if k not in("labels","searchnames")},flush=True)
json.dump(out,open(sys.argv[1],'w'),indent=1)

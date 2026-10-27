"""v009 Programme A falsification: exact check conv(F)\\U = int T1 u int T2 for structured s (large partial quotients, composite d) in a range beyond v008's d<=72.
usage: hollow_attack9.py PART NPARTS OUT.json"""
import os,sys,json,time
HERE=os.path.dirname(os.path.abspath(__file__))
for d_ in ('geometry','topology','frozen','theory'): sys.path.insert(0,os.path.join(HERE,'..',d_))
from math import gcd
import hollow_check as HC

def cf(a,b):
    q=[]
    while b: q.append(a//b); a,b=b,a%b
    return q
def pairs(d):
    S=set()
    for s in list(range(2,7))+[d-2,d-3,d-4,(d-1)//2,(d+1)//2,(d-1)//3,(d+1)//3,d//2-1,d//2+1]:
        S.add(s)
    S2=set()
    for s in S:
        if 1<s<d-1 and gcd(s,d)==1: S2.add(s); S2.add(pow(s,-1,d))
    # large partial quotient: s ~ d/k for k in 5..9 neighbours
    for k in range(5,10):
        for e in (-1,0,1):
            s=d//k+e
            if 1<s<d-1 and gcd(s,d)==1: S2.add(s); S2.add(pow(s,-1,d))
    return sorted(S2)
part,nparts,out=int(sys.argv[1]),int(sys.argv[2]),sys.argv[3]
ds=[d for d in range(73,111)]
mine=[d for i,d in enumerate(ds) if i%nparts==part]
rows=[];bad=[];t0=time.time()
for d in mine:
    for s in pairs(d):
        ok,tot,inT=HC.check(d,s)
        rows.append({'d':d,'s':s,'cf':cf(d,s),'maxpq':max(cf(d,s)),'exact':bool(ok)})
        if not ok: bad.append([d,s]); print('COUNTEREXAMPLE?',d,s,tot,inT,flush=True)
    open(out+'.progress','a').write('%d done %.0fs viol=%d\n'%(d,time.time()-t0,len(bad)))
json.dump({'range':[73,110],'pairs':len(rows),'violations':bad,'max_partial_quotient':max(r['maxpq'] for r in rows),'rows':rows,'seconds':round(time.time()-t0,1)},open(out,'w'))
print(len(rows),bad)

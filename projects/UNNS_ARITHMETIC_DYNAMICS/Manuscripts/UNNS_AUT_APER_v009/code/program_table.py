import json, sys, csv
import os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','inherited','audit_code')); sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from paths import *
from spec import ORDER, DELTA
from cert import fit_tokens
D=json.load(open(INH+'/concrete_itineraries.json'))
def net(word):
    v=[0,0,0,0]
    for m in word:
        for c in range(4): v[c]+=DELTA[ORDER[m]][c]
    return v
def program(a,rho):
    toks=fit_tokens(a,rho,D); z0=50000+rho
    st=[(a,0),(0,0),(z0,98),(0,0)]   # c0 + c1 t
    rows=[]; ntot=0
    for t in toks:
        if t[0]=='P': word=(t[1],); c,s=1,0
        else: word=t[1]; c,s=t[2],t[3]
        nv=net(word)
        nt=sum(4+m+1 for m in word); ntot+=nt
        rows.append(dict(word=[ORDER[m] for m in word],c=c,s=s,before=list(st),nobl=nt))
        st=[(st[i][0]+nv[i]*c, st[i][1]+nv[i]*s) for i in range(4)]
    return rows,st,ntot
if __name__=='__main__':
    rows,fin,nt=program(0,0)
    print('ntests',nt,'final',fin)
    for r in rows: print(r['word'] if len(r['word'])<6 else ('W%d'%len(r['word'])),r['c'],r['s'],r['before'],r['nobl'])
    # supplementary csv: all 196 programs in compact form
    out=[]
    for a in (0,1):
        for rho in range(98):
            rows,fin,nt=program(a,rho)
            items=[]
            for r in rows:
                w='-'.join(map(str,r['word']))
                items.append(f"[{w}]^({r['c']}+{r['s']}t)")
            out.append(dict(a=a,rho=rho,n_items=len(rows),n_obligations=nt,final_v2=fin[0][0],final_v5_const=fin[2][0],final_v5_slope=fin[2][1],program=' '.join(items)))
    w=csv.DictWriter(open(OUTD+'/programs_196.csv','w',newline=''),fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
    print('written',len(out),'total obligations',sum(o['n_obligations'] for o in out))

"""Verify the exchange-rate balance identity on all 196 certified round programs.
Reads the audit certificate programs (token lists fitted at t=0..7) and the audit spec.
For each family (a,rho): decompose the round at t=0 into prefix / W45^k1 / connector / W11^k2 / tail / 4^k3,
compute residues, and check
   49 z' = 2869 z + delta,  delta = 2820 (P5' - e1) + 49 (P5 + P2 + a - a' + 19 g7)
and the congruence delta = -27 r (mod 49).  Also checks block net vectors and slope arithmetic."""
import json, sys, csv
import os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','inherited','audit_code')); sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from paths import *
from spec import ORDER, DELTA
D=json.load(open(INH+'/concrete_itineraries.json'))
def net(word):
    v=[0,0,0,0]
    for m in word:
        for c in range(4): v[c]+=DELTA[ORDER[m]][c]
    return v
out=[]; allok=True
for a in (0,1):
  for rho in range(98):
    tk=D[f'{a},{rho},0']['tokens']; z=50000+rho
    v=[a,0,z,0]; phase=0; ev=None
    P=[0,0,0,0]; # net of all plain/short items excluding the three big blocks
    blocks=[]
    for t in tk:
        if t[0]=='P':
            d=DELTA[ORDER[t[1]]]; 
            for c in range(4): v[c]+=d[c]; P[c]+=d[c]
        else:
            word=t[2]; k=t[1]
            if len(word)==45 or len(word)==11 or (len(word)==1 and k>1000):
                nv=net(word)
                blocks.append((len(word),k,tuple(v)))
                for c in range(4): v[c]+=k*nv[c]
                if len(word)==45: e1=v[2]; v45=tuple(v)
            else:
                nv=net(word)
                for c in range(4): v[c]+=k*nv[c]; P[c]+=k*nv[c]
    assert [b[0] for b in blocks]==[45,11,1], (a,rho,[b[0] for b in blocks])
    k1,k2,k3=[b[1] for b in blocks]
    ap=v[0]; zp=v[2]; assert v[1]==0 and v[3]==0
    # identity: prefix net in v5 BEFORE the W45 block (P5pre) ; bookkeeping using the block counts of THIS tokenisation
    # direct check of balance relations
    ok = True
    # exact linear relations from net vectors (counts as tokenised, which fix the boundary convention)
    # v7: 0 = P7 + 151 k1 - 2 k2 ; v2: ap = a + P2 + 38 k2 - 2 k3 ; v5: zp = z + P5 - 49 k1 + 2 k3
    ok &= (0==P[3]+151*k1-2*k2)
    ok &= (ap==a+P[0]+38*k2-2*k3)
    ok &= (zp==z+P[2]-49*k1+2*k3)
    ok &= (P[1]==0)
    delta=49*zp-2869*z
    # closed form: zp = z + 2820 k1 + P5 + 19*g7 + P2 + a - ap   with g7=P7
    ok &= (zp==z+2820*k1+P[2]+19*P[3]+P[0]+a-ap)
    # 49 k1 = z + Q5 - e1 where Q5 = v5 before the W45 block minus z
    pre=blocks[0][2]; Q5=pre[2]-z
    ok &= (49*k1==z+Q5-e1)
    ok &= (delta==2820*(Q5-e1)+49*(P[2]+P[0]+a-ap+19*P[3]))
    ok &= ((delta+27*(z%49))%49==0)
    allok&=ok
    out.append(dict(a=a,rho=rho,r=z%49,k1=k1,k2=k2,k3=k3,e1=e1,Q5=Q5,P2=P[0],P5=P[2],P7=P[3],a_next=ap,delta=delta,ok=ok))
print('families',len(out),'all ok',allok)
print('e1 range',min(o['e1'] for o in out),max(o['e1'] for o in out),'P7 range',min(o['P7'] for o in out),max(o['P7'] for o in out))
print('Q5 range',min(o['Q5'] for o in out),max(o['Q5'] for o in out))
w=csv.DictWriter(open(OUTD+'/balance_identity_196.csv','w',newline=''),fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)

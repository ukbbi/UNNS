"""v009 Programme B falsification: every nonexceptional small box Q=(d+u,d+v), 0<=u,v<d, (u,v)!=(0,0), every unit s, d in [DMIN,DMAX]:
test the cap statement C_Q = H_Q \\ H_0 subset U_Q  (G9-CAP) and the stronger full statement H_Q subset U_Q.  Exact rational polygon arithmetic (v005 routine); H_0 = conv F_(d,d).
A cap failure = positive area of uncovered region outside H_0, written with the exact polygon.   usage: cap_attack.py DMIN DMAX OUT.json"""
import os,sys,json,time
HERE=os.path.dirname(os.path.abspath(__file__))
for d_ in ('geometry','topology','frozen','theory'): sys.path.insert(0,os.path.join(HERE,'..',d_))
import coverage as C
from lattice_model import Lat
import small_box as SB
def outside_h0_area2(pieces,d,s):
    H0=C.hull([(i,j) for i in range(d+1) for j in range(d+1) if (i or j) and (j-s*i)%d==0])
    H0=[(C.mpq(x),C.mpq(y)) for x,y in H0]; tot=0
    for p in pieces:
        r=p
        for k in range(len(H0)):
            a,b=H0[k],H0[(k+1)%len(H0)]
            A=-(b[1]-a[1]);B=(b[0]-a[0]);Cc=A*a[0]+B*a[1]
            r=C.clip(r,A,B,Cc)
            if len(r)<3: r=[];break
        inside=abs(C.area2(r)) if len(r)>=3 else 0
        tot+=abs(C.area2(p))-inside
    return tot
dmin,dmax,out=int(sys.argv[1]),int(sys.argv[2]),sys.argv[3]
res={'range':[dmin,dmax],'boxes':0,'full_covered':0,'cap_covered':0,'cap_failures':[],'full_failures':[]}; t0=time.time()
for d in range(dmin,dmax+1):
    for s in SB.units(d):
        for Q in SB.boxes(d):
            res['boxes']+=1; L=Lat(d,d,d,s)
            if C.is_hull_covered(L,Q): res['full_covered']+=1; res['cap_covered']+=1; continue
            pcs=C.uncovered(L,Q); res['full_failures'].append([d,s,list(Q)])
            if outside_h0_area2(pcs,d,s)==0: res['cap_covered']+=1
            else: res['cap_failures'].append({'d':d,'s':s,'Q':list(Q),'leftover':[[(str(x),str(y)) for x,y in p] for p in pcs]}); print('CAP FAILURE',d,s,Q,flush=True)
    open(out+'.progress','a').write('d %d boxes %d t %.0f\n'%(d,res['boxes'],time.time()-t0))
res['seconds']=round(time.time()-t0,1); json.dump(res,open(out,'w'),indent=1); print(res['boxes'],res['full_covered'],res['cap_covered'],len(res['cap_failures']))

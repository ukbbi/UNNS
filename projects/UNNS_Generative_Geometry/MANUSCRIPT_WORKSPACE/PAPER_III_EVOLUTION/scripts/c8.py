import sys, json; sys.path.insert(0,'.')
from eng3 import *
from grav import *
R={}
# classify Gr at each state of the eight-step orbit
def classify(x):
    x=Fr(x); ps,box,gr=region_graver(x); _,F=fibre(x); Fs=set(F)
    pos=[];edge=[];dorm=[]
    for g in gr:
        ng=tuple(-c for c in g)
        if g in Fs or ng in Fs: pos.append(g); continue
        found=False
        for u in F:
            v=tuple(a+b for a,b in zip(u,g))
            if v in Fs: found=True;break
        (edge if found else dorm).append(g)
    return {'ps':ps,'nGr':len(gr),'pos':len(pos),'edge':len(edge),'dormant':len(dorm),'dormant_vecs':dorm}
o=orbit(Fr(3025,3),12)
rows=[]
for n,t in enumerate(o):
    D=Dset(t); c=classify(t) if D or True else None
    rows.append({'n':n,'x':str(t),'b':t.denominator,'D':D,'class':c,'betti':bettiD(D) if D else None,'edges':sorted(edges(D)) if D else []})
R['t8_ext']=rows
for r in rows: print(r['n'],r['x'],r['D'],r['class']['nGr'],r['class']['pos'],r['class']['edge'],r['class']['dormant'],r['betti'])
# (1,-1) i.e. e_5-e_11 membership in Gr at each state (coordinates may differ) -> check 5/11 congruence in lattice
def e5e11(x):
    b=Fr(x).denominator; return (5-11)%b==0
R['e5_e11_in_lattice']=[e5e11(t) for t in o[:9]]
print(R['e5_e11_in_lattice'])
# l=5 tower step 5->6 ; l=29 step 23->24
o5=orbit(Fr(126**2,5),10)
for n in (5,6): print('l5',n,Dset(o5[n]),bettiD(Dset(o5[n])),classify(o5[n])['dormant'])
R['l5_5to6']={'D5':Dset(o5[5]),'D6':Dset(o5[6]),'b5':bettiD(Dset(o5[5])),'b6':bettiD(Dset(o5[6])),'dorm5':classify(o5[5])['dormant'],'dorm6':classify(o5[6])['dormant'],'nGr5':classify(o5[5])['nGr']}
o29=orbit(Fr(1890**2,29),26)
for n in (23,24): print('l29',n,Dset(o29[n]),bettiD(Dset(o29[n])),classify(o29[n])['dormant'])
R['l29_23to24']={'D23':Dset(o29[23]),'D24':Dset(o29[24]),'b23':bettiD(Dset(o29[23])),'b24':bettiD(Dset(o29[24]))}
# R3-T6.3 no dormant on ell=11 tower k=0,1, t=1..10
S11=lambda k: 2**2*3**(3+k)*5**4
nd=[]
for k in (0,1):
    for t in range(1,11):
        c=classify(Fr(t*S11(k)**2,11)); nd.append((k,t,c['dormant']))
R['l11_dormant']=nd; print('l11 dormant total',sum(x[2] for x in nd))
# orbit hits integer 12100
o=orbit(Fr(3025,3),12); R['hit12100']=[(n,str(t),bettiD(Dset(t))) for n,t in enumerate(o) if n>=8]
print(R['hit12100'])
json.dump(R,open('../results/c8.json','w'),default=str)

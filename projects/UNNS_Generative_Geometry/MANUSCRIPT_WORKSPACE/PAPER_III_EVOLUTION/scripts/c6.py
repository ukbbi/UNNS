import sys, json, time; sys.path.insert(0,'.')
from eng3 import *
R={}
# --- ell=29 control
x0=Fr(1890**2,29); o=orbit(x0,75); Dn=[tuple(Dset(t)) for t in o]
ev=[n for n in range(1,len(Dn)) if Dn[n]!=Dn[n-1]]
R['l29']={'events':ev[:8],'x35_over_x0':str(o[35]/o[0]),'x70_over_x35':str(o[70]/o[35]),'new_at_first':[d for d in Dn[ev[0]] if d not in Dn[ev[0]-1]],
          'G':sorted({LG(d)[1] for d in Dn if d})}
print(R['l29'])
# --- towers: scaling x_{n+8}=9x_n (11), x_{n+3}=4x_n (5)
S11=lambda k: 2**2*3**(3+k)*5**4; S5=lambda k: 126*2**k
o11=orbit(Fr(S11(0)**2,11),8*6); ok11=all(o11[n+8]==9*o11[n] for n in range(len(o11)-8))
ok11b=all(o11[8*k+j]==Fr((j+1)*S11(k)**2,11) for k in range(6) for j in range(8))
o5=orbit(Fr(S5(0)**2,5),3*8); ok5=all(o5[n+3]==4*o5[n] for n in range(len(o5)-3))
ok5b=all(o5[3*k+j]==Fr((j+1)*S5(k)**2,5) for k in range(8) for j in range(3))
R['tower_scaling']={'g11':ok11 and ok11b,'g5':ok5 and ok5b}; print(R['tower_scaling'])
# --- R3-T7: ratio matches R(N)=(N+1)^2/N on iterates, event level
def match(o, lim):
    Dn=[tuple(Dset(t)) for t in o]
    ch=[0]
    for n in range(1,len(Dn)): ch.append(ch[-1]+(Dn[n]!=Dn[n-1]))
    res={}
    for n in range(len(o)):
        for m in range(n+1,len(o)):
            r=o[m]/o[n]
            # r = (N+1)^2/N with N integer: N = denominator of r, check
            N=r.denominator
            if Fr((N+1)**2,N)==r:
                nd=ch[m]-ch[n]
                res.setdefault(N,[]).append((n,m,nd))
    return res
m11=match(orbit(Fr(S11(0)**2,11),40),40); m5=match(orbit(Fr(S5(0)**2,5),18),18)
def summ(m):
    out={}
    for N,l in sorted(m.items()):
        out[N]={'pairs':len(l),'dchanges':sorted({x[2] for x in l}),'ex':l[:4]}
    return out
R['R3T7']={'g11':summ(m11),'g5':summ(m5)}
for k,v in R['R3T7'].items(): print(k,{N:(d['pairs'],d['dchanges']) for N,d in v.items()})
# --- A5-T2.4 family closed form
def fam_time(P,ell,pi,q):
    N=P-1; m=N//ell; d=pi*q; r=N//gcd(d-1,N); v=0; t=N
    while t%q==0: t//=q; v+=1
    e=q**(2+v); M=lcm(r,e); return (m//M+1)*M
chk=[]
for (ell,ps,q) in [(3,[5,11],17),(7,[23,37,79],11),(5,[7,17,37,47],3),(3,[5,11],2),(7,[11,53,67],2)]:
    P=1
    for p in ps: P*=p
    N=P-1; m=N//ell
    for p in ps:
        u=fam_time(P,ell,p,q); d=p*q
        # direct membership: virtual point x_u = P^2 u/N ; d in D ? first u>m with membership
        first=None
        for uu in range(m+1, u+3*lcm(1,1)+1):
            if d in Dset(Fr(P*P*uu,N)): first=uu; break
            if uu>u+1: break
        chk.append({'ell':ell,'ps':ps,'q':q,'p':p,'pred_u':u,'direct':first,'ok':first==u})
R['A5T24']={'n':len(chk),'ok':sum(c['ok'] for c in chk),'rows':chk}; print('A5T24',R['A5T24']['n'],R['A5T24']['ok'])
# --- reachability: exact brute-force reached targets
def reach(ell,ps,q,maxn=3000):
    P=1
    for p in ps: P*=p
    x=Fr(P*P,ell); y=Fr((P*q)**2,ell); Dy=set(Dset(y)); cur=x
    for n in range(1,maxn+1):
        cur=C(cur)
        if cur is None: return ('Dempty',n)
        Dc=set(Dset(cur))
        if not Dc<=Dy: return ('BLOCKED',n,sorted(Dc-Dy))
        if cur==y: return ('REACHED',n)
        if cur>y: return ('OVERSHOT',n)
    return ('CAP',maxn)
tests=[(3,[5,11],2),(3,[5,11],17),(3,[29,647],11),(3,[47,1613],17),(5,[89,1709],19),(7,[11,53,67],2)]
rr=[]
for ell,ps,q in tests:
    t0=time.time(); res=reach(ell,ps,q); rr.append({'ell':ell,'ps':ps,'q':q,'res':res}); print(ell,ps,q,res,round(time.time()-t0,1),flush=True)
R['reach']=rr
json.dump(R,open('../results/c6.json','w'),default=str)

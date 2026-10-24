#!/usr/bin/env python3
"""Exact-integer verification for Volume I. Runs the additional checks of this file, then the base checks in checks_base.py.
Checks test selected exact instances; they complement, and do not replace, the proofs in the text."""
import json, runpy
from fractions import Fraction as Fr
from math import gcd, isqrt
from pathlib import Path
lcm=lambda a,b:a*b//gcd(a,b)
def D(t): return [d for d in range(2,isqrt(t)+1) if t%(d*d)==0]
def pred(t): return sorted({t//d**2*(d-1) for d in D(t)})
def succ(m): return {m*(N+1)**2//N for N in range(1,m+1) if m%N==0}
def desc(s,lim):
    seen={s};st=[s]
    while st:
        for t in succ(st.pop()):
            if t<=lim and t not in seen: seen.add(t);st.append(t)
    return seen
def anc(t,memo={}):
    if t not in memo:
        s={t}
        for p in pred(t): s|=anc(p)
        memo[t]=s
    return memo[t]
out=[]
def chk(n,ok): out.append({'id':n,'pass':bool(ok)})
chk('desc_1_le_100',desc(1,100)=={1,4,16,18,25,64,72,81,96,100})
chk('desc_2_le_100',desc(2,100)=={2,8,9,32,36,48,50,81,100})
chk('pred_32_300_tree',pred(32)==[6,8] and pred(300)==[27,48,75] and pred(75)==[12] and pred(48)==[9,12] and pred(27)==[6] and pred(12)==[3] and pred(9)==[2] and not pred(2) and not pred(3) and not pred(6))
chk('anc_32',anc(32)=={2,6,8,32}); chk('anc_300',anc(300)=={2,3,6,9,12,27,48,75,300})
chk('common_anc_2_6',anc(32)&anc(300)=={2,6} and 2 not in anc(6) and 6 not in anc(2) and 6/2<4)
# T24 case (iii): any D={q,q^2,e}-shaped triple has three distinct weights (scan, b>=2)
bad=0;n=0
for b in range(2,14):
    for s in range(2,1500):
        Dd=[d for d in range(2,s+1) if s%d==0 and d%b==1]
        if len(Dd)!=3: continue
        comp=[(x,y) for x in Dd for y in Dd if x<y and y%x==0]
        if len(comp)==1:
            n+=1
            w=[Fr(gcd(x-1,y-1),lcm(x,y)**2) for i,x in enumerate(Dd) for y in Dd[i+1:]]
            bad+= len(set(w))<3
chk(f'T24_case_iii_rigid_scan_{n}_cases',n>0 and bad==0)
# lattice-intersection lemma, brute force
ok=True
for p in range(1,13):
  for q in range(1,13):
    if gcd(p,q)!=1: continue
    for p2 in range(1,13):
      for q2 in range(1,13):
        if gcd(p2,q2)!=1: continue
        w=Fr(lcm(p,p2),gcd(q,q2)); u=Fr(p,q); v=Fr(p2,q2)
        mem=lambda z,g:(z/g).denominator==1
        for k in range(1,40):
            z=Fr(k,1)*w/ (1)  # multiples of w must lie in both
            if not(mem(z,u) and mem(z,v)): ok=False
        # minimality: no smaller positive element of both lattices among j/(q*q2)
        for j in range(1,int(w*q*q2)):
            z=Fr(j,q*q2)
            if mem(z,u) and mem(z,v): ok=False
chk('lattice_lcm_lemma_brute',ok)
# Example 72 table
rows={d:(d-1,72//d**2*(d-1),Fr(d*d,d-1)) for d in D(72)}
chk('anatomy72_table',rows=={2:(1,18,Fr(4)),3:(2,16,Fr(9,2)),6:(5,10,Fr(36,5))} and all(Fr(m*(n+1)**2,n)==72 for n,m,_ in rows.values()))
x=72; Dl=Fr(36)
chk('anatomy72_common_futures',all(((c-72)/r[2]).denominator==1 for c in (72,108,144,180) for r in rows.values()) and not any(all(((c-72)/r[2]).denominator==1 for r in rows.values()) for c in range(73,108)))
chk('anatomy72_values_between_common_futures',[int(Dl/r[2]) if (Dl/r[2]).denominator==1 else (Dl/r[2]) for r in rows.values()]==[9,8,5])
# Prop refine (F.T5): d*q in D(a/b) iff q = 1 mod b, over a scan
bad=0;n=0
for b in range(1,8):
    for a in range(1,600):
        if gcd(a,b)!=1: continue
        Dab=[d for d in range(2,isqrt(a)+1) if a%(d*d)==0 and d%b==1%b]
        for d in Dab:
            k=a//d**2
            for q in range(2,isqrt(k)+1 if k>=4 else 1):
                if k%(q*q): continue
                n+=1
                inD=(d*q)%b==1%b and a%(d*q*d*q)==0
                bad+= inD!=(q%b==1%b)
chk(f'T5_refinement_scan_{n}_cases',n>0 and bad==0)
# T10: sigma_N strictly increasing, step reduced with denominator N, injectivity of r->(v(r),v(Fr))
sig=[Fr((N+1)**2,N) for N in range(1,500)]
chk('T10_sigma_strictly_increasing_den_N',all(a<b for a,b in zip(sig,sig[1:])) and all(s.denominator==N for N,s in enumerate(sig,1)))
img={}; inj=True
for N in range(1,60):
    for M in range(1,60):
        v=Fr(M*(N+1)**2,N); key=(v,v+Fr((N+1)**2,N))
        if key in img: inj=False
        img[key]=(M,N)
chk('T10_injectivity_box',inj)
# Prop joinintr
chk('joinintr_values',lcm(18,8)==72 and lcm(2,3)==6 and 72*36==2592 and D(2592)==[2,3,4,6,9,12,18,36] and pred(2592)==[70,136,198,256,360,486,576,648])
a=anc(2592); chk('joinintr_ancestors',len(a)==42 and 16 in a and 72 not in a and 18 not in a and 10 not in a)
# Example two-joins
Jj=lambda r,s:(lcm(r[0],s[0]),lcm(r[1],s[1]))
def Jr(r,s):
    L=lcm(r[1],s[1]); V=lcm(r[0]*r[1]**2,s[0]*s[1]**2); return (V//L**2,L)
r,s=(18,2),(8,3)
chk('two_joins_example',Jj(r,s)==(72,6) and Jr(r,s)==(2,6) and 72*36==2592 and 2*36==72)
# decidability corollary: backward search restricted to [m,t] agrees with full ancestor set
def reach(m,t):
    if m==t: return True
    return any(p>=m and reach(m,p) for p in pred(t))
ok=all(reach(m,t)==(m in anc(t)) for t in range(1,400) for m in range(1,t+1))
chk('decide_corollary_t_lt_400',ok)
fails=sum(not x['pass'] for x in out)
Path(__file__).with_name('volume_i_additional_checks.json').write_text(json.dumps({'checks':out,'fail_count':fails},indent=1))
print(f"additional checks: {len(out)-fails} PASS; {fails} FAIL")
for x in out: print(('PASS ' if x['pass'] else 'FAIL ')+x['id'])
runpy.run_path(str(Path(__file__).with_name('checks_base.py')),run_name='__main__')
raise SystemExit(1 if fails else 0)

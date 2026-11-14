"""Check the register-cycle statements used in Section 'Mechanism'.
(1) top-three subsystem {2400,3,35} acts on (v2,v3) by F; all orbits on a large box reach one 45-cycle;
    every move shifts (v2 mod 9, v3 mod 5) by (4,4).
(2) closed-form generator of W45 = rotation u -> u+2 (mod 9) on representatives in [4,12].
(3) {3,35,4} regime with v5-register: cycle of length 11 and its net vector.
(4) 4-run: terminates at v2 in {0,1}."""
import sys
import os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','inherited','audit_code')); sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from paths import *
from spec import ORDER, DELTA, vec
D={N:DELTA[N] for N in ORDER}
# (1)
def F(s):
    v2,v3=s
    if v3>=1 and v2>=5: return (v2-5,v3-1),2400
    if v3>=1: return (v2+4,v3-1),3
    return (v2+4,v3+4),35
for N in (2400,3,35): assert (D[N][0]%9,D[N][1]%5)==(4,4),(N,D[N])
cycles=set(); 
for v2 in range(0,400):
  for v3 in range(0,12):
    s=(v2,v3); seen={}
    i=0
    while s not in seen:
        seen[s]=i; s,_=F(s); i+=1
    # s is on cycle; extract
    cyc=[s]; t,_=F(s)
    while t!=s: cyc.append(t); t,_=F(t)
    cycles.add(frozenset(cyc))
print('distinct cycles',len(cycles),'lengths',[len(c) for c in cycles])
cyc=list(cycles)[0]
s=min(cyc); word=[]
for _ in range(45):
    s,m=F(s); word.append(m)
from collections import Counter
print('counts',Counter(word)); net=[0,0,0,0]
for m in word:
    for c in range(4): net[c]+=D[m][c]
print('net',net)
# rotation generator
def gen(u0, n_blocks=9):
    w=[]; u=u0
    for _ in range(n_blocks):
        x=u
        for i in range(4):
            if x>=5: w.append(2400); x-=5
            else: w.append(3); x+=4
        w.append(35); u=x+4
    return w,u
for u0 in range(4,13):
    w,u=gen(u0,1); 
    assert (u-u0)%9==2 and 4<=u<=12, (u0,u)
    w9,u9=gen(u0); assert u9==u0
W45_audit=[2400,2400,3,2400,35,2400,3,3,2400,35,2400,3,2400,3,35,2400,3,2400,3,35,2400,2400,3,2400,35,3,2400,3,2400,35,2400,3,2400,3,35,2400,3,2400,3,35,2400,2400,3,3,35]
w,u=gen(12)
print('gen(12)==W45 as printed:', w==W45_audit, 'end u',u)
assert w==W45_audit
# (3) W11 regime as an automaton on (v3,v5) with v2,v7 large: rules 3 (v3>=1, and 2400 disabled i.e. v5<=1), 35 (v5>=1), 4
def G(s):
    v3,v5=s
    if v3>=1: return (v3-1,v5),3          # 2400 disabled needs v5<=1: checked below
    if v5>=1: return (v3+4,v5-1),35
    return (v3,v5+2),4
s=(0,0); seq=[]
for _ in range(11):
    assert not(s[0]>=1 and s[1]>=2)       # 2400 would pre-empt a '3' step
    s,m=G(s); seq.append(m)
print('W11 regime cycle word',seq,'returns to',s)
print('W11 order (3,3,3,3,35,3,3,3,3,4,35) rotation?', ''.join(map(str,seq*2)).find(''.join(map(str,[3,3,3,3,35,3,3,3,3,4,35])))>=0)
n=[0,0,0,0]
for m in seq:
    for c in range(4): n[c]+=D[m][c]
print('W11 net',n)
# (4) 4-run
print('Delta4',D[4], 'exchange gain', 151*19/49, 2869/49)

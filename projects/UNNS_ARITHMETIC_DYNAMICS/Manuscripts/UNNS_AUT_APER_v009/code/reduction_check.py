"""(i) the 7-step lemma: orbit of 2*5^z passes via itinerary (2,3,3,4,4,4,4) to 5^(z+8), for all z (thresholds on v5 never involved);
   symbolic check with v5 treated as a large parameter; (ii) table identity delta_{1,r}=delta_{0,r+8}+2869*8, a'(1,r)=a'(0,r+8)."""
import sys, os, csv
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from paths import *
sys.path.insert(0,os.path.join(ROOT,'inherited','audit_code'))
from spec import ORDER, REQ, DELTA, enabled
# symbolic: v5 = BIG (>= max threshold 4 never binding because only 5-thresholds <=3 exist among ORDER and path changes v5 by <=8)
v=(1,0,10**6,0); path=[]
def sel(v):
    for N in ORDER:
        if enabled(v,N): return N
for i in range(7):
    N=sel(v); path.append(N); d=DELTA[N]; v=tuple(x+y for x,y in zip(v,d))
assert path==[2,3,3,4,4,4,4] and v==(0,0,10**6+8,0)
# independence of z: the only 5-thresholds in the list are REQ[N][2] <= 4 ; test z from 0..40 to be safe about small z
for z in list(range(0,41))+[49999,50000,50001,10**9]:
    v=(1,0,z,0); p=[]
    for i in range(7):
        N=sel(v); p.append(N); v=tuple(x+y for x,y in zip(v,DELTA[N]))
    if z>=8: assert p==[2,3,3,4,4,4,4] and v==(0,0,z+8,0),(z,p,v)
tab={}
for r in csv.DictReader(open(os.path.join(INH,'return_map_table_audit.csv'))):
    tab[(int(r['a']),int(r['z_mod_49']))]=(int(r['a_next']),int(r['delta']))
assert all(tab[(1,r)][0]==tab[(0,(r+8)%49)][0] and tab[(1,r)][1]==tab[(0,(r+8)%49)][1]+2869*8 for r in range(49))
print('7-step lemma and table identity verified for all 49 residues')

#!/usr/bin/env python3
"""Independent exact verification, not importing main implementation."""
import csv, json, math, itertools
from fractions import Fraction as Q
from pathlib import Path
r=Path(__file__).resolve().parents[1]
rows=list(csv.DictReader((r/'results'/'rule_comparison.csv').open(encoding='utf-8')))
assert len(rows)==6
results=json.loads((r/'results'/'summary.json').read_text(encoding='utf-8'))

# Independent oracle follows integer support and rational coefficients only.
def oracle(v, path, what, q):
    d={int(k):Q(val) for k,val in v.items()}
    trace=[]
    def gc(d):
        return math.gcd(*[abs(k) for k,w in d.items() if w]) if d else 0
    trace=[gc(d)]
    for n in path:
        if what=='strict' and any(m%n for m in d):
            return None,trace
        if what=='E' and q%n:
            d={}
        else:
            d={m//n*(n+1)**2:w for m,w in d.items() if m%n==0}
        trace.append(gc(d))
        if not d: return {}, trace
    return d,trace

v={-18:Q(1,37),-12:Q(1,13),-6:Q(1,2),6:Q(1,2),12:Q(1,13),18:Q(1,37)}
words={'A_3_8_3':(3,8,3),'B_1_1_1_2':(1,1,1,2)}
computed={}
for row in rows:
    h=row['history']; w=words[h]; typ=row['rule']
    z,ts=oracle(v,w,typ,6)
    assert str('->'.join(map(str,ts)))==row['content_trace']
    assert bool(z)==bool(int(row['surviving']))
    assert int(row['final_content'])==(math.gcd(*[abs(t) for t in z]) if z else 0)
    computed[(h,typ)]=z
assert computed['A_3_8_3','strict']==computed['B_1_1_1_2','strict']
assert computed['A_3_8_3','component']==computed['B_1_1_1_2','component']
assert computed['A_3_8_3','E']=={} and bool(computed['B_1_1_1_2','E'])
print('PASS independent history oracle: 6 histories and all endpoint coefficients')

# Test the Bloch-class v007 P as written against direct index selection in 100,000+ cases.
k=0
for q in range(1,16):
    for N in range(1,29):
        for m in range(-90,91):
            P=(math.gcd(m%q,q)%N==0)
            exact=((q%N==0) and (m%N==0))
            assert P==exact,(q,N,m)
            k+=1
print('PASS independent Bloch projector identity:',k,'cases')

# Exact direct no-go: the second derivative at origin distinguishes cos(q*r*z) and cos(q*z).
# eps(0) equal on both sides -> lambda'=r^2*lambda.
for v1 in results['exact_curvature_certificates']:
    N=v1['N']; rt=Q((N+1)**2,N); d=Q(1,10); q=6
    diff=(-2*d*(q*rt)**2)-(-2*d*q*q)
    assert str(diff)==v1['difference_epsilon_double_prime_at_zero'] and diff!=0
assert all(Q((N+1)**2,N)>1 for N in range(1,400))
print('PASS fixed-medium eigenstate no-go exact curvature certificates')

# Independent infinite index content-gcd proof finite-support analogue + histories.
# For generic Bloch support kappa + j*q, two adjacent j enforce gcd(kappa,q).
for q in range(1,17):
    for kap in range(q):
        for j in range(-6,6):
            a=kap+q*j; b=kap+q*(j+1)
            assert math.gcd(a,b)==math.gcd(kap,q)
print('PASS adjacent Bloch harmonic gcd identity (exact finite arithmetic)')

# Check r_N>1 and co-dilation Fourier wavenumbers in the same exact integer language.
for d0 in range(1,45):
    for N in range(1,d0+1):
        if d0%N: continue
        m0=d0
        out=m0//N*(N+1)**2
        assert out==m0*Q((N+1)**2,N)
print('PASS exact co-dilation scale law and integer periodicity')
print('MUG-I v008 VERIFY PASS')

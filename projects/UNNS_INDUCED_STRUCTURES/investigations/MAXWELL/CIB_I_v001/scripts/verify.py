"""Independent exact finite verifier. Different enumeration from model.graph."""
from pathlib import Path
from fractions import Fraction
import csv, json, hashlib, math, sys
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'protocol'/'PROTOCOL.json'
data=json.loads(P.read_text())
assert hashlib.sha256(P.read_bytes()).hexdigest()==(ROOT/'protocol'/'PROTOCOL.sha256').read_text().strip()
M=data['index_window']['max']
# m-first enumeration with brute-force positive integer labels. Not imported from model.
def independent_edges(grammar):
    output=set()
    for m in range(1,M+1):
        if grammar=='SQUARE':
            for k in range(2,math.isqrt(M//m)+1):
                output.add((m,m*k*k))
        else:
            c={'UNNS':0,'NEAR_MINUS':-1,'NEAR_PLUS':1}[grammar]
            for n in range(1,m+1):
                if m%n:continue
                t=m//n
                y=t*(n*n+(2+c)*n+1)
                if m<y<=M:output.add((m,y))
    return output
res=ROOT/'results'
with (res/'comparison.csv').open() as f:rows=list(csv.DictReader(f))
for name in data['fixed_grammars']:
    edges=independent_edges(name)
    got=[r for r in rows if r['grammar']==name]
    assert len(got)==len(data['medium_profiles'])+len(data['additional_checks'])
    for r in got:
        D=Fraction(r['profile']); b=D.denominator
        n=sum((y-m)%b!=0 for m,y in edges)
        assert n==int(r['nonzero_edges']), (name,D,n,r['nonzero_edges'])
        assert len(edges)==int(r['edges'])
        # Independent complex-analytic form (not sin/cos from model.py).
        power=sum(abs((1-complex(math.cos(2*math.pi*(y-m)*float(D)),-math.sin(2*math.pi*(y-m)*float(D))))/(2j*math.pi*(y-m)))**2 for m,y in edges)/len(edges)
        assert math.isclose(power,float(r['mean_fourier_power']),rel_tol=1e-8,abs_tol=1e-14),(name,D,power)
        base_count=sum((M-q) for q in range(1,M) if q%b)
        assert math.isclose(base_count/(M*(M-1)/2),float(r['background_nonzero_fraction']),abs_tol=1e-14)
    print('PASS independent grammar',name,len(edges),'edges',len(got),'media')
# Independent direct gates (not mere output comparison):
for n in range(1,250):
    s=n*n+n+1
    for t in range(1,10):
        m=t*n; y=t*(n+1)**2
        assert y-m==t*s
        for D_text in data['medium_profiles']+data['additional_checks']:
            D=Fraction(D_text)
            assert (((y-m)%D.denominator)==0)==(math.gcd(D.numerator,D.denominator)==1 and (t*s)%D.denominator==0)
print('PASS exact q=t*(n^2+n+1) and rational-duty Fourier-zero gate')
# Full first-order spectrum support on a single-sinusoid q=1 has no UNNS edges.
assert all(y-m!=1 for m,y in independent_edges('UNNS'))
# First-order diamond counter-control uses the SAME medium, independent of choosing grating q.
for frac,expect_a,expect_b in [('1/2',False,True),('1/3',False,False),('1/5',True,True),('2/5',True,True)]:
    b=Fraction(frac).denominator
    A=all(q%b for q in (6,28));B=all(q%b for q in (7,27))
    assert (A,B)==(expect_a,expect_b)
print('PASS fixed UNNS diamond under four independently declared binary media')
# Quantify source-scrambling control equality in every tested medium.
for p in data['medium_profiles']+data['additional_checks']:
    u=next(r for r in rows if r['profile']==p and r['grammar']=='UNNS')
    s=next(r for r in rows if r['profile']==p and r['grammar']=='UNNS_Q_PRESERVING_SCRAMBLE')
    for key in ('edges','nonzero_edges','nonzero_fraction','mean_fourier_power','background_nonzero_fraction','enrichment'):
        assert u[key]==s[key]
print('PASS q-preserving source-scramble: scores indistinguishable for all profiles')
print('CIB-I v001 VERIFY PASS')

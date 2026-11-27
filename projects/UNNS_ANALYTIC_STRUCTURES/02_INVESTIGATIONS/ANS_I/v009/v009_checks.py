"""ANS-I v009 checks.  Usage: python3 -B v009_checks.py [factor|zeros|remainder|restricted]
Exact power-series arithmetic and floating-point checks; none of them is a proof of the theorems."""
import sys, os, json, platform
from fractions import Fraction
from math import gcd
import mpmath as mp
mp.mp.dps=30
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(HERE,'results')
def save(name,d):
    d['software']={'python':platform.python_version(),'mpmath':mp.__version__}
    json.dump(d,open(os.path.join(OUT,name),'w'),indent=1); print(json.dumps(d,indent=1))
ORDER=31
def mul(a,b):
    c=[0]*ORDER
    for i,x in enumerate(a):
        if x:
            for j in range(ORDER-i): c[i+j]+=x*b[j]
    return c
def local():                     # 1 - (z^5+z^6)/(1+z^2) as an integer power series
    inv=[0]*ORDER
    for j in range(0,ORDER,2): inv[j]=(-1)**(j//2)
    num=[0]*ORDER; num[5]=num[6]=1
    h=[-x for x in mul(num,inv)]; h[0]+=1; return h
def exponents(nmax):             # c_n with local = prod_n (1-z^n)^(-c_n) + O(z^(nmax+1))
    rest=local(); c={}
    for n in range(1,nmax+1):
        c[n]=rest[n]
        # divide rest by (1-z^n)^(-c_n), i.e. multiply by (1-z^n)^(c_n)
        e=c[n]; term=[0]*ORDER; b=1
        for m in range(0,(ORDER-1)//n+1):
            term[n*m]=(-1)**m*b
            b=b*(e-m)//(m+1)
        rest=mul(rest,term)
        assert rest[n]==0
    return c,rest

def factor():
    c,rest=exponents(10)
    first=next(i for i in range(1,ORDER) if rest[i]); assert first>=11
    c7,rest7=exponents(6); h7=next(i for i in range(1,ORDER) if rest7[i])
    # Euler-product identity of the review: Phi = zeta(4s)/zeta(2s) * prod (1+p^-2s+p^-3s)
    ok=[]
    for x in (Fraction(1,3),Fraction(2,7),Fraction(9,10)):
        lhs=1+x**3/(1+x**2); rhs=(1+x**2+x**3)*(1-x**2)/(1-x**4); ok.append(lhs==rhs)
    beta=mp.findroot(lambda t:t**3-t**2-1,1.46)     # -beta is the real root of 1+z^2+z^3
    m=1/mp.sqrt(beta)
    save('v009_factorisation.json',{'exponents_c_n':c,'first_nonzero_order_after_n<=10':first,
      'first_nonzero_order_after_zeta5_zeta6':h7,'local_identity_exact_at_test_points':ok,
      'modulus_of_nonreal_roots_of_1+z^2+z^3':float(m),'prime_with_p^(-1/10)_equal_to_it_would_be':float(beta**5)})

def zeros():
    c,_=exponents(10); rows=[]
    for j in range(1,31):
        rho=mp.zetazero(j)
        vals={n:float(abs(mp.zeta(n*rho/5))) for n in (2,3,6,7,8,9,10)}
        rows.append({'zero':j,'gamma':float(rho.imag),'abs_zeta(n rho/5)':vals,'min':min(vals.values())})
    save('v009_zeros.json',{'rows':rows,'smallest_value':min(r['min'] for r in rows)})

def factorint(n):
    f={};p=2
    while p*p<=n:
        while n%p==0: f[p]=f.get(p,0)+1;n//=p
        p+=1
    if n>1: f[n]=f.get(n,0)+1
    return f
def jordan(d,s):
    out=mp.mpc(1)
    for p,e in factorint(d).items(): out*=mp.power(p,e*s)-mp.power(p,(e-1)*s)
    return out
def rho_(d):
    r=1
    for p,e in factorint(d).items(): r*=p**((e+1)//2)
    return r
def remainder():
    # size of the second-order remainder of zeta(2s,1+1/d)-zeta(2s) in the strip |Re s|<1/16
    rows=[]
    for s in (mp.mpc('0.05','3'),mp.mpc('-0.05','3'),mp.mpc('0.001','10'),mp.mpc('-0.06','0.4')):
        for d in (2,5,20,100,1000):
            E=mp.zeta(2*s,1+mp.mpf(1)/d)-mp.zeta(2*s)+2*s*mp.zeta(2*s+1)/d
            rows.append({'s':[float(s.real),float(s.imag)],'d':d,'|E| d^2':float(abs(E)*d*d)})
    save('v009_remainder.json',{'rows':rows})
def restricted():
    # finite check of the lower bound used for exact pole order: D | N_1 implies D | K and E <= prod (N+1)^2
    bad=0; total=0
    import itertools
    for w in itertools.product(range(1,25),repeat=3):
        E=K=1
        for N in w:
            g=gcd(E,N); K=N*K//g; E=(N+1)**2*E//g
        bound=1
        for N in w: bound*=(N+1)**2
        total+=1; bad+= (K%w[0]!=0) or E>bound
    save('v009_restricted.json',{'words_tested':total,'violations':bad})
if __name__=='__main__':
    {'factor':factor,'zeros':zeros,'remainder':remainder,'restricted':restricted}[sys.argv[1]]()

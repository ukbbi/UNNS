"""KI-2 driver: exact minimal degree d=[Q(S,N):Q(S)] for every step not covered by KI-1, existence certificate (exact identity),
lower-bound certificate (rank mod p of the evaluation matrices), and the radical-tower (2-group) test for the ten unresolved Fibonacci labels."""
import sys,json,os,collections; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import ki_core as K, ki_degree as D, sympy as sp
from ki_core import m
def is_pow2(n): return n>0 and n&(n-1)==0
def lcm_list(L):
    import math; r=1
    for x in L: r=r*x//math.gcd(r,x)
    return r
def tower_test(fS,primes=(10007,10009,10037,10039),srange=range(2,400)):
    """search a specialization s0 mod p with squarefree reduction of numS(m)-s0*denS(m) whose factor degrees have lcm not a power of 2.
    Then the Galois group of numS-s*denS over Q(s) contains an element of non-2-power order, so it is not a 2-group."""
    n,dd=sp.fraction(fS); deg=sp.Poly(n,m).degree()
    for p in primes:
        for s0 in srange:
            poly=sp.Poly(n-s0*dd,m,modulus=p)
            if poly.degree()<deg: continue
            fl=poly.factor_list()[1]
            if any(e>1 for _,e in fl): continue
            degs=sorted(f.degree() for f,e in fl); L=lcm_list(degs)
            if not is_pow2(L): return dict(prime=p,s0=s0,factor_degrees=degs,order=L)
    return None
def run(one=None):
    k1=json.load(open(os.path.dirname(os.path.abspath(__file__))+"/../data/ki1_identities.json"))
    res={'fibonacci':{},'squares_direct':{},'squares_wrapper':{}}
    au=json.load(open(K.DATA+"/state_audit.json"))['per_step']
    def one_step(famname,key,i,N,S,eps,audit_cat):
        fN=D.to_rational_fn(famname,N,eps); fS=D.to_rational_fn(famname,S,eps)
        dN,dS=D.rf_degree(fN),D.rf_degree(fS); npts=(dN+1)*(dS+1)+30
        mv=[sp.Rational(k,7)+sp.Rational(1,3) for k in range(1,npts+60)]
        pts=D.values(fN,fS,mv)[:npts]; d=D.min_relation_degree(pts,dS,dN)
        cr=D.certify_min_relation(fN,fS,d,dN,dS)
        rec=dict(audit=audit_cat,degN=dN,degS=dS,d=d,exists=cr['exists'],identity_verified=cr.get('identity_verified'),points=cr.get('points_checked'),deg_s=cr.get('deg_s'),nullity=cr.get('nullity'))
        rec['lower_bound_modp']=f"no relation with deg_N<{d} (rank mod 2^61-1)"
        rec['pow2']=is_pow2(d)
        if audit_cat=='unexplained':
            rec['tower']=tower_test(fS)
        return rec
    for r,c in K.load_fib().items():
        R=c['R']
        for i in range(len(c['N'])):
            if k1['fibonacci'][str(r)][i]['kind']!='none': continue
            res['fibonacci'].setdefault(str(r),{})[str(i)]=one_step("fib",r,i,R.expr(c['N'][i]),R.expr(c['S'][i]),c['eps'],au['fibonacci'][str(r)][i]['cat'])
    for r,c in K.load_sq_direct().items():
        for i in range(len(c['N'])):
            if k1['squares_direct'][str(r)][i]['kind']!='none': continue
            res['squares_direct'].setdefault(str(r),{})[str(i)]=one_step("sq",r,i,c['N'][i],c['S'][i],None,au['squares_direct'][str(r)][i]['cat'])
    for nm,c in K.load_sq_wrapper().items():
        for i in range(len(c['N'])):
            if k1['squares_wrapper'][nm][i]['kind']!='none': continue
            res['squares_wrapper'].setdefault(nm,{})[str(i)]=one_step("sq",nm,i,c['N'][i],c['S'][i],None,au['squares_wrapper'][nm][i]['cat'])
    return res
if __name__=="__main__":
    o=run(); json.dump(o,open(sys.argv[1],'w'),indent=1,sort_keys=True,default=str)
    n=sum(len(v) for f in o.values() for v in f.values()); print("steps",n)

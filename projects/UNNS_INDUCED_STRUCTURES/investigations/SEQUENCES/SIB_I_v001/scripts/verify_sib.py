"""Independent forward checks and exported witness replay; no third-party modules."""
from pathlib import Path
import csv,json,math
from collections import defaultdict
from ancestry import incoming,routes,factor,prime,profile
from run_sib import panel,aggregate,ROOT

def main():
    checks=0
    def check(condition):
        nonlocal checks
        assert condition
        checks+=1
    # Independent forward enumeration: every source/label producing target<=512.
    bound=512; edges=defaultdict(list)
    for s in range(1,bound+1):
        for n in range(1,s+1):
            if s%n==0:
                t=(s//n)*(n+1)**2
                if t<=bound: edges[t].append((s,n))
    forward={0:{x:{(x,())} for x in range(1,bound+1)}}
    for depth in range(1,4):
        layer=defaultdict(set)
        for t,ee in edges.items():
            for s,n in ee:
                for a,w in forward[depth-1].get(s,set()): layer[t].add((a,w+(n,)))
        forward[depth]=layer
        for x in range(1,bound+1): check(set(routes(x,depth))==layer.get(x,set()))
    for x in range(1,10000):
        check(prime(x)==(x>=2 and all(x%d for d in range(2,math.isqrt(x)+1))))
    for k in range(60): check(len(incoming(2**k))==k//2)
    # Independent permutation-merger fixture.
    check((6,(1,2)) in routes(108,2) and (6,(2,1)) in routes(108,2))
    check(profile(108)['permutation_pairs']>0)
    check(profile(16)['merger_sources']==0)
    check((63,(63,1)) in routes(16384,2))
    check((63,(7,3,3)) in routes(16384,3))
    for r in range(20):
        for word in ((63,1),(7,3,3)):
            x=63*2**r
            for n in word: check(x%n==0);x=x//n*(n+1)**2
            check(x==2**(14+r))
    expected={'lucas':[2,1,3,4,7,11,18,29,47,76],
              'primes':[2,3,5,7,11,13,17,19,23,29],
              'totient':[1,1,2,2,4,2,6,4,6,4],
              'powers2':[1,2,4,8,16,32,64,128,256,512],
              'catalan':[1,1,2,5,14,42,132,429,1430,4862],
              'sylvester':[2,3,7,43,1807,3263443,10650056950807]}
    summary=json.loads((ROOT/'results'/'summary.json').read_text())
    for name,terms in panel().items():
        vals=[x for _,x in terms];check(vals[:len(expected[name])]==expected[name])
        check(summary[name]['occurrences']==aggregate(vals))
        check(summary[name]['unique_support']==aggregate(sorted(set(vals))))
        for x in vals:
            check(math.prod(p**e for p,e in factor(x))==x)
            # Directly replay every exported-depth route.
            for d in range(1,4):
                for source,word in routes(x,d):
                    y=source
                    for n in word:
                        check(y%n==0);y=y//n*(n+1)**2
                    check(y==x)
    with (ROOT/'results'/'witnesses.csv').open() as f:
        for w in csv.DictReader(f):
            wa=json.loads(w['word_a']);wb=json.loads(w['word_b']);check(wa!=wb)
            for word in (wa,wb):
                x=int(w['source'])
                for n in word: check(x%n==0);x=x//n*(n+1)**2
                check(x==int(w['target']))
    check(summary['primes']['occurrences']['active']==0)
    with (ROOT/'results'/'controls.csv').open() as f:
        for row in csv.DictReader(f):
            if row['control'] in ('order_scramble','cyclic_shift'):
                a=summary[row['sequence']]['occurrences']
                for key in ('active','unique','merger_targets','different_content_targets'):
                    check(int(row[key])==a[key])
                for key in ('mean_incoming','mean_routes'):
                    check(float(row[key])==a[key])
    out={'status':'PASS','checks':checks,'independent_forward_bound':bound,'max_depth':3}
    (ROOT/'results'/'verification.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out))

if __name__=='__main__':main()

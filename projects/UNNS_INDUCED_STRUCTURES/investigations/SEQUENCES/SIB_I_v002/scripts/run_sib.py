"""SIB-I v002: exhaustive small-integer census and exact arithmetic controls."""
from pathlib import Path
from collections import defaultdict,Counter
from functools import lru_cache
from math import isqrt,gcd,comb,prod
import csv,json,random,statistics,hashlib

ROOT=Path(__file__).resolve().parents[1]
BOUND=4096
SEED=20261122

def factors(n):
    out=[];p=2
    while p*p<=n:
        e=0
        while n%p==0: n//=p;e+=1
        if e: out.append((p,e))
        p+=1
    if n>1:out.append((n,1))
    return out

def signature(x):return tuple(sorted(e for p,e in factors(x)))

def forward(bound):
    """Generate edges by legal source divisors, then propagate all words upward."""
    outgoing=defaultdict(list);incoming=defaultdict(list)
    # T_N(s)>=4s: no source above bound//4 can contribute an edge.
    for s in range(1,bound//4+1):
        for n in range(1,s+1):
            if s%n==0:
                t=(s//n)*(n+1)**2
                if t<=bound:
                    outgoing[s].append((t,n));incoming[t].append((s,n))
    histories={x:set() for x in range(1,bound+1)}
    for s in range(1,bound+1):
        for t,n in outgoing[s]:
            histories[t].add((s,(n,)))
            histories[t].update((a,w+(n,)) for a,w in histories[s])
    return incoming,histories

@lru_cache(None)
def backward(x):
    """Independent inverse algorithm: test every d<=sqrt(x), no factorization."""
    result=set()
    for d in range(2,isqrt(x)+1):
        if x%(d*d)==0:
            s=x//(d*d)*(d-1);n=d-1
            result.add((s,(n,)))
            result.update((a,w+(n,)) for a,w in backward(s))
    return frozenset(result)

def metrics(x,rr,edges):
    groups=defaultdict(list)
    for s,w in sorted(rr):groups[s].append(w)
    perm=diff=0;witness=None
    for s,words in groups.items():
        c=Counter(tuple(sorted(w)) for w in words)
        p=sum(n*(n-1)//2 for n in c.values())
        perm+=p;diff+=len(words)*(len(words)-1)//2-p
        if witness is None and len(c)>1:
            a=words[0];b=next(w for w in words if sorted(w)!=sorted(a))
            witness=(s,a,b)
    return dict(value=x,signature='.'.join(map(str,signature(x))) or 'unit',
                bit_length=x.bit_length(),incoming=len(edges),
                depth2=sum(len(w)==2 for _,w in rr),
                routes=len(rr),sources=len(groups),
                max_depth=max((len(w) for _,w in rr),default=0),
                merger_sources=sum(len(ws)>1 for ws in groups.values()),
                permutation_pairs=perm,different_content_pairs=diff),witness

def panel():
    luc=[2,1]
    while len(luc)<84:luc.append(luc[-1]+luc[-2])
    ps=[];n=2
    while len(ps)<84:
        if all(n%d for d in range(2,isqrt(n)+1)):ps.append(n)
        n+=1
    sy=[2]
    while len(sy)<7:sy.append(sy[-1]**2-sy[-1]+1)
    raw={'lucas':list(enumerate(luc)), 'primes':list(enumerate(ps,1)),
         'totient':[(n,sum(gcd(n,k)==1 for k in range(1,n+1))) for n in range(1,85)],
         'powers2':[(k,2**k) for k in range(60)],
         'catalan':[(n,comb(2*n,n)//(n+1)) for n in range(30)],
         'sylvester':list(enumerate(sy))}
    return {name:[(i,x) for i,x in terms if x<=BOUND] for name,terms in raw.items()}

def csvwrite(path,rows):
    if not rows:return
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)

def order_metrics(values,edges,histories):
    labels=[set(n for _,n in edges[x]) for x in values]
    words=[set(w for _,w in histories[x]) for x in values]
    return dict(adjacent_pairs=max(0,len(values)-1),
        shared_incoming_label=sum(bool(a&b) for a,b in zip(labels,labels[1:])),
        shared_route_word=sum(bool(a&b) for a,b in zip(words,words[1:])),
        equal_values=sum(a==b for a,b in zip(values,values[1:])),
        proper_divisibility=sum(b>a and b%a==0 for a,b in zip(values,values[1:])),
        legal_transition=sum((a,n) in edges[b] for a,b in zip(values,values[1:]) for n in [next((n for s,n in edges[b] if s==a),0)]))

def run():
    for d in ('data','results','reports'):(ROOT/d).mkdir(exist_ok=True)
    edges,hist=forward(BOUND);checks=0;rows=[];witnesses=[]
    for x in range(1,BOUND+1):
        assert hist[x]==backward(x);checks+=1
        m,w=metrics(x,hist[x],edges[x]);rows.append(m)
        assert m['incoming']==prod(e//2+1 for p,e in factors(x))-1;checks+=1
        for s,word in hist[x]:
            y=s
            for n in word:
                assert y%n==0;checks+=1;y=y//n*(n+1)**2
            assert y==x;checks+=1
        if w:witnesses.append(dict(target=x,source=w[0],word_a=json.dumps(w[1]),word_b=json.dumps(w[2])))
    csvwrite(ROOT/'results'/'integer_census.csv',rows)
    csvwrite(ROOT/'results'/'different_witnesses.csv',witnesses)
    byx={m['value']:m for m in rows}
    power=[dict(exponent=k,**byx[2**k]) for k in range(13)]
    assert all(m['different_content_pairs']==0 for m in power[:-1]);checks+=1
    assert power[-1]['different_content_pairs']>0;checks+=1
    assert (6,(6,7,7)) in hist[4096] and (6,(3,2,3,3)) in hist[4096];checks+=1
    csvwrite(ROOT/'results'/'powers_all_depth.csv',power)
    groups=defaultdict(list)
    for m in rows:groups[(m['signature'],m['bit_length'])].append(m)
    strata=[];counterexamples=[]
    for (sig,bits),members in sorted(groups.items()):
        entry=dict(signature=sig,bit_length=bits,n=len(members),incoming=members[0]['incoming'])
        assert len(set(m['incoming'] for m in members))==1;checks+=1
        for key in ('depth2','routes','merger_sources','different_content_pairs'):
            lo=min(members,key=lambda m:(m[key],m['value']));hi=max(members,key=lambda m:(m[key],-m['value']))
            entry[key+'_min']=lo[key];entry[key+'_max']=hi[key]
            if lo[key]!=hi[key]:counterexamples.append(dict(signature=sig,bit_length=bits,metric=key,x=lo['value'],y=hi['value'],x_metric=lo[key],y_metric=hi[key]))
        strata.append(entry)
    csvwrite(ROOT/'results'/'arithmetic_strata.csv',strata)
    csvwrite(ROOT/'results'/'counterexamples.csv',counterexamples)
    matched=[];families={};order=[];pools=[]
    keys=('incoming','depth2','routes','merger_sources','different_content_pairs')
    for ordinal,(name,terms) in enumerate(panel().items()):
        values=[x for i,x in terms];support=set(values)
        csvwrite(ROOT/'data'/f'{name}.csv',[dict(index=i,value=x) for i,x in terms])
        for x in sorted(support):
            m=byx[x];pool=[v['value'] for v in groups[(m['signature'],m['bit_length'])] if v['value'] not in support]
            pools.append(dict(sequence=name,value=x,pool=json.dumps(pool)))
            row=dict(sequence=name,value=x,observations=values.count(x),signature=m['signature'],bit_length=m['bit_length'],pool_size=len(pool))
            for key in keys:
                row[key]=m[key];row['control_'+key]=statistics.mean(byx[y][key] for y in pool) if pool else None
            matched.append(row)
        family_rows=[r for r in matched if r['sequence']==name]
        covered=[r for r in family_rows if r['pool_size']]
        family=dict(terms=len(values),unique_count=len(support),covered_unique=len(covered),covered_observations=sum(r['observations'] for r in covered))
        for weight in ('unique','observations'):
            denom=sum(1 if weight=='unique' else r['observations'] for r in covered)
            family[weight]={}
            for key in keys:
                family[weight][key]={'observed':sum(r[key]*(1 if weight=='unique' else r['observations']) for r in covered)/denom if denom else None,
                                    'control':sum(r['control_'+key]*(1 if weight=='unique' else r['observations']) for r in covered)/denom if denom else None}
        families[name]=family
        order.append(dict(sequence=name,kind='observed',replicate=-1,**order_metrics(values,edges,hist)))
        rng=random.Random(SEED+ordinal)
        for rep in range(32):
            v=values[:];rng.shuffle(v)
            order.append(dict(sequence=name,kind='permutation',replicate=rep,**order_metrics(v,edges,hist)))
    csvwrite(ROOT/'results'/'matched_controls.csv',matched)
    csvwrite(ROOT/'results'/'control_pools.csv',pools)
    csvwrite(ROOT/'results'/'order_controls.csv',order)
    # Exact architecture counterexample within the same binary magnitude bin.
    assert signature(289)==signature(361)==(2,);checks+=1
    assert byx[289]['depth2']==2 and byx[361]['depth2']==1;checks+=1
    summary=dict(bound=BOUND,first_power_different_content=12,
                 forward_backward_targets_checked=BOUND,checks=checks,
                 total_histories=sum(len(v) for v in hist.values()),
                 exponent_bitlength_strata=len(strata),
                 variable_route_strata=sum(r['routes_min']!=r['routes_max'] for r in strata),
                 variable_different_content_strata=sum(r['different_content_pairs_min']!=r['different_content_pairs_max'] for r in strata),
                 families=families)
    (ROOT/'results'/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8',newline='\n')
    (ROOT/'results'/'verification.json').write_text(json.dumps(dict(status='PASS',checks=checks,independent_algorithms=['forward source-divisor DAG','backward square-divisor recursion'],targets=BOUND),indent=2)+'\n',encoding='utf-8',newline='\n')
    lines=['# SIB-I v002 results','','Complete ambient ancestry for every positive integer <=4096. Both algorithms agree at every target.','','## Powers of two','','First unrestricted-depth different-content common-source merger: 2^12=4096. None exists at 2^k for 0<=k<12. Two witnesses from source 6 have words (6,7,7) and (3,2,3,3). Homogeneity extends these witnesses to every k>=12.','','## Arithmetic architecture','','The unordered exponent signature determines the incoming COUNT exactly. It does not determine incoming labels, predecessor values, deeper route counts or merger geometry.','','289=17^2 and 361=19^2 share exponent signature (2) and bit length 9. Each has one incoming edge; their respective predecessors 16 and 18 have 2 and 1 incoming edges. Thus their exact depth-2 route counts differ.','',f"Of {len(strata)} nonempty exponent-signature/bit-length strata, {summary['variable_route_strata']} have variable total ancestry counts and {summary['variable_different_content_strata']} have variable different-content pair counts.",'','## Architecture-matched comparisons','','Every target is compared with ALL integers in 1..4096 having the same unordered prime-exponent signature and bit length, excluding the entire observed support of that family. Empty control pools remain missing. Results below use unique values and only covered targets.','','| Family | Terms | Unique | Covered unique | Observed mean all-depth routes | Control mean |','|---|---:|---:|---:|---:|---:|']
    for name,f in families.items():
        a=f['unique']['routes'];fmt=lambda v:'unavailable' if v is None else f'{v:.4f}'
        lines.append(f"| {name} | {f['terms']} | {f['unique_count']} | {f['covered_unique']} | {fmt(a['observed'])} | {fmt(a['control'])} |")
    lines+=['','These are exact finite-reference means, not significance tests. Uniform weighting within a pool is a declared reference choice. Different targets may share pools. Binary magnitude matching allows size differences within each bin. Singleton or exhausted strata create a support limitation; no substitute controls are invented. These results cover bounded subsets of the v001 panel and must not be numerically compared as if they used the full v001 samples.','','## External order','','Order permutations retain all values, all multiplicities and every marginal arithmetic profile. Only successive-index relations change. The following shared-route-word counts compare consecutive observations; equal-value adjacencies can contribute.','','| Family | Observed shared-word adjacencies | Mean across 32 permutations |','|---|---:|---:|']
    for name in families:
        obs=next(r for r in order if r['sequence']==name and r['kind']=='observed')
        rand=[r['shared_route_word'] for r in order if r['sequence']==name and r['kind']=='permutation']
        lines.append(f"| {name} | {obs['shared_route_word']} | {statistics.mean(rand):.4f} |")
    lines+=['','See order_controls.csv for equal-value adjacencies, label overlaps, proper divisibility and actual one-step transitions. These are descriptive order checks, not a causal attribution to recurrence mechanisms.','','## Interpretation','','The square-divisor count is fully explained by the exponent signature. Deeper geometry additionally depends on the arithmetic of d-1 at every backward step. Prime identities therefore matter even after matching exponent patterns. The full prime-labeled factorization fixes x itself, so preserving that entire factorization leaves no distinct integer control. Sequence-specific evidence must concern the distribution or order of values under explicitly declared controls, not a separate ancestry attached to the same integer.','','All finite outputs are reproducible with standard Python. No v001 file is changed. See REGISTER.md for the all-depth threshold proof and exact limits.']
    (ROOT/'reports'/'RESULTS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':run()

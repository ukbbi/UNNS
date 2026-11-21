"""Exact predecessor architecture; standard-library-only positive integer grammar."""
from collections import Counter,defaultdict
from functools import lru_cache
from math import isqrt

def exponents(x):
    out=[];p=2
    while p*p<=x:
        e=0
        while x%p==0:x//=p;e+=1
        if e:out.append(e)
        p+=1
    if x>1:out.append(1)
    return tuple(sorted(out))

def forward(bound):
    edges=[[] for _ in range(bound+1)]
    for s in range(1,bound//4+1):
        ds=set()
        for d in range(1,isqrt(s)+1):
            if s%d==0:ds.update((d,s//d))
        for n in sorted(ds):
            t=s//n*(n+1)**2
            if t<=bound:edges[t].append((s,n))
    histories=[set() for _ in range(bound+1)]
    counts=[Counter() for _ in range(bound+1)]
    for x in range(1,bound+1):
        for s,n in edges[x]:
            histories[x].add((s,(n,)))
            histories[x].update((a,w+(n,)) for a,w in histories[s])
            counts[x][s,(n,)]+=1
            for (a,c),v in counts[s].items():counts[x][a,tuple(sorted(c+(n,)))]+=v
    return edges,histories,counts

@lru_cache(None)
def backward(x):
    rr=set()
    for d in range(2,isqrt(x)+1):
        if x%(d*d)==0:
            s=x//(d*d)*(d-1);n=d-1
            rr.add((s,(n,)))
            rr.update((a,w+(n,)) for a,w in backward(s))
    return frozenset(rr)

def count_metrics(counts):
    bysource=defaultdict(list)
    for (s,c),v in counts.items():bysource[s].append(v)
    total_pairs=sum(sum(v)*(sum(v)-1)//2 for v in bysource.values())
    perm=sum(n*(n-1)//2 for v in bysource.values() for n in v)
    return dict(routes=sum(counts.values()),sources=len(bysource),
                merger_sources=sum(sum(v)>1 for v in bysource.values()),
                permutation_pairs=perm,different_content_pairs=total_pairs-perm,
                max_depth=max((len(c) for s,c in counts),default=0))

class Intern:
    def __init__(self):self.index={};self.keys=[]
    def add(self,key):
        if key not in self.index:self.index[key]=len(self.keys);self.keys.append(key)
        return self.index[key]

def signatures(edges,counts,bound):
    names=['E0','E1','E2','E3','Efull','Ufull','length_profile','source_spectrum','content_spectrum']
    ids={n:[0]*(bound+1) for n in names};tables={n:Intern() for n in names}
    for x in range(1,bound+1):
        e=exponents(x)
        ids['E0'][x]=tables['E0'].add(e)
        for level in range(1,4):
            name=f'E{level}';prev=f'E{level-1}'
            ids[name][x]=tables[name].add((e,tuple(sorted(ids[prev][s] for s,n in edges[x]))))
        ids['Efull'][x]=tables['Efull'].add((e,tuple(sorted(ids['Efull'][s] for s,n in edges[x]))))
        ids['Ufull'][x]=tables['Ufull'].add(tuple(sorted(ids['Ufull'][s] for s,n in edges[x])))
        bysource=defaultdict(list);lengths=Counter()
        for (s,c),v in counts[x].items():bysource[s].append(v);lengths[len(c)]+=v
        length_profile=tuple(lengths[d] for d in range(1,max(lengths,default=0)+1))
        ids['length_profile'][x]=tables['length_profile'].add(length_profile)
        ids['source_spectrum'][x]=tables['source_spectrum'].add(tuple(sorted(sum(v) for v in bysource.values())))
        ids['content_spectrum'][x]=tables['content_spectrum'].add(tuple(sorted(tuple(sorted(v)) for v in bysource.values())))
    return ids,{name:t.keys for name,t in tables.items()}

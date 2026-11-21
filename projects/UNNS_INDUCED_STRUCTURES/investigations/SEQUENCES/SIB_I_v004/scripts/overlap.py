"""Complete history counts and exact sequence-conditioned overlap kernels."""
from functools import lru_cache
from math import gcd,lcm
from arithmetic import incoming

VISITED=set()

@lru_cache(None)
def count(x):
    """Nonempty ordered words; each word has one source at a fixed target."""
    VISITED.add(x)
    return sum(1+count(s) for s,n in incoming(x))

@lru_cache(None)
def words(x):
    return frozenset({()}|{w+(n,) for s,n in incoming(x) for w in words(s)})

def threshold(word):
    t=1
    for n in word:t=lcm(t,n)//n*(n+1)**2
    return t

def valuation(x,p):
    e=0
    while x%p==0:x//=p;e+=1
    return e

def kernel(values,grammar='unns'):
    f=count if grammar=='unns' else lambda x:valuation(x,2 if grammar=='doubling' else 3)
    return [[f(gcd(x,y)) for y in values] for x in values]

def inclusion(K,i,j):return K[i][j]==K[i][i]

def panel():
    f=[0,1];l=[2,1]
    while len(f)<=84:f.append(f[-1]+f[-2]);l.append(l[-1]+l[-2])
    s=[2]
    while len(s)<7:s.append(s[-1]**2-s[-1]+1)
    return {'fibonacci':[(i,f[i]) for i in range(1,85)],
            'lucas':[(i,l[i]) for i in range(1,85)],
            'sylvester':list(enumerate(s)),
            'powers2':[(i,2**i) for i in range(25)]}

def relations(name,terms):
    n=len(terms)
    rel={'adjacent':[(i,i+1) for i in range(n-1)]}
    if name in ('fibonacci','lucas'):
        rel['index_divides']=[(i,j) for i,(m,a) in enumerate(terms) for j,(k,b) in enumerate(terms) if m<k and k%m==0]
        rel['odd_multiple']=[(i,j) for i,(m,a) in enumerate(terms) for j,(k,b) in enumerate(terms) if m<k and k%m==0 and (k//m)%2==1]
    if name in ('sylvester','powers2'):rel['all_increasing_indices']=[(i,j) for i in range(n) for j in range(i+1,n)]
    return rel

def relation_metrics(K,edges):
    active=[(i,j) for i,j in edges if K[i][i]>0]
    return dict(edges=len(edges),overlap_edges=sum(K[i][j]>0 for i,j in edges),
                shared_words=sum(K[i][j] for i,j in edges),
                inclusion_edges=sum(inclusion(K,i,j) for i,j in edges),
                nonempty_source_edges=len(active),
                nonempty_inclusion_edges=sum(inclusion(K,i,j) for i,j in active))

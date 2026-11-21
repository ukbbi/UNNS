"""Explicit-word and certificate verification, with reproducible control replay."""
from pathlib import Path
from collections import defaultdict
from functools import lru_cache
from fractions import Fraction
from itertools import product
from math import gcd,lcm,prod
import csv,json,random,hashlib
from arithmetic import prime

ROOT=Path(__file__).resolve().parents[1]
NAMES=('fibonacci','lucas','sylvester','powers2')
GRAMMARS=('unns','doubling','tripling')

def read(path):
    with path.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))

@lru_cache(None)
def modulus(w):
    t=1
    for n in w:t=lcm(t,n)*(n+1)**2//n
    return t

def valuation(x,b):
    n=0
    while x%b==0:x//=b;n+=1
    return n

def evaluate(M,edges):
    out=dict(edges=0,overlap_edges=0,shared_words=0,inclusion_edges=0,nonempty_source_edges=0,nonempty_inclusion_edges=0)
    for i,j in edges:
        out['edges']+=1;v=M[i][j];a=M[i][i]
        out['overlap_edges']+=int(v>0);out['shared_words']+=v
        out['inclusion_edges']+=int(v==a)
        if a>0:out['nonempty_source_edges']+=1;out['nonempty_inclusion_edges']+=int(v==a)
    return out

def main():
    checks=0
    def check(condition):
        nonlocal checks
        assert condition;checks+=1
    cert=read(ROOT/'results'/'count_certificate.csv');W={};counts={}
    for row in cert:
        x=int(row['value']);fs=json.loads(row['factors'])
        check(prod(p**e for p,e in fs)==x)
        check(all(prime(p) and e>0 for p,e in fs));check(len(set(p for p,e in fs))==len(fs))
        ds=[1]
        for p,e in fs:ds=[d*p**j for d in ds for j in range(e//2+1)]
        ws={()}
        for d in ds:
            if d==1:continue
            s=x//(d*d)*(d-1);check(s in W)
            ws.update(w+(d-1,) for w in W[s])
        W[x]=frozenset(ws);counts[x]=len(ws)-1
        check(counts[x]==int(row['nonempty_words']))
        for w in ws:check(x%modulus(w)==0)
    values={};indices={};matrices={};rels={}
    for name in NAMES:
        data=read(ROOT/'data'/f'{name}.csv');idx=[int(r['index']) for r in data];v=[int(r['value']) for r in data]
        values[name]=v;indices[name]=idx;n=len(v)
        check(idx==list(range(idx[0],idx[0]+n)))
        if name in ('fibonacci','lucas'):
            check(idx==list(range(1,85)));check(v[:2]==([1,1] if name=='fibonacci' else [1,3]))
            check(all(v[i+2]==v[i]+v[i+1] for i in range(n-2)))
        elif name=='sylvester':check(v[0]==2 and all(v[i+1]==v[i]*v[i]-v[i]+1 for i in range(n-1)))
        else:check(v==[2**i for i in range(25)])
        K=[[len(W[x]&W[y])-1 for y in v] for x in v]
        matrices[name]={'unns':K,'doubling':[[min(valuation(x,2),valuation(y,2)) for y in v] for x in v],
                        'tripling':[[min(valuation(x,3),valuation(y,3)) for y in v] for x in v]}
        for i in range(n):
            for j in range(n):
                check(W[v[i]]&W[v[j]]==W[gcd(v[i],v[j])])
                check((K[i][j]==K[i][i])==(W[v[i]]<=W[v[j]]))
        matrix=read(ROOT/'results'/f'{name}_kernel.csv')
        for i,row in enumerate(matrix):
            check(int(row['index'])==idx[i])
            for j,label in enumerate(idx):check(int(row[f'i_{label}'])==K[i][j])
        r={'adjacent':[(i,i+1) for i in range(n-1)]}
        if name in ('fibonacci','lucas'):
            r['index_divides']=[(i,j) for i in range(n) for j in range(i+1,n) if idx[j]%idx[i]==0]
            r['odd_multiple']=[(i,j) for i,j in r['index_divides'] if (idx[j]//idx[i])%2==1]
        else:r['all_increasing_indices']=[(i,j) for i in range(n) for j in range(i+1,n)]
        rels[name]=r
    for row in read(ROOT/'results'/'overlap_pairs.csv'):
        name=row['sequence'];i=indices[name].index(int(row['index_i']));j=indices[name].index(int(row['index_j']))
        x=values[name][i];y=values[name][j];K=matrices[name]['unns']
        check(int(row['value_i'])==x and int(row['value_j'])==y)
        check(int(row['gcd'])==gcd(x,y) and int(row['K'])==K[i][j])
        check((row['i_included_in_j']=='True')==(W[x]<=W[y]));check((row['j_included_in_i']=='True')==(W[y]<=W[x]))
        for grammar in ('doubling','tripling'):check(int(row[grammar+'_K'])==matrices[name][grammar][i][j])
    for row in read(ROOT/'results'/'relations.csv'):
        got=evaluate(matrices[row['sequence']][row['grammar']],rels[row['sequence']][row['relation']])
        for key,val in got.items():check(int(row[key])==val)
    permrows=iter(read(ROOT/'results'/'permutations.csv'));rewirerows=iter(read(ROOT/'results'/'rewired_relations.csv'))
    perm_stats=defaultdict(list)
    for ordinal,name in enumerate(NAMES):
        n=len(values[name]);rng=random.Random(20261121+ordinal)
        for rep in range(2000):
            order=list(range(n));rng.shuffle(order)
            for grammar in GRAMMARS:
                row=next(permrows);check(row['sequence']==name and row['grammar']==grammar and int(row['replicate'])==rep)
                got=evaluate(matrices[name][grammar],list(zip(order,order[1:])))
                for key,val in got.items():check(int(row[key])==val)
                if grammar=='unns':perm_stats[name].append(got['overlap_edges'])
        rng=random.Random(20261221+ordinal)
        for relation,edges in rels[name].items():
            for rep in range(256):
                order=list(range(n));rng.shuffle(order);mapped=[(order[i],order[j]) for i,j in edges]
                check(len(set(order))==n)
                for grammar in GRAMMARS:
                    row=next(rewirerows);check(row['sequence']==name and row['relation']==relation and row['grammar']==grammar and int(row['replicate'])==rep)
                    got=evaluate(matrices[name][grammar],mapped)
                    for key,val in got.items():check(int(row[key])==val)
    check(next(permrows,None) is None);check(next(rewirerows,None) is None)
    summary=json.loads((ROOT/'results'/'summary.json').read_text())['sequences']
    for name,s in summary.items():
        K=matrices[name]['unns'];n=len(K);E=sum(K[i][j]>0 for i in range(n) for j in range(i+1,n))
        check(s['off_diagonal_overlap_pairs']==E);check(Fraction(s['exact_permutation_expectation'])==Fraction(2*E,n))
        weight=sum(K[i][j] for i in range(n) for j in range(i+1,n))
        check(Fraction(s['exact_weighted_expectation'])==Fraction(2*weight,n))
        check(s['permutation_zero_count']==perm_stats[name].count(0))
        check(s['permutation_mean']==sum(perm_stats[name])/2000)
    check(summary['fibonacci']['off_diagonal_overlap_pairs']==94);check(summary['lucas']['off_diagonal_overlap_pairs']==113)
    for row in read(ROOT/'results'/'counterexamples.csv'):
        x=int(row['value_i']);y=int(row['value_j']);w=tuple(json.loads(row['word']))
        check(w in W[x]);check((w in W[y])==(row['kind']=='nonadjacent_overlap'))
    # Small independent forward fixture: no factorization, no predecessor formula.
    F={x:set() for x in range(1,257)}
    for x in range(1,257):
        for label in range(1,x+1):
            if x%label:continue
            y=x//label*(label+1)**2
            if y<=256:F[y].add((label,));F[y].update(w+(label,) for w in F[x])
    for length in range(1,4):
        for w in product(range(1,5),repeat=length):
            q=modulus(w)
            for x in range(1,257):check((w in F[x])==(x%q==0))
    for x in range(1,257):
        for y in range(x,257):check(F[x]&F[y]==F[gcd(x,y)])
    manifest=ROOT/'MANIFEST.json'
    if manifest.exists():
        for p,d in json.loads(manifest.read_text())['sha256'].items():check(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==d)
    print(json.dumps(dict(status='PASS',checks=checks,sequences=4,indexed_observations=sum(map(len,values.values())),gcd_identity='verified',permutation_counts=[94,113])))

if __name__=='__main__':main()

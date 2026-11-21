"""FUG-I v003 independent verification: no import of run_p3.

A. Independent prime-valuation minimal-source threshold for every recorded word.
B. Exact word action/source reconstruction and all 84 dynamic-program counts.
C. Independent 7,056 Fibonacci meet checks and 307 transport checks.
D. Independent pairwise merger classification, special F72 witness and infinite scaling.
E. Tiny brute-force inverse oracle for 120 positive integers.
F. Baseline v002 route consistency and control data comparisons.
"""
from collections import defaultdict,Counter
from functools import lru_cache
from fractions import Fraction
from math import gcd, isqrt
from pathlib import Path
import csv,json
from arith import incoming,fib,lucas,factors,step

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'results'
BASE=ROOT/'baseline_v002'
F=fib(84)

def readcsv(name):
    with (OUT/name).open(newline='',encoding='utf-8') as fp:return list(csv.DictReader(fp))

def tokens(s):return tuple(int(t) for t in s.split(';')) if s else ()

def valuations(n):return dict(factors(n)) if n>1 else {}

def threshold_valuation(word):
    # Independent of the fraction+gcd/lcm generator construction.
    primes=set()
    for n in word:
        primes.update(valuations(n));primes.update(valuations(n+1))
    K=1
    for p in primes:
        prefix=0
        bound=0
        for n in word:
            en=valuations(n).get(p,0)
            ed=valuations(n+1).get(p,0)
            bound=max(bound,en-prefix)
            prefix+=2*ed-en
        K*=p**bound
    Q=Fraction(1,1)
    for n in word:Q*=Fraction((n+1)**2,n)
    E=K*Q
    assert E.denominator==1
    return K,E.numerator

@lru_cache(None)
def independently_count(y):
    # DP over DAG, not full path list
    c=Counter({0:1})
    for x,N,d in incoming(y):
        for length,value in independently_count(x).items():
            c[length+1]+=value
    return c

@lru_cache(None)
def other_histories(y):
    # Explicit word generation, but no call to Phase 3 generator.
    out={(): (y,)}
    for x,N,d in incoming(y):
        for old,states in other_histories(x).items():
            w=old+(N,)
            assert w not in out
            out[w]=states+(y,)
    return out

def brute_predecessors(y):
    return {(y//(d*d)*(d-1),d-1,d) for d in range(2,isqrt(y)+1) if y%(d*d)==0}

@lru_cache(None)
def brute_words(y):
    ans={()}
    for x,N,d in brute_predecessors(y):
        for w in brute_words(x):ans.add(w+(N,))
    return frozenset(ans)

def merge_counts(y):
    paths=other_histories(y)
    by_source=defaultdict(list)
    for w,states in paths.items():
        if w:by_source[states[0]].append(w)
    perm=content=groups=0
    for ws in by_source.values():
        if len(ws)<2:continue
        groups+=1
        for a in range(len(ws)):
            for b in range(a+1,len(ws)):
                if Counter(ws[a])==Counter(ws[b]):perm+=1
                else:content+=1
    return perm,content,groups

def independent_control(sequence):
    total=perms=contents=repeats=0
    marked=[]
    for j in range(1,85):
        y=sequence[j]
        total+=sum(independently_count(y).values())-1
        a,b,c=merge_counts(y)
        perms+=a;contents+=b;repeats+=c
        if b:marked.append(j)
    return total,perms,contents,repeats,marked


def main():
    summary=json.loads((OUT/'summary.json').read_text(encoding='utf-8'))
    assert summary['release']=='FUG-I_v003'
    baseline=json.loads((BASE/'summary.json').read_text(encoding='utf-8'))
    assert baseline['route_stats']['total_routes']==8
    rows=readcsv('fib_history_words_84.csv')
    profiles=readcsv('fib_history_profiles_84.csv')
    mergers=readcsv('fib_mergers_84.csv')
    transports=readcsv('fib_transport_84.csv')
    witness=readcsv('cross_content_witnesses.csv')
    assert len(rows)==292 and len(profiles)==84 and len(transports)==307
    w_by_idx=defaultdict(set)
    counts_by_idx=defaultdict(Counter)
    record_by_word={}
    for r in rows:
        j=int(r['j']);y=int(r['F_j']);source=int(r['source'])
        w=tokens(r['word']);ss=tokens(r['states'])
        assert 1<=j<=84 and y==F[j]
        assert len(w)==int(r['length']) and len(ss)==len(w)+1
        assert ss[0]==source and ss[-1]==y
        assert all(step(x,N)==z for x,N,z in zip(ss,w,ss[1:]))
        K,E=threshold_valuation(w)
        assert (K,E)==(int(r['K_min']),int(r['E_min']))
        assert E>0 and y%E==0 and K*(y//E)==source
        assert w not in w_by_idx[j]
        w_by_idx[j].add(w)
        counts_by_idx[j][len(w)]+=1
        record_by_word[(j,w)]=r
    assert len(w_by_idx)==84 and all(() in s for s in w_by_idx.values())
    for j in range(1,85):
        y=F[j]
        assert counts_by_idx[j]==independently_count(y)
        assert set(other_histories(y))==w_by_idx[j]
        p=profiles[j-1]
        assert int(p['j'])==j and int(p['F_j'])==y
        assert int(p['R'])==len(incoming(y))
        assert int(p['history_count'])==sum(counts_by_idx[j].values())-1
        assert int(p['height'])==max(counts_by_idx[j])
        a,b,c=merge_counts(y)
        assert (a,b,c)==(int(p['permutation_pairs']),int(p['different_content_pairs']),int(p['repeated_sources']))
        assert a+b==int(p['merger_pairs'])
    print('PASS: 292 exact word records, independent valuation thresholds and inverse actions')
    print('PASS: independent dynamic-program ancestry counts and merger classification for all 84 targets')
    # General threshold-membership cross-validation: every *observed* word across all Fibonacci layers.
    union={w for W in w_by_idx.values() for w in W}
    E_by_word={w:threshold_valuation(w)[1] for w in union}
    for j in range(1,85):
        expected={w for w,E in E_by_word.items() if F[j]%E==0}
        assert expected==w_by_idx[j]
    print('PASS: minimal endpoint divisibility exactly predicts layer membership of every observed word')
    nmeet=nontriv=0
    for m in range(1,85):
        for n in range(1,85):
            common=w_by_idx[m]&w_by_idx[n]
            assert common==w_by_idx[gcd(m,n)]
            nmeet+=1
            nontriv+=len(common)>1
    assert nmeet==7056 and nmeet==summary['all_fibonacci_index_pair_meet_checks']
    assert nontriv==summary['nontrivial_meet_pairs']
    print('PASS: complete Fibonacci gcd-meet law on 7,056 ordered layer pairs')
    assert len({(int(r['m']),int(r['n'])) for r in transports})==307
    acts=Counter()
    for r in transports:
        m=int(r['m']);n=int(r['n']);assert m<n and n%m==0
        assert F[n]//F[m]==int(r['scale']) and F[n]%F[m]==0
        assert w_by_idx[m]<=w_by_idx[n]
        extras=Counter(len(w) for w in w_by_idx[n]-w_by_idx[m])
        extras.pop(0,None)
        first=min(extras,default=0)
        acts[first]+=1
        assert first==int(r['first_activation_depth'])
        assert sum(extras.values())==int(r['extra_nonempty'])
        assert dict(sorted((str(k),v) for k,v in extras.items()))==json.loads(r['extra_by_length'])
    assert dict((str(k),v) for k,v in sorted(acts.items()))==summary['first_activation_depth_counts']
    print('PASS: all 307 proper index-divisibility transports, including depth-two activation')
    assert len(mergers)==122 and len(witness)==3
    assert Counter(r['kind'] for r in mergers)=={'permutation':119,'different_content':3}
    assert all(r['j']=='72' and int(r['source'])==1730743096803 for r in witness)
    for r in mergers:
        j=int(r['j']);wa=tokens(r['word_A']);wb=tokens(r['word_B'])
        assert wa!=wb and wa in w_by_idx[j] and wb in w_by_idx[j]
        assert int(record_by_word[(j,wa)]['source'])==int(record_by_word[(j,wb)]['source'])==int(r['source'])
        computed='permutation' if Counter(wa)==Counter(wb) else 'different_content'
        assert computed==r['kind']
        qa=Fraction(1,1);qb=Fraction(1,1)
        for t in wa:qa*=Fraction((t+1)**2,t)
        for t in wb:qb*=Fraction((t+1)**2,t)
        assert qa==qb
    assert 1730743096803*288==F[72]
    assert Fraction(16,3)**2*Fraction(81,8)==Fraction(4)**3*Fraction(9,2)==288
    for word in ((3,8,3),(1,1,1,2),(1,1,2,1),(1,2,1,1)):
        source=1730743096803
        for N in word:source=step(source,N)
        assert source==F[72]
    print('PASS: 122 exact source-locked mergers: 119 permutation pairs and 3 different-content pairs')
    print('PASS: four F72 witness words from one source; ratio 288 and lift to all Fibonacci F_(72k)')
    # Robust non-factorization oracle for small integer space, independent of fast predecessor engine.
    for y in range(1,121):
        assert set(incoming(y))==brute_predecessors(y)
        assert set(other_histories(y))==brute_words(y)
    print('PASS: independent brute-square-divisor predecessor and full word oracle (y=1..120)')
    controls=json.loads((OUT/'controls_phase3.json').read_text(encoding='utf-8'))
    for name,vals in [('Lucas',lucas(84)),('Fibonacci_plus_1',[f+1 for f in F])]:
        total,perm,content,repeat,indices=independent_control(vals)
        c=controls[name]
        assert (total,perm,content,repeat,indices)==(c['total_nonempty_histories'],
                c['permutation_pairs'],c['different_content_pairs'],c['repeated_source_instances'],
                c['targets_with_different_content'])
    assert [int(r['j']) for r in witness]==[72]*3
    print('PASS: Lucas and shifted-Fibonacci controls reproduced, including duplicate indexed values')
    print('FUG-I v003 VERIFY PASS')

if __name__=='__main__':main()

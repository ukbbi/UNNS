"""FUG-I Phase 4: exact word-activation ranks and Fibonacci ancestry laws.

Works locally with Python 3 standard library only. Input is a frozen copy of
Phase 3's exact finite word records. Does not modify older releases.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from math import gcd, lcm
import csv
import json
from arith import incoming, fib, lucas, step

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT/'baseline_v003'
OUT = ROOT/'results'
LIMIT = 84
A = (1, 2, 3, 5, 7, 11)


def load_csv(p):
    with p.open(newline='', encoding='utf-8') as fh:
        return list(csv.DictReader(fh))


def write_csv(name, rows, fields):
    with (OUT/name).open('w', encoding='utf-8', newline='') as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def word_tokens(s):
    return tuple(map(int,s.split(';'))) if s else ()


def word_text(word):
    return ';'.join(map(str,word))


def min_endpoint(word):
    """Return minimum source K, minimum endpoint E, multiplier q.

    Prefix fraction test is from FUG-I v003 T1; retained here as baseline.
    """
    q = Fraction(1, 1)
    K = 1
    for N in word:
        K = lcm(K, (q.denominator*N)//gcd(q.numerator, q.denominator*N))
        q *= Fraction((N+1)**2, N)
    E = K*q
    assert E.denominator == 1
    return K, E.numerator, q


def fibonacci_mod(n, modulus):
    """Fast-doubling Fibonacci, exact mod modulus; enormous n supported."""
    a,b=0,1
    for bit in bin(n)[2:]:
        c=a*(2*b-a) % modulus
        d=(a*a+b*b) % modulus
        if bit=='0':a,b=c,d
        else:a,b=d,(c+d)%modulus
    return a


def fibonacci_mod64_period():
    a,b=0,1
    for n in range(1,97):
        a,b=b,(a+b)%64
    assert (a,b)==(0,1), (a,b)
    return 96


@lru_cache(None)
def wordset(y):
    ws={()}
    for x,N,d in incoming(y):
        for word in wordset(x):
            ws.add(word+(N,))
    return frozenset(ws)


def wordset_by_indices(values):
    return {j:wordset(values[j]) for j in range(1, LIMIT+1)}


def control_protocol(values):
    ws=wordset_by_indices(values)
    proper=0;inclusion_fail=0;new_at_depth={};violation_examples=[]
    for m in range(1,LIMIT+1):
        for n in range(2*m,LIMIT+1,m):
            proper+=1
            if not ws[m].issubset(ws[n]):
                inclusion_fail+=1
                if len(violation_examples)<5:
                    missing=sorted(ws[m]-ws[n],key=lambda w:(len(w),w))
                    violation_examples.append({'m':m,'n':n,'source':values[m],'target':values[n],
                                               'missing_word':word_text(missing[0])})
    obs=defaultdict(list)
    for j,W in ws.items():
        for w in W:
            if w:obs[w].append(j)
    periodic_fail=0;periodic_examples=[]
    for w,occ in obs.items():
        z=min(occ)
        ideal={i for i in range(1,LIMIT+1) if i%z==0}
        if set(occ)!=ideal:
            periodic_fail+=1
            if len(periodic_examples)<4:
                periodic_examples.append({'word':word_text(w),'first_index':z,'observed':occ[:12],
                                          'first_mismatch':next(i for i in range(1,LIMIT+1) if (i in occ)!=(i%z==0))})
    return {'indexed_layers':LIMIT,'proper_divisibility_pairs':proper,
            'inclusion_failures':inclusion_fail,'distinct_nonempty_words':len(obs),
            'first_index_periodicity_failures':periodic_fail,
            'inclusion_examples':violation_examples,'periodicity_examples':periodic_examples}


def main():
    OUT.mkdir(exist_ok=True,parents=True)
    F=fib(LIMIT)
    baseline=json.loads((BASE/'summary.json').read_text(encoding='utf-8'))
    assert baseline['release']=='FUG-I_v003' and baseline['all_fibonacci_index_pair_meet_checks']==7056
    rows=load_csv(BASE/'fib_history_words_84.csv')
    transports=load_csv(BASE/'fib_transport_84.csv')
    assert len(rows)==292 and len(transports)==307
    histories=defaultdict(dict)
    for row in rows:
        j=int(row['j']);w=word_tokens(row['word'])
        assert w not in histories[j]
        histories[j][w]=row
        K,E,q=min_endpoint(w)
        assert K==int(row['K_min']) and E==int(row['E_min'])
        assert F[j]%E==0
    assert len(histories)==LIMIT
    unique={w for W in histories.values() for w in W}
    thresholds={w:min_endpoint(w)[:2] for w in unique}
    activation=[]
    first_counts=Counter();first_length=defaultdict(Counter)
    for w in sorted(unique,key=lambda w:(len(w),w)):
        K,E=thresholds[w]
        z=next(n for n in range(1,LIMIT+1) if F[n]%E==0)
        indices=[n for n in range(1,LIMIT+1) if w in histories[n]]
        assert indices==list(range(z,LIMIT+1,z)),(w,z,indices)
        assert E==1 if not w else E>=4
        if w:
            first_counts[z]+=1;first_length[z][len(w)]+=1
        activation.append(dict(word=word_text(w),length=len(w),K_min=K,E_min=E,
                               rank=z,first_F=F[z],indexed_frequency=len(indices),
                               observed_indices=';'.join(map(str,indices))))
    assert len(activation)==len(unique)
    write_csv('word_activation_84.csv',activation,
              ['word','length','K_min','E_min','rank','first_F','indexed_frequency','observed_indices'])

    index_rows=[]
    for n in range(1,LIMIT+1):
        activated=[w for w in unique if n%next(int(r['rank']) for r in activation if r['word']==word_text(w))==0]
        assert set(activated)==set(histories[n])
        new=first_counts[n]
        index_rows.append(dict(n=n,F_n=F[n],active_nonempty=len(activated)-1,
                               new_nonempty_words=new,
                               first_length_counts=json.dumps({str(k):v for k,v in sorted(first_length[n].items())},separators=(',',':'))))
    write_csv('index_activation_84.csv',index_rows,
              ['n','F_n','active_nonempty','new_nonempty_words','first_length_counts'])

    # Reconstruct every Phase 3 transport via first-appearance ranks, independent
    # of the Phase 3 transport deltas.
    rank={w:next(int(r['rank']) for r in activation if r['word']==word_text(w)) for w in unique}
    reenacted=[]
    activation_depths=Counter()
    for row in transports:
        m=int(row['m']);n=int(row['n'])
        new=[w for w in unique if n%rank[w]==0 and m%rank[w]!=0]
        distribution=Counter(map(len,new));distribution.pop(0,None)
        first=min(distribution,default=0)
        assert first==int(row['first_activation_depth'])
        assert sum(distribution.values())==int(row['extra_nonempty'])
        assert {str(k):v for k,v in sorted(distribution.items())}==json.loads(row['extra_by_length'])
        activation_depths[first]+=1
        reenacted.append(dict(m=m,n=n,extra_words=len(new),first_depth=first,
                              new_by_length=json.dumps({str(k):v for k,v in sorted(distribution.items())},separators=(',',':'))))
    write_csv('transport_activation_84.csv',reenacted,['m','n','extra_words','first_depth','new_by_length'])
    assert dict(activation_depths)=={0:193,1:108,2:6}

    # Exact merger gate for selected nonpermutation label histories.
    left=(3,8,3);right=(1,1,1,2)
    KA,EA,qa=min_endpoint(left);KB,EB,qb=min_endpoint(right)
    assert qa==qb==288 and (KA,EA)==(3,864) and (KB,EB)==(1,288)
    pair_K=lcm(KA,KB)
    pair_E=pair_K*qa
    assert pair_E.denominator==1 and pair_E.numerator==864
    z_merger=next(n for n in range(1,LIMIT+1) if F[n]%pair_E==0)
    assert z_merger==72
    m_gate={'words':[word_text(left),word_text(right)],'common_multiplier':288,
            'K_left':KA,'K_right':KB,'joint_min_source':pair_K,'joint_min_endpoint':pair_E.numerator,
            'rank_joint_endpoint':z_merger,'first_fibonacci_target':F[z_merger],
            'admissible_fibonacci_indices':'n = 72*k for k>=1',
            'F24_mod_864':F[24]%864,'F36_mod_864':F[36]%864,'F72_mod_864':F[72]%864}
    (OUT/'merger_gate.json').write_text(json.dumps(m_gate,indent=2)+'\n',encoding='utf-8')

    # Infinite first depth=2 activation family for alphabet A. Show explicit odd
    # representative indices; proof for all odd r in THEORY file via mod64 period.
    assert fibonacci_mod64_period()==96
    assert [fibonacci_mod(12*r,64) for r in (1,3,5,7)]==[16,48,16,48]
    assert [fibonacci_mod(24*r,64) for r in (1,3)]==[32]*2
    w=(7,2)
    K,E,q=min_endpoint(w)
    assert (K,E,q)==(7,288,Fraction(288,7))
    assert next(j for j in range(1,LIMIT+1) if F[j]%E==0)==24
    delayed=[]
    for r in (1,3,5,7,9,11,13,15,17):
        u=12*r;v=24*r
        mod_u=fibonacci_mod(u,64);mod_v=fibonacci_mod(v,64)
        assert mod_u in (16,48) and mod_v==32
        assert fibonacci_mod(u,288)!=0 and fibonacci_mod(v,288)==0
        # One step incoming label N corresponds to (N+1)^2 | F_j.
        a_label=[N for N in A if fibonacci_mod(u,(N+1)**2)==0]
        b_label=[N for N in A if fibonacci_mod(v,(N+1)**2)==0]
        assert a_label==b_label==[1,2,3,5,11]
        assert E>0 and fibonacci_mod(v,E)==0
        delayed.append(dict(r=r,index_before=u,index_after=v,
                            F_before_mod64=mod_u,F_after_mod64=mod_v,
                            alphabet=';'.join(map(str,A)),
                            shared_one_step_labels=';'.join(map(str,a_label)),
                            new_two_step_word='7;2',threshold_endpoint=E))
    write_csv('delayed_family_witnesses.csv',delayed,
              ['r','index_before','index_after','F_before_mod64','F_after_mod64',
               'alphabet','shared_one_step_labels','new_two_step_word','threshold_endpoint'])

    # Unbounded ancestry depths along Fibonacci n=6*4^t using only modular
    # arithmetic (do not compute huge Fibonacci integers).
    spine=[]
    for t in range(0,12):
        n=6*4**t
        power=2*t+5
        mod=fibonacci_mod(n,1<<power)
        v2=(mod & -mod).bit_length()-1
        assert v2==3+2*t
        depth=v2//2
        assert depth==t+1
        spine.append(dict(t=t,index=n,v2_Fn=v2,longest_N1_word=depth,
                          first_forbidden_next_length=depth+1))
    write_csv('unbounded_depth_spine.csv',spine,['t','index','v2_Fn',
              'longest_N1_word','first_forbidden_next_length'])

    controls={}
    for name,arr in [('Lucas',lucas(LIMIT)),('Fibonacci_plus_1',[f+1 for f in F])]:
        controls[name]=control_protocol(arr)
    controls['Fibonacci']=control_protocol(F)
    assert controls['Fibonacci']['inclusion_failures']==0
    assert controls['Fibonacci']['first_index_periodicity_failures']==0
    (OUT/'control_activation_84.json').write_text(json.dumps(controls,indent=2)+'\n',encoding='utf-8')

    output={
      'release':'FUG-I_v004','scope':'exact activation ranks of all words observed through Fibonacci index 84; explicit unbounded family theorems',
      'substrate':'T_N(x) = x*(N+1)^2/N, N | x',
      'census':{'Fibonacci_indices':LIMIT,'phase3_history_records':len(rows),
                'distinct_words_including_empty':len(unique),
                'distinct_nonempty_words':len(unique)-1,
                'first_activated_word_index_counts':{str(k):v for k,v in sorted(first_counts.items())},
                'transport_pairs':len(transports),'transport_first_activation_depths':{str(k):v for k,v in sorted(activation_depths.items())}},
      'rank_gate':m_gate,
      'infinite_delayed_activation':{'restriction_alphabet':list(A),'index_pairs':'(12r,24r) with odd r>=1',
                                     'new_two_step_word':'7;2','E_of_word':288,'one_step_label_set':[1,2,3,5,11],
                                     'full_grammar_first_depth_two_for_all_odd_r':'NOT CLAIMED'},
      'unbounded_depth':{'indices':'6*4^t','t':'nonnegative integers',
                         'v2_F_index':'3+2t','max_consecutive_N1_history_depth':'t+1'},
      'controls':controls,
      'baseline':'FUG-I_v003 exact records; v001-v003 remain unchanged',
      'status':'PROVED theorem statements; VERIFIED-EXACT finite data; unmatched controls remain descriptive'
    }
    (OUT/'summary.json').write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print('FUG-I Phase 4 exact run PASS')
    print('Recomputed Phase 3 records:',len(rows))
    print('Distinct activated nonempty words:',len(unique)-1)
    print('Activation index counts:',dict(sorted(first_counts.items())))
    print('Transport first activation depths:',dict(sorted(activation_depths.items())))
    print('Exact different-content merger gate: E=864, first Fibonacci index=72')
    print('Infinite delayed depth-two family: (F_(12r),F_(24r)) for every odd r, restricted alphabet',A)
    print('Unbounded exact N=1 ancestry along F_(6*4^t)')
    print('Control results:',{k:(v['inclusion_failures'],v['first_index_periodicity_failures']) for k,v in controls.items()})
    print('Results:',OUT)

if __name__=='__main__': main()

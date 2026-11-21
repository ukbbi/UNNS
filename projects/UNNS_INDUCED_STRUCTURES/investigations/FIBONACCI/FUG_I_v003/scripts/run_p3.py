"""FUG-I Phase 3 — exact history spectrum, meet, transport and merger audit.
All arithmetic integer exact, via copied v002 64-bit factor module.
No GitHub and no Windows shell execution required.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from math import gcd, lcm
import csv, json
from arith import incoming, fib, lucas, step

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'results'
BASE=ROOT/'baseline_v002'
LIMIT=84


def save_csv(name,rows,fields):
    with (OUT/name).open('w',newline='',encoding='utf-8') as fp:
        w=csv.DictWriter(fp,fieldnames=fields,extrasaction='ignore')
        w.writeheader();w.writerows(rows)

@lru_cache(None)
def histories(y):
    """Return unique triples (source, label_word, forward_state_path), including empty."""
    arr=[(y,(),(y,))]
    for x,N,d in incoming(y):
        for source,word,states in histories(x):
            arr.append((source,word+(N,),states+(y,)))
    return tuple(sorted(arr,key=lambda z:(len(z[1]),z[1],z[0])))


def threshold(word):
    """Minimal source K(w), and minimal positive endpoint E(w), independent of factorization.

    The prefix multiplier Q=a/b is reduced. A step N is admissible
    exactly when the source is a multiple of bN/gcd(a,bN).
    """
    q=Fraction(1,1)
    K=1
    for N in word:
        K=lcm(K,(q.denominator*N)//gcd(q.numerator,q.denominator*N))
        q*=Fraction((N+1)**2,N)
    E=K*q
    assert E.denominator==1
    return K,E.numerator


def wordstr(w):return ';'.join(map(str,w))
def statestr(s):return ';'.join(map(str,s))

def stats_for(values):
    total_hist=0; total_merged_pairs=0; total_permuted=0; total_content=0
    merged_sources=0; targets_cross=[]; max_hist=0
    for j in range(1,LIMIT+1):
        y=values[j]
        arr=histories(y)
        total_hist+=len(arr)-1
        max_hist=max(max_hist,len(arr)-1)
        per_source=defaultdict(list)
        for source,word,states in arr:
            if word:per_source[source].append(word)
        for source,words in per_source.items():
            if len(words)<2:continue
            merged_sources+=1
            same=diff=0
            for aidx in range(len(words)):
                for bidx in range(aidx+1,len(words)):
                    if Counter(words[aidx])==Counter(words[bidx]):same+=1
                    else:diff+=1
            total_permuted+=same;total_content+=diff
            total_merged_pairs+=same+diff
            if diff:targets_cross.append(j)
    return dict(total_nonempty_histories=total_hist,merger_pairs=total_merged_pairs,
                permutation_pairs=total_permuted,different_content_pairs=total_content,
                repeated_source_instances=merged_sources,
                targets_with_different_content=sorted(set(targets_cross)),
                max_histories_per_target=max_hist)


def run():
    OUT.mkdir(parents=True,exist_ok=True)
    F=fib(LIMIT)
    assert F[LIMIT]<2**64
    baseline=json.loads((BASE/'summary.json').read_text(encoding='utf-8'))
    assert baseline['release']=='FUG-I_v002' and baseline['limit']==LIMIT
    assert baseline['route_stats']['distinct_pairs']==4 and baseline['route_stats']['total_routes']==8
    b_rows=list(csv.DictReader((BASE/'fib_ancestry_84.csv').open(encoding='utf-8',newline='')))
    b_routes=list(csv.DictReader((BASE/'fib_routes_all_84.csv').open(encoding='utf-8',newline='')))
    assert len(b_rows)==84 and len(b_routes)==8
    words_by_idx={};hist_by_idx={};profile=[];wordrows=[];merger_rows=[];cross_content=[]
    checked_baseline=0
    for j in range(1,LIMIT+1):
        y=F[j];hh=histories(y)
        assert len(set(w for src,w,st in hh))==len(hh)
        lengths=Counter(len(w) for src,w,states in hh)
        assert lengths[0]==1
        words_by_idx[j]=frozenset(w for src,w,st in hh)
        hist_by_idx[j]=lengths
        src_to_paths=defaultdict(list)
        for src,w,states in hh:
            K,E=threshold(w)
            assert y%E==0 and src==K*(y//E)
            assert states[0]==src and states[-1]==y
            for a,N,b in zip(states,w,states[1:]):assert step(a,N)==b
            wordrows.append(dict(j=j,F_j=y,source=src,length=len(w),word=wordstr(w),
                                 states=statestr(states),K_min=K,E_min=E))
            if w:src_to_paths[src].append((w,states))
        srcs={src for src,w,states in hh if w}
        perm=content=group_count=0
        for src,paths in src_to_paths.items():
            if len(paths)<2:continue
            group_count+=1
            for ai in range(len(paths)):
                for bi in range(ai+1,len(paths)):
                    wa,sa=paths[ai];wb,sb=paths[bi]
                    kind='permutation' if Counter(wa)==Counter(wb) else 'different_content'
                    if kind=='permutation':perm+=1
                    else:content+=1
                    merger_rows.append(dict(j=j,F_j=y,source=src,kind=kind,
                            word_A=wordstr(wa),word_B=wordstr(wb),
                            states_A=statestr(sa),states_B=statestr(sb),
                            length_A=len(wa),length_B=len(wb)))
                    if kind=='different_content':cross_content.append(merger_rows[-1])
        one=next(r for r in b_rows if int(r['j'])==j)
        assert len(hh)-1==int(one['total_nonempty_ancestral_routes'])
        assert len(incoming(y))==int(one['one_step'])
        assert max(lengths)==int(one['ancestry_height'])
        assert {str(k):v for k,v in lengths.items() if k}==json.loads(one['route_counts_by_length'])
        checked_baseline+=1
        profile.append(dict(j=j,F_j=y,R=len(incoming(y)),history_count=len(hh)-1,
                            height=max(lengths),distinct_sources=len(srcs),
                            merger_pairs=perm+content,permutation_pairs=perm,
                            different_content_pairs=content,
                            repeated_sources=group_count,
                            H_by_length=json.dumps({str(k):lengths[k] for k in sorted(lengths) if k},separators=(',',':'))))
    # Exact meet law over ALL indexed Fibonacci layer pairs; includes F1=F2 duplicate values.
    meets=0;nontrivial_meets=0
    for m in range(1,LIMIT+1):
        for n in range(1,LIMIT+1):
            idx=gcd(m,n)
            common=words_by_idx[m]&words_by_idx[n]
            assert common==words_by_idx[idx],(m,n,idx)
            meets+=1
            if len(common)>1:nontrivial_meets+=1
    transport=[];first_depth_counts=Counter()
    for m in range(1,LIMIT+1):
        for n in range(2*m,LIMIT+1,m):
            left,right=hist_by_idx[m],hist_by_idx[n]
            assert words_by_idx[m]<=words_by_idx[n]
            delta={k:right.get(k,0)-left.get(k,0) for k in range(1,max(max(left),max(right))+1)}
            assert all(v>=0 for v in delta.values())
            first=min((k for k,v in delta.items() if v>0),default=0)
            first_depth_counts[first]+=1
            transport.append(dict(m=m,n=n,F_m=F[m],F_n=F[n],scale=F[n]//F[m],
                inherited_nonempty=len(words_by_idx[m])-1,
                total_nonempty=len(words_by_idx[n])-1,
                extra_nonempty=sum(delta.values()),first_activation_depth=first,
                extra_by_length=json.dumps({str(k):v for k,v in delta.items() if v},separators=(',',':'))))
    assert len(cross_content)==3 and {r['j'] for r in cross_content}=={72}
    assert all(r['source']==1730743096803 for r in cross_content)
    assert any({r['word_A'],r['word_B']}=={'3;8;3','1;1;1;2'} for r in cross_content)
    assert next(r for r in transport if (r['m'],r['n'])==(12,24))['first_activation_depth']==2
    # Source-locked v002 Fibonacci paths (with index identity retained).
    all_fib_paths=[]
    for j in range(1,LIMIT+1):
        for source,w,states in histories(F[j]):
            if not w:continue
            for i in range(1,j):
                if F[i]==source:all_fib_paths.append((i,j,len(w),wordstr(w),statestr(states)))
    assert len(all_fib_paths)==8
    assert sorted(all_fib_paths)==sorted((int(r['i']),int(r['j']),int(r['length']),r['labels'],r['states']) for r in b_routes)
    save_csv('fib_history_words_84.csv',wordrows,['j','F_j','source','length','word','states','K_min','E_min'])
    save_csv('fib_history_profiles_84.csv',profile,['j','F_j','R','history_count','height','distinct_sources',
                                                   'merger_pairs','permutation_pairs','different_content_pairs',
                                                   'repeated_sources','H_by_length'])
    save_csv('fib_mergers_84.csv',merger_rows,['j','F_j','source','kind','word_A','word_B','states_A','states_B','length_A','length_B'])
    save_csv('fib_transport_84.csv',transport,['m','n','F_m','F_n','scale','inherited_nonempty','total_nonempty',
                                                'extra_nonempty','first_activation_depth','extra_by_length'])
    save_csv('cross_content_witnesses.csv',cross_content,['j','F_j','source','kind','word_A','word_B',
                                                         'states_A','states_B','length_A','length_B'])
    controls={}
    for name,sequence in [('Lucas',lucas(LIMIT)),('Fibonacci_plus_1',[v+1 for v in F])]:
        controls[name]=stats_for(sequence)
    (OUT/'controls_phase3.json').write_text(json.dumps(controls,indent=2)+'\n',encoding='utf-8')
    selected={str(j):next(r for r in profile if r['j']==j) for j in [6,12,24,48,72,84]}
    phase3={'release':'FUG-I_v003','scope':'exact histories, gcd-meet, transport and mergers; Fibonacci indices 1..84',
            'F_84':F[LIMIT],'baseline_v002_checked_layers':checked_baseline,
            'all_fibonacci_index_pair_meet_checks':meets,'nontrivial_meet_pairs':nontrivial_meets,
            'transport_index_divisibility_pairs':len(transport),
            'first_activation_depth_counts':{str(k):v for k,v in sorted(first_depth_counts.items())},
            'fibonacci_totals':stats_for(F),
            'selected_fibonacci_layers':selected,
            'cross_content_F72_source':1730743096803,
            'cross_content_F72_ratio':288,
            'cross_content_F72_pairs':len(cross_content),
            'infinite_family':'F_(72k) for k>=1 via Fibonacci strong divisibility',
            'controls':controls,
            'limits':'Index census finite (n<=84); inherited number-theory/GE0-HD results are credited'}
    (OUT/'summary.json').write_text(json.dumps(phase3,indent=2)+'\n',encoding='utf-8')
    print('FUG-I Phase 3 exact run PASS')
    print('Baseline v002 records checked:',checked_baseline)
    print('All ordered Fibonacci pair gcd-meet checks:',meets)
    print('Proper Fibonacci index-divisibility transports:',len(transport))
    print('Activation depths:',dict(sorted(first_depth_counts.items())))
    print('Fibonacci full-history mergers:',phase3['fibonacci_totals'])
    print('Cross-content F72 pairs:',len(cross_content),'(source 1730743096803; multiplier 288)')
    print('Results:',OUT)

if __name__=='__main__':run()

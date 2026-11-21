from pathlib import Path
from fractions import Fraction
from math import gcd,log1p
from collections import Counter
import csv,json,random,statistics
from arithmetic import factor,incoming
from overlap import count,words,threshold,kernel,panel,relations,relation_metrics,VISITED

ROOT=Path(__file__).resolve().parents[1]
SEED=20261121
PERMUTATIONS=2000
REWIRES=256
GRAMMARS=('unns','doubling','tripling')

def csvwrite(p,rows):
    with p.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def jsonwrite(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8',newline='\n')

def plot(kernels):
    # Exact computed matrices; a fixed log(1+K) scale is shared across all panels.
    maxk=max(max(map(max,K)) for K in kernels.values());den=log1p(maxk)
    parts=['<svg xmlns="http://www.w3.org/2000/svg" width="940" height="1030" viewBox="0 0 940 1030">',
      '<rect width="940" height="1030" fill="#f8fafc"/>',
      '<text x="30" y="35" font-family="Arial" font-size="22" fill="#10263b">Sequence-conditioned history-overlap kernels</text>',
      '<text x="30" y="61" font-family="Arial" font-size="13">K(i,j) = |W(a_i) intersect W(a_j)| - 1; complete incoming words</text>']
    for q,(name,K) in enumerate(kernels.items()):
        x0=40+(q%2)*460;y0=115+(q//2)*440;size=350;n=len(K);unit=size/n
        parts.append(f'<text x="{x0}" y="{y0-15}" font-family="Arial" font-size="18">{name}: {n} indexed observations</text>')
        for i,row in enumerate(K):
            for j,v in enumerate(row):
                t=log1p(v)/den if den else 0
                color='#ffffff' if not v else '#%02x%02x%02x'%(int(211-191*t),int(231-157*t),int(245-127*t))
                parts.append(f'<rect x="{x0+j*unit:.4f}" y="{y0+i*unit:.4f}" width="{unit+.03:.4f}" height="{unit+.03:.4f}" fill="{color}"><title>positions {i+1},{j+1}: K={v}</title></rect>')
        parts.append(f'<rect x="{x0}" y="{y0}" width="{size}" height="{size}" fill="none" stroke="#718096"/>')
        parts.append(f'<text x="{x0}" y="{y0+size+22}" font-family="Arial" font-size="12">Indices increase left to right and top to bottom.</text>')
    parts += [f'<text x="40" y="1000" font-family="Arial" font-size="13">White: 0. Blue: common log(1+K) scale, positive values 1 to {maxk}. Diagonal included.</text>','</svg>']
    (ROOT/'reports'/'overlap.svg').write_text('\n'.join(parts)+'\n',encoding='utf-8',newline='\n')

def run():
    for d in ('data','results','reports'):(ROOT/d).mkdir(exist_ok=True)
    summary={};pairs=[];relation_rows=[];perms=[];rewires=[];kernels={};counterexamples=[];checks=0
    for ordinal,(name,terms) in enumerate(panel().items()):
        print('Computing',name,flush=True)
        values=[x for i,x in terms];n=len(values)
        csvwrite(ROOT/'data'/f'{name}.csv',[dict(index=i,value=x) for i,x in terms])
        ks={g:kernel(values,g) for g in GRAMMARS};K=ks['unns'];kernels[name]=K
        matrix=[dict(index=i,**{f'i_{j}':K[a][b] for b,(j,y) in enumerate(terms)}) for a,(i,x) in enumerate(terms)]
        csvwrite(ROOT/'results'/f'{name}_kernel.csv',matrix)
        for i in range(n):
            for j in range(i,n):
                g=gcd(values[i],values[j]);v=K[i][j]
                assert (v>0)==bool(incoming(g));checks+=1
                pairs.append(dict(sequence=name,index_i=terms[i][0],index_j=terms[j][0],value_i=values[i],value_j=values[j],gcd=g,K=v,
                                  i_included_in_j=K[i][i]==v,j_included_in_i=K[j][j]==v,
                                  doubling_K=ks['doubling'][i][j],tripling_K=ks['tripling'][i][j]))
        rel=relations(name,terms)
        for relname,edges in rel.items():
            for grammar,M in ks.items():relation_rows.append(dict(sequence=name,relation=relname,grammar=grammar,**relation_metrics(M,edges)))
        # A uniform permutation of indexed observations preserves every marginal fibre.
        rng=random.Random(SEED+ordinal)
        for rep in range(PERMUTATIONS):
            order=list(range(n));rng.shuffle(order)
            for grammar,M in ks.items():
                perms.append(dict(sequence=name,grammar=grammar,replicate=rep,**relation_metrics(M,list(zip(order,order[1:])))))
        # Relabel the relation graph's vertices: preserves directed topology and degree multiset.
        rng=random.Random(SEED+100+ordinal)
        for relname,edges in rel.items():
            for rep in range(REWIRES):
                order=list(range(n));rng.shuffle(order)
                mapped=[(order[i],order[j]) for i,j in edges]
                for grammar,M in ks.items():rewires.append(dict(sequence=name,relation=relname,grammar=grammar,replicate=rep,**relation_metrics(M,mapped)))
        good=sum(K[i][j]>0 for i in range(n) for j in range(i+1,n))
        weight=sum(K[i][j] for i in range(n) for j in range(i+1,n))
        observed=relation_metrics(K,rel['adjacent'])
        pp=[r for r in perms if r['sequence']==name and r['grammar']=='unns']
        exp=Fraction(2*good,n);wexp=Fraction(2*weight,n)
        summary[name]=dict(terms=n,index_start=terms[0][0],index_end=terms[-1][0],active_terms=sum(K[i][i]>0 for i in range(n)),
            off_diagonal_overlap_pairs=good,observed_adjacency=observed,
            exact_permutation_expectation=str(exp),expectation_decimal=float(exp),
            exact_weighted_expectation=str(wexp),permutation_mean=statistics.mean(r['overlap_edges'] for r in pp),
            permutation_zero_count=sum(r['overlap_edges']==0 for r in pp),permutations=PERMUTATIONS)
        for i in range(n):
            for j in range(i+2,n):
                if K[i][j]>0:
                    if not any(r['sequence']==name and r['kind']=='nonadjacent_overlap' for r in counterexamples):
                        label=incoming(gcd(values[i],values[j]))[0][1]
                        counterexamples.append(dict(sequence=name,kind='nonadjacent_overlap',index_i=terms[i][0],index_j=terms[j][0],value_i=values[i],value_j=values[j],word=json.dumps([label])))
        if name in ('fibonacci','lucas'):assert observed['overlap_edges']==0;checks+=1
        if name=='sylvester':assert good==0;checks+=1
        if name=='powers2':assert all(K[i][j]==K[i][i] for i in range(n) for j in range(i,n));checks+=1
        if name=='lucas':
            for i,j in rel['index_divides']:
                if K[i][j]!=K[i][i]:
                    missing=next((n,) for s,n in incoming(values[i]) if values[j]%((n+1)**2)!=0) if any(values[j]%((n+1)**2)!=0 for s,n in incoming(values[i])) else min(words(values[i])-words(values[j]),key=lambda w:(len(w),w))
                    counterexamples.append(dict(sequence=name,kind='unrestricted_index_transport_failure',index_i=terms[i][0],index_j=terms[j][0],value_i=values[i],value_j=values[j],word=json.dumps(missing)))
                    break
        for i,j in (rel.get('index_divides',[]) if name=='fibonacci' else rel.get('odd_multiple',[]) if name=='lucas' else []):
            assert values[j]%values[i]==0 and K[i][j]==K[i][i];checks+=1
    assert summary['fibonacci']['off_diagonal_overlap_pairs']==94;checks+=1
    assert summary['lucas']['off_diagonal_overlap_pairs']==113;checks+=1
    csvwrite(ROOT/'results'/'overlap_pairs.csv',pairs)
    csvwrite(ROOT/'results'/'relations.csv',relation_rows)
    csvwrite(ROOT/'results'/'permutations.csv',perms)
    csvwrite(ROOT/'results'/'rewired_relations.csv',rewires)
    csvwrite(ROOT/'results'/'counterexamples.csv',counterexamples)
    # Count certificates are only for sequence terms, their pair gcds and required ancestors.
    csvwrite(ROOT/'results'/'count_certificate.csv',[dict(value=x,factors=json.dumps(factor(x)),nonempty_words=count(x)) for x in sorted(VISITED)])
    jsonwrite(ROOT/'results'/'summary.json',dict(sequences=summary,checks=checks,permutations=PERMUTATIONS,rewires=REWIRES,seed=SEED))
    plot(kernels)
    lines=['# SIB-I v004 - Sequence-Conditioned Generative Structure','','This investigation returns to four externally generated sequences. It computes complete history-overlap kernels and relations among indexed observations. No integer census is expanded.','','## Exact value-preserving permutation expectations','','| Sequence | Terms | Active terms | Overlap pairs anywhere | Observed adjacent overlaps | Exact expectation | Decimal |','|---|---:|---:|---:|---:|---:|---:|']
    for name,s in summary.items():lines.append(f"| {name} | {s['terms']} | {s['active_terms']} | {s['off_diagonal_overlap_pairs']} | {s['observed_adjacency']['overlap_edges']} | {s['exact_permutation_expectation']} | {s['expectation_decimal']:.6f} |")
    lines+=['','The expectation is 2E/n, where E counts unordered pairs of distinct indexed observations with nonempty shared histories. Every such pair is adjacent with probability 2/n in a uniform linear permutation. Repeated values, if present, retain separate observation identities.','','## Recurrence-conditioned laws','','Fibonacci and Lucas: adjacent exclusion, with nonadjacent overlap witnesses. Sylvester: global exclusion follows from pairwise coprimality, including future terms regardless of their individual ancestry. Powers of two: nested word sets by increasing exponent. These are exact consequences of external arithmetic relations combined with the unchanged grammar.','','The finite Sylvester sample has no active fibres. Its zero kernel is therefore a degenerate finite control comparison; the pairwise-coprimality theorem supplies the all-index exclusion law. The nesting of powers-of-two word sets need not be strict at every index. Inclusion of an empty nonempty-word set is reported separately from nonvacuous inclusion.','','## Transport and rewiring','','relations.csv distinguishes Fibonacci index-divisibility and Lucas odd-multiple transport from adjacency. It also tests unrestricted index-divisibility for Lucas as an explicit overextension control. rewired_relations.csv relabels observation vertices of these relation graphs, preserving each observation and the relation graph topology while changing which values meet each relation. No conditional rerandomization is performed.','','| Sequence / relation | Inclusion edges | All edges | Nonempty-source inclusion | Nonempty-source edges |','|---|---:|---:|---:|---:|']
    for r in relation_rows:
        if r['grammar']=='unns' and r['relation']!='adjacent':lines.append(f"| {r['sequence']} / {r['relation']} | {r['inclusion_edges']} | {r['edges']} | {r['nonempty_inclusion_edges']} | {r['nonempty_source_edges']} |")
    lines+=['','## Alternative grammars','','Doubling (s -> 2s) and tripling (s -> 3s) have kernels v_2(gcd) and v_3(gcd). Their word alphabets are separate. The same coprimality exclusions and divisibility inclusions hold in these grammars, so these qualitative regimes are not unique signatures of UNNS. The exported quantitative comparisons test how history multiplicities differ.','','## Monte Carlo checks','','Two thousand fixed-seed permutations estimate adjacency distributions; 256 vertex relabellings per relation supply rewiring controls. Zero-event frequencies are exploratory Monte Carlo proportions, not exact tail probabilities. Observed exclusion is already entailed by recurrence theorems and is not presented as an unexplained anomaly.','','| Sequence | Zero-overlap permutations | Total permutations |','|---|---:|---:|']
    for name,s in summary.items():lines.append(f"| {name} | {s['permutation_zero_count']} | {PERMUTATIONS} |")
    lines+=['','## Relabelled transport controls','','The control rate pools nonempty-source edges across 256 independently drawn vertex permutations. This is a descriptive pooled rate, not an independent-edge probability estimate.','','| Sequence / relation | Observed nonempty inclusion | Observed nonempty edges | Rewired pooled inclusion rate |','|---|---:|---:|---:|']
    for name,relname in [('fibonacci','index_divides'),('lucas','odd_multiple'),('powers2','all_increasing_indices')]:
        obs=next(r for r in relation_rows if r['sequence']==name and r['relation']==relname and r['grammar']=='unns')
        ctrl=[r for r in rewires if r['sequence']==name and r['relation']==relname and r['grammar']=='unns']
        a=sum(r['nonempty_inclusion_edges'] for r in ctrl);b=sum(r['nonempty_source_edges'] for r in ctrl)
        lines.append(f"| {name} / {relname} | {obs['nonempty_inclusion_edges']} | {obs['nonempty_source_edges']} | {a}/{b} = {a/b:.6f} |")
    lines+=['','## Quantitative grammar comparison','','Off-diagonal weighted sums count all shared nonempty words across unordered indexed pairs. Alphabets differ between grammars, so these are grammar-relative counts.','','| Sequence | UNNS weighted sum | Doubling weighted sum | Tripling weighted sum |','|---|---:|---:|---:|']
    for name in summary:
        pp=[r for r in pairs if r['sequence']==name and r['index_i']!=r['index_j']]
        lines.append(f"| {name} | {sum(r['K'] for r in pp)} | {sum(r['doubling_K'] for r in pp)} | {sum(r['tripling_K'] for r in pp)} |")
    lines+=['','## Scope','','Fibonacci F1..F84; Lucas L1..L84; Sylvester s0..s6; powers 2^0..2^24. The shorter powers sample is declared to keep complete-history arithmetic compact; no equal-sample-size cross-family ranking is made. Totient and Catalan are deferred until a specific external relation is chosen.','','See REGISTER.md for the endpoint-divisibility proof of the GCD identity and recurrence-specific transport proofs. overlap.svg displays exact kernels using a common logarithmic color scale, including their diagonal.']
    (ROOT/'reports'/'RESULTS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':run()

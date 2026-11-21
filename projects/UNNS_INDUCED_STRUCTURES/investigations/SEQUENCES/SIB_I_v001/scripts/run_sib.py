from pathlib import Path
import csv,json,math,statistics,hashlib
from ancestry import incoming,profile,prime,factor
from controls import controls,alternative

ROOT=Path(__file__).resolve().parents[1]
CEILING=10**18

def panel():
    luc=[2,1]
    while len(luc)<84: luc.append(luc[-1]+luc[-2])
    ps=[]; n=2
    while len(ps)<84:
        if prime(n): ps.append(n)
        n+=1
    tot=[sum(math.gcd(n,k)==1 for k in range(1,n+1)) for n in range(1,85)]
    sy=[2]
    while len(sy)<8 and sy[-1]**2-sy[-1]+1<=CEILING: sy.append(sy[-1]**2-sy[-1]+1)
    return {'lucas':list(enumerate(luc)), 'primes':list(enumerate(ps,1)),
            'totient':list(enumerate(tot,1)),
            'powers2':[(k,2**k) for k in range(84) if 2**k<=CEILING],
            'catalan':[(n,math.comb(2*n,n)//(n+1)) for n in range(30) if math.comb(2*n,n)//(n+1)<=CEILING],
            'sylvester':list(enumerate(sy))}

def writecsv(path,rows):
    if not rows: return
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def temporal(values):
    labels=[set(n for _,n in incoming(x)) for x in values]
    return dict(adjacent_shared_label=sum(bool(a&b) for a,b in zip(labels,labels[1:])),
                adjacent_transition=sum(any(s==a for s,_ in incoming(b)) for a,b in zip(values,values[1:])))

def aggregate(values):
    pp=[profile(x) for x in values]
    return dict(n=len(values),unique=len(set(values)),active=sum(p['incoming']>0 for p in pp),
        active_fraction=sum(p['incoming']>0 for p in pp)/len(pp),
        mean_incoming=statistics.mean(p['incoming'] for p in pp),
        mean_routes=statistics.mean(p['routes'] for p in pp),
        depth2_active=sum(p['depth2']>0 for p in pp),
        merger_targets=sum(p['merger_sources']>0 for p in pp),
        different_content_targets=sum(p['different_content_pairs']>0 for p in pp),**temporal(values))

def run():
    for d in ['data','results','reports']: (ROOT/d).mkdir(exist_ok=True)
    summary={}; ctrl=[]; witnesses=[]; transport=[]
    for order,(name,terms) in enumerate(panel().items()):
        print('Running',name,flush=True)
        values=[x for _,x in terms]
        writecsv(ROOT/'data'/f'{name}_firstN.csv',[dict(index=i,value=x) for i,x in terms])
        rows=[]
        for i,x in terms:
            p=profile(x); w=p.pop('witness')
            rows.append(dict(index=i,**p,**alternative(x)))
            if w: witnesses.append(dict(sequence=name,index=i,target=x,source=w[0],word_a=json.dumps(w[1]),word_b=json.dumps(w[2])))
        writecsv(ROOT/'results'/f'{name}_report.csv',rows)
        acts={key:next((r['index'] for r in rows if r[key]>0),None) for key in ['incoming','depth2','merger_sources','permutation_pairs','different_content_pairs']}
        summary[name]={'occurrences':aggregate(values),'unique_support':aggregate(sorted(set(values))),
                       'first_index':acts,'max_value':max(values),'index_start':terms[0][0],'index_end':terms[-1][0]}
        # Inclusion of incoming label sets is the finite transport diagnostic.
        for (i,a),(j,b) in zip(terms,terms[1:]):
            la=set(n for _,n in incoming(a));lb=set(n for _,n in incoming(b))
            transport.append(dict(sequence=name,index_a=i,index_b=j,shared_labels=json.dumps(sorted(la&lb)),
                                  nonempty_label_inclusion=bool(la) and la<=lb,
                                  value_divides=b%a==0,adjacent_transition=any(s==a for s,_ in incoming(b))))
        for kind,rep,v in controls(values,20261121+order):
            ctrl.append(dict(sequence=name,control=kind,replicate=rep,**aggregate(v)))
    writecsv(ROOT/'results'/'controls.csv',ctrl)
    writecsv(ROOT/'results'/'witnesses.csv',witnesses)
    writecsv(ROOT/'results'/'transport.csv',transport)
    (ROOT/'results'/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    lines=['# SIB-I v001 results','','Exact positive-integer ancestry through depth 3; all sources and intermediate states are ambient integers. No route enumeration cap.','','| Sequence | Terms | Unique | Incoming-active | Depth-2 active | Source-locked merger targets | Different-content targets |','|---|---:|---:|---:|---:|---:|---:|']
    for name,s in summary.items():
        a=s['occurrences'];lines.append(f"| {name} | {a['n']} | {a['unique']} | {a['active']} | {a['depth2_active']} | {a['merger_targets']} | {a['different_content_targets']} |")
    lines+=['','## Activation (external indices)','','Indices start at zero except primes and totient, which start at one. Null means absent through depth 3 in this sample.','','```json\n'+json.dumps({k:v['first_index'] for k,v in summary.items()},indent=2)+'\n```','','## Controls','','Eight replicates per randomized control; seed 20261121 + sequence ordinal. Effects are descriptive; no p-values or universal family ranking. Random controls match each term\'s binary magnitude. Monotone controls sort those same samples. Order scrambles preserve every value and its multiplicity; cyclic shifts preserve cyclic order. Nearby offsets are nonzero integers in [-16,16], clipped to positive integers.','','| Sequence | Observed active fraction | Nearby mean | Magnitude-matched mean | Observed mean routes | Magnitude-matched mean routes |','|---|---:|---:|---:|---:|---:|']
    for name,s in summary.items():
        a=s['occurrences'];near=[c for c in ctrl if c['sequence']==name and c['control']=='nearby'];rnd=[c for c in ctrl if c['sequence']==name and c['control']=='bitlength_random']
        lines.append(f"| {name} | {a['active_fraction']:.4f} | {statistics.mean(c['active_fraction'] for c in near):.4f} | {statistics.mean(c['active_fraction'] for c in rnd):.4f} | {a['mean_routes']:.4f} | {statistics.mean(c['mean_routes'] for c in rnd):.4f} |")
    lines+=['','## Interpretation and limits','','Primes are obstructed at every positive depth by the final-step square-divisor criterion. Sylvester conclusions concern only the seven sampled terms; pairwise coprimality alone does not establish squarefreeness of all terms. Totient multiplicities are reported separately from distinct numerical support and genuine common-source mergers. The powers-of-two incoming fibre has floor(k/2) members at 2^k; its support-restricted graph is two parity chains, while ambient ancestry can branch.','','Every nonempty ambient incoming profile has minimal route length 1. A meaningful delayed-activation question must specify a fixed source or a restricted source set. Here depth-2 activation and common-source mergers are bounded-depth diagnostics. Absence of mergers through depth 3 makes no claim about deeper mergers. An infinite different-content merger family at powers of two is proved separately by explicit witnesses and homogeneous scaling; see REGISTER.md SIB-07 and reports/FINDINGS.md. No further infinite-family claim is inferred from finite samples.','','Alternative doubling/tripling incoming indicators appear in each sequence report. Transport CSV distinguishes label overlap, inclusion, divisibility and actual consecutive-value transitions. No repeated-label pattern is promoted to a recurrence theorem. All route counts use words with repetition retained; permutation classification uses sorted multisets, not sets.','','See REGISTER.md for proofs, README.md for scope, and results/controls.csv for every control replicate.']
    (ROOT/'reports'/'RESULTS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    # Factorization certificate for original sequence values.
    cert=[dict(value=x,factors=json.dumps(factor(x))) for x in sorted({x for terms in panel().values() for _,x in terms})]
    writecsv(ROOT/'results'/'input_factors.csv',cert)
    print(json.dumps(summary,indent=2))

if __name__=='__main__': run()

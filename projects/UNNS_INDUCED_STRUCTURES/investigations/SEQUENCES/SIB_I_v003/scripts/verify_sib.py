"""Independent inverse-route verification of exported profiles and signature groups."""
import csv,json,hashlib
from collections import Counter,defaultdict
from math import isqrt
from run_sib import ROOT,BOUND,METRICS
from architecture import backward,exponents

def read(name):
    with (ROOT/'results'/name).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def canonical(x):
    return tuple(canonical(y) for y in x) if isinstance(x,list) else x

def main():
    checks=0
    def check(b):
        nonlocal checks
        assert b;checks+=1
    rows=read('census.csv');check(len(rows)==BOUND)
    census={int(r['value']):r for r in rows}
    tables=json.loads((ROOT/'results'/'signature_definitions.json').read_text())
    for x,r in census.items():
        rr=backward(x);by_source=defaultdict(list)
        for s,w in rr:by_source[s].append(w)
        perm=diff=0
        for ws in by_source.values():
            for i,a in enumerate(ws):
                for b in ws[i+1:]:
                    if sorted(a)==sorted(b):perm+=1
                    else:diff+=1
        expected=dict(routes=len(rr),max_depth=max((len(w) for _,w in rr),default=0),sources=len(by_source),
                      merger_sources=sum(len(ws)>1 for ws in by_source.values()),permutation_pairs=perm,different_content_pairs=diff)
        for key,val in expected.items():check(int(r[key])==val)
        preds=[(x//(d*d)*(d-1),d-1) for d in range(2,isqrt(x)+1) if x%(d*d)==0]
        check(int(r['incoming'])==len(preds));e=exponents(x)
        sigs={'E0':e}
        for k in range(1,4):sigs[f'E{k}']=(e,tuple(sorted(int(census[s][f'E{k-1}']) for s,n in preds)))
        sigs['Efull']=(e,tuple(sorted(int(census[s]['Efull']) for s,n in preds)))
        sigs['Ufull']=tuple(sorted(int(census[s]['Ufull']) for s,n in preds))
        lc=Counter(len(w) for _,w in rr)
        sigs['length_profile']=tuple(lc[d] for d in range(1,max(lc,default=0)+1))
        sigs['source_spectrum']=tuple(sorted(len(ws) for ws in by_source.values()))
        sigs['content_spectrum']=tuple(sorted(tuple(sorted(Counter(tuple(sorted(w)) for w in ws).values())) for ws in by_source.values()))
        for name,key in sigs.items():check(canonical(tables[name][int(r[name])])==key)
    groups={}
    for name in tables:
        for matched in (False,True):
            g=defaultdict(list)
            for x,r in census.items():g[(int(r[name]),x.bit_length() if matched else 0)].append(x)
            groups[name,matched]=g
    stats={}
    for row in read('signature_controls.csv'):
        name=row['signature'];matched=row['match_bit_length']=='True'
        xs=groups[name,matched][int(row['signature_id']),int(row['bit_length'])]
        check(int(row['targets'])==len(xs));check(int(row['first_target'])==min(xs))
        for key in METRICS:
            lo=min(int(census[x][key]) for x in xs);hi=max(int(census[x][key]) for x in xs)
            check(lo==int(row[key+'_min']));check(hi==int(row[key+'_max']))
            stats[name,matched,key]=stats.get((name,matched,key),0)+int(lo!=hi)
    for row in read('classification.csv'):
        name=row['signature'];matched=row['match_bit_length']=='True'
        check(int(row['groups'])==len(groups[name,matched]))
        check(int(row['non_singleton_targets'])==sum(len(xs) for xs in groups[name,matched].values() if len(xs)>1))
        for key in METRICS:check(int(row[key+'_varying_groups'])==stats[name,matched,key])
    for row in read('counterexamples.csv'):
        x=int(row['x']);y=int(row['y']);name=row['signature'];key=row['metric']
        check(census[x][name]==census[y][name]);check(census[x][key]!=census[y][key])
        check(census[x][key]==row['x_metric'] and census[y][key]==row['y_metric'])
        if row['match_bit_length']=='True':check(x.bit_length()==y.bit_length())
    for row in read('case_routes.csv'):
        check((int(row['source']),tuple(json.loads(row['word']))) in backward(int(row['target'])))
    for row in read('case_edges.csv'):
        s=int(row['source']);n=int(row['label']);t=int(row['target'])
        check(s%n==0 and s//n*(n+1)**2==t)
    # E3 and Efull induce the same partition on this census; not an infinite-domain claim.
    for xs in groups['E3',False].values():check(len(set(census[x]['Efull'] for x in xs))==1)
    for h in range(4):
        for xs in groups[f'E{h}',False].values():
            prefixes=set()
            for x in xs:
                lp=tables['length_profile'][int(census[x]['length_profile'])]
                prefixes.add(tuple((lp+[0]*(h+1))[:h+1]))
            check(len(prefixes)==1)
    manifest=ROOT/'MANIFEST.json'
    if manifest.exists():
        for p,digest in json.loads(manifest.read_text())['sha256'].items():check(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==digest)
    print(json.dumps(dict(status='PASS',export_checks=checks,all_depth_targets=BOUND)))

if __name__=='__main__':main()

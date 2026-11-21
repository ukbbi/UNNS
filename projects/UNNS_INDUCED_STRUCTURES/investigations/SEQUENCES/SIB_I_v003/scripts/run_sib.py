from pathlib import Path
from collections import defaultdict,Counter
from math import prod
import csv,json
from architecture import forward,backward,count_metrics,signatures,exponents

ROOT=Path(__file__).resolve().parents[1]
BOUND=65536
METRICS=('routes','max_depth','sources','merger_sources','permutation_pairs','different_content_pairs')

def writejson(p,data):p.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8',newline='\n')
def writecsv(p,rows):
    with p.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)

def run():
    for d in ('results','reports'):(ROOT/d).mkdir(exist_ok=True)
    edges,hist,counts=forward(BOUND)
    ids,tables=signatures(edges,counts,BOUND)
    checks=0;profiles={};census=[]
    for x in range(1,BOUND+1):
        assert hist[x]==backward(x);checks+=1
        exact=Counter((s,tuple(sorted(w))) for s,w in hist[x])
        assert counts[x]==exact;checks+=1
        assert len(edges[x])==prod(e//2+1 for e in exponents(x))-1;checks+=1
        m=count_metrics(counts[x]);profiles[x]=m
        census.append(dict(value=x,bit_length=x.bit_length(),incoming=len(edges[x]),**m,**{name:arr[x] for name,arr in ids.items()}))
        for s,w in hist[x]:
            y=s
            for n in w:
                assert y%n==0;checks+=1;y=y//n*(n+1)**2
            assert y==x;checks+=1
    groups_out=[];counterexamples=[];summary_rows=[]
    for name,arr in ids.items():
        for match_size in (False,True):
            groups=defaultdict(list)
            for x in range(1,BOUND+1):groups[(arr[x],x.bit_length() if match_size else 0)].append(x)
            sr=dict(signature=name,match_bit_length=match_size,groups=len(groups),non_singleton_targets=sum(len(xs) for xs in groups.values() if len(xs)>1))
            variation={key:0 for key in METRICS}
            examples={key:[] for key in METRICS}
            for (sid,bits),xs in sorted(groups.items()):
                row=dict(signature=name,match_bit_length=match_size,signature_id=sid,bit_length=bits,targets=len(xs),first_target=xs[0])
                for key in METRICS:
                    lo=min(xs,key=lambda x:(profiles[x][key],x));hi=max(xs,key=lambda x:(profiles[x][key],-x))
                    row[key+'_min']=profiles[lo][key];row[key+'_max']=profiles[hi][key]
                    if row[key+'_min']!=row[key+'_max']:
                        variation[key]+=1
                        a=xs[0];b=next(x for x in xs if profiles[x][key]!=profiles[a][key])
                        examples[key].append((a,b))
                groups_out.append(row)
            for key in METRICS:
                sr[key+'_varying_groups']=variation[key]
                if examples[key]:
                    a,b=min(examples[key]);counterexamples.append(dict(signature=name,match_bit_length=match_size,metric=key,x=a,y=b,x_metric=profiles[a][key],y_metric=profiles[b][key]))
            summary_rows.append(sr)
    # Theoretical invariants are validated over every finite group.
    for row in summary_rows:
        if row['signature'] in ('Ufull','Efull','length_profile'):
            assert row['routes_varying_groups']==row['max_depth_varying_groups']==0;checks+=1
        if row['signature']=='content_spectrum':
            assert all(row[k+'_varying_groups']==0 for k in ('routes','sources','merger_sources','permutation_pairs','different_content_pairs'));checks+=1
    witnesses=[]
    for target in (100,896,300,14884,700,8700,2112,2401):
        for source,word in sorted(hist[target]):witnesses.append(dict(target=target,source=source,word=json.dumps(word),content=json.dumps(sorted(word))))
    assert ids['Ufull'][100]==ids['Ufull'][896];checks+=1
    assert ids['Ufull'][300]==ids['Ufull'][14884];checks+=1
    writecsv(ROOT/'results'/'census.csv',census)
    writecsv(ROOT/'results'/'signature_controls.csv',groups_out)
    writecsv(ROOT/'results'/'classification.csv',summary_rows)
    writecsv(ROOT/'results'/'counterexamples.csv',counterexamples)
    writecsv(ROOT/'results'/'case_routes.csv',witnesses)
    writejson(ROOT/'results'/'signature_definitions.json',tables)
    case_edges=[]
    for target in (100,896,300,14884,700,8700,2112,2401):
        todo=[target];seen=set()
        while todo:
            x=todo.pop()
            if x in seen:continue
            seen.add(x)
            for s,n in edges[x]:case_edges.append(dict(case_target=target,source=s,label=n,target=x));todo.append(s)
    writecsv(ROOT/'results'/'case_edges.csv',case_edges)
    result=dict(bound=BOUND,all_depth_targets=BOUND,total_histories=sum(len(r) for r in hist),max_possible_depth=8,checks=checks,status='PASS',classification=summary_rows,cases={x:profiles[x] for x in (100,896,300,14884)})
    writejson(ROOT/'results'/'summary.json',result)
    lines=['# SIB-I v003 вЂ” Recursive Predecessor Architecture','','Complete census of all positive targets <=65536, with every admissible positive-length history. Forward and backward route sets agree at every target; the source/content recurrence agrees with explicit ordered-word enumeration.','','## Classification','','E0 is the sorted exponent list. E(h+1) retains the root exponent list and multiset of predecessor E(h) signatures. Efull recursively retains this decoration to all leaves. Ufull is the complete unlabelled predecessor tree unfolded without shared-source identities.','','| Signature | Classes | Classes varying in route count | Classes varying in source count | Classes varying in different-content pairs |','|---|---:|---:|---:|---:|']
    for row in summary_rows:
        if not row['match_bit_length']:
            lines.append(f"| {row['signature']} | {row['groups']} | {row['routes_varying_groups']} | {row['sources_varying_groups']} | {row['different_content_pairs_varying_groups']} |")
    lines+=['','Classifications use exact interned tuples, not probabilistic hashes. Zero variation is a finite observation unless a corresponding theorem is proved in REGISTER.md. Efull sufficiency for merger counts outside this domain remains OPEN.','','## Explicit counterexamples','','| Target | All routes | Distinct sources | Merger sources | Permutation pairs | Different-content pairs |','|---|---:|---:|---:|---:|---:|']
    for x in (100,896,300,14884):
        m=profiles[x];lines.append(f"| {x} | {m['routes']} | {m['sources']} | {m['merger_sources']} | {m['permutation_pairs']} | {m['different_content_pairs']} |")
    lines+=['','100 and 896 share Ufull; 300 and 14884 also share Ufull. All routes and the complete predecessor edges for these cases are exported. Matching a complete unfolded tree preserves depth and route counts, yet can lose convergence information and content distinctions. These named pairs need not share binary magnitude. Additional bit-length-matched counterexamples, where found, are in counterexamples.csv.','','## Exact source/content recurrence','','For each target retain a counter indexed by (source, label multiset). Each incoming edge appends its label to every predecessor content and contributes its direct one-step history. This computes exact multiplicities without retaining ordered words. Summing counters recovers route counts; grouping by source recovers merger multiplicities; splitting by content distinguishes permutation from different-content pairs. This is a sufficient representation, not a proven minimal signature.','','## Controls and limitations','','All targets in each signature class form an exhaustive finite control pool. A second analysis intersects classes with binary magnitude bins. For a target, its peers are the other members of its class; singleton classes have no controls. signature_controls.csv gives class sizes and metric ranges, and census.csv gives exact membership. There are no random trials or p-values. Matching on increasingly detailed recursively derived data is an information-sufficiency test, not independent causal evidence. The content-spectrum summary already encodes the partitions used in the merger counts; it is an exact aggregation, not a predictive discovery.','','This release deliberately studies the predecessor architecture rather than ranking external sequences. The root and all sources remain ordinary positive integers in the unchanged grammar. Source identities affect merger classification; observed sequence multiplicities would form a separate layer.','','The prior v001 and v002 releases are preserved; no GitHub changes are made.']
    (ROOT/'reports'/'RESULTS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('classification','cases')}))

if __name__=='__main__':run()

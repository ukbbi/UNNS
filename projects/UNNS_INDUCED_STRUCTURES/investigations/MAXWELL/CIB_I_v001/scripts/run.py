"""Deterministic comparative pass; computations do not use results to select profiles."""
from pathlib import Path
from fractions import Fraction
import csv, json, hashlib, sys
sys.path.insert(0,str(Path(__file__).parent))
from model import graph, profile_scores, scramble_sources, diamond, exact_nonzero

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'protocol'/'PROTOCOL.json'
protocol=json.loads(P.read_text())
assert hashlib.sha256(P.read_bytes()).hexdigest()==(ROOT/'protocol'/'PROTOCOL.sha256').read_text().strip()
M=protocol['index_window']['max']
names=list(protocol['fixed_grammars'])
profiles=protocol['medium_profiles']+protocol['additional_checks']
graphs={name:graph(name,M) for name in names}
orig=graphs['UNNS']
scrambled=scramble_sources(orig,M)
assert len(set((m,y) for m,y,n in scrambled))==len(scrambled)
assert sorted(y-m for m,y,n in orig)==sorted(y-m for m,y,n in scrambled)
graphs['UNNS_Q_PRESERVING_SCRAMBLE']=scrambled
rows=[]
for p in profiles:
    duty=Fraction(p)
    for name,edges in graphs.items():
        stats=profile_scores(edges,duty,M)
        rows.append({'profile':p,'grammar':name,**stats})
for p in profiles:
    ua=[r for r in rows if r['profile']==p and r['grammar']=='UNNS'][0]
    sh=[r for r in rows if r['profile']==p and r['grammar']=='UNNS_Q_PRESERVING_SCRAMBLE'][0]
    assert ua['nonzero_edges']==sh['nonzero_edges']
    assert ua['mean_fourier_power']==sh['mean_fourier_power']
RESULTS=ROOT/'results'
RESULTS.mkdir(exist_ok=True)
with (RESULTS/'comparison.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
with (RESULTS/'diamond.csv').open('w',newline='') as f:
    ds=[diamond(Fraction(p)) for p in profiles]
    for d in ds:
        d['A_first_order_edges']=','.join(map(str,map(int,d['A_first_order_edges'])))
        d['B_first_order_edges']=','.join(map(str,map(int,d['B_first_order_edges'])))
    w=csv.DictWriter(f,fieldnames=list(ds[0]));w.writeheader();w.writerows(ds)
# Analytic q=t*(N^2+N+1) witness table under blind medium set.
witnesses=[]
for n in range(1,15):
    s=n*n+n+1
    if s>M-1:break
    for t in (1,2,3):
        m=n*t; y=t*(n+1)**2
        if y>M:continue
        q=y-m
        witnesses.append({'n':n,'t':t,'source':m,'target':y,'q':q,**{p:int(exact_nonzero(q,Fraction(p))) for p in profiles}})
with (RESULTS/'witnesses.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(witnesses[0]));w.writeheader();w.writerows(witnesses)
summary={
 'release':'CIB_I_v001', 'scope':'analytic dielectric first-order Fourier comparison; not physical experimental predictive validation',
 'protocol_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),
 'graph_edge_counts':{name:len(edges) for name,edges in graphs.items()},
 'primary_profiles':protocol['medium_profiles'], 'additional_profiles':protocol['additional_checks'],
 'UNNS_scores':{r['profile']:{k:r[k] for k in ['edges','nonzero_edges','nonzero_fraction','mean_fourier_power','background_nonzero_fraction','enrichment']} for r in rows if r['grammar']=='UNNS'},
 'q_histogram_matching_control_exactly_equal_all_scores':True,
 'q1_couplings_UNNS':sum((y-m)==1 for m,y,n in orig),
 'v009_engineered_q_6_28_UNNS_overlap':[(m,y,n) for m,y,n in orig if y-m in (6,28)],
 'diamond':{p:diamond(Fraction(p)) for p in profiles},
 'conclusion':'coupling classifies chosen UNNS edges exactly but has no identifiable UNNS specificity after q-matched control; independent physical performance NOT established'
}
(RESULTS/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print('CIB-I v001 COMPUTE PASS, protocol',summary['protocol_sha256'])
print('Edge counts:',summary['graph_edge_counts'])
for p in profiles:
    s=summary['UNNS_scores'][p]
    print(p,'UNNS first-order hits',s['nonzero_edges'],'/',s['edges'], 'rate',round(s['nonzero_fraction'],6),'background',round(s['background_nonzero_fraction'],6),'enrichment',round(s['enrichment'],4))
print('Diamond 1/2:',summary['diamond']['1/2'])
print('Diamond 1/3:',summary['diamond']['1/3'])
print('q1 overlaps:',summary['q1_couplings_UNNS'],'engineered q6/28 overlaps:',summary['v009_engineered_q_6_28_UNNS_overlap'])

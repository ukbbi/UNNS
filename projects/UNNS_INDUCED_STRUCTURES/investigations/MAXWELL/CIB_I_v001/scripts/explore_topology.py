"""POST-PROTOCOL EXPLORATORY: 2-step path and merger topology; not primary scored."""
from pathlib import Path
from collections import defaultdict
from fractions import Fraction
import sys,csv,json
sys.path.insert(0,str(Path(__file__).parent))
from model import graph,scramble_sources
ROOT=Path(__file__).resolve().parents[1]
proto=json.loads((ROOT/'protocol'/'PROTOCOL.json').read_text())
M=proto['index_window']['max']; profiles=proto['medium_profiles']+proto['additional_checks']
names=list(proto['fixed_grammars'])
graphs={name:graph(name,M) for name in names}
graphs['UNNS_Q_PRESERVING_SCRAMBLE']=scramble_sources(graphs['UNNS'],M)
rows=[]
for profile in profiles:
    b=Fraction(profile).denominator
    for name,es in graphs.items():
        e=[(m,y) for m,y,n in es if (y-m)%b]
        target=defaultdict(list)
        for x,y in e:target[x].append(y)
        bypair=defaultdict(set)
        for x,y in e:
            for z in target.get(y,[]):bypair[(x,z)].add(y)
        paths=sum(len(v) for v in bypair.values())
        mergers=sum(len(v)*(len(v)-1)//2 for v in bypair.values())
        rows.append(dict(profile=profile,grammar=name,edges=len(e),two_step_paths=paths,merger_pairs=mergers))
with (ROOT/'results'/'topology_exploratory.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print('CIB-I v001 TOPOLOGY EXPLORATORY PASS')
for r in rows:
    if r['profile'] in ['1/2','1/3','1/5','1/7'] and r['grammar'] in ['UNNS','UNNS_Q_PRESERVING_SCRAMBLE']:
        print(r)

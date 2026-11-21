"""FUG-I Phase 2: complete directed ancestry for Fibonacci indices <=84.

Default run is exact for ALL possible path lengths, not a depth-limited scan.
No dependencies beyond Python 3.9 standard library. Creates ./results.
"""
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path
import csv, json, sys
from arith import fib, lucas, factors, incoming, is_prime, step

BASE=Path(__file__).resolve().parent.parent
OUT=BASE/'results'
LIMIT=84


def csvsave(name, rows, columns):
    with (OUT/name).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=columns)
        w.writeheader();w.writerows(rows)


@lru_cache(None)
def ancestry(y):
    """Routes of every length ending at y, each (states,labels) in forward order.

    A length-zero route at y is included; all other routes end at y.
    Recursive predecessor expansion is finite since each x <= y/4.
    """
    paths=[((y,),())]
    for x,N,d in incoming(y):
        for states,labels in ancestry(x):
            paths.append((states+(y,),labels+(N,)))
    return tuple(paths)


def build_indexed(values, limit):
    value_to_indices=defaultdict(list)
    for i in range(1,limit+1):value_to_indices[values[i]].append(i)
    rows=[];summary=[];profiles=[];closures=[]
    max_nodes=0
    for j in range(1,limit+1):
        y=values[j]
        routes=ancestry(y)
        nodes={x for states,_ in routes for x in states}
        roots={states[0] for states,labels in routes if not incoming(states[0])}
        # A root must not itself admit an incoming integer nest occurrence.
        assert roots and all(not incoming(x) for x in roots)
        h=max(map(lambda z:len(z[1]), routes))
        hist=Counter(len(labels) for states,labels in routes)
        for depth in range(1,h+1):
            assert hist.get(depth,0)>0
        for states,labels in routes:
            if not labels:continue
            for i in value_to_indices.get(states[0],()):
                if i>=j:continue
                rows.append(dict(i=i,j=j,F_i=values[i],F_j=y,
                    length=len(labels), labels=';'.join(map(str,labels)),
                    states=';'.join(map(str,states))))
        profiles.append(dict(j=j,F_j=y,one_step=len(incoming(y)),
            ancestry_height=h, distinct_ancestor_nodes=len(nodes)-1,
            total_nonempty_ancestral_routes=len(routes)-1,
            terminal_squarefree_roots=len(roots),
            roots=';'.join(map(str,sorted(roots))),
            route_counts_by_length=json.dumps({str(d):c for d,c in sorted(hist.items()) if d>0},separators=(',',':'))))
        if len(nodes)>max_nodes:max_nodes=len(nodes)
    rows.sort(key=lambda r:(r['length'],r['i'],r['j'],r['labels']))
    keys=[(r['i'],r['j'],r['labels']) for r in rows]
    assert len(set(keys))==len(keys)
    pair_routes=defaultdict(list)
    for row in rows:pair_routes[(row['i'],row['j'])].append(row)
    for (i,j),prs in sorted(pair_routes.items()):
        summary.append(dict(i=i,j=j,source=values[i],target=values[j],
            min_distance=min(r['length'] for r in prs),
            max_length=max(r['length'] for r in prs),
            total_routes=len(prs)))
    return rows,summary,profiles,{'distinct_pairs':len(pair_routes),
         'total_routes':len(rows),'routes_by_length':dict(sorted(Counter(r['length'] for r in rows).items())),
         'max_ancestry_height':max(r['ancestry_height'] for r in profiles),
         'max_nodes_one_target':max_nodes,
         'unique_reverse_nodes_in_memo':ancestry.cache_info().currsize}


def make_svg(paths,filename,title):
    """Stable, self-contained conceptual route SVG (actual edges and labels)."""
    # graph of target 144 (all actual immediate predecessor links)
    y=144
    edges={}
    nodes={y}
    for states,labels in ancestry(y):
        for a,N,b in zip(states,labels,states[1:]):
            nodes.add(a);nodes.add(b)
            edges[(a,b)]=N
    # horizontal layout by maximum distance from root to each node; no false edges
    rank={z:0 for z in nodes}
    for _ in range(len(nodes)):
        for (a,b),N in edges.items():rank[b]=max(rank[b],rank[a]+1)
    levels=defaultdict(list)
    for z in sorted(nodes):levels[rank[z]].append(z)
    height=105+max(len(v) for v in levels.values())*48
    width=860
    coords={}
    for r,vs in levels.items():
        for idx,z in enumerate(vs):
            x=75+r*235
            yy=70+(idx+1)*(height-110)/(len(vs)+1)
            coords[z]=(x,yy)
    # rank 0...3
    lines=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
    '<rect width="100%" height="100%" fill="#101927"/>',
    f'<text x="25" y="32" font-family="Arial" font-size="18" fill="white">{title}</text>']
    for (a,b),N in sorted(edges.items()):
        x1,y1=coords[a];x2,y2=coords[b]
        lines.append(f'<path d="M{x1+33},{y1} L{x2-33},{y2}" stroke="#7cbdc7" stroke-width="2" fill="none"/>')
        lines.append(f'<text x="{(x1+x2)/2}" y="{(y1+y2)/2-6}" font-family="Arial" font-size="11" fill="#c0dbe0" text-anchor="middle">N={N}</text>')
    for z in sorted(nodes):
        x,y=coords[z]
        color='#15a89b' if z in {2,5,8,144} else '#64748b'
        lines.append(f'<rect x="{x-34}" y="{y-17}" width="68" height="34" rx="9" fill="{color}"/>')
        lines.append(f'<text x="{x}" y="{y+5}" text-anchor="middle" fill="white" font-size="14" font-family="Arial">{z}</text>')
    lines.append('</svg>')
    filename.write_text('\n'.join(lines)+'\n',encoding='utf-8')


def run():
    OUT.mkdir(exist_ok=True)
    (BASE/'figures').mkdir(exist_ok=True)
    F=fib(LIMIT)
    assert F[-1]<(1<<64)
    rows,pairs,profiles,stats=build_indexed(F,LIMIT)
    # SOURCE-LOCKED prior release baseline: all eight v001 routes retained exactly
    assert len(rows)==8 and len(pairs)==4 and stats['routes_by_length']=={1:1,2:4,3:3},stats
    assert [(p['i'],p['j'],p['min_distance'],p['total_routes']) for p in pairs]==[
        (3,6,1,1),(3,12,3,3),(5,12,2,2),(6,12,2,2)]
    assert stats['max_ancestry_height']==5
    csvsave('fib_routes_all_84.csv',rows,['i','j','F_i','F_j','length','labels','states'])
    csvsave('fib_pairs_all_84.csv',pairs,['i','j','source','target','min_distance','max_length','total_routes'])
    csvsave('fib_ancestry_84.csv',profiles,['j','F_j','one_step','ancestry_height',
           'distinct_ancestor_nodes','total_nonempty_ancestral_routes',
           'terminal_squarefree_roots','roots','route_counts_by_length'])
    controls={}
    for name,vals in [('Lucas',lucas(LIMIT)),('Fibonacci_plus_1',[n+1 for n in F])]:
        cr,cp,pr,cs=build_indexed(vals,LIMIT)
        controls[name]={'stats':cs,'pairs':cp,
            'routes':[{'i':r['i'],'j':r['j'],'length':r['length'],
                       'labels':r['labels'],'states':r['states']} for r in cr]}
    (OUT/'controls_84.json').write_text(json.dumps(controls,indent=2)+'\n',encoding='utf-8')
    special={n:next(p for p in profiles if p['j']==n) for n in (6,12,24,48,72,84)}
    summary={'release':'FUG-I_v002','scope':'exact all-depth directed T_N routes, indexed Fibonacci n=1..84',
       'limit':LIMIT,'F_84':F[84], 'route_stats':stats,
       'fibonacci_pair_results':pairs,'selected_ancestry_layers':special,
       'controls':{k:v['stats'] for k,v in controls.items()},
       'complete_depth_algorithm':'reverse predecessor closure until squarefree roots',
       'factorization':'deterministic 64-bit Miller-Rabin witnesses, rho split, product certification'}
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    make_svg(rows,BASE/'figures'/'ancestry_144.svg','Complete backward-ancestry graph of F12 = 144')
    print('FUG-I Phase 2 complete exact run: PASS')
    print('Fibonacci indices:',LIMIT,'largest target:',F[84])
    print('All-depth reachable endpoint pairs:',stats['distinct_pairs'])
    print('All-depth route count:',stats['total_routes'],'depth histogram:',stats['routes_by_length'])
    print('Maximum actual Fibonacci-target backward depth:',stats['max_ancestry_height'])
    print('Lucas controls:',controls['Lucas']['stats']['distinct_pairs'],controls['Lucas']['stats']['total_routes'])
    print('Fibonacci+1 controls:',controls['Fibonacci_plus_1']['stats']['distinct_pairs'],controls['Fibonacci_plus_1']['stats']['total_routes'])
    print('Output directory:',OUT)

if __name__=='__main__':run()

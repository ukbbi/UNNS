"""Verify exported census, exact matching, witnesses and release byte hashes."""
import csv,json,hashlib
from collections import defaultdict
from run_sib import ROOT,BOUND,backward,signature,panel

def read(name):
    with (ROOT/'results'/name).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))

def main():
    checks=0
    def check(b):
        nonlocal checks
        assert b;checks+=1
    census=read('integer_census.csv');check(len(census)==BOUND)
    byx={int(r['value']):r for r in census}
    for x,r in byx.items():
        routes=backward(x);groups=defaultdict(list)
        for s,w in routes:groups[s].append(w)
        perm=diff=0
        for ws in groups.values():
            for i,a in enumerate(ws):
                for b in ws[i+1:]:
                    if sorted(a)==sorted(b):perm+=1
                    else:diff+=1
        check(int(r['routes'])==len(routes))
        check(int(r['incoming'])==sum(len(w)==1 for _,w in routes))
        check(int(r['depth2'])==sum(len(w)==2 for _,w in routes))
        check(int(r['sources'])==len(groups))
        check(int(r['permutation_pairs'])==perm)
        check(int(r['different_content_pairs'])==diff)
        check(int(r['merger_sources'])==sum(len(w)>1 for w in groups.values()))
        check(r['signature']==('.'.join(map(str,signature(x))) or 'unit'))
        check(int(r['max_depth'])==max((len(w) for _,w in routes),default=0))
    for row in read('different_witnesses.csv'):
        a=json.loads(row['word_a']);b=json.loads(row['word_b']);check(sorted(a)!=sorted(b))
        for w in (a,b):check((int(row['source']),tuple(w)) in backward(int(row['target'])))
    for k in range(12):check(int(byx[2**k]['different_content_pairs'])==0)
    check(int(byx[4096]['different_content_pairs'])>0)
    for w in ((6,7,7),(3,2,3,3)):check((6,w) in backward(4096))
    pools={(r['sequence'],int(r['value'])):json.loads(r['pool']) for r in read('control_pools.csv')}
    observed={n:set(x for i,x in t) for n,t in panel().items()}
    for row in read('matched_controls.csv'):
        name=row['sequence'];x=int(row['value']);pool=pools[(name,x)]
        expected=[y for y in range(1,BOUND+1) if y not in observed[name] and signature(y)==signature(x) and y.bit_length()==x.bit_length()]
        check(pool==expected);check(len(pool)==int(row['pool_size']))
        for key in ('incoming','depth2','routes','merger_sources','different_content_pairs'):
            check(int(row[key])==int(byx[x][key]))
            if pool:check(abs(float(row['control_'+key])-sum(int(byx[y][key]) for y in pool)/len(pool))<1e-12)
            else:check(row['control_'+key]=='')
    s=json.loads((ROOT/'results'/'summary.json').read_text())
    for name,terms in panel().items():
        check(s['families'][name]['unique_count']==len(set(x for i,x in terms)))
    check(not any(pools[('powers2',2**k)] for k in range(2,13)))
    manifest=ROOT/'MANIFEST.json'
    if manifest.exists():
        for name,digest in json.loads(manifest.read_text())['sha256'].items():
            check(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest)
    print(json.dumps(dict(status='PASS',export_checks=checks,all_depth_targets=BOUND)))

if __name__=='__main__':main()

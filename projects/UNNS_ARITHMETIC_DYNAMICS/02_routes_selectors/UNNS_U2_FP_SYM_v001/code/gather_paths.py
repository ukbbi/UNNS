import json,glob
import fibsearch2
paths={}
d=json.load(open('../data/fibonacci_identities_raw.json'))
for key in ('4','7','10'):
    paths[int(key)]=dict(P=12,r=int(key),steps=d[key]['raw'],nf=d[key]['nf'],source="fibparam (x,y vocabulary)")
for r in (2,3,6,8):
    res=fibsearch2.search2(12,r,8); paths[r]=dict(P=12,r=r,steps=res['steps'],nf=res['nf'],source="fibsearch2 K=8")
for f in glob.glob('../reports/deep_[ab].log'):
    for l in open(f):
        if l.startswith('{'):
            res=json.loads(l)
            if res.get('length'): paths[res['r']]=dict(P=12,r=res['r'],steps=res['steps'],nf=res['nf'],source="fibsearch2 K=10")
json.dump({str(k):v for k,v in sorted(paths.items())},open('../data/class_paths.json','w'),indent=1)
print(sorted(paths), {k:len(v['steps']) for k,v in sorted(paths.items())})

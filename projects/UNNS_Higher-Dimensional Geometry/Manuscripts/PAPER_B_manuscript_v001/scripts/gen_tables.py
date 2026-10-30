#!/usr/bin/env python3
"""Writes tex/gen_data.tex (macros + table bodies) and logs/data_summary.json from logs/*.json and the staged certificates."""
import json, collections
from geo2 import *
L=lambda f: json.load(open('../logs/'+f))
cl=L('classify.json'); sp=L('small_p.json')
c6=json.load(open('../src/certificates/C6_rank6.json'))
out=[]
def prof(m):
    c=collections.Counter(m); return ''.join('%d^{%d}'%(a,c[a]) if True else '' for a in sorted(c)) if False else ','.join('%d^{%d}'%(a,c[a]) for a in sorted(c))
# table k=3,4,5
rows=[]
G={3:24,4:1344,5:322560}
for k in (3,4,5):
    for i in cl['k%d'%k]['info']:
        rows.append('$%d$ & $%d$ & $%d$ & $%s$ & $%d$ & $%d$\\\\'%(k,i['p'],i['n2'],prof(i['m']).replace(',',',\\,'),i['orbit_size'],G[k]//i['orbit_size']))
out.append('\\newcommand{\\classtablebody}{%s}'%'\n'.join(rows))
# k=6 summary from own recomputation
byp=collections.defaultdict(list)
rec=[]
for c in c6:
    X=c['support']; Cw=set(code_from_points(X)[0].values()); cs=circuits_of(Cw); parts=one_partitions(cs,len(X))
    n2=n2_count(parts); byp[len(X)].append(n2); rec.append((len(X),n2,sorted(len(P) for P in parts)))
rows=[]
for p in sorted(byp):
    v=byp[p]; rows.append('$%d$ & $%d$ & $%d$ & $%d$\\\\'%(p,len(v),min(v),max(v)))
out.append('\\newcommand{\\ksixtablebody}{%s}'%'\n'.join(rows))
out.append('\\newcommand{\\ksixtotal}{%d}'%len(c6))
# small p table
rows=[]
for key,v in sp.items():
    if v['p']<=8 and v['minimal']>0 or True:
        rows.append('$%d$ & $%d$ & $%d$ & $%d$ & $%d$ & %s\\\\'%(v['p'],v['k'],v['candidates'],v['nonembedded'],v['minimal'],('$%d$'%v['min_n2']) if v['min_n2'] is not None else '---'))
rows.sort(key=lambda r:(int(r.split('&')[0].strip('$ ')),int(r.split('&')[1].strip('$ '))))
out.append('\\newcommand{\\smallptablebody}{%s}'%'\n'.join(rows))
open('../tex/gen_data.tex','w').write('\n'.join(out)+'\n')
json.dump(dict(k6=[(a,b,c) for a,b,c in rec]),open('../logs/k6_records.json','w'))
print('ok')

# ---------------------------------------------------------------- extra tables (identities, witnesses, types)
import itertools
def setstr(w,n): return '\\{'+','.join(str(i+1) for i in range(n) if w>>i&1)+'\\}'
rows=[]; wrows=[]
for k in (3,4,5):
    for idx,i in enumerate(cl['k%d'%k]['info']):
        X=i['rep']; n=len(X)
        Cw=set(code_from_points(X)[0].values()); cs=circuits_of(Cw); parts=one_partitions(cs,n)
        cnt=collections.Counter(len(P) for P in parts)
        lhs=sum((1<<len(P))-2 for P in parts)
        pars=sum((1<<len(P))*sum(weight(b)**2 for b in P)-2*n*n for P in parts)
        rows.append('$%d$ & $%d$ & $%s$ & $%d=%d$ & $%d=%d$\\\\'%(k,n,','.join('%d^{%d}'%(m,cnt[m]) for m in sorted(cnt)),lhs,(1<<k)-2,pars,n*((1<<k)-2*n)))
        tw=[P for P in parts if len(P)==2]
        P,Q=tw[0],tw[1]
        sp1=span_words(list(P)); sp2=span_words(list(Q))
        x=next(w for w in sorted(Cw) if w not in sp1 and w not in sp2)
        r=collision_rank((tuple(sorted(P)),x),(tuple(sorted(Q)),x),n)
        assert r==3
        wrows.append('$%d$ & $%d$ & $%s\\,|\\,%s$ & $%s\\,|\\,%s$ & $%s$ & $%d$\\\\'%(k,n,setstr(P[0],n),setstr(P[1],n),setstr(Q[0],n),setstr(Q[1],n),setstr(x,n),r))
out2=['\\newcommand{\\identitytablebody}{%s}'%'\n'.join(rows),'\\newcommand{\\witnesstablebody}{%s}'%'\n'.join(wrows)]
# types table
trows=[]
typ={3:collections.Counter(),4:collections.Counter(),5:collections.Counter(),6:collections.Counter()}
for k in (3,4,5):
    for i in cl['k%d'%k]['info']:
        c=collections.Counter(i['m']); typ[k][tuple((m-1,c[m]) for m in sorted(c))]+=1
for (p,n2,ms) in rec:
    c=collections.Counter(ms); typ[6][tuple((m-1,c[m]) for m in sorted(c))]+=1
for k in (3,4,5,6):
    for t,v in sorted(typ[k].items(), key=lambda kv:(-kv[1],kv[0])):
        trows.append('$%d$ & $[%s]$ & $%d$\\\\'%(k,'\\,'.join('%d^{%d}'%(d,c) for d,c in t),v))
out2.append('\\newcommand{\\typestablebody}{%s}'%'\n'.join(trows))
open('../tex/gen_data.tex','a').write('\n'.join(out2)+'\n')
print('extra ok')

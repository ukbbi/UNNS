import sys, os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from paths import *
import sys; sys.path.insert(0,'.')
from program_table import program
rows,fin,nt=program(0,0)
def aff(c0,c1):
    if c1==0: return f'{c0:,}'.replace(',','\\,')
    return f'{c0:,}'.replace(',','\\,')+f'+{c1}t'
out=[]; i=0; k=1
items=[]
# merge plain runs of >=2 consecutive plain single moves that are not long blocks
cur=None
for r in rows:
    plain=(r['c']==1 and r['s']==0 and len(r['word'])==1)
    if plain:
        if cur is None: cur=dict(kind='plain',words=[r['word'][0]],before=r['before'],nobl=r['nobl'])
        else: cur['words'].append(r['word'][0]); cur['nobl']+=r['nobl']
    else:
        if cur: items.append(cur); cur=None
        items.append(dict(kind='block',word=r['word'],c=r['c'],s=r['s'],before=r['before'],nobl=r['nobl']))
if cur: items.append(cur)
lines=[]
for n,it in enumerate(items,1):
    if it['kind']=='plain':
        mv=','.join(map(str,it['words'])); 
        if len(it['words'])>3: mvs=f"connector ({len(it['words'])} moves)"
        else: mvs=f'${mv}$'
        rep='1'
    else:
        w=it['word']
        if len(w)==45: mvs='$W_{45}$'
        elif len(w)==11: mvs='$W_{11}$'
        else: mvs='$'+str(w[0])+'$'
        rep='$'+(aff(it['c'],it['s']))+'$'
    b=it['before']
    st=' & '.join('$'+aff(*x)+'$' for x in b)
    lines.append(f"{n} & {mvs} & {rep} & {st} & {it['nobl']} \\\\")
open(TABD+'/worked00_rows.tex','w').write('\n'.join(lines)+'\n')
print('\n'.join(lines)); print(sum(it['nobl'] for it in items))

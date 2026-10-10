#!/usr/bin/env python3
"""Generate exact frozen-v005 geometry/model instance; real 4x4 explicitly forbidden without authorization."""
import argparse, hashlib, json, pathlib
from physical_energy_v005 import source_geometry,vertex_positions,incident_islands,K_pairs
p=argparse.ArgumentParser()
p.add_argument('--size',type=int,choices=(1,2,3,4),required=True)
p.add_argument('--output',required=True)
p.add_argument('--authorize-real',action='store_true')
a=p.parse_args()
if a.size==4 and not a.authorize_real:
    p.error('BLOCKED real 4x4 instance: requires explicit --authorize-real AFTER separate run authorization')
ins=source_geometry(a.size);vs=vertex_positions(a.size);incident=incident_islands(ins,vs)
n=len(ins)
assert n<=63 and len(incident)==a.size**2 and all(len(x)==4 for x in incident)
pairs=K_pairs(ins)
k={(i,j):v for i,j,v in pairs}
lines=[f'{n} {len(vs)}']
lines += [format(k[(i,j)],'.17g') for i in range(n) for j in range(i+1,n)]
for v,idx in zip(vs,incident):
    mask=sum(1<<i for i in idx)
    plusin=0
    for i in idx:
        isle=ins[i]
        dp=(v[0]-isle.x)*isle.ux+(v[1]-isle.y)*isle.uy
        assert abs(dp)>1e-6
        if dp>0:plusin|=1<<i
    lines.append(f'{mask} {plusin}')
out=pathlib.Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
out.write_text('\n'.join(lines)+'\n')
print(json.dumps({'size':a.size,'spins':n,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'path':str(out)}))

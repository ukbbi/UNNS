#!/usr/bin/env python3
"""Independent Yee FDTD solver for time-modulated transverse Maxwell 1D.
No use of spectral RK4 or its functions; validates spatial/time discretization separately.
"""
from __future__ import annotations
import json, math, sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]

def yee(q1=6,q2=28,start=2,eta=.009,stage=1.7,nx=2048,dt_target=.0008):
    total=2*stage
    steps=round(total/dt_target);dt=total/steps
    dz=2*np.pi/nx
    if dt>=dz: raise ValueError('Yee CFL unstable')
    z=np.arange(nx)*dz
    zh=z+dz/2
    D=np.exp(1j*start*z).astype(complex)
    Bh=np.exp(1j*start*(zh+dt/2)).astype(complex) # time -dt/2 stagger
    def env(t,a,b):
        return math.sin(math.pi*(t-a)/(b-a))**2 if a<t<b else 0.0
    def amps(D,Bcent,indices):
        d=np.fft.fft(D)/nx
        b=np.fft.fft(Bcent)/nx
        out={}
        for m in indices:
            B_m=b[m]*np.exp(-1j*m*dz/2)
            out[str(m)]=float(abs((d[m]+B_m)/2))
        return out
    midway=None
    for j in range(steps):
        t=j*dt
        f1=env(t,0.,stage)
        f2=env(t,stage,2*stage)
        eps=1.+2*eta*(f1*np.cos(q1*(z-t))+f2*np.cos(q2*(z-t)))
        E=D/eps
        Bnext=Bh-(dt/dz)*(np.roll(E,-1)-E)
        Dnext=D-(dt/dz)*(Bnext-np.roll(Bnext,1))
        if j+1==steps//2:
            midway=amps(Dnext,(Bh+Bnext)/2,[start,start+q1,start+q2,start+q1+q2,9,36,38])
        Bh=Bnext;D=Dnext
    # At final time, epsilon=1 and D=E
    Bprior=Bh.copy()
    # Need B at t+dt/2 to interpolate B(t) from B(t-dt/2) and B(t+dt/2)
    Bafter=Bh-(dt/dz)*(np.roll(D,-1)-D)
    final=amps(D,(Bprior+Bafter)/2,[start,start+q1,start+q2,start+q1+q2,9,36,38])
    return {'scheme':'Yee staggered FDTD independent of pseudospectral RK4', 'nx':nx,'dt':dt,
             'first_q':q1,'second_q':q2,'start':start,'eta':eta,'stage_duration':stage,
             'after_stage_1':midway,'after_stage_2':final}

if __name__=='__main__':
    p=ROOT/'results'/'heldout_raw.json'
    if not p.exists(): raise RuntimeError('Run run_v009.py first')
    raw=json.loads(p.read_text())['cases']
    a=yee()
    b=yee(q1=28,q2=6)
    c=yee(start=4)
    out={}
    for tag,case,fd,targets in [
       ('A_forward',raw['A_forward'],a,[8,36,9]),
       ('reverse_nonUNNS',raw['reverse_nonUNNS'],b,[30,36,9]),
       ('matched_nonUNNS_target',raw['matched_nonUNNS_target'],c,[10,38])]:
        vals=[]
        for m in targets:
            p1=case['outgoing']['after_stage_2'][str(m)]['amplitude']
            p2=fd['after_stage_2'][str(m)]
            if p1>1e-5:
                rel=abs(p2-p1)/p1
                if rel>=0.035:raise AssertionError(f'FDTD vs RK4 amplitude mismatch at {tag}, m{m}: {rel}')
                vals.append({'m':m,'RK4':p1,'Yee':p2,'relative_error':rel})
            else:
                if p2>5e-9:raise AssertionError(f'forbidden mode leakage at {tag}, m{m}: {p2}')
                vals.append({'m':m,'RK4':p1,'Yee':p2,'note':'symmetry-suppressed'})
        out[tag]={'comparison':vals,'fdtd':fd}
        print(tag,', '.join(f"m{v['m']}={v['Yee']:.8g}" for v in vals),'PASS')
    (ROOT/'results'/'independent_fdtd.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print('MUG-I v009 INDEPENDENT FDTD PASS')

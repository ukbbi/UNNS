#!/usr/bin/env python3
"""Optional distinct-parameter Maxwell controls of the proved fixed-medium no-go.

All eigenstates are newly computed, not reused from v007 numerical tables.
Requires numpy and scipy.
"""
import csv
from pathlib import Path
import numpy as np
from scipy.linalg import eigh

root=Path(__file__).resolve().parents[1]
# Fresh parameter combinations, all strict whole-field admissible with N | q.
cases=((4,0.08,1),(6,0.10,2),(8,0.14,1),(12,0.06,3),(7,0.12,1))
rows=[]
for q,delta,N in cases:
    m=np.arange(-(120//q),120//q+1,dtype=int)*q
    A=np.diag(m.astype(float)**2)
    B=np.eye(len(m))
    for i in range(len(m)-1):B[i,i+1]=B[i+1,i]=delta
    ew,V=eigh(A,B)
    choices=[]
    for i,lam in enumerate(ew):
        if lam<1e-8:continue
        weights={}
        for mi,ci in zip(m,V[:,i]):
            weights[abs(int(mi))]=weights.get(abs(int(mi)),0)+ci*ci
        if max(weights,key=weights.get)==q:
            choices.append((float(lam),V[:,i]))
    assert choices,(q,delta)
    lam,v=min(choices,key=lambda t:t[0]); r=(N+1)**2/N
    assert np.allclose(r*m,np.round(r*m))
    z=np.linspace(0,2*np.pi,2048,endpoint=False)
    e=np.exp(1j*np.outer(z,r*m))
    y=e@v
    lhs=e@((r*m)**2*v)
    fixed=1+2*delta*np.cos(q*z)
    cdil=1+2*delta*np.cos(q*r*z)
    b=fixed*y
    lfit=(np.vdot(b,lhs)/np.vdot(b,b)).real
    rho_fixed=float(np.linalg.norm(lhs-lfit*b)/np.linalg.norm(lhs))
    rho_cdil=float(np.linalg.norm(lhs-r*r*lam*cdil*y)/np.linalg.norm(lhs))
    assert rho_fixed>0.02 and rho_cdil<1e-8,(q,delta,N,rho_fixed,rho_cdil)
    rows.append(dict(q=q,delta=delta,N=N,r=f'{r:.12g}',omega_squared=f'{lam:.12g}',
                     fixed_medium_relative_residual=f'{rho_fixed:.12g}',
                     codilating_medium_relative_residual=f'{rho_cdil:.12g}'))
path=root/'results'/'spectral_controls.csv'
with path.open('w',newline='',encoding='utf8') as f:
    writer=csv.DictWriter(f,list(rows[0]));writer.writeheader();writer.writerows(rows)
print('PASS held-out scalar Maxwell eigenstate controls:',len(rows))
for x in rows:
    print(' ',x['q'],x['delta'],x['N'],x['fixed_medium_relative_residual'],x['codilating_medium_relative_residual'])

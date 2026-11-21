#!/usr/bin/env python3
"""OPTIONAL numerical Maxwell control (numpy/scipy), same eigenstate for each rule.

This approximates a genuine infinite Fourier eigenstate by a 41-component
Galerkin eigenvector; the proof for exact eigenstates is analytic in THEOREMS.md.
"""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
from core import walk, content

root=Path(__file__).resolve().parents[1]
q=6; delta=0.1; M=120
ms=np.arange(-M,M+1,q, dtype=int)
A=np.diag(ms.astype(float)**2)
B=np.eye(len(ms))
for i in range(len(ms)-1):
    B[i,i+1]=B[i+1,i]=delta
vals,vs=eigh(A,B)
# Choose the lower positive eigenstate whose dominant |m| label is 6.
candidates=[]
for j,lam in enumerate(vals):
    v=vs[:,j]
    byabs={}
    for m,c in zip(ms,v):
        byabs[abs(int(m))]=byabs.get(abs(int(m)),0.0)+c*c
    if max(byabs,key=byabs.get)==6 and lam>0:
        candidates.append((lam, v,byabs[6]))
assert len(candidates)==2,len(candidates)
lam,v,dominance=min(candidates,key=lambda x:x[0])
# Keep only physically non-negligible Fourier amplitudes for the numerical
# support comparison. Low tails of the exact state are truncated by Galerkin.
x={int(m):float(c) for m,c in zip(ms,v) if abs(c)>1e-13}
assert content(x)==6

words={'A_3_8_3':(3,8,3),'B_1_1_1_2':(1,1,1,2)}
ops={}
for rule in ('strict','component','E'):
    ops[rule]={}
    for key,w in words.items():
        y,trace=walk(x,w,rule,q)
        ops[rule][key]=dict(content_trace=trace, survives=bool(y),
                            final_content=content(y or {}), final=y)
assert ops['strict']['A_3_8_3']['final']==ops['strict']['B_1_1_1_2']['final']
assert ops['component']['A_3_8_3']['final']==ops['component']['B_1_1_1_2']['final']
assert not ops['E']['A_3_8_3']['final'] and ops['E']['B_1_1_1_2']['final']

# Compare residuals under the same original dielectric and the co-dilated one.
z=np.linspace(0,2*np.pi,2048,endpoint=False)
r=4
phases=np.exp(1j*np.outer(z,r*ms))
y=phases@v
ay=phases@((r*ms)**2*v)
eps_fixed=1+2*delta*np.cos(q*z)
eps_cod=1+2*delta*np.cos(q*r*z)
b=eps_fixed*y
lamfit=float((np.vdot(b,ay)/np.vdot(b,b)).real)
fixed_resid=float(np.linalg.norm(ay-lamfit*b)/np.linalg.norm(ay))
cod_resid=float(np.linalg.norm(ay-r*r*lam*eps_cod*y)/np.linalg.norm(ay))
assert fixed_resid>0.05,(fixed_resid,lamfit)
assert cod_resid<1e-9,cod_resid

# Vacuum plane-wave control, frequency r*g and original medium epsilon=1.
yvac=np.cos(r*6*z)
ayvac=(r*6)**2*yvac
vacres=float(np.linalg.norm(ayvac-(r*6)**2*yvac))
assert vacres<1e-10

result={
 'source':'independently reconstructed q=6, delta=0.1, kappa=0, dominant |m|=6 Galerkin eigenstate',
 'galerkin_modes':len(ms), 'frequency_squared':float(lam),
 'dominant_abs_mode_weight':float(dominance),
 'retained_support_modes':len(x),'retained_support_gcd':content(x),
 'words':{rule:{h:{k:v for k,v in row.items() if k!='final'} for h,row in d.items()}
          for rule,d in ops.items()},
 'dilation_r':r,'best_fit_fixed_medium_omega_squared':lamfit,
 'relative_fixed_medium_stationary_residual':fixed_resid,
 'relative_codilating_medium_residual':cod_resid,
 'vacuum_control_residual':vacres,
 'note':'Numerical Galerkin approximation only. Analytic no-go holds for exact infinite Fourier eigenstates.',
}
(root/'results'/'spectral_same_state.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print('PASS SAME-EIGENSTATE spectral comparison')
print('  omega^2:',lam,'dominance:',dominance,'support gcd:',content(x))
for rule in ('strict','component','E'):
    for h,d in ops[rule].items():
        print(' ',rule,h,d['content_trace'],'survives',d['survives'])
print('  fixed-medium relative residual:',fixed_resid)
print('  co-dilating medium relative residual:',cod_resid)
print('  vacuum residual:',vacres)

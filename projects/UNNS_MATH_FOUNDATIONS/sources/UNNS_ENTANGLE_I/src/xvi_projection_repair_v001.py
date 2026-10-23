"""XVI PROJECTION REPAIR v001: matched finite-grid Helmholtz projectors.

An INDEPENDENT candidate; DOES NOT MODIFY canonical Chamber XVI v0.8.4.
Requires numpy for FFT computations. Audit status concerns flux P, NOT tau evolution
and NOT any quantum observable probability measure.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

try:
    import numpy as np
except ImportError as err:
    raise SystemExit('NumPy required. Install via: python -m pip install -r requirements_XVI_REPAIR_v001.txt') from err

ROOT = Path(__file__).resolve().parents[1]
N_LIST = (64, 128, 256)
SEED_LIST = (41, 137)
TOL = {'div_rel': 1e-10, 'idem_rel': 1e-10,
       'energy_rel': 1e-10, 'orthog_rel': 1e-10, 'adjoint_rel': 1e-10}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_lock(project=ROOT):
    lock = json.loads((project / 'config/XVI_REPAIR_LOCK_v001.json').read_text('utf-8'))
    checks = {}
    for name, x in lock['inputs'].items():
        path = project / x['path']
        actual = sha256(path) if path.is_file() else None
        checks[name] = {'path': x['path'], 'expected_sha256': x['sha256'],
                        'actual_sha256': actual, 'pass': actual == x['sha256']}
    active = project / 'output/XVI_CANONICAL_BRIDGE_v001.json'
    if active.exists():
        checks['active_bridge'] = {'path': 'output/XVI_CANONICAL_BRIDGE_v001.json',
            'expected_sha256': lock['inputs']['frozen_bridge']['sha256'],
            'actual_sha256': sha256(active),
            'pass': sha256(active) == lock['inputs']['frozen_bridge']['sha256']}
    return {'all_pass': all(v['pass'] for v in checks.values()), 'checks': checks}


def derivative_symbols(n: int, kind: str):
    if not isinstance(n,int) or n<8 or n%2:
        raise ValueError('Need an even periodic grid, N >= 8')
    freq = np.fft.fftfreq(n)
    theta = 2*math.pi*freq
    if kind == 'central_source':
        # The original divergence uses grid_scale = pi / N times +/- neighbor.
        # Preserve it EXACTLY in D; a matching gradient is G=-D*.
        d = 1j*(2*math.pi/n)*np.sin(theta)
        # Central differences cannot see Nyquist/checkerboard components.
        d[n//2] = 0j
    elif kind == 'forward_volume':
        # Periodic forward divergence, backward gradient, 2pi physical domain.
        dx = 2*math.pi/n
        d = np.expm1(1j*theta)/dx
    else:
        raise ValueError('Unknown derivative kind: '+kind)
    dxhat = np.broadcast_to(d[None,:], (n,n)).copy()
    dyhat = np.broadcast_to(d[:,None], (n,n)).copy()
    gxhat, gyhat = -np.conj(dxhat), -np.conj(dyhat)
    denom = np.abs(dxhat)**2 + np.abs(dyhat)**2
    return dxhat, dyhat, gxhat, gyhat, denom


def checked_fields(jx,jy):
    x,y=np.asarray(jx),np.asarray(jy)
    if x.ndim!=2 or x.shape!=y.shape or x.shape[0]!=x.shape[1]:
        raise ValueError('Jx and Jy must be equally sized 2D square arrays')
    if x.shape[0]%2 or x.shape[0]<8 or not np.isfinite(x).all() or not np.isfinite(y).all():
        raise ValueError('Require finite fields and even N>=8')
    return x.astype(float,copy=False), y.astype(float,copy=False)


def central_divergence_spatial(jx,jy):
    x,y = checked_fields(jx,jy)
    scale = math.pi/len(x)
    return scale*(np.roll(x,-1,axis=1)-np.roll(x,1,axis=1)
                  +np.roll(y,-1,axis=0)-np.roll(y,1,axis=0))


def divergence(jx,jy,kind='central_source'):
    x,y=checked_fields(jx,jy)
    d1,d2,_,_,_=derivative_symbols(len(x),kind)
    return np.fft.ifft2(d1*np.fft.fft2(x)+d2*np.fft.fft2(y)).real


def gradient(phi,kind='central_source'):
    a=np.asarray(phi)
    if a.ndim!=2 or a.shape[0]!=a.shape[1] or a.shape[0]%2 or a.shape[0]<8:
        raise ValueError('scalar grid must be even N>=8')
    _,_,g1,g2,_=derivative_symbols(len(a),kind)
    phat=np.fft.fft2(a)
    return np.fft.ifft2(g1*phat).real, np.fft.ifft2(g2*phat).real


def project(jx,jy,kind='central_source'):
    """Orthogonal projection onto ker(D), with null modes LEFT UNCHANGED.

    D: vector -> scalar; G = -D* (with periodic normalization).
    Solve (DG) psi = D(J), modewise Moore-Penrose inverse,
    J* = J - G psi. DG = -D D*, so psi=-DJ / (|Dx|²+|Dy|²).
    """
    x,y=checked_fields(jx,jy)
    dhx,dhy,ghx,ghy,den=derivative_symbols(len(x),kind)
    xhat,yhat=np.fft.fft2(x),np.fft.fft2(y)
    divhat=dhx*xhat+dhy*yhat
    psihat=np.zeros_like(divhat)
    live=den>1e-26
    psihat[live]=-divhat[live]/den[live]
    projected_x=np.fft.ifft2(xhat-ghx*psihat)
    projected_y=np.fft.ifft2(yhat-ghy*psihat)
    potential=np.fft.ifft2(psihat)
    max_imag=max(float(np.max(np.abs(projected_x.imag))),
                 float(np.max(np.abs(projected_y.imag))),
                 float(np.max(np.abs(potential.imag))))
    if max_imag>1e-8: raise RuntimeError('Conjugate symmetry lost')
    return projected_x.real, projected_y.real, potential.real


def vdot(x1,y1,x2,y2):
    return float(np.mean(x1*x2+y1*y2))


def vnorm(x,y):
    return math.sqrt(max(0.,vdot(x,y,x,y)))


def rms(x):
    return float(np.sqrt(np.mean(x*x)))


def source_flux(n,seed=41):
    # Bandlimited analytic fields: independent reproducible mixed divergence/vorticity.
    rr=np.random.default_rng(seed)
    a,b,c=rr.uniform(0.65,1.2,3)
    y,x=np.meshgrid(np.arange(n)*2*math.pi/n,np.arange(n)*2*math.pi/n,indexing='ij')
    jx=a*np.sin(2*x+y)+0.5*np.cos(3*y-x)+c*np.sin(4*x-2*y)+0.17
    jy=b*np.cos(x+2*y)+0.65*np.sin(3*x-y)+0.31*np.cos(y)+0.29
    return jx,jy


def adjoint_defect(n,kind,seed=41):
    jx,jy=source_flux(n,seed)
    y,x=np.meshgrid(np.arange(n)*2*math.pi/n,np.arange(n)*2*math.pi/n,indexing='ij')
    phi=0.7*np.sin(3*x-y)+0.2*np.cos(x+2*y)
    d=divergence(jx,jy,kind)
    gx,gy=gradient(phi,kind)
    # For G = - D*: <D J,phi> + <J,G phi> = 0
    resid=float(np.mean(d*phi))+vdot(jx,jy,gx,gy)
    return abs(resid)/(rms(d)*rms(phi)+vnorm(jx,jy)*vnorm(gx,gy)+1e-30)


def certify_case(n,seed,kind):
    jx,jy=source_flux(n,seed)
    px,py,psi=project(jx,jy,kind)
    px2,py2,_=project(px,py,kind)
    d0=rms(divergence(jx,jy,kind))
    d1=rms(divergence(px,py,kind))
    rx,ry=jx-px,jy-py
    orig_energy=vdot(jx,jy,jx,jy)
    p_energy=vdot(px,py,px,py)
    rem_energy=vdot(rx,ry,rx,ry)
    report={'N':n,'seed':seed,'method':kind,'before_div_rms':d0,'after_div_rms':d1,
        'divergence_relative':d1/(d0+1e-30),
        'idempotence_relative':vnorm(px2-px,py2-py)/(vnorm(px,py)+1e-30),
        'energy_identity_relative':abs(orig_energy-p_energy-rem_energy)/(orig_energy+1e-30),
        'orthogonality_relative':abs(vdot(px,py,rx,ry))/(math.sqrt(p_energy*rem_energy)+1e-30),
        'adjoint_relative':adjoint_defect(n,kind,seed),
        'rms_correction_potential':rms(psi),
        'zero_mode_unchanged':abs(float(np.mean(jx-px)))<1e-11 and abs(float(np.mean(jy-py)))<1e-11}
    report['pass']=(d0>1e-5 and all(report[k]<=TOL[t]
                  for k,t in [('divergence_relative','div_rel'),('idempotence_relative','idem_rel'),
                              ('energy_identity_relative','energy_rel'),('orthogonality_relative','orthog_rel'),
                              ('adjoint_relative','adjoint_rel')]) and report['zero_mode_unchanged'])
    return report


def single_mode_original_vs_repair(project_dir=ROOT):
    # SAME physical array is supplied to the original engine and the repair.
    # Original engine numerical observations are from a direct execution of
    # unchanged source, captured in source-locked JS comparator JSON.
    record=json.loads((project_dir/'output/XVI_ORIGINAL_JS_REPAIR_COMPARATOR_v001.json').read_text('utf-8'))
    locked=json.loads((project_dir/'config/XVI_REPAIR_LOCK_v001.json').read_text('utf-8'))
    if record['sha256']!=locked['inputs']['engine']['sha256']:
        raise RuntimeError('JS comparator source does not match original engine')
    cases=[]
    for item in record['results']:
        n=item['N']; x=np.arange(n)[None,:]
        jx=np.broadcast_to(np.sin(2*math.pi*x/n),(n,n)).copy()
        jy=np.zeros_like(jx)
        bx=rms(divergence(jx,jy,'central_source'))
        px,py,_=project(jx,jy,'central_source')
        after=rms(divergence(px,py,'central_source'))
        cases.append({'N':n,'original_js_residual':item['actual_divergence_residual'],
                      'candidate_residual':after/(bx+1e-30),
                      'original_js_orthogonality_cross':item['normalized_orthogonality_cross'],
                      'original_js_energy_defect':item['normalized_energy_decomposition_defect'],
                      'pass':(item['actual_divergence_residual']>0.9 and after/(bx+1e-30)<1e-10)})
    return cases


def physical_reference_project(jx,jy):
    # Only for low-frequency band-limited tests; Nyquist treatment not a general theorem.
    n=len(jx)
    signed=np.fft.fftfreq(n)*n
    kx=np.broadcast_to(signed[None,:],(n,n))
    ky=np.broadcast_to(signed[:,None],(n,n))
    # Real field derivatives have ambiguous Nyquist; declare zero there.
    kx=kx.copy();ky=ky.copy();kx[:,n//2]=0;ky[n//2,:]=0
    den=kx*kx+ky*ky
    xh,yh=np.fft.fft2(jx),np.fft.fft2(jy)
    live=den>0
    longitudinal=np.zeros_like(xh)
    # kx Jx + ky Jy ; the orthogonal projection for each Fourier mode
    longitudinal[live]=(kx[live]*xh[live]+ky[live]*yh[live])/den[live]
    return np.fft.ifft2(xh-kx*longitudinal).real, np.fft.ifft2(yh-ky*longitudinal).real


def continuum_grid_error(n):
    jx,jy=source_flux(n,41)
    rx,ry=physical_reference_project(jx,jy)
    px,py,_=project(jx,jy,'central_source')
    return vnorm(px-rx,py-ry)/(vnorm(rx,ry)+1e-30)


def nyquist_test(n=64):
    x=np.arange(n)[None,:]
    checker=np.broadcast_to((-1.)**x,(n,n)).copy()
    z=np.zeros_like(checker)
    before_source=rms(divergence(checker,z,'central_source'))
    src_x,_,_=project(checker,z,'central_source')
    before_volume=rms(divergence(checker,z,'forward_volume'))
    vol_x,_,_=project(checker,z,'forward_volume')
    return {'central_divergence':before_source,
            'central_preserves_invisible_checkerboard':vnorm(src_x-checker,z),
            'forward_divergence':before_volume,
            'forward_removes_checkerboard':vnorm(vol_x,z)}


def measure_counterexample(n=64):
    # Both are divergence-free, orthonormal with respect to normalized L².
    y,x=np.meshgrid(2*math.pi*np.arange(n)/n,2*math.pi*np.arange(n)/n,indexing='ij')
    ux=np.zeros((n,n));uy=math.sqrt(2)*np.sin(x)
    vx=math.sqrt(2)*np.sin(y);vy=np.zeros((n,n))
    a,b=0.6,0.8
    jx,jy=a*ux+b*vx,a*uy+b*vy
    p_x,p_y,_=project(jx,jy)
    # q=1 & q=2 assign unequal but each normalized weights to SAME closed flux.
    probs={str(q):{'A':a**q/(a**q+b**q),'B':b**q/(a**q+b**q)} for q in (1,2,3)}
    return {'projected_invariance_relative':vnorm(p_x-jx,p_y-jy)/(vnorm(jx,jy)+1e-30),
            'orthogonality_uv':vdot(ux,uy,vx,vy),
            'norm_u':vnorm(ux,uy),'norm_v':vnorm(vx,vy),
            'amplitudes':[a,b],'outcome_weights':probs,
            'interpretation':'One and the same projection-closed field admits multiple separately postulated q-outcome weight assignments; projection alone does not select a probability law.'}


def build_report(project=ROOT):
    lock=source_lock(project)
    if not lock['all_pass']:
        raise RuntimeError('FROZEN_SOURCE_MISMATCH: do not proceed or overwrite baselines')
    cases=[certify_case(n,seed,k) for k in ('central_source','forward_volume')
           for n in N_LIST for seed in SEED_LIST]
    grid_errors=[{'N':n,'relative_error_vs_continuum':continuum_grid_error(n)} for n in N_LIST]
    ny=nyquist_test()
    head=single_mode_original_vs_repair(project_dir=project)
    cm=measure_counterexample()
    allpass=all(x['pass'] for x in cases)
    gridpass=(grid_errors[0]['relative_error_vs_continuum']>
              grid_errors[1]['relative_error_vs_continuum']>
              grid_errors[2]['relative_error_vs_continuum'])
    ny_pass=(ny['central_divergence']<1e-10 and ny['central_preserves_invisible_checkerboard']<1e-10
             and ny['forward_divergence']>0.1 and ny['forward_removes_checkerboard']<1e-10)
    measure_pass=(cm['projected_invariance_relative']<1e-10 and
                  abs(cm['outcome_weights']['1']['A']-cm['outcome_weights']['2']['A'])>0.01)
    verdicts={'L0':'PASS_FROZEN' if lock['all_pass'] else 'FAIL',
              'L1':'PASS_MATCHED_CENTRAL_FLUX' if all(x['pass'] for x in cases if x['method']=='central_source') else 'FAIL',
              'L2':'PASS_FINITE_VOLUME_COMPARATOR' if all(x['pass'] for x in cases if x['method']=='forward_volume') else 'FAIL',
              'L3':'PASS_SMOOTH_GRID_REFINEMENT' if gridpass else 'FAIL',
              'L4':'PASS_NULLSPACE_DISCLOSED' if ny_pass else 'FAIL',
              'L5':'NO_GO_PROJECTION_ALONE' if measure_pass else 'FAIL',
              'L6':'UNPROVED_OBSERVABLE_EVENT_BRIDGE',
              'L7':'UNTESTED_FULL_TAU_EVOLUTION'}
    if not (allpass and gridpass and ny_pass and measure_pass and all(x['pass'] for x in head)):
        raise RuntimeError('CANDIDATE_CERTIFICATION_FAILED: inspect quantitative gates')
    return {'protocol':'XVI_PROJECTION_REPAIR_v001',
       'scope':'Mathematically matched projection of a periodic numerical flux, separate from the unmodified canonical HTML and from quantum probabilities',
       'numpy_version':np.__version__,'input_lock':lock,
       'tolerances':TOL,'tested_methods':['central_source','forward_volume'],
       'tests':cases,'grid_refinement_vs_continuum':grid_errors,
       'nyquist_counterexample':ny,'same_mode_original_vs_repair':head,
       'probability_nonuniqueness_counterexample':cm,
       'gates':verdicts,'primary_verdict':'CANDIDATE_FLUX_PROJECTION_CERTIFIED_IN_TESTED_SCOPE',
       'born_rule':'NOT_DERIVED','physical_tau_evolution':'NOT_CERTIFIED',
       'original_html_modified':False}


def main():
    report=build_report()
    output=ROOT/'output/XVI_PROJECTION_REPAIR_v001.json'
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print('WROTE output/XVI_PROJECTION_REPAIR_v001.json')
    print('FLUX CERTIFIED (tested scope) | CANONICAL UNMODIFIED | MEASURE RULE NOT DERIVED')

if __name__=='__main__':
    main()

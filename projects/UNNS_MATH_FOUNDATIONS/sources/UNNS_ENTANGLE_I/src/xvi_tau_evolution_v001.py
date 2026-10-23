"""Source-grounded nonlinear tau closure audit; NOT a substitute for canonical JS.

Three independent projector variants on the SAME τ evolution and proto-flux.
The original HTML remains unmodified. All outputs are diagnostics, not quantum probabilities.

Run from project root: python -m src.xvi_tau_evolution_v001
Requires earlier src/xvi_projection_repair_v001.py from frozen Phase repair.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import numpy as np
from src import xvi_projection_repair_v001 as repair

ROOT = Path(__file__).resolve().parents[1]
NS = (64, 128, 256)
SEEDS = (41, 137)
METHODS = ('original_emulation', 'central_source', 'forward_volume')
DEFAULT = dict(lam=0.10, beta=2e-6, alpha_c=0.01, gamma=1e-5,
               interval=6, sigma=0.0, anneal_sigma=0.0, steps=180,
               max_abs_tau=1e6, rms_post_div_limit=1e-10, energy_rel_limit=1e-10,
               idem_rel_limit=1e-10, finite_window=180,
               max_rms_growth_factor=5.0, grid_cauchy_limit=0.10)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def source_lock(root=ROOT):
    lock = json.loads((root/'config/XVI_TAU_LOCK_v001.json').read_text('utf-8'))
    results = {}
    for key, entry in lock['inputs'].items():
        path = root/entry['path']
        actual = sha(path) if path.is_file() else None
        results[key] = dict(path=entry['path'], expected=entry['sha256'], actual=actual, pass_=actual==entry['sha256'])
    # Active report check only if present: don't change, don't require or overwrite.
    active = root/'output/XVI_PROJECTION_REPAIR_v001.json'
    if active.is_file():
        results['active_repair'] = dict(path='output/XVI_PROJECTION_REPAIR_v001.json',
            expected=lock['inputs']['frozen_repair']['sha256'],actual=sha(active),
            pass_=sha(active)==lock['inputs']['frozen_repair']['sha256'])
    return {'pass': all(v['pass_'] for v in results.values()), 'checks': results}


def init_tau(n, seed, corpus='smooth'):
    rng = np.random.default_rng(seed)
    if corpus == 'random':
        # independent NumPy seeded stress corpus, NOT Javascript RNG emulation.
        return rng.uniform(0.0, 2*math.pi, (n,n))
    if corpus != 'smooth':
        raise ValueError('corpus must be smooth or random')
    a,b,c=rng.uniform(0.8,1.2,3)
    ph=rng.uniform(-0.35,0.35)
    xy=2*math.pi*np.arange(n)/n
    y,x=np.meshgrid(xy,xy,indexing='ij')
    return (1.4 + a*np.sin(x+ph)*np.cos(2*y) + b*0.30*np.cos(3*x-y)
            + c*0.18*np.sin(2*x+3*y))


def laplacian_source(tau):
    """Precisely the HTML spectral k=(2*pi/N)*integer wavenumber convention."""
    n=len(tau)
    kk=np.fft.fftfreq(n)*n * (2*math.pi/n)
    k2=kk[None,:]**2+kk[:,None]**2
    return np.fft.ifft2(-k2*np.fft.fft2(tau)).real


def source_gradient(tau):
    # Literal HTML source: central neighboring difference divided by two.
    gx=0.5*(np.roll(tau,-1,axis=1)-np.roll(tau,1,axis=1))
    gy=0.5*(np.roll(tau,-1,axis=0)-np.roll(tau,1,axis=0))
    return gx,gy


def proto_flux(tau,gamma):
    tx,ty=source_gradient(tau)
    jx,jy=tau*tx,tau*ty
    if gamma>0:
        kappa=laplacian_source(tau)
        kx,ky=source_gradient(kappa)
        jx-=gamma*kx; jy-=gamma*ky
    return jx,jy


def source_original_project(jx,jy):
    """Port of HTML's mismatched projectFlux (FFT coefficient convention).

    Potential is real inverse FFT of -FFT(div_source)/k_html^2.
    Gradient is real inverse FFT(1j*k_html*potential_hat), same HTML convention.
    This is an isolated Python emulation, not JS runtime verification.
    """
    n=len(jx)
    if len(jy)!=n: raise ValueError('shape mismatch')
    div=repair.central_divergence_spatial(jx,jy)
    kk=np.fft.fftfreq(n)*n * (2*math.pi/n)
    kx,ky=np.broadcast_to(kk[None,:],(n,n)),np.broadcast_to(kk[:,None],(n,n))
    den=kx*kx+ky*ky
    dh=np.fft.fft2(div)
    psh=np.zeros_like(dh)
    mask=den>1e-10
    psh[mask]=-dh[mask]/den[mask]
    psi=np.fft.ifft2(psh).real
    px=np.fft.ifft2(np.fft.fft2(jx) - 1j*kx*psh).real
    py=np.fft.ifft2(np.fft.fft2(jy) - 1j*ky*psh).real
    return px,py,psi


def p_flux(jx,jy,method):
    if method=='original_emulation': return source_original_project(jx,jy)
    if method in ('central_source','forward_volume'):
        return repair.project(jx,jy,method)
    raise ValueError('unknown method')


def rms(a):
    return float(np.sqrt(np.mean(np.asarray(a)**2)))


def finite_metrics(tau):
    gx,gy=source_gradient(tau)
    return {'mean':float(np.mean(tau)),'rms':rms(tau),
       'std':float(np.std(tau)),'max_abs':float(np.max(np.abs(tau))),
       'roughness':math.sqrt(rms(gx)**2+rms(gy)**2)}


def diagnostics(jx,jy,px,py,kind):
    jnorm=max(repair.vnorm(jx,jy),1e-30)
    norm=repair.vnorm(px,py)
    rx,ry=jx-px,jy-py
    before=rms(repair.divergence(jx,jy,kind))
    after=rms(repair.divergence(px,py,kind))
    p2x,p2y,_=p_flux(px,py,'original_emulation' if kind=='original' else kind)
    energy=repair.vdot(jx,jy,jx,jy)
    pen=repair.vdot(px,py,px,py)
    ren=repair.vdot(rx,ry,rx,ry)
    return {'pre_div_rms':before,'post_div_rms':after,
       'relative_divergence':after/max(before,1e-30),
       'physical_forward_div_rms':rms(repair.divergence(px,py,'forward_volume')),
       'projector_idempotence_relative':repair.vnorm(p2x-px,p2y-py)/max(norm,1e-30),
       'energy_decomposition_relative':abs(energy-pen-ren)/max(energy,1e-30),
       'orthogonality_relative':abs(repair.vdot(px,py,rx,ry))/max(math.sqrt(pen*ren),1e-30),
       'source_flux_rms':jnorm}


def step_tau(tau, step_index, method, params):
    # Matching HTML ordering: standard evolution first; the closure operation is
    # applied after evolution at 0-indexed step_count>0 divisible by interval.
    lap=laplacian_source(tau)
    delta=np.roll(tau,-1,axis=1)-tau
    next_tau=tau+params['lam']*np.sin(delta)-params['beta']*lap
    close=(step_index>0 and step_index%params['interval']==0)
    if close:
        jx,jy=proto_flux(next_tau,params['gamma'])
        px,py,psi=p_flux(jx,jy,method)
        dg=diagnostics(jx,jy,px,py,'central_source' if method!='forward_volume' else 'forward_volume')
        dg['potential_rms']=rms(psi)
        # Original sealing update, with no post-hoc scaling of alpha.
        next_tau=next_tau-params['alpha_c']*psi
    else: dg=None
    return next_tau,dg


def run_case(n,seed,method,corpus='smooth',params=None,return_field=False):
    p=dict(DEFAULT);p.update(params or {})
    if p['sigma']!=0 or p['anneal_sigma']!=0:
        raise ValueError('Noisy evolution not yet certified: noise frozen to zero')
    tau=init_tau(n,seed,corpus)
    m0=finite_metrics(tau)
    trace=[]; closures=[]; status='FINITE_WINDOW_COMPLETED'
    for s in range(p['steps']):
        tau,dg=step_tau(tau,s,method,p)
        maxv=float(np.max(np.abs(tau)))
        if not math.isfinite(maxv) or maxv>p['max_abs_tau']:
            status='UNSTABLE_NONFINITE_OR_THRESHOLD';
            trace.append({'step':s+1,'max_abs':maxv})
            break
        if dg is not None:
            closures.append({'step':s+1, **dg})
        if s in (0,5,17,59,p['steps']-1):
            trace.append({'step':s+1,**finite_metrics(tau)})
    final=finite_metrics(tau) if bool(np.isfinite(tau).all()) else None
    out={'N':n,'seed':seed,'method':method,'corpus':corpus,
         'steps_requested':p['steps'],'steps_executed':s+1,
         'status':status,'initial':m0,'final':final,
         'closures_observed':len(closures),
         'max_post_div_rms':max((v['post_div_rms'] for v in closures),default=None),
         'max_idempotence_rel':max((v['projector_idempotence_relative'] for v in closures),default=None),
         'max_energy_defect':max((v['energy_decomposition_relative'] for v in closures),default=None),
         'max_orthogonality_defect':max((v['orthogonality_relative'] for v in closures),default=None),
         'max_independent_fv_div_rms':max((v['physical_forward_div_rms'] for v in closures),default=None),
         'max_potential_rms':max((v['potential_rms'] for v in closures),default=None),
         'tau_growth_ratio':final['rms']/max(m0['rms'],1e-30) if final else None,
         'trace':trace,
         'tail_closures':closures[-3:]}
    out['bounded_window']=(status=='FINITE_WINDOW_COMPLETED' and
       final['rms']<=p['max_rms_growth_factor']*m0['rms'] if final else False)
    if return_field:
        return out,tau
    return out


def cauchy_grid_errors(fields):
    # Collocated points on even grid; same physical trigonometric initial state.
    results=[]
    for n in (64,128):
        a=fields[n];b=fields[n*2]
        err=rms(a-b[::2,::2])/(rms(b[::2,::2])+1e-30)
        results.append({'N_coarse':n,'N_fine':n*2,'tau_grid_relative_error':err})
    return results


def build_report(root=ROOT,quick=False):
    lock=source_lock(root)
    if not lock['pass']: raise RuntimeError('SOURCE_LOCK_FAILURE: preserve originals')
    pp=dict(DEFAULT)
    if quick: pp['steps']=24
    records=[]; grid=[]
    for seed in SEEDS:
        for method in METHODS:
            fields={}
            for n in NS:
                case,fin=run_case(n,seed,method,'smooth',pp,return_field=True)
                records.append(case)
                fields[n]=fin
            if all(np.isfinite(x).all() for x in fields.values()):
                grid.append({'method':method,'seed':seed,'cauchy':cauchy_grid_errors(fields)})
    stress=[]
    for seed in SEEDS:
        for method in METHODS:
            for n in (64,128):
                p={**pp,'steps':min(72,pp['steps'])}
                stress.append(run_case(n,seed,method,'random',p))
    candidate=[r for r in records+stress if r['method']!='original_emulation']
    projection_ok=all((r['max_post_div_rms'] is not None and r['max_post_div_rms']<pp['rms_post_div_limit']
                       and r['max_idempotence_rel']<pp['idem_rel_limit']
                       and r['max_energy_defect']<pp['energy_rel_limit']) for r in candidate if r['closures_observed']>0)
    stable=all(r['bounded_window'] for r in candidate)
    # Cauchy gate: require BOTH pair-errors below 0.10, and second smaller than first.
    refine_ok=all(len(x['cauchy'])==2 and
        x['cauchy'][1]['tau_grid_relative_error']<x['cauchy'][0]['tau_grid_relative_error']
        and x['cauchy'][1]['tau_grid_relative_error']<pp['grid_cauchy_limit'] for x in grid if x['method']!='original_emulation')
    # No invariant-lock certificate: standalone numerical tests are not XV/XIV invariant port.
    witness_path=root/'output/XVI_TAU_JS_WITNESS_v001.json'
    witness=json.loads(witness_path.read_text('utf-8')) if witness_path.is_file() else None
    witness_valid=(witness is not None and witness.get('source_sha256')==
       json.loads((root/'config/XVI_TAU_LOCK_v001.json').read_text('utf-8'))['inputs']['canonical_engine']['sha256']
       and witness.get('original_engine_unmodified') is True
       and witness.get('all_pass') is True and len(witness.get('results',[]))==2
       and all(x['N']==64 and x['steps']==24 and x['relative_final_tau_error']<1e-10
             for x in witness['results']))
    gates={'T0_baseline_integrity':'PASS' if lock['pass'] else 'FAIL',
         'T1_full_nonlinear_sequence':'PASS_PYTHON_SOURCE_TRANSLATION_ONLY',
         'T2_repaired_flux_each_closure':'PASS_TESTED' if projection_ok else 'FAIL',
         'T3_bounded_finite_horizon':'PASS_TESTED' if stable else 'FAIL',
         'T4_grid_refinement':'PASS_SMOOTH_TESTED' if refine_ok else 'FAIL_OR_NONCONVERGENT',
         'T5_chamber_XIV_XV_invariants':'OPEN_NOT_CERTIFIED',
         'T6_canonical_js_reexecution':'PASS_24_STEP_ZERO_NOISE_WITNESS_ONLY' if witness_valid else 'NOT_RUN',
         'T7_born_rule':'NOT_DERIVED'}
    primary='FINITE_WINDOW_TAU_CANDIDATE_PASS_LIMITED' if (projection_ok and stable and refine_ok) else 'FULL_TAU_CERTIFICATION_NOT_ESTABLISHED'
    return {'protocol':'XVI_TAU_EVOLUTION_v001','scope':'Controlled Python translation of source nonlinear tau step, proto-flux, projection and sealing update; ORIGINAL_HTML_UNMODIFIED',
       'locks':lock,'parameters':pp,'randomness':'seeded NumPy PCG64 initial data only; sigma=0; NOT JavaScript RNG bit-for-bit',
       'smooth':records,'random_stress':stress,'grid_cauchy':grid,
       'original_js_witness':{'validated':bool(witness_valid),'record':witness if witness_valid else None},
       'gates':gates,'primary_verdict':primary,
       'measure_representation':'BLOCKED_INDEPENDENT_EVENT_BRIDGE_NOT_DERIVED'}


def write_js_input(root=ROOT):
    # Can be compared against the original unmodified JS class by optional Node probe.
    cases=[]
    p={**DEFAULT,'steps':24}
    for seed in SEEDS:
        n=64
        tau=init_tau(n,seed,'smooth')
        _,out=run_case(n,seed,'original_emulation','smooth',p,return_field=True)
        cases.append({'N':n,'seed':seed,'params':p,
            'initial_tau':tau.ravel().tolist(),'python_final_tau':out.ravel().tolist()})
    dest=root/'output/XVI_TAU_JS_INPUT_v001.json'
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps({'protocol':'XVI_TAU_JS_INPUT_v001','cases':cases})+'\n','utf-8')
    return dest


def main():
    pa=argparse.ArgumentParser()
    pa.add_argument('--quick',action='store_true',help='smoke verification, not full result')
    pa.add_argument('--js-input-only',action='store_true',help='write deterministic source-JS witness fixture')
    pa.add_argument('--output',default='output/XVI_TAU_EVOLUTION_v001.json')
    args=pa.parse_args()
    if args.js_input_only:
        print('WROTE',write_js_input().relative_to(ROOT));return
    report=build_report(quick=args.quick)
    dest=ROOT/args.output
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n','utf-8')
    print('WROTE',dest.relative_to(ROOT))
    print(' | '.join(k+': '+v for k,v in report['gates'].items()))
    print('VERDICT',report['primary_verdict'])

if __name__=='__main__':main()

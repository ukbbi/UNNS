"""XVI Grid Scaling v001 — source-lock + conditioning + physical-units countermodel.

An independently labeled research CANDIDATE. Never edits the original Chamber XVI,
never overwrites previous outputs, and never assigns a quantum Born measure.
Run: python -m src.xvi_grid_scaling_v001
NumPy required. Earlier project modules remain in place as imports.
"""
from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path
import numpy as np
from src import xvi_projection_repair_v001 as repair
from src import xvi_tau_evolution_v001 as tau_orig

ROOT=Path(__file__).resolve().parents[1]
N_LIST=(64,128,256)
SEEDS=(41,137)
# Physical-unit candidate C (NOT the canonical source evolution).
# Periodic continuum domain [0, 2pi]^2, h=2pi/N, physical time T=0.4.
# d_t tau = -c*d_x tau + nu*Laplacian(tau) - a*psi(J(tau)),
# J = tau*G(tau) - gamma*G(Laplacian(tau)), D J -> Poisson -> psi.
# Matched finite-volume D/G and periodic laplacian, dt capped by CFL.
CANDIDATE=dict(L=2*math.pi,T=0.4,c=0.45,nu=0.03,alpha=0.08,
               gamma=1e-5, adv_cfl=0.25,diff_cfl=0.20,
               grid_error_limit=0.10, retention_min=0.65,
               abs_projector_tol=1e-10, divergence_rel_tol=1e-10,
               conservation_tol=1e-10, max_abs_tau=100.0)


def sha256(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def baseline_lock(root=ROOT):
    spec=json.loads((root/'config/XVI_GRID_LOCK_v001.json').read_text('utf-8'))
    record={}
    for name,row in spec['inputs'].items():
        path=root/row['path']; actual=sha256(path) if path.is_file() else None
        record[name]={'path':row['path'],'expected_sha256':row['sha256'],
                      'actual_sha256':actual,'pass':actual==row['sha256']}
    frozen=json.loads((root/'docs/frozen/XVI_TAU_EVOLUTION_v001.json').read_text('utf-8'))
    negative=frozen['primary_verdict']=='FULL_TAU_CERTIFICATION_NOT_ESTABLISHED'
    old_gates=frozen['gates']; negative=negative and old_gates['T2_repaired_flux_each_closure']=='FAIL' and old_gates['T4_grid_refinement']=='FAIL_OR_NONCONVERGENT'
    active=root/'output/XVI_TAU_EVOLUTION_v001.json'
    if active.exists():
        # Keep active source untouched; distinguish mismatched bytes from the frozen uploaded copy.
        record['active_tau_report']={'path':'output/XVI_TAU_EVOLUTION_v001.json',
             'actual_sha256':sha256(active),'matches_uploaded_frozen':sha256(active)==spec['inputs']['uploaded_tau']['sha256'],
             'info_only':True}
    return {'pass':all(v['pass'] for v in record.values() if 'pass' in v) and negative,
            'previous_negative_verdict_preserved':negative,'checks':record,
            'frozen_primary_verdict':frozen['primary_verdict']}


def hval(n,p=CANDIDATE): return p['L']/n


def dt_steps(n,p=CANDIDATE):
    h=hval(n,p)
    ad=p['adv_cfl']*h/abs(p['c']) if p['c'] else math.inf
    diff=p['diff_cfl']*h*h/p['nu'] if p['nu'] else math.inf
    nsteps=math.ceil(p['T']/min(ad,diff))*p.get('time_substeps',1)
    if 'fixed_nsteps' in p:
        nsteps=p['fixed_nsteps']
        if p['T']/nsteps > min(ad,diff)*(1+1e-12):
            raise ValueError('fixed_nsteps violates declared CFL')
    return p['T']/nsteps,nsteps


def center_dx(a,h): return (np.roll(a,-1,axis=1)-np.roll(a,1,axis=1))/(2*h)


def lap2(a,h):
    return (np.roll(a,1,0)+np.roll(a,-1,0)+np.roll(a,1,1)+np.roll(a,-1,1)-4*a)/(h*h)


def stats(a):
    f=np.fft.fft2(a-np.mean(a))
    k=np.fft.fftfreq(a.shape[0])*a.shape[0]
    kx,ky=np.meshgrid(k,k,indexing='xy')
    low=(kx*kx+ky*ky)<=16
    e=np.abs(f)**2
    return {'mean':float(np.mean(a)),'std':float(np.std(a)),
            'rms':float(np.sqrt(np.mean(a*a))),
            'max_abs':float(np.max(np.abs(a))),
            'low_mode_power_fraction':float(e[low].sum()/max(e.sum(),1e-50))}


def projection_step(a,h,p=CANDIDATE):
    kap=lap2(a,h)
    gx,gy=repair.gradient(a,'forward_volume')
    kx,ky=repair.gradient(kap,'forward_volume')
    jx=a*gx-p['gamma']*kx
    jy=a*gy-p['gamma']*ky
    fx,fy,psi=repair.project(jx,jy,'forward_volume')
    before=repair.rms(repair.divergence(jx,jy,'forward_volume'))
    post=repair.rms(repair.divergence(fx,fy,'forward_volume'))
    f2x,f2y,_=repair.project(fx,fy,'forward_volume')
    vn=repair.vnorm(jx,jy)
    abs_idem=repair.vnorm(f2x-fx,f2y-fy)
    # Absolute units and scale-aware metrics avoid false "relative failure" near exact zero.
    idempotence_scaled=abs_idem/max(vn,1.0)
    xx,yy=jx-fx,jy-fy
    energy=repair.vdot(jx,jy,jx,jy)
    energy_def=abs(energy-repair.vdot(fx,fy,fx,fy)-repair.vdot(xx,yy,xx,yy))/max(energy,1e-30)
    return psi,{'before_div_rms':before,'post_div_rms':post,
                'post_rel':post/max(before,1e-30),
                'abs_idempotence':abs_idem,'scaled_idempotence':idempotence_scaled,
                'energy_rel':energy_def,'potential_rms':repair.rms(psi)}


def run_candidate(n,seed,p=CANDIDATE,include_field=False):
    if n not in N_LIST: raise ValueError('N must be from frozen grid set')
    arr=tau_orig.init_tau(n,seed,'smooth').copy()
    initial=stats(arr); h=hval(n,p);dt,ns=dt_steps(n,p)
    worst={'post_rel':0.0,'scaled_idempotence':0.0,'energy_rel':0.0,
           'post_div_rms':0.0,'potential_rms':0.0}
    status='COMPLETED';trace=[]
    for i in range(ns):
        psi,pg=projection_step(arr,h,p)
        for key in worst: worst[key]=max(worst[key],pg[key])
        adv=center_dx(arr,h)
        arr=arr+dt*(-p['c']*adv +p['nu']*lap2(arr,h)-p['alpha']*psi)
        if not np.isfinite(arr).all() or np.max(np.abs(arr))>p['max_abs_tau']:
            status='UNSTABLE';break
        if i in (0,ns//2,ns-1):trace.append({'step':i+1,'physical_time':(i+1)*dt,'stats':stats(arr)})
    final=stats(arr) if status=='COMPLETED' else None
    report={'N':n,'seed':seed,'domain_L':p['L'],'dx':h,'dt':dt,'steps':ns,
            'final_physical_time':ns*dt if status=='COMPLETED' else (i+1)*dt,
            'status':status,'initial':initial,'final':final,'max_projector_residuals':worst,
            'std_retention':final['std']/max(initial['std'],1e-30) if final else None,
            'trace':trace}
    if include_field: return report,arr
    return report


def field_diff(coarse,fine):
    x=fine[::2,::2]
    return float(np.sqrt(np.mean((coarse-x)**2))/max(np.sqrt(np.mean(x*x)),1e-30))


def conditioning_audit(n=256):
    jx,jy=repair.source_flux(n,41)
    result=[]
    for scale in (1.0,1e-6,1e-12,1e-16):
        j1,j2=jx*scale,jy*scale
        px,py,_=repair.project(j1,j2,'central_source')
        qx,qy,_=repair.project(px,py,'central_source')
        raw=repair.vnorm(qx-px,qy-py)
        size=repair.vnorm(px,py)
        threshold=1e-12*repair.vnorm(jx,jy)
        result.append({'amplitude_scale':scale,'projected_flux_norm':size,
                       'absolute_P2_P_residual':raw,
                       'relative_P2_P':raw/max(size,1e-300),
                       'relative_interpretable':bool(size>threshold),
                       'scaled_with_reference':raw/max(repair.vnorm(jx,jy),1e-300)})
    return result


def source_geometry():
    # Provenance: exact source operators, no reinterpretation as a complete PDE.
    return [{'N':n,'continuum_dx':2*math.pi/n,
             'source_gradient_raw_coefficient':0.5,
             'physical_center_gradient_coefficient':n/(4*math.pi),
             'source_to_physical_center_gradient_ratio':2*math.pi/n,
             'source_laplacian_low_mode_symbol':-(2*math.pi/n)**2,
             'continuum_laplacian_low_mode_symbol':-1.0,
             'note':'Original source has N-dependent implicit length; not fixed-domain geometry.'}
            for n in N_LIST]


def previous_errors(report):
    return [{'method':x['method'],'seed':x['seed'],
             'pair_64_128':x['cauchy'][0]['tau_grid_relative_error'],
             'pair_128_256':x['cauchy'][1]['tau_grid_relative_error']}
            for x in report['grid_cauchy']]


def build_report(root=ROOT):
    lock=baseline_lock(root)
    if not lock['pass']: raise RuntimeError('FROZEN_TAU_LOCK_FAILURE: do not overwrite')
    original=json.loads((root/'docs/frozen/XVI_TAU_EVOLUTION_v001.json').read_text('utf-8'))
    tests=[];grid=[]
    for seed in SEEDS:
        fields={}
        for n in N_LIST:
            row,field=run_candidate(n,seed,include_field=True)
            fields[n]=field;tests.append(row)
        er1=field_diff(fields[64],fields[128]);er2=field_diff(fields[128],fields[256])
        grid.append({'seed':seed,'error_64_to_128':er1,'error_128_to_256':er2,
                     'decreasing':er2<er1,'passes_frozen_threshold':er2<CANDIDATE['grid_error_limit']})
    # Independent mesh-only check at a common dt=0.004 across all grids.
    spatial_grid=[]
    dt_base,_=dt_steps(256)
    fixed_steps=round(CANDIDATE['T']/dt_base)
    for seed in SEEDS:
        ff={}
        for n in N_LIST:
            _,ff[n]=run_candidate(n,seed,p={**CANDIDATE,'fixed_nsteps':fixed_steps},include_field=True)
        e1=field_diff(ff[64],ff[128]);e2=field_diff(ff[128],ff[256])
        spatial_grid.append({'seed':seed,'dt':dt_base,'steps':fixed_steps,'error_64_to_128':e1,
              'error_128_to_256':e2,'decreasing':e2<e1,'passes_threshold':e2<CANDIDATE['grid_error_limit']})
    # Independent time-discretization and no-closure ablation checks.
    timestep_checks=[]
    for seed in SEEDS:
        orig,xx=run_candidate(128,seed,include_field=True)
        fine,yy=run_candidate(128,seed,p={**CANDIDATE,'time_substeps':2},include_field=True)
        timestep_checks.append({'seed':seed,'N':128,'dt':orig['dt'],'half_dt':fine['dt'],
                 'field_rel_error':float(np.sqrt(np.mean((xx-yy)**2))/max(np.sqrt(np.mean(yy*yy)),1e-30))})
    no_closure,ablation_field=run_candidate(64,41,p={**CANDIDATE,'alpha':0.0},include_field=True)
    with_closure,closure_field=run_candidate(64,41,include_field=True)
    ablation_error=float(np.sqrt(np.mean((closure_field-ablation_field)**2))/max(np.sqrt(np.mean(closure_field**2)),1e-30))
    bounded=all(x['status']=='COMPLETED' for x in tests)
    flux=all(x['max_projector_residuals']['post_rel']<CANDIDATE['divergence_rel_tol']
             and x['max_projector_residuals']['scaled_idempotence']<CANDIDATE['abs_projector_tol']
             and x['max_projector_residuals']['energy_rel']<CANDIDATE['conservation_tol'] for x in tests)
    preservation=all(x['std_retention']>=CANDIDATE['retention_min'] for x in tests)
    gridpass=all(x['decreasing'] and x['passes_frozen_threshold'] for x in grid)
    spatialpass=all(x['decreasing'] and x['passes_threshold'] for x in spatial_grid)
    timepass=all(x['field_rel_error']<0.01 for x in timestep_checks)
    ablationpass=ablation_error>0.001
    return {'protocol':'XVI_GRID_SCALING_v001',
            'scope':'Fixed-physical-domain, matched-finite-volume candidate; NOT the canonical Chamber XVI evolution',
            'frozen_tau_baseline':lock,
            'original_negative_gates':original['gates'],
            'original_negative_grid_cauchy':previous_errors(original),
            'candidate_parameters':CANDIDATE,
            'physical_geometry_audit':source_geometry(),
            'conditioning':conditioning_audit(),
            'physical_candidate_runs':tests,'physical_grid_cauchy':grid,
            'fixed_dt_mesh_cauchy':spatial_grid,
            'timestep_refinement':timestep_checks,
            'nontrivial_closure_ablation':{'N':64,'seed':41,'alpha_control':0.0,'alpha_candidate':CANDIDATE['alpha'],
                                             'field_rel_difference':ablation_error},
            'gates':{
               'S0':'PASS_FROZEN' if lock['pass'] else 'FAIL',
               'S1':'PASS_GEOMETRY_DISCREPANCY_IDENTIFIED',
               'S2':'PASS_CONDITIONING_DIAGNOSTIC_IMPLEMENTED',
               'S3': 'PASS_NEW_COUPLED_SPACE_TIME_CAUCHY' if gridpass else 'FAIL_NEW_COUPLED_SPACE_TIME_CAUCHY',
               'S3b':'PASS_FIXED_DT_MESH_CONTROL' if spatialpass else 'FAIL_FIXED_DT_MESH_CONTROL',
               'S4':'PASS_NEW_CANDIDATE_FLUX' if flux else 'FAIL_NEW_CANDIDATE_FLUX',
               'S5':'PASS_NEW_FINITE_STRUCTURAL_RETENTION' if preservation and bounded else 'FAIL_NEW_FINITE_STRUCTURAL_RETENTION',
               'S5a':'PASS_FIXED_GRID_DT_REFINEMENT' if timepass else 'FAIL_FIXED_GRID_DT_REFINEMENT',
               'S5b':'PASS_NONTRIVIAL_CLOSURE_ABLATION' if ablationpass else 'FAIL_NONTRIVIAL_CLOSURE_ABLATION',
               'S6':'OPEN_CHAMBER_XIV_XV_INVARIANTS_NOT_TRANSLATED',
               'S7':'NOT_DERIVED_OBSERVABLE_MEASURE'},
            'old_T4_remains':'FAIL_OR_NONCONVERGENT',
            'old_full_tau_verdict':'FULL_TAU_CERTIFICATION_NOT_ESTABLISHED',
            'candidate_verdict': 'LIMITED_PHYSICAL_GEOMETRY_WITNESS' if (gridpass and spatialpass and flux and preservation and bounded and timepass and ablationpass) else 'CANDIDATE_NOT_CERTIFIED',
            'full_canonical_tau_certified':False,'born_rule':'NOT_DERIVED'}


def main():
    report=build_report()
    path=ROOT/'output/XVI_GRID_SCALING_v001.json'
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print('WROTE output/XVI_GRID_SCALING_v001.json')
    print('FROZEN TAU: NEGATIVE VERDICT PRESERVED | NEW CANDIDATE: '+report['candidate_verdict']+' | BORN: NOT DERIVED')

if __name__=='__main__': main()

"""XVI source-fidelity invariant audit. Run from UNNS_ENTANGLE_I root:
python -m src.xvi_invariants_audit_v001

Source diagnostic formulas are copied *mathematically* from frozen XVI HTML,
not substituted with a physically regularized alternative. Reliability is reported
separately. No claim of canonically derived quantum probabilities.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import numpy as np
from src import xvi_grid_scaling_v001 as grid
from src import xvi_tau_evolution_v001 as tau

ROOT=Path(__file__).resolve().parents[1]
LOCK='config/XVI_INVARIANTS_LOCK_v001.json'
N_LIST=(64,128,256)
SEEDS=(41,137)
# Preregistered gates (not calibrated after looking at results)
CFG={'L':2*math.pi,'T':0.4,'tail_start_fraction':0.8,'retention_min':0.65,
     'fit_r2_min':0.95,'spectrum_target_p':2.28,'spectrum_p_tol':0.05,
     'phi':1.618,'phi_abs_tol':0.010,
     'spectral_support_min_bins':8,'spectral_support_min_octaves':1.0,'min_fit_supported_fraction':0.8,
     'spectral_bin_floor_relative_to_peak':1e-12,'max_spectral_peak_fraction':0.90,
     'entropy_tail_rel_threshold':1e-3,'beyond_diffusion_min_relative_field':0.01,
     'gate_requires_original_export_reproduction':True}

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def locked(root=ROOT):
    data=json.loads((root/LOCK).read_text('utf8'))
    checks={}
    for name,meta in data['inputs'].items():
        p=root/meta['path']; actual=sha(p) if p.is_file() else None
        checks[name]={'path':meta['path'],'expected':meta['sha256'],'actual':actual,'pass':actual==meta['sha256']}
    baseline=json.loads((root/'docs/frozen/XVI_GRID_SCALING_v001.json').read_text('utf8'))
    prev=baseline['old_full_tau_verdict']=='FULL_TAU_CERTIFICATION_NOT_ESTABLISHED' and baseline['candidate_verdict']=='LIMITED_PHYSICAL_GEOMETRY_WITNESS'
    return {'all_pass':all(x['pass'] for x in checks.values()) and prev,'checks':checks,'prior_negative_preserved':prev}

def mu_values():
    # Exactly JS loop's floating point *iterated addition*, not linspace.
    m=1.600; out=[]
    while m<=1.640:
        out.append(m);m+=0.001
    return out

def scaled_delta(a,mu):
    n=a.shape[0]
    u=np.arange(n,dtype=float)*mu
    u%=n
    i0=np.floor(u).astype(int); t=u-i0
    i1=(i0+1)%n
    # source x+W*y, x axis=1 and y axis=0, sample bilinear on wrapped pixel indices
    z=(1-t[None,:])*(1-t[:,None])*a[np.ix_(i0,i0)] \
     +(t[None,:])*(1-t[:,None])*a[np.ix_(i0,i1)] \
     +(1-t[None,:])*(t[:,None])*a[np.ix_(i1,i0)] \
     +(t[None,:])*(t[:,None])*a[np.ix_(i1,i1)]
    return float(np.mean((z-a)**2))

def scale_invariant(a):
    ms=mu_values(); scores=[scaled_delta(a,m) for m in ms]
    k=int(np.argmin(scores))
    return {'mu_star':ms[k],'delta_scale':scores[k],
            'search_interval':[ms[0],ms[-1]],'num_grid_points':len(ms),
            'at_search_edge':k in (0,len(ms)-1),
            'phi_in_window_by_design':True,
            'relative_score_contrast':float((max(scores)-min(scores))/max(max(scores),1e-30)),
            'note':'A restricted phi-centered sweep does not independently establish a physical phi attractor.'}

def spectrum_source(a):
    n=a.shape[0]; f=np.fft.fft2(a)
    modes=np.fft.fftfreq(n)*n
    xx,yy=np.meshgrid(modes,modes,indexing='xy')
    # HTML laplacianFFT: kx=(2π/W)*integer mode; spectrum uses FFT(kappa)
    kh=-(2*math.pi/n)**2*(xx*xx+yy*yy)*f
    power=np.abs(kh)**2
    bin_idx=np.floor(np.sqrt(xx*xx+yy*yy)).astype(int)
    valid=(bin_idx>0)&(bin_idx<n//2)
    bsum=np.bincount(bin_idx[valid].ravel(),weights=power[valid].ravel(),minlength=n//2)
    count=np.bincount(bin_idx[valid].ravel(),minlength=n//2)
    bins=np.arange(1,n//2)[count[1:n//2]>0]
    mean=bsum[bins]/count[bins]
    if len(bins)<3 or not (np.isfinite(mean).all() and (mean>0).all()):
        p=None;r2=None;status='SOURCE_LOG_FIT_UNDEFINED'
    else:
        x=np.log(bins.astype(float));y=np.log(mean)
        slope=float(np.sum((x-x.mean())*(y-y.mean()))/np.sum((x-x.mean())**2))
        ss=float(np.sum((y-y.mean())**2));r2=1-float(np.sum((y-(y.mean()+slope*(x-x.mean())))**2))/ss if ss>0 else None
        p=-slope;status='SOURCE_FIT_NUMERICALLY_FINITE'
    # Separately diagnosed physical spectral support. NEVER silently omit bins from source fit.
    peak=float(np.max(mean)) if mean.size else 0.0
    supported=(mean>=max(peak*CFG['spectral_bin_floor_relative_to_peak'],1e-300)) if peak>0 else np.zeros_like(mean,dtype=bool)
    realbins=bins[supported]
    span=float(np.log2(realbins[-1]/realbins[0])) if len(realbins)>1 else 0.0
    support_power=float(np.sum(mean[supported]*count[realbins])) if len(realbins) else 0.0
    total_power=float(np.sum(mean*count[bins])) if len(bins) else 0.0
    dominant=float(np.max(mean*count[bins])/max(total_power,1e-300)) if len(bins) else 1.0
    fit_support_fraction=len(realbins)/max(len(bins),1)
    reliable=bool(len(realbins)>=CFG['spectral_support_min_bins'] and span>=CFG['spectral_support_min_octaves'] and dominant<=CFG['max_spectral_peak_fraction'] and fit_support_fraction>=CFG['min_fit_supported_fraction'] and np.isfinite(total_power))
    return {'p':p,'r2':r2,'n':len(bins),'status':status,
            'source_bin_policy':'all nonempty radial bins, even if power is tiny',
            'power_support':{'bins_above_relative_floor':int(len(realbins)),'fit_bins_above_floor_fraction':fit_support_fraction,
              'octaves':span,'dominant_bin_power_fraction':dominant,
              'total_power':total_power,'power_above_floor_fraction':support_power/max(total_power,1e-300),
              'reliable_for_physical_slope_claim':reliable}}

def entropy_source(a):
    n=a.size;lo=float(np.min(a));hi=float(np.max(a));rng=hi-lo
    if rng==0:
        return {'H_r':None,'status':'CONSTANT_FIELD_UNDEFINED_IN_SOURCE_BIN_FORMULA'}
    bins=np.floor(((a.ravel()-lo)/rng)*49).astype(int)
    hist=np.bincount(np.clip(bins,0,49),minlength=50)
    p=hist[hist>0]/n
    return {'H_r':float(-np.sum(p*np.log2(p))),'status':'SOURCE_50_BIN_SHANNON'}

def diagnostics(a):
    return {'scale':scale_invariant(a),'spectrum':spectrum_source(a),'entropy':entropy_source(a)}

def step_states(n,seed,variant):
    p=grid.CANDIDATE
    arr=tau.init_tau(n,seed,'smooth').copy()
    dx=p['L']/n;dt,steps=grid.dt_steps(n)
    init=arr.copy(); tail=None;tail_at=max(1,int(round(steps*CFG['tail_start_fraction'])))
    for step in range(steps):
        if variant=='candidate':
            psi,_=grid.projection_step(arr,dx,p)
            rhs=-p['c']*grid.center_dx(arr,dx)+p['nu']*grid.lap2(arr,dx)-p['alpha']*psi
        elif variant=='advection_diffusion':
            rhs=-p['c']*grid.center_dx(arr,dx)+p['nu']*grid.lap2(arr,dx)
        elif variant=='diffusion_only':
            rhs=p['nu']*grid.lap2(arr,dx)
        else: raise ValueError(variant)
        arr=arr+dt*rhs
        if step+1==tail_at:tail=arr.copy()
    return {'initial':init,'tail':tail,'final':arr,'dt':dt,'steps':steps,'tail_time':tail_at*dt}

def relative_dist(x,y):return float(np.sqrt(np.mean((x-y)**2))/max(np.sqrt(np.mean(y*y)),1e-30))

def source_exports_summary(root):
    mapping={'64_A020':'docs/sources/XVI_RUN_64_A020.json',
             '128_A015':'docs/sources/XVI_RUN_128_A015.json',
             '128_A010':'docs/sources/XVI_RUN_128_A010.json',
             '256_A010':'docs/sources/XVI_RUN_256_A010.json'}
    out=[]
    for name,path in mapping.items():
        doc=json.loads((root/path).read_text('utf8'))
        out.append({'id':name,'path':path,'config':doc['config'],
            'reported_post_state':doc['post_state'], 'reported_criteria':doc['criteria'],
            'raw_tau_field_exported':False,'field_based_recalculation_possible':False,
            'warning':'Export contains final metrics but no raw field; exact independent reproduction of these individual exports is impossible.'})
    return out

def source_js_parity_witness(root=ROOT):
    """Compare recorded direct execution of UNMODIFIED source for common raw field fixtures.
    Does not replace the source diagnostics, and expects spectral parity may FAIL due to near-zero powers.
    """
    f=root/'output/XVI_INVARIANTS_JS_FIXTURE_v001.json'
    j=root/'output/XVI_INVARIANTS_JS_WITNESS_v001.json'
    if not(f.is_file() and j.is_file()):return {'status':'MISSING_OPTIONAL_WITNESS','cases':[]}
    raw=json.loads(f.read_text('utf8'))
    witness=json.loads(j.read_text('utf8'))
    srcsha=sha(root/'docs/sources/XVI_ENGINE_v084.html')
    if witness['source_sha256']!=srcsha:raise RuntimeError('JS witness source hash differs from locked engine')
    rows=[]
    for c,w in zip(raw['cases'],witness['cases']):
        if c['name']!=w['name']:raise RuntimeError('JS witness fixture order mismatch')
        local=diagnostics(np.array(c['values'],float).reshape(c['N'],c['N']))
        differences={}
        for k,fromjs,frompy in (
          ('mu_star',w['mu_star'],local['scale']['mu_star']),
          ('delta_scale',w['delta_scale'],local['scale']['delta_scale']),
          ('spectrum_p',w['p'],local['spectrum']['p']),
          ('spectrum_r2',w['r2'],local['spectrum']['r2']),
          ('entropy',w['entropy'],local['entropy']['H_r'])):
            differences[k]={'source_js':fromjs,'python':frompy,'abs_error':abs(fromjs-frompy) if fromjs is not None and frompy is not None else None}
        rows.append({'name':c['name'],'differences':differences,
          'scale_and_entropy_parity':all(differences[k]['abs_error'] is not None and differences[k]['abs_error']<1e-10 for k in ('mu_star','delta_scale','entropy')),
          'spectral_parity_1e-8':all(differences[k]['abs_error'] is not None and differences[k]['abs_error']<1e-8 for k in ('spectrum_p','spectrum_r2'))})
    return {'status':'DIRECT_ORIGINAL_JS_SOURCE_WITNESS','cases':rows,
          'all_scale_and_entropy_parity':all(r['scale_and_entropy_parity'] for r in rows),
          'all_spectral_parity':all(r['spectral_parity_1e-8'] for r in rows),
          'interpretation':'Differences in source FFT and NumPy FFT round-off, amplified by log of tiny radial-bin powers; p cannot be claimed source-reproduced at frozen numerical tolerance.'}

def build_report(root=ROOT):
    lock=locked(root)
    if not lock['all_pass']:raise RuntimeError('source/frozen input checksum mismatch; existing files untouched')
    rows=[]; controls=[]
    jsparity=source_js_parity_witness(root)
    for n in N_LIST:
        for seed in SEEDS:
            sims={v:step_states(n,seed,v) for v in ('candidate','advection_diffusion','diffusion_only')}
            records={}
            for name,run in sims.items():
                a=run['initial'];b=run['tail'];c=run['final']
                da,db,dc=diagnostics(a),diagnostics(b),diagnostics(c)
                initial_std=float(np.std(a));std=float(np.std(c))
                dh=db['entropy']['H_r'];ch=dc['entropy']['H_r']
                tail_rel=abs(ch-dh)/max(abs(ch),1e-30) if ch is not None and dh is not None else None
                records[name]={'initial':da,'tail':db,'final':dc,
                    'std_retention':std/max(initial_std,1e-30),
                    'tail_entropy_relative_change':tail_rel,'field_mean_final':float(np.mean(c)),
                    'dt':run['dt'],'steps':run['steps'],'tail_physical_time':run['tail_time']}
            rows.append({'N':n,'seed':seed,'runs':records,
                        'candidate_vs_no_closure_field_rel':relative_dist(sims['candidate']['final'],sims['advection_diffusion']['final']),
                        'candidate_vs_diffusion_only_field_rel':relative_dist(sims['candidate']['final'],sims['diffusion_only']['final'])})
    fidelity=all(row['runs']['candidate']['std_retention']>=CFG['retention_min'] for row in rows)
    distinguish=all(row['candidate_vs_no_closure_field_rel']>=CFG['beyond_diffusion_min_relative_field'] for row in rows)
    diag_source_reliable=all(row['runs']['candidate']['final']['spectrum']['power_support']['reliable_for_physical_slope_claim'] for row in rows)
    phi_target=all(row['runs']['candidate']['final']['scale']['mu_star'] is not None and
                   abs(row['runs']['candidate']['final']['scale']['mu_star']-CFG['phi'])<=CFG['phi_abs_tol'] and
                   not row['runs']['candidate']['final']['scale']['at_search_edge'] for row in rows)
    spectrum_target=all(row['runs']['candidate']['final']['spectrum']['p'] is not None and
                   abs(row['runs']['candidate']['final']['spectrum']['p']-CFG['spectrum_target_p'])<=CFG['spectrum_p_tol'] and
                   row['runs']['candidate']['final']['spectrum']['r2'] is not None and
                   row['runs']['candidate']['final']['spectrum']['r2']>=CFG['fit_r2_min'] for row in rows)
    entropy_stationary=all(row['runs']['candidate']['tail_entropy_relative_change'] is not None and
                           row['runs']['candidate']['tail_entropy_relative_change']<CFG['entropy_tail_rel_threshold'] for row in rows)
    # Fundamental distinction: no individual original exported field is present; no exact export reproduction claim allowed.
    reported={'protocol':'XVI_INVARIANTS_AUDIT_v001',
      'scope':'SOURCE-FORMULA diagnostics, candidate dynamics and controls. Not original Chamber dynamics or quantum probabilities.',
      'locked_inputs':lock, 'specification':CFG,
      'source_semantics':{'phi':'Source loops mu=1.600..1.640 in 0.001 increments, minimizing mean square periodic bilinear resampling defect',
           'spectrum':'Source FFT of its FFT-Laplacian kappa, radial k=floor(sqrt(kx^2+ky^2)) averages power in bins, fits all bin log powers vs log integer k, p=-slope',
           'entropy':'Source normalized histogram of 50 bins spanning each field own min,max; H=-sum p log2(p)',
           'sampling':'Diagnostics evaluated at final physical time and predefined 80% tail for new candidate; distinct from original engine monitor and cached entropy times',
           'reference_slope_target_from_html':2.28,
           'original_export_spectral_p_negative':'Sign convention as exported, no retuning or sign flip performed',
           'limitations':['Original JSON exports omit raw tau arrays','Phi minimizer constrained to window around golden ratio','Tiny FFT bin powers can dominate log fits','Entropy histogram varies with its own support','Original HTML entropy cache does not prove C4 without consecutive snapshots']},
      'original_chamber_exports':source_exports_summary(root),
      'direct_original_js_parity':jsparity,
      'experiments':rows,
      'gates':{
          'I0':'PASS_FROZEN' if lock['all_pass'] else 'FAIL',
          'I1':'PASS_SOURCE_FORMULAS_LOCKED',
          'I2':'BLOCKED_RAW_FIELDS_NOT_EXPORTED',
          'I3':'PARTIAL_PYTHON_FORMULA_PORT_WITH_SPECTRAL_PARITY_FAILURE' if not jsparity.get('all_spectral_parity',False) else 'PASS_SOURCE_FORMULA_PARITY',
          'I4':'PASS_FINITE_RETENTION' if fidelity else 'FAIL_FINITE_RETENTION',
          'I5':'PASS_ABLATION_EFFECT_ONLY' if distinguish else 'FAIL_OR_BELOW_EFFECT_THRESHOLD',
          'I6':'PASS_SPECTRAL_RELIABILITY' if diag_source_reliable else 'FAIL_SPECTRAL_RELIABILITY',
          'I7':'PASS_RESTRICTED_PHI_WINDOW' if phi_target else 'FAIL_OR_UNINFORMATIVE_PHI_WINDOW',
          'I8':'PASS_SOURCE_SPECTRAL_TARGET' if spectrum_target and diag_source_reliable else 'FAIL_SOURCE_SPECTRAL_TARGET',
          'I9':'PASS_NUMERIC_TAIL_NOT_UNIQUE' if entropy_stationary else 'FAIL_TAIL_ENTROPY_STATIONARITY',
          'I11':'NOT_DEMONSTRATED_NONTRIVIAL_INVARIANT_BEYOND_CONTROLS',
          'I12':'FAIL_STRICT_SPECTRAL_JS_PARITY' if not jsparity.get('all_spectral_parity',False) else 'PASS_STRICT_JS_PARITY',
          'I10':'NOT_DERIVED_OBSERVABLE_PROBABILITY'},
      'previous_verdict':'LIMITED_PHYSICAL_GEOMETRY_WITNESS',
      'full_canonical_XVI_invariant_certified':False,'born_rule':'NOT_DERIVED'}
    reported['scientific_verdict']='INVARIANT_FIDELITY_NOT_CERTIFIED'
    return reported

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',default='output/XVI_INVARIANTS_AUDIT_v001.json')
    args=parser.parse_args();report=build_report(); dest=ROOT/args.out
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n',encoding='utf8')
    print('WROTE',dest.relative_to(ROOT))
    print('FROZEN',report['gates']['I0'],'|',report['scientific_verdict'],'| BORN RULE NOT DERIVED')
if __name__=='__main__':main()

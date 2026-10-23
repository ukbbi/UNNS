"""Source-locked spectral conditioning. New diagnostic; never recasts previous negative gate."""
from __future__ import annotations
import hashlib,json,math
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
LOCK_PATH=Path('config/XVI_SPECTRAL_LOCK_v001.json')
RAW_PATH=Path('output/XVI_SPECTRAL_SOURCE_RAW_v001.json')
OUT_PATH=Path('output/XVI_SPECTRAL_CONDITIONING_v001.json')
# Predeclared conditioning policy, not fitted to canonical engine outcomes:
POLICY={
    'fixed_k_min':2,'fixed_k_max_fraction_of_n':0.25,
    'bin_relative_power_floor':1e-12,
    'min_supported_bins':8,'min_octaves':1.0,
    'min_supported_fraction_in_window':0.80,
    'max_dominant_power_fraction':0.9,
    'min_fit_r2_for_power_law':0.95,
    'source_p_target':2.28,'source_p_tolerance':0.05,
    'js_numpy_supported_relative_tolerance':1e-8,
    'sensitivity_floor_values':[1e-8,1e-10,1e-12,1e-14],
    'sensitivity_windows':['2_to_quarter','3_to_third','4_to_quarter'],
    'noise_relative_amplitudes':[0.0,1e-12,1e-9],
    'perturbation_seed':20261021,
}

def sha256(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def locked(root=ROOT):
    cfg=json.loads((root/LOCK_PATH).read_text('utf8'))
    results={}
    for name,entry in cfg['inputs'].items():
        path=root/entry['path'];actual=sha256(path) if path.exists() else None
        results[name]={'expected':entry['sha256'],'actual':actual,'pass':actual==entry['sha256']}
    base=json.loads((root/cfg['inputs']['frozen_invariants']['path']).read_text('utf8'))
    verdict=base['scientific_verdict']=='INVARIANT_FIDELITY_NOT_CERTIFIED' and not base['full_canonical_XVI_invariant_certified'] and base['born_rule']=='NOT_DERIVED'
    return {'pass':all(r['pass'] for r in results.values()) and verdict,'checks':results,'negative_verdict_preserved':verdict}

def source_bin_spectrum(tau):
    """Same kappa=FFT-laplacian, radial floor bin, and mean shell power as source JS."""
    a=np.asarray(tau,dtype=np.float64);N=a.shape[0]
    if a.shape!=(N,N) or N<16 or N&(N-1):raise ValueError('expected even square power-of-two grid')
    ks=np.fft.fftfreq(N)*N;kx,ky=np.meshgrid(ks,ks,indexing='xy')
    ksq=kx*kx+ky*ky
    phat=(-(2*math.pi/N)**2*ksq)*np.fft.fft2(a)
    power=np.abs(phat)**2
    bins=np.floor(np.sqrt(ksq)).astype(int)
    mask=(bins>0)&(bins<N//2)
    count=np.bincount(bins[mask].ravel(),minlength=N//2)
    bsum=np.bincount(bins[mask].ravel(),weights=power[mask].ravel(),minlength=N//2)
    k=np.flatnonzero(count)[1:] if count[0] else np.flatnonzero(count)
    k=k[k>0]
    return k.astype(int),bsum[k]/count[k],count[k]

def fit(k,power):
    k=np.asarray(k,float);power=np.asarray(power,float)
    if len(k)<3 or not np.all(np.isfinite(power)) or np.any(power<=0):
        return {'p':None,'r2':None,'n':len(k),'reason':'not enough valid positive bins'}
    x=np.log(k);y=np.log(power);x0=x-x.mean();den=np.sum(x0*x0)
    if den<=0:return {'p':None,'r2':None,'n':len(k),'reason':'degenerate k span'}
    slope=float(np.dot(x0,y-y.mean())/den);pred=y.mean()+slope*x0
    var=float(np.sum((y-y.mean())**2));ss=float(np.sum((y-pred)**2))
    return {'p':-slope,'r2':1-ss/var if var>0 else None,'n':len(k),'reason':'ok'}

def condition(k,Pk,count,N,floor=1e-12,window='2_to_quarter'):
    k=np.asarray(k,dtype=int);Pk=np.asarray(Pk,float);count=np.asarray(count,int)
    if len(k)!=len(Pk) or len(count)!=len(k):raise ValueError('bin lengths')
    lo,hi={'2_to_quarter':(2,N//4),'3_to_third':(3,N//3),'4_to_quarter':(4,N//4)}[window]
    band=(k>=lo)&(k<=hi);positive=band&np.isfinite(Pk)&(Pk>0)
    peak=float(max(Pk[positive],default=0.))
    select=positive&(Pk>=peak*floor) if peak>0 else np.zeros_like(band)
    kk=k[select];PP=Pk[select];fraction=float(select.sum()/max(1,band.sum()))
    octave=float(np.log2(kk[-1]/kk[0])) if len(kk)>1 else 0.
    masses=Pk[select]*count[select];den=float(sum(masses))
    dominance=float(max(masses)/den) if den>0 else 1.
    supported=bool(len(kk)>=POLICY['min_supported_bins'] and octave>=POLICY['min_octaves'] and
      fraction>=POLICY['min_supported_fraction_in_window'] and dominance<=POLICY['max_dominant_power_fraction'])
    f=fit(kk,PP)
    return {'window':window,'relative_floor':float(floor),'supported_bins':len(kk),'window_bins':int(band.sum()),
      'supported_fraction':fraction,'octaves':octave,'peak_fraction':dominance,
      'power_law_fit':f,'supported':supported,
      'reliable_power_law':bool(supported and f['r2'] is not None and f['r2']>=POLICY['min_fit_r2_for_power_law']),
      'k_support':[int(v) for v in kk]}

def synthetic_field(N,seed,p=2.28,narrow=False):
    """Controlled KNOWN-SOURCE power law is a calibration, not an UNNS prediction."""
    rng=np.random.default_rng(seed)
    white=rng.normal(size=(N,N));freq=np.fft.fftfreq(N)*N
    xx,yy=np.meshgrid(freq,freq);r=np.hypot(xx,yy)
    amp=np.zeros_like(r);ok=(r>=1)&(r<N//2)
    if narrow:ok=ok&(r<4)
    amp[ok]=r[ok]**(-(p+4)/2)
    data=np.fft.ifft2(np.fft.fft2(white)*amp).real
    return data

def run(root=ROOT):
    lock=locked(root)
    if not lock['pass']:raise RuntimeError('Frozen source or baseline tampered with')
    source=json.loads((root/RAW_PATH).read_text('utf8'))
    if source['source_sha256']!=lock['checks']['canonical_html']['actual'] or not source['source_unmodified']:
        raise RuntimeError('Raw witness not associated with frozen original source')
    rows=[]
    for case in source['cases']:
        N=case['N'];a=np.asarray(case['tau'],float).reshape((N,N));k,pk,ncounts=source_bin_spectrum(a)
        js=case['original_js'];k_js=np.asarray(js['k'],int);pk_js=np.asarray(js['Pk'],float)
        if not np.array_equal(k,k_js):raise RuntimeError('source bin order mismatch')
        fpy=fit(k,pk)
        spectral_parity={'p_abs_difference':abs(fpy['p']-js['p']) if fpy['p'] is not None and js['p'] is not None else None,
                         'r2_abs_difference':abs(fpy['r2']-js['r2']) if fpy['r2'] is not None and js['r2'] is not None else None}
        floor=POLICY['bin_relative_power_floor']
        cont=condition(k,pk,ncounts,N,floor=floor)
        cont_js=condition(k_js,pk_js,ncounts,N,floor=floor)
        p_js=cont_js['power_law_fit']['p'];p_py=cont['power_law_fit']['p']
        parity=bool(p_js is not None and p_py is not None and
               abs(p_js-p_py)<=POLICY['js_numpy_supported_relative_tolerance']*max(1,abs(p_js),abs(p_py)))
        variations=[condition(k,pk,ncounts,N,floor=f,window=w) for f in POLICY['sensitivity_floor_values'] for w in POLICY['sensitivity_windows']]
        rng=np.random.default_rng(POLICY['perturbation_seed'])
        noise=[]
        for factor in POLICY['noise_relative_amplitudes']:
            b=a+factor*max(float(np.std(a)),1.)*rng.normal(size=a.shape)
            bk,bpk,bc=source_bin_spectrum(b)
            noise.append({'amplitude':factor,'source_fit':fit(bk,bpk),'conditioned_fit':condition(bk,bpk,bc,N)})
        rows.append({'name':case['name'],'N':N,'step':case['step'],'source_js_fit':{key:js[key] for key in ('p','r2','n')},
         'source_python_fit':fpy,'all_bin_parity':spectral_parity,
         'conditioned_python':cont,'conditioned_js':cont_js,'supported_js_python_agreement':parity,
         'condition_sensitivity':variations,'noise_stress':noise,'historical_unns_invariant_claim':False})
    synthetic=[]
    for N in (64,128):
        for kind in ('known_powerlaw','narrowband','white_noise_null'):
            field=(np.random.default_rng(20261021).uniform(0,2*math.pi,size=(N,N))
                   if kind=='white_noise_null' else synthetic_field(N,20261021,p=2.28,narrow=kind=='narrowband'))
            k,pk,c=source_bin_spectrum(field)
            synthetic.append({'N':N,'kind':kind,'source_unconditioned':fit(k,pk),'conditioned':condition(k,pk,c,N),
              'intentional_power_law_target':2.28 if kind=='known_powerlaw' else (-4 if kind=='white_noise_null' else None)})
    conditioned_all=all(row['supported_js_python_agreement'] for row in rows)
    robustness=all(row['conditioned_python']['reliable_power_law'] for row in rows)
    source_target=all(row['conditioned_python']['reliable_power_law'] and
      abs(row['conditioned_python']['power_law_fit']['p']-POLICY['source_p_target'])<=POLICY['source_p_tolerance']
      for row in rows)
    source_reproduction=all(row['source_js_fit']['n']==row['source_python_fit']['n'] and
       row['all_bin_parity']['p_abs_difference'] is not None and row['all_bin_parity']['p_abs_difference']<1e-8 and
       row['all_bin_parity']['r2_abs_difference'] is not None and row['all_bin_parity']['r2_abs_difference']<1e-8
       for row in rows)
    report={'protocol':'XVI_SPECTRAL_CONDITIONING_v001','locked_inputs':lock,'policy':POLICY,
     'scope':'Source-locked original Chamber XVI diagnostic evaluated on NEW source-executed raw fields, not on four historical exports',
     'original_exports_raw_field_available':False,'historical_exports_exact_reproduction':'BLOCKED',
     'source_raw_witness_sha256':sha256(root/RAW_PATH),'original_source_unmodified':True,
     'source_formula':'FFT of source FFT-Laplacian kappa; shell-mean power by floor(k); unfiltered ordinary least-squares log fit to every radial bin',
     'conditioned_formula':'fixed k band, predeclared power floor and minimum support; separate DIAGNOSTIC, not rewritten source formula',
     'original_engine_cases':rows,'synthetic_controls':synthetic,
     'gates':{'P0':'PASS_FROZEN_NEGATIVE' if lock['pass'] else 'FAIL',
       'P1':'PASS_SOURCE_ENGINE_EXECUTED_RAW_NEW_FIELDS',
       'P2':'PASS_SOURCE_ALL_BIN_FIT_REPRODUCED_ON_SAME_FIELDS' if source_reproduction else 'FAIL_SOURCE_PARITY',
       'P3':'PASS_CONDITIONED_JS_PY_PARITY' if conditioned_all else 'FAIL_CONDITIONED_PARITY',
       'P4':'PASS_NUMERICAL_SPECTRAL_SUPPORT_ONLY' if robustness else 'FAIL_ORIGINAL_FIELD_SUPPORT',
       'P4b':'PASS_FROZEN_SOURCE_P_TARGET' if source_target else 'FAIL_FROZEN_SOURCE_P_TARGET',
       'P5':'PASS_SYNTHETIC_CONTROL_EVALUATED',
       'P6':'BLOCKED_HISTORICAL_RAW_FIELDS_MISSING',
       'P7':'NOT_DERIVED_OBSERVABLE_MEASURE'},
     'old_scientific_verdict':'INVARIANT_FIDELITY_NOT_CERTIFIED',
     'new_scientific_verdict':'SPECTRAL_CONDITIONING_AUDIT_ONLY',
     'full_canonical_invariant_certified':False,'born_rule':'NOT_DERIVED'}
    return report

def main():
    report=run(); dest=ROOT/OUT_PATH;dest.parent.mkdir(exist_ok=True)
    dest.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n','utf8')
    print('WROTE '+str(OUT_PATH).replace('/','\\'))
    print('FROZEN NEGATIVE PRESERVED | NEW SOURCE FIELDS AUDITED | FULL INVARIANT NOT CERTIFIED')

if __name__=='__main__':main()

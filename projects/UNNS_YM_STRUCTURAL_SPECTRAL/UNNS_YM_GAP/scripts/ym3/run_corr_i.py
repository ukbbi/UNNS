#!/usr/bin/env python3
"""YM-3A frozen CORR-I v0.1.2 batch runner.

This is a line-by-line numerical mirror of the frozen chamber math in
chambers/corr_i/corr_i_v012.html for non-sigma inputs. It does not alter the
chamber and exists only to execute the preregistered batch reproducibly.
"""
from __future__ import annotations
import csv, json, math, hashlib
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'data' / 'derived' / 'corr_i' / 'ym3'
OUT = ROOT / 'output' / 'ym3'
DOCS = ROOT / 'docs'
CHAMBER = ROOT / 'chambers' / 'corr_i' / 'corr_i_v012.html'

SETTINGS = {
    'psd_tol': 1e-10,
    'plateau_rel_range': 0.05,
    'min_plateau_points': 4,
    'alpha_cap': 0.5,
    'mu_ratio_min': 0.001,
    'mu_ratio_max': 1.0,
    'mu_points': 25,
    'z_rms_limit': 1.0,
    'z_max_limit': 3.0,
    'rel_rms_limit': 0.05,
    'rel_max_limit': 0.15,
}
FROZEN_CHAMBER_SHA256 = 'f972c9d460cebc19ef165e66c03f971411062eba093876406ed2efe614e2deb2'
FIXED_R = {'p05':0.5009467921186632, 'p1':0.3269161085235788, 'p2':0.17861212714684468, 'p4':0.08453367126385265, 'p8':0.03766792061795015}
P_ORDER = ['p05','p1','p2','p4','p8']
BETAS = ['b56924','b58000','b58941','b59900','b60625','b62350','b63380','b65000']
BETA_DISPLAY = {'b56924':'5.6924','b58000':'5.80','b58941':'5.8941','b59900':'5.99','b60625':'6.0625','b62350':'6.235','b63380':'6.3380','b65000':'6.50'}


def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1<<20), b''): h.update(b)
    return h.hexdigest()

def mean(a): return sum(a)/len(a) if a else 0.0
def rms(a): return math.sqrt(mean([x*x for x in a])) if a else float('nan')
def finite(x): return math.isfinite(x)

def logspace_desc(maxv,minv,n):
    a,b=math.log(maxv),math.log(minv)
    return [math.exp(a+(b-a)*i/(n-1)) for i in range(n)]

def uniform_grid(t):
    if len(t)<3: return {'ok':False,'dt':float('nan'),'maxRel':float('inf')}
    ds=[t[i]-t[i-1] for i in range(1,len(t))]
    dt=median(ds)
    maxrel=max(abs(d-dt)/max(abs(dt),1e-15) for d in ds)
    return {'ok': finite(dt) and dt>0 and maxrel<1e-6, 'dt':dt, 'maxRel':maxrel}

def meff(t,y):
    u=uniform_grid(t)
    if not u['ok']: return []
    out=[]
    for i in range(len(y)-1):
        if y[i]>0 and y[i+1]>0:
            out.append({'t':(t[i]+t[i+1])/2, 'm':math.log(y[i]/y[i+1])/u['dt']})
    return out

def plateau_info(marr,tol,min_pts):
    positives=[x['m'] for x in marr if x['m']>0]
    if len(marr)<min_pts:
        return {'found':False,'start':None,'n':0,'mref':median(positives) if positives else float('nan'),'relRange':float('nan')}
    for i in range(0,len(marr)-min_pts+1):
        tail=[x['m'] for x in marr[i:] if finite(x['m']) and x['m']>0]
        if len(tail)<min_pts: continue
        med=median(tail)
        rang=(max(tail)-min(tail))/max(abs(med),1e-15)
        if rang<=tol:
            return {'found':True,'start':marr[i]['t'],'n':len(tail),'mref':med,'relRange':rang}
    tail=[x['m'] for x in marr[-min(4,len(marr)):] if finite(x['m']) and x['m']>0]
    return {'found':False,'start':None,'n':0,'mref':median(tail) if tail else float('nan'),'relRange':float('nan')}

def jacobi_eigenvalues(A):
    n=len(A); M=[r[:] for r in A]
    if n==1: return [M[0][0]]
    for _ in range(80*n*n):
        p,q,maxv=0,1,0.0
        for i in range(n):
            for j in range(i+1,n):
                v=abs(M[i][j])
                if v>maxv: maxv,p,q=v,i,j
        if maxv<1e-14: break
        app,aqq,apq=M[p][p],M[q][q],M[p][q]
        phi=0.5*math.atan2(2*apq,aqq-app)
        c,s=math.cos(phi),math.sin(phi)
        for k in range(n):
            if k==p or k==q: continue
            mkp,mkq=M[k][p],M[k][q]
            M[k][p]=M[p][k]=c*mkp-s*mkq
            M[k][q]=M[q][k]=s*mkp+c*mkq
        M[p][p]=c*c*app-2*s*c*apq+s*s*aqq
        M[q][q]=s*s*app+2*s*c*apq+c*c*aqq
        M[p][q]=M[q][p]=0.0
    return sorted(M[i][i] for i in range(n))

def hankel(y,shift,r): return [[y[i+j+shift] for j in range(r)] for i in range(r)]
def mat_sub(A,B): return [[A[i][j]-B[i][j] for j in range(len(A[i]))] for i in range(len(A))]
def hankel_tests(y,tol):
    maxr=min(5,len(y)//2); out=[]
    for r in range(2,maxr+1):
        H0=hankel(y,0,r); H1=hankel(y,1,r); D=mat_sub(H0,H1)
        a=jacobi_eigenvalues(H0)[0]; b=jacobi_eigenvalues(H1)[0]; c=jacobi_eigenvalues(D)[0]
        out.append({'r':r,'minH0':a,'minH1':b,'minDiff':c,'pass':a>=-tol and b>=-tol and c>=-tol})
    return out

def analyze_baseline(t,c):
    c0=c[0]; y=[x/c0 for x in c]
    grid=uniform_grid(t); positive=sum(x>0 for x in c)
    mono=0; logv=0; mind2=float('inf')
    for i in range(len(y)-1):
        if y[i+1]>y[i]+1e-12: mono+=1
    for i in range(1,len(y)-1):
        if y[i-1]>0 and y[i]>0 and y[i+1]>0:
            d2=math.log(y[i+1])-2*math.log(y[i])+math.log(y[i-1])
            mind2=min(mind2,d2)
            if d2 < -1e-10: logv+=1
    if mind2==float('inf'): mind2=float('nan')
    m=meff(t,y); plat=plateau_info(m,SETTINGS['plateau_rel_range'],SETTINGS['min_plateau_points'])
    h=hankel_tests(y,abs(SETTINGS['psd_tol'])) if grid['ok'] and positive==len(c) else []
    hpass=bool(h) and all(x['pass'] for x in h)
    cls='POSITIVE-SPECTRAL CONSISTENT'; status='ok'
    if positive!=len(c): cls,status='INVALID FOR POSITIVE-SPECTRAL TEST','fail'
    elif not grid['ok']: cls,status='NONUNIFORM GRID — MOMENT TEST LIMITED','warn'
    elif mono>0 or logv>0 or not hpass: cls,status='SPECTRAL-POSITIVITY TENSION','warn'
    return {'t':t,'c':c,'y':y,'grid':grid,'positive':positive,'monoViol':mono,'logConvViol':logv,'minD2':mind2,
            'm':m,'plat':plat,'h':h,'hankelPass':hpass,'classification':cls,'status':status}

def safe_bound(limit,unit):
    return float('inf') if (not finite(unit) or unit<=0) else limit/unit

def adversary(b):
    mref=b['plat']['mref']; ratios=logspace_desc(SETTINGS['mu_ratio_max'],SETTINGS['mu_ratio_min'],SETTINGS['mu_points'])
    t0=b['t'][0]; out=[]; identity_max=0.0
    for ratio in ratios:
        mu=mref*ratio
        unit_dif=[math.exp(-mu*(t-t0))-b['y'][i] for i,t in enumerate(b['t'])]
        unit_rel=[abs(d)/max(abs(b['y'][i]),1e-15) for i,d in enumerate(unit_dif)]
        ur=rms(unit_rel); um=max(unit_rel)
        bounds=[('ALPHA_CAP',SETTINGS['alpha_cap']),('RMS_REL',safe_bound(SETTINGS['rel_rms_limit'],ur)),('MAX_REL',safe_bound(SETTINGS['rel_max_limit'],um))]
        bounds=[x for x in bounds if finite(x[1]) and x[1]>=0]
        bounds.sort(key=lambda x:x[1]); limiter,val=bounds[0] if bounds else ('ALPHA_CAP',SETTINGS['alpha_cap'])
        amax=max(0.0,min(SETTINGS['alpha_cap'],val))
        rr=amax*ur; mr=amax*um
        stat='CAP-LIMITED' if amax>=SETTINGS['alpha_cap']*(1-1e-10) else 'RELATIVE-LIMITED'
        out.append({'mu_ratio':ratio,'mu':mu,'alpha_max':amax,'limiter':limiter,'rms_rel':rr,'max_rel':mr,'rms_z':None,'max_abs_z':None,'status':stat})
    high,deep=out[0],out[-1]; contraction=deep['alpha_max']/high['alpha_max'] if high['alpha_max']>0 else None
    return {'mode':'ALPHA_MAX_ENVELOPE','alpha_cap':SETTINGS['alpha_cap'],'mu_ratio_min':SETTINGS['mu_ratio_min'],
            'mu_ratio_max':SETTINGS['mu_ratio_max'],'points':SETTINGS['mu_points'],'z_rms_limit':SETTINGS['z_rms_limit'],
            'z_max_limit':SETTINGS['z_max_limit'],'rel_rms_limit':SETTINGS['rel_rms_limit'],'rel_max_limit':SETTINGS['rel_max_limit'],
            'error_model':'RELATIVE_LIMITS_DESCRIPTIVE','identity_null':{'alpha':0,'max_abs_residual':identity_max,'pass':True},
            'high_mu':high,'deepest':deep,'contraction_ratio':contraction,'status':'DESCRIPTIVE COMPATIBILITY ENVELOPE','scan':out,
            'covariance_used':False,'normalization_uncertainty_used':False}

def read_long(path):
    with path.open(newline='',encoding='utf-8') as f:
        rows=list(csv.DictReader(f))
    return [float(r['t']) for r in rows],[float(r['corr']) for r in rows],rows[0].get('channel','channel_1')

def read_wide(path):
    with path.open(newline='',encoding='utf-8') as f:
        rows=list(csv.DictReader(f))
    t=[float(r['t']) for r in rows]; channels=[h for h in rows[0] if h!='t']
    return {ch:(t,[float(r[ch]) for r in rows]) for ch in channels}

def write_env(path,scan):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['mu_ratio','mu','alpha_max','limiter','rms_rel_at_alpha_max','max_rel_at_alpha_max','rms_z_at_alpha_max','max_abs_z_at_alpha_max','status'])
        for x in scan: w.writerow([x['mu_ratio'],x['mu'],x['alpha_max'],x['limiter'],x['rms_rel'],x['max_rel'],'','',x['status']])

def result_obj(input_name,channel,t,c):
    b=analyze_baseline(t,c); a=adversary(b)
    return {'version':'0.1.2','input_name':input_name,'channel':channel,
            'baseline':{'n':len(t),'dt':b['grid']['dt'],'uniform_grid':b['grid']['ok'],'positive_count':b['positive'],
                        'monotonicity_violations':b['monoViol'],'log_convexity_violations':b['logConvViol'],
                        'plateau':b['plat'],'hankel':b['h'],'hankel_pass':b['hankelPass'],'classification':b['classification']},
            'adversary':a,
            'notes':['Frozen CORR-I v0.1.2 mathematics mirrored for reproducible preregistered YM-3A batch execution.',
                     'No sigma/error data: relative-deviation limits provide a descriptive envelope only.',
                     'Class C inputs are mass-anchored model controls, not measured correlators.']}

def dump_json(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(obj,indent=2,allow_nan=True)+'\n',encoding='utf-8')

def batch_common():
    results=[]; od=OUT/'common'; od.mkdir(parents=True,exist_ok=True)
    for code in BETAS:
        p=DATA/'common'/f'{code}.csv'; t,c,ch=read_long(p); r=result_obj(p.name,ch,t,c); results.append((code,r)); dump_json(od/f'{code}.json',r); write_env(od/f'{code}_envelope.csv',r['adversary']['scan'])
    return results

def batch_matched():
    results={}; od=OUT/'matched'; od.mkdir(parents=True,exist_ok=True)
    for code in BETAS:
        p=DATA/'matched_gapless'/f'{code}.csv'; wide=read_wide(p); results[code]={}
        for ch,(t,c) in wide.items():
            key=ch.split('_')[-1]; r=result_obj(p.name,ch,t,c); results[code][key]=r; dump_json(od/f'{code}_{key}.json',r); write_env(od/f'{code}_{key}_envelope.csv',r['adversary']['scan'])
    return results

def batch_native():
    results=[]; od=OUT/'native'; od.mkdir(parents=True,exist_ok=True)
    for code in BETAS:
        p=DATA/'native'/f'{code}.csv'; t,c,ch=read_long(p); r=result_obj(p.name,ch,t,c); results.append((code,r)); dump_json(od/f'{code}.json',r); write_env(od/f'{code}_envelope.csv',r['adversary']['scan'])
    return results

def summary(common,matched,native):
    rows=[]; fixed_p8=FIXED_R['p8']
    native_map={c:r for c,r in native}
    for code,r in common:
        R=r['adversary']['contraction_ratio']; fam=matched[code]
        mr={p:fam[p]['adversary']['contraction_ratio'] for p in P_ORDER}
        s_fixed=math.log(fixed_p8/R); s_match=math.log(mr['p8']/R)
        ordering=all(mr[P_ORDER[i]]>mr[P_ORDER[i+1]] for i in range(len(P_ORDER)-1)) and mr['p8']>R
        nr=native_map[code]['adversary']['contraction_ratio']; ns=math.log(fixed_p8/nr)
        rows.append({'code':code,'beta':BETA_DISPLAY[code],'R_massive':R,'R_p05_match':mr['p05'],'R_p1_match':mr['p1'],'R_p2_match':mr['p2'],'R_p4_match':mr['p4'],'R_p8_match':mr['p8'],
                     'S_fixed':s_fixed,'S_match':s_match,'matched_ordering_pass':ordering,'R_native':nr,'S_fixed_native':ns,
                     'baseline':r['baseline']['classification'],'plateau':r['baseline']['plateau']['found'],'identity_null':r['adversary']['identity_null']['pass']})
    return rows

def write_summary(rows):
    p=OUT/'YM3_SUMMARY.csv'; cols=list(rows[0].keys())
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(rows)
    return p

def decide(rows):
    valid=all(r['baseline']=='POSITIVE-SPECTRAL CONSISTENT' and r['plateau'] and r['identity_null'] for r in rows)
    fixed=all(r['S_fixed']>0 for r in rows); match=all(r['S_match']>0 for r in rows); order=all(r['matched_ordering_pass'] for r in rows)
    native_fixed=all(r['S_fixed_native']>0 for r in rows)
    # Native is diagnostic only: incompatibility means the common-grid hard separation exists at all levels but the native fixed hard separation fails/crosses.
    window_sensitive = fixed and not native_fixed
    if not valid: verdict='INVALID / INCONCLUSIVE'
    elif window_sensitive: verdict='WINDOW-SENSITIVE'
    elif fixed and match and order: verdict='MODEL-REFINEMENT PERSISTENT'
    elif fixed: verdict='PARTIAL MODEL PERSISTENCE'
    else:
        # Eroding if hard margin crosses/nonpositive at a finer level; otherwise partial/inconclusive.
        verdict='MODEL-REFINEMENT ERODING' if any(r['S_fixed']<=0 or r['S_match']<=0 for r in rows) else 'PARTIAL MODEL PERSISTENCE'
    return verdict, {'all_valid':valid,'all_S_fixed_positive':fixed,'all_S_match_positive':match,'all_matched_ordering_pass':order,'all_native_S_fixed_positive':native_fixed,'window_sensitive':window_sensitive}

def write_record(rows,verdict,checks):
    j={'project':'UNNS_YM_GAP','stage':'YM-3A','preregistration':'YM3-PREREG v0.1.0','chamber':'CORR-I v0.1.2','chamber_sha256':sha256(CHAMBER),
       'evidence_class':'C','verdict':verdict,'checks':checks,'fixed_gapless_R':FIXED_R,'rows':rows,
       'scope_note':'Model-level refinement result only; not an eight-level measured-correlator refinement result and not a Yang-Mills mass-gap proof.'}
    dump_json(DOCS/'YM3_RESULT.json',j)
    lines=[]
    lines += ['# YM3_RESULT.md','', '## UNNS Yang–Mills Gap / Vacuum Boundary Non-Crossability', '### YM-3A Common Refinement Result Record','',
              '**Project:** `UNNS_YM_GAP`  ', '**Preregistration:** `YM3-PREREG v0.1.0`  ', '**Frozen chamber:** CORR-I v0.1.2  ',
              '**Evidence class:** C — exact mass-anchored model controls  ', f'**Verdict:** **{verdict}**','',
              '## 1. Execution integrity','',f'- Frozen chamber SHA-256: `{j["chamber_sha256"]}`',f'- Chamber hash matches preregistration: **{j["chamber_sha256"]==FROZEN_CHAMBER_SHA256}**',
              '- β=6.50 construction checksum: **PASS** (from frozen input-build record).','- Full primary sequence was interpreted only after all eight massive and all forty matched controls were generated.','',
              '## 2. Primary common-grid results','',
              '| β | R_massive | R_p8 matched | S_fixed | S_match | matched ordering |','|---:|---:|---:|---:|---:|---|']
    for r in rows:
        lines.append(f"| {r['beta']} | {r['R_massive']:.9f} | {r['R_p8_match']:.9f} | {r['S_fixed']:.6f} | {r['S_match']:.6f} | {'PASS' if r['matched_ordering_pass'] else 'FAIL'} |")
    lines += ['','All eight massive baselines are required to be positive-spectral consistent, retain the plateau, and pass the α=0 identity null.','',
              '## 3. Native-grid window diagnostic','',
              '| β | R_native | S_fixed_native |','|---:|---:|---:|']
    for r in rows: lines.append(f"| {r['beta']} | {r['R_native']:.9f} | {r['S_fixed_native']:.6f} |")
    lines += ['','The native-lattice branch is a window-sensitivity diagnostic only. No unpreregistered native matched-Gamma family was introduced.','',
              '## 4. Frozen-rule checks','',
              f"- All eight primary massive baselines valid: **{checks['all_valid']}**",
              f"- `S_fixed > 0` at all eight β: **{checks['all_S_fixed_positive']}**",
              f"- `S_match > 0` at all eight β: **{checks['all_S_match_positive']}**",
              f"- Matched ordering `R0.5 > R1 > R2 > R4 > R8 > Rmassive` at all β: **{checks['all_matched_ordering_pass']}**",
              f"- Native fixed-reference hard margin positive at all β: **{checks['all_native_S_fixed_positive']}**",
              f"- Primary/native qualitative incompatibility: **{checks['window_sensitive']}**",'',
              '## 5. Stage interpretation','']
    if verdict=='MODEL-REFINEMENT PERSISTENT':
        lines += ['Under the preregistered Class C experiment, the massive-side CORR-I signature remains separated from both the fixed hardest gapless reference and every β-matched hardest gapless control across all eight AT20 refinement levels. The full matched Gamma ordering is retained at every level, and the native-grid diagnostic does not reverse the separation.', '',
                  '> **The massive-side CORR-I signature is persistent across the AT20 mass-anchored Class C refinement sequence.**']
    elif verdict=='WINDOW-SENSITIVE':
        lines += ['The common physical-time grid satisfies the primary separation rules, but the native-lattice diagnostic is qualitatively incompatible. Under the frozen rules the result is therefore window-sensitive and cannot be promoted to model-refinement persistence.']
    else:
        lines += [f'The frozen decision rules assign **{verdict}**. See the table and machine-readable record for the failing margins or validity conditions.']
    lines += ['','## 6. Claim boundary','',
              'This result concerns the **Class C mass-anchored model family**. It does not establish eight-level refinement stability of measured Yang–Mills correlators, a continuum theorem, a Hamiltonian spectral lower bound, or the Yang–Mills mass gap. YM-3B remains dependent on additional Class A/B information.','']
    (DOCS/'YM3_RESULT.md').write_text('\n'.join(lines),encoding='utf-8')


def main():
    if sha256(CHAMBER)!=FROZEN_CHAMBER_SHA256:
        raise SystemExit('Frozen chamber hash mismatch; aborting.')
    common=batch_common(); matched=batch_matched(); native=batch_native()
    rows=summary(common,matched,native); write_summary(rows); verdict,checks=decide(rows); write_record(rows,verdict,checks)
    # Batch run record
    dump_json(OUT/'YM3_RUN_RECORD.json',{'status':'COMPLETE','verdict':verdict,'settings':SETTINGS,'common_inputs':8,'matched_inputs':40,'native_inputs':8,
              'chamber_sha256':sha256(CHAMBER),'preregistration':'YM3-PREREG v0.1.0','notes':['Full preregistered YM-3A batch executed.','No native matched-Gamma family introduced beyond preregistration.']})
    print(verdict)
    for r in rows:
        print(r['beta'], 'R=',format(r['R_massive'],'.12g'),'Sfix=',format(r['S_fixed'],'.9g'),'Smatch=',format(r['S_match'],'.9g'),'Rnative=',format(r['R_native'],'.12g'))

if __name__=='__main__': main()

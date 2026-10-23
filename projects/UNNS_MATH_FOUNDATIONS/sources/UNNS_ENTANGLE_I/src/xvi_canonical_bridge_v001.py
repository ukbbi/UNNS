"""Source-locked XVI canonical bridge audit. Python stdlib only.

Mathematical result concerns a 1D longitudinal Fourier mode embedded in the
2D periodic grid. This is a direct counterexample to exact Helmholtz projection
for the original, UNCHANGED Javascript projectFlux implementation.
"""
from __future__ import annotations
import hashlib
import json
import math
import re
import subprocess
import shutil
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
LOCK = PROJECT / 'config/XVI_BRIDGE_LOCK_v001.json'
OUTPUT = PROJECT / 'output/XVI_CANONICAL_BRIDGE_v001.json'


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_lock(project: Path = PROJECT) -> dict:
    lock = json.loads((project / 'config/XVI_BRIDGE_LOCK_v001.json').read_text(encoding='utf-8'))
    checks = {}
    for name, item in lock['inputs'].items():
        p = project / item['path']
        checks[name] = {'path': item['path'], 'expected_sha256': item['sha256'],
                        'actual_sha256': digest(p) if p.is_file() else None}
        checks[name]['pass'] = checks[name]['expected_sha256'] == checks[name]['actual_sha256']
    return {'all_pass': all(v['pass'] for v in checks.values()), 'checks': checks}


def source_audit(project: Path = PROJECT) -> dict:
    html = (project / 'docs/sources/XVI_ENGINE_v084.html').read_text(encoding='utf-8')
    frag = html[html.index('  projectFlux() {'):html.index('  // ========================================\n  // SPATIAL OPERATORS', html.index('  projectFlux() {'))]
    return {'engine_v084': "this.version = '0.8.4'" in html,
            'divergence_stencil_factor': '(2 * Math.PI) / (2.0 * this.W)' in frag,
            'spectral_k_factor': 'const factor = 2 * Math.PI / this.W' in html,
            'spectral_poisson': 'psi_hat_real[i] = -divJ_hat_real[i] / k2' in frag,
            'spectral_gradient': 'gradPsiX_hat_real[i] = -kx * psi_hat_imag[i]' in frag,
            'flux_correction': 'Jx[i] -= gradPsiX[i]' in frag,
            'metric_is_preprojection_divergence': 'const {divJ} = this.closure' in html and 'const mean_divJ = this.mean(divJ)' in html,
            'idempotence_is_tau_update_not_P_squared': 'const tau_before = new Float64Array(this.fields[0].tau)' in html and 'this.applyClosure(0)' in html,
            'export_version_mismatch': "version: '0.8.0'" in html,
            'c3_is_mean_over_rms_proxy': 'Math.abs(mean_divJ) / (rms_divJ + 1e-12)' in html}


def longitudinal_mode(N: int, m: int = 1) -> dict:
    if N < 8 or m < 1 or 2*m >= N:
        raise ValueError('Require N>=8 and 1<=m<N/2')
    theta = 2*math.pi*m/N
    source_k = 2*math.pi*m/N  # this.fft_cache.kx_grid, not physical k on a 2pi-domain
    source_scale = math.pi/N  # (J[x+1]-J[x-1]) coefficient
    source_deriv = 2*source_scale*math.sin(theta)
    corrected_fraction = source_deriv/source_k  # sin(theta)/m
    residual = 1-corrected_fraction
    return {'N': N, 'mode': m, 'theta':theta,
            'original_divergence_ratio_after_before':residual,
            'corrected_longitudinal_fraction':corrected_fraction,
            'relative_L2_energy_decomposition_defect':2*residual*corrected_fraction,
            'relative_projection_idempotence_defect':residual*corrected_fraction,
            'second_projection_ratio_to_original':residual**2,
            'ideal_spectral_comparator_divergence_ratio':0.0,
            'original_divergence_mean_is_zero':True}


def summarize_exports(project: Path = PROJECT) -> list[dict]:
    lock = json.loads((project/'config/XVI_BRIDGE_LOCK_v001.json').read_text(encoding='utf-8'))
    runs = []
    for key in ('run64','run128a','run128b','run256'):
        data = json.loads((project/lock['inputs'][key]['path']).read_text(encoding='utf-8'))
        timeline = data.get('timeline', [])
        crit=data.get('criteria', {})
        runs.append({'source':key, 'export_version':data.get('version'), 'engine_label':data.get('operator'),
                     'config':data.get('config'), 'timeline_count':len(timeline),
                     'first_logged_preprojection_rms_divJ':timeline[0].get('rms_divJ') if timeline else None,
                     'last_logged_preprojection_rms_divJ':timeline[-1].get('rms_divJ') if timeline else None,
                     'last_logged_mean_divJ':timeline[-1].get('mean_divJ') if timeline else None,
                     'validation_mode':crit.get('validation_mode'),
                     'criteria':crit,
                     'warning':'Mean and RMS divJ refer to ORIGINAL (pre-projection) flux at each step. No post-projection divergence series or raw fields are exported.'})
    return runs


def run_node_probe(project: Path = PROJECT) -> dict:
    exe = shutil.which('node')
    if exe is None: return {'status':'NODE_NOT_INSTALLED', 'nonblocking':True}
    run = subprocess.run([exe, str(project/'tools/xvi_original_engine_probe_v001.cjs')],
                         cwd=project, capture_output=True, text=True, timeout=90)
    if run.returncode: return {'status':'NODE_ERROR', 'nonblocking':False, 'stderr':run.stderr[-3000:]}
    result = json.loads(run.stdout)
    return {'status':'ORIGINAL_ENGINE_EXECUTED', 'nonblocking':False, 'result':result}


def build_report(project: Path = PROJECT, try_node:bool=False) -> dict:
    lock=verify_lock(project)
    if not lock['all_pass']:
        raise RuntimeError('FROZEN_INPUT_HASH_MISMATCH: refusing research report')
    audit=source_audit(project)
    if not all(audit.values()):
        raise RuntimeError('SOURCE_FORMULA_AUDIT_FAILED: implementation differs from source lock')
    models=[longitudinal_mode(N) for N in (64,128,256)]
    report={'protocol':'XVI_CANONICAL_BRIDGE_v001',
            'scientific_scope':'original Chamber XVI v0.8.4 single-mode discrete projection audit; not a Born-rule derivation',
            'baseline_integrity_pass':True,'input_lock':lock,
            'source_formula_checks':audit,
            'fourier_mode_analytic':models,
            'export_audit':summarize_exports(project),
            'original_js_probe':run_node_probe(project) if try_node else {'status':'NOT_RUN','nonblocking':True},
            'gates':{'B0':'PASS_FROZEN','B1':'PASS_SOURCE_IDENTIFIED',
                     'B2':'FAIL_EXACT_DIVERGENCE_FREE_FOR_ORIGINAL',
                     'B3':'FAIL_IDEMPOTENCE_AND_L2_ORTHOGONALITY_FOR_ORIGINAL',
                     'B4':'IDEAL_SPECTRAL_REFERENCE_ONLY',
                     'B5':'BLOCKED_NO_OBSERVABLE_EVENT_BRIDGE',
                     'B6':'NOT_DERIVED_BORN_RULE'},
            'primary_verdict':'CANONICAL_IMPLEMENTATION_OBSTRUCTION',
            'interpretation':'The actual original source mixes derivative symbols; an explicit Fourier mode is not projected to divergence-free. The ideal L2 Helmholtz decomposition remains valid with matched operators and boundary conditions, but does not supply a quantum probability postulate.'}
    return report


def main():
    report=build_report(try_node=False)
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    OUTPUT.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(f'WROTE {OUTPUT.relative_to(PROJECT)}  BASELINE PASS  IMPLEMENTATION OBSTRUCTION  BORN RULE NOT DERIVED')
    print('Node direct engine check (optional): node tools/xvi_original_engine_probe_v001.cjs')

if __name__=='__main__':main()

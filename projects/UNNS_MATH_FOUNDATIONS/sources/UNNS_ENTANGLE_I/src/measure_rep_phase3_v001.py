"""Phase 3: projection-measure representation audit, NOT a UNNS Born-rule derivation."""
import hashlib, json, math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / 'config' / 'PHASE3_LOCK.json'

def verify_lock(root=ROOT):
    lock = json.loads((root/'config'/'PHASE3_LOCK.json').read_text(encoding='utf-8'))
    frozen = root / lock['frozen_path']
    if hashlib.sha256(frozen.read_bytes()).hexdigest() != lock['sha256']:
        raise RuntimeError('Phase 2C frozen baseline integrity FAIL')
    active = root / lock['active_path']
    if active.exists() and hashlib.sha256(active.read_bytes()).hexdigest()!=lock['sha256']:
        raise RuntimeError('Active Phase 2C differs from frozen baseline; do not overwrite')
    return True

def contextual_counterexample():
    return {'C':{'e':0.25,'a':0.75}, 'D':{'e':0.75,'b':0.25}}

def frame2(theta,eps=0.5):
    return (1+eps*math.cos(6*theta))/2

def frame3_raw(q, components):
    return sum(abs(v)**q for v in components)

def generate():
    verify_lock()
    c=contextual_counterexample()
    q_cases=[]
    for q in [1,1.5,2,3,6]:
        initial=frame3_raw(q,(1,0,0))
        rotated=frame3_raw(q,(1/math.sqrt(3),)*3)
        q_cases.append({'q':q,'frame1_weight':initial,'frame2_weight':rotated,'defect':rotated-initial})
    report={'protocol':'MEASURE_REP_PHASE3_v001',
      'phase2c_integrity_pass':True,
      'contextual_countermodel':c,
      'context_probabilities_normalized':all(abs(sum(x.values())-1)<1e-12 for x in c.values()),
      'shared_event_context_difference':c['D']['e']-c['C']['e'],
      'two_dimensional_nonborn_frame_example':{'epsilon':0.5,'harmonic':6,'samples':[{'theta':t,'orthogonal_pair_sum':frame2(t)+frame2(t+math.pi/2)} for t in [0,0.17,0.41,0.79]]},
      'three_dimensional_power_frame_controls':q_cases,
      'gates':{'R0':'PASS','R1':'COUNTEREXAMPLE_PASS','R2':'COUNTEREXAMPLE_PASS','R3':'FINITE_CONTROL_PASS','R4':'UNPROVED_ASSUMPTIONS','R5':'BLOCKED_NOT_DERIVED'},
      'claim':'No UNNS quantum measure has been derived. Known Hilbert-space representation results are conditional references only.'}
    return report

def main():
    report=generate()
    out=ROOT/'output'/'MEASURE_REP_PHASE3_v001.json'
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print('WROTE',out,'BASELINE PASS PRIMARY BLOCKED_NOT_DERIVED')
if __name__=='__main__': main()

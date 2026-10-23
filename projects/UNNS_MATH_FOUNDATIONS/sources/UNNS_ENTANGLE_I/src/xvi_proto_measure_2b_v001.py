"""Phase 2B logical controls; NOT canonical Operator XVI."""
from pathlib import Path
import hashlib,json,math

ROOT=Path(__file__).resolve().parent.parent

def sha256(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def orbit(n):
    if n < 0: raise ValueError('nonnegative n required')
    return tuple('A' if i%2==0 else 'B' for i in range(n))

def discrete_distance(a,b): return 0 if a==b else 1

def proto_closed(n=40,eps=0.5):
    if n<4 or not (0<eps<1): raise ValueError('invalid finite witness parameters')
    seq=orbit(n)
    return len(set(seq))>1 and all(discrete_distance(seq[i],seq[i+2])<eps for i in range(n-2))

def projection(state):
    return {'A':(1.0,0.0),'B':(0.0,1.0)}[state]

def weight(v,q):
    if q<=0: raise ValueError('q must be positive')
    return math.hypot(*v)**q

def defect(q,u=(1.0,0.0),v=(0.0,1.0)):
    return weight((u[0]+v[0],u[1]+v[1]),q)-weight(u,q)-weight(v,q)

def verify_baselines():
    lock=json.loads((ROOT/'config/PHASE2B_LOCK.json').read_text(encoding='utf-8'))
    checks={}
    for name,expected in lock['source_baselines'].items():
        frozen=ROOT/'output/frozen'/name
        checks[name]={'expected_sha256':expected,'actual_sha256':sha256(frozen), 'pass':sha256(frozen)==expected}
        active=ROOT/'output'/name
        if active.exists():
            checks[name]['active_sha256']=sha256(active)
            checks[name]['active_matches_frozen']=sha256(active)==expected
    return checks

def build_report():
    checks=verify_baselines()
    return {
        'protocol':'XVI_PROTO_MEASURE_2B_v001',
        'baseline_integrity_pass':all(v['pass'] and v.get('active_matches_frozen',True) for v in checks.values()),
        'baselines':checks,
        'canonical_operator_evaluated':False,
        'proto_closure_finite_witness':proto_closed(),
        'sampled_q':[{'q':q,'orbit_weights':[weight(projection(s),q) for s in orbit(4)], 'orthogonal_additivity_defect':defect(q)} for q in (1.0,1.5,2.0,3.0,6.0)],
        'primary_theorem':'OPEN_B3_NOT_DERIVED',
        'conclusion':'Proto-closure does not select q. Orthogonal additivity selects q=2 only when independently supplied.'
    }

def main():
    report=build_report();out=ROOT/'output/XVI_PROTO_MEASURE_2B_v001.json'
    out.parent.mkdir(exist_ok=True,parents=True)
    out.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(f'WROTE {out} BASELINE {"PASS" if report["baseline_integrity_pass"] else "FAIL"} PRIMARY OPEN/BLOCKED')
    return 0 if report['baseline_integrity_pass'] else 1

if __name__=='__main__': raise SystemExit(main())

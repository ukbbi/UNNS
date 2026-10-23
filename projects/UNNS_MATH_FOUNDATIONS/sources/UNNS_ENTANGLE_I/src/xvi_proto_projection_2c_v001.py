"""Phase 2C: honest constructive audit, not a Born-rule derivation."""
from pathlib import Path
import hashlib,json,math
ROOT=Path(__file__).resolve().parent.parent

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def orbit(n):
    if n<0: raise ValueError('n>=0 required')
    return ['A' if k%2==0 else 'B' for k in range(n)]
def recurrence_witness(n=20):
    s=orbit(n)
    return n>=4 and len(set(s))==2 and all(s[i]==s[i+2] for i in range(n-2))
def projection(state,theta=0.0,scale=1.0):
    if state not in ('A','B') or scale<=0: raise ValueError('invalid projection')
    a=(0.0 if state=='A' else math.pi/2)+theta
    return (scale*math.cos(a),scale*math.sin(a))
def weight(v,q):
    if q<=0: raise ValueError('q>0')
    return math.hypot(*v)**q
def defect(q,theta=0.0,scale=1.0):
    u=projection('A',theta,scale);v=projection('B',theta,scale)
    return weight((u[0]+v[0],u[1]+v[1]),q)-weight(u,q)-weight(v,q)
def lock_ok():
    lk=json.loads((ROOT/'config/PHASE2C_LOCK.json').read_text(encoding='utf-8'))
    frozen=ROOT/'output/frozen'/lk['phase2b_filename']
    same=sha(frozen)==lk['phase2b_sha256']
    active=ROOT/'output'/lk['phase2b_filename']
    return same and (not active.exists() or sha(active)==lk['phase2b_sha256'])
def report():
    return {'protocol':'XVI_PROTO_PROJECTION_2C_v001','baseline_integrity_pass':lock_ok(),
            'finite_proto_closure_witness':recurrence_witness(),
            'projection':'Pi_theta,s(A)=s R_theta e1, Pi_theta,s(B)=s R_theta e2; exploratory',
            'q_countermodels':[{'q':q,'refinement_additivity_defect':defect(q)} for q in [1,1.5,2,3,6]],
            'rotation_controls':[{'theta':t,'q1_defect':defect(1,t),'q2_defect':defect(2,t)} for t in [0,math.pi/7,math.pi/3]],
            'scaling_controls':[{'scale':s,'q1_defect':defect(1,scale=s),'q2_defect':defect(2,scale=s)} for s in [0.5,1,2]],
            'gates':{'C0':'PASS' if lock_ok() else 'FAIL','C1':'FINITE_WITNESS_PASS','C2':'CONSTRUCTED_TOY','C3':'OPEN_NOT_DERIVED','C4':'FAIL_UNCONDITIONAL_OPEN_CANONICAL','C5':'NOT_ATTEMPTED'},
            'primary_theorem':'OPEN_NOT_DERIVED',
            'claim':'Proto-closure and an unspecified observation map do not imply orthogonal additivity.'}
def main():
    r=report();o=ROOT/'output/XVI_PROTO_PROJECTION_2C_v001.json';o.parent.mkdir(parents=True,exist_ok=True)
    o.write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
    print('WROTE',o,'BASELINE',r['gates']['C0'],'PRIMARY',r['primary_theorem'])
    return 0 if r['baseline_integrity_pass'] else 1
if __name__=='__main__': raise SystemExit(main())

"""Phase 2 preregistered toy countermodel audit; canonical XVI not included."""
import argparse,hashlib,json,math
from pathlib import Path

def defect(q,x,y):
    if q<=0: raise ValueError('q must be positive')
    return math.hypot(x,y)**q-abs(x)**q-abs(y)**q

def report(project_root):
    root=Path(project_root); lock=json.loads((root/'config/PHASE2_LOCK.json').read_text())
    blob=(root/lock['phase1_baseline_path']).read_bytes()
    actual=hashlib.sha256(blob).hexdigest()
    cases=[{'q':q,'defect_1_1':defect(q,1,1),'defect_2_3':defect(q,2,3)} for q in (1,1.5,2,3,6)]
    return {'protocol':'XVI_REFINEMENT_PHASE2_v001','phase1_sha256':actual,'phase1_integrity_pass':actual==lock['phase1_sha256'],'canonical_operator_evaluated':False,'primary_theorem':'BLOCKED_PENDING_CANONICAL_SOURCE','controls':cases,'interpretation':'Radial countermodels only; additivity is not implied by rotational closure.'}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--project-root',default=None);args=parser.parse_args()
    root=Path(args.project_root) if args.project_root else Path(__file__).resolve().parents[1]
    result=report(root); target=root/'output/XVI_REFINEMENT_v001.json';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(result,indent=2)+'\n')
    print('WROTE',target,'BASELINE', 'PASS' if result['phase1_integrity_pass'] else 'FAIL','PRIMARY BLOCKED')
    if not result['phase1_integrity_pass']: raise SystemExit(2)
if __name__=='__main__': main()

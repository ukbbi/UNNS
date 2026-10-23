"""Reproducible GCT v002: representation, recursion, Bell assumption and uniqueness audit."""
from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path
from .gct_joint_core_v002 import chsh, evolve_parity, joint_probabilities, marginals, parity_stationary
from .gct_countermodels_v002 import local_shared_route,saturated_joint_route
from .gct_quantum_comparator_v002 import singlet_reference

ROOT=Path(__file__).resolve().parents[1]
LOCK=ROOT/'config/GCT_LOCK_v002.json'
OUT=ROOT/'output/GCT_JOINT_ORIGIN_v002.json'
ANGLES=(0.,math.pi/2,math.pi/4,-math.pi/4)


def freeze_check()->dict:
    lock=json.loads(LOCK.read_text(encoding='utf-8'))
    checks={}
    for p,expected in lock['baseline_sha256'].items():
        actual=hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
        checks[p]={'expected_sha256':expected,'actual_sha256':actual,'pass':actual==expected}
    if lock['prior_verdict']!='NO_GO_WITH_LOCAL_FACTORIZATION':
        raise ValueError('v001 verdict must not be rewritten')
    if not all(x['pass'] for x in checks.values()):
        raise RuntimeError('frozen v001 baseline hash mismatch')
    return {'all_pass':True,'checks':checks,'original_v001_unchanged':True}


def case(name,kernel)->dict:
    settings=[(0.,0.),(0.,math.pi/8),(0.,math.pi/4),(0.,math.pi/2),(0.,math.pi)]
    samples=[]
    for a,b in settings:
        p=joint_probabilities(a,b,kernel)
        pa,pb=marginals(p)
        samples.append({'delta':a-b,'correlation':sum(A*B*v for (A,B),v in p.items()),
                        'p_pp':p[(1,1)],'p_pm':p[(1,-1)],'p_mp':p[(-1,1)],'p_mm':p[(-1,-1)],
                        'marginals_A':{str(k):v for k,v in pa.items()},
                        'marginals_B':{str(k):v for k,v in pb.items()},
                        'support':[f'{A},{B}' for (A,B),v in p.items() if v>1e-12]})
    s=chsh(kernel,*ANGLES)
    return {'name':name,'chsh_S':s,'abs_chsh':abs(s),'samples':samples,
            'recursion':{'refresh':0.3,'initial':{'-1':1.,'1':0.},
                         'stationary':{str(k):v for k,v in parity_stationary(kernel(0.,math.pi/8)).items()},
                         'after_25':{str(k):v for k,v in evolve_parity({-1:1.,1:0.},kernel(0.,math.pi/8),0.3,25).items()}}}


def main()->dict:
    locks=freeze_check()
    cases=[case('local_angle_overlap',local_shared_route),
           case('QUARANTINED_singlet_reference',singlet_reference),
           case('smooth_saturated_joint',saturated_joint_route)]
    c0,c1,c2=cases
    assert abs(c0['abs_chsh']-2.)<1e-12
    assert abs(c1['abs_chsh']-2*math.sqrt(2))<1e-12
    assert 2*math.sqrt(2)<c2['abs_chsh']<4.
    probe=[entry['correlation'] for entry in (x['samples'][1] for x in cases)]
    assert max(probe)-min(probe)>.1
    data={'protocol':'GCT_JOINT_ORIGIN_v002','scope':'A proof of underdetermination and a constructed nonfactorizable joint-context recursion; not canonical UNNS quantum dynamics',
          'previous_v001':{'verdict':'NO_GO_WITH_LOCAL_FACTORIZATION','frozen':locks},
          'theorems':{
           'representation':'Symmetric normalized binary pair outcomes yield P(A,B|a,b)=(1+AB*C(a,b))/4.',
           'stationary_recursion':'A refreshed joint parity route converges to pi(z)=(1+zC)/2 for each exogenously specified kernel C.',
           'bell_boundary':'If measurement independence and Bell-local factorization are both retained, |CHSH|<=2.',
           'nonuniqueness':'Different kernels satisfy identical structural symmetries, alignment, normalization and no-signalling but have distinct joint correlations and CHSH values.'},
          'frozen_chsh_settings':{'a':ANGLES[0],'a_prime':ANGLES[1],'b':ANGLES[2],'b_prime':ANGLES[3]},
          'cases':cases,
          'gates':{'J0':'PASS_V001_INTEGRITY','J1':'PROVED_BINARY_REPRESENTATION','J2':'PROVED_STATIONARY_RECURSION','J3':'PROVED_OPERATIONAL_NO_SIGNALLING','J4':'PASS_LOCAL_BELL_BOUND','J5':'PASS_CONSTRUCTIVE_NONUNIQUENESS','J6':'CONTEXT_DEPENDENCE_EXPLICITLY_NOT_BELL_LOCAL','J7':'UNPROVED_UNNS_SELECTION_OF_KERNEL','J8':'NOT_DERIVED_BORN_RULE'},
          'scientific_verdict':'UNDERDETERMINED_NONLOCAL_GENERATIVE_RULE','interpretation':'A shared joint recursion does not supply a unique correlation kernel. Bell violation can be represented only when nonfactorizable context dependence is built into the mechanism; doing this is not a derivation of the singlet correlations from UNNS axioms.'}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print('WROTE',OUT.relative_to(ROOT))
    print('VERDICT',data['scientific_verdict'])
    return data

if __name__=='__main__':
    main()

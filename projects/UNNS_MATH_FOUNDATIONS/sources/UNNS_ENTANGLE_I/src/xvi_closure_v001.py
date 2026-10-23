"""Operator XVI Phase 1: mathematically separate toy closure from refinement.

No quantum rule is embedded in the recursion. Python standard library only.
"""
from __future__ import annotations
import argparse, json, math

def radial_weight(x: float, y: float, q: float) -> float:
    if q <= 0: raise ValueError('q must be positive')
    return math.hypot(x, y)**q

def anisotropic_weight(x: float, y: float, epsilon: float = 0.4) -> float:
    r2=x*x+y*y
    if not r2: return 0.0
    return r2*(1+epsilon*(x*x-y*y)/r2)

def rotation_average(weight, x: float, y: float, n: int = 4096) -> float:
    if n < 8: raise ValueError('n must be >= 8')
    values=[]
    for k in range(n):
        t=2*math.pi*k/n
        values.append(weight(x*math.cos(t)-y*math.sin(t),x*math.sin(t)+y*math.cos(t)))
    return math.fsum(values)/n

def iterate_closure(weight, x: float, y: float, steps: int, n: int = 4096) -> float:
    """Exact iterate formula using numerical Haar quadrature for A[w]."""
    initial=weight(x,y); avg=rotation_average(weight,x,y,n)
    return avg+2**(-steps)*(initial-avg)

def refinement_defect(q: float, x: float = 1.0, y: float = 1.0) -> float:
    return radial_weight(x,y,q)-radial_weight(x,0,q)-radial_weight(0,y,q)

def projection_total(q: float, angle: float) -> float:
    return abs(math.sin(angle))**q+abs(math.cos(angle))**q

def q_probabilities(q:float,a:float,b:float):
    d=a-b
    s=abs(math.sin(d))**q; c=abs(math.cos(d))**q
    z=2*(s+c)
    return {'++':s/z,'--':s/z,'+-':c/z,'-+':c/z}

def correlation(q:float,a:float,b:float)->float:
    p=q_probabilities(q,a,b)
    return p['++']+p['--']-p['+-']-p['-+']

def chsh(q:float)->float:
    a,ap,b,bp=0,math.pi/4,math.pi/8,-math.pi/8
    return abs(correlation(q,a,b)+correlation(q,a,bp)+correlation(q,ap,b)-correlation(q,ap,bp))

def run():
    cases=[]
    for q in [1,1.5,2,3,6]:
        cases.append({'q':q,'radial_recursion_fixed_point':True,
                      'refinement_defect_at_1_1':refinement_defect(q),
                      'unnormalized_Z_at_0':projection_total(q,0),
                      'unnormalized_Z_at_pi_4':projection_total(q,math.pi/4),
                      'fixed_angle_CHSH':chsh(q),
                      'no_signalling_residual':max(abs(sum(v for k,v in q_probabilities(q,a,b).items() if k[0]=='+')-0.5)
                         for a,b in [(0,0.13),(0.7,1.1)])})
    examples=[]
    for steps in [0,1,2,4,8,16]:
        x,y=1.2,0.7; initial=anisotropic_weight(x,y)
        target=x*x+y*y
        v=iterate_closure(anisotropic_weight,x,y,steps)
        examples.append({'steps':steps,'weight':v,'expected':target+2**(-steps)*(initial-target)})
    return {'protocol':'XVI_CLOSURE_THEOREM_v001','candidate_operator':'Haar rotational averaging toy recursion (NOT canonical Operator XVI)',
            'q_cases':cases,'anisotropy_contraction':examples,
            'gates':{'G1':'PARTIAL','G2':'PARTIAL','G3':'FAIL_OPEN','G4':'FAIL','G5':'REFERENCE_PASS'},
            'conclusion':'Rotation closure leaves all radial powers fixed; q=2 needs an independently justified refinement-conservation axiom.'}

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--output',default='output/XVI_CLOSURE_v001.json'); args=parser.parse_args()
    from pathlib import Path
    destination=Path(args.output); destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_text(json.dumps(run(),indent=2)+'\n',encoding='utf-8')
    print('WROTE',destination,'G3 FAIL/OPEN; G4 FAIL (constructive counterexamples)')

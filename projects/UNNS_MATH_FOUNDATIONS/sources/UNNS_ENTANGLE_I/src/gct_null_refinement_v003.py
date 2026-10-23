"""GCT-III: source-constrained observable-null refinement countermodel.

This is an independently defined *extension* of documented UNNS structural axioms,
not the canonical UNNS operator and not an entanglement model.
Run: python -m src.gct_null_refinement_v003
Pure standard-library Python.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREVIOUS = ROOT / "docs" / "frozen" / "GCT_JOINT_ORIGIN_v002.json"
OUTPUT = ROOT / "output" / "GCT_NULL_REFINEMENT_v003.json"

Vec3 = tuple[float, float, float]

def add(a: Vec3, b: Vec3) -> Vec3:
    return tuple(x + y for x, y in zip(a, b))  # type: ignore[return-value]

def sub(a: Vec3, b: Vec3) -> Vec3:
    return tuple(x - y for x, y in zip(a, b))  # type: ignore[return-value]

def dot(a: Vec3, b: Vec3) -> float:
    return sum(x*y for x, y in zip(a, b))

def rot_z(a: Vec3, theta: float) -> Vec3:
    c, s = math.cos(theta), math.sin(theta)
    return (c*a[0]-s*a[1], s*a[0]+c*a[1], a[2])

@dataclass(frozen=True)
class Route:
    """Free two-channel route group over R^3, R=V⊕V."""
    ch0: Vec3
    ch1: Vec3

    def __add__(self, other: 'Route') -> 'Route':
        return Route(add(self.ch0, other.ch0), add(self.ch1, other.ch1))

    def __sub__(self, other: 'Route') -> 'Route':
        return Route(sub(self.ch0, other.ch0), sub(self.ch1, other.ch1))

    def scale(self, factor: float) -> 'Route':
        return Route(tuple(factor*x for x in self.ch0), tuple(factor*x for x in self.ch1))

    def rotate(self, theta: float) -> 'Route':
        return Route(rot_z(self.ch0, theta), rot_z(self.ch1, theta))


def elem(a: Vec3, channel: int) -> Route:
    zero: Vec3 = (0., 0., 0.)
    if channel == 0:
        return Route(a, zero)
    if channel == 1:
        return Route(zero, a)
    raise ValueError('channel must be 0 or 1')

def pi(x: Route) -> Vec3:
    """Observable projection: forget which route channel was used."""
    return add(x.ch0, x.ch1)

def refine(x: Route) -> Route:
    """A two-cycle on generative route identity."""
    return Route(x.ch1, x.ch0)

def b(x: Route, y: Route) -> float:
    """Admissible symmetric bilinear pairing with hidden channel information."""
    return -dot(x.ch0, y.ch0) - dot(x.ch1, y.ch1)

def b_quotient(u: Vec3, v: Vec3) -> float:
    """A *separately imposed* observable-only pairing, for comparison."""
    return -dot(u, v)

def close(x: Vec3, y: Vec3, tol=1e-12) -> bool:
    return max(abs(a-b) for a,b in zip(x,y)) <= tol

def witness():
    a: Vec3 = (1., 0., 0.)
    x0, x1 = elem(a,0), elem(a,1)
    null_x = x0 - x1
    return {
        "route_0":x0,
        "route_1":x1,
        "null_x":null_x,
        "probe":x0,
    }

def sha(path:Path)->str:
    return sha256(path.read_bytes()).hexdigest()

def run() -> dict:
    w = witness()
    x0, x1, null_x, y = (w[s] for s in ('route_0','route_1','null_x','probe'))
    base = json.loads(PREVIOUS.read_text(encoding='utf-8'))
    expected_prior_verdict = 'UNDERDETERMINED_NONLOCAL_GENERATIVE_RULE'
    previous_verdict_ok = base.get('scientific_verdict')==expected_prior_verdict
    angles = (0., math.pi/9, 0.7, math.pi/2)
    cov_errors = [abs(b(x0.rotate(t), y.rotate(t))-b(x0,y)) for t in angles]
    X, Y = x0+x1, x0
    mu_bilinear = b(X, Y)-(b(x0,Y)+b(x1,Y))
    refinement_error = b(refine(x0),refine(y)) - b(x0,y)
    pi_refinement_ok=close(pi(refine(x0)),pi(x0))
    result={
        'protocol':'GCT_NULL_REFINEMENT_v003',
        'scope':'Countermodel to observable-null entailment under documented UNNS mechanism/route/morphism requirements. Not canonical dynamics or quantum probability.',
        'source_basis':[
            {'name':'A First Introduction to the UNNS Substrate','section':'The Problem Addressed by UNNS / substrate tuple / route status'},
            {'name':'Mechanisms, Structural Closure, and Proto-Closure in the UNNS Substrate','section':'Definitions 3–7, structural equivalence and refinement'},
            {'name':'Introduction to the UNNS Substrate','section':'UNNS morphisms / exact intertwining of recursive action'}
        ],
        'prior_baseline':{
            'path':'docs/frozen/GCT_JOINT_ORIGIN_v002.json',
            'sha256':sha(PREVIOUS),
            'scientific_verdict':base.get('scientific_verdict'),
            'verdict_preserved':previous_verdict_ok
        },
        'model':{
            'route_space':'R^3 ⊕ R^3',
            'projection':'Pi(u,v)=u+v',
            'refinement':'T(u,v)=(v,u)',
            'observable_operator':'T_obs=id',
            'pairing':'B((u,v),(x,y))=-u·x-v·y',
            'symbolic_states':['route-channel-0','route-channel-1'],
            'admissible_renaming':'identity only',
            'structural_closure':'nontrivial two-cycle under T for channel-pure states',
            'same_observation_distinct_routes': close(pi(x0),pi(x1)) and x0!=x1
        },
        'checks':{
            'nontrivial_recurrence':refine(refine(x0))==x0 and refine(x0)!=x0,
            'exact_morphism':pi_refinement_ok,
            'rotational_covariance_max_abs_error':max(cov_errors),
            'bilinearity_additivity_abs_error':abs(mu_bilinear),
            'simultaneous_refinement_invariance_abs_error':abs(refinement_error),
            'perfect_aligned_anticorrelation_r0':b(x0,x0),
            'perfect_aligned_anticorrelation_r1':b(x1,x1),
            'observable_null_projection':pi(null_x),
            'observable_null_pairing':b(null_x,y),
            'observable_null_gate_passes':(close(pi(null_x),(0.,0.,0.)) and abs(b(null_x,y))<=1e-12),
            'required_quotient_pairing_value_if_imposed': b_quotient(pi(null_x),pi(y)),
        },
        'factorization_criterion':'A bilinear B on route space factors as b(PiX,PiY) if and only if ker(Pi) lies in both the left and right radicals of B (assuming Pi is onto its observable image).',
        'scientific_verdict':'NOT_ENTAILED_BY_DOCUMENTED_UNNS_AXIOMS',
        'interpretation':'An exact recursive morphism and structurally admissible refinement can preserve a hidden interaction while erasing its observable vector. To select the singlet kernel, a new interaction-factorization premise must be independently justified.'
    }
    return result

def main()->None:
    result=run()
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True),encoding='utf-8')
    print(f'WROTE {OUTPUT.relative_to(ROOT)}')
    print('VERDICT '+result['scientific_verdict'])
    print('NULL PROJECTION '+str(result['checks']['observable_null_projection']))
    print('NONZERO INTERACTION '+str(result['checks']['observable_null_pairing']))

if __name__=='__main__':
    main()

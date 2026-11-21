#!/usr/bin/env python3
"""Separate analytic second-order Maxwell perturbation certificate vs finite-eta solution."""
from __future__ import annotations
import cmath,csv,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def ic(t,omega):
    # integral_0^t exp(-i omega s) ds
    return t if abs(omega)<1e-12 else -cmath.expm1(-1j*omega*t)/(1j*omega) if hasattr(cmath,'expm1') else (1-cmath.exp(-1j*omega*t))/(1j*omega)

def sin2_fourier(t,omega):
    a=2*math.pi/t
    return .5*ic(t,omega)-.25*ic(t,omega-a)-.25*ic(t,omega+a)

def exact_born_coeff(start,q1,q2,t):
    """Abs coefficient at eta^2 for right-going m+q1+q2 after nonoverlapping traveling pulses.
    Includes exact virtual counterpropagating intermediate state.
    """
    p=start+q1;target=p+q2
    J=sin2_fourier(t,2*p)
    K=cmath.exp(2j*p*t)*J.conjugate()
    area=t/2
    return p*target/4 * abs(area*area-J*K)

def main():
    spec=json.loads((ROOT/'protocol'/'PREDICTIONS_LOCK.json').read_text())
    raw=json.loads((ROOT/'results'/'heldout_raw.json').read_text())['cases']
    eta=spec['numerics']['eta'];T=spec['numerics']['stage_duration']
    rows=[]
    for case in spec['locked_cases']:
        if not (case['first_on'] and case['second_on']):continue
        mid=case['start']+case['q_first'];tar=mid+case['q_second']
        pred=exact_born_coeff(case['start'],case['q_first'],case['q_second'],T)*eta**2
        actual=raw[case['id']]['outgoing']['after_stage_2'][str(tar)]['amplitude']
        rel=abs(pred-actual)/pred
        if rel>=.03:raise AssertionError(f'Born mismatch in {case["id"]}: {rel}')
        rows.append({'case':case['id'],'source':case['start'],'intermediate':mid,'target':tar,
                     'born_coefficient':pred/eta**2,'born_prediction':pred,
                     'maxwell_simulation':actual,'relative_difference':rel})
        print(f"PASS analytic O(eta^2) Maxwell coefficient {case['id']}: rel={rel:.4g}")
    with (ROOT/'results'/'born_comparison.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    print('MUG-I v009 BORN COEFFICIENT VERIFY PASS')

if __name__=='__main__':main()

"""Frozen Phase-0 q-family analysis. Requires Python 3.10+, numpy, scipy."""
from __future__ import annotations
import argparse, csv, json, math
from pathlib import Path
import numpy as np
from scipy.optimize import differential_evolution, brentq

ANGLES = (0., math.pi/4, math.pi/8, -math.pi/8)
QS = (1., 1.5, 2., 3., 6.)
SEED = 20261020

def probs(q: float, a: float, b: float) -> np.ndarray:
    if q <= 0: raise ValueError('q must be positive')
    d = a-b
    s, c = abs(math.sin(d))**q, abs(math.cos(d))**q
    z = 2*(s+c)
    return np.array([[s,c],[c,s]], dtype=float)/(s+c)/2

def correl(q: float,a:float,b:float)->float:
    p=probs(q,a,b)
    return float(p[0,0]+p[1,1]-p[0,1]-p[1,0])

def chsh(q:float, a:float, ap:float, b:float, bp:float)->float:
    return abs(correl(q,a,b)+correl(q,a,bp)+correl(q,ap,b)-correl(q,ap,bp))

def raw_weight(q:float, d:float)->float:
    # Four amplitudes have magnitude |sin d|/sqrt(2) twice and |cos d|/sqrt(2) twice.
    return 2**(1-q/2)*(abs(math.sin(d))**q+abs(math.cos(d))**q)

def optimized_chsh(q:float, maxiter:int=500, popsize:int=18):
    # Global rotational redundancy fixed by a=0. Remaining angles can be in [0,pi).
    fun=lambda x:-chsh(q,0.,float(x[0]),float(x[1]),float(x[2]))
    res=differential_evolution(fun, [(0,math.pi)]*3, seed=SEED,
                               tol=1e-11, atol=1e-12, popsize=popsize,
                               maxiter=maxiter, polish=True)
    return {'max_chsh_numeric':-float(res.fun), 'settings_rad':[0.]+[float(v) for v in res.x],
            'optimizer_success':bool(res.success), 'nfev':int(res.nfev),
            'method':'differential_evolution (numerical lower bound; not global proof)'}

def run(output:Path, do_optimize:bool=True):
    output.mkdir(parents=True, exist_ok=True)
    a,ap,b,bp=ANGLES
    records=[]
    for q in QS:
        r={'q':q, 'fixed_chsh':chsh(q,*ANGLES),
           'marginal_error_max':max(float(np.max(abs(probs(q,x,y).sum(axis=0)-.5))) for x,y in [(a,b),(a,bp),(ap,b),(ap,bp)]),
           'raw_weight_0':raw_weight(q,0), 'raw_weight_pi4':raw_weight(q,math.pi/4)}
        if do_optimize:r.update(optimized_chsh(q))
        records.append(r)
    threshold=math.log(3)/math.log(1+math.sqrt(2))
    meta={'model':'conditional normalized determinant q-family, NOT UNNS-derived',
          'seed':SEED, 'settings_rad':list(ANGLES),
          'fixed_angle_crossing_exact':threshold,
          'fixed_angle_crossing_root':brentq(lambda q:chsh(q,*ANGLES)-2,1,2),
          'notes':['q=2 imposed Born rule; not independently derived',
                   'optimization is numerical only; cannot certify global maximum',
                   'Tsirelson compliance is not a theorem from these runs'],
          'records':records}
    (output/'phase0_results.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')
    with (output/'q_table.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['q','fixed_chsh','max_chsh_numeric','marginal_error_max','raw_weight_0','raw_weight_pi4'],extrasaction='ignore');w.writeheader();w.writerows(records)
    for r in records:
        print('q={:g}  fixed S={:.9f}  optimized S={:.9f}  no-signal error={:.2g}'.format(r['q'],r['fixed_chsh'],r.get('max_chsh_numeric',float('nan')),r['marginal_error_max']))
    print('Fixed-angle crossing q =',threshold)
    return meta

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=Path('output'))
    parser.add_argument('--skip-optimization',action='store_true')
    args=parser.parse_args()
    run(args.output,not args.skip_optimization)

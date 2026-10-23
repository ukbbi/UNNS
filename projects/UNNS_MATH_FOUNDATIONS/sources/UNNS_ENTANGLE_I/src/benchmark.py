"""CHSH and no-signalling regression baseline for later independently derived models."""
import argparse
import json
from math import pi, sqrt, isfinite
from pathlib import Path
from .models import OUTCOMES,quantum_reference,bell_local_shared_sign,independent_null
ANGLES={'a':0.,'ap':pi/4,'b':pi/8,'bp':-pi/8}
PAIRS=[('a','b'),('a','bp'),('ap','b'),('ap','bp')]
def validate(p,tol=1e-12):
    if set(p)!={(x,y) for x in OUTCOMES for y in OUTCOMES}: raise ValueError('incomplete outcome distribution')
    if not all(isfinite(v) and v>=-tol for v in p.values()): raise ValueError('invalid probability')
    if abs(sum(p.values())-1)>tol: raise ValueError('not normalized')
def corr(p):return sum(x*y*p[x,y] for x in OUTCOMES for y in OUTCOMES)
def marg_a(p):return {str(x):sum(p[x,y] for y in OUTCOMES) for x in OUTCOMES}
def marg_b(p):return {str(y):sum(p[x,y] for x in OUTCOMES) for y in OUTCOMES}
def run_model(model):
    ps={(u,v):model(ANGLES[u],ANGLES[v]) for u,v in PAIRS}
    for p in ps.values():validate(p)
    es={u+'_'+v:corr(ps[u,v]) for u,v in PAIRS}
    s=abs(es['a_b']+es['a_bp']+es['ap_b']-es['ap_bp'])
    max_signal=0.
    for u in ('a','ap'):
        p,q=ps[u,'b'],ps[u,'bp']
        max_signal=max(max_signal,*(abs(marg_a(p)[str(x)]-marg_a(q)[str(x)]) for x in OUTCOMES))
    for v in ('b','bp'):
        p,q=ps['a',v],ps['ap',v]
        max_signal=max(max_signal,*(abs(marg_b(p)[str(y)]-marg_b(q)[str(y)]) for y in OUTCOMES))
    return {'S':s,'correlations':es,'max_remote_setting_marginal_shift':max_signal,
            'probabilities':{u+'_'+v:{str(x)+','+str(y):ps[u,v][x,y] for x in OUTCOMES for y in OUTCOMES} for u,v in PAIRS}}
def build_report():
    return {'status':'REFERENCE_ONLY_NO_UNNS_DERIVATION','protocol_version':'0.1.0',
            'angles':ANGLES,'quantum_reference':run_model(quantum_reference),
            'bell_local_null':run_model(bell_local_shared_sign),
            'independent_null':run_model(independent_null),
            'quantum_target':2*sqrt(2),'bell_local_bound':2.0}
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',default='output/reports/baseline.json')
    args=parser.parse_args();p=Path(args.out);p.parent.mkdir(parents=True,exist_ok=True)
    report=build_report();p.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print('Quantum target S:',round(report['quantum_reference']['S'],9))
    print('Bell-local null S:',round(report['bell_local_null']['S'],9))
    print('Max marginal shift:',report['quantum_reference']['max_remote_setting_marginal_shift'])
    print('WARNING: These are reference models, not UNNS results.')
    print('Report:',p)
if __name__=='__main__':main()

"""KI-1 driver: exact identities for all 268 audited steps -> data/ki1_identities.json  (symbolic, no sampling)"""
import sys,json,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import ki_core as K, ki_ident as I, sympy as sp
def ser(r):
    o={'kind':r['kind']}
    if r['kind']=='const': o['value']=str(r['value'])
    elif r['kind']=='affine': o.update(c0=str(r['c0']),c1=str(r['c1']),certified=bool(r['certified']))
    elif r['kind']=='quad':
        o['rel']={f"{i}{j}":str(v) for (i,j),v in r['rel'].items()}
        for k in ('ok_relation','ok_square','certified'): o[k]=bool(r[k])
        o['sign_A2']=r['sign_A2']; o['sign_W']=r['sign_W']
    return o
def run():
    out={'fibonacci':{},'squares_direct':{},'squares_wrapper':{}}
    for r,c in K.load_fib().items():
        fam=I.FibFam(c['eps']); R=c['R']
        out['fibonacci'][str(r)]=[dict(sign=c['signs'][i],**ser(I.analyse_step(fam,R.expr(c['N'][i]),R.expr(c['S'][i])))) for i in range(len(c['N']))]
    for r,c in K.load_sq_direct().items():
        fam=I.PolyFam(c['t0'])
        out['squares_direct'][str(r)]=[dict(sign=c['signs'][i],**ser(I.analyse_step(fam,c['N'][i],c['S'][i]))) for i in range(len(c['N']))]
    for nm,c in K.load_sq_wrapper().items():
        fam=I.PolyFam(c['t0'])
        out['squares_wrapper'][nm]=[dict(sign=c['signs'][i],**ser(I.analyse_step(fam,c['N'][i],c['S'][i]))) for i in range(len(c['N']))]
    return out
if __name__=="__main__":
    o=run(); json.dump(o,open(sys.argv[1],'w'),indent=1,sort_keys=True); print("ok")

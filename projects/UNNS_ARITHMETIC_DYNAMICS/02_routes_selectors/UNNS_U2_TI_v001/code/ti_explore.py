"""EXPLORATORY analysis (labelled as such; added after the registered results were seen): move-law signatures of the orbits and a first-order polynomial-recurrence recognizer E1."""
import sys,os,json,collections
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import ti_lang as G
from fractions import Fraction
def e1(seq):
    """a_{n+1}=c2 a_n^2+c1 a_n+c0 over Q fitted on the first 3 pairs and verified on all pairs of the first 60 terms; returns coefficients or None"""
    s=seq[:60]
    if len(s)<10: return None
    import sympy as sp
    c=sp.symbols('c0 c1 c2'); eqs=[c[0]+c[1]*s[i]+c[2]*s[i]**2-s[i+1] for i in range(3)]
    sol=sp.solve(eqs,c,dict=True)
    if not sol: return None
    sol=sol[0]
    if len(sol)<3: return None
    f=lambda x:sol[c[0]]+sol[c[1]]*x+sol[c[2]]*x**2
    if all(f(s[i])==s[i+1] for i in range(len(s)-1)): return [str(sol[c[0]]),str(sol[c[1]]),str(sol[c[2]])]
    return None
def law(rule,x0,T,ESC):
    r=G.run(rule,x0,T,ESC); seq=r['seq']; mv=r['moves']
    tail=[]
    for i in range(max(0,len(mv)-6),len(mv)):
        sg,N=mv[i]; x=seq[i]; tail.append(sg+("x" if N==x else str(N)))
    return r,tuple(tail)
if __name__=="__main__":
    cfg=json.load(open(HERE+"/../data/ti_config.json")); R=json.load(open(HERE+"/../data/ti_results.json"))
    out=[]
    for rec in R:
        a=rec['analysis']
        if a['status'] not in('escape','horizon'): continue
        r,tail=law(rec['rule'],rec['start'],cfg['horizon_T'],cfg['escape_ESC'])
        out.append(dict(cls=rec['cls'],rule_index=rec['rule_index'],start=rec['start'],tail=list(tail),e1=e1(r['seq']),registered_success=bool(a['linrec_V'] or a['linrec_R'] or any(d.get('consecutive') for k in('fam_V','fam_R') for d in a[k].values()))))
    json.dump(out,open(sys.argv[1],'w'))
    C=collections.Counter((o['registered_success'],o['e1'] is not None) for o in out); print(C)
    L=collections.Counter((o['registered_success'],o['e1'] is not None,tuple(o['tail'][-2:])) for o in out); 
    for k,v in L.most_common(14): print(k,v)
    E=collections.Counter(tuple(o['e1']) for o in out if o['e1']); print(E)

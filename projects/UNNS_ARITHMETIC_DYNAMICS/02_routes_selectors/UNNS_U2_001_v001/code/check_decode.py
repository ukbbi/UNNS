import sympy as sp, json, sys
from u2_selector import POLY, T0, _t
u=sp.symbols("u",nonnegative=True)
out={}
ok=True
for name,(ident,_,xs,_) in POLY.items():
    t0=T0[name]; rows=[]
    for i,p in enumerate(xs):
        q=sp.together(sp.expand(p.subs(_t,u+t0)))
        num,den=sp.fraction(q)
        pn=sp.Poly(sp.expand(num),u); pd=sp.Poly(sp.expand(den),u)
        d=sp.diff(q,u); dn,dd=sp.fraction(sp.together(d))
        pdn=sp.Poly(sp.expand(dn),u)
        # strictly increasing for u>=0: derivative numerator has nonneg coeffs, not identically 0, denominator positive
        good=all(c>=0 for c in pdn.all_coeffs()) and any(c>0 for c in pdn.all_coeffs()) and all(c>=0 for c in sp.Poly(sp.expand(dd),u).all_coeffs()) and any(c>0 for c in sp.Poly(sp.expand(dd),u).all_coeffs())
        poly = pd.degree()==0
        rows.append(dict(step=i,expr=str(sp.factor(p)),increasing=bool(good),polynomial=bool(poly)))
        ok&=bool(good)
    out[name]=rows
print("ALL STATES STRICTLY INCREASING:",ok)
json.dump(out,open(sys.argv[1],"w"),indent=1)
for n,r in out.items(): print(n,[x["expr"] for x in r])

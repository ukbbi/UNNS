"""Continuous monotonicity certificate for G_i(t)=p0(t)+p1(t)*alpha_eps(t), alpha_eps=(sqrt(5t^2+4eps)-t)/2, t>=40.
Exact: G' = p0' + p1' alpha + p1 alpha' with alpha>0, alpha'>0 and p1>=0, p1'>=0, p0'>0 (shifted-coefficient tests)."""
import sympy as sp, json
from fibcert2 import b as T, shift_nonneg
def parts(e):
    p0=sp.together(sp.sympify(e[0])); p1=sp.together(sp.sympify(e[1]))
    return p0,p1
def nonneg_shift(p,b0=40):
    num=sp.Poly(sp.numer(sp.together(p)),T); den=sp.denom(sp.together(p))
    return bool(den>0) and shift_nonneg(num,b0)
def certify_state(e,eps):
    p0,p1=parts(e)
    d0=sp.Poly(sp.diff(p0,T),T)
    checks=dict(
      p1_nonneg=nonneg_shift(p1), p1_deriv_nonneg=nonneg_shift(sp.diff(p1,T)),
      p0_deriv_nonneg=nonneg_shift(sp.diff(p0,T)), p0_nonconstant=not d0.is_zero,
      p0_ge_t=nonneg_shift(p0-T))
    # alpha>0 and alpha'>0 for t>=40 (independent of the state): sqrt(5t^2+4eps)>t iff 4t^2+4eps>0 ; 5t>sqrt(5t^2+4eps) iff 20t^2>4eps
    checks['alpha_pos']= (4*40**2+4*eps)>0
    checks['alpha_deriv_pos']= (20*40**2-4*eps)>0
    ok=all(checks.values()); return ok,checks
def certify_all(certs):
    out={};allok=True;n=0
    for r,o in certs.items():
        flags=[]
        for e in o['states_ring']:
            ok,ch=certify_state(e,o['eps']); flags.append(ok); n+=1
        out[r]=all(flags); allok&=all(flags)
    return allok,n,out

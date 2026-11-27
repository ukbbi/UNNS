"""Hurwitz zeta zeta(w,x) for real w != 1 and arrays x>0, by Euler-Maclaurin (numpy only)."""
import numpy as np
def hz(w,x):
    x=np.asarray(x,float); K=10; out=np.zeros_like(x)
    for k in range(K): out+=(x+k)**(-w)
    y=x+K
    out+=y**(1-w)/(w-1)+0.5*y**(-w)
    term=w*y**(-w-1)
    for j,b in enumerate((1/12,-1/720,1/30240,-1/1209600)):
        out+=b*term
        term=term*(w+2*j+1)*(w+2*j+2)/(y*y)
    return out

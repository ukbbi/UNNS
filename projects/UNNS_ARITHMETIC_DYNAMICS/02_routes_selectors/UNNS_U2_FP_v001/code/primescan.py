import sys, time, sympy
from u1_bnd_lib import *
lim=int(sys.argv[1]); out=sys.argv[2]
P=list(sympy.primerange(2,lim)); f=open(out,"w"); f.write("p,q,d,sec\n")
for p,q in zip(P,P[1:]):
    t=time.time(); d=distance(p,q,neighbours_fast,maxd=9)
    f.write(f"{p},{q},{d},{time.time()-t:.2f}\n"); f.flush()

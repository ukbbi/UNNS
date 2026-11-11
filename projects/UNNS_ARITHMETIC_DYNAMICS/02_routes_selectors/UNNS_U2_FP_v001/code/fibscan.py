import sys, time
from u1_bnd_lib import *
a,b=int(sys.argv[1]),int(sys.argv[2]); out=sys.argv[3]
F=[0,1]
while len(F)<=b+2: F.append(F[-1]+F[-2])
f=open(out,"w"); f.write("k,F_k,F_k+1,d,sec\n")
for k in range(a,b+1):
    t=time.time(); d=distance(F[k],F[k+1],neighbours_fast,maxd=9)
    f.write(f"{k},{F[k]},{F[k+1]},{d},{time.time()-t:.1f}\n"); f.flush()

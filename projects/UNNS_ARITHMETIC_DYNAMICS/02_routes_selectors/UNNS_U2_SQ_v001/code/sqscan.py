import sys, time
from u1_bnd_lib import *
a,b=int(sys.argv[1]),int(sys.argv[2]); out=sys.argv[3]
f=open(out,"w"); f.write("n,d_sq,sec\n")
for n in range(a,b+1):
    t=time.time(); d=distance(n*n,(n+1)**2,neighbours_fast,maxd=8)
    f.write(f"{n},{d},{time.time()-t:.3f}\n"); f.flush()

import sys
from u1_bnd_lib import *
k=int(sys.argv[1]); F=[0,1]
while len(F)<=k+1: F.append(F[-1]+F[-2])
print(distance(F[k],F[k+1],neighbours_fast,maxd=9))

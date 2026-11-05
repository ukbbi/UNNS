import sys; sys.path.insert(0,'.')
from eng3 import *
x=Fr(3025,3); o=orbit(x,8); print([str(t) for t in o]); print(o[-1]==Fr(12100,3))
for t in o: print(t, Dset(t), bettiD(Dset(t)) if Dset(t) else None)

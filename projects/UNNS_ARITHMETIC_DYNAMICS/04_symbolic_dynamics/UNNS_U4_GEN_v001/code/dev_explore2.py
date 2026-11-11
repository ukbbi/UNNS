"""DEVELOPMENT EXPLORATION 2 (pre-registration, logged): maxpp rule and complexity."""
import sys,math;sys.path.insert(0,'code')
from dev_explore import init,step,fac
def maxpp(e): return max(e,key=lambda p:e[p]*math.log(p))   # float for dev only
def run(x,H):
    e=init(x);w=[]
    for _ in range(H):
        p=maxpp(e);w.append(p);e=step(e,p)
    return w
def cx(w,n): return len({tuple(w[i:i+n]) for i in range(len(w)-n)})
for x in (2,3,6,10,30,97,360,2*5**20):
    w=run(x,20000);t=w[2000:]
    print(x,'symbols',sorted(set(t)),'complexity',[cx(t,n) for n in (1,2,3,5,10,20)],'first',w[:14])

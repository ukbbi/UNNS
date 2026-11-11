"""GL-1: the graph-local selector language of U2-TI (target-blind by construction).
A selector is DATA: a rule tuple from the finite grammar below.  One interpreter runs every rule.
Information channels (the only reads the interpreter performs):
   X   the current vertex x
   H   the previous vertices (window of length w in {0,1,2}, declared by the rule)   [class F]
   V   the set of all previously visited vertices                                    [class M only; unbounded memory, NOT finite control]
   NB  the graph neighbours of x, computed from x by the definition of G: (y,sign,N) with y=x(N+1)^2/N (N|x) or y=x(q-1)/q^2 (q^2|x, q>=2, N=q-1)
There is no step counter, no target, no external table.  The stopping horizon T and the escape bound ESC are applied OUTSIDE the selector."""
import sys,os,json
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE+"/../frozen_KI/baseline_R3_frozen/code")
import u1_bnd_lib as L
GRAMMAR=dict(
  dir=["any","up","down"],
  hist=["none","h1","h12"],                    # class F ; class M uses hist="visited" only
  band=["none","y<=2x","y>=x/2","x/2<=y<=2x"],
  key=["y","N","y%4","y%6","v2(y)"],
  order=["min","max"])
def rules_F(): return [dict(cls="F",dir=d,hist=h,band=b,key=k,order=o) for d in GRAMMAR["dir"] for h in GRAMMAR["hist"] for b in GRAMMAR["band"] for k in GRAMMAR["key"] for o in GRAMMAR["order"]]
def rules_M(): return [dict(cls="M",dir=d,hist="visited",band=b,key=k,order=o) for d in GRAMMAR["dir"] for b in GRAMMAR["band"] for k in GRAMMAR["key"] for o in GRAMMAR["order"]]
class Channels:
    """audit log of information reads"""
    def __init__(s): s.reads=dict(X=0,H=0,V=0,NB=0)
_NB={}
def neighbours(x):
    if x in _NB: return _NB[x]
    out=[]
    for N in L.divisors(x): out.append((x//N*(N+1)**2,'+',N))
    for q in L.sq_roots(x): out.append((x//(q*q)*(q-1),'-',q-1))
    out=sorted(set(out)); _NB[x]=out; return out
def v2(y):
    return (y&-y).bit_length()-1
def keyval(key,y,N):
    if key=="y": return y
    if key=="N": return N
    if key=="y%4": return y%4
    if key=="y%6": return y%6
    if key=="v2(y)": return v2(y)
    raise ValueError(key)
def step(rule,x,hist,visited,ch):
    """one selector step.  hist = tuple of previous vertices (most recent first). returns (y,sign,N,ncand) or None if no admissible neighbour."""
    ch.reads['X']+=1; ch.reads['NB']+=1
    C=neighbours(x); n0=len(C)
    if rule["dir"]=="up": C=[c for c in C if c[1]=='+']
    elif rule["dir"]=="down": C=[c for c in C if c[1]=='-']
    b=rule["band"]
    if b=="y<=2x": C=[c for c in C if c[0]<=2*x]
    elif b=="y>=x/2": C=[c for c in C if 2*c[0]>=x]
    elif b=="x/2<=y<=2x": C=[c for c in C if c[0]<=2*x and 2*c[0]>=x]
    h=rule["hist"]
    if h=="h1": ch.reads['H']+=1; C=[c for c in C if c[0] not in hist[:1]]
    elif h=="h12": ch.reads['H']+=1; C=[c for c in C if c[0] not in hist[:2]]
    elif h=="visited": ch.reads['V']+=1; C=[c for c in C if c[0] not in visited]
    if not C: return None
    sgn=1 if rule["order"]=="min" else -1
    best=min(C,key=lambda c:(sgn*keyval(rule["key"],c[0],c[2]),c[0]))
    return best[0],best[1],best[2],n0
def run(rule,x0,T,ESC):
    """iterate the rule from x0.  returns dict(seq, moves, status).  status: cyclic | stuck | escape | horizon"""
    ch=Channels(); seq=[x0]; mv=[]; hist=(); visited={x0}; seen={}; x=x0; cand=0
    for t in range(T):
        key=(x,hist)
        if rule["cls"]=="F":
            if key in seen: return dict(seq=seq,moves=mv,status="cyclic",pre=seen[key],period=t-seen[key],channels=ch.reads,cand=cand)
            seen[key]=t
        r=step(rule,x,hist,visited,ch)
        if r is None: return dict(seq=seq,moves=mv,status="stuck",channels=ch.reads,cand=cand)
        y,sg,N,n0=r; cand+=n0
        hw={"none":0,"h1":1,"h12":2,"visited":0}[rule["hist"]]
        hist=((x,)+hist)[:max(hw,0)] if hw else ()
        x=y; seq.append(x); mv.append((sg,N)); visited.add(x)
        if x>ESC: return dict(seq=seq,moves=mv,status="escape",channels=ch.reads,cand=cand)
    return dict(seq=seq,moves=mv,status="horizon",channels=ch.reads,cand=cand)

"""GL-2: ranked-neighbour selector language (registered; do not edit after registration).
rule = dict(side in F|I|A, end in top|bottom, k in 1..3, key None|degmin|degmax, tie hi|lo, nb bool)
Rank selectors: order the eligible set (side F: forward ascending-by-d = ascending-by-y; side I: inverse; side A: all, by value);
 'top k' = k-th largest, 'bottom k' = k-th smallest.  nb=True removes the previous vertex from the eligible set BEFORE ranking.
Degree selectors: among eligible set choose min or max degree, tie by largest(hi)/smallest(lo) value.
UNDEFINED RANK (eligible set smaller than k, or empty) => status 'stuck'.  No substitution of another rule, ever."""
import rn_core as C
def grammar():
    R=[]
    for nb in (False,True):
        for side in "FIA":
            for end in("top","bottom"):
                for k in (1,2,3): R.append(dict(side=side,end=end,k=k,key=None,tie=None,nb=nb))
            for key in("degmin","degmax"):
                for tie in("hi","lo"): R.append(dict(side=side,end="-",k=0,key=key,tie=tie,nb=nb))
    return R
def eligible(x,prev,rule):
    n=C.neighbours(x); side=rule["side"]
    Fl=[("F",t[0],t[1],t[2]) for t in n["F"]]; Il=[("I",t[0],t[1],t[2]) for t in n["I"]]
    L=Fl if side=="F" else Il if side=="I" else sorted(Fl+Il,key=lambda t:t[2])
    L=sorted(L,key=lambda t:t[2])
    if rule["nb"] and prev is not None: L=[t for t in L if t[2]!=prev]
    return L,n
def step(rule,x,prev):
    """returns (y,label,cert) or None for stuck"""
    L,n=eligible(x,prev,rule)
    if not L: return None
    if rule["key"] is None:
        k=rule["k"]
        if len(L)<k: return None
        t=L[-k] if rule["end"]=="top" else L[k-1]
    else:
        ds=[(C.degree_from_fact(t[3]),t) for t in L]
        best=min(d for d,_ in ds) if rule["key"]=="degmin" else max(d for d,_ in ds)
        c=[t for d,t in ds if d==best]
        t=max(c,key=lambda t:t[2]) if rule["tie"]=="hi" else min(c,key=lambda t:t[2])
    return t[2],(t[0],t[1]),n["cert"]
def label_class(x,lab):
    """move-label class relative to x (registered vocabulary)"""
    kind,par=lab; f=C.factor(x)[0]
    if kind=="F":
        p=min(f) if x>1 else None
        if par==x: return "F:x"
        if par==1: return "F:1"
        if p and par==x//p: return "F:x/p"
        if p and par==p: return "F:p"
        return "F:o"
    a=1
    for p,e in f.items(): a*=p**(e//2)
    pm=min([p for p,e in f.items() if e>=2],default=None)
    if par==a: return "I:a"+("=p" if a==pm else "")
    if par==pm: return "I:p"
    return "I:o"
def run(rule,x0,T,ESC):
    x=x0;prev=None;seq=[x0];labs=[];seen={(x0,prev if rule["nb"] else None):0};cert=True;status="horizon";snap=dict(C.CNT)
    while len(seq)<=T:
        r=step(rule,x,prev)
        if r is None: status="stuck";break
        y,lab,c=r;cert=cert and c
        labs.append(label_class(x,lab))
        prev=x;x=y;seq.append(x)
        if x>ESC: status="escape";break
        key=(x,prev if rule["nb"] else None)
        if key in seen: status="cyclic";pre=seen[key];break
        seen[key]=len(seq)-1
    out=dict(seq=seq,labels=labs,status=status,certified=cert,cost={k:C.CNT[k]-snap.get(k,0) for k in C.CNT})
    if status=="cyclic": out["pre"]=pre;out["period"]=len(seq)-1-pre
    return out

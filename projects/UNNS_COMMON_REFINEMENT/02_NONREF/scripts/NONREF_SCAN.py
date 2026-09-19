#!/usr/bin/env python3
import math, itertools, json

def monoid_elements(gens, limit):
    H={0}
    changed=True
    while changed:
        changed=False
        for x in list(H):
            for g in gens:
                y=x+g
                if y<=limit and y not in H:
                    H.add(y); changed=True
    return sorted(H)

def ambient_witnesses(a,b,c,d):
    if a+b!=c+d: return []
    lo=max(0,c-b); hi=min(a,c)
    out=[]
    for e in range(lo,hi+1):
        f=a-e; g=c-e; h=b-g
        if min(e,f,g,h)>=0 and e+f==a and g+h==b and e+g==c and f+h==d:
            out.append((e,f,g,h))
    return out

def exact_verdict(gens,a,b,c,d):
    H=set(monoid_elements(gens,max(a,b,c,d,a+b)))
    amb=ambient_witnesses(a,b,c,d)
    valid=[w for w in amb if all(x in H for x in w)]
    return {
        "generators":gens,
        "endpoint_equal":a+b==c+d,
        "ambient_witnesses":amb,
        "valid_witnesses":valid,
        "D_R":0 if valid else 1
    }

if __name__=="__main__":
    print(json.dumps(exact_verdict([2,3],2,4,3,3),indent=2))

#!/usr/bin/env python3
import math, csv, json
from pathlib import Path

def prime_factors(n):
    n=abs(int(n)); f={}; p=2
    while p*p<=n:
        while n%p==0:
            f[p]=f.get(p,0)+1; n//=p
        p += 1 if p==2 else 2
    if n>1: f[n]=f.get(n,0)+1
    return f

def ladder(n, prime_basis):
    f=prime_factors(n); s=0.0; out=[]
    for p in prime_basis:
        s += f.get(p,0)*math.log(p)
        out.append(s)
    return out

def main():
    here=Path(__file__).resolve().parents[2]
    basis=json.loads((here/"01_INTEGER/output/prime_basis.json").read_text(encoding="utf-8"))["prime_basis"]
    print("Canonical Phase-1 encoding:")
    print("L_x(k)=sum_{i<=k} v_p_i(x) log(p_i)")
    print("Prime basis:", basis)

if __name__=="__main__":
    main()

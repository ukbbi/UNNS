#!/usr/bin/env python3
import math, random, csv
from pathlib import Path

def refine_positive(a,b,c,d):
    if a*b != c*d:
        raise ValueError("ab != cd")
    e = math.gcd(a,c)
    f = a//e
    g = c//e
    if b % g or d % f:
        raise ArithmeticError("divisibility failure")
    h1, h2 = b//g, d//f
    if h1 != h2:
        raise ArithmeticError("inconsistent h")
    return e,f,g,h1

def verify(a,b,c,d,e,f,g,h):
    return a*b==c*d and a==e*f and b==g*h and c==e*g and d==f*h

def main():
    random.seed(260918)
    out = Path(__file__).resolve().parents[1]/"output"/"integer_cases_regen.csv"
    rows=[]
    for i in range(500):
        e0,f0,g0,h0=[random.randint(1,80) for _ in range(4)]
        a,b,c,d=e0*f0,g0*h0,e0*g0,f0*h0
        e,f,g,h=refine_positive(a,b,c,d)
        rows.append([i,a,b,c,d,a*b,e,f,g,h,int(verify(a,b,c,d,e,f,g,h))])
    with out.open("w",newline="",encoding="utf-8") as fp:
        w=csv.writer(fp); w.writerow(["id","a","b","c","d","product","e","f","g","h","valid"]); w.writerows(rows)
    print(out)

if __name__=="__main__":
    main()

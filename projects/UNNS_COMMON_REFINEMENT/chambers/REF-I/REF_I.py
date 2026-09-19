#!/usr/bin/env python3
import math, argparse, json

def refine(a,b,c,d):
    if min(a,b,c,d) <= 0:
        raise ValueError("Phase-1 REF-I accepts positive integers only.")
    if a*b != c*d:
        return {"class":"NOT_ENDPOINT_EQUIVALENT","refinable":False,"D_R":None}
    e=math.gcd(a,c); f=a//e; g=c//e
    if b%g or d%f:
        return {"class":"NR","refinable":False,"D_R":1}
    h1,h2=b//g,d//f
    if h1!=h2:
        return {"class":"NR","refinable":False,"D_R":1}
    ok=(a==e*f and b==g*h1 and c==e*g and d==f*h1)
    return {
        "class":"R" if ok else "NR",
        "refinable":ok,
        "D_R":0 if ok else 1,
        "endpoint":{"a":a,"b":b,"c":c,"d":d,"product":a*b},
        "witness":{"e":e,"f":f,"g":g,"h":h1},
        "checks":{"a=ef":a==e*f,"b=gh":b==g*h1,"c=eg":c==e*g,"d=fh":d==f*h1}
    }

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("a",type=int); ap.add_argument("b",type=int); ap.add_argument("c",type=int); ap.add_argument("d",type=int)
    x=ap.parse_args()
    print(json.dumps(refine(x.a,x.b,x.c,x.d),indent=2))

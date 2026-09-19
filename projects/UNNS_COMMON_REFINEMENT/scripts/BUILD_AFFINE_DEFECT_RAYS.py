#!/usr/bin/env python3
"""
BUILD_AFFINE_DEFECT_RAYS.py

Concrete retained-control instantiations of the general theorem proved in
02_NONREF/systems/AFFINE_DEFECT_RAY_THEOREM.md.

The theorem itself is algebraic and polyhedral; these checks are regression
instances, not the proof.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "04_PROOF_MAP" / "output"
REC = ROOT / "outputs" / "records"


def add(a,b): return tuple(x+y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def smul(n,a): return tuple(n*x for x in a)


def in_parity(v):
    x,y=v
    return x>=0 and y>=0 and (x+y)%2==0


def in_cone2(v):
    x,y=v
    return x>=0 and 0<=y<=2*x


def in_nonnormal(v):
    x,y=v
    return x>=0 and y>=0 and (x%2==0 or y>=1)


def in_square(v):
    x,y,n=v
    return n>=0 and 0<=x<=n and 0<=y<=n


def divisors(x,inH):
    if len(x)==2:
        for i in range(x[0]+1):
            for j in range(x[1]+1):
                d=(i,j)
                if inH(d) and inH(sub(x,d)):
                    yield d
    else:
        for i in range(x[0]+1):
            for j in range(x[1]+1):
                for k in range(x[2]+1):
                    d=(i,j,k)
                    if inH(d) and inH(sub(x,d)):
                        yield d


def nonrefines_at(x,u,b,v,inH):
    # x+u = b+v
    if not all(inH(z) for z in (x,u,b,v)):
        return False
    if add(x,u)!=add(b,v):
        return False
    for d in divisors(x,inH):
        e=sub(x,d)
        if inH(sub(b,d)) and inH(sub(v,e)):
            return False
    return True


CASES = [
    {
        "system":"NORMAL_PARITY",
        "a":(2,0), "u":(0,2), "b":(1,1), "v":(1,1), "rho":(2,0),
        "facet":"y=0", "functional":"lambda(x,y)=y", "inH":in_parity,
        "ray":"(2n+2,0)",
    },
    {
        "system":"NORMAL_CONE2",
        "a":(1,0), "u":(1,2), "b":(1,1), "v":(1,1), "rho":(1,0),
        "facet":"y=0", "functional":"lambda(x,y)=y", "inH":in_cone2,
        "ray":"(n+1,0)",
    },
    {
        "system":"NONNORMAL_2D",
        "a":(2,0), "u":(0,2), "b":(1,1), "v":(1,1), "rho":(2,0),
        "facet":"y=0", "functional":"lambda(x,y)=y", "inH":in_nonnormal,
        "ray":"(2n+2,0)",
    },
    {
        "system":"NORMAL_SQUARE3",
        "a":(0,0,1), "u":(1,1,1), "b":(1,0,1), "v":(0,1,1), "rho":(0,0,1),
        "facet":"x=0", "functional":"lambda(x,y,n)=x", "inH":in_square,
        "ray":"(0,0,n+1)",
    },
]


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    REC.mkdir(parents=True,exist_ok=True)
    rows=[]
    checks=0
    for c in CASES:
        a,u,b,v,rho,inH=c["a"],c["u"],c["b"],c["v"],c["rho"],c["inH"]
        assert add(a,u)==add(b,v)
        assert not inH(sub(v,a))  # a does not divide v
        assert not inH(sub(u,b))  # b does not divide u
        for n in range(25):
            x=add(a,smul(n,rho))
            vr=add(v,smul(n,rho))
            if not nonrefines_at(x,u,b,vr,inH):
                raise AssertionError((c["system"],n,x,u,b,vr))
            checks += 1
        rows.append({
            "system":c["system"],
            "atom_a":str(a),
            "u":str(u),
            "atom_b":str(b),
            "v":str(v),
            "base_equality":f"{a}+{u}={b}+{v}",
            "facet":c["facet"],
            "facet_functional":c["functional"],
            "rho":str(rho),
            "persistent_nonprimal_ray":c["ray"],
            "checked_n":"0..24",
        })

    out=OUT/"AFFINE_DEFECT_RAY_INSTANCES.csv"
    with out.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)

    result={
        "result":"AFFINE_DEFECT_RAY_THEOREM_PROVED",
        "statement":"For every positive affine monoid H with rank(H)>=2 and ARD(H)>0, H\\P(H) contains an infinite affine ray a+n*rho of non-primal elements.",
        "retained_failure_controls_instantiated":len(rows),
        "regression_instances_checked":checks,
        "proof_dependency":[
            "ARD>0 forces a non-prime atom",
            "minimal atomic witness gives an irredundant atom-pair equality",
            "one atom difference lies outside the pointed cone",
            "a violated facet supplies a nonzero tangent direction when rank>=2",
            "translation along that facet preserves non-refinability",
        ],
        "rank_one_contrast":"rank one has no nonzero facet direction; its established non-primal locus is finite after numerical normalization",
    }
    (REC/"AFFINE_DEFECT_RAY_RESULT.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()

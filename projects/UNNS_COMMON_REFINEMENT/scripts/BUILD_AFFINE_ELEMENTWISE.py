#!/usr/bin/env python3
"""
BUILD_AFFINE_ELEMENTWISE.py

Exact elementwise primal-locus records for the retained positive-affine controls.

This script does NOT infer primality from a bounded search.  The exact locus
formulas are the proved classifications documented in
04_PROOF_MAP/output/AFFINE_ELEMENTWISE_PROFILE.md.

The script:
  * writes the exact system summary;
  * writes parametric unbounded non-primal certificate families;
  * performs finite regression checks of the formulas and certificate
    constructors;
  * writes a machine-readable result record.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "04_PROOF_MAP" / "output"
REC = ROOT / "outputs" / "records"


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def in_parity(v):
    x, y = v
    return x >= 0 and y >= 0 and (x + y) % 2 == 0


def primal_parity(v):
    x, y = v
    return v == (0, 0) or (x >= 2 and y >= 2 and x % 2 == 0 and y % 2 == 0)


def in_cone2(v):
    x, y = v
    return x >= 0 and 0 <= y <= 2 * x


def primal_cone2(v):
    x, y = v
    return v == (0, 0) or (y >= 2 and y % 2 == 0 and 2 * x - y >= 2)


def in_nonnormal(v):
    x, y = v
    return x >= 0 and y >= 0 and (x % 2 == 0 or y >= 1)


def primal_nonnormal(v):
    x, y = v
    return v == (0, 0) or (x >= 2 and x % 2 == 0 and y >= 2)


def in_square(v):
    x, y, n = v
    return n >= 0 and 0 <= x <= n and 0 <= y <= n


def primal_square(v):
    x, y, n = v
    return 2 * x == n and 2 * y == n


def divisors_of_x(x, inH):
    if len(x) == 2:
        for a in range(x[0] + 1):
            for b in range(x[1] + 1):
                u = (a, b)
                if inH(u) and inH(sub(x, u)):
                    yield u
    else:
        for a in range(x[0] + 1):
            for b in range(x[1] + 1):
                for c in range(x[2] + 1):
                    u = (a, b, c)
                    if inH(u) and inH(sub(x, u)):
                        yield u


def certificate_valid(x, t, y, z, inH):
    if not all(inH(v) for v in (x, t, y, z)):
        return False, "membership"
    if add(x, t) != add(y, z):
        return False, "endpoint"
    for u in divisors_of_x(x, inH):
        v = sub(x, u)
        if inH(sub(y, u)) and inH(sub(z, v)):
            return False, f"refines via u={u}"
    return True, "non-refinable"


def parity_certificates(limit=8):
    rows = []
    # odd-odd interior family
    for m in range(limit):
        for n in range(limit):
            x = (2*m+1, 2*n+1)
            t = (1, 1)
            y = (2*m+2, 0)
            z = (0, 2*n+2)
            rows.append((x,t,y,z,in_parity))
    # two boundary-ray families
    for k in range(1, limit+1):
        rows.append(((2*k,0),(0,2),(1,1),(2*k-1,1),in_parity))
        rows.append(((0,2*k),(2,0),(1,1),(1,2*k-1),in_parity))
    return rows


def cone2_certificates(limit=8):
    rows=[]
    # odd-y interior family: X=(m+n+1,2n+1)
    for m in range(limit):
        for n in range(limit):
            x=(m+n+1,2*n+1); t=(1,1); y=(m+1,0); z=(n+1,2*n+2)
            rows.append((x,t,y,z,in_cone2))
    for k in range(1,limit+1):
        rows.append(((k,0),(1,2),(1,1),(k,1),in_cone2))
        rows.append(((k,2*k),(1,0),(1,1),(k,2*k-1),in_cone2))
    return rows


def nonnormal_certificates(limit=8):
    rows=[]
    for m in range(limit):
        for n in range(1,limit+1):
            x=(2*m+1,n); t=(1,1); y=(2*m+2,0); z=(0,n+1)
            rows.append((x,t,y,z,in_nonnormal))
    for n in range(1,limit+1):
        rows.append(((0,n),(2,1),(1,1),(1,n),in_nonnormal))
    for m in range(1,limit+1):
        rows.append(((2*m,0),(0,2),(1,1),(2*m-1,1),in_nonnormal))
        rows.append(((2*m,1),(0,1),(1,1),(2*m-1,1),in_nonnormal))
    return rows


def square_certificate(x):
    a,b,n=x
    assert in_square(x) and not primal_square(x)
    M=max(a,b,n-a,n-b)
    t=(M-a,M-b,2*M-n)
    if n != a+b:
        y=(M,0,M); z=(0,M,M); family="opposite_BC_faces"
    else:
        y=(0,0,M); z=(M,M,M); family="opposite_AD_faces"
    return t,y,z,family


def sample_counts():
    result={}
    N=24
    pts=[(x,y) for x in range(N+1) for y in range(N+1) if in_parity((x,y))]
    result["NORMAL_PARITY"]={"window":"0<=x,y<=24","elements":len(pts),"primal":sum(primal_parity(p) for p in pts)}

    pts=[(x,y) for x in range(N+1) for y in range(2*x+1)]
    result["NORMAL_CONE2"]={"window":"0<=x<=24, 0<=y<=2x","elements":len(pts),"primal":sum(primal_cone2(p) for p in pts)}

    pts=[(x,y) for x in range(N+1) for y in range(N+1) if in_nonnormal((x,y))]
    result["NONNORMAL_2D"]={"window":"0<=x,y<=24","elements":len(pts),"primal":sum(primal_nonnormal(p) for p in pts)}

    G=18
    pts=[(x,y,n) for n in range(G+1) for x in range(n+1) for y in range(n+1)]
    result["NORMAL_SQUARE3"]={"window":"grade 0<=n<=18","elements":len(pts),"primal":sum(primal_square(p) for p in pts)}
    return result


def run_regressions():
    checks=0
    for fam in (parity_certificates(), cone2_certificates(), nonnormal_certificates()):
        for x,t,y,z,inH in fam:
            ok,msg=certificate_valid(x,t,y,z,inH)
            if not ok:
                raise AssertionError((x,t,y,z,msg))
            checks += 1

    for n in range(1,11):
        for x in range(n+1):
            for y in range(n+1):
                p=(x,y,n)
                if primal_square(p):
                    continue
                t,a,b,family=square_certificate(p)
                ok,msg=certificate_valid(p,t,a,b,in_square)
                if not ok:
                    raise AssertionError((p,t,a,b,family,msg))
                checks += 1
    return checks


def write_summary():
    rows=[
        {
            "system":"FREE_N2","rank_gp":2,"ARD":0,"global_refinement":"YES",
            "exact_primal_locus":"all elements","nonprimal_unbounded":"NO","rank_gp_primal_locus":2,
            "relative_primal_density":"1","defect_geometry":"none"
        },
        {
            "system":"FREE_SKEW","rank_gp":2,"ARD":0,"global_refinement":"YES",
            "exact_primal_locus":"all elements","nonprimal_unbounded":"NO","rank_gp_primal_locus":2,
            "relative_primal_density":"1","defect_geometry":"none"
        },
        {
            "system":"NORMAL_PARITY","rank_gp":2,"ARD":1,"global_refinement":"NO",
            "exact_primal_locus":"{0} union {(2m,2n): m,n>=1}","nonprimal_unbounded":"YES","rank_gp_primal_locus":2,
            "relative_primal_density":"1/2 (box exhaustion)","defect_geometry":"unbounded odd-odd congruence class plus both boundary rays"
        },
        {
            "system":"NORMAL_CONE2","rank_gp":2,"ARD":1,"global_refinement":"NO",
            "exact_primal_locus":"{0} union {(x,y): y even, y>=2, 2x-y>=2}","nonprimal_unbounded":"YES","rank_gp_primal_locus":2,
            "relative_primal_density":"1/2 (x-grade exhaustion)","defect_geometry":"unbounded odd-y interior class plus both cone facets"
        },
        {
            "system":"NONNORMAL_2D","rank_gp":2,"ARD":1,"global_refinement":"NO",
            "exact_primal_locus":"{0} union {(2m,n): m>=1,n>=2}","nonprimal_unbounded":"YES","rank_gp_primal_locus":2,
            "relative_primal_density":"1/2 (box exhaustion)","defect_geometry":"unbounded odd-x class plus vertical axis and low horizontal strips"
        },
        {
            "system":"NORMAL_SQUARE3","rank_gp":3,"ARD":1,"global_refinement":"NO",
            "exact_primal_locus":"{k(1,1,2): k>=0}","nonprimal_unbounded":"YES","rank_gp_primal_locus":1,
            "relative_primal_density":"0 (grade exhaustion)","defect_geometry":"all elements except one central primal ray"
        },
        {
            "system":"FREE_N3","rank_gp":3,"ARD":0,"global_refinement":"YES",
            "exact_primal_locus":"all elements","nonprimal_unbounded":"NO","rank_gp_primal_locus":3,
            "relative_primal_density":"1","defect_geometry":"none"
        },
    ]
    path=OUT/"AFFINE_ELEMENTWISE_SUMMARY.csv"
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    return rows


def write_families():
    rows=[
      ["NORMAL_PARITY","odd-odd interior","m,n>=0","X=(2m+1,2n+1)","T=(1,1)","Y=(2m+2,0)","Z=(0,2n+2)","forces forbidden odd axis pieces"],
      ["NORMAL_PARITY","horizontal boundary","k>=1","X=(2k,0)","T=(0,2)","Y=(1,1)","Z=(2k-1,1)","boundary ray remains non-primal for all k"],
      ["NORMAL_PARITY","vertical boundary","k>=1","X=(0,2k)","T=(2,0)","Y=(1,1)","Z=(1,2k-1)","boundary ray remains non-primal for all k"],
      ["NORMAL_CONE2","odd-y interior","m,n>=0","X=(m+n+1,2n+1)","T=(1,1)","Y=(m+1,0)","Z=(n+1,2n+2)","transport of parity obstruction under lattice isomorphism"],
      ["NORMAL_CONE2","lower facet","k>=1","X=(k,0)","T=(1,2)","Y=(1,1)","Z=(k,1)","facet obstruction"],
      ["NORMAL_CONE2","upper facet","k>=1","X=(k,2k)","T=(1,0)","Y=(1,1)","Z=(k,2k-1)","facet obstruction"],
      ["NONNORMAL_2D","odd-x bulk","m>=0,n>=1","X=(2m+1,n)","T=(1,1)","Y=(2m+2,0)","Z=(0,n+1)","would require missing odd horizontal piece"],
      ["NONNORMAL_2D","vertical axis","n>=1","X=(0,n)","T=(2,1)","Y=(1,1)","Z=(1,n)","hole (1,0) blocks the split"],
      ["NONNORMAL_2D","even lower boundary","m>=1","X=(2m,0)","T=(0,2)","Y=(1,1)","Z=(2m-1,1)","low-strip obstruction"],
      ["NONNORMAL_2D","even y=1 strip","m>=1","X=(2m,1)","T=(0,1)","Y=(1,1)","Z=(2m-1,1)","low-strip obstruction"],
      ["NORMAL_SQUARE3","off BC splitting locus","X=(x,y,n), n!=x+y","M=max(x,y,n-x,n-y)","T=(M-x,M-y,2M-n)","Y=(M,0,M)","Z=(0,M,M)","any refinement would force n=x+y"],
      ["NORMAL_SQUARE3","on n=x+y but off diagonal","X=(x,y,n), n=x+y, x!=y","M=max(x,y,n-x,n-y)","T=(M-x,M-y,2M-n)","Y=(0,0,M)","Z=(M,M,M)","any refinement would force x=y"],
    ]
    path=OUT/"AFFINE_UNBOUNDED_CERTIFICATES.csv"
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f)
        w.writerow(["system","family","parameters_or_condition","distinguished_X","T_or_M","Y","Z","obstruction"])
        w.writerows(rows)
    return len(rows)


def main():
    OUT.mkdir(parents=True,exist_ok=True); REC.mkdir(parents=True,exist_ok=True)
    checks=run_regressions()
    summary=write_summary()
    fams=write_families()
    result={
        "result":"AFFINE_ELEMENTWISE_EXACT",
        "systems":len(summary),
        "failure_systems":4,
        "failure_systems_with_unbounded_nonprimal_locus":4,
        "finite_core_phenomenon_survives_higher_rank_controls":False,
        "certificate_families":fams,
        "regression_certificate_instances_checked":checks,
        "sample_counts":sample_counts(),
        "core_conclusion":"ARD>0 failure is not confined to a finite obstruction core in the retained higher-rank affine controls; non-primality propagates along unbounded rays, congruence classes, strips, or all but a lower-dimensional primal spine."
    }
    (REC/"AFFINE_ELEMENTWISE_RESULT.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()

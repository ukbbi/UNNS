#!/usr/bin/env python3
from pathlib import Path
from itertools import product
from math import log, sqrt
import csv, json, shutil

ROOT=Path(__file__).resolve().parents[1]
INDEX=ROOT/"corpus"/"CORPUS_INDEX.csv"
CASES=ROOT/"corpus"/"cases"
LADDERS=ROOT/"corpus"/"ladders"
SI=ROOT/"inputs"/"struc_i"
SP=ROOT/"inputs"/"struc_perc_i"
LADDER_INDEX=ROOT/"corpus"/"LADDER_INDEX.csv"

N=128
SQRT_PRIMES=[sqrt(p) for p in [2,3,5,7,11,13,17,19]]

def add_vec(a,b):
    return tuple(x+y for x,y in zip(a,b))

def scalar(v, weights):
    return sum(x*w for x,w in zip(v,weights))

def enumerate_vectors(gens,weights,n=N):
    d=len(gens[0])
    zero=(0,)*d
    current={zero}
    allset={zero}
    gh=[scalar(g,weights) for g in gens]
    hmin=min(gh)
    D=0
    while True:
        ranked=sorted((scalar(x,weights),x) for x in allset)
        if len(ranked)>=n:
            hn=ranked[n-1][0]
            if (D+1)*hmin > hn + 1e-12:
                return ranked[:n],D,len(allset),hn
        D+=1
        new=set()
        for x in current:
            for g in gens:
                y=add_vec(x,g)
                if y not in allset:
                    new.add(y)
        current=new
        allset |= new
        if not current:
            raise RuntimeError("enumeration stalled")
        if D>5000:
            raise RuntimeError("enumeration depth exceeded")

def build_one(c):
    sys=c["system"]
    cls=c["class"]

    if cls=="INT_FREE":
        ps=sys["active_primes"]
        r=len(ps)
        gens=[tuple(1 if i==j else 0 for i in range(r)) for j in range(r)]
        weights=[log(p) for p in ps]
        ranked,D,n_enum,hn=enumerate_vectors(gens,weights)
        method="prime_exponent_log_spectrum"
        exact=[list(x) for _,x in ranked]

    elif sys["kind"]=="rank1":
        gens=[(int(g),) for g in sys["generators"]]
        weights=[1.0]
        ranked,D,n_enum,hn=enumerate_vectors(gens,weights)
        method="rank1_element_spectrum"
        exact=[x[0] for _,x in ranked]

    elif sys["kind"]=="affine":
        gens=[tuple(map(int,g)) for g in sys["generators"]]
        d=len(gens[0])
        weights=SQRT_PRIMES[:d]
        ranked,D,n_enum,hn=enumerate_vectors(gens,weights)
        method="affine_sqrt_prime_projection"
        exact=[list(x) for _,x in ranked]

    else:
        raise ValueError(sys["kind"])

    values=[v for v,_ in ranked]
    if len(values)!=N:
        raise AssertionError("wrong spectrum length")
    if any(values[i] >= values[i+1] for i in range(len(values)-1)):
        raise AssertionError((c["case_id"],"spectrum is not strictly increasing"))

    return {
        "case_id":c["case_id"],
        "class":cls,
        "label":c["label"],
        "method":method,
        "N":N,
        "enumeration_depth":D,
        "elements_enumerated":n_enum,
        "H_128":hn,
        "values":values,
        "exact_elements":exact
    }

def main():
    LADDERS.mkdir(parents=True,exist_ok=True)
    SI.mkdir(parents=True,exist_ok=True)
    SP.mkdir(parents=True,exist_ok=True)

    for p in LADDERS.glob("*"):
        if p.is_file(): p.unlink()
    for p in SI.glob("*"):
        if p.is_file(): p.unlink()
    for p in SP.glob("*"):
        if p.is_file(): p.unlink()

    with INDEX.open(encoding="utf-8") as f:
        idx=list(csv.DictReader(f))

    all_rows=[]
    lrows=[]
    for row in idx:
        c=json.loads((ROOT/row["case_file"]).read_text(encoding="utf-8"))
        r=build_one(c)

        # Canonical corpus ladder file.
        lp=LADDERS/f"{r['case_id']}_system.csv"
        with lp.open("w",newline="",encoding="utf-8") as f:
            w=csv.writer(f); w.writerow(["value"])
            w.writerows([[format(x,".17g")] for x in r["values"]])

        # STRUC-PERC-I batch input: one file per ladder.
        shutil.copy2(lp, SP/f"{r['case_id']}.csv")

        # STRUC-I grouped input: one file, one ladder per case_id.
        all_rows.extend((r["case_id"],format(x,".17g")) for x in r["values"])

        # Detailed generation record.
        jp=LADDERS/f"{r['case_id']}_system.json"
        jp.write_text(json.dumps(r,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")

        lrows.append({
            "case_id":r["case_id"],
            "class":r["class"],
            "label":r["label"],
            "N":r["N"],
            "method":r["method"],
            "enumeration_depth":r["enumeration_depth"],
            "elements_enumerated":r["elements_enumerated"],
            "H_128":format(r["H_128"],".17g"),
            "ladder_file":f"corpus/ladders/{r['case_id']}_system.csv",
            "record_file":f"corpus/ladders/{r['case_id']}_system.json"
        })

    with (SI/"ALL_SYSTEM_SPECTRA.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["case_id","value"]); w.writerows(all_rows)

    with LADDER_INDEX.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(lrows[0]))
        w.writeheader(); w.writerows(lrows)

    print(f"Built {len(lrows)} ladders x {N} points.")
    print("STRUC-I input:", SI/"ALL_SYSTEM_SPECTRA.csv")
    print("STRUC-PERC-I batch files:", len(list(SP.glob("*.csv"))))

if __name__=="__main__":
    main()

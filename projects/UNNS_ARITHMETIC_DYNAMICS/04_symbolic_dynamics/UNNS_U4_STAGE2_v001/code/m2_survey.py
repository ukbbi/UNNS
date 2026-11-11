"""Stage 2C: exhaustive/sampled survey of metric admissibility rules of memory 1 and 2 on predeclared windows. Reads data/stage2_config.json."""
import sys,os,json,math,random,itertools,time
H=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,H)
import numpy as np,networkx as nx,sympy
import indep_graph as I
D=H+"/../data"
def targets(n):
    L=[];B=np.array([[1,1],[1,0]],dtype=object);P=np.identity(2,dtype=object)
    for _ in range(n): P=P.dot(B);L.append(int(P[0,0]+P[1,1]))
    C=np.array([[1,1,0],[0,1,1],[1,0,1]],dtype=object);P=np.identity(3,dtype=object);L3=[]
    for _ in range(n): P=P.dot(C);L3.append(int(sum(P[i,i] for i in range(3))))
    return {"golden_mean":tuple(L),"directed_3cycle_with_loops":tuple(L3),"full_2_shift":tuple(2**k for k in range(1,n+1)),"full_3_shift":tuple(3**k for k in range(1,n+1)),
            "NB_5_cycle":tuple(10 if k%5==0 else 0 for k in range(1,n+1)),"NB_4_cycle":tuple(8 if k%4==0 else 0 for k in range(1,n+1))}
def run():
    cfg=json.load(open(D+"/stage2_config.json"));S=cfg["survey_2C"];rnd=random.Random(cfg["seed"]);SL=S["signature_length"];tol=S["eig_tol"];TG=targets(SL)
    EXACT={};audit=[];res=dict(windows=[],targets_seen={m:{k:0 for k in TG} for m in (1,2)},aggregate={})
    agg={m:dict(rules=0,nonempty=0,nonreal=0,nonempty_no_period_le2=0,fixed_point_violations=0,reversal_asymmetric=0,asymmetric_nonreal=0,asym_nonempty=0,signatures=set()) for m in (1,2)}
    for F in S["windows"]:
        F=tuple(F);dist={(a,b):I.dist(a,b,10) for a in F for b in F};n=len(F)
        for m in S["memories"]:
            types={}
            for w in itertools.product(F,repeat=m+1):
                t=tuple(dist[(w[i],w[j])] for i in range(m+1) for j in range(i+1,m+1));types.setdefault(t,[]).append(w)
            T=sorted(types);states=list(itertools.product(F,repeat=m));idx={s:i for i,s in enumerate(states)}
            # per-type edge lists
            elist={t:[(idx[w[:-1]],idx[w[1:]]) for w in types[t]] for t in T}
            def rev(t):  # reversal of a window: distance tuple for reversed order
                if m==1: return t
                d01,d02,d12=t;return (d12,d02,d01)
            if len(T)<=14: rules=[frozenset(c) for r in range(len(T)+1) for c in itertools.combinations(T,r)];mode="exhaustive"
            else:
                rules=[];
                for _ in range(S["sampled_rules"]):
                    p=rnd.uniform(.05,.95);rules.append(frozenset(t for t in T if rnd.random()<p))
                mode="sampled"
            wr=dict(window=list(F),memory=m,types=len(T),mode=mode,rules=len(rules),nonreal=0,nonempty=0,nonempty_no_low=0,asym=0)
            for acc in rules:
                B=np.zeros((len(states),len(states)),dtype=np.int64)
                for t in acc:
                    for (a,b) in elist[t]: B[a,b]=1
                P=B.copy();pn=[int(np.trace(P))]
                for _ in range(SL-1): P=P.dot(B);pn.append(int(np.trace(P)))
                tr1=pn[0]
                A=agg[m];A["rules"]+=1
                if tr1 not in(0,n): A["fixed_point_violations"]+=1
                # exact recurrent structure: nonzero spectrum of B = union of spectra of nontrivial strongly connected blocks (A1 amendment)
                g=nx.DiGraph();g.add_nodes_from(range(len(states)));g.add_edges_from(zip(*np.nonzero(B)))
                blocks=[sorted(c) for c in nx.strongly_connected_components(g) if len(c)>1 or any(B[i,i] for i in c)]
                ne=bool(blocks)
                if ne: A["nonempty"]+=1;wr["nonempty"]+=1
                nonreal=False
                for blk in blocks:
                    sub=B[np.ix_(blk,blk)]
                    key=(sub.shape[0],sub.astype(np.int8).tobytes())
                    if key not in EXACT:
                        cp=sympy.Poly(sympy.Matrix(sub.tolist()).charpoly(sympy.Symbol('x')).as_expr(),sympy.Symbol('x'))
                        EXACT[key]=(sum(mult*sympy.Poly(f,sympy.Symbol('x')).count_roots() for f,mult in cp.sqf_list()[1])!=cp.degree())
                    if EXACT[key]: nonreal=True;break
                if nonreal: A["nonreal"]+=1;wr["nonreal"]+=1
                low=(pn[0]+pn[1])>0
                if ne and not low: A["nonempty_no_period_le2"]+=1;wr["nonempty_no_low"]+=1
                asym=any(rev(t) not in acc for t in acc)
                if asym: A["reversal_asymmetric"]+=1;wr["asym"]+=1;A["asym_nonempty"]+=ne
                if asym and nonreal: A["asymmetric_nonreal"]+=1
                sig=tuple(pn);A["signatures"].add(sig)
                for k,v in TG.items():
                    if sig==v: res["targets_seen"][m][k]+=1
            res["windows"].append(wr)
    for m in agg:
        a=agg[m];a["distinct_signatures"]=len(a.pop("signatures"))
    res["exact_blocks_classified"]=len(EXACT)
    res["aggregate"]=agg;res["target_signatures"]={k:list(v) for k,v in TG.items()}
    return res
if __name__=="__main__":
    t=time.time();r=run();json.dump(r,open(sys.argv[1],"w"),indent=1)
    print(json.dumps(r["aggregate"],indent=1));print(r["targets_seen"]);print(round(time.time()-t),"s")

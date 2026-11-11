"""Stage 2B: certificates for the non-backtracking memory-two shift Y_NB (theorem U4-M2). Independent engine for all distances."""
import sys,os,json,math,time
H=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,H);sys.path.insert(0,H+"/../engine")
import numpy as np,sympy
import indep_graph as I
def y_nb_valid_cycle(cyc,maxd=4):
    n=len(cyc)
    return all(I.dist(cyc[i],cyc[(i+1)%n],maxd)==1 and I.dist(cyc[i],cyc[(i+2)%n],maxd)==2 for i in range(n))
def primitive_period(seq):
    n=len(seq)
    return min(p for p in range(1,n+1) if n%p==0 and all(seq[i]==seq[(i+p)%n] for i in range(n)))
def ball(a,R):
    seen={a:0};fr=[a]
    for r in range(1,R+1):
        nf=[]
        for v in fr:
            for w in I.nbrs(v):
                if w not in seen: seen[w]=r;nf.append(w)
        fr=nf
    return seen
def hashimoto(vs):
    S=set(vs);E=[(u,v) for u in S for v in I.nbrs(u) if v in S];idx={e:i for i,e in enumerate(E)}
    rows=[];cols=[]
    for (u,v) in E:
        for w in I.nbrs(v):
            if w in S and w!=u: rows.append(idx[(u,v)]);cols.append(idx[(v,w)])
    M=np.zeros((len(E),len(E)),dtype=np.int64)
    for a,b in zip(rows,cols): M[a,b]=1
    return E,M
def periodic_counts(M,n):
    P=np.identity(len(M),dtype=np.int64);out=[]
    for _ in range(n):
        P=P.dot(M);out.append(int(np.trace(P)))
    return out
def rho_hashimoto_power(S):
    """dominant eigenvalue of the Hashimoto operator via power iteration using B^T v[j]=Sum_head(tail j) - v[rev j] (floats; lower-bound corroboration)"""
    S=set(S)
    # 2-core
    ch=True
    while ch:
        ch=False
        for v in list(S):
            if sum(1 for w in I.nbrs(v) if w in S)<=1: S.discard(v);ch=True
    E=[(u,v) for u in S for v in I.nbrs(u) if v in S]
    if not E: return 0.0,0,0
    idx={e:i for i,e in enumerate(E)};tail=np.array([e[0] for e in E]);head=np.array([e[1] for e in E])
    rev=np.array([idx[(v,u)] for (u,v) in E]);verts=sorted(S);vi={v:i for i,v in enumerate(verts)};tl=np.array([vi[t] for t in tail]);hd=np.array([vi[h] for h in head])
    x=np.ones(len(E));lam=0
    for _ in range(400):
        Sv=np.zeros(len(verts));np.add.at(Sv,hd,x)
        y=Sv[tl]-x[rev]
        nrm=y.sum()/x.sum();lam=nrm;x=y/y.sum()*len(E)
    return float(lam),len(S),len(E)
def run():
    out={}
    # 1. equivalence NB <=> d(x_n,x_{n+2})=2 (triangle-free): all paths a~b~c, a<=2500
    paths=0;viol=0
    for a in range(1,2501):
        na=set(I.nbrs(a))
        for b in na:
            for c in I.nbrs(b):
                if c==a: continue
                paths+=1
                if c in na: viol+=1                      # c adjacent to a would be a triangle (then d(a,c)=1)
    out["equivalence"]=dict(nonbacktracking_paths_checked=paths,triangle_violations=viol,passed=viol==0)
    # 2. witnesses + scaling family
    C4=[2,8,36,9];C5=[6,24,96,784,27]
    wit=dict(C4_valid=y_nb_valid_cycle(C4),C4_primitive_period=primitive_period(C4),C5_valid=y_nb_valid_cycle(C5),C5_primitive_period=primitive_period(C5))
    sc4=all(y_nb_valid_cycle([j*x for x in C4]) for j in range(1,41));sc5=all(y_nb_valid_cycle([j*x for x in C5]) for j in range(1,13))
    wit.update(scaling_C4_j_le_40=sc4,scaling_C5_j_le_12=sc5)
    # scaling is an adjacency-preserving injection (edge {kN,k(N+1)^2} -> {jkN,jk(N+1)^2}): checked on all edges x<=1500, j<=6
    sc_edge=all((j*b in set(I.nbrs(j*a))) for a in range(1,1500) for b in I.nbrs(a) for j in (2,3,5,6))
    wit["scaling_preserves_adjacency_checked"]=sc_edge
    out["witnesses"]=dict(wit,passed=bool(wit["C4_valid"] and wit["C5_valid"] and wit["C4_primitive_period"]==4 and wit["C5_primitive_period"]==5 and sc4 and sc5 and sc_edge))
    # 3. periodic-point counts of the window shift on ball(1,4) (Hashimoto trace)
    B4=ball(1,4);E,M=hashimoto(B4);pc=periodic_counts(M,10)
    B3=ball(1,3);E3,M3=hashimoto(B3);pc3=periodic_counts(M3,10)
    out["periodic_counts"]=dict(window_ball_1_radius_4_vertices=len(B4),states=len(E),p_1_to_10=pc,window_ball_1_radius_3_vertices=len(B3),p3_1_to_10=pc3,
          passed=bool(pc[0]==pc[1]==pc[2]==0 and pc[3]>0 and pc[4]>0 and pc3[0]==pc3[1]==pc3[2]==0))
    # 4. dead end at vertex 1; degree structure
    d1=I.deg(1);others=min(I.deg(x) for x in range(2,3001))
    out["dead_end"]=dict(deg_1=d1,min_deg_x_ge_2_up_to_3000=others,neighbours_of_1=list(I.nbrs(1)),passed=bool(d1==1 and others>=2))
    # 5. cycle-window spectra
    spec={}
    for name,cyc in (("C4",C4),("C5",C5)):
        E,M=hashimoto(cyc);ev=np.linalg.eigvals(M.astype(float));pcw=periodic_counts(M,2*len(cyc))
        spec[name]=dict(states=len(E),nonreal_eigenvalue_present=bool(any(abs(z.imag)>1e-9 for z in ev)),periodic_counts=pcw,eigenvalues_rounded=sorted({(round(z.real,6),round(z.imag,6)) for z in ev}))
    out["cycle_window_spectra"]=dict(spec,passed=bool(spec["C4"]["nonreal_eigenvalue_present"] and spec["C5"]["nonreal_eigenvalue_present"] and spec["C5"]["periodic_counts"][:4]==[0,0,0,0] and spec["C5"]["periodic_counts"][4]==10))
    # 6. exploratory entropy lower bounds on hub windows (not a theorem; Gurevich entropy of Y_NB is sup over finite windows)
    rows=[]
    for x in (12,60,360):
        b=ball(x,2);lam,nv,ne=rho_hashimoto_power(b.keys());rows.append(dict(hub=x,degree=I.deg(x),window_vertices=len(b),core_vertices=nv,core_directed_edges=ne,rho_hashimoto_lower_bound=lam,log_rho=math.log(lam) if lam>0 else None))
    out["entropy_lower_bounds_exploratory"]=dict(rows=rows,passed=True,status="Registered observation: finite-window lower bounds only; no claim about the supremum")
    return out
if __name__=="__main__":
    t=time.time();o=run();json.dump(o,open(sys.argv[1],"w"),indent=1,default=str)
    for k,v in o.items(): print(k,v.get("passed"))
    print(round(time.time()-t),"s")

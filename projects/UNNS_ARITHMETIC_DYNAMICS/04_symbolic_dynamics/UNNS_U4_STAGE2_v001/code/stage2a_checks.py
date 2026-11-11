"""Stage 2A independent checks for U4.3-T2, U4.3-T3, U4.3-T4, U4.2-T4. All distances from indep_graph (independent engine)."""
import sys,os,json,math,random,itertools,time
H=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,H)
import numpy as np,sympy,networkx as nx
from fractions import Fraction
from networkx.generators.atlas import graph_atlas_g
import indep_graph as I
def window_types(F,m):
    """all realised isometry types of (m+1)-windows over F (as tuples of the upper-triangular distance entries)"""
    D={(a,b):I.dist(a,b,10) for a in F for b in F}
    types={}
    for w in itertools.product(F,repeat=m+1):
        t=tuple(D[(w[i],w[j])] for i in range(m+1) for j in range(i+1,m+1))
        types.setdefault(t,[]).append(w)
    return D,types
def block_matrix(F,m,types,accepted):
    """transition matrix of the m-block presentation: states = F^m, (x0..x_{m-1})->(x1..x_m) iff the window type is accepted"""
    D,_=None,None
    states=list(itertools.product(F,repeat=m));idx={s:i for i,s in enumerate(states)}
    B=np.zeros((len(states),len(states)),dtype=object)
    for t,ws in types.items():
        if t in accepted:
            for w in ws: B[idx[w[:-1]],idx[w[1:]]]=1
    return B
def mat_trace_pows(B,n):
    Bi=np.array(B,dtype=object);P=np.identity(len(B),dtype=object);out=[]
    for k in range(1,n+1):
        P=P.dot(Bi);out.append(int(sum(P[i,i] for i in range(len(B)))))
    return out
# ============================ U4.3-T2
def check_T2(seed=11):
    rnd=random.Random(seed);rows=[];viol=0;nonempty_no_lowperiod=0;nrules=0
    windows=[(2,8,36,9),(1,4,16),(6,24,96,784,27),(4,2,18),(2,3,5),(12,2,4,9),(60,30,15,20)]
    for F in windows:
        for m in (1,2,3):
            D,types=window_types(F,m);T=list(types)
            if len(T)<=14: rules=[frozenset(c) for r in range(len(T)+1) for c in itertools.combinations(T,r)];mode="exhaustive"
            else: rules=[frozenset(t for t in T if rnd.random()<.5) for _ in range(3000)];mode="sampled3000"
            cnt=0
            for acc in rules:
                Bm=block_matrix(F,m,types,acc);tr1=mat_trace_pows(Bm,1)[0]
                cnt+=1;nrules+=1
                if tr1 not in(0,len(F)): viol+=1
                if m==1:
                    p1,p2=mat_trace_pows(Bm,2)[0],mat_trace_pows(Bm,2)[1]
                    # lemma M1-P2: nonempty memory-1 metric shift has a point of period <=2 (nonempty = some letter has a successor chain; here: any allowed pair)
                    if Bm.any() and (p1+p2)==0: nonempty_no_lowperiod+=1
            rows.append((F,m,mode,len(T),cnt))
    # scope witness: vertex-dependent (degree-augmented) rule realises the golden mean, so the dichotomy is genuinely metric-specific
    p=5;F=(p,4*p)
    A=np.zeros((2,2),dtype=int)
    for i,a in enumerate(F):
        for j,b in enumerate(F):
            ok=(I.dist(a,b,3)<=1) and (a!=b or I.deg(a)==2)
            A[i,j]=1 if ok else 0
    gm_ok=A.tolist()==[[1,1],[1,0]] and I.deg(5)==2 and I.deg(20)!=2
    return dict(rules_tested=nrules,windows=rows,fixed_point_violations=viol,lemma_M1_P2_violations=nonempty_no_lowperiod,
                degree_augmented_golden_mean_matrix=A.tolist(),degree_augmented_realises_golden_mean=bool(gm_ok),
                passed=bool(viol==0 and nonempty_no_lowperiod==0 and gm_ok))
# ============================ U4.3-T3
def newton_charpoly(pn,n):
    """power sums p1..pn -> characteristic polynomial coefficients via Newton identities (exact Fractions)"""
    e=[Fraction(1)]
    for k in range(1,n+1):
        s=sum((-1)**(i-1)*e[k-i]*pn[i-1] for i in range(1,k+1))
        e.append(s/k)
    return [(-1)**k*e[k] for k in range(n+1)]  # x^n + c1 x^{n-1}...  with sign pattern (-1)^k e_k
def check_T3():
    x=sympy.Symbol('x');atlas=[g for g in graph_atlas_g() if 1<=g.number_of_nodes()<=6];rows=0;bad=0;newton_bad=0
    for g in atlas:
        A=nx.to_numpy_array(g,dtype=int)
        for loops in (0,1):
            B=A+loops*np.eye(len(A),dtype=int);M=sympy.Matrix(B.tolist());cp=sympy.Poly(M.charpoly(x).as_expr(),x)
            rows+=1
            real_mult=sum(mult*sympy.Poly(fac,x).count_roots() for fac,mult in cp.sqf_list()[1])   # exact Sturm count per squarefree factor, with multiplicity
            if real_mult!=cp.degree(): bad+=1                              # all roots real
            n=len(B);pn=mat_trace_pows(B.astype(object),n);co=newton_charpoly(pn,n)
            if [int(c) if c.denominator==1 else None for c in co]!=[int(c) for c in cp.all_coeffs()]: newton_bad+=1
    # target: 3-cycle with loops
    Bt=np.array([[1,1,0],[0,1,1],[1,0,1]],dtype=object);Mt=sympy.Matrix(Bt.tolist());cpt=sympy.Poly(Mt.charpoly(x).as_expr(),x)
    pn_t=mat_trace_pows(Bt,12);coef=[int(c) for c in cpt.all_coeffs()]
    recovered=[int(c) for c in newton_charpoly(pn_t,3)]
    return dict(symmetric_01_matrices_tested=rows,matrices_with_nonreal_root=bad,newton_vs_sympy_charpoly_mismatch=newton_bad,
                target_charpoly=str(cpt.as_expr()),target_real_roots=cpt.count_roots(),target_degree=cpt.degree(),target_periodic_point_counts_1_12=pn_t,
                target_charpoly_recovered_from_periodic_points=recovered==coef,
                passed=bool(bad==0 and newton_bad==0 and cpt.count_roots()<cpt.degree() and recovered==coef))
# ============================ U4.3-T4
def check_T4():
    x=sympy.Symbol('x');rows=[];allok=True;maxrho={}
    for k in range(3,8):
        mx=Fraction(0);cnt=0;rho2_bad=0;mantel_bad=0;exact_bad=0
        for g in graph_atlas_g():
            if g.number_of_nodes()!=k or sum(nx.triangles(g).values())!=0: continue
            cnt+=1;A=nx.to_numpy_array(g,dtype=int);m=g.number_of_edges()
            rho=max(np.linalg.eigvalsh(A.astype(float)))
            if rho*rho>m+1e-9: rho2_bad+=1                       # Nosal: rho^2 <= m (triangle-free)
            if m>k*k//4: mantel_bad+=1                           # Mantel
            B=sympy.Matrix((A+np.eye(k,dtype=int)).tolist());cp=sympy.Poly(B.charpoly(x).as_expr(),x)
            if cp.count_roots(k,None)!=0: exact_bad+=1           # exact Sturm: no eigenvalue of A+I in [k,oo)
        rows.append(dict(k=k,triangle_free_graphs=cnt,rho2_gt_m=rho2_bad,mantel_violations=mantel_bad,eigenvalue_ge_k=exact_bad))
        allok&=(rho2_bad==0 and mantel_bad==0 and exact_bad==0)
    # independent entropy computation by word counting: log(#words_n)/n with exact integers, k=3..5 (extremal bipartite K_{floor(k/2),ceil(k/2)})
    ent=[]
    for k in (3,4,5,6):
        g=nx.complete_bipartite_graph(k//2,k-k//2);B=nx.to_numpy_array(g,dtype=int)+np.eye(k,dtype=int);Bo=B.astype(object)
        P=np.identity(k,dtype=object)
        for _ in range(60): P=P.dot(Bo)
        w60=int(P.sum());P2=P.dot(Bo);w61=int(P2.sum())
        ent.append(dict(k=k,ratio_words_61_over_60=w61/w60,log_k=math.log(k),max_log_rho=math.log(max(np.linalg.eigvalsh(B.astype(float)))),ratio_lt_k=bool(w61/w60<k)))
    # realisation at radius 2 by a star (independent distances), and k=2 realised at radius 1
    star=[]
    for k in (3,4,5,8):
        x=2
        while I.deg(x)<k-1: x+=1
        Fk=[x]+list(I.nbrs(x))[:k-1];mx=max(I.dist(a,b,4) for a in Fk for b in Fk if a!=b);star.append((k,x,mx))
    k2=I.dist(1,4,3)==1
    return dict(per_k=rows,entropy_word_counting=ent,star_realisations_max_distance=star,k2_realised_at_radius1=bool(k2),
                passed=bool(allok and all(e["ratio_lt_k"] for e in ent) and all(s[2]<=2 for s in star) and k2))
# ============================ U4.2-T4
def period_bfs_levels(n,edges):
    """period of the strongly connected digraph (nodes 0..n-1, edges list) by BFS levels: gcd(level[u]+1-level[v])"""
    adj={i:[] for i in range(n)}
    for u,v in edges: adj[u].append(v)
    lvl={0:0};q=[0]
    while q:
        u=q.pop(0)
        for v in adj[u]:
            if v not in lvl: lvl[v]=lvl[u]+1;q.append(v)
    if len(lvl)!=n: return None
    g=0
    for u,v in edges: g=math.gcd(g,lvl[u]+1-lvl[v])
    return g
def expanded_graph(F,rel,roof):
    """tower graph: node (a) at base position, edge a->b replaced by a path of roof(a,b) arcs through roof-1 fresh nodes"""
    idx={a:i for i,a in enumerate(F)};n=len(F);edges=[]
    for (a,b) in rel:
        r=roof[(a,b)];prev=idx[a]
        for j in range(1,r):
            edges.append((prev,n));prev=n;n+=1
        edges.append((prev,idx[b]))
    return n,edges
def check_T4P(seed=5):
    rnd=random.Random(seed);tested=0;mism=0;pot_bad=0;enum_bad=0;period_hist={}
    for _ in range(400):
        k=rnd.randint(2,5);F=rnd.sample(range(1,60),k);rel=set()
        # random symmetric relation, connected, with at least one loop
        for i in range(k):
            for j in range(i+1,k):
                if rnd.random()<.6: rel.add((F[i],F[j]));rel.add((F[j],F[i]))
        for a in F:
            if rnd.random()<.4: rel.add((a,a))
        rel.add((F[0],F[0]))
        # restrict to the component of F[0]
        comp={F[0]};ch=True
        while ch:
            ch=False
            for (a,b) in rel:
                if a in comp and b not in comp: comp.add(b);ch=True
        C=sorted(comp);R=[(a,b) for (a,b) in rel if a in comp and b in comp]
        roof={(a,b):(2 if a==b else I.dist(a,b,12)) for (a,b) in R}
        if any(v is None for v in roof.values()): continue
        tested+=1
        n,ed=expanded_graph(C,R,roof);per=period_bfs_levels(n,ed)
        # parity potential by BFS over the symmetric graph
        f={C[0]:0};q=[C[0]]
        while q:
            u=q.pop()
            for (a,b) in R:
                if a==u and b not in f: f[b]=(f[u]+roof[(a,b)])%2;q.append(b)
        has_pot=all((roof[(a,b)]-f[a]-f[b])%2==0 for (a,b) in R if a!=b)
        if per not in(1,2): mism+=1
        if (per==2)!=has_pot: pot_bad+=1
        # enumerate closed walks up to length 5 and check: all sums even <=> period 2
        sums_even=True;adj={a:[b for (x,b) in R if x==a] for a in C}
        def walk(start,cur,s,l):
            if cur==start and l>0 and s%2: return False
            if l==5: return True
            return all(walk(start,nx_,s+roof[(cur,nx_)],l+1) for nx_ in adj[cur])
        ev=all(walk(a,a,0,0) for a in C)
        if (per==2) and not ev: enum_bad+=1
        if ev is False and per==2: enum_bad+=1
        period_hist[per]=period_hist.get(per,0)+1
    # golden mean for every ordered embedding in 1..30
    gm_bad=0;gm=0
    for e0 in range(1,31):
        for e1 in range(1,31):
            if e0==e1: continue
            d=I.dist(e0,e1,12);R=[(e0,e0),(e0,e1),(e1,e0)];roof={(e0,e0):2,(e0,e1):d,(e1,e0):d}
            n,ed=expanded_graph([e0,e1],R,roof);per=period_bfs_levels(n,ed);gm+=1
            if per!=2: gm_bad+=1
    # scope witnesses: no loop => period can exceed 2; repeat-convention dependence
    a,b=2,36;d=I.dist(a,b,6);n,ed=expanded_graph([a,b],[(a,b),(b,a)],{(a,b):d,(b,a):d});noloop=period_bfs_levels(n,ed)
    n,ed=expanded_graph([0,1],[(0,0),(0,1),(1,0)],{(0,0):1,(0,1):5,(1,0):5});conv1=period_bfs_levels(n,ed)
    return dict(random_components=tested,period_histogram=period_hist,period_not_in_1_2=mism,parity_potential_mismatch=pot_bad,closed_walk_enumeration_mismatch=enum_bad,
                golden_mean_ordered_embeddings=gm,golden_mean_non_period2=gm_bad,
                scope_no_loop_period=noloop,scope_no_loop_roofsum=2*d,scope_repeat_cost_1_golden_mean_period=conv1,
                passed=bool(mism==0 and pot_bad==0 and enum_bad==0 and gm_bad==0 and noloop>2 and conv1==1))
if __name__=="__main__":
    out={};t0=time.time()
    for name,fn in (("U4.3-T2",check_T2),("U4.3-T3",check_T3),("U4.3-T4",check_T4),("U4.2-T4",check_T4P)):
        out[name]=fn();print(name,out[name]["passed"],round(time.time()-t0),"s",flush=True)
    json.dump(out,open(sys.argv[1],"w"),indent=1,default=str)

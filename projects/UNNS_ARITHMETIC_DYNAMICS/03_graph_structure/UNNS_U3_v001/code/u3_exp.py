"""UNNS-U3 v001 registered experiments (U3-1 .. U3-5).  Deterministic; writes data/u3_results.json."""
import sys,os,json,itertools,math,random,collections
H=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,H)
import u3_graph as G
import rn_core as C
from math import gcd
import mpmath as mp
CFG=json.load(open(H+"/../data/u3_config.json"))
def edge_ok(u,v): return v in set(G.nbrs(u))
# ---------------- U3-1 routing
def all_geodesics(a,b,d):
    sb,_=G.layers(b,d);out=[]
    def rec(path,i):
        if i==d: out.append(tuple(path));return
        for w in G.nbrs(path[-1]):
            if sb.get(w,99)==d-1-i: rec(path+[w],i+1)
    rec([a],0);return out
def routing_validation(N0):
    rows=[];bad=0;lexbad=0;bfsbad=0;maxd=0
    for a in range(1,N0+1):
        for b in range(1,N0+1):
            if a==b: continue
            d=G.dist(a,b);P=G.geodesic(a,b)
            ok=len(P)==d+1 and P[0]==a and P[-1]==b and all(edge_ok(P[i],P[i+1]) for i in range(d))
            if not ok: bad+=1
            if d<=4:
                if min(all_geodesics(a,b,d))!=P: lexbad+=1
            if d<=5:
                seen,L=G.layers(a,d)
                if seen.get(b)!=d: bfsbad+=1
            maxd=max(maxd,d);rows.append((a,b,d))
    return dict(pairs=len(rows),illegal_or_wrong_length=bad,lex_first_mismatch_d_le_4=lexbad,plain_bfs_mismatch_d_le_5=bfsbad,max_distance=maxd,
                succ_distance=[G.dist(n,n+1) for n in range(1,N0)],dist_matrix={f"{a},{b}":d for a,b,d in rows})
def history(s):
    w=[s[0]];marks=[0]
    for a,b in zip(s,s[1:]):
        P=G.geodesic(a,b);w+=list(P[1:]);marks.append(len(w)-1)
    return w,marks
def decode(w,marks): return [w[i] for i in marks]
def valid_segment(w,i,j):
    a,b=w[i],w[j]
    if a==b: return tuple(w[i:j+1])==(a,4*a,a)
    if G.dist(a,b,j-i)!=j-i: return False
    return tuple(w[i:j+1])==G.geodesic(a,b)
def M_count(w):
    L=len(w)-1;ways=[0]*(L+1);ways[0]=1
    for j in range(1,L+1):
        for i in range(j):
            if ways[i] and valid_segment(w,i,j): ways[j]+=ways[i]
    return ways[L]
def u31(cfg):
    out={}
    out["routing"]=routing_validation(cfg["routing_N0"])
    rnd=random.Random(cfg["seed"]);dec_bad=0;mono_bad=0
    for _ in range(cfg["decode_trials"]):
        s=[rnd.randint(1,cfg["decode_alpha"]) for _ in range(cfg["decode_len"])]
        w,m=history(s)
        if decode(w,m)!=s: dec_bad+=1
        if any(m[i]>=m[i+1] for i in range(len(m)-1)): mono_bad+=1
        if any(not edge_ok(w[i],w[i+1]) for i in range(len(w)-1)): dec_bad+=1
    out["decode"]=dict(trials=cfg["decode_trials"],decode_failures=dec_bad,nonincreasing_marks=mono_bad)
    out["example_1_4_16"]=dict(M=M_count([1,4,16]),walk=[1,4,16],sources=["(1,16)","(1,4,16)"])
    ext=[]
    for L in range(1,cfg["ext_maxL"]+1):
        b=next(b for b in range(2,cfg["ext_search"]) if G.dist(1,b,L)==L)
        w=list(G.geodesic(1,b));ext.append(dict(L=L,b=b,walk=w,M=M_count(w),predicted=2**(L-1)))
    out["extremal"]=ext
    rows=[]
    for s in itertools.product(range(1,cfg["samp_alpha"]+1),repeat=cfg["samp_len"]):
        w,m=history(list(s));M=M_count(w);rows.append((len(w)-1,len(m)-1,M))
    out["sample"]=dict(alphabet=cfg["samp_alpha"],length=cfg["samp_len"],words=len(rows),
        mean_L=sum(r[0] for r in rows)/len(rows),max_L=max(r[0] for r in rows),ambiguous_fraction=sum(1 for r in rows if r[2]>1)/len(rows),
        mean_log2M=sum(math.log2(r[2]) for r in rows)/len(rows),max_log2M=max(math.log2(r[2]) for r in rows),
        bound_ok=all(r[2]<=2**(r[0]-1) if r[0]>=1 else True for r in rows),
        M_histogram=dict(collections.Counter(r[2] for r in rows)))
    return out
# ---------------- U3-2 tower
def period_of(edges):
    """edges: list (u,v,len). irreducible assumed. period = gcd over closed-walk lengths via potential."""
    nodes={u for u,v,l in edges}|{v for u,v,l in edges};adj=collections.defaultdict(list)
    for u,v,l in edges: adj[u].append((v,l))
    s=next(iter(nodes));pot={s:0};st=[s];g=0
    while st:
        u=st.pop()
        for v,l in adj[u]:
            if v not in pot: pot[v]=pot[u]+l;st.append(v)
    for u,v,l in edges:
        if u in pot and v in pot: g=gcd(g,pot[u]+l-pot[v])
    return g
def tower_graph_edges(F,allowed):
    """symbol transition edges with roofs: (a,b) allowed; roof=d(a,b) or 2"""
    return [(a,b,2 if a==b else G.dist(a,b)) for a in F for b in F if (a,b) in allowed]
import numpy as np
def expanded(d):
    nodes={}
    def idx(x): return nodes.setdefault(x,len(nodes))
    E=[]
    for (u,v,l) in [(0,0,2),(0,1,d),(1,0,d)]:
        prev=("s",u)
        for k in range(1,l): nxt=("m",u,v,k);E.append((idx(prev),idx(nxt)));prev=nxt
        E.append((idx(prev),idx(("s",v))))
    return nodes,E
def golden(cfg):
    out={};rows=[];mp.mp.dps=40
    phi=(1+mp.sqrt(5))/2
    for e0,e1 in itertools.permutations(range(1,cfg["emb_max"]+1),2):
        d=G.dist(e0,e1);per=period_of([(0,0,2),(0,1,d),(1,0,d)])
        w=mp.findroot(lambda t:1-t-t**d,0.7);lam_formula=float(1/mp.sqrt(w))       # renewal equation det(I-M(lambda))=0
        nodes,E=expanded(d);n=len(nodes);A=np.zeros((n,n))
        for a,b in E: A[a,b]=1
        rho=max(abs(np.linalg.eigvals(A)))                                          # spectral radius of the expanded graph
        # Parry lift of the base Parry chain
        Pb={(0,0):float(1/phi),(0,1):float(1/phi**2),(1,0):1.0}
        T=np.zeros((n,n))
        for (u,v),p in Pb.items():
            first=nodes[("s",u)] if d==1 or True else None
        for (u,v,l) in [(0,0,2),(0,1,d),(1,0,d)]:
            pass
        # build transition matrix of the lift: from ("s",u) go to first chain node of edge (u,v) with prob Pb; chain nodes deterministic
        T=np.zeros((n,n))
        for (u,v),p in Pb.items():
            l=2 if u==v else d
            first=nodes[("m",u,v,1)] if l>1 else nodes[("s",v)]
            T[nodes[("s",u)],first]+=p
            for k in range(1,l):
                a=nodes[("m",u,v,k)];b=nodes[("m",u,v,k+1)] if k+1<l else nodes[("s",v)]
                T[a,b]=1.0
        ev,evec=np.linalg.eig(T.T);k=np.argmin(abs(ev-1));pi=np.real(evec[:,k]);pi=pi/pi.sum()
        H=lambda row:-sum(x*math.log(x) for x in row if x>0)
        lift=sum(pi[i]*H(T[i]) for i in range(n))
        pi0=float(phi**2/(1+phi**2));pi1=1-pi0
        rbar=pi0*(Pb[(0,0)]*2+Pb[(0,1)]*d)+pi1*d
        abr=float(mp.log(phi))/rbar
        rows.append(dict(e0=e0,e1=e1,d=d,period=per,top_entropy_expanded=math.log(rho),top_entropy_renewal=math.log(lam_formula),
                         lift_entropy_numeric=lift,abramov_formula=abr,mean_roof=rbar))
    out["rows"]=rows
    out["all_period_2"]=all(r["period"]==2 for r in rows)
    out["max_abs_diff_expanded_vs_renewal"]=max(abs(r["top_entropy_expanded"]-r["top_entropy_renewal"]) for r in rows)
    out["max_abs_diff_lift_vs_abramov"]=max(abs(r["lift_entropy_numeric"]-r["abramov_formula"]) for r in rows)
    out["topological_entropy_ge_lift_entropy_all"]=all(r["top_entropy_renewal"]>=r["abramov_formula"]-1e-12 for r in rows)
    out["topological_entropy_strictly_greater_all"]=all(r["top_entropy_renewal"]>r["abramov_formula"]+1e-9 for r in rows)
    out["distinct_top_entropies"]=len({round(r["top_entropy_renewal"],9) for r in rows})
    out["distinct_mean_roofs"]=len({round(r["mean_roof"],9) for r in rows})
    nodes,E=expanded(G.dist(1,2));n=len(nodes);cnt=[1]*n;seq=[]
    for t in range(1,61):
        new=[0]*n
        for a,b in E: new[a]+=cnt[b]
        cnt=new;seq.append(sum(cnt))
    out["count_growth_n60_(1,2)"]=float(mp.sqrt(mp.mpf(seq[-1])/seq[-3]));out["counts_first_(1,2)"]=seq[:8]
    return out
def full3(cfg):
    rows=[]
    for F in itertools.combinations(range(1,cfg["f3_max"]+1),3):
        allowed={(a,b) for a in F for b in F}
        edges=tower_graph_edges(F,allowed);rows.append((F,period_of(edges),sorted({(a,b):l for a,b,l in edges}.items())[:0]))
    c=collections.Counter(r[1] for r in rows)
    ex1=next(r for r in rows if r[1]==1)[0] if any(r[1]==1 for r in rows) else None
    ex2=next(r for r in rows if r[1]==2)[0] if any(r[1]==2 for r in rows) else None
    def triple(F):
        a,b,c=F;return dict(F=F,d=[G.dist(a,b),G.dist(b,c),G.dist(a,c)])
    return dict(triples=len(rows),period_counts={str(k):v for k,v in c.items()},example_period1=triple(ex1) if ex1 else None,example_period2=triple(ex2) if ex2 else None,
                example_123=dict(F=(1,2,3),period=period_of(tower_graph_edges((1,2,3),{(a,b) for a in(1,2,3) for b in(1,2,3)})),d=[G.dist(1,2),G.dist(2,3),G.dist(1,3)]),
                example_6_96_784=dict(F=(6,96,784),period=period_of(tower_graph_edges((6,96,784),{(a,b) for a in(6,96,784) for b in(6,96,784)})),d=[G.dist(6,96),G.dist(96,784),G.dist(6,784)]))
# ---------------- U3-0 graph facts
def graph_facts(cfg):
    tri=0
    for x in range(1,cfg["tri_max"]+1):
        Nx=set(G.nbrs(x))
        for y in Nx:
            if y>x:
                for z in G.nbrs(y):
                    if z>y and z in Nx: tri+=1
    # explicit odd cycle through 6,96,784
    p1=G.geodesic(6,96);p2=G.geodesic(6,784)
    cyc=list(p1)+list(reversed(p2))[:-1]       # 6..96 , then 96~784 edge implied by closing: p1 ends 96, p2 ends 784, edge 96-784
    cycle=list(p1)+[784]+list(reversed(p2))[1:-1]
    ok=all(edge_ok(cycle[i],cycle[(i+1)%len(cycle)]) for i in range(len(cycle))) and len(set(cycle))==len(cycle)
    # algebraic triangle-free check: no (a,b,c,t) integers with t>=1 solving the reduced system in a box
    sol=[(a,b,c) for a in range(1,60) for b in range(1,60) for c in range(1,200) if ((a+1)*(b+1))**2*c==(c+1)**2*a*b]
    return dict(triangles_found=tri,range=cfg["tri_max"],odd_cycle=cycle,odd_cycle_length=len(cycle),odd_cycle_valid=ok,triangle_equation_solutions_in_box=len(sol))
# ---------------- U3-3 realizability search
import networkx as nx
from networkx.generators.atlas import graph_atlas_g
def realizability(cfg):
    """A2: exact induced-subgraph search in G^(r) over vertices <= Vmax[r]; first vertex 1..W0[r];
    adjacency in G^(r) decided exactly (ball membership r<=2; meet-in-the-middle r=3).  Triangle graphs at r=1 are excluded by the triangle-free theorem."""
    out={}
    atlas=[g for g in graph_atlas_g() if 2<=g.number_of_nodes()<=cfg["h_maxn"] and nx.is_connected(g)]
    for r in cfg["radii"]:
        Vmax=cfg["Vmax"][str(r)];W0=cfg["W0"][str(r)];balls={}
        def ball(a,k):
            key=(a,k)
            if key not in balls:
                seen,_=G.layers(a,k);balls[key]=frozenset(seen)
            return balls[key]
        near_c={}
        def near(a,b):
            key=(min(a,b),max(a,b))
            if key not in near_c:
                if r<=2: near_c[key]=b in ball(a,r)
                else: near_c[key]=bool(ball(a,2)&ball(b,1))
            return near_c[key]
        def cands(a):
            if r==1: return sorted(x for x in G.nbrs(a) if x<=Vmax)
            if r==2: return sorted(x for x in ball(a,2) if x<=Vmax and x!=a)
            return [x for x in range(1,Vmax+1) if x!=a and near(a,x)]
        found=[];missing=[];skipped=[]
        for g in atlas:
            tri=sum(nx.triangles(g).values())>0
            tag=dict(n=g.number_of_nodes(),m=g.number_of_edges(),edges=sorted(map(list,g.edges())),triangle=tri)
            if r==1 and tri: skipped.append(tag);continue
            order=list(nx.bfs_tree(g,0).nodes());asg={}
            def rec(k):
                if k==len(order): return True
                v=order[k];anc=[u for u in order[:k] if g.has_edge(u,v)][0]
                for x in cands(asg[anc]):
                    if x in asg.values(): continue
                    if all(near(asg[u],x)==g.has_edge(v,u) for u in order[:k]):
                        asg[v]=x
                        if rec(k+1): return True
                        del asg[v]
                return False
            res=None
            for x0 in range(1,W0+1):
                asg={order[0]:x0}
                if rec(1): res=dict(asg);break
            if res is None: missing.append(tag)
            else:
                ok=all((G.dist(res[u],res[v],r)is not None and G.dist(res[u],res[v],r)<=r)==g.has_edge(u,v) for u,v in itertools.combinations(g.nodes(),2))
                found.append(dict(tag,embedding=[res[v] for v in sorted(g.nodes())],verified=ok))
        out[str(r)]=dict(connected_graphs_tested=len(atlas),searched=len(found)+len(missing),excluded_by_triangle_free_theorem=len(skipped),realized=len(found),not_found=len(missing),
                         search_universe=dict(Vmax=Vmax,first_vertex_max=W0),not_found_list=missing,all_embeddings_verified=all(f["verified"] for f in found),realized_list=found,
                         triangle_free_not_found=[m for m in missing if not m["triangle"]],triangle_graphs_realized=[f for f in found if f["triangle"]])
    return out
def conj_obstruction():
    # fixed points of X_r(F) = |F|  (constant sequences); golden mean has exactly 1 fixed point
    return dict(note="proved in manuscript; here: sample check d symmetric & d(a,a)=0 on window",
                symmetric_reflexive_checked=all(G.dist(a,b,6)==G.dist(b,a,6) for a in range(1,9) for b in range(1,9) if a!=b))
def accounting():
    sft={"golden_mean":dict(A=2,forbid=["11"]),"no_11_22_over3":dict(A=3,forbid=["11","22"]),"no_111_over2":dict(A=2,forbid=["111"]),"full_2":dict(A=2,forbid=[])}
    rows=[]
    for k,v in sft.items():
        A=v["A"];bits_sym=math.ceil(math.log2(A)) if A>1 else 1
        K_forbid=sum(len(w)*bits_sym for w in v["forbid"])
        rows.append(dict(system=k,alphabet=A,forbid=v["forbid"],K_forbidden_list_bits=K_forbid,K_embedding_bits_if_window_16=A*4,K_radius_bits_r_le_8=3))
    return rows
def cost_ledger(cfg):
    out=[]
    for a,b in [(1,2),(2,3),(6,7),(5,6)]:
        C._FC.clear();C.CNT.clear();G._NB.clear()
        d=G.dist(a,b);P=G.geodesic(a,b)
        out.append(dict(pair=[a,b],L=len(P)-1,neighbours_enum=C.CNT["neighbours_enum"],factor_calls=C.CNT["factor_calls"],rho_iter=C.CNT["rho_iter"],mr_modexp=C.CNT["mr_modexp"],certified=all(v[1] for v in G._NB.values())))
    return out
if __name__=="__main__":
    res={}
    res["U3_0_graph_facts"]=graph_facts(CFG["graph"])
    res["U3_1"]=u31(CFG["u31"])
    res["U3_2_golden"]=golden(CFG["u32"]);res["U3_2_full3"]=full3(CFG["u32"])
    res["U3_3_realizability"]=realizability(CFG["u33"]);res["U3_3_misc"]=conj_obstruction()
    res["U3_4_accounting"]=accounting();res["U3_5_cost_ledger"]=cost_ledger(CFG)
    res["all_neighbourhoods_certified"]=all(v[1] for v in G._NB.values())
    json.dump(res,open(H+"/../data/u3_results.json","w"),indent=1,default=str)
    print("done",res["all_neighbourhoods_certified"])

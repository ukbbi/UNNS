"""U4-M2-E1 verifier. Independent exact-integer layer (indep_graph). Usage: python3 ent_verify.py out.json"""
import os,sys,json,itertools,math
from fractions import Fraction
H=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,H)
import indep_graph as I
import numpy as np, sympy

def edge(a,b): return b in I.nbrs(a)
def blocks(x):
    """one 4-cycle per divisor N>=2 of x: x,4x,4y,y (cyclic), y=x(N+1)^2/N"""
    return {N:(x,4*x,4*(x*(N+1)**2//N),x*(N+1)**2//N) for N in sympy.divisors(x) if N>=2}   # N=1 gives y=4x: degenerate backtracking 'cycle', excluded
def window_ok(a,b,c): return edge(a,b) and edge(b,c) and I.dist(a,c)==2
def cycle_ok(cyc):
    n=len(cyc)
    return len(set(cyc))==n and all(window_ok(cyc[i],cyc[(i+1)%n],cyc[(i+2)%n]) for i in range(n))
def sequence_ok(seq): return all(window_ok(seq[i],seq[i+1],seq[i+2]) for i in range(len(seq)-2))

def check_blocks(xs):
    rep=[];bad=0
    for x in xs:
        B=blocks(x);ys=[b[3] for b in B.values()]
        ok=all(cycle_ok(c) for c in B.values()) and len(set(ys))==len(ys)
        # all ordered concatenations of length 2 and (for tau<=6) 3, checked on every window incl. the joins
        words=[]
        for L in (2,3 if len(B)<=6 else 2):
            for w in itertools.product(B,repeat=L):
                seq=[]
                for N in w: seq+=list(B[N])
                seq+=list(B[w[0]][:2])             # wrap two vertices to test the join windows after the last block
                words.append(sequence_ok(seq)); 
        ok&=all(words);bad+=(not ok)
        rep.append(dict(x=x,tau=len(B),branches_distinct=len(set(ys))==len(ys),all_ok=ok,words_checked=len(words)))
    return rep,bad

def pair_matrix(F):
    F=sorted(F);S=[(a,b) for a in F for b in F if I.dist(a,b)==1]
    idx={s:i for i,s in enumerate(S)};B=np.zeros((len(S),len(S)),dtype=object)
    for (a,b) in S:
        for (b2,c) in S:
            if b2==b and I.dist(a,c)==2: B[idx[(a,b)],idx[(b,c)]]=1
    return S,B

def cw_lower_bound(Bint):
    """Collatz-Wielandt: for B>=0, v>=0 nonzero and Bv>=lam*v, rho(B)>=lam. v rational from a float Perron vector, lam rational, tested in exact arithmetic"""
    Bf=np.array(Bint.tolist(),dtype=float);w,V=np.linalg.eig(Bf);k=int(np.argmax(w.real));v=np.abs(V[:,k].real)
    if v.max()==0: return Fraction(0)
    vq=[Fraction(int(round(t*10**6/v.max())),10**6) for t in v]
    best=None
    for lam in (Fraction(int(round(w[k].real*10**4)-1),10**4),):
        for den in (1,):
            Bv=[sum(Fraction(int(Bint[i,j]))*vq[j] for j in range(len(vq)) if Bint[i,j]) for i in range(len(vq))]
            # tight exact bound: min over rows with v_i>0 of (Bv)_i / v_i, which is rigorous by Collatz-Wielandt for the subvector supported where v>0 only if Bv>=lam v on all rows
            ratios=[Bv[i]/vq[i] for i in range(len(vq)) if vq[i]>0]
            lo=min(ratios) if ratios else Fraction(0)
    # restrict to support S={v>0}: submatrix B_S v_S >= lo v_S  => rho(B_S)>=lo => rho(B)>=lo
    sup=[i for i in range(len(vq)) if vq[i]>0]
    BS=[[Fraction(int(Bint[i,j])) for j in sup] for i in sup];vS=[vq[i] for i in sup]
    r=min(sum(BS[a][b]*vS[b] for b in range(len(sup)))/vS[a] for a in range(len(sup)))
    return r

def entropy_rows(ms):
    rows=[]
    for m in ms:
        x=2**m;B=blocks(x);F=set()
        for c in B.values(): F|=set(c)
        S,Bm=pair_matrix(F)
        lb=cw_lower_bound(Bm)
        Bf=np.array(Bm.tolist(),dtype=float);rho=max(abs(np.linalg.eigvals(Bf)))
        rows.append(dict(m=m,x=x,window_size=len(F),states=len(S),blocks=len(B),
            theorem_bound_h=math.log(m)/4,CW_certified_rho_lower=float(lb),CW_certified_h_lower=math.log(float(lb)) if lb>0 else None,
            rho_float=float(rho),h_float=math.log(rho),
            theorem_bound_rho=m**0.25,CW_exceeds_theorem_bound=bool(float(lb)>=m**0.25-1e-12)))
    return rows

def subsystem_exact(ms):
    """exact integer check of the conjugacy count: closed walks of length 4n through the block-start states >= m^n? Here: number of pair-state walks of length 4 from (x,4x) to (x,4x) in G equals tau(x) block count at minimum."""
    out=[]
    for m in ms:
        x=2**m;B=blocks(x);F=set()
        for c in B.values(): F|=set(c)
        S,Bm=pair_matrix(F);idx={s:i for i,s in enumerate(S)};s0=idx[(x,4*x)]
        P=np.identity(len(S),dtype=object)
        for _ in range(4): P=P.dot(Bm)
        out.append(dict(m=m,return_walks_len4=int(P[s0,s0]),blocks=len(B),at_least_blocks=int(P[s0,s0])>=len(B)))
    return out

def run():
    res={}
    res["E1_blocks_pow2"],bad=check_blocks([2**m for m in range(2,10)]);res["E1_pow2_bad"]=bad
    res["E1_blocks_all_x_le_200"],bad2=check_blocks(range(2,201));res["E1_all_bad"]=bad2
    res["example_x8"]={str(N):list(c) for N,c in blocks(8).items()}
    res["entropy_rows"]=entropy_rows(range(2,10))
    res["return_walks"]=subsystem_exact(range(2,10))
    res["passed"]=(bad==0 and bad2==0 and all(r["CW_exceeds_theorem_bound"] for r in res["entropy_rows"]) and all(r["at_least_blocks"] for r in res["return_walks"]))
    return res
if __name__=="__main__":
    r=run();json.dump(r,open(sys.argv[1],"w"),indent=1,default=str)
    print("passed",r["passed"]);[print(e) for e in r["entropy_rows"]];print(r["return_walks"]);print(r["example_x8"])

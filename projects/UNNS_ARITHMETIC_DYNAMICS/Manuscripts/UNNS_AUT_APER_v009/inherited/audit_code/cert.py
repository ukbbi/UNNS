"""Independent symbolic certificate for ADJ4 round map.
Method: for each family (a,rho), z=50000+rho+98t, the itinerary is a token list (plain moves / blocks W^T(t), T affine).
Every step's legality is proved for ALL integers t>=0 and 0<=k<T(t) by exact emptiness tests of 2-variable polyhedra
{ct*t+ck*k+c0>=0}, decided by vertex enumeration (the polyhedra are pointed because t>=0,k>=0 are always present;
a nonempty pointed polyhedron has a vertex = intersection of two boundary lines). Integer arithmetic only.
Rational emptiness implies integer emptiness, so every 'empty' verdict is sound for the integer problem."""
import json, sys
sys.path.insert(0,'.')
from spec import ORDER, REQ, DELTA

def nonempty_vertex(cons):
    """cons: list of (ct,ck,c0) meaning ct*t+ck*k+c0>=0. True iff polyhedron (assumed pointed) is nonempty."""
    n=len(cons)
    for i in range(n):
        ci=cons[i]
        for j in range(i+1,n):
            cj=cons[j]
            D=ci[0]*cj[1]-cj[0]*ci[1]
            if D==0: continue
            tn=-ci[2]*cj[1]+cj[2]*ci[1]; kn=-ci[0]*cj[2]+cj[0]*ci[2]
            ok=True
            if D>0:
                for c in cons:
                    if c[0]*tn+c[1]*kn+c[2]*D<0: ok=False;break
            else:
                for c in cons:
                    if c[0]*tn+c[1]*kn+c[2]*D>0: ok=False;break
            if ok: return True
    return False

class Aff:  # a + bt + ck  (state coordinate)
    __slots__=('a','b','c')
    def __init__(s,a=0,b=0,c=0): s.a=a;s.b=b;s.c=c
    def add(s,o): return Aff(s.a+o.a,s.b+o.b,s.c+o.c)
    def sub_const(s,r): return (s.b,s.c,s.a-r)   # constraint s>=r  ->  (ct,ck,c0)
def fit_tokens(a,rho,D):
    """tokens with affine counts from concrete runs at t=0..7"""
    ts=range(8); tok={t:D[f'{a},{rho},{t}']['tokens'] for t in ts}
    n=len(tok[0]); out=[]
    for i in range(n):
        k0=tok[0][i]
        for t in ts:
            assert tok[t][i][0]==k0[0] and (k0[0]=='P' and tok[t][i][1]==k0[1] or k0[0]=='B' and tok[t][i][2]==k0[2]),'shape'
        if k0[0]=='P': out.append(('P',k0[1]))
        else:
            c=[tok[t][i][1] for t in ts]; s=c[1]-c[0]
            assert all(c[t]==c[0]+s*t for t in ts),('nonaffine',a,rho,i,c)
            out.append(('B',tuple(k0[2]),c[0],s))
    return out

def certify(a,rho,toks,perturb=None):
    """returns dict with failures list and final-state data. perturb: optional (token_index, dT0) negative control."""
    z0=50000+rho
    v=[Aff(a),Aff(0),Aff(z0,98,0),Aff(0)]            # affine in t
    zt=(z0,98)                                          # z(t)
    fails=[]; ntests=0; steps_events=[]
    # flatten positions to know which is the last step
    tl=[]
    for i,t in enumerate(toks):
        if perturb and perturb[0]==i and t[0]=='B': t=('B',t[1],t[2]+perturb[1],t[3])
        tl.append(t)
    last_tok=len(tl)-1
    for ti,t in enumerate(tl):
        if t[0]=='P':
            word=(t[1],); T0=0; s=0; plain=True
        else:
            word=t[1]; T0=t[2]; s=t[3]; plain=False
        # word entries are indices into ORDER
        # per-position state at repetition k: v + k*dW + prefix
        dW=[0,0,0,0]
        for m in word:
            d=DELTA[ORDER[m]]
            for c in range(4): dW[c]+=d[c]
        base=[(x.a,x.b) for x in v]
        pref=[0,0,0,0]
        # domain constraints
        dom=[(1,0,0),(0,1,0)]                            # t>=0, k>=0
        if plain: dom.append((0,-1,0))                  # k<=0
        else: dom.append((s,-1,T0-1))                   # k<=T0-1+s*t
        for j,m in enumerate(word):
            N=ORDER[m]
            st=[Aff(base[c][0]+pref[c], base[c][1], dW[c]*(0 if plain else 1)) for c in range(4)]
            # (E) chosen move enabled
            for c in range(4):
                ntests+=1
                cons=dom+[(-st[c].b,-st[c].c,-st[c].a+REQ[N][c]-1)]   # state_c <= req-1
                if NONEMPTY(cons): fails.append(('E',ti,j,c))
            # (D) all higher-priority moves disabled
            for hm in range(m):
                Nh=ORDER[hm]; ntests+=1
                cons=dom+[(st[c].b,st[c].c,st[c].a-REQ[Nh][c]) for c in range(4)]
                if NONEMPTY(cons): fails.append(('D',ti,j,hm))
            # state after the step
            dm=DELTA[N]
            for c in range(4): pref[c]+=dm[c]
            post=[Aff(base[c][0]+pref[c], base[c][1], dW[c]*(0 if plain else 1)) for c in range(4)]
            is_final=(ti==last_tok and j==len(word)-1)   # final state of the very last token at last repetition handled below
            # (S) post-state is not in S with z''>=10 z, except the true final state (k=T-1 of last token, last position)
            if not (ti==last_tok and j==len(word)-1):
                ntests+=1
                cons=dom+[(-post[0].b,-post[0].c,-post[0].a+1),(-post[1].b,-post[1].c,-post[1].a),
                          (-post[3].b,-post[3].c,-post[3].a),(post[2].b-10*zt[1],post[2].c,post[2].a-10*zt[0])]
                if NONEMPTY(cons): fails.append(('S',ti,j))
            else:
                # last token last position: the same test must hold for k<=T-2 (every state before the final one)
                if not plain:
                    dom2=[(1,0,0),(0,1,0),(s,-1,T0-2)]
                    ntests+=1
                    cons=dom2+[(-post[0].b,-post[0].c,-post[0].a+1),(-post[1].b,-post[1].c,-post[1].a),
                          (-post[3].b,-post[3].c,-post[3].a),(post[2].b-10*zt[1],post[2].c,post[2].a-10*zt[0])]
                    if NONEMPTY(cons): fails.append(('S-last',ti,j))
        # advance state past the token
        T=(T0,s) if not plain else (1,0)
        for c in range(4):
            v[c]=Aff(v[c].a+dW[c]*T[0], v[c].b+dW[c]*T[1], 0)
        # counts must stay nonnegative for all t>=0
        if T[0]<0 or T[1]<0: fails.append(('T-neg',ti))
    return dict(fails=fails,ntests=ntests,final=[(x.a,x.b) for x in v])

def final_checks(a,rho,final):
    z0=50000+rho
    ok=True; msgs=[]
    (e2,e2t),(e3,e3t),(zz,zzt),(e7,e7t)=final[0],final[1],final[2],final[3]
    # v2,v3,v7 are constants and in the right set
    if not(e3==0 and e3t==0 and e7==0 and e7t==0 and e2t==0 and e2 in (0,1)): ok=False;msgs.append('end not in S-shape')
    # z'(t)=zz+zzt*t, must be >=10 z(t) for all t>=0
    if not (zz-10*z0>=0 and zzt-10*98>=0): ok=False;msgs.append('expansion z>=10z fails')
    return ok,msgs,(e2,zz,zzt)

NONEMPTY=nonempty_vertex

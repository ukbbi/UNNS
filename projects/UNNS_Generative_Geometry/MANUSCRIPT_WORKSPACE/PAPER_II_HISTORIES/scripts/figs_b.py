from figlib2 import *
from engine import *
from swaps import *
from topo import *
import math, itertools
HEX=[(14,3,2),(3,14,2),(3,2,14),(2,3,14),(2,14,3),(14,2,3)]
def hexpos(i,R=1.0,c=(0,0)): 
    a=math.pi/2+i*math.pi/3
    return (c[0]+R*math.cos(a),c[1]+R*math.sin(a))
def fig08():
    fig,axs=plt.subplots(1,3,figsize=(W,2.7))
    for ax,m,tg in zip(axs,(14,28,21),"abc"):
        clean(ax,(-1.9,1.9,-1.6,1.6))
        adm=[w for w in HEX if m%K(w)==0]
        for i in range(6):
            a,b=HEX[i],HEX[(i+1)%6]; ok=a in adm and b in adm
            seg(ax,hexpos(i),hexpos((i+1)%6),c=(KEEP if ok else GREY),lw=(2.2 if ok else 0.8),ls=("-" if ok else ":"))
        for i,w in enumerate(HEX):
            ok=w in adm; x,y=hexpos(i)
            node(ax,x,y,"",fc=(KEEP_L if ok else "white"),ec=(KEEP if ok else GREY),r=0.12,hatch=(None if ok else "///"),z=4)
            ax.text(x*1.42,y*1.22+(0.05 if y>0 else -0.05),f"$({','.join(map(str,w))})$\n$K={K(w)}$",ha="center",va="center",fontsize=5.8)
        from swaps import swap_classes
        panel(ax,tg,f"$m={m}$:  {len(swap_classes((2,3,14),m))} class(es)")
    DATA['fig08']={'hex':HEX,'K':{str(w):K(w) for w in HEX},'src14':{'h1':run(14,(14,3,2)),'h2':run(14,(2,3,14))}}
    fig.tight_layout(); save(fig,"fig08_same_content_two_components")
def fig09():
    cs=[(2,3,14),(2,3,5,6,7,15)]
    fig,axs=plt.subplots(1,2,figsize=(W,2.7),gridspec_kw={"width_ratios":[1,1.5]})
    for ax,c,tg in zip(axs,cs,"ab"):
        clean(ax); bl=sccs(c); E=feeding(c)
        bi={x:i for i,b in enumerate(bl) for x in b}
        # topological layers
        layer={}
        def lay(b):
            if b in layer: return layer[b]
            pr=[bi[a] for (a,bb) in E if bi[bb]==b and bi[a]!=b]
            layer[b]=0 if not pr else 1+max(lay(p) for p in set(pr)); return layer[b]
        for b in range(len(bl)): lay(b)
        cols={}
        for b in range(len(bl)): cols.setdefault(layer[b],[]).append(b)
        pos={}
        for l,bs in cols.items():
            y=0
            for b in bs:
                xs=bl[b]; k=len(xs)
                cx=l*2.4; cy=-y*2.0
                for j,x in enumerate(xs):
                    ang=2*math.pi*j/k+math.pi/2
                    pos[x]=(cx+(0.55*math.cos(ang) if k>1 else 0),cy+(0.55*math.sin(ang) if k>1 else 0))
                if k>1: ax.add_patch(Circle((cx,cy),0.95,fc="none",ec=SRC,lw=1,ls="--"))
                y+=1
        for x,(px,py) in pos.items(): node(ax,px,py,str(x),r=0.26,fs=7,fc=("white"))
        for a,b in E: arrow(ax,pos[a],pos[b],c=(SRC if bi[a]==bi[b] else LOST),lw=0.8,ls=("-" if bi[a]==bi[b] else "--"),rad=0.2,shrink=0.3)
        ax.autoscale_view(); ax.set_xlim(min(p[0] for p in pos.values())-1.2,max(p[0] for p in pos.values())+1.2); ax.set_ylim(min(p[1] for p in pos.values())-1.2,max(p[1] for p in pos.values())+1.2)
        panel(ax,tg,f"content {{{','.join(map(str,c))}}}: {len(bl)} block(s)")
        DATA.setdefault('fig09',{})[str(c)]={'blocks':bl,'edges':sorted(E)}
    axs[1].text(0.5,-0.02,"solid blue: inside a block;  dashed red: between blocks (feeder $\\to$ fed)",transform=axs[1].transAxes,ha="center",fontsize=6.3,va="top")
    fig.tight_layout(); save(fig,"fig09_feeding_blocks")
def fig10():
    fig,axs=plt.subplots(1,2,figsize=(W,2.7),gridspec_kw={"width_ratios":[1,1.4]})
    ax=axs[0]; clean(ax,(-1.9,1.9,-1.6,1.6))
    c=(2,3,8); arr=[(2,3,8),(3,2,8),(3,8,2),(8,3,2),(8,2,3),(2,8,3)]
    adm=[w for w in arr if 8%K(w)==0]
    for i in range(6):
        seg(ax,hexpos(i),hexpos((i+1)%6),c=GREY,lw=0.8,ls=":")
    for i,w in enumerate(arr):
        ok=w in adm; x,y=hexpos(i)
        node(ax,x,y,"",fc=(KEEP_L if ok else "white"),ec=(KEEP if ok else GREY),r=0.13,hatch=(None if ok else "///"),z=4)
        ax.text(x*1.4,y*1.22,f"$({','.join(map(str,w))})$\n$K={K(w)}$",ha="center",va="center",fontsize=6)
    seg(ax,hexpos(0),hexpos(3),c=WIT,lw=0.9,ls="--",z=1)
    ax.text(0,0,"antipodal",fontsize=6,ha="center",color=WIT,rotation=0,bbox=dict(fc="white",ec="none",pad=0.3))
    panel(ax,"a","$\\{2,3,8\\}$ at $m=8$: 2 classes")
    ax=axs[1]
    Ns=list(range(4,43)); sp=[(N%6 in (2,3) and N>=8) for N in Ns]
    ax.set_xlim(3.4,42.6); ax.set_ylim(-1,2)
    for N,s in zip(Ns,sp):
        ax.add_patch(Rectangle((N-0.45,0.1),0.9,0.8,fc=(KEEP_L if s else "white"),ec=(KEEP if s else GREY),hatch=(None if s else "///"),lw=0.6))
        ax.text(N,0.5,str(N),ha="center",va="center",fontsize=5.2,rotation=90)
        ax.text(N,-0.2,str(N%6),ha="center",va="center",fontsize=5.5)
    ax.text(3.6,-0.8,"second row: $N$ mod 6",fontsize=6); ax.axis("off")
    panel(ax,"b","$\\{2,3,N\\}$ has a split source iff $N\\equiv2,3\\ (6)$, $N\\geq8$")
    DATA['fig10']={'adm_at_8':[list(w) for w in adm],'K':{str(w):K(w) for w in arr},'split_N_le_42':[N for N,s in zip(Ns,sp) if s]}
    fig.tight_layout(); save(fig,"fig10_three_label_split")
def fig11():
    c=(2,3,8,9); m=72
    def kap(S):
        ps=set()
        for x in S: ps|=set(primes_of(x))|set(primes_of(x+1))
        k=1
        for p in ps:
            d=sum(delta(x,p) for x in S)
            if d<0:k*=p**(-d)
        return k
    fig,ax=plt.subplots(figsize=(W,3.2)); clean(ax,(-0.5,10.5,-0.9,4.9))
    levels={0:[()],1:list(itertools.combinations(c,1)),2:list(itertools.combinations(c,2)),3:list(itertools.combinations(c,3)),4:[c]}
    pos={}
    for l,Ss in levels.items():
        n=len(Ss)
        for i,S in enumerate(Ss): pos[S]=(10*(i+0.5)/n,4.2-l*1.0)
    infe={S for S in pos if S and S!=c and m%kap(S)!=0}
    for S in pos:
        for x in c:
            if x not in S:
                T=tuple(sorted(S+(x,)))
                seg(ax,pos[S],pos[T],c=(GREY if (S in infe or T in infe) else SRC),lw=(0.6 if (S in infe or T in infe) else 1.0),ls=(":" if (S in infe or T in infe) else "-"),z=1)
    for S,(x,y) in pos.items():
        bad=S in infe
        box(ax,x-0.5,y-0.2,1.0,0.4,"$\\{"+",".join(map(str,S))+"\\}$" if S else "$\\emptyset$",fc=(UNC if bad else "white"),ec=(UNC_E if bad else SRC),fs=6.5,hatch=("//" if bad else None),z=4)
    # count chains
    chains=len([w for w in permutations(c) if m%K(w)==0])
    ax.text(5,-0.6,f"Infeasible proper subsets at $m=72$: $\\{{2,8\\}}$ and $\\{{3,9\\}}$ (hatched). Maximal chains avoiding them = admissible arrangements: {chains} of 24.",ha="center",fontsize=6.6)
    DATA['fig11']={'infeasible':[list(S) for S in infe],'admissible_arrangements':chains}
    save(fig,"fig11_feasible_subsets")
def perm_coords(w,labs):
    pos=[w.index(l) for l in labs]; return pos
def fig12():
    c=(2,3,8,9); m=72; labs=sorted(c)
    allw=list(permutations(labs)); adm=set(w for w in allw if m%K(w)==0)
    # basis for projection of the 3-dim permutohedron in R^4 (sum-zero): isometric-like
    B=np.array([[1,-1,0,0],[0.5,0.5,-1,0],[0.3,0.3,0.3,-0.9]],float)
    def P3(w):
        p=np.array(perm_coords(w,labs),float)-1.5
        return B@p
    R=np.array([[0.88,0.15,-0.45],[-0.12,0.98,0.2]])  # 3->2 projection
    # tilt
    def P2(w): return R@P3(w)
    # faces: ordered partitions with 2 blocks
    faces=[];
    for op in ordered_partitions(4):
        if len(op)==2:
            verts=[tuple(labs[i] for i in v) for v in linear_exts(op)]
            faces.append((op,verts,all(v in adm for v in verts)))
    fig,axs=plt.subplots(1,2,figsize=(W,3.3))
    for ax,view in zip(axs,("front","back")):
        clean(ax)
        Rm=R if view=="front" else np.array([[-0.88,0.15,0.45],[-0.12,0.98,-0.2]])
        P=lambda w: Rm@P3(w)
        # draw faces
        for op,verts,ok in faces:
            pts=np.array([P(v) for v in verts]); ctr=pts.mean(0); ang=np.arctan2(pts[:,1]-ctr[1],pts[:,0]-ctr[0]); pts=pts[np.argsort(ang)]
            if ok: ax.add_patch(Polygon(pts,fc=KEEP_L,ec="none",alpha=0.65,zorder=1))
        for w in allw:
            for i in range(3):
                v=w[:i]+(w[i+1],w[i])+w[i+2:]
                if w<v:
                    both=(w in adm and v in adm)
                    p,q=P(w),P(v)
                    ax.plot([p[0],q[0]],[p[1],q[1]],color=(SRC if both else "#cfcfcf"),lw=(1.4 if both else 0.5),ls=("-" if both else ":"),zorder=2)
        for w in allw:
            p=P(w); ok=w in adm
            ax.plot([p[0]],[p[1]],marker="o",ms=(4.2 if ok else 3),mfc=(SRC if ok else "white"),mec=(SRC if ok else "#9a9a9a"),zorder=3)
        ax.autoscale_view(); ax.set_aspect("equal")
        panel(ax,"ab"[view=="back"],f"projection, {view} view")
    cells=perm_complex(c,m)
    DATA['fig12']={'f':cells[0],'betti':cells[1],'admissible':[list(w) for w in sorted(adm)],'filled_2cells':sum(1 for f in faces if f[2])}
    fig.suptitle("Permutohedral complex of $\\{2,3,8,9\\}$ at $m=72$ (projection of the 3-dimensional permutohedron): filled dots admissible, green faces filled, $\\beta_1=1$",fontsize=6.8,y=0.03)
    save(fig,"fig12_four_label_H1")
def fig13():
    c=(2,3,8,9,14); m=1008
    pf,pb=perm_complex(c,m); cf,cb=cubical_complex(c,m)
    fig,axs=plt.subplots(1,3,figsize=(W,2.5))
    ax=axs[0]; x=np.arange(4)
    ax.bar(x-0.2,pf,0.4,color=SRC_L,ec=SRC,label="permutohedral"); ax.bar(x[:len(cf)]+0.2,cf,0.4,color=TGT_L,ec=TGT,hatch="//",label="cubical")
    ax.set_xticks(x); ax.set_xticklabels(["$f_0$","$f_1$","$f_2$","$f_3$"]); ax.set_yscale("log"); ax.legend(frameon=False,fontsize=6); panel(ax,"a","face counts")
    ax=axs[1]; x=np.arange(5); pb2=pb+[0]*(5-len(pb)); cb2=cb+[0]*(5-len(cb))
    ax.bar(x-0.2,pb2,0.4,color=SRC_L,ec=SRC); ax.bar(x+0.2,cb2,0.4,color=TGT_L,ec=TGT,hatch="//")
    for i,(a,b) in enumerate(zip(pb2,cb2)):
        ax.text(i-0.2,a+0.4,str(a),ha="center",fontsize=6); ax.text(i+0.2,b+0.4,str(b),ha="center",fontsize=6)
    ax.set_xticks(x); ax.set_xticklabels([f"$\\beta_{i}$" for i in x]); panel(ax,"b","GF(2) Betti numbers")
    ax=axs[2]; clean(ax,(-2.2,2.2,-1.6,1.6))
    labs=sorted(c); Rr=[w for w in permutations(labs) if m%K(w)!=0]
    ns=nerve_sizes=None
    pre={}
    for w in Rr:
        for j in range(1,5): pre.setdefault(frozenset(w[:j]),[]).append(w)
    par={w:w for w in Rr}
    def f(x):
        while par[x]!=x: par[x]=par[par[x]];x=par[x]
        return x
    for ws in pre.values():
        for y in ws[1:]: par[f(y)]=f(ws[0])
    comp={}
    for w in Rr: comp.setdefault(f(w),[]).append(w)
    sizes=sorted(len(v) for v in comp.values())
    for i,s in enumerate(sizes):
        cx=-1.1+2.2*i
        ax.add_patch(Circle((cx,0.1),0.8,fc=(UNC if i==0 else "white"),ec=UNC_E,lw=1,hatch=("//" if i==0 else "\\\\")))
        ax.text(cx,0.1,f"{s}\narrangements",ha="center",va="center",fontsize=6.5)
    ax.text(0,-1.3,"$\\mathcal{N}(R)$: two components\n(facets $E|O$ and $O|E$)",ha="center",fontsize=6.5)
    panel(ax,"c","non-admissible set")
    DATA['fig13']={'perm_f':pf,'perm_betti':pb,'cub_f':cf,'cub_betti':cb,'nerve_components':sizes}
    fig.tight_layout(); save(fig,"fig13_five_label_H2")
def fig14():
    # witness: history in 72^3 with 4 pairwise non-overlapping legal swaps
    hs=histories(72**3); hset=set(hs); best=None
    for (s,w) in hs:
        legal=[i for i in range(len(w)-1) if w[i]!=w[i+1] and (s,w[:i]+(w[i+1],w[i])+w[i+2:]) in hset]
        ch=[];last=-5
        for i in legal:
            if i>last+1: ch.append(i);last=i
        if len(ch)==4: best=(s,w,ch);break
    s,w,ch=best
    fig,axs=plt.subplots(1,2,figsize=(W,3.0),gridspec_kw={"width_ratios":[1.15,1]})
    ax=axs[0]; clean(ax,(-2.4,3.4,-2.6,2.6))
    # tesseract projection
    gens=[np.array(v) for v in ((1.5,0.0),(0.0,1.5),(0.8,0.5),(-0.5,0.9))]
    def P(b): return sum((b[k]*gens[k] for k in range(4)),np.zeros(2))
    verts=list(itertools.product((0,1),repeat=4))
    for a in verts:
        for k in range(4):
            if a[k]==0:
                b=list(a);b[k]=1
                p,q=P(a),P(b); ax.plot([p[0],q[0]],[p[1],q[1]],color=[SRC,TGT,KEEP,LOST][k],ls=["-","--","-.",":"][k],lw=1.1,zorder=1)
    for a in verts: node(ax,*P(a),"",r=0.07,fc="white",z=4)
    ax.text(0.5,-2.35,"edge style = which swap ($s_1,\\ldots,s_4$)",ha="center",fontsize=6.3)
    panel(ax,"a","4-cube of commuting swaps (a projection)")
    ax=axs[1]; ax.axis("off"); ax.set_xlim(0,1);ax.set_ylim(0,1)
    rows=[("$r$","1","2","3","4"),("histories","4","100","3,601","194,864"),("swap classes","3","22","142","1,114"),("max cube dim.","1","2","4","5")]
    for i,row in enumerate(rows):
        for j,t in enumerate(row):
            ax.text([0.0,0.46,0.62,0.78,0.94][j],0.92-i*0.12,t,fontsize=6.5,fontweight=("bold" if i==0 else "normal"),ha=("left" if j==0 else "right"))
    ax.text(0.04,0.38,"finite-exact for $72^r$, $r\\leq4$.\nWitness for $r=3$, cube dim. 4:\n$m_0="+str(s)+"$,\n$w=("+",".join(map(str,w))+")$\nswap positions "+str([i+1 for i in ch]),fontsize=6.3,va="top")
    panel(ax,"b","finite-exact table")
    DATA['fig14']={'witness':{'source':s,'word':list(w),'positions':ch},'table':rows}
    fig.tight_layout(); save(fig,"fig14_commuting_swaps")
if __name__=="__main__":
    for f in (fig08,fig09,fig10,fig11,fig12,fig13,fig14): f()
    import json; D=json.load(open(os.path.join(OUT,'..','results','FIGURE_DATA.json'))); D.update(DATA); json.dump(D,open(os.path.join(OUT,'..','results','FIGURE_DATA.json'),'w'),indent=1,default=str)

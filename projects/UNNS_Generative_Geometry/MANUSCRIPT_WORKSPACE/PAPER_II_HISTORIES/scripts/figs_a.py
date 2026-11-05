from figlib2 import *
from engine import *
from swaps import *
from math import comb
import math
# ---------------- Fig 1: objects and equivalence relations (endpoint 72)
def fig01():
    hs=sorted(histories(72))
    fig,ax=plt.subplots(figsize=(W,3.1))
    clean(ax,(0,12.4,0,6.4))
    cols=[("state",0.2),("history",2.5),("content",5.6),("swap class",8.1),("endpoint",10.6)]
    for t,x in cols: ax.text(x+0.9,6.1,t,ha="center",fontsize=8,fontweight="bold")
    # four histories
    ys={(1,(1,1,2)):4.7,(1,(1,2,1)):3.6,(3,(3,2)):2.3,(10,(5,)):1.1}
    for (s,w),y in ys.items():
        box(ax,2.5,y-0.35,2.6,0.7,f"$m_0={s}$;  $w=({','.join(map(str,w))})$",fc=SRC_L,ec=SRC,fs=7)
        box(ax,0.2,y-0.35,1.6,0.7,"$"+"\\to".join(map(str,run(s,w)))+"$",fc="white",ec=GREY,fs=6.3,ls="--")
        seg(ax,(1.8,y),(2.5,y),c=GREY,ls="--")
    cont={(1,1,2):(4.15,[ (1,(1,1,2)),(1,(1,2,1))]),(2,3):(2.3,[(3,(3,2))]),(5,):(1.1,[(10,(5,))])}
    for c,(y,hl) in cont.items():
        box(ax,5.6,y-0.35,1.8,0.7,"$\\{"+",".join(map(str,c))+"\\}$",fc="white",ec=TGT,fs=7.5,ls="--")
        for h in hl: seg(ax,(5.1,ys[h]),(5.6,y),c=TGT,ls="--")
    swp=[("$[ (1,1,2)\\sim(1,2,1) ]$",4.15),("$[ (3,2) ]$",2.3),("$[ (5) ]$",1.1)]
    for t,y in swp:
        box(ax,8.1,y-0.35,2.0,0.7,t,fc=KEEP_L,ec=KEEP,fs=6.8)
    for c,(y,hl) in cont.items(): seg(ax,(7.4,y),(8.1,y),c=KEEP)
    box(ax,10.6,2.15,1.5,0.7,"$72$",fc=UNC,ec=UNC_E,fs=9,hatch="//")
    for t,y in swp: seg(ax,(10.1,y),(10.6,2.5),c=GREY,ls=":")
    ax.text(6.2,0.35,"Same endpoint 72, three contents, three swap classes, four histories (exact; $H(72)=4$).\n"
            "Solid green: swap relation (adjacent exchange of distinct labels). Dashed teal: content map. Dotted: endpoint map.",ha="center",fontsize=6.5)
    DATA['fig01']={'endpoint':72,'histories':[(s,list(w),run(s,w)) for s,w in hs]}
    save(fig,"fig01_objects")
# ---------------- Fig 2: the four histories to 72
def fig02():
    fig,ax=plt.subplots(figsize=(W,2.6)); clean(ax,(-0.4,10.4,-0.3,5.1))
    pos={1:(0.4,3.2),4:(2.6,3.2),16:(5.0,3.2),18:(5.0,4.5),3:(2.6,1.2),10:(5.0,0.2),72:(8.4,2.2)}
    for k,(x,y) in pos.items(): node(ax,x,y,str(k),fc=(UNC if k==72 else "white"),r=0.38,hatch=("//" if k==72 else None),fs=8)
    E=[(1,4,"1",SRC,"-",0),(4,16,"1",SRC,"-",0),(16,72,"2",SRC,"-",0),(4,18,"2",TGT,"--",0),(18,72,"1",TGT,"--",0),(3,16,"3",KEEP,"-.",0),(10,72,"5",LOST,":",0)]
    for a,b,l,c,ls,r in E: arrow(ax,pos[a],pos[b],f"$N={l}$",c=c,ls=ls,lw=1.2,rad=r,shrink=0.45,off=(0,0.22))
    ax.text(7.2,-0.2,"1$\\to$4$\\to$16$\\to$72  (solid blue)\n1$\\to$4$\\to$18$\\to$72  (dashed teal)\n3$\\to$16$\\to$72  (dash-dot green)\n10$\\to$72  (dotted red)",fontsize=6.8,va="bottom",ha="left")
    ax.text(5.0,-0.1,"",fontsize=6)
    DATA['fig02']={'edges':[(a,b,l) for a,b,l,*_ in E]}
    save(fig,"fig02_four_histories_72")
# ---------------- Fig 3: predecessor graph and count recursion
def fig03():
    nodes=set();E=[]
    def go(t):
        if t in nodes: return
        nodes.add(t)
        for d,s in pred(t): E.append((s,t,d-1)); go(s)
    go(72)
    levels={}
    def depth(t):
        ds=[depth(s) for d,s in pred(t)]
        return 0 if not ds else 1+max(ds)
    for t in nodes: levels.setdefault(depth(t),[]).append(t)
    fig,ax=plt.subplots(figsize=(W,3.0)); clean(ax,(-0.5,8.5,-0.5,4.6))
    pos={}
    for d,ts in levels.items():
        ts=sorted(ts)
        for i,t in enumerate(ts): pos[t]=(d*2.1,(i+0.5)*3.8/len(ts)+0.15 if len(ts)>1 else 1.9)
    # depth measured toward sources: reverse x so 72 is at the right
    mx=max(levels)
    pos={t:((mx-depth(t))*2.1+0.4 if False else pos[t][0],pos[t][1]) for t in pos}
    for t,(x,y) in pos.items(): node(ax,x,y,str(t),fc=(UNC if t==72 else ("white")),hatch=("//" if t==72 else None),r=0.34,fs=7.5)
    for s,t,N in E: arrow(ax,pos[s],pos[t],f"{N}",c=SRC,lw=0.9,off=(0,0.13),ts=6)
    for t,(x,y) in pos.items(): ax.text(x,y-0.52,f"$H={H(t)}$",ha="center",fontsize=6.3,color=TGT)
    ax.text(8.0,4.3,"$H(t)=\\sum_{d\\geq2,\\ d^2\\mid t}H\\left(\\frac{t(d-1)}{d^{2}}\\right)$; $H=1$ for squarefree $t$",ha="right",fontsize=7)
    DATA['fig03']={'nodes':sorted(nodes),'H':{str(t):H(t) for t in nodes},'edges':sorted(E)}
    save(fig,"fig03_predecessor_graph")
# ---------------- Fig 4: growth
def fig04():
    r=list(range(1,7)); h=[H(72**x) for x in r]; lb=[comb(2*x,x) for x in r]
    fig,axs=plt.subplots(1,2,figsize=(W,2.5))
    ax=axs[0]; ax.semilogy(r,h,"o-",color=SRC,label="$H(72^r)$ (finite-exact)"); ax.semilogy(r,lb,"s--",color=LOST,mfc="white",label="$\\binom{2r}{r}$ (proved lower bound)")
    for x,y in zip(r,h): ax.annotate(f"{y:,}",(x,y),textcoords="offset points",xytext=(-3,5),fontsize=5.8,ha="right")
    ax.set_xlabel("$r$"); ax.set_ylabel("count"); ax.legend(loc="upper left",frameon=False,fontsize=6.3); panel(ax,"a","counts and bound")
    ax=axs[1]; ax.plot(r,[a/b for a,b in zip(h,lb)],"o-",color=TGT); ax.set_yscale("log"); ax.set_xlabel("$r$"); ax.set_ylabel("$H(72^r)/\\binom{2r}{r}$"); panel(ax,"b","excess over the bound")
    DATA['fig04']={'r':r,'H':h,'binom':lb}
    fig.tight_layout(); save(fig,"fig04_growth")
# ---------------- Fig 5: valuation trajectories
def fig05():
    fig,axs=plt.subplots(1,3,figsize=(W,2.5),sharey=True)
    words=[(2,3,14),(14,3,2),(3,14,2)]
    sty={2:("o","-",SRC),3:("s","--",TGT),7:("^",":",LOST)}
    for ax,w in zip(axs,words):
        for p,(mk,ls,c) in sty.items():
            s=0;tr=[0]
            for N in w: s+=delta(N,p);tr.append(s)
            ax.plot(range(len(tr)),tr,marker=mk,ls=ls,color=c,label=f"$p={p}$",ms=4)
        ax.axhline(0,color="k",lw=0.5)
        ax.set_xticks(range(4)); ax.set_xticklabels(["0"]+[f"${N}$" for N in w])
        ax.set_title(f"$w=({','.join(map(str,w))})$,  $K(w)={K(w)}$",fontsize=7.5)
        ax.set_xlabel("step label")
        DATA.setdefault('fig05',{})[str(w)]={'K':K(w),'S':{p:[sum(delta(N,p) for N in w[:j]) for j in range(4)] for p in (2,3,7)}}
    axs[0].set_ylabel("$S_j(p)=\\sum_{i\\leq j}\\Delta_p(N_i)$"); h,l=axs[0].get_legend_handles_labels(); fig.legend(h,l,loc="lower center",ncol=3,frameon=False,bbox_to_anchor=(0.5,-0.06))
    fig.tight_layout(); save(fig,"fig05_valuation_trajectories")
# ---------------- Fig 6: content-level vs order-level
def fig06():
    arr=arrangements((2,3,14)); srcs=[7,14,21,28,42,84,70]
    fig,ax=plt.subplots(figsize=(W,2.9))
    ax.set_xlim(-0.6,len(srcs)-0.4); ax.set_ylim(-0.6,len(arr)-0.4); ax.invert_yaxis()
    for i,w in enumerate(arr):
        for j,m in enumerate(srcs):
            ok=m%K(w)==0
            ax.add_patch(Rectangle((j-0.45,i-0.4),0.9,0.8,fc=(KEEP_L if ok else "white"),ec=(KEEP if ok else GREY),lw=0.8,hatch=(None if ok else "///")))
            ax.text(j,i,"adm." if ok else "no",ha="center",va="center",fontsize=6.3,fontweight=("bold" if ok else "normal"))
    ax.set_xticks(range(len(srcs))); ax.set_xticklabels([f"$m={m}$" for m in srcs])
    ax.set_yticks(range(len(arr))); ax.set_yticklabels([f"$({','.join(map(str,w))})$,  $K={K(w)}$" for w in arr],fontsize=6.8)
    ax.set_title("Content $\\{2,3,14\\}$: order-level admissibility ($K(w)\\mid m$) differs from content-level data",fontsize=7.5)
    ax.tick_params(length=0)
    for s in ax.spines.values(): s.set_visible(False)
    DATA['fig06']={'K':{str(w):K(w) for w in arr},'sources':srcs}
    fig.tight_layout(); save(fig,"fig06_content_vs_order")
# ---------------- Fig 7: legal and forbidden swap diamonds
def fig07():
    fig,axs=plt.subplots(1,3,figsize=(W,2.5))
    def diamond(ax,x,A,B,ttl,tag_):
        clean(ax,(-2.1,2.1,-0.6,3.0))
        top=(0,0);L=(-1.2,1.3);Rr=(1.2,1.3);bot=(0,2.6)
        s0=x;sA=run(x,(A,)) ;sB=run(x,(B,))
        nodes={'top':(top,str(x),True),'L':(L,str(sA[-1]) if sA else "—",sA is not None),'R':(Rr,str(sB[-1]) if sB else "—",sB is not None)}
        okAB=run(x,(A,B)) is not None; okBA=run(x,(B,A)) is not None
        end=run(x,(A,B))[-1] if okAB else (run(x,(B,A))[-1] if okBA else None)
        for k,(p,t,ok) in nodes.items(): node(ax,p[0],p[1],t,fc=("white" if ok else UNC),r=0.33,hatch=(None if ok else "//"),fs=7)
        node(ax,bot[0],bot[1],str(end) if end else "—",fc=("white" if (okAB and okBA) else UNC),r=0.33,fs=7,hatch=(None if end else "//"))
        arrow(ax,top,L,f"{A}",c=SRC,off=(-0.22,0.05),shrink=0.4,lw=1.1,ls=("-" if sA else ":")); arrow(ax,top,Rr,f"{B}",c=TGT,ls=("--" if sB else ":"),off=(0.22,0.05),shrink=0.4,lw=1.1)
        arrow(ax,L,bot,f"{B}",c=TGT,ls=("--" if okAB else ":"),off=(-0.22,-0.05),shrink=0.4,lw=1.1); arrow(ax,Rr,bot,f"{A}",c=SRC,ls=("-" if okBA else ":"),off=(0.22,-0.05),shrink=0.4,lw=1.1)
        panel(ax,tag_,ttl)
        return okAB,okBA
    d1=diamond(axs[0],6,2,3,"$A=2,B=3,x=6$: $AB\\mid x$","a")
    d2=diamond(axs[1],2,2,3,"$x=2$: $AB\\nmid x$","b")
    d3=diamond(axs[2],14,2,14,"$A=2,B=14,x=14$","c")
    DATA['fig07']={'a':d1,'b':d2,'c':d3,'note':'dotted/orange: step not admissible'}
    fig.tight_layout(); save(fig,"fig07_swap_diamonds")
if __name__=="__main__":
    for f in (fig01,fig02,fig03,fig04,fig05,fig06,fig07): f()
    finish("a")

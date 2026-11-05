from figlib2 import *
from engine import *
from swaps import *
from topo import *
from rewrite import *
import json, itertools, math
RJ=json.load(open(os.path.join(HERE,'..','results','RESULTS_II_part2.json')))
def fig15():
    ob=RJ['irreducible']
    fig,axs=plt.subplots(1,4,figsize=(W,2.5))
    items=[("(2, 3, 4, 5, 6)@4","components"),("(2, 3, 4, 5, 6, 7)@4","components"),("(2, 3, 4, 5, 8)@32","$\\beta_1$"),("(2, 3, 4, 5, 6, 7)@24","$\\beta_1$")]
    for ax,(key,lab),tg in zip(axs,items,"abcd"):
        d=ob[key]; base=d['comps'] if 'comps' in d else d['betti'][1]
        ps=list(d['relax'].keys())
        vals=[(v if 'comps' in d else v[1]) for v in d['relax'].values()]
        ax.bar(["none"]+ps,[base]+vals,color=[LOST_L]+[(KEEP_L if v<base else "white") for v in vals],ec=[LOST]+[(KEEP if v<base else GREY) for v in vals],hatch=None)
        for i,(p,v) in enumerate(zip(["none"]+ps,[base]+vals)): ax.text(i,v+0.04,str(v),ha="center",fontsize=6.5)
        ax.set_ylim(0,max(base,1)*1.35+0.2); ax.set_yticks(range(0,int(max(base,1))+2)); ax.set_xlabel("prime relaxed")
        c,m=key.split("@")
        ax.set_title(f"$\\{{{c.strip('()').replace(' ','')}\\}}$, $m={m}$",fontsize=6.3)
        ax.set_ylabel(lab,fontsize=7)
    DATA['fig15']=ob
    fig.tight_layout(); save(fig,"fig15_irreducible_obstructions")
def fig16():
    V=RJ['kernel']['V']
    fig,axs=plt.subplots(1,2,figsize=(W,2.3),gridspec_kw={"width_ratios":[1.2,1]})
    ax=axs[0]; ax.axis("off"); ax.set_xlim(0,10); ax.set_ylim(0,5)
    ax.text(5,4.7,"$V_A=\\left(\\Delta_p(N_j)\\right)$,  rows $p=2,3$;  columns $N=1,2,3$",ha="center",fontsize=7)
    for i,row in enumerate(V):
        for j,x in enumerate(row):
            ax.add_patch(Rectangle((1.5+j*2.2,2.7-i*1.2),2.0,1.0,fc=("white" if x>=0 else LOST_L),ec="k",lw=0.7,hatch=("//" if x<0 else None)))
            ax.text(2.5+j*2.2,3.2-i*1.2,str(x),ha="center",va="center",fontsize=9)
    for i,p in enumerate((2,3)): ax.text(1.1,3.2-i*1.2,f"$p={p}$",ha="right",va="center",fontsize=7)
    ax.text(5,0.8,"$V_A\\,(7,-2,-4)^{\\mathsf{T}}=(0,0)^{\\mathsf{T}}$,   $\\ker_{\\mathbb{Z}}V_A=\\mathbb{Z}(7,-2,-4)$",ha="center",fontsize=7)
    panel(ax,"a","valuation matrix (hatched: negative entries)")
    ax=axs[1]; ax.axis("off"); ax.set_xlim(0,10); ax.set_ylim(0,5)
    ax.text(5,4.1,"$R(1)^7=R(2)^2R(3)^4=4^7$",ha="center",fontsize=8)
    ax.text(5,3.0,"$R(1)=4,\\ R(2)=\\frac{9}{2},\\ R(3)=\\frac{16}{3}$",ha="center",fontsize=7)
    ax.text(5,1.9,"$(\\frac{9}{2})^2(\\frac{16}{3})^4=\\frac{81}{4}\\cdot\\frac{65536}{81}=16384$",ha="center",fontsize=7)
    ax.text(5,0.7,"source 4 $\\to$ endpoint 65536",ha="center",fontsize=7.5)
    panel(ax,"b","the multiplier identity")
    DATA['fig16']={'V':V,'kernel':[7,-2,-4]}
    fig.tight_layout(); save(fig,"fig16_valuation_kernel")
def fig17():
    K_=RJ['kernel']; h1=K_['h1']; arr=K_['all_adm_2234']
    fig,axs=plt.subplots(1,2,figsize=(W,2.7),gridspec_kw={"width_ratios":[1.3,1]})
    ax=axs[0]
    ax.plot(range(8),[math.log2(x) for x in h1],"o-",color=SRC,label="$1^7$ (7 steps)",ms=4)
    sty=[("s","--",TGT),("^","-.",KEEP),("v",":",LOST)]
    for w,(mk,ls,c) in zip(arr,sty):
        st=run(4,tuple(w)); ax.plot(range(7),[math.log2(x) for x in st],marker=mk,ls=ls,color=c,ms=4,label="$("+",".join(map(str,w))+")$")
    ax.set_xlabel("step"); ax.set_ylabel("$\\log_2$ of the state"); ax.legend(frameon=False,fontsize=5.8,loc="upper left"); panel(ax,"a","two contents, one endpoint $65536=2^{16}$")
    ax=axs[1]; ax.axis("off"); ax.set_xlim(0,10); ax.set_ylim(0,10)
    y=9.2
    ax.text(0,y,"$1^7$:",fontsize=6.5,fontweight="bold"); ax.text(0.8,y,"$"+"\\!\\to\\!".join(map(str,h1))+"$",fontsize=5.6); y-=1.6
    for w in arr:
        st=run(4,tuple(w)); ax.text(0,y,"$("+",".join(map(str,w))+")$:",fontsize=6.2,fontweight="bold"); y-=0.9
        ax.text(0.3,y,"$"+"\\!\\to\\!".join(map(str,st))+"$",fontsize=5.6); y-=1.4
    ax.text(0,0.2,"$K(1^7)=1$, minimal $K$ of the other content $=2$",fontsize=6)
    DATA['fig17']={'h1':h1,'h2':arr,'states':[run(4,tuple(w)) for w in arr]}
    fig.tight_layout(); save(fig,"fig17_two_contents_65536")
def fig18():
    fig,axs=plt.subplots(1,2,figsize=(W,2.7),gridspec_kw={"width_ratios":[1.1,1]})
    j=3; U=(2,)*4+(3,)*j; V=(1,8,8)+(3,)*j
    ax=axs[0]
    tab={}
    for a in range(0,7):
        for b in range(0,j+1):
            m=2**a*3**b
            if adm_perms(U,m) and adm_perms(V,m):
                c,_=space_components(m,[U,V],[((2,2,2,2),(1,8,8))]); tab[(a,b)]=c
            else: tab[(a,b)]=0
    for (a,b),c in tab.items():
        fc={0:"white",1:KEEP_L,2:LOST_L}[c]; ec={0:GREY,1:KEEP,2:LOST}[c]
        ax.add_patch(Rectangle((a-0.45,b-0.45),0.9,0.9,fc=fc,ec=ec,lw=0.8,hatch=("xx" if c==0 else ("//" if c==2 else None))))
        ax.text(a,b,{0:"–",1:"1",2:"2"}[c],ha="center",va="center",fontsize=7)
    ax.set_xlim(-0.6,6.6); ax.set_ylim(-0.6,j+0.6); ax.set_xticks(range(7)); ax.set_yticks(range(j+1))
    ax.set_xlabel("$a=v_2(m)$"); ax.set_ylabel("$b=v_3(m)$"); panel(ax,"a",f"$j={j}$: components of the swap-and-rewrite space")
    ax=axs[1]; ax.axis("off"); ax.set_xlim(0,10); ax.set_ylim(0,10)
    ax.text(0,9,"$2^4\\,3^j\\ \\leftrightarrow\\ 1\\cdot8^2\\,3^j$",fontsize=8)
    ax.text(0,7.6,"connected iff $b\\geq1$ or $a\\geq4$;",fontsize=7)
    ax.text(0,6.6,"otherwise two components,",fontsize=7)
    ax.text(0,5.6,"one swap class per content.",fontsize=7)
    ax.text(0,4.0,"saturation bound: $P(C)=2^6\\,3^j$",fontsize=7)
    ax.text(0,3.0,"true exposure threshold: $2^4$ or $3$",fontsize=7)
    ax.text(0,1.4,"cells: “–” content not realisable; 1/2 = #components.\nChecked here for $j\\leq6$ (183 cases);\nproved for all $j$ (B-T9).",fontsize=6)
    panel(ax,"b","the family $F_j$")
    DATA['fig18']={'j':j,'table':{f"{a},{b}":c for (a,b),c in tab.items()}}
    fig.tight_layout(); save(fig,"fig18_rewrite_exposure")
def fig19():
    fam=RJ['R3T3']
    fig,axs=plt.subplots(1,2,figsize=(W,3.0),gridspec_kw={"width_ratios":[1.5,1]})
    ax=axs[0]; ax.axis("off")
    c=(2,4,5,9)
    cl=swap_classes(c,4)
    y=0
    ax.set_xlim(-0.5,5.5); ax.set_ylim(-5,1)
    for k,comp in enumerate(cl):
        ax.text(-0.45,y-0.1,f"component {k+1}  ($I={int(comp[0].index(2)<comp[0].index(4))}$)",fontsize=6.8,fontweight="bold"); y-=0.55
        for w in comp:
            for i,N in enumerate(w):
                hi=N in (2,4)
                ax.add_patch(Rectangle((i*0.9,y-0.22),0.8,0.44,fc=(SRC_L if N==2 else (TGT_L if N==4 else "white")),ec=(SRC if N==2 else (TGT if N==4 else GREY)),hatch=(None if N!=4 else "//"),lw=0.8))
                ax.text(i*0.9+0.4,y,str(N),ha="center",va="center",fontsize=7,fontweight=("bold" if hi else "normal"))
            y-=0.55
        y-=0.2
    panel(ax,"a","histories of $\\{2,4,5,9\\}$ from source 4; endpoint 9000")
    ax=axs[1]; ax.axis("off"); ax.set_xlim(0,10); ax.set_ylim(0,10)
    for x,t in ((0,"$A$"),(3.7,"endpoint"),(5.8,"comp."),(8.0,"$I$-values")): ax.text(x,9.2,t,fontsize=6.3,fontweight="bold",ha=("left" if x==0 else "center"))
    for i,f in enumerate(fam):
        ax.text(0,8.0-i*1.5,"$\\{"+",".join(map(str,f['A']))+"\\}$",fontsize=6)
        ax.text(3.7,8.0-i*1.5,str(f['endpoint']),fontsize=6.3,ha="center")
        ax.text(5.8,8.0-i*1.5,str(f['components']),fontsize=6.3,ha="center")
        ax.text(8.0,8.0-i*1.5,"$\\{0,1\\}$",fontsize=6.3,ha="center")
    ax.text(0,3.4,"$I=[2$ before $4]$ is constant on\nevery swap class. It is not a\ncomplete invariant: for\n$A=\\{3,5,9\\}$ there are 3 components\nbut $I$ takes two values.",fontsize=6,va="top")
    panel(ax,"b","finite-exact rows")
    DATA['fig19']={'components':[[list(w) for w in comp] for comp in cl],'family':fam}
    fig.tight_layout(); save(fig,"fig19_occurrence_events")
def fig20():
    fig,axs=plt.subplots(1,2,figsize=(W,2.7))
    ax=axs[0]; clean(ax,(-2,2,-2,2))
    ax.add_patch(Circle((0,0.3),0.35,fc=SRC_L,ec=SRC,lw=1))
    ax.text(0,0.3,"pt",ha="center",va="center",fontsize=7)
    ax.text(0,-0.5,"$K_{\\mathrm{move}}(9000)$",ha="center",fontsize=7)
    ax.text(0,-0.95,"contractible, Betti $(1,0,\\ldots,0)$",ha="center",fontsize=6.3)
    ax.text(0,-1.5,"(integer state: $b=1$)",ha="center",fontsize=6.3)
    ax.text(0,1.5,"state geometry of the endpoint",ha="center",fontsize=7,fontweight="bold")
    panel(ax,"a","")
    ax=axs[1]; clean(ax,(-2.3,2.3,-2,2))
    for i,(x,lab,sty) in enumerate([(-1.2,"$I=1$",SRC_L),(1.2,"$I=0$",TGT_L)]):
        ax.add_patch(Circle((x,0.5),0.55,fc=sty,ec=(SRC if i==0 else TGT),lw=1,hatch=("" if i==0 else "//")))
        ax.text(x,0.5,"2 histories",ha="center",va="center",fontsize=5.8); ax.text(x,-0.4,lab,ha="center",fontsize=7)
    ax.text(0,1.55,"history space of endpoint 9000",ha="center",fontsize=7,fontweight="bold")
    ax.text(0,-1.0,"2 components (contents $\\{2,4,5,9\\}$);\n48000 and 392000: 3 components each",ha="center",fontsize=6.3)
    panel(ax,"b","")
    fig.text(0.5,0.03,"No map between (a) and (b) is claimed or constructed (A4-T7, OPEN).",ha="center",fontsize=6.8)
    DATA['fig20']={'K_move_betti':[1,0,0,0],'history_components':{'9000':2,'48000':3,'392000':3}}
    save(fig,"fig20_state_vs_history")
if __name__=="__main__":
    for f in (fig15,fig16,fig17,fig18,fig19,fig20): f()
    D=json.load(open(os.path.join(OUT,'..','results','FIGURE_DATA.json'))); D.update(DATA); json.dump(D,open(os.path.join(OUT,'..','results','FIGURE_DATA.json'),'w'),indent=1,default=str)

import json, sys
sys.path.insert(0,'.')
from figlib3 import *
from grav import *
DATA={}
# ---------------- Fig 1: objects
fig,ax=plt.subplots(figsize=(W,2.9)); clean(ax,(0,12.4,0,6.0))
ax.text(0.05,5.75,"Schematic of the evolving record (example $x_0=3025/3$)",fontsize=8,fontweight="bold")
items=[(0.1,3.7,2.5,1.5,"state $x=a/b$\n$a=5^2\\cdot 11^2,\\ b=3$"),
       (3.2,3.7,2.7,1.5,"occurrence set\n$D(x)=\\{55\\}$\nfibre $F=\\{(1,1)\\}$"),
       (6.5,3.7,2.8,1.5,"lattice $\\Lambda_3$, box $[0,1]^2$\n$\\mathrm{Gr}=\\pm(1,1),\\pm(1,-1)$\n($\\pm(1,-1)$ dormant)"),
       (9.9,3.7,2.4,1.5,"move complex\n$K_{\\rm move}(x)$ = point\n$\\beta=(1)$")]
for (x,y,w,h,t) in items: box(ax,x,y,w,h,t,fc=SRC_L,ec=SRC,fs=7)
for i in range(3): arrow(ax,(items[i][0]+items[i][2],4.45),(items[i+1][0],4.45),c="k",shrink=0.02)
ax.text(1.35,3.45,"exact input",ha="center",fontsize=6.5,style="italic"); ax.text(4.55,3.45,"function of $x$",ha="center",fontsize=6.5,style="italic")
ax.text(7.9,3.45,"function of $b$, box, $F$",ha="center",fontsize=6.5,style="italic"); ax.text(11.1,3.45,"function of $D$ alone",ha="center",fontsize=6.5,style="italic")
box(ax,0.1,0.5,6.0,1.9,"collective step\n$C(x)=x+L^2/G,\\ L=\\operatorname{lcm}D,\\ G=\\gcd\\{d-1\\}$\nhere $L=55,\\ G=54$:  $x_1=57475/54$",fc=TGT_L,ec=TGT,fs=7)
box(ax,6.6,0.5,5.7,1.9,"events: $D$ grows (Lemma M); $K_{\\rm move}$ changes\nonly through the new occurrences\n(Sections 8--10)",fc=KEEP_L,ec=KEEP,fs=7)
arrow(ax,(1.35,3.7),(1.35,2.4),c=TGT,shrink=0.02); arrow(ax,(6.1,1.45),(6.6,1.45),c="k",shrink=0.02)
save(fig,"fig01_record")
DATA['fig01']={'x':'3025/3','D':Dset(Fr(3025,3)),'Gr':region_graver(Fr(3025,3))[2],'C':str(C(Fr(3025,3)))}
# ---------------- Fig 2: integer collapse (m=2^4 3^2 .. q=(2,1)) sigma=12 ; grid picture
m=2**4*3**2*7  # sigma=12
D=Dset(m); K=complex_of(D); f,r,b=betti(K,2)
fig,axs=plt.subplots(1,2,figsize=(W,2.7))
ax=axs[0]; ax.set_aspect("equal"); ax.axis("off"); panel(ax,"a","exponent box $[0,2]\\times[0,1]$, $\\sigma=12$")
cs=cellsets(K)
pr=K['pr']; vec=K['vec']
pos={d:(vec[d][0],vec[d][1]) for d in D}; pos[1]=(0,0)
for c in cs[2]:
    xs=[pos[v] for v in c]; x0=min(p[0] for p in xs); y0=min(p[1] for p in xs)
    ax.add_patch(Rectangle((x0,y0),1,1,fc="#dfe9f5",ec="none",zorder=1))
for (u,v) in K['E']: seg(ax,pos[u],pos[v],c="#444",lw=1.0)
for d in D: node(ax,pos[d][0],pos[d][1],str(d),r=0.13,fs=6.5)
node(ax,0,0,"1",fc="#eee",ec="k",ls=(0,(2,2)),r=0.13,fs=6.5)
ax.set_xlim(-0.4,2.5); ax.set_ylim(-0.4,1.5)
ax.text(1,-0.33,"exponent of 2",ha="center",fontsize=6.5); ax.text(-0.38,0.5,"exp. of 3",rotation=90,va="center",fontsize=6.5)
ax=axs[1]; ax.set_aspect("equal"); ax.axis("off"); panel(ax,"b","closed-star decomposition")
ax.set_xlim(0,5); ax.set_ylim(0,3)
box(ax,0.2,0.4,1.8,2.2,"box complex $B$\ncontractible",fc=SRC_L,ec=SRC,fs=7)
box(ax,2.4,1.6,2.4,1.0,"closed star of $0$:\ncone, contractible",fc=TGT_L,ec=TGT,fs=6.8)
box(ax,2.4,0.4,2.4,1.0,"$K=B\\setminus$ open star\n$\\simeq B$ (cone glued)",fc=KEEP_L,ec=KEEP,fs=6.8)
arrow(ax,(2.0,1.5),(2.4,2.1),shrink=0.02); arrow(ax,(2.0,1.5),(2.4,0.9),shrink=0.02)
save(fig,"fig02_integer_collapse")
DATA['fig02']={'m':m,'sigma':12,'D':D,'f':f,'betti':b}
# ---------------- Fig 3: equal D different Gr (r=13)
r_=13; X=Fr(25*r_*r_,5*r_-1); Y=Fr(25*r_*r_,8)
fig,axs=plt.subplots(1,3,figsize=(W,2.5))
for ax,(X_,tt) in zip(axs[:2],[(X,"$x_r=25r^2/(5r-1)$"),(Y,"$y_r=25r^2/8$")]):
    ps,box_,gr=region_graver(X_); ax.set_aspect("equal"); ax.set_xlim(-1.6,1.6); ax.set_ylim(-1.6,1.6); ax.axis("off")
    ax.set_title(tt+f", $r={r_}$",fontsize=7.5)
    for u in (-1,0,1):
        for v in (-1,0,1):
            ax.plot(u,v,"o",ms=2.5,color="#bbb")
    ax.add_patch(Rectangle((-0.0,-0.0),1,1,fc="none",ec=SRC,lw=0.8,ls="--"))
    for g in gr: arrow(ax,(0,0),(g[0],g[1]),c=(LOST if g in [(1,-1),(-1,1)] else TGT),lw=1.2,shrink=0.0)
    node(ax,1,1,"65",fc=SRC_L,ec=SRC,r=0.2,fs=6.5)
    ax.text(0,-1.55,f"$|\\mathrm{{Gr}}|={len(gr)}$, $D=\\{{65\\}}$",ha="center",fontsize=7)
ax=axs[2]; ks=[2,3,4,5]; ax.bar([k-0.18 for k in ks],[2]*4,width=0.35,color=SRC_L,ec=SRC,label="$x$"); ax.bar([k+0.18 for k in ks],[k*(k-1)+2 for k in ks],width=0.35,color=TGT_L,ec=TGT,hatch="//",label="$y$")
ax.set_xticks(ks); ax.set_xlabel("$k$ (number of primes)"); ax.set_ylabel("$|\\mathrm{Gr}|$"); ax.legend(frameon=False); ax.set_title("$D$ equal, $\\mathrm{Gr}$ not",fontsize=7.5)
for s in ("top","right"): ax.spines[s].set_visible(False)
save(fig,"fig03_equalD_diffGr")
DATA['fig03']={'r':13,'Grx':region_graver(X)[2],'Gry':region_graver(Y)[2]}
# ---------------- Fig 4: two-prime classification
types=[("$\\emptyset$",[],27*0),("A",[(1,0)],0),("B",[(0,1)],0),("C",[(1,1)],0),("E",[(1,-1)],0),("CE",[(1,1),(1,-1)],0),("ABCE",[(1,0),(0,1)],0)]
cnt=json.load(open('../results/c5.json'))['R3T2']['types']
names=['none','A','B','C','E','CE','ABCE']
fig,axs=plt.subplots(1,2,figsize=(W,2.7),gridspec_kw={'width_ratios':[2.3,1]})
ax=axs[0]; ax.axis("off"); ax.set_xlim(0,7); ax.set_ylim(0,3.2); panel(ax,"a","seven types (exponent plane of $(p,r)$)")
for i,(nm,gr,_) in enumerate(types):
    cx=0.5+i*0.95; cy=1.7
    ax.add_patch(Rectangle((cx-0.38,cy-0.38),0.76,0.76,fc="white",ec="#999",lw=0.5))
    ax.plot([cx],[cy],"o",ms=2,color="k")
    for g in gr:
        for s in (1,-1): ax.annotate("",xy=(cx+0.36*s*g[0],cy+0.36*s*g[1]),xytext=(cx,cy),arrowprops=dict(arrowstyle="-|>",color=TGT,lw=1.0))
    ax.text(cx,cy-0.65,nm,ha="center",fontsize=7)
    ax.text(cx,cy-0.98,"$D$="+{"none":"$\\emptyset$","A":"$\\{p\\}$","B":"$\\{r\\}$","C":"$\\{pr\\}$","E":"$\\emptyset$","CE":"$\\{pr\\}$","ABCE":"$\\{p,r,pr\\}$"}[names[i]],ha="center",fontsize=5.2)
ax.text(3.5,2.85,"types $T\\subseteq\\{A,B,C,E\\}$;  A: $p\\equiv 1$,  B: $r\\equiv 1$,  C: $pr\\equiv 1$,  E: $p\\equiv r$  (all mod $b$)",ha="center",fontsize=6.8)
ax=axs[1]; panel(ax,"b","tested states")
vals=[cnt.get(n,0) for n in names]; ax.barh(range(7),vals,color=SRC_L,ec=SRC); ax.set_yticks(range(7)); ax.set_yticklabels(["none","A","B","C","E","CE","ABCE"],fontsize=6.5); ax.invert_yaxis(); ax.set_xscale("log"); ax.set_xlabel("count (log)")
for s in ("top","right"): ax.spines[s].set_visible(False)
save(fig,"fig04_two_prime_types")
DATA['fig04']={'counts':cnt}
# ---------------- Fig 5: A_{k-1} dormant family k=3
fig,axs=plt.subplots(1,2,figsize=(W,2.7))
import numpy as np
ang=[90,210,330]; ev=[(math.cos(math.radians(a)),math.sin(math.radians(a))) for a in ang]
for ax,act,tt in zip(axs,[False,True],["at $x=P^2/\\ell$: all six roots dormant","at $y=(Pq)^2/\\ell$: roots realised by $p_iq/p_jq$"]):
    ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-1.9,1.9); ax.set_ylim(-1.9,1.9); ax.set_title(tt,fontsize=7.5)
    for i in range(3):
        for j in range(3):
            if i!=j:
                p=(ev[i][0]-ev[j][0],ev[i][1]-ev[j][1])
                ax.annotate("",xy=(0.62*p[0],0.62*p[1]),xytext=(0,0),arrowprops=dict(arrowstyle="-|>",color=(KEEP if act else GREY),lw=1.3,ls="-" if act else (0,(3,2))))
    for i in range(3): node(ax,1.35*ev[i][0],1.35*ev[i][1],f"$e_{i+1}$",fc="white",r=0.0,fs=0) 
    for i,e in enumerate(ev): ax.text(1.55*e[0],1.55*e[1],f"$e_{i+1}$",ha="center",va="center",fontsize=7)
    ax.text(0,-1.8,"$k=3$: $k(k-1)=6$ roots of $A_2$",ha="center",fontsize=6.8)
save(fig,"fig05_dormant_family")
# ---------------- Fig 6: collective coordinates along the 8-step orbit
o=orbit(Fr(3025,3),8); rows=[]
for n,t in enumerate(o):
    D=Dset(t); L,G=LG(D); a,b_=t.numerator,t.denominator
    rows.append({'n':n,'x':str(t),'b':b_,'L':L,'G':G,'t':a//(L*L) if a%(L*L)==0 else None,'D':D})
fig,axs=plt.subplots(1,2,figsize=(W,2.5))
ax=axs[0]; ax.plot(range(9),[r_['b'] for r_ in rows],"o-",color=SRC,ms=3,lw=0.9); ax.set_yscale("log"); ax.set_xlabel("step $n$"); ax.set_ylabel("denominator $b_n$"); panel(ax,"a","reduced denominator")
ax.plot(range(9),[r_['G'] for r_ in rows],"s--",color=LOST,ms=3,lw=0.8,label="$G_n$"); ax.legend(frameon=False)
ax=axs[1]; panel(ax,"b","$t_n=a_n/L_n^2$ and $L_n$")
ax.plot(range(9),[r_['L'] for r_ in rows],"o-",color=TGT,ms=3,label="$L_n$"); ax.plot(range(9),[r_['t'] for r_ in rows],"s--",color=UNC_E,ms=3,label="$t_n$"); ax.set_xlabel("step $n$"); ax.set_yscale("log"); ax.legend(frameon=False)
for a_ in axs:
    for s in ("top","right"): a_.spines[s].set_visible(False)
save(fig,"fig06_collective_coordinates")
DATA['fig06']=rows
# ---------------- Fig 7: rigid orbit vs persistent G=5
S5=lambda k:126*2**k
o_int=orbit(Fr(36),12); o5=orbit(Fr(S5(0)**2,5),12)
fig,axs=plt.subplots(1,2,figsize=(W,2.6))
ax=axs[0]; panel(ax,"a","$\\log_2(x_n/x_0)$")
ax.plot(range(13),[math.log2(t/o_int[0]) for t in o_int],"o-",color=SRC,ms=3,label="integer $x_0=36$ ($G=1$)")
ax.plot(range(13),[math.log2(t/o5[0]) for t in o5],"s--",color=LOST,ms=6,mfc="none",label="$x_0=126^2/5$ ($G=5$)")
ax.set_xlabel("step $n$"); ax.legend(frameon=False,fontsize=6.5); ax.set_xticks(range(0,13,3))
ax=axs[1]; panel(ax,"b","$G_n$ and denominator $b_n$")
Gint=[LG(Dset(t))[1] for t in o_int[:12]]; G5=[LG(Dset(t))[1] for t in o5[:12]]
ax.step(range(12),Gint,where="mid",color=SRC,label="$G_n$, integer orbit"); ax.step(range(12),G5,where="mid",color=LOST,ls="--",label="$G_n$, $G=5$ orbit")
ax.plot(range(12),[t.denominator for t in o5[:12]],"^:",color=LOST,ms=3,label="$b_n$, $G=5$ orbit"); ax.set_xlabel("step $n$"); ax.legend(frameon=False,fontsize=6.5)
for a_ in axs:
    for s in ("top","right"): a_.spines[s].set_visible(False)
save(fig,"fig07_rigid_vs_persistent")
DATA['fig07']={'int':[str(t) for t in o_int],'g5':[str(t) for t in o5],'ratio3_int':[str(o_int[n+3]/o_int[n]) for n in range(9)],'ratio3_g5':[str(o5[n+3]/o5[n]) for n in range(9)],'G5':G5,'Gint':Gint}
# ---------------- Fig 8 & 9: tower cycles
def cycle_fig(name,S,l,P,rho,kk):
    fig,ax=plt.subplots(figsize=(W,2.5)); clean(ax,(-0.2,P+3.3,-0.5,3.2))
    xs=list(range(P+1))
    for j in range(P+1):
        k=0 if j<P else 1; t_=(j+1) if j<P else 1
        txt=f"$x_{j}$\n${t_ if j<P else rho**2}S_0^2/{l}$" if j<P else f"$x_{P}$\n$=S_1^2/{l}$"
        c= KEEP_L if j==P else SRC_L; e= KEEP if j==P else SRC
        box(ax,j*(P+3.0)/(P+1)+0.0,1.0,(P+3.0)/(P+1)-0.15,1.0,txt,fc=c,ec=e,fs=6.2)
    for j in range(P):
        arrow(ax,((j+1)*(P+3.0)/(P+1)-0.15,1.5),((j+1)*(P+3.0)/(P+1),1.5),shrink=0.0,c="k")
    ax.text((P+3.0)/2,2.65,f"one period = ${P}$ steps; $t=1,\\dots,{rho**2}$; event at $t={rho**2}$ ($u^*={rho}$): $L:S_0\\to {rho}S_0$",ha="center",fontsize=7)
    d0=len(tD(S(0),l)); d1=len(tD(S(1),l))
    ax.text((P+3.0)/2,0.35,f"$|D|={d0}\\to{d1}$ at the event; $D$ constant on the other steps",ha="center",fontsize=7)
    save(fig,name)
def tD(S,m): return sorted(d for d in divisors(factor(S)) if d>=2 and d%m==1%m)
S11=lambda k: 2**2*3**(3+k)*5**4
cycle_fig("fig08_g5_cycle",S5,5,3,2,0)
cycle_fig("fig09_g11_cycle",S11,11,8,3,0)
DATA['fig08']={'D0':len(tD(S5(0),5)),'D1':len(tD(S5(1),5))}; DATA['fig09']={'D0':len(tD(S11(0),11)),'D1':len(tD(S11(1),11))}
json.dump(DATA,open('../results/FIGDATA_a.json','w'),default=str,indent=1)
print('done a')

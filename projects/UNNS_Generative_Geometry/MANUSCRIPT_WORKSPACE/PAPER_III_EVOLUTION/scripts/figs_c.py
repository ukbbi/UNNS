import json, sys
sys.path.insert(0,'.')
from figlib3 import *
from trans3 import analyse
DATA={}
def sp(ax):
    for s in ("top","right"): ax.spines[s].set_visible(False)
ex=lambda d: (factor(d).get(2,0), factor(d).get(11,0))
# -------- Fig 20: zig-zag K <- K0 -> K'
D=[8,22,176]; D2=Dset(orbit(Fr(176**2,7),6)[6]); t=analyse(D,D2)
K=complex_of(D); K2=complex_of(D2)
fig,axs=plt.subplots(1,3,figsize=(W,3.0),gridspec_kw={'width_ratios':[1,0.9,1.5]})
for ax in axs: ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-0.6,4.6); ax.set_ylim(-1.7,1.6)
# K
for (u,v) in K['E']: seg(axs[0],ex(u),ex(v),c="#444",lw=1.2)
for d in D: node(axs[0],*ex(d),str(d),r=0.22,fs=6)
panel(axs[0],"a","$K$")
axs[0].text(2,-1.2,"$\\beta(K)=(1,1)$\n$r=(1,0)$, $h=(0,3)$",ha="center",fontsize=6.3)
# K0
for d in D: node(axs[1],*ex(d),str(d),r=0.22,fs=6)
panel(axs[1],"b","$K^\\circ=K\\cap K'$ (3 points)")
axs[1].text(2,-1.2,"$\\beta(K^\\circ)=(3,0)$\nall 3 edges dead",ha="center",fontsize=6.3)
# K'
cs2=cellsets(K2)
for c in cs2[2]:
    xs=[ex(v) for v in c]; x0_=min(p[0] for p in xs); y0_=min(p[1] for p in xs); axs[2].add_patch(Rectangle((x0_,y0_),1,1,fc="#cfe6d2",ec="none",zorder=1))
for (u,v) in K2['E']: seg(axs[2],ex(u),ex(v),c=KEEP,lw=1.1)
for d in D2: node(axs[2],*ex(d),str(d),fc=(KEEP_L if d not in D else SRC_L),ec=(KEEP if d not in D else SRC),r=0.2,fs=5.5)
panel(axs[2],"c","$K'$")
axs[2].text(2,-1.2,"$\\beta(K')=(1)$\n$r'=(1,0)$, $h'=(0,2)$",ha="center",fontsize=6.3)
fig.text(0.5,0.02,"$\\Delta\\beta_1=(h_1'-h_1)+(r_1'-r_1)+(r_0'-r_0)=(2-3)+(0-0)+(1-1)=-1$.  Maps $K\\leftarrow K^\\circ\\to K'$ are inclusions.",ha="center",fontsize=6.6)
save(fig,"fig20_zigzag"); DATA['fig20']={k:v for k,v in t.items() if k!='chk'}
# -------- Fig 21: graph-level predictor
def predict_graph(D,N):
    D=sorted(D); Dn=sorted(set(D)|set(N)); E=edges(D); N=set(N)
    pierced={(u,v) for (u,v) in E if any(w%gcd(u,v)==0 and lcm(u,v)%w==0 for w in N)}
    pts=set(Dn)|{1}; newE=set()
    for w in N:
        for u in Dn:
            if u==w: continue
            a,b=min(u,w),max(u,w)
            if (a,b) in newE: continue
            g=gcd(a,b); l=lcm(a,b)
            if not any(z!=a and z!=b and z%g==0 and l%z==0 for z in pts): newE.add((a,b))
    surv=(E-pierced)|newE
    return len(surv)-len(Dn)+ncomp(Dn,surv)
pairs=[]
for l in (5,7,11,13):
    d=json.load(open('../results/census_l%d.json'%l)); cache={}
    for r in d['rows']:
        if (len(r['f'])>2 and any(r['f'][2:])) or (len(r['f2'])>2 and any(r['f2'][2:])): continue
        S,n=r['S'],r['n']
        if (l,S) not in cache:
            cur=Fr(S*S,l); Ds=[]
            for k in range(25):
                Dd=Dset(cur); Ds.append(tuple(Dd))
                if not Dd: break
                L_,G_=LG(Dd); cur=cur+Fr(L_*L_,G_)
            cache[(l,S)]=Ds
        Ds=cache[(l,S)]; Dd=Ds[n]; D2_=Ds[n+1]; N=[x for x in D2_ if x not in Dd]
        pairs.append((predict_graph(Dd,N), r['b2'][1]))
fig,axs=plt.subplots(1,2,figsize=(W,2.6))
ax=axs[0]; panel(ax,"a","$\\beta_1(K')$: predictor vs full rebuild")
from collections import Counter
cn=Counter(pairs); ax.scatter([p[1] for p in cn],[p[0] for p in cn],s=[8+3*cn[p] for p in cn],color=SRC,alpha=0.8)
mx=max(max(p) for p in pairs); ax.plot([0,mx],[0,mx],color=GREY,lw=0.6); ax.set_xlabel("rebuilt $\\beta_1(K(D'))$"); ax.set_ylabel("predicted $E-V+\\beta_0$"); sp(ax)
ax.text(0.05,0.95,f"{sum(a==b for a,b in pairs)}/{len(pairs)} graph-level events agree",transform=ax.transAxes,fontsize=6.5,va="top")
ax=axs[1]; panel(ax,"b","activation family: $\\Delta\\beta_1=\\binom{k+1}{2}-k$")
ks=np.arange(2,9); ax.plot(ks,(ks+1)*ks//2-ks,"o-",color=TGT,ms=3,label="$\\Delta E-\\Delta V+\\Delta\\beta_0$"); ax.set_xlabel("$k$"); ax.legend(frameon=False); sp(ax)
save(fig,"fig21_graph_update"); DATA['fig21']={'n':len(pairs),'ok':sum(a==b for a,b in pairs)}
# -------- Fig 22: event types
rows=[]
for l in (5,7,11,13): rows+=[dict(r,l=l) for r in json.load(open('../results/census_l%d.json'%l))['rows']]
types=['V','II','III','IV']; cnt={l:Counter(r['type'] for r in rows if r['l']==l) for l in (5,7,11,13)}
fig,axs=plt.subplots(1,2,figsize=(W,2.5),gridspec_kw={'width_ratios':[1.3,1]})
ax=axs[0]; panel(ax,"a","event types by modulus $\\ell$"); bot=np.zeros(4); cols=[SRC_L,UNC,KEEP_L,LOST_L]; hs=[None,"//","..","xx"]
for ty,c_,h_ in zip(types,cols,hs):
    v=np.array([cnt[l][ty] for l in (5,7,11,13)]); ax.bar(range(4),v,bottom=bot,color=c_,ec="k",lw=0.5,hatch=h_,label=f"Type {ty}"); bot+=v
ax.set_xticks(range(4)); ax.set_xticklabels(["5","7","11","13"]); ax.set_xlabel("$\\ell$"); ax.set_ylabel("$D$-events"); ax.legend(frameon=False,fontsize=6); sp(ax)
ax=axs[1]; panel(ax,"b","totals (no Type I)"); tot=Counter(r['type'] for r in rows)
ax.bar(range(4),[tot[t_] for t_ in types],color=cols,ec="k",lw=0.5,hatch=None); ax.set_xticks(range(4)); ax.set_xticklabels(["V","II","III","IV"]); ax.set_yscale("log")
for i,t_ in enumerate(types): ax.text(i,tot[t_]*1.1,f"{tot[t_]:,}",ha="center",fontsize=6.5)
ax.set_ylim(5,5000); sp(ax)
save(fig,"fig22_event_types"); DATA['fig22']={'totals':dict(tot),'by_l':{l:dict(c) for l,c in cnt.items()}}
# -------- Fig 23/24: towers
T5=json.load(open('../results/tower5.json')); T11=json.load(open('../results/tower11.json'))
fig,axs=plt.subplots(1,2,figsize=(W,2.6),gridspec_kw={'width_ratios':[1,1.3]})
ax=axs[0]; panel(ax,"a","$k=0,\\dots,12$ (zoom)")
for j,(c_,m_) in enumerate(((SRC,"o"),(UNC_E,"s"),(TGT,"^"))):
    ax.step([r['k'] for r in T5[:13]],[r['b'][j+1] if len(r['b'])>j+1 else 0 for r in T5[:13]],where="post",color=c_,marker=m_,ms=3,label=f"$\\beta_{j+1}$")
ax.set_xlabel("tower index $k$"); ax.legend(frameon=False); sp(ax)
ax.annotate("$\\beta_1:1\\to4$\n(orbit step 5$\\to$6)",(2,4),xytext=(4,1.3),fontsize=6,arrowprops=dict(arrowstyle="-|>",lw=0.5))
ax=axs[1]; panel(ax,"b","finite-exact range $k\\leq140$ (no extrapolation)")
ks=[r['k'] for r in T5]
for j,(c_,m_) in enumerate(((SRC,"o"),(UNC_E,"s"),(TGT,"^"))):
    ax.step(ks,[r['b'][j+1] if len(r['b'])>j+1 else 0 for r in T5],where="post",color=c_,lw=1.0,label=f"$\\beta_{j+1}$")
ax.axvspan(0,140,color="#eef3f8",zorder=0); ax.set_xlim(0,148); ax.set_xlabel("tower index $k$"); ax.legend(frameon=False,loc="center right"); sp(ax)
ax.text(70,7.3,"computed for every $k\\leq140$; $(1,6,5,0)$ for $7\\leq k\\leq140$",fontsize=6,ha="center")
ax.set_ylim(0,8.5)
save(fig,"fig23_g5_betti"); DATA['fig23']={'k':ks[:3],'rows_head':T5[:9],'last':T5[-1]}
fig,axs=plt.subplots(1,3,figsize=(W,2.6),gridspec_kw={'width_ratios':[1,1,1]})
kk=[r['k'] for r in T11]
b=lambda r,j: r['b'][j] if len(r['b'])>j else 0
ax=axs[0]; panel(ax,"a","$\\beta_1,\\beta_2$"); ax.step(kk,[b(r,1) for r in T11],where="post",color=SRC,label="$\\beta_1$"); ax.step(kk,[b(r,2) for r in T11],where="post",color=UNC_E,ls="--",label="$\\beta_2$"); ax.set_xlabel("$k$"); ax.legend(frameon=False,fontsize=6); sp(ax)
ax=axs[1]; panel(ax,"b","$\\beta_3$ ($k\\leq140$)"); ax.step(kk,[b(r,3) for r in T11],where="post",color=TGT); ax.set_xlabel("$k$"); sp(ax)
ax=axs[2]; panel(ax,"c","$\\beta_3(k+5)-\\beta_3(k)$"); inc=[(k_,b(T11[k_+5],3)-b(T11[k_],3)) for k_ in range(0,136)]
ax.plot([a for a,_ in inc],[v for _,v in inc],".",ms=2.5,color=KEEP); ax.axhline(9,color=GREY,lw=0.6); ax.axvline(8,color=LOST,lw=0.6,ls=":"); ax.set_xlabel("$k$"); ax.set_ylim(-1,11)
ax.text(70,9.5,"$=9$ for $k\\geq8$",fontsize=6,ha="center"); sp(ax)
save(fig,"fig24_g11_betti")
DATA['fig24']={'head':T11[:12],'last':T11[-1],'inc_ok':all(v==9 for a,v in inc if a>=8),'beta1_const_from':2,'beta2_const_from':6}
# -------- Fig 25: nested tower complexes
S5=lambda k:126*2**k; S11=lambda k: 2**2*3**(3+k)*5**4
def tD(S,m): return sorted(d for d in divisors(factor(S)) if d>=2 and d%m==1%m)
def maxl1(D,E):
    pr,vec=evec(D); return max([sum(abs(a-b) for a,b in zip(vec[u],vec[v])) for u,v in E]+[0])
def nested(Sf,m,ks):
    ok=True; prev=None
    for k in ks:
        D=tD(Sf(k),m); K=complex_of(D); C=cellsets(K)
        if prev is not None:
            Dp,Cp=prev
            for j in range(len(Cp)):
                if not Cp[j]<=(C[j] if j<len(C) else set()): ok=False
        prev=(D,C)
    return ok
n5=nested(S5,5,range(0,26)); n11=nested(S11,11,range(0,26))
ml5=[maxl1(tD(S5(k),5),edges(tD(S5(k),5))) for k in range(0,41)]; ml11=[maxl1(tD(S11(k),11),edges(tD(S11(k),11))) for k in range(0,41)]
fig,axs=plt.subplots(1,3,figsize=(W,2.5))
ax=axs[0]; panel(ax,"a","$G=5$: $f_j(K_k)$")
for j,(c_,m_) in enumerate(((SRC,"o"),(UNC_E,"s"),(TGT,"^"),(LOST,"d"))):
    ax.plot([r['k'] for r in T5[:21]],[r['f'][j] if len(r['f'])>j else 0 for r in T5[:21]],color=c_,marker=m_,ms=2.2,lw=0.8,label=f"$f_{j}$")
ax.set_xlabel("$k$"); ax.legend(frameon=False,fontsize=5.5,ncol=2); sp(ax)
ax=axs[1]; panel(ax,"b","$G=11$: $f_j(K_k)$")
for j,(c_,m_) in enumerate(((SRC,"o"),(UNC_E,"s"),(TGT,"^"),(LOST,"d"))):
    ax.plot([r['k'] for r in T11[:21]],[r['f'][j] if len(r['f'])>j else 0 for r in T11[:21]],color=c_,marker=m_,ms=2.2,lw=0.8,label=f"$f_{j}$")
ax.set_xlabel("$k$"); sp(ax)
ax=axs[2]; panel(ax,"c","max $\\ell_1$ of a realised move"); ax.step(range(41),ml5,where="post",color=SRC,label="$G=5$ (bound $4$)"); ax.step(range(41),ml11,where="post",color=LOST,ls="--",label="$G=11$ (bound $10$)")
ax.axhline(4,color=SRC,lw=0.4,ls=":"); ax.axhline(10,color=LOST,lw=0.4,ls=":"); ax.set_xlabel("$k$"); ax.legend(frameon=False,fontsize=5.8); sp(ax)
save(fig,"fig25_nested_towers"); DATA['fig25']={'nested_G5_k25':n5,'nested_G11_k25':n11,'maxl1_G5':ml5,'maxl1_G11':ml11}
print('nested',n5,n11,max(ml5),max(ml11))
# -------- Fig 26: hierarchy + SELECT-II obstruction
fig,axs=plt.subplots(1,2,figsize=(W,3.2),gridspec_kw={'width_ratios':[1.15,1]})
ax=axs[0]; ax.axis("off"); ax.set_xlim(0,6); ax.set_ylim(0,7); panel(ax,"a","correspondence hierarchy")
lv=[("L5  dynamical intertwining","not available (domains differ)",GREY),("L4  geometric structures","only at endpoints",GREY),("L3  reduced event records","N=1,2,5 ($G\\!=\\!11$); N=1 ($G\\!=\\!5$)",KEEP),("L2  occurrence information","implied by L1 at endpoints",SRC),("L1  numerical ratio","$x_m=R(N)x_n$",SRC)]
for i,(a_,b_,c_) in enumerate(lv):
    y=5.6-i*1.25; box(ax,0.1,y,5.8,1.0,"",fc=("white" if c_==GREY else (KEEP_L if c_==KEEP else SRC_L)),ec=c_,ls=("--" if c_==GREY else "-"))
    ax.text(0.25,y+0.68,a_,fontsize=6.6,fontweight="bold",va="center"); ax.text(0.25,y+0.3,b_,fontsize=6.0,va="center")
ax.text(3,0.15,"each level is tested separately; none is inferred from a weaker one",fontsize=5.6,ha="center",style="italic")
ax=axs[1]; panel(ax,"b","$R(N)=(N+1)^2/N$"); Ns=np.arange(1,13); ax.plot(Ns,(Ns+1)**2/Ns,"o",color=SRC,ms=3)
ax.axhline(4,color=KEEP,lw=0.7,ls="--"); ax.axhline(9,color=LOST,lw=0.9,ls="-"); ax.text(12.3,4.15,"$4$ ($N=1$)",fontsize=6,ha="right",color=KEEP); ax.text(12.3,9.2,"$9$: no integer $N$",fontsize=6,ha="right",color=LOST)
ax.set_xlabel("label $N$"); ax.set_ylabel("multiplier"); sp(ax); ax.set_ylim(0,15)
save(fig,"fig26_hierarchy_obstruction")
json.dump(DATA,open('../results/FIGDATA_c.json','w'),default=str,indent=1)
json.dump({'nested_G5_k25':n5,'nested_G11_k25':n11,'maxl1_G5_max':max(ml5),'maxl1_G11_max':max(ml11)},open('../results/nested_checks.json','w'))
print('done c')

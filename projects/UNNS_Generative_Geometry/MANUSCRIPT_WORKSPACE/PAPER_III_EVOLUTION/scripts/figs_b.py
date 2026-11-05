import json, sys
sys.path.insert(0,'.')
from figlib3 import *
from trans3 import analyse
DATA={}
def sp(ax):
    for s in ("top","right"): ax.spines[s].set_visible(False)
# -------- Fig 10: carries vs events (G=11 tower, k=0)
S11=lambda k: 2**2*3**(3+k)*5**4
o=orbit(Fr(S11(0)**2,11),17)
rows=[]
for n,t in enumerate(o):
    a=t.numerator; f=factor(a); q={p:f.get(p,0)//2 for p in (2,3,5)}
    rows.append({'n':n,'q2':q[2],'q3':q[3],'q5':q[5],'nD':len(Dset(t))})
fig,axs=plt.subplots(1,2,figsize=(W,2.6))
ax=axs[0]; panel(ax,"a","box coordinates $q_p(x_n)$")
for p,c_,m_ in ((2,SRC,"o"),(3,TGT,"s"),(5,UNC_E,"^")): ax.step(range(18),[r_['q%d'%p] for r_ in rows],where="post",color=c_,marker=m_,ms=2.5,lw=0.9,label=f"$q_{p}$")
ax.set_xlabel("step $n$"); ax.legend(frameon=False,ncol=3,loc="upper left")
for n in range(1,18):
    if rows[n]['q2']!=rows[n-1]['q2'] or rows[n]['q3']!=rows[n-1]['q3']: ax.axvline(n,color=GREY,lw=0.5,ls=":")
ax.set_ylim(0,8); sp(ax)
ax=axs[1]; panel(ax,"b","occurrence count $|D(x_n)|$")
ax.step(range(18),[r_['nD'] for r_ in rows],where="post",color=KEEP,marker="o",ms=2.5); ax.set_xlabel("step $n$"); ax.set_ylim(0,12); sp(ax)
for n in range(1,18):
    if rows[n]['q2']!=rows[n-1]['q2'] or rows[n]['q3']!=rows[n-1]['q3']: ax.axvline(n,color=GREY,lw=0.5,ls=':')
ax.text(0.4,11.0,'dotted: box changes at $n=%s$'%','.join(str(n) for n in range(1,18) if rows[n]['q2']!=rows[n-1]['q2'] or rows[n]['q3']!=rows[n-1]['q3']),fontsize=6)
save(fig,"fig10_carries_vs_events"); DATA['fig10']=rows
# -------- Fig 11: first-event congruence
x0=Fr(3025,3); D0=Dset(x0); L,G=LG(D0); a,b=x0.numerator,x0.denominator; h=G//b; Y0=a*h
def solve(c,rhs,m):
    c%=m; rhs%=m; g=gcd(c,m)
    if rhs%g: return None
    m2=m//g; return 0 if m2==1 else (rhs//g)*pow(c//g,-1,m2)%m2
pts=[]
for d in range(2,200):
    if d in D0: continue
    q=Q(d,G); j=solve(L*L,-Y0,q)
    if j is None: continue
    if j==0: j=q//gcd(L*L,q)
    pts.append((d,j))
jm=min(j for d,j in pts); dm=[d for d,j in pts if j==jm]
fig,ax=plt.subplots(figsize=(W,2.5))
ax.scatter([d for d,j in pts],[j for d,j in pts],s=6,color=SRC,zorder=3)
ax.scatter(dm,[jm]*len(dm),s=28,color=LOST,marker="D",zorder=4,label=f"first event: $d={dm[0]}$, $j={jm}$")
ax.set_yscale("log"); ax.set_xlabel("candidate $d$"); ax.set_ylabel("least $j\\geq 1$ with $d\\in D(x_0+jL^2/G)$"); ax.legend(frameon=False); sp(ax)
ax.set_title("$x_0=3025/3$: $L=55$, $G=54$, one linear congruence per candidate; candidates $d<200$",fontsize=7.2)
save(fig,"fig11_first_event"); DATA['fig11']={'L':L,'G':G,'a':a,'h':h,'min':(dm,jm),'n_candidates':len(pts)}
# -------- Fig 12: prediction vs reconstruction
c4=json.load(open('../results/c4_event.json'))
tests=c4['next_event']['tests']
fig,axs=plt.subplots(1,2,figsize=(W,2.6))
ax=axs[0]; panel(ax,"a","first-event time $\\tau_D$")
xs=[t['tau'] for t in tests]; ax.scatter(xs,xs,s=14,color=SRC,marker="o",label="sieve $=$ simulation"); mx=max(xs)
ax.plot([0,mx],[0,mx],color=GREY,lw=0.6); ax.set_xlabel("simulation of $C$ (steps)"); ax.set_ylabel("congruence law"); ax.legend(frameon=False); sp(ax)
ax=axs[1]; panel(ax,"b","new occurrences per event")
nn=[len(t['new']) for t in tests]; from collections import Counter
cn=Counter(nn); ax.bar(list(cn.keys()),list(cn.values()),color=TGT_L,ec=TGT); ax.set_xlabel("$|D_\\tau\\setminus D_0|$ (all equal to sieve prediction)"); ax.set_ylabel("orbits"); sp(ax)
save(fig,"fig12_prediction"); DATA['fig12']={'n':len(tests),'all_ok':all(t['ok'] for t in tests)}
# -------- Fig 13: activation family k=2 table
fig,ax=plt.subplots(figsize=(W,2.7)); clean(ax,(0,12,0,5.6))
Dy=Dset(Fr((55*17)**2,3)); ax.text(0.1,5.3,"Activation family, $k=2$, $\\ell=3$, $(p_1,p_2)=(5,11)$, $q=17$: $x=3025/3$, $y=935^2/3$",fontsize=7.5,fontweight="bold")
box(ax,0.1,3.4,4.6,1.5,"$x$:  $D(x)=\\{55\\}$\nvertex $(1,1;0)$ in $(p_1,p_2;q)$\n$K_{\\rm move}(x)$ = point",fc=SRC_L,ec=SRC,fs=7)
box(ax,5.0,3.4,6.9,1.5,"$y$:  $D(y)=\\{55,\\,85,\\,187\\}$\nvertices $(1,1;0),\\ (1,0;1),\\ (0,1;1)$\n$K_{\\rm move}(y)=K_3$ (triangle, no 2-cell), $\\beta_1=1$",fc=TGT_L,ec=TGT,fs=7)
arrow(ax,(4.7,4.15),(5.0,4.15),shrink=0.0)
pos={55:(2.3,1.4),85:(4.0,0.5),187:(0.6,0.5)}
for u,v in [(55,85),(55,187),(85,187)]: seg(ax,pos[u],pos[v],lw=1.1)
for d_,p_ in pos.items(): node(ax,p_[0],p_[1],str(d_),fc=(KEEP_L if d_!=55 else "white"),ec=(KEEP if d_!=55 else "k"),r=0.3,fs=7,bold=(d_!=55))
ax.text(7.7,1.6,"dormant at $x$: $e_1-e_2$ (primitive, no pair realises it)\nactive at $y$: $85/187=5/11$ realises it\nactivation by new occurrence vertices\n($p_iq$), not by new relations",fontsize=7,va="center")
save(fig,"fig13_activation_family"); DATA['fig13']={'Dy':Dy}
# -------- Fig 14: K_{k+1}
fig,axs=plt.subplots(1,4,figsize=(W,2.2),gridspec_kw={'width_ratios':[1,1,1,1.4]})
for ax,k in zip(axs[:3],[2,3,4]):
    ax.set_aspect("equal"); ax.axis("off"); n=k+1; pts=circ(n,1.0)
    for i in range(n):
        for j in range(i+1,n): seg(ax,pts[i],pts[j],c="#555",lw=0.7)
    for i,p_ in enumerate(pts): node(ax,p_[0],p_[1],"$P$" if i==0 else f"$v_{i}$",r=0.22,fs=5.5)
    ax.set_xlim(-1.5,1.5); ax.set_ylim(-1.6,1.5); ax.text(0,-1.55,f"$K_{k+1}$, $\\beta_1={k*(k-1)//2}$",ha="center",fontsize=7)
ax=axs[3]; ks=np.arange(2,9); ax.plot(ks,ks*(ks-1)//2,"o-",color=SRC,ms=3); ax.set_xlabel("$k$"); ax.set_ylabel("$\\beta_1$"); sp(ax)
save(fig,"fig14_complete_graph"); DATA['fig14']={'beta1':{int(k):int(k*(k-1)//2) for k in ks}}
# -------- Fig 15: the 8-step trajectory
t8=json.load(open('../results/c1_traj.json'))['t8']
fig,ax=plt.subplots(figsize=(W,3.9)); clean(ax,(0,9.4,-3.6,3.0))
fr=t8['orbit']; D_=t8['D']; B_=t8['betti']
for n in range(9):
    x=n*1.03; ev=(n in (6,8))
    box(ax,x,1.2,0.95,1.5,"",fc=(KEEP_L if ev else SRC_L),ec=(KEEP if ev else SRC))
    ax.text(x+0.475,2.35,f"$x_{n}$",ha="center",fontsize=6.8,fontweight="bold")
    ax.text(x+0.475,2.0,fr[n],ha="center",fontsize=5.6)
    ax.text(x+0.475,1.65,f"$b={t8['dens'][n]}$",ha="center",fontsize=5.8)
    ax.text(x+0.475,1.32,"$\\beta"+"=\\,$"+betti_str(B_[n]),ha="center",fontsize=6.2)
    if n<8: arrow(ax,(x+0.95,1.95),(x+1.03,1.95),shrink=0.0,lw=0.7)
ax.text(0,3.0,"Eight steps $3025/3\\to12100/3$ (target $q=2$)",fontsize=7.8,fontweight="bold",va="top")
for (n,lab) in [(6,"event at step 6:\n$D\\!:\\{55\\}\\to\\{10,55\\}$"),(8,"event at step 8:\n$D\\!:\\{10,55\\}\\to\\{10,22,55\\}$")]:
    x=n*1.03
    ax.text(x+0.475,0.8,lab,ha="center",fontsize=5.6,color=KEEP,va="top")
ax.text(0,0.65,"steps 0--5: $D=\\{55\\}$,",fontsize=5.8,va="top"); ax.text(0,0.4,"$K_{\\rm move}$ = point",fontsize=5.8,va="top")
# complexes
cx={0:(1.0,-1.9),6:(4.3,-1.9),8:(7.6,-1.9)}
for n,(X,Y) in cx.items():
    Dn=D_[n]; K=complex_of(Dn)
    pts=circ(len(Dn),0.8) if len(Dn)>1 else [(0,0)]
    pos={d:(X+p_[0],Y+p_[1]) for d,p_ in zip(sorted(Dn),pts)}
    for u,v in K['E']: seg(ax,pos[u],pos[v],lw=1.0,c="#444")
    for d in Dn: node(ax,pos[d][0],pos[d][1],str(d),r=0.22,fs=6.5)
    ax.text(X,Y-1.15,f"$K_{{\\rm move}}(x_{n})$, $\\beta_1={B_[n][1] if len(B_[n])>1 else 0}$",ha="center",fontsize=6.3)
ax.text(5.9,-3.45,"abstract layout; edges by the divisor-interval rule",fontsize=5.8,style="italic",ha="center")
save(fig,"fig15_eight_step"); DATA['fig15']={'orbit':fr,'D':D_,'betti':B_,'dens':t8['dens']}
# -------- Fig 16: 375-step
x375=Fr((11*53*67)**2,7); o375=orbit(x375,375)
bs=[t.denominator for t in o375]; nD=[len(Dset(t)) for t in o375]
fig,axs=plt.subplots(1,2,figsize=(W,2.6),gridspec_kw={'width_ratios':[1.4,1]})
ax=axs[0]; panel(ax,"a","denominator $b_n$, $n=0,\\dots,375$"); ax.plot(range(376),bs,color=SRC,lw=0.7); ax.set_yscale("log"); ax.set_xlabel("step $n$"); sp(ax)
for n in (372,373,375): ax.axvline(n,color=LOST,lw=0.5,ls=":")
ax=axs[1]; panel(ax,"b","last 12 steps")
ns=list(range(364,376)); b1=[]
for n in ns:
    D=Dset(o375[n]); bt=bettiD(D); b1.append(bt[1] if len(bt)>1 else 0)
ax.step(ns,[nD[n] for n in ns],where="post",color=KEEP,marker="o",ms=3,label="$|D|$"); ax.step(ns,b1,where="post",color=LOST,marker="s",ms=3,ls="--",label="$\\beta_1$"); ax.legend(frameon=False,loc="upper left"); ax.set_xlabel("step $n$"); sp(ax)
save(fig,"fig16_375_step"); DATA['fig16']={'events':{372:[106],373:[22],375:[134]},'b1_last12':dict(zip(ns,b1)),'nD_last12':{n:nD[n] for n in ns}}
# -------- Fig 17: activation without Betti change; Delta beta_1 distribution + mechanism
rows=[]
for l in (5,7,11,13): rows+=json.load(open('../results/census_l%d.json'%l))['rows']
from collections import Counter
dc=Counter(r['db'][1] if len(r['db'])>1 else 0 for r in rows)
mech=Counter(); 
for r in rows:
    d1=r['db'][1] if len(r['db'])>1 else 0
    mech[(r['dead'][1]>0 if len(r['dead'])>1 else False,(r['new'][2]>0) if len(r['new'])>2 else False,'up' if d1>0 else ('down' if d1<0 else 'same'))]+=1
fig,axs=plt.subplots(1,2,figsize=(W,2.7),gridspec_kw={'width_ratios':[1.2,1.3]})
ax=axs[0]; panel(ax,"a","$\\Delta\\beta_1$ over 2,576 $D$-events"); ks=sorted(dc); ax.bar(ks,[dc[k] for k in ks],color=SRC_L,ec=SRC); ax.set_yscale("log"); ax.set_xlabel("$\\Delta\\beta_1$"); ax.set_ylabel("events"); sp(ax)
ax=axs[1]; panel(ax,"b","$(\\text{dead edge?},\\text{new 2-cell?})\\to\\Delta\\beta_1$"); ax.axis("off"); ax.set_xlim(0,6); ax.set_ylim(0,5)
hdr=["dead","new 2c","up","same","down"]
for j,hh in enumerate(hdr): ax.text(0.5+j*1.0,4.5,hh,ha="center",fontsize=6.5,fontweight="bold")
for i,(de,n2) in enumerate([(False,False),(False,True),(True,False),(True,True)]):
    y=3.6-i*0.9; ax.text(0.5,y,"yes" if de else "no",ha="center",fontsize=6.8); ax.text(1.5,y,"yes" if n2 else "no",ha="center",fontsize=6.8)
    for j,k in enumerate(("up","same","down")): ax.text(2.5+j,y,str(mech.get((de,n2,k),0)),ha="center",fontsize=6.8,bbox=dict(fc=("#f1b9b2" if (de,n2,k) in [(False,False,'down')] else "white"),ec="#bbb",pad=1.5))
ax.text(3,0.2,"$(\\text{no},\\text{no})\\to$ down is empty: Theorem (cause)",fontsize=6,ha="center")
save(fig,"fig17_unchanged_betti")
DATA['fig17']={'delta_b1':{int(k):v for k,v in dc.items()},'mech':{str(k):v for k,v in mech.items()}}
# -------- Fig 18/19/20 : the divisor-interval event D={8,22,176} -> D'
D=[8,22,176]; D2=Dset(orbit(Fr(176**2,7),6)[5+1]); D1=Dset(orbit(Fr(176**2,7),6)[5])
assert D1==D, (D1,D)
t=analyse(D,D2)
fig,ax=plt.subplots(figsize=(W,2.7)); ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-0.8,5.2); ax.set_ylim(-0.9,2.1)
pts=[(a_,c_) for a_ in range(5) for c_ in range(2)]
label=lambda a_,c_: 2**a_*11**c_
for (a_,c_) in pts:
    d_=label(a_,c_); fc="white"; ec="k"; ls="-"
    if d_ in D: fc,ec=SRC_L,SRC
    elif d_ in D2: fc,ec=KEEP_L,KEEP
    elif d_==1: fc,ec,ls="#eee","k",(0,(2,2))
    else: fc,ec="white",GREY
    node(ax,a_,c_,str(d_),fc=fc,ec=ec,r=0.26,fs=6.5,ls=ls)
for (u,v,col,lab_,dy) in [(8,22,LOST,"interval of $\\{8,22\\}$",-0.5),(8,176,TGT,"interval of $\\{8,176\\}$",1.5)]:
    fu,fv=factor(u),factor(v); a0=min(fu.get(2,0),fv.get(2,0)); a1=max(fu.get(2,0),fv.get(2,0)); c0=min(fu.get(11,0),fv.get(11,0)); c1=max(fu.get(11,0),fv.get(11,0))
    ax.add_patch(Rectangle((a0-0.38,c0-0.38 if dy<0 else c0-0.30),a1-a0+0.76,c1-c0+0.76,fc="none",ec=col,lw=1.3,ls="--",zorder=4))
    ax.text((a0+a1)/2,dy,lab_,ha="center",fontsize=6.3,color=col)
ax.text(2,-0.85,"horizontal: exponent of 2;  vertical: exponent of 11.   blue: $D$;  green: new occurrences $D'\\setminus D$;  dashed: $1$",ha="center",fontsize=6)
save(fig,"fig18_divisor_interval")
DATA['fig18']={'D':D,'Dprime':D2,'pierced':[(8,22),(8,176),(22,176)],'zigzag':{k:v for k,v in t.items() if k!='chk'},'chk':t['chk']}
# fig19: before/after complexes in exponent coordinates (v2, v11): a genuine planar embedding of the grid complex
K=complex_of(D); K2=complex_of(D2)
ex=lambda d: (factor(d).get(2,0), factor(d).get(11,0))
fig,axs=plt.subplots(1,2,figsize=(W,2.5))
for ax in axs: ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-0.6,4.6); ax.set_ylim(-0.8,1.6)
pos1={d:ex(d) for d in D}; pos2={d:ex(d) for d in D2}
for (u,v) in K['E']: seg(axs[0],pos1[u],pos1[v],c=LOST,lw=1.5,ls=(0,(3,2)),z=3)
for d in D: node(axs[0],pos1[d][0],pos1[d][1],str(d),r=0.2,fs=6.5)
panel(axs[0],"a","$K(D)$: $\\beta=(1,1)$; 3 edges die"); axs[0].text(2,-0.65,"exponent of 2 (horizontal), of 11 (vertical)",ha="center",fontsize=5.8)
cs2=cellsets(K2)
for c in cs2[2]:
    xs=[pos2[v] for v in c]; x0_=min(p[0] for p in xs); y0_=min(p[1] for p in xs)
    axs[1].add_patch(Rectangle((x0_,y0_),1,1,fc="#cfe6d2",ec="none",zorder=1))
new_e=[e for e in K2['E'] if e not in K['E']]
for (u,v) in new_e: seg(axs[1],pos2[u],pos2[v],c=KEEP,lw=1.5,z=3)
for d in D2: node(axs[1],pos2[d][0],pos2[d][1],str(d),fc=(KEEP_L if d not in D else SRC_L),ec=(KEEP if d not in D else SRC),r=0.2,fs=6.2)
panel(axs[1],"b","$K(D')$: $f=(9,11,3)$, $\\beta=(1)$")
save(fig,"fig19_before_after"); DATA['fig19']={'f':t['f'],'f2':t['f2'],'b':t['b'],'b2':t['b2']}
json.dump(DATA,open('../results/FIGDATA_b.json','w'),default=str,indent=1)
print('done b')

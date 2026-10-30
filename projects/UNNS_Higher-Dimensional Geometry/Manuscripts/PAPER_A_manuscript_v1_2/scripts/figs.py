import json, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MP
from geo import *

plt.rcParams.update({"font.size":8,"axes.linewidth":0.6,"font.family":"serif","mathtext.fontset":"cm","pdf.fonttype":42})
COL={'L':'#4C78A8','D':'#54A24B','bottom':'#E45756','left':'#F58518','old':'#BBBBBB','fill':'#B279A2','Z':'#9ecae1','K':'#a1d99b','T':'#F58518'}
OUT="../figures/"
meta={}

def setup(ax,d,Q,title=None,pad=0.8,grid=True):
    ax.set_aspect('equal'); ax.set_xlim(-pad,Q[0]+pad); ax.set_ylim(-pad,Q[1]+pad)
    ax.set_xticks(range(0,Q[0]+1,1 if Q[0]<=14 else 2)); ax.set_yticks(range(0,Q[1]+1,1 if Q[1]<=14 else 2))
    ax.tick_params(length=2,labelsize=6.5)
    if grid: ax.grid(True,lw=0.2,color='#dddddd')
    ax.set_xlabel(r"$i$",labelpad=1); ax.set_ylabel(r"$j$",labelpad=1)
    if title: ax.set_title(title,fontsize=8)

def poly(ax,corners,fc,alpha=0.55,ec='k',lw=0.5,hatch=None,zorder=2):
    ax.add_patch(MP(list(corners),closed=True,fc=fc,alpha=alpha,ec=ec,lw=lw,hatch=hatch,zorder=zorder))

def pts(ax,F,d,labels=False,ms=9,color='k'):
    ax.scatter([p[0] for p in F],[p[1] for p in F],s=ms,c=color,zorder=5)
    ax.plot([0],[0],marker='o',mfc='white',mec='k',ms=4,zorder=6,lw=0)
    ax.plot([0],[0],marker='x',color='r',ms=4,zorder=7,lw=0)

def hullpatch(ax,d,s,Q,ec='k',lw=0.9):
    H=hull_poly(Fpts(d,s,Q)); xs,ys=H.exterior.xy
    ax.plot(xs,ys,color=ec,lw=lw,zorder=4)

def tri_hole(ax,d,s):
    t=inv(s,d); A=(0,d);B=(d,0);C=(d,d)
    L=(d-t,d-1); R=(d-1,(s*(d-1))%d)
    poly(ax,[A,L,C],COL['T'],alpha=0.35,hatch='////',lw=0.6,zorder=3); poly(ax,[B,R,C],COL['T'],alpha=0.35,hatch='////',lw=0.6,zorder=3)
    ax.text((A[0]+L[0]+C[0])/3,(A[1]+L[1]+C[1])/3+0.12,r"$T_1^\circ$",ha='center',fontsize=7,zorder=8)
    ax.text((B[0]+R[0]+C[0])/3+0.15,(B[1]+R[1]+C[1])/3,r"$T_2^\circ$",ha='center',fontsize=7,zorder=8)
    return L,R

def label_ABC(ax,d):
    for nm,p,off in (("A",(0,d),(-0.55,0.15)),("B",(d,0),(0.2,-0.6)),(r"$C_0$",(d,d),(0.2,0.2))):
        ax.annotate(nm,p,xytext=(p[0]+off[0],p[1]+off[1]),fontsize=7,zorder=9)

def save(fig,name):
    fig.savefig(OUT+name+".pdf",bbox_inches='tight'); plt.close(fig)

# ---------- Fig 1: occurrence fibre of x0
def fig1():
    d,s=5,2; Q=(5,5)
    fig,ax=plt.subplots(1,2,figsize=(6.6,3.1),gridspec_kw={'width_ratios':[1,1]})
    a=ax[0]; setup(a,d,Q,r"Exponent box and relation lattice $\Lambda_{11}$")
    for i in range(6):
        for j in range(6):
            a.plot(i,j,'.',color='#bbbbbb',ms=3,zorder=1)
    F=Fpts(d,s,Q); pts(a,F,d,ms=14)
    kap=lambda p:5**p[0]*3**p[1]
    for p in sorted(F):
        a.annotate(f"{kap(p)}",p,xytext=(p[0]+0.12,p[1]+0.12),fontsize=5.5,color='#1a4d8f',zorder=9)
    a.add_patch(plt.Rectangle((0,0),5,5,fill=False,ec='#888',lw=0.6,ls='--'))
    a.annotate("deleted origin\n($\\kappa=1$)",(0,0),xytext=(0.5,-0.55),fontsize=6,color='r',arrowprops=dict(arrowstyle='-',lw=0.4,color='r'))
    b=ax[1]; b.axis('off'); b.set_xlim(0,1); b.set_ylim(0,1)
    txt=("$x_0=5^{10}3^{10}/11$\n"
         "$\\kappa=5^i3^j$, $0\\leq i,j\\leq 5$\n"
         "$5^i3^j\\equiv1\\ (\\mathrm{mod}\\ 11)\\Leftrightarrow j\\equiv 2i\\ (\\mathrm{mod}\\ 5)$\n\n"
         "$\\Lambda_{11}=\\Gamma_{5,2}$ ($\\lambda_1=\\lambda_2=1$)\n"
         "$|F|=7$ occurrence indices:\n"
         "$243,\\ 45,\\ 2025,\\ 375,$\n$16875,\\ 3125,\\ 759375$")
    b.text(0.02,0.95,txt,va='top',fontsize=8)
    save(fig,"fig01_fibre"); meta['fig01']=dict(d=d,s=s,Q=Q,kappas=sorted(kap(p) for p in F))

# ---------- Fig 2: Graver cell and punctured origin
def fig2():
    d,s=7,3; Q=(10,7)
    fam=cap_family(d,s,Q)
    Om=omega(d,s,Q); first=(Om[0],Om[1]); 
    fig,ax=plt.subplots(1,2,figsize=(6.8,3.2))
    a=ax[0]; setup(a,d,Q,r"(a) admissible cell, $\Gamma_{7,3}$")
    F=Fpts(d,s,Q); pts(a,F,d)
    w=(1,3); g=(1,3); h=(2,-1)  # example inside lattice: find real example
    G=graver(d,s,10,7)
    # pick an actual admissible cell from the box (7,7) with largest area
    F0,G0,pars,segs=cells_all(d,s,(d,d))
    best=max(pars,key=lambda c:Polygon(c).area)
    poly(a,best,COL['Z'],alpha=0.6,lw=0.8)
    w0=best[0]; g0=(best[1][0]-w0[0],best[1][1]-w0[1]); h0=(best[3][0]-w0[0],best[3][1]-w0[1])
    a.annotate("",xy=best[1],xytext=w0,arrowprops=dict(arrowstyle='->',color='#08519c',lw=1)); a.annotate("",xy=best[3],xytext=w0,arrowprops=dict(arrowstyle='->',color='#08519c',lw=1))
    a.text(w0[0]+g0[0]/2,w0[1]+g0[1]/2+0.3,f"$g={g0}$",fontsize=6.5,color='#08519c'); a.text(w0[0]+h0[0]/2-1.6,w0[1]+h0[1]/2,f"$h={h0}$",fontsize=6.5,color='#08519c')
    a.text(w0[0]-0.6,w0[1]-0.55,f"$w={w0}$",fontsize=6.5)
    meta['fig02']=dict(d=d,s=s,cell=best,g=g0,h=h0)
    b=ax[1]; setup(b,d,Q,r"(b) first outer edge $B\to B+M$")
    pts(b,F,d); hullpatch(b,d,s,Q)
    p,q=first
    b.plot([p[0],q[0]],[p[1],q[1]],color=COL['bottom'],lw=2,zorder=6)
    shifted=[(p[0]-d,p[1]),(q[0]-d,q[1])]
    b.plot([shifted[0][0],shifted[1][0]],[shifted[0][1],shifted[1][1]],color=COL['bottom'],lw=1.5,ls='--',zorder=6)
    poly(b,[p,q,shifted[1],shifted[0]],COL['bottom'],alpha=0.18,lw=0.5,zorder=2)
    b.annotate("corner $B-(d,0)=0\\notin F_Q$",(0,0),xytext=(0.5,2.2),fontsize=6.5,color='r',arrowprops=dict(arrowstyle='->',color='r',lw=0.6))
    b.text(q[0]+0.15,q[1]-0.1,"$B+M$",fontsize=6.5); b.text(d+0.15,-0.55,"$B$",fontsize=6.5)
    save(fig,"fig02_cell"); 

# ---------- Fig 3: exceptional square, nonspecial
def fig3():
    d,s=7,3; Q=(d,d)
    F,G,pars,segs=cells_all(d,s,Q)
    fig,ax=plt.subplots(figsize=(3.8,3.7)); setup(ax,d,Q,r"$\Gamma_{7,3}$, $Q_0=(7,7)$: two open holes")
    for c in pars: poly(ax,c,COL['old'],alpha=0.5,lw=0.4)
    for (p,q) in segs: ax.plot([p[0],q[0]],[p[1],q[1]],color='#666',lw=0.5,zorder=3)
    L,R=tri_hole(ax,d,s); pts(ax,F,d); hullpatch(ax,d,s,Q); label_ABC(ax,d)
    ax.annotate("$P_{d-t}$",L,xytext=(L[0]-1.5,L[1]+0.35),fontsize=6.5); ax.annotate("$P_{d-1}$",R,xytext=(R[0]-0.4,R[1]-0.75),fontsize=6.5)
    save(fig,"fig03_two_holes"); meta['fig03']=dict(d=d,s=s,t=inv(s,d),cells=len(pars),segments=len(segs))

# ---------- Fig 4: zonogon + K for d=11,s=4
def zonogon_tiles(d,s):
    Q=(d,d); pts_=ccw_boundary_points(d,s,Q)
    iA=pts_.index((0,d)); chain=pts_[iA:]+[pts_[0]]   # A ... B  lower-left chain (ccw continues from A)
    steps=[(chain[k+1][0]-chain[k][0],chain[k+1][1]-chain[k][1]) for k in range(len(chain)-1)]
    A=(0,d); upper=[]; tiles=[]
    for v in steps:
        base=A
        for w in upper:
            if cross(w,v)!=0:
                tiles.append((base,(base[0]+w[0],base[1]+w[1]),(base[0]+w[0]+v[0],base[1]+w[1]+v[1]),(base[0]+v[0],base[1]+v[1])))
            base=(base[0]+w[0],base[1]+w[1])
        upper=[v]+upper
    return chain,steps,tiles
def fig4():
    d,s=11,4; t=inv(s,d); Q=(d,d)
    chain,steps,tiles=zonogon_tiles(d,s)
    fig,ax=plt.subplots(figsize=(4.6,4.5)); setup(ax,d,Q,rf"$\Gamma_{{{d},{s}}}$: zonogon $Z$, cell $K$, holes $T_1^\circ,T_2^\circ$")
    for k,c in enumerate(tiles): poly(ax,c,COL['Z'] if k%2==0 else '#c6dbef',alpha=0.8,lw=0.5)
    Kc=((d-t-1,d-s-1),(d-t-1+1,d-s-1+s),(d-t-1+1+t,d-s-1+s+1),(d-t-1+t,d-s-1+1))
    poly(ax,Kc,COL['K'],alpha=0.55,lw=0.8,zorder=3)
    tri_hole(ax,d,s); F=Fpts(d,s,Q); pts(ax,F,d); hullpatch(ax,d,s,Q); label_ABC(ax,d)
    ax.plot([p[0] for p in chain],[p[1] for p in chain],color='#08519c',lw=1.6,zorder=6)
    ax.text(3.6,0.35,"lower-left chain (Graver steps)",fontsize=6.5,color='#08519c')
    ax.text(sum(p[0] for p in Kc)/4-0.15,sum(p[1] for p in Kc)/4-0.1,r"$K$",fontsize=9,zorder=9)
    save(fig,"fig04_zonogon"); meta['fig04']=dict(d=d,s=s,t=t,steps=steps,tiles=len(tiles),K=Kc)
    # self-check: Z ∪ T1 ∪ T2 ∪ K covers hull
    H=hull_poly(F); t1=Polygon([(0,d),(d-t,d-1),(d,d)]); t2=Polygon([(d,0),(d-1,(s*(d-1))%d),(d,d)])
    U=unary_union([Polygon(c) for c in tiles]+[Polygon(Kc),t1,t2]); meta['fig04']['uncovered_area']=H.difference(U).area

# ---------- Fig 5: special classes
def fig5():
    d=7
    fig,ax=plt.subplots(1,2,figsize=(6.8,3.4))
    for k,(s,ttl) in enumerate(((d-1,r"$s\equiv-1$: fan graph, $\beta_1=d$"),(1,r"$s\equiv+1$: $W$ and two holes, $\beta_1=2$"))):
        a=ax[k]; setup(a,d,(d,d),ttl); F,G,pars,segs=cells_all(d,s,(d,d))
        for c in pars: poly(a,c,COL['old'],alpha=0.6,lw=0.5)
        for (p,q) in segs: a.plot([p[0],q[0]],[p[1],q[1]],color='#444',lw=0.6,zorder=3)
        pts(a,F,d); hullpatch(a,d,s,(d,d)); label_ABC(a,d)
        if s==1: tri_hole(a,d,1); a.text(1.6,2.5,r"$W$",fontsize=9)
    save(fig,"fig05_special"); meta['fig05']=dict(d=d)

# ---------- Fig 6: column strip
def fig6():
    d,s=5,2; Q=(8,13); t=inv(s,d)
    F=Fpts(d,s,Q); H=hull_poly(F)
    b=lambda i: d if i==0 else (s*i)%d
    K=lambda i:(Q[1]-b(i))//d
    fig,ax=plt.subplots(figsize=(4.4,6.0)); setup(ax,d,Q,rf"Column strips: $\Gamma_{{5,2}}$, $Q=(8,13)$")
    allc=[]
    for i in range(Q[0]):
        m=min(K(i),K(i+1)); db=b(i+1)-b(i)
        for k in range(m):
            w=(i,b(i)+k*d); c=(w,(w[0]+1,w[1]+db),(w[0]+1,w[1]+db+d),(w[0],w[1]+d)); poly(ax,c,COL['L'] if k%2==0 else '#9ecae1',alpha=0.7,lw=0.4); allc.append(c)
        if K(i)!=K(i+1):
            Ti=(i,b(i)+K(i)*d); Tj=(i+1,b(i+1)+K(i+1)*d)
            c=(Ti,Tj,(Tj[0],Tj[1]-d),(Ti[0],Ti[1]-d)); poly(ax,c,COL['bottom'],alpha=0.55,lw=0.4,zorder=3); allc.append(c)
    pts_=ccw_boundary_points(d,s,Q)
    for p,q in zip(pts_,pts_[1:]+pts_[:1]):
        if q[0]>p[0]:   # lower hull piece: translate up
            c=(p,q,(q[0],q[1]+d),(p[0],p[1]+d)); poly(ax,c,COL['D'],alpha=0.45,lw=0.4,zorder=2); allc.append(c)
        elif q[0]<p[0]: # upper hull piece: translate down
            c=(p,q,(q[0],q[1]-d),(p[0],p[1]-d)); poly(ax,c,COL['left'],alpha=0.45,lw=0.4,zorder=2); allc.append(c)
    pts(ax,F,d); hullpatch(ax,d,s,Q)
    U=unary_union([Polygon(c) for c in allc]); meta['fig06']=dict(d=d,s=s,Q=Q,uncovered_area=H.difference(U).area)
    save(fig,"fig06_columns")

# ---------- Fig 7: Pareto records and bottom cell
def fig7():
    d,s,u=13,5,6; Q=(d+u,d); t=inv(s,d); a=d-s; c=d-t
    r=[(s*i)%d for i in range(1,u+1)]; y=min(r); x=r.index(y)+1; M=(x,y)
    records=[]; cur=10**9
    for i,ri in enumerate(r,1):
        if ri<cur: records.append((i,ri)); cur=ri
    g1=(1,-a); g2=(c,-1); g=g1 if cross(g1,M)>=x*y else g2
    fig,ax=plt.subplots(figsize=(6.4,3.6)); ax.set_aspect('equal'); ax.set_xlim(d-3.5,d+u+1.5); ax.set_ylim(-1.2,d+0.6)
    ax.grid(True,lw=0.2,color='#ddd'); ax.set_xlabel(r"$i$"); ax.set_ylabel(r"$j$"); ax.tick_params(labelsize=6.5)
    ax.set_title(rf"Record minima of $s i\ \mathrm{{mod}}\ d$ ($d=13,s=5$, $u=6$): $M=({x},{y})$, $g={g}$",fontsize=8)
    F=Fpts(d,s,(d+u,d)); 
    ax.scatter([p[0] for p in F],[p[1] for p in F],s=10,c='k',zorder=5)
    B=(d,0); w=(B[0]-g[0],B[1]-g[1])
    cell=(w,B,(B[0]+x,B[1]+y),(w[0]+x,w[1]+y)); poly(ax,cell,COL['bottom'],alpha=0.35,lw=0.8)
    poly(ax,[B,(B[0]+x,B[1]+y),(d,y)],'#222',alpha=0.35,lw=0.8,zorder=4)
    ax.annotate("",xy=(B[0]+x,B[1]+y),xytext=B,arrowprops=dict(arrowstyle='->',lw=1.1,color='k')); ax.text(B[0]+x/2+0.15,y/2-0.45,r"$M$",fontsize=8)
    ax.annotate("",xy=B,xytext=w,arrowprops=dict(arrowstyle='->',lw=1.1,color='#a50f15')); ax.text(w[0]-1.4,w[1]+0.5,r"$g$",fontsize=8,color='#a50f15')
    ax.text(d+0.2,y+0.25,r"$\Delta_B$",fontsize=8); ax.text(B[0]-0.1,-0.9,"$B$",fontsize=7)
    for (i,ri) in records:
        ax.plot(d+i,ri,'o',mfc='none',mec='#1a4d8f',ms=8,zorder=6); ax.text(d+i-0.1,ri+0.35,f"$r_{{{i}}}={ri}$",fontsize=6,color='#1a4d8f')
    ax.text(0.99,0.03,f"$\\mathrm{{cr}}(g,M)={cross(g,M)}\\ \\geq\\ xy={x*y}$\n$a={a},\\ c={c},\\ t={t}$\n$\\max\\{{y+ax,\\,x+cy\\}}={max(y+a*x,x+c*y)}$",fontsize=7,transform=ax.transAxes,ha='right',va='bottom')
    save(fig,"fig07_records"); meta['fig07']=dict(d=d,s=s,u=u,M=M,g=g,records=records,cr=cross(g,M),xy=x*y)

# ---------- Fig 8: boundary chain
def classcolor(c): return {'R':'#4C78A8','C':'#54A24B','T':'#F58518','N':'#999999'}[c]
def fig8():
    d,s=7,3; Q=(11,12)
    F=Fpts(d,s,Q); Om=omega(d,s,Q)
    fig,ax=plt.subplots(figsize=(4.9,5.0)); setup(ax,d,Q,rf"Outer chain $\Omega$ for $\Gamma_{{7,3}}$, $Q=(11,12)$")
    ax.axvline(d,color='#888',lw=0.5,ls='--'); ax.axhline(d,color='#888',lw=0.5,ls='--')
    for p in F: ax.scatter(*p,s=12,c=classcolor(cls(p,d)),zorder=5,edgecolors='k',linewidths=0.2)
    hullpatch(ax,d,s,Q,lw=0.6)
    ax.plot([p[0] for p in Om],[p[1] for p in Om],color='k',lw=2,zorder=6)
    ax.scatter([d],[d],s=60,facecolors='none',edgecolors='r',zorder=7); ax.annotate("$C_0$",(d,d),xytext=(d+0.2,d-0.7),fontsize=7,color='r')
    for k,(nm,c) in enumerate((("R","R"),("C","C"),("T","T"),("N","N"))):
        ax.scatter([],[],s=18,c=classcolor(c),label=f"class {nm}",edgecolors='k',linewidths=0.2)
    ax.legend(fontsize=6.5,loc='lower right',frameon=True)
    word="".join(cls(p,d) for p in Om)
    ax.text(-0.5,Q[1]+0.1,"word of $\\Omega$: "+word,fontsize=6.5)
    save(fig,"fig08_chain"); meta['fig08']=dict(d=d,s=s,Q=Q,omega=Om,word=word,C0_on_boundary=bool(Point(d,d).distance(hull_poly(F).exterior)<1e-9))

# ---------- Fig 9: sweeps
def draw_cap(ax,d,s,Q,show_old=True,legend=False):
    r,U,H,fam=check_cover(d,s,Q,return_union=True)
    F0,G0,pars,segs=cells_all(d,s,(d,d))
    if show_old:
        for c in pars: poly(ax,c,COL['old'],alpha=0.45,lw=0.3)
        for c in fill_cells(d,s,Q): poly(ax,c,COL['fill'],alpha=0.4,lw=0.4)
    for k in ('L','D','bottom','left'):
        for c in fam[k]: poly(ax,c,COL[k],alpha=0.45,lw=0.5,zorder=3)
    F=Fpts(d,s,Q); pts(ax,F,d,ms=7); hullpatch(ax,d,s,Q)
    ax.axvline(d,color='#777',lw=0.4,ls=':'); ax.axhline(d,color='#777',lw=0.4,ls=':')
    return r,fam
def fig9():
    d,s,Q=7,3,(11,12)
    fig,ax=plt.subplots(figsize=(4.9,5.0)); setup(ax,d,Q,rf"Sweep cells: $\Gamma_{{7,3}}$, $Q=(11,12)$")
    r,fam=draw_cap(ax,d,s,Q)
    for k,lab in (('L',"L-cells $P(w;w'-w,(-d,0))$"),('D',"D-cells $P(w;w'-w,(0,-d))$"),('bottom',"bottom cell"),('left',"left cell")):
        ax.add_patch(MP([(0,0)],fc=COL[k],alpha=0.5,label=lab))
    ax.add_patch(MP([(0,0)],fc=COL['old'],alpha=0.5,label=r"cells of $U_0$")); ax.add_patch(MP([(0,0)],fc=COL['fill'],alpha=0.5,label="hole-filling cells")) 
    ax.legend(fontsize=6,loc='upper center',bbox_to_anchor=(0.5,-0.12),ncol=3,frameon=False)
    save(fig,"fig09_sweeps"); meta['fig09']=dict(d=d,s=s,Q=Q,uncovered_area=r,counts={k:len(fam[k]) for k in ('L','D','bottom','left')})

# ---------- Fig 10: bottom / left cells
def fig10():
    d,s=7,3
    fig,ax=plt.subplots(1,2,figsize=(6.9,3.4))
    for a,(Q,ttl) in zip(ax,(((11,7),r"(a) $u=4,\ v=0$: bottom cell"),((7,11),r"(b) $u=0,\ v=4$: left cell"))):
        setup(a,d,Q,ttl); r,fam=draw_cap(a,d,s,Q); 
        meta.setdefault('fig10',{})[str(Q)]=dict(uncovered_area=r,M=fam.get('_M'),g=fam.get('_g'),M2=fam.get('_M2'),g2=fam.get('_g2'))
    save(fig,"fig10_endcells")

# ---------- Fig 11: complete coverage
def fig11():
    d,s=5,2
    fig,ax=plt.subplots(1,3,figsize=(7.2,3.1))
    for a,(Q,ttl) in zip(ax,(((8,5),r"(a) one-sided: $Q=(8,5)$"),((8,7),r"(b) mixed: $Q=(8,7)$"),((8,8),r"(c) $Q=(8,8)$: $C_0$ interior"))):
        setup(a,d,Q,ttl,pad=0.6); r,fam=draw_cap(a,d,s,Q)
        a.scatter([d],[d],s=40,facecolors='none',edgecolors='r',zorder=8)
        meta.setdefault('fig11',{})[str(Q)]=dict(uncovered_area=r)
    save(fig,"fig11_cap")

# ---------- Fig 12: x0 vs x1
def fig12():
    d,s=5,2
    fig,ax=plt.subplots(1,2,figsize=(6.8,3.2))
    a=ax[0]; Q=(5,5); setup(a,d,Q,r"$x_0=5^{10}3^{10}/11$: $Q=(5,5)$, two holes")
    F,G,pars,segs=cells_all(d,s,Q)
    for c in pars: poly(a,c,COL['old'],alpha=0.55,lw=0.4)
    for (p,q) in segs: a.plot([p[0],q[0]],[p[1],q[1]],color='#444',lw=0.6,zorder=3)
    tri_hole(a,d,s); pts(a,F,d); hullpatch(a,d,s,Q); label_ABC(a,d)
    b=ax[1]; Q=(6,5); setup(b,d,Q,r"$x_1=5^{12}3^{10}/11$: $Q=(6,5)$, $U=\mathrm{conv}$")
    r,fam=draw_cap(b,d,s,Q)
    meta['fig12']=dict(x0_points=len(Fpts(d,s,(5,5))),x1_points=len(Fpts(d,s,(6,5))),uncovered_area_x1=r,
                       x0_complement_area=hull_poly(Fpts(d,s,(5,5))).difference(unary_union([Polygon(c) for c in cells_all(d,s,(5,5))[2]])).area)
    save(fig,"fig12_example")

if __name__=="__main__":
    for f in (fig1,fig2,fig3,fig4,fig5,fig6,fig7,fig8,fig9,fig10,fig11,fig12): f()
    json.dump(meta,open(OUT+"figure_data.json","w"),indent=1,default=str)
    print(json.dumps({k:(v if k not in('fig04','fig08') else {kk:vv for kk,vv in v.items() if kk in('uncovered_area','word','C0_on_boundary')}) for k,v in meta.items()},default=str)[:3000])

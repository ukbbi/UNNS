import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from math import gcd, isqrt, log, lcm
from fractions import Fraction as Fr
plt.rcParams.update({'font.family':'serif','font.size':9,'mathtext.fontset':'cm','pdf.fonttype':42,'axes.spines.top':False,'axes.spines.right':False})
BLUE='#1f4e8c'; RED='#b3361f'; GREY='#8a8a8a'; GREEN='#2a7a4b'; GOLD='#b8860b'
def divs(n): return [d for d in range(1,n+1) if n%d==0]
# ---- Fig A: routes through 72
x=72; Ds=[2,3,6]; cols=[BLUE,GREEN,GOLD]
fig,ax=plt.subplots(figsize=(6.2,2.5))
H=194
for i,d in enumerate(Ds):
    step=Fr(d*d,d-1); y=len(Ds)-i
    v=[x+j*step for j in range(0,int((H-x)/step)+1)]
    ax.hlines(y,x,H,color=cols[i],lw=.6,alpha=.4)
    ax.plot([float(t) for t in v],[y]*len(v),'o',ms=3.6,color=cols[i])
    ax.text(H+3,y,f'$d={d}$, step $d^2/(d-1)={step}$',va='center',fontsize=8,color=cols[i])
L=6;G=1;Dl=L*L//G
for k in range(0,5):
    c=x+k*Dl
    if c<=H: ax.axvline(c,color=RED,lw=1.1,ls='--',zorder=0); ax.text(c,3.72,f'{c}',ha='center',color=RED,fontsize=8)
ax.set_yticks([]); ax.set_xlim(x-6,H+2); ax.set_ylim(.4,4.1); ax.set_xlabel('value'); ax.spines['left'].set_visible(False)
fig.suptitle(r'Routes through $x=72$; common futures $x+j\Delta_{\mathrm{coll}}$ with $\Delta_{\mathrm{coll}}=L^2/G=36$',fontsize=9,x=.35,y=.99)
fig.subplots_adjust(right=.66,left=.03,bottom=.2,top=.88); fig.savefig('figs/fig_routes72.pdf'); plt.close(fig)
# ---- Fig B: R(m)
R=lambda m:len([d for d in range(2,isqrt(m)+1) if m%(d*d)==0])
ms=range(1,401); rs=[R(m) for m in ms]
fig,ax=plt.subplots(figsize=(6.2,2.3))
ax.vlines(list(ms),0,rs,color=BLUE,lw=.8)
sq=[m for m in ms if R(m)==0]
ax.plot(sq,[0]*len(sq),'|',color=GREY,ms=3,alpha=.5,label='squarefree ($R=0$, sources of the graph in Ch. 5)')
ax.set_xlabel('$m$'); ax.set_ylabel('$R(m)$'); ax.legend(frameon=False,loc='upper left',fontsize=8)
ax.set_title(r'Fibre multiplicity $R(m)$ for $m\leq 400$',fontsize=9)
fig.subplots_adjust(left=.08,bottom=.2,right=.99); fig.savefig('figs/fig_Rm.pdf'); plt.close(fig)
# ---- DAG helper
def dag(nodes,edges,pos,fn,title,hl_nodes=(),hl_edges=(),size=(6.2,3.4),lab=True,hl2=()):
    fig,ax=plt.subplots(figsize=size)
    for (a,N,b) in edges:
        (x1,y1),(x2,y2)=pos[a],pos[b]
        c=RED if (a,b) in hl_edges else GREY; lw=1.5 if (a,b) in hl_edges else .7
        ax.annotate('',xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle='-|>',color=c,lw=lw,shrinkA=9,shrinkB=9,mutation_scale=8))
        if lab: ax.text((x1+x2)/2,(y1+y2)/2,str(N),fontsize=6,color=c,ha='center',va='center',bbox=dict(fc='white',ec='none',pad=.3))
    for n in nodes:
        x,y=pos[n]; c=RED if n in hl_nodes else (GREEN if n in hl2 else BLUE)
        ax.text(x,y,str(n),ha='center',va='center',color='white',fontsize=8,bbox=dict(boxstyle='round,pad=.25',fc=c,ec='none'))
    xs=[pos[n][0] for n in nodes]; ys=[pos[n][1] for n in nodes]; ax.set_xlim(min(xs)-.8,max(xs)+.8); ax.set_ylim(min(ys)-.15,max(ys)+.15); ax.set_xticks([]); ax.set_ylabel(r'$\log_{10} m$'); ax.spines['bottom'].set_visible(False)
    fig.suptitle(title,fontsize=9,x=.5,y=.985); fig.subplots_adjust(left=.09,right=.99,bottom=.03,top=.91); fig.savefig(fn); plt.close(fig)
def ed(S): return sorted((m,N,m*(N+1)**2//N) for m in S for N in divs(m) if m*(N+1)**2//N in S)
def Y(n): return log(n,10)
# Fig C: no join
S=[1,4,16,18,25,64,72,81,96,100,2,8,9,32,36,48,50]
px={1:-4.2,4:-4.2,16:-4.6,18:-3.4,25:-5.4,64:-5.6,72:-3.9,96:-2.6,81:-.4,100:.2,2:4.2,8:3.6,9:4.8,32:3.0,36:4.2,48:5.4,50:2.2}
pos={n:(px[n],Y(n)) for n in S}
dag(S,ed(S),pos,'figs/fig_nojoin.pdf',r'Descendants of $1$ (left) and $2$ (right) up to $100$: the only common futures are $81$ and $100$',
    hl_nodes=(81,100),hl_edges=((8,81),(18,81),(9,100),(16,100),(4,16),(1,4),(4,2*0+18) if False else (4,18),(2,8),(2,9)),size=(6.2,3.7),hl2=(1,2))
# Fig D: ancestors 32,300
A=[2,6,8,32,3,9,12,27,48,75,300]
pa={2:-2.5,6:2.5,8:-3.0,9:-1.3,3:0.2,12:.8,27:3.4,48:-.5,75:1.5,32:.5,300:1.8}
pos={n:(pa[n],Y(n)) for n in A}
dag(A,ed(A),pos,'figs/fig_meets.pdf',r'Ancestors of $32$ and $300$: maximal common ancestors $2$ and $6$ are incomparable',
    hl_nodes=(2,6),hl_edges=(),size=(6.2,3.5),hl2=(32,300))
# Fig E: histories of 72 + not graded
Hn=[1,4,18,16,3,10,72]; ph={1:-2.0,4:-2.0,18:-.9,16:-3.0,3:-4.2,10:1.8,72:-1.5}
pos={n:(ph[n],Y(n)) for n in Hn}
dag(Hn,ed(Hn),pos,'figs/fig_hist72.pdf',r'Complete histories of $72$: four paths, $R(72)=3$ predecessors, $H_{\mathrm{hist}}(72)=4$',hl_nodes=(72,),hl_edges=((10,72),),size=(6.2,3.0),hl2=(1,3,10))
Gn=[6,24,27,196,784]; pg={6:0,24:-1.2,27:1.6,96:-1.8,108:0.4,196:-.3,784:0.2}
pos={n:(pg[n],Y(n)) for n in Gn}
dag(Gn,[e for e in ed(Gn) if e[0] in (6,24,27,196) and e[2] in (24,27,196,784) ],pos,'figs/fig_notgraded.pdf',r'Not graded: $6\to27\to784$ (two edges) and $6\to24\to196\to784$ (three edges)',hl_nodes=(784,),hl_edges=((6,27),(27,784),(6,24),(24,196),(196,784)),size=(6.2,2.6),hl2=(6,))
print('ok')

import sys, json, csv, math
import os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','inherited','audit_code')); sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from paths import *; sys.path.insert(0,'.')
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle, Circle
from spec import ORDER
from program_table import program
OUT=FIGD+'/'
plt.rcParams.update({'font.size':9,'font.family':'serif','mathtext.fontset':'cm','axes.spines.top':False,'axes.spines.right':False})
COL={2400:'#c0392b',3:'#2e86c1',35:'#27ae60',4:'#8e44ad',5:'#e67e22','other':'#7f8c8d'}
def col(n): return COL.get(n,COL['other'])
# ---------- Fig 1: exchange cycle
fig,ax=plt.subplots(figsize=(7.2,3.9)); ax.set_xlim(0,10); ax.set_ylim(0,6); ax.axis('off')
nodes={'5':(1.6,3.1),'7':(5.0,5.0),'2':(8.4,3.1)}
for k,(x,y) in nodes.items():
    ax.add_patch(Circle((x,y),0.62,fc='#fdf2e9' if k=='5' else ('#eaf2f8' if k=='7' else '#e8f6f3'),ec='k',lw=1.2))
    ax.text(x,y,r'$v_{%s}$'%k,ha='center',va='center',fontsize=14)
def arr(p,q,rad,txt,tp,ha='center'):
    ax.add_patch(FancyArrowPatch(p,q,connectionstyle=f'arc3,rad={rad}',arrowstyle='-|>',mutation_scale=16,lw=1.6,color='#34495e',shrinkA=24,shrinkB=24))
    ax.text(*tp,txt,ha=ha,va='center',fontsize=8.6,linespacing=1.35)
arr(nodes['5'],nodes['7'],-0.25,r'regime I: $W_{45}$ (top three moves)'+'\n'+r'$\Delta=(0,0,-49,+151)$'+'\n'+r'$k_1\approx z/49$ cycles',(1.7,5.35))
arr(nodes['7'],nodes['2'],-0.25,r'regime II: $W_{11}$'+'\n'+r'$\Delta=(+38,0,0,-2)$'+'\n'+r'$k_2\approx151k_1/2$ cycles',(8.35,5.35))
arr(nodes['2'],nodes['5'],-0.25,r'regime III: $4^{k_3}$,  $\Delta_4=(-2,0,+2,0)$,   $k_3\approx19k_2$ steps',(5.0,1.05))
ax.text(5.0,4.05,'one round',ha='center',fontsize=10,style='italic')
ax.text(5.0,3.35,r'gain $\;\dfrac{151}{49}\cdot 19\cdot 1=\dfrac{2869}{49}\approx58.55$',ha='center',fontsize=10.5)
plt.tight_layout(); plt.savefig(OUT+'fig_exchange.pdf'); plt.savefig(OUT+'fig_exchange.png',dpi=200); plt.close()
# ---------- Fig 2: register cycles
fig,(a1,a2)=plt.subplots(1,2,figsize=(7.6,3.6),gridspec_kw={'width_ratios':[1.35,1]})
# torus path: state (v2 mod 9, v3 mod 5) after each step of W45 (rotation (4,4))
def F(s):
    v2,v3=s
    if v3>=1 and v2>=5: return (v2-5,v3-1),2400
    if v3>=1: return (v2+4,v3-1),3
    return (v2+4,v3+4),35
s=(12,0); pts=[]; mv=[]
for i in range(45):
    pts.append((s[0]%9,s[1]%5)); s,m=F(s); mv.append(m)
for i in range(45):
    x,y=pts[i]; a1.add_patch(Rectangle((x-.5,y-.5),1,1,fc=col(mv[i]),ec='w',alpha=.85))
    a1.text(x,y,str(i),ha='center',va='center',fontsize=6.6,color='w')
a1.set_xlim(-.5,8.5); a1.set_ylim(-.5,4.5); a1.set_aspect('equal'); a1.set_xticks(range(9)); a1.set_yticks(range(5))
a1.set_xlabel(r'$v_2\ \mathrm{mod}\ 9$'); a1.set_ylabel(r'$v_3\ \mathrm{mod}\ 5$')
a1.set_title(r'(a) regime I: step index $i$ on $\mathbb{Z}/9\times\mathbb{Z}/5$',fontsize=9)
for k,l in [(2400,'2400'),(3,'3'),(35,'35')]: a1.add_patch(Rectangle((0,0),0,0,fc=col(k),label=l))
a1.legend(loc='upper center',bbox_to_anchor=(0.5,-0.22),ncol=3,frameon=False,fontsize=8)
# W11 ring
seq=[4,35,3,3,3,3,35,3,3,3,3]; regs=[(0,0)]
def G(s):
    v3,v5=s
    if v3>=1: return (v3-1,v5)
    if v5>=1: return (v3+4,v5-1)
    return (v3,v5+2)
s=(0,0)
for m in seq:
    regs.append(G(s)); s=regs[-1]
n=len(seq)
for i,m in enumerate(seq):
    th=2*math.pi*i/n+math.pi/2; x,y=math.cos(-th+math.pi)*1.0, math.sin(-th+math.pi)*1.0
    a2.add_patch(Circle((x,y),.2,fc=col(m),ec='k',lw=.6)); a2.text(x,y,str(m),ha='center',va='center',fontsize=7.2,color='w')
    r=1.42; a2.text(r*x,r*y,r'$(%d,%d)$'%regs[i],ha='center',va='center',fontsize=6.8)
a2.set_xlim(-1.9,1.9); a2.set_ylim(-1.9,1.9); a2.set_aspect('equal'); a2.axis('off')
a2.set_title(r'(b) regime II: $(v_3,v_5)$ before each move',fontsize=9)
a2.text(0,0,r'$W_{11}$'+'\n11 moves',ha='center',va='center',fontsize=9)
plt.tight_layout(); plt.savefig(OUT+'fig_registers.pdf'); plt.savefig(OUT+'fig_registers.png',dpi=200); plt.close()
# ---------- Fig 3: anatomy with real itinerary strip (family (0,0), t=0)
rows,fin,nt=program(0,0)
fig=plt.figure(figsize=(7.6,4.9)); gs=fig.add_gridspec(3,1,height_ratios=[0.8,1.15,1.15],hspace=0.9)
ax=fig.add_subplot(gs[0]); 
segs=[]; tot=0
for r in rows:
    L=len(r['word'])*r['c']; segs.append((r['word'],r['c'],L)); tot+=L
big=[('prefix',0,0)]
x=0; labels=[]
parts=[('regime I\n$W_{45}^{1020}$',45*1020+8+17+0,'#fadbd8'),('regime II\n$W_{11}^{77036}$',11*77036,'#d6eaf8'),('regime III\n$4^{1463697}$',1463697+9,'#e8daef')]
# exact: sum by role
n_pre=1; n_w45=45*1020; n_conn=17; n_w11=11*77036; n_tail=1+4; n_4=1463697
cum=0
for lab,n,c in [('prefix',n_pre,'#bbb'),('regime I',n_w45,'#fadbd8'),('conn.',n_conn,'#bbb'),('regime II',n_w11,'#d6eaf8'),('tail',n_tail,'#bbb'),('regime III',n_4,'#e8daef')]:
    ax.barh(0,n,left=cum,color=c,ec='k',lw=.6,height=.6)
    if n/ (n_pre+n_w45+n_conn+n_w11+n_tail+n_4) > .05: ax.text(cum+n/2,0,lab+f'\n{n:,} moves',ha='center',va='center',fontsize=8)
    cum+=n
ax.annotate('regime I\n(45,900 moves)',xy=(30000,0.3),xytext=(180000,-1.05),fontsize=7.5,ha='left',arrowprops=dict(arrowstyle='-',lw=.6)); ax.set_ylim(-1.3,.5); ax.set_xlim(0,cum); ax.set_yticks([]); ax.set_xticks([0,5e5,1e6,1.5e6,2e6]); ax.set_xticklabels(['0','0.5M','1.0M','1.5M','2.0M']); ax.set_xlabel('step within the round, family $(a,\\rho)=(0,0)$, $t=0$',fontsize=8)
ax.set_title(f'(a) one round, {cum:,} moves; steps are drawn to scale',fontsize=9,loc='left')
ax.spines['left'].set_visible(False)
def tiles(axx,mvs,title,per=None):
    n=len(mvs)
    for i,m in enumerate(mvs):
        axx.add_patch(Rectangle((i,0),1,1,fc=col(m),ec='w',lw=.6)); axx.text(i+.5,.5,str(m) if m!=2400 else '2400',ha='center',va='center',fontsize=4.8 if m==2400 else 6.5,color='w',rotation=90 if m==2400 else 0)
    axx.set_xlim(0,n); axx.set_ylim(0,1); axx.axis('off'); axx.set_title(title,fontsize=8.5,loc='left')
# expand first 45 moves of W45 (first block) and W11 + around handover
w45=rows[1]['word']; w11=[r for r in rows if len(r['word'])==11][0]['word']
conn=[r['word'][0] for r in rows[2:20]]
ax2=fig.add_subplot(gs[1]); tiles(ax2,[5]+w45+w45[:5],r'(b) start of the round: one move of $5$, then $W_{45}$ (45 moves), then its repetition begins')
ax3=fig.add_subplot(gs[2]); tiles(ax3,w11+w11+[35]+[3]*4+[4]*6,r'(c) regime II: two periods of $W_{11}$; hand-over $35,\,3^4$; then the run $4^{k_3}$ (first 6 moves)')
plt.savefig(OUT+'fig_anatomy2.pdf',bbox_inches='tight'); plt.savefig(OUT+'fig_anatomy2.png',dpi=200,bbox_inches='tight'); plt.close()
# ---------- Fig 4: return map
tab=list(csv.DictReader(open(INH+'/return_map_table_audit.csv')))
d={}
for r in tab:
    d[(int(r['a']),int(r['z_mod_49']))]=int(r['delta'])
pred=json.load(open(OUTD+'/predicted_returns.json'))
fig,axs=plt.subplots(1,3,figsize=(8.4,3.0))
ax=axs[0]
for a,mk,c in [(0,'o','#2e86c1'),(1,'s','#c0392b')]:
    ax.plot(range(49),[d[(a,r)] for r in range(49)],mk,ms=3,color=c,label=f'$a={a}$')
ax.axhline(0,color='k',lw=.5); ax.set_xlabel(r'$r=z\ \mathrm{mod}\ 49$'); ax.set_ylabel(r'$\delta_{a,r}$'); ax.legend(frameon=False,fontsize=8); ax.set_title('(a) correction table',fontsize=9)
ax=axs[1]
js=[p[0] for p in pred]; zs=[p[2] for p in pred]; ns=[p[3] for p in pred]
ax.loglog(zs,ns,'-',color='#7f8c8d',lw=.8)
for j,(z,n) in enumerate(zip(zs,ns)):
    ax.loglog([z],[n],'o' if j<=2 else 'o',mfc='#c0392b' if j<=2 else 'w',mec='#c0392b',ms=5)
    ax.annotate(f'$s_{j}$',(z,n),textcoords='offset points',xytext=(4,-9),fontsize=7)
ax.set_xlabel('$z$'); ax.set_ylabel('step number $n$'); ax.set_title('(b) successive returns',fontsize=9)
ax.text(.04,.9,'filled: executed directly\nopen: from Theorem 5.1',transform=ax.transAxes,fontsize=6.8,va='top')
ax=axs[2]
from fractions import Fraction
dev=[abs(float(Fraction(zs[j+1],zs[j])-Fraction(2869,49))) for j in range(len(zs)-1)]
ax.semilogy(range(1,len(zs)),dev,'o-',ms=4,color='#34495e')
ax.set_xlabel('$j$'); ax.set_ylabel(r'$|z_j/z_{j-1}-2869/49|$'); ax.set_title('(c) approach to the gain $2869/49$',fontsize=9)
plt.tight_layout(); plt.savefig(OUT+'fig_returnmap2.pdf'); plt.savefig(OUT+'fig_returnmap2.png',dpi=200); plt.close()
# ---------- Fig 5: itinerary across rounds
D=json.load(open(INH+'/certificate_audit.json'))
fam={(e['a'],e['rho']):e for e in D}
steps=json.load(open(OUTD+'/predicted_returns.json'))
Rows=[]
for j in range(len(steps)-1):
    _,a,z,n,_s=steps[j]; rho=(z-50000)%98; t=(z-50000)//98
    e=fam[(a,rho)]
    b1,b2=e['blocks']; (w1,c1,s1),(w2,c2,s2)=b1,b2
    run=e['run1'][-1]; k3=run[1]+run[2]*t
    k1=c1+s1*t; k2=c2+s2*t
    Rows.append((j,45*k1,11*k2,k3))
fig,(a1,a2)=plt.subplots(1,2,figsize=(7.6,3.0))
J=[r[0] for r in Rows]
a1.semilogy(J,[r[3] for r in Rows],'o-',color='#8e44ad',label='length of final run $4^{k_3}$')
a1.semilogy(J,[r[1]+r[2]+r[3] for r in Rows],'s--',color='#34495e',label='moves in the round')
a1.set_xlabel('round $j$'); a1.set_ylabel('moves'); a1.legend(frameon=False,fontsize=7.5,loc='upper left'); a1.set_title('(a) growth of the itinerary',fontsize=9)
for j,r in zip(J,Rows):
    T=r[1]+r[2]+r[3]
    a2.bar(j,r[1]/T,color='#c0392b'); a2.bar(j,r[2]/T,bottom=r[1]/T,color='#2e86c1'); a2.bar(j,r[3]/T,bottom=(r[1]+r[2])/T,color='#8e44ad')
a2.set_xlabel('round $j$'); a2.set_ylabel('share of moves'); a2.set_title('(b) block shares approach fixed proportions',fontsize=9)
plt.tight_layout(); plt.savefig(OUT+'fig_itinerary.pdf'); plt.savefig(OUT+'fig_itinerary.png',dpi=200); plt.close()
print('ok', Rows[:3])

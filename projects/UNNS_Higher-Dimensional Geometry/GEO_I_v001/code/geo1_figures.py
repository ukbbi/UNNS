"""Figures for GEO-I v001, computed from exact data (geo1lib). Projections only; every plotted point is an exact integer/rational datum."""
import sys, os, itertools
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from geo1lib import *
from fractions import Fraction as Fr
from math import prod
import numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
FD=os.path.join(HERE,'..','figures'); os.makedirs(FD,exist_ok=True)
plt.rcParams.update({'font.size':9,'figure.dpi':150,'axes.grid':True})
def lat(x):
    x=Fr(x); a,b=x.numerator,x.denominator; f=factor(a)
    ps=sorted(p for p,e in f.items() if e//2); h=[f[p]//2 for p in ps]; pts=[]
    allp=list(itertools.product(*[range(e+1) for e in h]))
    for k in allp:
        if any(k): pts.append((k,(prod(p**e for p,e in zip(ps,k))-1)%b==0))
    return ps,h,b,pts
# F1: 3600 box (3D) and 44100 box (4D via two 3D slices + parallel coordinates)
ps,h,b,pts=lat(3600)
fig=plt.figure(figsize=(9,4)); ax=fig.add_subplot(121,projection='3d')
for k,ok in pts+[((0,0,0),False)]:
    ax.scatter(*k,c='C0' if ok else 'lightgray',s=40 if ok else 20)
ax.scatter(0,0,0,c='k',marker='x'); ax.set_xlabel('alpha_2 (v2/2)'); ax.set_ylabel('alpha_3'); ax.set_zlabel('alpha_5')
ax.set_title('m=3600: 11 routes = box 3x2x2 minus origin')
ps4,h4,b4,pts4=lat(44100); ax2=fig.add_subplot(122)
for k,ok in pts4:
    ax2.plot(range(4),k,'-o',alpha=.5,ms=3)
ax2.set_xticks(range(4)); ax2.set_xticklabels(['a2','a3','a5','a7']); ax2.set_title('m=44100: 15 routes, 4 coordinates (parallel coordinates)')
fig.tight_layout(); fig.savefig(os.path.join(FD,'fig1_integer_boxes.png')); plt.close(fig)
# F2: rational cut 2304/5 in (alpha2,alpha3) grid
ps,h,b,pts=lat(Fr(2304,5))
fig,ax=plt.subplots(figsize=(4.8,3.6))
for k,ok in pts+[((0,0),False)]:
    ax.scatter(*k,c='C3' if ok else 'lightgray',s=70 if ok else 40,zorder=3)
    ax.annotate(str(prod(p**e for p,e in zip(ps,k))),k,textcoords='offset points',xytext=(4,4),fontsize=7)
ax.set_xlabel('alpha_2'); ax.set_ylabel('alpha_3'); ax.set_title('x=2304/5: kept points d=6,16 (red); lcm(6,16)=48 is a hole')
ax.annotate('',xy=(4,1),xytext=(1,1),arrowprops=dict(arrowstyle='->',color='C3',alpha=.4))
fig.tight_layout(); fig.savefig(os.path.join(FD,'fig2_rational_cut.png')); plt.close(fig)
# F3: SELECT-II from 6 in (v2,v3,v7) ; F4: histories of 72 in (v2,v3,v5)+height
def v(m,ps): return tuple(val(m,p) for p in ps)
fig=plt.figure(figsize=(9,4)); ax=fig.add_subplot(121,projection='3d'); P=(2,3,7)
o=v(6,P); ax.scatter(*o,c='k',s=40); ax.text(*o,' 6')
for N,mp in succ(6):
    e=v(mp,P); ax.quiver(*o,*(np.array(e)-np.array(o)),color='g',arrow_length_ratio=.12)
    ax.scatter(*e,c='g',s=30); ax.text(*e,' %d (N=%d)'%(mp,N))
ax.set_xlabel('v2');ax.set_ylabel('v3');ax.set_zlabel('v7'); ax.set_title('SELECT-II edges from 6 (exact displacements)')
ax=fig.add_subplot(122,projection='3d'); P=(2,3,5)
hist=[[1,4,16,72],[1,4,18,72],[3,16,72],[10,72]]
for i,hh in enumerate(hist):
    pts_=np.array([v(m,P) for m in hh]); ax.plot(pts_[:,0],pts_[:,1],pts_[:,2],'-o',label=' -> '.join(map(str,hh)),color='C%d'%i)
ax.legend(fontsize=6); ax.set_xlabel('v2');ax.set_ylabel('v3');ax.set_zlabel('v5'); ax.set_title('4 complete histories of 72 (3D projection)')
fig.tight_layout(); fig.savefig(os.path.join(FD,'fig3_select2_valuation.png')); plt.close(fig)
# F5: relation 6 -> 784: path polylines in (v2,v3,v7)
paths=[[6,27,784],[6,24,96,784],[6,24,196,784],[6,49,196,784]]
fig=plt.figure(figsize=(5.5,4.5)); ax=fig.add_subplot(111,projection='3d'); P=(2,3,7)
for i,pp in enumerate(paths):
    a=np.array([v(m,P) for m in pp]); ax.plot(a[:,0],a[:,1],a[:,2],'-o',label='%d edges: %s'%(len(pp)-1,'>'.join(map(str,pp))))
ax.legend(fontsize=6); ax.set_xlabel('v2');ax.set_ylabel('v3');ax.set_zlabel('v7'); ax.set_title('Ungradedness = relation 2D(1)+D(6)=D(2)+D(27)')
fig.tight_layout(); fig.savefig(os.path.join(FD,'fig4_ungraded_relation.png')); plt.close(fig)
# F6: orbit of 72: three strands; F7: g=11 R(n)
xs=[72]
for _ in range(40): xs.append(Cstep(xs[-1]))
fig,axs=plt.subplots(1,2,figsize=(9,3.6))
for ph in range(3):
    seq=xs[ph::3]; axs[0].plot([val(t,2) for t in seq],[val(t,3) for t in seq],'-o',ms=3,label='phase %d'%ph)
axs[0].set_xlabel('v2'); axs[0].set_ylabel('v3'); axs[0].set_title('orbit of 72, valuation plane: 3 parallel strands, step (+2,0)'); axs[0].legend()
axs[1].plot(range(len(xs)),[R(t) for t in xs],'o-',ms=3); axs[1].set_xlabel('n'); axs[1].set_ylabel('R(x_n)'); axs[1].set_title('fibre size along the orbit of 72')
fig.tight_layout(); fig.savefig(os.path.join(FD,'fig5_orbit72_strands.png')); plt.close(fig)
x=Fr(67500**2,11); ys=[x]
for _ in range(120): ys.append(Fr(Cstep(ys[-1])))
fig,axs=plt.subplots(1,2,figsize=(9,3.6))
axs[0].plot(range(121),[len(fibre_q(t)) for t in ys],'.-'); axs[0].plot(range(121),[7+2*(n//8) for n in range(121)],'r--',lw=.8,label='7+2*floor(n/8) (Vol II F.T50)'); axs[0].legend(); axs[0].set_xlabel('n'); axs[0].set_ylabel('R(x_n)'); axs[0].set_title('g=11 benchmark: R quasi-linear, slope 1/4')
ex=[]
for t in ys[:41]:
    a=t.numerator; ex.append((val(a,2)//2,val(a,3)//2,val(a,5)//2))
a=np.array(ex); axs[1].plot(a[:,1],range(len(a)),'o-',ms=3,label='box side h_3'); axs[1].plot(a[:,2],range(len(a)),'s-',ms=3,label='box side h_5'); axs[1].plot(a[:,0],range(len(a)),'^-',ms=3,label='box side h_2'); axs[1].set_xlabel('half-exponent'); axs[1].set_ylabel('n'); axs[1].set_title('box sides: h_3 grows by 1 per period; h_2 oscillates; h_5 fixed'); axs[1].legend(fontsize=7)
fig.tight_layout(); fig.savefig(os.path.join(FD,'fig6_g11_growth.png')); plt.close(fig)
print('figures ok')

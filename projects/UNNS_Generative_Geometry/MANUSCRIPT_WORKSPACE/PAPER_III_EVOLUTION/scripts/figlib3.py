"""Drawing conventions for Paper III figures. Colour is never the only cue (line style / marker / hatch / text)."""
import os, json, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Polygon, FancyArrowPatch, Rectangle
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(HERE,"..","figures")
os.makedirs(OUT,exist_ok=True)
SRC,TGT,KEEP,LOST="#1f5fa8","#17807e","#2e8b3d","#c0392b"
UNC,UNC_E,WIT,GREY="#f8c98a","#c47a12","#b0189e","#9aa5ad"
SRC_L,TGT_L,KEEP_L,LOST_L="#aecbeb","#a9dcd9","#bfe3c4","#f1b9b2"
plt.rcParams.update({"font.size":8,"axes.titlesize":8.5,"axes.labelsize":8,"legend.fontsize":7,"xtick.labelsize":7,"ytick.labelsize":7,
  "pdf.fonttype":42,"ps.fonttype":42,"hatch.linewidth":0.6,"axes.linewidth":0.6})
W=6.2
DATA={}
def save(fig,name):
    fig.savefig(os.path.join(OUT,name+".pdf"),bbox_inches="tight",pad_inches=0.03); plt.close(fig)
def node(ax,x,y,txt,fc="white",ec="k",r=0.28,fs=7,ls="-",lw=0.8,hatch=None,z=5,bold=False):
    c=Circle((x,y),r,fc=fc,ec=ec,lw=lw,ls=ls,zorder=z,hatch=hatch); ax.add_patch(c)
    ax.text(x,y,txt,ha="center",va="center",fontsize=fs,zorder=z+1,fontweight="bold" if bold else "normal")
def box(ax,x,y,w,h,txt="",fc="white",ec="k",fs=7,ls="-",lw=0.8,hatch=None,z=3,ha="center",va="center",rs=0.04):
    p=FancyBboxPatch((x,y),w,h,boxstyle=f"round,pad=0,rounding_size={rs}",fc=fc,ec=ec,lw=lw,ls=ls,hatch=hatch,zorder=z); ax.add_patch(p)
    if txt: ax.text(x+w/2 if ha=="center" else x+0.03,y+h/2,txt,ha=ha,va=va,fontsize=fs,zorder=z+1)
def arrow(ax,p,q,txt="",c="k",lw=0.9,ls="-",rad=0.0,fs=6.5,off=(0,0.1),shrink=0.28,z=2,style="-|>",tcol=None,ts=None):
    a=FancyArrowPatch(p,q,arrowstyle=style,mutation_scale=7,color=c,lw=lw,ls=ls,connectionstyle=f"arc3,rad={rad}",shrinkA=shrink*28,shrinkB=shrink*28,zorder=z)
    ax.add_patch(a)
    if txt:
        mx,my=(p[0]+q[0])/2+off[0],(p[1]+q[1])/2+off[1]
        ax.text(mx,my,txt,fontsize=ts or fs,ha="center",va="center",color=tcol or c,zorder=z+2,bbox=dict(fc="white",ec="none",pad=0.4,alpha=0.85))
def seg(ax,p,q,c="k",lw=0.9,ls="-",z=2):
    ax.plot([p[0],q[0]],[p[1],q[1]],color=c,lw=lw,ls=ls,zorder=z,solid_capstyle="round")
def panel(ax,s,title=""):
    ax.set_title(f"$\\mathbf{{{s}}}$  {title}",loc="left",fontsize=8.5)
def clean(ax,lim=None):
    ax.set_aspect("equal"); ax.axis("off")
    if lim: ax.set_xlim(lim[0],lim[1]); ax.set_ylim(lim[2],lim[3])
def finish(name):
    json.dump(DATA,open(os.path.join(HERE,"..","results","FIGURE_DATA.json"),"w"),indent=1,default=str)

# ---------- Paper III additions ----------
import math
from eng3 import *
from eng3 import _bd
def circ(n, r=1.0, phase=math.pi/2):
    return [(r*math.cos(phase+2*math.pi*i/n), r*math.sin(phase+2*math.pi*i/n)) for i in range(n)]
def draw_complex(ax, D, K, pos=None, dead_e=(), new_v=(), new_e=(), fs=6.5, r=0.17, shade2=True, label=True, scale=1.0):
    """abstract layout: vertices on a circle (no geometric meaning); edges = 1-cells; 2-cells shaded (their vertex sets)"""
    D=sorted(D)
    if pos is None:
        pts=circ(len(D), scale); pos={d:p for d,p in zip(D,pts)}
    cs=cellsets(K)
    if shade2 and len(cs)>2:
        for c in cs[2]:
            vs=sorted(c, key=lambda d: math.atan2(pos[d][1]-sum(pos[w][1] for w in c)/len(c), pos[d][0]-sum(pos[w][0] for w in c)/len(c)))
            ax.add_patch(Polygon([pos[v] for v in vs], closed=True, fc="#dfe9f5", ec="none", alpha=0.7, zorder=1))
    for (u,v) in sorted(K['E']):
        seg(ax, pos[u], pos[v], c=("#555" ), lw=0.9, z=2)
    for (u,v) in dead_e:
        seg(ax, pos[u], pos[v], c=LOST, lw=1.4, ls=(0,(3,2)), z=3)
    for (u,v) in new_e:
        seg(ax, pos[u], pos[v], c=KEEP, lw=1.5, z=3)
    for d in D:
        nv = d in new_v
        node(ax, pos[d][0], pos[d][1], str(d) if label else "", fc=(KEEP_L if nv else "white"), ec=(KEEP if nv else "k"), r=r, fs=fs, bold=nv)
    return pos
def betti_str(b):
    b=list(b)
    while len(b)>1 and b[-1]==0: b=b[:-1]
    return "("+",".join(map(str,b))+")"

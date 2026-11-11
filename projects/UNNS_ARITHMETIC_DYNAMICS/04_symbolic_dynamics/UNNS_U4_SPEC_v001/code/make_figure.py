import json,os,matplotlib;matplotlib.use("Agg");import matplotlib.pyplot as plt
H=os.path.dirname(os.path.abspath(__file__));R=json.load(open(H+"/../data/registry.json"))
col={"U3_CONSEQUENCE":"#4c78a8","STANDARD":"#72b7b2","NEW_ELEMENTARY":"#f58518","FROZEN_IMPORT":"#9d9d9d","OPEN":"#e45756","DEFINITION":"#eeca3b"}
stages=["U4.0","U4.1","U4.2","U4.3","U4.4","U4.5","U4.6"];pos={}
for si,s in enumerate(stages):
    items=[x for x in R if x["stage"]==s]
    for k,x in enumerate(items): pos[x["id"]]=(si,-k+len(items)/2)
fig,ax=plt.subplots(figsize=(13,7.5))
for x in R:
    for d in x["deps"]:
        (x0,y0),(x1,y1)=pos[d],pos[x["id"]]
        ax.annotate("",xy=(x1,y1),xytext=(x0,y0),arrowprops=dict(arrowstyle="-",color="#bbbbbb",lw=0.6),zorder=1)
for x in R:
    xx,yy=pos[x["id"]];ax.scatter(xx,yy,s=210,color=col[x["origin"]],edgecolor="k",linewidth=.5,zorder=2)
    ax.text(xx,yy-0.38,x["id"].split("-",1)[-1] if x["id"].startswith("U4") else x["id"],ha="center",va="top",fontsize=6.3,zorder=3)
ax.set_xticks(range(len(stages)));ax.set_xticklabels(stages);ax.set_yticks([]);ax.spines[:].set_visible(False)
for o,c in col.items(): ax.scatter([],[],color=c,edgecolor="k",label=o.replace("_"," ").title())
ax.legend(loc="upper center",ncol=6,fontsize=8,frameon=False,bbox_to_anchor=(0.5,1.07))
ax.set_title("Proof-dependency graph of the U4 claim registry (edges point from a claim to what it uses)",fontsize=10,pad=28)
plt.tight_layout();plt.savefig(H+"/../figures/dependency_graph.png",dpi=170)

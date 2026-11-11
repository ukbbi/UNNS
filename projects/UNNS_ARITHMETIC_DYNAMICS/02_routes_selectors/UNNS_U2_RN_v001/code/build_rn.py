import json,os,collections
import matplotlib;matplotlib.use("Agg");import matplotlib.pyplot as plt
H=os.path.dirname(os.path.abspath(__file__));B=H+"/.."
rep=json.load(open(B+"/reports/verification_report.json"))["items"]
R=json.load(open(B+"/data/rn_results.json"))
r2=rep["RN2"];r0=rep["RN0"];r1=rep["RN1_local_identities"];rd=rep["RN1_descent"];ex=rep["RN_exploratory_terminal_primes"]
sc=r2["status_counts"]
N=dict(Orbits=r2["orbits"],NRules=60,NStarts=14,Cyc=sc["cyclic"],Esc=sc["escape"],Stuck=sc["stuck"],Uncert=r2["uncertified_orbits"],
 ProvedCmp=r2["proved_law_orbit_comparisons"],NbCmp=r2["nb_variant_comparisons"],PrimRange="2{,}000{,}000",NbrRange="20{,}000",
 DegRange="10^6",DescRange="100{,}000",MaxSteps=rd["max_descent_steps"],PrimeEnd=rd["terminal_squarefree_prime_count"],OtherEnd=rd["terminal_squarefree_composite_or_one_count"],
 FracMinAll="%.3f"%ex["minall_attractor_prime_fraction"],FracMaxI="%.3f"%ex["maxi_terminal_prime_fraction"],MaxPrimes=r2["rules_with_ge3_distinct_primes_in_an_orbit"][0]["max_distinct_primes"])
open(B+"/manuscript/numbers.tex","w").write("".join("\\newcommand{\\%s}{%s}\n"%(k,v) for k,v in N.items()))
# table of selectors
def nm(r): return ("%s %s-%d"%(r["side"],r["end"],r["k"])) if r["key"] is None else "%s %s/%s"%(r["side"],r["key"],r["tie"])
agg=collections.OrderedDict()
for x in R:
    ru=x["rule"];k=nm(ru);d=agg.setdefault(k,{False:collections.Counter(),True:collections.Counter(),"p":0})
    d[ru["nb"]][x["analysis"]["status"]]+=1;d["p"]=max(d["p"],x["analysis"]["distinct_primes"])
rows=[]
for k,d in agg.items():
    f=lambda c:"%d/%d/%d"%(c["cyclic"],c["escape"],c["stuck"])
    rows.append("%s & %s & %s & %d\\\\"%(k.replace("_","\\_"),f(d[False]),f(d[True]),d["p"]))
open(B+"/manuscript/table_select.tex","w").write("\n".join(rows))
led=rep["RN3"]["ledger"]
lr=[]
for l in led:
    ru=l["rule"];cf=l["closed_form_evaluator"];ps=l["per_step"]
    lr.append("%s & %s & %.1f & %.1f & %s\\\\"%(nm(ru),l["tier"],ps["factor_calls"],ps["rho_iter"],("%.1f"%cf["factor_calls_per_step"]) if cf else "--"))
open(B+"/manuscript/table_ledger.tex","w").write("\n".join(lr))
fig,ax=plt.subplots(1,2,figsize=(9,3.3))
sides=["F","I","A"];cols={"cyclic":"#4c78a8","escape":"#f58518","stuck":"#54a24b"}
bot=[0]*6;labs=[]
for j,(s,nb) in enumerate([(s,nb) for nb in(False,True) for s in sides]):
    c=collections.Counter(x["analysis"]["status"] for x in R if x["rule"]["side"]==s and x["rule"]["nb"]==nb);b=0
    for st in("cyclic","escape","stuck"):
        ax[0].bar(j,c[st],bottom=b,color=cols[st],label=st if j==0 else None);b+=c[st]
    labs.append(s+("+nb" if nb else ""))
ax[0].set_xticks(range(6));ax[0].set_xticklabels(labs);ax[0].set_ylabel("orbits (of 140 per bar)");ax[0].legend(fontsize=7);ax[0].set_title("Registered run: orbit endings by side",fontsize=9)
tiers={"A":[],"B":[],"C":[]}
for l in led: tiers[l["tier"]].append(l["per_step"]["factor_calls"])
ax[1].bar(list(tiers),[sum(v)/len(v) for v in tiers.values()]);ax[1].set_yscale("symlog");ax[1].set_ylabel("factor calls per step (generic engine)");ax[1].set_title("Mean cost by observability tier",fontsize=9)
plt.tight_layout();plt.savefig(B+"/figures/rn_summary.pdf")
print(N)

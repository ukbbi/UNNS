import json,os,sys
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
H=os.path.dirname(os.path.abspath(__file__)); B=H+"/.."
r=json.load(open(B+"/reports/verification_report.json"))["items"]
t2=r["TI2"];t0=r["TI0"];a=r["TI3_audit"];ac=r["TI3_accounting"];ex=r["TI2_exploratory"]
st=t2["status"]; F=lambda c:sum(v for k,v in st.items() if k.startswith(c))
kr=ac["knowledge_rich"];g=ac["graph_local_rule"]
N={"Orbits":t2["orbits"],"OrbitsF":F("F"),"OrbitsM":F("M"),
"FCyc":st["F:cyclic"],"FEsc":st["F:escape"],"FHor":st["F:horizon"],"FStuck":st["F:stuck"],
"MEsc":st["M:escape"],"MHor":st["M:horizon"],"MStuck":st["M:stuck"],
"Succ":t2["registered_successes"],"SuccF":t2["successes_F"],"SuccM":t2["successes_M"],"SuccPrefixes":t2["distinct_successful_prefixes"],
"FibHits":t2["fibonacci_consecutive_hits"],"AnyConsHits":t2["any_family_consecutive_hits"],
"NonCyc":ex["non_cyclic_orbits"],"XLaw":ex["x_to_xplus1_squared_orbits"],
"DomN":t0["domain_inputs"],"ExtN":t0["extended_inputs"],"NLabels":t0["label_expressions"],
"NbCheck":3000,"LocN":a["locality_states_checked"],"IntBytes":g["interpreter_code_bytes"],
"RuleBytes":g["rule_bytes"],"RuleZ":g["rule_zlib_bytes"],"CandStep":"%.1f"%g["candidates_inspected_per_move"],"GramBits":"%.2f"%g["grammar_bits"]}
for k,p in (("Fib","fibonacci_KI"),("SqD","squares_direct_KI"),("SqW","squares_wrapper_KI")):
    v=kr[p]; N[k+"Tab"]=v["table_bytes"];N[k+"TabZ"]=v["table_zlib_bytes"];N[k+"Code"]=v["code_bytes"]
    N[k+"Moves"]="%.2f"%v["moves_per_term"];N[k+"Ops"]="%.0f"%v["arith_ops_per_term"];N[k+"Rec"]="%.2f"%v["recoveries_per_term"];N[k+"States"]=v["control_states"]
open(B+"/manuscript/numbers.tex","w").write("".join("\\newcommand{\\%s}{%s}\n"%(k,v) for k,v in N.items()))
fig,ax=plt.subplots(1,2,figsize=(9,3.2))
labs=["cyclic","escape","horizon","stuck"]
ax[0].bar([i-.2 for i in range(4)],[st["F:"+l] if "F:"+l in st else 0 for l in labs],.4,label="class F (finite control)")
ax[0].bar([i+.2 for i in range(4)],[st["M:"+l] if "M:"+l in st else 0 for l in labs],.4,label="class M (unbounded memory)")
ax[0].set_xticks(range(4));ax[0].set_xticklabels(labs);ax[0].set_ylabel("orbits");ax[0].legend(fontsize=7);ax[0].set_title("Registered run: orbit endings",fontsize=9)
names=["Fib. succ.","Squares dir.","Squares wrap."];ops=[kr[k]["arith_ops_per_term"] for k in("fibonacci_KI","squares_direct_KI","squares_wrapper_KI")]
ax[1].bar(names,ops);ax[1].set_yscale("log");ax[1].set_ylabel("arith. ops per route step (log)");ax[1].set_title("Knowledge-rich selectors, KI domain",fontsize=9)
plt.tight_layout();plt.savefig(B+"/figures/ti_summary.pdf")

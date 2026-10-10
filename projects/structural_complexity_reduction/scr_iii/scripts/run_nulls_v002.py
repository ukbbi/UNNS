from __future__ import annotations
import json, statistics
from scr_iii.compat import install_scr_ii_path
from scr_iii.engine_common import read_json_gz, safe_write_json, stable_int
from scr_iii.engine_v002_common import output_root_v002, scr_iii_root, load_seeds_v002
from scr_iii.nulls.controls_v001 import n1_p_accept, build_n4
from scr_iii.analysis.structure_stats_v001 import structure_stats
from scr_iii.analysis.metrics_v001 import preservation_metrics
install_scr_ii_path()
from nulls.controls import solve_n1_random_prefix, frozen_symbol_permutations, frozen_transition_permutations, permuted_transitions
from solver.exact_solver import solve_scr, solve_baseline


def ei_from_counts(N,m,L,retained):
    r=retained/m if m else 1.0; a0=(L-retained)/(N-m) if N>m else None
    return None if a0 is None or abs(1-a0)<1e-15 else (r-a0)/(1-a0)


def main():
    root=output_root_v002(); p=root/"primary"/"PRIMARY_RESULT_v002.json"
    if not p.exists(): print("v002 nulls blocked: primary incomplete."); return 2
    primary=json.loads(p.read_text(encoding="utf-8")); seeds=load_seeds_v002(); out=root/"nulls"; out.mkdir(parents=True,exist_ok=True)
    n1=[]; n4=[]; n2=[]; n3=[]
    first5={d:set(seeds["primary"][f"depth_{d}"][:5]) for d in (14,16,18)}
    n1base=int(seeds["analysis_rng"]["N1_base"])
    for idx,row in enumerate(primary["main_cells"],1):
        inst=read_json_gz(scr_iii_root()/row["instance_path"]); N=1<<int(row["depth"]); m=int(row["solution_count_baseline"]); L=int(row["L"])
        pacc=n1_p_accept(L,N,row["depth"]); eis=[]
        for rep in range(50):
            rr=solve_n1_random_prefix(inst,pacc,stable_int(n1base,row["cell_id"],rep)); e=ei_from_counts(N,m,int(rr["leaves_checked"]),int(rr["solution_count"]))
            if e is not None: eis.append(e)
        n1.append({"cell_id":row["cell_id"],"p_accept":pacc,"mean_EI":sum(eis)/len(eis) if eis else None,"replicates":50})
        anti=build_n4(inst); ba=solve_baseline(anti); sa=solve_scr(anti); sta=structure_stats(anti); ma=preservation_metrics(anti,ba,sa,sta,0.0,None)
        n4.append({"cell_id":row["cell_id"],"EI":ma["excess_inclusion_EI"],"recall":ma["solution_recall"]})
        if int(row["seed"]) in first5[int(row["depth"])]:
            for j,mapping in enumerate(frozen_symbol_permutations(),1):
                rr=solve_scr(inst,symbol_map=mapping); e=ei_from_counts(N,m,int(rr["leaves_checked"]),int(rr["solution_count"])); n2.append({"cell_id":row["cell_id"],"perm":j,"EI":e,"recall":rr["solution_count"]/m})
            for j,mapping in enumerate(frozen_transition_permutations(),1):
                tr=permuted_transitions(mapping); rr=solve_scr(inst,transitions=tr); e=ei_from_counts(N,m,int(rr["leaves_checked"]),int(rr["solution_count"])); n3.append({"cell_id":row["cell_id"],"perm":j,"EI":e,"recall":rr["solution_count"]/m})
        if idx%25==0: print("v002 nulls",idx,"/",len(primary["main_cells"]))
    n1vals=[x["mean_EI"] for x in n1 if x["mean_EI"] is not None]; n4vals=[x["EI"] for x in n4 if x["EI"] is not None]
    mean_n1=sum(n1vals)/len(n1vals) if n1vals else None; med_n4=statistics.median(n4vals) if n4vals else None
    z0_pass=all(x.get("exact_preservation") and x.get("L")==1<<int(x["depth"]) for x in primary["Z0"]) and bool(primary["Z0"])
    c1_pass=all(x.get("c1_exact") for x in primary["main_cells"]) and bool(primary["main_cells"])
    verdict=mean_n1 is not None and abs(mean_n1)<=0.01 and med_n4 is not None and med_n4<=0 and z0_pass and c1_pass
    result={"engine":"SCR_III_ENGINE_v002","status":"COMPLETE","H5_pass":verdict,"N1_mean_EI":mean_n1,"N4_median_EI":med_n4,"Z0_pass":z0_pass,"C1_pass":c1_pass,"N1":n1,"N4":n4,"N2":n2,"N3":n3}
    safe_write_json(out/"NULL_RESULT_v002.json",result); print("v002 NULLS COMPLETE H5=",verdict); return 0

if __name__=="__main__": raise SystemExit(main())

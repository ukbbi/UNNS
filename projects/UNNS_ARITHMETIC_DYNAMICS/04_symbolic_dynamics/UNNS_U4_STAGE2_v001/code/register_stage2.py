"""Writes data/stage2_config.json (preregistered designs for 2C and 2D) and data/stage2_registration.json (SHA-256 of config and experiment code).
Run BEFORE the experiments; rerun only through a disclosed amendment."""
import json,os,hashlib,sys
H=os.path.dirname(os.path.abspath(__file__));D=H+"/../data"
sha=lambda p:hashlib.sha256(open(p,'rb').read()).hexdigest()
u3=json.load(open(D+"/u3_v001_results.json"))["U3_3_realizability"]["1"]["realized_list"]
cfg=dict(
 seed=20261110,
 survey_2C=dict(windows=[x["embedding"] for x in u3],source="U3 v001 realized_list at r=1 (embeddings of all 10 realised connected graphs on <=5 vertices)",
   memories=[1,2],enumeration="exhaustive over all subsets of realised window types when #types<=14, else 20000 random subsets, inclusion probability drawn uniformly from [0.05,0.95] per rule",
   sampled_rules=20000,signature_length=12,eig_tol=1e-8,
   targets={"golden_mean":"tr([[1,1],[1,0]]^n)","directed_3cycle_with_loops":"tr(([[1,1,0],[0,1,1],[1,0,1]])^n)","full_2_shift":"2^n","full_3_shift":"3^n","NB_5_cycle":"10 if 5|n else 0","NB_4_cycle":"8 if 4|n else 0"},
   questions=["Q1 does any memory-2 metric rule have non-real nonzero spectrum (memory-1: none by U4.3-T3)?",
              "Q2 does any nonempty memory-2 rule have no point of period <=2 (memory-1: none)?",
              "Q3 do memory-2 rules reproduce, as periodic-point signatures, any of the targets (necessary condition for conjugacy only)?",
              "Q4 does the fixed-point dichotomy (U4.3-T2) hold in all memory-2 rules tested?"]),
 selectors_2D=dict(
   grammar="state (x,p): p = previous vertex or None; eligible set E = N(x) minus {p} (memory=NB) or N(x) (memory=state-only); order key in {val_asc, val_desc, deg_asc_then_val, deg_desc_then_val}; rank j in {1,2,3}; if |E|<j -> STUCK (no substitution)",
   starts=[1,2,3,4,5,6,7,8,9,10,12,15,16,30,60,72,210,2310],horizon=400,escape_bound=10**18,
   certification="neighbourhoods via frozen RN core; certified iff every prime factor used was certified (n<3.317e24); uncertified neighbourhoods are flagged and counted separately",
   observables="complete neighbourhood values and neighbour degrees only (no arithmetic target, no sequence-specific data)",
   metrics=["outcome in {CYCLE,ESCAPED,STUCK,HORIZON}","preperiod","period","distinct and total prime visits","uncertified count","neighbourhood evaluations","factorisation calls"],
   treatment="finite prime-visit counts are observations, never theorems; selectors are not claimed to be generators of any infinite family"),
 amendments=[dict(id="A1",text="First registered run of m2_survey.py classified non-real spectrum and non-emptiness from the floating-point eigenvalues of the whole transition matrix. Nilpotent (transient) blocks can produce spurious complex eigenvalues of size eps^(1/k), so that classifier was unsound. Replaced by exact strongly-connected-component structure (non-emptiness) and eigenvalues of the recurrent blocks only, with an exact sympy audit on a seeded sample. The first-run counts (memory 2: nonreal 72164, nonempty 85894, nonempty with no period<=2 point 6422 of 94352 rules) are retained here as superseded, not as results."),dict(id="A2",text="Second registered run (float classifier on recurrent blocks only, with exact audit of 400 sampled rules) disagreed with the exact audit on 12 of 400; the float classifier was therefore replaced for ALL rules by an exact test (sympy characteristic polynomial, square-free factorisation, real-root count with multiplicity) of each recurrent block, cached by block matrix. Second-run counts (memory 2: nonempty 85949, nonreal 70088, nonempty without period<=2 point 6337, NB_5_cycle 135, NB_4_cycle 514) are superseded.")])
json.dump(cfg,open(D+"/stage2_config.json","w"),indent=1,sort_keys=True)
files={"stage2_config.json":D+"/stage2_config.json","m2_survey.py":H+"/m2_survey.py","selector_exp.py":H+"/selector_exp.py","indep_graph.py":H+"/indep_graph.py",
       "engine/u3_graph.py":H+"/../engine/u3_graph.py","frozen_RN/rn_core.py":H+"/../frozen_RN/rn_core.py","frozen_RN/rn_naive.py":H+"/../frozen_RN/rn_naive.py"}
reg={k:sha(p) for k,p in files.items() if os.path.exists(p)}
json.dump(reg,open(D+"/stage2_registration.json","w"),indent=1,sort_keys=True);print(reg)

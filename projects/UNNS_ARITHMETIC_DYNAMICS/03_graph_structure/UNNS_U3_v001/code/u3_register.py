import json,os,hashlib
H=os.path.dirname(os.path.abspath(__file__));D=H+"/../data"
sha=lambda p:hashlib.sha256(open(p,'rb').read()).hexdigest()
cfg=dict(seed=20261109,
 graph=dict(tri_max=3000),
 u31=dict(routing_N0=10,decode_trials=500,decode_alpha=10,decode_len=8,seed=7,ext_maxL=5,ext_search=3000,samp_alpha=4,samp_len=4),
 u32=dict(emb_max=8,f3_max=9),
 u33=dict(radii=[1,2,3],W0={"1":300,"2":150,"3":40},Vmax={"1":1000000,"2":3000,"3":60},h_maxn=5),
 preregistered=["P1: lex-first geodesic is legal, shortest and matches brute-force enumeration (d<=4) and plain BFS (d<=5)",
  "P2: M(w)=2^(L-1) for lex-first geodesics (extremal ambiguity) and M(w)<=2^(L-1) for all sampled histories",
  "P3: golden-mean tower period=2 for every embedding in 1..8; Abramov relation for the lift of the base Parry measure; topological entropy of the tower from the renewal equation vs spectral radius of the expanded graph",
  "P4: realizability: report found / not-found only; 'not found' is never read as impossibility except where a theorem is cited",
  "P5: all neighbourhoods certified by the RN-0 policy"],amendments=["A3: the first P3 formulation compared the TOPOLOGICAL entropy of the tower with h/rbar computed for the base Parry measure. Abramov's formula is measure-wise; the tower's topological entropy is the supremum over invariant measures and exceeds the Parry-lift value. P3 was reformulated (lift entropy vs h/rbar; topological entropy vs expanded-graph spectral radius) and the run repeated.","A1: first run of the golden-mean Abramov check used a swapped Parry transition matrix (P00,P01) and a non-period-corrected growth ratio; the check failed (max diff 0.03) before the fix. Corrected in u3_exp.py and the full run repeated; the theorem is unchanged.","A2: first run searched induced subgraphs inside the window 1..40 only; that missed the 5-cycle 6,24,96,784,27 because its vertices exceed 40. Replaced by an exact ball-based search (first vertex 1..300, later vertices from exact balls) and the full run repeated."])
json.dump(cfg,open(D+"/u3_config.json","w"),indent=1,sort_keys=True)
reg={"config_sha256":sha(D+"/u3_config.json")}
for f in("u3_graph.py","u3_exp.py"): reg[f]=sha(H+"/"+f)
for f in("rn_core.py","rn_naive.py"): reg["frozen_RN/"+f]=sha(H+"/../frozen_RN/"+f)
json.dump(reg,open(D+"/u3_registration.json","w"),indent=1,sort_keys=True);print(reg)

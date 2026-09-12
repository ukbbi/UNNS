#!/usr/bin/env python3
"""Recompute MC_GRAMMAR_SELECT_v001 evidence/replay from existing project outputs."""
from pathlib import Path
import pandas as pd
import json

ROOT=Path(".")
rep=pd.read_csv(ROOT/"08_OUTPUTS/REP_STUDY_v002/FOUR_REP_RESULTS.csv")
rob=pd.read_csv(ROOT/"08_OUTPUTS/REP_STUDY_v002/ROBUSTNESS.csv")
nulls=pd.read_csv(ROOT/"08_OUTPUTS/GRAMMAR_DEV_v001/NULL_RESULTS.csv")

M_GATE=0.12
P_NULL=0.1
M_NULL=0.1
VARIANTS=['ORIGIN_SHIFT', 'CLOCK_EXCHANGE', 'AFFINE_STATE', 'DOWNSAMPLE_5', 'PREFIX_0.75', 'NOISE_0.02SD']

p=nulls[(nulls.metric=="JPR_parent_gain")&(nulls.null_model=="PHASE_LABEL_PERMUTE")][["id","p_upper"]]
p=p.rename(columns={"p_upper":"P_phase_label_p_upper"})
m=nulls[(nulls.metric=="FC_frac_mixed_gain")&(nulls.null_model=="FOURIER_PHASE")][["id","p_upper"]]
m=m.rename(columns={"p_upper":"M_fourier_p_upper"})

x=rep[["id","source","role","JPR_cover_advantage","FC_frac_mixed_gain"]].merge(p,on="id").merge(m,on="id")
st=[]
for rid,g in rob.groupby("id"):
    s=g[g.variant.isin(VARIANTS)]
    st.append({"id":rid,"M_stability_all_variants":bool((s.FC_frac_mixed_gain>=M_GATE).all()),
                "M_robust_min":float(s.FC_frac_mixed_gain.min())})
st=pd.DataFrame(st)
x=x.merge(st,on="id")
x["D_domain"]=True
x["P_anchor"]=x.P_phase_label_p_upper<=P_NULL
x["M_magnitude"]=x.FC_frac_mixed_gain>=M_GATE
x["M_spectral_null"]=x.M_fourier_p_upper<=M_NULL
x["TEMPORAL_CORE_CANDIDATE"]=x.D_domain & x.P_anchor & x.M_magnitude & x.M_spectral_null & x.M_stability_all_variants
print(x.to_string(index=False))

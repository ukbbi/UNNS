#!/usr/bin/env python3
"""Recreate the Bulava et al. 2019 fitted-model E0/E1/E2 pointwise curve.
This is a model reconstruction from reported parameters, not raw GEVP point data.
"""
from pathlib import Path
import csv, numpy as np
BASE=Path(__file__).resolve().parents[1]
out=BASE/'data/01_core_static_potential/bulava2019_model_reconstructed_pointwise_E_levels.csv'
a_fm=0.06426
ainv_GeV=0.1973269804/a_fm
p={'aE1':0.0019,'aE2':0.0262,'ag1':0.0154,'ag2':0.0080,'a2sigma':0.0229,'aV0hat':-0.434}
rows=[]
for r_over_a in [round(11+i*0.25,2) for i in range(int((25-11)/0.25)+1)]:
    Vhat=p['aV0hat']+p['a2sigma']*r_over_a
    H=np.array([[Vhat,p['ag1'],p['ag2']],[p['ag1'],p['aE1'],0.0],[p['ag2'],0.0,p['aE2']]],float)
    vals=np.linalg.eigvalsh(H)
    rows.append({'r_over_a':r_over_a,'r_fm':r_over_a*a_fm,'aV0_minus_2EB':vals[0],'aV1_minus_2EB':vals[1],'aV2_minus_2EB':vals[2],'V0_minus_2EB_GeV':vals[0]*ainv_GeV,'V1_minus_2EB_GeV':vals[1]*ainv_GeV,'V2_minus_2EB_GeV':vals[2]*ainv_GeV})
with out.open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
print('wrote', out)

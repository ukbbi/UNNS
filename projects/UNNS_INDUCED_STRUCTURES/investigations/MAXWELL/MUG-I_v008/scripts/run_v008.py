#!/usr/bin/env python3
"""Reproducible exact research results. Standard library only."""
import csv, json
from pathlib import Path
from fractions import Fraction
from core import (sample_fourier, strict_step, component_step, E_step, walk,
                  multiplier, content, exact_curvature_mismatch)

root = Path(__file__).resolve().parents[1]
outdir = root / 'results'
outdir.mkdir(exist_ok=True)
rows=[]
q=6
x0=sample_fourier()
for label, word in [('A_3_8_3',(3,8,3)),('B_1_1_1_2',(1,1,1,2))]:
    for name in ('strict','component','E'):
        x, p=walk(x0,word,name,q)
        rows.append(dict(history=label,word=','.join(map(str,word)),rule=name,
                         initial_content=content(x0),content_trace='->'.join(map(str,p)),
                         surviving=int(bool(x)),final_content=content(x or {}),
                         coefficients=len(x or {})))
with (outdir/'rule_comparison.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

# One-step theorem certificates: if delta nonzero, curvature mismatch != 0.
no_go=[]
for n in (1,2,3,8):
    r=multiplier(n)
    c=exact_curvature_mismatch(Fraction(1,10),6,n)
    no_go.append(dict(N=n,r=str(r),difference_epsilon_double_prime_at_zero=str(c),
                      nonzero=c!=0))

# Exhaustively compare P_N^q with Q_N for N|q, and zero otherwise.
equivalence_checks=0
for q0 in range(1,13):
    for n in range(1,22):
        for m in range(-60,61):
            x={m:Fraction(1)}
            a=E_step(x,n,q0)
            b=component_step(x,n) if q0 % n == 0 else {}
            assert a == b,(q0,n,m,a,b)
            equivalence_checks+=1

summary={
 'release':'MUG-I_v008',
 'status':'research candidate; local verification required',
 'model':'periodic scalar Maxwell-Hill; epsilon(z)=1+2delta*cos(qz), 0<abs(delta)<1/2; omega^2>0',
 'theorems':{
   'exact_eigenstate_full_fourier_content':'gcd(kappa,q), for delta!=0 and omega^2>0',
   'exact_fixed_medium_dilation_no_go':'no nontrivial r>1 direct eigenstate to eigenstate map for delta!=0',
   'strict_whole_field':'unblocked admissible histories compose endpoint-only, even though intermediate fields are not fixed-medium eigenstates',
   'rule_E_identity':'E_N = D_N*Q_N if N divides q, else zero',
   'co_dilating_medium':'epsilon_r(z)=epsilon(r*z), omega_r=r*omega exactly solves',
 },
 'same_source':{'q':6,'initial_content':6,'word_A':[3,8,3],'word_B':[1,1,1,2],
                 'target_content':1728,'rows':rows},
 'exact_curvature_certificates':no_go,
 'rule_E_component_equivalence_cases':equivalence_checks,
 'classification':{
   'strict_fourier_support':'both example histories legal and identical endpoint field, not stationary fixed-medium eigenmodes',
   'componentwise_filter':'both example histories survive in full with same endpoint; filtering is a declared rule',
   'v007_rule_E':'A blocked, B survives, because of the extra global N|q veto',
   'strict_exact_fixed_medium_eigenstate':'both histories stop at first step for nonzero delta',
   'exact_basis_resolution':'lossless as representation when the full eigenbasis is retained; no physical selection',
   'co_dilating_medium':'exact mode correspondence between different media/domains',
 },
 'physical_predictive_advantage':'NOT DEMONSTRATED',
 'prior_release':'MUG-I_v007 untouched',
}
(outdir/'summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('MUG-I v008 exact run PASS')
print('Rule E identity cases:',equivalence_checks)
for row in rows:
    print(' ',row['history'],row['rule'],'trace',row['content_trace'],'survives',bool(row['surviving']))
print('No-go curvature certificates:',[v['difference_epsilon_double_prime_at_zero'] for v in no_go])
print('Written',outdir)

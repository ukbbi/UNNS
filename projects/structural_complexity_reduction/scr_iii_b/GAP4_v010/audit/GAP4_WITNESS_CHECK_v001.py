#!/usr/bin/env python3
"""Read-only, independent witness energy and 2-in/2-out checks for GAP4 v010.
Does not solve, search, or claim certified optimality."""
import json,hashlib,math,sys
from pathlib import Path
inst=Path(sys.argv[1]); result=Path(sys.argv[2]); output=Path(sys.argv[3])
words=inst.read_text().split(); n=int(words[0]); nv=int(words[1]); assert n==40 and nv==16
p=2; edges=[]
for i in range(n):
 for j in range(i+1,n):
  edges.append((i,j,float(words[p])));p+=1
vertex=[]
for _ in range(nv):
 m=int(words[p]); orient=int(words[p+1]);p+=2
 assert (m>>n)==0 and orient & ~m ==0 and m.bit_count()==4
 vertex.append((m,orient))
assert p==len(words)
records=[json.loads(s) for s in result.read_text().splitlines() if s.strip()]
assert len(records)==2 and {r['objective'] for r in records}=={'ground','non_grammar'}
checks=[]
for r in records:
 state=int(r['witness_id']); assert 0<=state<(1<<n)
 spins=[1 if (state>>i)&1 else -1 for i in range(n)]
 terms=[k*spins[i]*spins[j] for i,j,k in edges]
 energy=math.fsum(terms)
 counts=[sum(((state>>i)&1)==((orient>>i)&1) for i in range(n) if ((m>>i)&1)) for m,orient in vertex]
 violations=sum(x!=2 for x in counts)
 witness_valid=violations>0 if r['objective']=='non_grammar' else True
 discrepancy=energy-float(r['upper'])
 checks.append({'objective':r['objective'],'witness_id':state,'energy_fsum_A':energy,'reported_upper_A':r['upper'],'difference_A':discrepancy,'violated_vertices':violations,'vertex_in_counts':counts,'witness_constraint_pass':witness_valid,'completed_claim':r['completed'],'solver_lower_claim_A':r['lower']})
by={r['objective']:r for r in checks}
gap=by['non_grammar']['energy_fsum_A']-by['ground']['energy_fsum_A']
report={'input_sha256':hashlib.sha256(inst.read_bytes()).hexdigest(),'results_sha256':hashlib.sha256(result.read_bytes()).hexdigest(),'n':n,'nv':nv,'pairs':len(edges),'witnesses':checks,'gap_A_witness_difference':gap,'witness_evaluations_pass':all(x['witness_constraint_pass'] and abs(x['difference_A'])<1e-12 for x in checks),'global_optimality_independently_certified':False,'status':'GAP_INCONCLUSIVE_PENDING_OPTIMALITY_CERTIFICATION'}
output.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'witness_pass':report['witness_evaluations_pass'],'gap_A':gap,'violated_vertices':by['non_grammar']['violated_vertices'],'status':report['status']}))

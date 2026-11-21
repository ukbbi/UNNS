"""POST-PROTOCOL EXACT THEOREM CHECK: prime residue-class label suppression."""
from pathlib import Path
import csv
ROOT=Path(__file__).resolve().parents[1]

def prime(p):return p>=2 and all(p%d for d in range(2,int(p**.5)+1))
rows=[]
for p in range(2,128):
    if not prime(p):continue
    roots=[n for n in range(p) if (n*n+n+1)%p==0]
    expected=1 if p==3 else (2 if p%3==1 else 0)
    assert len(roots)==expected
    for n in roots:
        assert all((t*(n*n+n+1))%p==0 for t in [1,2,3,7,11,19])
    rows.append(dict(prime=p,p_mod_3=p%3,blocked_label_residues=';'.join(map(str,roots)),root_count=len(roots)))
with (ROOT/'results'/'prime_residue_gates.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print('CIB-I v001 PRIME GATE PASS',len(rows),'primes; selected roots:',[(r['prime'],r['blocked_label_residues']) for r in rows if r['prime'] in [2,3,5,7,11,13,17,19]])

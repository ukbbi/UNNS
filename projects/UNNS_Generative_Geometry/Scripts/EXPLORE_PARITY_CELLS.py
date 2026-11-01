"""Exploratory exact k-dimensional Graver parallelotope counts, NOT a coverage result.

Run from project root: python Scripts/EXPLORE_PARITY_CELLS.py
This is an explicit candidate extension of Paper A's planar cell grammar.
"""
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.parity import parity_benchmark, graver_basis
from src.cells import admissible_cells

results = {'status': 'EXPLORATORY ONLY; candidate grammar, NOT a theorem on coverage or topology', 'definition': 'Every cell uses linearly independent oriented parity-lattice Graver directions and all 2^r corners in the arithmetic fibre', 'cases': []}
for ps in ((2,5,11), (2,5,11,17)):
    x, pts = parity_benchmark(ps)
    dirs = graver_basis(len(ps), oriented=True)
    case = {'k':len(ps), 'primes':list(ps), 'vertices':len(pts), 'oriented_graver_vectors':len(dirs), 'candidate_cells_by_dimension':{}}
    for r in range(1,len(ps)+1):
        case['candidate_cells_by_dimension'][str(r)]=len(admissible_cells(pts,dirs,r))
    results['cases'].append(case)
print(json.dumps(results,indent=2))
if '--save' in sys.argv:
    out=ROOT/'results'/'provisional_parity_cells.json'
    out.write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
    print('Saved',out)

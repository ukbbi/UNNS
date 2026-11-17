# SPEC v009
Inputs: v006 data, famE shapes (K = enumeration size parameter). B=10^6.
1. `classes.py` shape → (r0, m, n0). 2. `cover.py` residue-tree covering with frontier cap 1.5M, budgets 40/100/100 s (K=4/8/12) → results/C2_covering_search.json.
3. `height.py`/`run_height.py` minimal height over shortest paths (results H1*); `height4.py` over all simple routes ≤4 (results H2*).
4. `verify_all_v009.py [--quick]` → reports/VERIFY_v009_*.md. Layout: sibling dirs UNNS-SCALE-I_v00{2..8}, SHA256SUMS.txt (v001) at parent.
Stopping rules: covering search stops at budget; no uncovered-bound claim beyond the printed rigorous bound.

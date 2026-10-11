# SCR manuscript-completion record: exact 4×4 grammar count (v001)

**Status:** ADDITIVE. Does not modify, reopen or supersede any frozen record, verdict, prediction, certificate or hash. No Hamiltonian optimization, no coupling or energy value, no Lean check and no new physical run was involved.

## Result
|S_G(4)| = **193,662** configurations of the 2^40 = 1,099,511,627,776 nominal ones satisfy the frozen 2-in/2-out rule at all 16 vertices.
Excluded: 1,099,511,434,114. Contraction 1 − 193,662/2^40 = 0.9999998238654 (99.9999824%). One admitted configuration per 5,677,477.4 nominal ones.

| Patch | n | Nominal 2^n | Ice-rule count | Contraction |
|---|---|---|---|---|
| 1×1 | 4 | 16 | 6 | 62.5000% |
| 2×2 | 12 | 4,096 | 82 | 97.9980% |
| 3×3 | 24 | 16,777,216 | 2,604 | 99.9845% |
| 4×4 | 40 | 1,099,511,627,776 | **193,662** | 99.9999824% |

## What was done (three routes, all agree)
- **A. Variable-elimination DP** over the frozen vertex table of `GAP4_v010/output/real_4x4.txt` (16 vertex lines after the 780 coupling lines; coupling lines are never parsed). Also run on `public_1.txt` (6) and `public_2.txt` (82).
- **B. Pruned depth-first enumeration** over the same table (8,672,489 nodes): 193,662 solutions. The ground witness 711243241830 is among them; the two excluded-state ids 711243241766 and 161487427942 are not, as recorded.
- **C. Geometry route.** The vertex table rebuilt from `physical_energy_v005.source_geometry/incident_islands` for L = 1..4 gives counts 6, 82, 2,604, 193,662. The L=4 geometric table equals the file table exactly (same order). The geometric `ice_ok_geometric` agrees with the table rule on all 100,040 probe states (100,000 random plus the 40 single-flip neighbours of the ground state).
The earlier recorded counts for 1×1, 2×2 and 3×3 are reproduced exactly.

## Inputs (read-only)
- `GAP4_v010/output/real_4x4.txt` sha256 `3d47ed1256da7620292a5fe4c64e0bc226b9836768ac87df0ff4fdbf91c5f7a2` (equals `INSTANCE_SHA256.txt`).
- `GAP4_v010/physical_energy_v005.py` sha256 `3364d5524d9f7f020cb35a9cb3dc8136ef056b8f00ada1e229e60021378ad8ac`.
- Public repository commit `4e759d381875c7341e2f26cb72319b44d87aed15` contains the same files.

## Evidence level and limits
- A numerical-combinatorial result, **not machine-checked in Lean**. It uses the same grammar convention as the frozen files (exactly 2 of 4 incident islands inward); agreement of that convention with the geometric rule is evidenced by route C, not proved.
- Route B enumerates the full solution set; routes A and C are exact counts. All are in Python integers; there is no floating point in any count.
- This is the grammar-only count that earlier records marked "not recorded". It adds a contraction value for 4×4 and changes no verdict (G, P, T, C outcomes, the gap, δ₄, the certificates).

## Files
- `grammar_count_4x4_v001.py` (self-contained, standard library plus the frozen `physical_energy_v005.py`; run as `python3 grammar_count_4x4_v001.py <path to scr_iii_b>`; about 1.5 minutes)
- `grammar_count_4x4_v001_output.json` (full output of the recorded run)

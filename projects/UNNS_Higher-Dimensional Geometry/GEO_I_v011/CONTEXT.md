# GEO-I — context handoff after v011 (2026-10-26)

Deliverable of record: `GEO_I_v011.zip`. Frozen: v001–v010, both Mathematical Foundations volumes, the false transfer rules R-MIR/R-EUC/R-LAT (never reuse). Exact arithmetic; failed proofs are never recorded as falsifications; memory writes only under the project subtree.

## Status after v011
| ID | Statement | Status |
|---|---|---|
| G11-T3 (=G10-C1, W2) | every minimal non-embedded binary box has ≥ 2 two-circuit partitions of the all-ones word | **PROVED+CHECKED** |
| G11-L6 | `n_2 ≥ p−1` for `p ≥ 9` (sharp at `p = 16, 32`) | PROVED+CHECKED |
| G11-L5/L5b/L5c | vector-space-partition structure, counting & Parseval identities, no unit circuits | PROVED |
| G11-T4 | universal `r_min = 3` (binary 0/1 model) | PROVED |
| G10-C2 | rank-4 minimal box exists | FALSE |
| G11-C1/T1 | universal small-box cap `H_Q∖H_0 ⊆ U_Q` | **OPEN** |
| G11-T2 | complete planar stabilization | **OPEN** (needs only G11-C1) |
| G11-L3 | one-sided cap (explicit cell family) | CHECKED (39,590 triples d≤60; 544 certs) |
| G11-A | arithmetic lemma for the bottom cell | CHECKED (d≤150), unproved |
| G11-L4 | non-degenerate corner pentagon | CHECKED (345 boxes d≤15) |

## W2 proof in five lines
`V_P=span(blocks)` gives a vector-space partition of `F_2^{k−1}` (rigidity); `Σ(2^m−2)=2^k−2`; Parseval `Σ(2^m S−2p²)=p(2^k−2p)`; blocks ≥ 2 ⇒ `m ≤ p/2`; CS + `p(2^m/m−2) ≥ 2^m−2` (p ≥ 9) ⇒ `n_2 ≥ p−1`. `k=7,p=8` is `E_8` (not minimal); `k ≤ 6` classified.

## Cap: where it stands and the next step
One-sided cap: horizontal sweep cells along `∂W_u` from the record minimum `M` + one bottom cell `P(B−g;g,M)`, `g∈{(1,s−d),(d−t,−1)}`, valid iff `cr(g,M) ≥ x_m y_m` (G11-A). **Next:** prove G11-A (Pareto-chain lattice argument; both-fail ⇒ `d−t<x_m≤t`, `d−s<y_m<s`); prove Graver-ness of boundary steps; find uniform cells for the mixed corner pentagon and top triangle; 4,681 degenerate mixed boxes (`E_y ≥ d` or `E'_x ≥ d`) need their own analysis.

## Files
`theory/circuit_partitions.py`, `theory/cap_cells.py`; `experiments/w2_attack.py`, `cap_attack11.py`, `make_certificates_v11.py`, `figures_v11.py`; `certificates/checker11.py`, `C9_partition.json`, `C10_capcover.json`; `tests/test_geo11.py`; `verify.py` (+ inherited gate `verify_v010.py`); docs `README, REPORT, MATHEMATICS, CAP, CIRCUIT_PARTITIONS, RANK_UNIVERSAL, CERTIFICATION, PRIOR_ART, THEOREM_REGISTRY.tsv`; archived v010 docs in `docs_v010/`. Lessons: `pkill -f` self-matches; background waiters wait on the pid; full verify ≈ 2 h.

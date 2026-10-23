# FIELD-I v003 — Results

`python field3.py`: exit 0, ALL PASS, 0 FAIL (output/field3_output.txt). `RUN_TESTS.bat` runs field2.py (v002), synthesis/g_checks.py (v002) and field3.py. v002/memo/manuscript untouched.

## Collective growth (centrepiece; proved, conditional on adopting C)
- Plateau law: while D is unchanged, x_k = (γ_0+k)·u/v (Δ_coll is reduced, T17′).
- Growth-time bound: T(x) ≤ min_{d∉D} K_d ≤ G(x)·d_min² − 1 (T18). Checked on 1,828 consecutive growth events (457 seeds, R ≥ 1, 4 events each): 0 violations. Typical events are earlier than the bound (median T/bound 0.375; T = bound in 16.8%; largest T seen 77).
- **R(x_n) → ∞ for every realised start** (T19), no plateau of constant multiplicity can be infinite. The review's proof is correct; it holds already for R = 1 (a single route).
- Data: R after successive growth events: 36: 3,5,7,9,11,13,15; 81: 2,5,8,11,14,17,20; 2025/2: 5,11,17,23,29,35,41; 400/3: 2,5,7,9,…; 8: 1,2,3,…; 64: 3,4,5,… Linear growth in the events is observed, not proved.
- Honest scope: elementary result about C only; says nothing about G1-R, and nothing about a rate.

## R=3 rendezvous graphs
- Integer fibres: proved non-rigid (T20). D(m) is divisor- and lcm-closed; R=3 forces {p,q,pq} (all indices equal) or {p,p²,p³} (two equal). Verified on all m ≤ 200,000: 9,826 fibres (7,746 + 2,080), no other shape.
- Rational fibres: **not** non-rigid in general: x = 20736/5, D = {6,16,36}, H = {1,9,16} (T21). The v002 observation "R=3 always non-rigid" was a feature of its bounded corpus.

## Maintenance
Erratum on "only γ matters" recorded (THEOREMS.md). Launcher updated (new file; v002 launcher unchanged).

## Open
Rate of R growth and first-growth value; whether every d ≥ 2 eventually enters D(x_n); classification of rational R=3 fibres; rigidity for R ≥ 4; whether an independent principle selects C over route-aware interaction.

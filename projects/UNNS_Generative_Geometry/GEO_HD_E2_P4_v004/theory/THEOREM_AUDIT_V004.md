# v004 theorem audit
| Claim | Status | Dependency / check | Novelty |
|---|---|---|---|
| P4-Z1 (tiling soundness) | PROVED (inherited) | fine zonotopal tilings exist; vertices are subset sums; not externally reviewed | elementary |
| P4-Z2 explicit zero-vertex criterion | PROVED | coordinate squeeze; 48,715 cells agree with brute force | elementary |
| P4-P1 planar CP3-A | PROVED | P4-Z1 + Z2 + Graver minimality + axis-grid covering; hard-cell structure checked on 183 cells, 17 independently | elementary; prior art NOT searched |
| P4-S3 slab completeness / no S1 failures | PROVED | P4-S2 + zero-allowed tiling | elementary |
| P4-K1 | FALSE (lattice version) | counterexample re-verified (S17) | -- |
| 3D no-free-coordinate preservation | OPEN | -- | -- |
Weak points to review externally: (i) the fine-zonotopal-tiling step of P4-Z1; (ii) step (4) of P4-P1 (the Graver-minimality contradictions) -- each is a two-line argument but is the heart of the proof.
C3 is NOT claimed; the result is a lemma about the realized-geometry construction.

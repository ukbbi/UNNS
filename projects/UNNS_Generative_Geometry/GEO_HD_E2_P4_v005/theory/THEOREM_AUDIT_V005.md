# v005 theorem audit (what each claim rests on)

Independence caveat: all proofs, code and checks in v004 and v005 were produced by the same author (Claude, same project). v005 re-derives P5-P1 from a different decomposition (conformal sum + zero-vertex criterion + hard cells as Minkowski sums of segments + axis-grid covering), and checks it with three code routes (pinned v004 engine, numpy complex `geo3`, brute-force stdlib `mini`), but this is NOT independent human review.

| ID | Statement | Status | Rests on | Weak points |
|---|---|---|---|---|
| L1 | every lattice vector in a box is a conformal sum of Graver vectors | PROVED | induction on the conformal order | none known |
| T0 | tiling lemma: fine zonotopal tiling whose tile vertices are subset sums | PROVED from SF; exact volume/coverage tests | SF = lower facets of a generic lift project to a regular subdivision (textbook) | SF cited, not reproved; Bohne-Dress texts unread |
| Z | zero-vertex criterion | PROVED | T0, L1 | depends on T0 |
| LG | adjacent corners share a support coordinate | PROVED | Graver minimality | none known |
| H1 | hard cell = Minkowski sum of segments; only the origin star can escape | PROVED | Z, LG | most intricate step; checked by planar_audit structure tests (1)-(6) |
| P5-P1 | planar monotonicity of U | PROVED (rank-2 nested lattices, all boxes) | H1 + axis-grid covering | needs expert read |
| P5-P1.a | FIELD-I corollary valid only if Lambda_x <= Lambda_{C(x)} | PROVED (scope correction) | P5-P1 | the FIELD-I side was read, not re-derived |
| P5-F1 | cells in a coordinate plane are contained | PROVED | reduction to planar | |
| P5-D1 | diagonal dilation invariance | PROVED | definitions | |
| P5-C1/C2 | 3D no-free-coordinate conjecture FALSE (explicit cell, infinite family) | PROVED by hand + 3 routes | explicit witness p=(2/3,5/3,5/3) | none; fully checkable by hand |
| P5-C3 | BCC target also fails | FINITE-EXACT (engine certificate, independently verified) | exact engine | no hand proof |
| P5-S4 | split-target slab law and exact criterion | PROVED; pointwise union identity on 30,240 grid points; criterion vs engine 574 hard cells, 0 disagreements | slab decomposition | |
| P5-Q1 | which non-split targets preserve U | OPEN | census only | |
| C3 | -- | NOT CLAIMED | | |

Failed predictions kept: P4-K1 (lattice version, v003/v004) FALSE; "no free coordinate => preserved" (P5-K2) FALSE; "no split coordinate => preserved" FALSE (BCC).
Unavailable: no zbMATH/MathSciNet; no human referee; scans are finite (box-capped); extended census coverage see results/P5_SCAN3D_EXT.json.

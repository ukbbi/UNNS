# GEO-I v002 — Intrinsic Arithmetic Geometry, Modular Lattice Moves, and Cell Complexes

*Research report (no LaTeX manuscript at this stage). Separate active project: GEO-I v001 and the published `UNNS_MATH_FOUNDATIONS` archive (read-only, commit `fefa7910c807a5fdac90980749a5d7993e3ec0ca`) are unchanged; the v001 manifest still verifies.*
Verifier: `python3 verify.py` → **26/26 PASS** (full, 22 s); `--smoke` 26/26. Proofs and statuses: `MATHEMATICS.md`.

## 1. What was built
Two explicitly defined geometries on the realized fibre `F_x = (B_x ∩ Λ_b) ∖ {0}`:
* **K_axis** — cubical complex, unit-step adjacency.
* **K_move** — cubical set whose edges are the **region Graver moves** of `Λ_b` and whose higher cells are parallelotopes spanned by independent moves with all vertices in the fibre.
Dimensions `d_amb`, `d_aff`, `d_cell`; exact boundary matrices; Betti numbers over GF(2) and GF(2³¹−1) (they agreed on every complex — no torsion evidence); clique complex of the move graph as a comparison structure. Everything is exact integer arithmetic.

## 2. Mandatory experiments
| | Result (exact) |
|---|---|
| spec table | `(R, d_amb, d_aff, d_cell)`: 72 (3,2,2,1); 144 (5,2,2,2); 3600 (11,3,3,3); 44100 (15,4,4,3); 210⁴ (80,4,4,4); 2304/5 (2,2,1,0) — all reproduced |
| **E1** 3600 | 11 / 17 / 8 / 1 cells (0..3), χ = 1; full 3-cell `{1,2}×{0,1}×{0,1}` certified with 8 vertices, 12 edges, 6 faces, all in the complex |
| **E2** 44100 | 15 vertices, cells 15/28/18/4, **no 4-cell**; the four 3-cells are the far facets `a_i = 1` |
| **E3** 210⁴ | 80 vertices (the spec's "80" is correct: exponents 4 give q = 2, box 3⁴); cells 80/212/210/92/15; 4-cell `{1,2}⁴` certified: 16 vertices, 32 edges, 24 squares, 8 cubes |
| **E4** 2304/5 | coordinate adjacency: 0 edges, 2 components; move adjacency: 1 edge, vector (3,−1); region Graver set {(1,1),(3,−1),(4,0)} |
| **E5** corpus | 8,203 rational fibres (denominators 2..31 with numerators ≤ 20,000, plus L²/g reset states for 19 moduli); 0 skipped |
| **E6** dynamics | SELECT-II (3,124 edges ≤ 5000) and seven C-orbits (60 steps each) tracked separately; never combined |

## 3. Results
**Proved (details in `MATHEMATICS.md`).**
1. *Dimension classification, integer fibres* (your GEO-T1 baseline): `d_cell = k` if some `q_i ≥ 2`, else `k−1`. Elementary.
2. *Integer fibre complexes are contractible* (star-shapedness).
3. **Theorem A — the coordinate complex of any rational cut has no topology beyond its components.** `S = {i : p_i ≡ 1 mod b}`, `T` the rest: `#components = |(Λ_T∩B_T)∖0| + [S≠∅]`, all higher Betti numbers vanish, and `d_cell` has a closed formula. Matches all 8,203 fibres. For the g = 11 orbit it explains why the coordinate complex is edgeless (S = ∅, components = R).
4. **Theorem B — your GEO-T2 holds:** the Graver-move graph of a nonempty fibre is connected, including the awkward case where a conformal path would cross the removed origin (handled by a short origin lemma). This is Graver/Markov-basis theory plus the origin lemma — not claimed as new. 8,203 / 8,203 fibres connected.
5. K_axis ⊂ K_move, so `d_cell(move) ≥ d_cell(axis)` (strict on 264 fibres); SELECT-II changes `d_amb` by `−ω(N)..+ω(N+1)` and is **not monotone**; in C-orbits `d_amb`, `d_cell` are eventually periodic.

**Measured — not yet theorems.**
* **The move complex carries real topology.** `b₁(K_move)` is nonzero on 38 corpus fibres (moduli 3, 5, 7), and along G > 1 orbits grows to 8–25. In 8,086 of 8,203 corpus fibres `b₁ = max(0, |G⁺| − k)`, i.e. the number of Graver moves minus the lattice rank: each independent *relation among moves* is a cycle not filled by commutation squares. Smallest cases: 1600/3 (a triangle, `(2,0) = (1,1)+(1,−1)`), 19600/3 (an unfilled pentagon). **This is a conjecture, not a theorem: the upper bound `b₁ ≤ |G⁺|−k` is false** (9 of 420 orbit states exceed it, e.g. g = 11 orbit from L = 2·3³·5⁴ at n = 8).
* Along persistent G > 1 orbits `b₁` stops growing (constant over the last 15 of 60 steps in 5 of 6 orbits) while R keeps growing linearly; `b₂` keeps growing. Higher homology is absent from every corpus fibre (≤ 300 points).
* **Caution:** the topology depends on the cell definition. The clique complex of the same move graph is acyclic on the g = 11 orbit; it is nontrivial on 16 corpus fibres, mostly b = 2 where the cause is simply unfilled grid squares.

## 4. Answer to the gate question
*Is there higher-dimensional structure beyond coordinates?*
* **Established:** a precise, verified theory of what is 3D/4D in UNNS fibres — genuine 3-cells (3600) and 4-cells (210⁴), a fibre such as 44100 that is 4-dimensional but has no 4-cell, exact modular-move connectivity (Thm B) and a complete topological classification of the coordinate geometry (Thm A).
* **Information beyond the coordinate definition, so far:** (i) move connectivity — fibres that are totally disconnected under unit steps are always connected under Graver moves; (ii) Thm A links geometry to evolution quantitatively (components = R along g = 11; quasi-linear growth by v001 Thm 3.2); (iii) `b₁` of the move complex tracks the relation structure of the moves and stabilises along orbits. 
* **Not established:** any predictive use of the topology for eventual scaling, any geometry that does not reduce to lattice/Graver theory, any new general theorem about `H_{≥2}`. The `b₁` law is a conjecture with a counterexample to its natural bound. So the honest status is *higher-dimensional geometric structure: yes, rigorous and verified; new geometric theorems: one classification (Thm A) and a connectivity result of known type (Thm B); the topological conjectures remain open.*

## 5. Open problems (priority order)
1. Prove/refute M1 (`b₁` = Graver relation rank in a saturated regime) and explain the 117 deficits and 9 excesses.
2. Growth law of `b₂` along orbits; is it a boundary effect?
3. Eventual constancy of `b₁` along persistent orbits (5/6 observed).
4. Any theorem tying a topological invariant of `K_move` to the eventual `(P, s, p)` of the C-orbit (GEO-T4).
5. Composite/even g (O12.2): not tested here.

## 6. Acceptance checklist (review status, not self-certification)
- [x] six benchmark experiments reproduced exactly
- [x] both adjacency constructions defined; coordinate side checked against Thm A's independent formula, move side against an independent conformal-decomposition completeness test
- [x] 3D and 4D cells certified from vertex and face data (`geometry/cells/certified_cells.json`)
- [x] dimension classification proved (T1) or marked conjectural (M1, M2)
- [x] topology computed from finite complexes, mod 2 and mod 2³¹−1
- [x] Foundations archive and GEO-I v001 unchanged (v001 manifest verified)
- [x] verifier 26/26; nothing skipped (0 fibres over the 300-point cap); undetected/unresolved items listed in §5
- [~] novelty/previous work: included in `MATHEMATICS.md` §5, references from memory and not re-verified; an expert literature check is still needed

## 7. Files
`MATHEMATICS.md` (definitions, proofs) · `verify.py`, `geometry/geo2lib.py` · `geometry/{fibres,cells,modular_moves,topology}/` (exports) · `dynamics/` · `experiments/` (figure and export scripts) · `figures/` (V1 3600 cell layers, V2 4D projection + slices, V3 modular-move comparison, V4 dynamics) · `tests/` · `output/` (verifier JSON, corpus CSV, witnesses) · `RUN_SMOKE.bat`, `RUN_FULL.bat`, `MANIFEST.sha256`.

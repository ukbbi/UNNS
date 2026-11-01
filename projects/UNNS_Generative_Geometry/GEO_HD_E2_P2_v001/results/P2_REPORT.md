# GEO-HD-1B / E2-P2 — Arithmetic criteria for geometric transport between non-trivial relation lattices

Spec: E2_P2_SPEC_v001. Proofs: `theory/THEOREMS.md`. Certificates: `results/P2_CERTIFICATES.json`. Figures: `figures/`.

## Verdicts (kept separate)
| gate | verdict |
|---|---|
| Exact computation (preflight ARITH, CELL, GEOMETRY, generalization) | **EXACT_PASS** — see certificates; builder and audit share no code |
| Scoped theorem | **THEOREM_PASS (SCOPED)** — P2-TF1 (complete edge-survival classification of the infinite family 21^{2h}/5 → 21^{2h}/4, all h ≥ 1) plus T1, T2, T3, L1, L2; all elementary |
| Main gate C3 | **C3_CANDIDATE NOT claimed.** No result beyond inherited GEO-I and standard Graver facts qualifies; the effective survival test and rank bound are elementary |
| Conjectured laws | **COUNTEREXAMPLE** to six preregistered propositions P2-F1…F6 and to "the lattice never shrinks" (CE-P2-L6) |
| Planar containment CP2; coupled k=3 theorem; geometric prediction | **OPEN** |
| k=3 geometric comparison beyond E2-P1; 4-D; interactive viewer; comparison with GEO-I v012 hypotheses | **UNAVAILABLE** |
| inherited exhaustive GEO-I/Foundations suites | **NOT_RERUN** |

## 1. Exact arithmetic
P2-A: 21⁸/5 → 21⁸/4: D has 6 indices, L = 21⁴, G = 20, C = 21⁸/5 + 21⁸/20; primes (3,7), box (4,4). P2-B: 55¹²/27 → 55¹²/18: L = 55⁶, G = 54, primes (5,11), box (6,6). Both reproduce the specification's preflight counts (6→12 vertices, 11→29 edges, 12/8 Graver vectors; 6→8, 5→17). One typo in the specification: P2-B's lattices are a ≡ b (mod 18) and a ≡ b (mod 6) (not "(a,b) ≡ 0").

## 2. Relation-lattice classification
P2-A: Λ₅ = {a ≡ b (4)} ⊊ Λ₄ = {a ≡ b (2)} (indices 4 → 2); P2-B: Λ₂₇ ⊊ Λ₁₈ (18 → 6). **Denominator 5 → 4 is not divisibility-related yet the kernels are ordered** (T1). Over 596 admissible FIELD-I transitions (same primes and box, both lattices non-trivial, ≠): ENLARGE 275, SHRINK 262, INCOMPARABLE 59. The fibre always grows (F ⊆ F′), even when the lattice shrinks.

## 3. Graver-generator changes
P2-A: 12 source vectors, 8 target, common {±(1,1)}. P2-B: source {±(1,1)} (the entire Graver set), target 16 vectors containing it. Lemma L2: from the target orders ord₄(3) = ord₄(7) = 2 alone, all five vectors (4,0),(0,4),(1,−3),(3,−1),(2,−2) are blocked ((2,0) or (0,2) lies conformally below each), so the O(k) rule is exact here and predicts the survivor set {±(1,1)} without any target enumeration.

## 4. Cell survival
P2-A: vertices 6/6 kept; edges 3 kept (the consecutive diagonal), 8 lost, 26 new; the single 2-cell lost, 22 new. P2-B: vertices and all 5 edges kept; 12 new edges, 2 new 2-cells. **P2-TF1** (all h ≥ 1): surviving moves = {±(1,1)}, no 2-cell survives, survivors are the (1,1)-edges, E_kept = Σ c_r(h)² − 1 ≈ h²/4, against ≈ 3h²/2 source edges: **one sixth of the source edges survive asymptotically**. Prediction without the target complex (T2/T3) matches direct reconstruction on all 596 corpus rows.

## 5. Geometric-union comparison (k = 2, exact)
P2-A: U ⊊ U′: all 11 edges and the 2-cell lie in U′ although 8 edges and the 2-cell are abstractly lost (CE-P2-F4); realized Betti (1,2,0) → (1,0,0); abstract (1,5,0) → (1,2,6); both unions non-embedded. P2-B: U ⊊ U′ with all cells contained; realized Betti (1,0,0) → (1,2,0): the enlargement creates two holes. In all 266 planar ENLARGE rows and P2-F21 (h ≤ 8) U ⊆ U′ (conjecture CP2, not proved; 199 rows combine abstract edge loss with complete geometric containment).

## 6. Counterexamples (certified)
F1 strict enlargement keeping every old edge (P2-B; 57 rows) · F2 fibre inclusion without lattice order (321 transitions, e.g. 5690339646868044961/22 → …/20 INCOMPARABLE; 83733937890625/9 → 586137565234375/54 SHRINK) · F3 denominator rule (121 rows) · F4 abstract loss, geometric retention (199 rows) · F5 the planar containment pattern fails for the coupled three-coordinate transition of E2-P1 (cell P((0,0,2);(0,1,−1),(1,0,−1)) contains (⅔,⅔,⅔) ∉ U′) · F6 same class and indices (16 → 8), different survival · L6 the lattice can shrink under C.

## 7. Theorems — see `theory/THEOREMS.md` (L1, T1, L2, T2, T3, TF1, finding P2-D).

## 8. Comparison with GEO-I / known mathematics — `theory/SOURCE_OVERLAP.md`. Everything proved is elementary; nothing here is claimed as an independent discovery beyond the explicit family classification and the counterexamples. The relation of CP2 to GEO-I v012 planar coverage is **unchecked**.

## 9. Reproducibility
`python RUN_VERIFY.py` (full, includes byte-for-byte rebuild of all eight data/result files) or `--fast`; `python -m unittest discover -s tests`. Tamper tests: stored data mutated in a temporary copy must be rejected.

## 10. Answer to the scientific question and unresolved obligations
*When FIELD-I changes the modular relations among existing occurrence coordinates, can we determine in advance what survives?* **Yes for the algebraic layer, not yet for the geometric layer.** In advance (without target construction) we can decide the lattice class (T1), which Graver generators survive (T2, with an O(k) necessary test, L2), and therefore exactly which source cells survive and up to what dimension (T3); for the explicit family P2-F21 this is a closed formula. New admissible cells are the target cells with a generator outside G ∩ G′ or a vertex in F′ ∖ F. **Which regions persist geometrically is not predicted by this layer**: abstract loss is compatible with complete geometric retention in the plane (CP2 pattern) and with geometric loss in dimension 3, and the topology of the union can lose holes (P2-A) or gain them (P2-B). Open: CP2; an arithmetic obstruction criterion for containment (T4); a genuine k ≥ 3 theory (T5; only 14 abstract k=3 rows, no 3-D geometry beyond E2-P1); the sharp condition for the order rule.
Limits: builder and audit are by the same author; CONTAINED claims rest on one exact method implemented twice plus rational probes; corpus rows with ∏ orders > 20000 are UNAVAILABLE (337 k=2 states).

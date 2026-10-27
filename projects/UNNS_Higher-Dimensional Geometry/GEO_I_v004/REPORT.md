# GEO-I v004 — Report

*Arithmetic Obstructions and Stable Higher-Dimensional Geometry.*  Status labels: **[P]** proved by hand · **[C]** exact computer-assisted proof / finite certificate · **[O]** observed in exact data, unproved · **[Open]**.  Full statements and proofs: `MATHEMATICS.md`.  Constraint honoured: no change to GEO-I v001–v003, the Foundations manuscripts, or GitHub.

## 1. Answers to the two gates

### G4-C1 — planar stabilization (k = 2)

| Question | Answer |
|---|---|
| Does `q_i > o_i` for both `i` force `β_1(U) = 0`? | **No.**  13 certified counterexamples with explicit moduli, residues and primes (`output/data/counterexamples_g4c1.jsonl`); simplest: `x = 2^10·7^10/15`, `b = 15`, `q = (5,5)`, orders `(4,4)`: `K_abs` is embedded and `β(U) = β(K_abs) = (1,2,0)`.  Three independent exact routes (v003 pipeline over Q, scaling model, nerve of the maximal-cell cover over Q) agree.  **[C]** |
| What is true? | After the scaling reduction **[P]** every planar fibre is a pure lattice `Γ_{d,s}` in a scaled box `Q`.  For `d ≥ 2`, `Q ≥ (d,d)`, `Q ≠ (d,d)`: `U = conv(F)` (so contractible).  At `Q = (d,d)` `U` is hollow with `β_1 = B(d,s)` (`= d` for `s = -1` **[P]**, `= 2` otherwise **[C]**, `d ≤ 12`). |
| How far is it proved? | A **translation lemma [P]** reduces "all boxes `Q ≥ d`" for a fixed `(d,s)` to the `(2d)^2 - 1` boxes of the window `[d,3d-1]^2`.  **[C]** certified for **every** `(d,s)` with `2 ≤ d ≤ 13` (42 types, 15 048 boxes, zero violations; `d = 1` handled by hand).  **General `d` is [Open]**; `d ≥ 14` is not certified. |
| Independent check | 2 747 in-scope boxes of an exact scan over *all* lattices with orders ≤ 10 (3 215 boxes): the corrected statement predicts `β_1` in every box (0 mismatches); 59 boxes have `q_i > o_i` and `β_1 ≠ 0`. |
| Why did v003 look right? | For `a = c = 1` (e.g. `b=5, (2,3)`) the hollow box `Q=(d,d)` is `q = o`, which `q_i > o_i` excludes.  Counterexamples need `a, c ≥ 2` (`o_i` not equal to `d`). |

**Programme consequence.**  Stabilization is *not* the clean `q > o` law v003 suggested.  It is a threshold phenomenon governed by the pair `(d,s)` — the intersection `<p_1> ∩ <p_2>` and how the two cyclic groups meet inside it — with exactly one exceptional box per type.  A full proof needs an argument uniform in `d`; none is claimed.

### G4-T3 — finite obstruction criterion (any k)

* **T-REL [P]:** a face-closed polyhedral family is embedded iff the relative interiors of distinct cells are disjoint.
* **T-FIN [P]+[C]:** `K_abs(Λ,q)` is embedded iff `q` dominates no element of a finite antichain `Obs(Λ)` of **minimal obstruction boxes**, computed from finitely many *templates* `(A,B,δ)`, `δ ∈ Λ ∩ open zonotope`; both directions are proved (every realized template is a genuine non-face intersection; every non-face intersection is a realized template), with an explicit finite window for the base point `u`.
* **Validation [C]:** template prediction vs the v003 exhaustive polyhedral audit (separate code paths) on **10 852** `k=2` cases (233 residue classes, `b ≤ 14`, 3 431 non-embedded) and **1 450** `k=3` cases: **0 disagreements**.  `verify.py` repeats a large subset.

| Piece | Result |
|---|---|
| **G4-T4 Klein-four** (`Z^3 → Z/2×Z/2`) **[C]** | Exactly two lattices.  Type `(a,b,ab)` (`Λ = {α_1≡α_2≡α_3 mod 2}`, e.g. `b=8, (3,5,7)`): nine minimal boxes, the permutations of `(1,1,4)` and `(1,2,3)`; **all O-D** (a diagonal edge inside a 2-cell that lies in the non-coordinate plane spanned by `(0,0,2),(1,1,-1)`); `(2,2,2)` is embedded.  Same atlas for every modulus tested.  Type `(a,a,b)`: `{(1,3,2),(3,1,2),(2,2,2)}` plus four planar boxes. |
| **Erratum to v003** | v003 said "non-embedded from `q ≥ (3,3,2)`": true, not sharp (`(3,2,1)` already fails).  Recorded here; v003 untouched. |
| **G4-T5 the O2 case** `b=5, (2,3), q=(4,4)` **[P]** | Cell `P((0,4);(1,-3),(3,-1))` with the lattice point `(2,2)` at its centre; the Graver edge `(0,4)–(2,2)` (move `(2,-2)`) lies inside the cell without being a chord (**O-T**).  No edges cross.  Box minimal; `(3,4),(4,3)` embedded.  Atlas `{(1,8),(2,5),(4,4),(5,2),(8,1)}`: `(2,5)/(5,2)` are the v003 crossing (82944/5).  For `s=1` the O2 box `(d,d)` coincides with the hollow box. |
| **G4-T6 essential dimensionality** **[C]/[P]** | Adjoining a prime with residue 1: every obstruction persists **[P]**; whether the complex is embedded *for all boxes* never changes (102 classes, `b ≤ 12`; proved for k=2→3); **but thresholds are lowered** in all 88 non-direct ones (the 14 direct-product classes have empty atlases), always at height `q_3 = 1` (e.g. `b=5,(2,3)` gains `(1,5,1),(5,1,1)`).  So "a residue-1 prime is not essential" holds for classification and **fails for thresholds**.  In every atlas computed the minimal obstructions are *planar* (span dimension 2) with support 2 or 3. |
| **Genuinely 4D** **[C]** (exhaustive audits; template atlas for k=4 **UNAVAILABLE**) | Parity lattice `Σα_i even`: `k=3` first obstruction `(2,1,1)`; `k=4` has the new box **`(1,1,1,1)`** that no 3D box explains.  Lattice `b=24, (5,7,13,23)` (all coordinates same parity, `|H|=8<16`): embedded for all `max q ≤ 2`; minimal non-embedded boxes over `[0,4]^4`: `(3,2,1,1)` and `(4,1,1,1)`; no crossing edges. |
| `k=2` atlas **[O]** | `s=1`: `{(1,2d),(2,d+1),(d,d),(d+1,2),(2d,1)}` (`3 ≤ d ≤ 7`); `s=-1`: antidiagonal `Q_1+Q_2 = 2d+1`; other `s` irregular.  Not proved. |

**Programme consequence.**  A universal arithmetic classification of embeddedness is **not** achieved: what exists is a complete *decision procedure* (T-FIN) plus censuses.  The recurring structure (planar minimal obstructions in possibly non-coordinate planes; diagonal chords) suggests a conjecture that minimal obstructions always span a 2-plane — **[Open]**, supported only by the atlases computed.

## 2. The nine mandatory benchmarks (exact; `verify.py`)

`3600` (cells 11/17/8/1, embedded) · `210^4` (80/212/210/92/15, embedded) · `44100` (15/28/18/4, embedded) · `2304/5` (two points, one move edge, embedded) · `82944/5` (crossing at `(3,1)` ∉ Λ; non-embedded; Betti `(1,2,0)` vs `(1,0,0)`) · `2^{10+2t}3^4/5` (non-embedded; `β_2(K_abs) = ⌊t/4⌋` unbounded; `β(U) = (1,0,0)`) · `27348890625/8` (b=8, q=(3,3,2): no crossing edge, non-embedded, predicted by templates) · `5489031744/5` (30 interior edge crossings; predicted by edge-level templates) · `b=5, (2,3), q=(4,4)` (O2).

## 3. Experiments E1–E5

E1 stabilization certificates (`stabilization_certificate.py`, windows `[d,3d-1]^2`) and the general-lattice scan · E2 counterexample search (`counterexample_search.py`) · E3 obstruction atlases (`k2_atlas.py`, `klein_four.py`, `obstruction_kinds.py`) · E4 template-vs-audit validation (`validate_templates.py`) · E5 higher dimensions and essential dimensionality (`high_dimensional.py`, `essential_dimension.py`).  Figures: `fig1_hollow_vs_filled`, `fig2_beta1_at_dd`, `fig3_k2_obstruction_atlas_d7`, `fig4_phase_map_b5`, `fig5_higher_dim_minimal_boxes`.

## 4. Gates

| Gate | Status |
|---|---|
| G1 stabilization | **Partially met.**  Original conjecture refuted with certified counterexamples; corrected statement formulated, reduced to a finite window per type (proved) and certified for `d ≤ 13`; general proof **not** obtained. |
| G2 obstruction theory | **Met** for the criterion (T-REL, T-FIN proved both ways); classifications are exact computations, closed forms in `d` are conjectural. |
| G3 genuine higher dimensions | **Met** (3D Klein-four, 4D parity `(1,1,1,1)`, `b=24` example); `k=4` template atlas UNAVAILABLE. |
| G4 independent validation | **Met** (template vs audit, three Betti routes, scan vs prediction). |
| G5 research integrity | **Met** with flags: priority not assessed; the specification's "Ramras 2026" could not be confirmed (only a 2023 arXiv paper found, background only); Bauer–Kerber–Roll–Rolle verified at arXiv level. |
| G6 reproducibility | `verify.py`: **37 core checks**, identical count in `--smoke` and full mode, using only files inside the release (verified after a clean unzip, see below); 3 optional sibling-integrity checks reported separately. |
| G7 preservation | v001–v003, Foundations, GitHub untouched; frozen libraries hash-checked; sibling manifests checked optionally. |

## 5. Limits and what to do next

1. **Not shown:** stabilization for all `d`; `B(d,s)=2` for `s≠-1` in general; closed forms of the `k=2` atlas; any `k ≥ 4` classification; any bound on the span dimension of minimal obstructions.
2. The topology of `U_x` is that of the chosen parallelotope realization; no intrinsic topology is claimed.
3. **Suggested order for the next programme** (decided by these results rather than assumed): (i) a uniform proof of stabilization via the structure of `Γ_{d,s}` — only worthwhile because the finite certificates now show where it could fail; (ii) prove the `s=±1` atlases; (iii) test the span-2 conjecture on `k=4` lattices with a pruned template search; (iv) only then return to survivor prediction.  A negative outcome in (i) at some `d ≥ 14` would itself be informative.

## 6. Verification record

`python3 verify.py` → **CORE 37/37 PASS** (full mode, ≈ 4–5 min on two shared cores); `python3 verify.py --smoke` → 37/37 (≈ 2 min).  Both were run on a clean extraction of the final zip (sizes and times in `output/reports/verify_full.json`).  Optional: `GEO_I_v001`, `GEO_I_v002`, `GEO_I_v003` manifests verified unchanged (read-only).
Long runs whose results are shipped (not recomputed in full by `verify.py`, but re-checked for consistency and sampled): the base-window certificates for `d ≤ 13` (`stabilization_certificates.jsonl`), the template-vs-audit validations (`validation_k2_templates.jsonl`, `validation_k3_templates.jsonl`), the essential-dimension run, the general-lattice scan and the `k=2` atlas.  Each can be regenerated with the script of the same name in `experiments/`.

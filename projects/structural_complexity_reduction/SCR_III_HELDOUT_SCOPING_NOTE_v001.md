# SCR-III Held-out Physical Systems — Scoping Note v001 (DRAFT, UNFROZEN)

**Date:** 2026-10-10 · **Status:** scoping only. Nothing here is preregistered, ratified or authorized. It does not modify the frozen SCR-III-B protocol or its result.
**Question:** how should regime-dependent generative admissibility be investigated on physical systems that are genuinely held out, without adjusting the grammar to recover the 16 known excluded states?

## 1. What the primary result leaves us with
- G PASS, P FAIL, T NOT_TESTED, C NOT_ELIGIBLE (see PRIMARY_RESULT_v001.md, PRIMARY_AUDIT_v001.md).
- P is decided by the gap theorem: preserved iff W + tau < Δ_nonG. For 3×3, Δ_nonG = 0.9429 kT at 792 K, versus the 1 kT window. The 1×1 and 2×2 patches gave 0.871 and 0.952 kT.
- The 16 false exclusions are degenerate in energy (0.94290 kT each, equal to ~1e-14), so they look like one symmetry orbit of a single local excitation type. This is an observation about the results, not a tested mechanism.

## 2. Post hoc observation (exploratory; not evidence for anything preregistered)
In the v005 model the couplings K are geometric and temperature enters only through A(T) ∝ M(T)², with M = M0(1−T/Tc)^0.5, Tc = 820 K. The 3×3 gap in A units (0.010212546) therefore gives Δ_nonG/kT as a function of T, using only quantities already in the result:

| T (K) | 100 | 300 | 500 | 700 | 750 | 790.4 | 792 | 810 |
|---|---|---|---|---|---|---|---|---|
| Δ_nonG / kT | 192 | 46.2 | 17.1 | 4.57 | 2.49 | 1.000 | 0.943 | 0.33 |

The 1 kT criterion therefore fails only because T_ref = 792 K lies 1.6 K above a crossover at T* ≈ 790.4 K, close to Tc where M collapses. Consequences for design:
1. "Regime dependence" of P on this model is a one-parameter curve already determined by Δ_nonG(A units) and M(T). Reproducing it on more patches would test little unless Δ_nonG itself changes.
2. At low T, P passes trivially, because the target shrinks to near the ground states. A pass there is weak evidence of physical sufficiency.
3. The informative questions are: (a) does Δ_nonG (A units) stay near-constant with patch size and geometry, as a local-excitation picture would imply, and (b) does the grammar capture what matters for targets that are NOT an energy window. (b) is hypothesis T.
This calculation used the already-unblinded 3×3 and the model's validity range (T < Tc). It must not be cited as a prediction.

## 3. What counts as held out
Already consumed and unusable as held-out: 1×1, 2×2, 3×3 free-boundary square ice with the Dryad SPMMC dumbbell model at 792 K, with the 2-in/2-out grammar, energy-window targets and the 16 known FN ids. Held-out means at least one of the following is new and fixed before any outcome is computed, and the label is only valid while no outcome for that item has been seen:

| Axis | Held-out candidate | Why it is informative | Main risk |
|---|---|---|---|
| Size | 4×4 free boundary (n = 40) | Tests whether Δ_nonG (A units) is size-independent | 2^40 is not brute-forceable; needs exact branch-and-bound or similar; feasibility must be shown outcome-blind on synthetic instances |
| Geometry | Other lattice with a different local rule (e.g. kagome 2-1/1-2) | Tests whether the grammar idea carries beyond square ice | New Hamiltonian, new grammar, new validation; gap theorem still makes P energy-window-equivalent |
| Hamiltonian | Same lattice, different interaction (e.g. nearest-neighbour or truncated range) | Separates grammar from model details | Gap may change trivially with coupling truncation |
| Target | Non-energy-window target (observable, sampled ensemble, vertex-type statistics) | Only axis that can test T, since energy-window targets are gap-equivalent to the grammar | Needs an independent target definition and a falsification rule |
| External data | Unanalysed experimental or simulated states, e.g. `data/raw/mean_200nm_300K_50x50_verteximage.npz` is in the project tree | Real, outcome-independent target | Not yet inspected for SCR-III-B purposes; must confirm it has not been used in any grammar or window choice; noise and finite-T mixing |

## 4. Recommended structure (for discussion)
1. **Stage A, T-protocol first.** Because an energy-window target cannot test physical transfer (SPEC §1), define one target family that is not an energy window, with its own hypothesis, holdout and falsification. The vertex-type statistics in the external 50×50 image are the cheapest candidate, if it qualifies as untouched.
2. **Stage B, one falsifiable scale prediction.** Before computing anything for 4×4: state the predicted range of Δ_nonG (A units) and a pass/fail rule for "size-independent local excitation gap". This is the only prospective test that §2's observation supports. Run it only after an outcome-blind feasibility gate for the solver at n = 40.
3. **No grammar modification on the known data.** Any revised grammar is a new grammar. It may be judged only on held-out items, never on 1×1–3×3, and must be frozen before those items are touched. The 16 FN ids must not enter its design.

## 5. Rules to carry over unchanged
Outcome blindness with the invocation audit; G/P/T/C reported separately; no inferential claims without calibration; sensitivities cannot rescue a primary; failures reported, not repaired; shared authorship of grammar and verifier disclosed; additive versioned records; GitHub untouched until Igor decides.

## 6. Decisions needed from Igor
1. Which held-out axis first: external-data target (Stage A), 4×4 scale prediction (Stage B), or both?
2. Is the 50×50 vertex image eligible, or has it already informed any SCR-III-B choice?
3. For T: what physical quantity should the grammar be required to reproduce, and what result would count as failure?
4. Is the model's near-Tc regime even the right place to ask the question, or should the reference temperature be set by the data, before looking at gaps?
5. Does a different-source physical check (original Dryad SPMMC code) need to be restored to disk before any held-out run?

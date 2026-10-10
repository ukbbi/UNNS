# SCR-IV v002 — Certification status

**Date:** 2026-10-10 · **Toolchain:** Lean 4.34.1 (commit 5045d0056413), Lake 5.0.0, core only (no Mathlib) · **Built and run in:** Claude's Ubuntu 24.04 cloud container, **not yet in your WSL**. Run `bash RUN_TEST.sh` there to produce your own log.

| Stage | Verdict | Basis |
|---|---|---|
| IV-1 | **MODEL_FORMALIZED** (unchanged from v001) | v001 source files byte-identical; 25 theorems still pass |
| IV-2 | **WITNESSES_CERTIFIED** (unchanged from v001) | same 25-theorem axiom audit |
| IV-3 | **PRUNING_THEOREM_PROVEN** (scope below) | 44 kernel-checked theorems, `SCR_IV_Check3.lean` audit clean |
| IV-4 | PENDING | not started; no certificate generated or traversed |
| IV-5 | PENDING | not started. **The 4×4 gap is NOT promoted to a globally certified result.** |

## IV-3: what the Lean kernel has checked (no `sorry`, no extra axiom, no `native_decide`; only `propext`/`Classical.choice`/`Quot.sound`)
All statements are universally quantified; the 2^40 space is never evaluated. The only `decide +kernel` calls are finite table facts (`kRows = rowsL kAt 40 0 40`, the 16-vertex filter on the two frozen witnesses) and the tiny negative/positive controls.

1. **Energy decomposition** (`decomposition`): H = A(assigned,assigned) + Cross(assigned,unassigned) + UU(unassigned,unassigned), for arbitrary integer couplings and any depth d ≤ n.
2. **Lower-bound validity** (`lower_bound`, `lower_bound_ids`): B(p) ≤ H(s) for every prefix p and every ±1 completion s; at a full assignment the bound equals H (`bound_exact_at_leaf`).
3. **Pruning soundness with ties explicit** (`prune_sound`, `prune_no_strict_improvement`, `prune_strict_keeps_ties`, `prune_may_discard_tie`): B(p) ≥ U ⇒ no completion strictly below U; a strict prune keeps ties; a non-strict prune can discard a tie (explicit counterexample).
4. **Partition completeness** (`partition_cover`/`_disjoint`/`_sound` on spin functions; `partition_ids_cover`/`_disjoint`/`_sound_plus`/`_sound_minus` on configuration ids): the two children of an unfinished prefix cover every completion exactly once and contain only completions of the parent.
5. **Grammar pruning** (`violated_persists`, `completed_violation_persists`, `grammar_prune_sound`, `cppPossible_false_sound`, `cppViolates_iff`): a violated vertex stays violated under all later spins; the C++ `possible_violation` filter only discards subtrees containing no non-grammar state; `violates()` ⇔ ¬IsGrammar. The grammar and non-grammar objectives are separate definitions (`ObjGrammar`, `ObjNonGrammar`, `ObjAll`; `objectives_distinct`, `objective_relation`, `discard_ground`, `discard_nonGrammar`).
6. **Bridge to the frozen model** (`hScaled_eq_Hs`): the frozen list energy `hScaled id` equals the abstract energy of the decoded spins for every id.
7. **Faithful solver bound** (`solverBound_eq_Bnd`, `solver_prune_sound_ids`): the loop nest of `solver_v010.cpp::bound` (j outer, h inner, running `acc`) transcribed as folds equals `Bnd`; see `SOLVER_CROSSREF.md`.

## Controls
Negative controls (false claims, each rejected by the kernel with "decide proved … is false"): `neg_b_nofield`, `neg_b_notail`, `neg_b_reverse`, `neg_tie_strict`, `neg_partition`, `neg_solver_sign`, `neg_gfilter`, `neg_gfilter_leaf` plus the four v001 controls. `tests/pos_controls.lean` holds the true twins and must compile. `scripts/diff_test3.py` (evidence, not proof): Python transcription of the C++ bound vs Lean `#eval` (0/32 mismatches), bound ≤ brute-force minimum over all completions for 32 deep prefixes of the real instance (≤1024 completions each), and 14112 prefix×completion checks on random small instances (0 violations).

## Scope and limits (read before relying on IV-3)
1. **Exact-arithmetic theorem.** It concerns the real-number bound over the exact dyadic encoding of the 780 couplings. Binary64 rounding of the C++ bound and the outward guard `1e-11·max(1,Σ|K|)` are NOT formalised; the guard only enters as an arbitrary `g ≥ 0`. The floating-point safety of the pruning remains the SCR-III audit's (non-Lean) claim.
2. **Discard rules, not the whole search.** IV-3 does not prove that the DFS terminates with the true minimum, handles the incumbent correctly, or visits all surviving nodes. That is IV-4.
3. **Minimum value, not minimiser set** (ties; see above).
4. **All IV-1 limits stand** (exact encoded model, no interval enclosure of the physical couplings, grammar convention evidenced not proved against the geometric rule).
5. **No claim** about the values of the ground, grammar or non-grammar optima, about δ₄, or about the finite gap beyond the two witness-level facts of IV-2.

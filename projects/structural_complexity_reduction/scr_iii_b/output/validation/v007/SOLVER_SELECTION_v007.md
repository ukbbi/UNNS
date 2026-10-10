# SOLVER_SELECTION_v007 — DRAFT decision memo (not frozen)

Purpose: choose the **unchanged downstream solver and search task** for SCR-III-B before the preregistration is frozen. Nothing here is a result; numbers are v007 component costs (single thread, Linux-6.18.40.1-microsoft-standard-WSL2-x86_64-with-glibc2.43).

## Measured facts that constrain the choice (3×3, N=24)
- Exhaustive evaluation of all 16777216 states: direct 5.442 s, Gray-code incremental 0.145 s (8.645 ns/state).
- Grammar check over the nominal space: 0.08065 s (4.807 ns/state). Constructive generation: 25786 nodes, 0.0001294 s.
- Peak memory of the storing verifier: 131 MB.
- 4×4 (N=40) exact enumeration: lower-bound estimate ≈ 4.4 single-thread hours (not measured; streaming verifier required).

## Candidate tasks
| ID | Task | Exact? | Target set certified? | Main risk |
|---|---|---|---|---|
| S-A | Exhaustive threshold scan: Gray-code enumeration of 2^N states, report all s with H ≤ E0+W | yes | yes (it *is* the exact verifier) | Weak baseline: B0 is already seconds at 3×3; G_net is bounded by per-state cost ratios for G1 |
| S-B | Exact branch-and-bound over spins with an admissible energy lower bound, same output as S-A | yes | yes | Needs a bound design (Hamiltonian-aware but legitimate for a *baseline*); this is the baseline a reviewer will expect |
| S-C | Stochastic low-energy search (Metropolis/annealing) until a stopping rule | no | no | Cannot certify S_T; noisy time-to-solution; weak for exact-preservation claims |

## Recommendation (for your decision)
- Primary task **S-A at 3×3**: exact, deterministic, reproducible, target set certifiable, already implemented as the verifier core.
- Before any `VALID_STRUCTURAL_REDUCTION` claim, require **S-B as a stronger-baseline sensitivity arm**, because G_net against S-A alone can be an artefact of a weak baseline.
- Defer S-C; it cannot support an exact-preservation claim.

## How each architecture plugs in
- B0: solver over all 2^N states. G1: same solver restricted to states passing the grammar (charge the grammar check on every state tested). G2: generate states from incidence constraints (charge nodes, rejections, materialization), then apply the same energy test. N1/N2: replace incidence only. C1: threshold from full H (bound only). E2: see below.
- Charged units to fix in the preregistration: pair-multiplications per energy call (276), vertex checks per grammar call, search nodes, state materializations, wall-clock, peak memory. Count each cost once.

## Window-rule options (choose BEFORE any 3×3 window outcome is read; v007 withholds that outcome)
1. W = c·A(T_ref) (units of the coupling energy scale), c fixed in advance.
2. W = c·k_B·T_ref, c fixed in advance (physically interpretable thermal window).
3. W defined by target cardinality m (e.g., the m lowest configurations): independent of energy units, but the level degeneracy must be respected.
Any rule that references the ice-rule, Δ_nonice or the grammar would re-introduce the tautology and is not admissible.

## E2 comparator options (to be fully specified, then implemented)
- Truncated-interaction energy estimate with cutoff r_c plus a rigorous tail bound (can be exact); or the same without a bound (not exact, must be reported as such).
- Whatever is chosen must charge preprocessing, energy calls and decisions, and run on the same candidate universe and stopping rule.

## Still open
- Unchanged downstream solver and search task (candidates in SOLVER_SELECTION_v007.md).
- Stopping rule, configuration order and instrumentation of that solver.
- Energy-window rule (functional form and constant), frozen BEFORE any 3x3 window outcome is read.
- Charged E2 comparator design (including whether it can be exact).
- Seed registry, repeat count, null sample sizes, minimum G_net margin and uncertainty criterion.
- Runtime and memory limits.
- Transfer-confirmation criteria beyond guaranteed alignment.

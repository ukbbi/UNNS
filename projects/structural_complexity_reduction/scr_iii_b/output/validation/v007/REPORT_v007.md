# REPORT_v007 — 3×3 Exact-Verification Feasibility and Solver-Selection Gate

**Verdict:** `EXACT3_VERIFIER_FEASIBLE`

Feasibility gate only: no primary experiment, no G_net, no preregistration freeze, no transfer claim. Frozen v005/v006 check (F1): PASS.

## What was verified

- Exact 3×3 scan of all 16777216 states with both a direct and a Gray-code incremental evaluator; deterministic across 3 repeats (V4).
- The C++ verifier reproduces the frozen python at every 1×1 and 2×2 energy-level threshold (|S_T|, false exclusions, E0, |S_G|) and on 2,002 seeded 3×3 states (V1, V2).
- Brute-force 3×3 grammar count over all 2^24 states = python constructive = C++ constructive (V3).
- 3×3 anchor (W=0, no free parameter): E0 = -9.272e-20 J, ground states = 2, false exclusions = 0. Guaranteed-alignment anchor only; **no W>0 window outcome and no 3×3 level spectrum are disclosed**, so window rules can still be frozen blind.

## Component costs (single thread; not a speedup)

| Component | 3×3 | per state |
|---|---|---|
| direct energy pass (276 pair terms) | 5.442 s | 324.4 ns |
| Gray-code incremental energy | 0.145 s | 8.645 ns |
| grammar scan of the nominal space | 0.08065 s | 4.807 ns |
| constructive grammar generation | 0.0001294 s, 25786 nodes | – |
| direct energy on the 2,604 grammar survivors | 0.002044 s | – |

Peak RSS 131 MB (stores 2^24 doubles). Environment: Linux-6.18.40.1-microsoft-standard-WSL2-x86_64-with-glibc2.43.

**4×4 (40 spins, 2^40 states) exact verification is not measured.** Lower-bound estimate from the 3×3 Gray rate: ≈ 4.4 single-thread hours; it would need a streaming verifier.

## Consequences for the preregistration

1. 3×3 exact preservation **can** be verified: the full nominal space is enumerable in seconds, so an exact-preservation claim is available at 3×3.
2. The same fact weakens 3×3 as a *speed* benchmark: an optimized exhaustive baseline finishes in about 0.15 s, so absolute savings are tiny and any G_net depends strongly on how strong the baseline is.
3. Scanning the nominal space with the grammar (G1) costs one grammar check per state, so G1 cannot beat the baseline by more than the per-state cost ratio; the large node-count reduction belongs to constructive generation (G2).
4. A stronger conventional baseline (energy-bound pruning) is needed before any `VALID_STRUCTURAL_REDUCTION` claim; see `SOLVER_SELECTION_v007.md`.

## Tests

| ID | Test | Status |
|---|---|---|
| F1 | Frozen v005 and v006 code/outputs equal the hashes in their local manifests (read-only comparison) | **PASS** |
| V1 | C++ exact verifier reproduces python (v006) |S_T| and false-exclusion counts at EVERY energy-level threshold of 1x1 and 2x2, plus E0 and |S_G|; Gray-code incremental energy equals direct energy | **PASS** |
| V2 | Per-state energy: C++ equals frozen v005 python on all 4,096 2x2 states and on 2,002 seeded 3x3 states (incl. all-down and all-up) | **PASS** |
| V3 | 3x3 grammar set: brute-force scan of all 16,777,216 states equals python constructive set (v006) and C++ constructive generation (count, id sum, id xor) | **PASS** |
| V4 | 3x3 exact scan is complete (2^24 states evaluated by both direct and Gray-code passes), deterministic across 3 repeats, and the accumulated Gray-code drift stays >=10x below the 1e-9 degeneracy tolerance (<=1e-10 of the energy scale) | **PASS** |
| V5 | 3x3 W=0 anchor recorded (no free parameter); no W>0 window outcome and no level spectrum disclosed | **PASS** |
| K1 | Component costs measured separately (direct energy, grammar scan, incremental energy, constructive generation, memory) and 4x4 exact-verification cost extrapolated as an explicit estimate | **PASS** |

## Decisions still required from the project owner

- Unchanged downstream solver and search task (candidates in SOLVER_SELECTION_v007.md).
- Stopping rule, configuration order and instrumentation of that solver.
- Energy-window rule (functional form and constant), frozen BEFORE any 3x3 window outcome is read.
- Charged E2 comparator design (including whether it can be exact).
- Seed registry, repeat count, null sample sizes, minimum G_net margin and uncertainty criterion.
- Runtime and memory limits.
- Transfer-confirmation criteria beyond guaranteed alignment.

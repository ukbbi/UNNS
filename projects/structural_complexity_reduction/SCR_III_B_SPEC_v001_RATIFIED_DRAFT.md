# SCR_III_B_SPEC_v001 (v009 closure draft) — Generative Admissibility Primary Experiment

**Project:** UNNS Structural Complexity Reduction (SCR)  
**Branch:** SCR-III-B — Generative Admissibility / Physical Sufficiency (does not claim transfer)  
**Status:** REVISED DRAFT + v008 WORDING AMENDMENTS + v009 CLOSURE PROPOSALS — **UNFROZEN**  
**Date:** 2026-10-10  
**Primary execution:** NOT AUTHORIZED  
**Frozen dependencies:** SCR-III-A `COUPLING_MAP_ONLY`; v005 `PHYSICAL_HAMILTONIAN_LOCK_PASS`; v006 `FEASIBILITY_PASS`; v007 `EXACT3_VERIFIER_FEASIBLE`.

## 1. Scientific mission and epistemic discipline

**Primary research question:** Can an independently specified *generative grammar* construct a sharply smaller candidate space, and can that space retain the full set of independently defined physically relevant configurations?

The key object is **not** an optimized solver. The project asks whether a conventional nominal state representation overstates the space required to describe and investigate physically relevant structure.

Four independent evidence axes (with distinct endpoints):

- **G — Generative contraction:** a frozen target-blind grammar directly generates fewer configurations than the nominal state space, reproducibly and without first enumerating the nominal space.
- **P — Physical-target preservation / admissibility:** a separately defined physical Hamiltonian and target rule establish whether all relevant configurations lie inside the grammar-generated set.
- **T — Transfer to an independently defined physical target family:** requires a separate operational protocol and cannot be established by the fixed inclusive energy-window construction.
- **C — Computational consequence:** the resulting candidate restriction reduces actual resource consumption for a fixed downstream physical task, with all costs charged.

A G PASS does not imply P or T; a G+P PASS does not imply T or C. C failure does not erase G or P. An energy-window target below the first non-ice excitation may deliver *guaranteed alignment* but does **not** by itself establish independent non-tautological physical transfer.

Do **not** equate violation of the 2-in/2-out rule with physical impossibility: spin configurations outside the grammar exist in the physical baseline and may be physically relevant at higher energies. `S_G` is a grammatical set; it is not automatically the full physical state space.

## 2. Frozen sources and negative controls

- Use **unchanged** Dryad SPMMC v1.00 finite free-boundary Hamiltonian and physical parameters locked by v005.
- v006 established 1×1 (6 of 16) and 2×2 (82 of 4096) structural counts and a limited, gap-aligned 2×2 energy-window preservation case. These are reference and implementation controls, not fresh primary discoveries.
- v007 established feasible exhaustive exact verification for 3×3 (24 spins, 2^24 nominal states) and 2,604 constructively generated grammar states, with W=0 as a guaranteed-alignment anchor. It **withheld every W>0 target outcome and the excited spectrum**.
- Freeze documents v005–v007 and their files remain historical and untouched. Do not reselect parameters in response to primary results. GitHub remains untouched.

## 3. Objects and set relations

`S_0 = {-1,+1}^N`, with all spin states physically retained in the nominal baseline.

`G(s)=1` iff all specified constrained vertices obey the independently specified 2-in/2-out rule; `S_G={s in S_0:G(s)=1}`.

`H(s)` is the v005 physically locked Hamiltonian; `E_0=min_(s in S_0) H(s)`.

For a **prospectively frozen** window `W>=0`, `S_T(W)={s in S_0:H(s)<=E_0+W}`.

`S_T^G(W)=S_T(W) ∩ S_G`. Preservation requires **set equality** `S_T^G(W)=S_T(W)` (false exclusions = 0). Exact preservation must be independently certified using direct physical energies, not inferred from sampled agreement or a grammar-limited search.

Define `R_G=1-|S_G|/|S_0|`, `R_explored=1-N_explored^G/N_explored^B`, and `G_net=C_baseline/(C_generation+C_filter+C_downstream)` for a specified equal task. Do not use these interchangeable terms.

If proposing `S_generative ⊇ S_admissible ⊇ S_persistent`, operationally define and independently test every extra inclusion; v007 only verifies the frozen *ice-rule* grammar and does not validate a universal UNNS hierarchy.

### Gap-preservation theorem (methodological constraint)

For any finite nominal state space, fixed grammar `S_G`, and inclusive target `S_T(W)={s:H(s)<=E0+W}`, set `Δ_nonG=min_{s∉S_G}(H(s)-E0)` (with `+∞` if the complement is empty). For `W>=0`, provided there is an excluded configuration, **exactly**:

`S_T(W) ⊆ S_G  ⇔  W < Δ_nonG`.

The strict inequality is essential: at `W=Δ_nonG`, the minimum-energy excluded configuration enters the target. If `Δ_nonG=0`, no nonnegative window preserves every target. If `S_G=S_0`, preservation is automatic and not independently informative. This follows from the definitions, not an empirical generalization. Accordingly, a fixed ice-rule grammar **cannot** both preserve an inclusive full energy-window target and exhibit preservation unaccounted for by this gap. The former H-T requirement to do both is **RETIRED AS LOGICALLY UNSATISFIABLE**.

H-P remains a real prospective test of whether the preselected `W` lies below this independently measured boundary, not a test of a gap-free physical transfer mechanism. Target sets are not to be selected after comparing `W` to `Δ_nonG`.

## 4. Primary scale and exact certification

**Candidate primary physical scale:** 3×3 free-boundary square ice, N=24, nominal count 16,777,216; frozen grammar-generated count 2,604.

First, freeze an outcome-blind physical target-window rule, numerical energy grouping and threshold tie treatment, source hashes, and all test code. Then unblind the full physical spectrum and compute *exact* target membership for every nominal state.

Required exact certificates: energy threshold, all target IDs (or a complete cryptographically verifiable set representation), number of targets, number and IDs of false exclusions, level/tie policy, and exact grammar membership of each target.

1×1 and 2×2 are regression controls only. A 4×4 experiment is optional future work: v007 provided a timing extrapolation, **not** an exact 4×4 feasibility or preservation proof.

## 5. Architecture: grammar first, solver second

**G0 — Grammar construction:** deterministic constructive 2-in/2-out generator without energy queries. Charge preprocessing, enumeration nodes, materialization, deduplication, and grammar evaluation. Validate IDs against independent brute-force membership wherever feasible.

**B0 — Conventional exact baseline (primary C reference; H-C is stated as performance against this optimized exhaustive Gray-code baseline, B1 being sensitivity only):** enumerate all nominal states, evaluate the same Hamiltonian, return the **complete target set**. A single-thread optimized Gray-code baseline is compulsory because v007 measured it much faster than naive direct evaluation. The direct evaluator remains an independent correctness reference, not the sole performance baseline.

**G1 — Grammar-scan filter:** test nominal states for grammar membership before applying the *same target energy test*. Charge all checks and enumeration; G1 cannot claim a 2^N enumeration reduction.

**G2 — Constructive grammar:** generate `S_G` directly and apply the same downstream target-energy test. Implement fair incremental pair-energy updates along constructive search branches (or document a certified equivalently optimized alternative); do not handicap G2 with only slow direct re-evaluation while B0 uses incremental Gray-code energies. Charge partial-assignment updates, generator visits, setup and final evaluations. G2 reports `S_T∩S_G`; it cannot itself certify this equals `S_T`. Completeness is an *offline independent full-space audit* and is a prerequisite for any complete-task G2 gain claim. Distinguish deployment-time recurring certification costs from once-only research audit costs.

**B1 — Strong Hamiltonian-aware baseline:** implement exact branch-and-bound with a mathematically admissible lower bound and the **same complete-target-set stopping rule** as B0. Prove bound admissibility independently. Treat as a required **sensitivity comparator**, not a co-primary minimum speedup threshold; the highly optimized B0 remains the mandatory primary competitive baseline.

**E2 — Charged energy-informed comparator:** implement a prospectively chosen localized/truncated-interaction method, ideally with certified remainder bound; otherwise label it non-exact and disallow comparisons requiring full-set completeness. Charge preprocessing, bound computation, rejections, energy queries and all missed targets.

**C1 — Target-aware oracle:** report as an ideal bound only; do not treat it as target-blind evidence.

**N1/N2 — Structural nulls:** degree-preserving and unconstrained incidence rewiring where valid, holding `S_0`, `H`, selected `W`, target set and downstream task fixed. Freeze seed list, feasibility and rejection policies *before* outcomes. Include unchanged-incidence and intentionally perturbed controls. Nulls can change survivor counts; report capacity and contraction alongside preservation and ensure fair matched-size analysis where possible.

## 6. Primary regimes and transfer-scope repair

**Energy-window experiment (G/P/C):** classify each prospectively selected 3×3 window as `PRESERVED_BELOW_GAP` or `PRESERVATION_FAIL_AT_OR_ABOVE_GAP` (or `INCONCLUSIVE` for incomplete evidence). This classification is exhaustive under the theorem in §3; a non-ground window does not escape it. The expected-failure defect-inclusive control remains separate. Nulls assess whether actual vertex incidence is a distinctive grammatical restriction; they do not nullify the logical gap identity.

**H-T is a distinct, deferred experiment, not an additional criterion on this energy-window task.** A possible future protocol would freeze a *dynamical persistence target* (e.g., recurrence/occupation under a fully specified independent state-transition law and time scale), derive its target set independently of the grammar and energy-window cutoff, and ask if `S_G` predicts its membership, preservation, and null separation on held-out initial conditions. Full exact preservation may fail and must be honestly reported. Any external Hamiltonian or observable substituted into the same inclusive full energy-window definition obeys its own analogous gap theorem; merely switching Hamiltonians is NOT a non-gap transfer test. Other external target families are admissible only with an equally explicit, independently falsifiable protocol.

Before any T test, separately preregister target construction, dynamics, observation time, patch/population, complete versus sampled coverage, and whether success demands FN=0 or permits a specified statistical recall criterion. The current v008 gate is **not** authorized to create or unblind a T target. For the present 3×3 study, record `T=NOT_TESTED / PROTOCOL_UNFROZEN` and never `TRANSFER_CONFIRMED`.

## 7. Measurements and reporting

For each patch, window, architecture and null:

- `|S_0|`, `|S_G|`, `|S_T|`, `|S_T∩S_G|`, false exclusions, target capacity `|S_G|/|S_T|`;
- constructive search nodes, materialized candidates, unique candidates, grammar checks, Hamiltonian evaluations, pair operations;
- solver output equivalence and full target-ID set equality;
- time (warm and cold where applicable), environment/compiler/flags/threads, number of repetitions and uncertainty, peak RSS;
- full charged preprocessing, grammar/generator and downstream costs; relative performance against optimized B0 and exact B1;
- null target preservation and contraction distributions with their sample sizes.

Record the physical classification **separately** from search performance and from whether a comparator can enumerate all targets.

## 8. Pre-primary gate and reproducibility

The preregistration must freeze, **before reading any 3×3 W>0 result**:

1. Primary window functional form and numerical constants, including an independently chosen physically motivated window and a separately labeled guaranteed-alignment anchor.
2. Exact-task solver, state order, complete-set stopping rule, lower-bound proof for B1, and E2 implementation.
3. Primary hypothesis-specific thresholds for G/P/C, and a distinct, separately designed future T protocol (no T success criterion within current W-window study).
4. Seed registry, null counts and null acceptance criteria, repetitions, compiler settings and timing treatment.
5. Runtime/memory limits, correction/amendment procedures and SHA-256 input/source hashes.
6. Record v007 blindness leakage: `V4.relative_to_scale` and drift permit inference of an approximate upper-spectrum scale (~0.126 in A units), although low-energy levels and W>0 outcomes were not disclosed. Describe the study as **low-energy-outcome blinded**, not fully spectrum-blinded. The so-called independent verifier is separately implemented and cross-validated but **shares authorship** with the grammar code; no external independent replication has occurred.
7. Numerical drift tolerance and grouping policy **prospectively**; v007 V4 had a disclosed post-hoc revision from 1e−12 to 1e−10 and must not be silently reused as though preregistered.

Run a limited **acceptance-only** operational dry run with no disclosure of target membership beyond the already published W=0 anchor, if necessary. Freeze preregistration independently before launching the primary experiment.

Outputs: reproducible source, `SPEC`, preregistration and their freeze record, run manifest, machine-readable target certificates and results, human-readable synthesis, no overwritten prior artifacts.

## 9. Independent verdict axes

- **G:** `GENERATIVE_CONTRACTION_PASS/FAIL/INCONCLUSIVE`
- **P:** `TARGET_PRESERVATION_PASS/FAIL/INCONCLUSIVE`
- **T:** `NOT_TESTED / PROTOCOL_UNFROZEN` for this experiment; separate future transfer study required
- **C:** `CHARGED_GAIN_PASS/FAIL/INCONCLUSIVE`

Computational result C is conditional on independently certified P for the same physical task; if P fails, a fast incomplete G2 output is not a valid complete-task speedup. B1 remains a sensitivity arm.

Legacy phrases such as `VALID_STRUCTURAL_REDUCTION` and `TRANSFER_CONFIRMED` may be emitted **only if separately frozen cross-axis definitions are satisfied**; do not allow a favorable speed ratio to override physical target exclusion.

## 9A. v008 amendments (diagnostic, window disclosure, tie policy)

**Gap diagnostic.** For the real grammar and every valid structural null report `Δ_G = Δ_nonG = min_{s∉S_G}[H(s)−E0]` and, where `Δ_G>0`, `ρ_G = W/Δ_G`. `ρ_G<1` passes; `ρ_G≥1` fails. `Δ_G=0` (ground level excluded: no nonnegative window preserves) and an empty excluded set (`S_G=S_0`: not informative) are reported as separate classes. These quantities are computed on 3×3 and on nulls only AFTER freeze and primary unblinding; the v008 dry run computed them on the public 1×1 and 2×2 patches only.

**Thermal-window disclosure.** The candidate window `W=k_BT` (T_ref=792 K, k_BT=1.0935e-20 J) lies ABOVE the known gaps: 1×1 `Δ=9.529e-21 J=0.871 k_BT` (ρ_G≈1.15), 2×2 `Δ=1.041e-20 J=0.952 k_BT` (ρ_G≈1.05). Failure of 3×3 preservation at this window is a genuine possibility, to be reported as P FAIL; the window must not be changed to avoid it. The window constant remains OPEN and must not be chosen from v008 performance.

**Tie policy (proposed, tested on synthetic cases only, NOT frozen).** Membership `E ≤ E0+W+τ` with `τ = 1e-9·Σ|K_ij|`; `PRESERVED ⇔ W+τ < Δ`. Tolerance may only enlarge the target and must never convert an excluded target into a preserved one. The final rule and constant must be frozen before the real 3×3 thresholds are inspected.

**Blindness.** v008 inspected 3×3 only at the published W=0 anchor; the guard in the solver binary refuses n>16, W>0 without an explicit post-freeze flag.

## 9B. v009 closure proposals (PROPOSED — AWAITING RATIFICATION; this specification stays UNFROZEN)

**E2 — exact Hamiltonian-aware comparator.** With `H = H_R + H_O`, retained set R = strongest 25% of `|K_ij|` (ties: smaller pair index first), `B_O = Σ_O |K_ij|`: `H_R − B_O ≤ H ≤ H_R + B_O`. A state is rejected only if `H_R − B_O − ε > Ecut`, accepted without full evaluation only if `H_R + B_O + ε ≤ Ecut`; every other state falls back to the exact evaluation. E2 never queries grammar membership, uses the same E0, may be slower than B0, and is a sensitivity comparator.

**Common E0.** One frozen, hash-checked global ground energy (the v007 anchor) is given to every solver; a grammar-restricted estimate never replaces it.

**Numerical policy.** `τ = 1e-9·Σ|K|`; membership `E ≤ E0 + W + τ`; PRESERVED ⇔ `W + τ < Δ_nonG` (equality fails); UNRESOLVED_BOUNDARY is conservatively counted as target; evaluation error, membership tolerance and level grouping are distinct.

**Windows.** Primary `W = k_B T_ref` (792 K); sensitivity 0.5 and 2 k_BT. The public gaps exceed the primary window (1×1: 0.871 k_BT; 2×2: 0.952 k_BT), so 3×3 preservation may fail.

**Nulls, ordering, symmetry, costs.** Seed 20261010, 1,000 nulls per family (N1, N2), target-blind. Deterministic candidate orders per solver; Z₂ symmetry disabled in the primary experiment. Cost ledger setup/generation/filter/energy/other with E0 certification separate; 1 thread, 3 warm-ups, 15 rounds, median, 30 min and 2 GiB limits.

**Axis criteria.** G: exact membership and ≥ 99% contraction. P: FN = 0. T: NOT_TESTED. C: ≥ 1.20× against B0, only if P passed and completeness is certified (paired bootstrap lower bound).

**Blinding.** Real-3×3 W>0 and excitation-gap requests are refused by the guard and recorded in the audit; unblinding requires a separate freeze and authorization.

## 10. Document status

**LOGIC-REPAIRED REVISION — UNFROZEN.** It authorizes no primary run, no outcome unblinding and no changes to frozen code. The accompanying preregistration is also **UNFROZEN**, with open choices expressly marked. Its freeze must precede primary execution.


---

## Ratified design addendum (2026-10-10; primary document still UNFROZEN)

The companion `RATIFY_v001.md` is the authoritative prospective decision register for the current draft. It ratifies all eighteen v009 design decisions. In case of conflict, its specific values supersede earlier PROPOSED settings in this draft, including E2 interaction retention **75%** (not 25%) and the H-C decision rule below.

**H-C operational decision rule:** P must PASS and complete target-set equality must be certified; then for 15 predeclared charged paired B0/G2 timings require `median(B0_i/G2_i) >= 1.20` **and** `min(B0_i/G2_i) >= 1.20`. This replaces the under-covered nominal '95% bootstrap lower bound'. It is a stringent *finite-sample operational acceptance criterion*, not a calibrated 95% confidence statement. B1/E2 are mandatory sensitivity reports, not H-C denominators. Incomplete or timed-out pairs cannot be discarded; see `RATIFY_v001.md` for `INCONCLUSIVE` rules.

**Nulls:** 1,000 valid N1 and 1,000 valid N2, 5,000 draw cap per family, master seed 20261010. Report null survivor distributions and exclusion gaps descriptively; no confirmatory null-separation p-value or success criterion is claimed without a separately registered calibration. **Primary window:** `W=k_B*(792 K)`; sensitivity windows `0.5W` and `2W`, no post-outcome switching. **Numerical policy:** `tau=1e-9*sum(abs(K_ij))`, conservative inclusion and explicit borderline flags; operational versus unexpanded mathematical targets must be distinguished. **Global reversal:** disabled for the primary comparison.

These decisions are RATIFIED AS DESIGN, but these revised documents are **NOT FROZEN**. No 3×3 W>0 primary run is authorized. The final source/hash-lock and independent freeze record must precede explicit unblinding authorization.

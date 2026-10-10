# SCR_III_B_SPEC_v001 — Primary Experiment Specification

**Project:** UNNS Structural Complexity Reduction  
**Branch:** SCR-III-B — Generative Admissibility / Physical Sufficiency  
**Document status:** FROZEN PROTOCOL CONTENT (scientific specification) — execution NOT AUTHORIZED  
**Ratification:** 2026-10-10; companion `SCR_III_B_PREREG_v001.md` and `PRIMARY_FREEZE_v001.md`  
**Historical references:** FREEZE_v005–v009; RATIFY_v001.md.

## 1. Objective and inference boundaries

Ask whether a **target-blind 2-in/2-out generative grammar** can construct a dramatically smaller structural sector and preserve every configuration of an independently defined physical task. Keep four separate conclusions: G=generative contraction, P=physical sufficiency/preservation, T=independent physical transfer, and C=charged computational consequence.

**T is NOT_TESTED** in this experiment. The fixed energy-window target and ice-rule grammar obey a gap equivalence; successful preservation at a window protected by that gap does not establish transfer. G may pass even if P fails; C as complete-task acceleration is eligible only when P passes.

## 2. Frozen model and mathematical theorem

Use the frozen Dryad **SPMMC v1.00** pairwise finite free-boundary model and parameters (v005). Physical patch is **3×3**, 24 spins, nominal set `S0={-1,+1}^24`, `|S0|=16,777,216`. Frozen target-blind grammar `G` enforces 2-in/2-out at each constrained vertex; `SG={s:G(s)=1}`, previously counted as **2,604** (v007 reference; replication, not novel result).

Hamiltonian and global physical ground energy are fixed by v005/v007. Every algorithm must use the common reference `E0`; an independently derived grammar-restricted `E0_hat` is **not** a permissible substitute. The known anchor is `E0≈-9.271994751803727e-20 J` at 792 K, with full precision read from the frozen canonical source, not typed from this rounded document.

For a width `W>=0`, mathematical target `ST(W)={s:H(s)<=E0+W}`. Let `Δ_nonG=min_{s not in SG}(H(s)-E0)`, or `+infinity` if `SG=S0`. For a nonempty excluded set the exact set theorem is `ST(W) subset SG iff W < Δ_nonG`. At `W=Δ_nonG` the inclusive endpoint **fails** preservation. When `Δ_nonG=0`, every nonnegative window fails.

The operational membership target is **separately defined** as `ST_tau(W)={s:H(s)<=E0+W+tau}`, `tau=1e-9*sum_{i<j}|K_ij|`, using the same physical energy units. Its gap equivalence is `W+tau < Δ_nonG`. Always report the mathematical and operational targets distinctly where certification allows. Numerical uncertainty must never be used to silently remove an eligible target.

## 3. Prospectively fixed target windows and prior information

Reference temperature **792 K**; exact SI `k_B=1.380649e-23 J/K`. **Primary W=k_B T=1.093474008e-20 J**. Sensitivity windows are `0.5W` and `2W`; neither rescues a primary failure. The public 1×1 and 2×2 gaps are respectively about `0.871 k_B T` and `0.952 k_B T`, so their W=k_B T targets **fail** preservation. The 3×3 excited spectrum, its Δ_nonG and all W>0 outcomes were withheld as of this protocol. Window selection acknowledges prior small-patch results and cannot be modified after unblinding.

The W=0 3×3 anchor is a known guaranteed-alignment implementation control only. All actual 3×3 W>0 analyses are **primary**, prohibited until a separate explicit execution authorization.

## 4. Solver arms, identical task, and correctness

All complete-task solvers must output the exact configuration-ID set in the **operational** physical target at the same W, with identical parameter/reference and same threshold rule. Independent direct physical-energy certification scans the complete nominal space; it is an offline scientific audit, not a grammar solver.

- **B0:** optimized single-thread full-space Gray-code exhaustive scan with recorded resynchronization and completeness; mandatory performance denominator.
- **B1:** exact Hamiltonian-aware branch-and-bound with a certified admissible lower bound; required sensitivity comparator, not an H-C acceptance denominator.
- **G1:** nominal-space grammar scan then physical evaluation; all scanned-state and grammar costs charged; outputs `ST_tau∩SG`.
- **G2:** target-blind constructive grammar generator with **incremental pair-energy updates** along its assignment tree, charging construction, node visits, initialization, and downstream evaluation; outputs `ST_tau∩SG`. Must use competitive update algebra, not deliberately slower direct energy calls.
- **E2:** energy-aware, non-grammar exact comparator; retain the **strongest 75% of pair interactions by |K|** (ties by frozen pair index), compute omitted remainder bound `B=sum_omitted|K|`, safely accept/reject with `H_R±B` relative to the operational threshold, and perform full exact evaluation of ambiguous candidates. Charge preprocessing, bounds, fallbacks, all energy and memory costs.
- **C1:** target-aware theoretical oracle, if reported, is a bound only and not a competitive empirical baseline.
- **N1/N2 nulls:** incidence-only degree-preserving and free-incidence rewiring; keep physical patch, Hamiltonian, window and target unchanged; 1,000 *valid* nulls per family with a cap of 5,000 draws per family. Record acceptance/rejection and shortfalls; no target-informed null selection. Null findings are descriptive; **no confirmatory null significance claim**.

The bit convention, C++/Python mapping, grammar incidence and target-ID representation are inherited from frozen v005–v009. Per-solver iteration/branch ordering and any technical flags must be those implemented, tested and recorded in v009; log actual compiler options and artifact hashes. If a required ordering or option is missing from the installed v009 implementation, block primary execution rather than make a silent choice.

## 5. Numerical certificate and error handling

Use separate physical energy-evaluation error, incremental drift bound, reporting-level grouping tolerance, and operational membership expansion `tau`. Synthetic boundary tests from v009 must continue to pass. Higher-precision re-evaluation is required for near-threshold states; mark `UNRESOLVED_BOUNDARY` where neither direction is certifiable and conservatively include such states in target counting. Any unresolved membership or completeness issue prevents an **unqualified exact P PASS**.

Maintain inclusive equality at `E0+W+tau`; equality with `Δ_nonG` is a preservation failure. Gap, `W/Δ_nonG`, first excluded IDs, near-boundary flags, and null-gap distributions are **post-unblinding outputs**, never prefreeze inputs.

v007's incremental-drift tolerance was changed post hoc (1e-12 to 1e-10); it is historical. The primary use of direct/high-precision energies as target authority and numerical parameters above are prospectively ratified; retain the v007 disclosure.

## 6. Cost measurement and symmetry

Single thread; **3 warmups**, **15 paired timed rounds**, balanced deterministic interleaving. Master null seed **20261010** with the v009 domain-separated deterministic derivation; store seed registry and hash. Budget **30 minutes per algorithm arm**, **2 GiB peak resident memory**. Global reversal `Z2` quotient is **disabled for all primary arms**; optional separately labeled equal-opportunity sensitivity only.

Charged end-to-end cost must include setup, grammar generation/filtering, candidate handling, energy and bound operations, relevant preprocessing and downstream work **exactly once**. Report reference E0 certification and offline whole-space audit cost separately, plus an explicit deployment accounting scenario if certification would actually be required operationally. Do not hide costs that are necessary to deploy a correct exact-set solver. Record wall/CPU time, peak RSS, nodes, generated states, full/incremental energy calls, pair operations, retries/failures, serialization and per-round timings. Fixed complete-target outputs must be checked for identity.

For C the ratified finite-sample operational rule is: **P PASS required** and all 15 valid paired B0/G2 charges available; for every round `r_i=cost(B0)_i/cost(G2)_i`, require `median(r_i)>=1.20` **and** `min(r_i)>=1.20`. B1 and E2 are sensitivity only. This is **not** a 95% confidence interval or a guarantee of out-of-sample speedup. Incomplete/timed-out rounds are disclosed and classified by the preregistered rules, never silently dropped.

## 7. Outputs, safeguards and verdict structure

Outputs must include full target-ID certificates/checksums, per-window FN and gap diagnostics, grammar/null survivor counts, all cost ledgers and 15 paired timing records, near-threshold audit, frozen-source fingerprints, compiler/runtime environment and invocation audit. Preserve G/P/T/C as **independent result fields**. Report failure results faithfully; cannot promote conditional G2 speed to unconditional full-task C if P fails.

Frozen v005–v009 files and freeze records are reference-only; no overwrites, no changes to GitHub. All primary execution paths must remain guarded until a separate signed/recorded authorization. The attached freeze record confirms **document immutability by hashes**, not that any primary computation was performed.

**Protocol scientific status:** content frozen; **PRIMARY_NOT_AUTHORIZED**.

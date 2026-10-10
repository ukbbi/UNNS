# SCR_III_B_PREREG_v001 — Primary Preregistration

**Project:** UNNS Structural Complexity Reduction, SCR-III-B — Generative Admissibility / Physical Sufficiency  
**Status:** FROZEN PROTOCOL CONTENT — **PRIMARY EXECUTION NOT AUTHORIZED**  
**Ratification date:** 2026-10-10  
**Companion:** `SCR_III_B_SPEC_v001.md`; `PRIMARY_FREEZE_v001.md`; `RATIFY_v001.md`.

## 1. Prospectively declared task

A 3×3 free-boundary, 24-spin Dryad SPMMC v1.00 instance with frozen v005 Hamiltonian and v007 independently certified global physical ground energy E0. Frozen target-blind ice-rule grammar, previously **2,604/16,777,216** surviving configurations (historical replication).

**Primary target:** all spin IDs satisfying the operational inclusive window `H(s)<=E0+W+tau`, where **W=k_B*792 K=1.093474008e-20 J**, `k_B=1.380649e-23 J/K`, `tau=1e-9*sum|K_ij|` from physical frozen pairs. Sensitivities: `0.5W` and `2W`, reported irrespective of primary outcome. Mathematical unexpanded target `H<=E0+W` must be distinguished from operational target. All solvers use the same E0 and target definition. Neither sensitivity can substitute for primary failure.

Previous public gaps: 1×1 `Δ_nonG/(k_BT)≈0.871`, 2×2 `≈0.952`, both preservation failures for W=kBT. These were known when choosing W. **The 3×3 W>0 outcomes and low-energy Δ_nonG are not to be examined until separate authorization.** Past v007 V4 diagnostics disclose approximate upper spectral scale; blindness is *low-energy outcome* blindness only.

## 2. Hypotheses and independent decision rules

**H-G — constructive generative contraction (primary structural axis).** PASS iff grammar generated membership exactly equals independently enumerated grammar membership, no physical energy/target labels are used in construction, and at least **99%** of nominal configurations are not materialized as candidates. Record visited nodes and full work independently. Known preflight 2,604 count is replication, not new discovery. Mismatch/energy leakage fails; missing evidence is inconclusive.

**H-P — physical target preservation (co-primary sufficiency axis).** PASS iff every independently certified operational target ID is contained in SG (`FN=0`), with complete nominal-space verification and no unresolved threshold or identity errors. One excluded target yields FAIL. Report after unblinding `Δ_nonG = min_{s not in SG}(H(s)-E0)` (infinity if empty), `W/Δ_nonG` when defined, `W+tau` and the exact inclusive-boundary logic. For a nonempty excluded set, preservation iff `W+tau < Δ_nonG`. Numerical ambiguity that prevents exact classification makes P INCONCLUSIVE, not automatic PASS.

**H-T — independent physical transfer.** `NOT_TESTED / PROTOCOL_UNFROZEN`. A future independent target-family experiment requires separate formal hypothesis, holdout and falsification. Ice-rule/energy-window gap alignment cannot establish T, and T success is impossible under the retired beyond-gap criterion.

**H-C — conditional charged computational consequence.** Eligible only if **H-P PASS** and complete task-equivalent B0/G2 outputs are certified. Optimized Gray-code B0 is the only denominator; exact B1 and certified E2 are required *sensitivity arms*, not alternate denominators. After 3 warmups take **15 predeclared paired charged timings** with single thread and balanced order. For each valid pair calculate `r_i=C_B0,i/C_G2,i`; PASS iff `median(r_i)>=1.20` **and** `min(r_i)>=1.20`. If output equivalence passes and any measured ratio is below 1.20, label `THRESHOLD_NOT_MET` (not 'no speedup'). If a required paired round is missing/invalid/timed out, label `INCONCLUSIVE` or `EXECUTION_LIMIT`, preserving failed runs. **No inferential 95% interval is claimed.** The v009 nominal-95% bootstrap had only ~78–85% empirical synthetic coverage and is explicitly rejected as confirmatory.

G, P, T, C results are reported separately. No favorable finding can override another axis's failure. `VALID_STRUCTURAL_REDUCTION`/`TRANSFER_CONFIRMED` labels are not auto-awarded.

## 3. Analysis and controls

- **B0** optimized exhaustive Gray-code; **G1** full nominal grammar scan; **G2** constructive grammar with incremental pair updates; **B1** exact admissible-bound branch-and-bound; **E2** certified pair truncation with **75%** largest-|K| retained (fixed index ties), omitted-term rigorous bound and exact fallback; C1 oracle if included is informative only.
- **Nulls:** N1 degree-preserving and N2 free-incidence, **1,000 valid** each, **5,000 attempt cap** each, master seed `20261010` via frozen v009 domain-separated seed derivation; reject malformed independently of target performance; record survivors, acceptance counts, `Δ_null`, and preservation. Null comparisons **descriptive only**—no preregistered confirmatory p-value/null-superiority verdict.
- **Z2 symmetry** not used in primary. Any sensitivity must enable it equally for all applicable solvers and charge all costs.
- Run same task at fixed E0 and same threshold. Solver candidate order and flags must match the v009 documented/tested implementations. Report actual compiler flags and hash binaries.
- Primary limits **30 min per arm, 2 GiB RSS**; 15 paired rounds after 3 warmups; deterministic balanced order. Report CPU and wall time, pair operations, branches, generated nodes, memory, setup, reference certification and full verifier-audit cost separately. Deployment scenarios must explicitly include any indispensable correctness certification.
- Strict physical level boundary protocol: high-precision direct-energy check for close calls; inclusive exact equality, operational `tau` expansion distinct from energy-error tolerance and reporting-level grouping. Conservatively include unresolved target-boundary cases while making an unqualified P PASS unavailable if any unresolved certification remains.

## 4. Prospective falsification and reporting

- **G FAIL:** nonmatching generated set, energy-informed grammar leakage, or <99% candidate contraction; missing validation INCONCLUSIVE.
- **P FAIL:** any false exclusion (`FN>=1`) or a proven incorrect result; incomplete exact verification INCONCLUSIVE.
- **T NOT_TESTED** regardless of other axes.
- **C NOT_ELIGIBLE** if P fails; `THRESHOLD_NOT_MET` if complete valid paired measurements fail either 1.20 criterion; `INCONCLUSIVE` for incomplete/uncertified timing or output; PASS only by the fixed finite-sample rule. Do not drop unfavorable rounds.
- The primary W target must be reported even if it fails. Sensitivity windows and any post hoc exploration are labeled and **cannot rescue primary criteria**.
- Report physical survivor count, exact complete target sets, FN IDs and their physical energies, exclusion-gap diagnostics and null-gap distributions, full cost ledger, paired ratios, environment and hashes. No false claim that excluded non-ice configurations are physically nonexistent.

## 5. Blindness, frozen inputs, authorization

v005–v009 and the primary grammar, parameter model, seeds, target windows and scoring rules are immutable scientific inputs. No GitHub modifications. v007 post-hoc V4 tolerance revision remains part of historical disclosure. The verifier shares authorship with the grammar implementation, although it is separately implemented and cross-validated; it is **not externally independent**.

**This document's freeze does NOT grant permission to run the 3×3 W>0 experiment.** Retain guard; require a separately documented explicit primary authorization after confirming the file/hash manifest and execution command set. If a hash differs or a protocol required implementation flag is absent, STOP and create an additive amendment before any unblinding.

**Status:** PRIMARY_PROTOCOL_FROZEN / PRIMARY_NOT_AUTHORIZED / T_NOT_TESTED.

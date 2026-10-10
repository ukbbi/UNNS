# SCR_III_COUPLING_SPEC_v001

**Phase:** SCR-III-A — Coupling Threshold and Valid Reduction (controlled coupling-gradient)
**Status:** `RATIFIED_SPEC` — coupling specification frozen as the design basis for `SCR_III_PREREG_v001`.
**Drafted:** 2026-10-07  
**Ratified:** 2026-10-08
**Depends on (frozen, read-only):** SCR-I v003, SCR-II v002

Tags used below:

- **[DERIVED]** computed from frozen v002 records during drafting (read-only; no frozen file touched).
- **[ANALYTIC]** follows from counting; not yet verified by a pilot.
- **[RATIFIED]** a design choice or threshold frozen for SCR-III-A v001.

---

## 0. What this spec does, and what changed from `CTX_SCR_NEXT.md`

This ratified specification freezes the *meaning* of the coupling parameter, the interface any construction must satisfy, the v001 construction, the measures, controls, pre-primary gates, populations, and verdict rules. Changes to these scientific choices require a new specification version.

Re-reading the frozen v002 engine and records changed the design in three ways:

1. **Exact preservation was infeasible in all 30 v002 cells, whatever the coupling.** The grammar admitted 1–48 complete routes per instance; the exact solution sets had 338–10,461 members (§2). `S_T ⊆ S_G` was impossible by counting. Any coupling-gradient on the v002 family with its 2–4 % density band would return `P_exact ≡ 0` and be uninformative.
2. **The all-or-nothing exact tier is the wrong primary curve.** Its threshold depends on multiplicity (§3). The primary curves are recall and chance-corrected excess inclusion; exact preservation stays as the strict validity tier.
3. **SCR-III-A is a ruler experiment, not a discovery experiment.** Its outcome is substantially predictable from counting. Its value is a calibrated coupling scale with known ground truth, validated deployment-label-free SCR applicability estimators, and a measured reduction–preservation frontier. Whether UNNS grammars show real coupling is SCR-III-B's question (§14).

A drafting-time smoke test of the now-ratified construction on the frozen engine (§6.6) ran cleanly and produced a graded dose-response in recall and \(P_{exact}\) against q. It also indicates that no condition on the frozen grid is expected to reach the strict 20/20 exact-validity tier; v001 is therefore intentionally map-first (O12).

Symbol hygiene: this spec avoids \(\kappa\) (used for \(A_\kappa\) in STRUC-I), \(\lambda,\lambda_\star\) (τ-field coupling), \(\gamma_0,\beta,K,W\) (Chamber LII mechanism space) and \(\Lambda\). The coupling knob is **q**; the structural-degeneracy knob is **σ**.

---

## 1. Provenance and frozen inputs

SCR-III imports the following SCR-II v002 artifacts **unmodified**. Their SHA-256 values at drafting match `SHA256SUMS_ENGINE.txt` / `SHA256SUMS_V002_PREP.txt`:

| File (under `scr_ii/`) | SHA-256 |
|---|---|
| `grammar/route_grammar.py` | `f0b855b8201a23ba6abb175b8b342627fd4e389fc41608fe7b3b27958946c1a0` |
| `filter/structural_filter.py` | `162d91a9e75af7c7569069ec8049c5089c555a003a04e8a718dc84776c5f5be6` |
| `solver/exact_solver.py` | `f981bc237e99e605ea66b93a5175e0145110a9cff02236c11cdc39ee486539b0` |
| `nulls/controls.py` | `83451edaa2c1da0657cf7a21394944541be7d6f7929e5aae50bcc677f7f0caf1` |
| `generator/route_csp_i_v002.py` | `9f7e38c95e00f930af437a92fca3981344acb888d6a8fdb754ee1d2bc4f88d98` |
| `engine_common.py` | `4bd542d52e236248d8453bf00e8871335eadf9df6def44ee312c258a56a40bfe` |
| `analysis/metrics.py` | `58ddf67184cd53794174d69aaf52c88777cdc9c5d2b6cbceec3c54b3836b9cfd` |

Rules:

- The grammar Γ_route v001 (G1→G4, in that order), the structural filter, and the three solvers (`solve_baseline`, `solve_scr`, `solve_solver_native`) are **byte-identical** to v002. The preregistration must re-verify these hashes at preflight.
- `structural_filter.py` imports `structural_view` from `generator.route_csp_i` (the v001 module). That module stays in place. Any new instance must carry the same structural field names (`symbol`, `phase`, `discontinuity`, `branch_id`) so the frozen view function works unchanged.
- New code lives in a new `scr_iii/` branch. Nothing under `scr_ii/` or `SCR_I_PREREG_v003/` is edited. Any continuation of a frozen item is a new version.

---

## 2. Findings from the frozen v002 records [DERIVED]

Source: `scr_ii/output/v002_primary/PRIMARY_RESULT_v002.json` (30 cells). \(L=|S_G|\) is `leaves_scr`, the number of complete routes the filter admits; \(m=|S_T|\) is `solution_count_baseline`; \(N=2^d\).

### 2.1 Admitted set versus target set

| depth | cells | \(m\) range | \(L\) median (max) | `r_leaf` median | exact-preservation ceiling \(1-\rho\) |
|---|---|---|---|---|---|
| 14 | 10 | 338–647 | 8 (48) | 0.99951 | 0.9605–0.9794 |
| 16 | 10 | 1,612–2,584 | 4 (18) | 0.99994 | 0.9606–0.9754 |
| 18 | 10 | 5,820–10,461 | 4 (24) | 0.99998 | 0.9601–0.9778 |

Across all 30 cells: \(L<m\) in **30/30**, and the largest \(L\) (48) is below the smallest \(m\) (338). The overall ceiling \(1-\rho\) ranges 0.9601–0.9794. Observed `r_leaf` (median 0.999939) is far above it.

### 2.2 Consequences

- **Pigeonhole.** \(S_{SCR}=S_T\cap S_G\), so \(S_{SCR}=S_{baseline}\) requires \(L\ge m\). It failed in every cell before any solution was examined. The frozen record `PRESERVATION_FAIL 30/30` stands; its interpretation needs the qualifier in §2.4.
- **Reduction ceiling.** Any preservation-valid filter on these instances has \(R_{leaf}\le 1-\rho\le 0.98\). The 99.99 % contraction v002 observed was incompatible with preservation by construction.

### 2.3 Retrospective enrichment over matched-random retention

Matched-random leaf retention (each of the \(L\) admitted leaves is a uniform draw from the \(N\) leaves) predicts the retained solution count per cell as \(mL/N\).

- Retained solutions: **17 observed** versus **7.79 expected** (ratio 2.18). The hypergeometric z of 3.4 is overstated because admitted leaves share prefixes and hits clump (one cell returned 4, another 3).
- Cells returning at least one solution: **10 observed** versus **6.20 expected** (sd 2.00, z = 1.9). This cell-level test is the safer one.
- Per-cell excess inclusion EI (§4): mean +2.6×10⁻⁴, median −1.6×10⁻⁵, range −0.0020 to +0.0061. 20 cells have zero retained solutions.

Reading: coupling in v002 was approximately zero, with at most a weak positive excess. Note that an earlier informal comparison of 0.016 % retained against 0.06 % "random" mixed node-level and leaf-level reduction; at leaf level the random expectation is 0.0073 %, so v002 was **not** below chance. SCR-I recorded a 1.889× target-recall enrichment over rate-matched random pruning; the 2.18× here is a different quantity, but the similar magnitude is worth checking in SCR-III-B rather than interpreting now.

### 2.4 Interpretation addendum (to be recorded in `SCR_III_STRUCTURE_v001`, not by editing frozen v002 files)

> v002's non-transfer is correct and frozen. It was additionally forced by counting: the grammar's admitted set was smaller than the target set in every cell. v002 therefore establishes that large contraction with an independent dense target cannot preserve the target set; it could not distinguish "unaligned" from "aligned but too dense". The transfer-boundary statement remains a necessary condition, not a sufficient one.

---

## 3. Counting lemmas [ANALYTIC]

Let \(N=2^d\), \(m=|S_T|\), \(L=|S_G|\), \(a=L/N\), \(\rho=m/N\).

**L1 — Feasibility.** Exact preservation requires \(L\ge m\), equivalently \(R_{leaf}\le 1-\rho\).

**L2 — Blind-filter loss.** If \(S_T\) is independent of \(S_G\), the chance all \(m\) solutions fall inside \(S_G\) is \(\binom{L}{m}/\binom{N}{m}\le a^m\). Expected loss is \(m(1-a)\). For \(m\ge 2\) and small \(a\), exact preservation under independence is negligible.

**L3 — Multiplicity dependence.** If each solution leaks independently with probability \(\varepsilon=1-r\), \(P_{exact}\approx(1-\varepsilon)^m\approx e^{-m\varepsilon}\). Hence the coupling needed for exact preservation tightens as \(m\) grows (\(\varepsilon\lesssim 1/m\)). The independence assumption can fail (solutions can leak together); SCR-III measures the departure (§8, dispersion).

Consequences for design:

- Claims must be stated per multiplicity class, or in the collapse variable \(m\varepsilon\). A single universal "threshold" is not expected to exist.
- The v001 planted-backbone design (\(m=1\)) is the \(q\to1\) degenerate endpoint of the family below; v002 is the \(q=0\) endpoint. SCR-III interpolates between them, under a multiplicity floor.

---

## 4. Definitions

| Symbol | Meaning |
|---|---|
| \(d\), \(N=2^d\) | route depth, nominal route count |
| \(S_G\), \(L\) | complete routes admitted by G1→G4 (structure-only quantity) |
| \(S_T\), \(m\) | exact solution set of the checksum / cost-window / terminal-seal predicate (independent of the filter) |
| \(r=\lvert S_T\cap S_G\rvert/m\) | recall (per-solution survival) |
| \(\ell=\lvert S_T\setminus S_G\rvert\) | leak count; exact preservation iff \(\ell=0\) |
| \(a_0=\lvert S_G\setminus S_T\rvert/(N-m)\) | admission rate of non-solutions |
| **EI** \(=(r-a_0)/(1-a_0)\) | **excess inclusion**: chance-corrected recall. 0 = independent of target membership; 1 = full inclusion; negative = anti-aligned. Undefined if \(a_0=1\) (reported as "no contraction") |
| **q** | nominal coupling fraction (§6): share of layers at which the arithmetic layer respects the structural distinction |
| **σ** | structural degeneracy: probability a layer's decoy option is structurally indistinguishable from the good option |
| \(D\) | distinguishing layers (decoy differs structurally), \(\lvert D\rvert\approx(1-\sigma)d\) |
| \(M\) | masked layers, \(\lvert M\rvert=\mathrm{round}(qd)\) |
| **C** \(=\lvert M\cap D\rvert/\lvert D\rvert\) | **coverage**: ground-truth coupling in the ruler (structure + mask only; never uses survival) |
| \(N_{rej,free}\) | number of unmasked layers whose decoy is rejected by the frozen gates when evaluated from the good-path state (structure-only) |
| \(R_{leaf},R_{node},G_{time}\) | as defined in `SCR_II_PREREG_v002/METRICS.md` (filter cost included in \(T_{SCR,total}\)) |

---

## 5. Design principles

- **P1 Frozen G, filter, solvers.** Byte-identical to v002 (§1).
- **P2 Shared latent only.** The only link between structure and target is the declared C-MASK channel (§6.2). Nothing else may connect them.
- **P3 Filter blind.** The filter reads `structural_view` only. The v002 mutation test (`test_v002_firewall.py`) is extended to every new field.
- **P4 Acceptance never reads survival.** Instance/family acceptance may use only baseline multiplicity \(m\), the frozen design constants, and structure-only quantities. It may not use \(S_T\cap S_G\), recall, EI, exact preservation, or any post-filter target label.
- **P5 q is ordinal; C is realized ground truth.** Results are reported against nominal q and realized coupling coverage C. q is the imposed dose; C is the realized structural coverage of that dose.
- **P6 Paired, nested family design.** Seed family \(i\) at depth \(d\) is shared across all q and σ levels. Skeleton uniforms, mask permutation, and base arithmetic draws are shared. Masks are nested in q. A single accepted arithmetic-attempt index is used for the whole q-family; condition-specific acceptance is forbidden.
- **P7 Whole-family anti-leakage.** Any calibration/holdout split for the SCR applicability estimators is by complete seed family. Sibling q/σ cells from the same family may never be split across calibration and holdout.
- **P8 Anti-tuning.** After ratification no scientific constant, grid level, threshold, null, grammar rule, seed block, or validity definition may be changed within v001 in response to audit outcomes. Audit may only accept, exclude by a preregistered infeasibility rule, or close the study pre-primary.
- **P9 Anchors.** An unmodified v002-generator arm (A0) and a zero-contraction arm (Z0) are always run.
- **P10 Map-first.** SCR-III-A v001 is a coupling-ruler/map study. It is not required to produce a `VALID_STRUCTURAL_REDUCTION` condition. No post-audit expansion of q or σ is allowed within v001.
- **P11 No complexity-class language.**

---

## 6. Construction

### 6.1 Normative interface (any construction must satisfy)

- **N1** Predicate family unchanged in form: checksum mod 5, cost window, terminal seal.
- **N2** Arithmetic fields on options not touched by the coupling channel have the same law as v002.
- **N3** At σ = 0, q = 0 the generator reduces **in law** to v002 (byte identity is not required; the A0 arm supplies the byte-level anchor).
- **N4** Coupling is expressed only through instance fields. Solver and filter code are unchanged.
- **N5** Degeneracy refusal: instances with \(m<M_{min}\) are rejected, never silently accepted (v001 failure mode).
- **N6** Separate deterministic RNG streams: structure, arithmetic, coupling (mask).

### 6.2 `ROUTE_CSP_C v001` — layer-mask construction [RATIFIED]

Parameters: depth \(d\); σ ∈ {0.8, 0.9} for the main ruler; q ∈ {0.0, 0.1, 0.2, 0.3, 0.4} subject only to the preregistered depth-specific audit grid.

**Skeleton (structure stream).** As v002 `_structure`, with one extra variate \(u_i\) per layer, drawn unconditionally so skeletons are comparable across σ. If \(u_i<\sigma\), the decoy **mirrors** the good option: it copies the good option's `symbol`, `phase` and `discontinuity`, with `branch_id` swapped. At a mirror layer the gates cannot distinguish the options and the propagated structural state is identical. Otherwise the decoy is drawn as in v002.

**Mask (coupling stream).** A permutation π of the layers, independent of the structure stream and σ. \(M_q\) is the first \(\mathrm{round}(qd)\) entries of π. Masks are nested in q.

**Base arithmetic stream.** For each seed family and depth, the sequence of v002-style arithmetic attempts is generated once. The same attempt index is evaluated across every preregistered q level (and both σ levels). No q condition may select its own attempt.

For a given attempt and q, costs and checksum weights begin from the same v002 `_merge_attempt` draw. Then, for every masked layer \(i\in M_q\):

- the anchor bit is set to the good option's index (`backbone_bit`);
- the decoy option's `cost` is set to \(\mathrm{PENALTY}=2\,d\cdot\mathrm{COST\_MAX}\), which exceeds any attainable target window under the construction.

The anchor cost, checksum target, terminal seal and cost window are then computed as in v002, with half-width \(\mathrm{round}(0.025\,d\cdot1000)\). The anchor is a solution by construction.

**Declared coupling channel.** Arithmetic fields depend on structure only through `backbone_bit` at masked layers.

**Family-level acceptance.** For each seed family, inspect attempts 0–63 in order. An attempt is accepted only if **every active q level at that depth** satisfies both:

\[
m\ge M_{\min}=4
\]

and

\[
0.02\le m/2^f\le0.04,\qquad f=d-|M_q|.
\]

The first attempt satisfying all active q levels is frozen for the whole family and used at both σ levels. If no common attempt succeeds in 64 attempts, the family is recorded `INFEASIBLE_FAMILY`; its seed is not replaced. Survival, recall, EI and exact preservation are never consulted.

**Free layers by primary depth** (\(f\) after rounding \(qd\)):

| q | d = 14 | d = 16 | d = 18 |
|---|---|---|---|
| 0.0 | 14 | 16 | 18 |
| 0.1 | 13 | 14 | 16 |
| 0.2 | 11 | 13 | 14 |
| 0.3 | 10 | 11 | 13 |
| 0.4 | 8 | 10 | 11 |

The v001 primary grid stops at q = 0.4. q = 0.5 is not permitted in this version, regardless of audit outcomes.

### 6.3 Structure-only statistics and analysis populations

Before solving, compute \(L\), \(|D|\), coverage C, \(N_{rej,free}\), and \(R_{leaf}\). \(N_{rej,free}\) is obtained by calling the frozen `evaluate_gates` on each unmasked layer's decoy from the good-path state; no target-survival information is used.

Two populations are frozen:

**A — all-accepted analysis population.** Every successfully generated, non-`INVALID_RUN` cell is retained for recall, EI, \(P_{exact}\), reduction, cost, dispersion, and ruler plots. Cells with \(L<m\) or \(R_{leaf}<0.25\) remain in this population because they are informative about the reduction–preservation frontier.

**V — exact-validity-eligible population.** A cell is eligible for exact-validity classification only when:

\[
L\ge m
\]

and

\[
R_{leaf}\ge0.25.
\]

Cells with \(L<m\) are labelled `EXACT_TIER_INFEASIBLE`; cells with \(R_{leaf}<0.25\) are labelled `NO_MATERIAL_REDUCTION` for exact-tier purposes. Neither label removes the cell from population A.

Skeletons with \(|D|=0\) are valid zero-distinction observations in population A but are not validity-eligible unless they independently satisfy the exact-tier rules; Z0 remains the explicit zero-contraction anchor.

The screens use only structure and baseline multiplicity, never \(S_T\cap S_G\), recall, EI, or exact preservation.

### 6.4 Expected behaviour (to be measured, not assumed) [ANALYTIC]

- Typical (geometric) values: \(L\approx2^{\sigma d}\) and \(R_{leaf}\approx1-2^{-(1-\sigma)d}\). The *mean* \(L\) is larger (about 1.1–1.4 × \((1+\sigma)^d\) in the smoke test, §6.6) because the number of mirror layers is binomial and a few high-mirror skeletons dominate; mean \(R_{leaf}\) is correspondingly lower than the table.

| σ | d = 14 | d = 16 | d = 18 |
|---|---|---|---|
| 0.8 | \(R\approx0.86\), \(L\approx2.4\)k | 0.89, 7.1k | 0.92, 21.6k |
| 0.9 | 0.62, 6.2k | 0.67, 21.6k | 0.71, 75.4k |

- At σ ≥ 0.8 the *mean* \(L\) exceeds the largest feasible \(m\) (about 2× at σ = 0.8, d = 18, q = 0, where \(m\le0.04\cdot2^{18}\approx10.5\)k). \(L\) is random, though: at σ = 0.8, d = 18, q = 0 a sizeable minority of skeletons (roughly a quarter, from the binomial spread in mirror-layer count) still have \(L<m\) and are screened out as exact-infeasible (roughly 15–30 %, depending on \(m\) within the band; analytic estimate, not tested at d = 18). Lower q reduces \(m\) and shrinks that minority. Below about σ = 0.7 at d = 18, \(L<m\) on average at q = 0 and the exact tier is largely infeasible.
- First-order recall prediction: \(r\approx2^{-N_{rej,free}}\). This is approximate (admissible-by-luck decoys change propagated state), and is reported, not required.
- The exact tier is expected to move sharply with \(N_{rej,free}\), not gradually with q.
- Hard coupling only: this construction cannot model soft statistical dependence between structure and target.

### 6.5 `C-LABEL` note — out of scope for v001

C-LABEL was considered during drafting but is **not authorized in v001**. Target membership would be drawn as Bernoulli with rates depending on \(S_G\) membership while holding marginals fixed; this would give exact coupling control but would replace the arithmetic solver and remove the C1 ceiling. If C-MASK fails a closure gate, v001 closes pre-primary. C-LABEL would require a new specification and preregistration version.

### 6.6 Drafting-time smoke test (not preregistered, no verdict weight)

A throw-away prototype of §6.2 was run against the frozen v002 grammar, filter and solvers (imported unmodified), for d = 12 and 14, σ ∈ {0.8, 0.9}, q ∈ {0, 0.2, 0.4}, 30 seeds per condition, \(M_{min}=4\), density band 0.02–0.04 on the free subspace. **Seeds 9100000–9100029 are burned for this purpose and must not appear in audit or primary seed lists.**

- In-band acceptance 100 % in all 12 conditions. C1 exact in 100 % of cells. Extra solutions 0.
- **H3a holds in the sample:** all 29 cells with \(C=1\) were exact-preserving.
- Mean \(L\) was 1.1–1.4 × the mean of \(2^{\#\text{mirror}}\) (lucky decoys admit extra routes).
- First-order recall prediction \(2^{-N_{rej,free}}\) versus observed mean recall: \(N_{rej,free}=1\): 0.477 vs 0.500; \(=2\): 0.226 vs 0.250; \(=3\) (n = 8): 0.065 vs 0.125; \(=0\): 0.736 vs 1.0 (lucky decoys change propagated state, so the prediction is an approximation, as stated). \(P_{exact}\) by \(N_{rej,free}\) = 0, 1, 2, 3: 0.50, 0.12, 0.00, 0.00.
- Within the contraction- and feasibility-screened population, d = 14:

| σ | q | n | mean C | mean recall | \(P_{exact}\) | mean \(R_{leaf}\) |
|---|---|---|---|---|---|---|
| 0.8 | 0.0 | 28 | 0.00 | 0.30 | 0.04 | 0.73 |
| 0.8 | 0.2 | 28 | 0.14 | 0.35 | 0.14 | 0.73 |
| 0.8 | 0.4 | 28 | 0.44 | 0.47 | 0.21 | 0.73 |
| 0.9 | 0.0 | 20 | 0.00 | 0.39 | 0.00 | 0.59 |
| 0.9 | 0.2 | 20 | 0.24 | 0.49 | 0.20 | 0.59 |
| 0.9 | 0.4 | 20 | 0.59 | 0.69 | 0.55 | 0.59 |

  At d = 12, \(P_{exact}\) ran 0.04–0.53 over the same grid. Recall and \(P_{exact}\) increase with q, and C tracks q.
- **Implication:** exact-preservation rates can look deceptively high when skeletons contain few distinguishing layers. This is why Population A (full ruler map) and Population V (exact-validity eligibility) are separated (§6.3). Within q ≤ 0.4, the strict 20/20 condition-level `VALID_STRUCTURAL_REDUCTION` tier is **not expected** to occur. The primary output is the recall / \(P_{exact}\) map against q and C; C = 1 remains a construction anchor rather than a discovery result. See O12.

---

## 7. Arms and controls

| Arm | Definition | Role |
|---|---|---|
| **C0** | `solve_baseline` | ground truth \(S_T\) |
| **SCR** | `solve_scr` (unchanged) | structural arm under test |
| **C1** | `solve_solver_native` | problem-aligned ceiling; must preserve exactly in 100 % of cells |
| **A0** | unmodified v002 `generate_instance`, same depth-family seeds, same solvers | anchors SCR-III to SCR-II |
| **Z0** | σ = 1, q = 0 | zero-contraction control: \(S_{SCR}=S_{baseline}\) and \(L=N\) |
| **N1** | `solve_n1_random_prefix`; 50 replicates per cell, with per-edge \(p_{acc}=(L/N)^{1/d}\) derived from that cell's structure-only leaf fraction | rate-matched random retention; expected EI ≈ 0 |
| **N2** | frozen symbol permutation null from SCR-II v001 | tests dependence on actual structural symbols |
| **N3** | frozen degree-preserving transition permutation null from SCR-II v001 | tests dependence on the actual grammar |
| **N4** | preregistered anti-coupled construction below | sign check: EI must be ≤ 0 |

**N2/N3 subset.** Run 12 fixed permutations of each null on the first five preregistered primary seed families at every main \((σ,q,d)\) condition. Null outcomes are reported but do not alter the coupling-law verdict.

**N4 construction order.** Starting from the same base arithmetic draw and mask as C-MASK, define `anti_anchor_bit` as the decoy option at each masked layer. Apply the prohibitive penalty to the **good** option at masked layers, then compute the anti-anchor cost, checksum target, terminal seal and cost window from the anti-anchor route. Thus the constructed arithmetic target is directed toward the structurally disfavored branch before any solver is run. Mirror layers remain structurally neutral. No target-survival result is used in constructing N4.

A **solution-loss ledger** is recorded per SCR cell: for each baseline solution absent from \(S_{SCR}\), record the first failing gate via `walk_prefix`. This provides observational per-gate attribution. Causal single-gate coupling arms are deferred to `SCR_III_A2_GATE_ABLATION` and may not be added to v001 after results are seen.

---

## 8. Measures per cell

- **Preservation:** exact indicator \(S_{SCR}=S_{baseline}\) (strict tier); recall \(r\); leak count \(\ell\); \(a_0\); EI; extra solutions (must be 0).
- **Reduction:** \(R_{leaf}\), \(R_{node}\).
- **Cost:** \(G_{time}=T_{baseline}/T_{SCR,total}\) with the v002 convention (filter inside the traversal), plus \(T_{encode}\) (structural-view extraction) reported separately.
- **Structure-only:** \(L\), \(\lvert D\rvert\), C, \(N_{rej,free}\), \(m\), \(\rho\), \(f\).
- **Dispersion:** per condition, observed \(P_{exact}\) minus \(\overline{(1-\varepsilon)^m}\) (positive = solutions leak together).
- **Provenance:** instance SHA-256, accepted attempt, seeds, hash preflight.

---

## 9. SCR applicability estimators

Purpose: test whether limited calibration information can predict when SCR is usable on held-out instances. These are **deployment-label-free**, not absolutely label-free: target labels may be used in a preregistered calibration subset, but never from the held-out instance being predicted.

### E1 — family/regime calibration estimator

For each primary depth, the first five seed families in `SEEDS_v001.json` are the estimator-calibration families and the remaining fifteen are estimator-holdout families. Because the split is by whole family, sibling q/σ cells never cross the split.

For every \((σ,q,d)\) condition:

- compute mean recall and mean EI on the five calibration families;
- use those two means as the frozen predictions for the held-out condition mean recall and EI;
- evaluate predictions against the corresponding means on the fifteen held-out families.

Across the 30 main primary conditions, E1 passes if:

\[
\mathrm{MAE}(\widehat r,\bar r_{holdout})\le0.10
\]

and Spearman rank correlation between predicted and held-out condition-mean recall is ≥ 0.80. EI prediction error is reported separately.

This estimator answers a practical question: after solving a small calibration subset from a regime, can SCR applicability be predicted for comparable unseen instances?

### E2 — charged instance-level estimator

For each held-out primary cell, choose a deterministic random sample of eight prefix subtrees:

- prefix depth \(h=6\) for d ∈ {14,16,18};
- sample 8 of the \(2^h=64\) subtrees without replacement;
- subtree-sampling RNG is derived from the family seed and `estimator_sample_seed` in `SEEDS_v001.json`.

Exhaustively enumerate those sampled subtrees under C0 and SCR, estimate \(r\) and \(a_0\), and form \(\widehat{EI}\). The estimator never reads the unsampled target set. Its compute cost is recorded as \(C_{E2}\) and is not hidden inside a claimed net gain.

E2 passes if, across estimator-holdout primary cells:

- recall MAE ≤ 0.10; and
- Spearman correlation between predicted and observed recall ≥ 0.80.

\(C_{E2}/T_{baseline}\) is reported but is not a v001 pass/fail threshold.

Neither E1 nor E2 is called a direct estimator of the synthetic ground-truth coverage C. They are applicability estimators for preservation behaviour.

---

## 10. Pre-primary gates (audit stage)

Audit seeds are disjoint from primary seeds. **No scientific constant is tunable after ratification.** \(M_{min}=4\), PENALTY \(=2d\,COST_{MAX}\), the q/σ grids, estimator split, estimator thresholds, null definitions, and validity rules are frozen. N1's \(p_{acc}\) is a derived rate-matching quantity, not a tuned constant.

| Gate | Check | Failure status |
|---|---|---|
| PG1 | frozen-file hashes; determinism; RNG stream separation; extended arithmetic/filter firewall mutation tests; declared coupling channel is the only structure→arithmetic dependence; whole-family attempt reuse verified | `INVALID_RUN` |
| PG2 | σ = 0, q = 0 generator matches v002 in law against A0 for m, density and attempt behaviour | `CLOSED_PRE_PRIMARY — GENERATOR_NOT_V002_EQUIVALENT` |
| PG3 | family-level common-attempt acceptance rate ≥ 0.5 at each audit depth; all accepted cells satisfy \(m\ge4\) and the frozen free-subspace density band | failing depth/grid entries recorded `INFEASIBLE_CONDITION`; no replacement grid |
| PG4 | for each σ, at least one q has audit \(P(L\ge m)\ge0.9\) | σ level labelled `EXACT_TIER_INFEASIBLE`; still retained for population-A recall/EI |
| PG5 | dose response: one-sided seed-blocked permutation trend of recall versus ordered q is positive at nominal p < 0.10 in each audit panel | `CLOSED_PRE_PRIMARY — COUPLING_NOT_INDUCED` |
| PG6 | N4 sign check: median EI ≤ 0 | `CLOSED_PRE_PRIMARY — KNOB_SIGN_ERROR` |
| PG7 | Z0 exact and \(L=N\) in 100 % of valid audit cells | `INVALID_RUN` |
| PG8 | C1 exact in 100 %; baseline versus solver-native agreement | `INVALID_RUN` |
| PG9 | informative band: at least one audit condition with mean recall in (0.1, 0.9) | `CLOSED_PRE_PRIMARY — STEP_FUNCTION_KNOB` |

Audit outcomes cannot add q = 0.5, σ = 0.95, alter the multiplicity floor, or change any threshold. Any such change requires `SCR_III_COUPLING_SPEC_v002` and a new preregistration.

---

## 11. Design grid and seeds [RATIFIED]

| Factor | Levels |
|---|---|
| σ | main: 0.8, 0.9; anchors: Z0 at 1.0 and A0 v002 generator |
| q | fixed at 0.0, 0.1, 0.2, 0.3, 0.4 for primary |
| depth | audit: 10, 12; primary: 14, 16, 18 |
| audit q | d = 10: 0.0–0.3; d = 12: 0.0–0.4 |
| seed families | audit: 12 per depth; primary: 20 per depth |
| estimator split | first 5 primary families per depth = E1 calibration; remaining 15 = estimator holdout |

Main primary cells: \(2\times5\times3\times20=600\), plus A0 \(3\times20=60\) and Z0 \(3\times20=60\): **720 planned cells** before preregistered infeasibility logging.

The exact integer lists are frozen in `SEEDS_v001.json`. The same family seed is reused across q and σ as required by P6. Seeds are disjoint from the explicit SCR-I v003 and SCR-II v001/v002 blocks in the supplied project archive and from burned smoke-test seeds 9100000–9100029.

No failed or infeasible primary seed is replaced.

---

## 12. Hypotheses and analysis plan

### Confirmatory

**H0 — anchors.**
- A0: reproduce the qualitative v002 regime: \(L<m\) in 100 % of A0 cells and exact preservation 0/60. EI is reported against the frozen v002 range; failure to lie inside that range is a diagnostic, not a reason to alter the design.
- Z0: \(L=N\) and exact preservation in 100 % of valid cells.

**H1 — paired dose-response.** For each of the six primary \((σ,d)\) panels, test positive ordered recall response to q with a one-sided **seed-blocked permutation trend test**.

For each family \(i\), using all successfully generated q cells in population A, define

\[
T_i=\sum_j(q_{ij}-\bar q_i)(r_{ij}-\bar r_i),
\qquad
T=\sum_iT_i.
\]

Under the null, permute q labels within each seed family while preserving the observed missingness pattern. Use 100,000 Monte Carlo permutations with RNG seed `trend_permutation_seed` from `SEEDS_v001.json`. Test one-sided \(T>0\). Holm-correct the six panel p-values at familywise α = 0.05. Median recall by q is reported descriptively.

**H3a — construction anchor.** In population V, cells with \(C=1\) must be exact-preserving. This is a correctness check, not a discovery result.

**H3b — leak regime.** \(P_{exact}\le0.20\) when \(N_{rej,free}\ge3\).

**H4 — applicability estimation.** E1 and E2 meet the §9 frozen validation criteria on their held-out units.

**H5 — controls.**
- N1 mean EI within ±0.01;
- N4 median EI ≤ 0;
- Z0 and C1 pass their exactness requirements;
- N2/N3 are reported as structural-null diagnostics and are not verdict-bearing.

### Exploratory

- recall versus \(2^{-N_{rej,free}}\);
- \(P_{exact}\) versus \(m(1-r)\) and versus \(N_{rej,free}\);
- departure from the independent-leak prediction \(P_{exact}\approx\overline{r^m}\);
- dispersion and clustering of leaks;
- per-gate attribution from the solution-loss ledger;
- N2/N3 structural-null comparisons.

### Presentation

For every \((σ,d)\) panel report recall(q), EI(q), \(P_{exact}(q)\) with Clopper–Pearson intervals, \(R_{leaf}\), \(R_{node}\), \(G_{time}\), C, \(N_{rej,free}\), and C1 alongside. Plot against nominal q and realized C. Population-A and exact-validity classifications are shown separately.

---

## 13. Verdicts

### Cell level

Apply in this order:

`INVALID_RUN`
→ `PRESERVATION_FAIL` (exact set differs)
→ `NO_MATERIAL_REDUCTION` (\(R_{node}<0.25\))
→ `REDUCTION_WITHOUT_NET_GAIN` (\(G_{time}<1.10\))
→ `VALID_STRUCTURAL_REDUCTION`.

Recall/EI remain reported for every non-invalid cell regardless of exact-tier verdict.

### Condition level

A condition may be called **`VALID_STRUCTURAL_REDUCTION`** only if:

1. all 20 preregistered primary families were successfully generated;
2. all 20 cells are exact-validity eligible (population V);
3. all **20/20** are exact-preserving;
4. median \(R_{node}\ge0.25\); and
5. median \(G_{time}\ge1.10\).

The 95 % Clopper–Pearson interval is always reported. Exact means exact; a condition with any failed cell is not given this label.

A separate descriptive tier **`HIGH_RELIABILITY_REDUCTION`** may be reported when at least 18/20 preregistered cells are exact-preserving and the reduction/gain thresholds pass. This tier is not an exact-equivalence claim and does not count as `TRANSFER_CONFIRMED`.

### Study level

- **`TRANSFER_CONFIRMED`**: at least one predeclared condition satisfies `VALID_STRUCTURAL_REDUCTION` independently at each primary depth 14, 16 and 18 under the same q/σ setting. v001 is not designed to force this outcome.
- **`COUPLING_LAW_CANDIDATE`**: H1 passes in all feasible primary panels after Holm correction; H4 passes; H5 verdict-bearing controls pass; C1 is exact in 100 %; and the direction of recall with realized C is consistent with the preregistered ruler construction.
- **`COUPLING_MAP_ONLY`**: primary executes validly and yields the preregistered reduction–preservation map, but the criteria for `COUPLING_LAW_CANDIDATE` are not all met.
- **`CLOSED_PRE_PRIMARY — <reason>`**: a §10 closure gate fails. This is benchmark/design rejection, not a negative SCR result.

No complexity-class language is permitted.

---

## 14. What SCR-III-A can and cannot show

**Can show:** a coupling scale with ground truth; the measured reduction–preservation frontier on a grammar whose reach is controlled by σ; whether the estimator of §9 tracks that truth; whether the counting predictions of §3 hold in this engine.

**Cannot show:** that any UNNS grammar is coupled to any real target. Coverage C is set by the generator, so high-coupling results are true by construction and are labelled as such. Whether real systems fall in the preservation-valid region is SCR-III-B's question, answered by applying the §9 estimator to a physical benchmark whose grammar was frozen without access to the target.

UPI/H-UPI (blinded explanatory diagnostic) is out of scope here; revisit in SCR-III-B.

---

## 15. Ratified decisions

| # | Decision | Ratified v001 choice |
|---|---|---|
| O1 | Construction | C-MASK (§6.2). C-LABEL is not part of v001; using it requires a new version. |
| O2 | σ levels | 0.8, 0.9; Z0 at 1.0; A0 as the v002 anchor |
| O3 | q grid | 0.0–0.4 step 0.1 for primary; no q = 0.5 in v001 |
| O4 | \(M_{min}\), density band | 4; 0.02–0.04 on the free subspace |
| O5 | Exact condition validity | strict 20/20 exact-preserving, all 20 validity-eligible, plus reduction/gain thresholds; ≥18/20 may be reported only as `HIGH_RELIABILITY_REDUCTION` |
| O6 | Estimator thresholds | E1/E2 recall MAE ≤ 0.10 and Spearman ≥ 0.80 on preregistered held-out units |
| O7 | Seeds per depth | audit 12 families; primary 20 families |
| O8 | Seed block | explicit in `SEEDS_v001.json`; family-shared, script-verified disjoint; smoke-test block excluded |
| O9 | v002 interpretation addendum | record §2.4 in `SCR_III_STRUCTURE_v001`; frozen v002 files remain untouched |
| O10 | Per-gate causal arms | deferred to named future extension `SCR_III_A2_GATE_ABLATION`; v001 keeps only the solution-loss ledger |
| O11 | Schema | create `scr_iii/schemas/route_csp_c_v001.schema.json` because SCR-III has a distinct benchmark/version/interface and coupling metadata. The reason is **not** a nonexistent option-cost maximum in the old schema. |
| O12 | Study target | v001 is map-only by design; no q/σ expansion after audit. Any high-coupling extension requires a new spec/prereg version. |

These decisions are closed for v001.

---

## 16. Ratification outputs

This specification is now the frozen scientific basis for:

1. `SCR_III_STRUCTURE_v001.md` — phase layout and frozen-branch discipline, including the §2.4 interpretation addendum.
2. `SCR_III_PREREG_v001.md` — executable preregistration of the ratified design, grids, seed families, nulls, tests, populations, and verdict rules.
3. `SEEDS_v001.json` — explicit seed families and deterministic analysis RNG seeds.

No audit or primary execution is authorized until the preregistration preflight passes.

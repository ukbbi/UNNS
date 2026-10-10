# SCR_III_COUPLING_SPEC_v002

**Phase:** SCR-III-A — Coupling Threshold and Valid Reduction (controlled coupling-gradient)
**Status:** `RATIFIED_SPEC` — design decisions in §12 are frozen for SCR-III-A v002. Audit remains unauthorized until `SCR_III_PREREG_v002` preflight passes.
**Drafted:** 2026-10-08
**Supersedes (design basis only):** `SCR_III_COUPLING_SPEC_v001` (`RATIFIED_SPEC`, frozen; **not edited**)
**Depends on (frozen, read-only):** SCR-I v003, SCR-II v002, `SCR_III_COUPLING_SPEC_v001` (all sections not listed in §3 carry over unchanged)

Tags: **[DERIVED]** computed from existing records · **[ANALYTIC]** from counting or design-only simulation · **[PILOT]** from the acceptance-only pilot (§2.3) · **[RATIFIED]** frozen for v002.

---

## 0. Why v002 exists

`SCR_III_PREREG_v001` audit closed as

> `CLOSED_PRE_PRIMARY — COUPLING_NOT_INDUCED` (failure: PG5), `AUDIT_RESULT_v001.json`.

That closure is **final and is not rescued**. No v001 cell is re-run, re-gated or re-interpreted as a pass. v001 audit seeds `2026111101–12` and `2026111201–12` are spent.

The closure is a *design-resolution* closure, not a negative SCR result and not evidence that C-MASK fails to induce coupling:

| Audit panel | PG5 p (one-sided) | Families with any delivered dose (C range > 0) |
|---|---|---|
| d=10, σ=0.8 | 0.640 | 3 / 8 |
| d=10, σ=0.9 | 0.254 | 1 / 8 |
| d=12, σ=0.8 | 9.0×10⁻⁵ | 4 / 5 |
| d=12, σ=0.9 | 0.0248 | 2 / 5 |

(Dose-delivered counts from `main_cells` coverage C, a structure-and-mask-only quantity.) The d=10 panels failed PG5 mostly because the nominal dose q rarely reached any distinguishing layer, so q changed nothing in most families. The d=12 panels, where it was delivered, show the expected positive response. PG5 as written tested **nominal q**, which is only the *imposed* dose; P5 of v001 already says realized coverage C is the delivered dose. v001 therefore contained a spec-internal inconsistency that the audit exposed.

v002 repairs the audit's resolution and gating. It does **not** change the construction, the q-grid, the σ levels, the controls, the populations, the exact-validity rule or the map-first posture.

---

## 1. Retrospective data used, and its status

Everything below was computed read-only from frozen v001 artifacts, plus an acceptance-only pilot. Using the v001 audit to motivate a v002 repair is legitimate **because v002 gets a new preregistration and fresh seed blocks**; it would not be legitimate inside v001 (P8). The v001 audit outcome is cited here as the motivation for changes C1–C3, and §3 states each change's *design* justification independently of the audit's outcome, so the v002 gates are not tuned to produce a pass.

---

## 2. Findings

### 2.1 Dose delivery depends on σ and depth, not only on q [ANALYTIC]

Distinguishing layers are those with \(u_i\ge\sigma\), so \(|D|\sim\mathrm{Bin}(d,1-\sigma)\). Coverage \(C(q)=|M_q\cap D|/|D|\) is non-decreasing in q because masks are nested, and \(C(0)=0\). A family delivers a dose iff \(\max_q C(q)>0\). Design-only Monte Carlo (20,000 random skeleton/mask draws per cell, no solver, no outcomes):

| d | σ | P(dose delivered) | P(C range ≥ 0.5) | mean distinct C levels |
|---|---|---|---|---|
| 12 | 0.8 | 0.67 | 0.47 | 1.9 |
| 12 | 0.9 | 0.41 | 0.36 | 1.2 |
| 14 | 0.8 | 0.73 | 0.48 | 2.1 |
| 14 | 0.9 | 0.46 | 0.39 | 1.3 |
| 16 | 0.8 | 0.73 | 0.40 | 2.1 |
| 16 | 0.9 | 0.47 | 0.37 | 1.4 |
| 18 | 0.8 | 0.79 | 0.42 | 2.3 |
| 18 | 0.9 | 0.52 | 0.40 | 1.5 |

Consequences: (i) at σ=0.9 only about half of families deliver any dose, and the delivered C usually takes just two values (0 and a jump); (ii) q is a weak proxy for dose at small d; (iii) a depth-10 audit is structurally under-resolved. (For comparison, σ=0.6–0.7 would deliver dose in ≥0.88 of families, but v001 §6.4 shows the exact tier becomes infeasible at lower σ; σ is **not** changed in v002, see O-D6.)

### 2.2 Latent v001 problem: the "all 20 generated" validity clause [DERIVED from v001 §13 + §2.3 pilot]

v001 §13 condition-level `VALID_STRUCTURAL_REDUCTION` requires "all 20 preregistered primary families were successfully generated". With family-level infeasibility of roughly 12–35 % (§2.3), that clause would fail almost every condition before any solver result is read. This was not visible to the audit, which closed earlier. It is repaired in C5 (not outcome-driven).

### 2.3 Acceptance-only pilot [PILOT]

Purpose: measure common-attempt family acceptance (§6.2 of v001) at candidate audit and primary depths, with q-grid {0,.1,.2,.3,.4} unchanged. Acceptance reads only baseline multiplicity and free-subspace density (P4). **No recall, EI, preservation, `solve_scr` or filter output was read.**

- Seeds: `9212000–9212039` (d=12), `9214000–9214039` (d=14), `9216000–9216039` (d=16), `9218000–9218039` (d=18). **All four blocks are burned for this purpose** and must not appear in any v002 audit or primary seed list. (Together with v001's burned block `9100000–9100029`.)
- 40 families per depth (24 at d=18), up to 256 attempts (64 at d=18) so the attempt-cap curve is visible; σ irrelevant to acceptance.
- **Caveat:** the session's copy of the engine lacked `scr_iii/compat.py` and `scr_iii/engine_common.py`. The pilot used a functionally equivalent shim (SHA-256-derived `stable_int`, same generator file). Frozen v002-grammar and generator code were byte-identical; the stream-key hashing differs, so individual seeds do **not** reproduce v001 audit outcomes (checked: 7/12 shim vs 5/12 real on the same d=12 seeds, different families). Pilot rates are therefore statistical evidence about the construction only and **must be re-measured with the real engine in `SCR_III_PREREG_v002` preflight** before they are relied on.

| depth | families accepted ≤16 / 32 / **64** / 128 / 256 attempts (of 40) | rate at 64 |
|---|---|---|
| 12 | 25 / 27 / **31** / 31 / 32 | 0.78 |
| 14 | 22 / 25 / **28** / 31 / 35 | 0.70 |
| 16 | 24 / 26 / **26** / 27 / 29 | 0.65 |
| 18 | 15 / 15 / **18** of 24 (64-attempt cap only; the 256-attempt run was abandoned as too slow) | 0.75 |

Per-attempt pass rate falls with q (d=14: 0.67, 0.62, 0.38, 0.24, 0.13 for q = 0 … 0.4), so the common-attempt intersection is dominated by q=0.3–0.4, where the free subspace has few bits. The 64-attempt cap already clears the v001 PG3 floor (≥ 0.5) at every depth ≥ 12; raising the cap to 256 would add only 3–18 points and would also accept more late, atypical attempts. Roughly 12–35 % of families remain infeasible regardless of cap, so these must be planned for, not replaced.

---

## 3. Changes from v001 [RATIFIED]

Every section of v001 not listed here is **unchanged and incorporated by reference**: grammar and solver imports (§1), counting lemmas (§3), definitions (§4), P1–P11 except where noted, construction C-MASK (§6.2) including M_min=4, density band 0.02–0.04, PENALTY, mask and mirror rules, populations A/V (§6.3), arms C0/SCR/C1/A0/Z0/N1–N4 (§7), measures (§8), estimators E1/E2 (§9) with the same pass criteria, cell verdicts (§13 cell level), and "no complexity-class language".

| # | Change | v001 text | v002 text | Design reason (independent of audit outcome) |
|---|---|---|---|---|
| **C1** | PG5 tests realized coverage, with a structure-only dose-delivered rule | PG5 one-sided seed-blocked trend of **recall vs ordered q** in each audit panel | Trend statistic uses **realized C**; families with \(\max_q C_i=0\) are `DOSE_FREE_FAMILY` and contribute zero (§4) | P5 already defines C, not q, as the delivered dose. A family whose masks never touch a distinguishing layer has no manipulation in it. |
| **C2** | Panel-informativeness precondition (PG5a) | none | A panel enters PG5 only if it has ≥ `n_dose_min` dose-delivered accepted families (§4.2) | Prevents a panel with one or two lucky families from deciding closure either way. |
| **C3** | Audit depth | audit d=10, 12 | audit **d=14 only** (§6) | §2.1: d≤12 is under-resolved at σ=0.9; d=10 is below the primary range. Audit and primary may share a depth when seed blocks are disjoint and the design is frozen first. |
| **C4** | Attempt cap | MAX_ATTEMPTS = 64 | **64 retained** | §2.3: ≥ 0.65 acceptance at every depth ≥ 12. No change is justified. |
| **C5** | Condition-level validity denominator | "all 20 preregistered primary families were successfully generated" | "all **accepted** families (at least `n_acc_min`) are eligible and exact-preserving" (§7) | §2.2: infeasible families are never replaced, so a 20/20 generation clause is unreachable. |
| **C6** | Seeds | `SEEDS_v001.json` | new `SEEDS_v002.json`, fresh blocks (§8) | v001 audit seeds are spent. |
| **C7** | Primary family count | 20 per depth | **30 per depth** | σ=0.9 is the low-resolution arm; 30 families improves dose-bearing yield without changing the construction or thresholds. |

Explicitly **not** changed: C-MASK, q grid 0–0.4 (no q=0.5), σ ∈ {0.8, 0.9}, M_min, density band, PENALTY, C-LABEL (still out of scope), N1–N4, A0, Z0, C1, E1/E2 criteria, strict exactness, map-first verdict structure, symbol hygiene.

---

## 4. Dose-delivered families and PG5 [RATIFIED]

### 4.1 Structure-only definition

For an accepted family \(i\) at σ, with skeleton mirror variates \(u\) and mask permutation π:

\[
D_i=\{\ell: u_\ell\ge\sigma\},\quad C_i(q)=\frac{|M_q\cap D_i|}{|D_i|}\ (\text{undefined}\to0\text{ if }D_i=\varnothing),\quad
\text{dose-delivered}\iff \max_q C_i(q)>0.
\]

Only skeleton and mask enter (P4). Recall, EI, survival and every solver output are excluded. The rule is applied after family acceptance and before any solve beyond baseline.

Note this is strictly stronger than "\(|D_i|\ge1\)": a family can have \(|D_i|>0\) and still deliver no dose if no distinguishing layer enters the nested mask within q ≤ 0.4.

### 4.2 PG5a — panel informativeness

A panel \((σ,d)\) is **dose-informative** iff the number of dose-delivered accepted families is at least `n_dose_min`. `n_dose_min = 6`, frozen from the design-only dose-delivery probabilities and the decision to use 30 audit families. It is not derived from recall or preservation outcomes.

### 4.3 PG5 — dose-response

For each dose-informative panel, with families restricted to the dose-delivered set \(\mathcal F_\text{dose}\):

\[
T_C=\sum_{i\in\mathcal F_\text{dose}}\sum_j (C_{ij}-\bar C_i)(r_{ij}-\bar r_i)
\]

where \(r_{ij}\) is recall of family \(i\) at q-level \(j\) (population A, successfully generated cells). Null: permute the **within-family assignment of C values to recall values**, preserving missingness; 100,000 Monte Carlo permutations, a dedicated `trend_permutation_seed` in `SEEDS_v002.json`. One-sided \(T_C>0\).

Families outside \(\mathcal F_\text{dose}\) are excluded because \(C_{ij}\) is constant in them, so they carry no manipulation (their contribution to \(T_C\) is exactly zero anyway; excluding them only makes the panel count honest). Within a dose-delivered family, tied C values at different q are kept as ties. `DOSE_FREE_FAMILY` cells stay in population A and in all other analyses.

**PG5 passes** iff (a) **both** d=14 audit panels (σ=0.8 and σ=0.9) are dose-informative and (b) both have one-sided \(p<0.10\).

- (a) fails → `CLOSED_PRE_PRIMARY — DOSE_NOT_RESOLVED` (**closing** design-resolution verdict; distinct from a sign or coupling failure).
- (b) fails → `CLOSED_PRE_PRIMARY — COUPLING_NOT_INDUCED`.

The nominal \(p<0.10\) threshold is carried over unchanged from v001.

### 4.4 Primary H1

Primary H1 uses the same \(T_C\) on \(\mathcal F_\text{dose}\) for each of the six \((σ,d)\) panels, Holm-corrected at α = 0.05 over the panels that are dose-informative. A panel that is not dose-informative is recorded `PANEL_DOSE_UNRESOLVED`, reported descriptively, and counts as **not** supporting `COUPLING_LAW_CANDIDATE` (it is not silently dropped from the claim). Recall versus nominal q is still reported descriptively.

---

## 5. Gates [RATIFIED]

| Gate | v002 status |
|---|---|
| PG1, PG2, PG4, PG6, PG7, PG8, PG9 | unchanged from v001 §10 (including closure statuses) |
| PG3 | unchanged text: common-attempt acceptance ≥ 0.5 at each audit depth (64 attempts). With one audit depth (d=14) a failure of this gate records `INFEASIBLE_CONDITION` for that depth, no replacement grid. Pilot expectation ≈ 0.70 **[PILOT]**; re-measured in preflight with the real engine. |
| PG5a | new: dose-informative panels (§4.2) |
| PG5 | replaced: realized-C trend on dose-delivered families (§4.3) |

PG9 (informative band) now reads over d=14 audit conditions.

Audit outcomes still cannot add q = 0.5 or σ = 0.95, change M_min, the density band, thresholds, nulls, or the cap. Any such change needs `SCR_III_COUPLING_SPEC_v003`.

---

## 6. Design grid and seeds [RATIFIED]

| Factor | v001 | v002 |
|---|---|---|
| audit depths | 10, 12 | **14** |
| audit q | d10: 0–0.3; d12: 0–0.4 | 0, 0.1, 0.2, 0.3, 0.4 |
| audit families | 12 per depth | **30** |
| primary depths | 14, 16, 18 | 14, 16, 18 |
| primary families | 20 | **30** |
| σ / q grids | 0.8, 0.9 / 0–0.4 | unchanged |
| MAX_ATTEMPTS | 64 | 64 |

Audit at d=14 and primary at d=14 share a depth but use disjoint seed blocks and the same frozen design.

Planned primary cells: 900 main + 90 A0 + 90 Z0 = **1,080**, before infeasibility logging. Infeasible families are never replaced.

---

## 7. Verdicts: condition-level denominator [RATIFIED]

Cell-level verdicts unchanged. Condition-level **`VALID_STRUCTURAL_REDUCTION`** requires, for the condition's accepted family set \(A_c\):

1. \(|A_c|\ge n_{acc,min}=21\) of the 30 preregistered families; below it the condition is `UNDERPOWERED_CONDITION`;
2. every cell in \(A_c\) is exact-validity eligible (population V);
3. every cell in \(A_c\) is exact-preserving;
4. median \(R_{node}\ge0.25\); median \(G_{time}\ge1.10\).

The Clopper–Pearson interval over \(A_c\) is always reported with the number of infeasible families. `HIGH_RELIABILITY_REDUCTION` is ≥ 90 % of \(A_c\) exact-preserving with the same reduction/gain thresholds. It is not an exact-equivalence claim. `TRANSFER_CONFIRMED` unchanged. `COUPLING_LAW_CANDIDATE` unchanged except H1 is now the realized-C test of §4.4; `COUPLING_MAP_ONLY` and `CLOSED_PRE_PRIMARY` unchanged in form.

v001 §6.6 already indicates the strict exact tier is not expected to occur; this is unchanged and map-first stands.

---

## 8. Seed discipline [RATIFIED]

`SEEDS_v002.json` must be generated and checked by script to be disjoint from:

- SCR-I v003 and SCR-II v001/v002 explicit blocks;
- v001 audit seeds `2026111101–12`, `2026111201–12` (spent) and v001 primary seeds `2026112101–20`, `2026112201–20`, `2026112301–20` (never run, but reserved so no overlap can be argued either way);
- burned `9100000–9100029` and the pilot blocks `9212000–9212039`, `9214000–9214039`, `9216000–9216039`, `9218000–9218039`.

Whole-family calibration/holdout split for E1/E2 (first 5 families per depth = calibration) is unchanged (P7). Note: E1 calibration uses accepted families; with infeasible first-five families the calibration set can shrink, so the split is defined on accepted families in seed order (first 5 accepted = calibration, remainder = holdout).

---

## 9. What v002 can and cannot show

Unchanged from v001 §14: a ruler with ground-truth coverage, estimator validation, and the counting predictions; not that any UNNS grammar is coupled to a real target. Additionally: v002 says nothing about whether v001's closure would have been reversed had a different seed block been drawn; v001 stands as `CLOSED_PRE_PRIMARY`.

---

## 10. Frozen execution sequence [RATIFIED]

1. Ratify this specification.
2. Write and freeze `SCR_III_STRUCTURE_v002.md`, `SCR_III_PREREG_v002.md`, `SEEDS_v002.json`, and the v002 source/design hash records.
3. Build **additive** `SCR_III_ENGINE_v002` runners and analysis modules. v001 engine files and v001 outputs are not overwritten.
4. Before the audit, run the **acceptance-only real-engine preflight** on dedicated burned v002 preflight seeds at d=14/16/18. It may inspect only common-attempt acceptance, baseline multiplicity, free-subspace density, attempt index/count, and deterministic provenance. It may not call `solve_scr`, compute recall/EI, or inspect target survival.
5. The preflight remeasurement is diagnostic and frozen: it cannot change MAX_ATTEMPTS=64, q, σ, M_min, density band, thresholds, seed counts, or any verdict rule. Its results are recorded even if poorer than the shim pilot.
6. Run the d=14 audit on its independent 30-family seed block.
7. Freeze the audit. Primary is authorized only if no closing audit gate fails.
8. Run the independent d=14/16/18 primary seed blocks, then nulls/estimators/consolidation.

### Real-engine acceptance preflight reporting

For each of d=14,16,18, report accepted families out of 30 under the frozen 64-attempt common-attempt rule. Also report median accepted-attempt index and the full accepted/infeasible seed list.

- Acceptance < 0.50 at any depth is flagged `LOW_COMMON_ATTEMPT_ACCEPTANCE`.
- Fewer than 21/30 accepted preflight families at a depth is flagged `STRICT_VALIDITY_POWER_RISK`.
- These preflight flags **do not tune or replace the design and do not by themselves convert a primary condition into a pass or fail**. Audit PG3 remains the formal d=14 audit gate; actual primary accepted counts determine `UNDERPOWERED_CONDITION`.
- No preflight seed may appear in audit or primary.

The immutable C-MASK generator, frozen grammar/filter/solvers, controls, metrics, and estimator logic remain hash-locked. v002 executable changes are limited to the new acceptance-only preflight runner, PG5a/realized-C trend logic, v002 audit grid/seed handling, and accepted-family condition verdict logic.

The stale non-root `scr_iii\SCR_III_COUPLING_SPEC_v001.md` is not canonical and should be deleted locally. The canonical v001 specification remains at the project root.

---

## 11. Risks I see

- **σ=0.9 is a low-resolution arm.** Even at d≥14 about half its families deliver no dose and most of the rest have one jump in C. Expect weaker H1 power there. If this matters, the fix is σ-level design, not a threshold change; see O-D6.
- **Infeasible families bias the sample** toward arithmetic draws that satisfy the density band at every q. This was already true in v001; v002 reports it rather than hiding it.
- **Retrospective motivation.** v002's PG5 repair is motivated by an observed closure. The protections are: fresh seeds, thresholds justified from design-only tables, no q/σ/constant changes, and a preregistered closure path (`DOSE_NOT_RESOLVED`) that still lets the audit fail.
- **Pilot used a shim engine** (§2.3 caveat).

---

## 12. Ratified decisions

| # | Decision | Frozen v002 choice |
|---|---|---|
| **O-D1** | `n_acc_min` for condition validity | **21 accepted families of 30**; below this, `UNDERPOWERED_CONDITION` |
| **O-D2** | `n_dose_min` for a dose-informative panel | **6 dose-delivered accepted families** |
| **O-D3** | Audit panels required informative | **both d=14 panels**, σ=0.8 and σ=0.9 |
| **O-D4** | Primary families per depth | **30** |
| **O-D5** | Audit families at d=14 | **30** |
| **O-D6** | Add σ=0.7 arm | **No**; retain σ ∈ {0.8,0.9}. Any lower-σ study requires a later specification. |
| **O-D7** | Audit depth | **d=14 only** |
| **O-D8** | `DOSE_NOT_RESOLVED` | **Closing** pre-primary verdict |

Additional frozen implementation discipline:

- MAX_ATTEMPTS remains 64.
- q remains {0.0,0.1,0.2,0.3,0.4}.
- C-MASK, M_min=4, density band 0.02–0.04, PENALTY, controls, populations, E1/E2 criteria, strict exactness, and map-first posture are unchanged.
- The acceptance-only real-engine preflight uses dedicated burned seeds and cannot tune the design.
- v002 implementation is additive; v001 engine scripts/results remain reproducible and untouched.

These decisions are closed for v002. Any scientific change requires `SCR_III_COUPLING_SPEC_v003`.

---

## 13. Changelog v001 → v002

- Status: `RATIFIED_SPEC` (v001) → `RATIFIED_SPEC` (v002; new version, v001 remains frozen).
- PG5: nominal-q trend → realized-C trend on structure-only dose-delivered families; new PG5a informativeness gate; new closure status `DOSE_NOT_RESOLVED`.
- Audit: d=10,12 → d=14 (**30 families**).
- H1: realized-C test with Holm over dose-informative panels; uninformative panels recorded, not dropped.
- Validity denominator: fixed 20 generated → accepted families with `n_acc_min=21` of 30.
- Seeds: new blocks; four pilot blocks and v001 spent/reserved blocks excluded.
- Unchanged: C-MASK, q-grid, σ, M_min, density band, PENALTY, cap 64, controls, populations, E1/E2 criteria, exactness, map-first posture.

- Primary family count: 20 → **30 per depth** (1,080 planned cells including A0/Z0).
- Added dedicated real-engine acceptance-only preflight seed blocks at d=14/16/18; no outcome inspection and no tuning authority.

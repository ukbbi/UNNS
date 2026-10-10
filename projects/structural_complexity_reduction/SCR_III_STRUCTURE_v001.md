# SCR_III_STRUCTURE_v001

**Project:** Structural Complexity Reduction (SCR)  
**Phase:** SCR-III-A — Coupling Threshold and Valid Reduction  
**Status:** `FROZEN_STRUCTURE`  
**Frozen:** 2026-10-08  
**Scientific basis:** `SCR_III_COUPLING_SPEC_v001` (`RATIFIED_SPEC`)

## 1. Purpose

SCR-III-A is the controlled coupling-ruler phase between the two frozen endpoints already established:

\[
\text{SCR-I: structurally aligned target}
\rightarrow
\text{compression with basin/class preservation}
\]

and

\[
\text{SCR-II v002: independent dense arithmetic target}
\rightarrow
\text{extreme contraction with exact-target destruction}.
\]

SCR-III-A does not attempt to prove that a real UNNS grammar is coupled to a real target. It constructs a benchmark with declared shared generative cause, varies that coupling in a controlled way, and measures the reduction–preservation frontier.

## 2. Frozen retrospective addendum to SCR-II v002

No frozen SCR-II file is edited.

The following interpretation is carried forward:

> SCR-II v002's non-transfer result is correct and remains frozen. It was additionally forced by counting: the grammar-admitted set was smaller than the exact target set in every primary cell. Therefore v002 established that large contraction with an independent dense target cannot preserve the exact target set, but it could not distinguish "uncoupled" from "coupled but capacity-inadequate." The transfer-boundary condition remains necessary, not sufficient.

This addendum is interpretive only. It does not alter `PRIMARY_RESULT_v002.json`, the v002 freeze record, hashes, or verdict.

## 3. Frozen-branch discipline

The following are read-only:

```text
SCR_I_PREREG_v003/
scr_ii/
archive/
```

No SCR-III script may overwrite, patch, rename, or regenerate any frozen SCR-I/SCR-II artifact.

All new implementation lives under:

```text
scr_iii/
```

GitHub remains publication/reference only after local validation and freeze.

## 4. Canonical SCR-III layout

```text
structural_complexity_reduction/
│
├─ SCR_III_COUPLING_SPEC_v001.md
├─ SCR_III_STRUCTURE_v001.md
│
├─ scr_iii/
│  ├─ README.md
│  │
│  ├─ SCR_III_PREREG_v001/
│  │  ├─ SCR_III_PREREG_v001.md
│  │  ├─ SEEDS_v001.json
│  │  ├─ SOURCE_LOCK.md
│  │  ├─ METRICS.md
│  │  ├─ NULLS.md
│  │  ├─ DECISION_RULES.md
│  │  ├─ MANIFEST.md
│  │  ├─ SHA256SUMS.txt
│  │  ├─ config/
│  │  │  └─ prereg_v001.json
│  │  ├─ schema/
│  │  │  ├─ route_csp_c_v001.schema.json
│  │  │  └─ result_v001.schema.json
│  │  └─ scripts/
│  │     ├─ validate_prereg.py
│  │     ├─ hash_freeze.py
│  │     └─ RUN_VALIDATE.bat
│  │
│  ├─ generator/
│  │  └─ route_csp_c_v001.py
│  ├─ nulls/
│  │  └─ controls_v001.py
│  ├─ analysis/
│  │  ├─ metrics_v001.py
│  │  ├─ trend_test_v001.py
│  │  └─ estimators_v001.py
│  ├─ tests/
│  │  ├─ test_source_lock.py
│  │  ├─ test_seed_separation.py
│  │  ├─ test_stream_separation.py
│  │  ├─ test_family_pairing.py
│  │  ├─ test_filter_firewall.py
│  │  ├─ test_schema.py
│  │  └─ test_controls.py
│  ├─ scripts/
│  │  ├─ RUN_AUDIT.bat
│  │  └─ RUN_PRIMARY.bat
│  └─ output/
│     ├─ audit/
│     ├─ primary/
│     ├─ nulls/
│     ├─ estimators/
│     └─ reports/
│
├─ SCR_I_PREREG_v003/        # frozen
└─ scr_ii/                    # frozen
```

The exact implementation may add helper modules inside `scr_iii/`, but it may not alter the scientific interfaces, grids, seed blocks, metrics, null definitions, or verdicts frozen in the preregistration.

## 5. Scientific objects

SCR-III-A keeps three objects separate:

\[
G = \text{frozen structural grammar/filter},
\]

\[
T = \text{independently solved arithmetic target},
\]

\[
C = \frac{|M\cap D|}{|D|}
= \text{realized ground-truth coverage in the synthetic ruler}.
\]

The imposed dose q is not itself the measured coupling result. q defines the nested mask; C records how much of the structurally distinguishing support was actually covered.

Target survival is measured after construction and is never used to accept an instance.

## 6. Construction boundary

The v001 benchmark is `ROUTE_CSP_C v001` using the ratified C-MASK design.

Unchanged imports from SCR-II v002:

- Γ_route v001, G1→G4 in the same order;
- structural filter;
- baseline exact solver;
- SCR solver;
- solver-native C1 solver.

SCR-III adds only:

- σ-controlled structural degeneracy;
- q-controlled nested coupling mask;
- family-level shared arithmetic attempt;
- SCR-III metadata/schema;
- controls and estimators required by the preregistration.

## 7. Population doctrine

SCR-III distinguishes:

**Population A — all accepted cells:** used for the coupling ruler, recall, EI, exact-preservation probability, reduction and cost maps.

**Population V — exact-validity eligible:** cells satisfying both \(L\ge m\) and \(R_{leaf}\ge0.25\).

Exact-infeasible or weak-reduction cells remain scientifically visible in Population A. They are not silently dropped from the coupling curve.

## 8. Verdict doctrine

Preservation remains first.

Cell order:

```text
INVALID_RUN
→ PRESERVATION_FAIL
→ NO_MATERIAL_REDUCTION
→ REDUCTION_WITHOUT_NET_GAIN
→ VALID_STRUCTURAL_REDUCTION
```

Condition-level `VALID_STRUCTURAL_REDUCTION` is strict: all 20 preregistered primary cells must be generated, validity-eligible, exact-preserving, and meet the frozen reduction/gain thresholds.

A separate `HIGH_RELIABILITY_REDUCTION` label may describe ≥18/20 exact-preserving cells but is not an exact-equivalence claim.

Study-level map output is valid even if no exact-valid condition exists.

## 9. Anti-tuning rule

SCR-III-A v001 is explicitly a **map-first** study.

After audit begins, v001 may not:

- add q = 0.5;
- add σ = 0.95;
- relax the multiplicity floor;
- widen the density band;
- swap the C-MASK construction;
- change estimator thresholds;
- change primary seeds;
- redefine validity.

Any such change requires a new coupling specification and preregistration version.

## 10. Estimator boundary

SCR-III-A validates **SCR applicability estimators**, not a magical label-free measurement of physical coupling.

- E1 may use the preregistered five-family calibration subset and then predicts held-out families.
- E2 may use a charged sample of subtrees from the instance being predicted; its compute cost is reported.

Neither estimator may inspect the held-out instance's complete target set before prediction.

## 11. UPI

UPI/H-UPI remains outside SCR-III-A primary analysis.

It may return in SCR-III-B as a blinded explanatory diagnostic after the physical benchmark grammar and target protocol are frozen.

## 12. Execution order

```text
RATIFIED_SPEC
→ FROZEN_STRUCTURE
→ FROZEN_PREREG
→ BUILD_ENGINE
→ PREFLIGHT
→ AUDIT
→ AUDIT_FREEZE
→ PRIMARY
→ CONSOLIDATE
→ FREEZE
```

No primary run is authorized before all preregistered audit gates pass.

## 13. Next implementation artifact

After `SCR_III_PREREG_v001` is locally frozen and its hashes recorded, build:

```text
SCR_III_ENGINE_v001
```

The engine must implement the preregistration; it must not redesign it.

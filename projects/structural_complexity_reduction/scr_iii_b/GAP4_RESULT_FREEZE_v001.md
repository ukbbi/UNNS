# GAP4_RESULT_FREEZE_v001 — SCR-III-GAP-4X4

**Record date:** 2026-10-10  
**Classification:** Additive scientific result freeze; prior prediction, source, instance, outputs, and audits remain unchanged.  
**Final registered result:** `GAP_CONSISTENT / DELTA4_LT_1_CONFIRMED` **for the specified finite 40-spin v005 physical model**, based on the certification audit stated below.  
**Scope:** A prospective, finite-size, model-conditional exclusion-gap test. **Not** a universal gap law, independent physical experiment, transfer (T) result, or UNNS-specific computational speedup claim.

## 1. Prediction chronology and frozen decision rules

The source `GAP4_v010/PREDICTION_FREEZE_v001.md` locked the following **before the real 4×4 energy evaluation**:

1. **R2 range:** δ₄ ∈ **[0.790439676056526, 1.0333534753990623]**, endpoints inclusive.
2. **Separate directional prediction:** **δ₄ < 1**; equality fails.

Here δ₄ = [min_{s outside G} H(s) − min_s H(s)] / (k_B × 792 K), for the full frozen 40-spin free-boundary Hamiltonian with 16 constrained vertices. The gap-level degeneracy is descriptive, not a graded prediction. The prediction freeze was recorded before the instance and original optimization output; neither prediction was revised afterward.

## 2. Verified computational outcome

| Quantity | Frozen value |
|---|---:|
| Real instance | 4×4 square ice, 40 spins, 16 constrained vertices |
| Nominal configuration space | 2⁴⁰ = 1,099,511,627,776 |
| Global E₀ (A units) | −0.16364841082886986 |
| Global minimizing witness ID | 711243241830 |
| Ground search nodes | 700,405 |
| Lowest non-grammar energy (A units) | −0.1534031680911189 |
| Non-grammar minimizing witness ID | 161487427942 |
| Non-grammar search nodes | 1,316,073 |
| Exclusion gap Δ_nonG (A units) | **0.01024524273775096** |
| Normalized exclusion gap δ₄ | **0.9459172223430824** |

Both original searches reported `completed: true`. The freshly compiled v010 binary reproduced `GAP4_FIRST_RUN.jsonl` **byte for byte**, including witness IDs, energies, node counts, and completion flags. The first optimization was performed after the prediction was fixed, with the procedural deviations documented separately.

**Formal separate verdicts:**

- **R2: `GAP_CONSISTENT`** — δ₄ is within the locked range, with a nearest-edge margin of ≈ 0.0874363.
- **Directional: `DELTA4_LT_1_CONFIRMED`** — 1 − δ₄ ≈ 0.0540828. For the registered inclusive 1 k_BT + τ energy window, exact physical target preservation by the ice-rule grammar consequently **fails** for this model.

These are *two distinct adjudications*. The R2 result is consistency with a size-insensitive local exclusion scale, not proof of convergence or a universal law.

## 3. Witness verification and optimization certification

The supplied `GAP4_CERTIFICATION_AUDIT_v001.md` and machine-readable audit report establish the following technical basis:

- Ground witness: direct geometric ice-rule check finds **zero** violations across 16 vertices; non-grammar witness: **one** violation, at vertex 3 (geometric charge −2), independently of serialized vertex masks.
- Stored-coupling witness energies independently recomputed with exact-rational arithmetic agree with reported solver energies to approximately 4×10⁻¹⁷ A units; direct charge-position energy agrees with the K-model calculation to relative ≈ 2.3×10⁻¹⁵.
- All **780** frozen-model couplings and all **16** incidence masks were checked against the geometry. Coupling precision changes the gap by at most ≈ 9.44×10⁻¹⁶ A in the stated model comparison.
- The branch-and-bound lower-bound inequality and permissive non-grammar-violation filter were reviewed analytically. Independent exhaustive small-instance tests matched the public 1×1–3×3 minima and exclusion gaps (3×3 discrepancy ≈ 5.55×10⁻¹⁷ A).
- An all-prefix 2×2 rational-arithmetic recheck found no negative bound slack. **Audit discrepancy disclosed:** the first floating-point 2×2 JSON reported `bound_admissible: false` from ≈ −3.47×10⁻¹⁷ numerical roundoff; the original JSON remains unchanged and is explicitly superseded on that point by `RATIONAL_RECHECK_OUTPUT.txt`. The separately sampled 3×3 prefixes passed.
- Binary128 shadow re-evaluation of **1,008,197** actual 4×4 bound-prune events reported **zero unsafe decisions**; 15 violation-filter prunes had zero popcount mismatches.
- IEEE-754 round-to-nearest standard-model rounding analysis estimates ≤ 3.16005×10⁻¹⁴ A combined required pruning protection against the v010 guard of **1×10⁻¹¹ A** (≈ **316×** margin). This is a mathematical error analysis with independent shadow checks, **not directed-rounding interval arithmetic or a machine-checked proof certificate**.

Collectively these justify the result's `GAP_CONSISTENT` grade **under the project's accepted certification method** while accurately retaining its numerical and model-dependence limitations.

## 4. Execution deviations — explicitly retained

`GAP4_DEVIATION_v001.md` remains the authoritative additive deviation record. The planned large synthetic feasibility campaign and protected-real-instance fingerprint step were not completed prospectively; the direct real 4×4 run occurred before the final certification audit. The earlier exploratory verdict was `GAP_INCONCLUSIVE`, correctly pending that audit. These omissions are **not retroactively relabeled as completed**. The present record upgrades the verdict only on the later mathematical/witness/reproducibility evidence; it does not erase the deviations.

The original locally compiled executable's build environment was unavailable to the audit host, but a fresh hash-recorded build of the **unchanged source** produced byte-identical outputs. Execution guard and public 1×1–2×2 tests had already passed on the user's Ubuntu/WSL installation. The broader physical Hamiltonian derives from the common v005 source, not an independently reproduced original Dryad simulator.

## 5. Provenance and exact SHA-256 fingerprints

| Immutable input or supporting artifact | SHA-256 |
|---|---|
| `GAP4_v010/PREDICTION_FREEZE_v001.md` | `7d8e8ac5f12903c0712643afc4a3668211ee81357a3a554dc6082c3afbdb5947` |
| `GAP4_v010/solver_v010.cpp` | `d56cf6d38a1622134359726c3ef56fd09066bc4ba27b2f167361c21574d5dd44` |
| `GAP4_v010/output/real_4x4.txt` | `3d47ed1256da7620292a5fe4c64e0bc226b9836768ac87df0ff4fdbf91c5f7a2` |
| `GAP4_v010/output/GAP4_FIRST_RUN.jsonl` | `94bc7eebec0476217a9b688408123cdd6f9f047d7ec742ba84ff4902b1ed3680` |
| `GAP4_DEVIATION_v001.md` | `d4c398e064d635fea9c95b05d7a451f7f68ae5352053542ff2f27a1e56066a73` |
| `GAP4_CERTIFICATION_AUDIT_v001.md` | `f9cd7179c34509aa8161673039ba1ac91332bd5d367a062d0a8c1f8fce651c89` |
| `GAP4_AUDIT_RESULT_v001.json` | `0bb435fa5e18577a7a2356532437a50895a4fdaed884c14d9836162f317c0d20` |
| `RATIONAL_RECHECK_OUTPUT.txt` | `2d2e8a440df138ece6722ffbd06071a6fe00b4c9a9c75374d14029bbaf56e13c` |
| `MANIFEST_GAP4_AUDIT_v001.json` | `86bbbf5873fe59ab5f0c4057c45427bb58c27ff14d3d05c917607183d4813d24` |
| Fresh-build `solver_v010_fresh` executable (audit host) | `304083775bcb5d2cdfd54a1f5dc222cf9a23138c841156db88a351b3054c46be` |

The certification ZIP is `GAP4_AUDIT_v001(1).zip`, containing its own audit manifest and environment record; that manifest itemizes further script and shadow-log fingerprints. The original and fresh result output share the identical SHA-256 above.

## 6. Scientific limits and no further execution authorization

This is a **certified computational result within the documented numerical-certification framework for a specific finite Hamiltonian**, not an experimental measurement or an independent validation of that physical model. The 4×4 gap lying near those of 2×2 and 3×3 supports a finite-size recurrence hypothesis but does not establish an asymptotic limit. The search-node reduction is a branch-and-bound result and is not attributed to distinctive UNNS complexity reduction without comparative controls. Degeneracy of the first excluded level has not been exhaustively counted.

This freeze **authorizes no additional physical runs**, no 5×5 or 6×6 computation, and no changes to the 4×4 instance, frozen prediction, original output, v005–v009, SCR-III-B primary result, or GitHub. Any follow-up must use a separately frozen question and authorization. Keep this file adjacent to the GAP4 audit materials as a standalone additive scientific record.

**FINAL STATE:** `GAP4_RESULT_FROZEN / GAP_CONSISTENT / DELTA4_LT_1_CONFIRMED / MODEL_CONDITIONAL / NO_NEW_EXECUTION_AUTHORIZED`.

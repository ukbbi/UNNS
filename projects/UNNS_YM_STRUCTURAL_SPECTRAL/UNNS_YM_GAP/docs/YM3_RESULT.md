# YM3_RESULT.md

## UNNS Yang–Mills Gap / Vacuum Boundary Non-Crossability
### YM-3A Common Refinement Result Record

**Project:** `UNNS_YM_GAP`  
**Preregistration:** `YM3-PREREG v0.1.0`  
**Frozen chamber:** CORR-I v0.1.2  
**Evidence class:** C — exact mass-anchored model controls  
**Verdict:** **MODEL-REFINEMENT PERSISTENT**

## 1. Execution integrity

- Frozen chamber SHA-256: `f972c9d460cebc19ef165e66c03f971411062eba093876406ed2efe614e2deb2`
- Chamber hash matches preregistration: **True**
- β=6.50 construction checksum: **PASS** (from frozen input-build record).
- Full primary sequence was interpreted only after all eight massive and all forty matched controls were generated.
- All 40 matched Gamma controls are `POSITIVE-SPECTRAL CONSISTENT`, Hankel/Hausdorff consistent, and pass the α=0 identity null.
- All 40 matched Gamma controls remain without a stable constant-mass plateau, as expected for this gapless family.

## 2. Primary common-grid results

| β | R_massive | R_p8 matched | S_fixed | S_match | matched ordering |
|---:|---:|---:|---:|---:|---|
| 5.6924 | 0.018555950 | 0.041575147 | 0.708018 | 0.806712 | PASS |
| 5.80 | 0.012377229 | 0.040155639 | 1.112950 | 1.176904 | PASS |
| 5.8941 | 0.010214250 | 0.039233825 | 1.305025 | 1.345755 | PASS |
| 5.99 | 0.008840082 | 0.038463073 | 1.449513 | 1.470402 | PASS |
| 6.0625 | 0.008297253 | 0.038107768 | 1.512884 | 1.524494 | PASS |
| 6.235 | 0.007949606 | 0.037862577 | 1.555686 | 1.560841 | PASS |
| 6.3380 | 0.007984751 | 0.037888030 | 1.551275 | 1.557102 | PASS |
| 6.50 | 0.007687649 | 0.037667921 | 1.589194 | 1.589194 | PASS |

The fixed-reference margins use the exact frozen YM-2 `p=8` contraction ratio `0.03766792061795015`; the rounded preregistration table value `0.037668` is display-only.

## 3. Native-grid window diagnostic

| β | R_native | S_fixed_native |
|---:|---:|---:|
| 5.6924 | 0.000015665 | 7.785104 |
| 5.80 | 0.000034492 | 6.995831 |
| 5.8941 | 0.000101106 | 5.920395 |
| 5.99 | 0.000253379 | 5.001677 |
| 6.0625 | 0.000488523 | 4.345177 |
| 6.235 | 0.001858549 | 3.009013 |
| 6.3380 | 0.003589464 | 2.350806 |
| 6.50 | 0.007687649 | 1.589194 |

The native-lattice branch is a window-sensitivity diagnostic only. No unpreregistered native matched-Gamma family was introduced.

## 4. Frozen-rule checks

- All eight primary massive baselines valid: **True**
- `S_fixed > 0` at all eight β: **True**
- `S_match > 0` at all eight β: **True**
- Matched ordering `R0.5 > R1 > R2 > R4 > R8 > Rmassive` at all β: **True**
- Native fixed-reference hard margin positive at all β: **True**
- Primary/native qualitative incompatibility: **False**

## 5. Stage interpretation

Under the preregistered Class C experiment, the massive-side CORR-I signature remains separated from both the fixed hardest gapless reference and every β-matched hardest gapless control across all eight AT20 refinement levels. The full matched Gamma ordering is retained at every level, and the native-grid diagnostic does not reverse the separation.

> **The massive-side CORR-I signature is persistent across the AT20 mass-anchored Class C refinement sequence.**

## 6. Claim boundary

This result concerns the **Class C mass-anchored model family**. It does not establish eight-level refinement stability of measured Yang–Mills correlators, a continuum theorem, a Hamiltonian spectral lower bound, or the Yang–Mills mass gap. YM-3B remains dependent on additional Class A/B information.

# SCR-IV v001 — Certification status

**Date:** 2026-10-10 · **Toolchain:** Lean 4.34.1 (commit 5045d0056413), Lake 5.0.0, core only (no Mathlib) · **Built and run in:** Claude's Ubuntu 24.04 cloud container, **not yet in your WSL**. Run `bash RUN_TEST.sh` there to produce your own log.

| Stage | Verdict | Basis |
|---|---|---|
| IV-1 | **MODEL_FORMALIZED** (with the scope below) | `RUN_TEST.sh` stages 1–4 pass; logs in `output/` |
| IV-2 | **WITNESSES_CERTIFIED** | 25 kernel-checked theorems; axiom audit clean |
| IV-3 | PENDING | `SCR_IV_Bound.lean` is a stub: no theorem, no `sorry`, no axiom |
| IV-4 | PENDING | not started; no certificate generated |
| IV-5 | PENDING | not started |

Passing IV-1/IV-2 implies nothing about IV-3 to IV-5. **No global-optimality or finite-gap claim is made here.**

## What the Lean kernel has checked (`decide +kernel`; no `native_decide`)
- 40-spin decoding (`bit i = 1 ⇔ s_i = +1`), 40-bit ID validity, and injectivity of decoding on valid IDs (a real proof).
- The frozen vertex table: 16 vertices, each mask has exactly 4 islands, each plus-in mask 2 islands and lies inside its mask, masks distinct, every island covered by 1–2 vertices.
- Coupling table shape: 40 rows, row *i* has 39−*i* entries, 780 total. Energy is evaluated by two differently written functions (`hScaled`, `hIndexed`) that agree on both witnesses.
- Ground witness 711243241830: valid; in the grammar; all 16 vertices have 2 inward arms; exact energy −193201942568284180326 / 2⁷⁰ A.
- Non-grammar witness 161487427942: valid; not in the grammar; exactly 1 violated vertex, index 3; vertex counts `[2,2,2,1,2,…]`; exact energy −181106494839879484608 / 2⁷⁰ A.
- Both exact energies lie within 1e-16 A of the reported solver doubles (audit-observed ~4e-17).
- The witness ordering H(ground) < H(non-grammar), and the **witness-level** normalised gap lies in (0.9459172, 0.9459173) with A(792 K) taken as the exact frozen double and k_B·792 K = 1093474008/10²⁹ J. This evaluates two states only; it is *not* δ₄.
- Axiom audit: every theorem depends only on `propext`, `Classical.choice`, `Quot.sound`; no `sorryAx`, no `Lean.ofReduceBool`. Four negative controls (false claims) are rejected by the kernel for the right reason.

## Scope and limits of IV-1 (read before relying on it)
1. **Exact encoded model.** The theorems concern the finite Hamiltonian whose 780 coefficients are the exact dyadic rationals of the binary64 values read from `data/real_4x4.txt` (sha256 3d47ed12…). Provenance: text token → binary64 (correctly rounded) → `as_integer_ratio`; the token, bit pattern and numerator of every coefficient are in `data/coeff_bits.csv`. Lean cannot hash files or parse the text; `RUN_TEST.sh` stage 1 regenerates `SCR_IV_Data.lean` from the instance and compares byte-for-byte. That check is a script, not a kernel check.
2. **Not an interval-enclosed physical model.** No claim is made that these coefficients equal the physical couplings. The SCR-III audit (Python, 60-digit decimal, not Lean) found the doubles differ from the source formula by Σ|ΔK| = 4.7e-16 A, so a gap could shift by at most 9.4e-16 A. That bridge is not formalised.
3. **Grammar convention.** Lean defines the vertex predicate exactly as the frozen solver does (island points inward iff `(s_i = +1) == plusIn bit i`). Agreement with the geometric ice rule is *evidenced*, not proved in Lean: kernel-checked per-vertex counts match the independent audit's recorded counts for both witnesses, and `scripts/diff_test.py` compares Lean against the geometric rule of the frozen v005 module (copied unchanged to `data/provenance/`, sha 3364d552…) and exact Python energies on 504 configurations (0 mismatches; violation counts 0–15 exercised).
4. **Not repeated:** no physical optimisation, no 2⁴⁰ enumeration, no frozen file modified.

## Not in this package
`SCR_IV_Core.lean` and your Mathlib-based `SCR_IV_v001` project were not available to this session, so nothing here imports them; this package is standalone and core-only. Merge into your project by copying the `SCR_IV_*.lean` files (except any name clash) and the `lakefile.toml` `[[lean_lib]]` entry.

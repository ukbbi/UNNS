# E2-P3 — Proof obligations (what is discharged, what is not)

| # | Obligation (spec §) | Status | Where |
|---|---|---|---|
| O1 | Coverage-Gap Reduction (§4) | discharged (elementary) | THEOREMS P3-T0 |
| O2 | Normal-form reduction of a planar target to Γ_{d,s} with explicit box transformation (§5.2.1–3) | discharged | P3-L1 + exhaustive period check per row |
| O3 | Apply v005/v007/v010/v012 hypotheses, remove inherited hull-covered cases (§5.2.4–5) | discharged (applied, not re-proved) | P3-C1, results/P3_PLANAR.json |
| O4 | Construct target uncovered regions exactly (§5.2.6) | discharged for every classified row | `gap_decomposition`, hull-cover trees (independently verified for controls and stored rows) |
| O5 | CP3-A: residual planar containment for Λ ⊊ Λ′, **general** (§5.1, 5.3) | **OPEN** for d′ ≥ 2 targets that are hollow-box or sub-threshold. Proved for rectangular targets (d′ = 1) | P3-T3(e); finite exact audit otherwise |
| O6 | CP3-A counterexample obligation (§5.4) | not triggered: no planar counterexample in scope | results/P3_COUNTEREXAMPLES.json |
| O7 | Exact noncontainment and containment certificates with strict-boundary handling, independent replay, tamper rejection (§7) | discharged | exact_containment.py / certificate_check.py / tests / RUN_VERIFY V02 |
| O8 | Essential three-coordinate obstruction: coordinate support, affine dimension, face-irreducibility (§6.2) | computed for every witnessed failure | coupled_3d.evaluate_3d |
| O9 | Obstruction between TWO nontrivial lattices realised by a valid FIELD-I transition (§6.1, 6.4) | see STATUS (3D_WITNESS_PASS or NO_WITNESS_IN_SCOPE) | results/P3_3D.json |
| O10 | P3-T1 finite obstruction templates for a declared family | proved for the even-sum family and for the short-vector necessity; **no general classification** | P3-T3(c),(h) |
| O11 | P3-T2 inaccessibility of uncovered regions | proved for rectangular targets (k = 2 unconditional; k = 3 only through 2-cells); **not** for hollow / sub-threshold d′ ≥ 2 targets | P3-T3 |
| O12 | P3-T3 higher-dimensional criterion | corner-cube criterion for rectangular targets (any k) | P3-T3(b)–(f) |
| O13 | P3-T4 predictor with assumptions, domain, complexity, comparison, unavailable cases | discharged for rectangular targets; unavailable otherwise (stated) | P3-T4, results/P3_3D.json |
| O14 | Prior-art / novelty comparison (§9 P3-E5) | done in P3_THEOREM_AUDIT.md; **no claim of C3** | results/P3_THEOREM_AUDIT.md |

Honest remainder: the unrestricted planar conjecture CP3-A for d′ ≥ 2 targets with Q_norm below threshold or equal to (d,d); a classification (not just a family) of 3D
obstruction lattices; and a FIELD-I realisation, if any exists, of an essential obstruction between two nontrivial lattices when the target is not rectangular.

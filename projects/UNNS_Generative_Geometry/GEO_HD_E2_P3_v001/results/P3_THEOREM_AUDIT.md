# E2-P3 — Theorem and novelty audit

| Item | Status | Novelty assessment |
|---|---|---|
| P3-T0 Coverage-Gap Reduction | PROVED | elementary reformulation (stated as such by the spec); not C3 |
| P3-L1 planar scaling reduction | PROVED | equals GEO-I v004 S1; re-proved because the classification depends on it; not new |
| P3-C1 G12-T8 inheritance | inherited | explicitly **not** a discovery |
| P3-T3 corner-cube criterion (rectangular targets, any k) | PROVED | elementary: it is the statement that the complex of Z^k minus its origin cell has complement an open corner cube, plus Graver-minimality arguments. New *as a statement about FIELD-I transport*, but standard polyhedral facts do the work. |
| P3-T2a planar rectangular-target containment | PROVED | corollary of T3(d),(f); resolves CP3-A for d′ = 1 only |
| P3-T3(h) even-sum family classification | PROVED | explains E2-P1/Control C as a family (smallest failing box (1,1,2)); elementary |
| P3-T4 corner-cube predictor | PROVED correct; evaluated | avoids target reconstruction, still needs the source Graver set; cheap necessary screen is sound |
| CP3-A for hollow / sub-threshold d′ ≥ 2 | **OPEN** | exact audit finds no counterexample in scope: 3127 residual rows (297 with nonempty target gap) |
| Essential 3D obstruction, both lattices nontrivial, FIELD-I | 3D_WITNESS_PASS | see report §5 |

**C3 decision: SCOPED_THEOREM_ONLY.**  Reasons: (i) every proved statement reduces to elementary lattice/polyhedral reasoning; (ii) the only arithmetic content is the rectangularity test Λ′ = ⊕ o_iZ and the short-vector necessity |v|₁ ≤ k−1, neither of which explains hollow or sub-threshold targets; (iii) the open residual class is exactly where an arithmetic law would be new.  Prior-art comparison: single-fibre coverage (GEO-I v005–v012) gives hull-coverage for stabilised planar targets; generic polyhedral-containment decision (Fourier–Motzkin/LP, disjunctive programming) gives fixed-pair decidability — E2-P3's certificates are an implementation of that, not a theory.

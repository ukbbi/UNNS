# E2-P3 — Source overlap (P3-E0)

Read-only sources: GEO-I v012 (`THEOREM_REGISTRY.tsv`, `MATHEMATICS.md` §0, §6), GEO-I v004 `theory/stabilization.py` (S1), E2-P1/E2-P2 packages, GEO-I v003/v004
(realization, embeddedness) as summarised in the project's SOURCE_OVERLAP_MATRIX (R13, R17, R26).  GitHub was not touched.

| Item | Source | Status | E2-P3 treatment |
|---|---|---|---|
| G12-T8: U = conv F for d ≥ 2, unit s, Q ≥ (d,d), Q ≠ (d,d); inherited G5-C1, G7-T1, G10-R1 | v012 §6 | PROVED+CHECKED | applied as hypothesis check; **inherited, not new** |
| Hollow box Q = (d,d) | v010 / v012 §6 | stands | classified RESIDUAL_EXCEPTIONAL_HOLLOW_BOX; not re-proved |
| Scaling reduction S1 | v004 stabilization.py ("PROVED by hand") | cited | **re-proved here** (P3-L1) because the classification depends on it |
| d = 1 (rectangular lattice): "U always contractible" | v004 G4-C1 | cited | transport containment for d′ = 1 is a different question: proved as P3-T2a |
| v004 embeddedness / obstruction templates | v004 | cited | different question (single-fibre embedding), not used |
| E2-P2 corrections (P2-T1 wording, P2-TF1(v) range) | E2-P2 assessment | recorded | ERRATA/E2_P2_ADDENDUM_001 |
| E2-P2 overlap with v012 (F21 for h ≥ 3, hole changes in P2-A/B) | E2-P2 assessment | recorded | ERRATA/E2_P2_ADDENDUM_002 |
| E2-P2 planar window defect (square [0,q_1]²) | found in E2-P3 | recorded | ERRATA/E2_P2_ADDENDUM_003; 0 verdicts changed |

**G12-T8 applicability test used.**  For the target (P, b′, q): compute (a,c,d,s,Q_norm) exactly; the identity Λ_{b′} = diag(a,c)Γ_{d,s} is verified on a full period
(and re-verified by the independent audit on two periods) before the class is assigned.  Because diag(a,c) is a positive diagonal map, Graver vectors,
cells and unions correspond (P3-L1), so U′ = diag(a,c)·U_{d,s,Q_norm} and conv F′ = diag(a,c)·conv F_{d,s,Q_norm}.  Hence hull-coverage of the target is inherited
exactly when G12-T8 applies to (d,s,Q_norm).  No other hypothesis is used; in particular nothing is assumed about the **source** lattice.

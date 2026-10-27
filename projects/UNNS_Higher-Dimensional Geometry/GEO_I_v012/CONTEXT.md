# GEO-I — context handoff after v012 (2026-10-26)

Deliverable of record: `GEO_I_v012.zip`. Frozen: v001–v011 (W2 and universal `r_min=3` preserved), both Mathematical Foundations volumes, the false transfer rules R-MIR/R-EUC/R-LAT (never reuse). Exact arithmetic; memory writes only under the project subtree.

| ID | Statement | Status |
|---|---|---|
| G12-T1 (=G11-A) | `max(y+(d-s)x,(d-t)y+x) >= xy` for Pareto-minimal `M` | PROVED+CHECKED |
| G12-T2 | consecutive boundary steps of `H_Q` are Graver (reflection lemma) | PROVED+CHECKED |
| G12-T3/T4 | one-sided caps (horizontal; vertical by transposition) | PROVED+CHECKED |
| G12-T5/T6/T7 | boundary classification `R*C*T*`, no pentagon, complete mixed cover | PROVED+CHECKED |
| G12-T8 | universal planar stabilization `U = conv F` for all `d,s,Q != (d,d)` | PROVED+CHECKED (hypotheses G5-C1, G7-T1, G10-R1) |
| G11-C1/T1/T2, G10-T2/T3 | resolved by G12-T7/T8 | PROVED+CHECKED |

Proof in five lines: boundary list Omega of `H_Q` from `B` to `A`; reflection ⇒ steps Graver; `H_Q ∩ [0,d]^2 = H_0` (φ-reduction); Omega ∈ `R*C*T*`, no R→T; sweep cells `(−d,0)`, `(0,−d)` along Omega + bottom/left cells (G12-T1) cover `H_Q \ H_0`; closedness ⇒ equality.
Caveats: T8 is conditional on the inherited PROVED+CHECKED results; the proofs are written in MATHEMATICS.md and deserve independent human review; machine checks are instance-level (d≤12 certified, d≤30 sweep, adversarial to d≈400). Not claimed: closure of the broader geometric organisation of the occurrence geometry.
Next (suggestions): independent review of §1–§5; formal-proof transcription; use the Omega/cell structure for the global organisation questions.

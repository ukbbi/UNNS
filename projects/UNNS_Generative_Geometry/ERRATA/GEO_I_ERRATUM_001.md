# Proposed GEO-I erratum 001 — Paper A v1.2, trivial lattice d=1 remark

**Status:** proposed correction in the **separate active GEO-HD workspace**, not yet adopted into any frozen record. **No edits** to Paper A or GitHub.

**Source:** `PAPER_A_manuscript_v1_2/tex/part1.tex`, remark labelled `rem:d1`, paragraph `The case d=1`.

**Affected clause (short excerpt):** “all of H_Q is spanned by coordinate parallelograms, if the box has both sides at least 2”. This is incorrect as a coverage statement under the paper's corner-admissible cell convention.

**Exact counterexample.** Let `x=1296=2^4·3^4`, so `b=1`, `Λ_1=Z²`, and the exponent-coordinate box is `Q=(2,2)` with the origin excluded. Graver directions are `±e_1,±e_2`. Every unit coordinate parallelogram meeting the open square `(0,1)²` has the deleted origin as one corner, so none is admissible. The rational point `(1/2,1/2)` belongs to `conv(F_Q)` but lies in no admissible unit Graver parallelogram.

**Corrected suggested reading:** *For d=1 the relation lattice is rectangular and the Graver directions are coordinate directions. Deleting the origin removes the corner cell adjacent to it, so, even when both box sides are at least 2, the union of corner-admissible coordinate parallelograms need not equal the convex hull. The d=1 case lies outside the stabilization theorem.*

**Generalization (under the explicit coordinate-cubical grammar):** for `k>=2` and integer `Q_i>=1`, `F_Q=([0,Q]∩Z^k)\{0}`, `U_Q={u∈[0,Q]:max_i u_i>=1}`, `H_Q={u∈[0,Q]:sum_i u_i>=1}`. Thus `U_Q⊊H_Q`; `(1/2,1/2,0,...,0)` witnesses the gap. This is an origin-deletion issue already in k=2, not an intrinsically higher-dimensional obstruction.

**Unchanged:** Paper A's stabilization theorem assumes `d>=2`; the remark is outside its hypotheses. The correction does not claim a failure of that theorem or of Paper B.

**Provenance:** supplied Paper A v1.2 `tex/part1.tex`; internal exact verification and scripts in `Scripts/`. This erratum is **not** the existing F.T71 numerical erratum in the Foundations registry.

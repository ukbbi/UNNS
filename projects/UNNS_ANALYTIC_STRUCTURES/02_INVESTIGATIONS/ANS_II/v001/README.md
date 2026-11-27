# ANS-II v001 — Analytic invariance and expansive torsion

**State:** working research notes. Reviewed by the UNNS Research Collective (26 November 2026): proofs valid with the corrections now applied; see THEOREMS.md. No report or manuscript. ANS-I releases unchanged; the extension manuscripts were read, not modified.

## Run
    python ansii_checks.py      (Python 3.8+ with sympy and mpmath; about 30 s)

## Where things stand
- Valuation-type classes are exact scaled copies (control case).
- With finitely many torsion multipliers > 1 and positive drift at every affected prime (automatic for non-negative exponents), the depth, counting and derivative laws hold with exponent sigma_A, the root of B_A = 1 (for derivatives, sigma_A is the infimal Gevrey order; membership at that order is open).
- With negative drift at some prime the abscissa lies strictly below that root.
- The torsion order does not enter the exponent; the multiplier sizes do.
- The class series are comparable. The first-letter identity between classes carries a history-dependent factor; a letter alpha with non-negative exponents appended at the end acts linearly.

Files: PROOFS.md, THEOREMS.md, ansii_checks.py, results/.

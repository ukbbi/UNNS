# FIELD-I v001 — frozen mathematical and verification specification

## Domain

- Inputs `(M,N)` are **positive integers**, with `N>=1`, `M>=1`.
- Nest output `S_N(M) = Fraction(M*(N+1)**2, N)`, using exact rational arithmetic.
- Positive rational output `x=a/b` always denotes lowest terms (`gcd(a,b)=1`).
- *Integer anchor* iff `N | M`; *non-anchor (field)* iff `N ∤ M`, equivalently the output is noninteger.
- *Fixed-nest successor* is `U(M,N)=(M+1,N)`; the next integer anchor in that nest is `(M+N,N)` when starting at an anchor.
- Binary operations are NOT inherited from the original nest definition, and all such operations must be explicitly labelled proposed.

## Investigation gates

### F1 — rational fibres (mathematical)
Derive exact necessary and sufficient conditions on `d=N+1` for an occurrence of `x`, and a bijective inverse. Test independently against brute-force enumeration (not only the generating occurrence). Include denominator, reduction and squarefree edge cases.

### F2 — cross-nest intersections (mathematical)
Derive full rational progression for common outputs of nests `N1,N2`, not merely integer anchors, and verify the earliest common terms and finite-independent intersections.

### F3 — non-anchor structure (mathematical)
Enumerate exact collisions with `b>1` and classify multiplicity by congruence. Never use floats for equality. Counts from finite windows must state their bounds.

### F4 — relational observability (leakage control)
Distinguish recovery through `U`'s increment (equivalent to reading the nest label) from a genuinely derived binary interaction. On multi-route fibres test whether scalar-current-value alone determines a single fixed-nest next value (it does not). Label-recovery alone fails the nontrivial-invariant criterion.

### F5 — operation selection (falsifiable)
Test whether the founding unary rule plus CAI + simultaneous-successor covariance + same-nest agreement selects a unique binary operation. Supply two different explicitly proposed operations respecting all those constraints as a formal nonselection witness. Additional selection would require independently motivated extra rules.

### F6 — reproducibility
- Python 3.10+ stdlib only; deterministic, exact Fraction comparisons.
- Seven test modules plus adversarial independently enumerated cases.
- Reports to `output/` (no overwrite of earlier projects), manifest with SHA-256.
- A failed test causes nonzero exit code; all-pass suite does not imply discovery of a physical mechanism.

## Status vocabulary
- PROVED: full paper proof supplied under stated hypotheses.
- VERIFIED: executed finite tests, with bounded scope.
- PROPOSED: mathematical extension/definition, not original grammar.
- OPEN: no independently selected binary operation, no non-leaky intrinsic relational mechanism.

# Source provenance

The user supplied the v004 research specification, GCD word-intersection identity,
three sequence-conditioned regimes, Fibonacci/Lucas transport rules, and initial
pair totals 94 and 113. This release independently calculates the finite results
and provides self-contained proofs, explicitly separating general substrate
identities from external sequence arithmetic and their joint consequences.

Fibonacci (OEIS A000045), Lucas (A000032), Sylvester (A000058) and powers of two
(A000079) are generated from their stated recurrences. No downloaded dataset is
used. Index choices and cutoffs are recorded before the production comparison.

The arithmetic factorization module is carried forward from SIB-I v001. It uses
trial small factors, Pollard rho and the deterministic unsigned-64-bit Miller-Rabin
base set recorded there. All evaluated values remain below 2^64. The new release
adds memoized unrestricted history counts, word-set kernel calculations, external
index relations, exact permutation expectations and reproducible control samples.

The earlier package hashes are recorded in MANIFEST.json. No earlier release or
GitHub file is changed. All new sequence and transport proofs are supplied in
REGISTER.md so that their use does not depend on uninspected external references.

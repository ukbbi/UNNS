# Provenance

SIB-I v001 is the unchanged prior release, generated in this conversation and
independently reviewed by the user. Its grammar, sequence conventions and
distinction between observation multiplicity and route mergers are retained.

The user supplied the source-6 merger at 4096, its scaling extension and the
claim of first all-depth activation at exponent 12. This release independently
confirms the threshold using forward source-divisor enumeration and backward
square-divisor recursion for every positive target <=4096. Credit for the
proposed extension belongs to the user's supplied research audit.

External sequence definitions are inherited from v001: Lucas A000032, primes
A000040, totient A000010, powers of two A000079, Catalan A000108 and Sylvester
A000058. Data are regenerated from recurrences or elementary formulas; no new
external data are imported. See https://oeis.org/ for the named sequence entries.

Arithmetic proofs use the fixed incoming-fibre identity and homogeneity already
recorded in the UNNS_INDUCED_STRUCTURES baseline. New code uses only Python's
standard library and elementary trial division on this small census.

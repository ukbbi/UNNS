# Source provenance

Definitions were checked against the existing local project README.md,
substrate/ baseline and induction_methods/FORMAL_DEFINITIONS.md on 2026-11-21.
The project identifies FIELD-I F1 for the incoming-fibre formula and SELECT-II
for the integer self-substitution continuation. No prior frozen files were edited.

External sequence identifiers (data generated independently by definitions):

- Lucas: https://oeis.org/A000032 — L0=2, L1=1.
- Primes: https://oeis.org/A000040 — increasing primes, index starts at 1.
- Totient: https://oeis.org/A000010 — index starts at 1.
- Powers of two: https://oeis.org/A000079 — index starts at 0.
- Catalan: https://oeis.org/A000108 — index starts at 0.
- Sylvester: https://oeis.org/A000058 — s0=2.

The user supplied the panel and a reference screenshot. Values are calculated
from exact recurrences/formulas, not transcribed from the screenshot. No external
dataset downloads or fitted observation maps are required. All computations use
Python integers. Factorization uses trial small factors and Pollard rho;
primality uses the deterministic 64-bit Miller-Rabin base set
2,325,9375,28178,450775,9780504,1795265022.
Reference for this bounded deterministic base set: https://miller-rabin.appspot.com/.

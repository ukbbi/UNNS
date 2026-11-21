# Source and provenance — local Phase 3

**Original fixed nesting primitive:** `M ⟂ N=M(N+1)^2/N`; all positive integer pairs allow rational outputs.

**Selected continuation:** SELECT-II integer anchor self-substitution `T_N(x)=(x/N)(N+1)^2`, admissible when `N|x`.

**Immediate frozen local baseline:** FUG-I `v002`; copied source rows appear unchanged as data under `baseline_v002/` (six files). The user's uploaded copies of `summary.json` and `controls_84.json` differ in presentation whitespace from those bundled in v002 but parse to the same JSON data. All other source data files are byte identical to the bundled local v002 results. Nothing in `FUG_I_v001` or `FUG_I_v002` is modified.

**Arithmetic module:** `scripts/arith.py` is a byte-for-byte copy of `FUG_I_v002/scripts/arith.py` and is restricted to integers below `2^64`. Fixed 64-bit Miller–Rabin witnesses, Pollard-rho splitting, prime checks and recombination are used to enumerate exact divisors. `run_p3.py` uses Fraction rational arithmetic for minimal endpoints; the independent verifier reconstructs thresholds by prime valuations.

**Previously established mathematical results:**

- FIELD-I source arithmetic, fibres and nonselection: https://github.com/ukbbi/UNNS/blob/main/projects/UNNS_MATH_FOUNDATIONS/sources/FIELD-I/THEOREMS.md
- SELECT-II selected directed continuation: https://github.com/ukbbi/UNNS/blob/main/projects/UNNS_MATH_FOUNDATIONS/sources/SELECT-II/README.md
- GEO-HD-1 history and integer-kernel relations: https://github.com/ukbbi/UNNS/blob/main/projects/UNNS_Generative_Geometry/GEO_HD_1D_v004/theory/MERGER_KERNEL.md
- Generative geometry reference: https://github.com/ukbbi/UNNS/blob/main/projects/UNNS_Generative_Geometry/DEFINITIONS.md

These are read-only provenance references, not places of active development. Classical Fibonacci strong divisibility is used as an external established number-theoretic identity; this release does not claim it originates in UNNS.

**Status and interpretation:** General threshold and kernel arithmetic already belongs to classical divisibility/previous GEO-HD machinery. The new *FUG-I* result is an explicit F72 merger realization, its proven Fibonacci index-multiple family, and a reproducible finite ancestry/transport census. No inference of universal generativity, physics, or unique Fibonacci exceptionality is made.

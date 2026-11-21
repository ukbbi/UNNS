# SIB-I v002 results

Complete ambient ancestry for every positive integer <=4096. Both algorithms agree at every target.

## Powers of two

First unrestricted-depth different-content common-source merger: 2^12=4096. None exists at 2^k for 0<=k<12. Two witnesses from source 6 have words (6,7,7) and (3,2,3,3). Homogeneity extends these witnesses to every k>=12.

## Arithmetic architecture

The unordered exponent signature determines the incoming COUNT exactly. It does not determine incoming labels, predecessor values, deeper route counts or merger geometry.

289=17^2 and 361=19^2 share exponent signature (2) and bit length 9. Each has one incoming edge; their respective predecessors 16 and 18 have 2 and 1 incoming edges. Thus their exact depth-2 route counts differ.

Of 218 nonempty exponent-signature/bit-length strata, 89 have variable total ancestry counts and 13 have variable different-content pair counts.

## Architecture-matched comparisons

Every target is compared with ALL integers in 1..4096 having the same unordered prime-exponent signature and bit length, excluding the entire observed support of that family. Empty control pools remain missing. Results below use unique values and only covered targets.

| Family | Terms | Unique | Covered unique | Observed mean all-depth routes | Control mean |
|---|---:|---:|---:|---:|---:|
| lucas | 18 | 18 | 14 | 0.2857 | 0.2675 |
| primes | 84 | 84 | 30 | 0.0000 | 0.0000 |
| totient | 84 | 30 | 14 | 0.9286 | 0.6905 |
| powers2 | 13 | 13 | 1 | 0.0000 | 0.0000 |
| catalan | 9 | 8 | 6 | 0.1667 | 0.2292 |
| sylvester | 5 | 5 | 3 | 0.0000 | 0.0000 |

These are exact finite-reference means, not significance tests. Uniform weighting within a pool is a declared reference choice. Different targets may share pools. Binary magnitude matching allows size differences within each bin. Singleton or exhausted strata create a support limitation; no substitute controls are invented. These results cover bounded subsets of the v001 panel and must not be numerically compared as if they used the full v001 samples.

## External order

Order permutations retain all values, all multiplicities and every marginal arithmetic profile. Only successive-index relations change. The following shared-route-word counts compare consecutive observations; equal-value adjacencies can contribute.

| Family | Observed shared-word adjacencies | Mean across 32 permutations |
|---|---:|---:|
| lucas | 0 | 0.3438 |
| primes | 0 | 0.0000 |
| totient | 36 | 38.3125 |
| powers2 | 10 | 8.5625 |
| catalan | 0 | 0.0000 |
| sylvester | 0 | 0.0000 |

See order_controls.csv for equal-value adjacencies, label overlaps, proper divisibility and actual one-step transitions. These are descriptive order checks, not a causal attribution to recurrence mechanisms.

## Interpretation

The square-divisor count is fully explained by the exponent signature. Deeper geometry additionally depends on the arithmetic of d-1 at every backward step. Prime identities therefore matter even after matching exponent patterns. The full prime-labeled factorization fixes x itself, so preserving that entire factorization leaves no distinct integer control. Sequence-specific evidence must concern the distribution or order of values under explicitly declared controls, not a separate ancestry attached to the same integer.

All finite outputs are reproducible with standard Python. No v001 file is changed. See REGISTER.md for the all-depth threshold proof and exact limits.

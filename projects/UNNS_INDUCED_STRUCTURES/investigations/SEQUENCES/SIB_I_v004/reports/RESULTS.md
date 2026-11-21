# SIB-I v004 - Sequence-Conditioned Generative Structure

This investigation returns to four externally generated sequences. It computes complete history-overlap kernels and relations among indexed observations. No integer census is expanded.

## Exact value-preserving permutation expectations

| Sequence | Terms | Active terms | Overlap pairs anywhere | Observed adjacent overlaps | Exact expectation | Decimal |
|---|---:|---:|---:|---:|---:|---:|
| fibonacci | 84 | 18 | 94 | 0 | 47/21 | 2.238095 |
| lucas | 84 | 24 | 113 | 0 | 113/42 | 2.690476 |
| sylvester | 7 | 0 | 0 | 0 | 0 | 0.000000 |
| powers2 | 25 | 23 | 253 | 22 | 506/25 | 20.240000 |

The expectation is 2E/n, where E counts unordered pairs of distinct indexed observations with nonempty shared histories. Every such pair is adjacent with probability 2/n in a uniform linear permutation. Repeated values, if present, retain separate observation identities.

## Recurrence-conditioned laws

Fibonacci and Lucas: adjacent exclusion, with nonadjacent overlap witnesses. Sylvester: global exclusion follows from pairwise coprimality, including future terms regardless of their individual ancestry. Powers of two: nested word sets by increasing exponent. These are exact consequences of external arithmetic relations combined with the unchanged grammar.

The finite Sylvester sample has no active fibres. Its zero kernel is therefore a degenerate finite control comparison; the pairwise-coprimality theorem supplies the all-index exclusion law. The nesting of powers-of-two word sets need not be strict at every index. Inclusion of an empty nonempty-word set is reported separately from nonvacuous inclusion.

## Transport and rewiring

relations.csv distinguishes Fibonacci index-divisibility and Lucas odd-multiple transport from adjacency. It also tests unrestricted index-divisibility for Lucas as an explicit overextension control. rewired_relations.csv relabels observation vertices of these relation graphs, preserving each observation and the relation graph topology while changing which values meet each relation. No conditional rerandomization is performed.

| Sequence / relation | Inclusion edges | All edges | Nonempty-source inclusion | Nonempty-source edges |
|---|---:|---:|---:|---:|
| fibonacci / index_divides | 307 | 307 | 29 | 29 |
| fibonacci / odd_multiple | 139 | 139 | 12 | 12 |
| lucas / index_divides | 270 | 307 | 29 | 66 |
| lucas / odd_multiple | 139 | 139 | 29 | 29 |
| sylvester / all_increasing_indices | 21 | 21 | 0 | 0 |
| powers2 / all_increasing_indices | 300 | 300 | 253 | 253 |

## Alternative grammars

Doubling (s -> 2s) and tripling (s -> 3s) have kernels v_2(gcd) and v_3(gcd). Their word alphabets are separate. The same coprimality exclusions and divisibility inclusions hold in these grammars, so these qualitative regimes are not unique signatures of UNNS. The exported quantitative comparisons test how history multiplicities differ.

## Monte Carlo checks

Two thousand fixed-seed permutations estimate adjacency distributions; 256 vertex relabellings per relation supply rewiring controls. Zero-event frequencies are exploratory Monte Carlo proportions, not exact tail probabilities. Observed exclusion is already entailed by recurrence theorems and is not presented as an unexplained anomaly.

| Sequence | Zero-overlap permutations | Total permutations |
|---|---:|---:|
| fibonacci | 177 | 2000 |
| lucas | 79 | 2000 |
| sylvester | 2000 | 2000 |
| powers2 | 0 | 2000 |

## Relabelled transport controls

The control rate pools nonempty-source edges across 256 independently drawn vertex permutations. This is a descriptive pooled rate, not an independent-edge probability estimate.

| Sequence / relation | Observed nonempty inclusion | Observed nonempty edges | Rewired pooled inclusion rate |
|---|---:|---:|---:|
| fibonacci / index_divides | 29 | 29 | 1230/17306 = 0.071074 |
| lucas / odd_multiple | 29 | 29 | 1081/9620 = 0.112370 |
| powers2 / all_increasing_indices | 253 | 253 | 32919/70714 = 0.465523 |

## Quantitative grammar comparison

Off-diagonal weighted sums count all shared nonempty words across unordered indexed pairs. Alphabets differ between grammars, so these are grammar-relative counts.

| Sequence | UNNS weighted sum | Doubling weighted sum | Tripling weighted sum |
|---|---:|---:|---:|
| fibonacci | 424 | 584 | 232 |
| lucas | 134 | 469 | 232 |
| sylvester | 0 | 0 | 0 |
| powers2 | 145379 | 2300 | 0 |

## Scope

Fibonacci F1..F84; Lucas L1..L84; Sylvester s0..s6; powers 2^0..2^24. The shorter powers sample is declared to keep complete-history arithmetic compact; no equal-sample-size cross-family ranking is made. Totient and Catalan are deferred until a specific external relation is chosen.

See REGISTER.md for the endpoint-divisibility proof of the GCD identity and recurrence-specific transport proofs. overlap.svg displays exact kernels using a common logarithmic color scale, including their diagonal.

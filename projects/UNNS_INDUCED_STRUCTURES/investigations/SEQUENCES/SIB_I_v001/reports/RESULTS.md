# SIB-I v001 results

Exact positive-integer ancestry through depth 3; all sources and intermediate states are ambient integers. No route enumeration cap.

| Sequence | Terms | Unique | Incoming-active | Depth-2 active | Source-locked merger targets | Different-content targets |
|---|---:|---:|---:|---:|---:|---:|
| lucas | 84 | 84 | 23 | 7 | 1 | 0 |
| primes | 84 | 84 | 0 | 0 | 0 | 0 |
| totient | 84 | 30 | 61 | 22 | 6 | 0 |
| powers2 | 60 | 60 | 58 | 56 | 54 | 46 |
| catalan | 30 | 29 | 18 | 8 | 7 | 0 |
| sylvester | 7 | 7 | 0 | 0 | 0 | 0 |

## Activation (external indices)

Indices start at zero except primes and totient, which start at one. Null means absent through depth 3 in this sample.

```json
{
  "lucas": {
    "incoming": 3,
    "depth2": 6,
    "merger_sources": 54,
    "permutation_pairs": 54,
    "different_content_pairs": null
  },
  "primes": {
    "incoming": null,
    "depth2": null,
    "merger_sources": null,
    "permutation_pairs": null,
    "different_content_pairs": null
  },
  "totient": {
    "incoming": 5,
    "depth2": 17,
    "merger_sources": 37,
    "permutation_pairs": 37,
    "different_content_pairs": null
  },
  "powers2": {
    "incoming": 2,
    "depth2": 4,
    "merger_sources": 6,
    "permutation_pairs": 6,
    "different_content_pairs": 14
  },
  "catalan": {
    "incoming": 6,
    "depth2": 13,
    "merger_sources": 13,
    "permutation_pairs": 13,
    "different_content_pairs": null
  },
  "sylvester": {
    "incoming": null,
    "depth2": null,
    "merger_sources": null,
    "permutation_pairs": null,
    "different_content_pairs": null
  }
}
```

## Controls

Eight replicates per randomized control; seed 20261121 + sequence ordinal. Effects are descriptive; no p-values or universal family ranking. Random controls match each term's binary magnitude. Monotone controls sort those same samples. Order scrambles preserve every value and its multiplicity; cyclic shifts preserve cyclic order. Nearby offsets are nonzero integers in [-16,16], clipped to positive integers.

| Sequence | Observed active fraction | Nearby mean | Magnitude-matched mean | Observed mean routes | Magnitude-matched mean routes |
|---|---:|---:|---:|---:|---:|
| lucas | 0.2738 | 0.4033 | 0.3780 | 0.4524 | 1.4643 |
| primes | 0.0000 | 0.3943 | 0.3497 | 0.0000 | 1.0640 |
| totient | 0.7262 | 0.3304 | 0.3676 | 1.3810 | 0.5729 |
| powers2 | 0.9667 | 0.3583 | 0.3625 | 1952.5833 | 2.6646 |
| catalan | 0.6000 | 0.3750 | 0.3125 | 3.4667 | 1.3583 |
| sylvester | 0.0000 | 0.3571 | 0.3214 | 0.0000 | 1.3929 |

## Interpretation and limits

Primes are obstructed at every positive depth by the final-step square-divisor criterion. Sylvester conclusions concern only the seven sampled terms; pairwise coprimality alone does not establish squarefreeness of all terms. Totient multiplicities are reported separately from distinct numerical support and genuine common-source mergers. The powers-of-two incoming fibre has floor(k/2) members at 2^k; its support-restricted graph is two parity chains, while ambient ancestry can branch.

Every nonempty ambient incoming profile has minimal route length 1. A meaningful delayed-activation question must specify a fixed source or a restricted source set. Here depth-2 activation and common-source mergers are bounded-depth diagnostics. Absence of mergers through depth 3 makes no claim about deeper mergers. An infinite different-content merger family at powers of two is proved separately by explicit witnesses and homogeneous scaling; see REGISTER.md SIB-07 and reports/FINDINGS.md. No further infinite-family claim is inferred from finite samples.

Alternative doubling/tripling incoming indicators appear in each sequence report. Transport CSV distinguishes label overlap, inclusion, divisibility and actual consecutive-value transitions. No repeated-label pattern is promoted to a recurrence theorem. All route counts use words with repetition retained; permutation classification uses sorted multisets, not sets.

See REGISTER.md for proofs, README.md for scope, and results/controls.csv for every control replicate.

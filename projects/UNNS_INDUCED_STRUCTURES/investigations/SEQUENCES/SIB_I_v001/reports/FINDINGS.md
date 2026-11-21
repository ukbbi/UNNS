# Main findings

The six-family panel separates arithmetic obstruction, repeated observations,
permutation mergers, and different-content mergers.

The main constructive result is an infinite powers-of-two merger family:

    63 -> 4096 -> 16384       labels (63,1)
    63 -> 576 -> 3072 -> 16384  labels (7,3,3)

Scaling both histories by 2^r preserves all divisibility conditions. Therefore
every 2^k with k>=14 has these two different-content routes from 63*2^(k-14).
This is a direct proof based on a computed witness; see REGISTER.md SIB-07.
The finite search establishes first activation at k=14 only for depths <=3.

Primes have no incoming ancestry at any depth, because a final step requires a
nontrivial square divisor. All seven sampled Sylvester terms also meet this
obstruction; no claim is made for every future Sylvester term.

Lucas has 23 incoming-active terms of 84; only L54 has a common-source merger
in this depth-3 sample. Catalan has 18 active terms of 30 and 7 merger targets.
Neither has a different-content merger within the tested depth and index ranges.

Totient has 61 active observations of 84 but only 17 active distinct values
among 30. Six observations have common-source mergers, representing only two
distinct values. External repetition substantially changes weighted summaries.

Powers of two have the highest mean depth-1..3 route count in this panel:
1952.58 per term versus 2.66 in the eight bit-length-matched control replicates.
Lucas has 0.45 versus 1.46; Catalan 3.47 versus 1.36. These are descriptive
contrasts under the declared controls, with differing sample lengths and sizes.
They establish neither statistical significance nor a universal family ranking.

Verification uses independently generated forward edges for all targets <=512,
all paths through depth 3 in that finite domain, direct replay of all panel routes,
sequence prefix fixtures, factor reconstruction, and exported merger witnesses.

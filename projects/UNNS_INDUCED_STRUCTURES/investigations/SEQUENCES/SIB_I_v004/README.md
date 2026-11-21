# SIB-I v004 — Sequence-Conditioned Generative Structure

This release studies relationships induced when independently generated sequences
are organized through the unchanged integer UNNS continuation. No general integer
census is enlarged. Prior releases remain separate and unchanged.

## Run

Python 3.10 or later, standard library only:

    py -3 scripts\run_sib.py
    py -3 scripts\verify_sib.py

Use python instead of py -3 where appropriate, or RUN_SIB.bat on Windows.
Read reports/RESULTS.md and REGISTER.md. Open reports/overlap.svg in a browser
for the exact kernel visualization; each cell has an index/value tooltip.

## Declared sample

| Sequence | Observations | Reason |
|---|---|---|
| Fibonacci | F1..F84 | Positive-index recurrence panel; F0=0 is outside the positive substrate |
| Lucas | L1..L84 | Same positive-index convention as the user's control calculation |
| Sylvester | s0..s6 | Seven terms within the earlier numeric ceiling |
| Powers of two | 2^0..2^24 | Fixed compact panel with complete, unrestricted-depth histories |

Lucas differs from v001's L0..L83 by the chosen index endpoints. Powers of two
uses a shorter sample than v001. Comparisons do not assume equal sample lengths.
Totient and Catalan are deferred until an external relation is specified.

## Common object

W(x) includes the empty incoming word. K(i,j)=|W(a_i) intersect W(a_j)|-1
counts shared nonempty ordered label words. It discards source identity across
different targets, as appropriate for word transport. At each target, a word
determines one source. This differs from counting common numerical ancestors.

The endpoint-divisibility theorem proves W(x) intersect W(y)=W(gcd(x,y)).
The generator computes K by complete dynamic history counts at pairwise GCDs.
No depth cap or route truncation is used. Only observed values, their pair GCDs
and the predecessors needed for these calculations are evaluated.

## Three evidence layers

1. Substrate-intrinsic: endpoint moduli, GCD intersection, homogeneity.
2. External arithmetic: recurrence coprimality, Sylvester pairwise coprimality,
   Fibonacci divisibility and Lucas odd-multiple divisibility.
3. Joint consequences: exclusion, nested overlap and word transport along the
   independently specified index relations.

These consequences also have analogues under alternative grammars. Their joint
status does not claim they are exclusive to UNNS or unexplained by arithmetic.

## Controls

- Exact uniform-permutation expectation 2E/n for adjacency overlap counts.
- 2000 fixed-seed value-preserving permutations for each family. Observation
  identities, duplicates and every arithmetic fibre remain unchanged.
- 256 uniform vertex relabellings per index relation, retaining its directed
  topology and degree multiset while assigning different values to its endpoints.
  This preserves graph structure, not degrees attached to individual values.
- Doubling and tripling grammars, with separately defined alphabets and exact
  valuation-based overlap kernels, evaluated on the same control permutations.
- Explicit Lucas unrestricted-divisibility failure and nonadjacent overlap witnesses.

Inclusion is tested by K(i,j)=K(i,i). This can hold vacuously when K(i,i)=0;
every relation report supplies nonempty-source denominators and inclusion counts.
Sylvester's finite zero kernel is reported as a degenerate control case.

Seeds: 20261121 plus family ordinal for permutations; 20261221 plus ordinal for
relation relabellings. Family order is Fibonacci, Lucas, Sylvester, powers of two.
Different relation graphs use successive draws from that family's rewiring stream.
No rerandomization conditional on preserving or violating the generating relation.

## Outputs

data/ contains indexed terms. results/ has exact kernel CSVs, complete upper-triangle
pair tables, relation metrics, all permutation/rewiring replicates, counterexamples,
and a factor/count certificate for the evaluated arithmetic nodes. A counterexample
word is shared for overlap witnesses and missing at the destination for transport
failures; the kind column distinguishes these meanings.

The verifier reconstructs explicit word sets from certified factorizations,
checks the GCD identity on every observation pair, checks endpoint moduli and
replays every control with the stored seeds. Small direct-forward fixtures test
the arithmetic implementation independently; these are validation fixtures below
prior census bounds, not a new research census.

All output is UTF-8/LF. Intended location: investigations/SEQUENCES/SIB_I_v004/.

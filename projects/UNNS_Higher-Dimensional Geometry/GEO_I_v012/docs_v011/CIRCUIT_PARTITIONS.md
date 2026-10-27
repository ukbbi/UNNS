# GEO-I v011 — Programme B: circuit partitions (G11-L5, G11-L6, G11-T3)

**Answer: W2 is TRUE.** Every minimal non-embedded binary box has at least two distinct partitions of the all-ones word into exactly two circuits; for `p ≥ 9` it has at least `p − 1` of them. Full proofs: `MATHEMATICS.md` §1.

## Idea in four lines
1. The partitions of `1` into circuits form, modulo `⟨1⟩`, a **vector-space partition** of `F_2^{k−1}` (G11-L5): `V_P = span(blocks)`, `dim = m_P`; every word `≠ 0,1` lies in exactly one `V_P` (rigidity). Two-block partitions are the *points* of this partition.
2. Counting: `Σ_P (2^{m_P} − 2) = 2^k − 2`.
3. Parseval: `Σ_P (2^{m_P} S_P − 2p²) = p(2^k − 2p)` with `S_P` the sum of squared block sizes (second moment of the code).
4. Blocks have size ≥ 2 (G11-L5c), so `m_P ≤ p/2`; Cauchy–Schwarz and `p(2^m/m − 2) ≥ 2^m − 2` (valid for `3 ≤ m ≤ p/2` iff `p ≥ 9`) show that partitions with `m ≥ 3` blocks cannot absorb the Parseval budget unless `n_2 ≥ p − 1`.

## Finite cases
`p ≤ 8`: `k ≤ 7`. `k = 7, p = 8` is the even-weight code `E_8` (not minimal). `k ≤ 6`: inherited classification (G10-T4) **and** a fresh brute-force re-enumeration of every subset of `AG(2,2), AG(3,2), AG(4,2)` (1 / 37 / 19,373 minimal subsets, min `n_2` = 3 / 4 / 8).

## Data (output/data/v11_w2.json)
* all 231 classified minimal classes (k = 3..6): counting identity, Parseval identity, vector-space partition, `n_2 ≥ 2`, `n_2 ≥ p−1` for `p ≥ 9`: 0 violations; minimum `n_2` per `p` in `figures_v11/fig1_w2_inequality.png` (sharp at `p = 16, 32`).
* random minimal boxes: nullity 7 (154 tested), nullity 8 (2 tested): identities + bound, 0 violations (supplementary, not part of the proof).
* threshold lemma checked exactly for `9 ≤ p ≤ 400`; fails at `m=3` for `p = 6,7,8`.
* knapsack/Parseval feasibility (supplementary): no `n_2 ≤ 1` profile numerically possible for `k = 4, 6..12`; `k = 5` admits the numerical profile `p = 6`, which no minimal box realises (brute force).

## Code
`theory/circuit_partitions.py` (circuits, partitions, E1 count DP, minimality, identities, certificate), `experiments/w2_attack.py`, `certificates/checker11.py` (PARTITION).

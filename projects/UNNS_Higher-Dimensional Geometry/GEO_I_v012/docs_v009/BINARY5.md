# GEO-I v009 — Programme C: binary nullity five (G9-C2, G9-T4, G9-T5, G9-Z)

**Status: PROVED+CHECKED** (reduction theorem + exhaustive exact enumeration validated by two independent code paths and an independent orbit count).

## 1. Question
Is `r_min = 3` for every coordinatewise-minimal non-embedded 0/1 box with nullity `ν = dim ker M = 5`? Answer: **yes** (G9-T4), for every length `n` and every parity matrix. The problem is treated as a classification problem over arbitrary `n`, not a finite census: the reduction of minimal boxes to *reduced supports* (B-BASIS, B-SERIES, G9-Z) makes the classification finite.

## 2. Scope: zero columns (G9-Z)
The v008 census used nonzero parity columns only. **G9-Z** (MATHEMATICS §1, `PROVED+CHECKED`): a zero parity column makes `e_i` a codeword; any collision either contains `{i}` in both partitions (and survives deleting `i`), or avoids `i` and yields a collision in the deleted box (by a common-base argument). So zero columns never occur in minimal boxes, and the v008 completeness statements hold unrestricted.

## 3. Classification method
1. `Σ ⊆ F_2^5 \ 0` spanning; the box has code `C = {(u·σ)_σ}` with 32 words. Orbits under `GL(5,2)` (order 9,999,360).
2. Orbit generation (`theory/binary5.py`): grow subsets one point at a time, canonical test by an exact isomorphism search (rarest-invariant basis, pruned by per-point counts of 3- and 4-circuits). Result: orbits of non-empty subsets by size `1,1,2,3,5,9,14,21,34,50,67,91,113,129,145,145,129,…,1,1,1` (palindromic by complementation), total **1371**, **1326** spanning.
3. Independent count: Burnside over all elements of `GL(5,2)` (`tools/burnside5.c`) gives **1372** orbits including `∅`; the same program gives `4, 10, 46` for `k = 2,3,4` (generator: `3, 9, 45` non-empty).
4. For each spanning orbit: embeddedness (shared-centre criterion on the 32 words), all single deletions, all collisions, all witness ranks (exact rational Gaussian elimination). **12 minimal non-embedded orbits**, all `r_min = 3`.
5. Independent path: the v006 stack (`binary_01`, `centre_collisions`, `rank_reduction`) re-classifies all `785` spanning supports with `≤ 16` points (this includes all 12): 0 disagreements. The remaining 541 spanning supports (`> 16` points) are classified (non-minimal) by path 1 only, since the v006 path enumerates `2^p` words; this is reported as a single-path result for those supports. (Every support with `p ≥ 17` is either embedded or has a non-embedded deletion.)
6. Certificates: `certificates/C5_rank5.json`, 12 RANK certificates, accepted by the standalone `checker8.py`.

## 4. The twelve orbits
Support sizes `p`: 8, 9, 10, 10, 11, 11, 12, 12, 13, 14, 15, 16 (`p=16` is `RM(1,4)`, the 16 odd-weight vectors); exact supports in `output/data/v9_binary5.json`. Figure 6 shows the shared-centre collisions by circuit-partition sizes `(r,t)`; Figure 7 the minimum witness rank for **all** `212` non-embedded spanning orbits (minimal or not): always 3.

## 5. Consequences
* G9-T5: every non-embedded box of nullity `≤ 5` has `r_min = 3`; a counterexample to the universal statement (G8-T3) must have nullity `≥ 6`.
* G8-C3 (full support of minimal boxes) is not decided here and was not needed for the classification.
* B-COMMON: each of the 12 minimal boxes has two 2-circuit partitions with a common base whose collision has rank 3 (`output/data/v9_binary5_commonbase.json`, computed with the v008 `common_base_witness`); no rank-4 phenomenon appeared. This extends the v008 observation (n ≤ 9) to nullity 5 for all `n`.

## 6. What is not claimed
Nullity `≥ 6` is untouched; the census would need `GL(6,2)` orbits of subsets of `PG(5,2)` (`2^63` subsets): not attempted. **Rank-4 falsification:** none found; a counterexample would need an exact matrix, proof of non-embeddedness and minimality, complete exclusion of all rank `≤ 3` witnesses, an exact rank-`≥4` witness and independent verification — the RANK checker enforces all of these.

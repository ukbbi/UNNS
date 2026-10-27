# GEO-I v010 — Programme C: binary boxes — criterion, reduction, nullity six

* **G10-E1** (PROVED): non-embedded ⇔ some set has two distinct partitions into circuits. **G10-F1** (PROVED): in a minimal box the set is everything, `1 ∈ C` (this closes the former conjecture G8-C3/FS). **G10-A1** (PROVED): minimal boxes are `AGL(k−1,2)`-classes of spanning subsets of `AG(k−1,2)`. **G10-R** (PROVED): in a minimal box every word except `0,1` has a unique decomposition; `#families = 2^k − 2 + β`. Proofs: `MATHEMATICS.md` §1.
* **G10-T4 (PROVED+CHECKED), nullity six.**

| quantity | nullity 3 | 4 | 5 | 6 |
|---|---|---|---|---|
| non-empty affine orbits (subsets of `AG(k−1,2)`) | 4 | 9 | 31 | 381 |
| spanning | – | – | – | 350 |
| non-embedded | – | – | – | 349 |
| minimal non-embedded classes | 1 | 3 | 12 | **215** |
| minimum witness rank | 3 | 3 | 3 | **3** |

(Burnside counts including `∅`: 5, 10, 32, 382 for `AG(m,2)`, `m = 2..5`.) At nullity 6 all 215 classes have W2; the smallest number of two-circuit partitions of the all-ones word is `16 = 2^{k−2}`; reduced supports have `p = 10..32` points. The nullity 3, 4, 5 results reproduce v008/v009 (1, 3, 12 classes) by the new affine route.
* **Cross-validation.** (a) orbit enumeration: python generator vs. C Burnside program; (b) classification: partition criterion (`binary6.py`) vs. cell/collision engine (`binary5.py`) on all 350 spanning classes, **0 disagreements**; (c) certificates `C6_rank6.json` (215) accepted by `checker10.py`.
* **G10-K** (CHECKED): cut spaces of `K_{2,t}`, `t = 2..10` (unbounded nullity), minimal, rank 3, `2^{t−1}` two-blocks.
* Files: `theory/binary6.py`, `experiments/binary6_attack.py`, `experiments/binary6_crosscheck.py`, `experiments/orbits6.py`, `experiments/k2t_family.py`, `tools/burnside_affine.c`, `output/data/v10_binary*.json`, figures 1–6.
